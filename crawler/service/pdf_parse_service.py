"""PDF download + parse: skip already-success steps."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import datetime

from core.config import PARSER_NAME
from entity.announcement_content import AnnouncementContent
from entity.pending_announcement import PendingAnnouncement
from parser.pdf_text_parser import parse_pdf
from repository.announcement_content_repository import AnnouncementContentRepository
from repository.announcement_repository import AnnouncementRepository
from utils.pdf_download import download_pdf

logger = logging.getLogger(__name__)

PDF_OK, PDF_FAIL = 1, 2
PARSE_OK, PARSE_FAIL = 1, 2


class PdfDownloadError(Exception):
    pass


class PdfParseError(Exception):
    pass


@dataclass
class PdfProcessResult:
    total: int = 0
    success: int = 0
    skipped: int = 0
    download_failed: int = 0
    parse_failed: int = 0


class PdfParseService:
    def __init__(self):
        self.announcement_repo = AnnouncementRepository()
        self.content_repo = AnnouncementContentRepository()

    def process_pending(self, limit: int = 50, company_code: str | None = None) -> PdfProcessResult:
        pending = self.announcement_repo.find_pending_pdf(limit=limit, company_code=company_code)
        result = PdfProcessResult(total=len(pending))

        for item in pending:
            try:
                status = self._process_one(item)
                if status == "skipped":
                    result.skipped += 1
                else:
                    result.success += 1
            except PdfDownloadError as exc:
                result.download_failed += 1
                self.announcement_repo.update_pdf_status(item.id, PDF_FAIL)
                logger.error("PDF download failed id=%s: %s", item.id, exc)
            except PdfParseError as exc:
                result.parse_failed += 1
                logger.error("PDF parse failed id=%s: %s", item.id, exc)

        logger.info(
            "PDF done: total=%s ok=%s skipped=%s download_fail=%s parse_fail=%s",
            result.total,
            result.success,
            result.skipped,
            result.download_failed,
            result.parse_failed,
        )
        return result

    def _process_one(self, item: PendingAnnouncement) -> str:
        # 已下载成功且解析成功：直接跳过（查询层通常已过滤）
        if item.pdf_download_status == PDF_OK and item.parse_status == PARSE_OK:
            logger.info("skip done id=%s", item.id)
            return "skipped"

        # 1) 下载：成功过则复用本地文件，不重复拉网
        try:
            local_path, content_bytes, md5, file_name = download_pdf(
                pdf_url=item.adjunct_url,
                company_code=item.company_code,
                announcement_id=item.announcement_id,
                preferred_path=item.pdf_local_path,
            )
        except Exception as exc:
            raise PdfDownloadError(str(exc)) from exc

        if item.pdf_download_status != PDF_OK:
            self.announcement_repo.update_pdf_status(item.id, PDF_OK)

        # 2) 解析：已成功则不再解析
        if item.parse_status == PARSE_OK:
            logger.info("skip parse (already ok) id=%s", item.id)
            return "skipped"

        text, page_count, parser_version = "", 0, None
        parse_status, parse_message = PARSE_OK, None
        try:
            text, page_count, parser_version = parse_pdf(content_bytes)
            if not text:
                parse_status, parse_message = PARSE_FAIL, "empty parse result"
        except Exception as exc:
            parse_status, parse_message = PARSE_FAIL, str(exc)

        self.content_repo.insert(
            AnnouncementContent(
                announcement_id=item.id,
                pdf_url=item.adjunct_url,
                pdf_file_name=file_name,
                pdf_local_path=local_path,
                pdf_size=len(content_bytes),
                pdf_md5=md5,
                content=text,
                page_count=page_count,
                parser_name=PARSER_NAME,
                parser_version=parser_version,
                parse_status=parse_status,
                parse_message=parse_message,
                parse_time=datetime.now(),
            )
        )

        if parse_status == PARSE_FAIL:
            raise PdfParseError(parse_message or "parse failed")
        return "ok"
