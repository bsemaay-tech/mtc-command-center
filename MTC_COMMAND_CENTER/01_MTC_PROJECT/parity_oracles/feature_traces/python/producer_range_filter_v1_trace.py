from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ROOT / "00_PYTHON") not in sys.path:
    sys.path.insert(0, str(ROOT / "00_PYTHON"))

from mtc_v2.signals.range_filter import RangeFilterSignal

from parity_oracles.engines.pinets_runner import _build_case_bars
from parity_oracles.feature_traces.time_utils import to_iso_utc
from parity_oracles.feature_traces.trace_io import infer_value_type, write_long_trace


CASE_PLAN = ROOT / "05_PARITY" / "TW_EXPORT_CASES_V2" / "case_001" / "case_plan.json"


def export_trace(contract: dict[str, Any], case: dict[str, Any], out_path: Path) -> dict[str, Any]:
    _, bars = _build_case_bars(CASE_PLAN)
    config = {"rf_range": _contract_default(contract, "rf_range", 1000.0)}
    signal = RangeFilterSignal(config)
    rows: list[dict[str, Any]] = []
    first_timestamps: list[str] = []
    for bar in bars:
        raw = signal.calculate(bar)
        snapshot = signal.indicator_snapshot()
        timestamp = to_iso_utc(bar.timestamp)
        if len(first_timestamps) < 5:
            first_timestamps.append(timestamp)
        values = {
            "source_price": snapshot["source_price"],
            "filter_line": snapshot["filter_line"],
            "upper_band": snapshot["upper_band"],
            "lower_band": snapshot["lower_band"],
            "direction": snapshot["direction"],
            "raw_long": int(raw.long),
            "raw_short": int(raw.short),
        }
        for column_name, value in values.items():
            stage = "signal" if column_name in {"raw_long", "raw_short"} else "indicator"
            rows.append(
                {
                    "timestamp": timestamp,
                    "bar_index": bar.bar_index,
                    "feature_id": contract["feature_id"],
                    "feature_type": contract["feature_type"],
                    "stage": stage,
                    "column_name": column_name,
                    "value": "" if value is None else value,
                    "value_type": infer_value_type(value),
                    "source_oracle": "python",
                }
            )
    write_long_trace(out_path, rows)
    return {
        "status": "OK",
        "output": str(out_path),
        "rows": len(rows),
        "candle_source": "pinets_runner._build_case_bars(case_001 case_plan)",
        "config_source": "case_plan_overrides",
        "trace_source_mode": "case_plan_overrides",
        "timestamp_policy": "ISO_UTC",
        "bar_index_policy": "zero_based_case_candle_index",
        "first_timestamps": first_timestamps,
    }


def _contract_default(contract: dict[str, Any], name: str, fallback: float) -> float:
    for parameter in contract.get("input_parameters", []):
        if isinstance(parameter, dict) and parameter.get("name") == name:
            return float(parameter.get("default", fallback))
    return fallback
