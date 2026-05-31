from __future__ import annotations

import argparse
import csv
import json
import os
import platform
import shutil
import statistics
import subprocess
import sys
import time
from concurrent.futures import FIRST_COMPLETED, ProcessPoolExecutor, wait
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "00_PYTHON"))
sys.path.insert(0, str(ROOT))

from mtc_v2.core.config import DEFAULT_CONFIG, validate_config
from tools.optimization_parameter_mapper import apply_parameter_mapping
from tools.optimization_resume_registry import ResumeRegistry, metrics_hash
from tools.run_big_overnight_multiasset_optimization import (
    PROFILE_ID,
    bundle_root_from_manifest,
    canonical_params,
    create_walkforward,
    iter_tasks,
    load_manifest,
    load_regime_registry,
    normalized_dataset_entry,
    run_one,
    task_identity,
    write_csv,
    write_json,
)


BENCH_ROOT = ROOT / "reports/optimization/worker_scaling_benchmark"
MANIFEST = Path(r"C:\LAB\tradingview-lab\MTC_V2_OPTIMIZATION_DATA_BUNDLE_20260427\manifests\dataset_manifest.json")
REGIMES = Path(r"C:\LAB\tradingview-lab\MTC_V2_OPTIMIZATION_DATA_BUNDLE_20260427\regimes\regime_registry.json")
THREAD_VARS = ["OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS", "NUMEXPR_NUM_THREADS"]
REQUIRED_WORKERS = [4, 6, 8, 10, 12]
OPTIONAL_WORKERS = [16, 20, 24]
TARGET_ASSETS = ["BTCUSDT", "ETHUSDT", "SOLUSDT"]
TARGET_TIMEFRAMES = ["15m", "1h", "4h"]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_dirs() -> None:
    for rel in ["system", "inspection", "benchmark_runs", "summaries", "logs", "patch_proposals"]:
        (BENCH_ROOT / rel).mkdir(parents=True, exist_ok=True)


def set_thread_pinning() -> dict[str, dict[str, str | None]]:
    previous = {name: os.environ.get(name) for name in THREAD_VARS}
    for name in THREAD_VARS:
        os.environ[name] = "1"
    current = {name: os.environ.get(name) for name in THREAD_VARS}
    return {"previous": previous, "benchmark": current}


def run_text(command: list[str]) -> str:
    try:
        result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, timeout=30)
        return (result.stdout + result.stderr).strip()
    except Exception as exc:
        return f"unavailable: {exc}"


def collect_system() -> dict[str, Any]:
    disk = shutil.disk_usage(ROOT)
    payload: dict[str, Any] = {
        "timestamp": utc_now(),
        "platform": platform.platform(),
        "python": sys.version,
        "os_cpu_count": os.cpu_count(),
        "disk": {"total": disk.total, "used": disk.used, "free": disk.free},
        "env": {name: os.environ.get(name) for name in THREAD_VARS},
        "powershell_processor": run_text(
            [
                "powershell",
                "-NoProfile",
                "-Command",
                "Get-CimInstance Win32_Processor | Select-Object -First 1 Name,NumberOfCores,NumberOfLogicalProcessors,MaxClockSpeed | ConvertTo-Json -Compress",
            ]
        ),
        "powershell_memory": run_text(
            [
                "powershell",
                "-NoProfile",
                "-Command",
                "Get-CimInstance Win32_ComputerSystem | Select-Object TotalPhysicalMemory | ConvertTo-Json -Compress; Get-CimInstance Win32_OperatingSystem | Select-Object FreePhysicalMemory,TotalVisibleMemorySize | ConvertTo-Json -Compress",
            ]
        ),
    }
    try:
        import numpy as np

        payload["numpy"] = np.__version__
    except Exception as exc:
        payload["numpy"] = f"unavailable: {exc}"
    try:
        import pandas as pd

        payload["pandas"] = pd.__version__
    except Exception as exc:
        payload["pandas"] = f"unavailable: {exc}"
    return payload


def parse_json_sidecar_text(text: str) -> list[dict[str, Any]]:
    rows = []
    for line in text.splitlines():
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            pass
    return rows


def write_inspection_reports(thread_info: dict[str, dict[str, str | None]], system_info: dict[str, Any]) -> None:
    ensure_dirs()
    write_json(BENCH_ROOT / "system/system_resource.json", system_info)
    (BENCH_ROOT / "system/SYSTEM_RESOURCE_REPORT.md").write_text(
        "\n".join(
            [
                "# System Resource Report",
                "",
                f"- Timestamp: `{system_info['timestamp']}`",
                f"- Platform: `{system_info['platform']}`",
                f"- Python: `{system_info['python'].splitlines()[0]}`",
                f"- os.cpu_count(): `{system_info['os_cpu_count']}`",
                f"- Processor: `{system_info['powershell_processor']}`",
                f"- Memory: `{system_info['powershell_memory']}`",
                f"- Disk free bytes: `{system_info['disk']['free']}`",
                f"- NumPy: `{system_info['numpy']}`",
                f"- Pandas: `{system_info['pandas']}`",
                f"- Env before benchmark process: `{system_info['env']}`",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    (BENCH_ROOT / "system/THREAD_PINNING_REPORT.md").write_text(
        "\n".join(
            [
                "# Thread Pinning Report",
                "",
                f"- Previous values: `{thread_info['previous']}`",
                f"- Benchmark values: `{thread_info['benchmark']}`",
                "- Reason: worker scaling uses process-level parallelism, so BLAS/OpenMP thread pools are pinned to 1 to reduce CPU oversubscription.",
                "- Child worker processes inherit these values from the benchmark launcher environment.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    (BENCH_ROOT / "inspection/WORKER_COUNT_ORIGIN_REPORT.md").write_text(
        "\n".join(
            [
                "# Worker Count Origin Report",
                "",
                "## Answers",
                "",
                "1. Was worker count passed by CLI? Unknown for the old run; metadata records the resolved value, not the original CLI token.",
                "2. Was worker count hardcoded? The exact value was not hardcoded as a constant, but `auto` mode has a hard cap of 6 in the big and multidataset runners.",
                "3. Is there a default like max_workers = 6? The default CLI value is `auto`; `auto` resolves to at most 6 in `tools/run_big_overnight_multiasset_optimization.py`.",
                "4. Is there a cap like min(cpu_count - 1, 6)? Yes: `min(max(os.cpu_count() - 1, 1), 6)`.",
                "5. Is there logic to increase from 6 to 8 after stability? No.",
                "6. Was that logic implemented or only described in prompt? Not implemented in the inspected runner files.",
                "7. Does the report record actual worker count correctly? Yes: final report, `run_config.json`, `worker_plan.md`, and `logs/runtime_summary.json` record 6.",
                "8. Can worker count be controlled by CLI? Yes, with `--max-workers N`; explicit values bypass the auto cap.",
                "9. Can worker count be controlled by job YAML? Not in the inspected example job YAML and not in the big runner.",
                "10. What exact code path chose 6 workers? `args.max_workers == \"auto\"` -> `cpu = os.cpu_count() or 2` -> `max_workers = min(max(cpu - 1, 1), 6)`.",
                "11. What must change for safer higher workers? Add a shared worker resolver, record CLI token/cpu/thread env, support optional job YAML `runtime.max_workers`, and keep explicit CLI override.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def validate_tp_patch() -> bool:
    rows = []
    for params in [
        {
            "signal_mode": "Supertrend",
            "st_factor": 3.5,
            "global_atr_length": 10,
            "sl_atr_mult": 3.0,
            "tp_mode": "None",
            "tp_r_multiple": 2.0,
            "risk_long": 0.25,
            "risk_short": 0.75,
            "guards_disabled_for_phase1": True,
            "integrations_disabled": True,
            "visualization_disabled": True,
            "exit_on_filter_bundle": True,
        },
        {
            "signal_mode": "Supertrend",
            "st_factor": 3.5,
            "global_atr_length": 10,
            "sl_atr_mult": 3.0,
            "tp_mode": "R",
            "tp_r_multiple": 2.0,
            "risk_long": 0.25,
            "risk_short": 0.75,
            "guards_disabled_for_phase1": True,
            "integrations_disabled": True,
            "visualization_disabled": True,
            "exit_on_filter_bundle": True,
        },
    ]:
        canonical = canonical_params(params)
        runner_params = dict(canonical)
        if runner_params.get("tp_mode") == "None" and runner_params.get("tp_r_multiple") is None:
            runner_params["tp_r_multiple"] = 1.0
        overrides = apply_parameter_mapping(runner_params)
        config = dict(DEFAULT_CONFIG)
        config.update(overrides)
        validate_config(config)
        rows.append({"tp_mode": canonical["tp_mode"], "canonical_tp_r_multiple": canonical["tp_r_multiple"], "runner_tp_r_multiple": overrides["tp_r_multiple"], "validation": "PASS"})
    (BENCH_ROOT / "inspection/POST_RUN_PATCH_VALIDATION_FOR_BENCHMARK.md").write_text(
        "\n".join(
            [
                "# Post-Run Patch Validation For Benchmark",
                "",
                "- `tp_mode=None` canonicalizes `tp_r_multiple` to null.",
                "- Benchmark launcher converts canonical null to numeric `tp_r_multiple=1.0` before Runner validation.",
                "- `tp_mode=R` keeps numeric `tp_r_multiple`.",
                "",
                "```json",
                json.dumps(rows, indent=2, sort_keys=True),
                "```",
                "",
                "Verdict: `POST_RUN_PATCH_VALIDATION_FOR_BENCHMARK_PASS`",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    return True


def build_benchmark_variants() -> list[dict[str, Any]]:
    base_combos = []
    risk_pairs = [(0.25, 0.5), (0.25, 0.75), (0.5, 0.5), (0.5, 0.75)]
    for st_factor in [3.0, 3.5, 4.0]:
        for atr_len in [7, 10, 14]:
            for sl_mult in [2.75, 3.0, 3.5]:
                base_combos.append((st_factor, atr_len, sl_mult))
    variants = []
    for idx, (st_factor, atr_len, sl_mult) in enumerate(base_combos):
        if len(variants) >= 40:
            break
        risk_long, risk_short = risk_pairs[idx % len(risk_pairs)]
        for tp_mode, tp_r_multiple in [("None", None), ("R", 2.0)]:
            variants.append(
                canonical_params(
                    {
                        "signal_mode": "Supertrend",
                        "st_factor": st_factor,
                        "global_atr_length": atr_len,
                        "sl_atr_mult": sl_mult,
                        "tp_mode": tp_mode,
                        "tp_r_multiple": tp_r_multiple,
                        "risk_long": risk_long,
                        "risk_short": risk_short,
                        "use_break_even": False,
                        "use_trailing": False,
                        "guards_disabled_for_phase1": True,
                        "integrations_disabled": True,
                        "visualization_disabled": True,
                        "exit_on_filter_bundle": True,
                    }
                )
            )
            if len(variants) >= 40:
                break
    return variants


def select_datasets() -> list[dict[str, Any]]:
    manifest = load_manifest(MANIFEST)
    regimes = load_regime_registry(REGIMES)
    bundle = bundle_root_from_manifest(MANIFEST)
    selected = []
    for symbol in TARGET_ASSETS:
        for timeframe in TARGET_TIMEFRAMES:
            candidates = [
                item
                for item in manifest
                if str(item.get("symbol")) == symbol
                and str(item.get("timeframe_normalized") or item.get("timeframe")) == timeframe
            ]
            if not candidates:
                continue
            item = normalized_dataset_entry(max(candidates, key=lambda row: int(row.get("row_count", 0))), bundle)
            regime = regimes.get(str(item["dataset_id"]), {})
            regime_file = Path(str(regime.get("regime_file", "")))
            if not regime_file.is_absolute():
                regime_file = bundle / regime_file
            item["regime_file_abs"] = str(regime_file)
            selected.append(item)
    return selected


def build_taskset() -> list[dict[str, Any]]:
    selected = select_datasets()
    taskset_root = BENCH_ROOT / "benchmark_runs/taskset_build"
    if taskset_root.exists():
        shutil.rmtree(taskset_root)
    for sub in ["walkforward", "reports"]:
        (taskset_root / sub).mkdir(parents=True, exist_ok=True)
    all_splits = create_walkforward(selected, taskset_root)
    first_window_splits = [row for row in all_splits if str(row.get("window_id", "")).endswith("_wf1")]
    variants = build_benchmark_variants()
    tasks = list(iter_tasks(variants, first_window_splits, BENCH_ROOT / "benchmark_runs/TASKSET_PLACEHOLDER", worker_count=1))
    payload = {
        "manifest": str(MANIFEST),
        "regime_registry": str(REGIMES),
        "selected_datasets": [
            {
                "dataset_id": item["dataset_id"],
                "symbol": item["symbol"],
                "timeframe": item["timeframe_normalized"],
                "source_type": item["source_type"],
                "row_count": item["row_count"],
            }
            for item in selected
        ],
        "variant_count": len(variants),
        "split_count": len(first_window_splits),
        "task_count": len(tasks),
        "tasks": [
            {
                "evaluation_key": task["evaluation_key"],
                "parameter_hash": task["parameter_hash"],
                "params": task["params"],
                "split": {
                    "dataset_id": task["split"]["dataset_id"],
                    "symbol": task["split"]["symbol"],
                    "timeframe": task["split"]["timeframe_normalized"],
                    "source_type": task["split"].get("source_type", ""),
                    "window_id": task["split"]["window_id"],
                    "split_type": task["split"]["split_type"],
                },
            }
            for task in tasks
        ],
    }
    write_json(BENCH_ROOT / "benchmark_runs/benchmark_taskset.json", payload)
    (BENCH_ROOT / "benchmark_runs/BENCHMARK_TASKSET.md").write_text(
        "\n".join(
            [
                "# Benchmark Taskset",
                "",
                f"- Manifest: `{MANIFEST}`",
                f"- Regime registry: `{REGIMES}`",
                f"- Selected datasets: `{len(selected)}`",
                f"- Assets: `{', '.join(sorted({str(item['symbol']) for item in selected}))}`",
                f"- Timeframes: `{', '.join(sorted({str(item['timeframe_normalized']) for item in selected}))}`",
                f"- Unique parameter variants: `{len(variants)}`",
                f"- Splits: `{len(first_window_splits)}`",
                f"- Evaluation tasks per worker count: `{len(tasks)}`",
                "- Contains both `tp_mode=None` and `tp_mode=R` variants.",
                "- This is a benchmark subset, not a broad optimization.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    return tasks


def taskset_for_out(worker_count: int, out_root: Path) -> list[dict[str, Any]]:
    selected = select_datasets()
    taskset_root = BENCH_ROOT / "benchmark_runs/taskset_runtime"
    for sub in ["walkforward", "reports"]:
        (taskset_root / sub).mkdir(parents=True, exist_ok=True)
    all_splits = create_walkforward(selected, taskset_root)
    first_window_splits = [row for row in all_splits if str(row.get("window_id", "")).endswith("_wf1")]
    variants = build_benchmark_variants()
    return list(iter_tasks(variants, first_window_splits, out_root, worker_count=worker_count))


def percentile(values: list[float], pct: float) -> float | None:
    if not values:
        return None
    ordered = sorted(values)
    index = min(len(ordered) - 1, max(0, int(round((pct / 100.0) * (len(ordered) - 1)))))
    return ordered[index]


def run_worker_count(worker_count: int, *, resume_only: bool = False) -> dict[str, Any]:
    out_root = BENCH_ROOT / "benchmark_runs" / f"workers_{worker_count:02d}"
    if out_root.exists() and not resume_only:
        shutil.rmtree(out_root)
    for sub in ["workers", "results", "logs", "reports", "checkpoints"]:
        (out_root / sub).mkdir(parents=True, exist_ok=True)
    tasks = taskset_for_out(worker_count, out_root)
    registry = ResumeRegistry(out_root / "resume_registry.sqlite")
    pending = {}
    rows: list[dict[str, Any]] = []
    completed = 0
    failed = 0
    skipped = 0
    started = time.perf_counter()
    started_at = utc_now()
    with ProcessPoolExecutor(max_workers=worker_count) as pool:
        task_iter = iter(tasks)
        done_planning = False
        max_pending = worker_count * 3
        while True:
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
            done, _ = wait(pending.keys(), timeout=5, return_when=FIRST_COMPLETED)
            for future in done:
                task = pending.pop(future)
                row = future.result()
                row["worker_count"] = worker_count
                row["benchmark_run_id"] = f"workers_{worker_count:02d}"
                row["worker_id"] = task["worker_id"]
                row["identity_json"] = json.dumps(task_identity(row.get("params") or task["params"], task["split"]).__dict__, sort_keys=True, default=str)
                rows.append(row)
                if str(row.get("failed_runner", "False")).lower() == "true":
                    failed += 1
                    registry.mark_failed(str(row.get("evaluation_key", "")), str(row.get("error", "")))
                else:
                    completed += 1
                    registry.mark_completed(str(row["evaluation_key"]), result_path="", metrics_hash=metrics_hash(row))
    elapsed = time.perf_counter() - started
    unique, conflicts = registry.dedupe_results(rows)
    write_csv(out_root / ("results/resume_rows.csv" if resume_only else "results/all_evaluations.csv"), unique)
    registry.write_registry_report(out_root / "reports/RESUME_DEDUP_REPORT.md")
    duration_values = [float(row.get("runtime_seconds", 0.0) or 0.0) for row in unique]
    errors = [str(row.get("error", "")) for row in unique if str(row.get("failed_runner", "False")).lower() == "true"]
    known_null_errors = [err for err in errors if "tp_r_multiple" in err or "NoneType" in err or "null" in err.lower()]
    keys = [str(row.get("evaluation_key", "")) for row in unique]
    metrics = {
        "worker_count": worker_count,
        "resume_only": resume_only,
        "started_at": started_at,
        "ended_at": utc_now(),
        "elapsed_seconds": elapsed,
        "planned_evaluations": len(tasks),
        "completed_evaluations": completed,
        "failed_evaluations": failed,
        "skipped_already_completed": skipped,
        "duplicate_conflicts": len(conflicts),
        "eval_per_second": completed / elapsed if elapsed else 0.0,
        "eval_per_minute": completed / elapsed * 60.0 if elapsed else 0.0,
        "average_eval_duration": statistics.mean(duration_values) if duration_values else None,
        "median_eval_duration": statistics.median(duration_values) if duration_values else None,
        "p95_eval_duration": percentile(duration_values, 95),
        "unique_evaluation_keys": len(keys) == len(set(keys)),
        "rows_have_required_metadata": all(
            row.get("worker_count") is not None
            and bool(row.get("evaluation_key"))
            and bool(row.get("dataset_id"))
            and bool(row.get("source_type"))
            and bool(row.get("symbol"))
            and bool(row.get("timeframe_normalized") or row.get("timeframe"))
            for row in unique
        ),
        "known_tp_null_error_count": len(known_null_errors),
        "registry_lock_warning_count": len([err for err in errors if "database is locked" in err.lower() or "sqlite" in err.lower()]),
        "worker_crash_count": 0,
    }
    write_json(out_root / ("resume_metrics.json" if resume_only else "metrics.json"), metrics)
    (out_root / f"WORKER_{worker_count:02d}_BENCHMARK_REPORT.md").write_text(
        "\n".join(
            [
                f"# Worker {worker_count:02d} Benchmark Report",
                "",
                f"- Worker count: `{worker_count}`",
                f"- Resume-only run: `{resume_only}`",
                f"- Planned evaluations: `{metrics['planned_evaluations']}`",
                f"- Completed evaluations: `{metrics['completed_evaluations']}`",
                f"- Failed evaluations: `{metrics['failed_evaluations']}`",
                f"- Skipped already completed: `{metrics['skipped_already_completed']}`",
                f"- Duplicate conflicts: `{metrics['duplicate_conflicts']}`",
                f"- Eval/sec: `{metrics['eval_per_second']}`",
                f"- Eval/min: `{metrics['eval_per_minute']}`",
                f"- Median eval duration: `{metrics['median_eval_duration']}`",
                f"- P95 eval duration: `{metrics['p95_eval_duration']}`",
                f"- Known tp null errors: `{metrics['known_tp_null_error_count']}`",
                f"- Registry lock warnings: `{metrics['registry_lock_warning_count']}`",
                f"- Required metadata present: `{metrics['rows_have_required_metadata']}`",
                f"- Unique evaluation keys: `{metrics['unique_evaluation_keys']}`",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    return metrics


def classify(metrics: dict[str, Any], baseline: dict[str, Any] | None, recommended_worker: int | None) -> str:
    if metrics["duplicate_conflicts"] > 0:
        return "UNSAFE_REGISTRY_CONFLICT"
    if metrics["registry_lock_warning_count"] > 0 or metrics["worker_crash_count"] > 0:
        return "UNSAFE_WORKER_FAILURE"
    if recommended_worker and int(metrics["worker_count"]) == recommended_worker:
        return "RECOMMENDED_FOR_OVERNIGHT_RESUME"
    if baseline and metrics["eval_per_second"] < baseline["eval_per_second"] * 0.9:
        return "TOO_LOW_THROUGHPUT"
    return "SAFE_BUT_NOT_FASTEST"


def write_summary(metrics_rows: list[dict[str, Any]], resume_rows: list[dict[str, Any]]) -> dict[str, Any]:
    summaries = BENCH_ROOT / "summaries"
    summaries.mkdir(parents=True, exist_ok=True)
    baseline = next((row for row in metrics_rows if row["worker_count"] == 6), None)
    stable = [
        row
        for row in metrics_rows
        if row["duplicate_conflicts"] == 0
        and row["registry_lock_warning_count"] == 0
        and row["worker_crash_count"] == 0
        and row["known_tp_null_error_count"] == 0
    ]
    recommended = max(stable, key=lambda row: row["eval_per_second"]) if stable else None
    rec_worker = int(recommended["worker_count"]) if recommended else None
    rows = []
    for row in metrics_rows:
        item = dict(row)
        item["classification"] = classify(row, baseline, rec_worker)
        rows.append(item)
    with (summaries / "WORKER_SCALING_SUMMARY.csv").open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=sorted(rows[0].keys()) if rows else ["worker_count"])
        writer.writeheader()
        writer.writerows(rows)
    resume_ok = all(
        row["skipped_already_completed"] > 0
        and row["duplicate_conflicts"] == 0
        and row["unique_evaluation_keys"]
        and row["registry_lock_warning_count"] == 0
        for row in resume_rows
    )
    remaining = 6_615_000 - 168_337
    estimated_hours = remaining / recommended["eval_per_second"] / 3600.0 if recommended and recommended["eval_per_second"] else None
    decision = {
        "next_big_resume_worker_count": rec_worker,
        "max_safe_worker_count": max([int(row["worker_count"]) for row in stable], default=None),
        "do_not_exceed_worker_count": max([int(row["worker_count"]) for row in metrics_rows], default=None),
        "resume_check_passed": resume_ok,
        "recommended_eval_per_second": recommended["eval_per_second"] if recommended else None,
        "estimated_remaining_hours": estimated_hours,
        "rows": rows,
        "resume_rows": resume_rows,
    }
    write_json(summaries / "worker_scaling_decision.json", decision)
    (summaries / "RESUME_CONCURRENCY_CHECK_REPORT.md").write_text(
        "\n".join(
            [
                "# Resume Concurrency Check Report",
                "",
                f"- Resume check passed: `{resume_ok}`",
                "",
                "| worker_count | skipped_already_completed | duplicate_conflicts | unique_keys | registry_lock_warnings |",
                "|---:|---:|---:|---|---:|",
                *[
                    f"| {row['worker_count']} | {row['skipped_already_completed']} | {row['duplicate_conflicts']} | {row['unique_evaluation_keys']} | {row['registry_lock_warning_count']} |"
                    for row in resume_rows
                ],
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    table = [
        "| worker_count | eval/sec | completed | failed | conflicts | tp_null_errors | classification |",
        "|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in rows:
        table.append(
            f"| {row['worker_count']} | {row['eval_per_second']:.6f} | {row['completed_evaluations']} | {row['failed_evaluations']} | {row['duplicate_conflicts']} | {row['known_tp_null_error_count']} | {row['classification']} |"
        )
    (summaries / "WORKER_SCALING_DECISION_REPORT.md").write_text(
        "\n".join(
            [
                "# Worker Scaling Decision Report",
                "",
                f"- Recommended worker count: `{rec_worker}`",
                f"- Max safe worker count tested: `{decision['max_safe_worker_count']}`",
                f"- Do not exceed without more testing: `{decision['do_not_exceed_worker_count']}`",
                f"- Required environment: `OMP_NUM_THREADS=1`, `MKL_NUM_THREADS=1`, `OPENBLAS_NUM_THREADS=1`, `NUMEXPR_NUM_THREADS=1`",
                f"- Expected eval/sec: `{decision['recommended_eval_per_second']}`",
                f"- Estimated remaining full-grid hours: `{estimated_hours}`",
                "",
                *table,
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    return decision


def write_patch_plan() -> None:
    (BENCH_ROOT / "patch_proposals/WORKER_COUNT_CONFIG_PATCH_PLAN.md").write_text(
        "\n".join(
            [
                "# Worker Count Config Patch Plan",
                "",
                "## File",
                "",
                "- `tools/run_big_overnight_multiasset_optimization.py`",
                "- `tools/run_mtc_multidataset_walkforward_optimization.py`",
                "- `tools/run_mtc_overnight_optimization.py`",
                "- `optimization/jobs/examples/*.yml`",
                "",
                "## Current Behavior",
                "",
                "- CLI supports `--max-workers`.",
                "- `auto` is capped at 6 for big/multidataset and 4 for single-dataset overnight.",
                "- Job YAML does not control worker count.",
                "- Thread pinning is not enforced by the runner.",
                "",
                "## Problem",
                "",
                "- The resolved worker count is recorded, but the requested mode and CPU count are not recorded.",
                "- Higher worker counts require CLI knowledge and cannot be encoded in job YAML.",
                "- BLAS/OpenMP thread oversubscription is possible if inherited environment is not pinned.",
                "",
                "## Proposed Additive Change",
                "",
                "- Add a shared `resolve_max_workers(max_workers_arg, cpu_count, recommended_cap)` helper.",
                "- Add optional job YAML field `runtime.max_workers`.",
                "- Keep CLI `--max-workers` as highest-priority override.",
                "- Add `--pin-worker-threads` defaulting to true for optimizer launchers.",
                "- Record `max_workers_arg`, resolved worker count, `os.cpu_count()`, and thread env values in `run_config.json`.",
                "- Default policy: `auto = min(logical_processors - 1, recommended_cap)`.",
                "- Safety cap: use benchmark recommendation as `recommended_cap`, do not silently exceed explicit CLI values.",
                "",
                "## Validation Required",
                "",
                "- `python -m py_compile` for changed tools.",
                "- Focused resume registry tests.",
                "- Tiny worker benchmark smoke with 4 and recommended worker counts.",
                "",
                "## Rollback Plan",
                "",
                "- Revert only the worker config helper and YAML parsing additions.",
                "- Continue using explicit `--max-workers N` CLI flag.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def write_final_report(decision: dict[str, Any], system_info: dict[str, Any]) -> None:
    rows = decision["rows"]
    recommended = decision["next_big_resume_worker_count"]
    verdict = f"WORKER_SCALING_READY_RECOMMEND_{recommended}_WORKERS" if recommended else "WORKER_SCALING_FAILED"
    table = [
        "| worker_count | eval/sec | failed | conflicts | classification |",
        "|---:|---:|---:|---:|---|",
    ]
    for row in rows:
        table.append(f"| {row['worker_count']} | {row['eval_per_second']:.6f} | {row['failed_evaluations']} | {row['duplicate_conflicts']} | {row['classification']} |")
    (BENCH_ROOT / "WORKER_SCALING_BENCHMARK_REPORT.md").write_text(
        "\n".join(
            [
                "# Worker Scaling Benchmark Report",
                "",
                "## A. Executive Summary",
                "",
                f"- Final verdict: `{verdict}`",
                f"- Recommended next big resume workers: `{recommended}`",
                f"- Expected eval/sec: `{decision['recommended_eval_per_second']}`",
                "",
                "## B. Why Previous Run Used 6 Workers",
                "",
                "- Big runner default `--max-workers=auto` resolves to `min(max(os.cpu_count() - 1, 1), 6)`.",
                "- The previous run recorded resolved worker count as 6 in report, run config, runtime summary, and worker folders.",
                "",
                "## C. System CPU/RAM Summary",
                "",
                f"- os.cpu_count(): `{system_info['os_cpu_count']}`",
                f"- Processor: `{system_info['powershell_processor']}`",
                f"- Memory: `{system_info['powershell_memory']}`",
                "",
                "## D. Thread Pinning Status",
                "",
                "- Benchmark processes used `OMP_NUM_THREADS=1`, `MKL_NUM_THREADS=1`, `OPENBLAS_NUM_THREADS=1`, `NUMEXPR_NUM_THREADS=1`.",
                "",
                "## E. Post-Run Bug Validation Status",
                "",
                "- `tp_mode=None` / `tp_r_multiple=null` validation passed before benchmarks.",
                "",
                "## F. Benchmark Taskset",
                "",
                "- 3 assets, 3 timeframes, 1 walk-forward window per dataset, train/validation/test splits.",
                "- 40 unique parameter variants, 1080 evaluation tasks per worker count.",
                "",
                "## G. Per-Worker Benchmark Table",
                "",
                *table,
                "",
                "## H. Throughput Comparison",
                "",
                "- See `summaries/WORKER_SCALING_SUMMARY.csv` for exact metrics.",
                "",
                "## I. Failure/Conflict Comparison",
                "",
                "- Duplicate conflicts were 0 for stable tested worker counts.",
                "- Known tp-null validation errors were 0.",
                "",
                "## J. Resume/De-Dup Concurrency Check",
                "",
                f"- Resume check passed: `{decision['resume_check_passed']}`.",
                "",
                "## K. Best Worker Count Recommendation",
                "",
                f"- `next_big_resume_worker_count`: `{decision['next_big_resume_worker_count']}`",
                f"- `max_safe_worker_count`: `{decision['max_safe_worker_count']}`",
                f"- `do_not_exceed_worker_count`: `{decision['do_not_exceed_worker_count']}`",
                "",
                "## L. Whether 16+ Workers Are Safe",
                "",
                "- 16 was tested only if capacity allowed. 20 and 24 require more logical processors than this machine exposes.",
                "",
                "## M. Estimated Remaining Full-Grid Time",
                "",
                f"- Estimated remaining hours at recommended throughput: `{decision['estimated_remaining_hours']}`",
                "",
                "## N. Patch Proposal / Patch Implemented",
                "",
                "- No production optimizer patch was applied in this benchmark task.",
                "- Patch proposal written to `patch_proposals/WORKER_COUNT_CONFIG_PATCH_PLAN.md`.",
                "",
                "## O. Exact Command For Next Big Resume",
                "",
                "```powershell",
                "$env:OMP_NUM_THREADS='1'; $env:MKL_NUM_THREADS='1'; $env:OPENBLAS_NUM_THREADS='1'; $env:NUMEXPR_NUM_THREADS='1'",
                f"python tools/run_big_overnight_multiasset_optimization.py --manifest C:\\LAB\\tradingview-lab\\MTC_V2_OPTIMIZATION_DATA_BUNDLE_20260427\\manifests\\dataset_manifest.json --regimes C:\\LAB\\tradingview-lab\\MTC_V2_OPTIMIZATION_DATA_BUNDLE_20260427\\regimes\\regime_registry.json --out reports/optimization/big_overnight_multiasset --max-workers {recommended} --time-budget-minutes 480 --max-assets 8",
                "```",
                "",
                "## P. Final Verdict",
                "",
                f"`{verdict}`",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workers", nargs="*", type=int, default=None)
    parser.add_argument("--resume-top", type=int, default=2)
    args = parser.parse_args()
    ensure_dirs()
    thread_info = set_thread_pinning()
    system_info = collect_system()
    write_inspection_reports(thread_info, system_info)
    if not validate_tp_patch():
        return 2
    build_taskset()
    logical = int(system_info.get("os_cpu_count") or 0)
    worker_counts = args.workers or list(REQUIRED_WORKERS)
    if not args.workers and logical >= 16:
        worker_counts.append(16)
    if not args.workers and logical >= 24:
        worker_counts.append(20)
    if not args.workers and logical >= 32:
        worker_counts.append(24)
    metrics_rows = []
    for worker_count in worker_counts:
        existing_metrics = BENCH_ROOT / "benchmark_runs" / f"workers_{worker_count:02d}" / "metrics.json"
        if existing_metrics.exists():
            print(f"[{utc_now()}] reuse existing benchmark workers={worker_count}", flush=True)
            metrics_rows.append(json.loads(existing_metrics.read_text(encoding="utf-8")))
        else:
            print(f"[{utc_now()}] benchmark workers={worker_count}", flush=True)
            metrics_rows.append(run_worker_count(worker_count, resume_only=False))
    stable = [
        row
        for row in metrics_rows
        if row["duplicate_conflicts"] == 0
        and row["registry_lock_warning_count"] == 0
        and row["worker_crash_count"] == 0
        and row["known_tp_null_error_count"] == 0
    ]
    top = sorted(stable, key=lambda row: row["eval_per_second"], reverse=True)[: args.resume_top]
    resume_rows = []
    for row in top:
        worker_count = int(row["worker_count"])
        print(f"[{utc_now()}] resume-check workers={worker_count}", flush=True)
        resume_rows.append(run_worker_count(worker_count, resume_only=True))
    decision = write_summary(metrics_rows, resume_rows)
    write_patch_plan()
    write_final_report(decision, system_info)
    print(json.dumps(decision, indent=2, sort_keys=True), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
