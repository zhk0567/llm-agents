"""Validate JSON from framework stdout. Usage: python main.py ... | python validate_stdout.py"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from llm_agents_common.validate import is_fallback_output, validate_output


def main() -> int:
    raw = sys.stdin.read()
    try:
        # Use the last JSON object in stdout (some agents print step logs first)
        starts = [i for i, c in enumerate(raw) if c == "{"]
        data = None
        for start in reversed(starts):
            end = raw.rfind("}", start)
            if end <= start:
                continue
            try:
                data = json.loads(raw[start : end + 1])
                break
            except json.JSONDecodeError:
                continue
        if data is None:
            raise json.JSONDecodeError("no valid JSON object", raw, 0)
    except (json.JSONDecodeError, ValueError) as exc:
        print(f"INVALID_JSON: {exc}", file=sys.stderr)
        return 1
    errors = validate_output(data)
    if errors:
        print("SCHEMA_FAIL: " + "; ".join(errors), file=sys.stderr)
        return 2
    if is_fallback_output(data):
        print("FALLBACK", file=sys.stderr)
        return 3
    print("OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
