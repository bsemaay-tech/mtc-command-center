import json
import hashlib
from pathlib import Path
from typing import List, Dict, Any

def load_pareto(path: Path) -> Dict[str, Any]:
    """Load Pareto JSON file."""
    if not path.exists():
        raise FileNotFoundError(f"Pareto file not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def stable_shortkey(param_key: str) -> str:
    """Generate 12-char stable hash of param_key."""
    # SHA1 is stable across platforms/runs
    return hashlib.sha1(param_key.encode("utf-8")).hexdigest()[:12]

def select_candidates(payload: Dict[str, Any], top_k: int, include_pruned: bool) -> List[Dict[str, Any]]:
    """Select top-K candidates from Pareto payload."""
    items = payload.get("items", [])
    
    # 1. Filter
    filtered = []
    for item in items:
        status = item.get("status", "UNKNOWN")
        if not include_pruned and status == "PRUNED":
            continue
        filtered.append(item)
        
    # 2. Sort (Defensive, assuming Pareto JSON might be raw)
    # Sort order:
    # 1) dd_pct ASC (Minimize risk)
    # 2) net_profit DESC (Maximize return)
    # 3) param_key ASC (Tie-breaker)
    def sort_key(x):
        dd = float(x.get("dd_pct") or float("inf"))
        np = float(x.get("net_profit") or float("-inf"))
        pk = str(x.get("param_key", ""))
        return (dd, -np, pk)
        
    filtered.sort(key=sort_key)
    
    # 3. Top K
    if top_k > 0:
        return filtered[:top_k]
    return filtered

def write_candidates(
    candidates: List[Dict[str, Any]], 
    payload_meta: Dict[str, Any],
    outdir: Path, 
    name_prefix: str, 
    overwrite: bool
) -> List[Path]:
    """Write individual candidate files."""
    if not outdir.exists():
        outdir.mkdir(parents=True, exist_ok=True)
        
    written_files = []
    
    for i, cand in enumerate(candidates):
        rank = i + 1
        pk = cand.get("param_key", "")
        short = stable_shortkey(pk)
        dd = float(cand.get("dd_pct") or 0.0)
        np = float(cand.get("net_profit") or 0.0)
        
        # Formatting:
        # ddpct: 2 decimals, replace '.' with '_'
        dd_str = f"{dd:.2f}".replace(".", "_")
        
        # net: 2 decimals, replace '.' with '_', and '-' with 'm'
        net_str = f"{np:.2f}".replace(".", "_").replace("-", "m")
        
        # Filename: <prefix>_<rank>__ddpct_<dd>__net_<net>__key_<key>.json
        filename = f"{name_prefix}_{rank:03d}__ddpct_{dd_str}__net_{net_str}__key_{short}.json"
        
        # Sanitize filename (just in case)
        filename = filename.replace(":", "").replace("/", "")
        
        out_path = outdir / filename
        
        if out_path.exists() and not overwrite:
            # Check content? No, stricter guardrail: if file exists and no overwrite, fail.
            raise FileExistsError(f"Candidate file already exists and --overwrite not set: {out_path}")
            
        # Construct content
        content = {
            "meta": {
                "source_pareto": str(payload_meta.get("source_pareto_path", "unknown")),
                "run_id": payload_meta.get("run_id"),
                "rank": rank,
                "param_key": pk,
                "net_profit": np,
                "dd_pct": dd,
                "trades": cand.get("trades"),
                "pf": cand.get("pf"),
                "win_rate": cand.get("win_rate")
            },
            "params": cand.get("params", {})
        }
        
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(content, f, indent=2, sort_keys=True)
            
        written_files.append(out_path)
        
    return written_files
