"""Pydantic AI — TopicResearchAgent with Ollama (OpenAI-compatible)."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from pydantic import BaseModel, Field
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider

from llm_agents_common.config import get_topic_from_argv, load_ollama_config
from llm_agents_common.mock_search import search_topic as mock_search
from llm_agents_common.output import fallback_result, print_result


class ResearchOutput(BaseModel):
    topic: str
    bullets: list[str] = Field(min_length=1)
    summary: str


def main() -> None:
    topic = get_topic_from_argv()
    cfg = load_ollama_config()
    provider = OpenAIProvider(
        base_url=cfg["base_url"],
        api_key=cfg["api_key"],
    )
    model = OpenAIChatModel(cfg["default_model"], provider=provider)
    agent = Agent(
        model,
        output_type=ResearchOutput,
        system_prompt="调用 search_topic 工具后整理为结构化结果。",
    )

    @agent.tool_plain
    def search_topic(query: str) -> str:
        """Search for information about a topic."""
        return mock_search(query)

    prompt = f"研究主题：{topic}。先 search_topic，再返回 topic/bullets/summary。"
    try:
        result = agent.run_sync(prompt)
        print_result(result.output.model_dump())
    except Exception as exc:
        print_result(fallback_result(topic, str(exc)))


if __name__ == "__main__":
    main()
