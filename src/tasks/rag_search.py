from __future__ import annotations

import re
from dataclasses import dataclass

from src.config import get_config
from src.errors import AppError, ErrorCode
from src.rag.chunker import build_chunks
from src.rag.vector_store import SearchHit, extract_query_terms, lexical_search, matched_terms, row_to_text_chunk, semantic_search
from src.schemas import TaskRequest
from src.storage.sqlite_store import list_chunks_by_section
from src.tasks.common import generate_korean_checked, success_result


@dataclass
class EvidenceCandidate:
    hit: SearchHit
    section_title: str
    item_title: str
    content: str
    amounts: list[str]
    page_number: int | None = None


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
    hits = select_context_hits(hits, request.input_paths, query_terms, limit=8)
    candidates = build_evidence_candidates(hits)
    context = "\n\n".join(
        format_context_candidate(idx, candidate, query_terms)
        for idx, candidate in enumerate(candidates, start=1)
    )
    if not context:
        raise AppError(ErrorCode.UNKNOWN_COMMAND, "질문과 관련된 문서 근거를 찾지 못했습니다.")

    source_file_names = sorted({candidate.hit.chunk.path.name for candidate in candidates})
    prompt = build_rag_prompt(request.query, context, query_terms, source_file_names)
    try:
        answer = generate_korean_checked(prompt, model=config.main_model, task_name="RAG 질의응답")
    except AppError as error:
        answer = f"""Ollama 호출을 사용할 수 없어 검색 근거만 표시합니다.

원인: {error.message}

## 검색된 근거

{context}
"""
    answer = append_missing_candidate_rows(answer, candidates)
    if vector_error and search_mode == "lexical":
        answer = f"{answer}\n\n---\n\n참고: 벡터 검색을 사용할 수 없어 키워드 검색으로 대체했습니다. 원인: {vector_error}"

    sources = [
        {
            "candidate_id": f"C{index}",
            "path": str(candidate.hit.chunk.path),
            "chunk_index": candidate.hit.chunk.index,
            "score": candidate.hit.score,
            "search_mode": search_mode,
            "matched_terms": matched_terms(candidate.content, query_terms),
            "chunk_type": candidate.hit.chunk.chunk_type,
            "section_title": candidate.section_title,
            "item_title": candidate.item_title,
            "page_number": candidate.page_number,
        }
        for index, candidate in enumerate(candidates, start=1)
    ]
    return success_result(request, title="RAG 질의응답", body=answer, model=config.main_model, sources=sources)


def format_context_candidate(index: int, candidate: EvidenceCandidate, query_terms: list[str]) -> str:
    terms = sorted(
        set(
            matched_terms(candidate.section_title, query_terms)
            + matched_terms(candidate.item_title, query_terms)
            + matched_terms(candidate.content, query_terms)
        )
    )
    terms_text = ", ".join(terms) if terms else "직접 일치 없음"
    amount_text = format_amounts(candidate.amounts)
    excerpt = candidate.content[:1200]
    section_text = candidate.section_title or "없음"
    item_text = candidate.item_title or "없음"
    chunk_type = "section_item" if candidate.item_title else candidate.hit.chunk.chunk_type
    return (
        f"[{index}] {candidate.hit.chunk.path.name} / chunk {candidate.hit.chunk.index}\n"
        f"candidate_id: C{index}\n"
        f"근거 파일명(그대로 사용): {candidate.hit.chunk.path.name}\n"
        f"chunk type: {chunk_type}\n"
        f"section: {section_text}\n"
        f"item: {item_text}\n"
        f"amounts: {amount_text}\n"
        f"질문 키워드 일치: {terms_text}\n"
        f"{excerpt}"
    )


def build_evidence_candidates(hits: list[SearchHit]) -> list[EvidenceCandidate]:
    candidates: list[EvidenceCandidate] = []
    for hit in hits:
        section_items = hit.chunk.metadata.get("items") if hit.chunk.metadata else None
        if isinstance(section_items, list):
            section_candidates = [
                candidate
                for item in section_items
                if (candidate := evidence_candidate_from_item(hit, item)) is not None
            ]
            if section_candidates:
                candidates.extend(section_candidates)
                continue

        candidates.append(
            EvidenceCandidate(
                hit=hit,
                section_title=hit.chunk.section_title,
                item_title=hit.chunk.item_title,
                content=hit.chunk.content,
                amounts=normalize_amounts(hit.chunk.metadata.get("amounts") if hit.chunk.metadata else []),
                page_number=hit.chunk.page_number,
            )
        )
    return candidates


def evidence_candidate_from_item(hit: SearchHit, item) -> EvidenceCandidate | None:
    if not isinstance(item, dict):
        return None
    content = str(item.get("content") or "").strip()
    if not content:
        return None
    return EvidenceCandidate(
        hit=hit,
        section_title=hit.chunk.section_title,
        item_title=str(item.get("title") or "").strip(),
        content=content,
        amounts=normalize_amounts(item.get("amounts")),
        page_number=normalize_page_number(item.get("page_number")),
    )


def normalize_amounts(value) -> list[str]:
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    if value:
        return [str(value).strip()]
    return []


def normalize_page_number(value) -> int | None:
    if value in (None, ""):
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


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
        score = len(title_matches) * 3.0 + len(content_matches) * 0.5 + hit.score
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
    score += len(matched_terms(section_title, query_terms)) * 3.0
    score += len(matched_terms(item_title, query_terms)) * 0.5
    score += len(matched_terms(content, query_terms)) * 0.25
    return score


def build_rag_prompt(query: str, context: str, query_terms: list[str], source_file_names: list[str]) -> str:
    focus_text = ", ".join(query_terms) if query_terms else "질문에 명시된 핵심 주제"
    allowed_files = "\n".join(f"- {name}" for name in source_file_names) if source_file_names else "- 문서에서 확인 안 됨"
    table_instruction = ""
    if wants_table(query):
        table_instruction = """
- 사용자가 표를 요청했으므로 반드시 Markdown 표로 답변합니다.
- 표 컬럼은 `분야 | 예산 항목 | 지원 내용 | 금액 | 근거 파일명 | 근거 chunk`를 사용합니다.
- 문서 근거의 candidate_id 한 줄은 세부 사업 1개입니다.
- `근거 chunk`에는 `C1 / chunk 13`처럼 candidate_id와 chunk 번호를 함께 씁니다.
- 문서 근거에 나온 candidate_id를 한 개도 빠뜨리지 않습니다.
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


def append_missing_candidate_rows(answer: str, candidates: list[EvidenceCandidate]) -> str:
    missing_rows = []
    for index, candidate in enumerate(candidates, start=1):
        candidate_id = f"C{index}"
        if re.search(rf"\b{re.escape(candidate_id)}\b", answer):
            continue
        amount = extract_first_amount(candidate)
        missing_rows.append(
            "| {candidate_id} | {item_title} | {amount} | {file_name} | chunk {chunk_index} |".format(
                candidate_id=candidate_id,
                item_title=candidate.item_title or "문서에서 확인 안 됨",
                amount=amount,
                file_name=candidate.hit.chunk.path.name,
                chunk_index=candidate.hit.chunk.index,
            )
        )
    if not missing_rows:
        return answer

    lines = [
        answer.rstrip(),
        "",
        "## 누락 방지 후보",
        "",
        "| candidate_id | 예산 항목 | 증액 금액 | 근거 파일명 | 근거 chunk |",
        "| --- | --- | --- | --- | --- |",
        *missing_rows,
    ]
    return "\n".join(lines)


def extract_first_amount(candidate: EvidenceCandidate) -> str:
    if candidate.amounts:
        return f"+{candidate.amounts[0]}억원"
    return "문서에서 확인 안 됨"


def format_amounts(amounts: list[str]) -> str:
    if not amounts:
        return "문서에서 확인 안 됨"
    return ", ".join(f"+{amount}억원" for amount in amounts)


def wants_table(query: str) -> bool:
    lowered = query.lower()
    return "표" in lowered or "table" in lowered or "테이블" in lowered
