from __future__ import annotations

import csv
from pathlib import Path

from parity_oracles.reference_oracles.compare_reference_oracle import compare_reference_to_traces
from parity_oracles.reference_oracles.producer_range_filter_v1_reference import build_reference_rows
from parity_oracles.reference_oracles.reference_trace_io import write_reference_trace


def _write_feature_trace(path: Path, rows: list[dict[str, object]], source: str, *, mutate: tuple[int, str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = ["timestamp", "bar_index", "feature_id", "feature_type", "stage", "column_name", "value", "value_type", "source_oracle"]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for index, row in enumerate(rows):
            value = row["expected_value"]
            if mutate and index == mutate[0]:
                value = mutate[1]
            writer.writerow(
                {
                    "timestamp": row["timestamp"],
                    "bar_index": row["bar_index"],
                    "feature_id": row["feature_id"],
                    "feature_type": "signal_producer",
                    "stage": "signal" if row["column_name"] in {"raw_long", "raw_short"} else "indicator",
                    "column_name": row["column_name"],
                    "value": value,
                    "value_type": row["value_type"],
                    "source_oracle": source,
                }
            )


def test_range_filter_reference_trace_generation_is_independent() -> None:
    candles = [
        {"timestamp": "2024-01-01T00:00:00+00:00", "close": 100.0},
        {"timestamp": "2024-01-01T01:00:00+00:00", "close": 99.0},
        {"timestamp": "2024-01-01T02:00:00+00:00", "close": 101.5},
    ]
    rows = build_reference_rows(candles, feature_id="producer_range_filter_v1", rf_range=1.0)
    assert [row["column_name"] for row in rows[:7]] == [
        "source_price",
        "filter_line",
        "upper_band",
        "lower_band",
        "direction",
        "raw_long",
        "raw_short",
    ]
    assert rows[0]["expected_value"] == 100.0
    assert rows[7 + 1]["expected_value"] == 100.0
    assert rows[7 + 4]["expected_value"] == -1
    assert rows[14 + 1]["expected_value"] == 100.5
    assert rows[14 + 4]["expected_value"] == 1


def test_reference_comparison_detects_pass_and_mismatches(tmp_path: Path) -> None:
    reference_rows = build_reference_rows(
        [
            {"timestamp": "2024-01-01T00:00:00+00:00", "close": 100.0},
            {"timestamp": "2024-01-01T01:00:00+00:00", "close": 99.0},
        ],
        feature_id="producer_range_filter_v1",
        rf_range=1.0,
    )
    reference = tmp_path / "reference.csv"
    python_trace = tmp_path / "python.csv"
    pinets_trace = tmp_path / "pinets.csv"
    write_reference_trace(reference, reference_rows)
    _write_feature_trace(python_trace, reference_rows, "python")
    _write_feature_trace(pinets_trace, reference_rows, "pinets")

    result = compare_reference_to_traces(reference, python_trace, pinets_trace)
    assert result["verdict"] == "REFERENCE_PASS"

    _write_feature_trace(python_trace, reference_rows, "python", mutate=(0, "999"))
    result = compare_reference_to_traces(reference, python_trace, pinets_trace)
    assert result["verdict"] == "PYTHON_MISMATCH"

    _write_feature_trace(python_trace, reference_rows, "python")
    _write_feature_trace(pinets_trace, reference_rows, "pinets", mutate=(0, "999"))
    result = compare_reference_to_traces(reference, python_trace, pinets_trace)
    assert result["verdict"] == "PINETS_MISMATCH"


def test_reference_comparison_reports_missing_rows(tmp_path: Path) -> None:
    reference_rows = build_reference_rows(
        [{"timestamp": "2024-01-01T00:00:00+00:00", "close": 100.0}],
        feature_id="producer_range_filter_v1",
        rf_range=1.0,
    )
    reference = tmp_path / "reference.csv"
    python_trace = tmp_path / "python.csv"
    pinets_trace = tmp_path / "pinets.csv"
    write_reference_trace(reference, reference_rows)
    _write_feature_trace(python_trace, reference_rows[:-1], "python")
    _write_feature_trace(pinets_trace, reference_rows, "pinets")

    result = compare_reference_to_traces(reference, python_trace, pinets_trace)
    assert result["verdict"] == "NOT_COMPARABLE"
    assert result["missing_rows"]
