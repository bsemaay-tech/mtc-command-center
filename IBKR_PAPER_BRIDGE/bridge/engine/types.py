"""Core pydantic models (Bar, Signal, OrderPlan, Position, etc.)."""

from __future__ import annotations

import hashlib
import json
import math
from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import UTC, datetime
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


# ---------------------------------------------------------------------------
# Durable order-status vocabulary
#
# `orders.status` is written from several producers: the canonical
# `OrderState` values, the raw-alias spellings accepted by
# `normalize_raw_order_status`, and a small set of legacy spellings that
# `OrderManager._normalize_success_orders` persists verbatim after a
# successful submission (`ACCEPTED`, `RESTING`) or for a child order that is
# still waiting on its parent trigger (`WAITING_CHILD`).
#
# The sets below are *derived* from those three sources rather than
# hand-listed, so a new non-terminal `OrderState` or alias can never silently
# fall out of the "still live on the exchange" query. Anything outside
# `KNOWN_DURABLE_ORDER_STATUSES` is an unknown durable state: it is never
# dropped, it blocks (see `DIFF_LOCAL_ORDER_STATUS_UNKNOWN`).
# ---------------------------------------------------------------------------

LEGACY_LIVE_ORDER_STATUS_SPELLINGS: frozenset[str] = frozenset({
    "ACCEPTED",
    "RESTING",
    "WAITING_CHILD",
})
"""Accepted legacy live spellings persisted by the submission path."""

LIVE_DURABLE_ORDER_STATUSES: frozenset[str] = frozenset(
    {state.value for state in OrderState if state not in TERMINAL_ORDER_STATES}
    | {
        raw
        for raw, state in RAW_ORDER_STATUS_ALIASES.items()
        if state not in TERMINAL_ORDER_STATES
    }
    | LEGACY_LIVE_ORDER_STATUS_SPELLINGS
)
"""Every durable spelling that may still correspond to exchange-side state."""

TERMINAL_DURABLE_ORDER_STATUSES: frozenset[str] = frozenset(
    {state.value for state in TERMINAL_ORDER_STATES}
    | {
        raw
        for raw, state in RAW_ORDER_STATUS_ALIASES.items()
        if state in TERMINAL_ORDER_STATES
    }
)
"""Every durable spelling that is provably finished."""

KNOWN_DURABLE_ORDER_STATUSES: frozenset[str] = (
    LIVE_DURABLE_ORDER_STATUSES | TERMINAL_DURABLE_ORDER_STATUSES
)
"""The closed durable status space; anything else fails closed."""


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


# ---------------------------------------------------------------------------
# TS-P1-005 full reconciliation vocabulary
#
# A full capture is a *composite* of independently fetched components. The
# types below keep every component's completeness, exactness, source bounds and
# provenance separate so that a composite can never be called "current" by
# borrowing a healthy component from another observation.
# ---------------------------------------------------------------------------

FULL_RECONCILE_DEADLINE_S = 5.0
"""D2=A: strict wall-clock budget for one whole full capture."""

FULL_RECONCILE_MAX_SKEW_S = 5.0
"""D2=A: maximum spread between the earliest and latest component source time."""

# NOTE: there is deliberately **no** fixed history-window constant. The
# fills/funding lower bound is durable coverage continuity, never an arbitrary
# lookback: coverage is derived from the pointed checkpoint's immutable
# FILLS/FUNDING component bounds; see `FullReconciler._coverage_bounds`.

FULL_RECONCILE_MAX_PAGES = 32
"""Bounded page budget per paginated component; exceeding it fails closed."""


class ReconcileAttemptState(str, Enum):
    """Explicit attempt lifecycle — success is never inferred."""

    COLLECTING = "COLLECTING"
    COMPLETE = "COMPLETE"
    INCOMPLETE = "INCOMPLETE"
    CONFLICTING = "CONFLICTING"
    STALE = "STALE"


RECONCILE_TERMINAL_STATES = frozenset({
    ReconcileAttemptState.COMPLETE,
    ReconcileAttemptState.INCOMPLETE,
    ReconcileAttemptState.CONFLICTING,
    ReconcileAttemptState.STALE,
})


class ReconcileComponentKind(str, Enum):
    """Every component a complete capture must carry."""

    OPEN_ORDERS = "OPEN_ORDERS"
    FILLS = "FILLS"
    POSITIONS = "POSITIONS"
    BALANCES = "BALANCES"
    MARGIN = "MARGIN"
    FUNDING = "FUNDING"
    PENDING_ACTIONS = "PENDING_ACTIONS"


REQUIRED_RECONCILE_COMPONENTS: tuple[ReconcileComponentKind, ...] = tuple(
    sorted(ReconcileComponentKind, key=lambda kind: kind.value)
)


class ReconcileComponentStatus(str, Enum):
    COMPLETE = "COMPLETE"
    UNAVAILABLE = "UNAVAILABLE"
    TRUNCATED = "TRUNCATED"
    MALFORMED = "MALFORMED"
    CONFLICTING = "CONFLICTING"
    STALE = "STALE"


class ReconcileOwnership(str, Enum):
    """D1=B ownership classes.

    ``FOREIGN_IDENTIFIED`` is reserved for order-level rows carrying a
    complete, non-owned identity. Anything that cannot be attributed — notably
    an exchange position with no owned-order lineage — is
    ``UNKNOWN_OWNERSHIP`` and blocks readiness.
    """

    OWNED = "OWNED"
    FOREIGN_IDENTIFIED = "FOREIGN_IDENTIFIED"
    UNKNOWN_OWNERSHIP = "UNKNOWN_OWNERSHIP"


class FundingAttribution(str, Enum):
    ATTRIBUTED = "ATTRIBUTED"
    UNATTRIBUTED = "UNATTRIBUTED"


class ReconcileDiffKind(str, Enum):
    ORDER = "ORDER"
    POSITION = "POSITION"
    ACCOUNT = "ACCOUNT"
    FUNDING = "FUNDING"
    PENDING_ACTION = "PENDING_ACTION"


# Reason codes are the durable, secret-safe vocabulary of the diff.
DIFF_OWNED_ORDER_MISSING = "OWNED_ORDER_MISSING_ON_EXCHANGE"
DIFF_OWNED_ORDER_QTY_MISMATCH = "OWNED_ORDER_QTY_MISMATCH"
DIFF_OWNED_ORDER_STATUS_MISMATCH = "OWNED_ORDER_STATUS_MISMATCH"
DIFF_OWNED_ORDER_UNKNOWN_QUANTUM = "OWNED_ORDER_SIZE_QUANTUM_UNKNOWN"
DIFF_ORPHAN_OWNED_CLOID = "ORPHAN_OWNED_CLOID"
DIFF_FOREIGN_ORDER_OBSERVED = "FOREIGN_ORDER_OBSERVED"
DIFF_EXCHANGE_IDENTITY_CONFLICT = "EXCHANGE_IDENTITY_CONFLICT"
DIFF_UNKNOWN_OWNERSHIP_ORDER = "UNKNOWN_OWNERSHIP_ORDER"
DIFF_UNKNOWN_OWNERSHIP_POSITION = "UNKNOWN_OWNERSHIP_POSITION"
DIFF_POSITION_QTY_MISMATCH = "POSITION_QTY_MISMATCH"
DIFF_POSITION_UNKNOWN_QUANTUM = "POSITION_SIZE_QUANTUM_UNKNOWN"
DIFF_ACCOUNT_INCONSISTENT = "ACCOUNT_ARITHMETIC_INCONSISTENT"
DIFF_PENDING_ACTION_DIVERGENCE = "PENDING_ACTION_DIVERGENCE"
DIFF_FUNDING_UNATTRIBUTED = "FUNDING_UNATTRIBUTED"
DIFF_LOCAL_ORDER_STATUS_UNKNOWN = "LOCAL_ORDER_STATUS_UNKNOWN"

# Attempt-level reason codes for durable fills/funding coverage continuity.
FULL_RECONCILE_COVERAGE_UNPROVABLE = "FULL_RECONCILE_COVERAGE_UNPROVABLE"
FULL_RECONCILE_COVERAGE_GAP = "FULL_RECONCILE_COVERAGE_GAP"


def canonical_reconcile_json(payload: Any) -> str:
    """Deterministic JSON for hashing: sorted keys, compact, no NaN/Inf."""
    return json.dumps(
        payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False,
        allow_nan=False,
    )


def reconcile_digest(payload: Any) -> str:
    return hashlib.sha256(canonical_reconcile_json(payload).encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class FundingEventRecord:
    """One authoritative exchange funding event.

    ``event_id`` is the exchange-provided ``hash`` of the ``userFunding``
    record. It is never synthesized: a record without a usable hash makes the
    whole funding component invalid.
    """

    event_id: str
    symbol: str
    amount_usdc: float
    effective_ts: datetime
    source: str = "HL_USER_FUNDING"
    attribution: FundingAttribution = FundingAttribution.ATTRIBUTED
    funding_rate: float | None = None
    position_szi: float | None = None
    n_samples: int | None = None

    def authoritative(self) -> dict[str, Any]:
        """The exchange-authoritative, immutable content of the event.

        Every field here comes straight from the ``userFunding`` record and can
        never change for a given ``event_id``. ``attribution`` is deliberately
        absent: it is *locally derived* from owned-order lineage, so the same
        unchanged exchange event is UNATTRIBUTED before a symbol has lineage
        and ATTRIBUTED after it. Hashing it would make the append-only identity
        digest a function of local state, and a later capture of an untouched
        event would be rejected as a conflicting redefinition of itself.
        """
        return {
            "event_id": self.event_id,
            "symbol": self.symbol,
            "amount_usdc": self.amount_usdc,
            "effective_ts": self.effective_ts.astimezone(UTC).isoformat(),
            "source": self.source,
            "funding_rate": self.funding_rate,
            "position_szi": self.position_szi,
            "n_samples": self.n_samples,
        }

    def canonical(self) -> dict[str, Any]:
        """Full snapshot view: authoritative content plus local attribution."""
        return {**self.authoritative(), "attribution": self.attribution.value}

    @property
    def digest(self) -> str:
        """Identity digest over exchange-authoritative content only."""
        return reconcile_digest(self.authoritative())


@dataclass(frozen=True)
class ComponentEvidence:
    """One fetched component with its own completeness/exactness verdict.

    ``rows`` are already normalized to canonical mappings by the adapter; the
    reconciler sorts and hashes them, so wire-order differences can never
    change the resulting checkpoint.
    """

    kind: ReconcileComponentKind
    source: str
    status: ReconcileComponentStatus
    observed_ts: datetime | None
    rows: tuple[Mapping[str, Any], ...] = ()
    exact: bool = False
    complete: bool = False
    reason_code: str = "UNSPECIFIED"
    cursor_start_ms: int | None = None
    cursor_end_ms: int | None = None
    page_count: int = 0
    call_count: int = 0

    @property
    def accepted(self) -> bool:
        return (
            self.status is ReconcileComponentStatus.COMPLETE
            and self.exact
            and self.complete
            and self.observed_ts is not None
        )

    def canonical_rows(self) -> list[dict[str, Any]]:
        """Rows in canonical order; identical evidence sorts identically."""
        normalized = [dict(row) for row in self.rows]
        return sorted(normalized, key=canonical_reconcile_json)

    @property
    def digest(self) -> str:
        """Digest of the *evidence content only* — never of timing metadata."""
        return reconcile_digest({
            "kind": self.kind.value,
            "rows": self.canonical_rows(),
            "cursor_start_ms": self.cursor_start_ms,
            "cursor_end_ms": self.cursor_end_ms,
        })


@dataclass(frozen=True)
class PortfolioEvidence:
    """Positions, balances and margin derived from one account observation.

    Deriving all three from a single read is deliberate: it removes intra-
    account skew entirely and keeps the bounded REST budget at one call.
    """

    positions: ComponentEvidence
    balances: ComponentEvidence
    margin: ComponentEvidence


@dataclass(frozen=True)
class ReconcileDiffRecord:
    kind: ReconcileDiffKind
    subject: str
    reason_code: str
    ownership: ReconcileOwnership
    blocking: bool
    local: Mapping[str, Any] | None = None
    exchange: Mapping[str, Any] | None = None

    def canonical(self) -> dict[str, Any]:
        return {
            "kind": self.kind.value,
            "subject": self.subject,
            "reason_code": self.reason_code,
            "ownership": self.ownership.value,
            "blocking": self.blocking,
            "local": dict(self.local) if self.local is not None else None,
            "exchange": dict(self.exchange) if self.exchange is not None else None,
        }


@dataclass(frozen=True)
class FullReconcileResult:
    """The complete, immutable outcome of exactly one full capture."""

    attempt_id: str
    run_id: str
    state: ReconcileAttemptState
    started_ts: datetime
    ended_ts: datetime
    duration_ms: int
    components: tuple[ComponentEvidence, ...] = ()
    diffs: tuple[ReconcileDiffRecord, ...] = ()
    funding_events: tuple[FundingEventRecord, ...] = ()
    canonical_hash: str = ""
    reason_code: str = "NONE"
    accepted: bool = False

    @property
    def blocking_diffs(self) -> tuple[ReconcileDiffRecord, ...]:
        return tuple(diff for diff in self.diffs if diff.blocking)


# ===========================================================================
# TS-P1-006 — authoritative risk-input snapshot
#
# The v6 risk decision may read exactly one immutable, versioned, fresh,
# complete, latest-accepted TS-P1-005 checkpoint view. The vocabulary below is
# the *shape* of that view plus its fail-closed reason codes; the bounded
# SQLite loader that produces it lives in store/db.py and the consumer is
# engine/risk.py. See docs/27_AUTHORITATIVE_RISK_SNAPSHOT_CONTRACT.md.
# ===========================================================================

SNAPSHOT_PAYLOAD_VERSION_V1 = "ts-p1-005-snapshot-v1"
"""Accepted TS-P1-005 payload marker: metadata/digests only, no rows.

Retained byte-for-byte as historical evidence and still reopenable, but it
carries no authoritative portfolio rows, so it can never authorize v6 risk.
"""

SNAPSHOT_PAYLOAD_VERSION_V2 = "ts-p1-006-snapshot-v2"
"""TS-P1-006 payload marker: v1 content plus canonical risk-bearing rows."""

SNAPSHOT_PAYLOAD_VERSION_V3 = "ts-p1-008-snapshot-v3"
"""TS-P1-008 payload marker: v2 content plus per-position valuation, leverage
and a directional liquidation price for the exposure/leverage/liquidation gates.

A v3 POSITIONS row is the v2 ``{symbol, size}`` schema extended with
``position_value`` (nonnegative gross mark notional), ``liquidation_px``
(directional, optional only for a zero-size row) and ``leverage`` (the reported
exchange leverage). The mark price is derived as ``position_value / abs(size)``
for any nonzero size, never read from entry or signal price. v3 is produced and
consumed only on an opt-in schema-v8 store; v4-v7 stores keep v2 byte-for-byte
and a v2 checkpoint can never authorize v8 risk. See
``docs/29_TSP1008_EXPOSURE_LEVERAGE_LIQUIDATION.md``.
"""

RISK_SNAPSHOT_COMPONENTS: tuple[ReconcileComponentKind, ...] = (
    ReconcileComponentKind.BALANCES,
    ReconcileComponentKind.MARGIN,
    ReconcileComponentKind.POSITIONS,
)
"""The components whose canonical rows a v2 payload must carry, in canonical
(value-sorted) order. All seven components must still be complete; only these
three are *read* by risk, so only these three rows are persisted."""

ACCOUNT_IDENTITY_ABS_TOL = 1e-6
"""Absolute float residue tolerated when re-checking the account identity
``available_margin == equity - margin_used``.

Deliberately far below any economically meaningful amount: this is a
float-representation guard, never a permissive band, and it is never applied
to quantities (those are compared in exact integer lots). Defined here so the
TS-P1-005 reconciler and the TS-P1-006 risk loader share one definition rather
than drifting apart; ``reconcile.ACCOUNT_IDENTITY_ABS_TOL`` re-exports it.
"""

# --- fail-closed reason codes (stable, secret-safe, observable) -------------

RISK_SNAPSHOT_SCHEMA_INACTIVE = "RISK_SNAPSHOT_SCHEMA_INACTIVE"
RISK_SNAPSHOT_TRANSACTION_ACTIVE = "RISK_SNAPSHOT_TRANSACTION_ACTIVE"
RISK_SNAPSHOT_NO_CHECKPOINT = "RISK_SNAPSHOT_NO_CHECKPOINT"
RISK_SNAPSHOT_POINTER_DANGLING = "RISK_SNAPSHOT_POINTER_DANGLING"
RISK_SNAPSHOT_POINTER_MOVED = "RISK_SNAPSHOT_POINTER_MOVED"
RISK_SNAPSHOT_ATTEMPT_NOT_ACCEPTED = "RISK_SNAPSHOT_ATTEMPT_NOT_ACCEPTED"
RISK_SNAPSHOT_SUPERSEDED = "RISK_SNAPSHOT_SUPERSEDED"
RISK_SNAPSHOT_COMPONENTS_INCOMPLETE = "RISK_SNAPSHOT_COMPONENTS_INCOMPLETE"
RISK_SNAPSHOT_PAYLOAD_MALFORMED = "RISK_SNAPSHOT_PAYLOAD_MALFORMED"
RISK_SNAPSHOT_LEGACY_PAYLOAD = "RISK_SNAPSHOT_LEGACY_PAYLOAD"
RISK_SNAPSHOT_PAYLOAD_VERSION_UNSUPPORTED = "RISK_SNAPSHOT_PAYLOAD_VERSION_UNSUPPORTED"
RISK_SNAPSHOT_ROWS_MISSING = "RISK_SNAPSHOT_ROWS_MISSING"
RISK_SNAPSHOT_ROW_DIGEST_MISMATCH = "RISK_SNAPSHOT_ROW_DIGEST_MISMATCH"
RISK_SNAPSHOT_HASH_MISMATCH = "RISK_SNAPSHOT_HASH_MISMATCH"
RISK_SNAPSHOT_POSITION_MALFORMED = "RISK_SNAPSHOT_POSITION_MALFORMED"
RISK_SNAPSHOT_POSITION_DUPLICATE = "RISK_SNAPSHOT_POSITION_DUPLICATE"
RISK_SNAPSHOT_ACCOUNT_MALFORMED = "RISK_SNAPSHOT_ACCOUNT_MALFORMED"
RISK_SNAPSHOT_ACCOUNT_NEGATIVE = "RISK_SNAPSHOT_ACCOUNT_NEGATIVE"
RISK_SNAPSHOT_ACCOUNT_INCONSISTENT = "RISK_SNAPSHOT_ACCOUNT_INCONSISTENT"
RISK_SNAPSHOT_COVERAGE_UNPROVABLE = "RISK_SNAPSHOT_COVERAGE_UNPROVABLE"
RISK_SNAPSHOT_FUTURE_CLOCK = "RISK_SNAPSHOT_FUTURE_CLOCK"
RISK_SNAPSHOT_STALE = "RISK_SNAPSHOT_STALE"
RISK_SNAPSHOT_READ_FAILED = "RISK_SNAPSHOT_READ_FAILED"
RISK_SNAPSHOT_REQUIRED = "RISK_SNAPSHOT_REQUIRED"

# TS-P1-007 durable daily-risk reason/control vocabulary.
RISK_DAY_SCHEMA_INACTIVE = "RISK_DAY_SCHEMA_INACTIVE"
RISK_DAY_BASELINE_MISSING = "RISK_DAY_BASELINE_MISSING"
RISK_DAY_DATE_MISMATCH = "RISK_DAY_DATE_MISMATCH"
RISK_DAY_POLICY_MISMATCH = "RISK_DAY_POLICY_MISMATCH"
RISK_DAY_CHECKPOINT_MISMATCH = "RISK_DAY_CHECKPOINT_MISMATCH"
RISK_DAY_STATE_MALFORMED = "RISK_DAY_STATE_MALFORMED"
RISK_DAY_UNEXPLAINED_CASHFLOW = "RISK_DAY_UNEXPLAINED_CASHFLOW"
DAILY_RISK_STATE_REQUIRED = "DAILY_RISK_STATE_REQUIRED"
DAILY_RISK_CHECKPOINT_MISMATCH = "DAILY_RISK_CHECKPOINT_MISMATCH"
DAILY_RISK_POLICY_MISMATCH = "DAILY_RISK_POLICY_MISMATCH"
RISK_CONTROL_DAILY_LOSS = "DAILY_LOSS"
RISK_CONTROL_MAX_DRAWDOWN = "MAX_DRAWDOWN"
RISK_CONTROL_EQUITY_STOP = "EQUITY_STOP"
RISK_LATCH_ACCOUNT_SCOPE = "ACCOUNT"
RISK_CONTROL_ORDER = (
    RISK_CONTROL_EQUITY_STOP,
    RISK_CONTROL_DAILY_LOSS,
    RISK_CONTROL_MAX_DRAWDOWN,
)

# TS-P1-008 exposure / leverage / liquidation reason vocabulary. Stable,
# secret-safe and observable: each records the metric, scope, threshold,
# checkpoint and policy version without ever embedding secrets. Every code is a
# fail-closed veto that DISARMs before submission; none authorize a later gate.
EXPOSURE_EVIDENCE_INVALID = "EXPOSURE_EVIDENCE_INVALID"
"""A v3 position row is missing, non-finite, negative, zero-for-nonzero-size,
incoherent with its derived mark, or carries a missing / wrong-side liquidation
price on a nonzero position (including at 1x). No coercion, clamp or fallback."""
LIQ_DISTANCE_BREACH = "LIQ_DISTANCE_BREACH"
"""Directional liquidation distance ``(mark-liq)/mark`` (long) or
``(liq-mark)/mark`` (short) is at or below the configured minimum."""
LEVERAGE_REPORTED_BREACH = "LEVERAGE_REPORTED_BREACH"
"""A reported exchange position leverage is at or above the effective-leverage cap."""
LEVERAGE_EFFECTIVE_BREACH = "LEVERAGE_EFFECTIVE_BREACH"
"""Portfolio gross notional / equity (including the projected order once) is at
or above the effective-leverage cap."""
SYMBOL_GROSS_BREACH = "SYMBOL_GROSS_BREACH"
"""Gross mark notional for one symbol (existing rows plus the projected order
once) is at or above the per-symbol cap; long/short are never netted."""
PORTFOLIO_GROSS_BREACH = "PORTFOLIO_GROSS_BREACH"
"""Gross mark notional across the whole wallet (every nonzero row, foreign
positions included, plus the projected order once) is at or above the portfolio
cap; offsetting positions are never netted."""
WALLET_UTIL_BREACH = "WALLET_UTIL_BREACH"
"""``margin_used / equity`` from the same checkpoint is at or above the wallet
margin utilization cap."""


class RiskPolicyInvalid(ValueError):
    """A durable risk policy is incomplete, non-finite, or unsafe."""


@dataclass(frozen=True, slots=True)
class DurableRiskPolicy:
    policy_id: str
    max_daily_loss_pct: float
    max_intraday_drawdown_pct: float
    equity_floor_usdc: float
    version: str

    @classmethod
    def create(
        cls,
        *,
        policy_id: str,
        max_daily_loss_pct: float,
        max_intraday_drawdown_pct: float,
        equity_floor_usdc: float,
    ) -> DurableRiskPolicy:
        if not isinstance(policy_id, str) or not policy_id.strip():
            raise RiskPolicyInvalid("policy_id is required")
        values = {
            "max_daily_loss_pct": max_daily_loss_pct,
            "max_intraday_drawdown_pct": max_intraday_drawdown_pct,
            "equity_floor_usdc": equity_floor_usdc,
        }
        for name, value in values.items():
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                raise RiskPolicyInvalid(f"{name} must be numeric")
            if not math.isfinite(float(value)):
                raise RiskPolicyInvalid(f"{name} must be finite")
        if not 0.0 < float(max_daily_loss_pct) <= 1.0:
            raise RiskPolicyInvalid("max_daily_loss_pct must be in (0, 1]")
        if not 0.0 < float(max_intraday_drawdown_pct) <= 1.0:
            raise RiskPolicyInvalid("max_intraday_drawdown_pct must be in (0, 1]")
        if float(equity_floor_usdc) < 0.0:
            raise RiskPolicyInvalid("equity_floor_usdc must be non-negative")
        payload = json.dumps(
            {
                "policy_id": policy_id.strip(),
                "max_daily_loss_pct": float(max_daily_loss_pct).hex(),
                "max_intraday_drawdown_pct": float(max_intraday_drawdown_pct).hex(),
                "equity_floor_usdc": float(equity_floor_usdc).hex(),
            },
            sort_keys=True,
            separators=(",", ":"),
        )
        version = f"rpol-v1:{hashlib.sha256(payload.encode('utf-8')).hexdigest()}"
        return cls(
            policy_id=policy_id.strip(),
            max_daily_loss_pct=float(max_daily_loss_pct),
            max_intraday_drawdown_pct=float(max_intraday_drawdown_pct),
            equity_floor_usdc=float(equity_floor_usdc),
            version=version,
        )


@dataclass(frozen=True, slots=True)
class ExposureRiskPolicy:
    """Immutable, versioned TS-P1-008 exposure / leverage / liquidation policy.

    Mirrors :class:`DurableRiskPolicy`: the five owner-approved thresholds are
    validated at construction and hashed into an immutable ``version``. A later
    owner-approved configuration change produces a new version; old checkpoints
    and decisions retain the exact version and values under which they were
    evaluated. No dashboard or runtime actor may change these implicitly.

    Percent thresholds are stored as fractions in ``(0, 1]``; the effective
    leverage multiple is ``>= 1.0``. Every gate is fail-closed at its exact
    boundary.
    """

    policy_id: str
    max_symbol_gross_pct: float
    max_portfolio_gross_pct: float
    max_wallet_margin_util_pct: float
    max_effective_leverage: float
    min_liquidation_distance_pct: float
    version: str

    @classmethod
    def create(
        cls,
        *,
        policy_id: str,
        max_symbol_gross_pct: float,
        max_portfolio_gross_pct: float,
        max_wallet_margin_util_pct: float,
        max_effective_leverage: float,
        min_liquidation_distance_pct: float,
    ) -> ExposureRiskPolicy:
        if not isinstance(policy_id, str) or not policy_id.strip():
            raise RiskPolicyInvalid("policy_id is required")
        pct_values = {
            "max_symbol_gross_pct": max_symbol_gross_pct,
            "max_portfolio_gross_pct": max_portfolio_gross_pct,
            "max_wallet_margin_util_pct": max_wallet_margin_util_pct,
            "min_liquidation_distance_pct": min_liquidation_distance_pct,
        }
        for name, value in pct_values.items():
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                raise RiskPolicyInvalid(f"{name} must be numeric")
            if not math.isfinite(float(value)):
                raise RiskPolicyInvalid(f"{name} must be finite")
        for name, value in pct_values.items():
            if not 0.0 < float(value) <= 1.0:
                raise RiskPolicyInvalid(f"{name} must be in (0, 1]")
        if isinstance(max_effective_leverage, bool) or not isinstance(
            max_effective_leverage, (int, float)
        ):
            raise RiskPolicyInvalid("max_effective_leverage must be numeric")
        if not math.isfinite(float(max_effective_leverage)):
            raise RiskPolicyInvalid("max_effective_leverage must be finite")
        if float(max_effective_leverage) < 1.0:
            raise RiskPolicyInvalid("max_effective_leverage must be >= 1.0")
        if float(max_portfolio_gross_pct) < float(max_symbol_gross_pct):
            # A portfolio cap below the per-symbol cap is internally contradictory
            # and would make the symbol gate unreachable; reject at policy build
            # time rather than silently at evaluation time.
            raise RiskPolicyInvalid(
                "max_portfolio_gross_pct must be >= max_symbol_gross_pct"
            )
        payload = json.dumps(
            {
                "policy_id": policy_id.strip(),
                "max_symbol_gross_pct": float(max_symbol_gross_pct).hex(),
                "max_portfolio_gross_pct": float(max_portfolio_gross_pct).hex(),
                "max_wallet_margin_util_pct": float(max_wallet_margin_util_pct).hex(),
                "max_effective_leverage": float(max_effective_leverage).hex(),
                "min_liquidation_distance_pct": float(min_liquidation_distance_pct).hex(),
            },
            sort_keys=True,
            separators=(",", ":"),
        )
        version = f"epol-v1:{hashlib.sha256(payload.encode('utf-8')).hexdigest()}"
        return cls(
            policy_id=policy_id.strip(),
            max_symbol_gross_pct=float(max_symbol_gross_pct),
            max_portfolio_gross_pct=float(max_portfolio_gross_pct),
            max_wallet_margin_util_pct=float(max_wallet_margin_util_pct),
            max_effective_leverage=float(max_effective_leverage),
            min_liquidation_distance_pct=float(min_liquidation_distance_pct),
            version=version,
        )


def risk_control_reset_token(control: str, scope_key: str) -> str:
    """Exact human acknowledgement token for one immutable latch scope."""
    return f"ACK TS-P1-007 {str(control)} {str(scope_key)}"


def _frozen_field(index: int, name: str, doc: str) -> property:
    def getter(self):
        return tuple.__getitem__(self, index)

    getter.__name__ = name
    return property(getter, doc=doc)


class _FrozenRecord(tuple):
    __slots__ = ()

    @property
    def __class__(self):
        return type(self)


class RiskControlLatch(_FrozenRecord):
    __slots__ = ()

    _FIELDS = (
        "latch_row_id", "control", "scope_key", "trading_date", "checkpoint_id",
        "generation", "observed_value", "threshold_value", "equity",
        "reason_code", "policy_version", "latched_ts",
    )

    def __new__(
        cls, *, latch_row_id: int, control: str, scope_key: str,
        trading_date: str, checkpoint_id: str, generation: int,
        observed_value: float, threshold_value: float, equity: float,
        reason_code: str, policy_version: str, latched_ts: datetime,
    ) -> RiskControlLatch:
        return tuple.__new__(cls, (
            int(latch_row_id), str(control), str(scope_key), str(trading_date),
            str(checkpoint_id), int(generation), float(observed_value),
            float(threshold_value), float(equity), str(reason_code),
            str(policy_version), latched_ts,
        ))

    latch_row_id = _frozen_field(0, "latch_row_id", "")
    control = _frozen_field(1, "control", "")
    scope_key = _frozen_field(2, "scope_key", "")
    trading_date = _frozen_field(3, "trading_date", "")
    checkpoint_id = _frozen_field(4, "checkpoint_id", "")
    generation = _frozen_field(5, "generation", "")
    observed_value = _frozen_field(6, "observed_value", "")
    threshold_value = _frozen_field(7, "threshold_value", "")
    equity = _frozen_field(8, "equity", "")
    reason_code = _frozen_field(9, "reason_code", "")
    policy_version = _frozen_field(10, "policy_version", "")
    latched_ts = _frozen_field(11, "latched_ts", "")


class DailyRiskState(_FrozenRecord):
    __slots__ = ()

    def __new__(
        cls, *, mode: str, network: str, trading_date: str,
        checkpoint_id: str, attempt_id: str, run_id: str,
        accepted_ts: datetime, loaded_ts: datetime,
        baseline_checkpoint_id: str, baseline_ts: datetime,
        baseline_equity: float, peak_equity: float, equity: float,
        realized_pnl_local: float, funding_attributed_usdc: float,
        policy_version: str,
        active_latches: tuple[RiskControlLatch, ...] = (),
    ) -> DailyRiskState:
        return tuple.__new__(cls, (
            str(mode), str(network), str(trading_date), str(checkpoint_id),
            str(attempt_id), str(run_id), accepted_ts, loaded_ts,
            str(baseline_checkpoint_id), baseline_ts, float(baseline_equity),
            float(peak_equity), float(equity), float(realized_pnl_local),
            float(funding_attributed_usdc), str(policy_version),
            tuple(active_latches),
        ))

    mode = _frozen_field(0, "mode", "")
    network = _frozen_field(1, "network", "")
    trading_date = _frozen_field(2, "trading_date", "")
    checkpoint_id = _frozen_field(3, "checkpoint_id", "")
    attempt_id = _frozen_field(4, "attempt_id", "")
    run_id = _frozen_field(5, "run_id", "")
    accepted_ts = _frozen_field(6, "accepted_ts", "")
    loaded_ts = _frozen_field(7, "loaded_ts", "")
    baseline_checkpoint_id = _frozen_field(8, "baseline_checkpoint_id", "")
    baseline_ts = _frozen_field(9, "baseline_ts", "")
    baseline_equity = _frozen_field(10, "baseline_equity", "")
    peak_equity = _frozen_field(11, "peak_equity", "")
    equity = _frozen_field(12, "equity", "")
    realized_pnl_local = _frozen_field(13, "realized_pnl_local", "")
    funding_attributed_usdc = _frozen_field(14, "funding_attributed_usdc", "")
    policy_version = _frozen_field(15, "policy_version", "")
    active_latches = _frozen_field(16, "active_latches", "")

    @property
    def daily_pnl(self) -> float:
        return self.equity - self.baseline_equity

    @property
    def daily_loss_pct(self) -> float:
        return max(0.0, -self.daily_pnl / self.baseline_equity)

    @property
    def drawdown_pct(self) -> float:
        return max(0.0, (self.peak_equity - self.equity) / self.peak_equity)

    @property
    def latched_controls(self) -> tuple[str, ...]:
        return tuple(latch.control for latch in self.active_latches)


class RiskSnapshotUnavailable(Exception):
    """No authoritative risk snapshot could be proven.

    Carries a stable ``reason_code`` only — never a payload, path or
    credential. Every raise site is a veto: the caller must DISARM in memory
    before any submission and must never fall back to a point broker read, a
    cached snapshot, or a caller-supplied dictionary.
    """

    def __init__(self, reason_code: str) -> None:
        self.reason_code = str(reason_code)[:96]
        super().__init__(self.reason_code)


def _frozen_field(index: int, name: str, doc: str) -> property:
    """A read-only view onto one slot of a tuple-backed frozen record."""

    def getter(self):
        return tuple.__getitem__(self, index)

    getter.__name__ = name
    return property(getter, doc=doc)


class _FrozenRecord(tuple):
    """Deeply immutable tuple-backed record, same threat model as
    :class:`_ImmutableMapping`.

    A ``@dataclass(frozen=True)`` is *not* enough here: it still gives every
    instance a writable ``__dict__`` (or, with ``slots=True``, writable slot
    descriptors), so ``object.__setattr__`` can rewrite equity, a position size
    or a hash after validation and before the gates read it. Storing the values
    as the tuple's own elements removes the holder entirely: there is no
    ``__dict__`` and no assignable slot of any kind, the elements are fixed at
    ``tuple.__new__`` time, and every field accessor is a read-only property.
    A caller walking ``gc.get_referents`` transitively from an instance reaches
    only tuples, ``str``, ``int``, ``float`` and ``datetime`` values — never a
    ``dict``, ``list`` or ``set`` it could mutate.

    The read-only ``__class__`` data descriptor shadows ``object``'s inherited
    class-assignment path, so the type cannot be swapped for a layout-compatible
    one. Direct calls to a base ``__class__`` descriptor and broader runtime
    compromise stay outside the owner-approved threat model, exactly as
    documented for ``_ImmutableMapping``.
    """

    __slots__ = ()

    @property
    def __class__(self):
        """Expose the actual type while rejecting instance-level replacement."""
        return type(self)


class RiskPositionRow(_FrozenRecord):
    """One canonical reconciled position from the accepted capture.

    A v2 row (schema v4-v7) carries only ``symbol`` and ``size``; the v3 fields
    (:attr:`position_value`, :attr:`liquidation_px`, :attr:`leverage`) are
    ``None``. A v3 row (schema v8) carries the per-position valuation, the
    directional liquidation price and the reported leverage from the same
    ``user_state`` epoch. The mark price is always *derived* from
    ``position_value / abs(size)`` for a nonzero size, never stored or read from
    an entry/signal price.
    """

    __slots__ = ()

    def __new__(
        cls,
        symbol: str,
        size: float,
        *,
        position_value: float | None = None,
        liquidation_px: float | None = None,
        leverage: float | None = None,
    ) -> RiskPositionRow:
        base = (str(symbol), float(size))
        if position_value is None and liquidation_px is None and leverage is None:
            return tuple.__new__(cls, base)
        return tuple.__new__(cls, base + (position_value, liquidation_px, leverage))

    symbol = _frozen_field(0, "symbol", "Exchange symbol, non-empty and unique.")
    size = _frozen_field(1, "size", "Signed net position size; finite.")
    @property
    def position_value(self) -> float | None:
        return self[2] if len(self) == 5 else None

    @property
    def liquidation_px(self) -> float | None:
        return self[3] if len(self) == 5 else None

    @property
    def leverage(self) -> float | None:
        return self[4] if len(self) == 5 else None

    @property
    def is_v3(self) -> bool:
        """True when this row carries TS-P1-008 per-position valuation evidence."""
        return self.position_value is not None

    @property
    def mark_price(self) -> float | None:
        """Derived mark price ``position_value / abs(size)`` for a nonzero v3 row."""
        if self.position_value is None or self.size == 0.0:
            return None
        return self.position_value / abs(self.size)

    def __repr__(self) -> str:
        if self.is_v3:
            return (
                f"RiskPositionRow(symbol={self.symbol!r}, size={self.size!r}, "
                f"position_value={self.position_value!r}, "
                f"liquidation_px={self.liquidation_px!r}, leverage={self.leverage!r})"
            )
        return f"RiskPositionRow(symbol={self.symbol!r}, size={self.size!r})"


class AuthoritativeRiskSnapshot(_FrozenRecord):
    """Exactly one immutable, versioned portfolio view for the v6 risk gate.

    Every field originates from the *same* accepted TS-P1-005 capture, resolved
    through the sole ``reconcile_checkpoint_latest`` pointer inside one bounded
    SQLite read transaction. Nothing here may be synthesized by a caller, mixed
    with a later broker read, or reused after it goes stale.
    """

    __slots__ = ()

    def __new__(
        cls,
        *,
        payload_version: str,
        checkpoint_id: str,
        attempt_id: str,
        run_id: str,
        canonical_hash: str,
        accepted_ts: datetime,
        loaded_ts: datetime,
        observed_from_ts: datetime,
        observed_to_ts: datetime,
        coverage_start_ms: int,
        coverage_end_ms: int,
        positions: tuple[RiskPositionRow, ...],
        equity: float,
        withdrawable: float,
        margin_used: float,
        available_margin: float,
        exposure_policy_version: str | None = None,
    ) -> AuthoritativeRiskSnapshot:
        return tuple.__new__(
            cls,
            (
                str(payload_version),
                str(checkpoint_id),
                str(attempt_id),
                str(run_id),
                str(canonical_hash),
                accepted_ts,
                loaded_ts,
                observed_from_ts,
                observed_to_ts,
                int(coverage_start_ms),
                int(coverage_end_ms),
                tuple(positions),
                float(equity),
                float(withdrawable),
                float(margin_used),
                float(available_margin),
                None if exposure_policy_version is None else str(exposure_policy_version),
            ),
        )

    payload_version = _frozen_field(0, "payload_version", "Checkpoint payload format marker.")
    checkpoint_id = _frozen_field(1, "checkpoint_id", "Immutable accepted checkpoint identity.")
    attempt_id = _frozen_field(2, "attempt_id", "Attempt that produced the checkpoint.")
    run_id = _frozen_field(3, "run_id", "Run that owned the capture.")
    canonical_hash = _frozen_field(4, "canonical_hash", "Recomputed and verified evidence hash.")
    accepted_ts = _frozen_field(5, "accepted_ts", "UTC acceptance time of the checkpoint.")
    loaded_ts = _frozen_field(6, "loaded_ts", "UTC time this view was resolved.")
    observed_from_ts = _frozen_field(7, "observed_from_ts", "Earliest component observation.")
    observed_to_ts = _frozen_field(8, "observed_to_ts", "Latest component observation.")
    coverage_start_ms = _frozen_field(9, "coverage_start_ms", "Proven fills/funding lower bound.")
    coverage_end_ms = _frozen_field(10, "coverage_end_ms", "Proven fills/funding upper bound.")
    positions = _frozen_field(11, "positions", "Canonical reconciled positions.")
    equity = _frozen_field(12, "equity", "Account equity at the observation.")
    withdrawable = _frozen_field(13, "withdrawable", "Withdrawable balance at the observation.")
    margin_used = _frozen_field(14, "margin_used", "Margin used at the observation.")
    available_margin = _frozen_field(15, "available_margin", "Available margin at the observation.")
    exposure_policy_version = _frozen_field(
        16, "exposure_policy_version", "Policy hash bound into a v3 checkpoint."
    )

    @property
    def age_s(self) -> float:
        """Seconds between acceptance and the load that produced this view."""
        return (
            self.loaded_ts.astimezone(UTC) - self.accepted_ts.astimezone(UTC)
        ).total_seconds()

    @property
    def open_positions(self) -> tuple[RiskPositionRow, ...]:
        """Every reconciled row with nonzero exposure, in canonical order."""
        return tuple(row for row in self.positions if row.size != 0.0)

    @property
    def has_open_position(self) -> bool:
        return bool(self.open_positions)

    def account(self) -> AccountSnapshot:
        """The account view the existing gates consume, from this epoch only."""
        return AccountSnapshot(
            equity=self.equity,
            available_margin=self.available_margin,
            withdrawable=self.withdrawable,
        )

    def __repr__(self) -> str:
        return (
            f"AuthoritativeRiskSnapshot(checkpoint_id={self.checkpoint_id!r}, "
            f"attempt_id={self.attempt_id!r}, equity={self.equity!r}, "
            f"positions={len(self.positions)})"
        )
