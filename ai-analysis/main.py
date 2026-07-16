"""???????"""

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
    p = argparse.ArgumentParser(description="Investment Radar - ?? AI ??")
    p.add_argument("--model", default="", help="?? id??? ACTIVE_MODEL")
    p.add_argument("--list-models", action="store_true", help="???????")
    p.add_argument("--company-code", default="", help="?????????")
    p.add_argument("--limit", type=int, default=AI_BATCH_SIZE, help="????")
    p.add_argument("--loops", type=int, default=1, help="????0=??????")
    p.add_argument("--verbose", action="store_true")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    setup_logging(args.verbose)
    logger = logging.getLogger(__name__)

    if args.list_models:
        ids = list_model_ids()
        print("?????:" if ids else "???????????? MODEL_PROVIDER ???")
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
        logger.error("?? ai-analysis/.env ???? %s", hint)
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
            logger.info("?????????")
            break
        if args.loops == 0 and result.total < args.limit:
            break

    print("=" * 50)
    print(f"???? : {total}")
    print(f"??     : {success}")
    print(f"??     : {failed}")
    print("=" * 50)


if __name__ == "__main__":
    main()
