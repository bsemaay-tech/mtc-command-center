from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import struct
from typing import Optional, TypeAlias

from mtc_v2.core.indicators import IndicatorSnapshot
from mtc_v2.core.instrument import InstrumentMetadata


LifecycleId: TypeAlias = int
FillId: TypeAlias = str
CashEventId: TypeAlias = str

REFUSED_INVALID_CASH_LEDGER_JOIN = "REFUSED_INVALID_CASH_LEDGER_JOIN"


class EconomicTransitionError(ValueError):
    """Raised when an atomic transition violates its immutable ledger contract."""

    refusal_code = REFUSED_INVALID_CASH_LEDGER_JOIN


class CashEventKind(str, Enum):
    GROSS_REALIZATION = "GROSS_REALIZATION"
    FEE = "FEE"
    FUNDING = "FUNDING"


@dataclass(slots=True, frozen=True)
class DecisionEvent:
    sequence: int
    event_timestamp: datetime
    decision: str
    lifecycle_id: LifecycleId | None = None
    refusal_code: str | None = None
    details: tuple[tuple[str, str], ...] = ()


@dataclass(slots=True, frozen=True)
class FillDecision:
    sequence: int
    event_timestamp: datetime
    lifecycle_id: LifecycleId
    fill_id: FillId
    event_class: str
    side: str
    reference_price: float
    slippage_model_id: str
    slippage_bps: float
    slippage_impact: float
    slippage_application_count: int
    final_fill_price: float
    quantity: float
    liquidity_role: str
    exit_id: str | None = None
    target_fraction: float | None = None
    reference_quantity: float | None = None
    price_tick_alignment: str | None = None
    fill_trigger: str | None = None


# The transition owns one fill fact; result serialization projects it as a fill event.
FillEvent = FillDecision


@dataclass(slots=True, frozen=True)
class CashEvent:
    sequence: int
    cash_event_id: CashEventId
    event_timestamp: datetime
    lifecycle_id: LifecycleId
    kind: CashEventKind
    signed_delta: float
    settlement_currency: str
    fill_id: FillId | None = None
    funding_event_id: str | None = None


@dataclass(slots=True, frozen=True)
class FeeEvent:
    sequence: int
    event_timestamp: datetime
    lifecycle_id: LifecycleId
    fill_id: FillId
    event_class: str
    liquidity_role: str
    schedule_id: str
    schedule_digest: str
    rate: float
    fixed_component: float
    fee_notional: float
    fee_amount: float
    fee_cash_delta: float
    settlement_currency: str
    cash_event_id: CashEventId


@dataclass(slots=True, frozen=True)
class FundingEvent:
    sequence: int
    funding_event_id: str
    event_timestamp: datetime
    lifecycle_id: LifecycleId
    position_side: str
    open_qty: float
    contract_multiplier: float
    mark_price: float
    raw_rate: float
    positive_rate_payer: str
    long_cashflow_rate: float
    notional: float
    funding_cash_delta: float
    cumulative_funding: float
    schedule_id: str
    schedule_digest: str
    source_event_digest: str
    cash_event_id: CashEventId


@dataclass(slots=True, frozen=True)
class PositionFacts:
    lifecycle_id: LifecycleId | None
    side: str | None
    quantity: float
    entry_fill_price: float | None = None
    active_stop_price: float | None = None


def _same_binary64(left: float, right: float) -> bool:
    return struct.pack(">d", float(left)) == struct.pack(">d", float(right))


def _require_contiguous_sequences(label: str, rows: tuple[object, ...]) -> None:
    for expected, row in enumerate(rows):
        if getattr(row, "sequence", None) != expected:
            raise EconomicTransitionError(
                f"{REFUSED_INVALID_CASH_LEDGER_JOIN}: {label} sequence must be contiguous"
            )


@dataclass(slots=True, frozen=True)
class EconomicTransition:
    """One immutable economic transition applied exactly once by its caller.

    ``cash_events`` is the sole equity-mutation ledger. Fee and funding rows are
    equality-checked typed projections joined one-to-one by ``cash_event_id``.
    """

    semantics_id: str
    instrument_record_id: str
    instrument_record_digest: str
    funding_schedule_id: str
    funding_schedule_digest: str
    next_position_facts: PositionFacts
    cost_schedule_id: str | None = None
    cost_schedule_digest: str | None = None
    decision_events: tuple[DecisionEvent, ...] = ()
    fill_decisions: tuple[FillDecision, ...] = ()
    cash_events: tuple[CashEvent, ...] = ()
    fee_events: tuple[FeeEvent, ...] = ()
    funding_events: tuple[FundingEvent, ...] = ()

    def __post_init__(self) -> None:
        _require_contiguous_sequences("decision_events", self.decision_events)
        _require_contiguous_sequences("fill_decisions", self.fill_decisions)
        _require_contiguous_sequences("cash_events", self.cash_events)
        _require_contiguous_sequences("fee_events", self.fee_events)
        _require_contiguous_sequences("funding_events", self.funding_events)

        cash_by_id: dict[CashEventId, CashEvent] = {}
        for row in self.cash_events:
            if row.cash_event_id in cash_by_id:
                raise EconomicTransitionError(
                    f"{REFUSED_INVALID_CASH_LEDGER_JOIN}: duplicate cash_event_id"
                )
            cash_by_id[row.cash_event_id] = row

        projected_ids: set[CashEventId] = set()
        for row in self.fee_events:
            self._validate_projection(
                row.cash_event_id,
                row.fee_cash_delta,
                CashEventKind.FEE,
                row.schedule_id,
                row.schedule_digest,
                projected_ids,
            )
        for row in self.funding_events:
            self._validate_projection(
                row.cash_event_id,
                row.funding_cash_delta,
                CashEventKind.FUNDING,
                row.schedule_id,
                row.schedule_digest,
                projected_ids,
            )

        required_projection_ids = {
            row.cash_event_id
            for row in self.cash_events
            if row.kind in (CashEventKind.FEE, CashEventKind.FUNDING)
        }
        if projected_ids != required_projection_ids:
            raise EconomicTransitionError(
                f"{REFUSED_INVALID_CASH_LEDGER_JOIN}: missing or extra typed projection"
            )

    def _validate_projection(
        self,
        cash_event_id: CashEventId,
        signed_delta: float,
        expected_kind: CashEventKind,
        schedule_id: str,
        schedule_digest: str,
        projected_ids: set[CashEventId],
    ) -> None:
        if cash_event_id in projected_ids:
            raise EconomicTransitionError(
                f"{REFUSED_INVALID_CASH_LEDGER_JOIN}: multiply linked typed projection"
            )
        cash_row = next(
            (row for row in self.cash_events if row.cash_event_id == cash_event_id),
            None,
        )
        if cash_row is None or cash_row.kind is not expected_kind:
            raise EconomicTransitionError(
                f"{REFUSED_INVALID_CASH_LEDGER_JOIN}: projection kind or join mismatch"
            )
        if not _same_binary64(cash_row.signed_delta, signed_delta):
            raise EconomicTransitionError(
                f"{REFUSED_INVALID_CASH_LEDGER_JOIN}: projection delta mismatch"
            )
        if expected_kind is CashEventKind.FEE:
            if (
                self.cost_schedule_id is None
                or schedule_id != self.cost_schedule_id
                or schedule_digest != self.cost_schedule_digest
            ):
                raise EconomicTransitionError(
                    f"{REFUSED_INVALID_CASH_LEDGER_JOIN}: cost schedule identity mismatch"
                )
        elif (
            schedule_id != self.funding_schedule_id
            or schedule_digest != self.funding_schedule_digest
        ):
            raise EconomicTransitionError(
                f"{REFUSED_INVALID_CASH_LEDGER_JOIN}: funding schedule identity mismatch"
            )
        projected_ids.add(cash_event_id)


@dataclass(slots=True)
class Bar:
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float
    bar_index: int
    indicators: dict[str, float] = field(default_factory=dict)
    htf: dict[str, float] = field(default_factory=dict)


@dataclass(slots=True)
class RawSignal:
    long: bool
    short: bool
    reason: Optional[str] = None
    direction: Optional[int] = None
    line: Optional[float] = None


@dataclass(slots=True)
class EntryDecision:
    can_open: bool
    side: str | None = None
    reason: str | None = None
    same_bar_reentry_allowed: bool = False


@dataclass(slots=True, frozen=True)
class GateResult:
    gate_name: str
    long_ok: bool
    short_ok: bool
    value: float | None = None
    # Architecture-required category field. "filter" = L14 filter-block exit candidate;
    # "guard" = blocks entry only, never produces FILTER_BLOCK close reason.
    # All current gates are "filter"; guard-category gates are deferred.
    category: str = "filter"


@dataclass(slots=True)
class EntryLeg:
    entry_price: float
    qty: float
    entry_bar: int


@dataclass(slots=True)
class WorkingExit:
    exit_id: str
    kind: str
    target_price: float | None
    stop_price: float | None
    qty_fraction: float
    book_version: int = 0
    active: bool = True


@dataclass(slots=True)
class Position:
    side: str
    entry_price: float
    avg_entry_price: float
    qty: float
    entry_bar: int
    initial_qty: float = 0.0
    active_stop_price: float | None = None
    active_tp_price: float | None = None
    entry_legs: list[EntryLeg] = field(default_factory=list)
    lifecycle_id: int = 0
    working_exit_reference_qty: float = 0.0
    working_exit_book_version: int = 0
    active_stop_owner: str | None = None
    working_exits: list[WorkingExit] = field(default_factory=list)
    completed_exit_ids: set[str] = field(default_factory=set)
    be_active: bool = False
    trail_active: bool = False
    trail_price: float | None = None
    initial_risk_per_unit: float | None = None


@dataclass(slots=True)
class ExitEvent:
    bar_index: int
    exit_price: float
    exit_qty: float
    exit_reason: str
    realized_pnl: float
    exit_id: str | None = None
    was_pessimistic: bool = False
    was_partial: bool = False


@dataclass
class HtfSnapshot:
    """Prior-closed HTF bar values for one LTF bar.

    ``None`` fields mean the HTF bar is not yet complete (warmup period).
    Mirrors Pine's ``request.security(..., expr[1], barmerge.lookahead_off)``.
    """

    close: float | None = None
    open: float | None = None
    high: float | None = None
    low: float | None = None
    volume: float | None = None

    @classmethod
    def from_dict(cls, d: dict | None) -> "HtfSnapshot":
        """Create from a ``build_htf_lookup`` dict entry (or ``None`` for warmup)."""
        if d is None:
            return cls()
        return cls(
            close=d["close"],
            open=d["open"],
            high=d["high"],
            low=d["low"],
            volume=d["volume"],
        )

    @property
    def is_ready(self) -> bool:
        """``True`` when a prior-closed HTF bar is available."""
        return self.close is not None


@dataclass(slots=True)
class PortfolioState:
    initial_capital: float = 0.0
    equity: float = 0.0
    realized_equity: float = 0.0
    unrealized_pnl: float = 0.0
    last_sizing_equity_snapshot: float = 0.0
    position: Optional[Position] = None
    current_bar_index: int = 0
    opened_this_bar_reason: Optional[str] = None
    closed_this_bar_reason: Optional[str] = None
    block_new_entries_this_bar: bool = False
    last_entry_bar_index: int | None = None
    last_exit_bar_index: int | None = None
    total_entries: int = 0
    total_exits: int = 0
    warmup_bars: int = 0
    execution_profile_id: str = ""
    last_exit_price: float | None = None
    last_exit_qty: float = 0.0
    last_exit_id: str | None = None
    last_realized_pnl: float = 0.0
    last_exit_was_pessimistic: bool = False
    last_exit_was_partial: bool = False
    exit_events_this_bar: list[ExitEvent] = field(default_factory=list)
    regime_lock_side: str | None = None
    next_position_lifecycle_id: int = 1
    gated_long: bool = False
    gated_short: bool = False
    gate_results: dict[str, GateResult] = field(default_factory=dict)
    instrument: InstrumentMetadata = field(default_factory=InstrumentMetadata)
    indicator_snapshot: IndicatorSnapshot = field(default_factory=IndicatorSnapshot)
