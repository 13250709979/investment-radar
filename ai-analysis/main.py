"""批量分析入口。"""

from __future__ import annotations

import argparse
import logging
import sys

from core.config import AI_BATCH_SIZE, list_model_ids, resolve_model
from core.database import check_ai_analysis_table, check_connection
from llm.client import LLMClient
from service.analysis_service import AnalysisService


def setup_logging(verbose: bool) -> None:
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Investment Radar - 公告 AI 分析")
    p.add_argument("--model", default="", help="模型 id，覆盖 ACTIVE_MODEL")
    p.add_argument("--list-models", action="store_true", help="列出已配置模型")
    p.add_argument("--company-code", default="", help="仅分析指定股票代码")
    p.add_argument("--limit", type=int, default=AI_BATCH_SIZE, help="单批条数")
    p.add_argument("--loops", type=int, default=1, help="批次数，0=直到无待分析")
    p.add_argument("--verbose", action="store_true")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    setup_logging(args.verbose)
    logger = logging.getLogger(__name__)

    if args.list_models:
        ids = list_model_ids()
        print("已配置模型:" if ids else "未找到命名模型（可用扁平 MODEL_PROVIDER 配置）")
        for mid in ids:
            print(f"  - {mid}")
        return

    try:
        model = resolve_model(args.model or None)
    except ValueError as exc:
        logger.error("%s", exc)
        sys.exit(1)

    if not model.api_key or model.api_key == "your_api_key_here":
        hint = "API_KEY" if model.id == "default" else f"MODEL_{model.id.upper()}_API_KEY"
        logger.error("请在 ai-analysis/.env 配置有效 %s", hint)
        sys.exit(1)

    if not check_connection() or not check_ai_analysis_table():
        sys.exit(1)

    logger.info("Model=%s Provider=%s Name=%s", model.id, model.provider, model.model_name)
    service = AnalysisService(llm=LLMClient(model=model))

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
