"""Unified search_topic: mock (default) or DuckDuckGo via USE_MOCK_SEARCH."""

from __future__ import annotations

import importlib.util
import os
import sys
from pathlib import Path

from llm_agents_common.config import project_root


def use_mock_search() -> bool:
    return os.environ.get("USE_MOCK_SEARCH", "1").strip().lower() not in (
        "0",
        "false",
        "no",
    )


def _load_module(name: str, rel_path: str):
    path = project_root() / rel_path
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load {path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def search_topic(topic: str) -> str:
    if use_mock_search():
        mod = _load_module("shared_mock_search", "shared/tools/mock_search.py")
        return mod.search_topic(topic)
    mod = _load_module("shared_ddg_search", "shared/tools/duckduckgo_search.py")
    return mod.search_topic(topic)
