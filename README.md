# Investment Radar

AI 投资研究系统

## MVP

```text
输入股票 → 自动收集数据 → AI 分析 → 输出研究报告
```

## 知识库

| 文档 | 说明 |
|------|------|
| [01-Architecture.md](docs/01-Architecture.md) | 系统架构 |
| [02-Database.md](docs/02-Database.md) | 数据库表 |
| [04-Research-Workflow.md](docs/04-Research-Workflow.md) | 业务流程 |
| [05-AI-Service.md](docs/05-AI-Service.md) | AI 分析模块设计（V1） |
| [11-Prompts.md](docs/11-Prompts.md) | Prompt 模板 |
| [12-Crawler.md](docs/12-Crawler.md) | 数据采集（巨潮公告爬虫） |
| [13-Operation-Log.md](docs/13-Operation-Log.md) | 操作记录（部署 / 运行 / 排错） |

## 模块

| 模块 | 目录 | 状态 |
|------|------|------|
| Backend | `backend/` | Spring Boot API |
| Crawler | `crawler/` | 巨潮公告采集 + PDF 解析 |
| AI Service | `ai/` | 公告 AI 分析（开发中） |
| Frontend | 待建 | Web 界面 |

## 采集公告（快速执行）

```powershell
.\crawler\run.ps1 -StockCode 601012 -CompanyName 隆基绿能
```

详见 [13-Operation-Log.md](docs/13-Operation-Log.md)。

## PDF 下载解析

```powershell
.\crawler\run_pdf.ps1 -CompanyCode 601012 -Limit 10
```
