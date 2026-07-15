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
| AI Service | `ai/` | 公告 AI 分析 |
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

## 公告 AI 分析

在**项目根目录**执行：

```powershell
# 首次：复制环境变量并填写 ACTIVE_MODEL 对应模型的 API_KEY，初始化 ai_analysis 表
Copy-Item .\ai\.env.example .\ai\.env
.\ai\scripts\init_ai_db.ps1

.\ai\run.ps1 -CompanyCode 601012 -Limit 5

# 切换模型（.env 中需先配置对应 MODEL_<ID>_*）
.\ai\run.ps1 -Model deepseek -CompanyCode 601012 -Limit 5
.\ai\run.ps1 -ListModels
```

若已进入 `ai` 目录，则改为：

```powershell
.\run.ps1 -CompanyCode 601012 -Limit 5
```
