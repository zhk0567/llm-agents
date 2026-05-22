"""Smolagents — TopicResearchAgent with Ollama."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from smolagents import LiteLLMModel, ToolCallingAgent, tool

from llm_agents_common.config import get_topic_from_argv, load_ollama_config
from llm_agents_common.mock_search import search_topic as mock_search
from llm_agents_common.output import extract_json_object, fallback_result, print_result


def _search_topic_impl(topic: str) -> str:
    """Search for information about a topic.

    Args:
        topic: The research topic to search for.
    """
    return mock_search(topic)


search_topic = tool(_search_topic_impl)


def main() -> None:
    topic = get_topic_from_argv()
    cfg = load_ollama_config()
    model = LiteLLMModel(
        model_id=f"ollama_chat/{cfg['default_model']}",
        api_base=cfg["host"],
        api_key=cfg["api_key"],
    )
    agent = ToolCallingAgent(
        tools=[search_topic],
        model=model,
        max_steps=4,
    )
    prompt = (
        f"研究主题：{topic}\n"
        "调用 search_topic，输出 JSON："
        '{"topic":"...","bullets":["","",""],"summary":"..."}'
    )
    try:
        raw = agent.run(prompt)
        print_result(extract_json_object(str(raw)))
    except Exception as exc:
        print_result(fallback_result(topic, str(exc)))


if __name__ == "__main__":
    main()
