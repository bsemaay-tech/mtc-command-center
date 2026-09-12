"""WP-P0-12 Path D, decision B — the admitted reported-fee cost path.

D026 RED/GREEN for the ``economics.py`` fee branch under
``OD-20260912-P012-PATHD-1`` (B1=C admit reported + guarded estimator, B2=C 5%
relative, B3=B first authenticated fill, B4=A liquidation stays CANNOT_MAP).

Expected values are independent literals derived by hand from the record's own
declared rates and the intent's own arithmetic:

    notional  = 10 BTC x 60000 USDC x multiplier 1 = 600000 USDC
    estimate  = 600000 x taker_rate 0.00045        =    270.00 USDC
    tolerance = 5% of the estimate                 =     13.50 USDC

The admitted amount is never one of these: it is whatever the caller's venue
row reported, and the tests assert exactly that.

RED (pre-fix): every admitted-path case refuses with ``REFUSED_ECONOMIC_INPUT:
fee rounding rule is not executable`` because the pre-fix branch has only the
schedule path, and ``ReportedFillFee`` / ``REFUSED_MISSING_ADMITTED_FEE`` /
``FEE_ESTIMATOR_SUSPENDED`` do not exist.
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import pytest

from mtc_v2.core.economics import (
    ADMITTED_COST_SOURCE_REPORTED_PER_FILL_V1,
    ESTIMATOR_TOLERANCE_FORM,
    ESTIMATOR_TOLERANCE_RELATIVE,
    ESTIMATOR_DEVIATION_SIGNED_RISK_ID,
    GUARDED_ESTIMATOR_SCHEDULE_ID,
    REFUSED_BEFORE_ADMITTED_INTERVAL_START,
    REFUSED_ECONOMIC_INPUT,
    REFUSED_MISSING_ADMITTED_FEE,
    REFUSED_UNMAPPED_FILL_EVENT_CLASS,
    REFUSED_UNSPECIFIED_ADMITTED_INTERVAL_START,
    REFUSED_UNSUPPORTED_ADMITTED_COST_SOURCE,
    CorrectedEconomicsAdapter,
    EconomicIntent,
    EconomicRecords,
    EconomicState,
    EconomicsRefusal,
    IntentKind,
    MarketEvent,
    ReportedFillFee,
)
from mtc_v2.core.instrument import load_verified_json_record


MTC_V2_ROOT = Path(__file__).resolve().parents[4]
RECORD_ROOT = MTC_V2_ROOT / "core" / "economic_records"
COSTS = RECORD_ROOT / "costs"
INSTRUMENTS = RECORD_ROOT / "instruments"

# Hand-derived expectations (see module docstring).
NOTIONAL = 600000.0
ESTIMATE = 270.0
TOLERANCE = 13.5
INSIDE_TOLERANCE = 259.2  # 4% below the estimate
OUTSIDE_TOLERANCE = 243.0  # 10% below the estimate

MARKET = MarketEvent(
    timestamp=datetime(2026, 9, 12, 1, 0, tzinfo=timezone.utc),
    bar_index=1,
    open=60000.0,
    high=60000.0,
    low=60000.0,
    close=60000.0,
)
BEFORE_START = MarketEvent(
    timestamp=datetime(2026, 9, 11, 23, 0, tzinfo=timezone.utc),
    bar_index=0,
    open=60000.0,
    high=60000.0,
    low=60000.0,
    close=60000.0,
)


def _records(
    cost_id: str,
    instrument_id: str = "SYNTH-INSTRUMENT-QTYGUARD-01-GREEN-V1",
) -> EconomicRecords:
    return EconomicRecords.from_record_paths(
        instrument_path=INSTRUMENTS / f"{instrument_id}.json",
        cost_path=COSTS / f"{cost_id}.json",
        funding_path=RECORD_ROOT / "funding" / "SYNTH-FUNDING-PATHD-01-EMPTY-V1.json",
    )


def _intent(
    fees: tuple[ReportedFillFee, ...] = (),
    *,
    event_class: str = "ENTRY",
) -> EconomicIntent:
    return EconomicIntent(
        kind=IntentKind.OPEN,
        action_side="BUY",
        position_side="LONG",
        reference_price=60000.0,
        stop_price=50000.0,
        risk_pct=10.0,
        fallback_size_pct=10.0,
        max_leverage_cap=1.0,
        event_class=event_class,
        reported_fill_fees=fees,
    )


def _resolve(
    fees: tuple[ReportedFillFee, ...] = (),
    *,
    cost_id: str = "SYNTH-COST-ADMITTED-01-GREEN-V1",
    event_class: str = "ENTRY",
    market: MarketEvent = MARKET,
):
    return CorrectedEconomicsAdapter().resolve(
        EconomicState(sizing_equity=1_000_000.0),
        _intent(fees, event_class=event_class),
        market,
        _records(cost_id),
    )


def _decision(transition, name: str):
    rows = [row for row in transition.decision_events if row.decision == name]
    assert len(rows) == 1, [row.decision for row in transition.decision_events]
    return dict(rows[0].details)


# --------------------------------------------------------------------------
# GREEN: the admitted amount is the venue's own number
# --------------------------------------------------------------------------


def test_admitted_cost_is_the_reported_amount_not_the_schedule_estimate() -> None:
    reported = 199.99  # deliberately unlike 270.00
    transition = _resolve((ReportedFillFee("F0", reported, "TEST-USD"),))

    assert transition.fee_events[0].fee_amount == reported
    assert transition.fee_events[0].fee_cash_delta == -reported
    assert transition.cash_events[0].signed_delta == -reported
    assert transition.fee_events[0].fee_notional == NOTIONAL

    applied = _decision(transition, "ADMITTED_COST_APPLIED")
    assert applied["admitted_cost_source"] == ADMITTED_COST_SOURCE_REPORTED_PER_FILL_V1
    assert applied["reported_amount"] == reported
    assert applied["estimator_amount"] == pytest.approx(ESTIMATE)
    assert applied["estimator_schedule_id"] == GUARDED_ESTIMATOR_SCHEDULE_ID


def test_estimator_agrees_inside_the_owner_signed_tolerance() -> None:
    transition = _resolve((ReportedFillFee("F0", INSIDE_TOLERANCE, "TEST-USD"),))

    agreed = _decision(transition, "FEE_ESTIMATOR_AGREED")
    assert agreed["tolerance_form"] == ESTIMATOR_TOLERANCE_FORM
    assert agreed["tolerance_relative"] == ESTIMATOR_TOLERANCE_RELATIVE
    assert agreed["tolerance_absolute"] == pytest.approx(TOLERANCE)
    assert agreed["absolute_deviation"] == pytest.approx(ESTIMATE - INSIDE_TOLERANCE)
    assert transition.fee_events[0].fee_amount == INSIDE_TOLERANCE


def test_estimator_suspension_never_overrides_the_reported_amount() -> None:
    transition = _resolve((ReportedFillFee("F0", OUTSIDE_TOLERANCE, "TEST-USD"),))

    suspended = _decision(transition, "FEE_ESTIMATOR_SUSPENDED")
    assert suspended["signed_risk_id"] == ESTIMATOR_DEVIATION_SIGNED_RISK_ID
    assert suspended["estimator_suspended_for"] == "PRE_TRADE_SIZING"
    assert suspended["admitted_amount_overridden"] is False
    assert suspended["absolute_deviation"] == pytest.approx(ESTIMATE - OUTSIDE_TOLERANCE)
    # The admitted cash is still the venue's number, not the estimate.
    assert transition.fee_events[0].fee_amount == OUTSIDE_TOLERANCE
    assert transition.cash_events[0].signed_delta == -OUTSIDE_TOLERANCE
    assert [row.decision for row in transition.decision_events].count(
        "FEE_ESTIMATOR_AGREED"
    ) == 0


def test_a_declared_rebate_is_admitted_as_a_credit() -> None:
    transition = _resolve(
        (ReportedFillFee("F0", -5.0, "TEST-USD", fee_class="REBATE"),)
    )

    assert transition.fee_events[0].fee_amount == -5.0
    assert transition.cash_events[0].signed_delta == 5.0
    # A rebate is 275 away from a 270 estimate, so the estimator is suspended.
    assert _decision(transition, "FEE_ESTIMATOR_SUSPENDED")["reported_amount"] == -5.0


def test_closed_pnl_is_carried_beside_the_fee_never_merged_into_it() -> None:
    transition = _resolve(
        (ReportedFillFee("F0", 270.0, "TEST-USD", closed_pnl=-1234.5),)
    )

    assert _decision(transition, "ADMITTED_COST_APPLIED")["closed_pnl"] == -1234.5
    assert transition.fee_events[0].fee_amount == 270.0
    assert transition.cash_events[0].signed_delta == -270.0


# --------------------------------------------------------------------------
# Retained refusals (negative controls that must stay RED)
# --------------------------------------------------------------------------


def test_a_fill_without_a_reported_fee_is_refused_never_defaulted() -> None:
    with pytest.raises(EconomicsRefusal) as exc_info:
        _resolve(())

    assert exc_info.value.refusal_code == REFUSED_MISSING_ADMITTED_FEE
    assert "never defaulted, estimated or zeroed" in exc_info.value.detail


@pytest.mark.parametrize(
    ("fee", "reason"),
    [
        (ReportedFillFee("F0", float("nan"), "TEST-USD"), "not finite"),
        (ReportedFillFee("F0", float("inf"), "TEST-USD"), "not finite"),
        (ReportedFillFee("F0", None, "TEST-USD"), "not a number"),
        (ReportedFillFee("F0", -1.0, "TEST-USD"), "not declared a rebate"),
        (
            ReportedFillFee("F0", 1.0, "TEST-USD", fee_class="REBATE"),
            "declared a rebate but is positive",
        ),
        (ReportedFillFee("F0", 270.0, "USDC"), "not the settlement currency"),
        (
            ReportedFillFee("F0", 270.0, "TEST-USD", fee_class="FREE"),
            "unknown fee_class",
        ),
        (ReportedFillFee("F9", 270.0, "TEST-USD"), "no venue-reported fee"),
    ],
)
def test_unusable_reported_fees_refuse(fee: ReportedFillFee, reason: str) -> None:
    with pytest.raises(EconomicsRefusal) as exc_info:
        _resolve((fee,))

    assert exc_info.value.refusal_code == REFUSED_MISSING_ADMITTED_FEE
    assert reason in exc_info.value.detail


def test_two_reported_fees_for_one_fill_refuse() -> None:
    with pytest.raises(EconomicsRefusal) as exc_info:
        _resolve(
            (
                ReportedFillFee("F0", 270.0, "TEST-USD"),
                ReportedFillFee("F0", 271.0, "TEST-USD"),
            )
        )

    assert exc_info.value.refusal_code == REFUSED_MISSING_ADMITTED_FEE


def test_margin_call_liquidation_stays_cannot_map() -> None:
    with pytest.raises(EconomicsRefusal) as exc_info:
        _resolve(
            (ReportedFillFee("F0", 270.0, "TEST-USD"),),
            event_class="MARGIN_CALL_LIQUIDATION",
        )

    assert exc_info.value.refusal_code == REFUSED_UNMAPPED_FILL_EVENT_CLASS
    assert "CANNOT_MAP_NO_FROZEN_LIQUIDATION_FEE_SEMANTICS" in exc_info.value.detail


def test_unspecified_admitted_interval_start_refuses_every_computation() -> None:
    with pytest.raises(EconomicsRefusal) as exc_info:
        _resolve(
            (ReportedFillFee("F0", 270.0, "TEST-USD"),),
            cost_id="SYNTH-COST-ADMITTED-02-NOSTART-RED-V1",
        )

    assert exc_info.value.refusal_code == REFUSED_UNSPECIFIED_ADMITTED_INTERVAL_START
    assert "first authenticated own-account fill" in exc_info.value.detail


def test_a_fill_before_the_admitted_interval_start_refuses() -> None:
    with pytest.raises(EconomicsRefusal) as exc_info:
        _resolve((ReportedFillFee("F0", 270.0, "TEST-USD"),), market=BEFORE_START)

    assert exc_info.value.refusal_code == REFUSED_BEFORE_ADMITTED_INTERVAL_START


def test_an_unknown_admitted_cost_source_refuses() -> None:
    with pytest.raises(EconomicsRefusal) as exc_info:
        _resolve(
            (ReportedFillFee("F0", 270.0, "TEST-USD"),),
            cost_id="SYNTH-COST-ADMITTED-03-BADCLASS-RED-V1",
        )

    assert exc_info.value.refusal_code == REFUSED_UNSUPPORTED_ADMITTED_COST_SOURCE


def test_a_record_cannot_widen_the_owner_signed_tolerance() -> None:
    with pytest.raises(EconomicsRefusal) as exc_info:
        _resolve(
            (ReportedFillFee("F0", 270.0, "TEST-USD"),),
            cost_id="SYNTH-COST-ADMITTED-04-WIDETOL-RED-V1",
        )

    assert exc_info.value.refusal_code == REFUSED_UNSUPPORTED_ADMITTED_COST_SOURCE
    assert "owner-signed 0.05" in exc_info.value.detail


def test_the_schedule_path_is_unchanged_without_an_admitted_source() -> None:
    """A record with no admitted cost source still needs an executable rule."""
    records = EconomicRecords.from_record_paths(
        instrument_path=INSTRUMENTS / "SYNTH-INSTRUMENT-QTYGUARD-01-GREEN-V1.json",
        cost_path=COSTS / "HYPERLIQUID-BTC-PERP-BASE-TIER0-V1.json",
        funding_path=RECORD_ROOT / "funding" / "SYNTH-FUNDING-PATHD-01-EMPTY-V1.json",
    )
    intent = _intent(
        (ReportedFillFee("F0", 270.0, "USDC"),), event_class="MARKET_ENTRY"
    )

    with pytest.raises(EconomicsRefusal) as exc_info:
        CorrectedEconomicsAdapter().resolve(
            EconomicState(sizing_equity=1_000_000.0), intent, MARKET, records
        )

    assert exc_info.value.refusal_code == REFUSED_ECONOMIC_INPUT
    assert exc_info.value.detail == "fee rounding rule is not executable"


def test_the_production_v2_record_still_refuses_pending_the_declared_start() -> None:
    records = EconomicRecords.from_record_paths(
        instrument_path=INSTRUMENTS / "SYNTH-INSTRUMENT-QTYGUARD-01-GREEN-V1.json",
        cost_path=COSTS / "HYPERLIQUID-BTC-PERP-BASE-TIER0-V2.json",
        funding_path=RECORD_ROOT / "funding" / "SYNTH-FUNDING-PATHD-01-EMPTY-V1.json",
    )
    intent = _intent((ReportedFillFee("F0", 270.0, "USDC"),), event_class="MARKET_ENTRY")

    with pytest.raises(EconomicsRefusal) as exc_info:
        CorrectedEconomicsAdapter().resolve(
            EconomicState(sizing_equity=1_000_000.0), intent, MARKET, records
        )

    assert exc_info.value.refusal_code == REFUSED_UNSPECIFIED_ADMITTED_INTERVAL_START


# --------------------------------------------------------------------------
# B2: why the tolerance is 5% relative and not max(5%, 1e-6 USDC)
# --------------------------------------------------------------------------


def test_absolute_tolerance_floor_would_weaken_detection() -> None:
    """The packet's optional ``max(5%, 1e-6)`` floor is not adopted.

    The owner decision allows that variant only on a showing that it never
    weakens detection.  It does: this is a deviation of 90% of the estimate
    that the pure relative rule flags and the floored rule silently admits.
    """
    estimate = 1e-6
    reported = 1.9e-6
    deviation = abs(reported - estimate)

    relative_only = deviation > ESTIMATOR_TOLERANCE_RELATIVE * estimate
    with_absolute_floor = deviation > max(
        ESTIMATOR_TOLERANCE_RELATIVE * estimate, 1e-6
    )

    assert relative_only is True
    assert with_absolute_floor is False
    assert ESTIMATOR_TOLERANCE_RELATIVE == 0.05
    assert ESTIMATOR_TOLERANCE_FORM == "RELATIVE_FRACTION_OF_ESTIMATE_V1"


# --------------------------------------------------------------------------
# Record bytes
# --------------------------------------------------------------------------


def test_frozen_v1_cost_record_bytes_are_untouched() -> None:
    record = load_verified_json_record(COSTS / "HYPERLIQUID-BTC-PERP-BASE-TIER0-V1.json")

    assert record.digest == (
        "6ee6a34f0f1230973148e7392abdc11ec8409f06811d79fa6b65bcac104e3db5"
    )
    assert record.data["admission_status"] == "REFUSED_INCOMPLETE_COST_SCHEDULE"
    assert record.data["provenance"]["frozen_source_absence"]["disposition"] == (
        "KEEP_REFUSED"
    )
    assert "admitted_cost_source" not in record.data


def test_cost_record_v2_supersedes_only_the_admitted_path() -> None:
    path = COSTS / "HYPERLIQUID-BTC-PERP-BASE-TIER0-V2.json"
    record = load_verified_json_record(path)

    assert path.with_name(path.name + ".sha256").read_bytes() == (
        record.digest.encode("ascii") + b"\n"
    )
    data = record.data
    assert data["admitted_cost_source"] == ADMITTED_COST_SOURCE_REPORTED_PER_FILL_V1
    assert data["admission_status"] == "ADMITTED_HL_FEE_REPORTED_PER_FILL_V1"
    assert data["admitted_interval_start"] is None
    assert data["estimator_schedule_id"] == GUARDED_ESTIMATOR_SCHEDULE_ID
    assert data["estimator"]["tolerance_relative"] == ESTIMATOR_TOLERANCE_RELATIVE

    absence = data["provenance"]["frozen_source_absence"]
    assert absence["disposition"] == "SUPERSEDED_FOR_ADMITTED_COST_PATH_ONLY"
    assert absence["superseded_disposition"] == "KEEP_REFUSED"
    assert "HYPERLIQUID-BTC-PERP-BASE-TIER0-V1" in absence["supersession_scope"]

    # Retained, documented as not required for the admitted cost, never filled.
    assert data["refused_missing_fields"] == (
        "fee_rounding_rule",
        "fixed_component",
        "minimum_fee",
        "tier_account_selection_evidence",
    )
    assert "NOT REQUIRED FOR THE ADMITTED COST" in data["refused_missing_fields_disposition"]
    assert data["refused_event_classes"]["MARGIN_CALL_LIQUIDATION"].startswith(
        "CANNOT_MAP"
    )
    # The default-zero gate stays shut: none of these keys exists.
    for key in ("fee_rounding_rule", "fixed_component", "minimum_fee"):
        assert key not in data


def test_no_path_d_record_writes_the_identity_rounding_literal() -> None:
    forbidden = "EXACT_IDENTITY" + "_V1"
    path_d_records = [
        COSTS / "HYPERLIQUID-BTC-PERP-BASE-TIER0-V2.json",
        INSTRUMENTS / "HYPERLIQUID-BTC-PERP-V1.4.json",
        *sorted(COSTS.glob("SYNTH-COST-ADMITTED-*.json")),
        *sorted(INSTRUMENTS.glob("SYNTH-INSTRUMENT-QTYGUARD-*.json")),
    ]
    assert len(path_d_records) == 10

    for record_path in path_d_records:
        assert forbidden not in record_path.read_text(encoding="utf-8"), record_path
