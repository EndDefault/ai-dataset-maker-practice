from __future__ import annotations

import json
import socket
from dataclasses import dataclass
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from src.config import AppConfig, get_config
from src.errors import AppError, ErrorCode


@dataclass
class OllamaClient:
    config: AppConfig

    def _post_json(self, path: str, payload: dict) -> dict:
        data = json.dumps(payload).encode("utf-8")
        request = Request(
            f"{self.config.ollama_base_url}{path}",
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urlopen(request, timeout=self.config.llm_timeout_seconds) as response:
                return json.loads(response.read().decode("utf-8"))
        except socket.timeout as exc:
            raise AppError(ErrorCode.LLM_TIMEOUT, "Ollama 응답 시간이 초과됐습니다.") from exc
        except HTTPError as exc:
            message = exc.read().decode("utf-8", errors="ignore")
            if "model" in message.lower() and "not found" in message.lower():
                raise AppError(ErrorCode.MODEL_NOT_FOUND, "Ollama 모델을 찾을 수 없습니다.", {"response": message}) from exc
            raise AppError(ErrorCode.OLLAMA_NOT_RUNNING, "Ollama 호출 중 오류가 발생했습니다.", {"response": message}) from exc
        except URLError as exc:
            raise AppError(ErrorCode.OLLAMA_NOT_RUNNING, "Ollama가 실행 중인지 확인해 주세요.") from exc

    def generate(self, prompt: str, *, model: str | None = None, system: str = "") -> str:
        payload = {
            "model": model or self.config.main_model,
            "prompt": prompt,
            "system": system,
            "stream": False,
        }
        response = self._post_json("/api/generate", payload)
        return str(response.get("response", "")).strip()

    def embed(self, text: str, *, model: str | None = None) -> list[float]:
        model_name = model or self.config.embedding_model
        try:
            response = self._post_json("/api/embed", {"model": model_name, "input": text})
            embeddings = response.get("embeddings") or []
            if embeddings and isinstance(embeddings[0], list):
                return [float(value) for value in embeddings[0]]
        except AppError:
            response = self._post_json("/api/embeddings", {"model": model_name, "prompt": text})
            embedding = response.get("embedding") or []
            return [float(value) for value in embedding]
        return []

    def list_models(self) -> list[str]:
        request = Request(f"{self.config.ollama_base_url}/api/tags", method="GET")
        try:
            with urlopen(request, timeout=5) as response:
                data = json.loads(response.read().decode("utf-8"))
            return [item.get("name", "") for item in data.get("models", []) if item.get("name")]
        except Exception:
            return []


def get_ollama_client() -> OllamaClient:
    return OllamaClient(get_config())
