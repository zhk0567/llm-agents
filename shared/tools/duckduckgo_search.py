"""Optional real web search (requires: pip install duckduckgo-search)."""

from __future__ import annotations

import json


def search_topic(topic: str, max_results: int = 3) -> str:
    try:
        from duckduckgo_search import DDGS
    except ImportError as exc:
        raise ImportError(
            "Install duckduckgo-search: pip install duckduckgo-search"
        ) from exc

    snippets: list[str] = []
    sources: list[str] = []
    with DDGS() as ddgs:
        for item in ddgs.text(topic, max_results=max_results):
            body = item.get("body") or item.get("snippet") or ""
            href = item.get("href") or item.get("link") or ""
            if body:
                snippets.append(body[:300])
            if href:
                sources.append(href)

    if not snippets:
        snippets.append(f"{topic}：未检索到结果，请检查网络或改用 mock。")

    return json.dumps(
        {"topic": topic, "snippets": snippets, "sources": sources or ["duckduckgo"]},
        ensure_ascii=False,
    )
