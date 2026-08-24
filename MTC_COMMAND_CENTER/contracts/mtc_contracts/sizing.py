"""Snapshot-independent sizing requests and orchestrator bindings."""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Annotated, Literal

from pydantic import Field, model_validator

from .base import ContractModel, NonEmptyStr, Sha256, require_utc

PositiveDecimal = Annotated[Decimal, Field(gt=0, allow_inf_nan=False)]


class SizingMethod(str, Enum):
    RISK_AT_STOP = "RISK_AT_STOP"
    FIXED_QTY = "FIXED_QTY"
    FIXED_NOTIONAL = "FIXED_NOTIONAL"
    VOLATILITY_TARGET = "VOLATILITY_TARGET"


class SizingSourceClass(str, Enum):
    """Freeze-time provenance only; consumers must never branch on this value."""

    NATIVE_DECLARED = "NATIVE_DECLARED"
    SOURCE_DEFINED = "SOURCE_DEFINED"


class VolatilityTargetParams(ContractModel):
    target_volatility: PositiveDecimal
    estimator_id: NonEmptyStr
    estimator_params: dict[str, str | int | Decimal | bool] = Field(
        default_factory=dict
    )


class SizingRequest(ContractModel):
    """Kernel output with no snapshot, account state, or executable quantity.

    Exactly one ``requested_...`` constant from frozen package configuration is
    present and must match ``sizing_method``. ``sizing_source_class`` is
    provenance only and must not select or alter runtime behaviour.
    """

    sizing_method: SizingMethod
    requested_risk_fraction: PositiveDecimal | None = None
    requested_fixed_qty: PositiveDecimal | None = None
    requested_fixed_notional: PositiveDecimal | None = None
    vol_target_params: VolatilityTargetParams | None = None

    stop_price: PositiveDecimal | None = None
    entry_reference_price: PositiveDecimal
    direction: Literal["LONG", "SHORT"]

    instrument_metadata_hash: Sha256
    kernel_version: NonEmptyStr
    package_hash: Sha256
    decision_bar_ts: datetime
    sizing_source_class: SizingSourceClass
    source_rule_id: NonEmptyStr | None = None
    source_rule_provenance: NonEmptyStr | None = None

    @model_validator(mode="after")
    def validate_request_class(self) -> SizingRequest:
        expected = {
            SizingMethod.RISK_AT_STOP: "requested_risk_fraction",
            SizingMethod.FIXED_QTY: "requested_fixed_qty",
            SizingMethod.FIXED_NOTIONAL: "requested_fixed_notional",
            SizingMethod.VOLATILITY_TARGET: "vol_target_params",
        }[self.sizing_method]
        present = {
            name
            for name in (
                "requested_risk_fraction",
                "requested_fixed_qty",
                "requested_fixed_notional",
                "vol_target_params",
            )
            if getattr(self, name) is not None
        }
        if present != {expected}:
            raise ValueError(
                f"{self.sizing_method.value} requires exactly {expected}; got {sorted(present)}"
            )
        if self.sizing_method is SizingMethod.RISK_AT_STOP and self.stop_price is None:
            raise ValueError("RISK_AT_STOP requires stop_price")
        if self.sizing_source_class is SizingSourceClass.SOURCE_DEFINED:
            if not self.source_rule_id or not self.source_rule_provenance:
                raise ValueError(
                    "SOURCE_DEFINED provenance requires source_rule_id and source_rule_provenance"
                )
        elif self.source_rule_id is not None or self.source_rule_provenance is not None:
            raise ValueError("native sizing cannot carry source-rule provenance")
        require_utc(self.decision_bar_ts)
        return self


class BoundSizingIntent(ContractModel):
    """Orchestrator-bound request consumed by the Risk Allocator.

    Numerical freshness thresholds remain ``[OPEN]``. An unset
    ``snapshot_deadline_ms`` is fail-closed for every consumer; this type only
    records the shape and does not implement that policy.
    """

    request: SizingRequest
    snapshot_id: Sha256
    snapshot_taken_at: datetime
    snapshot_deadline_ms: Annotated[int, Field(gt=0)] | None = Field(
        default=None,
        description="[OPEN]; unset must be treated as fail-closed by consumers",
    )
    allocation_policy_version: NonEmptyStr
    bucket_id: NonEmptyStr
    deployment_identity_hash: Sha256
    allocator_reference_qty: PositiveDecimal | None = Field(
        default=None,
        description="Replay/parity/audit only; absent from production submission paths",
    )

    @model_validator(mode="after")
    def validate_timestamp(self) -> BoundSizingIntent:
        require_utc(self.snapshot_taken_at)
        return self
