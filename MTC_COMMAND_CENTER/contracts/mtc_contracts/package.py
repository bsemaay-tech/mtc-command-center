"""Frozen strategy-package and immutable account-snapshot shapes."""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Annotated, Any

from pydantic import Field, model_validator

from .base import ContractModel, NonEmptyStr, Sha256, require_utc
from .sizing import SizingRequest

PositiveDecimal = Annotated[Decimal, Field(gt=0, allow_inf_nan=False)]
NonNegativeDecimal = Annotated[Decimal, Field(ge=0, allow_inf_nan=False)]


class InstrumentMetadata(ContractModel):
    symbol: NonEmptyStr
    tick_size: PositiveDecimal
    lot_size: PositiveDecimal
    min_qty: PositiveDecimal
    min_notional: PositiveDecimal
    contract_multiplier: PositiveDecimal


class StrategyPackage(ContractModel):
    """Frozen deployable strategy semantics; no dataset/evaluation lineage."""

    candidate_id: NonEmptyStr
    family_id: NonEmptyStr
    package_hash: Sha256
    kernel_version: NonEmptyStr
    kernel_code_sha: Sha256
    spec: dict[str, Any]
    exact_params: dict[str, Any]
    modules_enabled: tuple[NonEmptyStr, ...]
    substitute_catalogue_versions: dict[str, str]
    instrument_metadata: InstrumentMetadata
    sizing_requests: tuple[SizingRequest, ...] = ()
    bar_close_only: bool
    degraded_policy: NonEmptyStr | None = Field(
        default=None,
        description="Per-worker policy; absence is fail-closed, never a global permissive default",
    )


class AccountSnapshot(ContractModel):
    """Immutable account truth bound by ``snapshot_id``; never kernel input."""

    snapshot_id: Sha256
    taken_at: datetime
    account_id: NonEmptyStr
    equity: NonNegativeDecimal
    available_margin: NonNegativeDecimal
    bucket_capital: dict[str, NonNegativeDecimal]
    open_exposure: NonNegativeDecimal
    margin_used: NonNegativeDecimal
    positions: dict[str, Decimal] = Field(default_factory=dict)

    @model_validator(mode="after")
    def validate_timestamp(self) -> AccountSnapshot:
        require_utc(self.taken_at)
        return self
