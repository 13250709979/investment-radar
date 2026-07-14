"""大模型统一封装（OpenAI Compatible API）。"""

from __future__ import annotations

import logging
from dataclasses import dataclass

import requests

from config import (
    AI_REQUEST_TIMEOUT,
    API_KEY,
    BASE_URL,
    LLM_TEMPERATURE,
    MODEL_NAME,
    MODEL_PROVIDER,
)

logger = logging.getLogger(__name__)


@dataclass
class LLMResponse:
    content: str
    input_tokens: int = 0
    output_tokens: int = 0
    total_tokens: int = 0


class LLMClient:
    def __init__(
        self,
        base_url: str | None = None,
        api_key: str | None = None,
        model_name: str | None = None,
        temperature: float | None = None,
        timeout: int | None = None,
    ):
        self.base_url = (base_url or BASE_URL).rstrip("/")
        self.api_key = api_key if api_key is not None else API_KEY
        self.model_name = model_name or MODEL_NAME
        self.temperature = LLM_TEMPERATURE if temperature is None else temperature
        self.timeout = AI_REQUEST_TIMEOUT if timeout is None else timeout
        self.provider = MODEL_PROVIDER

    def analyze(self, prompt: str) -> LLMResponse:
        if not self.api_key:
            raise ValueError("API_KEY 未配置，请在 ai/.env 中设置")

        url = f"{self.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": self.model_name,
            "temperature": self.temperature,
            "messages": [
                {"role": "user", "content": prompt},
            ],
        }

        logger.debug("调用 LLM: provider=%s model=%s", self.provider, self.model_name)
        response = requests.post(url, json=payload, headers=headers, timeout=self.timeout)
        response.raise_for_status()
        data = response.json()

        try:
            content = data["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError) as exc:
            raise ValueError(f"LLM 响应格式异常: {data}") from exc

        usage = data.get("usage") or {}
        input_tokens = int(usage.get("prompt_tokens") or 0)
        output_tokens = int(usage.get("completion_tokens") or 0)
        total_tokens = int(usage.get("total_tokens") or (input_tokens + output_tokens))

        return LLMResponse(
            content=content or "",
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_tokens=total_tokens,
        )
