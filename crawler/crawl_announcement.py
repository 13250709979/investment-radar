import argparse
import logging
import sys
from datetime import datetime, timedelta

from core.database import check_announcement_table, check_connection
from service.crawl_service import CrawlService


def setup_logging(verbose: bool):
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def parse_args():
    parser = argparse.ArgumentParser(description="Investment Radar - 巨潮公告采集")
    parser.add_argument("--stock-code", required=True, help="股票代码，如 601012")
    parser.add_argument("--company-name", default="", help="公司名称，如 隆基绿能")
    parser.add_argument(
        "--start-date",
        default=(datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d"),
        help="开始日期 YYYY-MM-DD，默认一年前",
    )
    parser.add_argument(
        "--end-date",
        default=datetime.now().strftime("%Y-%m-%d"),
        help="结束日期 YYYY-MM-DD，默认今天",
    )
    parser.add_argument("--max-pages", type=int, default=None, help="最大抓取页数")
    parser.add_argument("--verbose", action="store_true", help="输出调试日志")
    return parser.parse_args()


def main():
    args = parse_args()
    setup_logging(args.verbose)

    if not check_connection() or not check_announcement_table():
        sys.exit(1)

    service = CrawlService()
    result = service.crawl_and_save(
        stock_code=args.stock_code,
        company_name=args.company_name,
        start_date=args.start_date,
        end_date=args.end_date,
        max_pages=args.max_pages,
    )

    print("=" * 50)
    print(f"股票代码 : {result.stock_code}")
    print(f"公司名称 : {result.company_name or '-'}")
    print(f"抓取数量 : {result.fetched}")
    print(f"新增入库 : {result.inserted}")
    print(f"重复跳过 : {result.skipped}")
    print(f"库内总数 : {result.total_in_db}")
    print("=" * 50)


if __name__ == "__main__":
    main()
