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


DEFAULT_BASE_CASE = (
    PROJECT_ROOT
    / "results"
    / "overnight"
    / "supertrend_4h_broad_20260311_123759"
    / "cases"
    / "filters_broad_full.json"
)
DEFAULT_SPACE = PROJECT_ROOT / "configs" / "spaces" / "supertrend_4h_confirmation_guards_20260311.json"
DEFAULT_DATASET = "BTCUSDT_PERP_4h_20210101_20260101.parquet"

_SHARED_YEAR_FRAMES: dict[int, pd.DataFrame] = {}


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


def _worker_init(year_frames: dict[int, pd.DataFrame]) -> None:
    global _SHARED_YEAR_FRAMES
    _SHARED_YEAR_FRAMES = year_frames


def _build_year_windows(
    df: pd.DataFrame,
    years: list[int],
    preroll_days: int,
) -> tuple[dict[int, pd.DataFrame], list[dict[str, Any]]]:
    frames: dict[int, pd.DataFrame] = {}
    windows: list[dict[str, Any]] = []

    for year in years:
        start = datetime(year, 1, 1, tzinfo=timezone.utc)
        end = datetime(year + 1, 1, 1, tzinfo=timezone.utc)
        filter_start = start - timedelta(days=preroll_days) if preroll_days > 0 else start
        mask = (df["timestamp"] >= filter_start) & (df["timestamp"] <= end)
        year_df = df.loc[mask].copy().reset_index(drop=True)
        if year_df.empty:
            raise ValueError(f"No rows found for year={year} with preroll={preroll_days}")
        frames[year] = year_df
        windows.append({"year": year, "eval_start": start, "eval_end": end})

    return frames, windows


def _evaluate_trial(
    idx: int,
    params: dict[str, Any],
    base_config_dict: dict[str, Any],
    windows: list[dict[str, Any]],
    warmup_bars: int,
    min_trades_per_year: int,
    min_total_trades: int,
    max_dd_pct: float,
    min_profitable_years: int,
    dd_penalty: float,
    trade_bonus: float,
    profitable_year_bonus: float,
    worst_year_net_weight: float,
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
        initial_capital = _safe_float(cfg.strategy.initial_capital, default=10000.0)

        yearly_rows: list[dict[str, Any]] = []
        for window in windows:
            runner = MTCRunner(cfg)
            results = runner.run(
                _SHARED_YEAR_FRAMES[int(window["year"])],
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
            yearly_rows.append(
                {
                    "year": int(window["year"]),
                    "net_profit": net_profit,
                    "net_profit_pct": net_profit_pct,
                    "max_dd_pct": abs(_safe_float(metrics.get("max_drawdown_pct", metrics.get("max_drawdown")))),
                    "profit_factor": _safe_float(metrics.get("profit_factor"), cap_inf=999.0),
                    "win_rate": _safe_float(metrics.get("win_rate")),
                    "total_trades": int(_safe_float(metrics.get("total_trades"))),
                }
            )

        total_net_profit = sum(item["net_profit"] for item in yearly_rows)
        total_net_profit_pct = sum(item["net_profit_pct"] for item in yearly_rows)
        worst_dd = max(item["max_dd_pct"] for item in yearly_rows)
        total_trades = sum(item["total_trades"] for item in yearly_rows)
        profitable_years = sum(1 for item in yearly_rows if item["net_profit"] > 0)
        min_year_trades = min(item["total_trades"] for item in yearly_rows)
        worst_year_net_profit_pct = min(item["net_profit_pct"] for item in yearly_rows)
        avg_profit_factor = sum(item["profit_factor"] for item in yearly_rows) / len(yearly_rows)
        avg_win_rate = sum(item["win_rate"] for item in yearly_rows) / len(yearly_rows)

        row.update(
            {
                "total_net_profit": round(total_net_profit, 6),
                "total_net_profit_pct": round(total_net_profit_pct, 6),
                "worst_dd_pct": round(worst_dd, 6),
                "total_trades": int(total_trades),
                "profitable_years": int(profitable_years),
                "avg_profit_factor": round(avg_profit_factor, 6),
                "avg_win_rate": round(avg_win_rate, 6),
                "min_year_trades": int(min_year_trades),
                "worst_year_net_profit_pct": round(worst_year_net_profit_pct, 6),
            }
        )

        for item in yearly_rows:
            prefix = f"y{item['year']}_"
            row[f"{prefix}net_profit"] = round(item["net_profit"], 6)
            row[f"{prefix}net_profit_pct"] = round(item["net_profit_pct"], 6)
            row[f"{prefix}max_dd_pct"] = round(item["max_dd_pct"], 6)
            row[f"{prefix}profit_factor"] = round(item["profit_factor"], 6)
            row[f"{prefix}win_rate"] = round(item["win_rate"], 6)
            row[f"{prefix}total_trades"] = int(item["total_trades"])

        if min_year_trades < min_trades_per_year:
            row["prune_reason"] = "MIN_TRADES_PER_YEAR"
        elif total_trades < min_total_trades:
            row["prune_reason"] = "MIN_TOTAL_TRADES"
        elif worst_dd > max_dd_pct:
            row["prune_reason"] = "MAX_DD_PCT"
        elif profitable_years < min_profitable_years:
            row["prune_reason"] = "MIN_PROFITABLE_YEARS"
        else:
            score = (
                total_net_profit_pct
                - (dd_penalty * worst_dd)
                + (trade_bonus * total_trades)
                + (profitable_year_bonus * profitable_years)
                + (worst_year_net_weight * worst_year_net_profit_pct)
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


def _append_row(path: Path, row: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame([row]).to_csv(path, mode="a", header=not path.exists(), index=False)


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
            "min_year_trades": best_row.get("min_year_trades"),
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


def _year_metrics_from_results(results: dict[str, Any]) -> dict[str, Any]:
    metrics = results.get("metrics", {})
    return {
        "net_profit": _safe_float(metrics.get("net_profit")),
        "net_profit_pct": _safe_float(metrics.get("net_profit_pct")),
        "max_drawdown_pct": abs(_safe_float(metrics.get("max_drawdown_pct", metrics.get("max_drawdown")))),
        "profit_factor": _safe_float(metrics.get("profit_factor"), cap_inf=999.0),
        "win_rate": _safe_float(metrics.get("win_rate")),
        "total_trades": int(_safe_float(metrics.get("total_trades"))),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Optimize Supertrend 4h parameters against a multi-year objective.")
    ap.add_argument("--base-case", default=str(DEFAULT_BASE_CASE))
    ap.add_argument("--space-file", default=str(DEFAULT_SPACE))
    ap.add_argument("--dataset", default=DEFAULT_DATASET)
    ap.add_argument("--years", default="2022,2023,2024")
    ap.add_argument("--holdout-year", type=int, default=2025)
    ap.add_argument("--mode", choices=["random", "grid"], default="random")
    ap.add_argument("--iters", type=int, default=3000)
    ap.add_argument("--workers", type=int, default=max(1, (os.cpu_count() or 2) - 1))
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--min-trades-per-year", type=int, default=12)
    ap.add_argument("--min-total-trades", type=int, default=45)
    ap.add_argument("--max-dd", type=float, default=40.0)
    ap.add_argument("--min-profitable-years", type=int, default=2)
    ap.add_argument("--dd-penalty", type=float, default=2.0)
    ap.add_argument("--trade-bonus", type=float, default=0.25)
    ap.add_argument("--profitable-year-bonus", type=float, default=5.0)
    ap.add_argument("--worst-year-net-weight", type=float, default=1.0)
    ap.add_argument("--top-k", type=int, default=50)
    ap.add_argument("--outdir", default="")
    args = ap.parse_args()

    base_case_path = _resolve_path(args.base_case)
    space_file_path = _resolve_path(args.space_file)
    base_case = _read_json(base_case_path)

    dataset_name = str(args.dataset)
    df = _load_dataset(dataset_name)
    years = [int(value.strip()) for value in str(args.years).split(",") if value.strip()]
    if not years:
        raise ValueError("At least one optimization year is required.")
    if args.holdout_year in years:
        raise ValueError("holdout year must be outside optimization years.")

    stamp = time.strftime("%Y%m%d_%H%M%S")
    outdir = (
        _resolve_path(args.outdir)
        if args.outdir
        else (PROJECT_ROOT / "results" / "multiyear" / f"supertrend_4h_confirm_{stamp}").resolve()
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
        "years": years,
        "holdout_year": args.holdout_year,
        "mode": args.mode,
        "iters": args.iters,
        "workers": args.workers,
        "seed": args.seed,
        "thresholds": {
            "min_trades_per_year": args.min_trades_per_year,
            "min_total_trades": args.min_total_trades,
            "max_dd_pct": args.max_dd,
            "min_profitable_years": args.min_profitable_years,
        },
        "weights": {
            "dd_penalty": args.dd_penalty,
            "trade_bonus": args.trade_bonus,
            "profitable_year_bonus": args.profitable_year_bonus,
            "worst_year_net_weight": args.worst_year_net_weight,
        },
    }
    _write_json(state_path, state)

    try:
        preroll_days = int(base_case.get("preroll_days", 365))
        warmup_bars = int(base_case.get("warmup_bars", 200))
        year_frames, windows = _build_year_windows(df, years, preroll_days)
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
            _worker_init(year_frames)
            iterator = (
                _evaluate_trial(
                    idx,
                    params,
                    base_config_dict,
                    windows,
                    warmup_bars,
                    args.min_trades_per_year,
                    args.min_total_trades,
                    args.max_dd,
                    args.min_profitable_years,
                    args.dd_penalty,
                    args.trade_bonus,
                    args.profitable_year_bonus,
                    args.worst_year_net_weight,
                )
                for idx, params in tasks
            )
            for result in iterator:
                _append_row(trials_path, result)
                all_rows.append(result)
                processed_since_write += 1
                if processed_since_write >= 25:
                    state.update(_summarize_progress(all_rows))
                    _write_json(state_path, state)
                    processed_since_write = 0
        else:
            with concurrent.futures.ProcessPoolExecutor(
                max_workers=args.workers,
                initializer=_worker_init,
                initargs=(year_frames,),
            ) as executor:
                futures = [
                    executor.submit(
                        _evaluate_trial,
                        idx,
                        params,
                        base_config_dict,
                        windows,
                        warmup_bars,
                        args.min_trades_per_year,
                        args.min_total_trades,
                        args.max_dd,
                        args.min_profitable_years,
                        args.dd_penalty,
                        args.trade_bonus,
                        args.profitable_year_bonus,
                        args.worst_year_net_weight,
                    )
                    for idx, params in tasks
                ]
                for future in concurrent.futures.as_completed(futures):
                    result = future.result()
                    _append_row(trials_path, result)
                    all_rows.append(result)
                    processed_since_write += 1
                    if processed_since_write >= 25:
                        state.update(_summarize_progress(all_rows))
                        _write_json(state_path, state)
                        processed_since_write = 0

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
                "thresholds": state["thresholds"],
                "weights": state["weights"],
                "scheduled_trials": state.get("scheduled_trials", 0),
                "completed_trials": len(trials_df),
                "ok_trials": 0,
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
        candidate_meta["worst_year_net_profit_pct"] = _safe_float(best_row.get("worst_year_net_profit_pct"))
        candidate_meta["min_year_trades"] = int(_safe_float(best_row.get("min_year_trades")))
        candidate_meta["profitable_years"] = int(_safe_float(best_row.get("profitable_years")))
        for year in years:
            prefix = f"y{year}_"
            candidate_meta[f"{prefix}net_profit"] = _safe_float(best_row.get(f"{prefix}net_profit"))
            candidate_meta[f"{prefix}net_profit_pct"] = _safe_float(best_row.get(f"{prefix}net_profit_pct"))
            candidate_meta[f"{prefix}max_dd_pct"] = _safe_float(best_row.get(f"{prefix}max_dd_pct"))
            candidate_meta[f"{prefix}total_trades"] = int(_safe_float(best_row.get(f"{prefix}total_trades")))

        best_params = best_candidate.get("params", {})
        holdout_case_path = _materialize_case(
            base_case,
            best_params,
            candidate_meta,
            cases_dir / "best_case_full.json",
            dataset_name,
            str(base_case["start_date"]),
            str(base_case["end_date"]),
            "supertrend_4h_multiyear_best_case_full",
        )

        annual_results: dict[str, Any] = {}
        for year in years + [args.holdout_year]:
            start_date = f"{year}-01-01T00:00:00"
            end_date = f"{year + 1}-01-01T00:00:00"
            annual_case_path = _materialize_case(
                base_case,
                best_params,
                candidate_meta,
                cases_dir / f"best_case_{year}.json",
                dataset_name,
                start_date,
                end_date,
                f"supertrend_4h_multiyear_best_case_{year}",
            )
            run_results = _run_case(annual_case_path, eval_dir / str(year))
            annual_results[str(year)] = {
                "case_path": str(annual_case_path),
                "artifacts_dir": str((eval_dir / str(year)).resolve()),
                "metrics": _year_metrics_from_results(run_results),
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
            "years": years,
            "holdout_year": args.holdout_year,
            "thresholds": state["thresholds"],
            "weights": state["weights"],
            "best_candidate_path": str(best_candidate_path),
            "best_case_path": str(holdout_case_path),
            "best_score": _safe_float(best_row.get("score")),
            "best_metrics": {
                "total_net_profit": _safe_float(best_row.get("total_net_profit")),
                "total_net_profit_pct": _safe_float(best_row.get("total_net_profit_pct")),
                "worst_dd_pct": _safe_float(best_row.get("worst_dd_pct")),
                "total_trades": int(_safe_float(best_row.get("total_trades"))),
                "profitable_years": int(_safe_float(best_row.get("profitable_years"))),
                "min_year_trades": int(_safe_float(best_row.get("min_year_trades"))),
                "worst_year_net_profit_pct": _safe_float(best_row.get("worst_year_net_profit_pct")),
                "avg_profit_factor": _safe_float(best_row.get("avg_profit_factor")),
                "avg_win_rate": _safe_float(best_row.get("avg_win_rate")),
            },
            "annual_results": annual_results,
            "ranking_csv": str(ranking_path),
            "trials_csv": str(trials_path),
        }
        _write_json(summary_path, payload)
        state["status"] = "PASS"
        state["best_candidate_path"] = str(best_candidate_path)
        state["best_case_path"] = str(holdout_case_path)
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
