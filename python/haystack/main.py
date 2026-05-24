"""Haystack 2.x Agent + OllamaChatGenerator — TopicResearchAgent."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from haystack.components.agents import Agent
from haystack.dataclasses import ChatMessage
from haystack.tools import Tool
from haystack_integrations.components.generators.ollama import OllamaChatGenerator

from llm_agents_common.config import get_topic_from_argv, load_ollama_config
from llm_agents_common.output import extract_json_object, fallback_result, print_result
from llm_agents_common.search import search_topic as do_search


def search_fn(topic: str) -> str:
    return do_search(topic)


def main() -> None:
    topic = get_topic_from_argv()
    cfg = load_ollama_config()
    tools = [
        Tool(
            name="search_topic",
            description="Search for information about a topic",
            parameters={
                "type": "object",
                "properties": {
                    "topic": {"type": "string", "description": "Research topic"},
                },
                "required": ["topic"],
            },
            function=search_fn,
        )
    ]
    chat_gen = OllamaChatGenerator(
        model=cfg["default_model"],
        url=cfg["host"],
        generation_kwargs={"temperature": 0.2},
    )
    agent = Agent(
        chat_generator=chat_gen,
        tools=tools,
        system_prompt=(
            "你是研究助手。必须调用 search_topic。"
            "最终只输出 JSON：{\"topic\",\"bullets\",\"summary\"}。"
        ),
    )
    prompt = (
        f"研究主题：{topic}\n"
        "调用 search_topic 后输出 JSON，不要 markdown。"
    )
    try:
        result = agent.run(messages=[ChatMessage.from_user(prompt)])
        text = result["messages"][-1].text
        print_result(extract_json_object(text))
    except Exception as exc:
        print_result(fallback_result(topic, str(exc)))


if __name__ == "__main__":
    main()
