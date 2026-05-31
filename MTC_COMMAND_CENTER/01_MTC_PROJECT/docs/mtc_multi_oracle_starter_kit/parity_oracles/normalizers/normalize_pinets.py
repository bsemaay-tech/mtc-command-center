#!/usr/bin/env python3
"""
Normalize PineTS JSON output into standard oracle CSV files.

Because PineTS output schemas can vary depending on pinets-cli/adapters,
this script supports a conservative generic format:

Expected simple input example:
{
  "plots": [
    {"title": "RAW_LONG", "values": [{"time": "...", "value": 1}]}
  ]
}

If your real PineTS output differs, Codex should adapt only the parsing section,
while keeping the standard output columns unchanged.
"""

from __future__ import annotations

import argparse, json
from pathlib import Path
from common import ensure_dir, write_csv, write_json, COLUMNS

SIGNAL_NAMES = {"RAW_LONG", "RAW_SHORT", "FINAL_LONG", "FINAL_SHORT"}

def load_plots(obj):
    if isinstance(obj, dict):
        if "plots" in obj and isinstance(obj["plots"], list):
            return obj["plots"]
        if "data" in obj and isinstance(obj["data"], list):
            return obj["data"]
    if isinstance(obj, list):
        return obj
    return []

def normalize(input_json: Path, out_dir: Path) -> None:
    obj = json.loads(input_json.read_text(encoding="utf-8"))
    plots = load_plots(obj)

    by_ts = {}
    indicator_rows = []
    for plot in plots:
        title = plot.get("title") or plot.get("name") or plot.get("id") or "UNKNOWN"
        values = plot.get("values") or plot.get("data") or []
        for i, item in enumerate(values):
            ts = str(item.get("time") or item.get("timestamp") or item.get("t") or i)
            val = item.get("value", item.get("y", item.get("v", "")))
            if title in SIGNAL_NAMES:
                row = by_ts.setdefault(ts, {
                    "timestamp": ts, "bar_index": i,
                    "raw_long": "0", "raw_short": "0",
                    "final_long": "0", "final_short": "0",
                    "reason_code": ""
                })
                if title == "RAW_LONG": row["raw_long"] = "1" if float(val or 0) != 0 else "0"
                if title == "RAW_SHORT": row["raw_short"] = "1" if float(val or 0) != 0 else "0"
                if title == "FINAL_LONG": row["final_long"] = "1" if float(val or 0) != 0 else "0"
                if title == "FINAL_SHORT": row["final_short"] = "1" if float(val or 0) != 0 else "0"
            else:
                indicator_rows.append({"timestamp": ts, "indicator_name": title, "value": val})

    ensure_dir(out_dir)
    write_csv(out_dir / "normalized_signals.csv", COLUMNS["signals"], by_ts.values())
    write_csv(out_dir / "normalized_indicators.csv", COLUMNS["indicators"], indicator_rows)
    write_json(out_dir / "normalized_stats.json", {"source": "pinets", "note": "PineTS normalized as signal/indicator oracle only."})

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input-json", required=True)
    ap.add_argument("--out-dir", required=True)
    args = ap.parse_args()
    normalize(Path(args.input_json), Path(args.out_dir))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
