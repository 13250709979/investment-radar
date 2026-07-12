-- ============================================================================
-- Database : investment_radar
-- Table    : investment_radar.company
-- ============================================================================

\c investment_radar

CREATE SCHEMA IF NOT EXISTS investment_radar;

CREATE TABLE investment_radar.company (
    id           BIGSERIAL PRIMARY KEY,
    company_name VARCHAR(255) NOT NULL,
    stock_code   VARCHAR(32) UNIQUE,
    market       VARCHAR(20),
    industry     VARCHAR(200),
    website      VARCHAR(255),
    description  TEXT,
    created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE investment_radar.company IS '公司基础信息';

CREATE INDEX idx_stock_code ON investment_radar.company (stock_code);
