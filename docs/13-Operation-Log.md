# 操作记录

Investment Radar 项目操作手册与开发记录。

---

## 快速执行（采集公告）

> 在项目根目录 `investment-radar/` 下执行。

### 采集命令

```powershell
# 推荐：一键脚本
.\crawler\run.ps1 -StockCode 601012 -CompanyName 隆基绿能
```

```powershell
# 等价：直接调用 Python
cd crawler
.\.venv\Scripts\python main.py --stock-code 601012 --company-name 隆基绿能
```

### 带日期范围

```powershell
.\crawler\run.ps1 -StockCode 601012 -CompanyName 隆基绿能 -StartDate 2025-01-01 -EndDate 2026-07-13
```

### 测试（只抓 1 页）

```powershell
.\crawler\run.ps1 -StockCode 601012 -CompanyName 隆基绿能 -MaxPages 1
```

### PDF 下载解析

```powershell
# 建 announcement_content 表（首次）
.\crawler\scripts\init_content_db.ps1

# 下载并解析 PDF（处理 pdf_download_status=0 的记录）
.\crawler\run_pdf.ps1 -CompanyCode 601012 -Limit 10
```

```powershell
# 等价命令
cd crawler
.\.venv\Scripts\python main_pdf.py --company-code 601012 --limit 10
```

### 首次运行前（只需一次）

```powershell
docker start postgres
.\crawler\scripts\init_db.ps1
cd crawler
python -m venv .venv
.\.venv\Scripts\pip install -r requirements.txt
```

---

## 一、公告采集（Crawler）

### 1.1 环境要求

| 项 | 要求 |
|----|------|
| Python | 3.11+ |
| PostgreSQL | Docker 容器 `postgres` 已启动 |
| 数据库 | `investment_radar` |
| Schema | `investment_radar` |
| 网络 | 可访问 `www.cninfo.com.cn` |

### 1.2 首次部署

```powershell
# 1. 启动 PostgreSQL（如未启动）
docker start postgres

# 2. 建 announcement 表
.\crawler\scripts\init_db.ps1

# 3. 安装 Python 依赖
cd crawler
python -m venv .venv
.\.venv\Scripts\pip install -r requirements.txt
```

### 1.3 运行采集

**方式 A：一键脚本（推荐）**

```powershell
cd crawler
.\run.ps1 -StockCode 601012 -CompanyName 隆基绿能
```

**方式 B：直接调用 main.py**

```powershell
cd crawler
.\.venv\Scripts\python main.py --stock-code 601012 --company-name 隆基绿能
```

**常用参数**

| 参数 | 说明 | 示例 |
|------|------|------|
| `--stock-code` | 股票代码（必填） | `601012` |
| `--company-name` | 公司名称 | `隆基绿能` |
| `--start-date` | 开始日期 | `2025-01-01` |
| `--end-date` | 结束日期 | `2026-07-13` |
| `--max-pages` | 限制抓取页数 | `1` |
| `--verbose` | 调试日志 | — |

**限制只抓 1 页（测试用）**

```powershell
.\run.ps1 -StockCode 601012 -CompanyName 隆基绿能 -MaxPages 1
```

### 1.4 验证数据

```powershell
docker exec -it postgres psql -U postgres -d investment_radar -c "SELECT COUNT(*) FROM investment_radar.announcement;"
```

```powershell
docker exec -it postgres psql -U postgres -d investment_radar -c "SELECT company_code, title, publish_time FROM investment_radar.announcement ORDER BY publish_time DESC LIMIT 5;"
```

**预期输出示例**

```text
==================================================
股票代码 : 601012
公司名称 : 隆基绿能
抓取数量 : 30
新增入库 : 30
重复跳过 : 0
库内总数 : 30
==================================================
```

### 1.5 采集脚本结构

```text
crawler/
├── main.py                         # 公告采集入口
├── main_pdf.py                     # PDF 下载解析入口
├── run.ps1                         # 一键采集
├── run_pdf.ps1                     # 一键 PDF 解析
├── config.py
├── database.py
├── requirements.txt
├── scripts/
│   ├── init_db.ps1                 # 建 announcement 表
│   └── init_content_db.ps1         # 建 announcement_content 表
├── spider/
│   └── cninfo_spider.py
├── parser/
│   └── pdf_parser.py               # PyMuPDF 解析
├── entity/
│   ├── announcement.py
│   ├── pending_announcement.py
│   └── announcement_content.py
├── service/
│   ├── announcement_service.py
│   └── pdf_service.py              # PDF 下载解析编排
├── repository/
│   ├── announcement_repository.py
│   └── announcement_content_repository.py
└── utils/
    ├── http_util.py
    ├── orgid_util.py
    └── pdf_util.py                 # PDF 下载
```

### 1.6 PDF 下载解析流程

```text
announcement (pdf_download_status=0)
        │
        ▼
下载 PDF → crawler/data/pdf/{股票代码}/
        │
        ▼
PyMuPDF 解析
        │
        ▼
写入 announcement_content (parse_status=1)
        │
        ▼
更新 announcement.pdf_download_status=1
```

**执行命令**

```powershell
.\crawler\scripts\init_content_db.ps1
.\crawler\run_pdf.ps1 -CompanyCode 601012 -Limit 10
```

**验证解析结果**

```powershell
docker exec -it postgres psql -U postgres -d investment_radar -c "SELECT a.company_code, a.title, c.page_count, c.parse_status, LEFT(c.content, 50) FROM investment_radar.announcement_content c JOIN investment_radar.announcement a ON a.id = c.announcement_id LIMIT 5;"
```

### 1.7 采集流程

```text
main.py / run.ps1
    │
    ▼
AnnouncementService
    │
    ▼
CnInfoSpider → 巨潮接口 → JSON
    │
    ▼
Announcement Entity 转换
    │
    ▼
AnnouncementRepository → PostgreSQL
```

### 1.8 常见问题

| 问题 | 原因 | 解决 |
|------|------|------|
| `relation "announcement" does not exist` | 未建表或 Schema 错误 | 执行 `init_db.ps1`，确认 `DB_SCHEMA=investment_radar` |
| 接口返回 0 条 | orgId 错误 | 已从 `szse_stock.json` 动态查询，601012 → `9900022338` |
| `NameError: company_name` | Spider 初始化时机错误 | 已修复，Spider 在 `crawl_and_save` 中创建 |
| 重复运行数据重复 | — | 自动去重，`announcement_id` 唯一约束 |

---

## 二、AI 分析（规划中）

> 模块目录：`ai/`，与 `crawler/` 完全解耦。完整设计见 [05-AI-Service.md](05-AI-Service.md)。

### 2.1 流程

```text
announcement (ai_status=0)
    + announcement_content (parse_status=1)
        │
        ▼
读取待分析数据 → PromptBuilder → LLM → JSON
        │
        ▼
JsonParser → ai_analysis → 更新 ai_status=1
```

### 2.2 前置条件

1. 已采集公告（`announcement`）
2. 已解析 PDF（`announcement_content.parse_status=1`）
3. 已建 `ai_analysis` 表
4. 配置 `ai/.env`（参考 `ai/.env.example`）

### 2.3 配置

```env
MODEL_PROVIDER=DeepSeek
BASE_URL=https://api.deepseek.com/v1
MODEL_NAME=deepseek-chat
API_KEY=your_api_key_here
PROMPT_VERSION=v1.0
AI_BATCH_SIZE=20
```

### 2.4 执行命令（待实现）

```powershell
# 建 ai_analysis 表（首次）
.\ai\scripts\init_db.ps1

# 批量分析（每批 20 条）
.\ai\scripts\run.ps1 -Limit 20
```

### 2.5 验证（待实现）

```powershell
docker exec -it postgres psql -U postgres -d investment_radar -c "SELECT company_code, event_type, sentiment, summary FROM investment_radar.ai_analysis LIMIT 5;"
```

---

## 三、开发记录

### 2026-07-13 公告采集模块

| 事项 | 内容 |
|------|------|
| 新建 | `crawler/` 模块，分层架构：Spider → Entity → Repository |
| 数据源 | 巨潮资讯网 `hisAnnouncement/query` |
| 目标表 | `investment_radar.announcement` |
| 修复 | Schema 从 `investment` 改为 `investment_radar` |
| 修复 | orgId 从硬编码 `gssh0601012` 改为动态查询 `9900022338` |
| 修复 | 请求参数简化为 `stock` + `pageNum` + `pageSize` |
| 修复 | `AnnouncementService.__init__` 中 `company_name` 未定义 |
| 验证 | 601012 隆基绿能，抓取 30 条，入库 30 条 |
| 新增 | PDF 下载解析：`main_pdf.py` + PyMuPDF |
| 验证 | 601012 下载解析 2 条 PDF，parse_status=1 |

### 2026-07-14 AI 分析模块设计

| 事项 | 内容 |
|------|------|
| 文档 | 完成 [05-AI-Service.md](05-AI-Service.md) V1 设计 |
| 目录 | `ai/` 独立模块，8 个 Task 开发顺序 |
| 原则 | 与 Crawler 解耦，OpenAI Compatible API，JSON 输出 |
| Prompt | v1.0，详见 [11-Prompts.md](11-Prompts.md) |
| 配置 | `ai/.env.example` 模板 |

### 下一步

- [x] PDF 下载与正文解析 → `announcement_content`
- [ ] AI 分析 → `ai_analysis`（设计完成，待开发）
- [ ] 与 Spring Boot Research Worker 联动

---

## 三、相关文档

| 文档 | 说明 |
|------|------|
| [05-AI-Service.md](05-AI-Service.md) | AI 分析模块设计 |
| [11-Prompts.md](11-Prompts.md) | Prompt 模板 |
| [12-Crawler.md](12-Crawler.md) | Crawler 技术设计 |
| [02-Database.md](02-Database.md) | 数据库表结构 |
| [04-Research-Workflow.md](04-Research-Workflow.md) | 业务流程 |
