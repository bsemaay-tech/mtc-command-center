import json
import pandas as pd
from pathlib import Path
from typing import List, Dict, Any, Optional

from src.optimizer_v0.search import run_single_trial, TrialResult, _make_param_key
import json
import pandas as pd
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta, timezone

from src.optimizer_v0.search import run_single_trial, TrialResult, _make_param_key, _worker_init
from src.config.defaults import MTCConfig

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

def _parse_dt(raw: str, *, as_end: bool = False) -> datetime:
    try:
        dt = datetime.fromisoformat(raw)
    except ValueError:
        # Fallback for simple date strings YYYY-MM-DD
        dt = datetime.strptime(raw, "%Y-%m-%d")
        
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
        
    if as_end:
        # End of day if time is 00:00:00
        if dt.hour == 0 and dt.minute == 0 and dt.second == 0:
            dt = dt + timedelta(days=1) - timedelta(microseconds=1)
    return dt

def load_data_for_replay(case_path: Path) -> tuple[pd.DataFrame, MTCConfig, int, Optional[datetime], Optional[datetime]]:
    """Load config and data for a case (replicates __main__.py logic)."""
    with open(case_path, encoding="utf-8") as f:
        case = json.load(f)

    # 1. Config
    base_config = MTCConfig.model_validate(case.get("config", {}))

    # 2. Data
    # Fix dataset path resolution: relative to PROJECT_ROOT/data
    dataset_name = case["dataset"]
    # Check if absolute or relative
    if Path(dataset_name).exists():
        dataset_path = Path(dataset_name)
    else:
        dataset_path = PROJECT_ROOT / "data" / dataset_name
        
    if not dataset_path.exists():
         # Try resolving relative to case file? No, standard is PROJECT_ROOT/data
         raise FileNotFoundError(f"Dataset not found: {dataset_path}")

    if dataset_path.suffix == ".parquet":
        df = pd.read_parquet(dataset_path)
    else:
        df = pd.read_csv(dataset_path)

    # Timestamp handling
    if "timestamp" in df.columns:
        if pd.api.types.is_numeric_dtype(df["timestamp"]):
            df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms", utc=True)
        else:
            df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
            
    if df["timestamp"].dt.tz is None:
        df["timestamp"] = df["timestamp"].dt.tz_localize("UTC")
    else:
        df["timestamp"] = df["timestamp"].dt.tz_convert("UTC")

    # Filter (keep semantics aligned with optimizer_v0.__main__.load_data)
    start_dt = _parse_dt(case["start_date"], as_end=False)
    end_dt = _parse_dt(case["end_date"], as_end=True)
    
    preroll_days = case.get("preroll_days", 90)
    filter_start = start_dt - timedelta(days=preroll_days) if preroll_days > 0 else start_dt
    
    mask = (df["timestamp"] >= filter_start) & (df["timestamp"] <= end_dt)
    df_filtered = df.loc[mask].copy().reset_index(drop=True)

    warmup_bars = case.get("warmup_bars", 200)
    eval_start = start_dt if preroll_days > 0 else None
    
    return df_filtered, base_config, warmup_bars, eval_start, end_dt

def load_candidate_files(directory: Path) -> List[Path]:
    """Load all .json files from directory, sorted lexicographically."""
    if not directory.exists():
        raise FileNotFoundError(f"Directory not found: {directory}")
    return sorted(list(directory.glob("*.json")))

def load_candidate_params(path: Path) -> Dict[str, Any]:
    """Read params from a candidate JSON file."""
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    # Support both raw params dict and candidate export format {"params": {...}}
    if "params" in data:
        return data["params"]
    return data

def run_replay_batch(
    case_path: Path,
    candidate_files: List[Path],
    out_csv: Path,
    min_trades: int = 5,
    max_dd_pct: float = 20.0
) -> None:
    """
    Run backtest for each candidate file and write results to CSV.
    Uses sequential execution (workers=1).
    """
    import datetime
    from datetime import timezone
    
    # 1. Load Base Config & Data (Once)
    print(f"Loading case: {case_path}")
    data, base_config, warmup_bars, eval_start, eval_end = load_data_for_replay(case_path)
    
    # Convert base_config to dict for run_single_trial
    # Preserve alias-backed fields such as use_sl/use_tp/enable flags when the
    # config is reconstructed inside run_single_trial.
    base_config_dict = base_config.model_dump(by_alias=True)
    
    # Initialize worker state (needed for run_single_trial)
    _worker_init(data)
    
    results = []
    
    print(f"Replaying {len(candidate_files)} candidates...")
    
    for i, cand_file in enumerate(candidate_files):
        try:
            params = load_candidate_params(cand_file)
            
            # Create a virtual "trial"
            # We don't have a real idx or seed from the original run easily available/verified,
            # so we treat this as a deterministic single run.
            # search.run_single_trial requires: (idx, params, data, base_config, min_trades, max_dd)
            
            res: TrialResult = run_single_trial(
                idx=i,
                params=params, 
                base_config_dict=base_config_dict,
                warmup_bars=warmup_bars,
                eval_start=eval_start,
                eval_end=eval_end,
                min_trades=min_trades,
                max_dd_pct=max_dd_pct
            )
            
            # Prepare row
            row = {
                "candidate_file": cand_file.name,
                "params_key": _make_param_key(params),
                "status": res.status,
                "net_profit": res.net_profit,
                "max_dd_pct": res.max_dd_pct,
                "total_trades": res.total_trades,
                "win_rate": res.win_rate,
                "profit_factor": res.profit_factor,
                "score": res.score,
                "prune_reason": res.prune_reason,
                "runtime_s": res.runtime_s
            }
            results.append(row)
            
            # Simple progress
            print(f"  [{i+1}/{len(candidate_files)}] {cand_file.name}: {res.status} (NP={res.net_profit:.2f}, DD={res.max_dd_pct:.2f}%)")
            
        except Exception as e:
            print(f"  [{i+1}/{len(candidate_files)}] {cand_file.name}: ERROR - {e}")
            results.append({
                "candidate_file": cand_file.name,
                "status": "ERROR",
                "prune_reason": str(e)
            })

    # Write CSV
    if results:
        df = pd.DataFrame(results)
        # Ensure column order relative stability
        cols = [
            "candidate_file", "status", "net_profit", "max_dd_pct", 
            "total_trades", "win_rate", "profit_factor", "score", 
            "prune_reason", "params_key"
        ]
        # details
        remaining = [c for c in df.columns if c not in cols]
        final_cols = cols + sorted(remaining)
        
        # Filter strictly
        df = df.reindex(columns=final_cols)
        
        out_csv.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(out_csv, index=False)
        print(f"Replay results written to: {out_csv}")
    else:
        print("No results generated.")
