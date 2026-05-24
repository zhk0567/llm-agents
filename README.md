# llm-agents — 多语言主流 AI Agent 框架探索

在**当前仓库目录**内对比并实现主流 Agent 框架，统一基准任务 + 本地 **Ollama**（模型存放在 `./models/ollama`）。

## 前置条件（Windows）

1. 安装 [Ollama](https://ollama.com/download)
2. Python 3.11+、Node.js 20+（必选）
3. .NET 8 SDK、JDK 17+、Maven（运行 `dotnet/`、`java/` 示例时需要）

## 快速开始

```powershell
cd f:\commercial\llm-agents

# 一键初始化（venv、npm、依赖）
.\scripts\bootstrap.ps1

# 将 Ollama 模型目录指向本项目
. .\scripts\setup-ollama.ps1

# 拉取默认模型（见 config/ollama.json）
.\scripts\pull-models.ps1

# 启动 Ollama（另开终端，先 dot-source setup）
ollama serve

# 检查连通性与默认模型
.\scripts\check-ollama.ps1
```

若本机已有其他模型，可临时指定：`$env:OLLAMA_MODEL = "你的模型名"`

## Python 环境

```powershell
cd python
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[all]"
# 或：.\scripts\install-all.ps1
```

运行示例：

```powershell
cd python\langgraph
..\.venv\Scripts\python main.py "Rust 与 Go 在 CLI 工具中的取舍"
```

## 目录结构

| 路径 | 说明 |
|------|------|
| `shared/` | 统一任务规格与 mock 工具 |
| `config/ollama.json` | 模型与 API 端点 |
| `config/agent.json` | 重试、超时、默认主题、mock 检索开关 |
| `python/` | LangGraph、CrewAI、LlamaIndex、Haystack、DSPy 等 |
| `typescript/` | LangGraph.js、OpenAI Agents SDK |
| `dotnet/` | Microsoft Agent Framework / Semantic Kernel |
| `java/langchain4j/` | LangChain4j |
| `docs/` | 对比矩阵与各框架笔记 |

## 选型决策树

- 要强状态/可恢复 → **LangGraph**
- 要快做角色化团队 → **CrewAI**
- 要强 RAG → **LlamaIndex**
- 要类型与校验 → **Pydantic AI**
- Azure/.NET → **dotnet/**
- JVM → **java/langchain4j**

详见 [docs/FRAMEWORK_MATRIX.md](docs/FRAMEWORK_MATRIX.md)、[docs/COMPARISON_REPORT.md](docs/COMPARISON_REPORT.md)、[docs/CONFIG.md](docs/CONFIG.md)。

## 工具链与真机 smoke

- 安装 .NET / Maven：[docs/INSTALL_TOOLCHAIN.md](docs/INSTALL_TOOLCHAIN.md)
- 使用已有 Ollama 模型跑 smoke：`.\scripts\run-smoke-live.ps1 -Model <模型名>`
- 回填矩阵：`.\scripts\update-matrix-from-smoke.ps1`

## 后续任务

见 [docs/NEXT_TASKS.md](docs/NEXT_TASKS.md)（按 P0→P5 优先级排列的待办清单）。

## Smoke 测试

```powershell
.\scripts\run-all-smoke.ps1
```

结果写入 `docs/smoke-log.txt`。

## 约束

- 虚拟环境、依赖缓存、Ollama 权重均在项目根下，不使用用户目录外的绝对路径。
- 示例默认使用 mock `search_topic`，无需外网。
