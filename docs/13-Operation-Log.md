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
├── main.py                         # 入口
├── run.ps1                         # 一键运行
├── config.py                       # 配置
├── database.py                     # 数据库连接
├── requirements.txt
├── scripts/
│   └── init_db.ps1                 # 建表脚本
├── spider/
│   └── cninfo_spider.py            # 巨潮接口请求
├── entity/
│   └── announcement.py             # JSON → Entity
├── service/
│   └── announcement_service.py     # 采集编排
├── repository/
│   └── announcement_repository.py  # 数据入库
└── utils/
    ├── http_util.py                # HTTP 请求
    └── orgid_util.py               # orgId 查询
```

### 1.6 采集流程

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

### 1.7 常见问题

| 问题 | 原因 | 解决 |
|------|------|------|
| `relation "announcement" does not exist` | 未建表或 Schema 错误 | 执行 `init_db.ps1`，确认 `DB_SCHEMA=investment_radar` |
| 接口返回 0 条 | orgId 错误 | 已从 `szse_stock.json` 动态查询，601012 → `9900022338` |
| `NameError: company_name` | Spider 初始化时机错误 | 已修复，Spider 在 `crawl_and_save` 中创建 |
| 重复运行数据重复 | — | 自动去重，`announcement_id` 唯一约束 |

---

## 二、开发记录

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

### 下一步

- [ ] PDF 下载与正文解析 → `announcement_content`
- [ ] AI 分析 → `ai_analysis`
- [ ] 与 Spring Boot Research Worker 联动

---

## 三、相关文档

| 文档 | 说明 |
|------|------|
| [12-Crawler.md](12-Crawler.md) | Crawler 技术设计 |
| [02-Database.md](02-Database.md) | 数据库表结构 |
| [04-Research-Workflow.md](04-Research-Workflow.md) | 业务流程 |
