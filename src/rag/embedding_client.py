from __future__ import annotations

from src.llm.ollama_client import get_ollama_client


def embed_text(text: str, *, model: str | None = None) -> list[float]:
    return get_ollama_client().embed(text, model=model)
