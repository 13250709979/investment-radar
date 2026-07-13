# AI 分析模块（V1）

公告 AI 分析服务，独立于 Crawler 模块，读取已解析公告正文，调用大模型分析，结果写入 `ai_analysis`。

---

## 一、目标

完成公告 AI 分析模块，实现：

```text
announcement
        │
        ▼
announcement_content
        │
        ▼
读取待分析数据
        │
        ▼
构造 Prompt
        │
        ▼
调用大模型
        │
        ▼
返回 JSON
        │
        ▼
解析 JSON
        │
        ▼
保存 ai_analysis
        │
        ▼
更新 announcement.ai_status
```

**原则：AI 模块与 Crawler 模块完全解耦。**

---

## 二、目录结构

```text
investment-radar/
│
├── crawler/                    # 数据采集（独立）
│
├── ai/                         # AI 分析（独立）
│   ├── main.py                 # 批量分析入口
│   ├── config.py               # 配置（读取 .env）
│   ├── database.py             # PostgreSQL 连接
│   ├── prompt_builder.py       # Prompt 构造
│   ├── llm_client.py           # 大模型统一封装
│   ├── announcement_reader.py  # 读取待分析公告
│   ├── analysis_service.py     # 分析编排
│   ├── json_parser.py          # JSON 解析与校验
│   ├── ai_repository.py        # 写入 ai_analysis
│   ├── retry_manager.py        # 失败重试
│   ├── requirements.txt
│   └── .env.example            # 配置模板
│
└── .env                        # 实际配置（不入库）
```

---

## 三、执行流程

```text
读取数据库
        │
        ▼
构造 Prompt
        │
        ▼
调用 LLM
        │
        ▼
返回 JSON
        │
        ▼
JSON 解析
        │
        ▼
保存数据库（事务）
        │
        ▼
更新公告状态
```

---

## 四、数据库读取

### 待分析公告查询

一次分析 20 条，完成后继续下一批。

```sql
SELECT
    a.id,
    a.company_code,
    a.company_name,
    a.title,
    c.content
FROM investment_radar.announcement a
JOIN investment_radar.announcement_content c
    ON a.id = c.announcement_id
WHERE
    a.ai_status = 0
    AND c.parse_status = 1
    AND a.deleted = FALSE
ORDER BY a.publish_time DESC
LIMIT 20;
```

| 条件 | 说明 |
|------|------|
| `a.ai_status = 0` | 未分析 |
| `c.parse_status = 1` | PDF 已解析成功 |
| `LIMIT 20` | 单批处理量，可通过 `AI_BATCH_SIZE` 配置 |

**负责模块：** `announcement_reader.py`

---

## 五、Prompt Builder

**文件：** `prompt_builder.py`

**职责：** 将公告标题 + 正文组装为 Prompt，禁止在业务代码中拼字符串。

```text
公告标题 + 公告正文 → Prompt
```

Prompt 模板详见 [11-Prompts.md](11-Prompts.md)，当前版本 **v1.0**。

**要求：**
- 所有 Prompt 统一由此模块管理
- 数据库记录 `prompt_version`，支持历史数据重新分析

---

## 六、LLM Client

**文件：** `llm_client.py`

统一封装所有模型调用，业务代码不直接调 API。

```python
class LLMClient:

    def analyze(self, prompt: str) -> str:
        ...
```

**支持（OpenAI Compatible API）：**

| 提供商 | 说明 |
|--------|------|
| OpenAI | 官方 API |
| DeepSeek | 默认推荐 |
| Qwen | 通义千问 |
| Moonshot | 月之暗面 |
| Claude | OpenAI Compatible 代理 |

切换模型只改 `.env`，业务代码无需修改。

---

## 七、配置文件

**文件：** `ai/.env`（参考 `ai/.env.example`）

```env
# 大模型
MODEL_PROVIDER=DeepSeek
BASE_URL=https://api.deepseek.com/v1
MODEL_NAME=deepseek-chat
API_KEY=xxxxxxxx

# 数据库（与 crawler 共用）
DB_HOST=localhost
DB_PORT=5432
DB_NAME=investment_radar
DB_USER=investment
DB_PASSWORD=123456
DB_SCHEMA=investment_radar

# 分析参数
PROMPT_VERSION=v1.0
AI_BATCH_SIZE=20
AI_MAX_RETRIES=3
AI_MAX_CONTENT_LENGTH=12000
AI_REQUEST_TIMEOUT=120
LLM_TEMPERATURE=0.1
```

**禁止硬编码 API Key 和模型地址。**

---

## 八、Analysis Service

**文件：** `analysis_service.py`

**编排流程：**

```text
读取公告 → 生成 Prompt → 调用 LLM → 返回 JSON
    → JSON 解析 → 保存数据库 → 更新状态
```

**伪代码：**

```python
announcements = reader.find_wait_analysis()

for item in announcements:
    prompt = PromptBuilder.build(item)
    result = llm.analyze(prompt)
    data = JsonParser.parse(result)
    repository.save(data)          # 事务：先写 ai_analysis
    repository.update_status(item.id)  # 再更新 ai_status
```

---

## 九、JSON Parser

**文件：** `json_parser.py`

**原则：不信任 AI 返回，必须校验。**

```python
try:
    json.loads(result)
except:
    # 记录错误，不更新 announcement.ai_status
    ...
```

| 情况 | 处理 |
|------|------|
| 解析成功 | 写入 `ai_analysis`，更新 `ai_status=1` |
| 解析失败 | 记录 `error_message`，**不更新** `announcement.ai_status` |
| 重试超限 | `analysis_status=2` |

---

## 十、AI Repository

**文件：** `ai_repository.py`

| 操作 | 目标 |
|------|------|
| 保存分析结果 | `investment_radar.ai_analysis` |
| 更新公告状态 | `investment_radar.announcement` |

```sql
UPDATE investment_radar.announcement
SET ai_status = 1, update_time = NOW()
WHERE id = ?;
```

**事务要求：** `ai_analysis` 写入成功后再更新 `announcement.ai_status`。

---

## 十一、AI 分析结果字段

写入 `investment_radar.ai_analysis`：

| 字段 | 来源 / 说明 |
|------|-------------|
| `data_type` | 固定 `ANNOUNCEMENT` |
| `data_id` | `announcement.id` |
| `company_code` | 公告股票代码 |
| `company_name` | 公告公司名 |
| `industry` | LLM 返回 `industry` |
| `event_type` | LLM 返回 `eventType` |
| `event_level` | LLM 返回 `importance` |
| `sentiment` | LLM 返回 `sentiment` |
| `confidence` | 可选，后续版本 |
| `title` | 公告原标题 |
| `summary` | LLM 返回 `summary` |
| `reasoning` | LLM 返回 `reasoning` |
| `investment_opinion` | LLM 返回 `investmentOpinion` |
| `risk_warning` | LLM 返回 `riskWarning` |
| `tags` | LLM 返回 `tags`（JSONB） |
| `entities` | 可选，后续版本 |
| `model_provider` | `.env` MODEL_PROVIDER |
| `model_name` | `.env` MODEL_NAME |
| `prompt_version` | `.env` PROMPT_VERSION |
| `input_tokens` | LLM 返回用量 |
| `output_tokens` | LLM 返回用量 |
| `total_tokens` | LLM 返回用量 |
| `analysis_status` | 1=成功，2=失败 |
| `error_message` | 失败原因 |
| `analysis_time` | 分析完成时间 |

### LLM JSON → 数据库字段映射

| LLM 返回字段 | 数据库字段 |
|--------------|------------|
| `eventType` | `event_type` |
| `importance` | `event_level` |
| `sentiment` | `sentiment` |
| `industry` | `industry` |
| `company` | `company_name`（补充） |
| `tags` | `tags` |
| `summary` | `summary` |
| `reasoning` | `reasoning` |
| `investmentOpinion` | `investment_opinion` |
| `riskWarning` | `risk_warning` |

### 公告状态

| 字段 | 值 | 说明 |
|------|-----|------|
| `announcement.ai_status` | 0 | 未分析 |
| | 1 | 分析成功 |
| | 2 | 分析失败 |

---

## 十二、失败处理

**文件：** `retry_manager.py`

| 规则 | 说明 |
|------|------|
| 最大重试 | 3 次（`AI_MAX_RETRIES`） |
| 超限处理 | `analysis_status=2`，记录 `error_message` |
| JSON 解析失败 | 不更新 `announcement.ai_status`，等待下次重试 |
| 事务回滚 | `ai_analysis` 写入失败时不更新公告状态 |

---

## 十三、日志

每条分析记录以下信息：

```text
[INFO] 开始分析
[INFO] Announcement ID: 123456
[INFO] Model: DeepSeek
[INFO] Cost: 3.2s
[INFO] Tokens: 2134
[INFO] SUCCESS / FAILED
```

---

## 十四、Prompt 版本

数据库保存 `prompt_version`：

| 版本 | 说明 |
|------|------|
| v1.0 | 初始公告分析 Prompt |
| v1.1 | 后续优化 |
| v2.0 | 大版本升级 |

升级 Prompt 后可对历史数据重新分析。

---

## 十五、开发顺序

| Task | 模块 | 目标 |
|------|------|------|
| Task1 | `llm_client.py` | 完成模型调用 |
| Task2 | `prompt_builder.py` | 完成 Prompt 生成 |
| Task3 | `announcement_reader.py` | 读取待分析数据 |
| Task4 | `analysis_service.py` | 完成完整流程 |
| Task5 | `json_parser.py` | 完成 JSON 解析 |
| Task6 | `ai_repository.py` | 保存数据库 |
| Task7 | `retry_manager.py` | 失败重试 |
| Task8 | `main.py` | 批量分析入口 |

---

## 十六、端到端数据流

```text
巨潮公告
        │
        ▼
announcement（采集）
        │
        ▼
下载 PDF（crawler）
        │
        ▼
解析 PDF（crawler）
        │
        ▼
announcement_content
        │
        ▼
AI 读取（ai）
        │
        ▼
PromptBuilder
        │
        ▼
LLM
        │
        ▼
JSON
        │
        ▼
JsonParser
        │
        ▼
ai_analysis
        │
        ▼
更新 announcement.ai_status
```

---

## 十七、开发原则

1. AI 模块与 Crawler 模块完全解耦。
2. 所有模型统一使用 OpenAI Compatible API。
3. Prompt 统一由 `PromptBuilder` 管理。
4. 所有 AI 输出必须为 JSON，不允许 Markdown。
5. JSON 解析必须有异常处理。
6. 数据库更新采用事务，确保 `ai_analysis` 写入成功后再更新 `announcement.ai_status`。
7. 所有模型配置通过 `.env` 管理，不允许硬编码。
8. 所有异常必须记录日志，便于排查和重试。
9. 后续支持新闻、政策等数据源时，只需修改 `data_type` 和 `data_id`，无需修改 AI 分析流程。

---

## 相关文档

| 文档 | 说明 |
|------|------|
| [11-Prompts.md](11-Prompts.md) | Prompt 模板 |
| [02-Database.md](02-Database.md) | 数据库表 |
| [04-Research-Workflow.md](04-Research-Workflow.md) | 端到端流程 |
| [13-Operation-Log.md](13-Operation-Log.md) | 操作记录 |
