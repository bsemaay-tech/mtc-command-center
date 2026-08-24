"""Version handshake, source-normalization, and deterministic-batch shapes."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Literal

from pydantic import model_validator

from .base import CONTRACT_VERSION, ContractModel, NonEmptyStr, Sha256, require_utc
from .sizing import SizingMethod


class ContractHandshake(ContractModel):
    """Declared package version at a Kernel/Bridge handshake boundary.

    The v0 compatibility rule is refuse mismatch and co-deploy. This record is a
    shape only; the future consumer owns the fail-closed refusal.
    """

    component_id: NonEmptyStr
    component_role: Literal["KERNEL", "BRIDGE"]
    declared_contract_version: Literal[CONTRACT_VERSION] = CONTRACT_VERSION
    declared_at: datetime

    @model_validator(mode="after")
    def validate_timestamp(self) -> ContractHandshake:
        require_utc(self.declared_at)
        return self


class MissingRuleStatus(str, Enum):
    NOT_EXPRESSIBLE = "NOT_EXPRESSIBLE"


class MissingRuleRecord(ContractModel):
    """Freeze failure for a source rule that requires forbidden account state."""

    record_id: NonEmptyStr
    candidate_id: NonEmptyStr
    source_rule_id: NonEmptyStr
    source_rule_provenance: NonEmptyStr
    status: Literal[MissingRuleStatus.NOT_EXPRESSIBLE] = (
        MissingRuleStatus.NOT_EXPRESSIBLE
    )
    reason: NonEmptyStr
    substitute: NonEmptyStr
    substitute_catalogue_version: NonEmptyStr
    substitute_sizing_method: SizingMethod
    package_hash: Sha256 | None = None


class DeterministicSizingBatch(ContractModel):
    """One per-bucket/bar-close serial-batch contract; enforcement is downstream."""

    batch_id: NonEmptyStr
    bucket_id: NonEmptyStr
    decision_bar_ts: datetime
    snapshot_id: Sha256
    allocation_policy_version: NonEmptyStr
    worker_order: tuple[NonEmptyStr, ...]
    request_ids: tuple[NonEmptyStr, ...]
    replay_hash: Sha256 | None = None

    @model_validator(mode="after")
    def validate_shape(self) -> DeterministicSizingBatch:
        require_utc(self.decision_bar_ts)
        if len(self.worker_order) != len(self.request_ids):
            raise ValueError("worker_order and request_ids must have the same length")
        if tuple(sorted(self.worker_order)) != self.worker_order:
            raise ValueError("worker_order must be sorted deterministically")
        return self
