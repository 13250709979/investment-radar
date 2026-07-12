# API 接口文档

Base URL：`http://localhost:8080`

统一响应格式：

```json
{
  "code": 200,
  "message": "success",
  "data": {}
}
```

| code | 说明 |
|------|------|
| 200 | 成功 |
| 400 | 请求参数错误 |
| 404 | 资源不存在 |
| 500 | 系统异常 |

---

## 1. 健康检查

### `GET /health`

检查服务是否正常运行。

**响应示例：**

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "status": "UP"
  }
}
```

**手动测试（PowerShell）：**

```powershell
Invoke-RestMethod -Uri http://localhost:8080/health
```

---

## 2. 创建研究任务

### `POST /api/research`

创建研究任务，返回 `taskId`，不直接执行 AI 分析。

**请求头：**

```
Content-Type: application/json
```

**请求体：**

```json
{
  "companyName": "隆基绿能",
  "stockCode": "601012"
}
```

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| companyName | string | 是 | 公司名称 |
| stockCode | string | 否 | 股票代码 |

**响应示例：**

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "taskId": "7d4fd5d2-4e7d-4c87-84a8-2ec8d55b9f60",
    "status": "PENDING"
  }
}
```

**任务状态枚举：**

- `PENDING` — 待处理
- `RUNNING` — 执行中
- `SUCCESS` — 成功
- `FAILED` — 失败

**手动测试（PowerShell）：**

```powershell
$body = @{
  companyName = "隆基绿能"
  stockCode   = "601012"
} | ConvertTo-Json

Invoke-RestMethod -Uri http://localhost:8080/api/research `
  -Method Post `
  -ContentType "application/json" `
  -Body $body
```

**参数校验失败（400）：**

```json
{
  "code": 400,
  "message": "companyName: 公司名称不能为空",
  "data": null
}
```

---

## 3. 查询任务状态

### `GET /api/research/{taskId}`

根据 `taskId` 查询任务执行状态和进度。

**路径参数：**

| 参数 | 说明 |
|------|------|
| taskId | 任务 ID（UUID） |

**响应示例：**

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "taskId": "7d4fd5d2-4e7d-4c87-84a8-2ec8d55b9f60",
    "status": "RUNNING",
    "progress": 45
  }
}
```

**任务不存在（404）：**

```json
{
  "code": 404,
  "message": "研究任务不存在",
  "data": null
}
```

**手动测试（PowerShell）：**

```powershell
$taskId = "7d4fd5d2-4e7d-4c87-84a8-2ec8d55b9f60"
Invoke-RestMethod -Uri "http://localhost:8080/api/research/$taskId"
```

---

## 4. 获取研究报告

### `GET /api/report/{taskId}`

根据 `taskId` 获取 AI 生成的 Markdown 研究报告（取最新版本）。

**路径参数：**

| 参数 | 说明 |
|------|------|
| taskId | 任务 ID（UUID） |

**响应示例：**

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "taskId": "7d4fd5d2-4e7d-4c87-84a8-2ec8d55b9f60",
    "companyName": "隆基绿能",
    "reportMarkdown": "# 隆基绿能 投资研究报告\n\n...",
    "aiModel": "gpt-4",
    "reportVersion": 1,
    "createdAt": "2026-07-12T21:00:00"
  }
}
```

**报告不存在（404）：**

```json
{
  "code": 404,
  "message": "研究报告不存在",
  "data": null
}
```

**手动测试（PowerShell）：**

```powershell
$taskId = "7d4fd5d2-4e7d-4c87-84a8-2ec8d55b9f60"
Invoke-RestMethod -Uri "http://localhost:8080/api/report/$taskId"
```

---

## 5. 查询历史任务

### `GET /api/task/list`

返回所有研究任务列表，按创建时间倒序排列。

**响应示例：**

```json
{
  "code": 200,
  "message": "success",
  "data": [
    {
      "taskId": "7d4fd5d2-4e7d-4c87-84a8-2ec8d55b9f60",
      "companyName": "隆基绿能",
      "stockCode": "601012",
      "status": "PENDING",
      "progress": 0,
      "createdAt": "2026-07-12T21:00:00"
    }
  ]
}
```

**手动测试（PowerShell）：**

```powershell
Invoke-RestMethod -Uri http://localhost:8080/api/task/list
```

---

## 6. 异常测试（开发用）

### `GET /test/error`

故意触发系统异常，用于验证全局异常处理。

**响应示例：**

```json
{
  "code": 500,
  "message": "系统异常",
  "data": null
}
```

**手动测试（PowerShell）：**

```powershell
Invoke-RestMethod -Uri http://localhost:8080/test/error
```

---

## 自动化测试

### 运行全部测试

```powershell
cd backend
mvn test
```

### 测试类说明

| 测试类 | 覆盖接口 | 说明 |
|--------|---------|------|
| `BackendApplicationTests` | — | Spring 上下文加载 |
| `GlobalExceptionHandlerTest` | `GET /test/error` | 验证 500 异常响应 |
| `ResearchControllerTest` | Research 模块 | 创建任务、查询状态、任务列表 |

### ResearchControllerTest 用例

| 用例 | 接口 | 断言 |
|------|------|------|
| `createResearchShouldReturnTaskId` | `POST /api/research` | code=200，返回 taskId，status=PENDING |
| `getTaskStatusShouldReturnNotFoundWhenMissing` | `GET /api/research/{taskId}` | code=404，任务不存在 |
| `listTasksShouldReturnArray` | `GET /api/task/list` | code=200，data 为数组 |

### 单独运行 Research 测试

```powershell
cd backend
mvn test -Dtest=ResearchControllerTest
```

---

## 完整手动测试流程

前置条件：PostgreSQL 已启动，已执行建表 SQL，后端服务已启动。

```powershell
# 1. 健康检查
Invoke-RestMethod -Uri http://localhost:8080/health

# 2. 创建研究任务
$body = @{ companyName = "隆基绿能"; stockCode = "601012" } | ConvertTo-Json
$result = Invoke-RestMethod -Uri http://localhost:8080/api/research -Method Post -ContentType "application/json" -Body $body
$taskId = $result.data.taskId
Write-Host "taskId: $taskId"

# 3. 查询任务状态
Invoke-RestMethod -Uri "http://localhost:8080/api/research/$taskId"

# 4. 查询历史任务
Invoke-RestMethod -Uri http://localhost:8080/api/task/list

# 5. 获取报告（需 Worker 生成报告后才有数据）
Invoke-RestMethod -Uri "http://localhost:8080/api/report/$taskId"
```

---

## 接口总览

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/health` | 健康检查 |
| POST | `/api/research` | 创建研究任务 |
| GET | `/api/research/{taskId}` | 查询任务状态 |
| GET | `/api/report/{taskId}` | 获取研究报告 |
| GET | `/api/task/list` | 查询历史任务 |
| GET | `/test/error` | 异常测试（开发用） |
