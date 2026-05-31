from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_contract(path: str | Path) -> dict[str, Any]:
    text = Path(path).read_text(encoding="utf-8")
    if Path(path).suffix.lower() == ".json":
        return json.loads(text)
    return _load_simple_yaml(text)


def _load_simple_yaml(text: str) -> dict[str, Any]:
    try:
        import yaml  # type: ignore
    except Exception:
        yaml = None
    if yaml is not None:
        data = yaml.safe_load(text)
        return data or {}
    result: dict[str, Any] = {}
    stack: list[tuple[int, Any]] = [(-1, result)]
    for raw in text.splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        line = raw.strip()
        while stack and indent <= stack[-1][0]:
            stack.pop()
        parent = stack[-1][1]
        if line.startswith("- "):
            value = _scalar(line[2:])
            if isinstance(parent, list):
                parent.append(value)
            continue
        if ":" in line:
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip()
            parsed: Any
            if value == "":
                parsed = {}
                parent[key] = parsed
                stack.append((indent, parsed))
            else:
                parent[key] = _scalar(value)
    return result


def _scalar(value: str) -> Any:
    if value in {"null", "None"}:
        return None
    if value in {"true", "True"}:
        return True
    if value in {"false", "False"}:
        return False
    if value.startswith("[") or value.startswith("{"):
        try:
            return json.loads(value.replace("'", '"'))
        except Exception:
            return value
    try:
        if "." in value or "e" in value.lower():
            return float(value)
        return int(value)
    except ValueError:
        return value.strip('"')


def required_trace_columns(contract: dict[str, Any]) -> list[str]:
    trace = contract.get("trace", {})
    columns = trace.get("required_trace_columns", [])
    if isinstance(columns, list):
        values: list[str] = []
        for item in columns:
            if isinstance(item, dict):
                name = item.get("name") or item.get("column_name")
                if name:
                    values.append(str(name))
            else:
                values.append(str(item))
        return values
    return []
