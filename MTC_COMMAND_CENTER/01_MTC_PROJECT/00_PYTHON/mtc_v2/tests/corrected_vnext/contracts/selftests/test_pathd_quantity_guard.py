"""WP-P0-12 Path D, decision C — the owner quantity guard.

D026 RED/GREEN for the ``instrument.py`` minimum-quantity gate under
``OD-20260912-P012-PATHD-1`` (C1=A numeric guard + provenance marker, C2=B
K=10, C3=A floor-then-refuse).

Every expected number here is an independent literal: the sizing values are
hand-derived from the record's own declared step/notional and the intent's
risk arithmetic (``equity x risk% / stop distance``, floored to
``quantity_step``), never read back from a transition.

RED (pre-fix): ``HYPERLIQUID-BTC-PERP-V1.4.json`` and every
``SYNTH-INSTRUMENT-QTYGUARD-*`` record refuse with "minimum_quantity is
absent" because the pre-fix consumer has no marker contract; the unmarked and
wrong-marker controls are then indistinguishable from the marked one, and
``venue_minimum_quantity``/``min_qty_is_owner_guard`` do not exist at all.
"""

from __future__ import annotations

import hashlib
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
    ReportedFillFee,
)
from mtc_v2.core.instrument import (
    ADMITTED_MINIMUM_QUANTITY_PROVENANCE,
    MINIMUM_QUANTITY_OWNER_GUARD_V1,
    REFUSED_INCOMPLETE_INSTRUMENT_RECORD,
    REFUSED_MINIMUM_QUANTITY_NOT_A_VENUE_FACT,
    REFUSED_UNMARKED_MINIMUM_QUANTITY,
    VENUE_SOURCED_MINIMUM_QUANTITY_PROVENANCE,
    InstrumentRecordRefusal,
    load_verified_instrument_record,
    load_verified_json_record,
)


MTC_V2_ROOT = Path(__file__).resolve().parents[4]
RECORD_ROOT = MTC_V2_ROOT / "core" / "economic_records"
INSTRUMENTS = RECORD_ROOT / "instruments"

# Owner choice C2=B: K = 10 grid steps of 0.00001 BTC.
OWNER_GUARD_MINIMUM_QUANTITY = 0.0001
QUANTITY_STEP = 0.00001
MINIMUM_NOTIONAL = 10.0
GUARD_EVALUATION_TIME = "2026-09-12T01:00:00Z"


def _instrument(name: str):
    return load_verified_instrument_record(INSTRUMENTS / f"{name}.json")


def _records(instrument_name: str) -> EconomicRecords:
    return EconomicRecords.from_record_paths(
        instrument_path=INSTRUMENTS / f"{instrument_name}.json",
        cost_path=RECORD_ROOT / "costs" / "SYNTH-COST-ADMITTED-05-BOUND-GREEN-V1.json",
        funding_path=RECORD_ROOT / "funding" / "SYNTH-FUNDING-PATHD-01-EMPTY-V1.json",
    )


MARKET = MarketEvent(
    timestamp=datetime(2026, 9, 12, 1, 0, tzinfo=timezone.utc),
    bar_index=1,
    open=60000.0,
    high=60000.0,
    low=60000.0,
    close=60000.0,
)


def _open(equity: float) -> tuple[EconomicState, EconomicIntent]:
    fee_capture_bytes = (
        b'{"fill":"F0","fee":"270.0","synthetic":true,'
        b'"coin":"SYNTH-INSTRUMENT-QTYGUARD-01-GREEN-V1",'
        b'"time":1789174800000,"tid":7001,"feeToken":"TEST-USD"}'
    )
    return (
        EconomicState(sizing_equity=equity),
        EconomicIntent(
            kind=IntentKind.OPEN,
            action_side="BUY",
            position_side="LONG",
            reference_price=60000.0,
            stop_price=50000.0,
            risk_pct=10.0,
            fallback_size_pct=10.0,
            max_leverage_cap=1.0,
            event_class="ENTRY",
            # The admitted-cost path needs an authenticated own-account fill
            # fee; these bindings are labelled synthetic fixture values.
            reported_fill_fees=(
                ReportedFillFee(
                    "F0",
                    "270.0",
                    "TEST-USD",
                    source_class="HL_FEE_REPORTED_PER_FILL_V1",
                    account_scope="SYNTHETIC-DECLARED-ACCOUNT-0001",
                    product="SYNTHETIC-DECLARED-BTC-PERP",
                    capture_sha256=hashlib.sha256(fee_capture_bytes).hexdigest(),
                    capture_bytes=fee_capture_bytes,
                    native_fill_id="7001",
                    native_instrument="SYNTH-INSTRUMENT-QTYGUARD-01-GREEN-V1",
                ),
            ),
        ),
    )


def _decisions(transition) -> list[str]:
    return [row.decision for row in transition.decision_events]


# --------------------------------------------------------------------------
# The record versions themselves
# --------------------------------------------------------------------------


def test_frozen_v1_3_instrument_bytes_are_untouched() -> None:
    record = load_verified_json_record(INSTRUMENTS / "HYPERLIQUID-BTC-PERP-V1.3.json")

    assert record.digest == (
        "5abb99abbdb9735e95ad1084c706a3c5326fb6bb134e48a79e9bb0992b68316a"
    )
    assert record.data["minimum_quantity"] is None
    assert "minimum_quantity_provenance" not in record.data


def test_v1_4_carries_the_guard_and_keeps_open01_open() -> None:
    path = INSTRUMENTS / "HYPERLIQUID-BTC-PERP-V1.4.json"
    record = load_verified_json_record(path)

    assert path.with_name(path.name + ".sha256").read_bytes() == (
        record.digest.encode("ascii") + b"\n"
    )
    assert record.data["minimum_quantity"] == OWNER_GUARD_MINIMUM_QUANTITY
    assert record.data["minimum_quantity_provenance"] == (
        "HL_QTY_OWNER_GUARD_NOT_VENUE_FACT_V1"
    )
    assert record.data["open_items"] == ("OPEN01",)
    # The grid and the notional rule are untouched, and no notional rule is
    # converted into a BTC quantity.
    assert record.data["quantity_step"] == QUANTITY_STEP
    assert record.data["minimum_notional"] == MINIMUM_NOTIONAL
    assert record.data["minimum_quantity"] == 10 * QUANTITY_STEP
    # The record still does not claim the floor is absent, and no human record
    # review has happened for this version.
    assert record.data["provenance"]["human_reviewer"] is None
    minimum_gap = [
        gap for gap in record.data["gaps"] if gap["field"] == "minimum_quantity"
    ]
    assert len(minimum_gap) == 1
    assert "STILL A GAP" in minimum_gap[0]["status"]


# --------------------------------------------------------------------------
# RED -> GREEN on the consumer gate
# --------------------------------------------------------------------------


def test_null_minimum_quantity_is_still_refused() -> None:
    for name in (
        "HYPERLIQUID-BTC-PERP-V1.3",
        "SYNTH-INSTRUMENT-QTYGUARD-04-NULL-RED-V1",
    ):
        with pytest.raises(InstrumentRecordRefusal) as exc_info:
            _instrument(name).for_evaluation(GUARD_EVALUATION_TIME, {})
        assert exc_info.value.refusal_code == REFUSED_INCOMPLETE_INSTRUMENT_RECORD
        assert "minimum_quantity is absent" in str(exc_info.value)


def test_v1_4_clears_the_minimum_quantity_refusal_only() -> None:
    """GREEN: the minimum-quantity gate no longer refuses v1.4.

    The record still refuses, but on the *other* retained obligation, which is
    exactly what "OPEN01 stays open and final human review is still required"
    has to look like at the consumer.
    """
    with pytest.raises(InstrumentRecordRefusal) as exc_info:
        _instrument("HYPERLIQUID-BTC-PERP-V1.4").for_evaluation(
            "2026-08-31T07:00:53Z", {}
        )

    assert exc_info.value.refusal_code == REFUSED_INCOMPLETE_INSTRUMENT_RECORD
    assert "provenance.human_reviewer is absent" in str(exc_info.value)
    assert "minimum_quantity" not in str(exc_info.value)


def test_marked_guard_is_admitted() -> None:
    metadata = _instrument("SYNTH-INSTRUMENT-QTYGUARD-01-GREEN-V1").for_evaluation(
        GUARD_EVALUATION_TIME, {}
    )

    assert metadata.min_qty == OWNER_GUARD_MINIMUM_QUANTITY
    assert metadata.qty_step == QUANTITY_STEP
    assert metadata.min_notional == MINIMUM_NOTIONAL
    assert metadata.min_qty_provenance == MINIMUM_QUANTITY_OWNER_GUARD_V1
    assert metadata.min_qty_is_owner_guard is True


@pytest.mark.parametrize(
    "name",
    [
        "SYNTH-INSTRUMENT-QTYGUARD-02-NOMARKER-RED-V1",
        "SYNTH-INSTRUMENT-QTYGUARD-03-BADMARKER-RED-V1",
    ],
)
def test_unmarked_or_wrongly_marked_positive_floor_is_refused(name: str) -> None:
    with pytest.raises(InstrumentRecordRefusal) as exc_info:
        _instrument(name).for_evaluation(GUARD_EVALUATION_TIME, {})

    assert exc_info.value.refusal_code == REFUSED_UNMARKED_MINIMUM_QUANTITY


def test_zero_floor_records_keep_their_exact_behaviour() -> None:
    """The historical ``minimum_quantity: 0`` records are untouched."""
    metadata = _instrument("SYNTH-INSTRUMENT-RULE2-01-RED-V1").for_evaluation(
        "2000-01-01T00:10:00Z", {}
    )

    assert metadata.min_qty == 0.0
    assert metadata.min_qty_provenance is None
    assert metadata.min_qty_is_owner_guard is False


# --------------------------------------------------------------------------
# Negative control: nothing can report the guard as a venue fact
# --------------------------------------------------------------------------


def test_no_consumer_can_read_the_guard_as_a_venue_fact() -> None:
    assert VENUE_SOURCED_MINIMUM_QUANTITY_PROVENANCE == ()
    assert ADMITTED_MINIMUM_QUANTITY_PROVENANCE == (MINIMUM_QUANTITY_OWNER_GUARD_V1,)

    guarded = _instrument("SYNTH-INSTRUMENT-QTYGUARD-01-GREEN-V1").for_evaluation(
        GUARD_EVALUATION_TIME, {}
    )
    with pytest.raises(InstrumentRecordRefusal) as exc_info:
        guarded.venue_minimum_quantity()
    assert exc_info.value.refusal_code == REFUSED_MINIMUM_QUANTITY_NOT_A_VENUE_FACT
    assert "OPEN01 stays open" in str(exc_info.value)

    # The legacy unmarked zero is not a venue fact either.
    legacy = _instrument("SYNTH-INSTRUMENT-RULE2-01-RED-V1").for_evaluation(
        "2000-01-01T00:10:00Z", {}
    )
    with pytest.raises(InstrumentRecordRefusal) as exc_info:
        legacy.venue_minimum_quantity()
    assert exc_info.value.refusal_code == REFUSED_MINIMUM_QUANTITY_NOT_A_VENUE_FACT


def test_the_guard_surfaces_its_marker_in_the_sizing_trace() -> None:
    state, intent = _open(1_000_000.0)
    transition = CorrectedEconomicsAdapter().resolve(
        state, intent, MARKET, _records("SYNTH-INSTRUMENT-QTYGUARD-01-GREEN-V1")
    )

    admitted = [
        row
        for row in transition.decision_events
        if row.decision == "MINIMUM_QUANTITY_ADMITTED"
    ]
    assert len(admitted) == 1
    details = dict(admitted[0].details)
    assert details["required_minimum_quantity"] == OWNER_GUARD_MINIMUM_QUANTITY
    assert details["minimum_quantity_provenance"] == MINIMUM_QUANTITY_OWNER_GUARD_V1
    assert details["minimum_quantity_is_owner_guard"] is True


# --------------------------------------------------------------------------
# C3 = A: floor to the step, then the guard, then the notional rule
# --------------------------------------------------------------------------


def test_floor_then_refuse_below_the_guard() -> None:
    # equity 5 x 10% = 0.5 risk over a 10000 stop distance -> 0.00005 BTC,
    # already on the grid and below the 0.0001 guard.
    state, intent = _open(5.0)
    transition = CorrectedEconomicsAdapter().resolve(
        state, intent, MARKET, _records("SYNTH-INSTRUMENT-QTYGUARD-01-GREEN-V1")
    )

    assert _decisions(transition) == [
        "SEMANTICS_VALIDATED",
        "SIZING_COMPUTED",
        "REFUSED_MINIMUM_QUANTITY",
    ]
    refusal = transition.decision_events[-1]
    assert refusal.refusal_code == "REFUSED_MINIMUM_QUANTITY"
    assert dict(refusal.details)["floored_quantity"] == 0.00005
    assert transition.fill_decisions == ()
    assert transition.cash_events == ()
    assert transition.next_position_facts.quantity == 0.0


def test_size_is_floored_not_ceiled_or_rounded() -> None:
    # equity 15.9 x 10% / 10000 = 0.000159 BTC -> floor 0.00015, never 0.00016.
    state, intent = _open(15.9)
    transition = CorrectedEconomicsAdapter().resolve(
        state, intent, MARKET, _records("SYNTH-INSTRUMENT-QTYGUARD-01-GREEN-V1")
    )

    sizing = dict(transition.decision_events[2].details)
    assert transition.decision_events[2].decision == "MINIMUM_QUANTITY_ADMITTED"
    assert sizing["floored_quantity"] == 0.00015
    # 0.00015 x 60000 = 9.00 USDC, below the 10 USDC rule.
    assert _decisions(transition)[-1] == "REFUSED_MIN_NOTIONAL"
    assert dict(transition.decision_events[-1].details)["order_notional"] == 9.0


def test_the_guard_never_justifies_an_order_below_min_notional() -> None:
    # equity 10 x 10% / 10000 = 0.0001 BTC: exactly the guard, still only
    # 6.00 USDC of notional.
    state, intent = _open(10.0)
    transition = CorrectedEconomicsAdapter().resolve(
        state, intent, MARKET, _records("SYNTH-INSTRUMENT-QTYGUARD-01-GREEN-V1")
    )

    assert _decisions(transition) == [
        "SEMANTICS_VALIDATED",
        "SIZING_COMPUTED",
        "MINIMUM_QUANTITY_ADMITTED",
        "REFUSED_MIN_NOTIONAL",
    ]
    assert dict(transition.decision_events[-1].details) == {
        "order_notional": 6.0,
        "required_min_notional": MINIMUM_NOTIONAL,
    }
    assert transition.cash_events == ()


def test_an_admitted_size_above_both_floors_fills() -> None:
    # equity 1,000,000 x 10% / 10000 = 10 BTC, capped by leverage at 16.66 BTC.
    state, intent = _open(1_000_000.0)
    transition = CorrectedEconomicsAdapter().resolve(
        state, intent, MARKET, _records("SYNTH-INSTRUMENT-QTYGUARD-01-GREEN-V1")
    )

    assert _decisions(transition) == [
        "SEMANTICS_VALIDATED",
        "SIZING_COMPUTED",
        "MINIMUM_QUANTITY_ADMITTED",
        "MIN_NOTIONAL_ADMITTED",
        "ADMITTED_COST_APPLIED",
        "FEE_ESTIMATOR_AGREED",
    ]
    assert transition.fill_decisions[0].quantity == 10.0
    assert transition.fill_decisions[0].final_fill_price == 60000.0


def test_zero_floor_records_emit_no_minimum_quantity_decision() -> None:
    """The frozen decision stream of a ``min_qty == 0`` record is unchanged."""
    records = EconomicRecords.from_record_paths(
        instrument_path=INSTRUMENTS / "SYNTH-INSTRUMENT-RULE2-01-RED-V1.json",
        cost_path=RECORD_ROOT / "costs" / "SYNTH-COST-RULE2-01-RED-V1.json",
        funding_path=RECORD_ROOT / "funding" / "SYNTH-FUNDING-RULE2-01-RED-V1.json",
    )
    market = MarketEvent(
        timestamp=datetime(2000, 1, 1, 0, 11, tzinfo=timezone.utc),
        bar_index=1,
        open=100.0,
        high=100.0,
        low=100.0,
        close=100.0,
    )
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

    transition = CorrectedEconomicsAdapter().resolve(
        EconomicState(sizing_equity=1000.0), intent, market, records
    )

    assert _decisions(transition) == [
        "SEMANTICS_VALIDATED",
        "SIZING_COMPUTED",
        "MIN_NOTIONAL_ADMITTED",
    ]
    # The accepted 2.0.0 contract values for this frozen scenario.
    assert transition.fill_decisions[0].quantity == 5.0
    assert transition.cash_events[0].signed_delta == -0.45
