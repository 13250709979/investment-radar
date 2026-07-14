"""写入 ai_analysis，并更新 announcement.ai_status。"""

from __future__ import annotations

import json
import logging
from typing import Any

from psycopg2.extras import Json

from config import DB_SCHEMA
from database import transaction

logger = logging.getLogger(__name__)


class AiRepository:
    def save_success(
        self,
        announcement: dict,
        llm_data: dict[str, Any],
        *,
        model_provider: str,
        model_name: str,
        prompt_version: str,
        input_tokens: int,
        output_tokens: int,
        total_tokens: int,
    ) -> None:
        """事务：写入成功分析结果，再更新 announcement.ai_status=1。"""
        company_name = announcement.get("company_name") or llm_data.get("company") or ""
        tags = llm_data.get("tags") or []

        insert_sql = f"""
            INSERT INTO {DB_SCHEMA}.ai_analysis (
                data_type,
                data_id,
                company_code,
                company_name,
                industry,
                event_type,
                event_level,
                sentiment,
                title,
                summary,
                reasoning,
                investment_opinion,
                risk_warning,
                tags,
                model_provider,
                model_name,
                prompt_version,
                input_tokens,
                output_tokens,
                total_tokens,
                analysis_status,
                error_message,
                analysis_time,
                create_time,
                update_time
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                1, NULL, NOW(), NOW(), NOW()
            )
        """
        update_sql = f"""
            UPDATE {DB_SCHEMA}.announcement
            SET ai_status = 1, update_time = NOW()
            WHERE id = %s
        """

        with transaction() as (_conn, cursor):
            cursor.execute(
                insert_sql,
                (
                    "ANNOUNCEMENT",
                    announcement["id"],
                    announcement.get("company_code"),
                    company_name,
                    llm_data.get("industry") or "",
                    llm_data.get("eventType") or "",
                    llm_data.get("importance"),
                    llm_data.get("sentiment") or "",
                    announcement.get("title") or "",
                    llm_data.get("summary") or "",
                    llm_data.get("reasoning") or "",
                    llm_data.get("investmentOpinion") or "",
                    llm_data.get("riskWarning") or "",
                    Json(tags),
                    model_provider,
                    model_name,
                    prompt_version,
                    input_tokens,
                    output_tokens,
                    total_tokens,
                ),
            )
            cursor.execute(update_sql, (announcement["id"],))

        logger.info(
            "已保存分析结果 announcement_id=%s tags=%s",
            announcement["id"],
            json.dumps(tags, ensure_ascii=False),
        )

    def save_failure(
        self,
        announcement: dict,
        error_message: str,
        *,
        model_provider: str,
        model_name: str,
        prompt_version: str,
        input_tokens: int = 0,
        output_tokens: int = 0,
        total_tokens: int = 0,
        update_announcement_status: bool = True,
    ) -> None:
        """写入失败记录；重试超限时可同步将 announcement.ai_status=2。"""
        insert_sql = f"""
            INSERT INTO {DB_SCHEMA}.ai_analysis (
                data_type,
                data_id,
                company_code,
                company_name,
                title,
                model_provider,
                model_name,
                prompt_version,
                input_tokens,
                output_tokens,
                total_tokens,
                analysis_status,
                error_message,
                analysis_time,
                create_time,
                update_time
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                2, %s, NOW(), NOW(), NOW()
            )
        """
        update_sql = f"""
            UPDATE {DB_SCHEMA}.announcement
            SET ai_status = 2, update_time = NOW()
            WHERE id = %s
        """

        with transaction() as (_conn, cursor):
            cursor.execute(
                insert_sql,
                (
                    "ANNOUNCEMENT",
                    announcement["id"],
                    announcement.get("company_code"),
                    announcement.get("company_name"),
                    announcement.get("title") or "",
                    model_provider,
                    model_name,
                    prompt_version,
                    input_tokens,
                    output_tokens,
                    total_tokens,
                    (error_message or "")[:2000],
                ),
            )
            if update_announcement_status:
                cursor.execute(update_sql, (announcement["id"],))

        logger.warning(
            "已记录分析失败 announcement_id=%s err=%s",
            announcement["id"],
            error_message,
        )
