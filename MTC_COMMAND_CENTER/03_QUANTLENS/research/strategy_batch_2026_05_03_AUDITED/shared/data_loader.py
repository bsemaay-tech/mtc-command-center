from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


def load_manifest(bundle_root: Path) -> list[dict[str, object]]:
    return json.loads((bundle_root / "DATA_BUNDLE_MANIFEST.json").read_text(encoding="utf-8"))["datasets"]


def select_datasets(bundle_root: Path, symbols: list[str], timeframe: str) -> dict[str, dict[str, object]]:
    selected = {}
    for row in load_manifest(bundle_root):
        symbol = row.get("symbol")
        tf = str(row.get("timeframe_normalized", row.get("timeframe")))
        status = row.get("ohlcv_validation_status")
        if symbol in symbols and tf.lower() == timeframe.lower() and status == "PASS":
            current = selected.get(symbol)
            if current is None or int(row.get("row_count", 0)) > int(current.get("row_count", 0)):
                selected[symbol] = row
    return selected


def load_ohlcv(path: Path) -> pd.DataFrame:
    data = pd.read_csv(path)
    columns = {str(column).lower(): column for column in data.columns}
    timestamp_col = next((columns[name] for name in ["timestamp", "timestamp_utc", "time", "date", "datetime"] if name in columns), None)
    if timestamp_col is None:
        raise ValueError(f"Missing timestamp column in {path}")
    data = data.rename(columns={timestamp_col: "timestamp"})
    for name in ["open", "high", "low", "close", "volume"]:
        if name in columns:
            data = data.rename(columns={columns[name]: name})
    if "volume" not in data:
        data["volume"] = 0.0
    missing = [name for name in ["open", "high", "low", "close"] if name not in data]
    if missing:
        raise ValueError(f"Missing columns in {path}: {missing}")
    if pd.api.types.is_numeric_dtype(data["timestamp"]):
        data["timestamp"] = pd.to_datetime(data["timestamp"], unit="s", utc=True)
    else:
        data["timestamp"] = pd.to_datetime(data["timestamp"], utc=True)
    for name in ["open", "high", "low", "close", "volume"]:
        data[name] = pd.to_numeric(data[name], errors="coerce")
    return data[["timestamp", "open", "high", "low", "close", "volume"]].dropna(subset=["open", "high", "low", "close"]).sort_values("timestamp").reset_index(drop=True)
