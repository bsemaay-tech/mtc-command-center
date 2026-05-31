from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from parity_oracles.common.io_utils import ROOT, git_code_hash, read_csv, read_json, sha256_file, sha256_json, write_json


LEVEL_FILES = {
    "L0": "normalized_data.csv",
    "L1": "normalized_indicators.csv",
    "L2": "normalized_signals.csv",
    "L3": "normalized_signals.csv",
    "L4": "normalized_decisions.csv",
    "L5": "normalized_trades.csv",
    "L6": "normalized_stats.json",
}


def engine_dir(case_id: str, engine: str) -> Path:
    return ROOT / "reports" / "parity" / case_id / engine


def comparable_value(field: str, baseline: str, candidate: str, abs_tol: float, rel_tol: float) -> bool:
    if baseline == candidate:
        return True
    if baseline == "" or candidate == "":
        return False
    try:
        left = float(baseline)
        right = float(candidate)
    except ValueError:
        return baseline == candidate
    return math.isclose(left, right, abs_tol=abs_tol, rel_tol=rel_tol)


def compare_rows(
    baseline_rows: list[dict[str, str]],
    candidate_rows: list[dict[str, str]],
    level: str,
    abs_tol: float,
    rel_tol: float,
) -> dict[str, Any]:
    key = "timestamp" if level in {"L0", "L1", "L2", "L3", "L4"} else "trade_id"
    if level == "L1":
        key = "timestamp|indicator_name"
    baseline_map = {row_key(row, key): row for row in baseline_rows}
    candidate_map = {row_key(row, key): row for row in candidate_rows}
    missing = sorted(set(baseline_map) - set(candidate_map))
    extra = sorted(set(candidate_map) - set(baseline_map))
    mismatches = []
    matched = 0
    for item_key in sorted(set(baseline_map) & set(candidate_map)):
        left = baseline_map[item_key]
        right = candidate_map[item_key]
        fields = sorted(set(left) | set(right))
        diffs = []
        for field in fields:
            if field in {"reason_code", "blocked_reason"} and level in {"L1", "L2", "L3"}:
                continue
            if not comparable_value(field, left.get(field, ""), right.get(field, ""), abs_tol, rel_tol):
                diffs.append({"field": field, "baseline": left.get(field, ""), "candidate": right.get(field, "")})
        if diffs:
            mismatches.append({"key": item_key, "diffs": diffs[:10], "baseline": left, "candidate": right})
        else:
            matched += 1
    first = mismatches[0] if mismatches else None
    return {
        "matched": matched,
        "mismatched": len(mismatches),
        "missing_in_candidate": len(missing),
        "extra_in_candidate": len(extra),
        "missing_keys": missing[:50],
        "extra_keys": extra[:50],
        "first_divergence_timestamp": first_key_timestamp(first["key"]) if first else "",
        "first_divergence_bar_index": first["baseline"].get("bar_index", "") if first else "",
        "first_divergence_table": mismatches[:10],
        "suspected_cause": suspected_cause(level, missing, extra, mismatches),
        "passed": not missing and not extra and not mismatches,
    }


def row_key(row: dict[str, str], key: str) -> str:
    if key == "timestamp|indicator_name":
        return f"{row.get('timestamp', '')}|{row.get('indicator_name', '')}"
    return row.get(key, "")


def first_key_timestamp(key: str) -> str:
    return key.split("|", 1)[0]


def suspected_cause(level: str, missing: list[str], extra: list[str], mismatches: list[dict[str, Any]]) -> str:
    if missing or extra:
        return "Timestamp/index alignment or missing normalized rows."
    if mismatches and level == "L1":
        return "Indicator formula, warmup, precision, or source data difference."
    if mismatches and level in {"L2", "L3"}:
        return "Signal pulse normalization or confirmation state difference."
    if mismatches and level in {"L4", "L5"}:
        return "Execution rule, state owner, or event ordering difference."
    if mismatches and level == "L6":
        return "Stats aggregation, fees, slippage, or equity curve difference."
    return ""


def compare_stats(baseline_path: Path, candidate_path: Path, abs_tol: float, rel_tol: float) -> dict[str, Any]:
    baseline = read_json(baseline_path) if baseline_path.exists() else {}
    candidate = read_json(candidate_path) if candidate_path.exists() else {}
    keys = sorted(set(baseline) | set(candidate))
    mismatches = []
    matched = 0
    for key in keys:
        if comparable_value(key, str(baseline.get(key, "")), str(candidate.get(key, "")), abs_tol, rel_tol):
            matched += 1
        else:
            mismatches.append({"field": key, "baseline": baseline.get(key), "candidate": candidate.get(key)})
    return {
        "matched": matched,
        "mismatched": len(mismatches),
        "missing_in_candidate": 0,
        "extra_in_candidate": 0,
        "first_divergence_timestamp": "",
        "first_divergence_bar_index": "",
        "first_divergence_table": mismatches[:10],
        "suspected_cause": suspected_cause("L6", [], [], mismatches),
        "passed": not mismatches,
    }


def write_markdown(path: Path, payload: dict[str, Any]) -> None:
    lines = [
        f"# Parity Compare {payload['baseline']} vs {payload['candidate']} {payload['level']}",
        "",
        f"- Case: `{payload['case_id']}`",
        f"- Verdict: `{payload['verdict']}`",
        f"- Baseline file: `{payload['baseline_file']}`",
        f"- Candidate file: `{payload['candidate_file']}`",
        f"- Command: `{payload['command']}`",
        f"- Data hash: `{payload['data_hash']}`",
        f"- Config hash: `{payload['config_hash']}`",
        f"- Code hash: `{payload['code_hash']}`",
        "",
        "## Summary",
        "",
        f"- matched: {payload['matched']}",
        f"- mismatched: {payload['mismatched']}",
        f"- missing_in_baseline: {payload['extra_in_candidate']}",
        f"- missing_in_candidate: {payload['missing_in_candidate']}",
        f"- extra_in_candidate: {payload['extra_in_candidate']}",
        f"- first_divergence_timestamp: {payload['first_divergence_timestamp']}",
        f"- first_divergence_bar_index: {payload['first_divergence_bar_index']}",
        f"- suspected_cause: {payload['suspected_cause']}",
        "",
        "## First Divergences",
        "",
    ]
    for item in payload["first_divergence_table"]:
        lines.append(f"- `{item}`")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", type=Path, required=True)
    parser.add_argument("--baseline", required=True)
    parser.add_argument("--candidate", required=True)
    parser.add_argument("--level", choices=sorted(LEVEL_FILES), required=True)
    parser.add_argument("--abs-tol", type=float, default=1e-8)
    parser.add_argument("--rel-tol", type=float, default=1e-6)
    args = parser.parse_args()
    case = read_json(args.case)
    case_id = case["case_id"]
    filename = LEVEL_FILES[args.level]
    baseline_file = engine_dir(case_id, args.baseline) / filename
    candidate_file = engine_dir(case_id, args.candidate) / filename
    if args.level == "L6":
        result = compare_stats(baseline_file, candidate_file, args.abs_tol, args.rel_tol)
    else:
        result = compare_rows(read_csv(baseline_file), read_csv(candidate_file), args.level, args.abs_tol, args.rel_tol)
    payload = {
        "case_id": case_id,
        "baseline": args.baseline,
        "candidate": args.candidate,
        "level": args.level,
        "baseline_file": str(baseline_file),
        "candidate_file": str(candidate_file),
        "command": "python parity_oracles/compare/parity_compare.py "
        f"--case {args.case} --baseline {args.baseline} --candidate {args.candidate} --level {args.level}",
        "data_hash": sha256_file(ROOT / str(case.get("data_file", ""))),
        "config_hash": sha256_json(case.get("mtc_config", {})),
        "code_hash": git_code_hash(),
        "verdict": "PASS" if result["passed"] else f"FAIL_{args.level}",
        **result,
    }
    out_dir = ROOT / "reports" / "parity" / case_id
    json_path = out_dir / f"{args.baseline}_vs_{args.candidate}_{args.level}.json"
    md_path = out_dir / f"{args.baseline}_vs_{args.candidate}_{args.level}.md"
    write_json(json_path, payload)
    write_markdown(md_path, payload)
    print(md_path)
    print(json_path)
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
