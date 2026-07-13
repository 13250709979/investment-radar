import logging
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional

from entity.announcement import Announcement
from repository.announcement_repository import AnnouncementRepository
from spider.cninfo_spider import CnInfoSpider

logger = logging.getLogger(__name__)


@dataclass
class CrawlResult:
    stock_code: str
    company_name: str
    fetched: int
    inserted: int
    skipped: int
    total_in_db: int


class AnnouncementService:
    def __init__(self):
        self.repository = AnnouncementRepository()

    def crawl_and_save(
        self,
        stock_code: str,
        company_name: str = "",
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        max_pages: Optional[int] = None,
    ) -> CrawlResult:
        stock_code = stock_code.strip()
        if not stock_code:
            raise ValueError("stock_code 不能为空")

        end_date = end_date or datetime.now().strftime("%Y-%m-%d")
        start_date = start_date or (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")

        spider = CnInfoSpider(company_name=company_name)

        # 1. 请求巨潮接口，返回 JSON
        raw_list = spider.fetch_all(
            stock_code=stock_code,
            start_date=start_date,
            end_date=end_date,
            max_pages=max_pages,
        )

        # 2. JSON 转换为 Entity
        entities = Announcement.from_cninfo_list(raw_list)

        inserted = 0
        skipped = 0
        resolved_name = company_name

        # 3. Entity 写入 PostgreSQL
        for entity in entities:
            if not resolved_name and entity.company_name:
                resolved_name = entity.company_name
            if not entity.company_code:
                entity.company_code = stock_code
            if company_name:
                entity.company_name = company_name

            if self.repository.insert(entity):
                inserted += 1
            else:
                skipped += 1

        total_in_db = self.repository.count_by_company(stock_code)
        result = CrawlResult(
            stock_code=stock_code,
            company_name=resolved_name or company_name,
            fetched=len(entities),
            inserted=inserted,
            skipped=skipped,
            total_in_db=total_in_db,
        )

        logger.info(
            "采集完成: stock=%s fetched=%s inserted=%s skipped=%s total=%s",
            result.stock_code,
            result.fetched,
            result.inserted,
            result.skipped,
            result.total_in_db,
        )
        return result
