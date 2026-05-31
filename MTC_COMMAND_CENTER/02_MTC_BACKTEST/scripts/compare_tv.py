#!/usr/bin/env python
"""
Parity comparison: TradingView CSV vs Python debug trades CSV.

Usage:
    python scripts/compare_tv.py <tv_csv> <py_trades_csv>
    python scripts/compare_tv.py  (auto-detect from case file)
    python scripts/compare_tv.py configs/cases/dec2025_parity.json

Reads both CSVs, pairs trades by entry time, and reports mismatches.
"""
import sys
import json
from pathlib import Path
from typing import Optional

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(PROJECT_ROOT))

import pandas as pd


def _parse_tv_time(raw: str, tv_tz: str = "Europe/London") -> pd.Timestamp:
    """
    Parse a single TV timestamp string into a UTC pd.Timestamp.

    TV exports timestamps in the chart's display timezone.  If that TZ
    observes DST (e.g. Europe/London = GMT in winter, BST = UTC+1 in
    summer) a fixed minute-shift is *wrong* -- we must localize first,
    then convert to UTC so the offset adapts to the date.

    Parameters
    ----------
    raw : str    e.g. "2025-10-10 22:30"
    tv_tz : str  IANA timezone of the TV chart, default "Europe/London"
    """
    ts = pd.to_datetime(raw, errors="coerce")
    if pd.isna(ts):
        return pd.NaT
    # Localize as the TV display timezone, then convert to UTC.
    # Keep strategy aligned with src.parity.compare_tv_trades._parse_dt_to_utc.
    s = pd.Series([ts])
    try:
        s = s.dt.tz_localize(tv_tz, ambiguous="infer", nonexistent="shift_forward")
    except Exception:
        s = s.dt.tz_localize(tv_tz, ambiguous=True, nonexistent="shift_forward")
    return s.dt.tz_convert("UTC").iloc[0]


def load_tv_csv(path: str, tv_tz: str = "Europe/London") -> pd.DataFrame:
    """
    Load TradingView 'List of trades' export.

    TV CSV has pairs of rows per trade: Entry row + Exit row, both sharing the same Trade #.
    We pivot into one row per trade with entry/exit columns.

    Parameters
    ----------
    tv_tz : str
        IANA timezone of the TradingView chart display. Timestamps in the
        CSV are in this timezone and will be converted to UTC.
        Default "Europe/London" (GMT winter / BST summer).
    """
    p = Path(path)
    if not p.exists():
        p = PROJECT_ROOT / path
    if not p.exists():
        print(f"ERROR: TV CSV not found: {path}")
        sys.exit(1)

    # TV CSVs can have BOM and varied encodings
    for enc in ("utf-8-sig", "utf-8", "cp1252", "latin-1"):
        try:
            df = pd.read_csv(p, encoding=enc)
            break
        except (UnicodeDecodeError, pd.errors.ParserError):
            continue
    else:
        print(f"ERROR: Could not decode TV CSV: {path}")
        sys.exit(1)

    # Normalize column names (strip whitespace)
    df.columns = df.columns.str.strip()

    # Find key columns (TV uses various naming conventions)
    trade_col = next((c for c in df.columns if "trade" in c.lower() and "#" in c.lower()), None)
    type_col = next((c for c in df.columns if "type" in c.lower()), None)
    time_col = next((c for c in df.columns if "date" in c.lower() or "time" in c.lower()), None)
    signal_col = next((c for c in df.columns if "signal" in c.lower()), None)
    price_col = next((c for c in df.columns if "price" in c.lower()), None)
    pnl_col = next((c for c in df.columns if "p&l" in c.lower() or "profit" in c.lower() or "pnl" in c.lower()), None)

    if not all([trade_col, type_col, time_col]):
        print(f"WARNING: Could not identify TV CSV columns. Found: {list(df.columns)}")
        print("Attempting generic parse...")
        return df

    # Build unified trade list
    trades = []
    grouped = df.groupby(trade_col)
    for trade_num, group in grouped:
        entry_rows = group[group[type_col].str.contains("Entry", case=False, na=False)]
        exit_rows = group[group[type_col].str.contains("Exit", case=False, na=False)]

        if len(entry_rows) == 0:
            continue

        entry = entry_rows.iloc[0]
        side = "LONG" if "long" in str(entry[type_col]).lower() else "SHORT"
        entry_time = _parse_tv_time(entry[time_col], tv_tz=tv_tz)
        entry_price = float(str(entry[price_col]).replace(",", "").replace(" ", "")) if price_col else None

        exit_time = None
        exit_price = None
        exit_signal = None
        net_pnl = None

        if len(exit_rows) > 0:
            ex = exit_rows.iloc[0]
            exit_time = _parse_tv_time(ex[time_col], tv_tz=tv_tz)
            exit_price = float(str(ex[price_col]).replace(",", "").replace(" ", "")) if price_col else None
            exit_signal = str(ex[signal_col]).strip() if signal_col else None
            if pnl_col:
                try:
                    net_pnl = float(str(ex[pnl_col]).replace(",", "").replace(" ", "").replace("−", "-"))
                except (ValueError, AttributeError):
                    net_pnl = None

        trades.append({
            "trade_num": int(trade_num) if not pd.isna(trade_num) else 0,
            "side": side,
            "entry_time": entry_time,
            "entry_price": entry_price,
            "exit_time": exit_time,
            "exit_signal": exit_signal,
            "exit_price": exit_price,
            "net_pnl": net_pnl,
        })

    return pd.DataFrame(trades).sort_values("entry_time").reset_index(drop=True)


def load_py_csv(path: str) -> pd.DataFrame:
    """Load Python debug_python_trades CSV."""
    p = Path(path)
    if not p.exists():
        p = PROJECT_ROOT / path
    if not p.exists():
        print(f"ERROR: Python trades CSV not found: {path}")
        sys.exit(1)

    df = pd.read_csv(p)
    df["entry_time"] = pd.to_datetime(df["entry_timestamp"], utc=True)
    df["exit_time"] = pd.to_datetime(df["exit_timestamp"], utc=True)

    trades = []
    for _, row in df.iterrows():
        trades.append({
            "side": row["side"].upper(),
            "entry_time": row["entry_time"],
            "entry_price": row["entry_price"],
            "exit_time": row["exit_time"],
            "exit_signal": row.get("reason", ""),
            "exit_price": row["exit_price"],
            "net_pnl": row["pnl"],
        })

    return pd.DataFrame(trades).sort_values("entry_time").reset_index(drop=True)


def compare(tv: pd.DataFrame, py: pd.DataFrame, max_mismatches: int = 20):
    """Compare TV and Python trades, print report."""

    print(f"\n{'='*70}")
    print(f"PARITY COMPARISON REPORT")
    print(f"{'='*70}")
    print(f"  TV trades  : {len(tv)}")
    print(f"  PY trades  : {len(py)}")
    print(f"  Difference : {len(tv) - len(py)}")
    print()

    # Quick metric comparison
    if "net_pnl" in tv.columns and "net_pnl" in py.columns:
        tv_pnl = tv["net_pnl"].dropna().sum()
        py_pnl = py["net_pnl"].dropna().sum()
        print(f"  TV Net P&L : ${tv_pnl:>10.2f}")
        print(f"  PY Net P&L : ${py_pnl:>10.2f}")
        print(f"  P&L Diff   : ${tv_pnl - py_pnl:>10.2f}")
        print()

    # Exit reason distribution
    print("  Exit Reason Distribution:")
    print(f"  {'Reason':<12s} {'TV':>6s} {'PY':>6s} {'Diff':>6s}")
    print(f"  {'-'*36}")
    all_reasons = set()
    tv_reasons: dict[str, int] = {}
    py_reasons: dict[str, int] = {}
    if "exit_signal" in tv.columns:
        for r in tv["exit_signal"].dropna():
            r = str(r).strip().upper()
            tv_reasons[r] = tv_reasons.get(r, 0) + 1
            all_reasons.add(r)
    if "exit_signal" in py.columns:
        for r in py["exit_signal"].dropna():
            r = str(r).strip().upper()
            py_reasons[r] = py_reasons.get(r, 0) + 1
            all_reasons.add(r)
    for reason in sorted(all_reasons):
        tc = tv_reasons.get(reason, 0)
        pc = py_reasons.get(reason, 0)
        marker = " *" if tc != pc else ""
        print(f"  {reason:<12s} {tc:>6d} {pc:>6d} {tc-pc:>+6d}{marker}")
    print()

    # Trade-by-trade matching (by entry_time nearest neighbor)
    print(f"  First {max_mismatches} Mismatches (entry time pairing):")
    print(f"  {'#':>3s} {'TV Entry':>20s} {'PY Entry':>20s} {'TimeDiff':>10s} {'TV Side':>7s} {'PY Side':>7s} {'TV Exit':>8s} {'PY Exit':>8s} {'TV P&L':>10s} {'PY P&L':>10s}")
    print(f"  {'-'*120}")

    mismatch_count = 0
    matched_py = set()

    for i, tv_row in tv.iterrows():
        # Find nearest PY trade by entry time
        best_idx = None
        best_diff = pd.Timedelta(hours=999)
        for j, py_row in py.iterrows():
            if j in matched_py:
                continue
            diff = abs(tv_row["entry_time"] - py_row["entry_time"])
            if diff < best_diff:
                best_diff = diff
                best_idx = j

        if best_idx is not None and best_diff <= pd.Timedelta(hours=2):
            py_row = py.iloc[best_idx]
            matched_py.add(best_idx)

            # Check for mismatches
            side_match = tv_row["side"] == py_row["side"]
            time_match = best_diff <= pd.Timedelta(minutes=30)
            exit_match = str(tv_row.get("exit_signal", "")).strip().upper() == str(py_row.get("exit_signal", "")).strip().upper()

            if not (side_match and time_match and exit_match):
                mismatch_count += 1
                if mismatch_count <= max_mismatches:
                    tv_exit = str(tv_row.get("exit_signal", ""))[:8]
                    py_exit = str(py_row.get("exit_signal", ""))[:8]
                    tv_pnl = f"${tv_row.get('net_pnl', 0):>8.2f}" if pd.notna(tv_row.get("net_pnl")) else "     N/A"
                    py_pnl = f"${py_row.get('net_pnl', 0):>8.2f}" if pd.notna(py_row.get("net_pnl")) else "     N/A"
                    print(f"  {mismatch_count:>3d} {str(tv_row['entry_time']):>20s} {str(py_row['entry_time']):>20s} {str(best_diff):>10s} {tv_row['side']:>7s} {py_row['side']:>7s} {tv_exit:>8s} {py_exit:>8s} {tv_pnl:>10s} {py_pnl:>10s}")
        else:
            # TV trade has no PY match
            mismatch_count += 1
            if mismatch_count <= max_mismatches:
                tv_exit = str(tv_row.get("exit_signal", ""))[:8]
                tv_pnl = f"${tv_row.get('net_pnl', 0):>8.2f}" if pd.notna(tv_row.get("net_pnl")) else "     N/A"
                print(f"  {mismatch_count:>3d} {str(tv_row['entry_time']):>20s} {'--- NO MATCH ---':>20s} {'':>10s} {tv_row['side']:>7s} {'':>7s} {tv_exit:>8s} {'':>8s} {tv_pnl:>10s} {'':>10s}")

    # PY trades with no TV match
    unmatched_py = set(range(len(py))) - matched_py
    for j in sorted(unmatched_py):
        mismatch_count += 1
        if mismatch_count <= max_mismatches:
            py_row = py.iloc[j]
            py_exit = str(py_row.get("exit_signal", ""))[:8]
            py_pnl = f"${py_row.get('net_pnl', 0):>8.2f}" if pd.notna(py_row.get("net_pnl")) else "     N/A"
            print(f"  {mismatch_count:>3d} {'--- NO MATCH ---':>20s} {str(py_row['entry_time']):>20s} {'':>10s} {'':>7s} {py_row['side']:>7s} {'':>8s} {py_exit:>8s} {'':>10s} {py_pnl:>10s}")

    print(f"\n  Total mismatches: {mismatch_count}")

    # Matched stats
    matched_count = len(tv) - mismatch_count + len(unmatched_py)
    total = max(len(tv), len(py))
    parity_pct = (1 - mismatch_count / total) * 100 if total > 0 else 0
    print(f"  Parity score : {parity_pct:.1f}%")
    print(f"{'='*70}\n")

    return mismatch_count


def auto_detect_from_case(case_path: str) -> tuple[Optional[str], Optional[str], str]:
    """Try to auto-detect TV CSV, PY CSV, and TV timezone from a case file.

    Returns (tv_csv, py_csv, tv_tz).
    """
    p = Path(case_path)
    if not p.exists():
        p = PROJECT_ROOT / case_path
    if not p.exists():
        return None, None, "Europe/London"

    with open(p, encoding="utf-8") as f:
        case = json.load(f)

    tv_csv = case.get("tv_csv")
    tv_tz = case.get("tv_tz", "Europe/London")
    debug_dir = case.get("config", {}).get("parity", {}).get("debug_dir", "debug")

    # Find latest PY trades CSV in debug dir
    py_csv = None
    dd = PROJECT_ROOT / debug_dir
    if dd.exists():
        py_files = sorted(dd.glob("debug_python_trades_*.csv"), key=lambda x: x.stat().st_mtime, reverse=True)
        if py_files:
            py_csv = str(py_files[0].relative_to(PROJECT_ROOT))

    return tv_csv, py_csv, tv_tz


if __name__ == "__main__":
    tv_tz = "Europe/London"  # default

    if len(sys.argv) == 2 and sys.argv[1].endswith(".json"):
        # Auto-detect from case file
        tv_path, py_path, tv_tz = auto_detect_from_case(sys.argv[1])
        if not tv_path or not py_path:
            print("ERROR: Could not auto-detect CSV paths from case file.")
            print(f"  TV CSV: {tv_path}")
            print(f"  PY CSV: {py_path}")
            sys.exit(1)
        print(f"Auto-detected from case file:")
        print(f"  TV: {tv_path}")
        print(f"  PY: {py_path}")
        print(f"  TZ: {tv_tz}")
    elif len(sys.argv) == 3:
        tv_path = sys.argv[1]
        py_path = sys.argv[2]
    elif len(sys.argv) == 4:
        tv_path = sys.argv[1]
        py_path = sys.argv[2]
        tv_tz = sys.argv[3]
    else:
        print("Usage:")
        print("  python scripts/compare_tv.py <tv_csv> <py_trades_csv> [tv_tz]")
        print("  python scripts/compare_tv.py configs/cases/dec2025_parity.json")
        print("  tv_tz: IANA timezone of TV chart (default: Europe/London)")
        sys.exit(1)

    tv = load_tv_csv(tv_path, tv_tz=tv_tz)
    py = load_py_csv(py_path)
    compare(tv, py)
