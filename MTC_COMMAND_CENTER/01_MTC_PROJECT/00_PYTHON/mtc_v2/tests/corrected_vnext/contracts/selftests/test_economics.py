from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import pytest

from mtc_v2.core.economics import (
    CorrectedEconomicsAdapter,
    EconomicIntent,
    EconomicRecords,
    EconomicState,
    EconomicsRefusal,
    ExitCandidate,
    IntentKind,
    LegacyEconomicsAdapter,
    MarketEvent,
    REFUSED_AMBIGUOUS_SAME_BAR,
    REFUSED_DUPLICATE_FUNDING_EVENT,
    REFUSED_MISSING_COST_SCHEDULE,
    REFUSED_MISSING_FUNDING_EVENT,
    REFUSED_UNSUPPORTED_COLLISION_POLICY,
)


MTC_V2_ROOT = Path(__file__).resolve().parents[4]
RECORD_ROOT = MTC_V2_ROOT / "core" / "economic_records"


def _records(scenario_id: str) -> EconomicRecords:
    return EconomicRecords.from_record_paths(
        instrument_path=(
            RECORD_ROOT / "instruments" / f"SYNTH-INSTRUMENT-{scenario_id}-V1.json"
        ),
        cost_path=RECORD_ROOT / "costs" / f"SYNTH-COST-{scenario_id}-V1.json",
        funding_path=RECORD_ROOT / "funding" / f"SYNTH-FUNDING-{scenario_id}-V1.json",
    )


def test_corrected_open_uses_multiplier_and_emits_one_fee_cash_join() -> None:
    market = MarketEvent(
        timestamp=datetime(2000, 1, 1, 0, 11, tzinfo=timezone.utc),
        bar_index=1,
        open=100.0,
        high=100.0,
        low=100.0,
        close=100.0,
    )
    state = EconomicState(sizing_equity=1000.0)
    intent = EconomicIntent(
        kind=IntentKind.OPEN,
        action_side="BUY",
        position_side="LONG",
        reference_price=100.0,
        stop_price=90.0,
        risk_pct=10.0,
        fallback_size_pct=10.0,
        max_leverage_cap=10.0,
    )
    records = _records("RULE2-01-RED")

    corrected = CorrectedEconomicsAdapter().resolve(state, intent, market, records)
    legacy = LegacyEconomicsAdapter().resolve(state, intent, market, records)

    assert corrected.fill_decisions[0].quantity == 5.0
    assert corrected.next_position_facts.quantity == 5.0
    assert corrected.cash_events[0].signed_delta == -0.45
    assert corrected.fee_events[0].cash_event_id == corrected.cash_events[0].cash_event_id
    assert legacy.fill_decisions[0].quantity == 10.0
    assert legacy.cash_events == ()


def _collision_intent(policy: str | None, *, equal_prices: bool = False) -> EconomicIntent:
    return EconomicIntent(
        kind=IntentKind.PROTECTIVE_STOP,
        exit_candidates=(
            ExitCandidate("TARGET-NEAR", IntentKind.TARGET, 105.0, 0.5),
            ExitCandidate("TARGET-FAR", IntentKind.TARGET, 105.0 if equal_prices else 110.0, 0.5),
            ExitCandidate("STOP", IntentKind.PROTECTIVE_STOP, 90.0),
        ),
        same_bar_collision_policy_id=policy,
    )


def _collision_market() -> MarketEvent:
    return MarketEvent(
        timestamp=datetime(2000, 1, 1, 0, 12, tzinfo=timezone.utc),
        bar_index=2,
        open=100.0,
        high=115.0,
        low=85.0,
        close=105.0,
    )


def _open_long_state() -> EconomicState:
    return EconomicState(
        lifecycle_id=1,
        position_side="LONG",
        quantity=2.0,
        entry_fill_price=100.0,
        sizing_equity=1000.0,
        equity=999.91,
    )


def test_collision_policies_resolve_before_slippage_and_cash() -> None:
    records = _records("RULE2-06-RED")
    adapter = CorrectedEconomicsAdapter()

    stop_first = adapter.resolve(
        _open_long_state(), _collision_intent("STOP_FIRST"), _collision_market(), records
    )
    target_first = adapter.resolve(
        _open_long_state(), _collision_intent("TARGET_FIRST"), _collision_market(), records
    )

    assert [(row.final_fill_price, row.quantity) for row in stop_first.fill_decisions] == [
        (90.0, 2.0)
    ]
    assert [row.fill_id for row in target_first.fill_decisions] == ["F0", "F1"]
    assert [(row.final_fill_price, row.quantity) for row in target_first.fill_decisions] == [
        (105.0, 1.0),
        (110.0, 1.0),
    ]
    assert [row.kind.value for row in target_first.cash_events] == [
        "FEE",
        "GROSS_REALIZATION",
        "FEE",
        "GROSS_REALIZATION",
    ]
    assert target_first.next_position_facts.quantity == 0.0


def test_equal_price_target_first_orders_by_exit_id_utf8_bytes() -> None:
    transition = CorrectedEconomicsAdapter().resolve(
        _open_long_state(),
        _collision_intent("TARGET_FIRST", equal_prices=True),
        _collision_market(),
        _records("RULE2-06-EQUAL-PRICE-RED"),
    )

    collision = next(
        row
        for row in transition.decision_events
        if row.decision == "COLLISION_RESOLVED"
    )
    chosen = dict(collision.details)["ordered_chosen_exit_ids"]
    assert chosen == ["TARGET-FAR", "TARGET-NEAR"]


def test_finite_corrected_exit_vocabulary_omits_unmapped_short_tokens() -> None:
    state = _open_long_state()
    state = EconomicState(
        lifecycle_id=state.lifecycle_id,
        position_side="SHORT",
        quantity=state.quantity,
        entry_fill_price=state.entry_fill_price,
        sizing_equity=state.sizing_equity,
        equity=state.equity,
    )

    transition = CorrectedEconomicsAdapter().resolve(
        state,
        _collision_intent("STOP_FIRST"),
        _collision_market(),
        _records("RULE2-06-RED"),
    )

    assert transition.fill_decisions
    assert "HIGH_TOUCH" not in repr(transition.decision_events)
    assert "SHORT_DESCENDING_TARGET_PRICE" not in repr(transition.decision_events)


@pytest.mark.parametrize(
    ("policy", "code"),
    [
        (None, REFUSED_UNSUPPORTED_COLLISION_POLICY),
        ("UNKNOWN", REFUSED_UNSUPPORTED_COLLISION_POLICY),
        ("SUBBAR_UNKNOWN", REFUSED_AMBIGUOUS_SAME_BAR),
    ],
)
def test_collision_refusal_families(policy: str | None, code: str) -> None:
    with pytest.raises(EconomicsRefusal) as exc_info:
        CorrectedEconomicsAdapter().resolve(
            _open_long_state(), _collision_intent(policy), _collision_market(), _records("RULE2-06-RED")
        )
    assert exc_info.value.refusal_code == code


def test_slippage_is_adverse_tick_aligned_and_applied_once() -> None:
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
        MarketEvent(
            timestamp=datetime(2000, 1, 1, 0, 11, tzinfo=timezone.utc),
            bar_index=1,
            open=100.0,
            high=100.0,
            low=100.0,
            close=100.0,
        ),
        _records("RULE2-05-RED"),
    )

    fill = transition.fill_decisions[0]
    assert (fill.reference_price, fill.slippage_impact, fill.final_fill_price) == (
        100.0,
        1.0,
        101.0,
    )
    assert fill.slippage_application_count == 1


def test_entry_relative_stop_and_sizing_use_the_final_fill() -> None:
    transition = CorrectedEconomicsAdapter().resolve(
        EconomicState(sizing_equity=1000.0),
        EconomicIntent(
            kind=IntentKind.OPEN,
            action_side="BUY",
            position_side="LONG",
            reference_price=100.0,
            stop_percent=10.0,
            risk_pct=10.0,
            max_leverage_cap=10.0,
        ),
        MarketEvent(
            timestamp=datetime(2000, 1, 1, 0, 11, tzinfo=timezone.utc),
            bar_index=1,
            open=100.0,
            high=100.0,
            low=100.0,
            close=100.0,
        ),
        _records("RULE2-05-RED"),
    )

    assert transition.fill_decisions[0].final_fill_price == 101.0
    assert transition.next_position_facts.active_stop_price == 90.9


def test_funding_tick_emits_one_cash_row_and_one_equal_projection() -> None:
    records = EconomicRecords.from_record_paths(
        instrument_path=(
            RECORD_ROOT / "instruments" / "SYNTH-INSTRUMENT-RULE2-08-RED-V1.json"
        ),
        funding_path=RECORD_ROOT / "funding" / "SYNTH-FUNDING-RULE2-08-V1.json",
    )
    state = EconomicState(
        lifecycle_id=1,
        position_side="LONG",
        quantity=1.0,
        entry_fill_price=100.0,
        sizing_equity=1000.0,
        equity=1000.0,
    )
    intent = EconomicIntent(
        kind=IntentKind.FUNDING_TICK,
        funding_event_id="TEST-FUND-1",
    )
    market = MarketEvent(
        timestamp=datetime(2000, 1, 1, tzinfo=timezone.utc),
        bar_index=2,
        open=100.0,
        high=100.0,
        low=100.0,
        close=100.0,
    )

    transition = CorrectedEconomicsAdapter().resolve(state, intent, market, records)

    assert transition.cash_events[0].signed_delta == -0.1
    assert transition.funding_events[0].funding_cash_delta == -0.1
    assert transition.cash_events[0].cash_event_id == transition.funding_events[0].cash_event_id
    assert transition.funding_events[0].cumulative_funding == -0.1


@pytest.mark.parametrize(
    ("state", "event_id", "code"),
    [
        (_open_long_state(), "MISSING", REFUSED_MISSING_FUNDING_EVENT),
        (
            EconomicState(
                lifecycle_id=1,
                position_side="LONG",
                quantity=1.0,
                entry_fill_price=100.0,
                applied_funding_event_keys=frozenset({("TEST-FUND-1", 1)}),
            ),
            "TEST-FUND-1",
            REFUSED_DUPLICATE_FUNDING_EVENT,
        ),
    ],
)
def test_funding_refusal_families(
    state: EconomicState, event_id: str, code: str
) -> None:
    records = EconomicRecords.from_record_paths(
        instrument_path=(
            RECORD_ROOT / "instruments" / "SYNTH-INSTRUMENT-RULE2-08-RED-V1.json"
        ),
        funding_path=RECORD_ROOT / "funding" / "SYNTH-FUNDING-RULE2-08-V1.json",
    )
    with pytest.raises(EconomicsRefusal) as exc_info:
        CorrectedEconomicsAdapter().resolve(
            state,
            EconomicIntent(kind=IntentKind.FUNDING_TICK, funding_event_id=event_id),
            MarketEvent(
                timestamp=datetime(2000, 1, 1, tzinfo=timezone.utc),
                bar_index=2,
                open=100.0,
                high=100.0,
                low=100.0,
                close=100.0,
            ),
            records,
        )
    assert exc_info.value.refusal_code == code


def test_w276_f02_funding_duplicate_identity_includes_lifecycle_id() -> None:
    records = EconomicRecords.from_record_paths(
        instrument_path=(
            RECORD_ROOT / "instruments" / "SYNTH-INSTRUMENT-RULE2-08-RED-V1.json"
        ),
        funding_path=RECORD_ROOT / "funding" / "SYNTH-FUNDING-RULE2-08-V1.json",
    )
    state = EconomicState(
        lifecycle_id=2,
        position_side="LONG",
        quantity=1.0,
        entry_fill_price=100.0,
        applied_funding_event_keys=frozenset({("TEST-FUND-1", 1)}),
    )

    transition = CorrectedEconomicsAdapter().resolve(
        state,
        EconomicIntent(kind=IntentKind.FUNDING_TICK, funding_event_id="TEST-FUND-1"),
        MarketEvent(
            timestamp=datetime(2000, 1, 1, tzinfo=timezone.utc),
            bar_index=2,
            open=100.0,
            high=100.0,
            low=100.0,
            close=100.0,
        ),
        records,
    )

    assert transition.funding_events[0].lifecycle_id == 2


def test_fill_without_cost_schedule_is_refused() -> None:
    records = EconomicRecords.from_record_paths(
        instrument_path=(
            RECORD_ROOT / "instruments" / "SYNTH-INSTRUMENT-RULE2-08-RED-V1.json"
        ),
        funding_path=RECORD_ROOT / "funding" / "SYNTH-FUNDING-RULE2-08-V1.json",
    )
    with pytest.raises(EconomicsRefusal) as exc_info:
        CorrectedEconomicsAdapter().resolve(
            EconomicState(sizing_equity=1000.0),
            EconomicIntent(
                kind=IntentKind.OPEN,
                action_side="BUY",
                position_side="LONG",
                reference_price=100.0,
                requested_quantity=1.0,
            ),
            MarketEvent(
                timestamp=datetime(2000, 1, 1, tzinfo=timezone.utc),
                bar_index=0,
                open=100.0,
                high=100.0,
                low=100.0,
                close=100.0,
            ),
            records,
        )
    assert exc_info.value.refusal_code == REFUSED_MISSING_COST_SCHEDULE
