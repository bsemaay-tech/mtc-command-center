#!/usr/bin/env python
"""
Parity regression gate.

Runs the canonical parity case, compares with TV reference CSV,
and exits non-zero if any acceptance criterion fails.

Usage:
    python scripts/parity_regression.py
    python scripts/parity_regression.py configs/cases/full_jul2025_jan2026_parity.json
"""
import sys
import json
from pathlib import Path
from datetime import datetime, time, timezone, timedelta

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(PROJECT_ROOT))

DEFAULT_CASE = "configs/cases/full_jul2025_jan2026_parity.json"

# ---------- acceptance thresholds ----------
MAX_MISMATCH = 0
MAX_PNL_DELTA = 10.0  # USDT absolute
MAX_DD_PCT_DELTA = 10.0  # absolute percentage points (realized TV DD vs PY DD)


def _parse_dt(raw: str, *, as_end: bool = False) -> datetime:
    """Parse date or ISO datetime string to UTC datetime."""
    try:
        dt = datetime.fromisoformat(raw)
    except ValueError:
        dt = datetime.strptime(raw, "%Y-%m-%d")
    if dt.hour == 0 and dt.minute == 0 and dt.second == 0 and "T" not in raw:
        dt = datetime.combine(dt.date(), time.max if as_end else time.min)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


def _tv_realized_max_drawdown_pct(tv_trades_df, initial_capital: float) -> float:
    """
    Compute realized max drawdown % from TradingView trade rows.

    We use cumulative realized PnL reconstructed from closed trades:
      equity = initial_capital + cumsum(net_pnl)
      drawdown_pct = (peak_equity - equity) / peak_equity * 100
    """
    if tv_trades_df is None or len(tv_trades_df) == 0:
        return 0.0
    pnl = tv_trades_df.get("net_pnl")
    if pnl is None:
        return 0.0
    pnl = pnl.dropna()
    if pnl.empty:
        return 0.0

    realized_eq = float(initial_capital) + pnl.cumsum()
    peak = realized_eq.cummax()
    dd_pct = ((peak - realized_eq) / peak.replace(0, float("nan"))) * 100.0
    return float(dd_pct.max()) if len(dd_pct) else 0.0


def run(case_path: str) -> int:
    """Run parity regression. Returns 0 on pass, 1 on fail."""
    import pandas as pd
    from src.config.defaults import MTCConfig
    from src.engine.mtc_runner import MTCRunner

    case_file = PROJECT_ROOT / case_path
    with open(case_file, encoding="utf-8") as f:
        case = json.load(f)

    # --- 1. Run backtest ---
    config = MTCConfig.model_validate(case.get("config", {}))
    # Force disable debug export for speed
    config.parity.export_debug_csv = False

    dataset_path = PROJECT_ROOT / "data" / case["dataset"]
    if dataset_path.suffix == ".parquet":
        df = pd.read_parquet(dataset_path)
    else:
        df = pd.read_csv(dataset_path)

    if "timestamp" in df.columns:
        if pd.api.types.is_numeric_dtype(df["timestamp"]):
            df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms", utc=True)
        else:
            df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
    if df["timestamp"].dt.tz is None:
        df["timestamp"] = df["timestamp"].dt.tz_localize("UTC")
    else:
        df["timestamp"] = df["timestamp"].dt.tz_convert("UTC")

    start_dt = _parse_dt(case["start_date"], as_end=False)
    end_dt = _parse_dt(case["end_date"], as_end=True)
    preroll_days = case.get("preroll_days", 90)

    filter_start = start_dt - timedelta(days=preroll_days) if preroll_days > 0 else start_dt
    mask = (df["timestamp"] >= filter_start) & (df["timestamp"] <= end_dt)
    df_filtered = df.loc[mask].copy().reset_index(drop=True)

    warmup_bars = case.get("warmup_bars", 200)
    runner = MTCRunner(config)
    results = runner.run(
        df_filtered,
        warmup_bars=warmup_bars,
        eval_start=start_dt if preroll_days > 0 else None,
        eval_end=end_dt,
    )
    py_trades = results["trades"]
    py_count = len(py_trades)

    # --- 2. Load TV trades ---
    tv_csv_path = PROJECT_ROOT / case.get("tv_csv", "")
    if not tv_csv_path.exists():
        print(f"FAIL: TV CSV not found: {tv_csv_path}")
        return 1

    # Import compare_tv functions (with DST-aware parsing)
    sys.path.insert(0, str(SCRIPT_DIR))
    from compare_tv import load_tv_csv, load_py_csv

    tv_tz = case.get("tv_tz", "Europe/London")
    tv = load_tv_csv(str(tv_csv_path), tv_tz=tv_tz)

    # Filter out "Open" trades from TV (unclosed positions)
    tv = tv[tv["exit_signal"].astype(str).str.upper().str.strip() != "OPEN"].reset_index(drop=True)
    tv_count = len(tv)

    # --- 3. Compare ---
    # Build simple comparison: pair by entry_time
    failures = []

    # a) Trade count
    if tv_count != py_count:
        failures.append(f"Trade count: TV={tv_count} PY={py_count} delta={py_count - tv_count}")

    # b) Detailed matching (clip to overlapping window)
    from src.parity.compare_tv_trades import load_tv_trades, load_py_trades, clip_overlap, build_report

    tv_det = load_tv_trades(tv_csv_path, tv_tz=tv_tz, tv_shift_min=0)
    # Exclude TV "Open" trades
    tv_det = tv_det[tv_det["reason"].astype(str).str.upper() != "OPEN"].reset_index(drop=True)
    tv_det["seq"] = range(1, len(tv_det) + 1)

    # Write PY trades to temp CSV for loading
    import tempfile, os
    py_pnl_total = sum(t.pnl for t in py_trades)

    # Use latest debug CSV if available, else create temp
    debug_dir = PROJECT_ROOT / config.parity.debug_dir
    py_csv_candidates = sorted(debug_dir.glob("debug_python_trades_*.csv"), key=lambda x: x.stat().st_mtime, reverse=True) if debug_dir.exists() else []

    if not py_csv_candidates:
        # Need to re-run with export
        config.parity.export_debug_csv = True
        runner2 = MTCRunner(config)
        results2 = runner2.run(
            df_filtered,
            warmup_bars=warmup_bars,
            eval_start=start_dt if preroll_days > 0 else None,
            eval_end=end_dt,
        )
        py_csv_candidates = sorted(debug_dir.glob("debug_python_trades_*.csv"), key=lambda x: x.stat().st_mtime, reverse=True)

    py_det = load_py_trades(py_csv_candidates[0])
    tv_clip, py_clip = clip_overlap(tv_det, py_det)
    report = build_report(tv_clip, py_clip)

    mismatches = int((~report["all_core_match"]).sum())
    if mismatches > MAX_MISMATCH:
        failures.append(f"Core mismatches: {mismatches}/{len(report)}")

    # c) P&L delta (from TV closed trades vs PY)
    tv_pnl_total = tv["net_pnl"].dropna().sum() if "net_pnl" in tv.columns else 0.0
    pnl_delta = abs(py_pnl_total - tv_pnl_total)
    if pnl_delta > MAX_PNL_DELTA:
        failures.append(f"P&L delta: {pnl_delta:.2f} USDT (threshold {MAX_PNL_DELTA})")

    # d) Drawdown parity (TV realized DD% vs Python DD%)
    py_dd_pct = float(results["metrics"].get("max_drawdown", 0.0))
    tv_dd_pct = _tv_realized_max_drawdown_pct(tv, float(config.strategy.initial_capital))
    dd_delta = abs(py_dd_pct - tv_dd_pct)
    if dd_delta > MAX_DD_PCT_DELTA:
        failures.append(
            f"DD delta: {dd_delta:.2f} pct (TV={tv_dd_pct:.2f}, PY={py_dd_pct:.2f}, threshold {MAX_DD_PCT_DELTA})"
        )

    # --- 4. Report ---
    if failures:
        print(
            "FAIL | "
            f"trades TV={tv_count} PY={py_count} | mismatches={mismatches} | "
            f"pnl_delta={pnl_delta:.2f} | dd_tv={tv_dd_pct:.2f}% dd_py={py_dd_pct:.2f}% dd_delta={dd_delta:.2f}"
        )
        for f in failures:
            print(f"  - {f}")
        return 1
    else:
        print(
            "PASS | "
            f"trades={tv_count} | mismatches=0 | pnl_delta={pnl_delta:.2f} USDT | "
            f"dd_tv={tv_dd_pct:.2f}% dd_py={py_dd_pct:.2f}% dd_delta={dd_delta:.2f}"
        )
        return 0


if __name__ == "__main__":
    case = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_CASE
    sys.exit(run(case))
