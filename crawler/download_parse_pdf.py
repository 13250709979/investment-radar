import argparse
import logging
import sys

from core.config import PDF_BATCH_LIMIT
from core.database import (
    check_announcement_content_table,
    check_announcement_table,
    check_connection,
)
from service.pdf_parse_service import PdfParseService


def setup_logging(verbose: bool):
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def parse_args():
    parser = argparse.ArgumentParser(description="Investment Radar - 公告 PDF 下载解析")
    parser.add_argument("--company-code", default="", help="仅处理指定股票代码")
    parser.add_argument("--limit", type=int, default=PDF_BATCH_LIMIT, help="单次处理条数")
    parser.add_argument("--verbose", action="store_true", help="输出调试日志")
    return parser.parse_args()


def main():
    args = parse_args()
    setup_logging(args.verbose)

    if not check_connection() or not check_announcement_table() or not check_announcement_content_table():
        sys.exit(1)

    service = PdfParseService()
    result = service.process_pending(
        limit=args.limit,
        company_code=args.company_code or None,
    )

    print("=" * 50)
    print(f"待处理   : {result.total}")
    print(f"成功     : {result.success}")
    print(f"下载失败 : {result.download_failed}")
    print(f"解析失败 : {result.parse_failed}")
    print("=" * 50)


if __name__ == "__main__":
    main()
