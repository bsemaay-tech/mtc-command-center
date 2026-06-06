#!/usr/bin/env python
"""Disk-backed OHLCV data coverage checks for QuantLens workflows."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

DEFAULT_MANIFEST = Path(
    r"C:\LAB\_MTC_V2_REPO_CLEANUP_ARCHIVE_20260529"
    r"\MTC_V2_OPTIMIZATION_DATA_BUNDLE_20260427\manifests\dataset_manifest.json"
)


def _read_csv_range(path: Path) -> tuple[str, str, int]:
    first = last = ""
    rows = 0
    with path.open("r", encoding="utf-8", errors="replace") as f:
        header = f.readline().strip().split(",")
        ts_idx = header.index("timestamp_utc") if "timestamp_utc" in header else 0
        for line in f:
            if not line.strip():
                continue
            parts = line.rstrip("\n").split(",")
            rows += 1
            ts = parts[ts_idx]
            first = first or ts
            last = ts
    return first, last, rows


def _read_parquet_range(path: Path) -> tuple[str, str, int]:
    df = pd.read_parquet(path, columns=None)
    ts_col = "timestamp_utc" if "timestamp_utc" in df.columns else ("timestamp" if "timestamp" in df.columns else df.columns[0])
    rows = int(len(df))
    if rows == 0:
        return "", "", 0
    return str(df[ts_col].iloc[0]), str(df[ts_col].iloc[-1]), rows


def verify_actual_range(symbol: str, tf: str, manifest_path: str | Path = DEFAULT_MANIFEST) -> dict:
    manifest_path = Path(manifest_path)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    ds = next((d for d in manifest.get("datasets", [])
               if d.get("symbol") == symbol
               and d.get("timeframe_normalized") == tf
               and d.get("ohlcv_validation_status") == "PASS"), None)
    if not ds:
        return {"status": "NO_DATA", "symbol": symbol, "timeframe": tf, "manifest": str(manifest_path)}

    data_path = manifest_path.parents[1] / ds["normalized_path"]
    if not data_path.exists():
        return {"status": "MISSING_FILE", "symbol": symbol, "timeframe": tf, "path": str(data_path)}

    if data_path.suffix.lower() == ".parquet":
        first, last, rows = _read_parquet_range(data_path)
    else:
        first, last, rows = _read_csv_range(data_path)

    return {
        "status": "PASS" if rows > 0 else "EMPTY_FILE",
        "symbol": symbol,
        "timeframe": tf,
        "path": str(data_path),
        "first": first,
        "last": last,
        "bar_count": rows,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("symbol")
    parser.add_argument("timeframe")
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = verify_actual_range(args.symbol, args.timeframe, args.manifest)
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(result)
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
