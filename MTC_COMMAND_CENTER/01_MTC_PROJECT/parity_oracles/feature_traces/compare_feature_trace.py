from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any

from .trace_io import read_long_trace, write_json
from .trace_schema import DEFAULT_TOLERANCE, STAGE_TO_FAIL_VERDICT


def _key(row: dict[str, str]) -> tuple[str, str, str]:
    return (row.get("bar_index", ""), row.get("stage", ""), row.get("column_name", ""))


def _as_bool(value: str) -> bool | None:
    lowered = str(value).strip().lower()
    if lowered in {"true", "1", "1.0"}:
        return True
    if lowered in {"false", "0", "0.0"}:
        return False
    return None


def _compare_values(a: str, b: str, value_type: str, abs_tol: float, rel_tol: float) -> tuple[bool, bool]:
    if value_type == "number":
        try:
            af = float(a)
            bf = float(b)
        except ValueError:
            return False, False
        if math.isnan(af) and math.isnan(bf):
            return True, False
        exact = af == bf
        return math.isclose(af, bf, abs_tol=abs_tol, rel_tol=rel_tol), not exact
    if value_type == "bool":
        return _as_bool(a) == _as_bool(b), False
    return str(a) == str(b), False


def compare_traces(
    baseline_path: str | Path,
    candidate_path: str | Path,
    *,
    warmup_bars: int = 0,
    numeric_abs_tol: float = DEFAULT_TOLERANCE["numeric_abs_tol"],
    numeric_rel_tol: float = DEFAULT_TOLERANCE["numeric_rel_tol"],
    include_columns: set[str] | None = None,
) -> dict[str, Any]:
    baseline = [row for row in read_long_trace(baseline_path) if int(row.get("bar_index") or 0) >= warmup_bars]
    candidate = [row for row in read_long_trace(candidate_path) if int(row.get("bar_index") or 0) >= warmup_bars]
    if include_columns is not None:
        baseline = [row for row in baseline if row.get("column_name") in include_columns]
        candidate = [row for row in candidate if row.get("column_name") in include_columns]
    candidate_by_key = {_key(row): row for row in candidate}
    matched = 0
    tolerance_matches = 0
    missing = 0
    first_divergence = None
    window: list[dict[str, Any]] = []
    for row in baseline:
        key = _key(row)
        other = candidate_by_key.get(key)
        if other is None:
            missing += 1
            if first_divergence is None:
                first_divergence = {"reason": "missing_candidate_row", **{k: row.get(k, "") for k in ["timestamp", "bar_index", "feature_id", "stage", "column_name"]}}
            continue
        ok, within_tolerance = _compare_values(row.get("value", ""), other.get("value", ""), row.get("value_type", ""), numeric_abs_tol, numeric_rel_tol)
        if ok:
            matched += 1
            if within_tolerance:
                tolerance_matches += 1
            continue
        if first_divergence is None:
            first_divergence = {
                "reason": "value_mismatch",
                "timestamp": row.get("timestamp", ""),
                "bar_index": row.get("bar_index", ""),
                "feature_id": row.get("feature_id", ""),
                "stage": row.get("stage", ""),
                "column_name": row.get("column_name", ""),
                "baseline_value": row.get("value", ""),
                "candidate_value": other.get("value", ""),
            }
            center = int(row.get("bar_index") or 0)
            for b in baseline:
                try:
                    idx = int(b.get("bar_index") or 0)
                except ValueError:
                    continue
                if center - 3 <= idx <= center + 3 and b.get("column_name") == row.get("column_name"):
                    window.append({"baseline": b, "candidate": candidate_by_key.get(_key(b), {})})
    if first_divergence:
        stage = first_divergence.get("stage", "decision")
        verdict = STAGE_TO_FAIL_VERDICT.get(str(stage), "FEATURE_TRACE_NOT_COMPARABLE")
    elif tolerance_matches:
        verdict = "FEATURE_TRACE_PASS_WITH_TOLERANCE"
    else:
        verdict = "FEATURE_TRACE_PASS"
    return {
        "verdict": verdict,
        "matched": matched,
        "missing_candidate_rows": missing,
        "baseline_rows": len(baseline),
        "candidate_rows": len(candidate),
        "first_divergence": first_divergence,
        "window": window,
    }


def markdown_report(result: dict[str, Any]) -> str:
    first = result.get("first_divergence") or {}
    return "\n".join(
        [
            "# Feature Trace Comparison",
            "",
            f"- Verdict: `{result['verdict']}`",
            f"- Matched rows: {result['matched']}",
            f"- Baseline rows: {result['baseline_rows']}",
            f"- Candidate rows: {result['candidate_rows']}",
            f"- Missing candidate rows: {result['missing_candidate_rows']}",
            "",
            "## First Divergence",
            "",
            "None" if not first else json.dumps(first, indent=2),
        ]
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--baseline", required=True)
    parser.add_argument("--candidate", required=True)
    parser.add_argument("--out-json", required=True)
    parser.add_argument("--out-md", required=True)
    parser.add_argument("--warmup-bars", type=int, default=0)
    args = parser.parse_args()
    result = compare_traces(args.baseline, args.candidate, warmup_bars=args.warmup_bars)
    write_json(args.out_json, result)
    Path(args.out_md).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out_md).write_text(markdown_report(result), encoding="utf-8")
    return 0 if result["verdict"].startswith("FEATURE_TRACE_PASS") else 1


if __name__ == "__main__":
    raise SystemExit(main())
