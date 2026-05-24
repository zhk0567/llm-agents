"""DSPy — TopicResearchAgent with Ollama (LiteLLM backend)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import dspy

from llm_agents_common.config import get_topic_from_argv, load_ollama_config
from llm_agents_common.output import extract_json_object, fallback_result, print_result
from llm_agents_common.search import search_topic as do_search


class ResearchSignature(dspy.Signature):
    """Given topic and search snippets, produce JSON with topic, bullets, summary."""

    topic: str = dspy.InputField()
    search_data: str = dspy.InputField(desc="JSON from search_topic tool")
    result_json: str = dspy.OutputField(
        desc='JSON only: {"topic":"...","bullets":["a","b","c"],"summary":"..."}'
    )


class ResearchModule(dspy.Module):
    def forward(self, topic: str) -> dspy.Prediction:
        search_data = do_search(topic)
        return self.prog(topic=topic, search_data=search_data)


def main() -> None:
    topic = get_topic_from_argv()
    cfg = load_ollama_config()
    lm = dspy.LM(
        model=f"ollama_chat/{cfg['default_model']}",
        api_base=cfg["host"],
        api_key=cfg.get("api_key", "ollama"),
        temperature=0.2,
    )
    dspy.configure(lm=lm)
    module = ResearchModule()
    module.prog = dspy.ChainOfThought(ResearchSignature)
    try:
        pred = module(topic)
        print_result(extract_json_object(pred.result_json))
    except Exception as exc:
        print_result(fallback_result(topic, str(exc)))


if __name__ == "__main__":
    main()
