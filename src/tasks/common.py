from __future__ import annotations

from datetime import datetime

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
    markdown = render_frontmatter(request, status=TaskStatus.SUCCESS, model=model)
    markdown += f"# {title}\n\n{body.strip()}\n"
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
