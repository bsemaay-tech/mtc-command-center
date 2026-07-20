"""Core pydantic models (Bar, Signal, OrderPlan, Position, etc.)."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from types import MappingProxyType
from typing import Literal, Mapping

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


# No module-level name binds this dict: once MappingProxyType wraps it below,
# the literal is unreachable to callers (fixes audit F1 — a named seed is a
# mutable backing surface even when the proxy itself blocks writes).
ORDER_STATE_TRANSITIONS: Mapping[OrderState, frozenset[OrderState]] = MappingProxyType({
    OrderState.PENDING_NEW: frozenset({OrderState.PENDING_NEW, OrderState.SUBMITTING}),
    OrderState.SUBMITTING: frozenset(
        {
            OrderState.SUBMITTING,
            OrderState.SUBMITTED,
            OrderState.REJECTED,
            OrderState.UNKNOWN_SUBMISSION,
        }
    ),
    OrderState.SUBMITTED: frozenset(
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
    OrderState.OPEN: frozenset(
        {
            OrderState.OPEN,
            OrderState.PARTIALLY_FILLED,
            OrderState.FILLED,
            OrderState.PENDING_CANCEL,
            OrderState.CANCELED,
            OrderState.EXPIRED,
        }
    ),
    OrderState.PARTIALLY_FILLED: frozenset(
        {
            OrderState.PARTIALLY_FILLED,
            OrderState.FILLED,
            OrderState.PENDING_CANCEL,
            OrderState.CANCELED,
            OrderState.EXPIRED,
        }
    ),
    OrderState.PENDING_CANCEL: frozenset(
        {
            OrderState.PENDING_CANCEL,
            OrderState.CANCELED,
            OrderState.FILLED,
            OrderState.PARTIALLY_FILLED,
            OrderState.OPEN,
            OrderState.EXPIRED,
        }
    ),
    OrderState.UNKNOWN_SUBMISSION: frozenset(
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
    OrderState.FILLED: frozenset({OrderState.FILLED}),
    OrderState.CANCELED: frozenset({OrderState.CANCELED}),
    OrderState.REJECTED: frozenset({OrderState.REJECTED}),
    OrderState.EXPIRED: frozenset({OrderState.EXPIRED}),
})


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
    The message never interpolates `repr(raw)`/`str(raw)` — only the type
    name — so a hostile `raw.__repr__` can neither leak arbitrary text into
    the message nor escape this exception with one of its own.
    """

    def __init__(self, raw: object, reason_code: str) -> None:
        self.raw = raw
        self.reason_code = reason_code
        super().__init__(
            f"{reason_code}: unrecognized raw order status of type {type(raw).__name__}"
        )


# No module-level name binds this dict either, for the same reason as
# ORDER_STATE_TRANSITIONS above (audit F1).
RAW_ORDER_STATUS_ALIASES: Mapping[str, OrderState] = MappingProxyType({
    "OPEN": OrderState.OPEN,
    "SUBMITTED": OrderState.SUBMITTED,
    "PENDING": OrderState.SUBMITTED,
    "FILLED": OrderState.FILLED,
    "CANCELLED_BY_ENGINE": OrderState.CANCELED,
})


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
