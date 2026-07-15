# Todo

## AI 分析模块（V1）

- [x] Task1 — `llm/client.py`：完成模型调用
- [x] Task2 — `llm/prompt.py`：完成 Prompt 生成
- [x] Task3 — `repository/announcement_reader.py`：读取待分析数据
- [x] Task4 — `service/analysis_service.py`：完成完整流程
- [x] Task5 — `llm/json_parser.py`：完成 JSON 解析
- [x] Task6 — `repository/ai_repository.py`：保存数据库
- [x] Task7 — `llm/retry.py`：失败重试
- [x] Task8 — `main.py`：批量分析入口

详见 [05-AI-Service.md](05-AI-Service.md)。

## 已完成

- [x] Crawler 公告采集
- [x] PDF 下载解析 → `announcement_content`
- [x] AI 批量分析模块代码 → `ai/`

## 待开发

- [ ] AI 批量分析联调验证（配置 API_KEY 后跑通）
- [ ] 与 Spring Boot Research Worker 联动
- [ ] 研究报告生成 → `research_report`
