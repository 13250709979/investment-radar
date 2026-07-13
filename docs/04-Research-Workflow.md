# Workflow

## 端到端流程

```text
输入股票
    │
    ▼
创建研究任务（Spring Boot）
    │
    ▼
① 数据采集（Crawler）
    │
    ▼
② PDF 下载解析（Crawler）
    │
    ▼
③ AI 分析（AI Service）          ← 当前阶段
    │
    ▼
④ 输出研究报告
```

---

## ① 公告采集

```text
main.py → CnInfoSpider → 巨潮接口 → JSON
    → Entity → announcement
```

详见 [12-Crawler.md](12-Crawler.md)。

---

## ② PDF 下载解析

```text
announcement (pdf_download_status=0)
    → 下载 PDF → PyMuPDF 解析
    → announcement_content (parse_status=1)
    → 更新 pdf_download_status=1
```

详见 [12-Crawler.md](12-Crawler.md)、[13-Operation-Log.md](13-Operation-Log.md)。

---

## ③ AI 分析

```text
announcement (ai_status=0)
    + announcement_content (parse_status=1)
        │
        ▼
读取待分析数据
        │
        ▼
PromptBuilder → LLM → JSON
        │
        ▼
JsonParser → ai_analysis
        │
        ▼
更新 announcement.ai_status=1
```

详见 [05-AI-Service.md](05-AI-Service.md)。

---

## ④ 研究报告（规划中）

```text
ai_analysis 汇总 → research_report
```

详见 [Investment-Radar-Research-MVP.md](../backend/docs/Investment-Radar-Research-MVP.md)。

---

## 研究任务流程

```text
Create task → Async Worker → Report
```

Worker 后续串联：采集 → PDF 解析 → AI 分析 → 研报生成。
