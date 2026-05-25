# 框架对比报告

> 主题：`AI Agent 框架选型` · 任务：[TASK_SPEC.md](../shared/TASK_SPEC.md)  
> 数据来自 `docs/benchmarks.md` / `docs/smoke-log.txt`（自动生成 + 人工结论）

## 1. 测试环境

| 项 | 值 |
|----|-----|
| OS | Windows |
| LLM | Ollama（本地） |
| 默认模型 | `config/ollama.json` → 本机已安装模型（如 `nemotron-3-super:cloud`） |
| 检索 | mock `search_topic`（`USE_MOCK_SEARCH=1`） |

## 2. 横向对比（摘要）

| 框架 | 语言 | 范式 | 上手 | Ollama 真连 | 多 Agent | 生产向 |
|------|------|------|------|-------------|----------|--------|
| LangGraph | Python | 状态图 | 中 | 是 | 是 | 高 |
| CrewAI | Python | 角色 Crew | 低 | 是 | 是 | 中 |
| LlamaIndex | Python | Agent/RAG | 中 | 是 | 是 | 中 |
| Pydantic AI | Python | 类型化 | 低 | 是 | 有限 | 中 |
| Haystack | Python | Agent/Pipeline | 中 | 是 | 是 | 中 |
| DSPy | Python | 编程式 | 高 | 是 | 有限 | 研究 |
| AG2 | Python | 对话 | 中 | 是 | 是 | 中 |
| Smolagents | Python | Tool Agent | 低 | 是 | 有限 | 低 |
| MAF/SK | Python/.NET | Kernel | 中 | 是 | 是 | 高 |
| LangGraph.js | TS | 状态图 | 中 | 是 | 是 | 高 |
| LangChain4j | Java | AiServices | 中 | 是 | 是 | 高 |

详细矩阵见 [FRAMEWORK_MATRIX.md](./FRAMEWORK_MATRIX.md)。

## 3. 选型建议

- **复杂编排 / checkpoint / HITL** → LangGraph（见 `python/langgraph/checkpoint_demo.py`）
- **最快多角色原型** → CrewAI
- **RAG + Agent 一体** → LlamaIndex 或 Haystack
- **强类型输出** → Pydantic AI
- **Prompt 程序优化** → DSPy
- **.NET 企业栈** → `dotnet/` Semantic Kernel
- **JVM** → LangChain4j

## 4. Ollama 注意事项

1. 先 `setup-ollama.ps1`，模型落在 `./models/ollama`
2. 无默认模型时用 `$env:OLLAMA_MODEL=已有模型`
3. 使用 `ollama list` 已有模型；修改 `config/ollama.json` 或 `$env:OLLAMA_MODEL`

## 5. 复现

```powershell
. .\scripts\setup-ollama.ps1
.\scripts\check-ollama.ps1
.\scripts\run-smoke-live.ps1
.\scripts\update-matrix-from-smoke.ps1
```

结果写入 `docs/smoke-log.txt`、`docs/benchmarks.md`。

## 6. 项目交付状态

| 项 | 值 |
|----|-----|
| Live smoke 日期 | 2026-05-24 |
| 模型 | `nemotron-3-super:cloud` |
| OK | 14（Python 13 + TypeScript 2） |
| SKIP | 3（dotnet、java/langchain4j、java/google-adk） |
| 策略 | 不下载模型/工具链；仅用 Ollama |

完整说明见 [PROJECT_STATUS.md](./PROJECT_STATUS.md)。

### CI 与本地 benchmark

- **GitHub Actions**（`.github/workflows/smoke.yml`）：依赖安装 + 少量 demo 冒烟，无 Ollama，允许 fallback。
- **本地 `run-smoke-live.ps1`**：权威 benchmark（Ollama 真连 + JSON schema 校验）。

