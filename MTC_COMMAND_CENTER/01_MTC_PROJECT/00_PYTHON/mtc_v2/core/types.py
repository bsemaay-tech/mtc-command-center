from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from mtc_v2.core.indicators import IndicatorSnapshot
from mtc_v2.core.instrument import InstrumentMetadata


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
