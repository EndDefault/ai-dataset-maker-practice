from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from uuid import uuid4

from src.errors import AppError, ErrorCode


class TaskType(str, Enum):
    SUMMARIZE = "summarize"
    SEARCH = "search"
    EXPLAIN_ERROR = "explain_error"
    RAG_SEARCH = "rag_search"
    UNKNOWN = "unknown"


class TaskStatus(str, Enum):
    SUCCESS = "success"
    FAILED = "failed"


@dataclass
class TaskRequest:
    run_id: str
    command: str
    task_type: TaskType
    query: str = ""
    input_paths: list[Path] = field(default_factory=list)
    output_format: str = "markdown"
    include_error_file: bool = True
    metadata: dict = field(default_factory=dict)


@dataclass
class TaskResult:
    run_id: str
    task_type: TaskType
    status: TaskStatus
    title: str
    markdown: str
    model: str
    created_at: datetime
    output_path: Path | None = None
    error_code: str | None = None
    error_message: str | None = None
    error_path: Path | None = None
    sources: list[dict] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)


def new_run_id() -> str:
    return uuid4().hex[:8]


def task_type_from_value(value: str | None) -> TaskType:
    if not value:
        return TaskType.UNKNOWN
    normalized = value.strip().lower()
    for task_type in TaskType:
        if task_type.value == normalized:
            return task_type
    return TaskType.UNKNOWN


def validate_task_request(payload: dict) -> TaskRequest:
    command = str(payload.get("command", "")).strip()
    if not command:
        raise AppError(ErrorCode.EMPTY_COMMAND, "명령을 입력해 주세요.")

    task_type = task_type_from_value(str(payload.get("task_type", "")))
    if task_type == TaskType.UNKNOWN:
        raise AppError(ErrorCode.UNKNOWN_COMMAND, "아직 처리할 수 없는 명령입니다.")

    raw_paths = payload.get("input_paths") or []
    input_paths = [Path(path) for path in raw_paths if str(path).strip()]

    return TaskRequest(
        run_id=str(payload.get("run_id") or new_run_id()),
        command=command,
        task_type=task_type,
        query=str(payload.get("query") or command).strip(),
        input_paths=input_paths,
        output_format=str(payload.get("output_format") or "markdown"),
        include_error_file=bool(payload.get("include_error_file", True)),
        metadata=dict(payload.get("metadata") or {}),
    )
