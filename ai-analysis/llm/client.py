"""??????OpenAI Compatible API??"""

from __future__ import annotations

import logging
from dataclasses import dataclass

import requests

from core.config import AI_REQUEST_TIMEOUT, LLM_TEMPERATURE, ModelConfig

logger = logging.getLogger(__name__)

# status -> (????, ?????)?{body}/{provider} ????
_HTTP_ERRORS = {
    401: ("API Key ???401????? .env", False),
    402: ("?????402????={provider}?????????", False),
    403: ("?????403?: {body}", False),
    429: ("???429?: {body}", True),
}


class LLMError(Exception):
    def __init__(self, message: str, *, retryable: bool = True, status_code: int | None = None):
        super().__init__(message)
        self.retryable = retryable
        self.status_code = status_code


@dataclass
class LLMResponse:
    content: str
    input_tokens: int = 0
    output_tokens: int = 0
    total_tokens: int = 0


class LLMClient:
    def __init__(self, model: ModelConfig, temperature: float | None = None, timeout: int | None = None):
        self.model = model
        self.temperature = LLM_TEMPERATURE if temperature is None else temperature
        self.timeout = AI_REQUEST_TIMEOUT if timeout is None else timeout

    @property
    def provider(self) -> str:
        return self.model.provider

    @property
    def model_name(self) -> str:
        return self.model.model_name

    def analyze(self, prompt: str) -> LLMResponse:
        if not self.model.api_key:
            raise LLMError("API_KEY ?????? ai-analysis/.env ???", retryable=False)

        logger.debug("?? LLM: %s / %s", self.provider, self.model_name)
        data = self._post(prompt)
        return self._parse(data)

    def _post(self, prompt: str) -> dict:
        url = f"{self.model.base_url.rstrip('/')}/chat/completions"
        payload = {
            "model": self.model_name,
            "temperature": self.temperature,
            "messages": [{"role": "user", "content": prompt}],
        }
        headers = {
            "Authorization": f"Bearer {self.model.api_key}",
            "Content-Type": "application/json",
        }
        try:
            resp = requests.post(url, json=payload, headers=headers, timeout=self.timeout)
        except requests.RequestException as exc:
            raise LLMError(f"LLM ????: {exc}", retryable=True) from exc

        if resp.status_code >= 400:
            raise self._to_error(resp)
        return resp.json()

    def _parse(self, data: dict) -> LLMResponse:
        try:
            content = data["choices"][0]["message"]["content"] or ""
        except (KeyError, IndexError, TypeError) as exc:
            raise LLMError(f"LLM ??????: {data}", retryable=False) from exc

        usage = data.get("usage") or {}
        inp = int(usage.get("prompt_tokens") or 0)
        out = int(usage.get("completion_tokens") or 0)
        total = int(usage.get("total_tokens") or (inp + out))
        return LLMResponse(content=content, input_tokens=inp, output_tokens=out, total_tokens=total)

    def _to_error(self, resp: requests.Response) -> LLMError:
        status = resp.status_code
        body = (resp.text or "")[:500]
        provider = f"{self.provider}({self.model.id})"

        if status in _HTTP_ERRORS:
            msg, retryable = _HTTP_ERRORS[status]
            return LLMError(msg.format(body=body, provider=provider), retryable=retryable, status_code=status)
        if status >= 500:
            return LLMError(f"??????{status}?: {body}", retryable=True, status_code=status)
        return LLMError(f"LLM ?????{status}?: {body}", retryable=False, status_code=status)
