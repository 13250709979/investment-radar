-- ============================================================================
-- Database : investment_radar
-- Table    : investment_radar.research_report
-- ============================================================================

\c investment_radar

CREATE SCHEMA IF NOT EXISTS investment_radar;

CREATE TABLE investment_radar.research_report (
    id              BIGSERIAL PRIMARY KEY,
    task_id         VARCHAR(64)  NOT NULL,
    company_name    VARCHAR(255) NOT NULL,
    report_markdown TEXT,
    ai_model        VARCHAR(100),
    report_version  INT DEFAULT 1,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE investment_radar.research_report IS 'AI研究报告';

CREATE INDEX idx_report_task ON investment_radar.research_report (task_id);
