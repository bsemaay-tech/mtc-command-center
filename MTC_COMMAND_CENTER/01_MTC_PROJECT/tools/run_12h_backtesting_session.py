from __future__ import annotations

import argparse
import csv
import hashlib
import itertools
import json
import os
import sys
import time
import traceback
from concurrent.futures import FIRST_COMPLETED, ProcessPoolExecutor, wait
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "00_PYTHON"))
sys.path.insert(0, str(ROOT))

from mtc_v2.core.config import DEFAULT_CONFIG, validate_config
from tools.build_per_asset_timeframe_seed_rankings import build_seed_rankings, write_csv as write_seed_csv
from tools.optimization_parameter_mapper import apply_parameter_mapping
from tools.optimization_resume_registry import EvaluationIdentity, ResumeRegistry, evaluation_key, metrics_hash
from tools.runner_metrics_adapter import RUNNER_METRICS_ADAPTER_VERSION, run_with_result
from tools.run_big_overnight_multiasset_optimization import (
    ALLOWED_SOURCE_TYPES,
    MAPPER_VERSION,
    bundle_root_from_manifest,
    create_walkforward,
    load_bars,
    load_manifest,
    load_regime_map,
    load_regime_registry,
    normalized_dataset_entry,
    regime_metrics_for_trades,
    sha256_file,
    utc_now,
    write_csv,
    write_json,
)


PROFILE_ID = "supertrend_producer_seed_extraction_12h_v1"
OPTIMIZER_VERSION = "mtc_v2_12h_smart_seed_session_v1"
RESEARCH_WARNING = "Research seed only; not Pine default; not production parameter."
PRIMARY_ASSETS = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT", "XRPUSDT", "ADAUSDT", "AVAXUSDT", "DOGEUSDT"]
EXPANSION_ASSETS = ["LINKUSDT", "DOTUSDT", "POLUSDT", "LTCUSDT", "TRXUSDT", "NEARUSDT", "APTUSDT", "ARBUSDT", "OPUSDT"]
TIMEFRAMES = ["15m", "1h", "2h", "4h", "1D"]
PRODUCER_RANGES = {
    "st_factor": [2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0],
    "global_atr_length": [7, 10, 14, 21, 28],
    "sl_atr_mult": [2.0, 2.5, 2.75, 3.0, 3.5],
    "tp_mode": ["None", "R"],
    "tp_r_multiple": [1.0, 1.5, 2.0, 2.5, 3.0],
    "risk_long": [0.25, 0.5, 0.75],
    "risk_short": [0.25, 0.5, 0.75, 1.0],
}


def canonical_params(raw: dict[str, Any]) -> dict[str, Any]:
    params = dict(raw)
    if params.get("tp_mode") == "None":
        params["tp_r_multiple"] = None
    return params


def parameter_hash(params: dict[str, Any]) -> str:
    return hashlib.sha256(json.dumps(params, sort_keys=True, default=str).encode("utf-8")).hexdigest()[:16]


def base_variant(overrides: dict[str, Any]) -> dict[str, Any]:
    params: dict[str, Any] = {
        "signal_mode": "Supertrend",
        "st_factor": 3.5,
        "global_atr_length": 14,
        "sl_atr_mult": 3.0,
        "tp_mode": "R",
        "tp_r_multiple": 2.0,
        "risk_long": 0.5,
        "risk_short": 0.5,
        "use_break_even": False,
        "use_trailing": False,
        "guards_disabled_for_phase1": True,
        "integrations_disabled": True,
        "visualization_disabled": True,
        "exit_on_filter_bundle": True,
    }
    params.update(overrides)
    return canonical_params(params)


def generate_smart_sample_variants(target_count: int) -> list[dict[str, Any]]:
    seen: dict[str, dict[str, Any]] = {}
    for key, values in PRODUCER_RANGES.items():
        for value in values:
            params = base_variant({key: value})
            seen[parameter_hash(params)] = params

    keys = list(PRODUCER_RANGES)
    for combo in itertools.product(*[PRODUCER_RANGES[key] for key in keys]):
        raw = dict(zip(keys, combo))
        params = base_variant(raw)
        seen.setdefault(parameter_hash(params), params)

    ordered = sorted(seen.values(), key=lambda row: parameter_hash(row))
    return ordered[:target_count]


def select_stage_datasets(manifest_path: Path, regime_path: Path, out_root: Path, max_assets: int) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    bundle = bundle_root_from_manifest(manifest_path)
    manifest = load_manifest(manifest_path)
    regimes = load_regime_registry(regime_path)
    desired_assets = (PRIMARY_ASSETS + EXPANSION_ASSETS)[:max_assets]
    usable: list[dict[str, Any]] = []
    skipped: list[dict[str, Any]] = []
    for raw in manifest:
        item = normalized_dataset_entry(raw, bundle)
        reason = ""
        if str(item.get("symbol")) not in desired_assets:
            reason = "symbol_not_selected"
        elif str(item.get("timeframe_normalized")) not in TIMEFRAMES:
            reason = "timeframe_not_selected"
        elif item.get("source_type") not in ALLOWED_SOURCE_TYPES:
            reason = f"source_type_not_allowed:{item.get('source_type')}"
        elif str(item.get("ohlcv_validation_status", "PASS")).upper() != "PASS":
            reason = f"ohlcv_not_pass:{item.get('ohlcv_validation_status')}"
        elif not Path(str(item["source_path"])).exists():
            reason = "normalized_file_missing"
        elif not item.get("sha256"):
            reason = "sha256_missing"
        elif item.get("dataset_id") not in regimes:
            reason = "regime_registry_missing"
        if reason:
            if reason != "symbol_not_selected":
                skipped.append({"dataset_id": item.get("dataset_id"), "symbol": item.get("symbol"), "timeframe": item.get("timeframe_normalized"), "reason": reason})
            continue
        usable.append(item)

    by_pair: dict[tuple[str, str], list[dict[str, Any]]] = {}
    for item in usable:
        by_pair.setdefault((str(item["symbol"]), str(item["timeframe_normalized"])), []).append(item)

    selected: list[dict[str, Any]] = []
    for symbol in desired_assets:
        available_timeframes = {tf for asset, tf in by_pair if asset == symbol}
        if len([tf for tf in TIMEFRAMES if tf in available_timeframes]) < 4:
            continue
        for timeframe in TIMEFRAMES:
            candidates = by_pair.get((symbol, timeframe), [])
            if not candidates:
                continue
            candidates.sort(key=lambda row: (row.get("source_type") != "binance_public_futures_klines", -int(row.get("row_count", 0))))
            selected.append(candidates[0])

    for item in selected:
        regime = regimes.get(str(item["dataset_id"]), {})
        regime_file = Path(str(regime.get("regime_file", "")))
        if regime_file and not regime_file.is_absolute():
            regime_file = bundle / regime_file
        item["regime_file_abs"] = str(regime_file)

    summary = {
        "selected_assets": sorted({str(item["symbol"]) for item in selected}, key=lambda sym: desired_assets.index(sym)),
        "selected_timeframes": TIMEFRAMES,
        "selected_dataset_count": len(selected),
        "skipped": skipped,
    }
    write_json(out_root / "datasets/dataset_selection.json", {"summary": summary, "datasets": selected})
    lines = [
        "# 12h Session Dataset Selection",
        "",
        RESEARCH_WARNING,
        "",
        f"- Selected assets: `{', '.join(summary['selected_assets'])}`",
        f"- Selected datasets: `{len(selected)}`",
        "",
        "| symbol | timeframe | dataset_id | rows | source_type | sha256 |",
        "|---|---|---|---:|---|---|",
    ]
    for item in selected:
        lines.append(f"| {item['symbol']} | {item['timeframe_normalized']} | {item['dataset_id']} | {item.get('row_count')} | {item.get('source_type')} | {item.get('sha256')} |")
    (out_root / "reports/DATASET_SELECTION_REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return selected, summary


def task_identity(params: dict[str, Any], split: dict[str, Any]) -> EvaluationIdentity:
    return EvaluationIdentity(
        profile_id=PROFILE_ID,
        dataset_id=str(split["dataset_id"]),
        dataset_hash=str(split["sha256"]),
        symbol=str(split["symbol"]),
        timeframe=str(split["timeframe_normalized"]),
        window_id=str(split["window_id"]),
        split_type=str(split["split_type"]),
        params=params,
        runner_version=RUNNER_METRICS_ADAPTER_VERSION,
        optimizer_version=OPTIMIZER_VERSION,
        parameter_mapper_version=MAPPER_VERSION,
    )


def iter_tasks(variants: list[dict[str, Any]], splits: list[dict[str, Any]], out_root: Path, worker_count: int) -> Iterable[dict[str, Any]]:
    ordinal = 0
    for variant_index, params in enumerate(variants):
        p_hash = parameter_hash(params)
        for split in splits:
            key = evaluation_key(task_identity(params, split))
            yield {
                "evaluation_key": key,
                "variant_index": variant_index,
                "parameter_hash": p_hash,
                "params": params,
                "split": split,
                "out_root": str(out_root),
                "worker_id": f"worker_{ordinal % worker_count:05d}",
                "run_id": PROFILE_ID,
            }
            ordinal += 1


def run_one(task: dict[str, Any]) -> dict[str, Any]:
    started = time.time()
    split = task["split"]
    params = dict(task["params"])
    worker_root = Path(task["out_root"]) / "workers" / task["worker_id"] / PROFILE_ID / str(split["dataset_id"]) / str(split["window_id"]) / str(split["split_type"]) / str(task["evaluation_key"])
    worker_root.mkdir(parents=True, exist_ok=True)
    try:
        actual_hash = sha256_file(Path(str(split["source_path"])))
        if actual_hash != str(split["sha256"]):
            raise RuntimeError(f"dataset_hash_mismatch expected={split['sha256']} actual={actual_hash}")
        bars = load_bars(Path(str(split["source_path"])), int(split["split_start"]), int(split["split_end"]))
        runner_params = dict(params)
        if runner_params.get("tp_mode") == "None" and runner_params.get("tp_r_multiple") is None:
            runner_params["tp_r_multiple"] = 1.0
        overrides = apply_parameter_mapping(runner_params)
        base = dict(DEFAULT_CONFIG)
        base.update(
            {
                "instrument_symbol": str(split["symbol"]),
                "instrument_price_tick": 0.1,
                "instrument_qty_step": 0.001,
                "instrument_min_qty": 0.001,
                "instrument_min_notional": 0.0,
                "initial_capital": 10000.0,
                "max_leverage_cap": 1.0,
                "margin_long_pct": 100.0,
                "margin_short_pct": 100.0,
            }
        )
        base.update(overrides)
        validate_config(base)
        result = run_with_result(bars, config_overrides=base, dataset_hash=actual_hash, dataset_id=str(split["dataset_id"]), run_id=PROFILE_ID)
        row = {
            **result.to_optimizer_row(),
            "profile": PROFILE_ID,
            "run_id": PROFILE_ID,
            "stage": "A_PRODUCER_ONLY_SEED_EXTRACTION",
            "evaluation_key": task["evaluation_key"],
            "parameter_hash": task["parameter_hash"],
            "variant_index": task["variant_index"],
            "params_json": json.dumps(params, sort_keys=True),
            "overrides_json": json.dumps(overrides, sort_keys=True),
            "dataset_id": split["dataset_id"],
            "symbol": split["symbol"],
            "asset": split["symbol"],
            "timeframe": split["timeframe_normalized"],
            "timeframe_normalized": split["timeframe_normalized"],
            "source_type": split.get("source_type", ""),
            "source_path": split["source_path"],
            "window_id": split["window_id"],
            "split_type": split["split_type"],
            "split_start": split["split_start"],
            "split_end": split["split_end"],
            "dataset_hash_valid": True,
            "failed_runner": False,
            "runtime_seconds": round(time.time() - started, 6),
            "research_warning": RESEARCH_WARNING,
        }
        regime_file = str(split.get("regime_file_abs", ""))
        row.update(regime_metrics_for_trades(result.trades, load_regime_map(regime_file)) if regime_file else {"regime_metrics_status": "REGIME_METRICS_UNAVAILABLE"})
        write_json(worker_root / "result.json", row)
        write_json(worker_root / "metrics.json", result.to_optimizer_row())
        write_json(worker_root / "params.json", params)
        (worker_root / "logs.txt").write_text(f"{utc_now()} completed\n", encoding="utf-8")
        return row
    except Exception as exc:
        row = {
            "profile": PROFILE_ID,
            "run_id": PROFILE_ID,
            "stage": "A_PRODUCER_ONLY_SEED_EXTRACTION",
            "evaluation_key": task.get("evaluation_key", ""),
            "parameter_hash": task.get("parameter_hash", ""),
            "variant_index": task.get("variant_index", -1),
            "params_json": json.dumps(task.get("params", {}), sort_keys=True),
            "dataset_id": split.get("dataset_id", ""),
            "symbol": split.get("symbol", ""),
            "asset": split.get("symbol", ""),
            "timeframe": split.get("timeframe_normalized", split.get("timeframe", "")),
            "timeframe_normalized": split.get("timeframe_normalized", ""),
            "source_type": split.get("source_type", ""),
            "source_path": split.get("source_path", ""),
            "window_id": split.get("window_id", ""),
            "split_type": split.get("split_type", ""),
            "split_start": split.get("split_start", ""),
            "split_end": split.get("split_end", ""),
            "dataset_hash_valid": "dataset_hash_mismatch" not in str(exc),
            "failed_runner": True,
            "error": str(exc),
            "traceback": traceback.format_exc(),
            "net_profit": 0.0,
            "net_profit_pct": 0.0,
            "profit_factor": 0.0,
            "max_drawdown_pct": 999.0,
            "win_rate": 0.0,
            "total_trades": 0,
            "runtime_seconds": round(time.time() - started, 6),
            "regime_metrics_status": "REGIME_METRICS_UNAVAILABLE",
            "research_warning": RESEARCH_WARNING,
        }
        write_json(worker_root / "result.json", row)
        write_json(worker_root / "metrics.json", row)
        write_json(worker_root / "params.json", task.get("params", {}))
        (worker_root / "logs.txt").write_text(f"{utc_now()} failed {exc}\n{traceback.format_exc()}\n", encoding="utf-8")
        return row


def append_heartbeat(out_root: Path, payload: dict[str, Any]) -> None:
    path = out_root / "heartbeat/heartbeat.log"
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps({"timestamp": utc_now(), **payload}, sort_keys=True, default=str) + "\n")


def checkpoint(out_root: Path, payload: dict[str, Any]) -> None:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    write_json(out_root / "checkpoints" / f"checkpoint_{stamp}.json", {**payload, "timestamp": utc_now()})


def write_progress_reports(out_root: Path, rows: list[dict[str, Any]], summary: dict[str, Any], *, source_run_id: str) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    registry = ResumeRegistry(out_root / "resume_registry.sqlite")
    unique, conflicts = registry.dedupe_results(rows)
    write_csv(out_root / "ranked/all_evaluations.csv", unique)
    write_csv(out_root / "results/all_evaluations.csv", unique)
    failed_rows = [row for row in unique if str(row.get("failed_runner", "False")).lower() == "true"]
    write_json(out_root / "failures/failed_evaluations.json", failed_rows)
    seed_candidates, per_group_summary = build_seed_rankings(
        unique,
        source_run_id=source_run_id,
        source_output_path=str(out_root / "ranked/all_evaluations.csv"),
        top_n=5,
    )
    write_seed_csv(out_root / "ranked/per_asset_timeframe_seed_candidates.csv", seed_candidates)
    write_seed_csv(out_root / "ranked/per_asset_timeframe_summary.csv", per_group_summary)
    write_seed_csv(out_root / "per_asset_timeframe/per_asset_timeframe_seed_candidates.csv", seed_candidates)
    write_seed_csv(out_root / "parameter_library_updates/supertrend_best_by_asset_timeframe_candidate_update.csv", seed_candidates)
    write_json(out_root / "ranked/per_asset_timeframe_seed_candidates.json", seed_candidates)
    lines = [
        "# Producer Seed Extraction Progress",
        "",
        RESEARCH_WARNING,
        "",
        f"- Timestamp: `{utc_now()}`",
        f"- Planned evaluations: `{summary.get('planned')}`",
        f"- Completed evaluations: `{summary.get('completed')}`",
        f"- Failed evaluations: `{summary.get('failed')}`",
        f"- Skipped already completed: `{summary.get('skipped_already_completed')}`",
        f"- Duplicate conflicts: `{summary.get('duplicate_conflicts')}`",
        f"- Seed candidate rows: `{len(seed_candidates)}`",
        f"- Asset/timeframe groups: `{len(per_group_summary)}`",
    ]
    (out_root / "reports/PRODUCER_SEED_EXTRACTION_PROGRESS.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (out_root / "reports/RUNTIME_PROGRESS.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return seed_candidates, conflicts


def run_tasks(variants: list[dict[str, Any]], splits: list[dict[str, Any]], out_root: Path, max_workers: int, time_budget_minutes: int) -> dict[str, Any]:
    registry = ResumeRegistry(out_root / "resume_registry.sqlite")
    deadline = datetime.now().astimezone() + timedelta(minutes=time_budget_minutes)
    planned = len(variants) * len(splits)
    completed = 0
    failed = 0
    skipped = 0
    results: list[dict[str, Any]] = []
    conflicts: list[dict[str, Any]] = []
    task_iter = iter(iter_tasks(variants, splits, out_root, max_workers))
    pending: dict[Any, dict[str, Any]] = {}
    max_pending = max_workers * 3
    done_planning = False
    last_checkpoint = time.time()
    last_heartbeat = 0.0
    start_ts = time.time()

    checkpoint(out_root, {"planned": planned, "completed": completed, "failed": failed, "skipped_already_completed": skipped, "pending": 0, "max_workers": max_workers})
    append_heartbeat(out_root, {"status": "running", "planned": planned, "completed": completed, "failed": failed, "pending": 0, "max_workers": max_workers})

    with ProcessPoolExecutor(max_workers=max_workers) as pool:
        while datetime.now().astimezone() < deadline:
            while not done_planning and len(pending) < max_pending:
                try:
                    task = next(task_iter)
                except StopIteration:
                    done_planning = True
                    break
                key = str(task["evaluation_key"])
                if registry.is_completed(key):
                    registry.mark_skipped_already_completed(key)
                    skipped += 1
                    continue
                registry.register_planned(key)
                registry.mark_running(key)
                pending[pool.submit(run_one, task)] = task

            if not pending and done_planning:
                break
            if not pending:
                time.sleep(1)
                continue

            done, _not_done = wait(pending.keys(), timeout=5, return_when=FIRST_COMPLETED)
            for future in done:
                task = pending.pop(future)
                try:
                    row = future.result()
                except Exception as exc:
                    row = {
                        "profile": PROFILE_ID,
                        "run_id": PROFILE_ID,
                        "stage": "A_PRODUCER_ONLY_SEED_EXTRACTION",
                        "evaluation_key": str(task.get("evaluation_key", "")),
                        "parameter_hash": str(task.get("parameter_hash", "")),
                        "failed_runner": True,
                        "error": str(exc),
                        "traceback": traceback.format_exc(),
                    }
                results.append(row)
                if str(row.get("failed_runner", "False")).lower() == "true":
                    failed += 1
                    registry.mark_failed(str(row.get("evaluation_key", "")), str(row.get("error", "")))
                else:
                    completed += 1
                    registry.mark_completed(str(row["evaluation_key"]), result_path="", metrics_hash=metrics_hash(row))

            if time.time() - last_heartbeat >= 5 * 60:
                append_heartbeat(out_root, {"status": "running", "planned": planned, "completed": completed, "failed": failed, "skipped_already_completed": skipped, "pending": len(pending), "max_workers": max_workers})
                last_heartbeat = time.time()

            if time.time() - last_checkpoint >= 15 * 60:
                summary = {"planned": planned, "completed": completed, "failed": failed, "skipped_already_completed": skipped, "pending": len(pending), "max_workers": max_workers, "deadline": deadline.isoformat()}
                _seeds, conflicts = write_progress_reports(out_root, results, {**summary, "duplicate_conflicts": len(conflicts)}, source_run_id=PROFILE_ID)
                write_json(out_root / "logs/runtime_summary.json", {**summary, "duplicate_conflicts": len(conflicts), "elapsed_seconds": round(time.time() - start_ts, 3)})
                checkpoint(out_root, {**summary, "duplicate_conflicts": len(conflicts)})
                registry.write_registry_report(out_root / "reports/RESUME_DEDUP_REPORT.md")
                last_checkpoint = time.time()
                if conflicts:
                    break

    summary = {"planned": planned, "completed": completed, "failed": failed, "skipped_already_completed": skipped, "pending": len(pending), "max_workers": max_workers, "deadline": deadline.isoformat()}
    seed_candidates, conflicts = write_progress_reports(out_root, results, {**summary, "duplicate_conflicts": len(conflicts)}, source_run_id=PROFILE_ID)
    write_json(out_root / "logs/runtime_summary.json", {**summary, "duplicate_conflicts": len(conflicts), "elapsed_seconds": round(time.time() - start_ts, 3), "seed_candidate_rows": len(seed_candidates)})
    checkpoint(out_root, {**summary, "duplicate_conflicts": len(conflicts), "seed_candidate_rows": len(seed_candidates)})
    append_heartbeat(out_root, {"status": "completed" if done_planning and not pending else "time_budget_reached", "planned": planned, "completed": completed, "failed": failed, "skipped_already_completed": skipped, "pending": len(pending), "max_workers": max_workers})
    registry.write_registry_report(out_root / "reports/RESUME_DEDUP_REPORT.md")
    return {**summary, "duplicate_conflicts": len(conflicts), "seed_candidate_rows": len(seed_candidates), "time_budget_reached": not done_planning or bool(pending)}


def write_session_reports(out_root: Path, payload: dict[str, Any]) -> None:
    lines = [
        "# 12h Backtesting Session Runtime Report",
        "",
        RESEARCH_WARNING,
        "",
        f"- Timestamp: `{utc_now()}`",
        f"- Run id: `{PROFILE_ID}`",
        f"- Verdict: `{payload.get('verdict')}`",
        f"- Worker count: `{payload.get('max_workers')}`",
        f"- Planned evaluations: `{payload.get('planned')}`",
        f"- Completed evaluations: `{payload.get('completed')}`",
        f"- Failed evaluations: `{payload.get('failed')}`",
        f"- Duplicate conflicts: `{payload.get('duplicate_conflicts')}`",
        f"- Seed candidate rows: `{payload.get('seed_candidate_rows')}`",
        f"- Time budget reached: `{payload.get('time_budget_reached')}`",
        "",
        "## Outputs",
        "",
        "- `ranked/per_asset_timeframe_seed_candidates.csv`",
        "- `ranked/per_asset_timeframe_summary.csv`",
        "- `ranked/all_evaluations.csv`",
        "- `logs/runtime_summary.json`",
        "- `reports/RESUME_DEDUP_REPORT.md`",
    ]
    (out_root / "reports/12H_BACKTESTING_SESSION_RUNTIME_REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--regimes", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--max-workers", type=int, required=True)
    parser.add_argument("--time-budget-minutes", type=int, required=True)
    parser.add_argument("--max-assets", type=int, default=8)
    parser.add_argument("--target-variants", type=int, default=720)
    args = parser.parse_args()

    if args.max_workers < 16:
        raise SystemExit("--max-workers must be at least 16 for the 12h session unless a separate documented fallback is used")
    if args.max_workers > 16:
        raise SystemExit("--max-workers must not exceed 16 without a new scaling benchmark")
    if args.time_budget_minutes < 1:
        raise SystemExit("--time-budget-minutes must be positive")

    for key in ["OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS", "NUMEXPR_NUM_THREADS"]:
        os.environ[key] = "1"

    out_root = Path(args.out)
    for subdir in ["detached", "logs", "checkpoints", "heartbeat", "ranked", "results", "per_asset_timeframe", "parameter_library_updates", "reports", "failures", "datasets", "walkforward", "workers"]:
        (out_root / subdir).mkdir(parents=True, exist_ok=True)

    started_at = utc_now()
    manifest_path = Path(args.manifest)
    regime_path = Path(args.regimes)
    selected, selection_summary = select_stage_datasets(manifest_path, regime_path, out_root, args.max_assets)
    if len({str(item["symbol"]) for item in selected}) < 5:
        write_json(out_root / "detached/run_status.json", {"status": "blocked", "reason": "fewer_than_5_assets", "selected_assets": sorted({str(item["symbol"]) for item in selected})})
        return 2

    splits = create_walkforward(selected, out_root)
    variants = generate_smart_sample_variants(args.target_variants)
    planned = len(variants) * len(splits)
    run_config = {
        "started_at": started_at,
        "run_id": PROFILE_ID,
        "mode": "staged_supertrend_producer_only_seed_extraction",
        "warning": RESEARCH_WARNING,
        "manifest": str(manifest_path),
        "regime_registry": str(regime_path),
        "selected_assets": selection_summary["selected_assets"],
        "selected_timeframes": TIMEFRAMES,
        "selected_dataset_count": len(selected),
        "walkforward_split_count": len(splits),
        "unique_parameter_variants": len(variants),
        "planned_evaluations": planned,
        "max_workers": args.max_workers,
        "time_budget_minutes": args.time_budget_minutes,
        "thread_pinning": {key: os.environ.get(key) for key in ["OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS", "NUMEXPR_NUM_THREADS"]},
        "resume_registry": str(out_root / "resume_registry.sqlite"),
        "output_root": str(out_root),
    }
    write_json(out_root / "run_config.json", run_config)
    write_json(out_root / "detached/run_status.json", {"status": "running", **run_config})
    (out_root / "session_plan_runtime.md").write_text(
        "# Runtime Session Plan\n\n"
        f"- Stage: `A_PRODUCER_ONLY_SEED_EXTRACTION`\n"
        f"- Planned evaluations: `{planned}`\n"
        f"- Workers: `{args.max_workers}`\n"
        f"- Time budget minutes: `{args.time_budget_minutes}`\n"
        f"- Warning: {RESEARCH_WARNING}\n",
        encoding="utf-8",
    )

    print(json.dumps(run_config, indent=2, sort_keys=True))
    summary = run_tasks(variants, splits, out_root, args.max_workers, args.time_budget_minutes)
    verdict = "12H_BACKTESTING_SESSION_COMPLETED" if not summary.get("time_budget_reached") and summary.get("duplicate_conflicts") == 0 else "12H_BACKTESTING_SESSION_TIME_BUDGET_REACHED"
    final_payload = {**run_config, **summary, "completed_at": utc_now(), "verdict": verdict}
    write_json(out_root / "detached/run_status.json", {"status": "completed", **final_payload})
    write_session_reports(out_root, final_payload)
    print(json.dumps(final_payload, indent=2, sort_keys=True))
    return 0 if summary.get("duplicate_conflicts") == 0 else 3


if __name__ == "__main__":
    raise SystemExit(main())
