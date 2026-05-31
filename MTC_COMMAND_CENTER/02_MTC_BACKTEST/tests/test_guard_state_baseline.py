from datetime import datetime, timezone

import pytest

from src.engine.mtc_state import DailyStats, Direction, ExitReason, MTCState


def test_daily_stats_loss_percent():
    stats = DailyStats(date=datetime(2026, 2, 15, tzinfo=timezone.utc), starting_equity=10_000.0)
    assert stats.loss_percent(9_500.0) == pytest.approx(5.0)
    assert stats.loss_percent(10_100.0) == pytest.approx(-1.0)


def test_consecutive_loss_counter_resets_on_winner():
    state = MTCState(initial_capital=10_000.0, balance=10_000.0, equity=10_000.0)
    state.current_time = datetime(2026, 2, 15, tzinfo=timezone.utc)
    state.bar_index = 1
    state.open_position(Direction.LONG, entry_price=100.0, quantity=1.0, sl_price=99.0)
    state.close_position(exit_price=99.0, exit_reason=ExitReason.SL, commission_pct=0.0)
    assert state.consecutive_losses == 1

    state.bar_index = 2
    state.open_position(Direction.LONG, entry_price=100.0, quantity=1.0, sl_price=99.0)
    state.close_position(exit_price=101.0, exit_reason=ExitReason.TP, commission_pct=0.0)
    assert state.consecutive_losses == 0
