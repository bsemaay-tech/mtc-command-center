#!/usr/bin/env python3
"""Bridge CLI for MTC-Engine Validation.

Runs a manual producer adapter through the existing MTCRunner using the
light-risk profile. This CLI orchestrates; it does not implement a new engine.
"""

from __future__ import annotations

import argparse
import csv
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
REPO_ROOT = PROJECT_ROOT.parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.config.profiles.light_risk import build_light_risk_config
from src.data.io import load_dataset, validate_dataset
from src.engine.mtc_runner import MTCRunner
from src.modules.signals.producers import create_producer
from src.workflow.artifacts import build_manifest, default_artifact_dir, write_manifest, write_results


def _json_file(path: str | None) -> dict[str, Any]:
    if not path:
        return {}
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"JSON file not found: {p}")
    return json.loads(p.read_text(encoding="utf-8"))


def _parse_iso(value: str | None) -> datetime | None:
    if not value:
        return None
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def _safe_pct(value: float | int | None) -> float:
    return float(value or 0.0)


def _buy_hold_return_pct(df: pd.DataFrame, eval_start: str | None, eval_end: str | None) -> float:
    scoped = df
    if eval_start or eval_end:
        ts = pd.to_datetime(scoped["timestamp"], utc=True)
        if eval_start:
            scoped = scoped.loc[ts >= pd.Timestamp(_parse_iso(eval_start))]
            ts = pd.to_datetime(scoped["timestamp"], utc=True)
        if eval_end:
            scoped = scoped.loc[ts <= pd.Timestamp(_parse_iso(eval_end))]
    if len(scoped) < 2:
        raise ValueError("Need at least two eval-window bars for buy-and-hold comparison")
    first = float(scoped["close"].iloc[0])
    last = float(scoped["close"].iloc[-1])
    if first <= 0:
        raise ValueError("First eval-window close must be positive for buy-and-hold comparison")
    return ((last / first) - 1.0) * 100.0


def _trade_rows(results: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for t in results.get("trades", []):
        direction = t.direction.value if hasattr(t.direction, "value") else str(t.direction)
        exit_reason = t.exit_reason.value if hasattr(t.exit_reason, "value") else str(t.exit_reason)
        rows.append(
            {
                "trade_id": t.trade_id,
                "direction": direction,
                "entry_time": t.entry_time,
                "exit_time": t.exit_time,
                "entry_price": t.entry_price,
                "exit_price": t.exit_price,
                "quantity": t.quantity,
                "pnl": t.pnl,
                "pnl_pct": t.pnl_pct,
                "pnl_r": t.pnl_r,
                "exit_reason": exit_reason,
                "bars_held": t.bars_held,
            }
        )
    return rows


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fieldnames = list(rows[0].keys()) if rows else ["trade_id"]
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def _run_parity_command(command: str | None, outdir: Path) -> dict[str, Any]:
    if not command:
        return {
            "status": "NOT_RUN",
            "reason": "No --parity-command supplied. Run producer-level Python vs Pine adapter parity separately.",
        }
    completed = subprocess.run(
        command,
        cwd=str(REPO_ROOT),
        shell=True,
        text=True,
        capture_output=True,
        timeout=900,
    )
    (outdir / "parity_stdout.txt").write_text(completed.stdout, encoding="utf-8")
    (outdir / "parity_stderr.txt").write_text(completed.stderr, encoding="utf-8")
    return {
        "status": "PASS" if completed.returncode == 0 else "FAIL",
        "returncode": completed.returncode,
        "command": command,
        "stdout": str(outdir / "parity_stdout.txt"),
        "stderr": str(outdir / "parity_stderr.txt"),
    }


def _resolve_parity(args: argparse.Namespace, producer: Any, df: pd.DataFrame, outdir: Path) -> dict[str, Any]:
    """Producer-level parity: compare Python vs Pine raw signals if a Pine export
    CSV is supplied; else run an external parity command; else NOT_RUN."""
    if args.pine_signals_csv:
        from src.workflow.signal_parity import compare_signals, load_pine_signals_csv

        py_long, py_short = producer.generate(df)
        pine_long, pine_short = load_pine_signals_csv(args.pine_signals_csv)
        full = compare_signals(
            py_long, py_short, pine_long, pine_short, min_match_rate=args.parity_min_match_rate
        )
        compare_path = outdir / "parity_compare.json"
        compare_path.write_text(json.dumps(full, indent=2), encoding="utf-8")
        return {
            "status": full["status"],
            "mode": "signal_compare",
            "bars": full["bars"],
            "long_match_rate": full["long_match_rate"],
            "short_match_rate": full["short_match_rate"],
            "min_match_rate": full["min_match_rate"],
            "pine_signals_csv": str(args.pine_signals_csv),
            "artifact": str(compare_path),
        }
    return _run_parity_command(args.parity_command, outdir)


def _config_snapshot(config: Any) -> dict[str, Any]:
    return {
        "profile": "light-risk",
        "filters_off": all(
            not bool(getattr(config.filters, name))
            for name in [
                "use_ma_filter",
                "ma_use_higher_timeframe",
                "use_ma_slope_filter",
                "use_volume_filter",
                "use_atr_vol_filter",
                "use_mcginley_filter",
                "use_mcginley_htf",
                "use_htf_trend_filter",
                "use_macd_filter",
                "macd_use_htf_bias",
                "use_range_filters",
                "use_range_regime_filter",
                "adx_use_higher_timeframe",
                "chop_use_higher_timeframe",
            ]
        ),
        "guards_off": all(
            not bool(getattr(config.guards, name))
            for name in [
                "use_dd_guard",
                "use_consec_loss_guard",
                "use_cooldown_guard",
                "use_eq_curve_guard",
                "use_mae_guard",
                "use_guard_recovery",
            ]
        )
        and not config.risk.use_daily_loss_limit
        and not config.risk.use_max_trades_per_day,
        "risk_on": {
            "stop_loss": bool(config.stop_loss.enabled),
            "take_profit": bool(config.take_profit.enabled),
            "break_even": bool(config.break_even.enabled),
            "multi_tp": bool(config.multi_tp.enabled),
            "trailing": bool(config.trailing.enabled),
            "risk_long_percent": config.risk.risk_long_percent,
            "risk_short_percent": config.risk.risk_short_percent,
            "max_leverage_cap": config.risk.max_leverage_cap,
            "fallback_qty_pct": config.risk.fallback_qty_pct,
        },
        "sl_tp_trailing": {
            "stop_loss": config.stop_loss.model_dump(by_alias=True),
            "take_profit": config.take_profit.model_dump(by_alias=True),
            "break_even": config.break_even.model_dump(by_alias=True),
            "multi_tp": config.multi_tp.model_dump(by_alias=True),
            "trailing": config.trailing.model_dump(by_alias=True),
        },
    }


def _render_report(payload: dict[str, Any], artifacts: dict[str, str]) -> str:
    m = payload["metrics"]
    cfg = payload["config_snapshot"]
    lines = [
        "# MTC-Engine Validation Report",
        "",
        "## Summary",
        f"- status: `{payload['status']}`",
        f"- producer: `{payload['producer']}`",
        f"- dataset: `{payload['dataset']}`",
        f"- symbol: `{payload.get('symbol', '')}`",
        f"- timeframe: `{payload.get('timeframe', '')}`",
        f"- date_range: `{payload.get('eval_start') or '-inf'} -> {payload.get('eval_end') or '+inf'}`",
        "- engine: `existing MTCRunner`",
        "- profile: `light-risk`",
        f"- filters_off: `{cfg['filters_off']}`",
        f"- guards_off: `{cfg['guards_off']}`",
        "- risk_on: `True`",
        f"- parity_status: `{payload['parity']['status']}`",
        "",
        "## Metrics",
        f"- strategy_return_pct: `{m['strategy_return_pct']:.4f}`",
        f"- buy_hold_return_pct: `{m['buy_hold_return_pct']:.4f}`",
        f"- excess_alpha_pct: `{m['excess_alpha_pct']:.4f}`",
        f"- max_drawdown_pct: `{m['max_drawdown_pct']:.4f}`",
        f"- profit_factor: `{m['profit_factor']}`",
        f"- total_trades: `{m['total_trades']}`",
        f"- win_rate_pct: `{m['win_rate_pct']:.4f}`",
        "",
        "## Risk Settings",
    ]
    for key, value in cfg["risk_on"].items():
        lines.append(f"- {key}: `{value}`")
    lines.extend(["", "## Artifact Index"])
    for key, value in artifacts.items():
        lines.append(f"- {key}: `{value}`")
    lines.append("")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run shortlisted producer raw signals through existing MTCRunner with the light-risk profile."
    )
    parser.add_argument("--producer", required=True, help="Manual producer adapter name, e.g. supertrend")
    parser.add_argument("--producer-params", help="JSON file with producer adapter params")
    parser.add_argument("--overrides", help="JSON file with light-risk config overrides")
    parser.add_argument("--data", required=True, help="OHLCV CSV/parquet path")
    parser.add_argument("--symbol", default="", help="Symbol label for reports")
    parser.add_argument("--timeframe", default="", help="Timeframe label for reports")
    parser.add_argument("--eval-start", help="Evaluation start ISO timestamp")
    parser.add_argument("--eval-end", help="Evaluation end ISO timestamp")
    parser.add_argument("--warmup", type=int, default=None, help="Warmup bars; omit for runner default")
    parser.add_argument("--output", help="Output directory; default uses results/mtc_engine_validation_runs")
    parser.add_argument("--run-id", help="Stable run id; default is timestamped")
    parser.add_argument("--parity-command", help="Optional producer-level Python vs Pine adapter parity command")
    parser.add_argument("--pine-signals-csv", help="PineTS export CSV with raw_long/raw_short columns; enables direct signal-compare parity")
    parser.add_argument("--parity-min-match-rate", type=float, default=1.0, help="Min long/short match rate for parity PASS (default 1.0 = exact)")
    parser.add_argument("--dry-run", action="store_true", help="Validate inputs/config without running MTCRunner")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    data_path = Path(args.data)
    if not data_path.exists():
        raise FileNotFoundError(f"Data file not found: {data_path}")

    producer_params = _json_file(args.producer_params)
    overrides = _json_file(args.overrides)
    producer = create_producer(args.producer, producer_params)
    config = build_light_risk_config(overrides)
    config_snapshot = _config_snapshot(config)
    if not config_snapshot["filters_off"] or not config_snapshot["guards_off"]:
        raise ValueError("light-risk profile invariant failed: filters/guards must be off")

    df = load_dataset(data_path)
    ok, messages = validate_dataset(df)
    if not ok:
        raise ValueError("Invalid dataset: " + "; ".join(messages))

    run_id = args.run_id or f"mtc_engine_validation_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%SZ')}"
    outdir = Path(args.output).resolve() if args.output else default_artifact_dir(PROJECT_ROOT, "mtc_engine_validation", args.producer)
    outdir.mkdir(parents=True, exist_ok=True)

    if args.dry_run:
        print(f"DRY_RUN_OK producer={producer.name} bars={len(df)} outdir={outdir}")
        return 0

    runner = MTCRunner(config)
    runner.signal_plugin = producer
    results = runner.run(
        df,
        warmup_bars=args.warmup,
        eval_start=_parse_iso(args.eval_start),
        eval_end=_parse_iso(args.eval_end),
    )

    metrics = results.get("metrics", {})
    strategy_return = _safe_pct(metrics.get("net_profit_pct"))
    buy_hold = _buy_hold_return_pct(df, args.eval_start, args.eval_end)
    enriched_metrics = {
        "strategy_return_pct": strategy_return,
        "buy_hold_return_pct": buy_hold,
        "excess_alpha_pct": strategy_return - buy_hold,
        "max_drawdown_pct": _safe_pct(metrics.get("max_drawdown_pct")),
        "profit_factor": metrics.get("profit_factor", 0.0),
        "total_trades": int(metrics.get("total_trades", 0)),
        "win_rate_pct": _safe_pct(metrics.get("win_rate")),
        "raw_metrics": metrics,
    }

    trades_path = outdir / "trades.csv"
    _write_csv(trades_path, _trade_rows(results))
    parity = _resolve_parity(args, producer, df, outdir)

    payload = {
        "run_id": run_id,
        "status": "COMPLETED",
        "producer": producer.name,
        "producer_params": producer_params,
        "dataset": str(data_path),
        "symbol": args.symbol,
        "timeframe": args.timeframe,
        "eval_start": args.eval_start,
        "eval_end": args.eval_end,
        "engine": "MTCRunner",
        "profile": "light-risk",
        "config_snapshot": config_snapshot,
        "metrics": enriched_metrics,
        "parity": parity,
    }

    results_path = write_results(outdir, payload)
    manifest = build_manifest(
        project_root=PROJECT_ROOT,
        run_type="mtc_engine_validation",
        run_id=run_id,
        dataset_file=data_path,
        symbol=args.symbol,
        timeframe=args.timeframe,
        start_date=args.eval_start,
        end_date=args.eval_end,
        config_obj=config,
        extra={"producer": producer.name, "parity_status": parity["status"]},
    )
    manifest_path = write_manifest(outdir, manifest)
    artifacts = {
        "report": str(outdir / "report.md"),
        "results_json": str(results_path),
        "manifest_json": str(manifest_path),
        "trades_csv": str(trades_path),
    }
    report_path = outdir / "report.md"
    report_path.write_text(_render_report(payload, artifacts), encoding="utf-8")

    print(f"MTC_ENGINE_VALIDATION_COMPLETED outdir={outdir}")
    print(f"strategy_return_pct={strategy_return:.4f} buy_hold_return_pct={buy_hold:.4f} excess_alpha_pct={strategy_return - buy_hold:.4f}")
    print(f"parity_status={parity['status']}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
