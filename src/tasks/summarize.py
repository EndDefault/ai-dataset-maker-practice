from __future__ import annotations

from src.config import get_config
from src.errors import AppError, ErrorCode
from src.rag.chunker import load_documents
from src.schemas import TaskRequest
from src.tasks.common import generate_korean_checked, success_result


def run(request: TaskRequest):
    config = get_config()
    documents = load_documents(request.input_paths)
    if not documents:
        raise AppError(ErrorCode.MISSING_FILE, "요약할 txt/md/pdf 파일을 찾지 못했습니다.")

    combined = "\n\n".join(f"## {doc.path.name}\n{doc.content[:6000]}" for doc in documents[:5])
    prompt = f"""아래 문서를 한국어로 요약해 주세요.

요구사항:
- 사고 과정, 분석 방법, 추론 과정은 쓰지 않습니다.
- 문서에 직접 있는 사실과 수치만 사용합니다.
- 문서에서 확인되지 않는 연도, 정책명, 평가 의견은 만들지 않습니다.
- 핵심 내용 5개 이하
- 중요한 파일명 언급
- 다음 행동이 문서에 직접 있으면 별도 표시
- Markdown으로 간결하게 작성합니다.

문서:
{combined}
"""
    try:
        summary = generate_korean_checked(prompt, model=config.main_model, task_name="문서 요약")
    except AppError as error:
        summary = fallback_summary(combined, error.message)

    sources = [{"path": str(doc.path), "name": doc.path.name} for doc in documents]
    return success_result(request, title="문서 요약", body=summary, model=config.main_model, sources=sources)


def fallback_summary(text: str, reason: str) -> str:
    preview = text.strip().replace("\r\n", "\n")[:1800]
    return f"""Ollama 호출을 사용할 수 없어 간단 요약 모드로 처리했습니다.

원인: {reason}

## 문서 미리보기

{preview}
"""
