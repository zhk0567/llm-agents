# Python Agent 框架示例

```powershell
cd f:\commercial\llm-agents\python
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .
```

| 目录 | 说明 |
|------|------|
| `langgraph/` | LangGraph ReAct Agent |
| `crewai/` | CrewAI 单 Agent + `crew_research.py` 多 Agent |
| `llamaindex/` | LlamaIndex FunctionAgent |
| `pydantic_ai/` | Pydantic AI 类型化输出 |
| `ag2/` | AG2 (pyautogen) |
| `smolagents/` | Hugging Face Smolagents |
| `maf/` | Semantic Kernel (Microsoft 栈) |

公共模块：`llm_agents_common/`
