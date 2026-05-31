"""
Grid and random search engine for MTC parameter optimization.

Calls the existing MTCRunner for each candidate config.
"""
from __future__ import annotations

import concurrent.futures
import copy
import itertools
import json
import os
import random
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional, Sequence

import pandas as pd

from ..config.defaults import MTCConfig
from ..engine.mtc_runner import MTCRunner


# ── param space definition ──────────────────────────────────────────

@dataclass
class ParamDef:
    """Single parameter range definition."""
    key: str          # dot-notation path, e.g. "supertrend.factor"
    low: float = 0.0
    high: float = 0.0
    step: float = 0.0
    dtype: Literal["float", "int"] = "float"
    choices: Optional[List[Any]] = None

    def grid_values(self) -> List[Any]:
        if self.choices is not None:
            return self.choices
        if self.step <= 0:
            return [self.low, self.high]
        vals = []
        v = self.low
        while v <= self.high + 1e-9:
            vals.append(int(v) if self.dtype == "int" else round(v, 6))
            v += self.step
        return vals

    def random_value(self, rng: random.Random) -> Any:
        if self.choices is not None:
            return rng.choice(self.choices)
        if self.dtype == "int":
            return rng.randint(int(self.low), int(self.high))
        if self.step > 0:
            # uniform_float with step: sample uniform then snap to nearest step within bounds
            val = rng.uniform(self.low, self.high)
            snapped = self.low + round((val - self.low) / self.step) * self.step
            snapped = max(self.low, min(snapped, self.high))
            return round(snapped, 6)
        return round(rng.uniform(self.low, self.high), 6)


# ── default param space ─────────────────────────────────────────────

DEFAULT_PARAMS: List[ParamDef] = [
    ParamDef("supertrend.factor",   2.0,  8.0,  0.5,  "float"),
    ParamDef("supertrend.atr_len",  10,   50,    5,    "int"),
    ParamDef("stop_loss.atr_mult",  2.0,  6.0,  0.5,  "float"),
    ParamDef("take_profit.atr_mult",1.5,  5.0,  0.5,  "float"),
]


# ── result row ──────────────────────────────────────────────────────

@dataclass
class TrialResult:
    idx: int
    params: Dict[str, Any]
    score: float
    net_profit: float
    max_dd_pct: float
    total_trades: int
    win_rate: float
    profit_factor: float
    runtime_s: float
    status: str = "OK"  # OK | PRUNED | ERROR
    prune_reason: str = ""
    min_trades_threshold: int = 0
    max_dd_threshold_pct: float = 0.0
    pruned_metric_value: float = 0.0



# ── config apply ────────────────────────────────────────────────────

def _apply_params(base: MTCConfig, params: Dict[str, Any]) -> MTCConfig:
    """Deep-copy base config and set params via dot-path keys."""
    # Preserve alias-backed fields such as stop_loss.use_sl when rebuilding
    # configs from a model instance; otherwise Pydantic falls back to defaults.
    d = base.model_dump(by_alias=True)
    for key, val in params.items():
        parts = key.split(".")
        target = d
        for p in parts[:-1]:
            target = target[p]
        target[parts[-1]] = val
    return MTCConfig.model_validate(d)


# ── worker state ────────────────────────────────────────────────────

_SHARED_DF: Optional[pd.DataFrame] = None

def _worker_init(df: pd.DataFrame) -> None:
    """Initialize worker process with shared dataframe to avoid pickling overhead."""
    global _SHARED_DF
    _SHARED_DF = df


def run_single_trial(
    idx: int,
    params: Dict[str, Any],
    base_config_dict: Dict[str, Any],
    warmup_bars: int,
    eval_start: Optional[datetime],
    eval_end: Optional[datetime],
    min_trades: int,
    max_dd_pct: float,
) -> TrialResult:
    """Top-level function for multiprocessing. 
    Reconstructs config and runs backtest using global _SHARED_DF.
    """
    t0 = time.time()
    
    # Defaults
    score = float("-inf")
    status = "PRUNED"
    prune_reason = ""
    pruned_value = 0.0
    
    m = {} 
    
    try:
        # Reconstruct base config
        base_config = MTCConfig.model_validate(base_config_dict)
        cfg = _apply_params(base_config, params)
        cfg.parity.export_debug_csv = False  # speed

        if _SHARED_DF is None:
            raise RuntimeError("Worker _SHARED_DF is None. Initializer failed?")

        runner = MTCRunner(cfg)
        results = runner.run(
            _SHARED_DF,
            warmup_bars=warmup_bars,
            eval_start=eval_start,
            eval_end=eval_end,
        )
        m = results["metrics"]
        
        # Extract metrics
        trades = m.get("total_trades", 0)
        dd_pct = abs(m.get("max_drawdown_pct", abs(m.get("max_drawdown", 0.0)))) # Handle fallback if pct missing
        net = m.get("net_profit", 0.0)
        dd = abs(m.get("max_drawdown", 0.0))
        
        # Calculate score and check bounds
        if trades < min_trades:
            prune_reason = "MIN_TRADES"
            pruned_value = float(trades)
        elif dd_pct > max_dd_pct:
            prune_reason = "MAX_DD_PCT"
            pruned_value = dd_pct
        else:
            if dd == 0:
                score = net
            else:
                score = net / dd
            
            # Check NaN
            if pd.isna(score) or pd.isna(net):
                score = float("-inf")
                prune_reason = "NAN_METRIC"
                pruned_value = 0.0
            else:
                status = "OK"

        return TrialResult(
            idx=idx,
            params=params,
            score=score,
            net_profit=net,
            max_dd_pct=dd_pct,
            total_trades=trades,
            win_rate=m.get("win_rate", 0.0),
            profit_factor=m.get("profit_factor", 0.0),
            runtime_s=round(time.time() - t0, 2),
            status=status,
            prune_reason=prune_reason,
            min_trades_threshold=min_trades,
            max_dd_threshold_pct=max_dd_pct,
            pruned_metric_value=pruned_value,
        )
    except Exception as e:
        return TrialResult(
            idx=idx, params=params, score=float("-inf"),
            net_profit=0, max_dd_pct=0, total_trades=0,
            win_rate=0, profit_factor=0,
            runtime_s=round(time.time() - t0, 2), 
            status=f"ERROR: {e}",
            prune_reason="EXCEPTION",
            min_trades_threshold=min_trades,
            max_dd_threshold_pct=max_dd_pct,
            pruned_metric_value=0.0
        )


def load_search_space(path: Path) -> tuple[List[ParamDef], List[ParamDef]]:
    """Load grid and random params from JSON with strict schema validation."""
    if not path.exists():
        raise FileNotFoundError(f"Search space file not found: {path}")

    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    
    grid_params = []
    random_params = []

    # 1. Parse Grid
    grid_data = data.get("grid", {})
    if not isinstance(grid_data, dict):
        raise ValueError("Search space 'grid' section must be a dictionary")

    for key, item in grid_data.items():
        if not isinstance(item, dict):
             raise ValueError(f"grid.{key}: must be an object")

        # Either values OR low/high/step
        choices = item.get("values")
        low = item.get("low")
        high = item.get("high")
        step = item.get("step")
        dtype_str = item.get("dtype", "float")

        if choices is not None:
             if not isinstance(choices, list) or len(choices) == 0:
                 raise ValueError(f"grid.{key}: values must be a non-empty list")
             # Use explicit values
             p = ParamDef(key=key, dtype=dtype_str, choices=choices)
        else:
             if low is None or high is None or step is None:
                 raise ValueError(f"grid.{key}: provide values or low/high/step")
             if step <= 0:
                 raise ValueError(f"grid.{key}: step must be > 0")
             
             p = ParamDef(
                 key=key, 
                 low=float(low), 
                 high=float(high), 
                 step=float(step), 
                 dtype=dtype_str
             )
        grid_params.append(p)

    # 2. Parse Random
    random_data = data.get("random", {})
    if not isinstance(random_data, dict):
        raise ValueError("Search space 'random' section must be a dictionary")

    for key, item in random_data.items():
        if not isinstance(item, dict):
             raise ValueError(f"random.{key}: must be an object")
             
        dist = item.get("dist")
        if not dist:
            raise ValueError(f"random.{key}: missing dist")
        
        if dist == "choice":
            vals = item.get("values")
            if not vals or not isinstance(vals, list):
                raise ValueError(f"random.{key}: dist 'choice' requires non-empty values")
            p = ParamDef(key=key, choices=vals)
        
        elif dist == "uniform_int":
            low = item.get("low")
            high = item.get("high")
            if low is None or high is None:
                raise ValueError(f"random.{key}: dist 'uniform_int' requires low and high")
            p = ParamDef(key=key, low=float(low), high=float(high), dtype="int")
            
        elif dist == "uniform_float":
            low = item.get("low")
            high = item.get("high")
            step = item.get("step", 0.0)
            if low is None or high is None:
                 raise ValueError(f"random.{key}: dist 'uniform_float' requires low and high")
            # step optional, if present must be > 0 checked in ParamDef? strict validation says step>0 if used
            if "step" in item and item["step"] <= 0:
                 raise ValueError(f"random.{key}: step must be > 0")
                 
            p = ParamDef(key=key, low=float(low), high=float(high), step=float(step), dtype="float")
        
        else:
            raise ValueError(f"random.{key}: unsupported dist={dist}")
            
        random_params.append(p)
            
    return grid_params, random_params


# ── search engines ──────────────────────────────────────────────────

# ── persistence helpers ─────────────────────────────────────────────

def _make_param_key(params: Dict[str, Any]) -> str:
    """Canonical string representation of params for deduplication.
    
    Normalizes floats to 6 decimal places to avoid fp string differences.
    """
    normalized = {}
    for k, v in params.items():
        if isinstance(v, float):
            normalized[k] = round(v, 6)
        else:
            normalized[k] = v
    return json.dumps(normalized, sort_keys=True)


def _get_resume_state(out_path: Path) -> set[str]:
    """Return set of param keys already present in the CSV."""
    seen = set()
    if not out_path.exists():
        return seen

    try:
        df = pd.read_csv(out_path)
        # Identify param columns: all cols except known result fields
        result_cols = {
            "idx", "score", "net_profit", "max_dd_pct", "total_trades",
            "win_rate", "profit_factor", "runtime_s", "status",
            "prune_reason", "min_trades_threshold", "max_dd_threshold_pct", "pruned_metric_value"
        }
        param_cols = [c for c in df.columns if c not in result_cols]
        
        for _, row in df.iterrows():
            # Reconstruct params dict
            p = {}
            for k in param_cols:
                val = row[k]
                # Handle numpy types
                if hasattr(val, "item"):
                    val = val.item()
                p[k] = val
            
            seen.add(_make_param_key(p))
    except Exception as e:
        print(f"WARNING: Failed to read resume state from {out_path}: {e}")
    
    return seen


def _append_result(result: TrialResult, out_path: Path, first_write: bool) -> None:
    """Append a single result directly to CSV."""
    row = {
        "idx": result.idx,
        "score": result.score if result.score > float("-inf") else None,
        "net_profit": result.net_profit,
        "max_dd_pct": result.max_dd_pct,
        "total_trades": result.total_trades,
        "win_rate": result.win_rate,
        "profit_factor": result.profit_factor,
        "runtime_s": result.runtime_s,
        "status": result.status,
        "prune_reason": result.prune_reason,
        "min_trades_threshold": result.min_trades_threshold,
        "max_dd_threshold_pct": result.max_dd_threshold_pct,
        "pruned_metric_value": result.pruned_metric_value,
    }
    row.update(result.params)

    # Use pandas to write a single row with header if needed
    df = pd.DataFrame([row])
    
    # Check if header is needed (if file doesn't exist or is empty)
    header = not out_path.exists() or (out_path.stat().st_size == 0)
    
    # Use 'a' mode to append. 
    df.to_csv(out_path, mode='a', header=header, index=False)


# ── search engines ──────────────────────────────────────────────────

def grid_search(
    df: pd.DataFrame,
    base_config: MTCConfig,
    param_defs: List[ParamDef],
    out_path: Optional[Path] = None,
    warmup_bars: int = 200,
    eval_start: Optional[datetime] = None,
    eval_end: Optional[datetime] = None,
    min_trades: int = 50,
    max_dd_pct: float = 40.0,
    workers: int = 1,
    store: Optional[Any] = None,
    run_id: Optional[str] = None,
) -> List[TrialResult]:
    """Exhaustive grid search over all param combinations."""
    names = [p.key for p in param_defs]
    grids = [p.grid_values() for p in param_defs]
    combos = list(itertools.product(*grids))
    print(f"Grid search: {len(combos)} combinations")
    print(f"Active Thresholds: min_trades={min_trades} | max_dd_pct={max_dd_pct}")

    # Load resume state
    seen_params = set()
    
    # Rule: If store provided, resume ONLY from DB
    if store and run_id:
        seen_params = store.fetch_seen_params(run_id)
        if seen_params:
             print(f"Resuming from DB with {len(seen_params)} already completed trials.")
    elif out_path:
        # Fallback to CSV resume
        out_path.parent.mkdir(parents=True, exist_ok=True)
        seen_params = _get_resume_state(out_path)
        if seen_params:
            print(f"Resuming from CSV with {len(seen_params)} already completed trials.")

    results: List[TrialResult] = []

    # Filter items to process
    tasks = []
    for i, vals in enumerate(combos):
        params = dict(zip(names, vals))
        param_key = _make_param_key(params)
        
        if param_key in seen_params:
            continue
        
        tasks.append((i, params))

    print(f"Executing {len(tasks)} trials with {workers} workers...")

    # Define helper to launch
    # Serialize with aliases so nested use_* flags survive worker rebuilds.
    base_config_dict = base_config.model_dump(by_alias=True)

    # Sequential execution
    if workers <= 1:
        # Initialize global state for sequential mode too, or just pass df directly if we used the old function.
        # But to unify logic, we can set _SHARED_DF locally or just use the extracted function if we set _SHARED_DF.
        # Let's just use the old in-place logic or the new function. 
        # Using new function requires _SHARED_DF. 
        _worker_init(df)
        
        for idx, params in tasks:
            r = run_single_trial(idx, params, base_config_dict, warmup_bars, eval_start, eval_end, min_trades, max_dd_pct)
            results.append(r)
            if out_path:
                _append_result(r, out_path, first_write=False)
            if store and run_id:
                store.upsert_trial(run_id, r)
            
            _log_progress(idx, len(combos), r, results)

    else:
        # Parallel execution
        with concurrent.futures.ProcessPoolExecutor(max_workers=workers, initializer=_worker_init, initargs=(df,)) as executor:
            # Use map to preserve order: it yields results in the order of tasks
            # tasks is list of (idx, params)
            
            # Prepare args for each task
            # map takes iterables. helpers must be partials or mapped.
            
            futures_args = [
                (idx, params, base_config_dict, warmup_bars, eval_start, eval_end, min_trades, max_dd_pct)
                for idx, params in tasks
            ]
            
            # wrapper to unpack args because executor.map passes one arg
            # or we can use submit and wait. 
            # Ideally use submit in a loop and collect futures, keeping order.
            
            # Actually executor.map supports multiple iterables if function takes multiple args, 
            # but run_single_trial takes many args.
            # simpler: use submit and store futures in a list, then iterate list.
            
            future_to_idx = {}
            ordered_futures = []
            
            for args_tuple in futures_args:
                f = executor.submit(run_single_trial, *args_tuple)
                ordered_futures.append(f)
            
            for f in ordered_futures:
                r = f.result()
                results.append(r)
                if out_path:
                    _append_result(r, out_path, first_write=False)
                if store and run_id:
                    store.upsert_trial(run_id, r)
                
                # Progress logging might be "bursty" if we wait for order, but it's correct.
                _log_progress(r.idx, len(combos), r, results)

    return results


def _log_progress(idx: int, total: int, r: TrialResult, all_results: List[TrialResult]) -> None:
    """Helper to print progress."""
    if len(all_results) % 10 == 0 or idx == total - 1:
        # Calculate best from current run's results
        current_best = max((r2.score for r2 in all_results if r2.status == 'OK'), default=float("-inf"))
        best_str = f"{current_best:.4f}" if current_best > float("-inf") else "None"
        
        # Estimate speed
        # Simple estimation based on runtime of last trial is not great for parallel.
        # But we don't have global start time easily passed here. 
        # Just print status.
        print(f"  [{idx+1}/{total}] Score: {r.score:.4f} (Best: {best_str}) | Net: {r.net_profit:.2f}")


def random_search(
    df: pd.DataFrame,
    base_config: MTCConfig,
    param_defs: List[ParamDef],
    out_path: Optional[Path] = None,
    n_iters: int = 200,
    seed: int = 42,
    warmup_bars: int = 200,
    eval_start: Optional[datetime] = None,
    eval_end: Optional[datetime] = None,
    min_trades: int = 50,
    max_dd_pct: float = 40.0,
    workers: int = 1,
    store: Optional[Any] = None,
    run_id: Optional[str] = None,
) -> List[TrialResult]:
    """Seeded random search."""
    rng = random.Random(seed)
    print(f"Random search: {n_iters} iterations (seed={seed})")
    print(f"Active Thresholds: min_trades={min_trades} | max_dd_pct={max_dd_pct}")

    # Load resume state
    seen_params = set()
    
    # Rule: If store provided, resume ONLY from DB
    if store and run_id:
        seen_params = store.fetch_seen_params(run_id)
        if seen_params:
             print(f"Resuming from DB with {len(seen_params)} already completed trials.")
    elif out_path:
        # Fallback to CSV resume
        out_path.parent.mkdir(parents=True, exist_ok=True)
        seen_params = _get_resume_state(out_path)
        if seen_params:
            print(f"Resuming from CSV with {len(seen_params)} already completed trials.")

    results: List[TrialResult] = []
    
    # Pre-generate all params deterministically in main process
    tasks = []
    for i in range(n_iters):
        params = {p.key: p.random_value(rng) for p in param_defs}
        param_key = _make_param_key(params)

        if param_key in seen_params:
            continue
            
        tasks.append((i, params))
        
    print(f"Executing {len(tasks)} trials with {workers} workers (seed={seed})...")

    base_config_dict = base_config.model_dump(by_alias=True)

    if workers <= 1:
        _worker_init(df)
        for idx, params in tasks:
            r = run_single_trial(idx, params, base_config_dict, warmup_bars, eval_start, eval_end, min_trades, max_dd_pct)
            results.append(r)
            if out_path:
                _append_result(r, out_path, first_write=False)
            if store and run_id:
                store.upsert_trial(run_id, r)
            _log_progress(idx, n_iters, r, results)
    else:
        with concurrent.futures.ProcessPoolExecutor(max_workers=workers, initializer=_worker_init, initargs=(df,)) as executor:
            # Preserve order using stored futures list
            futures = []
            for idx, params in tasks:
                f = executor.submit(
                    run_single_trial, 
                    idx, params, base_config_dict, warmup_bars, eval_start, eval_end, min_trades, max_dd_pct
                )
                futures.append(f)
            
            for f in futures:
                r = f.result()
                results.append(r)
                if out_path:
                    _append_result(r, out_path, first_write=False)
                if store and run_id:
                    store.upsert_trial(run_id, r)
                _log_progress(r.idx, n_iters, r, results)

    return results






def _sample_near_best(
    best_params: Dict[str, Any],
    param_defs: List[ParamDef],
    rng: random.Random,
) -> Dict[str, Any]:
    """Deterministic local proposal around current best params."""
    proposed: Dict[str, Any] = {}
    for p in param_defs:
        best_val = best_params.get(p.key)
        if p.choices is not None:
            if best_val is not None and rng.random() < 0.7:
                proposed[p.key] = best_val
            else:
                proposed[p.key] = rng.choice(p.choices)
            continue

        if p.dtype == "int":
            if best_val is None:
                proposed[p.key] = rng.randint(int(p.low), int(p.high))
                continue
            center = int(best_val)
            radius = max(1, int((p.high - p.low) * 0.15))
            lo = max(int(p.low), center - radius)
            hi = min(int(p.high), center + radius)
            proposed[p.key] = rng.randint(lo, hi)
            continue

        if best_val is None:
            proposed[p.key] = p.random_value(rng)
            continue
        center = float(best_val)
        step = p.step if p.step > 0 else max((p.high - p.low) / 20.0, 1e-6)
        lo = max(float(p.low), center - 3 * step)
        hi = min(float(p.high), center + 3 * step)
        val = rng.uniform(lo, hi)
        if p.step > 0:
            val = p.low + round((val - p.low) / p.step) * p.step
            val = max(p.low, min(val, p.high))
        proposed[p.key] = round(val, 6)

    return proposed


def bayes_search(
    df: pd.DataFrame,
    base_config: MTCConfig,
    param_defs: List[ParamDef],
    out_path: Optional[Path] = None,
    n_init: int = 20,
    n_iter: int = 50,
    seed: int = 42,
    warmup_bars: int = 200,
    eval_start: Optional[datetime] = None,
    eval_end: Optional[datetime] = None,
    min_trades: int = 50,
    max_dd_pct: float = 40.0,
    workers: int = 1,
    store: Optional[Any] = None,
    run_id: Optional[str] = None,
) -> List[TrialResult]:
    """Determinism-preserving two-phase optimizer."""
    if workers != 1:
        raise ValueError("bayes mode currently supports workers=1 only for determinism.")

    rng = random.Random(seed)
    total = max(0, n_init) + max(0, n_iter)
    print(f"Bayes search: init={n_init}, iter={n_iter}, total={total} (seed={seed}, workers=1)")
    print(f"Active Thresholds: min_trades={min_trades} | max_dd_pct={max_dd_pct}")

    seen_params = set()
    if store and run_id:
        seen_params = store.fetch_seen_params(run_id)
        if seen_params:
            print(f"Resuming from DB with {len(seen_params)} already completed trials.")
    elif out_path:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        seen_params = _get_resume_state(out_path)
        if seen_params:
            print(f"Resuming from CSV with {len(seen_params)} already completed trials.")

    results: List[TrialResult] = []
    base_config_dict = base_config.model_dump(by_alias=True)
    _worker_init(df)

    accepted = 0
    idx = 0
    while accepted < total:
        if accepted < n_init:
            params = {p.key: p.random_value(rng) for p in param_defs}
        else:
            ok = [r for r in results if r.status == "OK"]
            best_params = max(ok, key=lambda r: r.score).params if ok else {}
            params = _sample_near_best(best_params, param_defs, rng)

        param_key = _make_param_key(params)
        if param_key in seen_params:
            idx += 1
            continue

        r = run_single_trial(
            idx,
            params,
            base_config_dict,
            warmup_bars,
            eval_start,
            eval_end,
            min_trades,
            max_dd_pct,
        )
        results.append(r)
        seen_params.add(param_key)

        if out_path:
            _append_result(r, out_path, first_write=False)
        if store and run_id:
            store.upsert_trial(run_id, r)
        _log_progress(r.idx, total, r, results)

        accepted += 1
        idx += 1

    return results
# ── output ──────────────────────────────────────────────────────────

def results_to_csv(results: List[TrialResult], out_path: Path) -> Path:
    """Write results CSV. Returns path.
    
    DEPRECATED: Prefer incremental writing via _append_result.
    Kept for backward compatibility if user calls it manually.
    """
    rows = []
    for r in results:
        row = {
            "idx": r.idx,
            "score": r.score if r.score > float("-inf") else None,
            "net_profit": r.net_profit,
            "max_dd_pct": r.max_dd_pct,
            "total_trades": r.total_trades,
            "win_rate": r.win_rate,
            "profit_factor": r.profit_factor,
            "runtime_s": r.runtime_s,
            "status": r.status,
            "prune_reason": r.prune_reason,
            "min_trades_threshold": r.min_trades_threshold,
            "max_dd_threshold_pct": r.max_dd_threshold_pct,
            "pruned_metric_value": r.pruned_metric_value,
        }
        row.update(r.params)
        rows.append(row)

    df = pd.DataFrame(rows)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_path, index=False)
    return out_path


def print_top_n(results: List[TrialResult], n: int = 10) -> None:
    """Print detailed summary tables."""
    ok_trials = [r for r in results if r.status == "OK"]
    # Double check valid status
    ok_trials = [r for r in ok_trials if r.max_dd_pct <= r.max_dd_threshold_pct] # Safety filter
    
    ok_trials.sort(key=lambda x: x.score, reverse=True)
    
    pruned_trials = [r for r in results if r.status == "PRUNED"]
    errors = [r for r in results if r.status.startswith("ERROR")]

    print(f"\n{'='*100}")
    print(f"FINAL SUMMARY | Total: {len(results)} | OK: {len(ok_trials)} | PRUNED: {len(pruned_trials)} | ERRORS: {len(errors)}")
    print(f"{'='*100}")

    # 1. TOP PRUNED
    if pruned_trials:
        print(f"\n[{'TOP PRUNED TRIALS (Grouped by Reason)'}]")
        # Group by reason
        by_reason = {}
        for r in pruned_trials:
            reason = r.prune_reason or "UNKNOWN"
            by_reason.setdefault(reason, []).append(r)
        
        for reason, items in by_reason.items():
            count = len(items)
            # Sort by net_profit desc to see "best" pruned
            items.sort(key=lambda x: x.net_profit, reverse=True)
            subset = items[:5]
            
            print(f"\nReason: {reason:<15} (Count: {count})")
            print(f"  {'Net P&L':>10}  {'DD%':>7}  {'Trades':>6}  {'Limit':>6}  Params")
            print(f"  {'-'*75}")
            for r in subset:
                limit_val = r.max_dd_threshold_pct if "DD" in reason else r.min_trades_threshold
                if "NAN" in reason: limit_val = 0
                
                p_str = " ".join(f"{k}={v}" for k,v in r.params.items())
                print(f"  {r.net_profit:>10.2f}  {r.max_dd_pct:>6.1f}%  {r.total_trades:>6}  {limit_val:>6}  {p_str}")

    # 2. TOP OK
    print(f"\n[{f'TOP {min(n, len(ok_trials))} OK TRIALS'}]")
    if not ok_trials:
        print("  No OK trials found.")
    else:
        # Check if thresholds are consistent in the results (they should be same for all)
        # We can just read from the first one
        t_dd = ok_trials[0].max_dd_threshold_pct
        t_tr = ok_trials[0].min_trades_threshold
        
        print(f"  Filter Limits: min_trades={t_tr} | max_dd_pct={t_dd}")
        print(f"{'-'*110}")
        print(f"{'#':>3}  {'Score':>10}  {'Net P&L':>10}  {'DD%':>7}  {'Limit%':>6}  {'Trades':>6}  {'WR%':>6}  {'PF':>6}  Params")
        print(f"{'-'*110}")
        
        for i, r in enumerate(ok_trials[:n]):
            p_str = "  ".join(f"{k}={v}" for k, v in r.params.items())
            print(f"{i+1:>3}  {r.score:>10.4f}  {r.net_profit:>10.2f}  {r.max_dd_pct:>6.1f}%  {r.max_dd_threshold_pct:>6.1f}  {r.total_trades:>6}  {r.win_rate:>5.1f}%  {r.profit_factor:>5.2f}  {p_str}")
            
    print(f"{'='*100}\n")

