"""Pure, fail-closed evidence contracts for the approved P021 Decision 1 slice.

This module validates evidence shape and identity only.  It deliberately has no
I/O, runtime execution, evaluator, readiness, or numeric-limit behavior.
"""

from __future__ import annotations

import re
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import datetime, timedelta
from hashlib import sha256

from mtc_contracts.admission import EligibilityState
from mtc_contracts.identity import canonical_json
from mtc_contracts.lineage import UnsimulatedControl


_SHA256_PATTERN = re.compile(r"[0-9a-f]{64}")
_MISSING_INTENT = object()


class EvidenceContractRefused(ValueError):
    """The supplied evidence cannot be interpreted under this contract."""

    def __init__(self, reason_id: str) -> None:
        self.reason_id = reason_id
        super().__init__(reason_id)


@dataclass(frozen=True)
class ControlInventoryItem:
    control_id: str
    required_for_promotion: bool


@dataclass(frozen=True)
class ControlEvidence:
    inventory_sha256: str
    manifest_sha256: str
    undeclared_control_ids: tuple[str, ...]
    informational_control_ids: tuple[str, ...]
    blocking_required_control_ids: tuple[str, ...]


@dataclass(frozen=True)
class DatasetIdentity:
    contract: str
    digest: str


@dataclass(frozen=True)
class IntentEvidence:
    candidate_id: str
    package_hash: str
    deployment_identity_hash: str
    dataset_identity: DatasetIdentity
    instrument_id: str
    decision_bar_timestamp_utc: datetime
    intent_id: str
    p012_intent_contract: str
    p012_semantic_payload_sha256: str


@dataclass(frozen=True)
class DecisionKey:
    instrument_id: str
    decision_bar_timestamp_utc: datetime


@dataclass(frozen=True)
class LookaheadEvidence:
    full_series_decision_count: int
    prefix_decision_count: int
    tested_decision_count: int
    intent_mismatch_count: int
    first_mismatch_key: DecisionKey | None
    first_full_intent_sha256: str | None
    first_prefix_intent_sha256: str | None


@dataclass(frozen=True)
class ClosedBarRuntimeReceipt:
    candidate_id: str
    package_hash: str
    deployment_identity_hash: str
    dataset_identity: DatasetIdentity
    instrument_id: str
    timeframe: str
    bar_open_timestamp_utc: datetime
    bar_close_timestamp_utc: datetime
    decision_timestamp_utc: datetime
    intent_sha256: str
    runtime_producer_id: str
    runtime_code_sha256: str
    source: str


def _require_nonempty(value: object, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise EvidenceContractRefused(f"INVALID_TEXT:{field_name}")
    return value


def _canonical_sha256(value: object) -> str:
    return sha256(canonical_json(value).encode("utf-8")).hexdigest()


def _require_utc(value: object, field_name: str) -> datetime:
    if (
        not isinstance(value, datetime)
        or value.tzinfo is None
        or value.utcoffset() != timedelta(0)
    ):
        raise EvidenceContractRefused(f"INVALID_UTC_DATETIME:{field_name}")
    return value


def _validated_dataset_identity(identity: object) -> DatasetIdentity:
    if not isinstance(identity, DatasetIdentity):
        raise EvidenceContractRefused("DS_V1_INVALID_IDENTITY")
    digest = require_ds_v1_digest(
        {"contract": identity.contract, "digest": identity.digest}
    )
    return DatasetIdentity("ds-v1", digest)


def _unique_inventory(
    items: tuple[ControlInventoryItem, ...],
) -> tuple[ControlInventoryItem, ...]:
    if any(not isinstance(item, ControlInventoryItem) for item in items):
        raise EvidenceContractRefused("CONTROL_INVENTORY_INVALID_ITEM")
    if any(not isinstance(item.required_for_promotion, bool) for item in items):
        raise EvidenceContractRefused("CONTROL_INVENTORY_INVALID_REQUIRED_FLAG")
    for item in items:
        _require_nonempty(item.control_id, "control_id")
    if len({item.control_id for item in items}) != len(items):
        raise EvidenceContractRefused("CONTROL_INVENTORY_DUPLICATE_ID")
    return tuple(sorted(items, key=lambda item: item.control_id))


def _unique_manifest(
    items: tuple[UnsimulatedControl, ...],
) -> tuple[UnsimulatedControl, ...]:
    if any(not isinstance(item, UnsimulatedControl) for item in items):
        raise EvidenceContractRefused("UNSIMULATED_CONTROLS_INVALID_ITEM")
    if any(not isinstance(item.required_for_promotion, bool) for item in items):
        raise EvidenceContractRefused("UNSIMULATED_CONTROLS_INVALID_REQUIRED_FLAG")
    if any(not isinstance(item.control_id, str) or not item.control_id.strip() for item in items):
        raise EvidenceContractRefused("UNSIMULATED_CONTROLS_INVALID_CONTROL_ID")
    if any(not isinstance(item.reason, str) or not item.reason.strip() for item in items):
        raise EvidenceContractRefused("UNSIMULATED_CONTROLS_INVALID_REASON")
    if len({item.control_id for item in items}) != len(items):
        raise EvidenceContractRefused("UNSIMULATED_CONTROLS_DUPLICATE_ID")
    return tuple(sorted(items, key=lambda item: item.control_id))


def control_inventory_sha256(items: tuple[ControlInventoryItem, ...]) -> str:
    ordered = _unique_inventory(items)
    return _canonical_sha256(
        {
            "schema": "p021.control-inventory/v1",
            "controls": [
                {
                    "control_id": item.control_id,
                    "required_for_promotion": item.required_for_promotion,
                }
                for item in ordered
            ],
        }
    )


def unsimulated_controls_sha256(items: tuple[UnsimulatedControl, ...]) -> str:
    ordered = _unique_manifest(items)
    return _canonical_sha256(
        {
            "schema": "p021.unsimulated-controls/v1",
            "controls": [
                {
                    "control_id": item.control_id,
                    "required_for_promotion": item.required_for_promotion,
                    "reason": item.reason,
                }
                for item in ordered
            ],
        }
    )


def evaluate_control_evidence(
    *,
    target_state: EligibilityState,
    inventory: tuple[ControlInventoryItem, ...],
    executed_control_ids: tuple[str, ...],
    manifest: tuple[UnsimulatedControl, ...],
    expected_control_inventory_hash: str,
    expected_unsimulated_controls_hash: str,
) -> ControlEvidence:
    """Validate and classify control evidence without producing a verdict."""

    if not isinstance(target_state, EligibilityState):
        raise EvidenceContractRefused("CONTROL_INVALID_TARGET_STATE")
    if type(executed_control_ids) is not tuple:
        raise EvidenceContractRefused("CONTROL_INVALID_EXECUTED_IDS_CARRIER")
    ordered_inventory = _unique_inventory(inventory)
    ordered_manifest = _unique_manifest(manifest)
    inventory_by_id = {item.control_id: item for item in ordered_inventory}
    manifest_by_id = {item.control_id: item for item in ordered_manifest}

    for control_id in executed_control_ids:
        _require_nonempty(control_id, "executed_control_id")
    if len(set(executed_control_ids)) != len(executed_control_ids):
        raise EvidenceContractRefused("CONTROL_DUPLICATE_EXECUTED_ID")
    if not set(executed_control_ids) <= set(inventory_by_id):
        raise EvidenceContractRefused("CONTROL_EXECUTED_NOT_IN_INVENTORY")
    if not set(manifest_by_id) <= set(inventory_by_id):
        raise EvidenceContractRefused("CONTROL_MANIFEST_NOT_IN_INVENTORY")
    if set(executed_control_ids) & set(manifest_by_id):
        raise EvidenceContractRefused("CONTROL_EXECUTED_AND_UNSIMULATED")
    if any(
        item.required_for_promotion
        != inventory_by_id[item.control_id].required_for_promotion
        for item in ordered_manifest
    ):
        raise EvidenceContractRefused("CONTROL_REQUIRED_FLAG_MISMATCH")

    actual_inventory_hash = control_inventory_sha256(inventory)
    actual_manifest_hash = unsimulated_controls_sha256(manifest)
    if (
        _require_sha256(
            expected_control_inventory_hash,
            "expected_control_inventory_hash",
        )
        != actual_inventory_hash
    ):
        raise EvidenceContractRefused("CONTROL_INVENTORY_HASH_MISMATCH")
    if (
        _require_sha256(
            expected_unsimulated_controls_hash,
            "expected_unsimulated_controls_hash",
        )
        != actual_manifest_hash
    ):
        raise EvidenceContractRefused("CONTROL_MANIFEST_HASH_MISMATCH")

    undeclared = tuple(
        sorted(set(inventory_by_id) - set(executed_control_ids) - set(manifest_by_id))
    )
    if undeclared:
        raise EvidenceContractRefused("CONTROL_UNDECLARED_INVENTORY_ITEM")
    informational = tuple(
        item.control_id
        for item in ordered_manifest
        if not item.required_for_promotion
    )
    blocking_required = ()
    if target_state is not EligibilityState.SHADOW_ELIGIBLE:
        blocking_required = tuple(
            item.control_id for item in ordered_manifest if item.required_for_promotion
        )
    return ControlEvidence(
        inventory_sha256=actual_inventory_hash,
        manifest_sha256=actual_manifest_hash,
        undeclared_control_ids=undeclared,
        informational_control_ids=informational,
        blocking_required_control_ids=blocking_required,
    )


def intent_evidence_sha256(intent: IntentEvidence) -> str:
    """Hash the exact P021 binding to accepted P012 semantic intent fields."""

    if not isinstance(intent, IntentEvidence):
        raise EvidenceContractRefused("INTENT_INVALID_EVIDENCE")
    dataset = _validated_dataset_identity(intent.dataset_identity)
    for field_name in ("candidate_id", "instrument_id", "intent_id"):
        _require_nonempty(getattr(intent, field_name), field_name)
    if intent.p012_intent_contract != "p012.intent-stream/v1":
        raise EvidenceContractRefused("INTENT_UNSUPPORTED_P012_CONTRACT")
    decision_time = _require_utc(
        intent.decision_bar_timestamp_utc, "decision_bar_timestamp_utc"
    )
    package_hash = _require_sha256(intent.package_hash, "package_hash")
    deployment_hash = _require_sha256(
        intent.deployment_identity_hash, "deployment_identity_hash"
    )
    semantic_hash = _require_sha256(
        intent.p012_semantic_payload_sha256, "p012_semantic_payload_sha256"
    )
    return _canonical_sha256(
        {
            "schema": "p021.intent-evidence/v1",
            "candidate_id": intent.candidate_id,
            "package_hash": package_hash,
            "deployment_identity_hash": deployment_hash,
            "dataset_identity": {
                "contract": dataset.contract,
                "digest": dataset.digest,
            },
            "instrument_id": intent.instrument_id,
            "decision_bar_timestamp_utc": decision_time,
            "intent_id": intent.intent_id,
            "p012_intent_contract": intent.p012_intent_contract,
            "p012_semantic_payload_sha256": semantic_hash,
        }
    )


def _validated_decision_key(key: object) -> DecisionKey:
    if not isinstance(key, DecisionKey):
        raise EvidenceContractRefused("LOOKAHEAD_INVALID_DECISION_KEY")
    _require_nonempty(key.instrument_id, "decision_key.instrument_id")
    _require_utc(
        key.decision_bar_timestamp_utc,
        "decision_key.decision_bar_timestamp_utc",
    )
    return key


def _validated_intents(
    intents: Mapping[DecisionKey, IntentEvidence], field_name: str
) -> dict[DecisionKey, tuple[IntentEvidence, str]]:
    if not isinstance(intents, Mapping):
        raise EvidenceContractRefused(f"LOOKAHEAD_INVALID_MAPPING:{field_name}")
    validated: dict[DecisionKey, tuple[IntentEvidence, str]] = {}
    for key, intent in intents.items():
        decision_key = _validated_decision_key(key)
        if (
            not isinstance(intent, IntentEvidence)
            or intent.instrument_id != decision_key.instrument_id
            or intent.decision_bar_timestamp_utc
            != decision_key.decision_bar_timestamp_utc
        ):
            raise EvidenceContractRefused(f"LOOKAHEAD_KEY_INTENT_MISMATCH:{field_name}")
        validated[decision_key] = (intent, intent_evidence_sha256(intent))
    return validated


def compare_lookahead(
    *,
    closed_decision_keys: tuple[DecisionKey, ...],
    full_intents: Mapping[DecisionKey, IntentEvidence],
    prefix_intents: Mapping[DecisionKey, IntentEvidence],
) -> LookaheadEvidence:
    """Compare full and prefix intents over their fixed CLOSED-bar union."""

    closed = tuple(_validated_decision_key(key) for key in closed_decision_keys)
    if len(set(closed)) != len(closed):
        raise EvidenceContractRefused("LOOKAHEAD_DUPLICATE_CLOSED_KEY")
    full = _validated_intents(full_intents, "full_intents")
    prefix = _validated_intents(prefix_intents, "prefix_intents")
    union = set(full) | set(prefix)
    if not union:
        raise EvidenceContractRefused("LOOKAHEAD_EMPTY_UNION")
    if not union <= set(closed):
        raise EvidenceContractRefused("LOOKAHEAD_DECISION_OUTSIDE_CLOSED_UNIVERSE")

    ordered_union = sorted(
        union,
        key=lambda key: (key.decision_bar_timestamp_utc, key.instrument_id),
    )
    mismatches = []
    for key in ordered_union:
        full_intent = full[key][0] if key in full else _MISSING_INTENT
        prefix_intent = prefix[key][0] if key in prefix else _MISSING_INTENT
        if (
            full_intent is _MISSING_INTENT
            or prefix_intent is _MISSING_INTENT
            or full_intent != prefix_intent
        ):
            mismatches.append(key)
    first = mismatches[0] if mismatches else None
    first_full = full.get(first) if first is not None else None
    first_prefix = prefix.get(first) if first is not None else None
    return LookaheadEvidence(
        full_series_decision_count=len(full),
        prefix_decision_count=len(prefix),
        tested_decision_count=len(union),
        intent_mismatch_count=len(mismatches),
        first_mismatch_key=first,
        first_full_intent_sha256=first_full[1] if first_full is not None else None,
        first_prefix_intent_sha256=(
            first_prefix[1] if first_prefix is not None else None
        ),
    )


def validate_closed_bar_runtime_receipt(
    receipt: ClosedBarRuntimeReceipt,
    *,
    expected_candidate_id: str,
    expected_package_sha256: str,
    expected_deployment_identity_sha256: str,
    expected_dataset_identity: DatasetIdentity,
    expected_intent_sha256: str,
    expected_runtime_code_sha256: str,
) -> ClosedBarRuntimeReceipt:
    """Validate an immutable receipt emitted by the runtime decision loop."""

    if not isinstance(receipt, ClosedBarRuntimeReceipt):
        raise EvidenceContractRefused("CLOSED_BAR_INVALID_RECEIPT")
    if receipt.source != "RUNTIME_DECISION_LOOP":
        raise EvidenceContractRefused("CLOSED_BAR_INVALID_RUNTIME_SOURCE")
    for field_name in (
        "candidate_id",
        "instrument_id",
        "timeframe",
        "runtime_producer_id",
    ):
        _require_nonempty(getattr(receipt, field_name), field_name)

    bar_open = _require_utc(receipt.bar_open_timestamp_utc, "bar_open_timestamp_utc")
    bar_close = _require_utc(
        receipt.bar_close_timestamp_utc, "bar_close_timestamp_utc"
    )
    decision_time = _require_utc(
        receipt.decision_timestamp_utc, "decision_timestamp_utc"
    )
    if not bar_open < bar_close <= decision_time:
        raise EvidenceContractRefused("CLOSED_BAR_INVALID_CHRONOLOGY")

    actual_dataset = _validated_dataset_identity(receipt.dataset_identity)
    expected_dataset = _validated_dataset_identity(expected_dataset_identity)
    actual_package = _require_sha256(receipt.package_hash, "package_hash")
    actual_deployment = _require_sha256(
        receipt.deployment_identity_hash, "deployment_identity_hash"
    )
    actual_intent = _require_sha256(receipt.intent_sha256, "intent_sha256")
    actual_runtime_code = _require_sha256(
        receipt.runtime_code_sha256, "runtime_code_sha256"
    )
    expected_package = _require_sha256(
        expected_package_sha256, "expected_package_sha256"
    )
    expected_deployment = _require_sha256(
        expected_deployment_identity_sha256,
        "expected_deployment_identity_sha256",
    )
    expected_intent = _require_sha256(
        expected_intent_sha256, "expected_intent_sha256"
    )
    expected_runtime_code = _require_sha256(
        expected_runtime_code_sha256, "expected_runtime_code_sha256"
    )
    _require_nonempty(expected_candidate_id, "expected_candidate_id")

    if (
        receipt.candidate_id != expected_candidate_id
        or actual_package != expected_package
        or actual_deployment != expected_deployment
        or actual_dataset != expected_dataset
        or actual_intent != expected_intent
        or actual_runtime_code != expected_runtime_code
    ):
        raise EvidenceContractRefused("CLOSED_BAR_IDENTITY_MISMATCH")
    return receipt


def _require_sha256(value: object, field_name: str) -> str:
    if not isinstance(value, str) or _SHA256_PATTERN.fullmatch(value) is None:
        raise EvidenceContractRefused(f"INVALID_SHA256:{field_name}")
    return value


def require_ds_v1_digest(envelope: Mapping[str, object]) -> str:
    """Return the bare digest from an exact external ``ds-v1`` envelope."""

    if not isinstance(envelope, Mapping):
        raise EvidenceContractRefused("DS_V1_INVALID_ENVELOPE")
    keys = tuple(envelope)
    if any(type(key) is not str for key in keys) or set(keys) != {
        "contract",
        "digest",
    }:
        raise EvidenceContractRefused("DS_V1_INVALID_ENVELOPE")
    if envelope["contract"] != "ds-v1":
        raise EvidenceContractRefused("DS_V1_UNSUPPORTED_CONTRACT")
    return _require_sha256(envelope["digest"], "dataset.digest")
