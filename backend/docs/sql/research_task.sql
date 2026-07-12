-- ============================================================================
-- Database : investment_radar
-- Table    : investment_radar.research_task
-- ============================================================================

\c investment_radar

CREATE SCHEMA IF NOT EXISTS investment_radar;

CREATE TABLE investment_radar.research_task (
    id            BIGSERIAL PRIMARY KEY,
    task_id       VARCHAR(64)  NOT NULL UNIQUE,
    company_name  VARCHAR(255) NOT NULL,
    stock_code    VARCHAR(32),
    market        VARCHAR(20),
    status        VARCHAR(20)  NOT NULL,
    progress      INT DEFAULT 0,
    report_id     BIGINT,
    error_message TEXT,
    created_at    TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at    TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE investment_radar.research_task IS '研究任务';

COMMENT ON COLUMN investment_radar.research_task.task_id       IS '任务ID';
COMMENT ON COLUMN investment_radar.research_task.company_name  IS '公司名称';
COMMENT ON COLUMN investment_radar.research_task.stock_code    IS '股票代码';
COMMENT ON COLUMN investment_radar.research_task.market        IS '市场';
COMMENT ON COLUMN investment_radar.research_task.status        IS '任务状态';
COMMENT ON COLUMN investment_radar.research_task.progress      IS '执行进度';
COMMENT ON COLUMN investment_radar.research_task.report_id     IS '报告ID';
COMMENT ON COLUMN investment_radar.research_task.error_message IS '错误信息';

CREATE INDEX idx_task_status  ON investment_radar.research_task (status);
CREATE INDEX idx_company_name ON investment_radar.research_task (company_name);

GRANT ALL ON SCHEMA investment_radar TO investment;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA investment_radar TO investment;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA investment_radar TO investment;
