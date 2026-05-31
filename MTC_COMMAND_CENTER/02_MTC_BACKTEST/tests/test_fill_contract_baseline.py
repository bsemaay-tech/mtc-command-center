from datetime import datetime, timezone

from src.engine.fills import (
    BarData,
    PositionState,
    SameBarConflictPolicy,
    check_sl_hit,
    check_tp_hit,
    resolve_same_bar_conflict,
)


def _bar() -> BarData:
    return BarData(
        bar_index=1,
        timestamp=datetime(2026, 1, 1, tzinfo=timezone.utc),
        open=100.0,
        high=105.0,
        low=95.0,
        close=101.0,
    )


def test_same_bar_conflict_policy_resolution():
    pos = PositionState(is_long=True, quantity=1.0, avg_entry_price=100.0)
    assert resolve_same_bar_conflict(True, True, pos, SameBarConflictPolicy.WORST_CASE) == "sl"
    assert resolve_same_bar_conflict(True, True, pos, SameBarConflictPolicy.BEST_CASE) == "tp"
    assert resolve_same_bar_conflict(True, True, pos, SameBarConflictPolicy.SL_PRIORITY) == "sl"
    assert resolve_same_bar_conflict(True, True, pos, SameBarConflictPolicy.TP_PRIORITY) == "tp"


def test_sl_tp_touch_checks_for_long_and_short():
    bar = _bar()
    long_pos = PositionState(is_long=True, quantity=1.0, avg_entry_price=100.0, sl_price=96.0, tp1_price=104.0)
    short_pos = PositionState(is_long=False, quantity=1.0, avg_entry_price=100.0, sl_price=104.0, tp1_price=96.0)

    assert check_sl_hit(bar, long_pos) is True
    assert check_tp_hit(bar, long_pos, long_pos.tp1_price) is True
    assert check_sl_hit(bar, short_pos) is True
    assert check_tp_hit(bar, short_pos, short_pos.tp1_price) is True
