from __future__ import annotations

import argparse
import csv
import json
import os
import time
from concurrent.futures import FIRST_COMPLETED, ProcessPoolExecutor, wait
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from tools.optimization_resume_registry import ResumeRegistry, metrics_hash
from tools.run_big_overnight_multiasset_optimization import (
    bundle_root_from_manifest,
    checkpoint,
    create_walkforward,
    generate_variants,
    iter_tasks,
    load_manifest,
    load_regime_registry,
    run_one,
    select_datasets,
    write_csv,
    write_json,
    write_parameter_grid,
)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def append_heartbeat(path: Path, message: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(f"{utc_now()} {message}\n")


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def choose_smoke_tasks(manifest_path: Path, regimes_path: Path, out_root: Path, max_workers: int, max_evaluations: int) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    manifest = load_manifest(manifest_path)
    regimes = load_regime_registry(regimes_path)
    bundle_root = bundle_root_from_manifest(manifest_path)
    selected, selection_summary = select_datasets(manifest, regimes, bundle_root, out_root, max_assets=2)

    for item in selected:
        regime = regimes.get(str(item["dataset_id"]), {})
        regime_file = Path(str(regime.get("regime_file", "")))
        if regime_file and not regime_file.is_absolute():
            regime_file = bundle_root / regime_file
        item["regime_file_abs"] = str(regime_file)

    splits = create_walkforward(selected, out_root)
    first_window_splits = [split for split in splits if str(split.get("window_id", "")).endswith("_wf1")]
    variants = generate_variants()[:2]
    write_parameter_grid(out_root, variants)
    tasks = list(iter_tasks(variants, first_window_splits, out_root, worker_count=max_workers))[:max_evaluations]
    return tasks, {
        "selected_dataset_count": len(selected),
        "selected_datasets": [
            {
                "dataset_id": item.get("dataset_id"),
                "symbol": item.get("symbol"),
                "timeframe": item.get("timeframe_normalized"),
                "source_type": item.get("source_type"),
            }
            for item in selected
        ],
        "selection_summary": selection_summary,
        "split_count": len(splits),
        "first_window_split_count": len(first_window_splits),
        "variant_count": len(variants),
        "planned_smoke_evaluations": len(tasks),
    }


def run_smoke(args: argparse.Namespace) -> int:
    out_root = Path(args.out).resolve()
    out_root.mkdir(parents=True, exist_ok=True)
    for subdir in ["workers", "results", "ranked", "logs", "reports", "checkpoints", "walkforward", "datasets"]:
        (out_root / subdir).mkdir(parents=True, exist_ok=True)

    heartbeat_path = out_root / "heartbeat.log"
    status_path = out_root / "run_status.json"
    registry = ResumeRegistry(out_root / "resume_registry.sqlite")

    write_json(
        status_path,
        {
            "status": "running",
            "started_at": utc_now(),
            "pid": os.getpid(),
            "out_root": str(out_root),
            "manifest": str(args.manifest),
            "regimes": str(args.regimes),
            "max_workers": args.max_workers,
            "max_evaluations": args.max_evaluations,
            "thread_env": {
                "OMP_NUM_THREADS": os.environ.get("OMP_NUM_THREADS"),
                "MKL_NUM_THREADS": os.environ.get("MKL_NUM_THREADS"),
                "OPENBLAS_NUM_THREADS": os.environ.get("OPENBLAS_NUM_THREADS"),
                "NUMEXPR_NUM_THREADS": os.environ.get("NUMEXPR_NUM_THREADS"),
            },
        },
    )
    append_heartbeat(heartbeat_path, f"started pid={os.getpid()}")

    tasks, task_summary = choose_smoke_tasks(Path(args.manifest), Path(args.regimes), out_root, args.max_workers, args.max_evaluations)
    write_json(out_root / "smoke_taskset.json", {"created_at": utc_now(), **task_summary, "tasks": tasks})

    completed_rows: list[dict[str, Any]] = []
    failed = 0
    skipped = 0
    started = time.time()
    pending = {}
    task_iter = iter(tasks)

    with ProcessPoolExecutor(max_workers=args.max_workers) as pool:
        while True:
            while len(pending) < args.max_workers:
                try:
                    task = next(task_iter)
                except StopIteration:
                    break
                pending[pool.submit(run_one, task)] = task

            if not pending:
                break

            done, _not_done = wait(pending, timeout=1.0, return_when=FIRST_COMPLETED)
            if not done:
                append_heartbeat(heartbeat_path, f"running completed={len(completed_rows)} pending={len(pending)}")
                continue

            for future in done:
                task = pending.pop(future)
                row = future.result()
                row["smoke_run_id"] = "detached_resume_smoke"
                row["worker_count"] = args.max_workers
                completed_rows.append(row)
                if row.get("failed_runner"):
                    failed += 1
                    registry.mark_failed(str(row["evaluation_key"]), str(row.get("error", "")))
                else:
                    registry.mark_completed(str(row["evaluation_key"]), result_path="", metrics_hash=metrics_hash(row))
                append_heartbeat(heartbeat_path, f"completed={len(completed_rows)} failed={failed} pending={len(pending)}")

    unique_rows, conflicts = registry.dedupe_results(completed_rows)
    rows_have_required_metadata = all(row.get("dataset_id") and row.get("source_type") and row.get("evaluation_key") for row in completed_rows)
    unique_evaluation_keys = len({str(row.get("evaluation_key")) for row in completed_rows}) == len(completed_rows)
    elapsed = time.time() - started

    write_csv(out_root / "results/smoke_evaluations.csv", unique_rows)
    write_csv(out_root / "ranked/all_evaluations.csv", unique_rows)
    checkpoint(
        out_root,
        {
            "planned": len(tasks),
            "completed": len(completed_rows),
            "failed": failed,
            "skipped_already_completed": skipped,
            "duplicate_conflicts": len(conflicts),
        },
    )
    registry.write_registry_report(out_root / "reports/RESUME_DEDUP_REPORT.md")

    metrics = {
        "status": "completed",
        "started_at": datetime.fromtimestamp(started, timezone.utc).isoformat(),
        "ended_at": utc_now(),
        "elapsed_seconds": elapsed,
        "pid": os.getpid(),
        "planned_evaluations": len(tasks),
        "completed_evaluations": len(completed_rows),
        "failed_evaluations": failed,
        "skipped_already_completed": skipped,
        "duplicate_conflicts": len(conflicts),
        "rows_have_required_metadata": rows_have_required_metadata,
        "unique_evaluation_keys": unique_evaluation_keys,
        "output_rows_path": str(out_root / "results/smoke_evaluations.csv"),
        "heartbeat_path": str(heartbeat_path),
        "thread_env": {
            "OMP_NUM_THREADS": os.environ.get("OMP_NUM_THREADS"),
            "MKL_NUM_THREADS": os.environ.get("MKL_NUM_THREADS"),
            "OPENBLAS_NUM_THREADS": os.environ.get("OPENBLAS_NUM_THREADS"),
            "NUMEXPR_NUM_THREADS": os.environ.get("NUMEXPR_NUM_THREADS"),
        },
        **task_summary,
    }
    write_json(out_root / "metrics.json", metrics)
    write_json(status_path, metrics)
    append_heartbeat(heartbeat_path, f"completed evaluations={len(completed_rows)} failed={failed} conflicts={len(conflicts)}")

    for index in range(args.post_run_heartbeats):
        append_heartbeat(heartbeat_path, f"post_run_alive index={index + 1}")
        time.sleep(args.heartbeat_interval_seconds)

    return 0 if failed == 0 and len(conflicts) == 0 and rows_have_required_metadata and unique_evaluation_keys else 1


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--regimes", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--max-workers", type=int, default=2)
    parser.add_argument("--max-evaluations", type=int, default=12)
    parser.add_argument("--post-run-heartbeats", type=int, default=6)
    parser.add_argument("--heartbeat-interval-seconds", type=float, default=2.0)
    args = parser.parse_args()
    if not 5 <= args.max_evaluations <= 20:
        raise SystemExit("--max-evaluations must be between 5 and 20")
    return args


if __name__ == "__main__":
    raise SystemExit(run_smoke(parse_args()))
