from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from parity_oracles.common.io_utils import git_code_hash, sha256_file
from parity_oracles.reference_oracles.reference_trace_io import (
    read_feature_trace,
    read_reference_trace,
    write_comparison_rows,
    write_json,
)
from parity_oracles.reference_oracles.reference_trace_schema import DEFAULT_ABS_TOL, DEFAULT_REL_TOL


def _key(row: dict[str, str]) -> tuple[str, str, str]:
    return (row.get("bar_index", ""), row.get("feature_id", ""), row.get("column_name", ""))


def _as_bool(value: str) -> bool | None:
    text = str(value).strip().lower()
    if text in {"true", "1", "1.0"}:
        return True
    if text in {"false", "0", "0.0"}:
        return False
    return None


def values_match(expected: str, actual: str, value_type: str, abs_tol: float = DEFAULT_ABS_TOL, rel_tol: float = DEFAULT_REL_TOL) -> bool:
    if actual == "":
        return False
    if value_type == "number":
        try:
            left = float(expected)
            right = float(actual)
        except ValueError:
            return False
        if math.isnan(left) and math.isnan(right):
            return True
        return math.isclose(left, right, abs_tol=abs_tol, rel_tol=rel_tol)
    if value_type == "bool":
        return _as_bool(expected) == _as_bool(actual)
    return str(expected) == str(actual)


def _trace_value_map(rows: list[dict[str, str]]) -> dict[tuple[str, str, str], str]:
    return {
        (row.get("bar_index", ""), row.get("feature_id", ""), row.get("column_name", "")): row.get("value", "")
        for row in rows
    }


def compare_reference_to_traces(
    reference_path: str | Path,
    python_trace_path: str | Path,
    pinets_trace_path: str | Path,
    *,
    abs_tol: float = DEFAULT_ABS_TOL,
    rel_tol: float = DEFAULT_REL_TOL,
) -> dict[str, Any]:
    reference_rows = read_reference_trace(reference_path)
    python_values = _trace_value_map(read_feature_trace(python_trace_path))
    pinets_values = _trace_value_map(read_feature_trace(pinets_trace_path))
    comparison_rows: list[dict[str, Any]] = []
    missing_rows: list[dict[str, Any]] = []
    python_mismatches = 0
    pinets_mismatches = 0
    both_mismatches = 0
    matched = 0
    first_divergence: dict[str, Any] | None = None

    for row in reference_rows:
        key = _key(row)
        expected = row.get("expected_value", "")
        value_type = row.get("value_type", "")
        python_value = python_values.get(key, "")
        pinets_value = pinets_values.get(key, "")
        python_present = key in python_values
        pinets_present = key in pinets_values
        python_match = python_present and values_match(expected, python_value, value_type, abs_tol, rel_tol)
        pinets_match = pinets_present and values_match(expected, pinets_value, value_type, abs_tol, rel_tol)
        if not python_present or not pinets_present:
            row_verdict = "NOT_COMPARABLE"
            missing_rows.append(
                {
                    "timestamp": row.get("timestamp", ""),
                    "bar_index": row.get("bar_index", ""),
                    "feature_id": row.get("feature_id", ""),
                    "column_name": row.get("column_name", ""),
                    "missing_python": not python_present,
                    "missing_pinets": not pinets_present,
                }
            )
        elif python_match and pinets_match:
            row_verdict = "REFERENCE_PASS"
            matched += 1
        elif not python_match and not pinets_match:
            row_verdict = "BOTH_MISMATCH"
            python_mismatches += 1
            pinets_mismatches += 1
            both_mismatches += 1
        elif not python_match:
            row_verdict = "PYTHON_MISMATCH"
            python_mismatches += 1
        else:
            row_verdict = "PINETS_MISMATCH"
            pinets_mismatches += 1
        output_row = {
            "timestamp": row.get("timestamp", ""),
            "bar_index": row.get("bar_index", ""),
            "feature_id": row.get("feature_id", ""),
            "column_name": row.get("column_name", ""),
            "expected_value": expected,
            "python_value": python_value,
            "pinets_value": pinets_value,
            "python_match": int(bool(python_match)),
            "pinets_match": int(bool(pinets_match)),
            "verdict": row_verdict,
        }
        comparison_rows.append(output_row)
        if row_verdict != "REFERENCE_PASS" and first_divergence is None:
            first_divergence = output_row

    if missing_rows:
        verdict = "NOT_COMPARABLE"
    elif python_mismatches and pinets_mismatches:
        verdict = "BOTH_MISMATCH" if both_mismatches else "BOTH_MISMATCH"
    elif python_mismatches:
        verdict = "PYTHON_MISMATCH"
    elif pinets_mismatches:
        verdict = "PINETS_MISMATCH"
    else:
        verdict = "REFERENCE_PASS"

    return {
        "verdict": verdict,
        "compared_row_count": len(reference_rows),
        "matched_row_count": matched,
        "python_mismatches": python_mismatches,
        "pinets_mismatches": pinets_mismatches,
        "both_mismatches": both_mismatches,
        "missing_rows": missing_rows[:50],
        "missing_row_count": len(missing_rows),
        "first_divergence": first_divergence,
        "comparison_rows": comparison_rows,
        "reference_path": str(reference_path),
        "python_trace_path": str(python_trace_path),
        "pinets_trace_path": str(pinets_trace_path),
        "reference_hash": sha256_file(Path(reference_path)),
        "python_trace_hash": sha256_file(Path(python_trace_path)),
        "pinets_trace_hash": sha256_file(Path(pinets_trace_path)),
        "code_hash": git_code_hash(),
    }


def markdown_report(payload: dict[str, Any], command: str, comparison_csv: str | None = None) -> str:
    first = payload.get("first_divergence")
    lines = [
        "# Independent Reference Oracle Comparison",
        "",
        f"- Verdict: `{payload['verdict']}`",
        f"- Command: `{command}`",
        f"- Reference: `{payload['reference_path']}`",
        f"- Python trace: `{payload['python_trace_path']}`",
        f"- PineTS trace: `{payload['pinets_trace_path']}`",
        f"- Comparison CSV: `{comparison_csv or ''}`",
        f"- Compared rows: {payload['compared_row_count']}",
        f"- Matched rows: {payload['matched_row_count']}",
        f"- Python mismatches: {payload['python_mismatches']}",
        f"- PineTS mismatches: {payload['pinets_mismatches']}",
        f"- Both mismatches: {payload['both_mismatches']}",
        f"- Missing rows: {payload['missing_row_count']}",
        f"- Reference hash: `{payload['reference_hash']}`",
        f"- Python trace hash: `{payload['python_trace_hash']}`",
        f"- PineTS trace hash: `{payload['pinets_trace_hash']}`",
        f"- Code hash: `{payload['code_hash']}`",
        "",
        "## First Divergence",
        "",
        "None" if not first else json.dumps(first, indent=2),
    ]
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--reference", required=True)
    parser.add_argument("--python-trace", required=True)
    parser.add_argument("--pinets-trace", required=True)
    parser.add_argument("--out-md", required=True)
    parser.add_argument("--out-json", required=True)
    parser.add_argument("--out-csv", default="")
    args = parser.parse_args()
    command = "python parity_oracles/reference_oracles/compare_reference_oracle.py " + " ".join(sys.argv[1:])
    result = compare_reference_to_traces(args.reference, args.python_trace, args.pinets_trace)
    comparison_rows = result.pop("comparison_rows")
    out_csv = args.out_csv or str(Path(args.out_json).with_name(Path(args.out_json).stem + "_rows.csv"))
    write_comparison_rows(out_csv, comparison_rows)
    result["command"] = command
    result["output_paths"] = {"markdown": args.out_md, "json": args.out_json, "comparison_csv": out_csv}
    write_json(args.out_json, result)
    Path(args.out_md).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out_md).write_text(markdown_report(result, command, out_csv), encoding="utf-8")
    return 0 if result["verdict"] == "REFERENCE_PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
