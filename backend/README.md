# Backend 开发指南

Spring Boot 后端项目的编译、启动、测试与 Git 提交流程。

## 环境要求

| 项 | 版本 |
|---|---|
| Spring Boot | 2.7.18 |
| JDK | 8 |
| 构建工具 | Maven 3.x |
| Group | `com.investmentradar` |
| Artifact | `backend` |
| 默认端口 | 8080 |

## 依赖

- Spring Web
- Validation
- Lombok
- PostgreSQL + MyBatis-Plus

## 文档

- [API 接口文档（含测试）](docs/api.md)
- [PostgreSQL 部署](docs/postgresql-docker.md)
- [Research MVP 设计](docs/Investment-Radar-Research-MVP.md)

## 1. 编译

```powershell
cd backend

# 仅编译
mvn compile

# 编译 + 打包（生成 target/backend-0.0.1-SNAPSHOT.jar）
mvn package
```

成功标志：终端输出 `BUILD SUCCESS`。

## 2. 启动

### 方式 A：Maven 直接启动（开发常用）

```powershell
cd backend
mvn spring-boot:run
```

### 方式 B：JAR 包启动

```powershell
cd backend
java -jar target\backend-0.0.1-SNAPSHOT.jar
```

成功标志：日志出现 `Started BackendApplication`，服务监听 `http://localhost:8080`。

### 端口被占用

```powershell
# 查看占用 8080 的进程
netstat -ano | findstr ":8080"

# 结束进程（替换为实际 PID）
taskkill /PID <PID> /F

# 再重新启动
mvn spring-boot:run
```

停止服务：在运行终端按 `Ctrl + C`。

## 3. 测试

### 单元测试

```powershell
cd backend
mvn test
```

### 接口测试（需服务已启动）

详见 [API 接口文档](docs/api.md)，快速验证：

```powershell
# 健康检查
Invoke-RestMethod -Uri http://localhost:8080/health

# 创建研究任务
$body = @{ companyName = "隆基绿能"; stockCode = "601012" } | ConvertTo-Json
Invoke-RestMethod -Uri http://localhost:8080/api/research -Method Post -ContentType "application/json" -Body $body
```

预期 `/health` 响应：

```json
{
  "code": 200,
  "message": "success",
  "data": { "status": "UP" }
}
```

## 4. Git 提交

```powershell
cd ..

# 查看变更
git status
git diff

# 暂存 backend 相关文件
git add backend/

# 提交
git commit -m "feat: 初始化 Spring Boot 后端并添加 /health 接口"

# 推送到远程（如需）
git push
```

提交前确认：

- `target/`、`.idea/`、`.venv/` 已在 `.gitignore` 中，不会被提交
- 不要提交 `.env`、密钥等敏感文件

## 完整工作流

```powershell
cd backend
mvn clean package          # 1. 编译打包
mvn test                   # 2. 跑测试
mvn spring-boot:run        # 3. 启动服务
# 浏览器或 Invoke-RestMethod 验证 /health
# Ctrl+C 停止后回到项目根目录提交
cd ..
git add backend/
git commit -m "feat: 初始化 Spring Boot 后端并添加 /health 接口"
```

## 项目结构

| 文件 | 说明 |
|------|------|
| `pom.xml` | Maven 配置（Web、Validation、Lombok） |
| `src/main/java/com/investmentradar/BackendApplication.java` | 启动类 |
| `src/main/java/com/investmentradar/controller/` | REST 接口 |
| `src/test/java/com/investmentradar/ResearchControllerTest.java` | Research 接口测试 |
| `src/main/resources/application.yml` | 应用配置（端口 8080、数据库） |
| `docs/api.md` | API 接口文档 |
