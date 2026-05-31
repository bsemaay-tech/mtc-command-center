#!/usr/bin/env python3
"""
Multi-oracle normalized output comparator.

Compares normalized CSV files from two engines at a selected parity level.

Usage:
  python parity_oracles/compare/parity_compare.py \
    --baseline-dir examples/synthetic_outputs/baseline_python \
    --candidate-dir examples/synthetic_outputs/candidate_pinets \
    --level L2 \
    --out-md reports/synthetic_L2_compare.md \
    --out-json reports/synthetic_L2_compare.json
"""

from __future__ import annotations

import argparse, csv, json, math
from pathlib import Path
from datetime import datetime, timezone
from typing import Any

LEVEL_FILE = {
    "L0": "normalized_data.csv",
    "L1": "normalized_indicators.csv",
    "L2": "normalized_signals.csv",
    "L3": "normalized_signals.csv",
    "L4": "normalized_decisions.csv",
    "L5": "normalized_trades.csv",
    "L6": "normalized_stats.json",
}

KEYS = {
    "L0": ["timestamp"],
    "L1": ["timestamp", "indicator_name"],
    "L2": ["timestamp"],
    "L3": ["timestamp"],
    "L4": ["timestamp", "side"],
    "L5": ["trade_id"],
}

COMPARE_COLUMNS = {
    "L0": ["open", "high", "low", "close", "volume"],
    "L1": ["value"],
    "L2": ["bar_index", "raw_long", "raw_short", "final_long", "final_short", "reason_code"],
    "L3": ["bar_index", "final_long", "final_short", "reason_code"],
    "L4": ["bar_index", "entry_allowed", "blocked_reason", "position_before", "position_after"],
    "L5": ["timestamp", "bar_index", "event_type", "side", "qty", "price", "reason", "sl", "tp", "commission", "equity_after"],
}

def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))

def read_json(path: Path) -> Any:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))

def key_for(row: dict[str, str], cols: list[str]) -> tuple[str, ...]:
    return tuple(str(row.get(c, "")) for c in cols)

def maybe_float(s: Any):
    try:
        if s is None or s == "":
            return None
        return float(s)
    except Exception:
        return None

def values_equal(a: Any, b: Any, abs_tol=1e-8, rel_tol=1e-6) -> bool:
    fa, fb = maybe_float(a), maybe_float(b)
    if fa is not None and fb is not None:
        return math.isclose(fa, fb, abs_tol=abs_tol, rel_tol=rel_tol)
    return str(a) == str(b)

def compare_rows(base_rows, cand_rows, level: str, abs_tol: float, rel_tol: float):
    key_cols = KEYS[level]
    cmp_cols = COMPARE_COLUMNS[level]
    bmap = {key_for(r, key_cols): r for r in base_rows}
    cmap = {key_for(r, key_cols): r for r in cand_rows}

    all_keys = sorted(set(bmap) | set(cmap))
    mismatches = []
    matched = 0
    missing_in_candidate = []
    extra_in_candidate = []

    for k in all_keys:
        b = bmap.get(k)
        c = cmap.get(k)
        if b is None:
            extra_in_candidate.append(k)
            continue
        if c is None:
            missing_in_candidate.append(k)
            continue

        row_diffs = []
        for col in cmp_cols:
            if not values_equal(b.get(col, ""), c.get(col, ""), abs_tol=abs_tol, rel_tol=rel_tol):
                row_diffs.append({
                    "column": col,
                    "baseline": b.get(col, ""),
                    "candidate": c.get(col, "")
                })
        if row_diffs:
            mismatches.append({"key": k, "diffs": row_diffs, "baseline_row": b, "candidate_row": c})
        else:
            matched += 1

    return {
        "matched": matched,
        "mismatched": len(mismatches),
        "missing_in_candidate": len(missing_in_candidate),
        "extra_in_candidate": len(extra_in_candidate),
        "first_divergence": mismatches[0] if mismatches else None,
        "mismatches_sample": mismatches[:20],
        "missing_in_candidate_sample": missing_in_candidate[:20],
        "extra_in_candidate_sample": extra_in_candidate[:20],
    }

def compare_stats(base_stats: dict, cand_stats: dict, abs_tol: float, rel_tol: float):
    keys = sorted(set(base_stats) | set(cand_stats))
    diffs = []
    matched = 0
    for k in keys:
        if values_equal(base_stats.get(k, ""), cand_stats.get(k, ""), abs_tol, rel_tol):
            matched += 1
        else:
            diffs.append({"key": k, "baseline": base_stats.get(k), "candidate": cand_stats.get(k)})
    return {
        "matched": matched,
        "mismatched": len(diffs),
        "first_divergence": diffs[0] if diffs else None,
        "mismatches_sample": diffs[:50],
    }

def verdict(level: str, result: dict) -> str:
    if result.get("missing_input"):
        return "NOT_COMPARABLE"
    if result.get("mismatched", 0) == 0 and result.get("missing_in_candidate", 0) == 0 and result.get("extra_in_candidate", 0) == 0:
        return "PASS"
    if level == "L0": return "FAIL_DATA"
    if level == "L1": return "FAIL_INDICATOR"
    if level in {"L2", "L3"}: return "FAIL_SIGNAL"
    if level in {"L4", "L5"}: return "FAIL_EXECUTION"
    if level == "L6": return "FAIL_STATS"
    return "FAIL"

def md_report(payload: dict) -> str:
    r = payload["result"]
    lines = [
        f"# Multi-Oracle Parity Compare — {payload['level']}",
        "",
        f"- Baseline dir: `{payload['baseline_dir']}`",
        f"- Candidate dir: `{payload['candidate_dir']}`",
        f"- Compared file: `{payload['compared_file']}`",
        f"- Verdict: **{payload['verdict']}**",
        f"- Generated UTC: `{payload['generated_at_utc']}`",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "|---|---:|",
    ]
    for k in ["matched", "mismatched", "missing_in_candidate", "extra_in_candidate"]:
        if k in r:
            lines.append(f"| {k} | {r[k]} |")

    lines += ["", "## First divergence", ""]
    if r.get("first_divergence"):
        lines.append("```json")
        lines.append(json.dumps(r["first_divergence"], indent=2, ensure_ascii=False))
        lines.append("```")
    else:
        lines.append("No divergence detected.")

    lines += ["", "## Mismatch sample", ""]
    if r.get("mismatches_sample"):
        lines.append("```json")
        lines.append(json.dumps(r["mismatches_sample"][:5], indent=2, ensure_ascii=False))
        lines.append("```")
    else:
        lines.append("No mismatch sample.")
    return "\n".join(lines) + "\n"

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--baseline-dir", required=True)
    ap.add_argument("--candidate-dir", required=True)
    ap.add_argument("--level", required=True, choices=sorted(LEVEL_FILE))
    ap.add_argument("--out-md", required=True)
    ap.add_argument("--out-json", required=True)
    ap.add_argument("--abs-tol", type=float, default=1e-8)
    ap.add_argument("--rel-tol", type=float, default=1e-6)
    args = ap.parse_args()

    baseline_dir = Path(args.baseline_dir)
    candidate_dir = Path(args.candidate_dir)
    fname = LEVEL_FILE[args.level]
    bp = baseline_dir / fname
    cp = candidate_dir / fname

    if args.level == "L6":
        if not bp.exists() or not cp.exists():
            result = {"missing_input": True, "baseline_exists": bp.exists(), "candidate_exists": cp.exists()}
        else:
            result = compare_stats(read_json(bp), read_json(cp), args.abs_tol, args.rel_tol)
    else:
        if not bp.exists() or not cp.exists():
            result = {"missing_input": True, "baseline_exists": bp.exists(), "candidate_exists": cp.exists()}
        else:
            result = compare_rows(read_csv(bp), read_csv(cp), args.level, args.abs_tol, args.rel_tol)

    payload = {
        "level": args.level,
        "baseline_dir": str(baseline_dir),
        "candidate_dir": str(candidate_dir),
        "compared_file": fname,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "verdict": verdict(args.level, result),
        "result": result,
    }

    out_json = Path(args.out_json); out_json.parent.mkdir(parents=True, exist_ok=True)
    out_md = Path(args.out_md); out_md.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    out_md.write_text(md_report(payload), encoding="utf-8")

    print(f"Verdict: {payload['verdict']}")
    print(f"Wrote {out_json}")
    print(f"Wrote {out_md}")
    return 0 if payload["verdict"] in {"PASS"} else 2

if __name__ == "__main__":
    raise SystemExit(main())
