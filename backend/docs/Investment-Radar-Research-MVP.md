# Investment Radar - Research 模块设计（MVP）

## 目标

`POST /api/research` 不直接执行 AI 分析，而是**创建研究任务**，返回
`taskId`，后续由异步任务完成分析。

------------------------------------------------------------------------

## 整体流程

``` text
前端
  │
  ▼
POST /api/research
  │
  ▼
ResearchController
  │
  ▼
ResearchService
  │
  ▼
保存 research_task
  │
  ▼
返回 taskId
```

后续异步流程：

``` text
Research Worker
    │
    ▼
读取 research_task
    │
    ▼
采集新闻/公告/财报
    │
    ▼
调用 Python AI Service
    │
    ▼
生成 Markdown 报告
    │
    ▼
保存 research_report
    │
    ▼
更新 research_task.status
```

------------------------------------------------------------------------

## POST /api/research

### 请求

``` http
POST /api/research
Content-Type: application/json
```

``` json
{
  "companyName": "隆基绿能",
  "stockCode": "601012"
}
```

### 返回

``` json
{
  "code": 200,
  "message": "success",
  "data": {
    "taskId": "7d4fd5d2-4e7d-4c87-84a8-2ec8d55b9f60",
    "status": "PENDING"
  }
}
```

------------------------------------------------------------------------

## 职责

Controller： - 参数校验 - 调用 Service - 返回统一响应

Service： - 生成 UUID TaskId - 创建任务 - 保存数据库 - 返回 TaskId

数据库： - 保存 research_task

------------------------------------------------------------------------

## research_task 状态

-   PENDING
-   RUNNING
-   SUCCESS
-   FAILED

------------------------------------------------------------------------

## 后续接口

### 查询任务状态

`GET /api/research/{taskId}`

返回：

``` json
{
  "taskId": "xxx",
  "status": "RUNNING",
  "progress": 45
}
```

### 获取报告

`GET /api/report/{taskId}`

返回 AI 生成的 Markdown 报告。

### 查询历史任务

`GET /api/task/list`

返回任务列表。

------------------------------------------------------------------------

## MVP 开发顺序

1.  ResearchTask Entity
2.  ResearchTaskMapper
3.  ResearchService
4.  ResearchController
5.  POST /api/research 写入 PostgreSQL
6.  GET /api/research/{taskId}
7.  Python AI Service
8.  AI 生成 research_report
9.  前端联调

------------------------------------------------------------------------

## 接口文档

完整接口说明与测试方法见 [api.md](api.md)。
