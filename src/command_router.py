from __future__ import annotations

from datetime import datetime

from src.config import get_config
from src.errors import AppError
from src.normalization.io_cleaner import normalize_command
from src.schemas import TaskRequest, TaskResult, TaskStatus, TaskType, validate_task_request
from src.storage import error_writer, markdown_writer, sqlite_store
from src.tasks import explain_error, rag_search, search, summarize
from src.tasks.common import render_frontmatter


TASK_HANDLERS = {
    TaskType.SUMMARIZE: summarize.run,
    TaskType.SEARCH: search.run,
    TaskType.EXPLAIN_ERROR: explain_error.run,
    TaskType.RAG_SEARCH: rag_search.run,
}


def execute_command(command: str, *, selected_task: str | None = None, input_paths: list[str] | None = None) -> TaskResult:
    config = get_config()
    payload = normalize_command(command, selected_task=selected_task, input_paths=input_paths)
    request = validate_task_request(payload)
    sqlite_store.insert_run(request, model=config.main_model)

    try:
        handler = TASK_HANDLERS[request.task_type]
        result = handler(request)
        result.output_path = markdown_writer.write_markdown(result)
        sqlite_store.finish_run(result)
        sqlite_store.add_artifact(result.run_id, "markdown", result.output_path)
        return result
    except AppError as error:
        result = build_failed_result(request, error)
        result.output_path = markdown_writer.write_markdown(result)
        if request.include_error_file:
            result.error_path = error_writer.write_error(result)
        sqlite_store.finish_run(result)
        sqlite_store.add_artifact(result.run_id, "markdown", result.output_path)
        if result.error_path:
            sqlite_store.add_artifact(result.run_id, "error", result.error_path)
        sqlite_store.add_error(result.run_id, error.code, error.message, error.details)
        return result


def build_failed_result(request: TaskRequest, error: AppError) -> TaskResult:
    config = get_config()
    markdown = render_frontmatter(request, status=TaskStatus.FAILED, model=config.main_model)
    markdown += f"""# 작업 실패

## 안내

{error.message}

## 오류 코드

```txt
{error.code}
```
"""
    return TaskResult(
        run_id=request.run_id,
        task_type=request.task_type,
        status=TaskStatus.FAILED,
        title="작업 실패",
        markdown=markdown,
        model=config.main_model,
        created_at=datetime.now(),
        error_code=error.code,
        error_message=error.message,
        metadata=error.details or {},
    )
