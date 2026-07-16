from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from core.config import CNINFO_STATIC_BASE


@dataclass
class Announcement:
    """公告实体，对应 investment_radar.announcement 表。"""

    announcement_id: str
    company_code: str
    company_name: str
    title: str
    announcement_type: Optional[str]
    adjunct_url: str
    adjunct_size: Optional[int]
    adjunct_type: Optional[str]
    page_column: Optional[str]
    publish_time: datetime

    @classmethod
    def from_cninfo_json(cls, raw: dict) -> Optional["Announcement"]:
        """将巨潮接口返回的 JSON 转换为 Announcement 实体。"""
        announcement_id = str(raw.get("announcementId") or "").strip()
        adjunct_path = str(raw.get("adjunctUrl") or "").strip()
        title = str(raw.get("announcementTitle") or "").strip()

        if not announcement_id or not title or not adjunct_path:
            return None

        return cls(
            announcement_id=announcement_id,
            company_code=str(raw.get("secCode") or "").strip(),
            company_name=str(raw.get("secName") or "").strip(),
            title=title,
            announcement_type=raw.get("announcementType"),
            adjunct_url=_build_adjunct_url(adjunct_path),
            adjunct_size=raw.get("adjunctSize"),
            adjunct_type=raw.get("adjunctType"),
            page_column=raw.get("pageColumn"),
            publish_time=_parse_publish_time(raw.get("announcementTime")),
        )

    @classmethod
    def from_cninfo_list(cls, raw_list: List[dict]) -> List["Announcement"]:
        """批量转换 JSON 列表。"""
        entities = []
        for raw in raw_list:
            entity = cls.from_cninfo_json(raw)
            if entity:
                entities.append(entity)
        return entities


def _build_adjunct_url(adjunct_path: str) -> str:
    if not adjunct_path:
        return ""
    if adjunct_path.startswith("http"):
        return adjunct_path
    return CNINFO_STATIC_BASE + adjunct_path.lstrip("/")


def _parse_publish_time(raw_value) -> datetime:
    if raw_value is None:
        return datetime.now()
    if isinstance(raw_value, (int, float)):
        if raw_value > 1_000_000_000_000:
            return datetime.fromtimestamp(raw_value / 1000)
        return datetime.fromtimestamp(raw_value)
    text = str(raw_value).strip()
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
        try:
            return datetime.strptime(text, fmt)
        except ValueError:
            continue
    return datetime.now()
