from __future__ import annotations

LONG_TRACE_COLUMNS = [
    "timestamp",
    "bar_index",
    "feature_id",
    "feature_type",
    "stage",
    "column_name",
    "value",
    "value_type",
    "source_oracle",
]

SUPPORTED_STAGES = {
    "data",
    "indicator",
    "signal",
    "transform",
    "gate",
    "decision",
    "execution",
    "sizing",
    "guard",
    "alert",
    "visualization",
}

VERDICTS = {
    "FEATURE_TRACE_PASS",
    "FEATURE_TRACE_PASS_WITH_TOLERANCE",
    "FEATURE_TRACE_FAIL_DATA",
    "FEATURE_TRACE_FAIL_INDICATOR",
    "FEATURE_TRACE_FAIL_SIGNAL",
    "FEATURE_TRACE_FAIL_TRANSFORM",
    "FEATURE_TRACE_FAIL_DECISION",
    "FEATURE_TRACE_FAIL_EXECUTION",
    "FEATURE_TRACE_FAIL_SIZING",
    "FEATURE_TRACE_FAIL_ALERT",
    "FEATURE_TRACE_NOT_COMPARABLE",
    "ORACLE_UNAVAILABLE",
}

DEFAULT_TOLERANCE = {
    "numeric_abs_tol": 1.0e-8,
    "numeric_rel_tol": 1.0e-6,
    "tick_tolerance": None,
}

STAGE_TO_FAIL_VERDICT = {
    "data": "FEATURE_TRACE_FAIL_DATA",
    "indicator": "FEATURE_TRACE_FAIL_INDICATOR",
    "signal": "FEATURE_TRACE_FAIL_SIGNAL",
    "transform": "FEATURE_TRACE_FAIL_TRANSFORM",
    "gate": "FEATURE_TRACE_FAIL_DECISION",
    "decision": "FEATURE_TRACE_FAIL_DECISION",
    "execution": "FEATURE_TRACE_FAIL_EXECUTION",
    "sizing": "FEATURE_TRACE_FAIL_SIZING",
    "guard": "FEATURE_TRACE_FAIL_DECISION",
    "alert": "FEATURE_TRACE_FAIL_ALERT",
    "visualization": "FEATURE_TRACE_FAIL_DECISION",
}
