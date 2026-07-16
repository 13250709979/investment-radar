"""PostgreSQL 连接与健康检查。"""

from __future__ import annotations

import logging
from contextlib import contextmanager
from typing import Iterator

import psycopg2
from psycopg2.extensions import connection as PgConnection
from psycopg2.extensions import cursor as PgCursor
from psycopg2.extras import RealDictCursor

from core.config import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_SCHEMA, DB_USER

logger = logging.getLogger(__name__)


def connect() -> PgConnection:
    """打开一条连接（调用方负责关闭）。"""
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        options=f"-c search_path={DB_SCHEMA}",
    )
    conn.autocommit = False
    return conn


@contextmanager
def get_cursor(*, dict_cursor: bool = False) -> Iterator[PgCursor]:
    """获取游标：成功自动 commit，失败 rollback。"""
    conn = connect()
    cursor = conn.cursor(cursor_factory=RealDictCursor if dict_cursor else None)
    try:
        yield cursor
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()


# 写库事务与 get_cursor 相同（保留别名，兼容旧调用）
transaction = get_cursor


def check_connection() -> bool:
    try:
        with get_cursor() as cur:
            cur.execute("SELECT 1")
        logger.info("数据库连接成功: %s/%s (schema=%s)", DB_HOST, DB_NAME, DB_SCHEMA)
        return True
    except Exception as exc:
        logger.error("数据库连接失败: %s", exc)
        return False


def check_ai_analysis_table() -> bool:
    sql = """
        SELECT 1
        FROM information_schema.tables
        WHERE table_schema = %s AND table_name = 'ai_analysis'
    """
    try:
        with get_cursor() as cur:
            cur.execute(sql, (DB_SCHEMA,))
            if cur.fetchone():
                return True
        logger.error(
            "表 %s.ai_analysis 不存在，请先执行: .\\ai-analysis\\scripts\\init_db.ps1",
            DB_SCHEMA,
        )
        return False
    except Exception as exc:
        logger.error("检查 ai_analysis 表失败: %s", exc)
        return False
