from __future__ import annotations

from dataclasses import replace
from datetime import datetime, timezone
from pathlib import Path

import pytest

from mtc_v2.core.economics import (
    CorrectedEconomicsAdapter,
    EconomicsRefusal,
    EconomicIntent,
    EconomicRecords,
    EconomicState,
    IntentKind,
    MarketEvent,
    REFUSED_DUPLICATE_FUNDING_EVENT,
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
    FundingEvent,
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
        fill_decisions=(
            replace(_d026_exit_fill("F0"), quantity=1.0),
            replace(_d026_exit_fill("F1"), sequence=1, quantity=1.0),
        ),
        cash_events=(
            _d026_gross_cash("CE-GROSS-0", "F0", signed_delta=-1e16),
            _d026_gross_cash("CE-GROSS-1", "F1", signed_delta=1.0, sequence=1),
        ),
    )
    state = PortfolioState(
        initial_capital=0.0,
        equity=1e16,
        realized_equity=1e16,
        position=_open_position(),
    )

    _manager().apply_transition(bar=_bar(), state=state, transition=transition)

    assert state.position is None
    assert state.realized_equity == 1.0
    assert state.equity == 1.0


def test_w279b_f13_cumulative_funding_applies_rows_in_order() -> None:
    funding_deltas = (-1e16, 1.0)
    transition = EconomicTransition(
        semantics_id="2.0.0",
        instrument_record_id="I",
        instrument_record_digest="0" * 64,
        funding_schedule_id="F",
        funding_schedule_digest="1" * 64,
        next_position_facts=PositionFacts(None, None, 0.0),
        cash_events=tuple(
            CashEvent(
                sequence=sequence,
                cash_event_id=f"CE-FUND-{sequence}",
                event_timestamp=NOW,
                lifecycle_id=1,
                kind=CashEventKind.FUNDING,
                signed_delta=delta,
                settlement_currency="TEST-USD",
                funding_event_id=f"FUND-{sequence}",
            )
            for sequence, delta in enumerate(funding_deltas)
        ),
        funding_events=tuple(
            FundingEvent(
                sequence=sequence,
                funding_event_id=f"FUND-{sequence}",
                event_timestamp=NOW,
                lifecycle_id=1,
                position_side="LONG",
                open_qty=1.0,
                contract_multiplier=1.0,
                mark_price=1.0,
                raw_rate=0.0,
                positive_rate_payer="LONG",
                long_cashflow_rate=0.0,
                notional=1.0,
                funding_cash_delta=delta,
                cumulative_funding=0.0 if sequence == 0 else 1.0,
                schedule_id="F",
                schedule_digest="1" * 64,
                source_event_digest="3" * 64 if sequence == 0 else "4" * 64,
                cash_event_id=f"CE-FUND-{sequence}",
            )
            for sequence, delta in enumerate(funding_deltas)
        ),
    )
    state = PortfolioState(cumulative_funding=1e16)

    _manager().apply_transition(bar=_bar(), state=state, transition=transition)

    assert state.cumulative_funding == 1.0


def test_w279b_f13_cumulative_fee_applies_rows_in_order() -> None:
    fee_amounts = (1e16, 1.0)
    transition = EconomicTransition(
        semantics_id="2.0.0",
        instrument_record_id="I",
        instrument_record_digest="0" * 64,
        cost_schedule_id="C",
        cost_schedule_digest="2" * 64,
        funding_schedule_id="F",
        funding_schedule_digest="1" * 64,
        next_position_facts=PositionFacts(None, None, 0.0),
        fill_decisions=tuple(
            replace(
                _d026_exit_fill(f"F{sequence}", sequence=sequence),
                quantity=1.0,
                exit_id=f"EXIT-{sequence}",
            )
            for sequence in range(len(fee_amounts))
        ),
        cash_events=(
            *tuple(
                CashEvent(
                    sequence=sequence,
                    cash_event_id=f"CE-FEE-{sequence}",
                    event_timestamp=NOW,
                    lifecycle_id=1,
                    kind=CashEventKind.FEE,
                    signed_delta=-amount,
                    settlement_currency="TEST-USD",
                    fill_id=f"F{sequence}",
                )
                for sequence, amount in enumerate(fee_amounts)
            ),
            *tuple(
                _d026_gross_cash(
                    f"CE-GROSS-{sequence}",
                    f"F{sequence}",
                    sequence=sequence + len(fee_amounts),
                    signed_delta=0.0,
                )
                for sequence in range(len(fee_amounts))
            ),
        ),
        fee_events=tuple(
            FeeEvent(
                sequence=sequence,
                event_timestamp=NOW,
                lifecycle_id=1,
                fill_id=f"F{sequence}",
                event_class="MARKET_EXIT",
                liquidity_role="TAKER",
                schedule_id="C",
                schedule_digest="2" * 64,
                rate=0.0,
                fixed_component=amount,
                fee_notional=1.0,
                fee_amount=amount,
                fee_cash_delta=-amount,
                settlement_currency="TEST-USD",
                cash_event_id=f"CE-FEE-{sequence}",
            )
            for sequence, amount in enumerate(fee_amounts)
        ),
    )
    state = PortfolioState(cumulative_fee=-1e16, position=_open_position())

    _manager().apply_transition(bar=_bar(), state=state, transition=transition)

    assert state.cumulative_fee == 1.0


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


def test_w283r_r5_funding_key_set_distinguishes_lifecycle_and_refuses_same_pair() -> None:
    records = EconomicRecords.from_record_paths(
        instrument_path=(
            RECORD_ROOT / "instruments" / "SYNTH-INSTRUMENT-RULE2-08-RED-V1.json"
        ),
        funding_path=RECORD_ROOT / "funding" / "SYNTH-FUNDING-RULE2-08-V1.json",
    )
    prior_keys = {("TEST-FUND-1", 1)}
    state = PortfolioState(
        initial_capital=1000.0,
        equity=1000.0,
        position=replace(_open_position(), lifecycle_id=2),
        applied_funding_event_keys=set(prior_keys),
    )
    economic_state = EconomicState(
        lifecycle_id=2,
        position_side="LONG",
        quantity=2.0,
        entry_fill_price=100.0,
        equity=1000.0,
        applied_funding_event_keys=frozenset(prior_keys),
    )
    intent = EconomicIntent(kind=IntentKind.FUNDING_TICK, funding_event_id="TEST-FUND-1")
    market = MarketEvent(NOW, 1, 100.0, 100.0, 100.0, 100.0)

    transition = CorrectedEconomicsAdapter().resolve(
        economic_state,
        intent,
        market,
        records,
    )
    _manager().apply_transition(bar=_bar(), state=state, transition=transition)

    assert state.applied_funding_event_keys == {
        ("TEST-FUND-1", 1),
        ("TEST-FUND-1", 2),
    }
    same_pair_state = replace(
        economic_state,
        applied_funding_event_keys=frozenset(state.applied_funding_event_keys),
    )
    with pytest.raises(EconomicsRefusal) as exc_info:
        CorrectedEconomicsAdapter().resolve(
            same_pair_state,
            intent,
            market,
            records,
        )
    assert exc_info.value.refusal_code == REFUSED_DUPLICATE_FUNDING_EVENT


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


def _mutate_transition(
    transition: EconomicTransition, **overrides: object
) -> EconomicTransition:
    for name, value in overrides.items():
        object.__setattr__(transition, name, value)
    return transition


def _funding_row(
    *,
    cash_event_id: str,
    funding_event_id: str,
    sequence: int,
) -> tuple[CashEvent, FundingEvent]:
    cash = CashEvent(
        sequence=sequence,
        cash_event_id=cash_event_id,
        event_timestamp=NOW,
        lifecycle_id=1,
        kind=CashEventKind.FUNDING,
        signed_delta=-0.1,
        settlement_currency="TEST-USD",
        funding_event_id=funding_event_id,
    )
    row = FundingEvent(
        sequence=sequence,
        funding_event_id=funding_event_id,
        event_timestamp=NOW,
        lifecycle_id=1,
        position_side="LONG",
        open_qty=1.0,
        contract_multiplier=1.0,
        mark_price=100.0,
        raw_rate=0.0,
        positive_rate_payer="LONG",
        long_cashflow_rate=0.0,
        notional=1.0,
        funding_cash_delta=-0.1,
        cumulative_funding=-0.1,
        schedule_id="F",
        schedule_digest="1" * 64,
        source_event_digest="3" * 64,
        cash_event_id=cash_event_id,
    )
    return cash, row


def test_d026_duplicate_cash_key_refuses_before_applied_set_collapses() -> None:
    base = EconomicTransition(
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
                signed_delta=1.0,
                settlement_currency="TEST-USD",
                fill_id="F0",
            ),
        ),
    )
    duplicate = _mutate_transition(
        base,
        cash_events=(
            base.cash_events[0],
            replace(base.cash_events[0], sequence=1),
        ),
    )
    state = PortfolioState(initial_capital=1000.0, equity=1000.0)
    initial = (state.realized_equity, state.equity, len(state.cash_events))
    with pytest.raises(
        EconomicTransitionError, match="duplicate cash event key"
    ):
        _manager().apply_transition(bar=_bar(), state=state, transition=duplicate)
    assert (state.realized_equity, state.equity, len(state.cash_events)) == initial
    assert state.cash_events == []


def test_d026_duplicate_funding_key_refuses_before_applied_set_collapses() -> None:
    cash_0, row_0 = _funding_row(
        cash_event_id="CE-FUND-0", funding_event_id="TEST-FUND-1", sequence=0
    )
    cash_1, row_1 = _funding_row(
        cash_event_id="CE-FUND-1", funding_event_id="TEST-FUND-1", sequence=1
    )
    base = EconomicTransition(
        semantics_id="2.0.0",
        instrument_record_id="I",
        instrument_record_digest="0" * 64,
        funding_schedule_id="F",
        funding_schedule_digest="1" * 64,
        next_position_facts=PositionFacts(None, None, 0.0),
        cash_events=(cash_0,),
        funding_events=(row_0,),
    )
    duplicate = _mutate_transition(
        base, cash_events=(cash_0, cash_1), funding_events=(row_0, row_1)
    )
    state = PortfolioState(initial_capital=1000.0, equity=1000.0)
    with pytest.raises(
        EconomicTransitionError, match="duplicate funding event key"
    ):
        _manager().apply_transition(bar=_bar(), state=state, transition=duplicate)
    assert state.funding_events == []
    assert state.applied_funding_event_keys == set()


def test_d026_duplicate_gross_fill_join_refuses_before_dict_fans_out() -> None:
    gross_cash = CashEvent(
        sequence=0,
        cash_event_id="CE-GROSS-0",
        event_timestamp=NOW,
        lifecycle_id=1,
        kind=CashEventKind.GROSS_REALIZATION,
        signed_delta=7.0,
        settlement_currency="TEST-USD",
        fill_id="F0",
    )
    base = EconomicTransition(
        semantics_id="2.0.0",
        instrument_record_id="I",
        instrument_record_digest="0" * 64,
        funding_schedule_id="F",
        funding_schedule_digest="1" * 64,
        next_position_facts=PositionFacts(None, None, 0.0),
        fill_decisions=(
            FillDecision(
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
            ),
        ),
        cash_events=(gross_cash,),
    )
    duplicate = _mutate_transition(
        base,
        cash_events=(
            gross_cash,
            replace(gross_cash, sequence=1, cash_event_id="CE-GROSS-1"),
        ),
    )
    state = PortfolioState(
        initial_capital=1000.0,
        equity=1000.0,
        position=_open_position(),
    )
    with pytest.raises(
        EconomicTransitionError, match="duplicate gross fill join"
    ):
        _manager().apply_transition(
            bar=_bar(), state=state, transition=duplicate, reason="time_stop"
        )
    assert state.exit_events_this_bar == []
    assert state.position is not None


def test_d026_duplicate_exit_fill_id_refuses_before_gross_join() -> None:
    gross_cash = CashEvent(
        sequence=0,
        cash_event_id="CE-GROSS-0",
        event_timestamp=NOW,
        lifecycle_id=1,
        kind=CashEventKind.GROSS_REALIZATION,
        signed_delta=7.0,
        settlement_currency="TEST-USD",
        fill_id="F0",
    )
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
        quantity=1.0,
        liquidity_role="TAKER",
        exit_id="TIME_STOP",
    )
    base = EconomicTransition(
        semantics_id="2.0.0",
        instrument_record_id="I",
        instrument_record_digest="0" * 64,
        funding_schedule_id="F",
        funding_schedule_digest="1" * 64,
        next_position_facts=PositionFacts(None, None, 0.0),
        fill_decisions=(fill,),
        cash_events=(gross_cash,),
    )
    duplicate = _mutate_transition(
        base,
        fill_decisions=(fill, replace(fill, sequence=1)),
    )
    state = PortfolioState(
        initial_capital=1000.0,
        equity=1000.0,
        position=_open_position(),
    )
    with pytest.raises(
        EconomicTransitionError, match="duplicate exit fill id"
    ):
        _manager().apply_transition(
            bar=_bar(), state=state, transition=duplicate, reason="time_stop"
        )
    assert state.exit_events_this_bar == []


def test_d026_applied_fill_renumber_keeps_independent_ids() -> None:
    fill = FillDecision(
        sequence=0,
        event_timestamp=NOW,
        lifecycle_id=1,
        fill_id="F5",
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
        cash_event_id="CE-GROSS-5",
        event_timestamp=NOW,
        lifecycle_id=1,
        kind=CashEventKind.GROSS_REALIZATION,
        signed_delta=7.0,
        settlement_currency="TEST-USD",
        fill_id="F5",
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

    assert [row.fill_id for row in state.fill_events] == ["F5"]
    assert [row.cash_event_id for row in state.cash_events] == ["CE-GROSS-5"]
    assert [row.exit_id for row in state.exit_events_this_bar] == ["TIME_STOP"]
    assert [row.fill_id for row in state.exit_events_this_bar] == ["F5"]
    assert [row.sequence for row in state.fill_events] == [0]
    assert [row.sequence for row in state.cash_events] == [0]


def _d026_bare_transition(**overrides: object) -> EconomicTransition:
    values: dict[str, object] = {
        "semantics_id": "2.0.0",
        "instrument_record_id": "I",
        "instrument_record_digest": "0" * 64,
        "funding_schedule_id": "F",
        "funding_schedule_digest": "1" * 64,
        "next_position_facts": PositionFacts(None, None, 0.0),
    }
    values.update(overrides)
    return EconomicTransition(**values)


def _d026_exit_fill(fill_id: str = "F0", *, sequence: int = 0) -> FillDecision:
    return FillDecision(
        sequence=sequence,
        event_timestamp=NOW,
        lifecycle_id=1,
        fill_id=fill_id,
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


def _d026_entry_fill(fill_id: str = "F0", *, sequence: int = 0) -> FillDecision:
    return FillDecision(
        sequence=sequence,
        event_timestamp=NOW,
        lifecycle_id=1,
        fill_id=fill_id,
        event_class="MARKET_ENTRY",
        side="BUY",
        reference_price=100.0,
        slippage_model_id="BPS_OF_REFERENCE_V1",
        slippage_bps=0.0,
        slippage_impact=0.0,
        slippage_application_count=1,
        final_fill_price=101.0,
        quantity=1.0,
        liquidity_role="TAKER",
    )


def _d026_gross_cash(
    cash_event_id: str,
    fill_id: str,
    *,
    sequence: int = 0,
    signed_delta: float = 7.0,
) -> CashEvent:
    return CashEvent(
        sequence=sequence,
        cash_event_id=cash_event_id,
        event_timestamp=NOW,
        lifecycle_id=1,
        kind=CashEventKind.GROSS_REALIZATION,
        signed_delta=signed_delta,
        settlement_currency="TEST-USD",
        fill_id=fill_id,
    )


def _d026_fee_cash(
    cash_event_id: str,
    fill_id: str,
    *,
    sequence: int = 0,
) -> CashEvent:
    return CashEvent(
        sequence=sequence,
        cash_event_id=cash_event_id,
        event_timestamp=NOW,
        lifecycle_id=1,
        kind=CashEventKind.FEE,
        signed_delta=-0.1,
        settlement_currency="TEST-USD",
        fill_id=fill_id,
    )


def _d026_fee_event(cash: CashEvent, *, sequence: int = 0) -> FeeEvent:
    return FeeEvent(
        sequence=sequence,
        event_timestamp=NOW,
        lifecycle_id=1,
        fill_id=cash.fill_id,
        event_class="ENTRY",
        liquidity_role="TAKER",
        schedule_id="COST",
        schedule_digest="2" * 64,
        rate=0.001,
        fixed_component=0.0,
        fee_notional=100.0,
        fee_amount=0.1,
        fee_cash_delta=cash.signed_delta,
        settlement_currency="TEST-USD",
        cash_event_id=cash.cash_event_id,
    )


def test_d026_exit_fill_without_gross_row_refuses_before_join() -> None:
    transition = _d026_bare_transition(fill_decisions=(_d026_exit_fill(),))
    state = PortfolioState(
        initial_capital=1000.0,
        equity=1000.0,
        position=_open_position(),
    )
    initial = (state.realized_equity, state.equity, state.guard_realized_equity)
    with pytest.raises(
        EconomicTransitionError, match="exit gross-cash join mismatch"
    ):
        _manager().apply_transition(
            bar=_bar(), state=state, transition=transition, reason="time_stop"
        )
    assert state.position is not None
    assert state.exit_events_this_bar == []
    assert (state.realized_equity, state.equity, state.guard_realized_equity) == initial


def test_d026_orphan_gross_row_refuses_before_join() -> None:
    transition = _d026_bare_transition(
        fill_decisions=(_d026_exit_fill(),),
        cash_events=(_d026_gross_cash("CE-GROSS-9", "F9"),),
    )
    state = PortfolioState(
        initial_capital=1000.0,
        equity=1000.0,
        position=_open_position(),
    )
    initial = (state.realized_equity, state.equity, state.guard_realized_equity)
    with pytest.raises(
        EconomicTransitionError, match="exit gross-cash join mismatch"
    ):
        _manager().apply_transition(
            bar=_bar(), state=state, transition=transition, reason="time_stop"
        )
    assert state.position is not None
    assert state.exit_events_this_bar == []
    assert (state.realized_equity, state.equity, state.guard_realized_equity) == initial


def test_d026_entry_bound_gross_fill_refuses_before_open() -> None:
    transition = _d026_bare_transition(
        next_position_facts=PositionFacts(1, "LONG", 1.0),
        fill_decisions=(_d026_entry_fill(),),
        cash_events=(_d026_gross_cash("CE-GROSS-0", "F0", signed_delta=1.0),),
    )
    state = PortfolioState(initial_capital=1000.0, equity=1000.0)
    initial = (state.realized_equity, state.equity, state.total_entries)
    with pytest.raises(
        EconomicTransitionError, match="gross cash row requires exit fill"
    ):
        _manager().apply_transition(
            bar=_bar(), state=state, transition=transition, reason="signal"
        )
    assert state.position is None
    assert state.cash_events == []
    assert (state.realized_equity, state.equity, state.total_entries) == initial


def test_d026_entry_bound_foreign_fee_fill_refuses_before_open() -> None:
    fee_cash = _d026_fee_cash("CE-FEE-9", "F9")
    transition = _d026_bare_transition(
        cost_schedule_id="COST",
        cost_schedule_digest="2" * 64,
        next_position_facts=PositionFacts(1, "LONG", 1.0),
        fill_decisions=(_d026_entry_fill(),),
        cash_events=(fee_cash,),
        fee_events=(_d026_fee_event(fee_cash),),
    )
    state = PortfolioState(initial_capital=1000.0, equity=1000.0)
    with pytest.raises(
        EconomicTransitionError, match="entry cash fill join mismatch"
    ):
        _manager().apply_transition(
            bar=_bar(), state=state, transition=transition, reason="signal"
        )
    assert state.position is None
    assert state.cash_events == []


def test_d026_entry_bound_duplicate_cash_fill_refuses() -> None:
    fee_cash_0 = _d026_fee_cash("CE-FEE-0", "F0")
    fee_cash_1 = _d026_fee_cash("CE-FEE-1", "F0", sequence=1)
    transition = _d026_bare_transition(
        cost_schedule_id="COST",
        cost_schedule_digest="2" * 64,
        next_position_facts=PositionFacts(1, "LONG", 1.0),
        fill_decisions=(_d026_entry_fill(),),
        cash_events=(fee_cash_0, fee_cash_1),
        fee_events=(
            _d026_fee_event(fee_cash_0),
            _d026_fee_event(fee_cash_1, sequence=1),
        ),
    )
    state = PortfolioState(initial_capital=1000.0, equity=1000.0)
    with pytest.raises(
        EconomicTransitionError, match="duplicate entry cash fill join"
    ):
        _manager().apply_transition(
            bar=_bar(), state=state, transition=transition, reason="signal"
        )
    assert state.position is None
    assert state.cash_events == []


def test_d026_no_fill_duplicate_gross_fill_refuses_before_mutation() -> None:
    transition = _d026_bare_transition(
        cash_events=(
            _d026_gross_cash("CE-GROSS-0", "F0"),
            _d026_gross_cash("CE-GROSS-1", "F0", sequence=1, signed_delta=1.0),
        ),
    )
    state = PortfolioState(initial_capital=0.0, equity=0.0)
    initial = (state.realized_equity, state.equity)
    with pytest.raises(
        EconomicTransitionError, match="duplicate gross fill join"
    ):
        _manager().apply_transition(bar=_bar(), state=state, transition=transition)
    assert (state.realized_equity, state.equity) == initial
    assert state.cash_events == []


def test_d026_no_fill_valid_gross_row_refuses_before_mutation() -> None:
    transition = _d026_bare_transition(
        cash_events=(_d026_gross_cash("CE-GROSS-0", "F0"),),
    )
    state = PortfolioState(initial_capital=0.0, equity=0.0)
    initial = (state.realized_equity, state.equity)
    with pytest.raises(
        EconomicTransitionError, match="gross cash row requires exit fill"
    ):
        _manager().apply_transition(bar=_bar(), state=state, transition=transition)
    assert (state.realized_equity, state.equity) == initial
    assert state.cash_events == []
    assert state.position is None


def test_d026_no_fill_gross_missing_fill_id_refuses_after_mutation() -> None:
    base = _d026_bare_transition(
        cash_events=(_d026_gross_cash("CE-GROSS-0", "F0"),),
    )
    stripped = _mutate_transition(
        base,
        cash_events=(replace(base.cash_events[0], fill_id=None),),
    )
    state = PortfolioState(initial_capital=0.0, equity=0.0)
    with pytest.raises(
        EconomicTransitionError, match="gross cash row requires fill_id"
    ):
        _manager().apply_transition(bar=_bar(), state=state, transition=stripped)
    assert state.realized_equity == 0.0
    assert state.cash_events == []
