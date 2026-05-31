from __future__ import annotations

REFERENCE_TRACE_COLUMNS = [
    "timestamp",
    "bar_index",
    "feature_id",
    "column_name",
    "expected_value",
    "value_type",
    "source",
]

REFERENCE_COMPARISON_COLUMNS = [
    "timestamp",
    "bar_index",
    "feature_id",
    "column_name",
    "expected_value",
    "python_value",
    "pinets_value",
    "python_match",
    "pinets_match",
    "verdict",
]

DEFAULT_ABS_TOL = 1e-8
DEFAULT_REL_TOL = 1e-6

REFERENCE_VERDICTS = [
    "REFERENCE_PASS",
    "PINETS_MISMATCH",
    "PYTHON_MISMATCH",
    "BOTH_MISMATCH",
    "NOT_COMPARABLE",
]
