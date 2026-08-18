"""Broker protocol (abstract interface)."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Protocol

from bridge.engine.types import AccountSnapshot, Bar, BrokerEvent, BrokerOrder, OrderPlan, Position


# ---------------------------------------------------------------------------
# TS-P1-003 submission outcome vocabulary (exchange-neutral)
# ---------------------------------------------------------------------------

class SubmissionOutcome(str, Enum):
    """Structured adapter outcome after a placement attempt."""
    PRE_SEND_FAILURE = "PRE_SEND_FAILURE"        # error before send confirmed
    DEFINITIVE_REJECTION = "DEFINITIVE_REJECTION"  # exchange explicitly rejected
    OUTCOME_UNKNOWN = "OUTCOME_UNKNOWN"            # ambiguous (timeout/partial/…)
    VERIFIED_SUCCESS = "VERIFIED_SUCCESS"          # normal confirmed success


@dataclass
class SubmissionEvidence:
    """Single evidence item collected during recovery."""
    source: str            # "open_orders", "historical_orders", "fills", "positions"
    cloid: str
    found: bool
    detail: str            # sanitized — never raw exchange text


@dataclass
class RecoveryAttempt:
    """One complete evidence-collection cycle for a set of planned cloids."""
    ts: str  # ISO timestamp
    verdict: str  # "PRESENT", "ABSENT_CANDIDATE", "INCOMPLETE", "CONFLICTING"
    evidences: list[SubmissionEvidence] = field(default_factory=list)
    notes: str = ""


# ---------------------------------------------------------------------------
# Broker protocol
# ---------------------------------------------------------------------------

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

    async def place_bracket(self, plan: OrderPlan) -> dict[str, Any]:
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

    # ------------------------------------------------------------------
    # TS-P1-003 read-only recovery evidence (never mutates orders)
    # ------------------------------------------------------------------

    async def query_order_by_cloid(self, cloid: str) -> dict[str, Any] | None:
        """Look up a single order by cloid (read-only). Returns None if not found."""
        ...

    async def historical_orders(
        self, coin: str, lookback_hours: float
    ) -> list[dict[str, Any]]:
        """Read-only: recent order history (filled, canceled, expired)."""
        ...

    async def user_fills(
        self, coin: str, lookback_hours: float
    ) -> list[dict[str, Any]]:
        """Read-only: recent fill history."""
        ...
