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


def get_topic_from_argv() -> str:
    if len(sys.argv) > 1:
        return " ".join(sys.argv[1:])
    return "AI Agent 框架选型"
