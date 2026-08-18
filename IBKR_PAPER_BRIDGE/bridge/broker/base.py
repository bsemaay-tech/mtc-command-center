"""Broker protocol (abstract interface)."""

from __future__ import annotations

import enum
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any, Protocol

from bridge.engine.types import AccountSnapshot, Bar, BrokerEvent, BrokerOrder, OrderPlan, Position


# ---------------------------------------------------------------------------
# TS-P1-003 structured broker outcomes
# ---------------------------------------------------------------------------

class SubmissionOutcome(enum.Enum):
    """Structured result of a bracket-submission attempt."""
    PRE_SEND_FAILURE = "PRE_SEND_FAILURE"        # adapter proved no exchange write started
    DEFINITIVE_REJECTION = "DEFINITIVE_REJECTION" # complete response proves every planned order rejected
    VERIFIED_SUCCESS = "VERIFIED_SUCCESS"         # exact complete planned-role/cloid coverage confirmed
    OUTCOME_UNKNOWN = "OUTCOME_UNKNOWN"           # timeout, transport loss, partial, verification failure


class EvidenceVerdict(enum.Enum):
    """Request-specific recovery evidence verdict."""
    PRESENT = "PRESENT"                # any planned cloid authoritatively found
    ABSENT_CANDIDATE = "ABSENT_CANDIDATE"  # every mandatory source complete, all cloids absent
    INCOMPLETE = "INCOMPLETE"          # any required query failed/truncated/stale/incomplete
    CONFLICTING = "CONFLICTING"        # sources disagree, partial bracket, unattributable evidence


@dataclass
class RecoveryEvidence:
    """Typed, normalized, secret-safe broker evidence for exact planned cloids."""
    verdict: EvidenceVerdict
    planned_cloids: dict[str, str]  # role -> cloid mapping that was planned
    found_cloids: list[str] = field(default_factory=list)  # cloids authoritatively located
    sources_checked: list[str] = field(default_factory=list)  # e.g. "direct_lookup", "open_orders", "historical", "fills"
    sources_complete: list[str] = field(default_factory=list)  # subset that completed successfully
    reason_codes: list[str] = field(default_factory=list)  # safe reason codes, no raw messages
    ts_start: str | None = None
    ts_end: str | None = None
    attempt_window_covered: bool = False  # True if evidence spans the full attempt window


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

    # ------------------------------------------------------------------
    # TS-P1-003 broker-boundary methods
    # ------------------------------------------------------------------

    def compute_plan_cloids(self, decision_uid: str, roles: tuple[str, ...] = ("entry", "sl", "tp")) -> dict[str, str]:
        """Pure broker-boundary method returning the exact planned role→cloid map.

        Used by both OrderManager (submission attempt) and the adapter (verification).
        Must be deterministic and side-effect-free.
        """
        ...

    async def recovery_evidence(
        self,
        planned_cloids: dict[str, str],
        attempt_start_ts: str | None,
    ) -> RecoveryEvidence:
        """Return typed, normalized, secret-safe evidence for exact planned cloids.

        Must distinguish PRESENT / ABSENT_CANDIDATE / INCOMPLETE / CONFLICTING.
        Must never collapse query failure/unavailability into empty-success.
        """
        ...

    async def query_order_by_cloid(self, cloid: str, coin: str) -> dict[str, Any] | None:
        """Request-specific direct lookup of a single cloid. Returns None if not found."""
        ...

    async def historical_orders(self, coin: str, since_ts: str | None) -> list[dict[str, Any]]:
        """Historical order snapshot covering the attempt window."""
        ...

    async def user_fills_by_time(self, coin: str, since_ts: str | None) -> list[dict[str, Any]]:
        """Fill history covering the attempt window."""
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
