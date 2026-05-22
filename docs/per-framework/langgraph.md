# LangGraph

## 范式

有向图状态机（StateGraph / ReAct prebuilt），适合可恢复、HITL、分支编排。

## Ollama

`ChatOllama` 指向 `config/ollama.json` 的 `host` 与 `default_model`。

## 实测备注

- 示例路径：`python/langgraph/main.py`
- 无 Ollama 时走 `fallback_result`，便于 smoke
- LangGraph 1.x 中 `create_react_agent` 有弃用提示，可迁移至 `langchain.agents`

## 何时选用

复杂工作流、需要 checkpoint 与生产级编排时优先。
