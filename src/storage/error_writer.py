from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from src.config import get_config
from src.schemas import TaskResult


def write_error(result: TaskResult) -> Path:
    config = get_config()
    now = datetime.now()
    output_dir = config.outputs_dir / now.strftime("%Y-%m-%d")
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / f"{result.task_type.value}_{now.strftime('%Y%m%d_%H%M%S')}_{result.run_id}.error.json"
    payload = {
        "run_id": result.run_id,
        "task_type": result.task_type.value,
        "status": result.status.value,
        "error_code": result.error_code,
        "error_message": result.error_message,
        "created_at": result.created_at.isoformat(timespec="seconds"),
        "metadata": result.metadata,
    }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return path
