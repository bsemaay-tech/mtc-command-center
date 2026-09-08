from __future__ import annotations

import json
import subprocess
import sys
from copy import deepcopy
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
    ExitCandidate,
    IntentKind,
    MarketEvent,
    REFUSED_ECONOMIC_INPUT,
)
from mtc_v2.core.position_manager import PositionManager
from mtc_v2.core.runner import Runner
from mtc_v2.core.results import (
    CorrectedRunManifest,
    _closed_lifecycle_trades,
    corrected_surfaces,
)
from mtc_v2.core.types import (
    Bar,
    CashEvent,
    CashEventKind,
    DecisionEvent,
    EconomicTransition,
    EconomicTransitionError,
    EntryLeg,
    FeeEvent,
    FillDecision,
    FundingEvent,
    PortfolioState,
    Position,
    PositionFacts,
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


def _fill(
    *,
    event_class: str,
    quantity: float,
    exit_id: str | None = None,
    sequence: int = 0,
    fill_id: str = "F0",
) -> FillDecision:
    return FillDecision(
        sequence=sequence,
        event_timestamp=NOW,
        lifecycle_id=1,
        fill_id=fill_id,
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
        price_tick_alignment="CEIL" if event_class == "ENTRY" else "FLOOR",
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
                sequence=1,
                fill_id="F1",
            ),
        ],
        cash_events=[
            CashEvent(
                sequence=0,
                cash_event_id="CE-GROSS-1",
                event_timestamp=NOW,
                lifecycle_id=1,
                kind=CashEventKind.GROSS_REALIZATION,
                signed_delta=0.0,
                settlement_currency="TEST-USD",
                fill_id="F1",
            )
        ],
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


def test_w279b_f11_equal_empty_transition_keys_are_process_stable() -> None:
    script = """
import json
from datetime import datetime, timezone

from mtc_v2.core.position_manager import PositionManager
from mtc_v2.core.types import Bar, EconomicTransition, PortfolioState, PositionFacts

now = datetime(2000, 1, 1, tzinfo=timezone.utc)
transition = EconomicTransition(
    semantics_id="2.0.0",
    instrument_record_id="I",
    instrument_record_digest="0" * 64,
    funding_schedule_id="F",
    funding_schedule_digest="1" * 64,
    next_position_facts=PositionFacts(1, "LONG", 1.0, 100.0),
)
state = PortfolioState()
manager = PositionManager(
    enable_long=True,
    enable_short=True,
    regime_lock=False,
    max_entries=1,
    cooldown_bars=0,
    contract_multiplier=1.0,
)
manager.apply_transition(
    bar=Bar(now, 100.0, 100.0, 100.0, 100.0, 1.0, 7),
    state=state,
    transition=transition,
)
print(json.dumps(next(iter(state.applied_transition_keys)), separators=(",", ":")))
"""
    runs = [
        subprocess.run(
            [sys.executable, "-c", script],
            cwd=MTC_V2_ROOT.parent,
            capture_output=True,
            text=True,
            check=False,
        )
        for _ in range(2)
    ]
    assert [run.returncode for run in runs] == [0, 0], "\n".join(
        run.stderr for run in runs
    )
    assert runs[0].stdout.encode("utf-8") == runs[1].stdout.encode("utf-8")

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
    with pytest.raises(EconomicTransitionError, match="transition already applied"):
        manager.apply_transition(bar=_bar(), state=state, transition=second)
    assert len(state.applied_transition_keys) == 1


def test_w279_f20_unknown_positive_rate_payer_is_a_typed_refusal() -> None:
    records = EconomicRecords.from_record_paths(
        instrument_path=(
            RECORD_ROOT
            / "instruments"
            / "SYNTH-INSTRUMENT-RULE2-08-RED-V1.json"
        ),
        funding_path=(
            RECORD_ROOT / "funding" / "SYNTH-FUNDING-RULE2-08-V1.json"
        ),
    )
    funding_event = dict(records.funding["events"][0])
    funding_event["positive_rate_payer"] = "TYPO"
    funding = dict(records.funding)
    funding["events"] = (funding_event,)
    modified_records = replace(records, funding=funding)

    with pytest.raises(EconomicsRefusal) as exc_info:
        CorrectedEconomicsAdapter().resolve(
            EconomicState(
                lifecycle_id=1,
                position_side="LONG",
                quantity=1.0,
                entry_fill_price=100.0,
            ),
            EconomicIntent(
                kind=IntentKind.FUNDING_TICK,
                funding_event_id="TEST-FUND-1",
            ),
            MarketEvent(NOW, 1, 100.0, 100.0, 100.0, 100.0),
            modified_records,
        )

    assert exc_info.value.refusal_code == REFUSED_ECONOMIC_INPUT
    assert "positive_rate_payer" in str(exc_info.value)


def test_w279_f21_trade_exit_ids_use_the_exit_surface_source_set() -> None:
    records = _records("RULE2-07-RED")
    state = PortfolioState(
        initial_capital=1000.0,
        equity=1000.0,
        fill_events=[
            _fill(event_class="ENTRY", quantity=1.0),
            _fill(
                event_class="MARKET_EXIT",
                quantity=1.0,
                exit_id="UNJOINED-EXIT",
                sequence=1,
                fill_id="F1",
            ),
        ],
    )

    with pytest.raises(ValueError, match="exit gross-cash join mismatch"):
        corrected_surfaces(
            state=state,
            equity_values=[],
            manifest=CorrectedRunManifest.from_records(
                records,
                execution_profile_id="close_only_deterministic_v2",
            ),
        )


def test_w279_f17_state_writer_emits_closed_override_refusal_members() -> None:
    records = _records("RULE2-03-RED")
    state = PortfolioState(
        initial_capital=1000.0,
        equity=1000.0,
        decision_events=[
            DecisionEvent(
                sequence=0,
                event_timestamp=NOW,
                decision="REFUSED_INSTRUMENT_OVERRIDE_ON_EVALUATION",
                refusal_code="REFUSED_INSTRUMENT_OVERRIDE_ON_EVALUATION",
                details=(
                    ("field", "price_tick"),
                    ("record_value", 0.5),
                    ("runtime_value", 0.25),
                ),
            )
        ],
    )

    refusal = corrected_surfaces(
        state=state,
        equity_values=[],
        manifest=CorrectedRunManifest.from_records(
            records,
            execution_profile_id="close_only_deterministic_v2",
        ),
    )["RESULT_SURFACE"]["refusals"]

    assert refusal == [
        {
            "code": "REFUSED_INSTRUMENT_OVERRIDE_ON_EVALUATION",
            "field": "price_tick",
            "record_value": 0.5,
            "runtime_value": 0.25,
            "stage": "PRE_EVALUATION",
        }
    ]


def test_v283r2_d1_first_bar_default_funding_window_does_not_repeat_strictly_earlier() -> None:
    document = json.loads(
        (
            MTC_V2_ROOT
            / "tests/corrected_vnext/contracts/inputs/RULE2-08-RED.json"
        ).read_text(encoding="utf-8")
    )
    legacy = document["legacy_arm"]
    corrected = document["corrected_only"]
    config = {
        **legacy["config"],
        **corrected["records"],
        "kernel_semantics_version": "2.0.0",
        "same_bar_collision_policy_id": "STOP_FIRST",
        "slippage_model_id": "BPS_OF_REFERENCE_V1",
    }
    runner = Runner(config)
    runner.state.position = Position(
        side="long",
        entry_price=100.0,
        avg_entry_price=100.0,
        qty=1.0,
        entry_bar=0,
        initial_qty=1.0,
        entry_legs=[EntryLeg(100.0, 1.0, 0)],
        lifecycle_id=1,
    )
    assert runner._corrected_records is not None
    template = dict(runner._corrected_records.funding["events"][0])
    strictly_earlier = {
        **template,
        "funding_event_id": "STRICTLY-EARLIER",
        "event_timestamp": "1999-12-31T23:59:00Z",
    }
    same_timestamp = {
        **template,
        "funding_event_id": "SAME-TIMESTAMP",
        "event_timestamp": "2000-01-01T00:00:00Z",
    }
    runner._corrected_records = replace(
        runner._corrected_records,
        funding={
            **runner._corrected_records.funding,
            "events": (strictly_earlier, same_timestamp),
        },
    )
    first_bar = Bar(NOW, 100.0, 100.0, 100.0, 100.0, 0.0, 0)

    runner.run([first_bar])

    funding_decisions = [
        row
        for row in runner.state.decision_events
        if row.decision == "FUNDING_ELIGIBILITY"
    ]
    assert [
        (
            dict(row.details)["funding_event_id"],
            dict(row.details)["eligible"],
        )
        for row in funding_decisions
    ] == [("STRICTLY-EARLIER", False), ("SAME-TIMESTAMP", True)]
    assert [row.funding_event_id for row in runner.state.funding_events] == [
        "SAME-TIMESTAMP"
    ]


def _d026_funding_row(
    *,
    sequence: int,
    funding_event_id: str,
    lifecycle_id: int,
) -> tuple[CashEvent, FundingEvent]:
    cash = CashEvent(
        sequence=sequence,
        cash_event_id=f"CE-FUND-{sequence}",
        event_timestamp=NOW,
        lifecycle_id=lifecycle_id,
        kind=CashEventKind.FUNDING,
        signed_delta=-0.1,
        settlement_currency="TEST-USD",
        funding_event_id=funding_event_id,
    )
    row = FundingEvent(
        sequence=sequence,
        funding_event_id=funding_event_id,
        event_timestamp=NOW,
        lifecycle_id=lifecycle_id,
        position_side="LONG",
        open_qty=1.0,
        contract_multiplier=1.0,
        oracle_price=100.0,
        raw_rate=0.001,
        positive_rate_payer="LONG",
        long_cashflow_rate=-0.001,
        notional=100.0,
        funding_cash_delta=-0.1,
        cumulative_funding=-0.1,
        schedule_id="F",
        schedule_digest="1" * 64,
        source_event_digest="3" * 64,
        cash_event_id=cash.cash_event_id,
    )
    return cash, row


def test_d026_funding_row_order_puts_lifecycle_after_utf8_event_id() -> None:
    cash_a, row_a = _d026_funding_row(
        sequence=0, funding_event_id="SAME-EVENT", lifecycle_id=1
    )
    cash_b, row_b = _d026_funding_row(
        sequence=1, funding_event_id="SAME-EVENT", lifecycle_id=2
    )
    transition = EconomicTransition(
        semantics_id="2.0.0",
        instrument_record_id="I",
        instrument_record_digest="0" * 64,
        funding_schedule_id="F",
        funding_schedule_digest="1" * 64,
        next_position_facts=PositionFacts(None, None, 0.0),
        cash_events=(cash_a, cash_b),
        funding_events=(row_a, row_b),
    )
    assert transition.funding_events == (row_a, row_b)

    with pytest.raises(
        EconomicTransitionError, match="funding rows are not in event order"
    ):
        reverse_cash_a, reverse_row_a = _d026_funding_row(
            sequence=0, funding_event_id="SAME-EVENT", lifecycle_id=2
        )
        reverse_cash_b, reverse_row_b = _d026_funding_row(
            sequence=1, funding_event_id="SAME-EVENT", lifecycle_id=1
        )
        EconomicTransition(
            semantics_id="2.0.0",
            instrument_record_id="I",
            instrument_record_digest="0" * 64,
            funding_schedule_id="F",
            funding_schedule_digest="1" * 64,
            next_position_facts=PositionFacts(None, None, 0.0),
            cash_events=(reverse_cash_a, reverse_cash_b),
            funding_events=(reverse_row_a, reverse_row_b),
        )


def test_d026_empty_state_surfaces_accept_empty_event_collections() -> None:
    records = _records("RULE2-07-GREEN")
    state = PortfolioState(
        initial_capital=1000.0,
        equity=1000.0,
    )
    surfaces = corrected_surfaces(
        state=state,
        equity_values=[],
        manifest=CorrectedRunManifest.from_records(
            records,
            execution_profile_id="close_only_deterministic_v2",
        ),
    )
    assert surfaces["EVENT_SURFACE"]["funding_events"] == []
    assert surfaces["EVENT_SURFACE"]["cash_events"] == []
    assert surfaces["EVENT_SURFACE"]["exit_events"] == []


def test_d026_exit_foreign_fee_fill_refuses_before_any_state_mutation() -> None:
    transition = EconomicTransition(
        semantics_id="2.0.0",
        instrument_record_id="I",
        instrument_record_digest="0" * 64,
        funding_schedule_id="F",
        funding_schedule_digest="1" * 64,
        cost_schedule_id="COST",
        cost_schedule_digest="2" * 64,
        next_position_facts=PositionFacts(None, None, 0.0),
        fill_decisions=(
            _fill(event_class="MARKET_EXIT", quantity=1.0, exit_id="EXIT-ONLY"),
        ),
        cash_events=(
            CashEvent(
                sequence=0,
                cash_event_id="CE-GROSS-0",
                event_timestamp=NOW,
                lifecycle_id=1,
                kind=CashEventKind.GROSS_REALIZATION,
                signed_delta=5.0,
                settlement_currency="TEST-USD",
                fill_id="F0",
            ),
            CashEvent(
                sequence=1,
                cash_event_id="CE-FEE-9",
                event_timestamp=NOW,
                lifecycle_id=1,
                kind=CashEventKind.FEE,
                signed_delta=-0.7,
                settlement_currency="TEST-USD",
                fill_id="F9",
            ),
        ),
        fee_events=(
            FeeEvent(
                sequence=0,
                event_timestamp=NOW,
                lifecycle_id=1,
                fill_id="F9",
                event_class="MARKET_EXIT",
                liquidity_role="TAKER",
                schedule_id="COST",
                schedule_digest="2" * 64,
                rate=0.0005,
                fixed_component=0.2,
                fee_notional=100.0,
                fee_amount=0.7,
                fee_cash_delta=-0.7,
                settlement_currency="TEST-USD",
                cash_event_id="CE-FEE-9",
            ),
        ),
    )
    position = Position(
        side="long", entry_price=100.0, avg_entry_price=100.0, qty=1.0,
        entry_bar=0, initial_qty=1.0, entry_legs=[EntryLeg(100.0, 1.0, 0)],
        lifecycle_id=1,
    )
    state = PortfolioState(position=position, equity=1000.0, initial_capital=1000.0)
    snapshot = deepcopy(state)

    with pytest.raises(EconomicTransitionError, match="fee fill join mismatch"):
        _manager().apply_transition(
            bar=_bar(), state=state, transition=transition, reason="time_stop"
        )

    assert state == snapshot
