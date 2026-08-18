"""Core pydantic models (Bar, Signal, OrderPlan, Position, etc.)."""

from __future__ import annotations

import math
from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal, InvalidOperation
from enum import Enum
from typing import Any, Literal

from pydantic import BaseModel


class Bar(BaseModel):
    ts: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float


class Signal(BaseModel):
    ts: datetime
    symbol: str
    direction: Literal["LONG", "SHORT", "FLAT"]
    reason: str
    ref_price: float
    stop_loss: float | None = None
    take_profit: float | None = None


class OrderPlan(BaseModel):
    decision_uid: str | None = None
    signal: Signal
    qty: float
    entry_type: Literal["MKT", "LMT"]
    limit_price: float | None = None
    stop_loss: float
    take_profit: float | None = None
    leverage: int = 1
    risk_dollars: float = 0.0
    risk_pct: float = 0.0


class Position(BaseModel):
    symbol: str
    size: float
    entry_px: float
    unrealized: float = 0.0
    leverage: int = 1
    liquidation_px: float | None = None
    margin_used: float = 0.0


class AccountSnapshot(BaseModel):
    equity: float
    available_margin: float
    withdrawable: float = 0.0


class BrokerOrder(BaseModel):
    cloid: str
    oid: int | None = None
    coin: str
    side: Literal["BUY", "SELL"]
    size: float
    status: str = "OPEN"
    role: Literal["ENTRY", "SL", "TP", "CLOSE", "UNKNOWN"] = "UNKNOWN"
    reduce_only: bool = False
    trigger_px: float | None = None
    order_type: str | None = None
    order_ref: str | None = None


class FillEvent(BaseModel):
    event_type: Literal["FILL"] = "FILL"
    fill_id: str
    cloid: str
    coin: str
    qty: float
    px: float
    ts: datetime
    fee: float = 0.0
    funding: float = 0.0
    role: Literal["ENTRY", "SL", "TP", "CLOSE", "UNKNOWN"] = "UNKNOWN"


class OrderUpdateEvent(BaseModel):
    event_type: Literal["ORDER"] = "ORDER"
    cloid: str
    status: str
    ts: datetime
    filled_qty: float | None = None
    avg_fill_px: float | None = None


BrokerEvent = FillEvent | OrderUpdateEvent


class Rejection(BaseModel):
    stage: Literal["RISK", "LLM", "STATE"]
    reason: str


class RegimeDirective(BaseModel):
    ts: datetime
    regime: Literal["LONG_ONLY", "SHORT_ONLY", "BOTH", "NO_TRADE"]
    confidence: float
    ttl_minutes: int
    sources: list[str]
    rationale: str


class OrderState(str, Enum):
    """Canonical order lifecycle states (TS-P1-001, ADR-0023).

    TS-P1-004 wires partial-fill and cancel-reservation progress into durable
    order status. See docs/22_ORDER_STATE_CONTRACT.md for the full glossary,
    raw-status mapping, and transition table.
    """

    PENDING_NEW = "PENDING_NEW"
    SUBMITTING = "SUBMITTING"
    SUBMITTED = "SUBMITTED"
    OPEN = "OPEN"
    PARTIALLY_FILLED = "PARTIALLY_FILLED"
    PENDING_CANCEL = "PENDING_CANCEL"
    FILLED = "FILLED"
    CANCELED = "CANCELED"
    REJECTED = "REJECTED"
    EXPIRED = "EXPIRED"
    UNKNOWN_SUBMISSION = "UNKNOWN_SUBMISSION"


TERMINAL_ORDER_STATES: frozenset[OrderState] = frozenset(
    {OrderState.FILLED, OrderState.CANCELED, OrderState.REJECTED, OrderState.EXPIRED}
)


class _ImmutableMapping(tuple, Mapping):
    """Read-only Mapping with no mutable object anywhere in its referent graph,
    and no writable holder attribute that could later replace its contents.

    `MappingProxyType(d)` blocks writes *through the proxy*, but `d` itself
    remains a plain `dict` and is returned directly by
    `gc.get_referents(proxy)` — mutating that `dict` still changes what the
    proxy reports, whether or not `d` is bound to a module-level name (audit
    F1-R). An earlier revision of this class stored its `(key, value)` pairs
    in an instance attribute (`self._pairs = tuple(pairs)`), which closed the
    *contents* hole (tuples cannot be mutated in place) but left a second,
    distinct hole open: `_pairs` was itself a writable slot, so normal
    attribute assignment or `object.__setattr__` could replace the whole
    tuple wholesale and change every later `can_transition`/
    `normalize_raw_order_status` decision, even though no individual
    container was ever mutated in place (audit finding, this repair).
    This class closes that hole by not having an instance attribute at all:
    it subclasses `tuple` directly and stores its `(key, value)` pairs as the
    tuple's own elements, fixed at `tuple.__new__` time. Combined with
    `__slots__ = ()` — and `collections.abc.Mapping` itself declaring
    `__slots__ = ()` — instances have no `__dict__` and no assignable slot of
    any kind, so there is no `_pairs` attribute-holder left to reassign.

    A zero-slot tuple subclass can still inherit `object`'s special
    `__class__` assignment path and be changed to a layout-compatible class.
    The read-only `__class__` data descriptor below shadows that inherited
    path for both ordinary instance assignment and `object.__setattr__`;
    both raise `AttributeError` before the runtime can replace the type.
    Direct calls to an inherited/base `__class__` descriptor and broader
    runtime compromise are outside the owner-approved threat model documented
    in the contract. A caller walking `gc.get_referents` transitively from an
    instance of this class only ever reaches tuples, `frozenset`s, and
    `OrderState`/`str` values — never a `dict` or `list` it could mutate.
    """

    __slots__ = ()

    def __new__(cls, pairs):
        return super().__new__(cls, tuple(pairs))

    @property
    def __class__(self):
        """Expose the actual type while rejecting instance-level replacement."""
        return type(self)

    def __getitem__(self, key):
        for stored_key, value in tuple.__iter__(self):
            if stored_key == key:
                return value
        raise KeyError(key)

    def __iter__(self):
        return (stored_key for stored_key, _ in tuple.__iter__(self))

    def __len__(self) -> int:
        return tuple.__len__(self)

    def __repr__(self) -> str:
        return f"{type(self).__name__}({dict(tuple.__iter__(self))!r})"


ORDER_STATE_TRANSITIONS: Mapping[OrderState, frozenset[OrderState]] = _ImmutableMapping((
    (OrderState.PENDING_NEW, frozenset({OrderState.PENDING_NEW, OrderState.SUBMITTING})),
    (
        OrderState.SUBMITTING,
        frozenset(
            {
                OrderState.SUBMITTING,
                OrderState.SUBMITTED,
                OrderState.REJECTED,
                OrderState.UNKNOWN_SUBMISSION,
            }
        ),
    ),
    (
        OrderState.SUBMITTED,
        frozenset(
            {
                OrderState.SUBMITTED,
                OrderState.OPEN,
                OrderState.REJECTED,
                OrderState.FILLED,
                OrderState.PARTIALLY_FILLED,
                OrderState.EXPIRED,
                OrderState.PENDING_CANCEL,
                OrderState.CANCELED,
            }
        ),
    ),
    (
        OrderState.OPEN,
        frozenset(
            {
                OrderState.OPEN,
                OrderState.PARTIALLY_FILLED,
                OrderState.FILLED,
                OrderState.PENDING_CANCEL,
                OrderState.CANCELED,
                OrderState.EXPIRED,
            }
        ),
    ),
    (
        OrderState.PARTIALLY_FILLED,
        frozenset(
            {
                OrderState.PARTIALLY_FILLED,
                OrderState.FILLED,
                OrderState.PENDING_CANCEL,
                OrderState.CANCELED,
                OrderState.EXPIRED,
            }
        ),
    ),
    (
        OrderState.PENDING_CANCEL,
        frozenset(
            {
                OrderState.PENDING_CANCEL,
                OrderState.CANCELED,
                OrderState.FILLED,
                OrderState.PARTIALLY_FILLED,
                OrderState.OPEN,
                OrderState.EXPIRED,
            }
        ),
    ),
    (
        OrderState.UNKNOWN_SUBMISSION,
        frozenset(
            {
                OrderState.UNKNOWN_SUBMISSION,
                OrderState.SUBMITTED,
                OrderState.OPEN,
                OrderState.PARTIALLY_FILLED,
                OrderState.PENDING_CANCEL,
                OrderState.FILLED,
                OrderState.CANCELED,
                OrderState.REJECTED,
                OrderState.EXPIRED,
            }
        ),
    ),
    (OrderState.FILLED, frozenset({OrderState.FILLED})),
    (OrderState.CANCELED, frozenset({OrderState.CANCELED})),
    (OrderState.REJECTED, frozenset({OrderState.REJECTED})),
    (OrderState.EXPIRED, frozenset({OrderState.EXPIRED})),
))


class IllegalOrderTransitionError(Exception):
    """Raised when a requested order-state transition is not in ORDER_STATE_TRANSITIONS."""

    def __init__(self, from_state: OrderState, to_state: OrderState) -> None:
        self.from_state = from_state
        self.to_state = to_state
        self.reason_code = "ILLEGAL_ORDER_TRANSITION"
        super().__init__(
            f"{self.reason_code}: illegal order-state transition: "
            f"{from_state.value} -> {to_state.value}"
        )


def can_transition(from_state: OrderState, to_state: OrderState) -> bool:
    """Pure query: never raises, never mutates ORDER_STATE_TRANSITIONS."""
    return to_state in ORDER_STATE_TRANSITIONS.get(from_state, frozenset())


def validate_order_transition(from_state: OrderState, to_state: OrderState) -> OrderState:
    """Fail-closed: returns to_state on a legal transition, else raises."""
    if not can_transition(from_state, to_state):
        raise IllegalOrderTransitionError(from_state, to_state)
    return to_state


class UnknownRawOrderStatusError(Exception):
    """Raised when a raw broker/DB status string cannot be normalized.

    Fail-closed by design: never defaults to a live/filled/retryable state.
    The message is a constant string per `reason_code` and never accesses
    any attribute of `raw` or `type(raw)` — not `repr()`/`str()`, and not
    even `type(raw).__name__` (accessing a class's `__name__` is dispatched
    through its metaclass, so a caller-controlled metaclass can intercept
    that lookup and raise; audit F2-R). `.raw` still holds the original
    object unmodified for a caller who wants to inspect it directly.
    """

    def __init__(self, raw: object, reason_code: str) -> None:
        self.raw = raw
        self.reason_code = reason_code
        super().__init__(f"{reason_code}: raw order status could not be normalized")


RAW_ORDER_STATUS_ALIASES: Mapping[str, OrderState] = _ImmutableMapping((
    ("OPEN", OrderState.OPEN),
    ("SUBMITTED", OrderState.SUBMITTED),
    ("PENDING", OrderState.SUBMITTED),
    ("PARTIALLY_FILLED", OrderState.PARTIALLY_FILLED),
    ("PENDING_CANCEL", OrderState.PENDING_CANCEL),
    ("FILLED", OrderState.FILLED),
    ("CANCELED", OrderState.CANCELED),
    ("CANCELLED", OrderState.CANCELED),
    ("CANCELLED_BY_ENGINE", OrderState.CANCELED),
    ("REJECTED", OrderState.REJECTED),
    ("EXPIRED", OrderState.EXPIRED),
))


def normalize_raw_order_status(raw: object) -> OrderState:
    """Normalize a raw broker/DB status string to a canonical OrderState.

    Case/whitespace-tolerant for known aliases (matches existing adapter
    behavior, e.g. hyperliquid.py's `.upper()` normalization). Anything not
    an exact known alias fails closed with UnknownRawOrderStatusError instead
    of defaulting to OPEN/SUBMITTED/FILLED.
    """
    if not isinstance(raw, str):
        raise UnknownRawOrderStatusError(raw, "NON_STRING_RAW_STATUS")
    key = raw.strip().upper()
    if not key:
        raise UnknownRawOrderStatusError(raw, "EMPTY_RAW_STATUS")
    try:
        return RAW_ORDER_STATUS_ALIASES[key]
    except KeyError:
        raise UnknownRawOrderStatusError(raw, "UNRECOGNIZED_RAW_STATUS") from None


# ===========================================================================
# TS-P1-004 — partial-fill protect-or-flatten model
#
# Pure model only: no broker I/O, no persistence, no clock. The state
# machine that consumes these lives in engine/orders.py; the durable v5
# ledger lives in store/db.py. See docs/25_PARTIAL_FILL_PROTECTION_CONTRACT.md.
# ===========================================================================


PROTECT_DEADLINE_S: float = 10.0
"""Non-resetting primary protect-or-flatten budget (owner decision 1)."""

FLATTEN_VERIFY_DEADLINE_S: float = 5.0
"""Non-resetting flatten-verification budget (owner decision 1)."""


class LotQuantizationError(Exception):
    """Fail-closed: a size could not be expressed in exact integer lot units."""

    def __init__(self, reason_code: str) -> None:
        self.reason_code = reason_code
        super().__init__(f"{reason_code}: size is not an exact lot multiple")


@dataclass(frozen=True)
class LotUnit:
    """Exchange size quantum for one symbol, expressed as decimal places.

    ``size_decimals`` comes from exchange metadata (Hyperliquid ``szDecimals``)
    or an explicit test fixture. A missing or invalid quantum is fail-closed:
    callers must treat ``None`` as "cannot size an order" and abort without
    mutation, never fall back to raw float comparison.
    """

    size_decimals: int

    def __post_init__(self) -> None:
        value = self.size_decimals
        if isinstance(value, bool) or not isinstance(value, int):
            raise LotQuantizationError("INVALID_SIZE_QUANTUM")
        if value < 0 or value > 18:
            raise LotQuantizationError("INVALID_SIZE_QUANTUM")

    @property
    def scale(self) -> Decimal:
        return Decimal(10) ** self.size_decimals


def quantize_lots(value: float | int | str | Decimal, lot: LotUnit) -> int:
    """Exact integer lot normalization; never an epsilon comparison.

    The value is read through its shortest exact decimal spelling, scaled by
    the symbol quantum, and rejected unless the result is an exact integer.
    Binary-float residue (e.g. ``0.1 + 0.2``) therefore fails closed instead of
    silently rounding to a tradeable size.
    """
    if isinstance(value, bool):
        raise LotQuantizationError("NON_NUMERIC_SIZE")
    if isinstance(value, float) and not math.isfinite(value):
        raise LotQuantizationError("NON_FINITE_SIZE")
    try:
        decimal_value = value if isinstance(value, Decimal) else Decimal(str(value))
    except (InvalidOperation, ValueError, TypeError) as exc:
        raise LotQuantizationError("NON_NUMERIC_SIZE") from exc
    if not decimal_value.is_finite():
        raise LotQuantizationError("NON_FINITE_SIZE")
    scaled = decimal_value * lot.scale
    if scaled != scaled.to_integral_value():
        raise LotQuantizationError("NON_LOT_MULTIPLE")
    return int(scaled)


def lots_to_size(lots: int, lot: LotUnit) -> float:
    """Inverse of :func:`quantize_lots` for order placement."""
    if isinstance(lots, bool) or not isinstance(lots, int):
        raise LotQuantizationError("NON_INTEGER_LOTS")
    return float(Decimal(lots) / lot.scale)


class ActionOutcome(str, Enum):
    """Typed broker verdict for one reserved partial-recovery action.

    ``NOT_APPLIED`` means *proven* not applied. Transport failures, malformed
    bodies, missing fields, and timeouts are always ``UNKNOWN`` — never an
    optimistic success and never a licence to retry blindly.
    """

    APPLIED = "APPLIED"
    NOT_APPLIED = "NOT_APPLIED"
    UNKNOWN = "UNKNOWN"


class ActionRecordStatus(str, Enum):
    """Append-only action-event vocabulary in ``partial_fill_action_events``."""

    RESERVED = "RESERVED"
    SENT = "SENT"
    APPLIED = "APPLIED"
    NOT_APPLIED = "NOT_APPLIED"
    UNKNOWN = "UNKNOWN"
    EVIDENCE = "EVIDENCE"


class PartialActionKind(str, Enum):
    """Deterministic action-identity domains."""

    INSTALL_STOP = "INSTALL_STOP"
    CANCEL_ENTRY = "CANCEL_ENTRY"
    CANCEL_PROTECTION = "CANCEL_PROTECTION"
    FLATTEN = "FLATTEN"


class Provenance(str, Enum):
    """Ownership verdict for the authoritative symbol state."""

    OWNED = "OWNED"
    MIXED = "MIXED"
    FOREIGN = "FOREIGN"
    AMBIGUOUS = "AMBIGUOUS"
    UNVERIFIED = "UNVERIFIED"


class PartialProtectionState(str, Enum):
    """Recovery-generation state; deliberately separate from ``OrderState``."""

    PARTIAL_DETECTED = "PARTIAL_DETECTED"
    PROTECTION_PENDING = "PROTECTION_PENDING"
    PROTECTION_VERIFIED = "PROTECTION_VERIFIED"
    PROTECTED_PARTIAL = "PROTECTED_PARTIAL"
    CANCEL_PENDING = "CANCEL_PENDING"
    CANCEL_UNKNOWN = "CANCEL_UNKNOWN"
    FLATTEN_PENDING = "FLATTEN_PENDING"
    FLATTEN_UNKNOWN = "FLATTEN_UNKNOWN"
    SAFE_FLAT = "SAFE_FLAT"
    UNPROTECTED_ABORT = "UNPROTECTED_ABORT"


PARTIAL_ACCEPTING_STATES: frozenset[PartialProtectionState] = frozenset({
    PartialProtectionState.PROTECTED_PARTIAL,
    PartialProtectionState.SAFE_FLAT,
})

PARTIAL_TERMINAL_STATES: frozenset[PartialProtectionState] = frozenset({
    PartialProtectionState.PROTECTED_PARTIAL,
    PartialProtectionState.SAFE_FLAT,
    PartialProtectionState.UNPROTECTED_ABORT,
})


PARTIAL_STATE_TRANSITIONS: Mapping[
    PartialProtectionState, frozenset[PartialProtectionState]
] = _ImmutableMapping((
    (
        PartialProtectionState.PARTIAL_DETECTED,
        frozenset({
            PartialProtectionState.PARTIAL_DETECTED,
            PartialProtectionState.PROTECTION_PENDING,
            PartialProtectionState.CANCEL_PENDING,
            PartialProtectionState.FLATTEN_PENDING,
            PartialProtectionState.UNPROTECTED_ABORT,
        }),
    ),
    (
        PartialProtectionState.PROTECTION_PENDING,
        frozenset({
            PartialProtectionState.PROTECTION_PENDING,
            PartialProtectionState.PROTECTION_VERIFIED,
            PartialProtectionState.PARTIAL_DETECTED,
            PartialProtectionState.FLATTEN_PENDING,
            PartialProtectionState.UNPROTECTED_ABORT,
        }),
    ),
    (
        PartialProtectionState.PROTECTION_VERIFIED,
        frozenset({
            PartialProtectionState.PROTECTION_VERIFIED,
            PartialProtectionState.CANCEL_PENDING,
            PartialProtectionState.PARTIAL_DETECTED,
            PartialProtectionState.FLATTEN_PENDING,
            PartialProtectionState.UNPROTECTED_ABORT,
        }),
    ),
    (
        PartialProtectionState.CANCEL_PENDING,
        frozenset({
            PartialProtectionState.CANCEL_PENDING,
            PartialProtectionState.CANCEL_UNKNOWN,
            PartialProtectionState.PROTECTED_PARTIAL,
            PartialProtectionState.PARTIAL_DETECTED,
            PartialProtectionState.FLATTEN_PENDING,
            PartialProtectionState.SAFE_FLAT,
            PartialProtectionState.UNPROTECTED_ABORT,
        }),
    ),
    (
        PartialProtectionState.CANCEL_UNKNOWN,
        frozenset({
            PartialProtectionState.CANCEL_UNKNOWN,
            PartialProtectionState.CANCEL_PENDING,
            PartialProtectionState.PROTECTED_PARTIAL,
            PartialProtectionState.PARTIAL_DETECTED,
            PartialProtectionState.FLATTEN_PENDING,
            PartialProtectionState.UNPROTECTED_ABORT,
        }),
    ),
    (
        PartialProtectionState.PROTECTED_PARTIAL,
        frozenset({
            PartialProtectionState.PROTECTED_PARTIAL,
            # A later authoritative owned fill re-opens quantity recomputation
            # inside the same recovery row (Gate 1 §4).
            PartialProtectionState.PARTIAL_DETECTED,
        }),
    ),
    (
        PartialProtectionState.FLATTEN_PENDING,
        frozenset({
            PartialProtectionState.FLATTEN_PENDING,
            PartialProtectionState.FLATTEN_UNKNOWN,
            PartialProtectionState.SAFE_FLAT,
            PartialProtectionState.UNPROTECTED_ABORT,
        }),
    ),
    (
        PartialProtectionState.FLATTEN_UNKNOWN,
        frozenset({
            PartialProtectionState.FLATTEN_UNKNOWN,
            PartialProtectionState.FLATTEN_PENDING,
            PartialProtectionState.SAFE_FLAT,
            PartialProtectionState.UNPROTECTED_ABORT,
        }),
    ),
    (PartialProtectionState.SAFE_FLAT, frozenset({PartialProtectionState.SAFE_FLAT})),
    (
        PartialProtectionState.UNPROTECTED_ABORT,
        frozenset({PartialProtectionState.UNPROTECTED_ABORT}),
    ),
))


class IllegalPartialTransitionError(Exception):
    """Raised when a partial-recovery transition is not declared legal."""

    def __init__(
        self, from_state: PartialProtectionState, to_state: PartialProtectionState
    ) -> None:
        self.from_state = from_state
        self.to_state = to_state
        self.reason_code = "ILLEGAL_PARTIAL_TRANSITION"
        super().__init__(
            f"{self.reason_code}: {from_state.value} -> {to_state.value}"
        )


def can_transition_partial(
    from_state: PartialProtectionState, to_state: PartialProtectionState
) -> bool:
    """Pure query; never raises, never mutates the policy table."""
    return to_state in PARTIAL_STATE_TRANSITIONS.get(from_state, frozenset())


def validate_partial_transition(
    from_state: PartialProtectionState, to_state: PartialProtectionState
) -> PartialProtectionState:
    if not can_transition_partial(from_state, to_state):
        raise IllegalPartialTransitionError(from_state, to_state)
    return to_state


def canonical_order_state(
    *,
    raw_status: object,
    ordered_qty: float,
    filled_qty: float,
    lot: LotUnit | None = None,
    cancel_reserved: bool = False,
) -> OrderState:
    """Derive the canonical order state from durable quantities and evidence.

    ``orders.status`` keeps its accepted v4 raw spelling — this task does not
    rewrite the legacy status column — but the *canonical* lifecycle state is
    wired by quantity exactly as ADR-0023 and Gate 1 §4 require:

    * ``0 < filled < ordered`` -> ``PARTIALLY_FILLED``
    * a cancel reserved before I/O -> ``PENDING_CANCEL``
    * an exchange-confirmed terminal raw status wins over both

    Quantities are compared only in exact integer lot units. Missing quantum,
    non-lot evidence, and overfill are integrity failures rather than states.
    """
    base = normalize_raw_order_status(raw_status)
    if lot is None:
        raise LotQuantizationError("SIZE_QUANTUM_UNAVAILABLE")
    ordered_units = quantize_lots(ordered_qty, lot)
    filled_units = quantize_lots(filled_qty, lot)
    if filled_units < 0 or ordered_units <= 0:
        raise LotQuantizationError("NON_POSITIVE_ORDER_QUANTITY")
    if filled_units > ordered_units:
        raise LotQuantizationError("ORDER_OVERFILL")
    if base in TERMINAL_ORDER_STATES:
        return base
    if filled_units == ordered_units:
        return validate_order_transition(base, OrderState.FILLED)
    if cancel_reserved:
        return validate_order_transition(base, OrderState.PENDING_CANCEL)
    if filled_units > 0:
        return validate_order_transition(base, OrderState.PARTIALLY_FILLED)
    return base


@dataclass(frozen=True)
class Evidence:
    """Bounded, secret-safe provenance for one typed broker result."""

    source: str
    reason_code: str
    observed_ts: datetime | None = None
    detail: str = ""

    def as_payload(self) -> dict[str, Any]:
        return {
            "source": self.source,
            "reason_code": self.reason_code,
            "observed_ts": (
                self.observed_ts.isoformat() if self.observed_ts is not None else None
            ),
            "detail": self.detail[:512],
        }


@dataclass(frozen=True)
class CancelResult:
    outcome: ActionOutcome
    cloid: str
    evidence: Evidence


@dataclass(frozen=True)
class PlaceResult:
    outcome: ActionOutcome
    cloid: str
    exchange_order_id: int | None
    evidence: Evidence


@dataclass(frozen=True)
class FlattenResult:
    outcome: ActionOutcome
    cloid: str | None
    evidence: Evidence


@dataclass(frozen=True)
class OrderQueryResult:
    """Direct single-order evidence.

    ``known`` is False whenever the adapter could not obtain an authoritative
    answer (transport error, unparseable body, truncated page). A caller must
    treat ``known=False`` as UNKNOWN and must never read ``found``/``terminal``
    as proof in that case.
    """

    known: bool
    found: bool = False
    terminal: bool = False
    raw_status: str | None = None
    filled_size: float | None = None
    evidence: Evidence = field(
        default_factory=lambda: Evidence("QUERY_ORDER", "UNSPECIFIED")
    )


@dataclass(frozen=True)
class OrderView:
    """One live exchange order as seen inside a bounded symbol snapshot."""

    cloid: str
    coin: str
    side: Literal["BUY", "SELL"]
    size: float
    role: str = "UNKNOWN"
    reduce_only: bool = False
    trigger_px: float | None = None
    status: str = "OPEN"
    order_ref: str | None = None


@dataclass(frozen=True)
class SymbolSnapshot:
    """Bounded per-symbol evidence tuple.

    ``exact`` is True only when the position read *and* the open-order read
    both succeeded, are mutually consistent, and the size quantum is known.
    Anything less is never treated as safe.
    """

    symbol: str
    exact: bool
    net_size: float | None
    open_orders: tuple[OrderView, ...]
    lot: LotUnit | None
    evidence: Evidence
    observed_ts: datetime | None = None
