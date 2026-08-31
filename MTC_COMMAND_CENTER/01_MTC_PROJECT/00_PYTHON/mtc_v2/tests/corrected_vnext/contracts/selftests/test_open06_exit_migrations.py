"""OPEN-06 exit-owned migration fixtures P09-P26.

Runner/position-manager portions of shared rows are covered when those modules
are rewired; this file pins the exit-book and exit-selection portion now.
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import pytest

from mtc_v2.core.economics import EconomicRecords, EconomicsRefusal
from mtc_v2.core.exits import (
    STOP_OWNER_BE,
    STOP_OWNER_TRAIL,
    build_working_exit_book,
    disable_active_target_exits,
    evaluate_price_exit,
    resolve_corrected_price_exits,
    update_protective_stop_owner,
)
from mtc_v2.core.types import Bar, EntryLeg, Position, WorkingExit


ROOT = Path(__file__).resolve().parents[4]
RECORDS = ROOT / "core" / "economic_records"


def _records(scenario: str) -> EconomicRecords:
    return EconomicRecords.from_record_paths(
        instrument_path=RECORDS / "instruments" / f"SYNTH-INSTRUMENT-{scenario}-V1.json",
        cost_path=RECORDS / "costs" / f"SYNTH-COST-{scenario}-V1.json",
        funding_path=RECORDS / "funding" / f"SYNTH-FUNDING-{scenario}-V1.json",
    )


def _bar(open_: float, high: float, low: float, close: float) -> Bar:
    return Bar(
        timestamp=datetime(2000, 1, 1, tzinfo=timezone.utc),
        open=open_,
        high=high,
        low=low,
        close=close,
        volume=0.0,
        bar_index=2,
    )


def _position(
    *,
    side: str = "long",
    stop: float | None = 90.0,
    exits: list[WorkingExit] | None = None,
) -> Position:
    return Position(
        side=side,
        entry_price=100.0,
        avg_entry_price=100.0,
        qty=2.0,
        entry_bar=1,
        initial_qty=2.0,
        active_stop_price=stop,
        entry_legs=[EntryLeg(100.0, 2.0, 1)],
        lifecycle_id=1,
        working_exit_reference_qty=2.0,
        working_exit_book_version=1,
        active_stop_owner="STOP" if stop is not None else None,
        working_exits=list(exits or []),
        initial_risk_per_unit=10.0,
    )


def test_p09_none_mode_builds_no_target_book() -> None:
    first, book = build_working_exit_book(
        {"tp_mode": "None"},
        entry_price=100.0,
        is_long=True,
        price_tick=1.0,
        book_version=1,
    )
    assert (first, book) == (None, [])


@pytest.mark.parametrize("is_long, expected", [(True, 105.0), (False, 95.0)])
def test_p10_atr_target_requires_present_atr(is_long: bool, expected: float) -> None:
    config = {"tp_mode": "ATR", "tp_atr_mult": 1.0}
    assert build_working_exit_book(
        config,
        entry_price=100.0,
        is_long=is_long,
        price_tick=1.0,
        atr_value=None,
        book_version=1,
    ) == (None, [])
    first, book = build_working_exit_book(
        config,
        entry_price=100.0,
        is_long=is_long,
        price_tick=1.0,
        atr_value=5.0,
        book_version=1,
    )
    assert first == expected and book[0].target_price == expected


@pytest.mark.parametrize("is_long, expected", [(True, 111.1), (False, 90.9)])
def test_p11_percent_target_uses_final_entry_fill(is_long: bool, expected: float) -> None:
    first, _ = build_working_exit_book(
        {"tp_mode": "Percent", "tp_percent": 10.0},
        entry_price=101.0,
        is_long=is_long,
        price_tick=0.1,
        book_version=1,
    )
    assert first == expected


def test_p12_r_target_requires_positive_final_fill_risk() -> None:
    config = {"tp_mode": "R", "tp_r_multiple": 1.0}
    assert build_working_exit_book(
        config,
        entry_price=100.0,
        is_long=True,
        price_tick=1.0,
        initial_risk_per_unit=0.0,
        book_version=1,
    ) == (None, [])
    first, _ = build_working_exit_book(
        config,
        entry_price=100.0,
        is_long=True,
        price_tick=1.0,
        initial_risk_per_unit=10.0,
        book_version=1,
    )
    assert first == 110.0


@pytest.mark.parametrize(
    "completed, expected",
    [(set(), ["TP1", "TP2"]), ({"TP1"}, ["TP2"]), ({"TP2"}, ["TP1"])],
)
def test_p13_multi_target_book_preserves_completed_ids(
    completed: set[str], expected: list[str]
) -> None:
    _, book = build_working_exit_book(
        {
            "tp_mode": "Multi-TP",
            "tp1_r_multiple": 0.5,
            "tp1_close_pct": 50.0,
            "tp2_r_multiple": 1.0,
        },
        entry_price=100.0,
        is_long=True,
        price_tick=1.0,
        initial_risk_per_unit=10.0,
        book_version=2,
        completed_exit_ids=completed,
    )
    assert [item.exit_id for item in book] == expected


@pytest.mark.parametrize(
    "side,bar,expected",
    [
        ("long", _bar(106, 106, 100, 100), 106.0),
        ("long", _bar(100, 106, 99, 100), 105.0),
        ("short", _bar(94, 100, 94, 100), 94.0),
        ("short", _bar(100, 101, 94, 100), 95.0),
    ],
)
def test_p14_p15_raw_target_order_and_reference(
    side: str, bar: Bar, expected: float
) -> None:
    target = 105.0 if side == "long" else 95.0
    position = _position(
        side=side,
        stop=None,
        exits=[WorkingExit("TARGET", "TP", target, None, 1.0, 1)],
    )
    hit = evaluate_price_exit(
        {
            "execution_profile_id": "raw_close_only_v1",
            "tp_mode": "Percent",
            "use_sl_percent": False,
            "use_sl_swing_atr": False,
        },
        bar=bar,
        position=position,
    )
    assert hit.hit and hit.fill_price == expected


def test_p15_raw_target_no_touch_is_green() -> None:
    position = _position(
        stop=None,
        exits=[WorkingExit("TARGET", "TP", 105.0, None, 1.0, 1)],
    )
    assert not evaluate_price_exit(
        {
            "execution_profile_id": "raw_close_only_v1",
            "tp_mode": "Percent",
            "use_sl_percent": False,
            "use_sl_swing_atr": False,
        },
        bar=_bar(100, 104, 99, 100),
        position=position,
    ).hit


def test_p16_p17_stop_first_collision_and_target_only_twin() -> None:
    exits = [WorkingExit("TARGET", "TP", 110.0, 90.0, 1.0, 1)]
    collision = resolve_corrected_price_exits(
        bar=_bar(100, 115, 85, 111),
        position=_position(exits=exits),
        records=_records("RULE2-06-RED"),
    )
    target_only = resolve_corrected_price_exits(
        bar=_bar(100, 115, 95, 111),
        position=_position(exits=exits),
        records=_records("RULE2-06-RED"),
    )
    assert collision.fill_decisions[0].exit_id == "STOP"
    assert target_only.fill_decisions[0].exit_id == "TARGET"


def test_p18_close_only_cancel_flag_and_target_disable() -> None:
    exits = [
        WorkingExit("TP1", "TP1", 105.0, 90.0, 0.5, 1),
        WorkingExit("TP2", "TP2", 110.0, 90.0, 1.0, 1),
    ]
    position = _position(exits=exits)
    config = {
        "execution_profile_id": "close_only_deterministic_v2",
        "tp_mode": "Multi-TP",
        "use_sl_percent": True,
        "use_sl_swing_atr": False,
    }
    tp1_only = evaluate_price_exit(config, bar=_bar(100, 106, 99, 106), position=position)
    both = evaluate_price_exit(config, bar=_bar(100, 111, 99, 111), position=position)
    assert not tp1_only.cancel_remaining_targets_after_fill
    assert both.cancel_remaining_targets_after_fill
    disable_active_target_exits(position)
    assert position.active_tp_price is None and not any(item.active for item in position.working_exits)


@pytest.mark.parametrize(
    "side,bar,expected_reference,expected_fill",
    [
        ("long", _bar(90, 95, 85, 92), 90.0, 89.1),
        ("long", _bar(100, 105, 89, 100), 90.0, 89.1),
        ("short", _bar(110, 115, 105, 108), 110.0, 111.1),
        ("short", _bar(100, 111, 95, 100), 110.0, 111.1),
    ],
)
def test_p20_raw_stop_reference_precedes_one_adverse_slippage(
    side: str, bar: Bar, expected_reference: float, expected_fill: float
) -> None:
    position = _position(side=side, stop=90.0 if side == "long" else 110.0)
    transition = resolve_corrected_price_exits(
        bar=bar,
        position=position,
        records=_records("RULE2-05-RED"),
    )
    fill = transition.fill_decisions[0]
    assert fill.reference_price == expected_reference
    assert fill.final_fill_price == expected_fill
    assert fill.slippage_application_count == 1


@pytest.mark.parametrize("policy", [None, "UNKNOWN", "TARGET_FIRST"])
def test_p21_production_refuses_missing_unknown_or_non_stop_first_policy(
    policy: str | None,
) -> None:
    with pytest.raises(EconomicsRefusal):
        resolve_corrected_price_exits(
            bar=_bar(100, 115, 85, 105),
            position=_position(),
            records=_records("RULE2-06-RED"),
            same_bar_collision_policy_id=policy,  # type: ignore[arg-type]
        )


def test_p24_absent_stop_empty_book_and_invalid_bar_are_no_fill_controls() -> None:
    for bar in (_bar(100, 104, 96, 100), _bar(100, 99, 101, 100)):
        transition = resolve_corrected_price_exits(
            bar=bar,
            position=_position(stop=None, exits=[]),
            records=_records("RULE2-06-GREEN"),
        )
        assert transition.fill_decisions == ()
        assert transition.next_position_facts.quantity == 2.0


@pytest.mark.parametrize("side", ["long", "short"])
def test_p25_trailing_retains_distinct_close_and_wick_profiles(side: str) -> None:
    raw = _position(side=side, stop=90.0 if side == "long" else 110.0)
    close_only = _position(side=side, stop=90.0 if side == "long" else 110.0)
    bar = _bar(100, 115, 85, 100)
    base = {
        "use_trailing": True,
        "trail_start_r": 1.0,
        "trail_distance_atr_mult": 1.0,
        "use_break_even": False,
    }
    update_protective_stop_owner(
        {**base, "execution_profile_id": "raw_close_only_v1"},
        position=raw,
        bar=bar,
        price_tick=1.0,
        trail_atr=5.0,
    )
    update_protective_stop_owner(
        {**base, "execution_profile_id": "close_only_deterministic_v2"},
        position=close_only,
        bar=bar,
        price_tick=1.0,
        trail_atr=5.0,
    )
    assert raw.active_stop_owner == STOP_OWNER_TRAIL
    assert close_only.active_stop_owner != STOP_OWNER_TRAIL


@pytest.mark.parametrize("side", ["long", "short"])
def test_p26_break_even_retains_distinct_close_and_wick_profiles(side: str) -> None:
    raw = _position(side=side, stop=90.0 if side == "long" else 110.0)
    close_only = _position(side=side, stop=90.0 if side == "long" else 110.0)
    bar = _bar(100, 115, 85, 100)
    base = {
        "use_trailing": False,
        "use_break_even": True,
        "be_trigger_r": 1.0,
        "be_buffer_r": 0.1,
    }
    update_protective_stop_owner(
        {**base, "execution_profile_id": "raw_close_only_v1"},
        position=raw,
        bar=bar,
        price_tick=1.0,
    )
    update_protective_stop_owner(
        {**base, "execution_profile_id": "close_only_deterministic_v2"},
        position=close_only,
        bar=bar,
        price_tick=1.0,
    )
    assert raw.active_stop_owner == STOP_OWNER_BE
    assert close_only.active_stop_owner != STOP_OWNER_BE
