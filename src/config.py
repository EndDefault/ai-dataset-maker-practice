from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class AppConfig:
    root_dir: Path = ROOT_DIR
    data_dir: Path = ROOT_DIR / "data"
    uploads_dir: Path = ROOT_DIR / "uploads"
    outputs_dir: Path = ROOT_DIR / "outputs"
    db_path: Path = ROOT_DIR / "data" / "app.db"
    ollama_base_url: str = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
    main_model: str = os.getenv("OLLAMA_MAIN_MODEL", "qwen3:14b")
    cleaner_model: str = os.getenv("OLLAMA_CLEANER_MODEL", "qwen3:4b")
    embedding_model: str = os.getenv("OLLAMA_EMBEDDING_MODEL", "bge-m3")
    llm_timeout_seconds: int = int(os.getenv("OLLAMA_TIMEOUT_SECONDS", "90"))


def get_config() -> AppConfig:
    config = AppConfig()
    ensure_directories(config)
    return config


def ensure_directories(config: AppConfig | None = None) -> None:
    config = config or AppConfig()
    config.data_dir.mkdir(parents=True, exist_ok=True)
    config.uploads_dir.mkdir(parents=True, exist_ok=True)
    config.outputs_dir.mkdir(parents=True, exist_ok=True)
