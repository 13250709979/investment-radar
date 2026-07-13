# Architecture

```text
Frontend
  │
  ▼
Spring Boot（任务管理 / API）
  │
  ▼
PostgreSQL ◄── Crawler（公告采集 + PDF 解析）
  │                AI（公告分析）
  ▼
研究报告生成
```

## 模块

| 模块 | 目录 | 技术 | 说明 |
|------|------|------|------|
| Frontend | 待建 | — | 输入股票、查看任务与报告 |
| Backend | `backend/` | Spring Boot 2.7 | REST API、研究任务管理 |
| Crawler | `crawler/` | Python | 巨潮公告采集 + PDF 解析，详见 [12-Crawler.md](12-Crawler.md) |
| AI Service | `ai/` | Python | 公告 AI 分析，详见 [05-AI-Service.md](05-AI-Service.md) |
| Database | — | PostgreSQL 15 | 任务、公告、报告、AI 分析结果 |

## 模块解耦

```text
crawler/          ai/
   │               │
   ▼               ▼
announcement   读取 content
   +               │
announcement_content  ▼
                   ai_analysis
```

Crawler 与 AI 通过数据库衔接，互不依赖。

## 文档索引

| 文档 | 说明 |
|------|------|
| [12-Crawler.md](12-Crawler.md) | 数据采集 |
| [05-AI-Service.md](05-AI-Service.md) | AI 分析 |
| [11-Prompts.md](11-Prompts.md) | Prompt 模板 |
| [02-Database.md](02-Database.md) | 数据库表 |
