# CrewAI

## 范式

角色（Agent）+ 任务（Task）+ Crew 顺序/层级流程。

## Ollama

`LLM(model="ollama/<model>", base_url=..., api_key=ollama)`。

## 文件

- `python/crewai/main.py` — 单 Agent
- `python/crewai/crew_research.py` — ResearchCrew 多 Agent

## 何时选用

快速搭建多角色原型；线性「研究 → 写作」流水线。
