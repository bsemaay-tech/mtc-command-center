from __future__ import annotations

from dataclasses import FrozenInstanceError, replace
from datetime import datetime, timezone

import pytest

from mtc_v2.core.types import (
    CashEvent,
    CashEventKind,
    EconomicTransition,
    EconomicTransitionError,
    FeeEvent,
    FundingEvent,
    PositionFacts,
)


def _cash(
    kind: CashEventKind,
    cash_event_id: str,
    signed_delta: float,
    *,
    sequence: int = 0,
    fill_id: str | None = None,
    funding_event_id: str | None = None,
) -> CashEvent:
    return CashEvent(
        sequence=sequence,
        cash_event_id=cash_event_id,
        event_timestamp=datetime(2000, 1, 1, tzinfo=timezone.utc),
        lifecycle_id=1,
        kind=kind,
        signed_delta=signed_delta,
        settlement_currency="TEST-USD",
        fill_id=fill_id,
        funding_event_id=funding_event_id,
    )


def _transition(**overrides: object) -> EconomicTransition:
    values: dict[str, object] = {
        "semantics_id": "2.0.0",
        "instrument_record_id": "I",
        "instrument_record_digest": "0" * 64,
        "cost_schedule_id": "COST",
        "cost_schedule_digest": "2" * 64,
        "funding_schedule_id": "F",
        "funding_schedule_digest": "1" * 64,
        "next_position_facts": PositionFacts(lifecycle_id=1, side="LONG", quantity=1.0),
    }
    values.update(overrides)
    return EconomicTransition(**values)


def test_fee_and_funding_rows_are_one_to_one_cash_ledger_projections() -> None:
    fee_cash = _cash(
        CashEventKind.FEE, "CE-FEE", -0.1, fill_id="FILL-1"
    )
    funding_cash = _cash(
        CashEventKind.FUNDING,
        "CE-FUND",
        -0.2,
        sequence=1,
        funding_event_id="TEST-FUND-1",
    )
    transition = _transition(
        cash_events=(fee_cash, funding_cash),
        fee_events=(
            FeeEvent(
                sequence=0,
                event_timestamp=fee_cash.event_timestamp,
                lifecycle_id=1,
                fill_id="FILL-1",
                event_class="ENTRY",
                liquidity_role="TAKER",
                schedule_id="COST",
                schedule_digest="2" * 64,
                rate=0.001,
                fixed_component=0.0,
                fee_notional=100.0,
                fee_amount=0.1,
                fee_cash_delta=-0.1,
                settlement_currency="TEST-USD",
                cash_event_id=fee_cash.cash_event_id,
            ),
        ),
        funding_events=(
            FundingEvent(
                sequence=0,
                funding_event_id="TEST-FUND-1",
                event_timestamp=funding_cash.event_timestamp,
                lifecycle_id=1,
                position_side="LONG",
                open_qty=1.0,
                contract_multiplier=1.0,
                mark_price=100.0,
                raw_rate=0.001,
                positive_rate_payer="LONG",
                long_cashflow_rate=-0.001,
                notional=100.0,
                funding_cash_delta=-0.2,
                cumulative_funding=-0.2,
                schedule_id="F",
                schedule_digest="1" * 64,
                source_event_digest="3" * 64,
                cash_event_id=funding_cash.cash_event_id,
            ),
        ),
    )

    assert transition.cash_events == (fee_cash, funding_cash)


@pytest.mark.parametrize(
    "overrides",
    [
        {"cash_events": (_cash(CashEventKind.FEE, "CE", -0.1),)},
        {
            "cash_events": (_cash(CashEventKind.FEE, "CE", -0.1),),
            "fee_events": (
                FeeEvent(
                    sequence=0,
                    event_timestamp=datetime(2000, 1, 1, tzinfo=timezone.utc),
                    lifecycle_id=1,
                    fill_id="FILL-1",
                    event_class="ENTRY",
                    liquidity_role="TAKER",
                    schedule_id="COST",
                    schedule_digest="2" * 64,
                    rate=0.001,
                    fixed_component=0.0,
                    fee_notional=100.0,
                    fee_amount=0.1,
                    fee_cash_delta=-0.2,
                    settlement_currency="TEST-USD",
                    cash_event_id="CE",
                ),
            ),
        },
        {
            "cash_events": (
                _cash(CashEventKind.GROSS_REALIZATION, "CE", 1.0),
                _cash(CashEventKind.FEE, "CE", -0.1),
            )
        },
    ],
)
def test_invalid_cash_ledger_joins_are_refused(overrides: dict[str, object]) -> None:
    with pytest.raises(EconomicTransitionError):
        _transition(**overrides)


def test_transition_and_nested_rows_are_immutable() -> None:
    transition = _transition()

    with pytest.raises(FrozenInstanceError):
        transition.semantics_id = "1.0.0"  # type: ignore[misc]

    with pytest.raises(FrozenInstanceError):
        transition.next_position_facts.quantity = 2.0  # type: ignore[union-attr,misc]


def _fee_event(
    cash_event_id: str,
    *,
    fill_id: str = "FILL-1",
    fee_cash_delta: float = -0.1,
    sequence: int = 0,
) -> FeeEvent:
    return FeeEvent(
        sequence=sequence,
        event_timestamp=datetime(2000, 1, 1, tzinfo=timezone.utc),
        lifecycle_id=1,
        fill_id=fill_id,
        event_class="ENTRY",
        liquidity_role="TAKER",
        schedule_id="COST",
        schedule_digest="2" * 64,
        rate=0.001,
        fixed_component=0.0,
        fee_notional=100.0,
        fee_amount=0.1,
        fee_cash_delta=fee_cash_delta,
        settlement_currency="TEST-USD",
        cash_event_id=cash_event_id,
    )


def _funding_event(
    cash_event_id: str,
    *,
    funding_event_id: str = "TEST-FUND-1",
    lifecycle_id: int = 1,
    event_timestamp: datetime | None = None,
    sequence: int = 0,
    source_event_digest: str = "3" * 64,
) -> FundingEvent:
    return FundingEvent(
        sequence=sequence,
        funding_event_id=funding_event_id,
        event_timestamp=event_timestamp or datetime(2000, 1, 1, tzinfo=timezone.utc),
        lifecycle_id=lifecycle_id,
        position_side="LONG",
        open_qty=1.0,
        contract_multiplier=1.0,
        mark_price=100.0,
        raw_rate=0.001,
        positive_rate_payer="LONG",
        long_cashflow_rate=-0.001,
        notional=100.0,
        funding_cash_delta=-0.2,
        cumulative_funding=-0.2,
        schedule_id="F",
        schedule_digest="1" * 64,
        source_event_digest=source_event_digest,
        cash_event_id=cash_event_id,
    )


def _funding_pair(
    *,
    first: FundingEvent,
    second: FundingEvent,
) -> dict[str, object]:
    cash_rows = (
        _cash(
            CashEventKind.FUNDING,
            first.cash_event_id,
            first.funding_cash_delta,
            funding_event_id=first.funding_event_id,
        ),
        _cash(
            CashEventKind.FUNDING,
            second.cash_event_id,
            second.funding_cash_delta,
            sequence=1,
            funding_event_id=second.funding_event_id,
        ),
    )
    return {
        "cash_events": cash_rows,
        "funding_events": (first, second),
    }


def test_d026_projection_kind_guard_discriminates_a_gross_cash_join() -> None:
    gross_cash = _cash(
        CashEventKind.GROSS_REALIZATION, "CE-GROSS", -0.1, fill_id="FILL-1"
    )
    with pytest.raises(
        EconomicTransitionError, match="projection kind or join mismatch"
    ):
        _transition(
            cash_events=(gross_cash,),
            fee_events=(_fee_event(gross_cash.cash_event_id),),
        )


def test_d026_projection_delta_guard_discriminates_unequal_cash() -> None:
    fee_cash = _cash(CashEventKind.FEE, "CE-FEE", -0.1, fill_id="FILL-1")
    with pytest.raises(EconomicTransitionError, match="projection delta mismatch"):
        _transition(
            cash_events=(fee_cash,),
            fee_events=(
                _fee_event(fee_cash.cash_event_id, fee_cash_delta=-0.2),
            ),
        )


def test_d026_fee_schedule_identity_guard_discriminates_foreign_id() -> None:
    fee_cash = _cash(CashEventKind.FEE, "CE-FEE", -0.1, fill_id="FILL-1")
    with pytest.raises(EconomicTransitionError, match="cost schedule identity mismatch"):
        _transition(
            cash_events=(fee_cash,),
            fee_events=(
                replace(_fee_event(fee_cash.cash_event_id), schedule_id="OTHER-COST"),
            ),
        )


def test_d026_funding_schedule_identity_guard_discriminates_foreign_id() -> None:
    funding_cash = _cash(
        CashEventKind.FUNDING,
        "CE-FUND",
        -0.2,
        funding_event_id="TEST-FUND-1",
    )
    with pytest.raises(
        EconomicTransitionError, match="funding schedule identity mismatch"
    ):
        _transition(
            cash_events=(funding_cash,),
            funding_events=(
                replace(
                    _funding_event(funding_cash.cash_event_id),
                    schedule_id="OTHER-FUNDING",
                ),
            ),
        )


def test_d026_duplicate_cash_event_id_refuses_before_any_map_is_built() -> None:
    with pytest.raises(
        EconomicTransitionError, match="duplicate cash_event_id"
    ):
        _transition(
            cash_events=(
                _cash(CashEventKind.FEE, "CE-DUP", -0.1, fill_id="F0"),
                _cash(CashEventKind.FEE, "CE-DUP", -0.2, sequence=1, fill_id="F1"),
            ),
            fee_events=(
                _fee_event("CE-DUP", fill_id="F0", fee_cash_delta=-0.1),
                _fee_event("CE-DUP", fill_id="F1", fee_cash_delta=-0.2, sequence=1),
            ),
        )


def test_d026_duplicate_funding_key_refuses_before_projection_join() -> None:
    first = _funding_event("CE-FUND-0")
    second = _funding_event(
        "CE-FUND-1", sequence=1
    )
    with pytest.raises(
        EconomicTransitionError, match="duplicate funding event key"
    ):
        _transition(**_funding_pair(first=first, second=second))


def test_d026_fee_cash_row_requires_fill_id() -> None:
    fee_cash = _cash(CashEventKind.FEE, "CE-FEE", -0.1)
    with pytest.raises(
        EconomicTransitionError, match="fee cash row requires fill_id"
    ):
        _transition(
            cash_events=(fee_cash,),
            fee_events=(_fee_event(fee_cash.cash_event_id),),
        )


def test_d026_fee_cash_fill_id_mismatch_refuses() -> None:
    fee_cash = _cash(CashEventKind.FEE, "CE-FEE", -0.1, fill_id="F-OTHER")
    with pytest.raises(
        EconomicTransitionError, match="fee cash fill_id mismatch"
    ):
        _transition(
            cash_events=(fee_cash,),
            fee_events=(_fee_event(fee_cash.cash_event_id, fill_id="FILL-1"),),
        )


def test_d026_funding_cash_row_requires_funding_event_id() -> None:
    funding_cash = _cash(CashEventKind.FUNDING, "CE-FUND", -0.2)
    with pytest.raises(
        EconomicTransitionError,
        match="funding cash row requires funding_event_id",
    ):
        _transition(
            cash_events=(funding_cash,),
            funding_events=(_funding_event(funding_cash.cash_event_id),),
        )


def test_d026_funding_cash_funding_event_id_mismatch_refuses() -> None:
    funding_cash = _cash(
        CashEventKind.FUNDING,
        "CE-FUND",
        -0.2,
        funding_event_id="OTHER-EVENT",
    )
    with pytest.raises(
        EconomicTransitionError,
        match="funding cash funding_event_id mismatch",
    ):
        _transition(
            cash_events=(funding_cash,),
            funding_events=(_funding_event(funding_cash.cash_event_id),),
        )


def test_d026_gross_cash_row_requires_fill_id() -> None:
    with pytest.raises(
        EconomicTransitionError, match="gross cash row requires fill_id"
    ):
        _transition(cash_events=(_cash(CashEventKind.GROSS_REALIZATION, "CE-G", 1.0),))


def test_d026_funding_rows_order_by_timestamp_then_utf8_event_id() -> None:
    out_of_order = _funding_pair(
        first=_funding_event(
            "CE-FUND-1",
            funding_event_id="B-EVENT",
            sequence=0,
            event_timestamp=datetime(2000, 1, 1, 0, 30, tzinfo=timezone.utc),
        ),
        second=_funding_event(
            "CE-FUND-0",
            funding_event_id="A-EVENT",
            sequence=1,
            event_timestamp=datetime(1999, 12, 31, 23, 59, tzinfo=timezone.utc),
        ),
    )
    with pytest.raises(
        EconomicTransitionError, match="funding rows are not in event order"
    ):
        _transition(**out_of_order)
    earlier = _funding_event(
        "CE-FUND-0",
        funding_event_id="A-EVENT",
        event_timestamp=datetime(1999, 12, 31, 23, 59, tzinfo=timezone.utc),
    )
    later = _funding_event(
        "CE-FUND-1",
        funding_event_id="B-EVENT",
        sequence=1,
        event_timestamp=datetime(2000, 1, 1, 0, 30, tzinfo=timezone.utc),
    )
    in_order = _funding_pair(first=earlier, second=later)
    assert _transition(**in_order).funding_events == (earlier, later)


def test_d026_funding_rows_order_equal_timestamps_by_utf8_bytes_of_event_id() -> None:
    with pytest.raises(
        EconomicTransitionError, match="funding rows are not in event order"
    ):
        _transition(
            **_funding_pair(
                first=_funding_event(
                    "CE-FUND-1", funding_event_id="B-EVENT", sequence=0
                ),
                second=_funding_event(
                    "CE-FUND-0", funding_event_id="A-EVENT", sequence=1
                ),
            )
        )
    a_row = _funding_event("CE-FUND-0", funding_event_id="A-EVENT")
    b_row = _funding_event("CE-FUND-1", funding_event_id="B-EVENT", sequence=1)
    in_order = _transition(**_funding_pair(first=a_row, second=b_row))
    assert in_order.funding_events == (a_row, b_row)


def test_d026_funding_rows_mixed_tz_awareness_refuse_order_check() -> None:
    naive = _funding_event(
        "CE-FUND-1",
        funding_event_id="B-EVENT",
        sequence=1,
        event_timestamp=datetime(2000, 1, 1),
    )
    aware = _funding_event("CE-FUND-0", funding_event_id="A-EVENT")
    with pytest.raises(
        EconomicTransitionError, match="funding rows are not in event order"
    ):
        _transition(**_funding_pair(first=aware, second=naive))


def test_d026_funding_source_event_digest_requires_lowercase_64_hex() -> None:
    funding_cash = _cash(
        CashEventKind.FUNDING, "CE-FUND", -0.2, funding_event_id="TEST-FUND-1"
    )
    for digest in (
        None,
        "",
        "   ",
        "A" * 64,
        "a" * 63,
        "g" * 64,
        "3" * 63 + "G",
    ):
        with pytest.raises(
            EconomicTransitionError, match="lowercase 64-hex"
        ):
            _transition(
                cash_events=(funding_cash,),
                funding_events=(
                    _funding_event(
                        funding_cash.cash_event_id, source_event_digest=digest
                    ),
                ),
            )
    valid = _transition(
        cash_events=(funding_cash,),
        funding_events=(_funding_event(funding_cash.cash_event_id),),
    )
    assert valid.funding_events[0].source_event_digest == "3" * 64


@pytest.mark.parametrize(
    "digest",
    [None, "", "   ", "A" * 64, "a" * 63, "g" * 64],
)
def test_d026_instrument_record_digest_requires_lowercase_64_hex(
    digest: str | None,
) -> None:
    with pytest.raises(EconomicTransitionError, match="lowercase 64-hex"):
        _transition(instrument_record_digest=digest)


def test_d026_valid_instrument_digest_passes_through_unchanged() -> None:
    transition = _transition(instrument_record_digest="b" * 64)
    assert transition.instrument_record_digest == "b" * 64


def test_d026_funding_schedule_digest_requires_lowercase_64_hex() -> None:
    with pytest.raises(EconomicTransitionError, match="lowercase 64-hex"):
        _transition(funding_schedule_digest="F" * 64)


def test_d026_cost_digest_required_with_id_and_absent_without() -> None:
    with pytest.raises(EconomicTransitionError, match="lowercase 64-hex"):
        _transition(cost_schedule_id="COST", cost_schedule_digest="C" * 64)
    with pytest.raises(
        EconomicTransitionError, match="cost schedule digest without id"
    ):
        _transition(cost_schedule_id=None, cost_schedule_digest="2" * 64)
    empty = _transition(
        cost_schedule_id=None,
        cost_schedule_digest=None,
    )
    assert empty.cost_schedule_id is None
    assert empty.fee_events == ()


def test_d026_empty_transition_collections_remain_valid() -> None:
    transition = _transition()
    assert transition.decision_events == ()
    assert transition.fill_decisions == ()
    assert transition.cash_events == ()
    assert transition.fee_events == ()
    assert transition.funding_events == ()


def test_d026_fee_cash_row_must_not_carry_funding_event_id() -> None:
    fee_cash = _cash(
        CashEventKind.FEE,
        "CE-FEE",
        -0.1,
        fill_id="FILL-1",
        funding_event_id="TEST-FUND-1",
    )
    with pytest.raises(
        EconomicTransitionError, match="fee cash row must not carry funding_event_id"
    ):
        _transition(cash_events=(fee_cash,))


def test_d026_gross_cash_row_must_not_carry_funding_event_id() -> None:
    gross_cash = _cash(
        CashEventKind.GROSS_REALIZATION,
        "CE-GROSS",
        1.0,
        fill_id="F0",
        funding_event_id="TEST-FUND-1",
    )
    with pytest.raises(
        EconomicTransitionError,
        match="gross cash row must not carry funding_event_id",
    ):
        _transition(cash_events=(gross_cash,))


def test_d026_funding_cash_row_must_not_carry_fill_id() -> None:
    funding_cash = _cash(
        CashEventKind.FUNDING,
        "CE-FUND",
        -0.2,
        fill_id="F0",
        funding_event_id="TEST-FUND-1",
    )
    with pytest.raises(
        EconomicTransitionError, match="funding cash row must not carry fill_id"
    ):
        _transition(cash_events=(funding_cash,))


def test_d026_funding_cash_row_requires_funding_event_id_without_projection() -> None:
    with pytest.raises(
        EconomicTransitionError, match="funding cash row requires funding_event_id"
    ):
        _transition(cash_events=(_cash(CashEventKind.FUNDING, "CE-FUND", -0.2),))
