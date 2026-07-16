"""PDF download helpers: skip network if local file already exists."""

from __future__ import annotations

import hashlib
import logging
import os
import re
from urllib.parse import urlparse

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


def load_local_pdf(local_path: str) -> tuple[str, bytes, str, str] | None:
    """若本地文件存在则读取，否则返回 None。"""
    if not local_path or not os.path.isfile(local_path):
        return None
    with open(local_path, "rb") as f:
        content = f.read()
    if not content:
        return None
    md5 = hashlib.md5(content).hexdigest()
    logger.info("reuse local PDF: %s (%s bytes)", local_path, len(content))
    return local_path, content, md5, os.path.basename(local_path)


def download_pdf(
    pdf_url: str,
    company_code: str,
    announcement_id: str,
    preferred_path: str | None = None,
) -> tuple[str, bytes, str, str]:
    """
    下载 PDF 并保存到本地。
    本地已存在则直接复用，不重复下载。
    返回: (local_path, content_bytes, md5, file_name)
    """
    local_path = preferred_path or build_local_path(company_code, announcement_id, pdf_url)
    cached = load_local_pdf(local_path)
    if cached:
        return cached

    # preferred_path 无效时，再试标准路径
    if preferred_path:
        standard = build_local_path(company_code, announcement_id, pdf_url)
        cached = load_local_pdf(standard)
        if cached:
            return cached
        local_path = standard

    session = create_session()
    response = session.get(pdf_url, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()

    content = response.content
    if not content:
        raise ValueError("PDF content is empty")

    md5 = hashlib.md5(content).hexdigest()
    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    with open(local_path, "wb") as f:
        f.write(content)

    file_name = os.path.basename(local_path)
    logger.info("PDF downloaded: %s (%s bytes)", local_path, len(content))
    return local_path, content, md5, file_name
