"""Broker protocol (abstract interface)."""

from __future__ import annotations

from collections.abc import Callable, Iterator, Mapping
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Protocol

from bridge.engine.types import (
    AccountSnapshot,
    Bar,
    BrokerEvent,
    BrokerOrder,
    CancelResult,
    ComponentEvidence,
    FlattenResult,
    KillEvidenceCapture,
    KillEvidenceEpoch,
    LotUnit,
    OrderPlan,
    OrderQueryResult,
    PlaceResult,
    PortfolioEvidence,
    Position,
    SymbolSnapshot,
)


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

    async def place_bracket(
        self, plan: OrderPlan, *, pre_send_guard: Callable[[], bool] | None = None
    ) -> SubmissionOutcome:
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


# ---------------------------------------------------------------------------
# TS-P1-004 bounded partial-recovery surface
#
# Deliberately a *separate* protocol. `Broker` keeps its accepted
# `cancel` / `flatten` / `reprotect_position` shape so unrelated fakes outside
# the allow-list are untouched; an adapter opts in by implementing the methods
# below. `OrderManager` feature-detects and treats a missing surface as
# "recovery unavailable" — abort with zero mutation, never a silent success.
# ---------------------------------------------------------------------------


class PartialRecoveryUnavailable(RuntimeError):
    """The adapter cannot serve the bounded partial-recovery contract."""

    def __init__(self, reason_code: str = "PARTIAL_RECOVERY_API_UNAVAILABLE") -> None:
        self.reason_code = reason_code
        super().__init__(reason_code)


class PartialRecoveryBroker(Protocol):
    """Typed, bounded, evidence-carrying surface used by partial recovery.

    Every method returns a typed result whose outcome is conservative:
    transport failures, unparseable bodies and missing fields map to
    ``ActionOutcome.UNKNOWN`` / ``known=False`` / ``exact=False``, never to a
    claimed success.
    """

    def lot_unit(self, symbol: str) -> LotUnit | None:
        """Exchange size quantum, or ``None`` when unknown (fail-closed)."""
        ...

    async def symbol_snapshot(self, symbol: str) -> SymbolSnapshot:
        """Bounded position + open-order evidence for exactly one symbol."""
        ...

    async def query_order(self, cloid: str, symbol: str) -> OrderQueryResult:
        """Direct single-order lookup used to resolve UNKNOWN outcomes."""
        ...

    async def cancel_order_by_cloid(self, cloid: str, symbol: str) -> CancelResult:
        """Cancel one owned order by its stable cloid."""
        ...

    async def place_protective_stop(
        self,
        *,
        symbol: str,
        cloid: str,
        exit_side: str,
        size: float,
        trigger_px: float,
    ) -> PlaceResult:
        """Place one exact-size, reduce-only stop for the owned position."""
        ...

    async def flatten_reduce_only(
        self, *, symbol: str, cloid: str, size: float, exit_side: str
    ) -> FlattenResult:
        """Reduce-only market close of exactly ``size`` on ``symbol``."""
        ...


# TS-P1-009 deliberately reuses the proven typed primitives while defining a
# separate capability boundary from the broad legacy cancel_all/flatten API.
class KillRecoveryBroker(Protocol):
    def lot_unit(self, symbol: str) -> LotUnit | None:
        ...

    async def symbol_snapshot(self, symbol: str) -> SymbolSnapshot:
        ...

    async def capture_kill_evidence(
        self,
        *,
        epoch: KillEvidenceEpoch,
        symbol: str,
        start_ms: int,
        end_ms: int,
    ) -> KillEvidenceCapture:
        """Fresh authoritative positions, orders and fills before mutation."""
        ...

    async def query_order(self, cloid: str, symbol: str) -> OrderQueryResult:
        ...

    async def kill_cancel_order_by_cloid(
        self,
        cloid: str,
        symbol: str,
        *,
        epoch: KillEvidenceEpoch,
        epoch_guard: Callable[[KillEvidenceEpoch], None],
        worker_epoch_guard: Callable[[KillEvidenceEpoch], None],
    ) -> CancelResult:
        """KILL-only cancel fenced inside the adapter's final write boundary."""
        ...

    async def kill_flatten_reduce_only(
        self,
        *,
        symbol: str,
        cloid: str,
        size: float,
        exit_side: str,
        epoch: KillEvidenceEpoch,
        epoch_guard: Callable[[KillEvidenceEpoch], None],
        worker_epoch_guard: Callable[[KillEvidenceEpoch], None],
    ) -> FlattenResult:
        """KILL-only flatten fenced inside the adapter's final write boundary."""
        ...


# ---------------------------------------------------------------------------
# TS-P1-005 bounded read-only full-reconciliation surface
#
# A *separate* protocol again, following the `PartialRecoveryBroker` precedent
# above: `Broker` keeps its accepted shape, and an adapter opts in by
# implementing the read-only methods below. Nothing here may mutate exchange
# state. `FullReconciler` feature-detects the surface and treats a missing one
# as "reconciliation unavailable" — a non-accepting attempt, never a success.
# ---------------------------------------------------------------------------


class FullReconciliationUnavailable(RuntimeError):
    """The adapter cannot serve the bounded full-reconciliation contract."""

    def __init__(self, reason_code: str = "FULL_RECONCILE_API_UNAVAILABLE") -> None:
        self.reason_code = reason_code
        super().__init__(reason_code)


class FullReconciliationBroker(Protocol):
    """Read-only authoritative evidence for one full portfolio capture.

    Every method returns typed evidence whose verdict is conservative:
    transport failures, unparseable bodies, truncated pages and unprovable
    pagination completeness map to a non-``COMPLETE`` status, never to an
    empty-but-accepted component.
    """

    def lot_unit(self, symbol: str) -> LotUnit | None:
        """Exchange size quantum, or ``None`` when unknown (fail-closed)."""
        ...

    async def portfolio_evidence(self) -> PortfolioEvidence:
        """Positions, balances and margin from one account observation."""
        ...

    async def open_orders_evidence(self) -> ComponentEvidence:
        """Authoritative live open-order rows for the whole account."""
        ...

    async def fills_evidence(
        self, *, start_ms: int, end_ms: int
    ) -> ComponentEvidence:
        """Time-paginated fills; incomplete history windows fail closed."""
        ...

    async def funding_evidence(
        self, *, start_ms: int, end_ms: int
    ) -> ComponentEvidence:
        """Time-paginated funding ledger keyed by the exchange event hash."""
        ...
