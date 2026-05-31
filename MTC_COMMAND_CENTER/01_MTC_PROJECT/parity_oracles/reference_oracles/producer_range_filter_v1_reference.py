from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from parity_oracles.common.io_utils import ROOT, git_code_hash, sha256_file, sha256_json
from parity_oracles.reference_oracles.reference_trace_io import write_json, write_reference_trace


FEATURE_ID = "producer_range_filter_v1"
REQUIRED_COLUMNS = ["source_price", "filter_line", "upper_band", "lower_band", "direction", "raw_long", "raw_short"]


def _iso_from_ms(value: object) -> str:
    return datetime.fromtimestamp(float(value) / 1000.0, tz=timezone.utc).isoformat()


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _contract_rf_range(contract_path: Path) -> float | None:
    if not contract_path.exists():
        return None
    text = contract_path.read_text(encoding="utf-8")
    match = re.search(r"name:\s*rf_range[\s\S]*?default:\s*([0-9.]+)", text)
    return float(match.group(1)) if match else None


def resolve_rf_range(case_path: Path, contract_path: Path) -> float:
    case = _read_json(case_path)
    for section in ("planned_overrides", "mtc_config"):
        value = case.get(section, {})
        if isinstance(value, dict) and "rf_range" in value:
            return float(value["rf_range"])
    contract_value = _contract_rf_range(contract_path)
    if contract_value is not None:
        return contract_value
    return 1000.0


def _default_candle_json_path() -> Path:
    return ROOT / "reports" / "parity" / "case_001" / "features" / FEATURE_ID / "pinets_range_filter_input_candles.json"


def load_candles(case_path: Path, candle_json: Path | None = None) -> list[dict[str, Any]]:
    source = candle_json or _default_candle_json_path()
    if source.exists():
        raw = json.loads(source.read_text(encoding="utf-8"))
        candles = []
        for item in raw:
            timestamp = item.get("timestamp") or item.get("time") or item.get("openTime")
            candles.append(
                {
                    "timestamp": timestamp if isinstance(timestamp, str) and "T" in timestamp else _iso_from_ms(timestamp),
                    "open": float(item.get("open", 0.0)),
                    "high": float(item.get("high", 0.0)),
                    "low": float(item.get("low", 0.0)),
                    "close": float(item.get("close", 0.0)),
                    "volume": float(item.get("volume", 0.0)),
                }
            )
        return candles
    case = _read_json(case_path)
    data_file = ROOT / str(case.get("data_file", ""))
    raise FileNotFoundError(f"Reference candle JSON not found: {source}; fallback CSV range loader is intentionally not guessed for {data_file}")


def _append(rows: list[dict[str, Any]], timestamp: str, bar_index: int, column_name: str, expected_value: Any, value_type: str) -> None:
    rows.append(
        {
            "timestamp": timestamp,
            "bar_index": bar_index,
            "feature_id": FEATURE_ID,
            "column_name": column_name,
            "expected_value": expected_value,
            "value_type": value_type,
            "source": "independent_reference",
        }
    )


def build_reference_rows(candles: list[dict[str, Any]], *, feature_id: str = FEATURE_ID, rf_range: float) -> list[dict[str, Any]]:
    global FEATURE_ID
    previous_feature_id = FEATURE_ID
    FEATURE_ID = feature_id
    try:
        rows: list[dict[str, Any]] = []
        filter_line: float | None = None
        direction = 0
        for index, candle in enumerate(candles):
            close = float(candle["close"])
            raw_long = 0
            raw_short = 0
            if filter_line is None:
                filter_line = close
                direction = 0
            else:
                upper = filter_line + rf_range
                lower = filter_line - rf_range
                if direction < 0 and close > filter_line:
                    direction = 1
                    filter_line = close - rf_range
                    raw_long = 1
                elif direction <= 0 and close > upper:
                    direction = 1
                    filter_line = close - rf_range
                    raw_long = 1
                elif direction >= 0 and close < filter_line:
                    direction = -1
                    filter_line = close + rf_range
                    raw_short = 1
                elif direction > 0 and close > upper:
                    filter_line = close - rf_range
                elif direction < 0 and close < lower:
                    filter_line = close + rf_range
            upper_band = filter_line + rf_range
            lower_band = filter_line - rf_range
            timestamp = str(candle["timestamp"])
            _append(rows, timestamp, index, "source_price", close, "number")
            _append(rows, timestamp, index, "filter_line", filter_line, "number")
            _append(rows, timestamp, index, "upper_band", upper_band, "number")
            _append(rows, timestamp, index, "lower_band", lower_band, "number")
            _append(rows, timestamp, index, "direction", direction, "number")
            _append(rows, timestamp, index, "raw_long", raw_long, "number")
            _append(rows, timestamp, index, "raw_short", raw_short, "number")
        return rows
    finally:
        FEATURE_ID = previous_feature_id


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", default="cases/fast_suite_case_001_range_filter.json")
    parser.add_argument("--contract", default="feature_contracts/active/producer_range_filter_v1.yml")
    parser.add_argument("--candles-json", default="")
    parser.add_argument("--out", default="reports/INDEPENDENT_REFERENCE_ORACLE/range_filter_reference_trace.csv")
    parser.add_argument("--meta-json", default="reports/INDEPENDENT_REFERENCE_ORACLE/range_filter_reference_trace_meta.json")
    args = parser.parse_args()
    case_path = ROOT / args.case
    contract_path = ROOT / args.contract
    candle_path = ROOT / args.candles_json if args.candles_json else None
    rf_range = resolve_rf_range(case_path, contract_path)
    candles = load_candles(case_path, candle_path)
    rows = build_reference_rows(candles, feature_id=FEATURE_ID, rf_range=rf_range)
    out_path = ROOT / args.out
    write_reference_trace(out_path, rows)
    meta = {
        "command": "python parity_oracles/reference_oracles/producer_range_filter_v1_reference.py " + " ".join(sys.argv[1:]),
        "case_path": str(case_path),
        "contract_path": str(contract_path),
        "candle_source": str(candle_path or _default_candle_json_path()),
        "output_path": str(out_path),
        "feature_id": FEATURE_ID,
        "rf_range": rf_range,
        "candle_count": len(candles),
        "row_count": len(rows),
        "required_columns": REQUIRED_COLUMNS,
        "data_hash": sha256_file(candle_path or _default_candle_json_path()),
        "config_hash": sha256_json({"rf_range": rf_range}),
        "code_hash": git_code_hash(),
        "production_imports": "none: does not import RangeFilterSignal or production Runner",
    }
    write_json(ROOT / args.meta_json, meta)
    print(out_path)
    print(ROOT / args.meta_json)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
