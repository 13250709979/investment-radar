from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class PendingAnnouncement:
    """待处理 PDF 的公告（未下载成功，或未解析成功）。"""

    id: int
    announcement_id: str
    company_code: str
    company_name: str
    title: str
    adjunct_url: str
    adjunct_size: Optional[int]
    publish_time: datetime
    pdf_download_status: int = 0
    pdf_local_path: Optional[str] = None
    parse_status: Optional[int] = None
