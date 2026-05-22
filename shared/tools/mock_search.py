"""Shared mock search tool for TopicResearchAgent benchmarks."""

from __future__ import annotations

import json


def search_topic(topic: str) -> str:
    """Return deterministic mock search results for any topic."""
    payload = {
        "topic": topic,
        "snippets": [
            f"{topic}：社区生态成熟，文档与第三方库丰富。",
            f"{topic}：在性能与开发效率之间需要按场景权衡。",
            f"{topic}：企业落地需关注可观测性、成本与合规。",
        ],
        "sources": ["mock://local/knowledge-base"],
    }
    return json.dumps(payload, ensure_ascii=False)


def search_topic_dict(topic: str) -> dict:
    """Same as search_topic but returns a dict."""
    return json.loads(search_topic(topic))
