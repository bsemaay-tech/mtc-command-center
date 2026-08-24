"""Canonical identity formulae from brief section 6.7."""

from __future__ import annotations

import hashlib
import json
from datetime import date, datetime
from decimal import Decimal
from enum import Enum
from typing import Any

from pydantic import BaseModel


def _json_value(value: Any) -> Any:
    if isinstance(value, BaseModel):
        return _json_value(value.model_dump(mode="python"))
    if isinstance(value, dict):
        return {str(key): _json_value(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_value(item) for item in value]
    if isinstance(value, Decimal):
        return format(value, "f")
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    if isinstance(value, Enum):
        return value.value
    return value


def canonical_json(value: Any) -> str:
    """Stable UTF-8 JSON used as the unambiguous identity preimage."""

    return json.dumps(
        _json_value(value),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    )


def _hash_named_parts(**parts: Any) -> str:
    return hashlib.sha256(canonical_json(parts).encode("utf-8")).hexdigest()


def make_candidate_id(frozen_on: date, source_provenance: Any) -> str:
    provenance_hash = hashlib.sha256(
        canonical_json(source_provenance).encode("utf-8")
    ).hexdigest()
    return f"QLC-{frozen_on:%Y%m%d}-{provenance_hash[:8]}"


def compute_package_hash(
    *,
    spec_json: Any,
    kernel_code_sha: str,
    exact_params_json: Any,
    modules_enabled_json: Any,
    substitute_catalogue_versions_json: Any,
    instrument_metadata_json: Any,
    environment_lineage: Any | None = None,
) -> str:
    """Hash deployable semantics; accepted lineage context is excluded."""

    return _hash_named_parts(
        spec_json=spec_json,
        kernel_code_sha=kernel_code_sha,
        exact_params_json=exact_params_json,
        modules_enabled_json=modules_enabled_json,
        substitute_catalogue_versions_json=substitute_catalogue_versions_json,
        instrument_metadata_json=instrument_metadata_json,
    )


def compute_evaluation_run_hash(
    *,
    package_hash: str,
    dataset_manifest_sha: str,
    cost_model_json: Any,
    simulator_class: str,
    simulator_version: str,
    evaluation_config_json: Any,
    environment_lineage: Any | None = None,
) -> str:
    """Hash evaluation inputs; accepted lineage context remains separate."""

    return _hash_named_parts(
        package_hash=package_hash,
        dataset_manifest_sha=dataset_manifest_sha,
        cost_model_json=cost_model_json,
        simulator_class=simulator_class,
        simulator_version=simulator_version,
        evaluation_config_json=evaluation_config_json,
    )


def compute_deployment_identity_hash(
    *,
    package_hash: str,
    allocator_code_sha: str,
    allocation_policy_version: str,
    guardian_code_sha: str,
    guardian_policy_json: Any,
    risk_bucket_policy_json: Any,
    economic_policy_json: Any,
    runtime_policy_json: Any,
    protection_semantics_json: Any,
    broker_adapter_id: str,
    broker_adapter_version: str,
    cost_lineage_json: Any,
    environment_lineage: Any | None = None,
) -> str:
    """Hash economic identity; accepted environment lineage stays excluded."""

    return _hash_named_parts(
        package_hash=package_hash,
        allocator_code_sha=allocator_code_sha,
        allocation_policy_version=allocation_policy_version,
        guardian_code_sha=guardian_code_sha,
        guardian_policy_json=guardian_policy_json,
        risk_bucket_policy_json=risk_bucket_policy_json,
        economic_policy_json=economic_policy_json,
        runtime_policy_json=runtime_policy_json,
        protection_semantics_json=protection_semantics_json,
        broker_adapter_id=broker_adapter_id,
        broker_adapter_version=broker_adapter_version,
        cost_lineage_json=cost_lineage_json,
    )


def make_trial_id(evaluation_run_hash: str, param_hash: str, sequence: int) -> str:
    if sequence < 0:
        raise ValueError("trial sequence must be non-negative")
    return f"{evaluation_run_hash}.{param_hash}.{sequence}"


def make_run_id(deployment_identity_hash: str, environment: str, sequence: int) -> str:
    if sequence < 0:
        raise ValueError("run sequence must be non-negative")
    return f"{deployment_identity_hash}.{environment}.{sequence}"


def compute_family_id(
    *, source_provenance: Any, producer: str, parameter_neighbourhood: Any
) -> str:
    """Derive family lineage from source, producer, and parameter neighbourhood."""

    digest = _hash_named_parts(
        source_provenance=source_provenance,
        producer=producer,
        parameter_neighbourhood=parameter_neighbourhood,
    )
    return f"FAM-{digest[:16]}"
