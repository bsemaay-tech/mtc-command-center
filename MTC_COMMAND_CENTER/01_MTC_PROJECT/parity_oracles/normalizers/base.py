from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from parity_oracles.common.io_utils import NORMALIZED_FILES, empty_normalized_set, read_csv, read_json, write_csv, write_json


def normalize_generic_csv(raw_path: Path, out_dir: Path, source_name: str) -> dict[str, str]:
    outputs = empty_normalized_set(out_dir)
    rows = read_csv(raw_path)
    if not rows:
        return outputs

    lower_map = {key.lower(): key for key in rows[0].keys()}
    if {"timestamp", "open", "high", "low", "close"}.issubset(lower_map):
        data_rows = []
        for row in rows:
            data_rows.append({
                "timestamp": row.get(lower_map["timestamp"], ""),
                "open": row.get(lower_map["open"], ""),
                "high": row.get(lower_map["high"], ""),
                "low": row.get(lower_map["low"], ""),
                "close": row.get(lower_map["close"], ""),
                "volume": row.get(lower_map.get("volume", ""), ""),
            })
        filename, fields = NORMALIZED_FILES["data"]
        target = out_dir / filename
        write_csv(target, fields, data_rows)
        outputs["data"] = str(target)

    signal_keys = {"raw_long", "raw_short", "final_long", "final_short"}
    if signal_keys.intersection(lower_map):
        signal_rows = []
        for index, row in enumerate(rows):
            signal_rows.append({
                "timestamp": row.get(lower_map.get("timestamp", ""), ""),
                "bar_index": row.get(lower_map.get("bar_index", ""), index),
                "raw_long": row.get(lower_map.get("raw_long", ""), ""),
                "raw_short": row.get(lower_map.get("raw_short", ""), ""),
                "final_long": row.get(lower_map.get("final_long", ""), ""),
                "final_short": row.get(lower_map.get("final_short", ""), ""),
                "reason_code": row.get(lower_map.get("reason_code", ""), source_name),
            })
        filename, fields = NORMALIZED_FILES["signals"]
        target = out_dir / filename
        write_csv(target, fields, signal_rows)
        outputs["signals"] = str(target)

    return outputs


def normalize_generic_json(raw_path: Path, out_dir: Path, source_name: str) -> dict[str, str]:
    outputs = empty_normalized_set(out_dir)
    payload = read_json(raw_path)
    if isinstance(payload, dict):
        for section, rows in payload.items():
            if section in NORMALIZED_FILES and isinstance(rows, list):
                filename, fields = NORMALIZED_FILES[section]
                target = out_dir / filename
                write_csv(target, fields, rows)
                outputs[section] = str(target)
        if isinstance(payload.get("stats"), dict):
            target = out_dir / "normalized_stats.json"
            write_json(target, payload["stats"])
            outputs["stats"] = str(target)
    return outputs


def normalize(raw: Path | None, out_dir: Path, source_name: str) -> dict[str, str]:
    if raw is None or not raw.exists():
        return empty_normalized_set(out_dir)
    if raw.suffix.lower() == ".json":
        return normalize_generic_json(raw, out_dir, source_name)
    if raw.suffix.lower() == ".csv":
        return normalize_generic_csv(raw, out_dir, source_name)
    return empty_normalized_set(out_dir)


def main(source_name: str) -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw", type=Path)
    parser.add_argument("--out-dir", type=Path, required=True)
    args = parser.parse_args()
    outputs = normalize(args.raw, args.out_dir, source_name)
    print(json.dumps(outputs, indent=2, sort_keys=True))
