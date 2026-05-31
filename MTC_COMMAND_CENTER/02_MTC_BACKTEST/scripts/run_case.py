#!/usr/bin/env python
"""
CLI runner for MTC Backtest cases.

Usage:
  python scripts/run_case.py configs/cases/dec2025_parity.json

Reads a JSON case file, runs the backtest, prints summary, and emits
standard artifacts (manifest.json, results.json, report.md) by default.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, time, timezone, timedelta
from pathlib import Path
from collections import defaultdict
from typing import Any

import pandas as pd

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.config.defaults import MTCConfig
from src.engine.mtc_runner import MTCRunner
from src.workflow.artifacts import (
    build_manifest,
    default_artifact_dir,
    render_simple_report,
    write_manifest,
    write_report,
    write_results,
)


def load_case(case_path: str) -> tuple[dict, Path]:
    p = Path(case_path)
    if not p.exists():
        p = PROJECT_ROOT / case_path
    if not p.exists():
        print(f"ERROR: Case file not found: {case_path}")
        sys.exit(1)
    with p.open(encoding="utf-8") as f:
        return json.load(f), p.resolve()


def _resolve_dataset_path(dataset_ref: str) -> Path:
    ref = str(dataset_ref).strip()
    p = Path(ref)

    # 1) absolute path
    if p.is_absolute() and p.exists():
        return p.resolve()

    # 2) relative to project root
    candidate_rel = (PROJECT_ROOT / p).resolve()
    if candidate_rel.exists():
        return candidate_rel

    # 3) legacy relative to mtc_backtest/data
    candidate_data = (PROJECT_ROOT / "data" / ref).resolve()
    if candidate_data.exists():
        return candidate_data

    # 4) symbol:timeframe lookup in backtest_assets/data_catalog.json
    if ":" in ref and p.suffix == "":
        symbol, tf = [s.strip() for s in ref.split(":", 1)]
        catalog = PROJECT_ROOT / "backtest_assets" / "data_catalog.json"
        if catalog.exists():
            try:
                payload = json.loads(catalog.read_text(encoding="utf-8"))
                entry = payload.get(symbol, {}).get(tf, {})
                abs_path = str(entry.get("abs_path", "")).strip()
                rel_path = str(entry.get("path", "")).strip()
                if abs_path:
                    pp = Path(abs_path)
                    if pp.exists():
                        return pp.resolve()
                if rel_path:
                    for pp in (
                        (PROJECT_ROOT.parent / rel_path).resolve(),
                        (PROJECT_ROOT.parent / "110_" / rel_path).resolve(),
                    ):
                        if pp.exists():
                            return pp
            except Exception:
                pass

    raise FileNotFoundError(f"Dataset not found from reference: {dataset_ref}")


def load_dataset(dataset_ref: str) -> tuple[pd.DataFrame, Path]:
    filepath = _resolve_dataset_path(dataset_ref)
    if not filepath.exists():
        print(f"ERROR: Dataset not found: {filepath}")
        sys.exit(1)

    if filepath.suffix == ".parquet":
        df = pd.read_parquet(filepath)
    elif filepath.suffix == ".csv":
        df = pd.read_csv(filepath)
    else:
        print(f"ERROR: Unsupported format: {filepath.suffix}")
        sys.exit(1)

    # Normalize timestamp axis across both legacy flat files and standardized
    # parquet datasets where time is stored as DatetimeIndex.
    if "timestamp" not in df.columns:
        if isinstance(df.index, pd.DatetimeIndex):
            df = df.reset_index()
            if "timestamp" not in df.columns:
                # reset_index may name the column "index" depending on source.
                first_col = str(df.columns[0])
                df = df.rename(columns={first_col: "timestamp"})
        elif "index" in df.columns:
            df = df.rename(columns={"index": "timestamp"})

    if "timestamp" not in df.columns:
        raise ValueError(
            f"Dataset has no timestamp axis: {filepath}. "
            "Expected 'timestamp' column or DatetimeIndex."
        )

    if pd.api.types.is_numeric_dtype(df["timestamp"]):
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms", utc=True)
    else:
        df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")

    if df["timestamp"].isna().any():
        bad = int(df["timestamp"].isna().sum())
        raise ValueError(f"Failed to parse {bad} timestamp rows in dataset: {filepath}")

    if df["timestamp"].dt.tz is None:
        df["timestamp"] = df["timestamp"].dt.tz_localize("UTC")
    else:
        df["timestamp"] = df["timestamp"].dt.tz_convert("UTC")

    return df, filepath


def build_config(case: dict) -> MTCConfig:
    cfg_dict = case.get("config", {})
    return MTCConfig.model_validate(cfg_dict)


def _parse_case_datetime(raw: str) -> datetime:
    try:
        dt = datetime.fromisoformat(raw)
    except ValueError:
        dt = datetime.strptime(raw, "%Y-%m-%d")

    if dt.hour == 0 and dt.minute == 0 and dt.second == 0 and "T" not in raw:
        dt = datetime.combine(dt.date(), time.min)

    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


def filter_data(df: pd.DataFrame, case: dict) -> tuple[pd.DataFrame, datetime, datetime]:
    start_dt = _parse_case_datetime(case["start_date"])
    end_dt = _parse_case_datetime(case["end_date"])
    preroll_days = int(case.get("preroll_days", 90))

    filter_start = start_dt - timedelta(days=preroll_days) if preroll_days > 0 else start_dt
    mask = (df["timestamp"] >= filter_start) & (df["timestamp"] <= end_dt)
    return df.loc[mask].copy().reset_index(drop=True), start_dt, end_dt


def _exit_reason_counts(results: dict) -> dict[str, int]:
    counts: dict[str, int] = {}
    for t in results.get("trades", []):
        reason = t.exit_reason.value if hasattr(t.exit_reason, "value") else str(t.exit_reason)
        counts[reason] = counts.get(reason, 0) + 1
    return counts


def _compute_regime_trade_breakdown(trades: list[Any], calendar_path: Path) -> dict[str, dict[str, float]]:
    """
    Compute per-regime trade distribution by mapping trade entry_time to regime windows.
    Returns empty dict if calendar is missing/unreadable.
    """
    if not calendar_path.exists():
        return {}

    try:
        payload = json.loads(calendar_path.read_text(encoding="utf-8"))
        windows_raw = payload.get("windows", [])
        windows: list[tuple[pd.Timestamp, pd.Timestamp, str]] = []
        for w in windows_raw:
            s = pd.Timestamp(w["start"])
            e = pd.Timestamp(w["end"])
            if s.tzinfo is None:
                s = s.tz_localize("UTC")
                e = e.tz_localize("UTC")
            else:
                s = s.tz_convert("UTC")
                e = e.tz_convert("UTC")
            windows.append((s, e, str(w.get("label", "UNLABELED"))))
    except Exception:
        return {}

    agg: dict[str, dict[str, float]] = defaultdict(lambda: {"trades": 0.0, "wins": 0.0, "net_profit": 0.0})
    for t in trades:
        et = getattr(t, "entry_time", None)
        pnl = float(getattr(t, "pnl", 0.0))
        label = "UNLABELED"
        if et is not None:
            et_ts = pd.Timestamp(et)
            if et_ts.tzinfo is None:
                et_ts = et_ts.tz_localize("UTC")
            else:
                et_ts = et_ts.tz_convert("UTC")
            for s, e, w_label in windows:
                if s <= et_ts <= e:
                    label = w_label
                    break

        agg[label]["trades"] += 1.0
        agg[label]["wins"] += 1.0 if pnl > 0 else 0.0
        agg[label]["net_profit"] += pnl

    out: dict[str, dict[str, float]] = {}
    for label in sorted(agg.keys()):
        trades_n = int(agg[label]["trades"])
        wins_n = int(agg[label]["wins"])
        net = float(agg[label]["net_profit"])
        out[label] = {
            "trades": trades_n,
            "win_rate": round((100.0 * wins_n / trades_n) if trades_n > 0 else 0.0, 4),
            "net_profit": round(net, 6),
        }
    return out


# ---------------------------------------------------------------------------
# Regime filter (additive — does NOT touch the engine)
# ---------------------------------------------------------------------------
_REGIME_LABEL_MAP = {
    "bull": "TREND_BULL",
    "bear": "TREND_BEAR",
    "range": "RANGE",
    "chop": "CHOPPY",
}


def _apply_regime_filter(
    df: pd.DataFrame,
    regime: str,
    calendar_path: Path | None = None,
) -> tuple[pd.DataFrame, str | None]:
    """
    Pre-filter *df* to rows belonging to the requested regime.

    Returns (filtered_df, regime_label | None).
    If regime == 'all' or no calendar exists, returns original df unchanged.
    """
    if regime == "all":
        return df, None

    import json as _json

    if calendar_path is None:
        calendar_path = PROJECT_ROOT / "backtest_assets" / "regime_calendar_4h.json"

    if not calendar_path.exists():
        print(
            f"[regime] WARN: --regime '{regime}' requested but regime_calendar_4h.json "
            f"not found at {calendar_path}. Running full history."
        )
        return df, None

    target_label = _REGIME_LABEL_MAP.get(regime)
    if target_label is None:
        print(f"[regime] WARN: unknown regime '{regime}'. Running full history.")
        return df, None

    cal = _json.loads(calendar_path.read_text(encoding="utf-8"))
    windows = [w for w in cal.get("windows", []) if w["label"] == target_label]

    # Build boolean mask on df's index (or timestamp column)
    if isinstance(df.index, pd.DatetimeIndex):
        idx = df.index
    elif "timestamp" in df.columns:
        idx = pd.DatetimeIndex(df["timestamp"])
    else:
        print("[regime] WARN: cannot locate timestamp axis. Running full history.")
        return df, None

    mask = pd.Series(False, index=df.index)
    for w in windows:
        s = pd.Timestamp(w["start"])
        e = pd.Timestamp(w["end"])
        if s.tzinfo is None:
            s = s.tz_localize("UTC")
            e = e.tz_localize("UTC")
        if idx.tz is None:
            s = s.tz_localize(None)
            e = e.tz_localize(None)
        mask |= (idx >= s) & (idx <= e)

    filtered = df[mask.values].copy()
    print(
        f"[regime] Filter: {regime.upper()} ({target_label}) "
        f"→ {len(filtered):,} / {len(df):,} bars retained "
        f"({100 * len(filtered) / max(len(df), 1):.1f}%)"
    )
    return filtered, target_label


def run(
    case_path: str,
    *,
    emit_artifacts: bool = True,
    artifacts_dir: str | None = None,
    run_id: str | None = None,
    regime: str = "all",
) -> dict:
    case, case_file = load_case(case_path)
    config = build_config(case)

    print("=" * 60)
    print(f"CASE: {case_file.stem}")
    print("=" * 60)
    print(f"  Dataset : {case['dataset']}")
    print(f"  Range   : {case['start_date']} .. {case['end_date']}")
    print(f"  Preroll : {case.get('preroll_days', 90)} days")
    print(f"  Parity  : {config.parity.enabled} / {config.parity.fill_contract}")
    print(f"  Debug   : {config.parity.export_debug_csv}")
    print()

    df, dataset_file = load_dataset(case["dataset"])
    df_filtered, start_dt, end_dt = filter_data(df, case)
    warmup_bars = int(case.get("warmup_bars", 200))

    print(f"  Total bars  : {len(df)}")
    print(f"  Filtered    : {len(df_filtered)} (incl. preroll)")
    if regime != "all":
        print(f"  Regime      : {regime}")
    print()

    # Apply optional regime filter (additive — engine is NOT touched)
    df_filtered, _regime_label = _apply_regime_filter(df_filtered, regime)

    runner = MTCRunner(config)
    results = runner.run(
        df_filtered,
        warmup_bars=warmup_bars,
        eval_start=start_dt if int(case.get("preroll_days", 90)) > 0 else None,
        eval_end=end_dt,
    )

    m = results["metrics"]
    print("\n" + "=" * 60)
    print("RESULTS")
    print("=" * 60)
    print(f"  Net Profit    : ${m['net_profit']:>10.2f}")
    print(f"  Total Trades  : {m['total_trades']:>10d}")
    print(f"  Total Entries : {m.get('total_entries', 0):>10d}")
    print(f"  Win Rate      : {m['win_rate']:>10.1f}%")
    print(f"  Profit Factor : {m['profit_factor']:>10.2f}")
    print(f"  Max Drawdown  : {m['max_drawdown']:>10.1f}%")
    print(f"  Avg Trade     : ${m['avg_trade']:>10.2f}")
    print(f"  Largest Win   : ${m['largest_win']:>10.2f}")

    if "debug_exports" in results:
        print("\n  Debug CSVs:")
        for k, v in results["debug_exports"].items():
            print(f"    {k}: {v}")

    reason_counts = _exit_reason_counts(results)
    regime_calendar_path = PROJECT_ROOT / "backtest_assets" / "regime_calendar_4h.json"
    regime_breakdown = _compute_regime_trade_breakdown(results.get("trades", []), regime_calendar_path)

    if reason_counts:
        print("\n  Exit Reasons:")
        for reason, count in sorted(reason_counts.items(), key=lambda x: -x[1]):
            print(f"    {reason:>12s}: {count}")
    if regime_breakdown:
        print("\n  Regime Breakdown (entry-time mapped):")
        for lbl, vals in regime_breakdown.items():
            print(
                f"    {lbl:>12s}: trades={int(vals['trades'])} "
                f"win_rate={vals['win_rate']:.2f}% net={vals['net_profit']:.2f}"
            )

    if emit_artifacts:
        resolved_run_id = run_id or f"backtest_{case_file.stem}_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%SZ')}"
        outdir = Path(artifacts_dir).resolve() if artifacts_dir else default_artifact_dir(PROJECT_ROOT, "backtest", case_file.stem)

        manifest = build_manifest(
            project_root=PROJECT_ROOT,
            run_type="backtest",
            run_id=resolved_run_id,
            case_file=case_file,
            dataset_file=dataset_file,
            start_date=str(case.get("start_date", "")),
            end_date=str(case.get("end_date", "")),
            config_obj=config,
            extra={
                "preroll_days": int(case.get("preroll_days", 90)),
                "warmup_bars": warmup_bars,
                "parity_enabled": bool(config.parity.enabled),
                "fill_contract": str(config.parity.fill_contract),
                "strategy_id": str(case.get("strategy_id", case_file.stem)),
                "module_id": str(config.signal_mode),
                "feature_flags": dict(case.get("feature_flags", {})),
                "regime_calendar_used": str(regime_calendar_path) if regime_breakdown else "",
            },
        )

        payload = {
            "run_id": resolved_run_id,
            "run_type": "backtest",
            "status": "PASS",
            "strategy_id": str(case.get("strategy_id", case_file.stem)),
            "module_id": str(config.signal_mode),
            "feature_flags": dict(case.get("feature_flags", {})),
            "metrics": results.get("metrics", {}),
            "exit_reason_breakdown": reason_counts,
            "regime_breakdown": regime_breakdown,
            "debug_exports": results.get("debug_exports", {}),
            "artifacts": {},
        }

        manifest_path = write_manifest(outdir, manifest)
        results_path = write_results(outdir, payload)
        report_md = render_simple_report(
            title="MTC Backtest Report",
            run_id=resolved_run_id,
            status="PASS",
            key_values={
                "case_file": case_file,
                "dataset_file": dataset_file,
                "start_date": case.get("start_date", ""),
                "end_date": case.get("end_date", ""),
                "net_profit": m.get("net_profit", ""),
                "max_dd_pct": m.get("max_drawdown", ""),
                "total_trades": m.get("total_trades", ""),
                "win_rate": m.get("win_rate", ""),
                "profit_factor": m.get("profit_factor", ""),
                "regime_groups": len(regime_breakdown),
            },
            artifact_paths={
                "manifest": str(manifest_path),
                "results": str(results_path),
            },
        )
        if regime_breakdown:
            report_md += "## Regime Breakdown\n"
            for lbl, vals in regime_breakdown.items():
                report_md += (
                    f"- `{lbl}`: trades={int(vals['trades'])}, "
                    f"win_rate={vals['win_rate']:.2f}%, "
                    f"net_profit={vals['net_profit']:.6f}\n"
                )
            report_md += "\n"

        report_path = write_report(outdir, report_md)

        payload["artifacts"] = {
            "manifest": str(manifest_path),
            "results": str(results_path),
            "report": str(report_path),
        }
        write_results(outdir, payload)
        print(f"\nArtifacts: {outdir}")

    print("\n" + "=" * 60 + "\n")
    return results


def main() -> int:
    ap = argparse.ArgumentParser(description="Run a single MTC backtest case.")
    ap.add_argument("case", help="Case JSON path")
    ap.add_argument("--no-artifacts", action="store_true", help="Disable manifest/results/report output")
    ap.add_argument("--artifacts-dir", default="", help="Custom output directory for run artifacts")
    ap.add_argument("--run-id", default="", help="Optional run-id override")
    ap.add_argument(
        "--regime",
        choices=["bull", "bear", "range", "chop", "all"],
        default="all",
        help=(
            "Filter backtest to a specific market regime (requires "
            "mtc_backtest/backtest_assets/regime_calendar_4h.json). "
            "Choices: bull | bear | range | chop | all (default: all)"
        ),
    )
    args = ap.parse_args()

    run(
        args.case,
        emit_artifacts=not args.no_artifacts,
        artifacts_dir=(args.artifacts_dir or None),
        run_id=(args.run_id or None),
        regime=args.regime,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
