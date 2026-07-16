import logging
from datetime import datetime

from core.database import get_cursor
from entity.announcement_content import AnnouncementContent

logger = logging.getLogger(__name__)

INSERT_SQL = """
INSERT INTO announcement_content (
    announcement_id,
    pdf_url,
    pdf_file_name,
    pdf_local_path,
    pdf_size,
    pdf_md5,
    content,
    page_count,
    parser_name,
    parser_version,
    parse_status,
    parse_message,
    parse_time,
    create_time,
    update_time
) VALUES (
    %(announcement_id)s,
    %(pdf_url)s,
    %(pdf_file_name)s,
    %(pdf_local_path)s,
    %(pdf_size)s,
    %(pdf_md5)s,
    %(content)s,
    %(page_count)s,
    %(parser_name)s,
    %(parser_version)s,
    %(parse_status)s,
    %(parse_message)s,
    %(parse_time)s,
    %(create_time)s,
    %(update_time)s
)
ON CONFLICT (announcement_id) DO UPDATE SET
    pdf_url = EXCLUDED.pdf_url,
    pdf_file_name = EXCLUDED.pdf_file_name,
    pdf_local_path = EXCLUDED.pdf_local_path,
    pdf_size = EXCLUDED.pdf_size,
    pdf_md5 = EXCLUDED.pdf_md5,
    content = EXCLUDED.content,
    page_count = EXCLUDED.page_count,
    parser_name = EXCLUDED.parser_name,
    parser_version = EXCLUDED.parser_version,
    parse_status = EXCLUDED.parse_status,
    parse_message = EXCLUDED.parse_message,
    parse_time = EXCLUDED.parse_time,
    update_time = EXCLUDED.update_time
"""


class AnnouncementContentRepository:
    def insert(self, entity: AnnouncementContent) -> None:
        now = datetime.now()
        params = {
            "announcement_id": entity.announcement_id,
            "pdf_url": entity.pdf_url,
            "pdf_file_name": entity.pdf_file_name,
            "pdf_local_path": entity.pdf_local_path,
            "pdf_size": entity.pdf_size,
            "pdf_md5": entity.pdf_md5,
            "content": entity.content,
            "page_count": entity.page_count,
            "parser_name": entity.parser_name,
            "parser_version": entity.parser_version,
            "parse_status": entity.parse_status,
            "parse_message": entity.parse_message,
            "parse_time": entity.parse_time or now,
            "create_time": now,
            "update_time": now,
        }

        with get_cursor() as cursor:
            cursor.execute(INSERT_SQL, params)

        logger.debug("写入 announcement_content: announcement_id=%s", entity.announcement_id)

    def count_parsed(self, company_code: str = "") -> int:
        sql = """
            SELECT COUNT(*)
            FROM announcement_content ac
            JOIN announcement a ON a.id = ac.announcement_id
            WHERE ac.parse_status = 1
        """
        params = []
        if company_code:
            sql += " AND a.company_code = %s"
            params.append(company_code)

        with get_cursor() as cursor:
            cursor.execute(sql, params)
            row = cursor.fetchone()
            return row[0] if row else 0
