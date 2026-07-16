# Crawler 模块

Python 数据采集服务，从巨潮资讯网抓取上市公司公告，写入 PostgreSQL。

## 执行命令

在项目根目录 `investment-radar/` 执行：

```powershell
# 采集隆基绿能（601012）公告
.\crawler\scripts\run_crawl_announcement.ps1 -StockCode 601012 -CompanyName 隆基绿能
```

```powershell
# 指定日期范围
.\crawler\scripts\run_crawl_announcement.ps1 -StockCode 601012 -CompanyName 隆基绿能 -StartDate 2025-01-01 -EndDate 2026-07-13
```

```powershell
# 直接调用 crawl_announcement.py
cd crawler
.\.venv\Scripts\python crawl_announcement.py --stock-code 601012 --company-name 隆基绿能
```

| 参数 | 说明 |
|------|------|
| `-StockCode` / `--stock-code` | 股票代码（必填） |
| `-CompanyName` / `--company-name` | 公司名称 |
| `-StartDate` / `--start-date` | 开始日期 |
| `-EndDate` / `--end-date` | 结束日期 |
| `-MaxPages` / `--max-pages` | 最大页数 |

完整部署与排错见 [13-Operation-Log.md](13-Operation-Log.md)。

## PDF 下载解析

```text
announcement (pdf_download_status=0)
        │
        ▼
下载 PDF
        │
        ▼
PyMuPDF 解析
        │
        ▼
写入 announcement_content
        │
        ▼
更新 pdf_download_status=1, parse_status=1
```

```powershell
.\crawler\scripts\run_download_parse_pdf.ps1 -CompanyCode 601012 -Limit 10
```

## 目录结构

```text
crawler/
├── crawl_announcement.py / download_parse_pdf.py  # CLI 入口
├── requirements.txt
├── .env.example                # 配置模板（复制为 .env）
├── core/
│   ├── config.py               # 从 .env 加载配置
│   └── database.py             # PostgreSQL 连接
├── scripts/
│   ├── run_crawl_announcement.ps1   # 公告采集
│   ├── run_download_parse_pdf.ps1   # PDF 下载解析
│   ├── init_db.ps1
│   └── init_content_db.ps1
├── spider/
│   └── cninfo_spider.py
├── entity/
├── service/
│   ├── crawl_service.py
│   └── pdf_parse_service.py
├── repository/
├── parser/
│   └── pdf_text_parser.py
└── utils/
    └── pdf_download.py
```

## 分层职责

| 层 | 文件 | 职责 |
|----|------|------|
| 入口 | `crawl_announcement.py` / `scripts/run_crawl_announcement.ps1` | 解析参数，启动采集 |
| 编排 | `service/crawl_service.py` | Spider → Entity → Repository |
| 爬虫 | `spider/cninfo_spider.py` | 请求巨潮接口，返回 JSON |
| 工具 | `utils/orgid_util.py` | 股票代码 → orgId 映射 |
| 工具 | `utils/http_util.py` | HTTP 请求头、重试 |
| 实体 | `entity/announcement.py` | JSON → Entity 转换 |
| 仓储 | `repository/announcement_repository.py` | 写入数据库，去重 |
| 基础 | `core/config.py` / `core/database.py` | 配置与数据库连接 |

## 采集流程

```text
crawl_announcement.py
    │
    ▼
CrawlService
    │
    ▼
CnInfoSpider → 巨潮接口 → JSON
    │
    ▼
Announcement.from_cninfo_json()
    │
    ▼
AnnouncementRepository
    │
    ▼
PostgreSQL (investment_radar.announcement)
```

## 巨潮接口

| 项 | 值 |
|----|-----|
| 地址 | `https://www.cninfo.com.cn/new/hisAnnouncement/query` |
| 方法 | POST |
| stock | `601012,9900022338`（代码,orgId） |
| 分页 | `pageNum` + `pageSize` |
| 日期 | `seDate=2025-01-01~2026-07-13`（可选） |
| orgId 来源 | `szse_stock.json`（含全部 A 股） |
| PDF 域名 | `https://static.cninfo.com.cn/` |

## 数据表

| 表 | 说明 |
|----|------|
| `investment_radar.announcement` | 公告元数据 |
| `investment_radar.announcement_content` | PDF 正文（规划中） |
| `investment_radar.ai_analysis` | AI 分析（规划中） |

## 操作手册

完整部署、运行、排错步骤见 [13-Operation-Log.md](13-Operation-Log.md)。
