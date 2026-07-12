CREATE TABLE company (
    id BIGSERIAL PRIMARY KEY,

    company_name VARCHAR(255) NOT NULL,

    stock_code VARCHAR(32) UNIQUE,

    market VARCHAR(20),

    industry VARCHAR(200),

    website VARCHAR(255),

    description TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE company IS '公司基础信息';

CREATE INDEX idx_stock_code ON company(stock_code);
