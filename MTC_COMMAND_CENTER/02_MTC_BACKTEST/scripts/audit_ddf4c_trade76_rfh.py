from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from mtc_backtest.src.engine.indicators import bollinger_bands, choppiness, rsi, rma, tr
from mtc_backtest.src.modules.signals.range_filter import RangeFilterHybridSignal

DEFAULT_CASE = ROOT / "mtc_backtest/configs/cases/tvddf4c_variants/no_same_bar_no_eqcurve.json"
DEFAULT_DEBUG = ROOT / "debug/optimization/rf_stage7_tvddf4c/debug_python_signals_20260308_234922_b8432c23.csv"
DEFAULT_OUTDIR = ROOT / "mtc_backtest/results/ddf4c_trade76_audit"
WINDOW_START = "2025-10-09T12:00:00+00:00"
WINDOW_END = "2025-10-09T16:00:00+00:00"


def _load_case(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _dataset_path(case_payload: dict) -> Path:
    dataset = case_payload["dataset"]
    return ROOT / "mtc_backtest/data" / dataset


def _load_df(path: Path) -> pd.DataFrame:
    df = pd.read_parquet(path)
    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
        df = df.set_index("timestamp")
    elif not isinstance(df.index, pd.DatetimeIndex):
        raise ValueError(f"{path} missing timestamp axis")
    else:
        if df.index.tz is None:
            df.index = df.index.tz_localize("UTC")
        else:
            df.index = df.index.tz_convert("UTC")
    return df.sort_index()


def _rma_loop(src: pd.Series, length: int) -> pd.Series:
    out = pd.Series(np.nan, index=src.index, dtype=float)
    if length <= 0 or src.empty:
        return out
    vals = src.to_numpy(dtype=float)
    if len(vals) < length:
        return out
    seed = np.nanmean(vals[:length])
    out.iloc[length - 1] = seed
    alpha = 1.0 / float(length)
    prev = seed
    for i in range(length, len(vals)):
        prev = alpha * vals[i] + (1.0 - alpha) * prev
        out.iloc[i] = prev
    return out


def _range_filter_loop(df: pd.DataFrame, cfg: dict) -> pd.DataFrame:
    high = df["high"]
    low = df["low"]
    close = df["close"]

    up_move = high.diff()
    down_move = -low.diff()
    plus_dm = pd.Series(
        np.where((up_move > down_move) & (up_move > 0), up_move, 0.0),
        index=df.index,
        dtype=float,
    )
    minus_dm = pd.Series(
        np.where((down_move > up_move) & (down_move > 0), down_move, 0.0),
        index=df.index,
        dtype=float,
    )
    tr_v = tr(high, low, close)
    tr_rma = _rma_loop(tr_v, 14)
    plus_rma = _rma_loop(plus_dm, 14)
    minus_rma = _rma_loop(minus_dm, 14)
    plus_di = pd.Series(np.where(tr_rma != 0, 100.0 * plus_rma / tr_rma, 0.0), index=df.index, dtype=float)
    minus_di = pd.Series(np.where(tr_rma != 0, 100.0 * minus_rma / tr_rma, 0.0), index=df.index, dtype=float)
    dx = pd.Series(
        np.where((plus_di + minus_di) != 0, 100.0 * (plus_di - minus_di).abs() / (plus_di + minus_di), 0.0),
        index=df.index,
        dtype=float,
    )
    adx = _rma_loop(dx, 14)
    chop = choppiness(high, low, close, length=14)
    rsi_v = rsi(close, length=int(cfg["rsi_len"]))
    bb_upper, bb_mid, bb_lower = bollinger_bands(close, length=int(cfg["bb_len"]), mult=float(cfg["bb_mult"]))

    is_trending = (adx > float(cfg["adx_trend_threshold"])) & (chop < float(cfg["chop_trend_threshold"]))
    is_ranging = (adx < float(cfg["adx_range_threshold"])) & (chop > float(cfg["chop_range_threshold"]))
    adx_prev = adx.shift(1).fillna(adx)
    trend_short = is_trending & (minus_di > plus_di) & (adx > adx_prev)

    if bool(cfg["use_bb_filter"]):
        near_upper = close >= (bb_upper * 0.98)
    else:
        near_upper = pd.Series(True, index=df.index)
    range_short = is_ranging & (rsi_v > float(cfg["rsi_overbought"])) & near_upper
    short_raw = (trend_short | range_short).fillna(False)

    return pd.DataFrame(
        {
            "loop_adx": adx,
            "loop_plus_di": plus_di,
            "loop_minus_di": minus_di,
            "loop_chop": chop,
            "loop_rsi": rsi_v,
            "loop_regime_trend": is_trending,
            "loop_regime_range": is_ranging,
            "loop_trend_short": trend_short,
            "loop_range_short": range_short,
            "loop_short_raw": short_raw,
            "loop_bb_upper": bb_upper,
            "loop_bb_mid": bb_mid,
            "loop_bb_lower": bb_lower,
        },
        index=df.index,
    )


def _load_debug(path: Path) -> pd.DataFrame:
    dbg = pd.read_csv(path)
    dbg["timestamp"] = pd.to_datetime(dbg["timestamp"], utc=True)
    dbg = dbg.set_index("timestamp").sort_index()
    return dbg


def build_audit(case_path: Path, debug_path: Path, outdir: Path) -> None:
    payload = _load_case(case_path)
    ds = _load_df(_dataset_path(payload))
    cfg = payload["config"]["range_filter"]
    plugin = RangeFilterHybridSignal(
        adx_trend_threshold=cfg["adx_trend_threshold"],
        adx_range_threshold=cfg["adx_range_threshold"],
        chop_trend_threshold=cfg["chop_trend_threshold"],
        chop_range_threshold=cfg["chop_range_threshold"],
        rsi_len=cfg["rsi_len"],
        rsi_oversold=cfg["rsi_oversold"],
        rsi_overbought=cfg["rsi_overbought"],
        bb_len=cfg["bb_len"],
        bb_mult=cfg["bb_mult"],
        use_bb_filter=cfg["use_bb_filter"],
    )
    plugin.generate(ds)
    vec = pd.DataFrame(plugin.get_debug_series(ds))
    vec = vec.rename(columns={c: f"vec_{c}" for c in vec.columns})
    vec["vec_adx_prev"] = vec["vec_adx"].shift(1).fillna(vec["vec_adx"])
    vec["vec_adx_rising_margin"] = vec["vec_adx"] - vec["vec_adx_prev"]
    vec["vec_minus_plus_margin"] = vec["vec_minus_di"] - vec["vec_plus_di"]
    vec["vec_adx_trend_margin"] = vec["vec_adx"] - float(cfg["adx_trend_threshold"])
    vec["vec_chop_trend_margin"] = float(cfg["chop_trend_threshold"]) - vec["vec_chop"]

    loop = _range_filter_loop(ds, cfg)
    audit = vec.join(loop, how="outer")
    for lhs, rhs, name in [
        ("vec_adx", "loop_adx", "adx"),
        ("vec_plus_di", "loop_plus_di", "plus_di"),
        ("vec_minus_di", "loop_minus_di", "minus_di"),
        ("vec_chop", "loop_chop", "chop"),
    ]:
        audit[f"delta_{name}"] = audit[lhs] - audit[rhs]
    audit["delta_short_raw"] = (
        audit["vec_short_raw"].fillna(False).astype(int) - audit["loop_short_raw"].fillna(False).astype(int)
    )

    dbg = _load_debug(debug_path)[
        [
            "sig_short_raw",
            "entry_signal_short",
            "guardAllow",
            "finalShortEntry",
            "allowShort",
            "sig_adx",
            "sig_plus_di",
            "sig_minus_di",
            "sig_chop",
            "sig_regime_trend",
        ]
    ]
    audit = audit.join(dbg, how="left")
    window = audit.loc[WINDOW_START:WINDOW_END].copy()

    outdir.mkdir(parents=True, exist_ok=True)
    csv_path = outdir / "trade76_window.csv"
    md_path = outdir / "trade76_window.md"
    window.to_csv(csv_path, index=True)

    flip_rows = window.index[window["vec_short_raw"].fillna(False)]
    first_vec_short_raw = flip_rows.min() if len(flip_rows) else None
    guard_rows = window.index[window["guardAllow"].fillna(False)]
    first_guard = guard_rows.min() if len(guard_rows) else None
    entry_rows = window.index[window["finalShortEntry"].fillna(False)]
    first_entry = entry_rows.min() if len(entry_rows) else None

    snapshot_cols = [
        "vec_adx",
        "vec_adx_prev",
        "vec_adx_rising_margin",
        "vec_plus_di",
        "vec_minus_di",
        "vec_minus_plus_margin",
        "vec_chop",
        "vec_adx_trend_margin",
        "vec_chop_trend_margin",
        "vec_regime_trend",
        "vec_short_raw",
        "loop_short_raw",
        "delta_adx",
        "delta_plus_di",
        "delta_minus_di",
        "delta_chop",
        "sig_short_raw",
        "entry_signal_short",
        "guardAllow",
        "finalShortEntry",
    ]

    lines = [
        "# DDF4C Trade 76 RF Audit",
        "",
        f"- Case: `{case_path.as_posix()}`",
        f"- Debug: `{debug_path.as_posix()}`",
        f"- Window: `{WINDOW_START}` -> `{WINDOW_END}`",
        "",
        "## First Bars",
        f"- First vectorized `short_raw=true`: `{first_vec_short_raw}`",
        f"- First engine `guardAllow=true`: `{first_guard}`",
        f"- First engine `finalShortEntry=true`: `{first_entry}`",
        "",
        "## Findings",
        "- Vectorized and loop RF calculations match within numerical noise if the deltas below stay near zero.",
        "- If `vec_short_raw` is already true before `guardAllow`, the remaining delay is not RF raw generation.",
        "- If `guardAllow` turns true one bar before TV still waits, the remaining suspect is Pine-side RF timing or non-exported gate timing.",
        "",
        "## Snapshot",
        "",
        "```text",
        window[snapshot_cols].to_string(),
        "```",
        "",
    ]
    md_path.write_text("\n".join(lines), encoding="utf-8")
    print(csv_path)
    print(md_path)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", type=Path, default=DEFAULT_CASE)
    parser.add_argument("--debug", type=Path, default=DEFAULT_DEBUG)
    parser.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    args = parser.parse_args()
    build_audit(args.case.resolve(), args.debug.resolve(), args.outdir.resolve())


if __name__ == "__main__":
    main()
