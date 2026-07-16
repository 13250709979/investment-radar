# Decisions

## D-001：AI 模块与 Crawler 解耦

**决策：** `ai-analysis/` 与 `crawler/` 完全独立，通过数据库衔接。

**原因：**
- 采集和分析可独立部署、独立扩缩
- 分析失败不影响采集
- 后续可接入新闻、政策等不同数据源

**数据衔接：**

```text
crawler → announcement + announcement_content
ai      → 读取上述表 → 写入 ai_analysis
```

---

## D-002：统一 OpenAI Compatible API

**决策：** 所有大模型通过 `llm/client.py` 统一封装，兼容 OpenAI API 格式。

**支持：** OpenAI、DeepSeek、Qwen、Moonshot、Claude（代理）

**配置：** 通过 `.env` 切换，业务代码不修改。

---

## D-003：AI 输出必须为 JSON

**决策：** Prompt 强制要求返回 JSON，禁止 Markdown 和解释性文字。

**解析：** `llm/json_parser.py` 校验，失败不更新 `announcement.ai_status`。

---

## D-004：事务更新顺序

**决策：** 先写 `ai_analysis`，成功后再更新 `announcement.ai_status=1`。

**原因：** 避免状态已更新但分析结果丢失。

---

## D-005：Prompt 版本化管理

**决策：** 数据库记录 `prompt_version`（如 v1.0），支持 Prompt 升级后重新分析历史数据。

**管理：** 模板在 [11-Prompts.md](11-Prompts.md)，代码在 `llm/prompt.py`。

---

## D-006：Schema 统一为 investment_radar

**决策：** 所有表使用 `investment_radar` schema，与 Spring Boot 后端一致。

**注意：** 设计文档中 `investment.` 前缀已统一修正为 `investment_radar.`。
