"""LangGraph HITL — confirm before tool execution (stdin y/n)."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from langchain_ollama import ChatOllama
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from langgraph.types import Command

from llm_agents_common.config import get_topic_from_argv, load_agent_config, load_ollama_config
from llm_agents_common.output import extract_json_object, fallback_result, print_result
from llm_agents_common.search import search_topic as do_search


@tool
def search_topic(topic: str) -> str:
    """Search for information about a topic."""
    return do_search(topic)


def main() -> None:
    topic = get_topic_from_argv()
    cfg = load_ollama_config()
    llm = ChatOllama(
        model=cfg["default_model"],
        base_url=cfg["host"],
        temperature=0.2,
        num_retries=2,
    )
    memory = MemorySaver()
    agent = create_react_agent(
        llm,
        [search_topic],
        checkpointer=memory,
        interrupt_before=["tools"],
    )
    run_config = {"configurable": {"thread_id": "hitl-topic-research"}}
    prompt = (
        f"研究主题：{topic}\n"
        "必须先调用 search_topic，再输出 JSON："
        '{"topic":"...","bullets":["","",""],"summary":"..."}'
    )
    try:
        state = agent.invoke(
            {"messages": [HumanMessage(content=prompt)]},
            config=run_config,
        )
        while True:
            snap = agent.get_state(run_config)
            if not snap.next:
                break
            pending = snap.values.get("messages", [])
            last = pending[-1] if pending else None
            tool_calls = getattr(last, "tool_calls", None) or []
            if tool_calls:
                print("\n--- 待执行工具 ---", file=sys.stderr)
                for tc in tool_calls:
                    print(f"  {tc.get('name')}({tc.get('args')})", file=sys.stderr)
                answer = input("是否允许执行工具？[y/N]: ").strip().lower()
                if answer not in ("y", "yes"):
                    print_result(fallback_result(topic, "[fallback] 用户拒绝工具调用"))
                    return
            state = agent.invoke(Command(resume=True), config=run_config)

        text = state["messages"][-1].content
        print_result(extract_json_object(text))
    except Exception as exc:
        print_result(fallback_result(topic, str(exc)))


if __name__ == "__main__":
    main()
