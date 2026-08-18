"""Broker protocol (abstract interface)."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any, Literal, Protocol

from bridge.engine.types import AccountSnapshot, Bar, BrokerEvent, BrokerOrder, OrderPlan, Position


# ---------------------------------------------------------------------------
# TS-P1-003 typed broker-boundary outcomes
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class SubmissionResult:
    """Structured outcome of a broker submission call.

    Exactly one of these verdicts is set; the other fields are empty/None.

    - verified_success: every planned role/cloid covered with success-compatible
      statuses. Contains role->order-dict mapping.
    - definitive_rejection: complete response proves every planned order rejected.
      Contains role->error-reason mapping.
    - pre_send_failure: adapter proved no exchange write call began.
    - outcome_unknown: anything else (timeout, transport loss, partial acceptance,
      malformed response, verification mismatch, exception after send may have
      started).
    """
    verdict: Literal[
        "VERIFIED_SUCCESS", "DEFINITIVE_REJECTION",
        "PRE_SEND_FAILURE", "OUTCOME_UNKNOWN",
    ]
    verified_orders: dict[str, dict[str, Any]] = field(default_factory=dict)
    rejection_reasons: dict[str, str] = field(default_factory=dict)
    error_type: str | None = None
    safe_detail: str | None = None

    def __getitem__(self, key: str) -> dict[str, Any]:
        """Backward-compatible dict-like access for legacy callers."""
        if key in self.verified_orders:
            return self.verified_orders[key]
        raise KeyError(key)

    def __contains__(self, key: str) -> bool:
        return key in self.verified_orders

    def keys(self):
        return self.verified_orders.keys()

    def values(self):
        return self.verified_orders.values()

    def items(self):
        return self.verified_orders.items()

    def __iter__(self):
        return iter(self.verified_orders)

    def __len__(self) -> int:
        return len(self.verified_orders)


@dataclass(frozen=True)
class RecoveryEvidence:
    """Normalized, secret-safe broker evidence for one cloid during recovery.

    Per-source verdicts:
    - FOUND: authoritative match (open, historical, fill, etc.)
    - NOT_FOUND: authoritative absence for this source
    - QUERY_FAILED: API call raised or returned invalid
    - INCOMPLETE: response truncated or missing coverage
    - STALE: response window doesn't cover attempt window
    - TRUNCATED: known partial data
    """
    planned_cloid: str
    source: str  # DIRECT_LOOKUP, OPEN_ORDERS, HISTORICAL_ORDERS, FILLS, POSITION
    verdict: str  # FOUND, NOT_FOUND, QUERY_FAILED, INCOMPLETE, STALE, TRUNCATED
    completeness: str  # COMPLETE, INCOMPLETE, COVERAGE_MISSING
    safe_payload: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class RecoveryCycle:
    """One complete evidence collection cycle for an attempt."""
    cycle_id: str
    attempt_id: int
    evidence: list[RecoveryEvidence] = field(default_factory=list)
    cycle_start_ts: str = ""
    cycle_end_ts: str = ""


class Broker(Protocol):
    """Abstract broker interface for exchange operations."""

    async def connect(self) -> None:
        ...

    async def account(self) -> AccountSnapshot:
        ...

    async def positions(self) -> list[Position]:
        ...

    async def open_orders(self) -> list[BrokerOrder]:
        ...

    async def historical_bars(self, coin: str, tf: str, lookback: int) -> list[Bar]:
        ...

    def subscribe_bars(self, coin: str, tf: str, on_bar_closed: Callable[[Bar], None]) -> None:
        ...

    def subscribe_user_events(self, on_event: Callable[[BrokerEvent], None]) -> None:
        ...

    async def place_bracket(self, plan: OrderPlan) -> SubmissionResult:
        ...

    async def modify_stop(self, cloid: str, new_stop: float) -> None:
        ...

    async def cancel(self, cloid: str) -> None:
        ...

    async def cancel_all(self) -> None:
        ...

    async def flatten(self, coin: str) -> None:
        ...

    async def reprotect_position(
        self,
        position: Position,
        stop_loss: float,
        take_profit: float | None,
        decision_uid: str,
    ) -> dict[str, Any] | None:
        ...

    # --- TS-P1-003 recovery evidence ---

    async def query_order_by_cloid(self, cloid: str) -> dict[str, Any] | None:
        """Direct lookup of a single order by cloid.  Returns None on NOT_FOUND;
        raises on query failure.  Must not swallow exceptions into None."""
        ...

    async def historical_orders(self, coin: str, since_ts: str) -> list[dict[str, Any]]:
        """All order history (including cancelled/rejected/expired) since timestamp.
        Must not swallow exceptions into []; raise on query failure."""
        ...

    async def user_fills(self, coin: str, since_ts: str) -> list[dict[str, Any]]:
        """All fills since timestamp. Must not swallow exceptions into [];
        raise on query failure."""
        ...

    def get_planned_cloids(self, plan: OrderPlan) -> dict[str, str]:
        """Return the deterministic role→cloid map for a plan without
        broker I/O.  Used by OrderManager before the broker call."""
        ...
