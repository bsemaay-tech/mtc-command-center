from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


RESERVED = {
    "idx",
    "score",
    "net_profit",
    "max_dd_pct",
    "max_dd_threshold_pct",
    "total_trades",
    "win_rate",
    "profit_factor",
    "status",
    "prune_reason",
    "runtime_s",
    "params_key",
}


def _coerce(value: str) -> Any:
    v = value.strip()
    if v == "":
        return None
    low = v.lower()
    if low == "true":
        return True
    if low == "false":
        return False
    try:
        if "." not in v and "e" not in low:
            return int(v)
    except Exception:
        pass
    try:
        return float(v)
    except Exception:
        return v


def _set_dot(cfg: dict[str, Any], key: str, value: Any) -> None:
    parts = key.split(".")
    cur = cfg
    for p in parts[:-1]:
        nxt = cur.get(p)
        if not isinstance(nxt, dict):
            nxt = {}
            cur[p] = nxt
        cur = nxt
    cur[parts[-1]] = value


def main() -> int:
    ap = argparse.ArgumentParser(description="Select best optimizer trial and materialize a new case JSON.")
    ap.add_argument("--base-case", required=True)
    ap.add_argument("--trials-csv", required=True)
    ap.add_argument("--out-case", required=True)
    ap.add_argument("--min-trades", type=int, default=0)
    ap.add_argument("--max-dd", type=float, default=None)
    ap.add_argument("--min-pf", type=float, default=None)
    ap.add_argument("--tag", default="")
    args = ap.parse_args()

    base_case_path = Path(args.base_case)
    trials_path = Path(args.trials_csv)
    out_path = Path(args.out_case)

    case = json.loads(base_case_path.read_text(encoding="utf-8"))

    best_row = None
    with trials_path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get("status") != "OK":
                continue
            trades = int(float(row.get("total_trades") or 0))
            dd = float(row.get("max_dd_pct") or 0.0)
            pf_raw = row.get("profit_factor")
            pf = float(pf_raw) if pf_raw not in (None, "", "nan") else None
            score_raw = row.get("score")
            score = float(score_raw) if score_raw not in (None, "", "nan") else float("-inf")
            if trades < args.min_trades:
                continue
            if args.max_dd is not None and dd > args.max_dd:
                continue
            if args.min_pf is not None and (pf is None or pf < args.min_pf):
                continue
            row["_score"] = score
            row["_dd"] = dd
            row["_pf"] = pf if pf is not None else float("-inf")
            if best_row is None:
                best_row = row
                continue
            if (row["_score"], float(row.get("net_profit") or 0.0), -row["_dd"], row["_pf"]) > (
                best_row["_score"],
                float(best_row.get("net_profit") or 0.0),
                -best_row["_dd"],
                best_row["_pf"],
            ):
                best_row = row

    if best_row is None:
        raise SystemExit("No eligible optimizer trial found.")

    params = {}
    for key, value in best_row.items():
        if key in RESERVED or key.startswith("_"):
            continue
        if "." not in key:
            continue
        params[key] = _coerce(value)

    for key, value in params.items():
        _set_dot(case.setdefault("config", {}), key, value)

    feature_flags = case.setdefault("feature_flags", {})
    feature_flags["materialized_from_optimizer_trial"] = True
    if args.tag:
        feature_flags[f"optimizer_stage_{args.tag}"] = True
    case["_optimizer_selection"] = {
        "trials_csv": str(trials_path),
        "selected_score": best_row["_score"],
        "selected_net_profit": float(best_row.get("net_profit") or 0.0),
        "selected_max_dd_pct": best_row["_dd"],
        "selected_total_trades": int(float(best_row.get("total_trades") or 0)),
        "selected_profit_factor": best_row["_pf"] if best_row["_pf"] != float("-inf") else None,
        "selected_params": params,
    }

    if args.tag:
        case["strategy_id"] = f"{case.get('strategy_id', 'mtc')}_{args.tag}"

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(case, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"materialized_case={out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
