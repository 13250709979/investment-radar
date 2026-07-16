"""JSON 解析与校验：不信任 AI 返回。"""

from __future__ import annotations

import json
import logging
import re
from typing import Any

logger = logging.getLogger(__name__)

REQUIRED_FIELDS = (
    "eventType",
    "summary",
    "importance",
    "sentiment",
    "industry",
    "company",
    "tags",
    "reasoning",
    "investmentOpinion",
    "riskWarning",
)

VALID_SENTIMENTS = {"POSITIVE", "NEUTRAL", "NEGATIVE"}


class JsonParseError(ValueError):
    pass


class JsonParser:
    @classmethod
    def parse(cls, result: str) -> dict[str, Any]:
        if result is None:
            raise JsonParseError("LLM 返回为空")

        text = result.strip()
        if not text:
            raise JsonParseError("LLM 返回为空字符串")

        raw = cls._extract_json_text(text)
        try:
            data = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise JsonParseError(f"JSON 解析失败: {exc}") from exc

        if not isinstance(data, dict):
            raise JsonParseError(f"期望 JSON 对象，实际为 {type(data).__name__}")

        missing = [f for f in REQUIRED_FIELDS if f not in data]
        if missing:
            raise JsonParseError(f"缺少字段: {', '.join(missing)}")

        importance = data.get("importance")
        try:
            importance_int = int(importance)
        except (TypeError, ValueError) as exc:
            raise JsonParseError(f"importance 非法: {importance}") from exc
        if importance_int < 1 or importance_int > 5:
            raise JsonParseError(f"importance 须在 1-5: {importance_int}")
        data["importance"] = importance_int

        sentiment = str(data.get("sentiment") or "").strip().upper()
        if sentiment not in VALID_SENTIMENTS:
            raise JsonParseError(
                f"sentiment 非法: {data.get('sentiment')}，"
                f"允许值: {', '.join(sorted(VALID_SENTIMENTS))}"
            )
        data["sentiment"] = sentiment

        tags = data.get("tags")
        if tags is None:
            data["tags"] = []
        elif not isinstance(tags, list):
            raise JsonParseError(f"tags 须为数组，实际为 {type(tags).__name__}")

        for key in (
            "eventType",
            "summary",
            "industry",
            "company",
            "reasoning",
            "investmentOpinion",
            "riskWarning",
        ):
            value = data.get(key)
            data[key] = "" if value is None else str(value)

        return data

    @classmethod
    def _extract_json_text(cls, text: str) -> str:
        """剥离可选的 Markdown 代码围栏，再定位 JSON 对象。"""
        fenced = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text, re.IGNORECASE)
        if fenced:
            text = fenced.group(1).strip()

        if text.startswith("{") and text.endswith("}"):
            return text

        start = text.find("{")
        end = text.rfind("}")
        if start >= 0 and end > start:
            return text[start : end + 1]

        raise JsonParseError("未找到 JSON 对象")
