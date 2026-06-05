from __future__ import annotations

from src.config import get_config
from src.errors import AppError, ErrorCode
from src.rag.chunker import build_chunks
from src.rag.vector_store import lexical_search
from src.schemas import TaskRequest
from src.tasks.common import success_result


def run(request: TaskRequest):
    config = get_config()
    chunks = build_chunks(request.input_paths)
    if not chunks:
        raise AppError(ErrorCode.MISSING_FILE, "검색할 txt/md 파일을 찾지 못했습니다.")

    hits = lexical_search(request.query, chunks, limit=8)
    if not hits:
        body = "관련 문단을 찾지 못했습니다. 검색어를 더 구체적으로 입력해 주세요."
        return success_result(request, title="문서 검색", body=body, model="local-search", sources=[])

    lines = []
    sources = []
    for hit in hits:
        snippet = hit.chunk.content[:700].strip()
        lines.append(f"## {hit.chunk.path.name} / chunk {hit.chunk.index}\n\n{snippet}\n\nscore: {hit.score:.2f}\n")
        sources.append({"path": str(hit.chunk.path), "chunk_index": hit.chunk.index, "score": hit.score})
    return success_result(request, title="문서 검색", body="\n".join(lines), model="local-search", sources=sources)
