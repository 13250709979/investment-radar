import logging
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from config import PARSER_NAME
from entity.announcement_content import AnnouncementContent
from parser.pdf_parser import parse_pdf
from repository.announcement_content_repository import AnnouncementContentRepository
from repository.announcement_repository import AnnouncementRepository
from utils.pdf_util import download_pdf

logger = logging.getLogger(__name__)

PDF_STATUS_DOWNLOADED = 1
PDF_STATUS_FAILED = 2
PARSE_STATUS_SUCCESS = 1
PARSE_STATUS_FAILED = 2


class PdfDownloadError(Exception):
    pass


class PdfParseError(Exception):
    pass


@dataclass
class PdfProcessResult:
    total: int
    success: int
    download_failed: int
    parse_failed: int


class PdfService:
    def __init__(self):
        self.announcement_repo = AnnouncementRepository()
        self.content_repo = AnnouncementContentRepository()

    def process_pending(
        self,
        limit: int = 50,
        company_code: Optional[str] = None,
    ) -> PdfProcessResult:
        pending = self.announcement_repo.find_pending_pdf(limit=limit, company_code=company_code)
        result = PdfProcessResult(
            total=len(pending),
            success=0,
            download_failed=0,
            parse_failed=0,
        )

        for item in pending:
            try:
                self._process_one(item)
                result.success += 1
            except PdfDownloadError as exc:
                result.download_failed += 1
                self.announcement_repo.update_pdf_status(item.id, PDF_STATUS_FAILED)
                logger.error("PDF 下载失败 id=%s: %s", item.id, exc)
            except PdfParseError as exc:
                result.parse_failed += 1
                logger.error("PDF 解析失败 id=%s: %s", item.id, exc)

        logger.info(
            "PDF 处理完成: total=%s success=%s download_failed=%s parse_failed=%s",
            result.total,
            result.success,
            result.download_failed,
            result.parse_failed,
        )
        return result

    def _process_one(self, item) -> None:
        # 1. 下载 PDF
        try:
            local_path, content_bytes, md5, file_name = download_pdf(
                pdf_url=item.adjunct_url,
                company_code=item.company_code,
                announcement_id=item.announcement_id,
            )
        except Exception as exc:
            raise PdfDownloadError(str(exc)) from exc

        # 2. PyMuPDF 解析
        parse_status = PARSE_STATUS_SUCCESS
        parse_message = None
        text = ""
        page_count = 0
        parser_version = None

        try:
            text, page_count, parser_version = parse_pdf(content_bytes)
            if not text:
                parse_status = PARSE_STATUS_FAILED
                parse_message = "解析结果为空"
        except Exception as exc:
            parse_status = PARSE_STATUS_FAILED
            parse_message = str(exc)

        # 3. 写入 announcement_content
        content_entity = AnnouncementContent(
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
        self.content_repo.insert(content_entity)

        # 4. 更新 announcement.pdf_download_status
        self.announcement_repo.update_pdf_status(item.id, PDF_STATUS_DOWNLOADED)

        if parse_status == PARSE_STATUS_FAILED:
            raise PdfParseError(parse_message or "解析失败")
