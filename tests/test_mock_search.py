from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))


def _load_mock():
    path = ROOT / "shared" / "tools" / "mock_search.py"
    spec = importlib.util.spec_from_file_location("mock_search", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_mock_search_returns_json():
    mod = _load_mock()
    raw = mod.search_topic("测试主题")
    data = json.loads(raw)
    assert data["topic"] == "测试主题"
    assert len(data["snippets"]) >= 1


def test_validate_output_ok():
    from llm_agents_common.validate import validate_output

    data = {
        "topic": "x",
        "bullets": ["a", "b", "c"],
        "summary": "ok",
    }
    assert validate_output(data) == []


def test_is_fallback():
    from llm_agents_common.validate import is_fallback_output

    assert is_fallback_output({"topic": "t", "bullets": ["a"], "summary": "[fallback] x"})
