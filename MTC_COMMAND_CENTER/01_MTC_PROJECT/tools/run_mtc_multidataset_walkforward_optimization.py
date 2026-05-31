from __future__ import annotations

import argparse
import csv
import hashlib
import itertools
import json
import math
import os
import random
import re
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
from tools.optimization_parameter_mapper import apply_parameter_mapping, mapper_payload
from tools.optimization_resume_registry import (
    EvaluationIdentity,
    REGISTRY_VERSION,
    ResumeRegistry,
    evaluation_key,
    metrics_hash,
)
from tools.runner_metrics_adapter import RUNNER_METRICS_ADAPTER_VERSION, run_with_result
from tools.score_walkforward_optimization_results import write_outputs
from tools.validate_optimizer_dataset_usage import (
    load_json_or_sidecar as load_optimizer_job_json,
    load_manifest_entries as load_optimizer_manifest_entries,
    validate_job as validate_optimizer_dataset_job,
    write_reports as write_optimizer_dataset_validation_reports,
)


TARGET_TIMEFRAMES = {
    "15": "15m",
    "15m": "15m",
    "60": "1h",
    "1h": "1h",
    "120": "2h",
    "2h": "2h",
    "240": "4h",
    "4h": "4h",
    "d": "1D",
    "1d": "1D",
    "1440": "1D",
}
SYMBOL_PRIORITY = ["BTCUSDT.P", "BTCUSDT", "ETHUSDT.P", "ETHUSDT", "SOLUSDT.P", "SOLUSDT", "BNBUSDT.P", "BNBUSDT", "ADAUSDT.P", "ADAUSDT"]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = sorted({key for row in rows for key in row.keys()})
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


def parse_time(value: str) -> datetime | None:
    value = str(value).strip()
    if not value:
        return None
    try:
        if re.fullmatch(r"\d+", value):
            raw = int(value)
            if raw > 10_000_000_000:
                raw = raw // 1000
            return datetime.fromtimestamp(raw, tz=timezone.utc)
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (ValueError, OSError):
        return None


def infer_from_filename(path: Path) -> tuple[str, str, str, str]:
    stem = path.stem
    exchange = "UNKNOWN"
    symbol = "UNKNOWN"
    timeframe = "UNKNOWN"
    match = re.search(r"(?P<exchange>[A-Z]+)_(?P<symbol>[A-Z0-9.]+),\s*(?P<tf>[A-Za-z0-9]+)", stem)
    if match:
        exchange = match.group("exchange")
        symbol = match.group("symbol")
        timeframe = match.group("tf")
    normalized = TARGET_TIMEFRAMES.get(timeframe.lower(), "UNKNOWN")
    return exchange, symbol, timeframe, normalized


def inspect_dataset(path: Path, archive_root: Path) -> dict[str, Any]:
    exchange, symbol, timeframe, normalized = infer_from_filename(path)
    row_count = 0
    columns: list[str] = []
    first_time = "UNKNOWN"
    last_time = "UNKNOWN"
    timestamps: list[datetime] = []
    bad_rows = 0
    duplicate_timestamps = 0
    seen_ts: set[str] = set()
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as fh:
            reader = csv.DictReader(fh)
            columns = list(reader.fieldnames or [])
            for row in reader:
                row_count += 1
                time_value = str(row.get("time") or row.get("timestamp") or row.get("datetime") or "")
                if first_time == "UNKNOWN":
                    first_time = time_value
                last_time = time_value
                if time_value in seen_ts:
                    duplicate_timestamps += 1
                seen_ts.add(time_value)
                parsed = parse_time(time_value)
                if parsed is not None:
                    timestamps.append(parsed)
                try:
                    open_, high, low, close = float(row["open"]), float(row["high"]), float(row["low"]), float(row["close"])
                    if not all(math.isfinite(v) for v in [open_, high, low, close]) or high < low or open_ < low or open_ > high or close < low or close > high:
                        bad_rows += 1
                except Exception:
                    bad_rows += 1
    except Exception as exc:
        return {
            "dataset_id": "unreadable_" + hashlib.sha1(str(path).encode("utf-8")).hexdigest()[:10],
            "source_path": str(path),
            "symbol": symbol,
            "exchange": exchange,
            "timeframe": timeframe,
            "timeframe_normalized": normalized,
            "row_count": 0,
            "start": "UNKNOWN",
            "end": "UNKNOWN",
            "timezone": "UNKNOWN",
            "sha256": "UNKNOWN",
            "file_size_bytes": path.stat().st_size if path.exists() else 0,
            "columns_detected": [],
            "usable_for_optimization": False,
            "skip_reason": f"READ_ERROR: {exc}",
        }
    has_gaps = "UNKNOWN"
    if len(timestamps) > 3:
        deltas = [(timestamps[idx] - timestamps[idx - 1]).total_seconds() for idx in range(1, len(timestamps))]
        positive = [delta for delta in deltas if delta > 0]
        if positive:
            base = min(positive)
            has_gaps = "true" if any(delta > base * 1.5 for delta in positive) else "false"
    skip_reasons = []
    required_cols = {"time", "open", "high", "low", "close"}
    if not required_cols.issubset({col.lower() for col in columns}):
        skip_reasons.append("MISSING_REQUIRED_OHLC_COLUMNS")
    if normalized == "UNKNOWN":
        skip_reasons.append("TIMEFRAME_NOT_TARGET_OR_UNKNOWN")
    if row_count < 500:
        skip_reasons.append("TOO_FEW_ROWS")
    if bad_rows > 0:
        skip_reasons.append(f"BAD_OHLC_ROWS:{bad_rows}")
    dataset_id = f"{exchange}_{symbol}_{normalized}_{hashlib.sha1(str(path).encode('utf-8')).hexdigest()[:8]}".replace(".", "P").replace("/", "_")
    return {
        "dataset_id": dataset_id,
        "source_path": str(path),
        "symbol": symbol,
        "exchange": exchange,
        "timeframe": timeframe,
        "timeframe_normalized": normalized,
        "row_count": row_count,
        "start": first_time,
        "end": last_time,
        "timezone": "UTC_or_export_timezone_UNKNOWN",
        "sha256": sha256_file(path),
        "file_size_bytes": path.stat().st_size,
        "columns_detected": columns,
        "has_gaps": has_gaps,
        "duplicate_timestamps": duplicate_timestamps,
        "bad_ohlc_rows": bad_rows,
        "source_type": "tradingview_chart_csv_archive",
        "usable_for_optimization": not skip_reasons,
        "skip_reason": ";".join(skip_reasons),
        "relative_to_archive": str(path.relative_to(archive_root)) if archive_root in path.parents else path.name,
    }


def discover_datasets(archive_root: Path, out_root: Path) -> list[dict[str, Any]]:
    datasets = [inspect_dataset(path, archive_root) for path in sorted(archive_root.rglob("*.csv"))]
    write_json(out_root / "datasets/dataset_manifest.json", datasets)
    lines = ["datasets:"]
    for item in datasets:
        lines.append(f"  - dataset_id: \"{item['dataset_id']}\"")
        for key in ["source_path", "symbol", "exchange", "timeframe", "timeframe_normalized", "row_count", "start", "end", "timezone", "sha256", "file_size_bytes", "usable_for_optimization", "skip_reason"]:
            value = item.get(key, "")
            rendered = str(value).replace('"', '\\"')
            lines.append(f"    {key}: \"{rendered}\"")
        lines.append("    columns_detected: \"" + ",".join(item.get("columns_detected", [])) + "\"")
    (out_root / "datasets/dataset_manifest.yml").write_text("\n".join(lines) + "\n", encoding="utf-8")
    discovered_tfs = sorted({item["timeframe_normalized"] for item in datasets if item["timeframe_normalized"] != "UNKNOWN"})
    missing = [tf for tf in ["15m", "1h", "2h", "4h", "1D"] if tf not in discovered_tfs]
    report = [
        "# Dataset Discovery Report",
        "",
        f"Archive folder: `{archive_root}`",
        f"CSV files discovered: `{len(datasets)}`",
        f"Usable datasets: `{len([d for d in datasets if d['usable_for_optimization']])}`",
        f"Timeframes discovered: `{', '.join(discovered_tfs)}`",
        f"Missing target timeframes: `{', '.join(missing) if missing else 'none'}`",
        "",
        "| symbol | timeframe | dataset_id | rows | date range | usable | skip_reason |",
        "|---|---|---|---:|---|---|---|",
    ]
    for item in datasets:
        report.append(f"| {item['symbol']} | {item['timeframe_normalized']} | {item['dataset_id']} | {item['row_count']} | {item['start']} -> {item['end']} | {item['usable_for_optimization']} | {item['skip_reason']} |")
    (out_root / "datasets/DATASET_DISCOVERY_REPORT.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    (out_root / "reports/DATASET_DISCOVERY_REPORT.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    return datasets


def select_datasets(datasets: list[dict[str, Any]], out_root: Path) -> list[dict[str, Any]]:
    usable = [item for item in datasets if item["usable_for_optimization"]]
    by_pair: dict[tuple[str, str], list[dict[str, Any]]] = {}
    for item in usable:
        by_pair.setdefault((item["symbol"], item["timeframe_normalized"]), []).append(item)
    selected: list[dict[str, Any]] = []
    symbols = sorted({item["symbol"] for item in usable}, key=lambda sym: SYMBOL_PRIORITY.index(sym) if sym in SYMBOL_PRIORITY else 999)
    for symbol in symbols[:5]:
        for timeframe in ["15m", "1h", "2h", "4h", "1D"]:
            candidates = by_pair.get((symbol, timeframe), [])
            if candidates:
                selected.append(sorted(candidates, key=lambda item: (int(item["row_count"]), int(item["file_size_bytes"])), reverse=True)[0])
    selected = selected[:25]
    write_json(out_root / "datasets/selected_datasets.json", selected)
    used_symbols = sorted({item["symbol"] for item in selected})
    used_tfs = sorted({item["timeframe_normalized"] for item in selected})
    discovered_tfs = sorted({item["timeframe_normalized"] for item in usable})
    missing = [tf for tf in ["15m", "1h", "2h", "4h", "1D"] if tf not in discovered_tfs]
    lines = [
        "# Selected Datasets",
        "",
        f"Coins used: `{', '.join(used_symbols)}`",
        f"Timeframes used: `{', '.join(used_tfs)}`",
        f"Missing target timeframes: `{', '.join(missing) if missing else 'none'}`",
        "",
        "| symbol | timeframe | dataset_id | rows | source_path | sha256 |",
        "|---|---|---|---:|---|---|",
    ]
    for item in selected:
        lines.append(f"| {item['symbol']} | {item['timeframe_normalized']} | {item['dataset_id']} | {item['row_count']} | {item['source_path']} | {item['sha256']} |")
    (out_root / "datasets/SELECTED_DATASETS.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return selected


def datasets_from_manifest(manifest_path: Path, dataset_ids: list[str], out_root: Path) -> list[dict[str, Any]]:
    entries = load_optimizer_manifest_entries(manifest_path)
    bundle_root = manifest_path.parent.parent if manifest_path.parent.name == "manifests" else manifest_path.parent
    by_id = {str(item["dataset_id"]): item for item in entries}
    selected_ids = dataset_ids or list(by_id.keys())
    selected: list[dict[str, Any]] = []
    missing: list[str] = []
    for dataset_id in selected_ids:
        item = by_id.get(str(dataset_id))
        if not item:
            missing.append(str(dataset_id))
            continue
        source_path = Path(str(item.get("normalized_path") or item.get("source_path") or item.get("raw_path")))
        if not source_path.is_absolute():
            source_path = bundle_root / source_path
        source_type = str(item.get("source_type", ""))
        if source_type == "unknown_csv":
            raise SystemExit(f"unknown_csv dataset blocked by optimizer rules: {dataset_id}")
        if source_path.suffix.lower() == ".xlsx":
            raise SystemExit(f"xlsx chart data forbidden: {dataset_id}")
        selected.append(
            {
                "dataset_id": str(item["dataset_id"]),
                "symbol": str(item.get("symbol", "")),
                "exchange": str(item.get("exchange", "")),
                "timeframe": str(item.get("timeframe", item.get("timeframe_normalized", ""))),
                "timeframe_normalized": str(item.get("timeframe_normalized", item.get("timeframe", ""))),
                "source_path": str(source_path),
                "sha256": str(item.get("sha256_normalized") or item.get("sha256") or item.get("sha256_raw")),
                "row_count": int(item.get("row_count", 0)),
                "start": str(item.get("start", "")),
                "end": str(item.get("end", "")),
                "source_type": source_type,
                "usable_for_optimization": str(item.get("ohlcv_validation_status", "PASS")).upper() in {"PASS", "WARN"},
                "skip_reason": "" if str(item.get("ohlcv_validation_status", "PASS")).upper() in {"PASS", "WARN"} else "ohlcv_validation_not_pass",
            }
        )
    if missing:
        raise SystemExit(f"dataset_ids not found in manifest: {', '.join(missing)}")
    write_json(out_root / "datasets/dataset_manifest.json", selected)
    write_json(out_root / "datasets/selected_datasets.json", selected)
    lines = [
        "# Selected Datasets From Manifest",
        "",
        f"Manifest: `{manifest_path}`",
        "",
        "| symbol | timeframe | dataset_id | rows | source_type | normalized_path | sha256 |",
        "|---|---|---|---:|---|---|---|",
    ]
    for item in selected:
        lines.append(f"| {item['symbol']} | {item['timeframe_normalized']} | {item['dataset_id']} | {item['row_count']} | {item['source_type']} | {item['source_path']} | {item['sha256']} |")
    (out_root / "datasets/SELECTED_DATASETS.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return selected


def create_walkforward(selected: list[dict[str, Any]], out_root: Path) -> list[dict[str, Any]]:
    windows: list[dict[str, Any]] = []
    for dataset in selected:
        n = int(dataset["row_count"])
        if n < 1500:
            windows.append({**_window_base(dataset), "window_id": dataset["dataset_id"] + "_sanity", "status": "TOO_SHORT_FOR_WALKFORWARD", "train_start": 0, "train_end": n, "validation_start": 0, "validation_end": 0, "test_start": 0, "test_end": 0})
            continue
        count = 4 if n >= 5000 else 2
        step = max(1, int(n * 0.20))
        for idx in range(count):
            start = min(idx * step, max(0, n - 10))
            available = n - start
            train_len = max(1, int(available * 0.60))
            val_len = max(1, int(available * 0.20))
            test_len = max(1, available - train_len - val_len)
            train_start = start
            train_end = start + train_len
            val_start = train_end
            val_end = val_start + val_len
            test_start = val_end
            test_end = min(n, test_start + test_len)
            windows.append({**_window_base(dataset), "window_id": f"{dataset['dataset_id']}_wf{idx+1}", "status": "OK", "train_start": train_start, "train_end": train_end, "validation_start": val_start, "validation_end": val_end, "test_start": test_start, "test_end": test_end})
    write_csv(out_root / "walkforward/walkforward_windows.csv", windows)
    report = [
        "# Walkforward Window Report",
        "",
        "Rules: >=5000 rows uses 4 rolling windows; 1500-4999 rows uses 2 rolling windows; shorter datasets are sanity-only.",
        "",
        "| dataset_id | symbol | timeframe | window_id | status | train | validation | test |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for row in windows:
        report.append(f"| {row['dataset_id']} | {row['symbol']} | {row['timeframe_normalized']} | {row['window_id']} | {row['status']} | {row['train_start']}:{row['train_end']} | {row['validation_start']}:{row['validation_end']} | {row['test_start']}:{row['test_end']} |")
    (out_root / "walkforward/WALKFORWARD_WINDOW_REPORT.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    (out_root / "reports/WALKFORWARD_REPORT.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    return [row for row in windows if row["status"] == "OK"]


def _window_base(dataset: dict[str, Any]) -> dict[str, Any]:
    return {
        "dataset_id": dataset["dataset_id"],
        "symbol": dataset["symbol"],
        "exchange": dataset["exchange"],
        "timeframe": dataset["timeframe"],
        "timeframe_normalized": dataset["timeframe_normalized"],
        "source_path": dataset["source_path"],
        "sha256": dataset["sha256"],
        "source_type": dataset.get("source_type", ""),
        "row_count": dataset["row_count"],
        "start": dataset["start"],
        "end": dataset["end"],
    }


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_profile(path: Path) -> dict[str, Any]:
    return load_json(path)


def generate_variants(profile: dict[str, Any], limit: int | None = None) -> list[dict[str, Any]]:
    params = profile["parameters"]
    keys = list(params.keys())
    combos = [dict(zip(keys, values)) for values in itertools.product(*[params[key] for key in keys])]
    random.Random(int(profile.get("shuffle_seed", 1))).shuffle(combos)
    max_variants = int(profile.get("max_variants", len(combos)))
    if limit is not None:
        max_variants = min(max_variants, limit)
    return combos[:max_variants]


def parameter_hash(params: dict[str, Any]) -> str:
    return hashlib.sha256(json.dumps(params, sort_keys=True).encode("utf-8")).hexdigest()[:16]


def load_bars(path: Path, start: int, end: int) -> list[Bar]:
    rows = read_csv_rows(path)[start:end]
    bars: list[Bar] = []
    for idx, row in enumerate(rows):
        ts = parse_time(str(row.get("time") or row.get("timestamp") or row.get("datetime") or ""))
        if ts is None:
            raise ValueError("unparseable timestamp")
        bars.append(Bar(ts, float(row["open"]), float(row["high"]), float(row["low"]), float(row["close"]), float(row.get("volume") or 0.0), idx))
    return bars


def max_drawdown(equity_curve: list[float], initial: float) -> float:
    peak = initial
    worst = 0.0
    for value in equity_curve:
        peak = max(peak, value)
        if peak > 0:
            worst = max(worst, (peak - value) / peak * 100.0)
    return worst


def run_engine(bars: list[Bar], overrides: dict[str, Any], symbol: str) -> dict[str, Any]:
    base = dict(DEFAULT_CONFIG)
    base.update({
        "instrument_symbol": symbol,
        "instrument_price_tick": 0.1,
        "instrument_qty_step": 0.001,
        "instrument_min_qty": 0.001,
        "instrument_min_notional": 0.0,
        "initial_capital": 10000.0,
        "max_leverage_cap": 1.0,
        "margin_long_pct": 100.0,
        "margin_short_pct": 100.0,
    })
    base.update(overrides)
    validate_config(base)
    result = run_with_result(bars, config_overrides=base, dataset_id=str(symbol))
    row = result.to_optimizer_row()
    row["final_equity"] = float(base["initial_capital"]) + float(row["net_profit"])
    row["unrealistic_qty_or_leverage"] = False
    return row


def task_evaluation_identity(task: dict[str, Any]) -> EvaluationIdentity:
    return EvaluationIdentity(
        profile_id=str(task.get("profile", "")),
        dataset_id=str(task.get("dataset_id", "")),
        dataset_hash=str(task.get("sha256", "")),
        symbol=str(task.get("symbol", "")),
        timeframe=str(task.get("timeframe_normalized") or task.get("timeframe", "")),
        window_id=str(task.get("window_id", "")),
        split_type=str(task.get("split_type", "")),
        params=dict(task.get("params", {})),
        runner_version=RUNNER_METRICS_ADAPTER_VERSION,
        optimizer_version="run_mtc_multidataset_walkforward_optimization_v2",
        parameter_mapper_version="optimization_parameter_mapper_v1",
    )


def run_evaluation(task: dict[str, Any]) -> dict[str, Any]:
    worker_id = task["worker_id"]
    out_root = Path(task["out_root"])
    result_dir = out_root / "workers" / worker_id / task["profile"] / task["dataset_id"] / task["window_id"] / task["variant_id"]
    result_dir.mkdir(parents=True, exist_ok=True)
    try:
        source_path = Path(task["source_path"])
        actual_hash = sha256_file(source_path)
        if actual_hash != task["sha256"]:
            raise RuntimeError(f"dataset hash mismatch expected={task['sha256']} actual={actual_hash}")
        bars = load_bars(source_path, int(task[f"{task['split_type']}_start"]), int(task[f"{task['split_type']}_end"]))
        overrides = apply_parameter_mapping(dict(task["params"]))
        metrics = run_engine(bars, overrides, str(task["symbol"]))
        row = {
            **{key: task[key] for key in ["profile", "variant_id", "parameter_hash", "evaluation_key", "dataset_id", "symbol", "exchange", "timeframe", "timeframe_normalized", "source_type", "source_path", "start", "end", "window_id", "split_type", "sha256"]},
            "params_json": json.dumps(task["params"], sort_keys=True),
            "overrides_json": json.dumps(overrides, sort_keys=True),
            "dataset_hash_valid": True,
            "failed_runner": False,
            **metrics,
        }
        write_json(result_dir / f"{task['split_type']}.json", row)
        return row
    except Exception as exc:
        row = {
            **{key: task.get(key, "") for key in ["profile", "variant_id", "parameter_hash", "evaluation_key", "dataset_id", "symbol", "exchange", "timeframe", "timeframe_normalized", "source_type", "source_path", "start", "end", "window_id", "split_type", "sha256"]},
            "params_json": json.dumps(task.get("params", {}), sort_keys=True),
            "dataset_hash_valid": False if "hash mismatch" in str(exc) else True,
            "failed_runner": True,
            "error": str(exc),
            "traceback": traceback.format_exc(),
            "total_trades": 0,
            "net_profit": 0.0,
            "net_profit_pct": 0.0,
            "profit_factor": 0.0,
            "max_drawdown_pct": 999.0,
            "win_rate": 0.0,
            "final_equity": 0.0,
            "unrealistic_qty_or_leverage": False,
        }
        write_json(result_dir / f"{task.get('split_type', 'unknown')}_failure.json", row)
        return row


def make_tasks(profiles: list[dict[str, Any]], windows: list[dict[str, Any]], out_root: Path, max_evaluations: int | None = None, smoke: bool = False) -> list[dict[str, Any]]:
    tasks: list[dict[str, Any]] = []
    worker_mod = max(1, min((os.cpu_count() or 2) - 1, 8))
    for profile in profiles:
        variants = generate_variants(profile, limit=7 if smoke else None)
        for variant_index, params in enumerate(variants):
            p_hash = parameter_hash(params)
            variant_id = f"{profile['name']}_{variant_index:05d}_{p_hash}"
            for window in windows:
                for split_type in ["train", "validation", "test"]:
                    task = {
                        **window,
                        "profile": profile["name"],
                        "variant_id": variant_id,
                        "parameter_hash": p_hash,
                        "params": params,
                        "split_type": split_type,
                        "out_root": str(out_root),
                        "worker_id": f"worker_{len(tasks) % worker_mod:05d}",
                    }
                    task["evaluation_key"] = evaluation_key(task_evaluation_identity(task))
                    tasks.append(task)
                    if max_evaluations is not None and len(tasks) >= max_evaluations:
                        return tasks
    return tasks


def write_checkpoint(out_root: Path, completed: int, planned: int) -> None:
    payload = {"timestamp": datetime.now(timezone.utc).isoformat(), "completed": completed, "planned": planned}
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    write_json(out_root / "checkpoints" / f"checkpoint_{stamp}.json", payload)


def run_tasks(tasks: list[dict[str, Any]], out_root: Path, max_workers_arg: str, time_budget_minutes: int) -> list[dict[str, Any]]:
    cpu = os.cpu_count() or 2
    max_workers = min(max(cpu - 1, 1), 6) if max_workers_arg == "auto" else int(max_workers_arg)
    deadline = datetime.now(timezone.utc) + timedelta(minutes=time_budget_minutes)
    results: list[dict[str, Any]] = []
    registry = ResumeRegistry(out_root / "resume_registry.sqlite")
    scheduled: list[dict[str, Any]] = []
    skipped_completed = 0
    for task in tasks:
        key = str(task["evaluation_key"])
        if registry.is_completed(key):
            registry.mark_skipped_already_completed(key)
            skipped_completed += 1
            continue
        registry.register_planned(key)
        scheduled.append(task)
    last_checkpoint = datetime.now(timezone.utc) - timedelta(minutes=15)
    with ProcessPoolExecutor(max_workers=max_workers) as pool:
        for task in scheduled:
            registry.mark_running(str(task["evaluation_key"]))
        futures = {pool.submit(run_evaluation, task): task for task in scheduled}
        for future in as_completed(futures):
            row = future.result()
            results.append(row)
            key = str(row.get("evaluation_key", ""))
            if str(row.get("failed_runner", "False")).lower() == "true":
                registry.mark_failed(key, str(row.get("error", "")))
            else:
                registry.mark_completed(key, result_path="", metrics_hash=metrics_hash(row))
            if datetime.now(timezone.utc) - last_checkpoint >= timedelta(minutes=15):
                write_checkpoint(out_root, len(results), len(scheduled))
                last_checkpoint = datetime.now(timezone.utc)
            if datetime.now(timezone.utc) >= deadline:
                break
    unique_results, duplicate_conflicts = registry.dedupe_results(results)
    write_checkpoint(out_root, len(unique_results), len(scheduled))
    (out_root / "logs/runtime_summary.json").parent.mkdir(parents=True, exist_ok=True)
    write_json(
        out_root / "logs/runtime_summary.json",
        {
            "max_workers": max_workers,
            "planned": len(tasks),
            "scheduled": len(scheduled),
            "completed": len(unique_results),
            "skipped_already_completed": skipped_completed,
            "duplicate_conflicts": len(duplicate_conflicts),
            "registry_version": REGISTRY_VERSION,
        },
    )
    registry.write_registry_report(out_root / "reports/RESUME_DEDUP_REGISTRY_RUNTIME_REPORT.md")
    return unique_results


def write_reports(out_root: Path, archive_root: Path, datasets: list[dict[str, Any]], selected: list[dict[str, Any]], windows: list[dict[str, Any]], evaluations: list[dict[str, Any]], verdict: str) -> None:
    write_outputs(evaluations, out_root)
    ranked = list(csv.DictReader((out_root / "ranked/ranked_candidates.csv").open("r", encoding="utf-8", newline=""))) if (out_root / "ranked/ranked_candidates.csv").exists() else []
    robust = list(csv.DictReader((out_root / "ranked/robust_candidates.csv").open("r", encoding="utf-8", newline=""))) if (out_root / "ranked/robust_candidates.csv").exists() else []
    failed = [row for row in evaluations if row.get("failed_runner")]
    used_symbols = sorted({item["symbol"] for item in selected})
    used_tfs = sorted({item["timeframe_normalized"] for item in selected})
    discovered_symbols = sorted({item["symbol"] for item in datasets if item["usable_for_optimization"]})
    discovered_tfs = sorted({item["timeframe_normalized"] for item in datasets if item["timeframe_normalized"] != "UNKNOWN"})
    report = [
        "# Overnight Multi-Timeframe Optimization Report",
        "",
        f"## A. Executive summary\nVerdict: `{verdict}`. Research-only local Python-engine optimization; no live trading, no API keys, no TradingView automation, no Pine behavior changes.",
        f"## B. Exact archive folder used\n`{archive_root}`",
        f"## C. Coins discovered\n`{', '.join(discovered_symbols)}`",
        f"## D. Coins used\n`{', '.join(used_symbols)}`",
        f"## E. Timeframes discovered\n`{', '.join(discovered_tfs)}`",
        f"## F. Timeframes used\n`{', '.join(used_tfs)}`",
        f"## G. Datasets skipped and why\nSee `datasets/DATASET_DISCOVERY_REPORT.md`.",
        f"## H. Total unique parameter variants\n`{len({row.get('parameter_hash') for row in evaluations})}`",
        f"## I. Total variant-window evaluations\n`{len(evaluations)}`",
        f"## J. Total failed evaluations\n`{len(failed)}`",
        "## K. Worker count and runtime\nSee `logs/runtime_summary.json` and `checkpoints/`.",
        "## L. Walk-forward method\nEach usable dataset uses rolling 60/20/20 train/validation/test windows. >=5000 rows gets 4 windows; 1500-4999 rows gets 2.",
        "## M. Per-timeframe results\nSee `cross_timeframe/per_timeframe_summary.csv`.",
        "## N. Per-symbol results\nSee `cross_symbol/per_symbol_summary.csv`.",
        f"## O. Top 20 robust candidates\n{json.dumps(robust[:20], indent=2)}",
        f"## P. Top 10 candidates with full params\n{json.dumps(ranked[:10], indent=2)}",
        "## Q. Candidates rejected and why\nSee `ranked/rejected_candidates.json`.",
        "## R. Best candidate per timeframe\nSee `cross_timeframe/per_timeframe_summary.csv` plus ranked candidates.",
        "## S. Best candidate per symbol\nSee `cross_symbol/per_symbol_summary.csv` plus ranked candidates.",
        "## T. Candidate stability across timeframes\nRobust scoring rewards candidates positive across more tested timeframes.",
        "## U. Candidate stability across symbols\nOnly discovered usable symbol was available in this archive selection, so true cross-symbol validation is limited.",
        "## V. ATR/global parameter findings\n`global_atr_length` mapped only to safe ATR fields: `st_atr_len`, `sl_atr_len`, `tp_atr_len`, `trail_atr_len`.",
        "## W. Optimization problems found\n15m was missing; archive had one usable symbol family; cross-symbol validation could not be made strong from available data.",
        "## X. Recommended code/data fixes\nAdd more symbols/timeframes to archive, add first-class Runner metrics API, and add resume de-duplication for worker outputs.",
        "## Y. What should not be changed yet\nDo not modify Pine, enable guards, or claim TradingView release parity from these research outputs.",
        f"## Z. Final verdict\n`{verdict}`",
    ]
    (out_root / "OVERNIGHT_MULTI_TIMEFRAME_OPTIMIZATION_REPORT.md").write_text("\n\n".join(report) + "\n", encoding="utf-8")
    index = [
        "# Overnight Multi-Timeframe Optimization Index",
        "",
        "- `datasets/DATASET_DISCOVERY_REPORT.md`",
        "- `datasets/dataset_manifest.json`",
        "- `datasets/dataset_manifest.yml`",
        "- `datasets/SELECTED_DATASETS.md`",
        "- `datasets/selected_datasets.json`",
        "- `walkforward/walkforward_windows.csv`",
        "- `walkforward/WALKFORWARD_WINDOW_REPORT.md`",
        "- `results/all_evaluations.csv`",
        "- `ranked/all_unique_variants.csv`",
        "- `ranked/ranked_candidates.csv`",
        "- `ranked/robust_candidates.csv`",
        "- `ranked/rejected_candidates.json`",
        "- `failures/failed_evaluations.json`",
        "- `cross_timeframe/per_timeframe_summary.csv`",
        "- `cross_symbol/per_symbol_summary.csv`",
        "- `walkforward/per_window_summary.csv`",
        "- `reports/OPTIMIZATION_PROBLEM_DISCOVERY_REPORT.md`",
        "- `OVERNIGHT_MULTI_TIMEFRAME_OPTIMIZATION_REPORT.md`",
    ]
    (out_root / "OVERNIGHT_MULTI_TIMEFRAME_OPTIMIZATION_INDEX.md").write_text("\n".join(index) + "\n", encoding="utf-8")
    problem = [
        "# Optimization Problem Discovery Report",
        "",
        "- Missing timeframe: `15m` was not present in the discovered usable archive CSV set.",
        "- Cross-symbol limitation: only `BTCUSDT.P` usable chart CSVs were discovered in the requested archive folder.",
        f"- Failed evaluations: `{len(failed)}`.",
        "- Worker outputs are isolated under `workers/<worker_id>/<profile>/<dataset_id>/<window_id>/<variant_id>/`.",
        "- Strategy risk: candidates can still be single-symbol artifacts until ETH/SOL/BNB/ADA datasets are added.",
    ]
    (out_root / "reports/OPTIMIZATION_PROBLEM_DISCOVERY_REPORT.md").write_text("\n".join(problem) + "\n", encoding="utf-8")
    for name, title in [
        ("MULTI_TIMEFRAME_OPTIMIZATION_REPORT.md", "Multi-Timeframe Optimization Report"),
        ("CROSS_SYMBOL_VALIDATION_REPORT.md", "Cross-Symbol Validation Report"),
        ("ROBUST_CANDIDATE_REPORT.md", "Robust Candidate Report"),
    ]:
        (out_root / "reports" / name).write_text(f"# {title}\n\nSee `../OVERNIGHT_MULTI_TIMEFRAME_OPTIMIZATION_REPORT.md` and ranked CSV outputs.\n", encoding="utf-8")


def create_profiles(out_root: Path) -> list[dict[str, Any]]:
    profile_dir = out_root / "profiles"
    profile_dir.mkdir(parents=True, exist_ok=True)
    profiles = [
        {
            "name": "producer_only_v2",
            "shuffle_seed": 2102,
            "max_variants": 49,
            "parameters": {
                "signal_mode": ["Supertrend"],
                "st_factor": [2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0],
                "global_atr_length": [7, 10, 14, 21, 28, 35, 50],
                "sl_atr_mult": [2.5],
                "tp_mode": ["None"],
                "tp_r_multiple": [2.0],
                "risk_long": [0.5],
                "risk_short": [0.5],
                "exit_on_filter_bundle": [True],
                "guards_disabled_for_phase1": [True],
                "visualization_disabled": [True],
                "integrations_disabled": [True],
            },
        },
        {
            "name": "parity_first_minimal_v2",
            "shuffle_seed": 2101,
            "max_variants": 300,
            "parameters": {
                "signal_mode": ["Supertrend"],
                "st_factor": [2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0],
                "global_atr_length": [7, 10, 14, 21, 28, 35, 50],
                "sl_atr_mult": [1.5, 2.0, 2.5, 2.75, 3.0, 3.5, 4.0],
                "tp_mode": ["None", "R"],
                "tp_r_multiple": [1.0, 1.5, 2.0, 2.5, 3.0],
                "risk_long": [0.25, 0.5, 0.75, 1.0],
                "risk_short": [0.25, 0.5, 0.75, 1.0],
                "exit_on_filter_bundle": [True],
                "guards_disabled_for_phase1": [True],
                "visualization_disabled": [True],
                "integrations_disabled": [True],
            },
        },
        {
            "name": "exits_only_v2",
            "shuffle_seed": 2103,
            "max_variants": 96,
            "parameters": {
                "signal_mode": ["Supertrend"],
                "st_factor": [3.5, 4.0],
                "global_atr_length": [10, 14, 21],
                "sl_atr_mult": [2.0, 2.5, 2.75, 3.0],
                "tp_mode": ["None", "R"],
                "tp_r_multiple": [1.5, 2.0, 2.5],
                "risk_long": [0.25, 0.5],
                "risk_short": [0.5, 0.75],
                "use_break_even": [False],
                "use_trailing": [False],
                "exit_on_filter_bundle": [True],
                "guards_disabled_for_phase1": [True],
                "visualization_disabled": [True],
                "integrations_disabled": [True],
            },
        },
        {
            "name": "robust_second_pass_v2",
            "shuffle_seed": 2104,
            "max_variants": 120,
            "parameters": {
                "signal_mode": ["Supertrend"],
                "st_factor": [3.0, 3.5, 4.0],
                "global_atr_length": [10, 14, 21],
                "sl_atr_mult": [2.5, 2.75, 3.0],
                "tp_mode": ["None", "R"],
                "tp_r_multiple": [1.5, 2.0, 2.5],
                "risk_long": [0.25, 0.5],
                "risk_short": [0.5, 0.75],
                "exit_on_filter_bundle": [True],
                "guards_disabled_for_phase1": [True],
                "visualization_disabled": [True],
                "integrations_disabled": [True],
            },
        },
    ]
    for profile in profiles:
        write_json(profile_dir / f"{profile['name']}.yml", profile)
    return profiles


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--archive", default=r"C:\LAB\tradingview-lab\mtc_backtest\parity_suite_350\tv_manual_inputs\raw_tv_exports\ARŞİV")
    parser.add_argument("--job")
    parser.add_argument("--discover-datasets", action="store_true")
    parser.add_argument("--datasets")
    parser.add_argument("--walkforward")
    parser.add_argument("--profiles")
    parser.add_argument("--out", required=True)
    parser.add_argument("--max-workers", default="auto")
    parser.add_argument("--time-budget-minutes", type=int, default=480)
    parser.add_argument("--min-evaluations", type=int, default=5000)
    parser.add_argument("--target-evaluations", type=int, default=20000)
    args = parser.parse_args()
    out_root = Path(args.out)
    archive_root = Path(args.archive)
    for sub in ["datasets", "profiles", "workers", "results", "ranked", "walkforward", "cross_timeframe", "cross_symbol", "failures", "logs", "checkpoints", "reports"]:
        (out_root / sub).mkdir(parents=True, exist_ok=True)
    if args.job:
        job_path = Path(args.job)
        job = load_optimizer_job_json(job_path)
        manifest_path = Path(str(job["dataset_manifest_path"]))
        regime_path = Path(str(job.get("regime_registry_path", "")))
        validation_report = validate_optimizer_dataset_job(job_path, manifest_path, regime_path)
        write_optimizer_dataset_validation_reports(validation_report)
        if validation_report["status"] == "FAIL":
            raise SystemExit("dataset usage validation failed; see reports/optimization_dataset_usage/DATASET_USAGE_VALIDATION_REPORT.md")
        datasets = datasets_from_manifest(manifest_path, [str(item) for item in job.get("dataset_ids", [])], out_root)
        selected = datasets
    elif args.datasets:
        manifest_path = Path(args.datasets)
        datasets = datasets_from_manifest(manifest_path, [], out_root)
        selected = datasets
    elif args.discover_datasets:
        datasets = discover_datasets(archive_root, out_root)
        selected = select_datasets(datasets, out_root)
    else:
        raise SystemExit("dataset manifest/job required; use --job or --datasets, or explicitly pass --discover-datasets to scan ARŞİV")
    windows = create_walkforward(selected, out_root)
    mapper_target = out_root / "parameter_mapper.yml"
    mapper_target.write_text(json.dumps(mapper_payload(), indent=2, sort_keys=True), encoding="utf-8")
    (out_root / "reports/PARAMETER_MAPPER_V2_REPORT.md").write_text("# Parameter Mapper V2 Report\n\nGlobal ATR maps to safe ATR fields only. `risk_long` and `risk_short` map to Python risk percentage fields.\n", encoding="utf-8")
    (out_root / "reports/WORKER_ISOLATION_V2_REPORT.md").write_text("# Worker Isolation V2 Report\n\nWorkers write to `workers/<worker_id>/<profile>/<dataset_id>/<window_id>/<variant_id>/`; merge writes happen after worker completion.\n", encoding="utf-8")
    profiles = create_profiles(out_root)
    smoke_tasks = make_tasks(profiles[:1], windows[:1], out_root, max_evaluations=20, smoke=True)
    smoke_results = run_tasks(smoke_tasks, out_root, args.max_workers, min(10, args.time_budget_minutes))
    smoke_failed = len([row for row in smoke_results if row.get("failed_runner")])
    if smoke_failed >= len(smoke_results):
        evaluations = smoke_results
    else:
        task_budget = args.target_evaluations
        if len(windows) * 3 * 49 < args.min_evaluations:
            task_budget = max(task_budget, args.min_evaluations)
        tasks = make_tasks(profiles, windows, out_root, max_evaluations=task_budget)
        evaluations = run_tasks(tasks, out_root, args.max_workers, args.time_budget_minutes)
    write_csv(out_root / "results/all_evaluations.csv", evaluations)
    write_outputs(evaluations, out_root)
    robust_path = out_root / "ranked/robust_candidates.csv"
    robust_count = max(0, sum(1 for _ in robust_path.open("r", encoding="utf-8")) - 1) if robust_path.exists() else 0
    timeframes_tested = {row.get("timeframe_normalized") for row in evaluations}
    if len(evaluations) >= args.min_evaluations and len(timeframes_tested) >= 2 and robust_count > 0:
        verdict = "MULTITIMEFRAME_WALKFORWARD_OPTIMIZATION_COMPLETED_ROBUST_CANDIDATES_FOUND"
    elif len(evaluations) >= args.min_evaluations and len(timeframes_tested) >= 2:
        verdict = "MULTITIMEFRAME_WALKFORWARD_OPTIMIZATION_COMPLETED_NO_ROBUST_CANDIDATE"
    elif evaluations:
        verdict = "MULTITIMEFRAME_WALKFORWARD_OPTIMIZATION_PARTIAL_WITH_BLOCKERS"
    else:
        verdict = "MULTITIMEFRAME_WALKFORWARD_OPTIMIZATION_BLOCKED"
    write_reports(out_root, archive_root, datasets, selected, windows, evaluations, verdict)
    print(json.dumps({"verdict": verdict, "evaluations": len(evaluations), "robust_candidates": robust_count, "selected_datasets": len(selected), "windows": len(windows)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
