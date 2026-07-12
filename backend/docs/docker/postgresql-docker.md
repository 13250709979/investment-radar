# PostgreSQL Docker 部署指南

Windows + Docker Desktop + PostgreSQL 16，数据持久化到 Docker 卷。

## 环境要求

- Docker Desktop 已安装并运行
- PowerShell

## 连接信息

| 项 | 值 |
|---|---|
| 容器名 | `postgres` |
| 端口 | `5432` |
| 数据库 | `investment_radar` |
| Schema | `investment_radar` |
| 应用用户 | `investment` / `123456` |
| 超级用户 | `postgres` / `123456` |

---

## 1. 启动 PostgreSQL

```powershell
# 清理旧环境（⚠️ docker volume rm 会删除所有数据）
docker rm -f postgres
docker volume rm pg_data

# 创建数据卷并启动容器
docker volume create pg_data
docker run -d `
  --name postgres `
  -e POSTGRES_PASSWORD=123456 `
  -p 5432:5432 `
  -v pg_data:/var/lib/postgresql/data `
  postgres:16

# 验证
docker ps
docker exec -it postgres psql -U postgres -c "SELECT version();"
```

---

## 2. 创建数据库与用户

```powershell
docker exec -it postgres psql -U postgres -c "CREATE DATABASE investment_radar;"
docker exec -it postgres psql -U postgres -c "CREATE USER investment WITH PASSWORD '123456';"
docker exec -it postgres psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE investment_radar TO investment;"
```

---

## 3. 初始化表结构

SQL 脚本位于 `backend/docs/sql/`，表均建在 `investment_radar` schema 下。

| 脚本 | 表 |
|------|-----|
| `research_task.sql` | `investment_radar.research_task` |
| `research_report.sql` | `investment_radar.research_report` |
| `company.sql` | `investment_radar.company` |

**在项目根目录执行（PowerShell）：**

```powershell
Get-Content backend/docs/sql/research_task.sql   | docker exec -i postgres psql -U postgres
Get-Content backend/docs/sql/research_report.sql | docker exec -i postgres psql -U postgres
Get-Content backend/docs/sql/company.sql         | docker exec -i postgres psql -U postgres
```

> `research_task.sql` 末尾已包含 schema 授权，`investment` 用户可直接读写表。

**进入 psql 交互终端：**

```powershell
docker exec -it postgres psql -U postgres -d investment_radar
```

**查看已创建的表：**

```sql
\dt investment_radar.*
```

---

## 4. 后端配置

`backend/src/main/resources/application.yml`：

```yaml
spring:
  datasource:
    url: jdbc:postgresql://localhost:5432/investment_radar?currentSchema=investment_radar
    username: investment
    password: 123456
    driver-class-name: org.postgresql.Driver
```

启动后端时会自动检查数据库连接，连接失败则应用无法启动。

---

## 5. 常用命令

```powershell
docker start postgres          # 启动
docker stop postgres           # 停止
docker logs postgres           # 查看日志
docker exec -it postgres psql -U postgres -d investment_radar   # 进入 psql
```

---

## 注意事项

- 数据持久化在 Docker 卷 `pg_data`，删除容器不丢数据
- `docker volume rm pg_data` 会**永久删除**所有数据，慎用
- PostgreSQL 中 `investment_radar.表名` 表示 **schema.表名**，非 MySQL 的 `库.表` 写法
- 若报 `relation "research_task" does not exist`，请确认已执行第 3 步建表脚本

## 相关文档

- [API 接口文档](api.md)
- [Research MVP 设计](Investment-Radar-Research-MVP.md)
