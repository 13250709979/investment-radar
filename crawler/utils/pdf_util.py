import hashlib
import logging
import os
import re
from typing import Tuple
from urllib.parse import urlparse

import requests

from core.config import PDF_STORAGE_DIR, REQUEST_TIMEOUT
from utils.http_util import create_session

logger = logging.getLogger(__name__)


def _safe_filename(name: str) -> str:
    name = re.sub(r'[\\/:*?"<>|]', "_", name)
    return name[:200] if name else "unknown"


def build_local_path(company_code: str, announcement_id: str, pdf_url: str) -> str:
    ext = os.path.splitext(urlparse(pdf_url).path)[1] or ".pdf"
    filename = f"{announcement_id}{ext}"
    return os.path.join(str(PDF_STORAGE_DIR), company_code, filename)


def download_pdf(pdf_url: str, company_code: str, announcement_id: str) -> Tuple[str, bytes, str, str]:
    """
    下载 PDF 并保存到本地。
    返回: (local_path, content_bytes, md5, file_name)
    """
    session = create_session()
    response = session.get(pdf_url, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()

    content = response.content
    if not content:
        raise ValueError("PDF 内容为空")

    md5 = hashlib.md5(content).hexdigest()
    local_path = build_local_path(company_code, announcement_id, pdf_url)
    os.makedirs(os.path.dirname(local_path), exist_ok=True)

    with open(local_path, "wb") as f:
        f.write(content)

    file_name = os.path.basename(local_path)
    logger.info("PDF 已下载: %s (%s bytes)", local_path, len(content))
    return local_path, content, md5, file_name
