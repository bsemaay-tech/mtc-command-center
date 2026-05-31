from __future__ import annotations

import argparse
import csv
import hashlib
import itertools
import json
import math
import os
import sys
import time
import traceback
from concurrent.futures import FIRST_COMPLETED, ProcessPoolExecutor, wait
from datetime import datetime, time as dt_time, timedelta, timezone
from functools import lru_cache
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "00_PYTHON"))
sys.path.insert(0, str(ROOT))

from mtc_v2.core.config import DEFAULT_CONFIG, validate_config
from mtc_v2.core.types import Bar
from tools.optimization_parameter_mapper import apply_parameter_mapping
from tools.optimization_resume_registry import (
    EvaluationIdentity,
    ResumeRegistry,
    evaluation_key,
    metrics_hash,
)
from tools.runner_metrics_adapter import RUNNER_METRICS_ADAPTER_VERSION, run_with_result


PROFILE_ID = "supertrend_exhaustive_core_v1"
OPTIMIZER_VERSION = "big_overnight_multiasset_exhaustive_grid_v1"
MAPPER_VERSION = "optimization_parameter_mapper_v1"
TARGET_TIMEFRAMES = ["15m", "1h", "2h", "4h", "1D"]
PREFERRED_ASSETS = [
    "BTCUSDT",
    "ETHUSDT",
    "SOLUSDT",
    "BNBUSDT",
    "XRPUSDT",
    "ADAUSDT",
    "AVAXUSDT",
    "DOGEUSDT",
    "LINKUSDT",
    "DOTUSDT",
    "POLUSDT",
    "LTCUSDT",
    "TRXUSDT",
    "NEARUSDT",
    "APTUSDT",
    "ARBUSDT",
    "OPUSDT",
]
ALLOWED_SOURCE_TYPES = {"binance_public_futures_klines", "tradingview_chart_csv_binance"}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + f".{os.getpid()}.tmp")
    tmp.write_text(json.dumps(payload, indent=2, sort_keys=True, default=str), encoding="utf-8")
    tmp.replace(path)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = sorted({key for row in rows for key in row})
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def parse_time(value: str) -> datetime:
    value = str(value).strip()
    if value.isdigit():
        raw = int(value)
        if raw > 10_000_000_000:
            raw //= 1000
        return datetime.fromtimestamp(raw, timezone.utc)
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def load_json_or_sidecar(path: Path) -> dict[str, Any]:
    if not path.exists() and path.with_suffix(".json").exists():
        path = path.with_suffix(".json")
    text = path.read_text(encoding="utf-8-sig").strip()
    if text.startswith("{"):
        return json.loads(text)
    sidecar = path.with_suffix(".json")
    if sidecar.exists():
        return json.loads(sidecar.read_text(encoding="utf-8-sig"))
    raise ValueError(f"JSON sidecar required for YAML manifest: {path}")


def bundle_root_from_manifest(path: Path) -> Path:
    return path.parent.parent if path.parent.name == "manifests" else path.parent


def load_manifest(path: Path) -> list[dict[str, Any]]:
    payload = load_json_or_sidecar(path)
    return [dict(item) for item in payload.get("datasets", [])]


def load_regime_registry(path: Path) -> dict[str, dict[str, Any]]:
    payload = load_json_or_sidecar(path)
    return {str(item["dataset_id"]): dict(item) for item in payload.get("datasets", []) if item.get("dataset_id")}


def normalized_dataset_entry(item: dict[str, Any], bundle_root: Path) -> dict[str, Any]:
    source_path = Path(str(item.get("normalized_path") or item.get("raw_path")))
    if not source_path.is_absolute():
        source_path = bundle_root / source_path
    return {
        **item,
        "source_path": str(source_path),
        "sha256": str(item.get("sha256_normalized") or item.get("sha256_raw") or item.get("sha256")),
        "timeframe_normalized": str(item.get("timeframe_normalized") or item.get("timeframe")),
    }


def select_datasets(manifest: list[dict[str, Any]], regimes: dict[str, dict[str, Any]], bundle_root: Path, out_root: Path, max_assets: int) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    usable = []
    skipped = []
    for raw in manifest:
        item = normalized_dataset_entry(raw, bundle_root)
        reason = ""
        if item.get("source_type") not in ALLOWED_SOURCE_TYPES:
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
            skipped.append({"dataset_id": item.get("dataset_id"), "symbol": item.get("symbol"), "timeframe": item.get("timeframe_normalized"), "reason": reason})
        else:
            usable.append(item)

    by_pair: dict[tuple[str, str], list[dict[str, Any]]] = {}
    for item in usable:
        by_pair.setdefault((str(item["symbol"]), str(item["timeframe_normalized"])), []).append(item)

    assets = []
    discovered = {}
    for symbol in sorted({str(item["symbol"]) for item in usable}, key=lambda sym: PREFERRED_ASSETS.index(sym) if sym in PREFERRED_ASSETS else 999):
        timeframes = sorted({str(item["timeframe_normalized"]) for item in usable if item["symbol"] == symbol}, key=lambda tf: TARGET_TIMEFRAMES.index(tf) if tf in TARGET_TIMEFRAMES else 999)
        discovered[symbol] = timeframes
        coverage = len([tf for tf in TARGET_TIMEFRAMES if tf in timeframes])
        if coverage >= 5:
            assets.append((0, PREFERRED_ASSETS.index(symbol) if symbol in PREFERRED_ASSETS else 999, symbol))
        elif coverage >= 4:
            assets.append((1, PREFERRED_ASSETS.index(symbol) if symbol in PREFERRED_ASSETS else 999, symbol))
    selected_symbols = [symbol for _bucket, _priority, symbol in sorted(assets)[:max_assets]]
    selected = []
    for symbol in selected_symbols:
        for timeframe in TARGET_TIMEFRAMES:
            candidates = by_pair.get((symbol, timeframe), [])
            if not candidates:
                continue
            candidates.sort(key=lambda row: (row.get("source_type") != "binance_public_futures_klines", int(row.get("row_count", 0))), reverse=False)
            selected.append(max(candidates, key=lambda row: int(row.get("row_count", 0))))

    summary = {
        "discovered_assets": discovered,
        "selected_assets": selected_symbols,
        "selected_dataset_count": len(selected),
        "skipped": skipped,
    }
    write_json(out_root / "dataset_selection.json", {"summary": summary, "datasets": selected})
    lines = [
        "# Dataset Selection Report",
        "",
        f"- Discovered assets: `{len(discovered)}`",
        f"- Selected assets: `{', '.join(selected_symbols)}`",
        f"- Selected datasets: `{len(selected)}`",
        "",
        "| symbol | timeframe | dataset_id | rows | source_type | start | end | sha256 | regime |",
        "|---|---|---|---:|---|---|---|---|---|",
    ]
    for item in selected:
        lines.append(f"| {item['symbol']} | {item['timeframe_normalized']} | {item['dataset_id']} | {item['row_count']} | {item['source_type']} | {item['start']} | {item['end']} | {item['sha256']} | yes |")
    lines.extend(["", "## Skipped", ""])
    for item in skipped:
        lines.append(f"- `{item.get('dataset_id')}` {item.get('symbol')} {item.get('timeframe')}: `{item.get('reason')}`")
    for path in [out_root / "datasets/DATASET_SELECTION_REPORT.md", out_root / "reports/DATASET_SELECTION_REPORT.md"]:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return selected, summary


def load_bars(path: Path, start: int, end: int) -> list[Bar]:
    bars: list[Bar] = []
    with path.open("r", encoding="utf-8-sig", newline="") as fh:
        rows = list(csv.DictReader(fh))[start:end]
    for idx, row in enumerate(rows):
        bars.append(
            Bar(
                timestamp=parse_time(str(row.get("timestamp_utc") or row.get("time") or row.get("timestamp") or row.get("datetime"))),
                open=float(row["open"]),
                high=float(row["high"]),
                low=float(row["low"]),
                close=float(row["close"]),
                volume=float(row.get("volume") or 0.0),
                bar_index=idx,
            )
        )
    return bars


def quality_check(selected: list[dict[str, Any]], out_root: Path) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    passed = []
    failed = []
    for item in selected:
        path = Path(str(item["source_path"]))
        reason = ""
        actual_hash = sha256_file(path) if path.exists() else ""
        if not path.exists():
            reason = "file_missing"
        elif actual_hash != str(item["sha256"]):
            reason = f"sha256_mismatch:{actual_hash}"
        else:
            times = []
            duplicates = 0
            invalid_ohlc = 0
            seen = set()
            with path.open("r", encoding="utf-8-sig", newline="") as fh:
                for row in csv.DictReader(fh):
                    ts = parse_time(str(row.get("timestamp_utc") or row.get("time") or row.get("timestamp") or row.get("datetime")))
                    key = ts.isoformat()
                    if key in seen:
                        duplicates += 1
                    seen.add(key)
                    times.append(ts)
                    try:
                        o = float(row["open"]); h = float(row["high"]); low = float(row["low"]); c = float(row["close"])
                        if h < low or o < low or o > h or c < low or c > h or min(o, h, low, c) < 0 or c <= 0:
                            invalid_ohlc += 1
                    except Exception:
                        invalid_ohlc += 1
            if times != sorted(times):
                reason = "timestamps_not_sorted"
            elif duplicates:
                reason = f"duplicate_timestamps:{duplicates}"
            elif invalid_ohlc:
                reason = f"invalid_ohlc:{invalid_ohlc}"
        record = {**item, "quality_reason": reason, "actual_sha256": actual_hash}
        if reason:
            failed.append(record)
        else:
            passed.append(record)
    write_json(out_root / "datasets/dataset_quality.json", {"passed": passed, "failed": failed})
    lines = ["# Dataset Quality Report", "", f"- Passed: `{len(passed)}`", f"- Failed: `{len(failed)}`", ""]
    for row in failed:
        lines.append(f"- `{row['dataset_id']}`: `{row['quality_reason']}`")
    (out_root / "datasets/DATASET_QUALITY_REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return passed, failed


def create_walkforward(selected: list[dict[str, Any]], out_root: Path) -> list[dict[str, Any]]:
    windows = []
    for dataset in selected:
        n = int(dataset["row_count"])
        if n < 1500:
            continue
        if n >= 10000:
            count = 5; train_pct = 0.50; val_pct = 0.25; step_pct = 0.15
        elif n >= 5000:
            count = 4; train_pct = 0.60; val_pct = 0.20; step_pct = 0.20
        else:
            count = 2; train_pct = 0.60; val_pct = 0.20; step_pct = 0.20
        step = max(1, int(n * step_pct))
        for idx in range(count):
            start = min(idx * step, n - 1)
            available = n - start
            train_len = max(1, int(available * train_pct))
            val_len = max(1, int(available * val_pct))
            test_len = max(1, available - train_len - val_len)
            train_start = start; train_end = start + train_len
            val_start = train_end; val_end = val_start + val_len
            test_start = val_end; test_end = min(n, test_start + test_len)
            base = {
                **dataset,
                "window_id": f"{dataset['dataset_id']}_wf{idx+1}",
                "window_index": idx + 1,
            }
            for split_type, split_start, split_end in [
                ("train", train_start, train_end),
                ("validation", val_start, val_end),
                ("test", test_start, test_end),
            ]:
                windows.append({**base, "split_type": split_type, "split_start": split_start, "split_end": split_end})
    write_csv(out_root / "walkforward/walkforward_windows.csv", windows)
    lines = ["# Walkforward Window Report", "", f"- Split evaluations per variant: `{len(windows)}`", ""]
    lines.append("| dataset_id | symbol | timeframe | window_id | split | start | end |")
    lines.append("|---|---|---|---|---|---:|---:|")
    for row in windows:
        lines.append(f"| {row['dataset_id']} | {row['symbol']} | {row['timeframe_normalized']} | {row['window_id']} | {row['split_type']} | {row['split_start']} | {row['split_end']} |")
    for path in [out_root / "walkforward/WALKFORWARD_WINDOW_REPORT.md", out_root / "reports/WALKFORWARD_SUMMARY_REPORT.md"]:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return windows


def canonical_params(raw: dict[str, Any]) -> dict[str, Any]:
    params = dict(raw)
    if params.get("tp_mode") == "None":
        params["tp_r_multiple"] = None
    return params


def generate_variants() -> list[dict[str, Any]]:
    grid = {
        "signal_mode": ["Supertrend"],
        "st_factor": [2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0],
        "global_atr_length": [7, 10, 14, 21, 28],
        "sl_atr_mult": [2.0, 2.5, 2.75, 3.0, 3.5],
        "tp_mode": ["None", "R"],
        "tp_r_multiple": [1.0, 1.5, 2.0, 2.5, 3.0],
        "risk_long": [0.25, 0.5, 0.75],
        "risk_short": [0.25, 0.5, 0.75, 1.0],
        "use_break_even": [False],
        "use_trailing": [False],
        "guards_disabled_for_phase1": [True],
        "integrations_disabled": [True],
        "visualization_disabled": [True],
        "exit_on_filter_bundle": [True],
    }
    seen = {}
    keys = list(grid.keys())
    for combo in itertools.product(*[grid[key] for key in keys]):
        params = canonical_params(dict(zip(keys, combo)))
        seen[hashlib.sha256(json.dumps(params, sort_keys=True).encode("utf-8")).hexdigest()[:16]] = params
    return [seen[key] for key in sorted(seen)]


def write_parameter_grid(out_root: Path, variants: list[dict[str, Any]]) -> None:
    text = {
        "profile": PROFILE_ID,
        "unique_parameter_variants": len(variants),
        "invalid_combo_rules": ["tp_mode None canonicalizes tp_r_multiple to null"],
        "parameters": {
            "st_factor": [2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0],
            "global_atr_length": [7, 10, 14, 21, 28],
            "sl_atr_mult": [2.0, 2.5, 2.75, 3.0, 3.5],
            "tp_mode": ["None", "R"],
            "tp_r_multiple": [1.0, 1.5, 2.0, 2.5, 3.0],
            "risk_long": [0.25, 0.5, 0.75],
            "risk_short": [0.25, 0.5, 0.75, 1.0],
        },
    }
    (out_root / "parameter_grid.yml").write_text(json.dumps(text, indent=2, sort_keys=True), encoding="utf-8")


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
        p_hash = hashlib.sha256(json.dumps(params, sort_keys=True).encode("utf-8")).hexdigest()[:16]
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
            }
            ordinal += 1


@lru_cache(maxsize=128)
def load_regime_map(regime_file: str) -> dict[str, str]:
    mapping = {}
    path = Path(regime_file)
    if not path.exists():
        return mapping
    with path.open("r", encoding="utf-8-sig", newline="") as fh:
        for row in csv.DictReader(fh):
            mapping[str(row.get("timestamp_utc"))] = str(row.get("regime", "UNKNOWN"))
    return mapping


def regime_metrics_for_trades(trades: list[Any], regime_map: dict[str, str]) -> dict[str, Any]:
    buckets: dict[str, list[float]] = {name: [] for name in ["TRENDING", "RANGING", "CONSOLIDATING", "CHOPPY"]}
    for trade in trades:
        exit_time = trade.exit_time.isoformat() if getattr(trade, "exit_time", None) else ""
        regime = regime_map.get(exit_time, "UNKNOWN")
        if regime in buckets:
            buckets[regime].append(float(trade.pnl))
    result = {}
    for regime, pnl_values in buckets.items():
        wins = [v for v in pnl_values if v > 0]
        losses = [v for v in pnl_values if v < 0]
        gross_profit = sum(wins)
        gross_loss = abs(sum(losses))
        result[f"regime_{regime.lower()}_trades"] = len(pnl_values)
        result[f"regime_{regime.lower()}_net_profit"] = sum(pnl_values)
        result[f"regime_{regime.lower()}_profit_factor"] = gross_profit / gross_loss if gross_loss else None
    result["regime_metrics_status"] = "OK" if any(result.get(f"regime_{name.lower()}_trades", 0) for name in buckets) else "REGIME_METRICS_UNAVAILABLE"
    return result


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
            "evaluation_key": task["evaluation_key"],
            "parameter_hash": task["parameter_hash"],
            "variant_index": task["variant_index"],
            "params_json": json.dumps(params, sort_keys=True),
            "overrides_json": json.dumps(overrides, sort_keys=True),
            "dataset_id": split["dataset_id"],
            "symbol": split["symbol"],
            "timeframe": split["timeframe"],
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
            "evaluation_key": task.get("evaluation_key", ""),
            "parameter_hash": task.get("parameter_hash", ""),
            "variant_index": task.get("variant_index", -1),
            "params_json": json.dumps(task.get("params", {}), sort_keys=True),
            "dataset_id": split.get("dataset_id", ""),
            "symbol": split.get("symbol", ""),
            "timeframe": split.get("timeframe", ""),
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
        }
        write_json(worker_root / "result.json", row)
        write_json(worker_root / "metrics.json", row)
        write_json(worker_root / "params.json", task.get("params", {}))
        (worker_root / "logs.txt").write_text(f"{utc_now()} failed {exc}\n{traceback.format_exc()}\n", encoding="utf-8")
        return row


def checkpoint(out_root: Path, payload: dict[str, Any]) -> None:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    write_json(out_root / "checkpoints" / f"checkpoint_{stamp}.json", {**payload, "timestamp": utc_now()})


def local_deadline(minutes: int) -> datetime:
    now = datetime.now().astimezone()
    seven = datetime.combine(now.date(), dt_time(7, 0), tzinfo=now.tzinfo)
    if seven <= now:
        seven = now + timedelta(minutes=minutes)
    return min(now + timedelta(minutes=minutes), seven)


def run_tasks(variants: list[dict[str, Any]], splits: list[dict[str, Any]], out_root: Path, max_workers: int, time_budget_minutes: int) -> dict[str, Any]:
    registry = ResumeRegistry(out_root / "resume_registry.sqlite")
    deadline = local_deadline(time_budget_minutes)
    planned = len(variants) * len(splits)
    completed = 0
    failed = 0
    skipped = 0
    results: list[dict[str, Any]] = []
    conflicts: list[dict[str, Any]] = []
    task_iter = iter(iter_tasks(variants, splits, out_root, max_workers))
    pending = {}
    max_pending = max_workers * 3
    last_checkpoint = time.time()
    done_planning = False
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
                continue
            done, _not_done = wait(pending.keys(), timeout=5, return_when=FIRST_COMPLETED)
            for future in done:
                task = pending.pop(future)
                row = future.result()
                results.append(row)
                if str(row.get("failed_runner", "False")).lower() == "true":
                    failed += 1
                    registry.mark_failed(str(row.get("evaluation_key", "")), str(row.get("error", "")))
                else:
                    completed += 1
                    registry.mark_completed(str(row["evaluation_key"]), result_path="", metrics_hash=metrics_hash(row))
            if time.time() - last_checkpoint >= 15 * 60:
                unique, conflicts = registry.dedupe_results(results)
                write_json(out_root / "logs/runtime_summary.json", {"planned": planned, "completed": completed, "failed": failed, "skipped_already_completed": skipped, "pending": len(pending), "duplicate_conflicts": len(conflicts), "deadline": deadline.isoformat(), "max_workers": max_workers})
                checkpoint(out_root, {"planned": planned, "completed": completed, "failed": failed, "skipped_already_completed": skipped, "pending": len(pending)})
                last_checkpoint = time.time()
    unique, conflicts = registry.dedupe_results(results)
    write_json(out_root / "results/raw_completed_batch.json", unique)
    write_json(out_root / "logs/runtime_summary.json", {"planned": planned, "completed": completed, "failed": failed, "skipped_already_completed": skipped, "duplicate_conflicts": len(conflicts), "deadline": deadline.isoformat(), "max_workers": max_workers})
    checkpoint(out_root, {"planned": planned, "completed": completed, "failed": failed, "skipped_already_completed": skipped, "duplicate_conflicts": len(conflicts)})
    registry.write_registry_report(out_root / "reports/RESUME_DEDUP_REPORT.md")
    return {"rows": unique, "planned": planned, "completed": completed, "failed": failed, "skipped": skipped, "conflicts": conflicts, "deadline": deadline.isoformat(), "max_workers": max_workers}


def finite(value: Any) -> bool:
    try:
        return math.isfinite(float(value))
    except Exception:
        return False


def fnum(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except Exception:
        return default


def split_ok(row: dict[str, Any]) -> bool:
    return (
        not bool(row.get("failed_runner"))
        and str(row.get("dataset_hash_valid", "False")).lower() == "true"
        and finite(row.get("net_profit_pct"))
        and finite(row.get("profit_factor"))
        and finite(row.get("max_drawdown_pct"))
        and fnum(row.get("net_profit_pct")) > 0
        and fnum(row.get("profit_factor")) > 1
        and fnum(row.get("max_drawdown_pct")) <= 35
        and fnum(row.get("total_trades")) >= 20
    )


def score_and_write(rows: list[dict[str, Any]], out_root: Path) -> dict[str, Any]:
    groups: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        groups.setdefault(str(row.get("parameter_hash")), []).append(row)
    candidates = []
    rejected = []
    failed = [row for row in rows if row.get("failed_runner")]
    for p_hash, items in groups.items():
        train = [r for r in items if r.get("split_type") == "train"]
        validation = [r for r in items if r.get("split_type") == "validation"]
        test = [r for r in items if r.get("split_type") == "test"]
        pos_train = [r for r in train if split_ok(r)]
        pos_validation = [r for r in validation if split_ok(r)]
        pos_test = [r for r in test if split_ok(r)]
        symbols = sorted({str(r.get("symbol")) for r in items})
        timeframes = sorted({str(r.get("timeframe_normalized")) for r in items})
        pos_symbols = sorted({str(r.get("symbol")) for r in pos_test})
        pos_timeframes = sorted({str(r.get("timeframe_normalized")) for r in pos_test})
        consistency = len(pos_test) / max(1, len(test))
        validation_ratio = len(pos_validation) / max(1, len(validation))
        test_ratio = len(pos_test) / max(1, len(test))
        test_np = sorted(fnum(r.get("net_profit_pct")) for r in test if finite(r.get("net_profit_pct")))
        test_pf = sorted(fnum(r.get("profit_factor")) for r in test if finite(r.get("profit_factor")))
        test_dd = [fnum(r.get("max_drawdown_pct"), 999.0) for r in test if finite(r.get("max_drawdown_pct"))]
        median_np = test_np[len(test_np) // 2] if test_np else 0.0
        median_pf = test_pf[len(test_pf) // 2] if test_pf else 0.0
        worst_dd = max(test_dd) if test_dd else 999.0
        score = max(0.0, median_np) * 0.25 + max(0.0, median_pf - 1) * 10 + consistency * 20 - worst_dd * 0.2 + len(pos_symbols) * 3 + len(pos_timeframes) * 2
        level = "REJECTED"
        if len(pos_train) == len(train) and len(pos_validation) == len(validation) and len(pos_test) == len(test) and consistency >= 0.70 and validation_ratio >= 0.50 and test_ratio >= 0.50 and len(pos_symbols) >= 3 and len(pos_timeframes) >= 3:
            level = "ROBUST_STRICT"
        elif len(pos_symbols) >= 3 and len(pos_timeframes) >= 3 and consistency >= 0.60:
            level = "ROBUST_MEDIUM"
        elif len(pos_test) > 0:
            level = "RESEARCH_ONLY"
        candidate = {
            "parameter_hash": p_hash,
            "params_json": items[0].get("params_json", ""),
            "evaluations": len(items),
            "symbols_tested": "|".join(symbols),
            "timeframes_tested": "|".join(timeframes),
            "positive_symbol_count": len(pos_symbols),
            "positive_timeframe_count": len(pos_timeframes),
            "walkforward_consistency": consistency,
            "validation_positive_ratio": validation_ratio,
            "test_positive_ratio": test_ratio,
            "median_test_net_profit_pct": median_np,
            "median_test_profit_factor": median_pf,
            "worst_test_drawdown_pct": worst_dd,
            "robust_level": level,
            "score": score,
        }
        candidates.append(candidate)
        if level == "REJECTED":
            rejected.append({**candidate, "reject_reasons": ["coverage_or_split_filter_failed"]})
    candidates.sort(key=lambda r: fnum(r["score"]), reverse=True)
    write_csv(out_root / "ranked/all_evaluations.csv", rows)
    write_csv(out_root / "ranked/all_unique_variants.csv", candidates)
    write_csv(out_root / "ranked/ranked_candidates.csv", candidates)
    write_csv(out_root / "ranked/robust_strict_candidates.csv", [r for r in candidates if r["robust_level"] == "ROBUST_STRICT"])
    write_csv(out_root / "ranked/robust_medium_candidates.csv", [r for r in candidates if r["robust_level"] == "ROBUST_MEDIUM"])
    write_csv(out_root / "ranked/research_only_candidates.csv", [r for r in candidates if r["robust_level"] == "RESEARCH_ONLY"])
    write_json(out_root / "ranked/rejected_candidates.json", rejected)
    write_json(out_root / "ranked/failed_evaluations.json", failed)
    return {"candidates": candidates, "failed": failed}


def aggregate_reports(rows: list[dict[str, Any]], scored: dict[str, Any], out_root: Path, run_summary: dict[str, Any], selected: list[dict[str, Any]], variants: list[dict[str, Any]], splits: list[dict[str, Any]], started_at: str, bundle: Path) -> str:
    def summarize(key: str) -> list[dict[str, Any]]:
        grouped: dict[str, list[dict[str, Any]]] = {}
        for row in rows:
            grouped.setdefault(str(row.get(key, "")), []).append(row)
        output = []
        for value, items in grouped.items():
            tests = [r for r in items if r.get("split_type") == "test"]
            output.append({"name": value, "evaluations": len(items), "test_positive": len([r for r in tests if split_ok(r)]), "test_total": len(tests)})
        return sorted(output, key=lambda r: r["name"])
    per_symbol = summarize("symbol")
    per_tf = summarize("timeframe_normalized")
    write_csv(out_root / "cross_symbol/per_symbol_summary.csv", per_symbol)
    write_csv(out_root / "cross_timeframe/per_timeframe_summary.csv", per_tf)
    regime_rows = []
    for regime in ["trending", "ranging", "consolidating", "choppy"]:
        trades = sum(int(fnum(r.get(f"regime_{regime}_trades"))) for r in rows)
        pnl = sum(fnum(r.get(f"regime_{regime}_net_profit")) for r in rows)
        regime_rows.append({"regime": regime.upper(), "trades": trades, "net_profit": pnl})
    write_csv(out_root / "regimes/regime_performance_summary.csv", regime_rows)
    for path in [out_root / "regimes/REGIME_PERFORMANCE_REPORT.md", out_root / "reports/REGIME_PERFORMANCE_REPORT.md"]:
        path.write_text("# Regime Performance Report\n\nSee `regime_performance_summary.csv`.\n", encoding="utf-8")
    robust_strict = [r for r in scored["candidates"] if r["robust_level"] == "ROBUST_STRICT"]
    robust_medium = [r for r in scored["candidates"] if r["robust_level"] == "ROBUST_MEDIUM"]
    research = [r for r in scored["candidates"] if r["robust_level"] == "RESEARCH_ONLY"]
    if robust_strict:
        verdict = "BIG_OVERNIGHT_OPTIMIZATION_COMPLETED_STRICT_ROBUST_FOUND"
    elif robust_medium:
        verdict = "BIG_OVERNIGHT_OPTIMIZATION_COMPLETED_MEDIUM_ROBUST_FOUND"
    elif research:
        verdict = "BIG_OVERNIGHT_OPTIMIZATION_COMPLETED_RESEARCH_ONLY"
    elif run_summary["completed"] < run_summary["planned"]:
        verdict = "BIG_OVERNIGHT_OPTIMIZATION_PARTIAL_TIME_BUDGET_REACHED"
    else:
        verdict = "BIG_OVERNIGHT_OPTIMIZATION_COMPLETED_NO_CANDIDATE"
    ended_at = utc_now()
    runtime_seconds = (datetime.fromisoformat(ended_at) - datetime.fromisoformat(started_at)).total_seconds()
    reports = {
        "CROSS_ASSET_REPORT.md": ("Cross Asset Report", per_symbol),
        "CROSS_TIMEFRAME_REPORT.md": ("Cross Timeframe Report", per_tf),
        "ROBUST_CANDIDATE_REPORT.md": ("Robust Candidate Report", scored["candidates"][:50]),
        "WORKER_RUNTIME_REPORT.md": ("Worker Runtime Report", [run_summary]),
        "PROBLEM_DISCOVERY_REPORT.md": ("Problem Discovery Report", [{"failed_evaluations": len(scored["failed"]), "duplicate_conflicts": len(run_summary.get("conflicts", [])), "partial": run_summary["completed"] < run_summary["planned"]}]),
    }
    for name, (title, payload) in reports.items():
        (out_root / "reports" / name).write_text(f"# {title}\n\n```json\n{json.dumps(payload, indent=2, sort_keys=True, default=str)}\n```\n", encoding="utf-8")
    report_lines = [
        "# Big Overnight Multi-Asset Optimization Report",
        "",
        f"## A. Executive summary\nVerdict: `{verdict}`. Research-only Python-engine optimization; no live trading, no TradingView export, no Pine behavior change.",
        f"## B. Time started / ended / runtime\nStarted `{started_at}`; ended `{ended_at}`; runtime seconds `{runtime_seconds}`.",
        "## C. Keep-awake status\nSee `power/keep_awake_status.md` and `power/heartbeat.log`.",
        f"## D. Dataset bundle used\n`{bundle}`",
        f"## E. Assets discovered\n`{', '.join(sorted({str(d['symbol']) for d in selected}))}`",
        f"## F. Assets selected\n`{', '.join(sorted({str(d['symbol']) for d in selected}))}`",
        f"## G. Timeframes discovered\n`{', '.join(TARGET_TIMEFRAMES)}`",
        f"## H. Timeframes selected\n`{', '.join(sorted({str(d['timeframe_normalized']) for d in selected}))}`",
        "## I. Missing assets/timeframes\nSee dataset selection report.",
        f"## J. Unique parameter variants planned\n`{len(variants)}`",
        f"## K. Unique parameter variants completed\n`{len({r.get('parameter_hash') for r in rows})}`",
        f"## L. Total variant-window-split evaluations planned\n`{run_summary['planned']}`",
        f"## M. Total variant-window-split evaluations completed\n`{len(rows)}`",
        f"## N. Worker count\n`{run_summary['max_workers']}`",
        f"## O. Resume/de-dup status\nSkipped completed `{run_summary['skipped']}`; conflicts `{len(run_summary.get('conflicts', []))}`.",
        f"## P. Failed evaluations\n`{len(scored['failed'])}`",
        "## Q. Walk-forward method\n5 rolling windows for >=10000 rows; 4 for 5000-9999; 2 for 1500-4999; each split into train/validation/test.",
        f"## R. Per-asset result\nSee `cross_symbol/per_symbol_summary.csv`.",
        f"## S. Per-timeframe result\nSee `cross_timeframe/per_timeframe_summary.csv`.",
        f"## T. Per-regime result\nSee `regimes/regime_performance_summary.csv`.",
        f"## U. Robust strict candidates\n`{len(robust_strict)}`",
        f"## V. Robust medium candidates\n`{len(robust_medium)}`",
        f"## W. Top 20 research candidates\n```json\n{json.dumps(research[:20], indent=2, sort_keys=True)}\n```",
        f"## X. Best candidate full parameter table\n```json\n{json.dumps(scored['candidates'][:10], indent=2, sort_keys=True)}\n```",
        "## Y. Overfit candidates and why rejected\nSee `ranked/rejected_candidates.json`.",
        "## Z. Biggest optimization/data/runner problems\nSee `reports/PROBLEM_DISCOVERY_REPORT.md`.",
        "## AA. Code improvements needed\nContinue regime-level scoring integration and optimize runner throughput for millions of split evaluations.",
        "## AB. What should not be changed yet\nDo not enable guards/session/HTF/MACD/candle families from this research run alone.",
        "## AC. Next recommended prompt\nResume this run from `reports/optimization/big_overnight_multiasset/resume_registry.sqlite` until exhaustive core grid completes, then run exits_refinement_v1 around top candidates.",
    ]
    (out_root / "BIG_OVERNIGHT_OPTIMIZATION_REPORT.md").write_text("\n\n".join(report_lines) + "\n", encoding="utf-8")
    index = [
        "# Big Overnight Optimization Index",
        "",
        "- `BIG_OVERNIGHT_OPTIMIZATION_REPORT.md`",
        "- `dataset_selection.json`",
        "- `datasets/DATASET_SELECTION_REPORT.md`",
        "- `datasets/DATASET_QUALITY_REPORT.md`",
        "- `walkforward/walkforward_windows.csv`",
        "- `ranked/ranked_candidates.csv`",
        "- `ranked/robust_strict_candidates.csv`",
        "- `ranked/robust_medium_candidates.csv`",
        "- `ranked/research_only_candidates.csv`",
        "- `ranked/rejected_candidates.json`",
        "- `reports/RESUME_DEDUP_REPORT.md`",
    ]
    (out_root / "BIG_OVERNIGHT_OPTIMIZATION_INDEX.md").write_text("\n".join(index) + "\n", encoding="utf-8")
    return verdict


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--regimes", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--max-workers", default="auto")
    parser.add_argument("--time-budget-minutes", type=int, default=480)
    parser.add_argument("--max-assets", type=int, default=8)
    args = parser.parse_args()
    out_root = Path(args.out)
    for sub in ["power", "datasets", "profiles", "workers", "results", "ranked", "walkforward", "regimes", "cross_timeframe", "cross_symbol", "logs", "failures", "checkpoints", "reports"]:
        (out_root / sub).mkdir(parents=True, exist_ok=True)
    started_at = utc_now()
    (out_root / "run_started.txt").write_text(started_at + "\n", encoding="utf-8")
    manifest_path = Path(args.manifest)
    regime_path = Path(args.regimes)
    bundle = bundle_root_from_manifest(manifest_path)
    manifest = load_manifest(manifest_path)
    regimes = load_regime_registry(regime_path)
    selected, selection_summary = select_datasets(manifest, regimes, bundle, out_root, args.max_assets)
    if len({str(item["symbol"]) for item in selected}) < 5:
        (out_root / "PREFLIGHT_BLOCKED_REPORT.md").write_text("DATA_COVERAGE_BLOCKED: fewer than 5 usable assets.\n", encoding="utf-8")
        print(json.dumps({"verdict": "BIG_OVERNIGHT_OPTIMIZATION_BLOCKED_DATA_COVERAGE"}, indent=2))
        return 2
    selected, quality_failed = quality_check(selected, out_root)
    if len({str(item["symbol"]) for item in selected}) < 5:
        print(json.dumps({"verdict": "BIG_OVERNIGHT_OPTIMIZATION_BLOCKED_DATA_COVERAGE"}, indent=2))
        return 2
    for item in selected:
        regime = regimes.get(str(item["dataset_id"]), {})
        regime_file = Path(str(regime.get("regime_file", "")))
        if not regime_file.is_absolute():
            regime_file = bundle / regime_file
        item["regime_file_abs"] = str(regime_file)
    splits = create_walkforward(selected, out_root)
    variants = generate_variants()
    write_parameter_grid(out_root, variants)
    planned = len(variants) * len(splits)
    cpu = os.cpu_count() or 2
    max_workers = min(max(cpu - 1, 1), 6) if args.max_workers == "auto" else int(args.max_workers)
    run_config = {
        "started_at": started_at,
        "manifest": str(manifest_path),
        "regime_registry": str(regime_path),
        "bundle": str(bundle),
        "selected_assets": sorted({str(item["symbol"]) for item in selected}),
        "selected_dataset_count": len(selected),
        "walkforward_split_count": len(splits),
        "unique_parameter_variants": len(variants),
        "planned_evaluations": planned,
        "max_workers": max_workers,
        "time_budget_minutes": args.time_budget_minutes,
    }
    write_json(out_root / "run_config.json", run_config)
    (out_root / "worker_plan.md").write_text(f"# Worker Plan\n\n- Workers: `{max_workers}`\n- Planned evaluations: `{planned}`\n- Output layout: `workers/<worker_id>/<profile>/<dataset_id>/<window_id>/<split_type>/<evaluation_key>/`\n", encoding="utf-8")
    print(json.dumps(run_config, indent=2, sort_keys=True))
    run_summary = run_tasks(variants, splits, out_root, max_workers, args.time_budget_minutes)
    scored = score_and_write(run_summary["rows"], out_root)
    verdict = aggregate_reports(run_summary["rows"], scored, out_root, run_summary, selected, variants, splits, started_at, bundle)
    print(json.dumps({"verdict": verdict, "completed": len(run_summary["rows"]), "planned": planned}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
