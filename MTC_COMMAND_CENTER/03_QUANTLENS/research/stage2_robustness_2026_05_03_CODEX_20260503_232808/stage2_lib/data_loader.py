from __future__ import annotations

from pathlib import Path

import pandas as pd


def normalize_ohlcv(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    columns = {c.lower(): c for c in df.columns}
    rename = {
        columns.get("timestamp") or columns.get("timestamp_utc") or columns.get("date") or columns.get("datetime") or columns.get("time"): "timestamp",
        columns.get("open"): "open",
        columns.get("high"): "high",
        columns.get("low"): "low",
        columns.get("close"): "close",
        columns.get("volume"): "volume",
    }
    df = df.rename(columns={k: v for k, v in rename.items() if k})
    if "volume" not in df:
        df["volume"] = 0.0
    required = ["timestamp", "open", "high", "low", "close", "volume"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"{path} missing columns {missing}")
    df = df[required].copy()
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
    for col in ["open", "high", "low", "close", "volume"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    return df.dropna(subset=["timestamp", "open", "high", "low", "close"]).drop_duplicates("timestamp").sort_values("timestamp").reset_index(drop=True)


def data_quality(df: pd.DataFrame, timeframe: str) -> dict[str, object]:
    if df.empty:
        return {"bar_count": 0, "first_ts": "", "last_ts": "", "duplicate_count": 0, "missing_count": 0, "quality": "EMPTY"}
    freq = {"5m": "5min", "15m": "15min", "1h": "1h", "4h": "4h", "1D": "1D"}.get(timeframe)
    missing = 0
    if freq:
        full = pd.date_range(df["timestamp"].iloc[0], df["timestamp"].iloc[-1], freq=freq, tz="UTC")
        missing = max(len(full) - len(df), 0)
    return {
        "bar_count": int(len(df)),
        "first_ts": str(df["timestamp"].iloc[0]),
        "last_ts": str(df["timestamp"].iloc[-1]),
        "duplicate_count": int(df["timestamp"].duplicated().sum()),
        "missing_count": int(missing),
        "quality": "PASS" if missing == 0 else "WARN_MISSING",
    }
