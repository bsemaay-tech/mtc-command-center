from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import pytest

from mtc_v2.core.economics import (
    CorrectedEconomicsAdapter,
    EconomicIntent,
    EconomicRecords,
    EconomicState,
    IntentKind,
    MarketEvent,
)
from mtc_v2.core.exits import resolve_corrected_price_exits
from mtc_v2.core.position_manager import PositionManager
from mtc_v2.core.types import (
    Bar,
    CashEvent,
    CashEventKind,
    EconomicTransition,
    EconomicTransitionError,
    EntryLeg,
    FeeEvent,
    FillDecision,
    PortfolioState,
    Position,
    PositionFacts,
    WorkingExit,
)


MTC_V2_ROOT = Path(__file__).resolve().parents[4]
RECORD_ROOT = MTC_V2_ROOT / "core" / "economic_records"
NOW = datetime(2000, 1, 1, 0, 12, tzinfo=timezone.utc)


def _records(scenario_id: str) -> EconomicRecords:
    return EconomicRecords.from_record_paths(
        instrument_path=(
            RECORD_ROOT / "instruments" / f"SYNTH-INSTRUMENT-{scenario_id}-V1.json"
        ),
        cost_path=RECORD_ROOT / "costs" / f"SYNTH-COST-{scenario_id}-V1.json",
        funding_path=RECORD_ROOT / "funding" / f"SYNTH-FUNDING-{scenario_id}-V1.json",
    )


def _manager() -> PositionManager:
    return PositionManager(
        enable_long=True,
        enable_short=True,
        regime_lock=False,
        max_entries=2,
        cooldown_bars=0,
        contract_multiplier=1.0,
        qty_step=1.0,
    )


def _bar(*, index: int = 1, open_: float = 100.0, high: float = 100.0,
         low: float = 100.0, close: float = 100.0) -> Bar:
    return Bar(NOW, open_, high, low, close, 1.0, index)


def _open_position(*, completed: set[str] | None = None) -> Position:
    return Position(
        side="long",
        entry_price=100.0,
        avg_entry_price=100.0,
        qty=2.0,
        entry_bar=0,
        initial_qty=2.0,
        active_stop_price=90.0,
        active_tp_price=105.0,
        entry_legs=[EntryLeg(100.0, 2.0, 0)],
        lifecycle_id=1,
        working_exit_reference_qty=2.0,
        working_exit_book_version=1,
        active_stop_owner="STOP",
        working_exits=[
            WorkingExit("TARGET-NEAR", "TP1", 105.0, None, 0.5, 1),
            WorkingExit("TARGET-FAR", "TP2", 110.0, None, 1.0, 1),
        ],
        completed_exit_ids=set(completed or ()),
        initial_risk_per_unit=10.0,
    )


def test_apply_transition_opens_at_final_fill_and_applies_only_cash_ledger() -> None:
    records = _records("RULE2-05-RED")
    transition = CorrectedEconomicsAdapter().resolve(
        EconomicState(sizing_equity=1000.0),
        EconomicIntent(
            kind=IntentKind.OPEN,
            action_side="BUY",
            position_side="LONG",
            reference_price=100.0,
            requested_quantity=1.0,
            fallback_size_pct=10.0,
            max_leverage_cap=10.0,
        ),
        MarketEvent(NOW, 1, 100.0, 100.0, 100.0, 100.0),
        records,
    )
    state = PortfolioState(initial_capital=1000.0, equity=1000.0)

    _manager().apply_transition(
        bar=_bar(), state=state, transition=transition, reason="signal"
    )

    assert state.position is not None
    assert state.position.entry_price == 101.0
    assert state.position.avg_entry_price == 101.0
    assert state.position.qty == 0.0
    assert state.realized_equity == transition.cash_events[0].signed_delta
    assert state.equity == 1000.0 + transition.cash_events[0].signed_delta
    assert state.cash_events == list(transition.cash_events)
    assert state.fee_events == list(transition.fee_events)


def test_w276_f01_runtime_equity_applies_cash_events_in_order() -> None:
    transition = EconomicTransition(
        semantics_id="2.0.0",
        instrument_record_id="I",
        instrument_record_digest="0" * 64,
        funding_schedule_id="F",
        funding_schedule_digest="1" * 64,
        next_position_facts=PositionFacts(None, None, 0.0),
        cash_events=(
            CashEvent(
                sequence=0,
                cash_event_id="CE-GROSS-0",
                event_timestamp=NOW,
                lifecycle_id=1,
                kind=CashEventKind.GROSS_REALIZATION,
                signed_delta=-1e16,
                settlement_currency="TEST-USD",
                fill_id="F0",
            ),
            CashEvent(
                sequence=1,
                cash_event_id="CE-GROSS-1",
                event_timestamp=NOW,
                lifecycle_id=1,
                kind=CashEventKind.GROSS_REALIZATION,
                signed_delta=1.0,
                settlement_currency="TEST-USD",
                fill_id="F1",
            ),
        ),
    )
    state = PortfolioState(
        initial_capital=0.0,
        equity=1e16,
        realized_equity=1e16,
    )

    _manager().apply_transition(bar=_bar(), state=state, transition=transition)

    assert state.realized_equity == 1.0
    assert state.equity == 1.0


def test_apply_transition_is_atomic_and_cannot_apply_same_cash_twice() -> None:
    transition = CorrectedEconomicsAdapter().resolve(
        EconomicState(sizing_equity=1000.0),
        EconomicIntent(
            kind=IntentKind.OPEN,
            action_side="BUY",
            position_side="LONG",
            reference_price=100.0,
            requested_quantity=1.0,
            fallback_size_pct=10.0,
            max_leverage_cap=10.0,
        ),
        MarketEvent(NOW, 1, 100.0, 100.0, 100.0, 100.0),
        _records("RULE2-05-GREEN"),
    )
    state = PortfolioState(initial_capital=1000.0, equity=1000.0)
    manager = _manager()
    manager.apply_transition(bar=_bar(), state=state, transition=transition)
    snapshot = (state.realized_equity, state.equity, len(state.cash_events))

    with pytest.raises(EconomicTransitionError, match="already applied"):
        manager.apply_transition(bar=_bar(), state=state, transition=transition)

    assert (state.realized_equity, state.equity, len(state.cash_events)) == snapshot


def test_exit_application_uses_gross_cash_fact_instead_of_recomputing_pnl() -> None:
    fill = FillDecision(
        sequence=0,
        event_timestamp=NOW,
        lifecycle_id=1,
        fill_id="F0",
        event_class="MARKET_EXIT",
        side="SELL",
        reference_price=110.0,
        slippage_model_id="BPS_OF_REFERENCE_V1",
        slippage_bps=0.0,
        slippage_impact=0.0,
        slippage_application_count=1,
        final_fill_price=110.0,
        quantity=2.0,
        liquidity_role="TAKER",
        exit_id="TIME_STOP",
    )
    gross = CashEvent(
        sequence=0,
        cash_event_id="CE-GROSS-0",
        event_timestamp=NOW,
        lifecycle_id=1,
        kind=CashEventKind.GROSS_REALIZATION,
        signed_delta=7.0,
        settlement_currency="TEST-USD",
        fill_id="F0",
    )
    transition = EconomicTransition(
        semantics_id="2.0.0",
        instrument_record_id="I",
        instrument_record_digest="0" * 64,
        funding_schedule_id="F",
        funding_schedule_digest="1" * 64,
        next_position_facts=PositionFacts(None, None, 0.0),
        fill_decisions=(fill,),
        cash_events=(gross,),
    )
    state = PortfolioState(
        initial_capital=1000.0,
        equity=1000.0,
        position=_open_position(),
    )

    _manager().apply_transition(
        bar=_bar(), state=state, transition=transition, reason="time_stop"
    )

    assert state.position is None
    assert state.realized_equity == 7.0
    assert state.last_gross_realized_pnl == 7.0
    assert state.exit_events_this_bar[0].realized_pnl == 7.0


def test_p13_partial_target_preserves_remainder_and_completed_ids() -> None:
    state = PortfolioState(
        initial_capital=1000.0,
        equity=1000.0,
        position=_open_position(completed={"OLD-TARGET"}),
    )
    transition = resolve_corrected_price_exits(
        bar=_bar(high=106.0, low=99.0, close=104.0),
        position=state.position,
        records=_records("RULE2-06-RED"),
        same_bar_collision_policy_id="STOP_FIRST",
    )

    _manager().apply_transition(
        bar=_bar(high=106.0, low=99.0, close=104.0),
        state=state,
        transition=transition,
        reason="TARGET",
    )

    assert state.position is not None
    assert state.position.qty == 1.0
    assert state.position.completed_exit_ids == {"OLD-TARGET", "TARGET-NEAR"}
    assert [row.exit_id for row in state.position.working_exits if row.active] == [
        "TARGET-FAR"
    ]
    assert [row.exit_id for row in state.exit_events_this_bar] == ["TARGET-NEAR"]


def test_p22_stop_first_collision_applies_full_close_with_no_remainder() -> None:
    state = PortfolioState(
        initial_capital=1000.0,
        equity=1000.0,
        position=_open_position(),
    )
    bar = _bar(high=115.0, low=85.0, close=105.0)
    transition = resolve_corrected_price_exits(
        bar=bar,
        position=state.position,
        records=_records("RULE2-06-RED"),
    )

    _manager().apply_transition(
        bar=bar, state=state, transition=transition, reason="PROTECTIVE_STOP"
    )

    assert state.position is None
    assert state.exit_events_this_bar[0].exit_id == "STOP"
    assert state.last_exit_qty == 2.0


def test_open10_closed_guard_pnl_is_gross_minus_all_lifecycle_fees() -> None:
    records = _records("RULE2-07-RED")
    entry = CorrectedEconomicsAdapter().resolve(
        EconomicState(sizing_equity=1000.0),
        EconomicIntent(
            kind=IntentKind.OPEN,
            action_side="BUY",
            position_side="LONG",
            reference_price=100.0,
            requested_quantity=1.0,
            fallback_size_pct=10.0,
            max_leverage_cap=10.0,
        ),
        MarketEvent(NOW.replace(minute=11), 1, 100.0, 100.0, 100.0, 100.0),
        records,
    )
    exit_fill = FillDecision(
        sequence=0,
        event_timestamp=NOW,
        lifecycle_id=1,
        fill_id="F0",
        event_class="MARKET_EXIT",
        side="SELL",
        reference_price=100.0,
        slippage_model_id="BPS_OF_REFERENCE_V1",
        slippage_bps=0.0,
        slippage_impact=0.0,
        slippage_application_count=1,
        final_fill_price=100.0,
        quantity=1.0,
        liquidity_role="TAKER",
        exit_id="TIME_STOP",
    )
    exit_fee_cash = CashEvent(
        sequence=0,
        cash_event_id="CE-FEE-0",
        event_timestamp=NOW,
        lifecycle_id=1,
        kind=CashEventKind.FEE,
        signed_delta=-0.1,
        settlement_currency="TEST-USD",
        fill_id="F0",
    )
    exit_gross_cash = CashEvent(
        sequence=1,
        cash_event_id="CE-GROSS-0",
        event_timestamp=NOW,
        lifecycle_id=1,
        kind=CashEventKind.GROSS_REALIZATION,
        signed_delta=0.0,
        settlement_currency="TEST-USD",
        fill_id="F0",
    )
    exit_transition = EconomicTransition(
        semantics_id="2.0.0",
        instrument_record_id=records.instrument.record_id,
        instrument_record_digest=records.instrument.digest,
        cost_schedule_id=records.cost_schedule_id,
        cost_schedule_digest=records.cost_digest,
        funding_schedule_id=records.funding_schedule_id,
        funding_schedule_digest=records.funding_digest,
        next_position_facts=PositionFacts(None, None, 0.0),
        fill_decisions=(exit_fill,),
        cash_events=(exit_fee_cash, exit_gross_cash),
        fee_events=(
            FeeEvent(
                sequence=0,
                event_timestamp=NOW,
                lifecycle_id=1,
                fill_id="F0",
                event_class="MARKET_EXIT",
                liquidity_role="TAKER",
                schedule_id=str(records.cost_schedule_id),
                schedule_digest=str(records.cost_digest),
                rate=0.001,
                fixed_component=0.0,
                fee_notional=100.0,
                fee_amount=0.1,
                fee_cash_delta=-0.1,
                settlement_currency="TEST-USD",
                cash_event_id="CE-FEE-0",
            ),
        ),
    )
    state = PortfolioState(initial_capital=1000.0, equity=1000.0)
    manager = _manager()
    manager.apply_transition(bar=_bar(), state=state, transition=entry)
    manager.apply_transition(
        bar=_bar(index=2),
        state=state,
        transition=exit_transition,
        reason="time_stop",
    )

    assert state.last_gross_realized_pnl == 0.0
    assert state.last_closed_guard_pnl == -0.2
    assert state.last_realized_pnl == -0.2
    assert state.guard_realized_equity == -0.2
    assert state.realized_equity == -0.2


def test_funding_transition_updates_signed_total_and_exact_event_identity() -> None:
    records = EconomicRecords.from_record_paths(
        instrument_path=(
            RECORD_ROOT / "instruments" / "SYNTH-INSTRUMENT-RULE2-08-RED-V1.json"
        ),
        funding_path=RECORD_ROOT / "funding" / "SYNTH-FUNDING-RULE2-08-V1.json",
    )
    transition = CorrectedEconomicsAdapter().resolve(
        EconomicState(
            lifecycle_id=1,
            position_side="LONG",
            quantity=2.0,
            entry_fill_price=100.0,
            equity=1000.0,
        ),
        EconomicIntent(kind=IntentKind.FUNDING_TICK, funding_event_id="TEST-FUND-1"),
        MarketEvent(NOW, 1, 100.0, 100.0, 100.0, 100.0),
        records,
    )
    state = PortfolioState(
        initial_capital=1000.0,
        equity=1000.0,
        position=_open_position(),
    )

    _manager().apply_transition(bar=_bar(), state=state, transition=transition)

    assert state.position is not None and state.position.qty == 2.0
    assert state.cumulative_funding == -0.2
    assert state.funding_events == list(transition.funding_events)
    assert state.applied_funding_event_keys == {("TEST-FUND-1", 1)}


def test_p08_same_side_add_retains_book_history_and_final_entry_facts() -> None:
    state = PortfolioState(position=_open_position(completed={"TARGET-NEAR"}))
    replacement = [WorkingExit("TARGET-FAR", "TP2", 112.0, None, 1.0, 2)]

    _manager().open_position(
        bar=_bar(index=2, close=101.0),
        side="long",
        qty=1.0,
        state=state,
        reason="add",
        active_stop_price=91.0,
        working_exits=replacement,
        fill_price=101.0,
    )

    assert state.position is not None
    assert state.position.qty == 3.0
    assert state.position.avg_entry_price == pytest.approx(100.0 + (1.0 / 3.0))
    assert state.position.active_stop_price == 91.0
    assert state.position.working_exit_book_version == 2
    assert state.position.completed_exit_ids == {"TARGET-NEAR"}
    assert state.position.working_exits == replacement
