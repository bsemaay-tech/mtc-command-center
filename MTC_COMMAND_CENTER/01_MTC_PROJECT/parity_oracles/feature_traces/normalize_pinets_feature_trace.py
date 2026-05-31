from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from .trace_io import infer_value_type, write_long_trace


PREFIX = "FEATURE__"


def normalize_pinets_json(input_path: str | Path, output_path: str | Path, feature_type: str = "signal_producer") -> dict[str, Any]:
    payload = json.loads(Path(input_path).read_text(encoding="utf-8"))
    rows: list[dict[str, Any]] = []
    records = payload if isinstance(payload, list) else payload.get("data", payload.get("plots", []))
    for bar_index, record in enumerate(records):
        if not isinstance(record, dict):
            continue
        timestamp = record.get("timestamp") or record.get("time") or bar_index
        for key, value in record.items():
            if not str(key).startswith(PREFIX):
                continue
            parts = str(key).split("__")
            if len(parts) < 4:
                continue
            _, feature_id, stage, column_name = parts[:4]
            rows.append(
                {
                    "timestamp": timestamp,
                    "bar_index": record.get("bar_index", bar_index),
                    "feature_id": feature_id,
                    "feature_type": feature_type,
                    "stage": stage,
                    "column_name": column_name,
                    "value": value,
                    "value_type": infer_value_type(value),
                    "source_oracle": "pinets",
                }
            )
    write_long_trace(output_path, rows)
    return {"rows": len(rows), "output": str(output_path)}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--feature-type", default="signal_producer")
    args = parser.parse_args()
    print(normalize_pinets_json(args.input, args.output, args.feature_type))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
