CREATE SCHEMA IF NOT EXISTS investment_radar;

CREATE TABLE IF NOT EXISTS investment_radar.research_task (
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

CREATE TABLE IF NOT EXISTS investment_radar.research_report (
    id              BIGSERIAL PRIMARY KEY,
    task_id         VARCHAR(64)  NOT NULL,
    company_name    VARCHAR(255) NOT NULL,
    report_markdown TEXT,
    ai_model        VARCHAR(100),
    report_version  INT DEFAULT 1,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS investment_radar.ai_analysis (
    id                 BIGSERIAL PRIMARY KEY,
    data_type          VARCHAR(50) NOT NULL,
    data_id            BIGINT NOT NULL,
    company_code       VARCHAR(20),
    company_name       VARCHAR(200),
    industry           VARCHAR(200),
    event_type         VARCHAR(100),
    event_level        SMALLINT,
    sentiment          VARCHAR(30),
    confidence         NUMERIC(5,2),
    title              TEXT,
    summary            TEXT,
    reasoning          TEXT,
    investment_opinion TEXT,
    risk_warning       TEXT,
    tags               VARCHAR(4000),
    entities           VARCHAR(4000),
    model_provider     VARCHAR(100),
    model_name         VARCHAR(100),
    prompt_version     VARCHAR(50),
    input_tokens       INTEGER,
    output_tokens      INTEGER,
    total_tokens       INTEGER,
    analysis_status    SMALLINT NOT NULL DEFAULT 1,
    error_message      TEXT,
    analysis_time      TIMESTAMP,
    create_time        TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    update_time        TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
