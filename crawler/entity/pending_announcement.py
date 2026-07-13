from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class PendingAnnouncement:
    """待下载 PDF 的公告记录。"""

    id: int
    announcement_id: str
    company_code: str
    company_name: str
    title: str
    adjunct_url: str
    adjunct_size: Optional[int]
    publish_time: datetime
