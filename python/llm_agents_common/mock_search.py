"""Import shared mock search from repo root."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

from llm_agents_common.config import project_root


def _load_shared_mock():
    path = project_root() / "shared" / "tools" / "mock_search.py"
    spec = importlib.util.spec_from_file_location("shared_mock_search", path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load {path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["shared_mock_search"] = mod
    spec.loader.exec_module(mod)
    return mod


_shared = None


def search_topic(topic: str) -> str:
    global _shared
    if _shared is None:
        _shared = _load_shared_mock()
    return _shared.search_topic(topic)
