"""LangGraph — TopicResearchAgent with Ollama + mock search."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from langchain_ollama import ChatOllama
try:
    from langgraph.prebuilt import create_react_agent
except ImportError:
    from langchain.agents import create_agent as create_react_agent  # noqa: F401

from llm_agents_common.config import get_topic_from_argv, load_ollama_config
from llm_agents_common.search import search_topic as do_search
from llm_agents_common.output import extract_json_object, fallback_result, print_result


@tool
def search_topic(topic: str) -> str:
    """Search for information about a topic. Returns JSON snippets."""
    return do_search(topic)


def main() -> None:
    topic = get_topic_from_argv()
    cfg = load_ollama_config()
    agent_cfg = load_agent_config()
    llm = ChatOllama(
        model=cfg["default_model"],
        base_url=cfg["host"],
        temperature=0.2,
        num_retries=int(agent_cfg.get("max_retries", 2)),
    )
    agent = create_react_agent(llm, [search_topic])
    prompt = (
        f"研究主题：{topic}\n"
        "1. 调用 search_topic 工具\n"
        "2. 输出 JSON：{\"topic\":\"...\",\"bullets\":[\"\",\"\",\"\"],\"summary\":\"...\"}\n"
        "只输出 JSON，不要 markdown。"
    )
    try:
        result = agent.invoke({"messages": [HumanMessage(content=prompt)]})
        text = result["messages"][-1].content
        print_result(extract_json_object(text))
    except Exception as exc:
        print_result(fallback_result(topic, str(exc)))


if __name__ == "__main__":
    main()
