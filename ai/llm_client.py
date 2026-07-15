"""大模型统一封装（OpenAI Compatible API）。"""

from __future__ import annotations

import logging
from dataclasses import dataclass

import requests

import config as cfg
from config import ModelConfig

logger = logging.getLogger(__name__)


class LLMError(Exception):
    """LLM 调用失败。"""

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
    def __init__(
        self,
        model: ModelConfig | None = None,
        temperature: float | None = None,
        timeout: int | None = None,
    ):
        if model is None:
            self.model_id = cfg.ACTIVE_MODEL
            self.provider = cfg.MODEL_PROVIDER
            self.base_url = cfg.BASE_URL.rstrip("/")
            self.api_key = cfg.API_KEY
            self.model_name = cfg.MODEL_NAME
        else:
            self.model_id = model.id
            self.provider = model.provider
            self.base_url = model.base_url.rstrip("/")
            self.api_key = model.api_key
            self.model_name = model.model_name
        self.temperature = cfg.LLM_TEMPERATURE if temperature is None else temperature
        self.timeout = cfg.AI_REQUEST_TIMEOUT if timeout is None else timeout

    def analyze(self, prompt: str) -> LLMResponse:
        if not self.api_key:
            raise LLMError(
                "API_KEY 未配置，请在 ai/.env 中设置对应模型的 API_KEY",
                retryable=False,
            )

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

        logger.debug(
            "调用 LLM: id=%s provider=%s model=%s",
            self.model_id,
            self.provider,
            self.model_name,
        )
        try:
            response = requests.post(
                url, json=payload, headers=headers, timeout=self.timeout
            )
        except requests.RequestException as exc:
            raise LLMError(f"LLM 网络异常: {exc}", retryable=True) from exc

        if response.status_code >= 400:
            raise self._http_error(response)

        data = response.json()

        try:
            content = data["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError) as exc:
            raise LLMError(f"LLM 响应格式异常: {data}", retryable=False) from exc

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

    def _http_error(self, response: requests.Response) -> LLMError:
        status = response.status_code
        body = (response.text or "")[:500]
        if status == 401:
            return LLMError(
                "API Key 无效或未授权（401）。请检查 ai/.env 中对应模型的 API_KEY。",
                retryable=False,
                status_code=status,
            )
        if status == 402:
            return LLMError(
                "大模型账户余额不足或未开通付费（402 Payment Required）。"
                f"当前提供商={self.provider}（id={self.model_id}）。请到对应平台充值，"
                "或切换 ACTIVE_MODEL / --model 到其他有余量的模型。",
                retryable=False,
                status_code=status,
            )
        if status == 403:
            return LLMError(
                f"API 拒绝访问（403）。请检查账号权限与 API_KEY。详情: {body}",
                retryable=False,
                status_code=status,
            )
        if status == 429:
            return LLMError(
                f"请求过于频繁被限流（429），稍后可重试。详情: {body}",
                retryable=True,
                status_code=status,
            )
        if status >= 500:
            return LLMError(
                f"模型服务端错误（{status}），可重试。详情: {body}",
                retryable=True,
                status_code=status,
            )
        return LLMError(
            f"LLM 请求失败（{status}）: {body}",
            retryable=False,
            status_code=status,
        )
