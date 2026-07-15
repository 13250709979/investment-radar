"""批量分析入口。"""

from __future__ import annotations

import argparse
import logging
import sys

from analysis_service import AnalysisService
from config import (
    AI_BATCH_SIZE,
    activate_model,
    list_model_ids,
)
from database import check_ai_analysis_table, check_connection
from llm_client import LLMClient


def setup_logging(verbose: bool) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def parse_args():
    parser = argparse.ArgumentParser(description="Investment Radar - 公告 AI 分析")
    parser.add_argument(
        "--model",
        default="",
        help="使用的模型 id（对应 .env 中 MODEL_<ID>_；覆盖 ACTIVE_MODEL）",
    )
    parser.add_argument(
        "--list-models",
        action="store_true",
        help="列出 .env 中已配置的命名模型后退出",
    )
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

    if args.list_models:
        ids = list_model_ids()
        if not ids:
            print("未找到命名模型（MODEL_<ID>_PROVIDER）。可使用旧版扁平 MODEL_PROVIDER 配置。")
        else:
            print("已配置模型:")
            for model_id in ids:
                print(f"  - {model_id}")
            print("用法: 设置 ACTIVE_MODEL=<id>，或启动时加 --model <id>")
        return

    try:
        model_cfg = activate_model(args.model or None)
    except ValueError as exc:
        logger.error("%s", exc)
        sys.exit(1)

    if not model_cfg.api_key or model_cfg.api_key == "your_api_key_here":
        if model_cfg.id == "legacy":
            logger.error("请先在 ai/.env 配置有效 API_KEY")
        else:
            logger.error(
                "请先在 ai/.env 配置有效 API_KEY（当前模型 id=%s，变量 MODEL_%s_API_KEY）",
                model_cfg.id,
                model_cfg.id.upper(),
            )
        sys.exit(1)

    if not check_connection() or not check_ai_analysis_table():
        sys.exit(1)

    logger.info(
        "ActiveModel=%s Provider=%s Model=%s",
        model_cfg.id,
        model_cfg.provider,
        model_cfg.model_name,
    )
    service = AnalysisService(llm=LLMClient(model=model_cfg))

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
