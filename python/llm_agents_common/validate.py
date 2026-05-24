"""Validate TopicResearchAgent JSON output against shared schema."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from llm_agents_common.config import project_root


def load_schema() -> dict[str, Any]:
    path = project_root() / "shared" / "schema" / "research_output.json"
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def validate_output(data: dict[str, Any]) -> list[str]:
    """Return list of validation errors (empty if valid)."""
    errors: list[str] = []
    schema = load_schema()
    required = schema.get("required", [])
    for key in required:
        if key not in data:
            errors.append(f"missing required field: {key}")
    topic = data.get("topic")
    if topic is not None and (not isinstance(topic, str) or not topic.strip()):
        errors.append("topic must be non-empty string")
    bullets = data.get("bullets")
    if bullets is not None:
        if not isinstance(bullets, list) or len(bullets) < 1:
            errors.append("bullets must be a non-empty array")
        elif not all(isinstance(b, str) and b.strip() for b in bullets):
            errors.append("bullets items must be non-empty strings")
    summary = data.get("summary")
    if summary is not None and (not isinstance(summary, str) or not summary.strip()):
        errors.append("summary must be non-empty string")
    return errors


def is_fallback_output(data: dict[str, Any]) -> bool:
    summary = str(data.get("summary", ""))
    return (
        "[fallback]" in summary.lower()
        or "（fallback）" in summary
        or "Connection error" in summary
        or "10061" in summary
        or "not found" in summary.lower()
        or "status code: 404" in summary.lower()
    )
