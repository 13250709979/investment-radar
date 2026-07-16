"""PostgreSQL connection helpers."""

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


def _table_exists(table_name: str) -> bool:
    sql = """
        SELECT 1 FROM information_schema.tables
        WHERE table_schema = %s AND table_name = %s
    """
    with get_cursor() as cur:
        cur.execute(sql, (DB_SCHEMA, table_name))
        return cur.fetchone() is not None


def check_connection() -> bool:
    try:
        with get_cursor() as cur:
            cur.execute("SELECT 1")
        logger.info("DB ok: %s/%s schema=%s", DB_HOST, DB_NAME, DB_SCHEMA)
        return True
    except Exception as exc:
        logger.error("DB connect failed: %s", exc)
        return False


def check_announcement_table() -> bool:
    if _table_exists("announcement"):
        return True
    logger.error(
        "missing %s.announcement, run: .\\crawler\\scripts\\init_db.ps1",
        DB_SCHEMA,
    )
    return False


def check_announcement_content_table() -> bool:
    if _table_exists("announcement_content"):
        return True
    logger.error(
        "missing %s.announcement_content, run: .\\crawler\\scripts\\init_content_db.ps1",
        DB_SCHEMA,
    )
    return False
