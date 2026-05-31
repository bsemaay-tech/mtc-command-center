from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path
from typing import Any

from tools.build_per_asset_timeframe_seed_rankings import build_seed_rankings, write_csv as write_seed_csv
from tools.run_big_overnight_multiasset_optimization import (
    ALLOWED_SOURCE_TYPES,
    create_walkforward,
    iter_tasks,
    load_manifest,
    load_regime_registry,
    normalized_dataset_entry,
    run_one,
    write_csv,
    write_json,
)


RESEARCH_WARNING = "Research seed only; not Pine default; not production parameter."


def build_producer_only_variants() -> list[dict[str, Any]]:
    variants: list[dict[str, Any]] = []
    for st_factor in [2.5, 3.0, 3.5, 4.0, 4.5]:
        for global_atr_length in [7, 10, 14, 21]:
            variants.append(
                {
                    "signal_mode": "Supertrend",
                    "st_factor": st_factor,
                    "global_atr_length": global_atr_length,
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
            )
    return variants


def bundle_root_from_manifest(path: Path) -> Path:
    return path.parent.parent if path.parent.name == "manifests" else path.parent


def select_smoke_datasets(manifest_path: Path, regime_path: Path, symbols: list[str], timeframes: list[str]) -> list[dict[str, Any]]:
    bundle_root = bundle_root_from_manifest(manifest_path)
    manifest = load_manifest(manifest_path)
    regimes = load_regime_registry(regime_path)
    selected: list[dict[str, Any]] = []
    for raw in manifest:
        item = normalized_dataset_entry(raw, bundle_root)
        if str(item.get("symbol")) not in symbols:
            continue
        if str(item.get("timeframe_normalized")) not in timeframes:
            continue
        if item.get("source_type") not in ALLOWED_SOURCE_TYPES:
            continue
        if str(item.get("ohlcv_validation_status", "PASS")).upper() != "PASS":
            continue
        if not Path(str(item["source_path"])).exists():
            continue
        if not item.get("sha256"):
            continue
        regime = regimes.get(str(item.get("dataset_id")), {})
        if not regime:
            continue
        regime_file = Path(str(regime.get("regime_file", "")))
        if regime_file and not regime_file.is_absolute():
            regime_file = bundle_root / regime_file
        item["regime_file_abs"] = str(regime_file)
        selected.append(item)
    selected.sort(key=lambda item: (symbols.index(str(item["symbol"])), timeframes.index(str(item["timeframe_normalized"]))))
    return selected


def run_smoke(args: argparse.Namespace) -> int:
    out_root = Path(args.out)
    for subdir in ["ranked", "reports", "results", "workers", "walkforward", "datasets", "logs"]:
        (out_root / subdir).mkdir(parents=True, exist_ok=True)

    os.environ["OMP_NUM_THREADS"] = "1"
    os.environ["MKL_NUM_THREADS"] = "1"
    os.environ["OPENBLAS_NUM_THREADS"] = "1"
    os.environ["NUMEXPR_NUM_THREADS"] = "1"

    selected = select_smoke_datasets(
        Path(args.manifest),
        Path(args.regimes),
        symbols=[symbol.strip() for symbol in args.symbols.split(",") if symbol.strip()],
        timeframes=[timeframe.strip() for timeframe in args.timeframes.split(",") if timeframe.strip()],
    )
    variants = build_producer_only_variants()[: args.max_variants]
    splits = create_walkforward(selected, out_root)
    first_window_splits = [split for split in splits if str(split.get("window_id", "")).endswith("_wf1")]
    tasks = list(iter_tasks(variants, first_window_splits, out_root, worker_count=args.max_workers))
    if len(tasks) > args.max_evaluations:
        tasks = tasks[: args.max_evaluations]

    write_json(
        out_root / "seed_granularity_smoke_config.json",
        {
            "purpose": "producer-only per-asset/timeframe seed granularity smoke",
            "warning": RESEARCH_WARNING,
            "manifest": args.manifest,
            "regimes": args.regimes,
            "symbols": args.symbols,
            "timeframes": args.timeframes,
            "selected_dataset_count": len(selected),
            "variant_count": len(variants),
            "planned_evaluations": len(tasks),
            "max_workers": args.max_workers,
            "thread_pinning": {
                "OMP_NUM_THREADS": os.environ.get("OMP_NUM_THREADS"),
                "MKL_NUM_THREADS": os.environ.get("MKL_NUM_THREADS"),
                "OPENBLAS_NUM_THREADS": os.environ.get("OPENBLAS_NUM_THREADS"),
                "NUMEXPR_NUM_THREADS": os.environ.get("NUMEXPR_NUM_THREADS"),
            },
        },
    )

    started = time.time()
    rows: list[dict[str, Any]] = []
    if args.max_workers <= 1:
        for task in tasks:
            row = run_one(task)
            row["seed_granularity_smoke"] = True
            rows.append(row)
    else:
        with ProcessPoolExecutor(max_workers=args.max_workers) as pool:
            futures = [pool.submit(run_one, task) for task in tasks]
            for future in as_completed(futures):
                row = future.result()
                row["seed_granularity_smoke"] = True
                rows.append(row)
    rows.sort(key=lambda row: str(row.get("evaluation_key", "")))
    write_csv(out_root / "ranked/all_evaluations.csv", rows)
    write_csv(out_root / "results/all_evaluations.csv", rows)

    duplicate_conflicts = len(rows) - len({str(row.get("evaluation_key", "")) for row in rows})
    failed = len([row for row in rows if str(row.get("failed_runner", "False")).lower() == "true"])
    seed_candidates, summary_rows = build_seed_rankings(
        rows,
        source_run_id="seed_granularity_smoke_v1",
        source_output_path=str(out_root / "ranked/all_evaluations.csv"),
        top_n=args.top_n,
    )
    write_seed_csv(out_root / "ranked/per_asset_timeframe_seed_candidates.csv", seed_candidates)
    write_seed_csv(out_root / "ranked/per_asset_timeframe_summary.csv", summary_rows)
    (out_root / "ranked/per_asset_timeframe_seed_candidates.json").write_text(
        json.dumps(seed_candidates, indent=2, sort_keys=True, default=str),
        encoding="utf-8",
    )

    report_lines = [
        "# Seed Granularity Smoke Report",
        "",
        RESEARCH_WARNING,
        "",
        f"- Selected datasets: `{len(selected)}`",
        f"- Variants: `{len(variants)}`",
        f"- Completed evaluations: `{len(rows)}`",
        f"- Failed evaluations: `{failed}`",
        f"- Duplicate conflicts: `{duplicate_conflicts}`",
        f"- Granular seed rows: `{len(seed_candidates)}`",
        f"- Asset/timeframe groups: `{len(summary_rows)}`",
        f"- Runtime seconds: `{round(time.time() - started, 3)}`",
        "",
        "## Selected Datasets",
        "",
    ]
    for item in selected:
        report_lines.append(f"- `{item['symbol']}` `{item['timeframe_normalized']}` `{item['dataset_id']}` `{item.get('source_type')}`")
    (out_root / "reports/SEED_GRANULARITY_SMOKE_REPORT.md").write_text("\n".join(report_lines) + "\n", encoding="utf-8")

    return 0 if failed == 0 and duplicate_conflicts == 0 and len(seed_candidates) > 0 else 1


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--regimes", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--symbols", default="BTCUSDT,ETHUSDT")
    parser.add_argument("--timeframes", default="15m,1h,4h")
    parser.add_argument("--max-variants", type=int, default=20)
    parser.add_argument("--max-evaluations", type=int, default=360)
    parser.add_argument("--max-workers", type=int, default=4)
    parser.add_argument("--top-n", type=int, default=5)
    args = parser.parse_args()
    if args.max_variants < 20 or args.max_variants > 60:
        raise SystemExit("--max-variants must be between 20 and 60")
    if args.max_evaluations > 500:
        raise SystemExit("--max-evaluations must be <= 500")
    return run_smoke(args)


if __name__ == "__main__":
    raise SystemExit(main())
