"""AG2 — ResearchCrew: researcher then writer (sequential)."""

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


def _client(cfg: dict) -> OpenAIChatCompletionClient:
    return OpenAIChatCompletionClient(
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


async def run_crew(topic: str) -> str:
    cfg = load_ollama_config()
    client = _client(cfg)
    researcher = AssistantAgent(
        name="Researcher",
        model_client=client,
        system_message="你是研究员。根据主题列出 3 条要点（纯文本）。",
    )
    writer = AssistantAgent(
        name="Writer",
        model_client=client,
        system_message=(
            "你是撰稿人。根据研究素材输出 JSON："
            '{"topic":"...","bullets":["a","b","c"],"summary":"..."}。只输出 JSON。'
        ),
    )
    r = await researcher.on_messages(
        [TextMessage(content=f"主题：{topic}（模拟已 search_topic）", source="user")],
        cancellation_token=None,
    )
    notes = r.chat_message.content
    w = await writer.on_messages(
        [TextMessage(content=f"主题：{topic}\n素材：\n{notes}", source="user")],
        cancellation_token=None,
    )
    return w.chat_message.content


def main() -> None:
    topic = get_topic_from_argv()
    try:
        text = asyncio.run(run_crew(topic))
        print_result(extract_json_object(text))
    except Exception as exc:
        print_result(fallback_result(topic, str(exc)))


if __name__ == "__main__":
    main()
