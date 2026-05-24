# 贡献指南

## 新增框架 demo

1. 在对应语言目录下新建子文件夹（如 `python/myfw/`）。
2. 实现 [shared/TASK_SPEC.md](shared/TASK_SPEC.md) 中的 **TopicResearchAgent**。
3. 检索统一使用 `llm_agents_common.search.search_topic`（Python）或等价 mock（其他语言）。
4. 连接 Ollama 时读取 [config/ollama.json](config/ollama.json)，勿写用户目录绝对路径。
5. 增加 `README.md` 与 [docs/per-framework/](docs/per-framework/) 笔记。
6. 在 [docs/FRAMEWORK_MATRIX.md](docs/FRAMEWORK_MATRIX.md) 增加一行。

## 路径与依赖约束

- 模型：`./models/ollama`（`scripts/setup-ollama.ps1`）
- Python venv：仅 `python/.venv`
- Node：`typescript/node_modules`
- 勿提交 `.env`、API Key、模型权重

## 本地检查

```powershell
.\scripts\bootstrap.ps1
.\scripts\run-all-smoke.ps1
cd python
..\.venv\Scripts\python -m pytest ..\tests\
```

## Pull Request

- 说明框架版本号与是否在 Ollama 真机下验证
- 附上 `docs/smoke-log.txt` 或 `docs/benchmarks.md` 变更摘要（若跑过 smoke）
