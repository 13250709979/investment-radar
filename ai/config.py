import os
from pathlib import Path

from dotenv import load_dotenv

_AI_DIR = Path(__file__).resolve().parent
load_dotenv(_AI_DIR / ".env")
load_dotenv(_AI_DIR.parent / ".env", override=False)

# 大模型
MODEL_PROVIDER = os.getenv("MODEL_PROVIDER", "DeepSeek")
BASE_URL = os.getenv("BASE_URL", "https://api.deepseek.com/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "deepseek-chat")
API_KEY = os.getenv("API_KEY", "")

# 数据库（与 crawler 共用）
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_NAME = os.getenv("DB_NAME", "investment_radar")
DB_USER = os.getenv("DB_USER", "investment")
DB_PASSWORD = os.getenv("DB_PASSWORD", "123456")
DB_SCHEMA = os.getenv("DB_SCHEMA", "investment_radar")

# 分析参数
PROMPT_VERSION = os.getenv("PROMPT_VERSION", "v1.0")
AI_BATCH_SIZE = int(os.getenv("AI_BATCH_SIZE", "20"))
AI_MAX_RETRIES = int(os.getenv("AI_MAX_RETRIES", "3"))
AI_MAX_CONTENT_LENGTH = int(os.getenv("AI_MAX_CONTENT_LENGTH", "12000"))
AI_REQUEST_TIMEOUT = int(os.getenv("AI_REQUEST_TIMEOUT", "120"))
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.1"))
