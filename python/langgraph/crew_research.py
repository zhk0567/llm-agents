"""LangGraph — ResearchCrew: Researcher (tools) -> Writer (JSON)."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.tools import tool
from langchain_ollama import ChatOllama
from langgraph.graph import END, START, StateGraph
from langgraph.prebuilt import create_react_agent
from typing_extensions import TypedDict

from llm_agents_common.config import get_topic_from_argv, load_ollama_config
from llm_agents_common.output import extract_json_object, fallback_result, print_result
from llm_agents_common.search import search_topic as do_search


@tool
def search_topic(topic: str) -> str:
    """Search for information about a topic."""
    return do_search(topic)


class CrewState(TypedDict):
    topic: str
    research_notes: str
    final_json: str


def build_graph(topic: str, cfg: dict):
    llm = ChatOllama(model=cfg["default_model"], base_url=cfg["host"], temperature=0.2)
    researcher = create_react_agent(llm, [search_topic])

    def research_node(state: CrewState) -> CrewState:
        prompt = (
            f"主题：{state['topic']}\n"
            "调用 search_topic，整理 3 条要点（纯文本列表）。"
        )
        result = researcher.invoke({"messages": [HumanMessage(content=prompt)]})
        notes = str(result["messages"][-1].content)
        return {**state, "research_notes": notes}

    def write_node(state: CrewState) -> CrewState:
        prompt = (
            f"主题：{state['topic']}\n"
            f"研究素材：\n{state['research_notes']}\n\n"
            "只输出 JSON：{\"topic\":\"...\",\"bullets\":[\"\",\"\",\"\"],\"summary\":\"...\"}"
        )
        msg = llm.invoke(
            [
                SystemMessage(content="你只输出合法 JSON，不要 markdown。"),
                HumanMessage(content=prompt),
            ]
        )
        return {**state, "final_json": str(msg.content)}

    g = StateGraph(CrewState)
    g.add_node("research", research_node)
    g.add_node("write", write_node)
    g.add_edge(START, "research")
    g.add_edge("research", "write")
    g.add_edge("write", END)
    return g.compile()


def main() -> None:
    topic = get_topic_from_argv()
    cfg = load_ollama_config()
    try:
        graph = build_graph(topic, cfg)
        out = graph.invoke(
            {"topic": topic, "research_notes": "", "final_json": ""}
        )
        print_result(extract_json_object(out["final_json"]))
    except Exception as exc:
        print_result(fallback_result(topic, str(exc)))


if __name__ == "__main__":
    main()
