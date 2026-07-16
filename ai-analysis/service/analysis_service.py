"""分析编排：读取 → Prompt → LLM → 解析 → 落库。"""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass, field

from llm.client import LLMClient, LLMError, LLMResponse
from llm.json_parser import JsonParseError, JsonParser
from llm.prompt import PromptBuilder
from llm.retry import RetryManager
from repository.ai_repository import AiRepository
from repository.announcement_reader import AnnouncementReader

logger = logging.getLogger(__name__)


@dataclass
class BatchResult:
    total: int = 0
    success: int = 0
    failed: int = 0
    errors: list[str] = field(default_factory=list)


class AnalysisService:
    def __init__(
        self,
        llm: LLMClient,
        reader: AnnouncementReader | None = None,
        repository: AiRepository | None = None,
        retry_manager: RetryManager | None = None,
    ):
        self.llm = llm
        self.reader = reader or AnnouncementReader()
        self.repository = repository or AiRepository()
        self.retry = retry_manager or RetryManager()

    def run_batch(self, limit: int | None = None, company_code: str | None = None) -> BatchResult:
        items = self.reader.find_wait_analysis(limit=limit, company_code=company_code)
        result = BatchResult(total=len(items))
        for item in items:
            if self.analyze_one(item):
                result.success += 1
            else:
                result.failed += 1
                result.errors.append(f"id={item.get('id')}")
        return result

    def analyze_one(self, item: dict) -> bool:
        """单条：Prompt → LLM(+重试) → 解析 → 落库。"""
        aid = item.get("id")
        logger.info("开始分析 id=%s model=%s/%s", aid, self.llm.provider, self.llm.model_name)

        prompt = PromptBuilder.build(item)
        version = PromptBuilder.version()
        usage = LLMResponse(content="")
        last_error = "unknown error"

        for attempt in range(1, self.retry.attempts() + 1):
            started = time.perf_counter()
            try:
                # 1) 调模型  2) 解析 JSON  3) 写成功结果
                usage = self.llm.analyze(prompt)
                data = JsonParser.parse(usage.content)
                self._save_ok(item, data, version, usage)
                logger.info("SUCCESS id=%s cost=%.1fs tokens=%s", aid, time.perf_counter() - started, usage.total_tokens)
                return True
            except (JsonParseError, LLMError, Exception) as exc:  # noqa: BLE001
                last_error = str(exc)
                self._log_attempt(aid, attempt, started, exc)
                if isinstance(exc, LLMError) and not exc.retryable:
                    break
                if not self.retry.should_retry(attempt):
                    break

        self._save_fail(item, last_error, version, usage)
        logger.info("FAILED id=%s tokens=%s", aid, usage.total_tokens)
        return False

    def _model_meta(self) -> dict:
        return {"model_provider": self.llm.provider, "model_name": self.llm.model_name}

    def _token_meta(self, usage: LLMResponse) -> dict:
        return {
            "input_tokens": usage.input_tokens,
            "output_tokens": usage.output_tokens,
            "total_tokens": usage.total_tokens,
        }

    def _save_ok(self, item: dict, data: dict, version: str, usage: LLMResponse) -> None:
        self.repository.save_success(
            item, data, prompt_version=version, **self._model_meta(), **self._token_meta(usage)
        )

    def _save_fail(self, item: dict, error: str, version: str, usage: LLMResponse) -> None:
        try:
            self.repository.save_failure(
                item,
                error,
                prompt_version=version,
                update_announcement_status=True,
                **self._model_meta(),
                **self._token_meta(usage),
            )
        except Exception:
            logger.exception("写入失败记录异常 id=%s", item.get("id"))

    def _log_attempt(self, aid, attempt: int, started: float, exc: Exception) -> None:
        cost = time.perf_counter() - started
        total = self.retry.attempts()
        if isinstance(exc, JsonParseError):
            logger.warning("JSON 解析失败 attempt=%s/%s id=%s cost=%.1fs err=%s", attempt, total, aid, cost, exc)
        elif isinstance(exc, LLMError):
            logger.error("LLM 失败 attempt=%s/%s id=%s cost=%.1fs err=%s", attempt, total, aid, cost, exc)
        else:
            logger.exception("分析异常 attempt=%s/%s id=%s cost=%.1fs", attempt, total, aid, cost)
