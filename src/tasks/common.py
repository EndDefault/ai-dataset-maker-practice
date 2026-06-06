from __future__ import annotations

from datetime import datetime

from src.errors import AppError, ErrorCode
from src.llm.ollama_client import get_ollama_client
from src.schemas import TaskRequest, TaskResult, TaskStatus


def render_frontmatter(request: TaskRequest, *, status: TaskStatus, model: str) -> str:
    return "\n".join(
        [
            "---",
            f"task_type: {request.task_type.value}",
            f"status: {status.value}",
            f"model: {model}",
            f"created_at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"run_id: {request.run_id}",
            "---",
            "",
        ]
    )


def success_result(request: TaskRequest, *, title: str, body: str, model: str, sources: list[dict] | None = None) -> TaskResult:
    body = require_non_empty_body(body, title=title)
    markdown = render_frontmatter(request, status=TaskStatus.SUCCESS, model=model)
    markdown += f"# {title}\n\n{body}\n"
    return TaskResult(
        run_id=request.run_id,
        task_type=request.task_type,
        status=TaskStatus.SUCCESS,
        title=title,
        markdown=markdown,
        model=model,
        created_at=datetime.now(),
        sources=sources or [],
    )


def require_non_empty_body(body: str, *, title: str) -> str:
    cleaned = body.strip()
    if cleaned:
        return cleaned
    raise AppError(ErrorCode.LLM_EMPTY_RESPONSE, f"{title} 결과가 비어 있습니다. 다시 실행해 주세요.")


def generate_korean_checked(prompt: str, *, model: str, task_name: str) -> str:
    client = get_ollama_client()
    answer = client.generate_korean(prompt, model=model)
    if answer.strip():
        return answer.strip()

    retry_prompt = f"""이전 응답이 비어 있었습니다.
아래 요청에 대해 반드시 한국어 Markdown으로 답변해 주세요.
근거가 부족하면 `문서에서 확인 안 됨`이라고 쓰고, 빈 응답은 반환하지 마세요.

요청:
{prompt}
"""
    retry_answer = client.generate_korean(retry_prompt, model=model)
    if retry_answer.strip():
        return retry_answer.strip()

    raise AppError(ErrorCode.LLM_EMPTY_RESPONSE, f"{task_name} 모델 응답이 비어 있습니다.")
