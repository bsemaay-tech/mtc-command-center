from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

from .trace_schema import LONG_TRACE_COLUMNS


def infer_value_type(value: Any) -> str:
    if value is None or value == "":
        return "null"
    if isinstance(value, bool):
        return "bool"
    if isinstance(value, (int, float)):
        return "number"
    text = str(value).strip()
    if text.lower() in {"true", "false"}:
        return "bool"
    try:
        float(text)
        return "number"
    except ValueError:
        return "string"


def write_long_trace(path: str | Path, rows: list[dict[str, Any]]) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=LONG_TRACE_COLUMNS)
        writer.writeheader()
        for row in rows:
            output = {column: row.get(column, "") for column in LONG_TRACE_COLUMNS}
            if not output["value_type"]:
                output["value_type"] = infer_value_type(output["value"])
            writer.writerow(output)


def read_long_trace(path: str | Path) -> list[dict[str, str]]:
    with Path(path).open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_json(path: str | Path, payload: dict[str, Any]) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
