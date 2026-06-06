from __future__ import annotations

from src.config import get_config
from src.errors import AppError, ErrorCode
from src.rag.chunker import build_chunks
from src.rag.vector_store import SearchHit, extract_query_terms, lexical_search, matched_terms, row_to_text_chunk, semantic_search
from src.schemas import TaskRequest
from src.storage.sqlite_store import list_chunks_by_section
from src.tasks.common import generate_korean_checked, success_result


def run(request: TaskRequest):
    config = get_config()
    search_mode = "vector"
    vector_error: str | None = None
    try:
        hits = semantic_search(request.query, request.input_paths, limit=8)
    except AppError as error:
        vector_error = error.message
        hits = []
    except Exception as error:
        vector_error = str(error)
        hits = []

    if not hits:
        search_mode = "lexical"
        chunks = build_chunks(request.input_paths)
        if not chunks:
            raise AppError(ErrorCode.MISSING_FILE, "RAG 검색에 사용할 txt/md/pdf 파일을 찾지 못했습니다.")

        hits = lexical_search(request.query, chunks, limit=8)
        if not hits:
            hits = lexical_search(" ".join(request.query.split()[:3]), chunks, limit=8)

    query_terms = extract_query_terms(request.query)
    hits = select_context_hits(hits, request.input_paths, query_terms, limit=12)
    context = "\n\n".join(
        format_context_hit(idx, hit, query_terms)
        for idx, hit in enumerate(hits, start=1)
    )
    if not context:
        raise AppError(ErrorCode.UNKNOWN_COMMAND, "질문과 관련된 문서 근거를 찾지 못했습니다.")

    source_file_names = sorted({hit.chunk.path.name for hit in hits})
    prompt = build_rag_prompt(request.query, context, query_terms, source_file_names)
    try:
        answer = generate_korean_checked(prompt, model=config.main_model, task_name="RAG 질의응답")
    except AppError as error:
        answer = f"""Ollama 호출을 사용할 수 없어 검색 근거만 표시합니다.

원인: {error.message}

## 검색된 근거

{context}
"""
    answer = append_missing_candidate_rows(answer, hits, request.query)
    if vector_error and search_mode == "lexical":
        answer = f"{answer}\n\n---\n\n참고: 벡터 검색을 사용할 수 없어 키워드 검색으로 대체했습니다. 원인: {vector_error}"

    sources = [
        {
            "path": str(hit.chunk.path),
            "chunk_index": hit.chunk.index,
            "score": hit.score,
            "search_mode": search_mode,
            "matched_terms": matched_terms(hit.chunk.content, query_terms),
            "chunk_type": hit.chunk.chunk_type,
            "section_title": hit.chunk.section_title,
            "item_title": hit.chunk.item_title,
            "page_number": hit.chunk.page_number,
        }
        for hit in hits
    ]
    return success_result(request, title="RAG 질의응답", body=answer, model=config.main_model, sources=sources)


def format_context_hit(index: int, hit, query_terms: list[str]) -> str:
    terms = matched_terms(hit.chunk.content, query_terms)
    terms_text = ", ".join(terms) if terms else "직접 일치 없음"
    excerpt = hit.chunk.content[:1200]
    section_text = hit.chunk.section_title or "없음"
    item_text = hit.chunk.item_title or "없음"
    return (
        f"[{index}] {hit.chunk.path.name} / chunk {hit.chunk.index}\n"
        f"candidate_id: C{index}\n"
        f"근거 파일명(그대로 사용): {hit.chunk.path.name}\n"
        f"chunk type: {hit.chunk.chunk_type}\n"
        f"section: {section_text}\n"
        f"item: {item_text}\n"
        f"질문 키워드 일치: {terms_text}\n"
        f"{excerpt}"
    )


def select_context_hits(hits: list[SearchHit], input_paths, query_terms: list[str], *, limit: int = 8) -> list[SearchHit]:
    if not hits:
        return []
    if not query_terms:
        return hits[:limit]

    section_title = choose_section_title(hits, query_terms)
    if section_title:
        section_rows = list_chunks_by_section(input_paths, section_title)
        section_hits = [SearchHit(chunk=row_to_text_chunk(row), score=hit_score_for_section_row(row, query_terms)) for row in section_rows]
        if section_hits:
            return section_hits[:limit]

    selected = [hit for hit in hits if matched_terms(hit.chunk.content, query_terms)]
    if len(selected) >= 3:
        return selected[:limit]

    for hit in hits:
        if hit not in selected:
            selected.append(hit)
        if len(selected) >= limit:
            break
    return selected


def choose_section_title(hits: list[SearchHit], query_terms: list[str]) -> str:
    candidates: dict[str, float] = {}
    for hit in hits:
        title = hit.chunk.section_title
        if not title:
            continue
        title_matches = matched_terms(title, query_terms)
        content_matches = matched_terms(hit.chunk.content, query_terms)
        score = len(title_matches) * 2.0 + len(content_matches) * 0.5 + hit.score
        if score > candidates.get(title, 0):
            candidates[title] = score
    if not candidates:
        return ""
    return max(candidates, key=candidates.get)


def hit_score_for_section_row(row, query_terms: list[str]) -> float:
    score = 1.0
    section_title = str(row["section_title"] or "")
    item_title = str(row["item_title"] or "")
    content = str(row["content"] or "")
    score += len(matched_terms(section_title, query_terms)) * 2.0
    score += len(matched_terms(item_title, query_terms)) * 0.5
    score += len(matched_terms(content, query_terms)) * 0.25
    return score


def build_rag_prompt(query: str, context: str, query_terms: list[str], source_file_names: list[str]) -> str:
    focus_text = ", ".join(query_terms) if query_terms else "질문에 명시된 핵심 주제"
    allowed_files = "\n".join(f"- {name}" for name in source_file_names) if source_file_names else "- 문서에서 확인 안 됨"
    table_instruction = ""
    if wants_table(query):
        table_columns = "항목 | 핵심 내용 | 근거 파일명 | 근거 chunk"
        numeric_instruction = ""
        if wants_numeric_column(query):
            table_columns = "항목 | 핵심 내용 | 금액/수치 | 근거 파일명 | 근거 chunk"
            numeric_instruction = "\n- 질문이 요구한 금액이나 수치는 같은 근거 안에서 확인되는 값만 씁니다."
        table_instruction = f"""
- 사용자가 표를 요청했으므로 반드시 Markdown 표로 답변합니다.
- 사용자가 컬럼명을 직접 지정하지 않았다면 `{table_columns}`를 기본 컬럼으로 사용합니다.
- `근거 chunk`에는 `C1 / chunk 13`처럼 candidate_id와 chunk 번호를 함께 씁니다.
- 문서 근거에서 확인되지 않는 값은 `문서에서 확인 안 됨`이라고 씁니다.
- 다른 근거의 수치나 표현을 재사용하지 않습니다.
- page 번호나 표 행번호를 근거 chunk로 쓰지 않습니다.
{numeric_instruction}
"""

    return f"""아래 문서 근거만 사용해서 질문에 답해 주세요.

질문:
{query}

질문 핵심 주제:
{focus_text}

문서 근거:
{context}

허용된 근거 파일명:
{allowed_files}

답변 요구사항:
- 한국어로 답변합니다.
- 질문 핵심 주제와 직접 관련된 항목만 포함합니다.
- 질문 핵심 주제 중 하나라도 직접 관련되면 포함합니다. 모든 핵심 주제를 동시에 만족할 필요는 없습니다.
- 사용자가 제외하라고 한 조건은 반드시 제외합니다.
- 제외된 항목 목록이나 참고 항목 목록은 사용자가 요청한 경우에만 작성합니다.
- 사용자가 `모두`라고 요청하면 문서 근거에서 확인되는 관련 항목을 빠뜨리지 않습니다.
- 모든 행 또는 문단에는 근거 파일명과 chunk 번호를 함께 표시합니다.
- 근거 파일명은 허용된 근거 파일명 중 하나를 그대로 복사합니다. 파일명을 요약하거나 바꾸지 않습니다.
- 문서 근거에서 확인되지 않는 내용은 추측하지 말고 `문서에서 확인 안 됨`이라고 씁니다.
- 문서의 종류를 임의로 가정하지 않습니다.
- 사고 과정이나 추론 과정을 쓰지 말고 최종 답변만 작성합니다.
{table_instruction}"""


def append_missing_candidate_rows(answer: str, hits: list[SearchHit], query: str) -> str:
    if not wants_completeness_check(query):
        return answer

    missing_rows = []
    for index, hit in enumerate(hits, start=1):
        candidate_id = f"C{index}"
        if candidate_id in answer:
            continue
        missing_rows.append(
            "| {candidate_id} | {candidate_text} | {file_name} | chunk {chunk_index} |".format(
                candidate_id=candidate_id,
                candidate_text=build_candidate_summary(hit),
                file_name=hit.chunk.path.name,
                chunk_index=hit.chunk.index,
            )
        )
    if not missing_rows:
        return answer

    lines = [
        answer.rstrip(),
        "",
        "## 누락 방지 후보",
        "",
        "| candidate_id | 후보 내용 | 근거 파일명 | 근거 chunk |",
        "| --- | --- | --- | --- |",
        *missing_rows,
    ]
    return "\n".join(lines)


def build_candidate_summary(hit: SearchHit) -> str:
    if hit.chunk.item_title:
        return hit.chunk.item_title
    first_line = next((line.strip() for line in hit.chunk.content.splitlines() if line.strip()), "")
    return first_line[:80] if first_line else "문서에서 확인 안 됨"


def wants_completeness_check(query: str) -> bool:
    return any(keyword in query for keyword in ["모두", "전체", "전부", "빠짐없이", "누락 없이"])


def wants_table(query: str) -> bool:
    lowered = query.lower()
    return "표" in lowered or "table" in lowered or "테이블" in lowered


def wants_numeric_column(query: str) -> bool:
    return any(keyword in query for keyword in ["금액", "비용", "예산", "증액", "수치", "가격", "단가"])
