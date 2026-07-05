from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from datetime import timedelta
from pathlib import Path
from typing import Any

import pandas as pd

from manual_tw_futures_audit import (
    PARITY_ROOT,
    REPORTS_DIR,
    Trade,
    build_case_overrides,
    latest_xlsx,
    load_trades,
    parse_chart_timezone,
    read_tv_workbook,
    run_case_parity,
    write_case_override,
)


REPO_ROOT = Path(__file__).resolve().parents[2]
LOCAL_TF = pd.Timedelta(hours=1)
DEFAULT_CASES = ["case_001", "case_010", "case_020", "case_021"]
WINDOW_COLUMNS = [
    "timestamp",
    "open",
    "high",
    "low",
    "close",
    "long_signal",
    "short_signal",
    "long_gated",
    "short_gated",
    "exit_signal",
    "position_side",
    "entry_price",
    "exit_price",
    "active_stop_price",
    "trail_price",
    "be_active",
    "tp1_hit",
    "tp2_hit",
]


def load_signal_frame() -> pd.DataFrame:
    raw = json.loads((REPO_ROOT / "data" / "mtc_signals.json").read_text(encoding="utf-8"))
    df = pd.DataFrame(raw["signals"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms", utc=True)
    return df


def compare_sequential(ref: list[Trade], other: list[Trade]) -> tuple[int | None, Trade | None, Trade | None]:
    compared = min(len(ref), len(other))
    for idx in range(compared):
        a = ref[idx]
        b = other[idx]
        if not (
            a.side == b.side
            and a.entry_time == b.entry_time
            and a.exit_time == b.exit_time
            and a.reason == b.reason
            and abs(a.entry_price - b.entry_price) <= 0.05
            and abs(a.exit_price - b.exit_price) <= 0.05
            and abs(a.qty - b.qty) <= 0.001
        ):
            return idx, a, b
    return None, None, None


def trade_to_dict(trade: Trade | None) -> dict[str, Any] | None:
    if trade is None:
        return None
    out = asdict(trade)
    out["entry_time"] = trade.entry_time.isoformat()
    out["exit_time"] = trade.exit_time.isoformat()
    return out


def find_bar_row(df: pd.DataFrame, ts: pd.Timestamp) -> dict[str, Any] | None:
    hit = df.loc[df["timestamp"] == ts]
    if hit.empty:
        return None
    row = hit.iloc[0]
    out: dict[str, Any] = {}
    for col in WINDOW_COLUMNS:
        if col not in row.index:
            continue
        value = row[col]
        if isinstance(value, pd.Timestamp):
            out[col] = value.isoformat()
        elif pd.isna(value):
            out[col] = None
        else:
            out[col] = value.item() if hasattr(value, "item") else value
    return out


def build_window(df: pd.DataFrame, center: pd.Timestamp, bars_before: int = 3, bars_after: int = 3) -> list[dict[str, Any]]:
    start = center - (LOCAL_TF * bars_before)
    end = center + (LOCAL_TF * bars_after)
    window = df.loc[(df["timestamp"] >= start) & (df["timestamp"] <= end), WINDOW_COLUMNS].copy()
    if window.empty:
        return []
    window["timestamp"] = window["timestamp"].map(lambda value: value.isoformat())
    records = window.to_dict(orient="records")
    cleaned: list[dict[str, Any]] = []
    for record in records:
        row: dict[str, Any] = {}
        for key, value in record.items():
            row[key] = None if pd.isna(value) else value
        cleaned.append(row)
    return cleaned


def classify_divergence(case_name: str, tw_trade: Trade, local_trade: Trade) -> str:
    if tw_trade.reason == "MARGIN_CALL":
        return "margin_call_semantics"
    if tw_trade.reason == "OPP_SIGNAL" and local_trade.reason == "OPP_SIGNAL":
        entry_diff = int((local_trade.entry_time - tw_trade.entry_time).total_seconds() / 60.0)
        exit_diff = int((local_trade.exit_time - tw_trade.exit_time).total_seconds() / 60.0)
        if abs(entry_diff) == 60 or abs(exit_diff) == 60:
            return "reversal_bar_alignment"
    if tw_trade.reason == "SL" and local_trade.reason == "BE_HIT":
        return "break_even_vs_stop_semantics"
    if local_trade.reason == "TRAIL_HIT":
        return "trailing_vs_reversal_label_semantics"
    return f"unclassified::{case_name}"


def build_findings(case_name: str, tw_trade: Trade, local_trade: Trade, local_prev_trade: Trade | None) -> list[str]:
    findings: list[str] = []
    if case_name == "case_001":
        findings.append(
            "TW reversal sequence drifts by one bar after the preceding SL; local engine flips on the 2025-01-13 07:00 UTC close, TW records the new short at 08:00 UTC."
        )
        findings.append(
            "Exit also drifts by one bar in the opposite direction: TW closes at 20:00 UTC, local closes at 21:00 UTC, both tagged as opposite-signal."
        )
    elif case_name == "case_010":
        findings.append(
            "TW splits the opening short into multiple child trades and force-closes two of them one hour later with Margin call."
        )
        findings.append(
            "Local engine keeps one aggregated short open until 2025-01-10 17:00 UTC and has no margin-call event in the lifecycle."
        )
    elif case_name == "case_020":
        findings.append(
            "TW classifies the first divergent short as SL at 2025-01-13 15:00 UTC, while local keeps the position alive and exits later via break-even on 20:00 UTC."
        )
        findings.append(
            "This is not only a timestamp drift; the exit owner differs: stop-loss vs break-even protection."
        )
    elif case_name == "case_021":
        findings.append(
            "TW holds the opening short until the opposite long signal on 2025-01-10 17:00 UTC and labels the exit with the opposite entry tag."
        )
        findings.append(
            "Local engine exits much earlier on 2025-01-08 11:00 UTC via trailing-stop, so the divergence is protective-exit semantics, not entry timing."
        )
    if local_prev_trade is not None:
        findings.append(
            f"Previous local trade exited at {local_prev_trade.exit_time.isoformat()} with reason `{local_prev_trade.reason}`."
        )
    findings.append(
        f"Local execution profile is decision-bar-close: signal bar, fill bar, and exit-trigger bar are the same local bar unless a future owner changes this policy."
    )
    return findings


def fix_candidates(classification: str) -> list[str]:
    if classification == "reversal_bar_alignment":
        return [
            "Audit TradingView reversal fills against current decision-bar-close policy.",
            "Check whether PineTS reconstruction should defer reversal entry to next bar for TW-equivalent mode.",
            "Check whether opposite-signal close and opposite entry should be split into separate lifecycle events.",
        ]
    if classification == "margin_call_semantics":
        return [
            "Define whether TW-style forced liquidation should be emulated in Python runner.",
            "Check whether Pine trade reconstruction must split one lifecycle into child margin-call subtrades.",
            "Audit leverage/margin settings against TradingView tester formulas before changing runner behavior.",
        ]
    if classification == "break_even_vs_stop_semantics":
        return [
            "Compare BE activation timing and stop-owner precedence against TradingView strategy tester behavior.",
            "Audit intrabar path assumptions for the bar where TW reports SL and local reports BE_HIT.",
        ]
    if classification == "trailing_vs_reversal_label_semantics":
        return [
            "Compare trailing-stop activation/update timing against TradingView tester behavior.",
            "Check whether TW export labels reversal-close differently even when a protective order closes first.",
        ]
    return ["Unclassified divergence: inspect semantic owner before patching."]


def audit_case(case_name: str, baseline_info: dict[str, Any], chart_tz_label: str) -> dict[str, Any]:
    chart_tz = parse_chart_timezone(chart_tz_label)
    case_dir = PARITY_ROOT / case_name
    xlsx_path = latest_xlsx(case_dir)
    xlsx_info = read_tv_workbook(xlsx_path, chart_tz)
    overrides = build_case_overrides(case_name, xlsx_info, baseline_info)
    override_json = write_case_override(case_name, overrides, f"manual_tw_lifecycle_{case_name}")
    artifacts = run_case_parity(case_name, xlsx_info, override_json)

    signal_df = load_signal_frame()
    tw_trades = xlsx_info["trades"]
    pine_trades = load_trades(artifacts["pine_trades_csv"])
    python_trades = load_trades(artifacts["python_trades_csv"])

    mismatch_idx, tw_trade, local_trade = compare_sequential(tw_trades, pine_trades)
    if mismatch_idx is None or tw_trade is None or local_trade is None:
        raise RuntimeError(f"No mismatch found for {case_name}; lifecycle audit expects a TW divergence.")

    local_prev_trade = pine_trades[mismatch_idx - 1] if mismatch_idx > 0 else None
    local_next_trade = pine_trades[mismatch_idx + 1] if mismatch_idx + 1 < len(pine_trades) else None

    entry_signal_bar = find_bar_row(signal_df, local_trade.entry_time)
    entry_prev_bar = find_bar_row(signal_df, local_trade.entry_time - LOCAL_TF)
    exit_trigger_bar = find_bar_row(signal_df, local_trade.exit_time)
    exit_prev_bar = find_bar_row(signal_df, local_trade.exit_time - LOCAL_TF)

    return {
        "case": case_name,
        "xlsx": str(xlsx_path.relative_to(REPO_ROOT)),
        "chart_timezone": chart_tz_label,
        "applied_overrides": overrides,
        "counts": {
            "tw_trades": len(tw_trades),
            "pine_trades": len(pine_trades),
            "python_trades": len(python_trades),
        },
        "classification": classify_divergence(case_name, tw_trade, local_trade),
        "local_execution_model": {
            "fill_policy": "decision_bar_close",
            "signal_bar_equals_fill_bar": True,
            "exit_trigger_bar_equals_exit_fill_bar": True,
            "note": "This reflects current PineTS reconstruction and Python runner semantics.",
        },
        "mismatch_sequence_index_1based": mismatch_idx + 1,
        "tw_trade": trade_to_dict(tw_trade),
        "local_trade": trade_to_dict(local_trade),
        "local_prev_trade": trade_to_dict(local_prev_trade),
        "local_next_trade": trade_to_dict(local_next_trade),
        "time_deltas": {
            "entry_diff_minutes_local_minus_tw": (local_trade.entry_time - tw_trade.entry_time).total_seconds() / 60.0,
            "exit_diff_minutes_local_minus_tw": (local_trade.exit_time - tw_trade.exit_time).total_seconds() / 60.0,
        },
        "price_deltas": {
            "entry_price_local_minus_tw": local_trade.entry_price - tw_trade.entry_price,
            "exit_price_local_minus_tw": local_trade.exit_price - tw_trade.exit_price,
        },
        "lifecycle_bars": {
            "entry_signal_bar": entry_signal_bar,
            "entry_prev_bar": entry_prev_bar,
            "exit_trigger_bar": exit_trigger_bar,
            "exit_prev_bar": exit_prev_bar,
            "entry_window": build_window(signal_df, local_trade.entry_time),
            "exit_window": build_window(signal_df, local_trade.exit_time),
        },
        "findings": build_findings(case_name, tw_trade, local_trade, local_prev_trade),
        "fix_candidates": fix_candidates(classify_divergence(case_name, tw_trade, local_trade)),
    }


def render_markdown(results: list[dict[str, Any]]) -> str:
    lines = ["# Manual TW Lifecycle Audit", ""]
    for result in results:
        lines.append(f"## {result['case']}")
        lines.append(f"- classification: `{result['classification']}`")
        lines.append(
            f"- counts: TW `{result['counts']['tw_trades']}` / PineTS `{result['counts']['pine_trades']}` / Python `{result['counts']['python_trades']}`"
        )
        lines.append(
            f"- first mismatch seq: `{result['mismatch_sequence_index_1based']}` | entry delta `{result['time_deltas']['entry_diff_minutes_local_minus_tw']}` min | exit delta `{result['time_deltas']['exit_diff_minutes_local_minus_tw']}` min"
        )
        lines.append(
            f"- TW trade: `{result['tw_trade']['side']}` {result['tw_trade']['entry_time']} -> {result['tw_trade']['exit_time']} `{result['tw_trade']['reason']}`"
        )
        lines.append(
            f"- Local trade: `{result['local_trade']['side']}` {result['local_trade']['entry_time']} -> {result['local_trade']['exit_time']} `{result['local_trade']['reason']}`"
        )
        for finding in result["findings"]:
            lines.append(f"- {finding}")
        for candidate in result["fix_candidates"]:
            lines.append(f"- next fix candidate: {candidate}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Lifecycle audit for selected TW manual export cases.")
    parser.add_argument("--cases", nargs="+", default=DEFAULT_CASES)
    parser.add_argument("--chart-timezone", default="UTC+3")
    parser.add_argument("--report-prefix", default="manual_tw_lifecycle_audit_2026-03-31")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    chart_tz = parse_chart_timezone(args.chart_timezone)
    baseline_xlsx = latest_xlsx(PARITY_ROOT / "case_001")
    baseline_info = read_tv_workbook(baseline_xlsx, chart_tz)

    results = [audit_case(case_name, baseline_info, args.chart_timezone) for case_name in args.cases]

    json_path = REPORTS_DIR / f"{args.report_prefix}.json"
    md_path = REPORTS_DIR / f"{args.report_prefix}.md"
    json_path.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
    md_path.write_text(render_markdown(results), encoding="utf-8")

    print(json.dumps({"json": str(json_path), "markdown": str(md_path)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
