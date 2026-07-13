-- =============================================
-- Project  : Investment Radar
-- Database : investment_radar
-- Schema   : investment
-- Table    : ai_analysis
-- Description : AI分析结果
-- PostgreSQL 16+
-- =============================================

CREATE TABLE IF NOT EXISTS investment_radar.ai_analysis
(
    id                      BIGSERIAL PRIMARY KEY,

    data_type               VARCHAR(50) NOT NULL,

    data_id                 BIGINT NOT NULL,

    company_code            VARCHAR(20),

    company_name            VARCHAR(200),

    industry                VARCHAR(200),

    event_type              VARCHAR(100),

    event_level             SMALLINT,

    sentiment               VARCHAR(30),

    confidence              NUMERIC(5,2),

    title                   TEXT,

    summary                 TEXT,

    reasoning               TEXT,

    investment_opinion      TEXT,

    risk_warning            TEXT,

    tags                    JSONB,

    entities                JSONB,

    model_provider          VARCHAR(100),

    model_name              VARCHAR(100),

    prompt_version          VARCHAR(50),

    input_tokens            INTEGER,

    output_tokens           INTEGER,

    total_tokens            INTEGER,

    analysis_status         SMALLINT NOT NULL DEFAULT 1,

    error_message           TEXT,

    analysis_time           TIMESTAMP,

    create_time             TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    update_time             TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_ai_analysis_data
ON investment_radar.ai_analysis(data_type, data_id);

CREATE INDEX idx_ai_analysis_company_code
ON investment_radar.ai_analysis(company_code);

CREATE INDEX idx_ai_analysis_company_name
ON investment_radar.ai_analysis(company_name);

CREATE INDEX idx_ai_analysis_industry
ON investment_radar.ai_analysis(industry);

CREATE INDEX idx_ai_analysis_event_type
ON investment_radar.ai_analysis(event_type);

CREATE INDEX idx_ai_analysis_event_level
ON investment_radar.ai_analysis(event_level);

CREATE INDEX idx_ai_analysis_status
ON investment_radar.ai_analysis(analysis_status);

CREATE INDEX idx_ai_analysis_analysis_time
ON investment_radar.ai_analysis(analysis_time DESC);

CREATE INDEX idx_ai_analysis_tags
ON investment_radar.ai_analysis
USING GIN(tags);

CREATE INDEX idx_ai_analysis_entities
ON investment_radar.ai_analysis
USING GIN(entities);

COMMENT ON TABLE investment_radar.ai_analysis IS 'AI分析结果';

COMMENT ON COLUMN investment_radar.ai_analysis.id IS '主键ID';

COMMENT ON COLUMN investment_radar.ai_analysis.data_type IS '数据来源类型：ANNOUNCEMENT、NEWS、POLICY、COMPANY_NEWS';

COMMENT ON COLUMN investment_radar.ai_analysis.data_id IS '原始数据ID';

COMMENT ON COLUMN investment_radar.ai_analysis.company_code IS '股票代码';

COMMENT ON COLUMN investment_radar.ai_analysis.company_name IS '公司名称';

COMMENT ON COLUMN investment_radar.ai_analysis.industry IS '所属行业';

COMMENT ON COLUMN investment_radar.ai_analysis.event_type IS '事件类型，如扩产、并购、中标、回购、业绩预增';

COMMENT ON COLUMN investment_radar.ai_analysis.event_level IS '事件重要等级（1-5，5最高）';

COMMENT ON COLUMN investment_radar.ai_analysis.sentiment IS '情绪分析：POSITIVE、NEUTRAL、NEGATIVE';

COMMENT ON COLUMN investment_radar.ai_analysis.confidence IS 'AI分析置信度（0~100）';

COMMENT ON COLUMN investment_radar.ai_analysis.title IS 'AI生成标题';

COMMENT ON COLUMN investment_radar.ai_analysis.summary IS 'AI摘要';

COMMENT ON COLUMN investment_radar.ai_analysis.reasoning IS 'AI分析理由';

COMMENT ON COLUMN investment_radar.ai_analysis.investment_opinion IS '投资观点';

COMMENT ON COLUMN investment_radar.ai_analysis.risk_warning IS '风险提示';

COMMENT ON COLUMN investment_radar.ai_analysis.tags IS 'AI标签(JSON数组)';

COMMENT ON COLUMN investment_radar.ai_analysis.entities IS 'AI识别实体(JSON对象)';

COMMENT ON COLUMN investment_radar.ai_analysis.model_provider IS '模型提供商，如OpenAI、DeepSeek、Qwen';

COMMENT ON COLUMN investment_radar.ai_analysis.model_name IS '模型名称';

COMMENT ON COLUMN investment_radar.ai_analysis.prompt_version IS 'Prompt版本';

COMMENT ON COLUMN investment_radar.ai_analysis.input_tokens IS '输入Token数量';

COMMENT ON COLUMN investment_radar.ai_analysis.output_tokens IS '输出Token数量';

COMMENT ON COLUMN investment_radar.ai_analysis.total_tokens IS '总Token数量';

COMMENT ON COLUMN investment_radar.ai_analysis.analysis_status IS '分析状态：1成功，2失败';

COMMENT ON COLUMN investment_radar.ai_analysis.error_message IS '分析失败原因';

COMMENT ON COLUMN investment_radar.ai_analysis.analysis_time IS 'AI分析完成时间';

COMMENT ON COLUMN investment_radar.ai_analysis.create_time IS '创建时间';

COMMENT ON COLUMN investment_radar.ai_analysis.update_time IS '更新时间';