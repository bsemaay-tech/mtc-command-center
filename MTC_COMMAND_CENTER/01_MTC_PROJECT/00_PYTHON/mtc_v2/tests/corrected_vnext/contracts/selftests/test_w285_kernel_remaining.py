from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import pytest

from mtc_v2.core.economics import (
    CorrectedEconomicsAdapter,
    EconomicIntent,
    EconomicRecords,
    EconomicState,
    ExitCandidate,
    IntentKind,
    MarketEvent,
)
from mtc_v2.core.position_manager import PositionManager
from mtc_v2.core.results import _closed_lifecycle_trades
from mtc_v2.core.types import (
    Bar,
    EconomicTransitionError,
    EntryLeg,
    FillDecision,
    PortfolioState,
    Position,
)


MTC_V2_ROOT = Path(__file__).resolve().parents[4]
CORE_ROOT = MTC_V2_ROOT / "core"
RECORD_ROOT = CORE_ROOT / "economic_records"
NOW = datetime(2000, 1, 1, tzinfo=timezone.utc)
SMALL_POSITIVE_REMAINDER = 1.0 - 0.9999999999995


def _records(scenario_id: str) -> EconomicRecords:
    return EconomicRecords.from_record_paths(
        instrument_path=(
            RECORD_ROOT
            / "instruments"
            / f"SYNTH-INSTRUMENT-{scenario_id}-V1.json"
        ),
        cost_path=RECORD_ROOT / "costs" / f"SYNTH-COST-{scenario_id}-V1.json",
        funding_path=(
            RECORD_ROOT / "funding" / f"SYNTH-FUNDING-{scenario_id}-V1.json"
        ),
    )


def _fill(*, event_class: str, quantity: float, exit_id: str | None = None) -> FillDecision:
    return FillDecision(
        sequence=0,
        event_timestamp=NOW,
        lifecycle_id=1,
        fill_id="F0",
        event_class=event_class,
        side="BUY" if event_class == "ENTRY" else "SELL",
        reference_price=100.0,
        slippage_model_id="BPS_OF_REFERENCE_V1",
        slippage_bps=0.0,
        slippage_impact=0.0,
        slippage_application_count=1,
        final_fill_price=100.0,
        quantity=quantity,
        liquidity_role="TAKER",
        exit_id=exit_id,
    )


def _manager() -> PositionManager:
    return PositionManager(
        enable_long=True,
        enable_short=True,
        regime_lock=False,
        max_entries=1,
        cooldown_bars=0,
        contract_multiplier=1.0,
        qty_step=1e-15,
    )


def _bar() -> Bar:
    return Bar(NOW, 100.0, 100.0, 100.0, 100.0, 1.0, 1)


def test_w279_f13_price_exit_preserves_a_positive_binary64_remainder() -> None:
    transition = CorrectedEconomicsAdapter().resolve(
        EconomicState(
            lifecycle_id=1,
            position_side="LONG",
            quantity=1.0,
            entry_fill_price=100.0,
        ),
        EconomicIntent(
            kind=IntentKind.TARGET,
            exit_candidates=(
                ExitCandidate(
                    "TARGET-ALMOST-ALL",
                    IntentKind.TARGET,
                    101.0,
                    0.9999999999995,
                ),
            ),
            same_bar_collision_policy_id="STOP_FIRST",
        ),
        MarketEvent(NOW, 1, 100.0, 101.0, 100.0, 101.0),
        _records("RULE2-06-RED"),
    )

    assert transition.next_position_facts.lifecycle_id == 1
    assert transition.next_position_facts.quantity.hex() == SMALL_POSITIVE_REMAINDER.hex()


def test_w279_f13_market_exit_preserves_a_positive_binary64_remainder() -> None:
    transition = CorrectedEconomicsAdapter().resolve(
        EconomicState(
            lifecycle_id=1,
            position_side="LONG",
            quantity=1.0,
            entry_fill_price=100.0,
        ),
        EconomicIntent(
            kind=IntentKind.MARKET_EXIT,
            requested_quantity=0.9999999999995,
            event_class="MARKET_EXIT",
            exit_id="ALMOST-ALL",
        ),
        MarketEvent(NOW, 1, 100.0, 100.0, 100.0, 100.0),
        _records("RULE2-07-RED"),
    )

    assert transition.next_position_facts.lifecycle_id == 1
    assert transition.next_position_facts.quantity.hex() == SMALL_POSITIVE_REMAINDER.hex()


def test_w279_f13_position_manager_keeps_a_positive_binary64_remainder() -> None:
    position = Position(
        side="long",
        entry_price=100.0,
        avg_entry_price=100.0,
        qty=1.0,
        entry_bar=0,
        initial_qty=1.0,
        entry_legs=[EntryLeg(100.0, 1.0, 0)],
        lifecycle_id=1,
    )
    exited = 0.9999999999995
    remaining = position.qty - exited

    next_position = PositionManager._position_after_exit(
        position,
        (_fill(event_class="MARKET_EXIT", quantity=exited, exit_id="ALMOST-ALL"),),
        next_quantity=remaining,
        qty_step=1e-15,
    )

    assert next_position is not None
    assert next_position.qty.hex() == remaining.hex()


def test_w279_f13_trade_requires_exactly_complete_exit_quantity() -> None:
    state = PortfolioState(
        fill_events=[
            _fill(event_class="ENTRY", quantity=1.0),
            _fill(
                event_class="MARKET_EXIT",
                quantity=0.9999999999995,
                exit_id="ALMOST-ALL",
            ),
        ]
    )

    assert _closed_lifecycle_trades(state) == []


def test_w279_f13_corrected_path_contains_no_new_absolute_epsilon() -> None:
    economics_source = (CORE_ROOT / "economics.py").read_text(encoding="utf-8")
    manager_source = (CORE_ROOT / "position_manager.py").read_text(encoding="utf-8")
    results_source = (CORE_ROOT / "results.py").read_text(encoding="utf-8")

    assert "1e-12" not in economics_source
    assert manager_source.count("1e-12") == 1  # Frozen legacy close threshold.
    assert "1e-12" not in results_source


def test_w279_f16_fee_cash_event_id_uses_the_fill_sequence() -> None:
    transition = CorrectedEconomicsAdapter().resolve(
        EconomicState(
            lifecycle_id=1,
            position_side="LONG",
            quantity=1.0,
            entry_fill_price=100.0,
            next_fill_sequence=7,
            next_cash_sequence=11,
            next_fee_sequence=2,
        ),
        EconomicIntent(
            kind=IntentKind.MARKET_EXIT,
            event_class="MARKET_EXIT",
            exit_id="EXIT-SEVEN",
        ),
        MarketEvent(NOW, 1, 100.0, 100.0, 100.0, 100.0),
        _records("RULE2-07-RED"),
    )

    assert transition.fill_decisions[0].fill_id == "F7"
    assert transition.fee_events[0].sequence == 2
    assert transition.cash_events[0].cash_event_id == "CE-FEE-7"
    assert transition.fee_events[0].cash_event_id == "CE-FEE-7"


def test_w279_f19_distinct_empty_transitions_have_distinct_apply_identities() -> None:
    economic_state = EconomicState(
        lifecycle_id=1,
        position_side="LONG",
        quantity=1.0,
        entry_fill_price=100.0,
        next_decision_sequence=1,
    )
    intent = EconomicIntent(
        kind=IntentKind.MARKET_EXIT,
        requested_quantity=0.0,
        event_class="MARKET_EXIT",
        exit_id="NO-OP",
    )
    market = MarketEvent(NOW, 1, 100.0, 100.0, 100.0, 100.0)
    records = _records("RULE2-07-RED")
    first = CorrectedEconomicsAdapter().resolve(economic_state, intent, market, records)
    second = CorrectedEconomicsAdapter().resolve(economic_state, intent, market, records)
    assert not first.decision_events and not first.fill_decisions and not first.cash_events
    assert not second.decision_events and not second.fill_decisions and not second.cash_events

    position = Position(
        side="long",
        entry_price=100.0,
        avg_entry_price=100.0,
        qty=1.0,
        entry_bar=0,
        initial_qty=1.0,
        entry_legs=[EntryLeg(100.0, 1.0, 0)],
        lifecycle_id=1,
    )
    state = PortfolioState(position=position)
    manager = _manager()

    manager.apply_transition(bar=_bar(), state=state, transition=first)
    manager.apply_transition(bar=_bar(), state=state, transition=second)
    assert len(state.applied_transition_keys) == 2
    with pytest.raises(EconomicTransitionError, match="transition already applied"):
        manager.apply_transition(bar=_bar(), state=state, transition=first)
