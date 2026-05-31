from __future__ import annotations

import csv
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from parity_oracles.feature_traces.time_utils import to_iso_utc
from parity_oracles.feature_traces.trace_io import infer_value_type, write_long_trace


CASE_PLAN = ROOT / "05_PARITY" / "TW_EXPORT_CASES_V2" / "case_001" / "case_plan.json"
ISOLATION_DIR = ROOT / "reports" / "parity" / "case_001" / "supertrend_isolation"
PINETS_SUPERTREND = ISOLATION_DIR / "pinets_supertrend.csv"


def _ensure_pinets_source() -> None:
    if PINETS_SUPERTREND.exists():
        return
    completed = subprocess.run(
        [
            sys.executable,
            "parity_oracles/engines/supertrend_isolation_runner.py",
            "--case-plan",
            str(CASE_PLAN),
            "--out-dir",
            str(ISOLATION_DIR),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr or completed.stdout or "supertrend isolation runner failed")


def export_trace(contract: dict[str, Any], case: dict[str, Any], out_path: Path) -> dict[str, Any]:
    _ensure_pinets_source()
    rows: list[dict[str, Any]] = []
    first_timestamps: list[str] = []
    with PINETS_SUPERTREND.open("r", newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        for fallback_index, row in enumerate(reader):
            timestamp = to_iso_utc(row.get("timestamp", ""))
            if len(first_timestamps) < 5:
                first_timestamps.append(timestamp)
            bar_index = int(row.get("bar_index") or fallback_index)
            values = {
                "supertrend_line": row.get("supertrend_line", ""),
                "direction": row.get("direction", ""),
                "long_raw": row.get("long_raw", ""),
                "short_raw": row.get("short_raw", ""),
            }
            for column_name, value in values.items():
                stage = "signal" if column_name in {"long_raw", "short_raw"} else "indicator"
                rows.append(
                    {
                        "timestamp": timestamp,
                        "bar_index": bar_index,
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
        "source": str(PINETS_SUPERTREND),
        "candle_source": "pinets_runner._build_case_bars(case_001 case_plan)",
        "config_source": "case_plan_overrides",
        "trace_source_mode": "case_plan_overrides",
        "timestamp_policy": "ISO_UTC",
        "bar_index_policy": "zero_based_case_candle_index",
        "first_timestamps": first_timestamps,
    }
