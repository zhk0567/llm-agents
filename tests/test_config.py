from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))


def test_load_agent_config_defaults():
    from llm_agents_common.config import load_agent_config

    cfg = load_agent_config()
    assert cfg["default_topic"]
    assert "max_retries" in cfg
    assert "timeout_seconds" in cfg


def test_use_mock_search_from_agent_json(monkeypatch):
    from llm_agents_common.search import use_mock_search

    monkeypatch.delenv("USE_MOCK_SEARCH", raising=False)
    assert use_mock_search() is True
    monkeypatch.setenv("USE_MOCK_SEARCH", "0")
    assert use_mock_search() is False
