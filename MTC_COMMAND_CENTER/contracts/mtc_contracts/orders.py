"""Order and exit intent shapes; no execution behaviour lives here."""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Annotated, Literal

from pydantic import Field, model_validator

from .base import ContractModel, NonEmptyStr, Sha256, require_utc

PositiveDecimal = Annotated[Decimal, Field(gt=0, allow_inf_nan=False)]
Fraction = Annotated[Decimal, Field(gt=0, le=1, allow_inf_nan=False)]


class OrderAction(str, Enum):
    OPEN = "OPEN"
    ADD = "ADD"
    REDUCE = "REDUCE"
    CLOSE = "CLOSE"
    MODIFY_STOP = "MODIFY_STOP"
    MODIFY_TARGET = "MODIFY_TARGET"


class QuantitySemantics(str, Enum):
    DELTA = "DELTA"
    TARGET_TOTAL = "TARGET_TOTAL"


class Authorization(str, Enum):
    AUTHORIZED_AS_REQUESTED = "AUTHORIZED_AS_REQUESTED"
    REJECTED = "REJECTED"


class StopSemantics(str, Enum):
    STRATEGY_NATIVE = "STRATEGY_NATIVE"
    STRATEGY_SYNTHETIC_PLUS_EMERGENCY_NATIVE = (
        "STRATEGY_SYNTHETIC_PLUS_EMERGENCY_NATIVE"
    )


class TakeProfitLeg(ContractModel):
    leg_id: NonEmptyStr
    price: PositiveDecimal
    qty_fraction: Fraction
    activation: NonEmptyStr
    oco_group: NonEmptyStr | None = None


class OrderIntent(ContractModel):
    """Guardian outcome consumed by the Bridge; V2 has no resize state."""

    intent_id: NonEmptyStr
    candidate_id: NonEmptyStr
    package_hash: Sha256
    deployment_identity_hash: Sha256
    worker_id: NonEmptyStr
    revision: Annotated[int, Field(ge=0)]

    decision_bar_ts: datetime
    emitted_at: datetime
    valid_until_bar_ts: datetime

    action: OrderAction
    direction: Literal["LONG", "SHORT"]
    authorized_qty: PositiveDecimal | None
    qty_semantics: QuantitySemantics
    qty_unit: Literal["base", "quote", "contracts"]

    authorization: Authorization
    allocation_policy_version: NonEmptyStr
    snapshot_id: Sha256
    rejection_reason: NonEmptyStr | None = None

    stop_price: PositiveDecimal | None = None
    stop_semantics: StopSemantics
    tp_legs: tuple[TakeProfitLeg, ...] = ()

    entry_reason: NonEmptyStr | None = None
    exit_reason: NonEmptyStr | None = None
    blocked_by: tuple[NonEmptyStr, ...] = ()

    @model_validator(mode="after")
    def validate_authorization_shape(self) -> OrderIntent:
        for value in (self.decision_bar_ts, self.emitted_at, self.valid_until_bar_ts):
            require_utc(value)
        if self.authorization is Authorization.AUTHORIZED_AS_REQUESTED:
            if self.authorized_qty is None:
                raise ValueError("authorized order requires authorized_qty")
            if self.rejection_reason is not None:
                raise ValueError("authorized order cannot carry rejection_reason")
        else:
            if self.authorized_qty is not None:
                raise ValueError("rejected order cannot carry executable quantity")
            if self.rejection_reason is None:
                raise ValueError("rejected order requires rejection_reason")
        if sum((leg.qty_fraction for leg in self.tp_legs), Decimal(0)) > Decimal(1):
            raise ValueError("take-profit leg fractions cannot exceed one position")
        return self


class ExitIntent(ContractModel):
    """Kernel or governed operator request to reduce or tighten protection only."""

    intent_id: NonEmptyStr
    candidate_id: NonEmptyStr
    package_hash: Sha256
    deployment_identity_hash: Sha256
    worker_id: NonEmptyStr
    revision: Annotated[int, Field(ge=0)]
    decision_bar_ts: datetime
    emitted_at: datetime
    valid_until_bar_ts: datetime
    action: Literal["REDUCE", "CLOSE", "MODIFY_STOP", "MODIFY_TARGET"]
    direction: Literal["LONG", "SHORT"]
    requested_price: PositiveDecimal | None = None
    requested_qty: PositiveDecimal | None = None
    qty_semantics: QuantitySemantics
    reduce_only: Literal[True]
    reason: NonEmptyStr

    @model_validator(mode="after")
    def validate_timestamps(self) -> ExitIntent:
        for value in (self.decision_bar_ts, self.emitted_at, self.valid_until_bar_ts):
            require_utc(value)
        return self
