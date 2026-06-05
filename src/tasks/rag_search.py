from __future__ import annotations

from src.config import get_config
from src.errors import AppError, ErrorCode
from src.llm.ollama_client import get_ollama_client
from src.rag.chunker import build_chunks
from src.rag.vector_store import lexical_search
from src.schemas import TaskRequest
from src.tasks.common import success_result


def run(request: TaskRequest):
    config = get_config()
    chunks = build_chunks(request.input_paths)
    if not chunks:
        raise AppError(ErrorCode.MISSING_FILE, "RAG 검색에 사용할 txt/md 파일을 찾지 못했습니다.")

    hits = lexical_search(request.query, chunks, limit=6)
    if not hits:
        hits = lexical_search(" ".join(request.query.split()[:3]), chunks, limit=6)

    context = "\n\n".join(
        f"[{idx}] {hit.chunk.path.name} / chunk {hit.chunk.index}\n{hit.chunk.content[:1200]}"
        for idx, hit in enumerate(hits, start=1)
    )
    if not context:
        raise AppError(ErrorCode.UNKNOWN_COMMAND, "질문과 관련된 문서 근거를 찾지 못했습니다.")

    prompt = f"""아래 문서 근거만 사용해서 질문에 답해 주세요.

질문:
{request.query}

문서 근거:
{context}

답변 요구사항:
- 한국어로 답변
- 근거 파일명을 함께 표시
- 모르는 내용은 추측하지 말기
"""
    try:
        answer = get_ollama_client().generate(prompt, model=config.main_model)
    except AppError as error:
        answer = f"""Ollama 호출을 사용할 수 없어 검색 근거만 표시합니다.

원인: {error.message}

## 검색된 근거

{context}
"""

    sources = [
        {"path": str(hit.chunk.path), "chunk_index": hit.chunk.index, "score": hit.score}
        for hit in hits
    ]
    return success_result(request, title="RAG 질의응답", body=answer, model=config.main_model, sources=sources)
