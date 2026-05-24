from __future__ import annotations

import json
import re
import sys
from typing import Any


def extract_json_object(text: str) -> dict[str, Any]:
    """Parse JSON from model output, tolerating markdown fences."""
    text = text.strip()
    fence = re.search(r"```(?:json)?\s*([\s\S]*?)```", text)
    if fence:
        text = fence.group(1).strip()
    start = text.find("{")
    end = text.rfind("}")
    if start >= 0 and end > start:
        text = text[start : end + 1]
    return json.loads(text)


def print_result(data: dict[str, Any]) -> None:
    print(json.dumps(data, ensure_ascii=False, indent=2))


def fallback_result(topic: str, raw: str | None = None) -> dict[str, Any]:
    """Deterministic output when LLM parsing fails (smoke / offline)."""
    return {
        "topic": topic,
        "bullets": [
            f"{topic}：适合作为 Agent 框架对比的基准主题。",
            f"{topic}：本地 Ollama 可离线运行 mock 检索流程。",
            f"{topic}：各框架应输出相同 JSON 结构便于横向比较。",
        ],
        "summary": (raw or f"[fallback] 关于「{topic}」的简要总结。")[:500],
    }
