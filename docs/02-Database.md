# Database

Schema：`investment_radar`

## 研究任务

| 表 | 说明 |
|----|------|
| `research_task` | 研究任务 |
| `company` | 公司基础信息 |
| `research_report` | AI 研究报告 |

## 数据采集

| 表 | 说明 |
|----|------|
| `announcement` | 上市公司公告原始信息（巨潮） |
| `announcement_content` | 公告 PDF 解析正文 |

## AI 分析

| 表 | 说明 |
|----|------|
| `ai_analysis` | AI 分析结果（事件类型、情绪、投资观点等） |

### ai_analysis 关键字段

| 字段 | 说明 |
|------|------|
| `data_type` | 数据来源：`ANNOUNCEMENT` |
| `data_id` | 原始数据 ID（`announcement.id`） |
| `event_type` | 事件类型 |
| `event_level` | 重要等级 1-5 |
| `sentiment` | `POSITIVE` / `NEUTRAL` / `NEGATIVE` |
| `analysis_status` | 1=成功，2=失败 |

### 状态字段

| 表.字段 | 值 | 说明 |
|---------|-----|------|
| `announcement.ai_status` | 0/1/2 | 未分析 / 成功 / 失败 |
| `announcement.pdf_download_status` | 0/1/2 | 未下载 / 已下载 / 失败 |
| `announcement_content.parse_status` | 0/1/2 | 未解析 / 成功 / 失败 |

建表 SQL：`backend/docs/sql/`