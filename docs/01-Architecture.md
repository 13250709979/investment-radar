# Architecture

```text
Frontend
  │
  ▼
Spring Boot（任务管理 / API）
  │
  ▼
PostgreSQL ◄── Crawler（公告采集）
  │
  ▼
Python AI Service（分析 / 研报生成）
```

## 模块

| 模块 | 技术 | 说明 |
|------|------|------|
| Frontend | 待开发 | 输入股票、查看任务与报告 |
| Backend | Spring Boot 2.7 | REST API、研究任务管理 |
| Crawler | Python | 巨潮资讯网公告采集，详见 [12-Crawler.md](12-Crawler.md) |
| AI Service | Python | 公告分析、研究报告生成 |
| Database | PostgreSQL 15 | 任务、公告、报告、AI 分析结果 |