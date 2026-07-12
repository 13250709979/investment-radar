# Windows 上使用 Docker 安装 PostgreSQL 16（数据持久化）

## 前置条件

- 已安装 Docker Desktop
- PowerShell 或命令提示符

---

## 完整操作命令（一键复制执行）

```powershell
# 1. 清理旧容器和旧数据卷
docker rm -f postgres
docker volume rm pg_data

# 2. 创建新数据卷
docker volume create pg_data

# 3. 运行 PostgreSQL 16 容器（⚠️ 把 你的密码 改成你自己的密码）
docker run -d --name postgres -e POSTGRES_PASSWORD=123456 -p 5432:5432 -v pg_data:/var/lib/postgresql/data postgres:16

# 4. 验证容器状态
docker ps

# 5. 测试数据库连接
docker exec -it postgres psql -U postgres -c "SELECT version();"
```

---

## 创建项目数据库与用户

```powershell
docker exec -it postgres psql -U postgres -c "CREATE DATABASE investment_radar;"
docker exec -it postgres psql -U postgres -c "CREATE USER investment WITH PASSWORD '123456';"
docker exec -it postgres psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE investment_radar TO investment;"
```

或在 psql 交互终端中执行：

```sql
CREATE DATABASE investment_radar;
CREATE USER investment WITH PASSWORD '123456';
GRANT ALL PRIVILEGES ON DATABASE investment_radar TO investment;
```

---

## 初始化表结构

### 研究任务表（research_task）

```sql
CREATE TABLE research_task (
    id BIGSERIAL PRIMARY KEY,

    task_id VARCHAR(64) NOT NULL UNIQUE,

    company_name VARCHAR(255) NOT NULL,

    stock_code VARCHAR(32),

    market VARCHAR(20),

    status VARCHAR(20) NOT NULL,

    progress INT DEFAULT 0,

    report_id BIGINT,

    error_message TEXT,

    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE research_task IS '研究任务';

COMMENT ON COLUMN research_task.task_id IS '任务ID';
COMMENT ON COLUMN research_task.company_name IS '公司名称';
COMMENT ON COLUMN research_task.stock_code IS '股票代码';
COMMENT ON COLUMN research_task.market IS '市场';
COMMENT ON COLUMN research_task.status IS '任务状态';
COMMENT ON COLUMN research_task.progress IS '执行进度';
COMMENT ON COLUMN research_task.report_id IS '报告ID';
COMMENT ON COLUMN research_task.error_message IS '错误信息';

CREATE INDEX idx_task_status ON research_task(status);
CREATE INDEX idx_company_name ON research_task(company_name);
```

执行方式（在项目根目录，PowerShell）：

```powershell
Get-Content backend/docs/sql/research_task.sql | docker exec -i postgres psql -U postgres -d investment_radar
```

### 公司基础信息表（company）

```sql
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
```

执行方式（在项目根目录，PowerShell）：

```powershell
Get-Content backend/docs/sql/company.sql | docker exec -i postgres psql -U postgres -d investment_radar
```

### 研究报告表（research_report）

```sql
CREATE TABLE research_report (
    id BIGSERIAL PRIMARY KEY,

    task_id VARCHAR(64) NOT NULL,

    company_name VARCHAR(255) NOT NULL,

    report_markdown TEXT,

    ai_model VARCHAR(100),

    report_version INT DEFAULT 1,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE research_report IS 'AI研究报告';

CREATE INDEX idx_report_task ON research_report(task_id);
```

执行方式（在项目根目录，PowerShell）：

```powershell
Get-Content backend/docs/sql/research_report.sql | docker exec -i postgres psql -U postgres -d investment_radar
```

或进入 psql 后粘贴上述 SQL：

```powershell
docker exec -it postgres psql -U postgres -d investment_radar
```

授权应用用户访问表：

```sql
GRANT ALL ON SCHEMA public TO investment;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO investment;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO investment;
```

---

## 后端连接配置

在 `application.yml` 中配置如下：

```yaml
spring:
  datasource:
    url: jdbc:postgresql://localhost:5432/investment_radar
    username: investment
    password: 123456
    driver-class-name: org.postgresql.Driver
```

---

## 常用管理命令

```powershell
# 停止容器
docker stop postgres

# 启动容器
docker start postgres

# 查看日志
docker logs postgres

# 进入 psql 交互终端
docker exec -it postgres psql -U postgres
```

---

## 数据持久化说明

- 数据存储在 Docker 卷 `pg_data` 中
- 删除容器不会丢失数据：`docker rm -f postgres` 后重新 `docker run` 并挂载同一卷即可恢复
- **注意**：`docker volume rm pg_data` 会永久删除所有数据，请谨慎操作
