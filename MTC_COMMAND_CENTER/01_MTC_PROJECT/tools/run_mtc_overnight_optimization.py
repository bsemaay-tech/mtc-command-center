from __future__ import annotations

import argparse
import csv
import itertools
import json
import math
import os
import random
import sys
import traceback
from concurrent.futures import ProcessPoolExecutor, as_completed
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "00_PYTHON"))
sys.path.insert(0, str(ROOT))

from mtc_v2.core.config import DEFAULT_CONFIG, validate_config
from mtc_v2.core.runner import Runner
from mtc_v2.core.types import Bar
from tools.optimization_parameter_mapper import apply_parameter_mapping
from tools.optimization_resume_registry import (
    EvaluationIdentity,
    REGISTRY_VERSION,
    ResumeRegistry,
    evaluation_key,
    metrics_hash,
)
from tools.optimization_worker_io import WorkerPaths, append_log, ensure_variant, safe_id, utc_run_id, write_json_isolated
from tools.runner_metrics_adapter import RUNNER_METRICS_ADAPTER_VERSION, run_with_result
from tools.score_optimization_results import write_scored_outputs
from tools.verify_dataset_manifest import read_simple_yaml, sha256_file, verify_manifest


def load_json_or_yaml(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8").strip()
    if text.startswith("{"):
        return json.loads(text)
    return read_simple_yaml(path)


def load_bars(csv_path: Path, *, start: int = 0, end: int | None = None) -> list[Bar]:
    bars: list[Bar] = []
    with csv_path.open("r", encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh)
        rows = list(reader)
    selected = rows[start:end]
    for idx, row in enumerate(selected):
        raw_time = str(row.get("time") or row.get("timestamp") or row.get("datetime") or "")
        if raw_time.isdigit():
            ts = datetime.fromtimestamp(int(raw_time), tz=timezone.utc)
        else:
            ts = datetime.fromisoformat(raw_time.replace("Z", "+00:00"))
        bars.append(
            Bar(
                timestamp=ts,
                open=float(row["open"]),
                high=float(row["high"]),
                low=float(row["low"]),
                close=float(row["close"]),
                volume=float(row.get("volume") or 0.0),
                bar_index=idx,
            )
        )
    return bars


def generate_variants(profile: dict[str, Any]) -> list[dict[str, Any]]:
    params: dict[str, list[Any]] = profile.get("parameters", {})
    keys = list(params.keys())
    values = [params[key] for key in keys]
    variants = [dict(zip(keys, combo)) for combo in itertools.product(*values)]
    seed = int(profile.get("shuffle_seed", 1701))
    random.Random(seed).shuffle(variants)
    max_variants = int(profile.get("max_variants", len(variants)))
    return variants[:max_variants]


def _max_drawdown_pct(equity_curve: list[float], initial_capital: float) -> float:
    if not equity_curve:
        return 0.0
    peak = initial_capital
    max_dd = 0.0
    for value in equity_curve:
        peak = max(peak, value)
        if peak > 0:
            max_dd = max(max_dd, (peak - value) / peak * 100.0)
    return max_dd


def run_engine_metrics(bars: list[Bar], overrides: dict[str, Any]) -> dict[str, Any]:
    base = dict(DEFAULT_CONFIG)
    base.update(
        {
            "instrument_symbol": "BTCUSDT.P",
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
    config = base
    result = run_with_result(bars, config_overrides=config)
    row = result.to_optimizer_row()
    initial = float(config["initial_capital"])
    row.update(
        {
            "final_equity": initial + float(row["net_profit"]),
            "max_qty": None,
            "max_notional": None,
            "trade_events": [
                {
                    **trade.__dict__,
                    "entry_time": trade.entry_time.isoformat() if trade.entry_time else None,
                    "exit_time": trade.exit_time.isoformat() if trade.exit_time else None,
                }
                for trade in result.trades
            ],
            "unrealistic_qty_or_leverage": False,
        }
    )
    return row


def task_evaluation_identity(task: dict[str, Any], manifest: dict[str, Any] | None = None) -> EvaluationIdentity:
    manifest = manifest or {}
    return EvaluationIdentity(
        profile_id=str(task.get("profile_name", "")),
        dataset_id=str(manifest.get("dataset_id", task.get("dataset_id", "single_dataset"))),
        dataset_hash=str(manifest.get("sha256", task.get("dataset_sha256", ""))),
        symbol=str(manifest.get("symbol", task.get("symbol", ""))),
        timeframe=str(manifest.get("timeframe", task.get("timeframe", ""))),
        window_id=str(task.get("window_id", "in_out_split")),
        split_type=str(task.get("split_type", "combined_in_out")),
        params=dict(task.get("params", {})),
        runner_version=RUNNER_METRICS_ADAPTER_VERSION,
        optimizer_version="run_mtc_overnight_optimization_v1",
        parameter_mapper_version="optimization_parameter_mapper_v1",
    )


def run_variant(task: dict[str, Any]) -> dict[str, Any]:
    root = Path(task["root"])
    worker_paths = WorkerPaths(root=root, run_id=task["run_id"], worker_id=task["worker_id"])
    variant_id = task["variant_id"]
    variant_root = ensure_variant(worker_paths, variant_id)
    try:
        manifest = read_simple_yaml(Path(task["dataset_manifest"]))
        source_type = str(manifest.get("source_type", "legacy_single_dataset_manifest"))
        if source_type == "unknown_csv":
            raise RuntimeError("unknown_csv dataset blocked by optimizer rules")
        source_path = Path(str(manifest["source_path"]))
        if not source_path.is_absolute():
            source_path = ROOT / source_path
        if source_path.suffix.lower() == ".xlsx":
            raise RuntimeError("xlsx chart data forbidden")
        expected_hash = str(manifest["sha256"])
        actual_hash = sha256_file(source_path)
        if expected_hash != actual_hash:
            raise RuntimeError(f"dataset_hash_mismatch expected={expected_hash} actual={actual_hash}")
        raw_params = dict(task["params"])
        overrides = apply_parameter_mapping(raw_params)
        split = task["split"]
        in_bars = load_bars(source_path, start=0, end=split)
        out_bars = load_bars(source_path, start=split, end=None)
        in_metrics = run_engine_metrics(in_bars, overrides)
        out_metrics = run_engine_metrics(out_bars, overrides)
        out_quality = 0.0
        if out_metrics["net_profit_pct"] > 0 and out_metrics["profit_factor"] > 1.0:
            out_quality = min(1.0, (out_metrics["profit_factor"] - 1.0) / 2.0)
        record = {
            "profile": task["profile_name"],
            "variant_id": variant_id,
            "evaluation_key": task.get("evaluation_key", ""),
            "worker_id": task["worker_id"],
            "dataset_sha256": actual_hash,
            "source_type": source_type,
            "params": raw_params,
            "overrides": overrides,
            "failed_runner": False,
            "dataset_hash_mismatch": False,
            "out_of_sample_quality": out_quality,
            **{f"in_sample_{key}": value for key, value in in_metrics.items() if key != "trade_events"},
            **{key: value for key, value in out_metrics.items() if key != "trade_events"},
        }
        write_json_isolated(variant_root / "result.json", worker_paths.worker_root, record)
        write_json_isolated(variant_root / "in_sample_trades.json", worker_paths.worker_root, in_metrics["trade_events"])
        write_json_isolated(variant_root / "out_of_sample_trades.json", worker_paths.worker_root, out_metrics["trade_events"])
        append_log(worker_paths, f"{variant_id} ok score_input_trades={record['total_trades']}")
        return record
    except Exception as exc:
        failure = {
            "profile": task["profile_name"],
            "variant_id": variant_id,
            "evaluation_key": task.get("evaluation_key", ""),
            "worker_id": task["worker_id"],
            "params": task["params"],
            "failed_runner": True,
            "error": str(exc),
            "traceback": traceback.format_exc(),
            "net_profit_pct": 0.0,
            "profit_factor": 0.0,
            "max_drawdown_pct": 999.0,
            "win_rate": 0.0,
            "total_trades": 0,
            "out_of_sample_quality": 0.0,
        }
        write_json_isolated(variant_root / "failure.json", worker_paths.worker_root, failure)
        append_log(worker_paths, f"{variant_id} failed {exc}")
        return failure


def write_checkpoint(root: Path, profile_name: str, completed: int, planned: int) -> None:
    checkpoint_dir = root / "checkpoints"
    checkpoint_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    payload = {
        "profile": profile_name,
        "completed": completed,
        "planned": planned,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    (checkpoint_dir / f"{profile_name}_{stamp}.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")


def write_profile_report(profile: dict[str, Any], out_dir: Path, records: list[dict[str, Any]], worker_count: int, dataset_hash: str) -> None:
    ranked_path = out_dir / "ranked_results.csv"
    top_path = out_dir / "top_20_candidates.json"
    top = json.loads(top_path.read_text(encoding="utf-8")) if top_path.exists() else []
    completed = len(records)
    failed = len([row for row in records if row.get("failed_runner")])
    rejected = len(json.loads((out_dir / "rejected_variants.json").read_text(encoding="utf-8"))) if (out_dir / "rejected_variants.json").exists() else 0
    best = top[0] if top else {}
    lines = [
        f"# {profile['name']} Optimization Report",
        "",
        f"## A. Profile purpose\n{profile.get('purpose', '')}",
        f"## B. Parameter space\n{json.dumps(profile.get('parameters', {}), indent=2)}",
        f"## C. Dataset hash\n{dataset_hash}",
        f"## D. Worker count\n{worker_count}",
        f"## E. Variants planned\n{profile.get('max_variants')}",
        f"## F. Variants completed\n{completed}",
        f"## G. Failed variants\n{failed}",
        f"## H. Rejected variants\n{rejected}",
        f"## I. Top 20 candidates\n{json.dumps(top[:20], indent=2)}",
        f"## J. Best in-sample result\n{json.dumps({k: v for k, v in best.items() if str(k).startswith('in_sample_')}, indent=2)}",
        f"## K. Best out-of-sample result\n{json.dumps({k: best.get(k) for k in ['net_profit_pct','profit_factor','max_drawdown_pct','win_rate','total_trades','score']}, indent=2)}",
        "## L. Stability notes\nOnly candidates with positive out-of-sample metrics can rank; this is research output, not production readiness.",
        "## M. Search-space problems\nGuard, integration, visualization, session, HTF, MACD complex, and candle families stayed excluded.",
        "## N. Runtime problems\nSee failed_variants.json and worker logs.",
        "## O. Recommendation\nUse top out-of-sample stable candidates only as next audit inputs; do not change Pine behavior from this run alone.",
        f"\nRanked CSV: {ranked_path}",
    ]
    report_dir = ROOT / "reports/optimization/overnight_optimization/reports"
    report_dir.mkdir(parents=True, exist_ok=True)
    (report_dir / f"{profile['name']}_OPTIMIZATION_REPORT.md").write_text("\n\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", required=True)
    parser.add_argument("--dataset", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--max-workers", default="auto")
    parser.add_argument("--time-budget-minutes", type=int, default=420)
    parser.add_argument("--validation-batch", type=int, default=20)
    args = parser.parse_args()
    ok, message = verify_manifest(Path(args.dataset))
    if not ok:
        raise SystemExit(message)
    profile = load_json_or_yaml(Path(args.profile))
    out_dir = Path(args.out)
    root = ROOT / "reports/optimization/overnight_optimization"
    out_dir.mkdir(parents=True, exist_ok=True)
    run_id = utc_run_id(profile["name"])
    cpu = os.cpu_count() or 2
    worker_count = min(max(cpu - 1, 1), 4) if args.max_workers == "auto" else max(1, int(args.max_workers))
    variants = generate_variants(profile)
    manifest = read_simple_yaml(Path(args.dataset))
    if str(manifest.get("source_type", "")) == "unknown_csv":
        raise SystemExit("unknown_csv dataset blocked by optimizer rules")
    source_path = Path(str(manifest["source_path"]))
    if not source_path.is_absolute():
        source_path = ROOT / source_path
    if source_path.suffix.lower() == ".xlsx":
        raise SystemExit("xlsx chart data forbidden")
    row_count = int(manifest["row_count"])
    split = int(row_count * 0.70) if row_count >= 100 else int(row_count * 0.80)
    deadline = datetime.now(timezone.utc) + timedelta(minutes=args.time_budget_minutes)
    tasks = []
    for idx, params in enumerate(variants):
        worker_id = safe_id("worker", idx % worker_count)
        task = {
            "root": str(root),
            "run_id": run_id,
            "worker_id": worker_id,
            "variant_id": safe_id("variant", idx),
            "profile_name": profile["name"],
            "params": params,
            "dataset_manifest": str(Path(args.dataset)),
            "source_type": str(manifest.get("source_type", "legacy_single_dataset_manifest")),
            "split": split,
        }
        task["evaluation_key"] = evaluation_key(task_evaluation_identity(task, manifest))
        tasks.append(task)
    records: list[dict[str, Any]] = []
    registry = ResumeRegistry(out_dir / "resume_registry.sqlite")
    scheduled_tasks: list[dict[str, Any]] = []
    skipped_completed = 0
    for task in tasks:
        key = str(task["evaluation_key"])
        if registry.is_completed(key):
            registry.mark_skipped_already_completed(key)
            skipped_completed += 1
            continue
        registry.register_planned(key)
        scheduled_tasks.append(task)
    last_checkpoint = datetime.now(timezone.utc) - timedelta(minutes=15)
    with ProcessPoolExecutor(max_workers=worker_count) as pool:
        for task in scheduled_tasks:
            registry.mark_running(str(task["evaluation_key"]))
        futures = {pool.submit(run_variant, task): task for task in scheduled_tasks}
        for future in as_completed(futures):
            row = future.result()
            records.append(row)
            key = str(row.get("evaluation_key", ""))
            if bool(row.get("failed_runner")):
                registry.mark_failed(key, str(row.get("error", "")))
            else:
                registry.mark_completed(key, result_path="", metrics_hash=metrics_hash(row))
            if datetime.now(timezone.utc) - last_checkpoint >= timedelta(minutes=15):
                write_checkpoint(root, profile["name"], len(records), len(scheduled_tasks))
                last_checkpoint = datetime.now(timezone.utc)
            if datetime.now(timezone.utc) >= deadline:
                break
    records, duplicate_conflicts = registry.dedupe_results(records)
    write_checkpoint(root, profile["name"], len(records), len(scheduled_tasks))
    registry.write_registry_report(out_dir / "RESUME_DEDUP_REGISTRY_RUNTIME_REPORT.md")
    raw_path = out_dir / "raw_variant_records.json"
    raw_path.write_text(json.dumps(records, indent=2, sort_keys=True), encoding="utf-8")
    write_scored_outputs(records, out_dir)
    in_rows = []
    out_rows = []
    for row in records:
        in_rows.append({key.replace("in_sample_", ""): value for key, value in row.items() if key.startswith("in_sample_")} | {"variant_id": row["variant_id"]})
        out_rows.append({key: value for key, value in row.items() if key in {"variant_id", "net_profit_pct", "profit_factor", "max_drawdown_pct", "win_rate", "total_trades", "failed_runner"}})
    for path, rows in [(out_dir / "in_sample_results.csv", in_rows), (out_dir / "out_of_sample_results.csv", out_rows)]:
        fields = sorted({key for item in rows for key in item.keys()})
        with path.open("w", encoding="utf-8", newline="") as fh:
            writer = csv.DictWriter(fh, fieldnames=fields)
            writer.writeheader()
            writer.writerows(rows)
    write_profile_report(profile, out_dir, records, worker_count, str(manifest["sha256"]))
    print(json.dumps({"profile": profile["name"], "planned": len(tasks), "scheduled": len(scheduled_tasks), "completed": len(records), "skipped_already_completed": skipped_completed, "duplicate_conflicts": len(duplicate_conflicts), "registry_version": REGISTRY_VERSION, "workers": worker_count, "out": str(out_dir)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
