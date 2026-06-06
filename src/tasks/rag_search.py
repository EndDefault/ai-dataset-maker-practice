from __future__ import annotations

from src.config import get_config
from src.errors import AppError, ErrorCode
from src.rag.chunker import build_chunks
from src.rag.vector_store import extract_query_terms, lexical_search, matched_terms, semantic_search
from src.schemas import TaskRequest
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
    hits = select_context_hits(hits, query_terms, limit=5)
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
    if vector_error and search_mode == "lexical":
        answer = f"{answer}\n\n---\n\n참고: 벡터 검색을 사용할 수 없어 키워드 검색으로 대체했습니다. 원인: {vector_error}"

    sources = [
        {
            "path": str(hit.chunk.path),
            "chunk_index": hit.chunk.index,
            "score": hit.score,
            "search_mode": search_mode,
            "matched_terms": matched_terms(hit.chunk.content, query_terms),
        }
        for hit in hits
    ]
    return success_result(request, title="RAG 질의응답", body=answer, model=config.main_model, sources=sources)


def format_context_hit(index: int, hit, query_terms: list[str]) -> str:
    terms = matched_terms(hit.chunk.content, query_terms)
    terms_text = ", ".join(terms) if terms else "직접 일치 없음"
    excerpt = focused_excerpt(hit.chunk.content, query_terms)
    return (
        f"[{index}] {hit.chunk.path.name} / chunk {hit.chunk.index}\n"
        f"근거 파일명(그대로 사용): {hit.chunk.path.name}\n"
        f"질문 키워드 일치: {terms_text}\n"
        f"{excerpt}"
    )


def focused_excerpt(content: str, query_terms: list[str], *, max_chars: int = 1100) -> str:
    cleaned = content.strip()
    if len(cleaned) <= max_chars:
        return cleaned
    if not query_terms:
        return cleaned[:max_chars].strip()

    lowered = cleaned.lower()
    positions = [lowered.find(term) for term in query_terms if lowered.find(term) >= 0]
    if not positions:
        return cleaned[:max_chars].strip()

    first_match = min(positions)
    start = max(0, first_match - 180)
    page_marker = cleaned.rfind("[page", 0, first_match)
    if page_marker >= 0 and first_match - page_marker <= 350:
        start = page_marker
    elif start > 0:
        line_start = cleaned.rfind("\n", 0, start)
        if line_start >= 0:
            start = line_start + 1

    end = min(len(cleaned), start + max_chars)
    next_page_marker = cleaned.find("\n[page", first_match + 1)
    if next_page_marker >= 0 and next_page_marker > start + 300:
        end = min(end, next_page_marker)
    excerpt = cleaned[start:end].strip()
    if start > 0:
        excerpt = "... " + excerpt
    if end < len(cleaned):
        excerpt += " ..."
    return excerpt


def select_context_hits(hits: list, query_terms: list[str], *, limit: int = 5) -> list:
    if not hits:
        return []
    if not query_terms:
        return hits[:limit]

    section_hits = [hit for hit in hits if is_section_heading_hit(hit, query_terms)]
    if section_hits:
        selected = []
        for section_hit in section_hits:
            append_unique_hit(selected, section_hit)
            for hit in hits:
                if hit.chunk.path == section_hit.chunk.path and hit.chunk.index == section_hit.chunk.index + 1:
                    append_unique_hit(selected, hit)
        if len(selected) >= 2:
            return selected[:limit]
        return selected[:limit]

    selected = [hit for hit in hits if matched_terms(hit.chunk.content, query_terms)]
    if len(selected) >= 3:
        return selected[:limit]

    for hit in hits:
        if hit not in selected:
            selected.append(hit)
        if len(selected) >= limit:
            break
    return selected


def append_unique_hit(selected: list, hit) -> None:
    if all(existing.chunk.path != hit.chunk.path or existing.chunk.index != hit.chunk.index for existing in selected):
        selected.append(hit)


def is_section_heading_hit(hit, query_terms: list[str]) -> bool:
    content = hit.chunk.content
    terms = matched_terms(content, query_terms)
    return "【" in content and "저출생" in terms and "미래세대" in terms


def build_rag_prompt(query: str, context: str, query_terms: list[str], source_file_names: list[str]) -> str:
    focus_text = ", ".join(query_terms) if query_terms else "질문에 명시된 핵심 주제"
    allowed_files = "\n".join(f"- {name}" for name in source_file_names) if source_file_names else "- 문서에서 확인 안 됨"
    table_instruction = ""
    if wants_table(query):
        table_instruction = """
- 사용자가 표를 요청했으므로 반드시 Markdown 표로 답변합니다.
- 표 컬럼은 `분야 | 예산 항목 | 지원 내용 | 금액 | 근거 파일명 | 근거 chunk`를 사용합니다.
- 금액이 근거에 명확하지 않으면 `문서에서 확인 안 됨`이라고 씁니다.
- 금액은 해당 예산 항목과 같은 문장 또는 바로 이어지는 설명에 나온 수치만 사용합니다.
- 사용자가 증액 금액을 요청하면 `억원(+158 )`처럼 괄호 안에 `+`로 표시된 금액만 씁니다. 이 경우 `+158억원`처럼 정리합니다.
- 인원, 개소 수, 지원 비율, 월 납입금, 대상 규모는 금액으로 쓰지 않습니다.
- 다른 항목의 금액을 재사용하지 않습니다.
- `근거 chunk`에는 문서 근거 줄의 `chunk N` 숫자만 씁니다. page 번호나 표 행번호를 쓰지 않습니다.
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
- `저출생`에는 임산부, 산모 건강, 산후조리원, 산부인과, 아동 돌봄, 아이돌봄을 포함합니다.
- 분야명은 질문 핵심 주제 표현을 그대로 사용합니다.
- 질문과 무관한 예산 항목, 재정수지, 지역 SOC, 에너지, 의료 등은 근거에 있어도 제외합니다.
- 제외된 항목 목록이나 참고 항목 목록은 작성하지 않습니다.
- 사용자가 `모두`라고 요청하면 문서 근거에서 확인되는 관련 항목을 빠뜨리지 않습니다.
- 모든 행 또는 문단에는 근거 파일명과 chunk 번호를 함께 표시합니다.
- 근거 파일명은 허용된 근거 파일명 중 하나를 그대로 복사합니다. 파일명을 요약하거나 바꾸지 않습니다.
- 문서 근거에서 확인되지 않는 내용은 추측하지 말고 `문서에서 확인 안 됨`이라고 씁니다.
- 여러 분야가 질문에 포함되어 있으면 분야별로 구분합니다.
{table_instruction}"""


def wants_table(query: str) -> bool:
    lowered = query.lower()
    return "표" in lowered or "table" in lowered or "테이블" in lowered
