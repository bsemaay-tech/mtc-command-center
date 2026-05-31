import json
import sqlite3
import pandas as pd
from pathlib import Path
from typing import List, Dict, Any, Sequence, Tuple

_MAXIMIZE_DEFAULT = ("net_profit",)
_MINIMIZE_DEFAULT = ("max_dd_pct",)


def _metric_value(item: Dict[str, Any], metric: str) -> float:
    """Resolve metric aliases and return float value."""
    aliases = {
        "max_dd_pct": ("max_dd_pct", "dd_pct"),
        "dd_pct": ("dd_pct", "max_dd_pct"),
        "profit_factor": ("profit_factor", "pf"),
        "total_trades": ("total_trades", "trades"),
    }
    keys = aliases.get(metric, (metric,))
    for key in keys:
        if key in item and item[key] is not None:
            return float(item[key])
    raise KeyError(metric)


def compute_pareto(
    items: List[Dict[str, Any]],
    maximize: Sequence[str] = _MAXIMIZE_DEFAULT,
    minimize: Sequence[str] = _MINIMIZE_DEFAULT,
) -> List[Dict[str, Any]]:
    """
    Compute Pareto frontier for arbitrary maximize/minimize objectives.
    Input: list of dicts with numeric objective fields.
    Output: list of dicts used in optimal set.
    """
    maximize = tuple(maximize)
    minimize = tuple(minimize)

    # Filter valid
    valid_items = []
    for item in items:
        values: Dict[str, float] = {}
        try:
            for m in maximize:
                values[m] = _metric_value(item, m)
            for m in minimize:
                values[m] = _metric_value(item, m)
        except (ValueError, TypeError, KeyError):
            continue

        # Keep compatibility keys for existing exports/tests.
        normalized = dict(item)
        if "max_dd_pct" in values:
            normalized["dd_pct"] = values["max_dd_pct"]
        valid_items.append(normalized)

    def sort_key(x):
        key_parts: List[float | str | int] = []
        for m in minimize:
            key_parts.append(_metric_value(x, m))
        for m in maximize:
            key_parts.append(-_metric_value(x, m))
        key_parts.append(str(x.get("param_key", "")))
        key_parts.append(int(x.get("idx", 0)))
        return tuple(key_parts)

    valid_items.sort(key=sort_key)

    def dominates(a: Dict[str, Any], b: Dict[str, Any]) -> bool:
        any_strict = False
        for m in maximize:
            av = _metric_value(a, m)
            bv = _metric_value(b, m)
            if av < bv:
                return False
            if av > bv:
                any_strict = True
        for m in minimize:
            av = _metric_value(a, m)
            bv = _metric_value(b, m)
            if av > bv:
                return False
            if av < bv:
                any_strict = True
        return any_strict

    pareto_frontier: List[Dict[str, Any]] = []
    for i, candidate in enumerate(valid_items):
        dominated = False
        for j, other in enumerate(valid_items):
            if i == j:
                continue
            if dominates(other, candidate):
                dominated = True
                break
        if not dominated:
            pareto_frontier.append(candidate)

    pareto_frontier.sort(key=sort_key)
    return pareto_frontier


def load_trials_from_db(db_path: Path, run_id: str, include_pruned: bool) -> List[Dict[str, Any]]:
    """Fetch trials from DB and flatten structure."""
    if not db_path.exists():
        raise FileNotFoundError(f"DB not found: {db_path}")

    trials = []
    with sqlite3.connect(db_path) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.execute(
            "SELECT idx, params_json, metrics_json, status, prune_reason, runtime_s, params_key FROM trials WHERE run_id = ?", 
            (run_id,)
        )
        rows = cursor.fetchall()
        
    for row in rows:
        r = dict(row)
        if not include_pruned and r["status"] == "PRUNED":
            continue
            
        metrics = json.loads(r["metrics_json"]) if r["metrics_json"] else {}
        params = json.loads(r["params_json"]) if r["params_json"] else {}
        
        # Flatten
        item = {
            "idx": r["idx"],
            "status": r["status"],
            "prune_reason": r["prune_reason"],
            "runtime_s": r["runtime_s"],
            "params_key": r["params_key"],
            "params": params,
            **metrics # Expand net_profit, dd_pct, etc.
        }
        if "max_dd_pct" in item and "dd_pct" not in item:
            item["dd_pct"] = item["max_dd_pct"]
        trials.append(item)
        
    return trials

def load_trials_from_csv(csv_path: Path, include_pruned: bool) -> List[Dict[str, Any]]:
    """Fetch trials from CSV."""
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV not found: {csv_path}")
        
    df = pd.read_csv(csv_path)
    trials = []
    
    for _, row in df.iterrows():
        r = row.to_dict()
        if not include_pruned and r.get("status") == "PRUNED":
            continue
            
        # Reconstruct params ??
        # In CSV, params are columns not in reserved list.
        # See search.py _get_resume_state for logic
        
        # Simplified: We just need metrics for pareto. 
        # But user wants "params" dict in JSON output.
        # So we must reconstruct params dict.
        
        reserved = {
            "idx", "score", "net_profit", "max_dd_pct", "total_trades",
            "win_rate", "profit_factor", "runtime_s", "status",
            "prune_reason", "min_trades_threshold", "max_dd_threshold_pct", "pruned_metric_value"
        }
        
        params = {}
        for k, v in r.items():
            if k not in reserved:
                # pandas loads as floats/ints
                if hasattr(v, "item"): v = v.item()
                if pd.isna(v): continue
                params[k] = v
                
        # param_key needed for determinism
        # We can implement a local make_key or re-import
        # Let's just use empty string if we can't easily make it, 
        # OR import _make_param_key from search.py (circular import risk?)
        # search.py imports nothing from pareto.py, so it is safe.
        
        item = {
            "idx": int(r.get("idx", -1)),
            "status": r.get("status"),
            "net_profit": r.get("net_profit"),
            "dd_pct": r.get("max_dd_pct"),  # Map CSV col name
            # Map other fields
            "trades": r.get("total_trades"),
            "win_rate": r.get("win_rate"),
            "pf": r.get("profit_factor"),
            "params": params
        }
        trials.append(item)
        
    return trials

def write_pareto_json(path: Path, payload: Dict[str, Any]) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, sort_keys=True)
