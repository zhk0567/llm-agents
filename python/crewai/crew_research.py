"""CrewAI — ResearchCrew (Researcher -> Writer) multi-agent variant."""

from __future__ import annotations

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
        role="Researcher",
        goal="检索主题并列出要点",
        backstory="负责调用 search_topic 并整理 bullets 素材。",
        llm=llm,
        tools=[search_topic_tool],
        verbose=False,
    )
    writer = Agent(
        role="Writer",
        goal="根据研究素材输出最终 JSON",
        backstory="负责写成规定 JSON 格式。",
        llm=llm,
        verbose=False,
    )
    research_task = Task(
        description=f"对主题「{topic}」调用 search_topic，输出要点列表（纯文本即可）。",
        expected_output="3 条要点",
        agent=researcher,
    )
    write_task = Task(
        description=(
            "根据上一步要点，输出 JSON："
            '{"topic":"...","bullets":["","",""],"summary":"..."}，只输出 JSON。'
        ),
        expected_output="合法 JSON",
        agent=writer,
        context=[research_task],
    )
    crew = Crew(
        agents=[researcher, writer],
        tasks=[research_task, write_task],
        process=Process.sequential,
        verbose=False,
    )
    try:
        raw = crew.kickoff()
        text = str(raw.raw) if hasattr(raw, "raw") else str(raw)
        print_result(extract_json_object(text))
    except Exception as exc:
        print_result(fallback_result(topic, str(exc)))


if __name__ == "__main__":
    main()
