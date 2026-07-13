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

建表 SQL：`backend/docs/sql/`