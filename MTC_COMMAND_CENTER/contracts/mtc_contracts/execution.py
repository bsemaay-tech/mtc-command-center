"""Freshness, evidence-window, reconciliation, Guardian, and ledger shapes."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Annotated

from pydantic import Field, model_validator

from .base import ContractModel, NonEmptyStr, Sha256, require_utc
from .lineage import Environment, EnvironmentLineage
from .risk import GuardianVetoClass


class FreshnessState(str, Enum):
    FRESH = "FRESH"
    AGING = "AGING"
    STALE = "STALE"
    UNKNOWN = "UNKNOWN"
    DRIFT = "DRIFT"
    DEGRADED = "DEGRADED"
    RECOVERING = "RECOVERING"


class FreshnessDomain(str, Enum):
    MARKET = "MARKET"
    ORDER = "ORDER"
    FILL = "FILL"
    ACCOUNT = "ACCOUNT"
    RECONCILER = "RECONCILER"


class FreshnessEvent(ContractModel):
    """Shared freshness event. Numeric boundaries are [OPEN] and fail-closed."""

    domain: FreshnessDomain
    state: FreshnessState
    observed_at: datetime
    source_timestamp: datetime | None
    age_ms: Annotated[int, Field(ge=0)] | None
    freshness_threshold_ms: Annotated[int, Field(gt=0)] | None = Field(
        default=None, description="[OPEN]; unset is fail-closed"
    )
    worker_id: NonEmptyStr
    environment: Environment

    @model_validator(mode="after")
    def validate_timestamps(self) -> FreshnessEvent:
        require_utc(self.observed_at)
        if self.source_timestamp is not None:
            require_utc(self.source_timestamp)
        return self


class EvidenceWindowStatus(str, Enum):
    OPEN = "OPEN"
    CLOSED = "CLOSED"
    INVALIDATED = "INVALIDATED"
    PRIOR_IDENTITY = "PRIOR_IDENTITY"


class EvidenceWindow(ContractModel):
    """Worker- and environment-scoped evidence window; thresholds are [OPEN]."""

    window_id: NonEmptyStr
    worker_id: NonEmptyStr
    environment: Environment
    deployment_identity_hash: Sha256
    started_at: datetime
    ended_at: datetime | None
    status: EvidenceWindowStatus
    environment_lineage: EnvironmentLineage
    outage_threshold_ms: Annotated[int, Field(gt=0)] | None = Field(
        default=None, description="[OPEN]; unset is fail-closed"
    )

    @model_validator(mode="after")
    def validate_timestamps(self) -> EvidenceWindow:
        require_utc(self.started_at)
        if self.ended_at is not None:
            require_utc(self.ended_at)
        return self


class EvidenceGapRecord(ContractModel):
    gap_id: NonEmptyStr
    window_id: NonEmptyStr
    worker_id: NonEmptyStr
    environment: Environment
    deployment_identity_hash: Sha256
    gap_started_at: datetime
    gap_ended_at: datetime | None
    reason: NonEmptyStr
    explained: bool
    reconciliation_record_id: NonEmptyStr | None
    invalidates_window: bool
    environment_lineage: EnvironmentLineage

    @model_validator(mode="after")
    def validate_timestamps(self) -> EvidenceGapRecord:
        require_utc(self.gap_started_at)
        if self.gap_ended_at is not None:
            require_utc(self.gap_ended_at)
        return self


class ReconciliationMode(str, Enum):
    TWO_WAY_INTERIM = "TWO_WAY_INTERIM"
    THREE_WAY = "THREE_WAY"


class ReconciliationStatus(str, Enum):
    MATCHED = "MATCHED"
    DIVERGED = "DIVERGED"
    UNKNOWN = "UNKNOWN"


class ReconciliationRecord(ContractModel):
    reconciliation_id: NonEmptyStr
    mode: ReconciliationMode
    worker_id: NonEmptyStr
    environment: Environment
    deployment_identity_hash: Sha256
    observed_at: datetime
    intended_or_authorized_hash: Sha256 | None
    store_hash: Sha256
    venue_hash: Sha256
    status: ReconciliationStatus
    breaks: tuple[NonEmptyStr, ...]
    environment_lineage: EnvironmentLineage

    @model_validator(mode="after")
    def validate_mode(self) -> ReconciliationRecord:
        require_utc(self.observed_at)
        if (
            self.mode is ReconciliationMode.THREE_WAY
            and self.intended_or_authorized_hash is None
        ):
            raise ValueError(
                "THREE_WAY reconciliation requires intended/authorized truth"
            )
        return self


class GuardianOutcome(str, Enum):
    AUTHORIZED_AS_REQUESTED = "AUTHORIZED_AS_REQUESTED"
    REJECTED = "REJECTED"


class GuardianDecision(ContractModel):
    decision_id: NonEmptyStr
    deployment_identity_hash: Sha256
    policy_version: NonEmptyStr
    outcome: GuardianOutcome
    veto_class: GuardianVetoClass | None
    reason: NonEmptyStr | None
    timestamp: datetime


class LifecycleWriterClass(str, Enum):
    REGISTRAR = "REGISTRAR"
    ENVIRONMENT_ADMISSION_AUTHORITY = "ENVIRONMENT_ADMISSION_AUTHORITY"
    PROMOTION_AUTHORITY = "PROMOTION_AUTHORITY"
    MULTI_WORKER_SUPERVISOR = "MULTI_WORKER_SUPERVISOR"


class LifecycleEvent(ContractModel):
    """Append-only lifecycle-ledger event shape; this package stores nothing."""

    event_id: NonEmptyStr
    event_type: NonEmptyStr
    writer_id: NonEmptyStr
    writer_class: LifecycleWriterClass
    previous_state: NonEmptyStr | None
    next_state: NonEmptyStr
    candidate_id: NonEmptyStr
    package_hash: Sha256 | None
    deployment_identity_hash: Sha256 | None
    reason: NonEmptyStr
    trigger: NonEmptyStr | None
    evidence_references: tuple[NonEmptyStr, ...]
    timestamp: datetime

    @model_validator(mode="after")
    def validate_timestamp(self) -> LifecycleEvent:
        require_utc(self.timestamp)
        return self
