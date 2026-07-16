import logging
from typing import Tuple

import fitz

from core.config import PARSER_NAME

logger = logging.getLogger(__name__)


def parse_pdf(content: bytes) -> Tuple[str, int, str]:
    """
    使用 PyMuPDF 解析 PDF 正文。
    返回: (text, page_count, parser_version)
    """
    doc = fitz.open(stream=content, filetype="pdf")
    try:
        pages = []
        for page in doc:
            pages.append(page.get_text("text"))
        text = "\n".join(pages).strip()
        page_count = doc.page_count
        version = getattr(fitz, "__version__", "unknown")
        logger.info("PDF 解析完成: %s 页, %s 字符", page_count, len(text))
        return text, page_count, str(version)
    finally:
        doc.close()
