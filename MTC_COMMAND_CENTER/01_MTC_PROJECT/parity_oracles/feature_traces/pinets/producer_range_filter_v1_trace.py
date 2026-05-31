from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from parity_oracles.engines.pinets_runner import _build_case_bars, _plot_values, _write_input_json
from parity_oracles.feature_traces.time_utils import to_iso_utc
from parity_oracles.feature_traces.trace_io import infer_value_type, write_long_trace


CASE_PLAN = ROOT / "05_PARITY" / "TW_EXPORT_CASES_V2" / "case_001" / "case_plan.json"
ADAPTER = ROOT / "parity_oracles" / "feature_adapters" / "pinets" / "producer_range_filter_v1.pine"


PLOTS = {
    "source_price": "FEATURE__producer_range_filter_v1__indicator__source_price",
    "filter_line": "FEATURE__producer_range_filter_v1__indicator__filter_line",
    "upper_band": "FEATURE__producer_range_filter_v1__indicator__upper_band",
    "lower_band": "FEATURE__producer_range_filter_v1__indicator__lower_band",
    "direction": "FEATURE__producer_range_filter_v1__indicator__direction",
    "raw_long": "FEATURE__producer_range_filter_v1__signal__raw_long",
    "raw_short": "FEATURE__producer_range_filter_v1__signal__raw_short",
}


def export_trace(contract: dict[str, Any], case: dict[str, Any], out_path: Path) -> dict[str, Any]:
    _, bars = _build_case_bars(CASE_PLAN)
    out_dir = out_path.parent
    input_path = out_dir / "pinets_range_filter_input_candles.json"
    raw_path = out_dir / "pinets_range_filter_raw.json"
    _write_input_json(input_path, bars)
    module_path = ROOT.parent / "node_modules" / "pinets" / "dist" / "pinets.min.es.js"
    completed = subprocess.run(
        [
            "node",
            "parity_oracles/engines/pinets_signal_export.mjs",
            "--pine",
            str(ADAPTER),
            "--data",
            str(input_path),
            "--out",
            str(raw_path),
            "--pinets-module",
            str(module_path),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        reason = completed.stderr or completed.stdout
        if raw_path.exists():
            raw = json.loads(raw_path.read_text(encoding="utf-8"))
            reason = str(raw.get("error", reason))
        return {"status": "PINETS_TRACE_UNAVAILABLE", "reason": reason}

    raw = json.loads(raw_path.read_text(encoding="utf-8"))
    if raw.get("status") != "success":
        return {"status": "PINETS_TRACE_UNAVAILABLE", "reason": str(raw.get("error", "PineTS failed"))}

    plot_values = {column: _plot_values(raw, title) for column, title in PLOTS.items()}
    rows: list[dict[str, Any]] = []
    first_timestamps: list[str] = []
    for index, bar in enumerate(bars):
        timestamp = to_iso_utc(bar.timestamp)
        if len(first_timestamps) < 5:
            first_timestamps.append(timestamp)
        for column_name, values in plot_values.items():
            value = values[index] if index < len(values) else ""
            stage = "signal" if column_name in {"raw_long", "raw_short"} else "indicator"
            rows.append(
                {
                    "timestamp": timestamp,
                    "bar_index": bar.bar_index,
                    "feature_id": contract["feature_id"],
                    "feature_type": contract["feature_type"],
                    "stage": stage,
                    "column_name": column_name,
                    "value": value,
                    "value_type": infer_value_type(value),
                    "source_oracle": "pinets",
                }
            )
    write_long_trace(out_path, rows)
    return {
        "status": "OK",
        "output": str(out_path),
        "rows": len(rows),
        "source": str(raw_path),
        "adapter": str(ADAPTER),
        "candle_source": "pinets_runner._build_case_bars(case_001 case_plan)",
        "config_source": "case_plan_overrides",
        "trace_source_mode": "case_plan_overrides",
        "timestamp_policy": "ISO_UTC",
        "bar_index_policy": "zero_based_case_candle_index",
        "first_timestamps": first_timestamps,
    }
