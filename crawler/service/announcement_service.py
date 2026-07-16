"""Announcement crawl orchestration: spider -> entity -> DB."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import datetime, timedelta

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
    def __init__(self, repository: AnnouncementRepository | None = None):
        self.repository = repository or AnnouncementRepository()

    def crawl_and_save(
        self,
        stock_code: str,
        company_name: str = "",
        start_date: str | None = None,
        end_date: str | None = None,
        max_pages: int | None = None,
    ) -> CrawlResult:
        stock_code = stock_code.strip()
        if not stock_code:
            raise ValueError("stock_code is required")

        end_date = end_date or datetime.now().strftime("%Y-%m-%d")
        start_date = start_date or (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")

        # 1) fetch JSON  2) to entities  3) insert
        raw_list = CnInfoSpider(company_name=company_name).fetch_all(
            stock_code=stock_code,
            start_date=start_date,
            end_date=end_date,
            max_pages=max_pages,
        )
        entities = Announcement.from_cninfo_list(raw_list)

        inserted = skipped = 0
        resolved_name = company_name
        for entity in entities:
            if not resolved_name and entity.company_name:
                resolved_name = entity.company_name
            entity.company_code = entity.company_code or stock_code
            if company_name:
                entity.company_name = company_name

            if self.repository.insert(entity):
                inserted += 1
            else:
                skipped += 1

        result = CrawlResult(
            stock_code=stock_code,
            company_name=resolved_name or company_name,
            fetched=len(entities),
            inserted=inserted,
            skipped=skipped,
            total_in_db=self.repository.count_by_company(stock_code),
        )
        logger.info(
            "crawl done: stock=%s fetched=%s inserted=%s skipped=%s total=%s",
            result.stock_code,
            result.fetched,
            result.inserted,
            result.skipped,
            result.total_in_db,
        )
        return result
