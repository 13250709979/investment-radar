# Prompts

AI 分析模块使用的 Prompt 模板。由 `ai-analysis/llm/prompt.py` 统一管理。

当前版本：**v1.0**

---

## 公告分析 Prompt（v1.0）

### 模板

```
你是一名专业投资研究分析师。

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
```

### 变量

| 变量 | 来源 |
|------|------|
| `{{title}}` | `announcement.title` |
| `{{content}}` | `announcement_content.content` |

### 返回字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| `eventType` | string | 事件类型，如扩产、并购、中标、回购、业绩预增 |
| `summary` | string | 公告摘要 |
| `importance` | int | 重要等级 1-5，5 最高 |
| `sentiment` | string | `POSITIVE` / `NEUTRAL` / `NEGATIVE` |
| `industry` | string | 所属行业 |
| `company` | string | 公司名称 |
| `tags` | array | 标签列表 |
| `reasoning` | string | 分析理由 |
| `investmentOpinion` | string | 投资观点 |
| `riskWarning` | string | 风险提示 |

### 版本记录

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.0 | 2026-07-13 | 初始版本，公告分析 |

---

## 设计文档

完整 AI 模块设计见 [05-AI-Service.md](05-AI-Service.md)。
