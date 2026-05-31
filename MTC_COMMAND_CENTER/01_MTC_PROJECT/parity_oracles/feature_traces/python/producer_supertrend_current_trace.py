from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ROOT / "00_PYTHON") not in sys.path:
    sys.path.insert(0, str(ROOT / "00_PYTHON"))

from mtc_v2.signals.supertrend import SupertrendSignal

from parity_oracles.engines.pinets_runner import _build_case_bars
from parity_oracles.feature_traces.time_utils import to_iso_utc
from parity_oracles.feature_traces.trace_io import infer_value_type, write_long_trace


CASE_PLAN = ROOT / "05_PARITY" / "TW_EXPORT_CASES_V2" / "case_001" / "case_plan.json"


def export_trace(contract: dict[str, Any], case: dict[str, Any], out_path: Path) -> dict[str, Any]:
    plan, bars = _build_case_bars(CASE_PLAN)
    config = plan.get("planned_overrides", {})
    signal = SupertrendSignal(config if isinstance(config, dict) else {})
    rows: list[dict[str, Any]] = []
    for bar in bars:
        raw = signal.calculate(bar)
        snapshot = signal.indicator_snapshot().supertrend
        hl2 = (bar.high + bar.low) / 2.0
        values = {
            "hl2": hl2,
            "atr": snapshot.atr,
            "upper_band": snapshot.upper_band,
            "lower_band": snapshot.lower_band,
            "supertrend_line": snapshot.line,
            "direction": snapshot.direction,
            "long_raw": int(raw.long),
            "short_raw": int(raw.short),
        }
        for column_name, value in values.items():
            stage = "signal" if column_name in {"long_raw", "short_raw"} else "indicator"
            rows.append(
                {
                    "timestamp": to_iso_utc(bar.timestamp),
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
        "first_timestamps": [to_iso_utc(bar.timestamp) for bar in bars[:5]],
    }
