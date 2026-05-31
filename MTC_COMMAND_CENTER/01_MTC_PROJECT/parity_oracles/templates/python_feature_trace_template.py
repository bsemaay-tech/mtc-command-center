from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any

from parity_oracles.feature_traces.trace_contract import load_contract
from parity_oracles.feature_traces.trace_io import infer_value_type, write_long_trace


def load_case(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def load_candles(path: str | Path) -> list[dict[str, str]]:
    with Path(path).open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def emit(rows: list[dict[str, Any]], *, candle: dict[str, Any], bar_index: int, contract: dict[str, Any], stage: str, column: str, value: Any) -> None:
    rows.append(
        {
            "timestamp": candle.get("timestamp") or candle.get("time") or bar_index,
            "bar_index": bar_index,
            "feature_id": contract["feature_id"],
            "feature_type": contract["feature_type"],
            "stage": stage,
            "column_name": column,
            "value": value,
            "value_type": infer_value_type(value),
            "source_oracle": "python",
        }
    )


def build_trace(case_path: str, contract_path: str, output_path: str) -> None:
    case = load_case(case_path)
    contract = load_contract(contract_path)
    candles = load_candles(case["data_file"])
    rows: list[dict[str, Any]] = []
    for bar_index, candle in enumerate(candles):
        close = float(candle.get("close") or candle.get("Close") or 0.0)
        emit(rows, candle=candle, bar_index=bar_index, contract=contract, stage="indicator", column="example_indicator", value=close)
        emit(rows, candle=candle, bar_index=bar_index, contract=contract, stage="signal", column="raw_long", value=False)
        emit(rows, candle=candle, bar_index=bar_index, contract=contract, stage="gate", column="allowed_long", value=True)
        emit(rows, candle=candle, bar_index=bar_index, contract=contract, stage="execution", column="exit_reason", value="")
        emit(rows, candle=candle, bar_index=bar_index, contract=contract, stage="sizing", column="qty", value=0.0)
        emit(rows, candle=candle, bar_index=bar_index, contract=contract, stage="alert", column="payload_json", value="{}")
    write_long_trace(output_path, rows)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", required=True)
    parser.add_argument("--contract", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    build_trace(args.case, args.contract, args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
