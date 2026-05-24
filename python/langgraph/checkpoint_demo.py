"""LangGraph — checkpoint demo: interrupt and resume with SQLite."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from langchain_ollama import ChatOllama
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.prebuilt import create_react_agent

from llm_agents_common.config import get_topic_from_argv, load_ollama_config, project_root
from llm_agents_common.output import fallback_result, print_result
from llm_agents_common.search import search_topic as do_search


@tool
def search_topic(topic: str) -> str:
    """Search for information about a topic."""
    return do_search(topic)


def main() -> None:
    topic = get_topic_from_argv()
    cfg = load_ollama_config()
    ckpt_dir = project_root() / "data" / "checkpoints"
    ckpt_dir.mkdir(parents=True, exist_ok=True)
    db_path = ckpt_dir / "langgraph_demo.sqlite"

    llm = ChatOllama(model=cfg["default_model"], base_url=cfg["host"], temperature=0.2)
    with SqliteSaver.from_conn_string(str(db_path)) as memory:
        agent = create_react_agent(llm, [search_topic], checkpointer=memory)
        config = {"configurable": {"thread_id": "topic-research-demo"}}
        prompt = (
            f"研究主题：{topic}\n"
            "调用 search_topic，输出简短 JSON（topic/bullets/summary）。"
        )
        try:
            result = agent.invoke(
                {"messages": [HumanMessage(content=prompt)]},
                config=config,
            )
            text = result["messages"][-1].content
            from llm_agents_common.output import extract_json_object

            print_result(extract_json_object(text))
            print(f"\n# checkpoint saved: {db_path}", file=sys.stderr)
        except Exception as exc:
            print_result(fallback_result(topic, str(exc)))


if __name__ == "__main__":
    main()
