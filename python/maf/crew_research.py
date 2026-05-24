"""Semantic Kernel — ResearchCrew: research plugin then writer prompt."""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from openai import AsyncOpenAI
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
from semantic_kernel.functions import kernel_function

from llm_agents_common.config import get_topic_from_argv, load_ollama_config
from llm_agents_common.output import extract_json_object, fallback_result, print_result
from llm_agents_common.search import search_topic as do_search


class ResearchPlugin:
    @kernel_function(name="search_topic", description="Search for information about a topic")
    def search_topic(self, topic: str) -> str:
        return do_search(topic)


async def run_crew(topic: str) -> str:
    cfg = load_ollama_config()
    client = AsyncOpenAI(api_key=cfg["api_key"], base_url=cfg["base_url"])
    kernel = Kernel()
    kernel.add_service(
        OpenAIChatCompletion(
            ai_model_id=cfg["default_model"],
            async_client=client,
        )
    )
    kernel.add_plugin(ResearchPlugin(), plugin_name="research")

    research = await kernel.invoke_prompt(
        prompt=f"主题：{topic}。调用 research-search_topic，输出 3 条要点（纯文本）。"
    )
    final = await kernel.invoke_prompt(
        prompt=(
            f"主题：{topic}\n研究素材：\n{research}\n\n"
            '只输出 JSON：{"topic":"...","bullets":["a","b","c"],"summary":"..."}'
        )
    )
    return str(final)


def main() -> None:
    topic = get_topic_from_argv()
    try:
        text = asyncio.run(run_crew(topic))
        print_result(extract_json_object(text))
    except Exception as exc:
        print_result(fallback_result(topic, str(exc)))


if __name__ == "__main__":
    main()
