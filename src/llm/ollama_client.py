from __future__ import annotations

import json
import socket
from dataclasses import dataclass
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from src.config import AppConfig, get_config
from src.errors import AppError, ErrorCode


DEFAULT_SYSTEM_PROMPT = """너는 로컬 파일 작업을 돕는 한국어 AI 비서다.
사용자가 다른 언어를 명시적으로 요청하지 않는 한 모든 답변은 한국어로 작성한다.
문서 원문이 영어여도 요약, 설명, 답변은 자연스러운 한국어로 제공한다.
"""

KOREAN_REWRITE_SYSTEM_PROMPT = """너는 영어 또는 혼합 언어 답변을 한국어로 교정하는 편집자다.
원문의 의미와 Markdown 구조는 유지하고, 설명 문장은 자연스러운 한국어로 다시 작성한다.
파일명, 코드, 명령어, 고유명사는 필요한 경우 그대로 둔다.
"""


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

    def generate(self, prompt: str, *, model: str | None = None, system: str = DEFAULT_SYSTEM_PROMPT) -> str:
        payload = {
            "model": model or self.config.main_model,
            "prompt": prompt,
            "system": system,
            "stream": False,
        }
        response = self._post_json("/api/generate", payload)
        return str(response.get("response", "")).strip()

    def generate_korean(self, prompt: str, *, model: str | None = None, system: str = DEFAULT_SYSTEM_PROMPT) -> str:
        response = self.generate(prompt, model=model, system=system)
        if not should_rewrite_to_korean(response):
            return response

        rewrite_prompt = f"""다음 답변을 한국어 Markdown으로 다시 작성해 주세요.

조건:
- 핵심 내용은 바꾸지 않습니다.
- 파일명, 코드, 명령어, 숫자, 고유명사는 필요한 경우 그대로 둡니다.
- 설명 문장과 제목은 한국어로 작성합니다.

원문 답변:
{response}
"""
        rewritten = self.generate(rewrite_prompt, model=model, system=KOREAN_REWRITE_SYSTEM_PROMPT)
        return rewritten or response

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


def should_rewrite_to_korean(text: str) -> bool:
    stripped = text.strip()
    if len(stripped) < 80:
        return False

    hangul_count = sum(1 for char in stripped if "\uac00" <= char <= "\ud7a3")
    ascii_alpha_count = sum(1 for char in stripped if char.isascii() and char.isalpha())

    if hangul_count >= 20:
        return False
    if ascii_alpha_count < 80:
        return False
    return ascii_alpha_count > max(hangul_count * 6, 120)
