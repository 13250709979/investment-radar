-- =============================================
-- Project  : Investment Radar
-- Database : investment_radar
-- Schema   : investment
-- Table    : announcement
-- Description : 上市公司公告原始信息
-- PostgreSQL 16+
-- =============================================

CREATE SCHEMA IF NOT EXISTS investment_radar;


CREATE TABLE IF NOT EXISTS investment_radar.announcement
(
    id                  BIGSERIAL PRIMARY KEY,

    announcement_id     VARCHAR(64) NOT NULL,

    company_code        VARCHAR(10) NOT NULL,

    company_name        VARCHAR(100) NOT NULL,

    title               TEXT NOT NULL,

    announcement_type   VARCHAR(100),

    adjunct_url         TEXT NOT NULL,

    adjunct_size        BIGINT,

    adjunct_type        VARCHAR(20),

    page_column         VARCHAR(100),

    publish_time        TIMESTAMP NOT NULL,

    crawl_time          TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    ai_status           SMALLINT NOT NULL DEFAULT 0,

    pdf_download_status SMALLINT NOT NULL DEFAULT 0,

    deleted             BOOLEAN NOT NULL DEFAULT FALSE,

    create_time         TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    update_time         TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE investment_radar.announcement
    ADD CONSTRAINT uk_announcement_notice
    UNIQUE (announcement_id);

CREATE INDEX idx_announcement_company_code
    ON investment_radar.announcement(company_code);

CREATE INDEX idx_announcement_company_name
    ON investment_radar.announcement(company_name);

CREATE INDEX idx_announcement_publish_time
    ON investment_radar.announcement(publish_time DESC);

CREATE INDEX idx_announcement_ai_status
    ON investment_radar.announcement(ai_status);

CREATE INDEX idx_announcement_pdf_status
    ON investment_radar.announcement(pdf_download_status);

CREATE INDEX idx_announcement_deleted
    ON investment_radar.announcement(deleted);

COMMENT ON TABLE investment_radar.announcement IS '上市公司公告原始数据';

COMMENT ON COLUMN investment_radar.announcement.id IS '主键ID';

COMMENT ON COLUMN investment_radar.announcement.announcement_id IS '巨潮公告唯一ID';

COMMENT ON COLUMN investment_radar.announcement.company_code IS '股票代码';

COMMENT ON COLUMN investment_radar.announcement.company_name IS '公司名称';

COMMENT ON COLUMN investment_radar.announcement.title IS '公告标题';

COMMENT ON COLUMN investment_radar.announcement.announcement_type IS '公告类型';

COMMENT ON COLUMN investment_radar.announcement.adjunct_url IS '公告PDF地址';

COMMENT ON COLUMN investment_radar.announcement.adjunct_size IS 'PDF文件大小(Byte)';

COMMENT ON COLUMN investment_radar.announcement.adjunct_type IS '附件类型(PDF等)';

COMMENT ON COLUMN investment_radar.announcement.page_column IS '公告栏目';

COMMENT ON COLUMN investment_radar.announcement.publish_time IS '公告发布时间';

COMMENT ON COLUMN investment_radar.announcement.crawl_time IS '采集时间';

COMMENT ON COLUMN investment_radar.announcement.ai_status IS 'AI分析状态：0未分析 1分析成功 2分析失败';

COMMENT ON COLUMN investment_radar.announcement.pdf_download_status IS 'PDF下载状态：0未下载 1已下载 2下载失败';

COMMENT ON COLUMN investment_radar.announcement.deleted IS '逻辑删除';

COMMENT ON COLUMN investment_radar.announcement.create_time IS '创建时间';

COMMENT ON COLUMN investment_radar.announcement.update_time IS '更新时间';