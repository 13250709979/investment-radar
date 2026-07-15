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
        reader: AnnouncementReader | None = None,
        llm: LLMClient | None = None,
        repository: AiRepository | None = None,
        retry_manager: RetryManager | None = None,
    ):
        self.reader = reader or AnnouncementReader()
        self.llm = llm or LLMClient()
        self.repository = repository or AiRepository()
        self.retry_manager = retry_manager or RetryManager()

    def run_batch(
        self,
        limit: int | None = None,
        company_code: str | None = None,
    ) -> BatchResult:
        items = self.reader.find_wait_analysis(limit=limit, company_code=company_code)
        result = BatchResult(total=len(items))

        for item in items:
            ok = self.analyze_one(item)
            if ok:
                result.success += 1
            else:
                result.failed += 1
                result.errors.append(f"id={item.get('id')}")

        return result

    def analyze_one(self, item: dict) -> bool:
        announcement_id = item.get("id")
        logger.info("开始分析")
        logger.info("Announcement ID: %s", announcement_id)
        logger.info("Model: %s (%s)", self.llm.provider, self.llm.model_name)

        prompt = PromptBuilder.build(item)
        prompt_version = PromptBuilder.version()
        last_error = ""
        last_usage = LLMResponse(content="")

        for attempt in range(1, self.retry_manager.attempts() + 1):
            started = time.perf_counter()
            try:
                llm_resp = self.llm.analyze(prompt)
                last_usage = llm_resp
                data = JsonParser.parse(llm_resp.content)
                self.repository.save_success(
                    item,
                    data,
                    model_provider=self.llm.provider,
                    model_name=self.llm.model_name,
                    prompt_version=prompt_version,
                    input_tokens=llm_resp.input_tokens,
                    output_tokens=llm_resp.output_tokens,
                    total_tokens=llm_resp.total_tokens,
                )
                cost = time.perf_counter() - started
                logger.info("Cost: %.1fs", cost)
                logger.info("Tokens: %s", llm_resp.total_tokens)
                logger.info("SUCCESS")
                return True
            except JsonParseError as exc:
                last_error = str(exc)
                cost = time.perf_counter() - started
                logger.warning(
                    "JSON 解析失败 attempt=%s/%s id=%s cost=%.1fs err=%s",
                    attempt,
                    self.retry_manager.attempts(),
                    announcement_id,
                    cost,
                    exc,
                )
            except LLMError as exc:
                last_error = str(exc)
                cost = time.perf_counter() - started
                logger.error(
                    "LLM 调用失败 attempt=%s/%s id=%s cost=%.1fs err=%s",
                    attempt,
                    self.retry_manager.attempts(),
                    announcement_id,
                    cost,
                    exc,
                )
                if not exc.retryable:
                    break
            except Exception as exc:  # noqa: BLE001 - 单条失败不影响批次
                last_error = str(exc)
                cost = time.perf_counter() - started
                logger.exception(
                    "分析异常 attempt=%s/%s id=%s cost=%.1fs",
                    attempt,
                    self.retry_manager.attempts(),
                    announcement_id,
                    cost,
                )

            if not self.retry_manager.should_retry(attempt):
                break

        # 重试超限：写入失败记录，并将 announcement.ai_status=2
        try:
            self.repository.save_failure(
                item,
                last_error or "unknown error",
                model_provider=self.llm.provider,
                model_name=self.llm.model_name,
                prompt_version=prompt_version,
                input_tokens=last_usage.input_tokens,
                output_tokens=last_usage.output_tokens,
                total_tokens=last_usage.total_tokens,
                update_announcement_status=True,
            )
        except Exception:
            logger.exception("写入失败记录异常 id=%s", announcement_id)

        logger.info("Tokens: %s", last_usage.total_tokens)
        logger.info("FAILED")
        return False
