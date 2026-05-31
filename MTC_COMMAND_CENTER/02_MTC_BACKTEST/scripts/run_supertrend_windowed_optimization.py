from __future__ import annotations

import argparse
import concurrent.futures
import itertools
import json
import math
import os
import random
import subprocess
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import pandas as pd


SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.config.defaults import MTCConfig
from src.engine.mtc_runner import MTCRunner
from src.optimizer_v0.candidates import write_candidates
from src.optimizer_v0.search import ParamDef, load_search_space


DEFAULT_BASE_CASE = PROJECT_ROOT / "configs" / "cases" / "supertrend_1h_full_20260312.json"
DEFAULT_SPACE = PROJECT_ROOT / "configs" / "spaces" / "supertrend_1h_confirmation_guards_20260312.json"
DEFAULT_DATASET = "C:/LAB/tradingview-lab/110_/data/processed_hist/binance_usdm/BTCUSDT.P/1h.parquet"

_SHARED_WINDOW_FRAMES: dict[str, pd.DataFrame] = {}


def _resolve_path(path_like: str | Path) -> Path:
    path = Path(path_like)
    if path.is_absolute():
        return path.resolve()
    return (PROJECT_ROOT / path).resolve()


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def _safe_float(value: Any, *, default: float = 0.0, cap_inf: float | None = None) -> float:
    try:
        out = float(value)
    except (TypeError, ValueError):
        return default
    if math.isnan(out):
        return default
    if math.isinf(out):
        if cap_inf is not None:
            return cap_inf if out > 0 else -cap_inf
        return default
    return out


def _load_dataset(dataset_ref: str) -> pd.DataFrame:
    ref = str(dataset_ref).strip()
    candidates = [
        Path(ref),
        PROJECT_ROOT / ref,
        PROJECT_ROOT / "data" / ref,
    ]
    path = next((p.resolve() for p in candidates if p.exists()), None)
    if path is None:
        raise FileNotFoundError(f"Dataset not found: {dataset_ref}")

    if path.suffix == ".parquet":
        df = pd.read_parquet(path)
    elif path.suffix == ".csv":
        df = pd.read_csv(path)
    else:
        raise ValueError(f"Unsupported dataset format: {path.suffix}")

    if "timestamp" not in df.columns:
        if isinstance(df.index, pd.DatetimeIndex):
            df = df.reset_index()
            first_col = str(df.columns[0])
            if first_col != "timestamp":
                df = df.rename(columns={first_col: "timestamp"})
        elif "index" in df.columns:
            df = df.rename(columns={"index": "timestamp"})

    if "timestamp" not in df.columns:
        raise ValueError(f"Dataset has no timestamp axis: {path}")

    if pd.api.types.is_numeric_dtype(df["timestamp"]):
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms", utc=True)
    else:
        df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")

    if df["timestamp"].isna().any():
        raise ValueError(f"Dataset contains invalid timestamps: {path}")

    if df["timestamp"].dt.tz is None:
        df["timestamp"] = df["timestamp"].dt.tz_localize("UTC")
    else:
        df["timestamp"] = df["timestamp"].dt.tz_convert("UTC")

    return df.sort_values("timestamp").reset_index(drop=True)


def _parse_dt(raw: str) -> datetime:
    value = str(raw).strip()
    try:
        dt = datetime.fromisoformat(value)
    except ValueError:
        dt = datetime.strptime(value, "%Y-%m-%d")
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    else:
        dt = dt.astimezone(timezone.utc)
    return dt


def _iso_no_tz(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).replace(tzinfo=None).isoformat(timespec="seconds")


def _window_key(label: str) -> str:
    cleaned = "".join(ch if ch.isalnum() else "_" for ch in label.lower())
    while "__" in cleaned:
        cleaned = cleaned.replace("__", "_")
    return cleaned.strip("_")


def _make_param_key(params: dict[str, Any]) -> str:
    normalized: dict[str, Any] = {}
    for key, value in params.items():
        if isinstance(value, float):
            normalized[key] = round(value, 6)
        else:
            normalized[key] = value
    return json.dumps(normalized, sort_keys=True)


def _set_dot(target: dict[str, Any], key: str, value: Any) -> None:
    parts = key.split(".")
    cur = target
    for part in parts[:-1]:
        nxt = cur.get(part)
        if not isinstance(nxt, dict):
            nxt = {}
            cur[part] = nxt
        cur = nxt
    cur[parts[-1]] = value


def _apply_params(base: MTCConfig, params: dict[str, Any]) -> MTCConfig:
    payload = base.model_dump(by_alias=True)
    for key, value in params.items():
        _set_dot(payload, key, value)
    return MTCConfig.model_validate(payload)


def _worker_init(window_frames: dict[str, pd.DataFrame]) -> None:
    global _SHARED_WINDOW_FRAMES
    _SHARED_WINDOW_FRAMES = window_frames


def _build_windows(
    *,
    eval_start: datetime,
    eval_end: datetime,
    window_months: int,
    require_full_windows: bool,
) -> list[dict[str, Any]]:
    start_ts = pd.Timestamp(eval_start).tz_convert("UTC")
    end_ts = pd.Timestamp(eval_end).tz_convert("UTC")
    cur = start_ts
    windows: list[dict[str, Any]] = []
    idx = 0
    while cur < end_ts:
        next_boundary = cur + pd.DateOffset(months=window_months)
        if require_full_windows and next_boundary > end_ts:
            break
        effective_end = min(next_boundary, end_ts)
        if effective_end <= cur:
            break
        eval_end_inclusive = (effective_end - pd.Timedelta(seconds=1)).to_pydatetime()
        label = f"w{idx:02d}_{cur.strftime('%Y%m%d')}_{effective_end.strftime('%Y%m%d')}"
        windows.append(
            {
                "label": label,
                "eval_start": cur.to_pydatetime(),
                "eval_end": eval_end_inclusive,
                "boundary_end": effective_end.to_pydatetime(),
            }
        )
        cur = next_boundary
        idx += 1
    return windows


def _build_window_frames(
    df: pd.DataFrame,
    windows: list[dict[str, Any]],
    preroll_days: int,
) -> tuple[dict[str, pd.DataFrame], list[dict[str, Any]]]:
    frames: dict[str, pd.DataFrame] = {}
    accepted: list[dict[str, Any]] = []
    for window in windows:
        eval_start = window["eval_start"]
        eval_end = window["eval_end"]
        filter_start = eval_start - timedelta(days=preroll_days) if preroll_days > 0 else eval_start
        mask = (df["timestamp"] >= filter_start) & (df["timestamp"] <= eval_end)
        window_df = df.loc[mask].copy().reset_index(drop=True)
        eval_mask = (window_df["timestamp"] >= eval_start) & (window_df["timestamp"] <= eval_end)
        if window_df.empty or not eval_mask.any():
            continue
        frames[str(window["label"])] = window_df
        accepted.append(window)
    return frames, accepted


def _evaluate_trial(
    idx: int,
    params: dict[str, Any],
    base_config_dict: dict[str, Any],
    windows: list[dict[str, Any]],
    warmup_bars: int,
    min_trades_per_window: int,
    min_total_trades: int,
    max_dd_pct: float,
    min_profitable_windows: int,
    dd_penalty: float,
    trade_bonus: float,
    profitable_window_bonus: float,
    worst_window_net_weight: float,
) -> dict[str, Any]:
    started = time.time()
    row: dict[str, Any] = {
        "idx": idx,
        "param_key": _make_param_key(params),
        "status": "PRUNED",
        "prune_reason": "",
        "score": None,
        "runtime_s": 0.0,
        "error": "",
    }
    row.update(params)

    try:
        base_config = MTCConfig.model_validate(base_config_dict)
        cfg = _apply_params(base_config, params)
        cfg.parity.export_debug_csv = False
        if not cfg.trade.enable_long and not cfg.trade.enable_short:
            row["prune_reason"] = "NO_DIRECTION_ENABLED"
            row["runtime_s"] = round(time.time() - started, 2)
            return row
        if cfg.time_stop.enabled and not (cfg.time_stop.use_bars or cfg.time_stop.eod or cfg.time_stop.eow):
            row["prune_reason"] = "TIME_STOP_NO_TRIGGER"
            row["runtime_s"] = round(time.time() - started, 2)
            return row
        if cfg.trade.entry_mode == "Signal" and cfg.trade.signal_mode_max_entries > cfg.trade.max_pyramid_positions:
            row["prune_reason"] = "SIGNAL_ENTRIES_GT_PYRAMID"
            row["runtime_s"] = round(time.time() - started, 2)
            return row
        initial_capital = _safe_float(cfg.strategy.initial_capital, default=10000.0)

        window_rows: list[dict[str, Any]] = []
        for window in windows:
            runner = MTCRunner(cfg)
            results = runner.run(
                _SHARED_WINDOW_FRAMES[str(window["label"])],
                warmup_bars=warmup_bars,
                eval_start=window["eval_start"],
                eval_end=window["eval_end"],
            )
            metrics = results.get("metrics", {})
            net_profit = _safe_float(metrics.get("net_profit"))
            net_profit_pct = _safe_float(
                metrics.get("net_profit_pct"),
                default=(net_profit / initial_capital * 100.0) if initial_capital else 0.0,
            )
            window_rows.append(
                {
                    "label": str(window["label"]),
                    "net_profit": net_profit,
                    "net_profit_pct": net_profit_pct,
                    "max_dd_pct": abs(_safe_float(metrics.get("max_drawdown_pct", metrics.get("max_drawdown")))),
                    "profit_factor": _safe_float(metrics.get("profit_factor"), cap_inf=999.0),
                    "win_rate": _safe_float(metrics.get("win_rate")),
                    "total_trades": int(_safe_float(metrics.get("total_trades"))),
                }
            )

        total_net_profit = sum(item["net_profit"] for item in window_rows)
        total_net_profit_pct = sum(item["net_profit_pct"] for item in window_rows)
        worst_dd = max(item["max_dd_pct"] for item in window_rows)
        total_trades = sum(item["total_trades"] for item in window_rows)
        profitable_windows = sum(1 for item in window_rows if item["net_profit"] > 0)
        min_window_trades = min(item["total_trades"] for item in window_rows)
        worst_window_net_profit_pct = min(item["net_profit_pct"] for item in window_rows)
        avg_profit_factor = sum(item["profit_factor"] for item in window_rows) / len(window_rows)
        avg_win_rate = sum(item["win_rate"] for item in window_rows) / len(window_rows)

        row.update(
            {
                "total_net_profit": round(total_net_profit, 6),
                "total_net_profit_pct": round(total_net_profit_pct, 6),
                "worst_dd_pct": round(worst_dd, 6),
                "total_trades": int(total_trades),
                "profitable_windows": int(profitable_windows),
                "avg_profit_factor": round(avg_profit_factor, 6),
                "avg_win_rate": round(avg_win_rate, 6),
                "min_window_trades": int(min_window_trades),
                "worst_window_net_profit_pct": round(worst_window_net_profit_pct, 6),
            }
        )

        for item in window_rows:
            prefix = f"{_window_key(item['label'])}_"
            row[f"{prefix}net_profit"] = round(item["net_profit"], 6)
            row[f"{prefix}net_profit_pct"] = round(item["net_profit_pct"], 6)
            row[f"{prefix}max_dd_pct"] = round(item["max_dd_pct"], 6)
            row[f"{prefix}profit_factor"] = round(item["profit_factor"], 6)
            row[f"{prefix}win_rate"] = round(item["win_rate"], 6)
            row[f"{prefix}total_trades"] = int(item["total_trades"])

        if min_window_trades < min_trades_per_window:
            row["prune_reason"] = "MIN_TRADES_PER_WINDOW"
        elif total_trades < min_total_trades:
            row["prune_reason"] = "MIN_TOTAL_TRADES"
        elif worst_dd > max_dd_pct:
            row["prune_reason"] = "MAX_DD_PCT"
        elif profitable_windows < min_profitable_windows:
            row["prune_reason"] = "MIN_PROFITABLE_WINDOWS"
        else:
            score = (
                total_net_profit_pct
                - (dd_penalty * worst_dd)
                + (trade_bonus * total_trades)
                + (profitable_window_bonus * profitable_windows)
                + (worst_window_net_weight * worst_window_net_profit_pct)
            )
            row["score"] = round(score, 6)
            row["status"] = "OK"

        row["runtime_s"] = round(time.time() - started, 2)
        return row
    except Exception as exc:
        row["status"] = "ERROR"
        row["prune_reason"] = "EXCEPTION"
        row["error"] = str(exc)
        row["runtime_s"] = round(time.time() - started, 2)
        return row


def _write_rows(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(path, index=False)


def _load_seen_param_keys(path: Path) -> set[str]:
    if not path.exists():
        return set()
    df = pd.read_csv(path)
    if "param_key" not in df.columns:
        return set()
    return {str(value) for value in df["param_key"].dropna().tolist()}


def _to_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return bool(value)
    return str(value).strip().lower() in {"1", "true", "yes", "on"}


def _coerce_param_value(value: Any, param_def: ParamDef) -> Any:
    if pd.isna(value):
        return None
    if param_def.choices is not None and param_def.choices:
        sample = param_def.choices[0]
        if isinstance(sample, bool):
            return _to_bool(value)
        if isinstance(sample, int) and not isinstance(sample, bool):
            return int(float(value))
        if isinstance(sample, float):
            return float(value)
        return str(value)
    if param_def.dtype == "int":
        return int(float(value))
    return float(value)


def _param_dict_from_row(row: pd.Series, param_defs: list[ParamDef]) -> dict[str, Any]:
    params: dict[str, Any] = {}
    for param_def in param_defs:
        params[param_def.key] = _coerce_param_value(row[param_def.key], param_def)
    return params


def _build_random_tasks(
    param_defs: list[ParamDef],
    iters: int,
    seed: int,
    seen_param_keys: set[str],
) -> list[tuple[int, dict[str, Any]]]:
    rng = random.Random(seed)
    generated = set(seen_param_keys)
    tasks: list[tuple[int, dict[str, Any]]] = []
    for idx in range(iters):
        params = {param.key: param.random_value(rng) for param in param_defs}
        param_key = _make_param_key(params)
        if param_key in generated:
            continue
        generated.add(param_key)
        tasks.append((idx, params))
    return tasks


def _build_grid_tasks(param_defs: list[ParamDef], seen_param_keys: set[str]) -> list[tuple[int, dict[str, Any]]]:
    names = [param.key for param in param_defs]
    grids = [param.grid_values() for param in param_defs]
    tasks: list[tuple[int, dict[str, Any]]] = []
    for idx, values in enumerate(itertools.product(*grids)):
        params = dict(zip(names, values))
        if _make_param_key(params) in seen_param_keys:
            continue
        tasks.append((idx, params))
    return tasks


def _summarize_progress(rows: list[dict[str, Any]]) -> dict[str, Any]:
    ok_rows = [row for row in rows if row.get("status") == "OK"]
    best = None
    if ok_rows:
        best_row = max(
            ok_rows,
            key=lambda item: (
                _safe_float(item.get("score"), default=float("-inf")),
                _safe_float(item.get("total_net_profit"), default=float("-inf")),
                -_safe_float(item.get("worst_dd_pct"), default=float("inf")),
            ),
        )
        best = {
            "score": best_row.get("score"),
            "total_net_profit": best_row.get("total_net_profit"),
            "total_net_profit_pct": best_row.get("total_net_profit_pct"),
            "worst_dd_pct": best_row.get("worst_dd_pct"),
            "total_trades": best_row.get("total_trades"),
            "min_window_trades": best_row.get("min_window_trades"),
            "profitable_windows": best_row.get("profitable_windows"),
        }
    return {
        "completed_trials": len(rows),
        "ok_trials": sum(1 for row in rows if row.get("status") == "OK"),
        "pruned_trials": sum(1 for row in rows if row.get("status") == "PRUNED"),
        "error_trials": sum(1 for row in rows if row.get("status") == "ERROR"),
        "best_so_far": best,
    }


def _materialize_case(
    base_case: dict[str, Any],
    params: dict[str, Any],
    candidate_meta: dict[str, Any],
    out_path: Path,
    dataset_name: str,
    start_date: str,
    end_date: str,
    tag: str,
) -> Path:
    case_payload = json.loads(json.dumps(base_case))
    case_payload["dataset"] = dataset_name
    case_payload["start_date"] = start_date
    case_payload["end_date"] = end_date
    config_payload = case_payload.setdefault("config", {})
    for key, value in params.items():
        _set_dot(config_payload, key, value)
    case_payload["_candidate_selection"] = {
        "candidate_file": str(out_path.parent.parent / "candidates" / candidate_meta["candidate_file"]),
        "meta": candidate_meta,
        "applied_params": params,
    }
    feature_flags = case_payload.setdefault("feature_flags", {})
    feature_flags[f"materialized_candidate_{tag}"] = True
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(case_payload, indent=2, ensure_ascii=False), encoding="utf-8")
    return out_path


def _run_case(case_path: Path, artifacts_dir: Path) -> dict[str, Any]:
    cmd = [
        sys.executable,
        str(PROJECT_ROOT / "scripts" / "run_case.py"),
        str(case_path),
        "--artifacts-dir",
        str(artifacts_dir),
    ]
    proc = subprocess.run(cmd, cwd=str(PROJECT_ROOT), capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(
            f"run_case failed for {case_path.name} ({proc.returncode})\nSTDOUT:\n{proc.stdout}\nSTDERR:\n{proc.stderr}"
        )
    return _read_json(artifacts_dir / "results.json")


def _metrics_from_results(results: dict[str, Any]) -> dict[str, Any]:
    metrics = results.get("metrics", {})
    return {
        "net_profit": _safe_float(metrics.get("net_profit")),
        "net_profit_pct": _safe_float(metrics.get("net_profit_pct")),
        "max_drawdown_pct": abs(_safe_float(metrics.get("max_drawdown_pct", metrics.get("max_drawdown")))),
        "profit_factor": _safe_float(metrics.get("profit_factor"), cap_inf=999.0),
        "win_rate": _safe_float(metrics.get("win_rate")),
        "total_trades": int(_safe_float(metrics.get("total_trades"))),
    }


def _row_window_results(row: pd.Series, windows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for window in windows:
        key = _window_key(str(window["label"]))
        items.append(
            {
                "label": str(window["label"]),
                "start": _iso_no_tz(window["eval_start"]),
                "end": _iso_no_tz(window["eval_end"]),
                "net_profit": _safe_float(row.get(f"{key}_net_profit")),
                "net_profit_pct": _safe_float(row.get(f"{key}_net_profit_pct")),
                "max_dd_pct": _safe_float(row.get(f"{key}_max_dd_pct")),
                "profit_factor": _safe_float(row.get(f"{key}_profit_factor")),
                "win_rate": _safe_float(row.get(f"{key}_win_rate")),
                "total_trades": int(_safe_float(row.get(f"{key}_total_trades"))),
            }
        )
    return items


def main() -> int:
    ap = argparse.ArgumentParser(description="Optimize Supertrend against a multi-window objective.")
    ap.add_argument("--base-case", default=str(DEFAULT_BASE_CASE))
    ap.add_argument("--space-file", default=str(DEFAULT_SPACE))
    ap.add_argument("--dataset", default=DEFAULT_DATASET)
    ap.add_argument("--eval-start", required=True)
    ap.add_argument("--eval-end", required=True)
    ap.add_argument("--window-months", type=int, default=6)
    ap.add_argument("--require-full-windows", action="store_true")
    ap.add_argument("--holdout-start", default="")
    ap.add_argument("--holdout-end", default="")
    ap.add_argument("--mode", choices=["random", "grid"], default="random")
    ap.add_argument("--iters", type=int, default=300)
    ap.add_argument("--workers", type=int, default=max(1, (os.cpu_count() or 2) - 1))
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--min-trades-per-window", type=int, default=2)
    ap.add_argument("--min-total-trades", type=int, default=80)
    ap.add_argument("--max-dd", type=float, default=40.0)
    ap.add_argument("--min-profitable-windows", type=int, default=6)
    ap.add_argument("--dd-penalty", type=float, default=2.0)
    ap.add_argument("--trade-bonus", type=float, default=0.2)
    ap.add_argument("--profitable-window-bonus", type=float, default=4.0)
    ap.add_argument("--worst-window-net-weight", type=float, default=1.0)
    ap.add_argument("--top-k", type=int, default=40)
    ap.add_argument("--outdir", default="")
    args = ap.parse_args()

    base_case_path = _resolve_path(args.base_case)
    space_file_path = _resolve_path(args.space_file)
    base_case = _read_json(base_case_path)
    dataset_name = str(args.dataset)
    df = _load_dataset(dataset_name)
    eval_start = _parse_dt(args.eval_start)
    eval_end = _parse_dt(args.eval_end)
    if eval_start >= eval_end:
        raise ValueError("eval-start must be earlier than eval-end.")

    windows = _build_windows(
        eval_start=eval_start,
        eval_end=eval_end,
        window_months=args.window_months,
        require_full_windows=bool(args.require_full_windows),
    )
    if not windows:
        raise ValueError("No optimization windows generated.")

    holdout_start = _parse_dt(args.holdout_start) if args.holdout_start else None
    holdout_end = _parse_dt(args.holdout_end) if args.holdout_end else None
    if bool(holdout_start) ^ bool(holdout_end):
        raise ValueError("holdout-start and holdout-end must be provided together.")
    if holdout_start and holdout_end and holdout_start >= holdout_end:
        raise ValueError("holdout-start must be earlier than holdout-end.")

    stamp = time.strftime("%Y%m%d_%H%M%S")
    outdir = (
        _resolve_path(args.outdir)
        if args.outdir
        else (PROJECT_ROOT / "results" / "windowed" / f"supertrend_windowed_{stamp}").resolve()
    )
    candidates_dir = outdir / "candidates"
    cases_dir = outdir / "cases"
    eval_dir = outdir / "evaluations"
    trials_path = outdir / "trials.csv"
    ranking_path = outdir / "ranking.csv"
    state_path = outdir / "state.json"
    summary_path = outdir / "summary.json"
    outdir.mkdir(parents=True, exist_ok=True)
    candidates_dir.mkdir(parents=True, exist_ok=True)
    cases_dir.mkdir(parents=True, exist_ok=True)
    eval_dir.mkdir(parents=True, exist_ok=True)

    state = {
        "status": "RUNNING",
        "started_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "outdir": str(outdir),
        "base_case": str(base_case_path),
        "space_file": str(space_file_path),
        "dataset": dataset_name,
        "eval_start": _iso_no_tz(eval_start),
        "eval_end": _iso_no_tz(eval_end),
        "window_months": args.window_months,
        "require_full_windows": bool(args.require_full_windows),
        "mode": args.mode,
        "iters": args.iters,
        "workers": args.workers,
        "seed": args.seed,
        "thresholds": {
            "min_trades_per_window": args.min_trades_per_window,
            "min_total_trades": args.min_total_trades,
            "max_dd_pct": args.max_dd,
            "min_profitable_windows": args.min_profitable_windows,
        },
        "weights": {
            "dd_penalty": args.dd_penalty,
            "trade_bonus": args.trade_bonus,
            "profitable_window_bonus": args.profitable_window_bonus,
            "worst_window_net_weight": args.worst_window_net_weight,
        },
    }
    _write_json(state_path, state)

    try:
        preroll_days = int(base_case.get("preroll_days", 365))
        warmup_bars = int(base_case.get("warmup_bars", 200))
        window_frames, accepted_windows = _build_window_frames(df, windows, preroll_days)
        if not accepted_windows:
            raise ValueError("No optimization windows had usable data.")
        state["windows"] = [
            {
                "label": str(window["label"]),
                "start": _iso_no_tz(window["eval_start"]),
                "end": _iso_no_tz(window["eval_end"]),
            }
            for window in accepted_windows
        ]
        _write_json(state_path, state)

        base_config = MTCConfig.model_validate(base_case.get("config", {}))
        base_config_dict = base_config.model_dump(by_alias=True)
        grid_params, random_params = load_search_space(space_file_path)
        param_defs = grid_params if args.mode == "grid" else random_params
        if not param_defs:
            raise ValueError(f"No params found for mode={args.mode} in {space_file_path}")

        seen_param_keys = _load_seen_param_keys(trials_path)
        tasks = (
            _build_grid_tasks(param_defs, seen_param_keys)
            if args.mode == "grid"
            else _build_random_tasks(param_defs, args.iters, args.seed, seen_param_keys)
        )
        state["scheduled_trials"] = len(tasks)
        _write_json(state_path, state)

        existing_rows: list[dict[str, Any]] = []
        if trials_path.exists():
            existing_rows = pd.read_csv(trials_path).to_dict(orient="records")

        all_rows = list(existing_rows)
        processed_since_write = 0
        if args.workers <= 1:
            _worker_init(window_frames)
            iterator = (
                _evaluate_trial(
                    idx,
                    params,
                    base_config_dict,
                    accepted_windows,
                    warmup_bars,
                    args.min_trades_per_window,
                    args.min_total_trades,
                    args.max_dd,
                    args.min_profitable_windows,
                    args.dd_penalty,
                    args.trade_bonus,
                    args.profitable_window_bonus,
                    args.worst_window_net_weight,
                )
                for idx, params in tasks
            )
            for result in iterator:
                all_rows.append(result)
                processed_since_write += 1
                if processed_since_write >= 25:
                    _write_rows(trials_path, all_rows)
                    state.update(_summarize_progress(all_rows))
                    _write_json(state_path, state)
                    processed_since_write = 0
        else:
            with concurrent.futures.ProcessPoolExecutor(
                max_workers=args.workers,
                initializer=_worker_init,
                initargs=(window_frames,),
            ) as executor:
                futures = [
                    executor.submit(
                        _evaluate_trial,
                        idx,
                        params,
                        base_config_dict,
                        accepted_windows,
                        warmup_bars,
                        args.min_trades_per_window,
                        args.min_total_trades,
                        args.max_dd,
                        args.min_profitable_windows,
                        args.dd_penalty,
                        args.trade_bonus,
                        args.profitable_window_bonus,
                        args.worst_window_net_weight,
                    )
                    for idx, params in tasks
                ]
                for future in concurrent.futures.as_completed(futures):
                    result = future.result()
                    all_rows.append(result)
                    processed_since_write += 1
                    if processed_since_write >= 25:
                        _write_rows(trials_path, all_rows)
                        state.update(_summarize_progress(all_rows))
                        _write_json(state_path, state)
                        processed_since_write = 0

        _write_rows(trials_path, all_rows)
        state.update(_summarize_progress(all_rows))
        _write_json(state_path, state)

        trials_df = pd.read_csv(trials_path)
        ok_df = trials_df[trials_df["status"] == "OK"].copy() if "status" in trials_df.columns else pd.DataFrame()
        if ok_df.empty:
            payload = {
                "status": "EMPTY",
                "started_at": state["started_at"],
                "completed_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "outdir": str(outdir),
                "scheduled_trials": state.get("scheduled_trials", 0),
                "completed_trials": len(trials_df),
                "ok_trials": 0,
                "windows": state["windows"],
                "thresholds": state["thresholds"],
                "weights": state["weights"],
                "reason": "no_candidate_passed_thresholds",
            }
            _write_json(summary_path, payload)
            state["status"] = "EMPTY"
            _write_json(state_path, state)
            return 0

        ok_df = ok_df.sort_values(
            ["score", "total_net_profit", "worst_dd_pct", "param_key"],
            ascending=[False, False, True, True],
        ).reset_index(drop=True)
        ok_df.to_csv(ranking_path, index=False)

        candidate_items: list[dict[str, Any]] = []
        for _, row in ok_df.head(args.top_k).iterrows():
            params = _param_dict_from_row(row, param_defs)
            candidate_items.append(
                {
                    "idx": int(_safe_float(row.get("idx"))),
                    "status": "OK",
                    "score": _safe_float(row.get("score")),
                    "net_profit": _safe_float(row.get("total_net_profit")),
                    "dd_pct": _safe_float(row.get("worst_dd_pct")),
                    "win_rate": _safe_float(row.get("avg_win_rate")),
                    "pf": _safe_float(row.get("avg_profit_factor")),
                    "trades": int(_safe_float(row.get("total_trades"))),
                    "params": params,
                    "param_key": str(row.get("param_key")),
                }
            )

        written_candidates = write_candidates(
            candidate_items,
            {"source_pareto_path": str(trials_path), "run_id": None},
            candidates_dir,
            name_prefix="candidate",
            overwrite=True,
        )
        best_candidate_path = written_candidates[0]
        best_candidate = _read_json(best_candidate_path)
        best_row = ok_df.iloc[0]
        candidate_meta = dict(best_candidate.get("meta", {}))
        candidate_meta["candidate_file"] = best_candidate_path.name
        candidate_meta["score"] = _safe_float(best_row.get("score"))
        candidate_meta["total_net_profit_pct"] = _safe_float(best_row.get("total_net_profit_pct"))
        candidate_meta["worst_window_net_profit_pct"] = _safe_float(best_row.get("worst_window_net_profit_pct"))
        candidate_meta["min_window_trades"] = int(_safe_float(best_row.get("min_window_trades")))
        candidate_meta["profitable_windows"] = int(_safe_float(best_row.get("profitable_windows")))

        best_params = best_candidate.get("params", {})
        full_start = str(base_case.get("start_date") or _iso_no_tz(eval_start))
        full_end = str(base_case.get("end_date") or _iso_no_tz(holdout_end or eval_end))
        best_case_path = _materialize_case(
            base_case,
            best_params,
            candidate_meta,
            cases_dir / "best_case_full.json",
            dataset_name,
            full_start,
            full_end,
            "windowed_best_case_full",
        )
        full_results = _run_case(best_case_path, eval_dir / "full")

        holdout_result = None
        holdout_case_path = None
        if holdout_start and holdout_end:
            holdout_case_path = _materialize_case(
                base_case,
                best_params,
                candidate_meta,
                cases_dir / "best_case_holdout.json",
                dataset_name,
                _iso_no_tz(holdout_start),
                _iso_no_tz(holdout_end),
                "windowed_best_case_holdout",
            )
            holdout_run = _run_case(holdout_case_path, eval_dir / "holdout")
            holdout_result = {
                "case_path": str(holdout_case_path),
                "artifacts_dir": str((eval_dir / "holdout").resolve()),
                "metrics": _metrics_from_results(holdout_run),
            }

        payload = {
            "status": "PASS",
            "started_at": state["started_at"],
            "completed_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "outdir": str(outdir),
            "base_case": str(base_case_path),
            "space_file": str(space_file_path),
            "dataset": dataset_name,
            "mode": args.mode,
            "requested_iters": args.iters,
            "scheduled_trials": state.get("scheduled_trials", 0),
            "completed_trials": int(len(trials_df)),
            "ok_trials": int(len(ok_df)),
            "windows": state["windows"],
            "thresholds": state["thresholds"],
            "weights": state["weights"],
            "best_candidate_path": str(best_candidate_path),
            "best_case_path": str(best_case_path),
            "best_score": _safe_float(best_row.get("score")),
            "best_metrics": {
                "total_net_profit": _safe_float(best_row.get("total_net_profit")),
                "total_net_profit_pct": _safe_float(best_row.get("total_net_profit_pct")),
                "worst_dd_pct": _safe_float(best_row.get("worst_dd_pct")),
                "total_trades": int(_safe_float(best_row.get("total_trades"))),
                "profitable_windows": int(_safe_float(best_row.get("profitable_windows"))),
                "min_window_trades": int(_safe_float(best_row.get("min_window_trades"))),
                "worst_window_net_profit_pct": _safe_float(best_row.get("worst_window_net_profit_pct")),
                "avg_profit_factor": _safe_float(best_row.get("avg_profit_factor")),
                "avg_win_rate": _safe_float(best_row.get("avg_win_rate")),
            },
            "window_results": _row_window_results(best_row, accepted_windows),
            "full_result": {
                "case_path": str(best_case_path),
                "artifacts_dir": str((eval_dir / "full").resolve()),
                "metrics": _metrics_from_results(full_results),
            },
            "holdout_result": holdout_result,
            "ranking_csv": str(ranking_path),
            "trials_csv": str(trials_path),
        }
        _write_json(summary_path, payload)
        state["status"] = "PASS"
        state["best_candidate_path"] = str(best_candidate_path)
        state["best_case_path"] = str(best_case_path)
        if holdout_case_path is not None:
            state["best_holdout_case_path"] = str(holdout_case_path)
        state["completed_at"] = payload["completed_at"]
        _write_json(state_path, state)
        return 0
    except Exception as exc:
        state["status"] = "FAIL"
        state["error"] = str(exc)
        state["failed_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        _write_json(state_path, state)
        raise


if __name__ == "__main__":
    raise SystemExit(main())
