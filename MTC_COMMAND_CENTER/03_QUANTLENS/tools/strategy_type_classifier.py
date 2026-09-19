"""Pure holding-hours classifier for P021 research measurements."""

from __future__ import annotations

import math
from collections.abc import Iterable, Mapping
from typing import Any

from strategy_type_policy_set import validate_policy_set


def _holding_hours(values: Iterable[float]) -> list[float]:
    result = []
    for index, value in enumerate(values):
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError(f"holding_hours[{index}] must be a finite number")
        if not math.isfinite(value):
            raise ValueError(f"holding_hours[{index}] must be finite")
        result.append(float(value))
    return result


def _stable_median(values: list[float]) -> float:
    ordered = sorted(values)
    middle = len(ordered) // 2
    if len(ordered) % 2:
        return ordered[middle]
    lower, upper = ordered[middle - 1 : middle + 1]
    return lower + (upper - lower) / 2


def classify_holding_hours(
    holding_hours: Iterable[float], policy: Mapping[str, Any]
) -> dict[str, Any]:
    """Classify one series; the result is classification-only, never readiness."""

    policy_version = validate_policy_set(policy)
    values = _holding_hours(holding_hours)
    taxonomy = policy["taxonomy"]
    non_negative = [value for value in values if value >= 0]
    counts = {"day": 0, "swing": 0, "position": 0}
    for value in non_negative:
        if value < taxonomy["day_max_hours"]:
            counts["day"] += 1
        elif value < taxonomy["swing_max_hours"]:
            counts["swing"] += 1
        else:
            counts["position"] += 1

    sample_count = len(non_negative)
    median_hours = _stable_median(non_negative) if non_negative else None
    dominant = max(counts, key=counts.get) if sample_count else None
    dominance = counts[dominant] / sample_count if dominant is not None else None

    refusal_code = None
    if len(non_negative) != len(values):
        refusal_code = "BLOCKED_NEGATIVE_HOLD"
    elif sample_count < taxonomy["sample_min"]:
        refusal_code = "BLOCKED_INSUFFICIENT_SAMPLE"
    elif median_hours == taxonomy["unmeasurable_hold_median_hours"]:
        refusal_code = "BLOCKED_UNMEASURABLE_HOLD"
    elif dominance < taxonomy["dominance_min"]:
        refusal_code = "BLOCKED_MIXED_HOLDING_PROFILE"

    return {
        "result_kind": "P021_STRATEGY_TYPE_CLASSIFICATION_ONLY",
        "status": "REFUSED" if refusal_code else "CLASSIFIED",
        "strategy_type": None if refusal_code else dominant,
        "refusal_code": refusal_code,
        "sample_count": sample_count,
        "median_hold_hours": median_hours,
        "dominance": dominance,
        "bucket_counts": counts,
        "policy_version": policy_version,
    }
