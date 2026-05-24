# AI Agent 框架对比矩阵

基准任务：[shared/TASK_SPEC.md](../shared/TASK_SPEC.md)（TopicResearchAgent + 本地 Ollama）

| 框架 | 语言 | 范式 | Ollama | 多 Agent | 状态/持久化 | 观测 | 上手成本 | 适用场景 | 实测备注 |
|------|------|------|--------|----------|-------------|------|----------|----------|----------|
| LangGraph | Python | 状态图 | 是 | 是 | Checkpoint | LangSmith | 中 | 复杂编排、生产 | `python/langgraph`；无 Ollama 时 fallback |
| CrewAI | Python | 角色 Crew | 是 | 是 | 有限 | 内置 tracing | 低 | 快速多 Agent 原型 | `crew_research.py` 多 Agent |
| LlamaIndex | Python | Agent/RAG | 是 | 是 | 索引持久化 | 可选 | 中 | 数据/RAG 向 Agent | FunctionAgent + Ollama LLM |
| Pydantic AI | Python | 类型化 Agent | 是 | 有限 | 无 | 可选 | 低 | 类型安全 Python | `ResearchOutput` 结构化输出 |
| AG2 | Python | 对话多 Agent | 是 | 是 | 会话 | 基础 | 中 | 研究式对话协作 | pyautogen + OpenAI 兼容 |
| Smolagents | Python | Code Agent | 是 | 有限 | 无 | HF | 低 | 轻量 HF 生态 | `@tool` + LiteLLMModel |
| MAF (Python) | Python | 企业 Agent | 是 | 是 | 依 SDK | Azure | 中 | Microsoft 生态 | SK `ResearchPlugin` |
| LangGraph.js | TypeScript | 状态图 | 是 | 是 | 依运行时 | LangSmith | 中 | 全栈 TS 编排 | `typescript/langgraph-js` |
| OpenAI Agents SDK | TypeScript | Handoff | 是 | 是 | 无 | 内置 | 低 | OpenAI 风格 API | Ollama via OpenAI client |
| MAF / SK (.NET) | C# | 插件/Agent | 是 | 是 | 依 SK | App Insights | 中 | .NET / Azure | `dotnet/src/TopicResearchAgent` |
| LangChain4j | Java | 链/Agent | 是 | 是 | 内存 | 可选 | 中 | JVM 企业栈 | AiServices + OllamaChatModel |
| Haystack | Python | Agent/Pipeline | 是 | 是 | 管道 | 可选 | 中 | NLP/RAG 管道 | `python/haystack` Agent+Ollama |
| DSPy | Python | 编程式优化 | 是 | 有限 | 无 | 实验 | 高 | Prompt 优化 | `python/dspy` Signature+CoT |
| Google ADK | Java/Kotlin | 工具 Agent | 部分 | 是 | 依平台 | GCP | 中 | Google Cloud | 文档级 |
| AutoGen (原版) | Python | 对话 | 是 | 是 | 会话 | 基础 | — | 维护模式 | 不默认实现 |
| Claude Agent SDK | TS/Python | 工具循环 | 否 | 是 | 会话 | Anthropic | 低 | Claude 原生 | 需云端 API |

## 选型速查

- **要强状态 / 可恢复 / HITL** → LangGraph
- **要快做角色化团队** → CrewAI
- **要强 RAG / 文档索引** → LlamaIndex
- **要类型与校验** → Pydantic AI
- **Azure / .NET 企业栈** → Microsoft Agent Framework
- **JVM** → LangChain4j
