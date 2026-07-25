"""Core pydantic models (Bar, Signal, OrderPlan, Position, etc.)."""

from __future__ import annotations

from collections.abc import Mapping
from datetime import datetime
from enum import Enum
from typing import Literal

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

    Pure model only: not wired into persistence, broker adapters, or the
    engine in this task. See docs/22_ORDER_STATE_CONTRACT.md for the full
    glossary, raw-status mapping, and transition table.
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
    ("FILLED", OrderState.FILLED),
    ("CANCELLED_BY_ENGINE", OrderState.CANCELED),
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
