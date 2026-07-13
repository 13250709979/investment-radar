import os

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_NAME = os.getenv("DB_NAME", "investment_radar")
DB_USER = os.getenv("DB_USER", "investment")
DB_PASSWORD = os.getenv("DB_PASSWORD", "123456")
DB_SCHEMA = os.getenv("DB_SCHEMA", "investment_radar")

CNINFO_QUERY_URL = os.getenv(
    "CNINFO_QUERY_URL",
    "https://www.cninfo.com.cn/new/hisAnnouncement/query",
)
CNINFO_STATIC_BASE = os.getenv(
    "CNINFO_STATIC_BASE",
    "https://static.cninfo.com.cn/",
)

DEFAULT_PAGE_SIZE = int(os.getenv("CRAWLER_PAGE_SIZE", "30"))
REQUEST_TIMEOUT = int(os.getenv("CRAWLER_REQUEST_TIMEOUT", "30"))
REQUEST_RETRY = int(os.getenv("CRAWLER_REQUEST_RETRY", "3"))

PDF_STORAGE_DIR = os.getenv("PDF_STORAGE_DIR", os.path.join(os.path.dirname(__file__), "data", "pdf"))
PARSER_NAME = "PyMuPDF"
