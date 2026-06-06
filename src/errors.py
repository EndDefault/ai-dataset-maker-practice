from __future__ import annotations

from dataclasses import dataclass


class ErrorCode:
    EMPTY_COMMAND = "EMPTY_COMMAND"
    UNKNOWN_COMMAND = "UNKNOWN_COMMAND"
    MISSING_FILE = "MISSING_FILE"
    UNSUPPORTED_FILE_TYPE = "UNSUPPORTED_FILE_TYPE"
    FILE_TOO_LARGE = "FILE_TOO_LARGE"
    ENCODING_ERROR = "ENCODING_ERROR"
    OLLAMA_NOT_RUNNING = "OLLAMA_NOT_RUNNING"
    MODEL_NOT_FOUND = "MODEL_NOT_FOUND"
    LLM_TIMEOUT = "LLM_TIMEOUT"
    LLM_EMPTY_RESPONSE = "LLM_EMPTY_RESPONSE"
    OUTPUT_WRITE_FAILED = "OUTPUT_WRITE_FAILED"
    DB_WRITE_FAILED = "DB_WRITE_FAILED"
    VECTOR_INDEX_FAILED = "VECTOR_INDEX_FAILED"


@dataclass
class AppError(Exception):
    code: str
    message: str
    details: dict | None = None

    def __str__(self) -> str:
        return f"{self.code}: {self.message}"
