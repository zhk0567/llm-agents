"""CrewAI — TopicResearchAgent (single agent) with Ollama."""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from crewai import Agent, Crew, LLM, Process, Task
from crewai.tools import tool

from llm_agents_common.config import get_topic_from_argv, load_ollama_config
from llm_agents_common.mock_search import search_topic as mock_search
from llm_agents_common.output import extract_json_object, fallback_result, print_result


@tool("search_topic")
def search_topic_tool(topic: str) -> str:
    """Search for information about a topic."""
    return mock_search(topic)


def main() -> None:
    topic = get_topic_from_argv()
    cfg = load_ollama_config()
    llm = LLM(
        model=f"ollama/{cfg['default_model']}",
        base_url=cfg["host"],
        temperature=0.2,
    )
    researcher = Agent(
        role="研究员",
        goal="根据主题检索并输出结构化 JSON",
        backstory="你擅长调用工具并整理要点。",
        llm=llm,
        tools=[search_topic_tool],
        verbose=False,
    )
    task = Task(
        description=(
            f"主题：{topic}\n"
            "使用 search_topic 工具，然后输出纯 JSON："
            '{"topic":"...","bullets":["a","b","c"],"summary":"..."}'
        ),
        expected_output="合法 JSON 字符串",
        agent=researcher,
    )
    crew = Crew(agents=[researcher], tasks=[task], process=Process.sequential, verbose=False)
    try:
        raw = crew.kickoff()
        text = str(raw.raw) if hasattr(raw, "raw") else str(raw)
        print_result(extract_json_object(text))
    except Exception as exc:
        print_result(fallback_result(topic, str(exc)))


if __name__ == "__main__":
    main()
