"""Risk-bucket, allocation-policy, and Guardian-policy data shapes."""

from __future__ import annotations

from decimal import Decimal
from enum import Enum
from typing import Annotated

from pydantic import Field

from .base import ContractModel, NonEmptyStr

OpenDecimal = Annotated[Decimal, Field(ge=0, allow_inf_nan=False)] | None
OpenInteger = Annotated[int, Field(ge=0)] | None


class GuardianVetoClass(str, Enum):
    BUCKET_CAP = "BUCKET_CAP"
    CORRELATION = "CORRELATION"
    STALENESS = "STALENESS"
    VENUE_STATE = "VENUE_STATE"
    DAILY_LOSS = "DAILY_LOSS"
    PROTECTION_UNPLACEABLE = "PROTECTION_UNPLACEABLE"
    POLICY_ERROR = "POLICY_ERROR"


class RiskBucketMember(ContractModel):
    candidate_id: NonEmptyStr
    package_hash: str = Field(pattern=r"^[0-9a-f]{64}$")
    weight: OpenDecimal = Field(
        default=None, description="[OPEN]; unset is fail-closed"
    )


class RiskBucket(ContractModel):
    """Risk-bucket shape. Every numeric policy threshold is [OPEN].

    Consumers must treat every unset threshold as fail-closed. This package
    records the shape and chooses or applies no threshold.
    """

    bucket_id: NonEmptyStr
    allocation_policy_version: NonEmptyStr
    capital_allocation: OpenDecimal = Field(
        default=None,
        description="[OPEN] fraction of account equity; unset is fail-closed",
    )
    max_gross_exposure: OpenDecimal = Field(
        default=None,
        description="[OPEN] fraction of bucket capital; unset is fail-closed",
    )
    max_bucket_leverage: OpenDecimal = Field(
        default=None, description="[OPEN]; unset is fail-closed"
    )
    max_daily_loss: OpenDecimal = Field(
        default=None,
        description="[OPEN] fraction of bucket capital; unset is fail-closed",
    )
    max_drawdown: OpenDecimal = Field(
        default=None,
        description="[OPEN] with separately defined peak reference; unset is fail-closed",
    )
    max_concurrent: OpenInteger = Field(
        default=None, description="[OPEN]; unset is fail-closed"
    )
    correlation_cap: OpenDecimal = Field(
        default=None,
        description="[OPEN] max pairwise absolute correlation; unset is fail-closed",
    )
    session_rule: NonEmptyStr | None = None
    evaluation_cadence: NonEmptyStr | None = None
    members: tuple[RiskBucketMember, ...] = ()
    venue_binding: NonEmptyStr | None = None


class AllocationPolicy(ContractModel):
    """Versioned allocation caps. Unset numeric thresholds are fail-closed."""

    version: NonEmptyStr
    bucket_ids: tuple[NonEmptyStr, ...]
    max_total_exposure: OpenDecimal = Field(
        default=None, description="[OPEN]; unset is fail-closed"
    )
    max_leverage: OpenDecimal = Field(
        default=None, description="[OPEN]; unset is fail-closed"
    )
    max_correlated_exposure: OpenDecimal = Field(
        default=None, description="[OPEN]; unset is fail-closed"
    )
    affected_environments: tuple[NonEmptyStr, ...] | None = Field(
        default=None,
        description="Unstated means all environments are invalidated by a material change",
    )


class GuardianPolicy(ContractModel):
    """Versioned Guardian definition. Unset numeric thresholds are fail-closed."""

    version: NonEmptyStr
    threshold_source_version: NonEmptyStr
    allowed_input_classes: tuple[str, ...] = (
        "BUCKET_EXPOSURE_AND_CAPS",
        "CORRELATION",
        "SNAPSHOT_FRESHNESS",
        "VENUE_STATE",
        "DAILY_LOSS_LEDGER",
        "PROTECTION_PLACEABILITY",
    )
    veto_classes: tuple[GuardianVetoClass, ...] = tuple(GuardianVetoClass)
    repeated_veto_flap_threshold: Annotated[int, Field(gt=0)] | None = Field(
        default=None, description="[OPEN]; unset is fail-closed"
    )
