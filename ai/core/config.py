import os
import re
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

_AI_DIR = Path(__file__).resolve().parent.parent  # ai/
load_dotenv(_AI_DIR / ".env")
load_dotenv(_AI_DIR.parent / ".env", override=False)

_MODEL_PREFIX_RE = re.compile(r"^MODEL_([A-Z0-9_]+)_PROVIDER$")

_DEFAULT_PROVIDER = "GoogleAIStudio"
_DEFAULT_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai"
_DEFAULT_MODEL_NAME = "gemini-2.5-flash"


@dataclass(frozen=True)
class ModelConfig:
    """一组已解析的大模型连接配置。"""

    id: str
    provider: str
    base_url: str
    model_name: str
    api_key: str


def _normalize_model_id(model_id: str) -> str:
    return model_id.strip().lower().replace("-", "_")


def _profile_env(model_id: str, field: str) -> str | None:
    key = f"MODEL_{_normalize_model_id(model_id).upper()}_{field}"
    value = os.getenv(key)
    if value is None:
        return None
    value = value.strip()
    return value if value else None


def list_model_ids() -> list[str]:
    """扫描 .env 中已配置的命名模型 id（如 google、deepseek）。"""
    ids: list[str] = []
    seen: set[str] = set()
    for key in os.environ:
        match = _MODEL_PREFIX_RE.match(key)
        if not match:
            continue
        model_id = match.group(1).lower()
        if model_id in seen:
            continue
        seen.add(model_id)
        ids.append(model_id)
    return sorted(ids)


def _load_named_profile(model_id: str) -> ModelConfig | None:
    provider = _profile_env(model_id, "PROVIDER")
    base_url = _profile_env(model_id, "BASE_URL")
    model_name = _profile_env(model_id, "NAME")
    api_key = _profile_env(model_id, "API_KEY")

    if not any([provider, base_url, model_name, api_key]):
        return None

    missing = [
        name
        for name, value in (
            ("PROVIDER", provider),
            ("BASE_URL", base_url),
            ("NAME", model_name),
            ("API_KEY", api_key),
        )
        if not value
    ]
    if missing:
        prefix = f"MODEL_{_normalize_model_id(model_id).upper()}_"
        raise ValueError(
            f"模型 '{model_id}' 配置不完整，缺少: "
            + ", ".join(f"{prefix}{m}" for m in missing)
        )

    return ModelConfig(
        id=_normalize_model_id(model_id),
        provider=provider or "",
        base_url=base_url or "",
        model_name=model_name or "",
        api_key=api_key or "",
    )


def _load_legacy_profile() -> ModelConfig:
    return ModelConfig(
        id="legacy",
        provider=os.getenv("MODEL_PROVIDER", _DEFAULT_PROVIDER),
        base_url=os.getenv("BASE_URL", _DEFAULT_BASE_URL),
        model_name=os.getenv("MODEL_NAME", _DEFAULT_MODEL_NAME),
        api_key=os.getenv("API_KEY", ""),
    )


def get_model_config(model_id: str | None = None) -> ModelConfig:
    """
    按 id 解析模型配置。

    优先级：
    1. 显式传入的 model_id / ACTIVE_MODEL → 读 MODEL_<ID>_* 命名配置
    2. 未指定且无命名配置 → 回退到旧版扁平 MODEL_PROVIDER / BASE_URL / MODEL_NAME / API_KEY
    """
    requested = (model_id or os.getenv("ACTIVE_MODEL", "") or "").strip()
    if requested:
        profile = _load_named_profile(requested)
        if profile is None:
            available = list_model_ids()
            hint = (
                f"可用模型: {', '.join(available)}"
                if available
                else "请先在 .env 中配置 MODEL_<ID>_PROVIDER 等变量"
            )
            raise ValueError(f"未找到模型配置 '{requested}'。{hint}")
        return profile

    named = list_model_ids()
    if named:
        raise ValueError(
            "已配置命名模型但未设置 ACTIVE_MODEL。"
            f"请在 .env 中设置 ACTIVE_MODEL（可选: {', '.join(named)}），"
            "或通过 --model 指定。"
        )
    return _load_legacy_profile()


def activate_model(model_id: str | None = None) -> ModelConfig:
    """解析并写入当前活跃模型对应的全局常量。"""
    global ACTIVE_MODEL, MODEL_PROVIDER, BASE_URL, MODEL_NAME, API_KEY
    cfg = get_model_config(model_id)
    ACTIVE_MODEL = cfg.id
    MODEL_PROVIDER = cfg.provider
    BASE_URL = cfg.base_url
    MODEL_NAME = cfg.model_name
    API_KEY = cfg.api_key
    return cfg


# 当前活跃模型（main / --model 调用 activate_model 后生效）
ACTIVE_MODEL = ""
MODEL_PROVIDER = _DEFAULT_PROVIDER
BASE_URL = _DEFAULT_BASE_URL
MODEL_NAME = _DEFAULT_MODEL_NAME
API_KEY = ""


def _bootstrap_active_model() -> None:
    """启动时按 ACTIVE_MODEL / 旧版扁平配置预加载；失败则留给 main 报错。"""
    try:
        activate_model()
    except ValueError:
        pass


_bootstrap_active_model()

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
