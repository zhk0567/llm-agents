"""AG2 / autogen-agentchat — Research assistant with Ollama."""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_core.models import ModelFamily, ModelInfo
from autogen_ext.models.openai import OpenAIChatCompletionClient

from llm_agents_common.config import get_topic_from_argv, load_ollama_config
from llm_agents_common.output import extract_json_object, fallback_result, print_result


async def run_agent(topic: str) -> str:
    cfg = load_ollama_config()
    client = OpenAIChatCompletionClient(
        model=cfg["default_model"],
        base_url=cfg["base_url"],
        api_key=cfg["api_key"],
        model_info=ModelInfo(
            vision=False,
            function_calling=True,
            json_output=True,
            family=ModelFamily.UNKNOWN,
        ),
    )
    assistant = AssistantAgent(
        name="researcher",
        model_client=client,
        system_message=(
            "你是研究助手。输出 JSON："
            '{"topic":"...","bullets":["a","b","c"],"summary":"..."}。只输出 JSON。'
        ),
    )
    prompt = (
        f"主题：{topic}\n"
        "模拟已调用 search_topic 得到三条要点，整理为规定 JSON。"
    )
    result = await assistant.on_messages(
        [TextMessage(content=prompt, source="user")],
        cancellation_token=None,
    )
    return result.chat_message.content


def main() -> None:
    topic = get_topic_from_argv()
    try:
        text = asyncio.run(run_agent(topic))
        print_result(extract_json_object(text))
    except Exception as exc:
        print_result(fallback_result(topic, str(exc)))


if __name__ == "__main__":
    main()
