from __future__ import annotations

from dataclasses import FrozenInstanceError
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
) -> CashEvent:
    return CashEvent(
        sequence=sequence,
        cash_event_id=cash_event_id,
        event_timestamp=datetime(2000, 1, 1, tzinfo=timezone.utc),
        lifecycle_id=1,
        kind=kind,
        signed_delta=signed_delta,
        settlement_currency="TEST-USD",
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
    fee_cash = _cash(CashEventKind.FEE, "CE-FEE", -0.1)
    funding_cash = _cash(CashEventKind.FUNDING, "CE-FUND", -0.2, sequence=1)
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
