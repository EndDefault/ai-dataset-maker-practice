from __future__ import annotations

from collections import OrderedDict

from src.errors import AppError, ErrorCode
from src.rag.chunker import build_chunks
from src.rag.vector_store import lexical_search
from src.schemas import TaskRequest
from src.tasks.common import success_result


def run(request: TaskRequest):
    chunks = build_chunks(request.input_paths)
    if not chunks:
        raise AppError(ErrorCode.MISSING_FILE, "검색할 txt/md/pdf 파일을 찾지 못했습니다.")

    hits = lexical_search(request.query, chunks, limit=8)
    if not hits:
        body = "관련 문단을 찾지 못했습니다. 검색어를 더 구체적으로 입력해 주세요."
        return success_result(request, title="문서 검색", body=body, model="local-search", sources=[])

    grouped_hits: OrderedDict[str, list] = OrderedDict()
    sources = []
    for hit in hits:
        key = str(hit.chunk.path)
        grouped_hits.setdefault(key, []).append(hit)
        sources.append({"path": str(hit.chunk.path), "chunk_index": hit.chunk.index, "score": hit.score})

    sections = [
        f"`{request.query}`에 대한 검색 결과입니다.",
        "",
        "## 검색 결과 요약",
        "",
    ]
    sections.extend(build_summary_table(grouped_hits))
    sections.extend(["", "## 문서별 관련 내용", ""])

    for path, document_hits in grouped_hits.items():
        first_hit = document_hits[0]
        total_score = sum(hit.score for hit in document_hits)
        sections.append(f"### {first_hit.chunk.path.name}")
        sections.append("")
        sections.append(f"관련도 {total_score:.2f} · 발췌 {len(document_hits)}개")
        sections.append("")
        for index, hit in enumerate(document_hits[:3], start=1):
            snippet = readable_excerpt(hit.chunk.content, request.query)
            sections.append(f"**발췌 {index}**")
            sections.append("")
            sections.append(to_blockquote(snippet))
            sections.append("")
        sections.append(f"경로: `{path}`")
        sections.append("")

    return success_result(request, title="문서 검색", body="\n".join(sections), model="local-search", sources=sources)


def build_summary_table(grouped_hits: OrderedDict[str, list]) -> list[str]:
    lines = [
        "| 문서 | 발췌 수 | 관련도 |",
        "| --- | ---: | ---: |",
    ]
    for document_hits in grouped_hits.values():
        first_hit = document_hits[0]
        total_score = sum(hit.score for hit in document_hits)
        lines.append(f"| {first_hit.chunk.path.name} | {len(document_hits)} | {total_score:.2f} |")
    return lines


def readable_excerpt(content: str, query: str, *, max_chars: int = 460) -> str:
    text = normalize_text(content)
    if len(text) <= max_chars:
        return text

    terms = [term.lower() for term in query.split() if term.strip()]
    lowered = text.lower()
    positions = [lowered.find(term) for term in terms if lowered.find(term) >= 0]
    center = min(positions) if positions else 0
    start = max(0, center - max_chars // 3)
    if start < 120:
        start = 0
    elif "\n" in text[:start]:
        start = text.rfind("\n", 0, start) + 1
    end = min(len(text), start + max_chars)
    snippet = text[start:end].strip()
    if start > 0:
        snippet = "... " + snippet
    if end < len(text):
        snippet += " ..."
    return snippet


def normalize_text(content: str) -> str:
    lines = [line.strip() for line in content.replace("\r\n", "\n").split("\n")]
    cleaned = []
    previous_blank = False
    for line in lines:
        if not line:
            if not previous_blank:
                cleaned.append("")
            previous_blank = True
            continue
        cleaned.append(line)
        previous_blank = False
    return "\n".join(cleaned).strip()


def to_blockquote(text: str) -> str:
    return "\n".join(f"> {line}" if line else ">" for line in text.splitlines())
