"""配置仅从 .env 读取。"""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

CRAWLER_DIR = Path(__file__).resolve().parent.parent
load_dotenv(CRAWLER_DIR / ".env")
load_dotenv(CRAWLER_DIR.parent / ".env", override=False)


def _env(key: str, default: str = "") -> str:
    return (os.getenv(key) or default).strip()


def _env_int(key: str, default: int) -> int:
    raw = _env(key)
    return int(raw) if raw else default


# 数据库（与 ai-analysis / backend 共用）
DB_HOST = _env("DB_HOST", "localhost")
DB_PORT = _env_int("DB_PORT", 5432)
DB_NAME = _env("DB_NAME", "investment_radar")
DB_USER = _env("DB_USER", "investment")
DB_PASSWORD = _env("DB_PASSWORD", "123456")
DB_SCHEMA = _env("DB_SCHEMA", "investment_radar")

# 巨潮接口
CNINFO_QUERY_URL = _env(
    "CNINFO_QUERY_URL",
    "https://www.cninfo.com.cn/new/hisAnnouncement/query",
)
CNINFO_STATIC_BASE = _env(
    "CNINFO_STATIC_BASE",
    "https://static.cninfo.com.cn/",
)
CNINFO_INDEX_URL = _env("CNINFO_INDEX_URL", "https://www.cninfo.com.cn/new/index")

# 采集参数
DEFAULT_PAGE_SIZE = _env_int("CRAWLER_PAGE_SIZE", 30)
REQUEST_TIMEOUT = _env_int("CRAWLER_REQUEST_TIMEOUT", 30)
REQUEST_RETRY = _env_int("CRAWLER_REQUEST_RETRY", 3)
REQUEST_SLEEP = float(_env("CRAWLER_REQUEST_SLEEP", "0.5") or "0.5")
PDF_BATCH_LIMIT = _env_int("PDF_BATCH_LIMIT", 50)

# PDF
PDF_STORAGE_DIR = Path(_env("PDF_STORAGE_DIR") or (CRAWLER_DIR / "data" / "pdf"))
PARSER_NAME = _env("PARSER_NAME", "PyMuPDF")
