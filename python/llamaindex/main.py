"""LlamaIndex — TopicResearchAgent with Ollama + mock search."""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from llama_index.core.agent.workflow import FunctionAgent
from llama_index.core.tools import FunctionTool
from llama_index.llms.ollama import Ollama

from llm_agents_common.config import get_topic_from_argv, load_ollama_config
from llm_agents_common.mock_search import search_topic as mock_search
from llm_agents_common.output import extract_json_object, fallback_result, print_result


def search_topic_fn(topic: str) -> str:
    return mock_search(topic)


async def run_agent(topic: str) -> str:
    cfg = load_ollama_config()
    llm = Ollama(
        model=cfg["default_model"],
        base_url=cfg["host"],
        request_timeout=120.0,
        temperature=0.2,
    )
    tool = FunctionTool.from_defaults(fn=search_topic_fn, name="search_topic")
    agent = FunctionAgent(
        tools=[tool],
        llm=llm,
        system_prompt=(
            "你是研究助手。必须调用 search_topic。"
            "最终只输出 JSON：{\"topic\",\"bullets\",\"summary\"}。"
        ),
    )
    prompt = (
        f"研究主题：{topic}\n"
        "调用 search_topic 后输出 JSON，不要 markdown。"
    )
    handler = agent.run(user_msg=prompt)
    if asyncio.iscoroutine(handler):
        result = await handler
    else:
        result = handler
    return str(result)


def main() -> None:
    topic = get_topic_from_argv()
    try:
        text = asyncio.run(run_agent(topic))
        print_result(extract_json_object(text))
    except Exception as exc:
        print_result(fallback_result(topic, str(exc)))


if __name__ == "__main__":
    main()
