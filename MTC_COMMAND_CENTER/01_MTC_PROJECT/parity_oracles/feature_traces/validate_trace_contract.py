from __future__ import annotations

import argparse
from pathlib import Path

from .trace_contract import load_contract, required_trace_columns
from .trace_io import read_long_trace
from .trace_schema import LONG_TRACE_COLUMNS, SUPPORTED_STAGES


def validate_trace(contract_path: str, trace_path: str) -> dict[str, object]:
    contract = load_contract(contract_path)
    rows = read_long_trace(trace_path)
    missing_file_columns = [column for column in LONG_TRACE_COLUMNS if rows and column not in rows[0]]
    observed = {row.get("column_name", "") for row in rows}
    required = set(required_trace_columns(contract))
    missing_trace_columns = sorted(required - observed)
    invalid_stages = sorted({row.get("stage", "") for row in rows if row.get("stage", "") not in SUPPORTED_STAGES})
    verdict = "TRACE_CONTRACT_OK"
    if missing_file_columns or missing_trace_columns or invalid_stages:
        verdict = "TRACE_CONTRACT_INCOMPLETE"
    return {
        "verdict": verdict,
        "missing_file_columns": missing_file_columns,
        "missing_trace_columns": missing_trace_columns,
        "invalid_stages": invalid_stages,
        "row_count": len(rows),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--contract", required=True)
    parser.add_argument("--trace", required=True)
    args = parser.parse_args()
    result = validate_trace(args.contract, args.trace)
    print(result)
    return 0 if result["verdict"] == "TRACE_CONTRACT_OK" else 2


if __name__ == "__main__":
    raise SystemExit(main())
