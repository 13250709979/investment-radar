import logging
from contextlib import contextmanager

import psycopg2
from psycopg2.extras import RealDictCursor

from config import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_SCHEMA, DB_USER

logger = logging.getLogger(__name__)


def get_connection():
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
def get_cursor(dict_cursor=False):
    conn = get_connection()
    cursor_factory = RealDictCursor if dict_cursor else None
    cursor = conn.cursor(cursor_factory=cursor_factory)
    try:
        yield cursor
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()


@contextmanager
def transaction():
    """多步写库事务：ai_analysis + announcement 状态更新。"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        yield conn, cursor
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()


def check_connection() -> bool:
    try:
        with get_cursor() as cursor:
            cursor.execute("SELECT 1")
        logger.info("数据库连接成功: %s/%s (schema=%s)", DB_HOST, DB_NAME, DB_SCHEMA)
        return True
    except Exception as exc:
        logger.error("数据库连接失败: %s", exc)
        return False


def check_ai_analysis_table() -> bool:
    try:
        with get_cursor() as cursor:
            cursor.execute(
                """
                SELECT 1 FROM information_schema.tables
                WHERE table_schema = %s AND table_name = 'ai_analysis'
                """,
                (DB_SCHEMA,),
            )
            exists = cursor.fetchone() is not None
        if exists:
            return True
        logger.error(
            "表 %s.ai_analysis 不存在，请先执行：\n"
            "  .\\ai\\scripts\\init_ai_db.ps1",
            DB_SCHEMA,
        )
        return False
    except Exception as exc:
        logger.error("检查 ai_analysis 表失败: %s", exc)
        return False
