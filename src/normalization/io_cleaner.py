from __future__ import annotations

from pathlib import Path

from src.schemas import TaskType, new_run_id


TASK_LABELS = {
    "자동 감지": None,
    "문서 요약": TaskType.SUMMARIZE.value,
    "문서 검색": TaskType.SEARCH.value,
    "에러 분석": TaskType.EXPLAIN_ERROR.value,
    "RAG 질의응답": TaskType.RAG_SEARCH.value,
}


def normalize_command(
    command: str,
    *,
    selected_task: str | None = None,
    input_paths: list[str] | None = None,
) -> dict:
    command = command.strip()
    task_type = selected_task or infer_task_type(command)
    return {
        "run_id": new_run_id(),
        "command": command,
        "task_type": task_type,
        "query": command,
        "input_paths": input_paths or [str(Path("uploads"))],
        "output_format": "markdown",
        "include_error_file": True,
    }


def infer_task_type(command: str) -> str:
    lowered = command.lower()
    if any(keyword in command for keyword in ["에러", "오류", "예외", "실패"]) or "error" in lowered:
        return TaskType.EXPLAIN_ERROR.value
    if any(keyword in command for keyword in ["요약", "정리", "summarize"]):
        return TaskType.SUMMARIZE.value
    if any(keyword in command for keyword in ["찾아", "검색", "관련", "어디", "근거"]):
        return TaskType.RAG_SEARCH.value
    return TaskType.SEARCH.value
