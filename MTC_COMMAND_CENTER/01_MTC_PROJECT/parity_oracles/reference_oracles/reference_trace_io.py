from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any, Iterable

from parity_oracles.reference_oracles.reference_trace_schema import (
    REFERENCE_COMPARISON_COLUMNS,
    REFERENCE_TRACE_COLUMNS,
)


def infer_value_type(value: Any) -> str:
    if value is None or value == "":
        return "null"
    if isinstance(value, bool):
        return "bool"
    if isinstance(value, (int, float)):
        return "number"
    text = str(value).strip().lower()
    if text in {"true", "false"}:
        return "bool"
    try:
        float(str(value))
        return "number"
    except ValueError:
        return "string"


def write_reference_trace(path: str | Path, rows: Iterable[dict[str, Any]]) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=REFERENCE_TRACE_COLUMNS)
        writer.writeheader()
        for row in rows:
            output = {column: row.get(column, "") for column in REFERENCE_TRACE_COLUMNS}
            if not output["value_type"]:
                output["value_type"] = infer_value_type(output["expected_value"])
            writer.writerow(output)


def read_reference_trace(path: str | Path) -> list[dict[str, str]]:
    with Path(path).open("r", newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def read_feature_trace(path: str | Path) -> list[dict[str, str]]:
    with Path(path).open("r", newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def write_comparison_rows(path: str | Path, rows: Iterable[dict[str, Any]]) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=REFERENCE_COMPARISON_COLUMNS)
        writer.writeheader()
        for row in rows:
            writer.writerow({column: row.get(column, "") for column in REFERENCE_COMPARISON_COLUMNS})


def write_json(path: str | Path, payload: dict[str, Any]) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
