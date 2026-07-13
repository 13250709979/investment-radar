import logging
from datetime import datetime
from typing import List, Optional, Tuple

from config import CNINFO_QUERY_URL, DEFAULT_PAGE_SIZE
from entity.announcement import Announcement
from utils.http_util import create_session, post_form, sleep_between_requests
from utils.orgid_util import build_stock_param

logger = logging.getLogger(__name__)


class CnInfoSpider:
    """巨潮资讯网公告爬虫，负责请求接口并返回原始 JSON。"""

    def __init__(self, page_size: int = DEFAULT_PAGE_SIZE, company_name: str = ""):
        self.page_size = page_size
        self.company_name = company_name
        self.session = create_session(company_name)
        self._warm_up()

    def _warm_up(self):
        """访问首页获取 Cookie。"""
        try:
            self.session.get("https://www.cninfo.com.cn/new/index", timeout=20)
        except Exception as exc:
            logger.warning("巨潮首页预热失败: %s", exc)

    def fetch_page(
        self,
        stock_code: str,
        page_num: int,
        start_date: str,
        end_date: str,
    ) -> Tuple[List[dict], bool]:
        stock_param = build_stock_param(self.session, stock_code)

        # 参考浏览器 curl：核心参数为 stock + pageNum + pageSize
        payload = {
            "stock": stock_param,
            "pageNum": page_num,
            "pageSize": self.page_size,
        }
        if start_date and end_date:
            payload["seDate"] = f"{start_date}~{end_date}"

        logger.info(
            "请求巨潮接口: url=%s stock=%s page=%s payload=%s",
            CNINFO_QUERY_URL,
            stock_param,
            page_num,
            payload,
        )

        data = post_form(self.session, CNINFO_QUERY_URL, payload)
        raw_list = data.get("announcements") or []
        has_more = bool(data.get("hasMore"))
        total = data.get("totalAnnouncement") or data.get("totalRecordNum") or 0

        logger.info(
            "第 %s 页返回 %s 条 JSON 记录（接口总计 %s 条）",
            page_num,
            len(raw_list),
            total,
        )

        sleep_between_requests()
        return raw_list, has_more

    def fetch_all(
        self,
        stock_code: str,
        start_date: str,
        end_date: str,
        max_pages: Optional[int] = None,
    ) -> List[dict]:
        all_raw: List[dict] = []
        page_num = 1
        start_dt = datetime.strptime(start_date, "%Y-%m-%d")
        end_dt = datetime.strptime(end_date, "%Y-%m-%d").replace(
            hour=23, minute=59, second=59
        )

        while True:
            raw_list, has_more = self.fetch_page(
                stock_code=stock_code,
                page_num=page_num,
                start_date=start_date,
                end_date=end_date,
            )

            if not raw_list:
                break

            # 按日期过滤（接口分页按时间倒序）
            stop = False
            for raw in raw_list:
                entity = Announcement.from_cninfo_json(raw)
                if not entity:
                    continue
                if entity.publish_time < start_dt:
                    stop = True
                    break
                if entity.publish_time <= end_dt:
                    all_raw.append(raw)

            if stop:
                break
            if not has_more:
                break
            if max_pages and page_num >= max_pages:
                break

            page_num += 1

        logger.info("共获取 %s 条 JSON 记录", len(all_raw))
        return all_raw
