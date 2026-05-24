from __future__ import annotations

import json
import os
import sys
from pathlib import Path


def project_root() -> Path:
    """Repository root (parent of python/)."""
    return Path(__file__).resolve().parents[2]


def load_ollama_config() -> dict:
    path = project_root() / "config" / "ollama.json"
    with path.open(encoding="utf-8") as f:
        cfg = json.load(f)
    if os.environ.get("OLLAMA_MODEL"):
        cfg = {**cfg, "default_model": os.environ["OLLAMA_MODEL"]}
    return cfg


def load_agent_config() -> dict:
    path = project_root() / "config" / "agent.json"
    with path.open(encoding="utf-8") as f:
        cfg = json.load(f)
    if os.environ.get("USE_MOCK_SEARCH") is not None:
        cfg = {
            **cfg,
            "use_mock_search": os.environ["USE_MOCK_SEARCH"].strip().lower()
            not in ("0", "false", "no"),
        }
    if os.environ.get("AGENT_TIMEOUT_SECONDS"):
        cfg = {**cfg, "timeout_seconds": int(os.environ["AGENT_TIMEOUT_SECONDS"])}
    return cfg


def get_topic_from_argv() -> str:
    if len(sys.argv) > 1:
        return " ".join(sys.argv[1:])
    return load_agent_config().get("default_topic", "AI Agent 框架选型")


def llm_timeout_seconds() -> float:
    return float(load_agent_config().get("timeout_seconds", 120))
