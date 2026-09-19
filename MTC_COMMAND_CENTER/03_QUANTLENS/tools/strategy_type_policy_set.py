"""Validation and identity helpers for caller-supplied P021 policy sets.

Successful validation proves only the v1 object shape and version hash.  It is
not policy approval, readiness, eligibility, or permission to use the values.
"""

from __future__ import annotations

import hashlib
import json
import math
from collections.abc import Mapping
from typing import Any


class PolicySetError(ValueError):
    """The caller-supplied policy set is malformed or has the wrong identity."""


_TOP_LEVEL_KEYS = {
    "schema",
    "policy_id",
    "profile",
    "taxonomy",
    "types",
    "shared",
    "methods",
    "provenance",
    "version",
}
_HASH_EXCLUDED_KEYS = {"version", "provenance"}
_TAXONOMY_KEYS = {
    "day_max_hours",
    "swing_max_hours",
    "dominance_min",
    "sample_min",
    "unmeasurable_hold_median_hours",
    "classified_unit",
}
_V1_TYPE_KEYS = {"day", "swing", "position"}
_PER_TYPE_KEYS = {"trade_count_min", "forward_trade_count_min", "forward_period_days"}
_SHARED_KEYS = {
    "single_trade_loss_risk_unit_multiple_max",
    "stop_loss_ceiling_equity_fraction",
    "normal_market_condition_count_min",
    "occupancy_min",
    "trades_per_condition_min",
    "gap_ratio_max",
    "divergence_tolerance",
    "divergence_window_length_days",
    "divergence_min_paired_observations",
}
_METHOD_KEYS = {
    "regime_method_version",
    "gap_method_version",
    "divergence_method_version",
}
_VERSION_PREFIX = "p021pol-v1:"


def _mapping(value: Any, path: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise PolicySetError(f"{path} must be an object")
    if not all(isinstance(key, str) for key in value):
        raise PolicySetError(f"{path} keys must be strings")
    return value


def _exact_keys(value: Any, expected: set[str], path: str) -> Mapping[str, Any]:
    obj = _mapping(value, path)
    actual = set(obj)
    if actual != expected:
        raise PolicySetError(
            f"{path} keys differ; missing={sorted(expected - actual)}; "
            f"extra={sorted(actual - expected)}"
        )
    return obj


def _finite_number(value: Any, path: str, *, nullable: bool = False) -> None:
    if value is None and nullable:
        return
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise PolicySetError(f"{path} must be a finite number" + (" or null" if nullable else ""))
    if not math.isfinite(value):
        raise PolicySetError(f"{path} must be finite")


def _canonical(value: Any, path: str = "policy") -> Any:
    if value is None or isinstance(value, (bool, int, str)):
        return value
    if isinstance(value, float):
        if not math.isfinite(value):
            raise PolicySetError(f"{path} contains a non-finite float")
        return value.hex()
    if isinstance(value, Mapping):
        if not all(isinstance(key, str) for key in value):
            raise PolicySetError(f"{path} keys must be strings")
        return {key: _canonical(item, f"{path}.{key}") for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_canonical(item, f"{path}[]") for item in value]
    raise PolicySetError(f"{path} contains unsupported value type {type(value).__name__}")


def compute_policy_version(policy: Mapping[str, Any]) -> str:
    """Compute the P021 v1 identity without approving or installing the policy."""

    obj = _mapping(policy, "policy")
    body = {key: value for key, value in obj.items() if key not in _HASH_EXCLUDED_KEYS}
    payload = json.dumps(_canonical(body), sort_keys=True, separators=(",", ":"))
    return _VERSION_PREFIX + hashlib.sha256(payload.encode("utf-8")).hexdigest()


def validate_policy_set(policy: Mapping[str, Any]) -> str:
    """Validate the caller-supplied v1 shape and return its verified version."""

    obj = _exact_keys(policy, _TOP_LEVEL_KEYS, "policy")
    if obj["schema"] != "p021.strategy_type_policy_set/v1":
        raise PolicySetError("policy.schema must be 'p021.strategy_type_policy_set/v1'")
    if obj["policy_id"] != "p021-evidence-policy":
        raise PolicySetError("policy.policy_id must be 'p021-evidence-policy'")
    if obj["profile"] not in {"fast", "balanced", "conservative"}:
        raise PolicySetError("policy.profile must be fast, balanced, or conservative")

    taxonomy = _exact_keys(obj["taxonomy"], _TAXONOMY_KEYS, "policy.taxonomy")
    for name in (
        "day_max_hours",
        "swing_max_hours",
        "dominance_min",
        "unmeasurable_hold_median_hours",
    ):
        _finite_number(taxonomy[name], f"policy.taxonomy.{name}")
    sample_min = taxonomy["sample_min"]
    if isinstance(sample_min, bool) or not isinstance(sample_min, int) or sample_min <= 0:
        raise PolicySetError("policy.taxonomy.sample_min must be a positive integer")
    if taxonomy["day_max_hours"] <= 0 or taxonomy["swing_max_hours"] <= taxonomy["day_max_hours"]:
        raise PolicySetError("policy taxonomy boundaries must satisfy 0 < day_max_hours < swing_max_hours")
    if not 0 < taxonomy["dominance_min"] <= 1:
        raise PolicySetError("policy.taxonomy.dominance_min must be in (0, 1]")
    if taxonomy["unmeasurable_hold_median_hours"] < 0:
        raise PolicySetError("policy.taxonomy.unmeasurable_hold_median_hours must be non-negative")
    if taxonomy["classified_unit"] != "strategy_id|asset|timeframe|variant|parameter_set":
        raise PolicySetError("policy.taxonomy.classified_unit is not the v1 classified unit")

    types = _exact_keys(obj["types"], _V1_TYPE_KEYS, "policy.types")
    for strategy_type, block_value in types.items():
        block = _exact_keys(block_value, _PER_TYPE_KEYS, f"policy.types.{strategy_type}")
        for name, value in block.items():
            _finite_number(value, f"policy.types.{strategy_type}.{name}", nullable=True)
            if value is not None and value < 0:
                raise PolicySetError(f"policy.types.{strategy_type}.{name} must be non-negative or null")

    shared = _exact_keys(obj["shared"], _SHARED_KEYS, "policy.shared")
    for name, value in shared.items():
        _finite_number(value, f"policy.shared.{name}", nullable=True)

    methods = _exact_keys(obj["methods"], _METHOD_KEYS, "policy.methods")
    for name, value in methods.items():
        if not isinstance(value, str) or not value:
            raise PolicySetError(f"policy.methods.{name} must be a non-empty string")
    _mapping(obj["provenance"], "policy.provenance")
    _canonical(obj["provenance"], "policy.provenance")

    recorded = obj["version"]
    if not isinstance(recorded, str) or not recorded.startswith(_VERSION_PREFIX):
        raise PolicySetError(f"policy.version must start with {_VERSION_PREFIX}")
    computed = compute_policy_version(obj)
    if recorded != computed:
        raise PolicySetError(f"policy.version mismatch: computed {computed}")
    return recorded
