from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

import numpy as np
import pandas as pd

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.engine.indicators import bollinger_bands, choppiness, rma, rsi, tr


def _load_case(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _load_df(case_path: Path, dataset_ref: str) -> pd.DataFrame:
    dataset_path = (case_path.parent.parent / dataset_ref).resolve() if not Path(dataset_ref).is_absolute() else Path(dataset_ref)
    if not dataset_path.exists():
        dataset_path = (PROJECT_ROOT / dataset_ref).resolve()
    df = pd.read_parquet(dataset_path)
    if "timestamp" not in df.columns:
        df = df.reset_index()
        if "timestamp" not in df.columns:
            raise ValueError(f"No timestamp column in dataset: {dataset_path}")
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
    return df


def _compute_rf_debug(df: pd.DataFrame, rf_cfg: dict) -> pd.DataFrame:
    high = df["high"].astype(float)
    low = df["low"].astype(float)
    close = df["close"].astype(float)

    up_move = high.diff()
    down_move = -low.diff()
    plus_dm = pd.Series(np.where((up_move > down_move) & (up_move > 0), up_move, 0.0), index=df.index, dtype=float)
    minus_dm = pd.Series(np.where((down_move > up_move) & (down_move > 0), down_move, 0.0), index=df.index, dtype=float)
    tr_v = tr(high, low, close).astype(float)
    tr_rma = rma(tr_v, 14)
    plus_rma = rma(plus_dm, 14)
    minus_rma = rma(minus_dm, 14)
    plus_di = pd.Series(np.where(tr_rma != 0, 100.0 * plus_rma / tr_rma, 0.0), index=df.index, dtype=float)
    minus_di = pd.Series(np.where(tr_rma != 0, 100.0 * minus_rma / tr_rma, 0.0), index=df.index, dtype=float)
    dx = pd.Series(
        np.where((plus_di + minus_di) != 0, 100.0 * (plus_di - minus_di).abs() / (plus_di + minus_di), 0.0),
        index=df.index,
        dtype=float,
    )
    adx = rma(dx, 14)
    chop = choppiness(high, low, close, length=14).astype(float)
    rsi_v = rsi(close, length=int(rf_cfg["rsi_len"])).astype(float)
    bb_upper, bb_mid, bb_lower = bollinger_bands(
        close,
        length=int(rf_cfg["bb_len"]),
        mult=float(rf_cfg["bb_mult"]),
    )

    regime_trend = (adx > float(rf_cfg["adx_trend_threshold"])) & (chop < float(rf_cfg["chop_trend_threshold"]))
    regime_range = (adx < float(rf_cfg["adx_range_threshold"])) & (chop > float(rf_cfg["chop_range_threshold"]))

    if bool(rf_cfg["use_bb_filter"]):
        range_long_gate = close <= (bb_lower * 1.02)
        range_short_gate = close >= (bb_upper * 0.98)
    else:
        range_long_gate = pd.Series(True, index=df.index)
        range_short_gate = pd.Series(True, index=df.index)

    adx_prev = adx.shift(1).fillna(adx)
    long_trend = regime_trend & (plus_di > minus_di) & (adx > adx_prev)
    short_trend = regime_trend & (minus_di > plus_di) & (adx > adx_prev)
    long_range = regime_range & (rsi_v < float(rf_cfg["rsi_oversold"])) & range_long_gate
    short_range = regime_range & (rsi_v > float(rf_cfg["rsi_overbought"])) & range_short_gate
    long_raw = long_trend | long_range
    short_raw = short_trend | short_range

    out = df.copy()
    out["up_move"] = up_move
    out["down_move"] = down_move
    out["plus_dm"] = plus_dm
    out["minus_dm"] = minus_dm
    out["tr"] = tr_v
    out["tr_rma"] = tr_rma
    out["plus_rma"] = plus_rma
    out["minus_rma"] = minus_rma
    out["plus_di"] = plus_di
    out["minus_di"] = minus_di
    out["dx"] = dx
    out["adx"] = adx
    out["adx_prev"] = adx_prev
    out["chop"] = chop
    out["rsi"] = rsi_v
    out["bb_upper"] = bb_upper
    out["bb_mid"] = bb_mid
    out["bb_lower"] = bb_lower
    out["regime_trend"] = regime_trend
    out["regime_range"] = regime_range
    out["long_trend"] = long_trend
    out["short_trend"] = short_trend
    out["long_range"] = long_range
    out["short_range"] = short_range
    out["long_raw"] = long_raw
    out["short_raw"] = short_raw
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description="Emit Range Filter Hybrid bar diagnostics around a target timestamp.")
    parser.add_argument("--case", required=True, help="Case JSON path")
    parser.add_argument("--timestamp", required=True, help="UTC timestamp, e.g. 2025-06-30T15:00:00Z")
    parser.add_argument("--window", type=int, default=4, help="Bars before/after target")
    parser.add_argument("--out", required=True, help="Output CSV path")
    args = parser.parse_args()

    case_path = Path(args.case).resolve()
    case_payload = _load_case(case_path)
    df = _load_df(case_path, case_payload["dataset"])
    rf_cfg = case_payload["config"]["range_filter"]
    out = _compute_rf_debug(df, rf_cfg)

    target = pd.Timestamp(args.timestamp)
    target = target.tz_localize("UTC") if target.tzinfo is None else target.tz_convert("UTC")
    idx = out.index[out["timestamp"] == target]
    if len(idx) == 0:
        raise ValueError(f"Timestamp not found in dataset: {target}")
    pos = int(idx[0])
    lo = max(0, pos - args.window)
    hi = min(len(out), pos + args.window + 1)
    cols = [
        "timestamp", "open", "high", "low", "close",
        "up_move", "down_move", "plus_dm", "minus_dm", "tr", "tr_rma",
        "plus_rma", "minus_rma", "plus_di", "minus_di", "dx", "adx", "adx_prev",
        "chop", "rsi", "bb_upper", "bb_mid", "bb_lower",
        "regime_trend", "regime_range", "long_trend", "short_trend",
        "long_range", "short_range", "long_raw", "short_raw",
    ]
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out.iloc[lo:hi][cols].to_csv(out_path, index=False)
    print(out_path)
    print(out.iloc[pos][cols].to_string())


if __name__ == "__main__":
    main()
