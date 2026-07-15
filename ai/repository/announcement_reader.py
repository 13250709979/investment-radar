"""读取待分析公告。"""

from __future__ import annotations

import logging

from core.config import AI_BATCH_SIZE, DB_SCHEMA
from core.database import get_cursor

logger = logging.getLogger(__name__)


class AnnouncementReader:
    def find_wait_analysis(
        self,
        limit: int | None = None,
        company_code: str | None = None,
    ) -> list[dict]:
        batch_size = AI_BATCH_SIZE if limit is None else limit
        params: list = []
        company_filter = ""
        if company_code:
            company_filter = "AND a.company_code = %s"
            params.append(company_code)
        params.append(batch_size)

        sql = f"""
            SELECT
                a.id,
                a.company_code,
                a.company_name,
                a.title,
                c.content
            FROM {DB_SCHEMA}.announcement a
            JOIN {DB_SCHEMA}.announcement_content c
                ON a.id = c.announcement_id
            WHERE
                a.ai_status = 0
                AND c.parse_status = 1
                AND a.deleted = FALSE
                {company_filter}
            ORDER BY a.publish_time DESC
            LIMIT %s
        """

        with get_cursor(dict_cursor=True) as cursor:
            cursor.execute(sql, params)
            rows = cursor.fetchall()

        result = [dict(row) for row in rows]
        logger.info("待分析公告: %s 条 (limit=%s)", len(result), batch_size)
        return result
