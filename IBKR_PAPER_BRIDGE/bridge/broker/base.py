"""Broker protocol (abstract interface)."""

from __future__ import annotations

from collections.abc import Callable, Iterator, Mapping
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Protocol

from bridge.engine.types import AccountSnapshot, Bar, BrokerEvent, BrokerOrder, OrderPlan, Position


class SubmissionDisposition(str, Enum):
    """Typed result of one bracket write attempt."""

    VERIFIED_SUCCESS = "VERIFIED_SUCCESS"
    DEFINITIVE_REJECTION = "DEFINITIVE_REJECTION"
    OUTCOME_UNKNOWN = "OUTCOME_UNKNOWN"


@dataclass(frozen=True)
class SubmissionOutcome(Mapping[str, dict[str, Any]]):
    """A typed broker result that remains mapping-compatible for callers."""

    disposition: SubmissionDisposition
    orders: Mapping[str, dict[str, Any]] = field(default_factory=dict)
    reason_code: str = "NONE"

    def __getitem__(self, key: str) -> dict[str, Any]:
        return self.orders[key]

    def __iter__(self) -> Iterator[str]:
        return iter(self.orders)

    def __len__(self) -> int:
        return len(self.orders)


class BrokerSubmissionError(RuntimeError):
    """Secret-safe typed adapter failure."""

    disposition: SubmissionDisposition
    write_may_have_started: bool

    def __init__(
        self,
        reason_code: str,
        *,
        disposition: SubmissionDisposition,
        write_may_have_started: bool,
    ) -> None:
        self.reason_code = reason_code
        self.disposition = disposition
        self.write_may_have_started = write_may_have_started
        super().__init__(reason_code)


class BrokerPreSendFailure(BrokerSubmissionError):
    """The adapter proved that no exchange write call began."""

    def __init__(self, reason_code: str = "PRE_SEND_FAILURE") -> None:
        super().__init__(
            reason_code,
            disposition=SubmissionDisposition.DEFINITIVE_REJECTION,
            write_may_have_started=False,
        )


class BrokerOutcomeUnknown(BrokerSubmissionError):
    """An exchange write may have begun and the outcome is not verified."""

    def __init__(self, reason_code: str = "OUTCOME_UNKNOWN") -> None:
        super().__init__(
            reason_code,
            disposition=SubmissionDisposition.OUTCOME_UNKNOWN,
            write_may_have_started=True,
        )


class SubmissionRejectedError(RuntimeError):
    """Known non-success used by the engine's ordinary rejection counter."""

    def __init__(self, reason_code: str, request_id: str, attempt_id: str) -> None:
        self.reason_code = reason_code
        self.request_id = request_id
        self.attempt_id = attempt_id
        super().__init__(reason_code)


class UnknownSubmissionError(RuntimeError):
    """Durable quarantine signal; contains identifiers and safe codes only."""

    def __init__(self, reason_code: str, request_id: str, attempt_id: str) -> None:
        self.reason_code = reason_code
        self.request_id = request_id
        self.attempt_id = attempt_id
        super().__init__(reason_code)


class EvidenceStatus(str, Enum):
    FOUND = "FOUND"
    NOT_FOUND = "NOT_FOUND"
    QUERY_FAILED = "QUERY_FAILED"
    UNAVAILABLE = "UNAVAILABLE"
    TRUNCATED = "TRUNCATED"
    STALE = "STALE"
    CONFLICTING = "CONFLICTING"


@dataclass(frozen=True)
class RecoveryQueryEvidence:
    status: EvidenceStatus
    found_cloids: tuple[str, ...] = ()
    reason_code: str = "NONE"


@dataclass(frozen=True)
class SubmissionRecoveryRequest:
    attempt_id: str
    request_id: str
    planned_cloids: Mapping[str, str]
    symbol: str
    window_start: str


@dataclass(frozen=True)
class SubmissionRecoveryEvidence:
    """One adapter observation cycle; timestamps are added by trusted local code."""

    request_id: str
    planned_cloids: Mapping[str, str]
    direct_lookup: Mapping[str, RecoveryQueryEvidence]
    open_orders: RecoveryQueryEvidence
    historical_orders: RecoveryQueryEvidence
    fills: RecoveryQueryEvidence
    position: RecoveryQueryEvidence


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

    def planned_cloids(self, plan: OrderPlan) -> dict[str, str]:
        ...

    async def place_bracket(self, plan: OrderPlan) -> SubmissionOutcome:
        ...

    async def submission_recovery_evidence(
        self, request: SubmissionRecoveryRequest
    ) -> SubmissionRecoveryEvidence:
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
