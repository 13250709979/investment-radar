"""失败重试控制。"""

from __future__ import annotations

from config import AI_MAX_RETRIES


class RetryManager:
    def __init__(self, max_retries: int | None = None):
        self.max_retries = AI_MAX_RETRIES if max_retries is None else max_retries

    def attempts(self) -> int:
        """含首次调用在内的总尝试次数。"""
        return max(1, self.max_retries)

    def should_retry(self, attempt: int) -> bool:
        """attempt 从 1 开始；未达上限则可继续重试。"""
        return attempt < self.attempts()
