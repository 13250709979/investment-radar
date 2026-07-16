"""配置仅从 .env 读取，代码不写死模型与密钥。"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

AI_DIR = Path(__file__).resolve().parent.parent
load_dotenv(AI_DIR / ".env")
load_dotenv(AI_DIR.parent / ".env", override=False)

_MODEL_RE = re.compile(r"^MODEL_([A-Z0-9_]+)_PROVIDER$")
_FIELDS = ("PROVIDER", "BASE_URL", "NAME", "API_KEY")


def _env(key: str, default: str = "") -> str:
    return (os.getenv(key) or default).strip()


def _env_int(key: str, default: int) -> int:
    raw = _env(key)
    return int(raw) if raw else default


def _env_float(key: str, default: float) -> float:
    raw = _env(key)
    return float(raw) if raw else default


@dataclass(frozen=True)
class ModelConfig:
    id: str
    provider: str
    base_url: str
    model_name: str
    api_key: str


# --- 运行参数（数值缺省仅作兜底，业务值以 .env 为准）---
DB_HOST = _env("DB_HOST", "localhost")
DB_PORT = _env_int("DB_PORT", 5432)
DB_NAME = _env("DB_NAME", "investment_radar")
DB_USER = _env("DB_USER", "investment")
DB_PASSWORD = _env("DB_PASSWORD", "123456")
DB_SCHEMA = _env("DB_SCHEMA", "investment_radar")

PROMPT_VERSION = _env("PROMPT_VERSION", "v1.0")
AI_BATCH_SIZE = _env_int("AI_BATCH_SIZE", 20)
AI_MAX_RETRIES = _env_int("AI_MAX_RETRIES", 3)
AI_MAX_CONTENT_LENGTH = _env_int("AI_MAX_CONTENT_LENGTH", 12000)
AI_REQUEST_TIMEOUT = _env_int("AI_REQUEST_TIMEOUT", 120)
LLM_TEMPERATURE = _env_float("LLM_TEMPERATURE", 0.1)


def _norm_id(model_id: str) -> str:
    return model_id.strip().lower().replace("-", "_")


def list_model_ids() -> list[str]:
    """扫描 .env 中 MODEL_<ID>_PROVIDER 声明的模型。"""
    ids = {
        m.group(1).lower()
        for key in os.environ
        if (m := _MODEL_RE.match(key))
    }
    return sorted(ids)


def _named_model(model_id: str) -> ModelConfig | None:
    mid = _norm_id(model_id)
    prefix = f"MODEL_{mid.upper()}_"
    values = {f: _env(f"{prefix}{f}") for f in _FIELDS}
    if not any(values.values()):
        return None
    missing = [f"{prefix}{f}" for f in _FIELDS if not values[f]]
    if missing:
        raise ValueError(f"模型 '{mid}' 配置不完整，缺少: {', '.join(missing)}")
    return ModelConfig(
        id=mid,
        provider=values["PROVIDER"],
        base_url=values["BASE_URL"],
        model_name=values["NAME"],
        api_key=values["API_KEY"],
    )


def _flat_model() -> ModelConfig:
    """兼容旧版扁平四元组：MODEL_PROVIDER / BASE_URL / MODEL_NAME / API_KEY。"""
    provider = _env("MODEL_PROVIDER")
    base_url = _env("BASE_URL")
    model_name = _env("MODEL_NAME")
    api_key = _env("API_KEY")
    missing = [
        name
        for name, value in (
            ("MODEL_PROVIDER", provider),
            ("BASE_URL", base_url),
            ("MODEL_NAME", model_name),
            ("API_KEY", api_key),
        )
        if not value
    ]
    if missing:
        raise ValueError(f"请在 .env 中配置: {', '.join(missing)}")
    return ModelConfig(
        id="default",
        provider=provider,
        base_url=base_url,
        model_name=model_name,
        api_key=api_key,
    )


def resolve_model(model_id: str | None = None) -> ModelConfig:
    """
    解析当前模型：
    1. --model / ACTIVE_MODEL → MODEL_<ID>_*
    2. 仅有命名模型但未指定 → 报错
    3. 无命名模型 → 旧版扁平配置
    """
    requested = _norm_id(model_id or _env("ACTIVE_MODEL")) if (model_id or _env("ACTIVE_MODEL")) else ""
    named = list_model_ids()

    if requested:
        profile = _named_model(requested)
        if profile is None:
            hint = f"可用: {', '.join(named)}" if named else "请先配置 MODEL_<ID>_PROVIDER 等"
            raise ValueError(f"未找到模型 '{requested}'。{hint}")
        return profile

    if named:
        raise ValueError(
            f"已配置模型但未指定 ACTIVE_MODEL / --model（可选: {', '.join(named)}）"
        )
    return _flat_model()
