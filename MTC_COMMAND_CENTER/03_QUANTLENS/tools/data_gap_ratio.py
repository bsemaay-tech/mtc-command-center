"""Fixed-step, 24/7 timestamp-gap measurements for P021 research."""

from __future__ import annotations

import math
from collections.abc import Iterable, Mapping
from typing import Any

from strategy_type_policy_set import validate_policy_set


TIMEFRAME_SECONDS = {
    "5m": 300,
    "15m": 900,
    "1h": 3_600,
    "2h": 7_200,
    "4h": 14_400,
    "1D": 86_400,
}


def _timestamps(values: Iterable[float]) -> list[float]:
    result = []
    for index, value in enumerate(values):
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError(f"timestamps[{index}] must be a finite number")
        if not math.isfinite(value):
            raise ValueError(f"timestamps[{index}] must be finite")
        result.append(float(value))
    if len(result) < 2:
        raise ValueError("at least two timestamps are required")
    return result


def _finite_ratio(numerator: int | float, denominator: int | float, name: str) -> float:
    try:
        result = numerator / denominator
    except OverflowError as error:
        raise ValueError(f"derived {name} must be finite") from error
    if not math.isfinite(result):
        raise ValueError(f"derived {name} must be finite")
    return result


def measure_data_gaps(
    timestamps: Iterable[float], timeframe: str, policy: Mapping[str, Any]
) -> dict[str, Any]:
    """Measure M1/M2/M3 without sorting, filling, or applying a policy limit."""

    policy_version = validate_policy_set(policy)
    if policy["methods"]["gap_method_version"] != "data_gap_ratio_m2_v1":
        raise ValueError("unsupported policy.methods.gap_method_version")
    try:
        step = TIMEFRAME_SECONDS[timeframe]
    except (KeyError, TypeError) as error:
        raise ValueError(f"unsupported timeframe: {timeframe!r}") from error

    values = _timestamps(timestamps)
    deltas = [right - left for left, right in zip(values, values[1:])]
    if not all(math.isfinite(delta) for delta in deltas):
        raise ValueError("derived timestamp deltas must be finite")
    span = values[-1] - values[0]
    if not math.isfinite(span) or span <= 0:
        raise ValueError("timestamp span must be finite and positive")
    expected_bars = round(span / step) + 1
    if expected_bars <= 0:
        raise ValueError("expected-bar denominator is undefined")

    detected = [delta for delta in deltas if delta > 1.5 * step]
    missing_by_gap = [max(0, round(delta / step) - 1) for delta in detected]
    missing_bars = sum(missing_by_gap)
    duplicate_count = len(values) - len(set(values))
    out_of_order_count = sum(delta < 0 for delta in deltas)
    early_count = sum(0 < delta < step for delta in deltas)
    irregular_count = sum(
        delta > 0
        and delta / step != round(delta / step)
        for delta in deltas
    )
    m3_missing_seconds = sum(delta - step for delta in detected)
    if not math.isfinite(m3_missing_seconds):
        raise ValueError("derived missing-time total must be finite")
    gap_event_count = len(detected)
    m1 = _finite_ratio(gap_event_count, len(deltas), "M1 gap-event ratio")
    m2 = _finite_ratio(missing_bars, expected_bars, "M2 missing-bar ratio")
    m3 = _finite_ratio(m3_missing_seconds, span, "M3 missing-time ratio")

    return {
        "result_kind": "P021_DATA_GAP_MEASUREMENT_ONLY",
        "timeframe": timeframe,
        "step_seconds": step,
        "observation_count": len(values),
        "interval_count": len(deltas),
        "coverage_seconds": span,
        "coverage_days": span / 86_400,
        "expected_bars": expected_bars,
        "gap_event_count": gap_event_count,
        "missing_bar_count": missing_bars,
        "m1_gap_event_ratio": m1,
        "m2_missing_bar_ratio": m2,
        "m3_missing_time_ratio": m3,
        "max_gap_bars": max(missing_by_gap, default=0),
        "max_gap_seconds": max((delta - step for delta in detected), default=0.0),
        "duplicate_timestamp_count": duplicate_count,
        "out_of_order_interval_count": out_of_order_count,
        "early_interval_count": early_count,
        "irregular_interval_count": irregular_count,
        "series_clean": not (
            gap_event_count
            or duplicate_count
            or out_of_order_count
            or early_count
            or irregular_count
        ),
        "policy_version": policy_version,
    }
