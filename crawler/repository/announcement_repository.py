import logging
from datetime import datetime
from typing import List, Optional

from core.database import get_cursor
from entity.announcement import Announcement
from entity.pending_announcement import PendingAnnouncement

logger = logging.getLogger(__name__)

INSERT_SQL = """
INSERT INTO announcement (
    announcement_id,
    company_code,
    company_name,
    title,
    announcement_type,
    adjunct_url,
    adjunct_size,
    adjunct_type,
    page_column,
    publish_time,
    crawl_time,
    ai_status,
    pdf_download_status,
    deleted,
    create_time,
    update_time
) VALUES (
    %(announcement_id)s,
    %(company_code)s,
    %(company_name)s,
    %(title)s,
    %(announcement_type)s,
    %(adjunct_url)s,
    %(adjunct_size)s,
    %(adjunct_type)s,
    %(page_column)s,
    %(publish_time)s,
    %(crawl_time)s,
    0,
    0,
    FALSE,
    %(create_time)s,
    %(update_time)s
)
ON CONFLICT (announcement_id) DO NOTHING
"""


class AnnouncementRepository:
    def exists(self, announcement_id: str) -> bool:
        with get_cursor() as cursor:
            cursor.execute(
                "SELECT 1 FROM announcement WHERE announcement_id = %s LIMIT 1",
                (announcement_id,),
            )
            return cursor.fetchone() is not None

    def insert(self, entity: Announcement) -> bool:
        now = datetime.now()
        params = {
            "announcement_id": entity.announcement_id,
            "company_code": entity.company_code,
            "company_name": entity.company_name,
            "title": entity.title,
            "announcement_type": entity.announcement_type,
            "adjunct_url": entity.adjunct_url,
            "adjunct_size": entity.adjunct_size,
            "adjunct_type": entity.adjunct_type,
            "page_column": entity.page_column,
            "publish_time": entity.publish_time,
            "crawl_time": now,
            "create_time": now,
            "update_time": now,
        }

        with get_cursor() as cursor:
            cursor.execute(INSERT_SQL, params)
            inserted = cursor.rowcount > 0

        if inserted:
            logger.debug("新增公告: %s %s", entity.announcement_id, entity.title)
        return inserted

    def count_by_company(self, company_code: str) -> int:
        with get_cursor() as cursor:
            cursor.execute(
                "SELECT COUNT(*) FROM announcement WHERE company_code = %s AND deleted = FALSE",
                (company_code,),
            )
            row = cursor.fetchone()
            return row[0] if row else 0

    def find_pending_pdf(
        self, limit: int = 50, company_code: Optional[str] = None
    ) -> List[PendingAnnouncement]:
        sql = """
            SELECT id, announcement_id, company_code, company_name,
                   title, adjunct_url, adjunct_size, publish_time
            FROM announcement
            WHERE pdf_download_status = 0 AND deleted = FALSE
        """
        params: list = []
        if company_code:
            sql += " AND company_code = %s"
            params.append(company_code)
        sql += " ORDER BY publish_time DESC LIMIT %s"
        params.append(limit)

        with get_cursor(dict_cursor=True) as cursor:
            cursor.execute(sql, params)
            rows = cursor.fetchall()

        return [
            PendingAnnouncement(
                id=row["id"],
                announcement_id=row["announcement_id"],
                company_code=row["company_code"],
                company_name=row["company_name"],
                title=row["title"],
                adjunct_url=row["adjunct_url"],
                adjunct_size=row["adjunct_size"],
                publish_time=row["publish_time"],
            )
            for row in rows
        ]

    def update_pdf_status(self, announcement_pk: int, status: int) -> None:
        with get_cursor() as cursor:
            cursor.execute(
                """
                UPDATE announcement
                SET pdf_download_status = %s, update_time = %s
                WHERE id = %s
                """,
                (status, datetime.now(), announcement_pk),
            )
