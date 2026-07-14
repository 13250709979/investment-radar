"""批量分析入口。"""

from __future__ import annotations

import argparse
import logging
import sys

from analysis_service import AnalysisService
from config import AI_BATCH_SIZE, API_KEY, MODEL_NAME, MODEL_PROVIDER
from database import check_ai_analysis_table, check_connection


def setup_logging(verbose: bool) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def parse_args():
    parser = argparse.ArgumentParser(description="Investment Radar - 公告 AI 分析")
    parser.add_argument("--company-code", default="", help="仅分析指定股票代码")
    parser.add_argument(
        "--limit",
        type=int,
        default=AI_BATCH_SIZE,
        help=f"单批处理条数，默认 {AI_BATCH_SIZE}",
    )
    parser.add_argument(
        "--loops",
        type=int,
        default=1,
        help="连续拍取批次数，0 表示直到无待分析数据",
    )
    parser.add_argument("--verbose", action="store_true", help="输出调试日志")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    setup_logging(args.verbose)
    logger = logging.getLogger(__name__)

    if not API_KEY or API_KEY == "your_api_key_here":
        logger.error("请先在 ai/.env 配置有效 API_KEY")
        sys.exit(1)

    if not check_connection() or not check_ai_analysis_table():
        sys.exit(1)

    logger.info("Provider=%s Model=%s", MODEL_PROVIDER, MODEL_NAME)
    service = AnalysisService()

    total = success = failed = 0
    loop = 0
    while True:
        loop += 1
        if args.loops != 0 and loop > args.loops:
            break

        result = service.run_batch(
            limit=args.limit,
            company_code=args.company_code or None,
        )
        total += result.total
        success += result.success
        failed += result.failed

        if result.total == 0:
            logger.info("无待分析公告，结束")
            break
        if args.loops == 0 and result.total < args.limit:
            break

    print("=" * 50)
    print(f"处理总计 : {total}")
    print(f"成功     : {success}")
    print(f"失败     : {failed}")
    print("=" * 50)


if __name__ == "__main__":
    main()
