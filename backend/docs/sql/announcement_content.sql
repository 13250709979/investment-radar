-- =============================================
-- Project  : Investment Radar
-- Database : investment_radar
-- Schema   : investment
-- Table    : announcement_content
-- Description : 公告正文（PDF解析）
-- PostgreSQL 16+
-- =============================================

CREATE TABLE IF NOT EXISTS investment_radar.announcement_content
(
    id                  BIGSERIAL PRIMARY KEY,

    announcement_id     BIGINT NOT NULL,

    pdf_url             TEXT NOT NULL,

    pdf_file_name       VARCHAR(500),

    pdf_local_path      TEXT,

    pdf_size            BIGINT,

    pdf_md5             VARCHAR(32),

    content             TEXT,

    page_count          INTEGER,

    parser_name         VARCHAR(100),

    parser_version      VARCHAR(50),

    parse_status        SMALLINT NOT NULL DEFAULT 0,

    parse_message       TEXT,

    parse_time          TIMESTAMP,

    create_time         TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    update_time         TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_announcement_content_announcement
        FOREIGN KEY (announcement_id)
        REFERENCES investment_radar.announcement(id)
        ON DELETE CASCADE
);

CREATE UNIQUE INDEX uk_announcement_content_notice
    ON investment_radar.announcement_content(announcement_id);

CREATE INDEX idx_announcement_content_parse_status
    ON investment_radar.announcement_content(parse_status);

CREATE INDEX idx_announcement_content_parse_time
    ON investment_radar.announcement_content(parse_time DESC);

COMMENT ON TABLE investment_radar.announcement_content IS '公告PDF解析内容';

COMMENT ON COLUMN investment_radar.announcement_content.id IS '主键ID';

COMMENT ON COLUMN investment_radar.announcement_content.announcement_id IS '公告主表ID';

COMMENT ON COLUMN investment_radar.announcement_content.pdf_url IS 'PDF下载地址';

COMMENT ON COLUMN investment_radar.announcement_content.pdf_file_name IS 'PDF文件名称';

COMMENT ON COLUMN investment_radar.announcement_content.pdf_local_path IS 'PDF本地存储路径';

COMMENT ON COLUMN investment_radar.announcement_content.pdf_size IS 'PDF文件大小(Byte)';

COMMENT ON COLUMN investment_radar.announcement_content.pdf_md5 IS 'PDF文件MD5，用于文件去重';

COMMENT ON COLUMN investment_radar.announcement_content.content IS 'PDF解析后的正文';

COMMENT ON COLUMN investment_radar.announcement_content.page_count IS 'PDF页数';

COMMENT ON COLUMN investment_radar.announcement_content.parser_name IS 'PDF解析器名称，例如PyMuPDF、pdfplumber';

COMMENT ON COLUMN investment_radar.announcement_content.parser_version IS 'PDF解析器版本';

COMMENT ON COLUMN investment_radar.announcement_content.parse_status IS '解析状态：0-未解析，1-解析成功，2-解析失败';

COMMENT ON COLUMN investment_radar.announcement_content.parse_message IS '解析失败原因或处理日志';

COMMENT ON COLUMN investment_radar.announcement_content.parse_time IS '解析完成时间';

COMMENT ON COLUMN investment_radar.announcement_content.create_time IS '创建时间';

COMMENT ON COLUMN investment_radar.announcement_content.update_time IS '更新时间';