from __future__ import annotations

from src.errors import AppError, ErrorCode
from src.rag.chunker import build_chunks
from src.rag.vector_store import lexical_search
from src.schemas import TaskRequest
from src.tasks.common import success_result


def run(request: TaskRequest):
    chunks = build_chunks(request.input_paths)
    if not chunks:
        raise AppError(ErrorCode.MISSING_FILE, "검색할 txt/md 파일을 찾지 못했습니다.")

    hits = lexical_search(request.query, chunks, limit=8)
    if not hits:
        body = "관련 문단을 찾지 못했습니다. 검색어를 더 구체적으로 입력해 주세요."
        return success_result(request, title="문서 검색", body=body, model="local-search", sources=[])

    grouped_hits: dict[str, list] = {}
    sources = []
    for hit in hits:
        key = str(hit.chunk.path)
        grouped_hits.setdefault(key, []).append(hit)
        sources.append({"path": str(hit.chunk.path), "chunk_index": hit.chunk.index, "score": hit.score})

    sections = [
        f"검색어: `{request.query}`",
        "",
        "아래 문서에서 관련 내용을 찾았습니다.",
        "",
    ]
    for path, document_hits in grouped_hits.items():
        first_hit = document_hits[0]
        total_score = sum(hit.score for hit in document_hits)
        sections.append(f"## {first_hit.chunk.path.name}")
        sections.append("")
        sections.append(f"- 관련도 점수: {total_score:.2f}")
        sections.append(f"- 관련 내용 수: {len(document_hits)}")
        sections.append("")
        for index, hit in enumerate(document_hits[:3], start=1):
            snippet = compact_snippet(hit.chunk.content, request.query)
            sections.append(f"### 관련 내용 {index}")
            sections.append("")
            sections.append(snippet)
            sections.append("")
        sections.append(f"파일 경로: `{path}`")
        sections.append("")

    return success_result(request, title="문서 검색", body="\n".join(sections), model="local-search", sources=sources)


def compact_snippet(content: str, query: str, *, max_chars: int = 520) -> str:
    text = " ".join(content.strip().split())
    if len(text) <= max_chars:
        return text

    terms = [term.lower() for term in query.split() if term.strip()]
    lowered = text.lower()
    positions = [lowered.find(term) for term in terms if lowered.find(term) >= 0]
    center = min(positions) if positions else 0
    start = max(0, center - max_chars // 3)
    end = min(len(text), start + max_chars)
    snippet = text[start:end].strip()
    if start > 0:
        snippet = "... " + snippet
    if end < len(text):
        snippet += " ..."
    return snippet
