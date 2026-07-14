"""Prompt 构造，禁止在业务代码中拼字符串。"""

from __future__ import annotations

from config import AI_MAX_CONTENT_LENGTH, PROMPT_VERSION

ANNOUNCEMENT_PROMPT_V1 = """你是一名专业投资研究分析师。

请阅读下面上市公司公告。

请严格返回JSON。

禁止返回Markdown。

禁止返回解释。

JSON格式：

{
    "eventType": "",
    "summary": "",
    "importance": 1,
    "sentiment": "",
    "industry": "",
    "company": "",
    "tags": [],
    "reasoning": "",
    "investmentOpinion": "",
    "riskWarning": ""
}

公告标题：

{{title}}

公告正文：

{{content}}
"""


class PromptBuilder:
    VERSION = PROMPT_VERSION

    @classmethod
    def build(cls, item: dict) -> str:
        title = (item.get("title") or "").strip()
        content = (item.get("content") or "").strip()
        if len(content) > AI_MAX_CONTENT_LENGTH:
            content = content[:AI_MAX_CONTENT_LENGTH]

        # 用占位符替换，避免正文中的 {} 触发 format 异常
        return (
            ANNOUNCEMENT_PROMPT_V1
            .replace("{{title}}", title)
            .replace("{{content}}", content)
        )

    @classmethod
    def version(cls) -> str:
        return cls.VERSION
