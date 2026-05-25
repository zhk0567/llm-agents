# 项目交付状态

> 最后更新：2026-05-24 · 仓库：[llm-agents](https://github.com/zhk0567/llm-agents)

## 交付范围

- 统一基准任务：[shared/TASK_SPEC.md](../shared/TASK_SPEC.md)（TopicResearchAgent）
- 本地 LLM：**Ollama**（[`config/ollama.json`](../config/ollama.json)）
- 检索：默认 mock `search_topic`（`USE_MOCK_SEARCH=1`）
- 输出：统一 JSON schema（[`shared/schema/research_output.json`](../shared/schema/research_output.json)）

## 模型策略

- **不自动下载**模型；使用 `ollama list` 中已有聊天模型
- 默认模型：`nemotron-3-super:cloud`（可通过 `$env:OLLAMA_MODEL` 覆盖）
- 仅当读者自行需要新模型时：`.\scripts\pull-models.ps1 -Download`

## Live smoke 结果（2026-05-24）

模型：`nemotron-3-super:cloud` · 主题：`AI Agent 框架选型`

| 结果 | 数量 | 说明 |
|------|------|------|
| OK | 14 | Python 13 + TypeScript 2 |
| SKIP | 3 | dotnet、java/langchain4j、java/google-adk |
| FAIL | 0 | — |

详见 [`smoke-log.txt`](./smoke-log.txt)、[`benchmarks.md`](./benchmarks.md)。

### 已通过（14）

- python/langgraph、python/langgraph-crew
- python/crewai、python/crewai-crew
- python/llamaindex、python/pydantic_ai、python/smolagents
- python/ag2、python/ag2-crew
- python/maf、python/maf-crew
- python/haystack、python/dspy
- typescript/langgraph-js、typescript/openai-agents

### 未 live 测（3，代码保留）

| 框架 | 原因 |
|------|------|
| dotnet/TopicResearchAgent | 需 .NET SDK（本仓库收尾不安装） |
| java/langchain4j | 需 Maven（本仓库收尾不安装） |
| java/google-adk | 需 Maven；真机需 Google API Key（非 Ollama） |

## 范围外（刻意不做）

- 自动拉取 Ollama 模型、安装 .NET / Maven 等工具链
- Google ADK / Gemini、Claude Agent SDK 等**非 Ollama** 云端模型验证
- AutoGen 原版 demo（矩阵标注为不默认实现）

## 复现（本地）

```powershell
cd f:\commercial\llm-agents
. .\scripts\setup-ollama.ps1
.\scripts\check-ollama.ps1
.\scripts\run-smoke-live.ps1
.\scripts\update-matrix-from-smoke.ps1
```

仅测 TypeScript：`.\scripts\run-ts-smoke.ps1`

## CI 与本地 benchmark

| 环境 | 作用 |
|------|------|
| GitHub Actions [`.github/workflows/smoke.yml`](../.github/workflows/smoke.yml) | 安装依赖 + 少量 demo 冒烟（无 Ollama，允许 fallback） |
| 本地 `run-smoke-live.ps1` | **权威 benchmark**（Ollama 真连 + schema 校验） |

## 扩展阅读

- [FRAMEWORK_MATRIX.md](./FRAMEWORK_MATRIX.md) — 框架对比矩阵
- [COMPARISON_REPORT.md](./COMPARISON_REPORT.md) — 选型报告
- [CONFIG.md](./CONFIG.md) — 配置说明
- [INSTALL_TOOLCHAIN.md](./INSTALL_TOOLCHAIN.md) — 读者自行扩展 dotnet/java 时参考
