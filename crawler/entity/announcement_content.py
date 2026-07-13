from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class AnnouncementContent:
    """公告 PDF 解析内容，对应 investment_radar.announcement_content 表。"""

    announcement_id: int
    pdf_url: str
    pdf_file_name: Optional[str]
    pdf_local_path: Optional[str]
    pdf_size: Optional[int]
    pdf_md5: Optional[str]
    content: Optional[str]
    page_count: Optional[int]
    parser_name: str
    parser_version: Optional[str]
    parse_status: int
    parse_message: Optional[str]
    parse_time: Optional[datetime]
