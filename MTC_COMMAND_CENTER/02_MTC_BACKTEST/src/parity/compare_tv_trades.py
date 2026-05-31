"""
Compare TradingView trade list CSV vs Python debug trades CSV.

Usage:
  python -m src.parity.compare_tv_trades \
      --tv debug/tv_trades.csv \
      --py debug/debug_python_trades.csv \
      --out debug/parity_compare_report.csv \
      --clip-overlap
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any, Dict, Tuple

import pandas as pd
from pandas.errors import EmptyDataError


def _normalize_reason(v: str) -> str:
    s = (v or "").strip().upper()
    mapping = {
        "OPEN": "MANUAL",
    }
    return mapping.get(s, s)


def _normalize_side(v: str) -> str:
    s = (v or "").strip().upper()
    if s.startswith("LONG"):
        return "LONG"
    if s.startswith("SHORT"):
        return "SHORT"
    return s


def _parse_dt_to_utc(series: pd.Series, source_tz: str, shift_min: int = 0) -> pd.Series:
    """
    Parse timestamp series and normalize to UTC.

    - If input is tz-naive, localize with `source_tz`.
    - If input is tz-aware, convert directly to UTC.
    - Apply optional minute shift for anchor normalization.
    """
    dt = pd.to_datetime(series, errors="coerce", utc=False)
    if getattr(dt.dt, "tz", None) is None:
        try:
            # Prefer deterministic DST inference when sequence permits.
            dt = dt.dt.tz_localize(source_tz, ambiguous="infer", nonexistent="shift_forward")
        except Exception:
            # Fall back to first occurrence for ambiguous clock-back hours.
            dt = dt.dt.tz_localize(source_tz, ambiguous=True, nonexistent="shift_forward")
    dt = dt.dt.tz_convert("UTC")
    if shift_min:
        dt = dt + pd.to_timedelta(int(shift_min), unit="m")
    return dt


def _empty_trade_frame() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "seq": pd.Series(dtype="int64"),
            "side": pd.Series(dtype="object"),
            "entry_time": pd.Series(dtype="datetime64[ns, UTC]"),
            "exit_time": pd.Series(dtype="datetime64[ns, UTC]"),
            "entry_price": pd.Series(dtype="float64"),
            "exit_price": pd.Series(dtype="float64"),
            "qty": pd.Series(dtype="float64"),
            "reason": pd.Series(dtype="object"),
        }
    )


def load_tv_trades(path: Path, tv_tz: str = "UTC", tv_shift_min: int = 0) -> pd.DataFrame:
    if not path.exists() or path.stat().st_size == 0:
        return _empty_trade_frame()
    try:
        df = pd.read_csv(path)
    except EmptyDataError:
        return _empty_trade_frame()
    df.columns = [c.strip() for c in df.columns]

    if df.empty:
        return _empty_trade_frame()

    trade_col = next((c for c in df.columns if c.startswith("Trade")), "")
    if not trade_col:
        return _empty_trade_frame()
    type_col = "Type"
    dt_col = "Date and time"
    signal_col = "Signal"
    price_col = next((c for c in df.columns if c.startswith("Price")), "")
    qty_col = next((c for c in df.columns if "(qty)" in c), "")
    if not qty_col:
        qty_col = next((c for c in df.columns if c.strip().lower() == "position size"), "")
    if not qty_col:
        qty_col = next((c for c in df.columns if c.lower().startswith("position size")), "")
    if not price_col or not qty_col:
        return _empty_trade_frame()
    for c in (type_col, dt_col, signal_col):
        if c not in df.columns:
            return _empty_trade_frame()

    df[trade_col] = pd.to_numeric(df[trade_col], errors="coerce").astype("Int64")
    df[dt_col] = _parse_dt_to_utc(df[dt_col], source_tz=tv_tz, shift_min=tv_shift_min)
    df[price_col] = pd.to_numeric(df[price_col], errors="coerce")
    df[qty_col] = pd.to_numeric(df[qty_col], errors="coerce")

    rows = []
    for tid, g in df.groupby(trade_col, dropna=True):
        g = g.sort_values(dt_col)
        entry = g[g[type_col].str.contains("Entry", case=False, na=False)]
        exit_ = g[g[type_col].str.contains("Exit", case=False, na=False)]
        if entry.empty or exit_.empty:
            continue
        e = entry.iloc[0]
        x = exit_.iloc[0]

        side = _normalize_side(str(e[signal_col]))
        rows.append(
            {
                "seq": int(tid),
                "side": side,
                "entry_time": e[dt_col],
                "exit_time": x[dt_col],
                "entry_price": float(e[price_col]),
                "exit_price": float(x[price_col]),
                "qty": float(e[qty_col]),
                "reason": _normalize_reason(str(x[signal_col])),
            }
        )

    if not rows:
        return _empty_trade_frame()
    out = pd.DataFrame(rows).sort_values("seq").reset_index(drop=True)
    out["seq"] = out.index + 1
    return out


def load_py_trades(path: Path, py_shift_min: int = 0) -> pd.DataFrame:
    if not path.exists() or path.stat().st_size == 0:
        return _empty_trade_frame()
    try:
        df = pd.read_csv(path)
    except EmptyDataError:
        return _empty_trade_frame()
    required = {
        "entry_timestamp",
        "exit_timestamp",
        "side",
        "entry_price",
        "exit_price",
        "qty",
        "reason",
    }
    if not required.issubset(set(df.columns)):
        return _empty_trade_frame()
    if df.empty:
        return _empty_trade_frame()
    df["entry_time"] = pd.to_datetime(df["entry_timestamp"], errors="coerce", utc=True)
    df["exit_time"] = pd.to_datetime(df["exit_timestamp"], errors="coerce", utc=True)
    if py_shift_min:
        shift_td = pd.to_timedelta(int(py_shift_min), unit="m")
        df["entry_time"] = df["entry_time"] + shift_td
        df["exit_time"] = df["exit_time"] + shift_td
    out = pd.DataFrame(
        {
            "seq": range(1, len(df) + 1),
            "side": df["side"].astype(str).map(_normalize_side),
            "entry_time": df["entry_time"],
            "exit_time": df["exit_time"],
            "entry_price": pd.to_numeric(df["entry_price"], errors="coerce"),
            "exit_price": pd.to_numeric(df["exit_price"], errors="coerce"),
            "qty": pd.to_numeric(df["qty"], errors="coerce"),
            "reason": df["reason"].astype(str).map(_normalize_reason),
        }
    )
    return out


def clip_overlap(tv: pd.DataFrame, py: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    t0 = max(tv["entry_time"].min(), py["entry_time"].min())
    t1 = min(tv["exit_time"].max(), py["exit_time"].max())
    tv2 = tv[(tv["entry_time"] >= t0) & (tv["exit_time"] <= t1)].copy()
    py2 = py[(py["entry_time"] >= t0) & (py["exit_time"] <= t1)].copy()
    tv2["seq"] = range(1, len(tv2) + 1)
    py2["seq"] = range(1, len(py2) + 1)
    return tv2.reset_index(drop=True), py2.reset_index(drop=True)


def _core_key(row: pd.Series) -> tuple[str, str, str, str]:
    return (
        str(row["side"]),
        str(row["entry_time"]),
        str(row["exit_time"]),
        str(row["reason"]),
    )


def normalize_broker_reporting(
    tv: pd.DataFrame,
    py: pd.DataFrame,
    *,
    qty_tol: float = 2e-6,
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Normalize TV/Python reporting-only split differences before parity compare.

    TradingView's broker emulator can sometimes export a single full-size exit row
    where the Python engine exports two consecutive rows with the same core key
    (side, entry/exit timestamps, reason) whose quantities sum to the TV row.
    The reverse can also occur. This helper collapses only those asymmetric
    one-vs-two reporting pairs and leaves symmetric one-vs-one / two-vs-two
    sequences untouched.
    """
    if tv.empty or py.empty:
        return tv.copy(), py.copy()

    tv = tv.reset_index(drop=True).copy()
    py = py.reset_index(drop=True).copy()
    out_tv: list[dict[str, Any]] = []
    out_py: list[dict[str, Any]] = []
    i = 0
    j = 0

    while i < len(tv) and j < len(py):
        tv_row = tv.iloc[i]
        py_row = py.iloc[j]
        tv_key = _core_key(tv_row)
        py_key = _core_key(py_row)

        if tv_key == py_key:
            tv_has_pair = i + 1 < len(tv) and _core_key(tv.iloc[i + 1]) == tv_key
            py_has_pair = j + 1 < len(py) and _core_key(py.iloc[j + 1]) == py_key

            if py_has_pair and not tv_has_pair:
                py_qty_sum = float(py.iloc[j]["qty"]) + float(py.iloc[j + 1]["qty"])
                if abs(py_qty_sum - float(tv_row["qty"])) <= float(qty_tol):
                    merged_py = py.iloc[j].copy()
                    merged_py["qty"] = py_qty_sum
                    out_tv.append(tv_row.to_dict())
                    out_py.append(merged_py.to_dict())
                    i += 1
                    j += 2
                    continue

            if tv_has_pair and not py_has_pair:
                tv_qty_sum = float(tv.iloc[i]["qty"]) + float(tv.iloc[i + 1]["qty"])
                if abs(tv_qty_sum - float(py_row["qty"])) <= float(qty_tol):
                    merged_tv = tv.iloc[i].copy()
                    merged_tv["qty"] = tv_qty_sum
                    out_tv.append(merged_tv.to_dict())
                    out_py.append(py_row.to_dict())
                    i += 2
                    j += 1
                    continue

        out_tv.append(tv_row.to_dict())
        out_py.append(py_row.to_dict())
        i += 1
        j += 1

    if i < len(tv):
        out_tv.extend(tv.iloc[i:].to_dict("records"))
    if j < len(py):
        out_py.extend(py.iloc[j:].to_dict("records"))

    tv_out = pd.DataFrame(out_tv) if out_tv else _empty_trade_frame()
    py_out = pd.DataFrame(out_py) if out_py else _empty_trade_frame()
    if not tv_out.empty:
        tv_out["seq"] = range(1, len(tv_out) + 1)
    if not py_out.empty:
        py_out["seq"] = range(1, len(py_out) + 1)
    tv_out = tv_out.reset_index(drop=True)
    py_out = py_out.reset_index(drop=True)
    tv_out, py_out = normalize_margin_call_be_clusters(tv_out, py_out)
    return tv_out.reset_index(drop=True), py_out.reset_index(drop=True)


def _compress_margin_call_be_clusters(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df.copy()

    out: list[dict[str, Any]] = []
    i = 0
    while i < len(df):
        row = df.iloc[i]
        side = row["side"]
        entry_time = row["entry_time"]
        j = i
        cluster: list[pd.Series] = []
        while (
            j < len(df)
            and df.iloc[j]["side"] == side
            and df.iloc[j]["entry_time"] == entry_time
            and str(df.iloc[j]["reason"]) in {"MARGIN CALL", "BE"}
        ):
            cluster.append(df.iloc[j])
            j += 1

        reasons = {str(r["reason"]) for r in cluster}
        if len(cluster) >= 2 and reasons == {"MARGIN CALL", "BE"}:
            mc_rows = [r for r in cluster if str(r["reason"]) == "MARGIN CALL"]
            be_rows = [r for r in cluster if str(r["reason"]) == "BE"]

            mc_rep = mc_rows[0].copy()
            mc_rep["qty"] = sum(float(r["qty"]) for r in mc_rows)
            out.append(mc_rep.to_dict())

            be_rep = be_rows[0].copy()
            be_rep["qty"] = sum(float(r["qty"]) for r in be_rows)
            out.append(be_rep.to_dict())

            i = j
            continue

        out.append(row.to_dict())
        i += 1

    out_df = pd.DataFrame(out) if out else _empty_trade_frame()
    if not out_df.empty:
        out_df["seq"] = range(1, len(out_df) + 1)
    return out_df.reset_index(drop=True)


def _compress_margin_call_sl_tail_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Collapse duplicated trailing SL rows inside a same-entry margin-call cluster.

    Some broker-emulator paths export:
      MARGIN CALL, MARGIN CALL, SL, SL
    for one entry, while TradingView exports:
      MARGIN CALL, MARGIN CALL, SL

    This helper only merges consecutive duplicate `SL` rows when they belong to
    a same-side / same-entry cluster that already contains at least one
    `MARGIN CALL`. It does not touch symmetric duplicate rows in non-margin
    clusters.
    """
    if df.empty:
        return df.copy()

    out: list[dict[str, Any]] = []
    i = 0
    while i < len(df):
        row = df.iloc[i]
        side = row["side"]
        entry_time = row["entry_time"]
        j = i
        cluster: list[pd.Series] = []
        while (
            j < len(df)
            and df.iloc[j]["side"] == side
            and df.iloc[j]["entry_time"] == entry_time
            and str(df.iloc[j]["reason"]) in {"MARGIN CALL", "SL"}
        ):
            cluster.append(df.iloc[j])
            j += 1

        reasons = {str(r["reason"]) for r in cluster}
        if len(cluster) >= 3 and reasons == {"MARGIN CALL", "SL"}:
            k = 0
            while k < len(cluster):
                cur = cluster[k]
                if str(cur["reason"]) == "SL":
                    qty_sum = float(cur["qty"])
                    m = k + 1
                    while (
                        m < len(cluster)
                        and str(cluster[m]["reason"]) == "SL"
                        and cluster[m]["exit_time"] == cur["exit_time"]
                    ):
                        qty_sum += float(cluster[m]["qty"])
                        m += 1
                    merged = cur.copy()
                    merged["qty"] = qty_sum
                    out.append(merged.to_dict())
                    k = m
                    continue
                out.append(cur.to_dict())
                k += 1
            i = j
            continue

        out.append(row.to_dict())
        i += 1

    out_df = pd.DataFrame(out) if out else _empty_trade_frame()
    if not out_df.empty:
        out_df["seq"] = range(1, len(out_df) + 1)
    return out_df.reset_index(drop=True)


def normalize_margin_call_be_clusters(tv: pd.DataFrame, py: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Normalize broker-emulator reporting for margin-call followed by BE remainder.

    TV can export a single `MARGIN CALL` trade plus a single `BE` trade for one
    entry, while Python may split the same economic event into multiple
    consecutive `MARGIN CALL` rows and multiple consecutive `BE` rows under the
    same entry timestamp. Collapse those same-entry clusters reason-wise.
    """
    tv = _compress_margin_call_be_clusters(tv)
    py = _compress_margin_call_be_clusters(py)
    tv = _compress_margin_call_sl_tail_duplicates(tv)
    py = _compress_margin_call_sl_tail_duplicates(py)
    return tv, py


def build_report(
    tv: pd.DataFrame,
    py: pd.DataFrame,
    *,
    price_tol: float = 0.5,
    qty_tol: float = 1e-9,
    strict_core: bool = False,
) -> pd.DataFrame:
    tv, py = normalize_broker_reporting(tv, py, qty_tol=max(float(qty_tol), 2e-6))
    n = min(len(tv), len(py))
    tv_n = tv.iloc[:n].copy()
    py_n = py.iloc[:n].copy()
    tv_n = tv_n.add_prefix("tv_")
    py_n = py_n.add_prefix("py_")
    m = pd.concat([tv_n, py_n], axis=1)

    m["side_match"] = m["tv_side"] == m["py_side"]
    m["reason_match"] = m["tv_reason"] == m["py_reason"]
    m["entry_time_diff_min"] = (m["py_entry_time"] - m["tv_entry_time"]).dt.total_seconds() / 60.0
    m["exit_time_diff_min"] = (m["py_exit_time"] - m["tv_exit_time"]).dt.total_seconds() / 60.0
    m["entry_price_diff"] = m["py_entry_price"] - m["tv_entry_price"]
    m["exit_price_diff"] = m["py_exit_price"] - m["tv_exit_price"]
    m["qty_diff"] = m["py_qty"] - m["tv_qty"]
    m["entry_price_match"] = m["entry_price_diff"].abs() <= float(price_tol)
    m["exit_price_match"] = m["exit_price_diff"].abs() <= float(price_tol)
    m["qty_match"] = m["qty_diff"].abs() <= float(qty_tol)
    m["all_price_qty_match"] = m["entry_price_match"] & m["exit_price_match"] & m["qty_match"]

    def _in_duplicate_pair(frame: pd.DataFrame, prefix: str) -> pd.Series:
        side = frame[f"{prefix}_side"]
        entry_time = frame[f"{prefix}_entry_time"]
        exit_time = frame[f"{prefix}_exit_time"]
        reason = frame[f"{prefix}_reason"]
        prev_same = (
            side.eq(side.shift(1))
            & entry_time.eq(entry_time.shift(1))
            & exit_time.eq(exit_time.shift(1))
            & reason.eq(reason.shift(1))
        )
        next_same = (
            side.eq(side.shift(-1))
            & entry_time.eq(entry_time.shift(-1))
            & exit_time.eq(exit_time.shift(-1))
            & reason.eq(reason.shift(-1))
        )
        return prev_same | next_same

    tv_dup_pair = _in_duplicate_pair(m, "tv")
    py_dup_pair = _in_duplicate_pair(m, "py")
    dup_be_near_match = (
        tv_dup_pair
        & py_dup_pair
        & (m["tv_reason"] == "BE")
        & (m["py_reason"] == "BE")
        & (m["tv_side"] == m["py_side"])
        & (m["tv_entry_time"] == m["py_entry_time"])
        & (m["exit_time_diff_min"].abs() <= 15.0 + 1e-9)
    )

    base_core = (
        m["side_match"]
        & m["reason_match"]
        & (m["entry_time_diff_min"].abs() < 1e-9)
        & ((m["exit_time_diff_min"].abs() < 1e-9) | dup_be_near_match)
    )
    m["all_core_match"] = base_core & m["all_price_qty_match"] if strict_core else base_core
    return m


def summarize_report(tv: pd.DataFrame, py: pd.DataFrame, report: pd.DataFrame | None = None) -> Dict[str, Any]:
    """
    Summarize parity status without hiding trailing extra trades.

    `build_report()` compares only the shared prefix length. This helper adds
    total-count awareness so callers can distinguish:
    - full strict parity
    - prefix-only parity with extra TV/Python trades
    - real core mismatches inside the shared prefix
    """
    raw_tv_total = int(len(tv))
    raw_py_total = int(len(py))
    tv_norm, py_norm = normalize_broker_reporting(tv, py, qty_tol=2e-6)
    rep = build_report(tv_norm, py_norm) if report is None else report
    compared = int(len(rep))
    tv_total = int(len(tv_norm))
    py_total = int(len(py_norm))
    core_match_count = int(rep["all_core_match"].sum()) if compared > 0 else 0
    entry_price_match_count = int(rep["entry_price_match"].sum()) if compared > 0 else 0
    exit_price_match_count = int(rep["exit_price_match"].sum()) if compared > 0 else 0
    qty_match_count = int(rep["qty_match"].sum()) if compared > 0 else 0
    all_price_qty_match_count = int(rep["all_price_qty_match"].sum()) if compared > 0 else 0
    extra_tv_trades = max(0, tv_total - compared)
    extra_py_trades = max(0, py_total - compared)
    count_match = tv_total == py_total
    prefix_core_match = core_match_count == compared
    strict_pass = count_match and prefix_core_match
    return {
        "tv_trades": tv_total,
        "py_trades": py_total,
        "raw_tv_trades": raw_tv_total,
        "raw_py_trades": raw_py_total,
        "compared": compared,
        "core_match_count": core_match_count,
        "entry_price_match_count": entry_price_match_count,
        "exit_price_match_count": exit_price_match_count,
        "qty_match_count": qty_match_count,
        "all_price_qty_match_count": all_price_qty_match_count,
        "extra_tv_trades": extra_tv_trades,
        "extra_py_trades": extra_py_trades,
        "trade_delta": py_total - tv_total,
        "count_match": count_match,
        "prefix_core_match": prefix_core_match,
        "strict_pass": strict_pass,
    }


def main() -> None:
    p = argparse.ArgumentParser(description="Compare TV trades and Python trades")
    p.add_argument("--tv", required=True, help="Path to tv_trades.csv")
    p.add_argument("--py", required=True, help="Path to debug_python_trades.csv")
    p.add_argument("--out", default="debug/parity_compare_report.csv", help="Output report CSV")
    p.add_argument("--clip-overlap", action="store_true", help="Compare only overlapping time interval")
    p.add_argument("--tv-tz", default="UTC", help="Timezone for tz-naive TV timestamps (default: UTC)")
    p.add_argument("--tv-shift-min", type=int, default=0, help="Shift TV timestamps by N minutes after tz normalization")
    p.add_argument("--py-shift-min", type=int, default=0, help="Shift Python timestamps by N minutes")
    args = p.parse_args()

    tv = load_tv_trades(Path(args.tv), tv_tz=args.tv_tz, tv_shift_min=args.tv_shift_min)
    py = load_py_trades(Path(args.py), py_shift_min=args.py_shift_min)

    if args.clip_overlap:
        tv, py = clip_overlap(tv, py)

    report = build_report(tv, py)
    summary = summarize_report(tv, py, report)
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    report.to_csv(out_path, index=False)

    print(f"TV trades: {summary['tv_trades']}")
    print(f"PY trades: {summary['py_trades']}")
    print(f"Compared: {summary['compared']}")
    print(f"Extra TV trades: {summary['extra_tv_trades']}")
    print(f"Extra PY trades: {summary['extra_py_trades']}")
    print(f"Report: {out_path}")

    if summary["compared"] == 0:
        if summary["strict_pass"]:
            print("No overlapping trades to compare.")
        else:
            print("No shared-prefix trades to compare, but trade counts differ.")
        return

    side_ok = int(report["side_match"].sum())
    reason_ok = int(report["reason_match"].sum())
    all_ok = summary["core_match_count"]
    print(f"Side match: {side_ok}/{summary['compared']}")
    print(f"Reason match: {reason_ok}/{summary['compared']}")
    print(f"Full core match: {all_ok}/{summary['compared']}")
    print(f"Strict parity: {'PASS' if summary['strict_pass'] else 'FAIL'}")

    bad = report[~report["all_core_match"]]
    if not bad.empty:
        first = bad.iloc[0]
        print("First mismatch:")
        print(
            f"  seq={int(first['tv_seq'])} "
            f"tv=({first['tv_side']}, {first['tv_entry_time']}, {first['tv_exit_time']}, {first['tv_reason']}) "
            f"py=({first['py_side']}, {first['py_entry_time']}, {first['py_exit_time']}, {first['py_reason']})"
        )


if __name__ == "__main__":
    main()
