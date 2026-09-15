from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import pytest

from mtc_v2.core.economics import (
    EconomicRecords,
    EconomicsRefusal,
    REFUSED_AMBIGUOUS_SAME_BAR,
)
from mtc_v2.core.exits import evaluate_price_exit, resolve_corrected_price_exits
from mtc_v2.core.types import Bar, EntryLeg, Position, WorkingExit


MTC_V2_ROOT = Path(__file__).resolve().parents[4]
RECORD_ROOT = MTC_V2_ROOT / "core" / "economic_records"


def _records(scenario: str = "RULE2-06-RED") -> EconomicRecords:
    return EconomicRecords.from_record_paths(
        instrument_path=(
            RECORD_ROOT / "instruments" / f"SYNTH-INSTRUMENT-{scenario}-V1.json"
        ),
        cost_path=RECORD_ROOT / "costs" / f"SYNTH-COST-{scenario}-V1.json",
        funding_path=RECORD_ROOT / "funding" / f"SYNTH-FUNDING-{scenario}-V1.json",
    )


def _position(*, equal_targets: bool = False, side: str = "long") -> Position:
    targets = (105.0, 105.0 if equal_targets else 110.0)
    return Position(
        side=side,
        entry_price=100.0,
        avg_entry_price=100.0,
        qty=2.0,
        entry_bar=1,
        initial_qty=2.0,
        active_stop_price=90.0 if side == "long" else 110.0,
        entry_legs=[EntryLeg(100.0, 2.0, 1)],
        lifecycle_id=1,
        working_exit_reference_qty=2.0,
        working_exit_book_version=1,
        active_stop_owner="STOP",
        working_exits=[
            WorkingExit("TARGET-NEAR", "TP1", targets[0], 90.0, 0.5, 1),
            WorkingExit("TARGET-FAR", "TP2", targets[1], 90.0, 0.5, 1),
        ],
        initial_risk_per_unit=10.0,
    )


def _bar(
    *,
    open_: float = 100.0,
    high: float = 115.0,
    low: float = 85.0,
    close: float = 105.0,
) -> Bar:
    return Bar(
        timestamp=datetime(2000, 1, 1, 0, 12, tzinfo=timezone.utc),
        open=open_,
        high=high,
        low=low,
        close=close,
        volume=0.0,
        bar_index=2,
    )


def test_production_collision_is_stop_first_and_atomic() -> None:
    transition = resolve_corrected_price_exits(
        bar=_bar(), position=_position(), records=_records()
    )

    assert [(fill.exit_id, fill.final_fill_price, fill.quantity) for fill in transition.fill_decisions] == [
        ("STOP", 90.0, 2.0)
    ]
    assert transition.next_position_facts.quantity == 0.0


def test_target_first_pair_is_explicit_test_machinery() -> None:
    transition = resolve_corrected_price_exits(
        bar=_bar(),
        position=_position(),
        records=_records(),
        same_bar_collision_policy_id="TARGET_FIRST",
        allow_test_policy=True,
    )

    assert [(fill.exit_id, fill.quantity) for fill in transition.fill_decisions] == [
        ("TARGET-NEAR", 1.0),
        ("TARGET-FAR", 1.0),
    ]


def test_equal_price_test_book_uses_utf8_exit_id_order() -> None:
    transition = resolve_corrected_price_exits(
        bar=_bar(),
        position=_position(equal_targets=True),
        records=_records("RULE2-06-EQUAL-PRICE-RED"),
        same_bar_collision_policy_id="TARGET_FIRST",
        allow_test_policy=True,
    )

    assert [fill.exit_id for fill in transition.fill_decisions] == [
        "TARGET-FAR",
        "TARGET-NEAR",
    ]


def test_subbar_unknown_is_available_only_as_test_refusal_arm() -> None:
    with pytest.raises(EconomicsRefusal) as exc_info:
        resolve_corrected_price_exits(
            bar=_bar(),
            position=_position(),
            records=_records(),
            same_bar_collision_policy_id="SUBBAR_UNKNOWN",
            allow_test_policy=True,
        )
    assert exc_info.value.refusal_code == REFUSED_AMBIGUOUS_SAME_BAR


def test_close_only_stop_is_retired_in_corrected_path_but_legacy_stays_exact() -> None:
    position = _position()
    position.working_exits = []
    position.active_stop_price = 100.0
    bar = _bar(open_=90.0, high=95.0, low=85.0, close=92.0)
    legacy = evaluate_price_exit(
        {
            "execution_profile_id": "close_only_deterministic_v2",
            "use_sl_percent": True,
            "use_sl_swing_atr": False,
            "tp_mode": "None",
        },
        bar=bar,
        position=position,
    )
    corrected = resolve_corrected_price_exits(
        bar=bar,
        position=position,
        records=_records("RULE2-04-RED"),
    )

    assert legacy.fill_price == 92.0
    assert corrected.fill_decisions[0].reference_price == 90.0
    assert corrected.fill_decisions[0].fill_trigger == "GAP_OPEN"


@pytest.mark.parametrize(
    "bar",
    [
        _bar(open_=105.0, high=106.0, low=101.0, close=104.0),
        _bar(open_=100.0, high=99.0, low=101.0, close=100.0),
    ],
)
def test_no_touch_or_invalid_bar_emits_no_fill(bar: Bar) -> None:
    position = _position()
    position.working_exits = []
    transition = resolve_corrected_price_exits(
        bar=bar,
        position=position,
        records=_records("RULE2-04-GREEN"),
    )
    assert transition.fill_decisions == ()
