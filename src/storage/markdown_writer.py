from __future__ import annotations

from datetime import datetime
from pathlib import Path

from src.config import get_config
from src.errors import AppError, ErrorCode
from src.schemas import TaskResult


def build_output_path(task_type: str, run_id: str) -> Path:
    config = get_config()
    now = datetime.now()
    output_dir = config.outputs_dir / now.strftime("%Y-%m-%d")
    output_dir.mkdir(parents=True, exist_ok=True)
    filename = f"{task_type}_{now.strftime('%Y%m%d_%H%M%S')}_{run_id}.md"
    return output_dir / filename


def write_markdown(result: TaskResult) -> Path:
    path = build_output_path(result.task_type.value, result.run_id)
    try:
        path.write_text(result.markdown, encoding="utf-8")
    except OSError as exc:
        raise AppError(ErrorCode.OUTPUT_WRITE_FAILED, "Markdown 결과 저장에 실패했습니다.", {"path": str(path)}) from exc
    return path
