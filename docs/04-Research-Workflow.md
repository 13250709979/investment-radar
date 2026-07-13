# Workflow

## 整体流程

```text
输入股票
    │
    ▼
创建研究任务（Spring Boot）
    │
    ▼
数据采集（Crawler）          ← 当前阶段
    │
    ▼
AI 分析（Python AI Service）
    │
    ▼
输出研究报告
```

## 研究任务流程

```text
Create task → Async AI → Report
```

详见 [Investment-Radar-Research-MVP.md](../backend/docs/Investment-Radar-Research-MVP.md)。

## 数据采集流程

```text
main.py
    │
    ▼
CnInfoSpider
    │
    ▼
请求巨潮接口
    │
    ▼
返回 JSON
    │
    ▼
转换 Entity
    │
    ▼
AnnouncementRepository
    │
    ▼
PostgreSQL (investment_radar.announcement)
```

详见 [12-Crawler.md](12-Crawler.md)。

## 后续流程（规划中）

```text
announcement（公告元数据）
    │
    ▼
PDF 下载 + 正文解析 → announcement_content
    │
    ▼
AI 分析 → ai_analysis
    │
    ▼
汇总生成 → research_report
```
