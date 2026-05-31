import pandas as pd
import pytest

from src.config.defaults import MTCConfig
from src.engine.mtc_runner import MTCRunner


class _StubSignal:
    def __init__(self, long_values, short_values):
        self._long_values = long_values
        self._short_values = short_values

    def generate(self, df: pd.DataFrame):
        idx = df.index
        return (
            pd.Series(self._long_values, index=idx, dtype=bool),
            pd.Series(self._short_values, index=idx, dtype=bool),
        )

    def get_debug_series(self, df: pd.DataFrame):
        idx = df.index
        return {
            "long_raw": pd.Series(self._long_values, index=idx, dtype=bool),
            "short_raw": pd.Series(self._short_values, index=idx, dtype=bool),
        }


class _StubFilter:
    def apply_with_details(self, df: pd.DataFrame):
        allow = pd.Series([True] * len(df), index=df.index, dtype=bool)
        return allow, allow, {}


def _df() -> pd.DataFrame:
    ts = pd.date_range("2026-01-01T00:00:00Z", periods=3, freq="15min", tz="UTC")
    return pd.DataFrame(
        {
            "timestamp": ts,
            "open": [100.0, 101.0, 99.0],
            "high": [101.0, 101.2, 99.2],
            "low": [99.8, 98.8, 98.7],
            "close": [100.0, 99.0, 98.9],
            "volume": [100.0, 100.0, 100.0],
        }
    )


def test_opp_signal_reversal_reopens_same_bar_when_flip_enabled():
    cfg = MTCConfig()
    cfg.signal_mode = "Range Filter Hybrid (ADX+Chop+BB)"
    cfg.trade.entry_mode = "Edge"
    cfg.trade.allow_flip = True
    cfg.trade.exit_on_opposite_signal = True
    cfg.trade.allow_same_bar_reentry = True
    cfg.trade.same_bar_reentry_requires_exit = True
    cfg.trade.signal_mode_max_entries = 1
    cfg.stop_loss.enabled = False
    cfg.take_profit.enabled = False
    cfg.break_even.enabled = False
    cfg.trailing.enabled = False
    cfg.multi_tp.enabled = False
    cfg.strategy.slippage_ticks = 0
    cfg.strategy.commission_percent = 0.0
    cfg.strategy.close_open_at_end = False

    runner = MTCRunner(cfg)
    runner.signal_plugin = _StubSignal(
        long_values=[True, False, False],
        short_values=[False, True, True],
    )
    runner.filter_chain = _StubFilter()

    out = runner.run(_df(), warmup_bars=0)

    assert out["metrics"]["total_entries"] == 2
    assert len(runner.state.trades) == 1
    assert runner.state.trades[0].direction.value == "long"
    assert runner.state.trades[0].exit_reason.value == "OPP_SIGNAL"
    assert runner.state.trades[0].exit_bar == 1
    assert runner.state.position is not None
    assert runner.state.is_short
    assert runner.state.position.entry_bar == 1


def test_same_bar_flip_sizes_from_bar_start_realized_equity_snapshot():
    ts = pd.date_range("2026-01-01T00:00:00Z", periods=3, freq="15min", tz="UTC")
    df = pd.DataFrame(
        {
            "timestamp": ts,
            "open": [100.0, 90.0, 90.0],
            "high": [100.0, 90.0, 90.0],
            "low": [100.0, 90.0, 90.0],
            "close": [100.0, 90.0, 90.0],
            "volume": [100.0, 100.0, 100.0],
        }
    )

    cfg = MTCConfig()
    cfg.signal_mode = "Range Filter Hybrid (ADX+Chop+BB)"
    cfg.trade.entry_mode = "Edge"
    cfg.trade.allow_flip = True
    cfg.trade.exit_on_opposite_signal = True
    cfg.trade.allow_same_bar_reentry = True
    cfg.trade.same_bar_reentry_requires_exit = True
    cfg.stop_loss.enabled = False
    cfg.take_profit.enabled = False
    cfg.break_even.enabled = False
    cfg.trailing.enabled = False
    cfg.multi_tp.enabled = False
    cfg.strategy.slippage_ticks = 0
    cfg.strategy.commission_percent = 0.0
    cfg.risk.risk_long_percent = 100.0
    cfg.risk.risk_short_percent = 100.0
    cfg.risk.fallback_qty_pct = 100.0
    cfg.risk.risk_equity_mode = "Realized"

    runner = MTCRunner(cfg)
    runner.signal_plugin = _StubSignal(
        long_values=[False, True, True],
        short_values=[True, False, False],
    )
    runner.filter_chain = _StubFilter()

    out = runner.run(df, warmup_bars=0)

    assert out["metrics"]["total_entries"] == 2
    assert len(runner.state.trades) == 1
    assert runner.state.trades[0].direction.value == "short"
    assert runner.state.position is not None
    assert runner.state.is_long
    # Pine sizes same-bar reversals from bar-start realized equity, not post-exit balance.
    assert runner.state.position.quantity == pytest.approx(111.111111, rel=0, abs=1e-6)


def test_same_bar_flip_realized_snapshot_includes_pending_entry_commission():
    ts = pd.date_range("2026-01-01T00:00:00Z", periods=3, freq="15min", tz="UTC")
    df = pd.DataFrame(
        {
            "timestamp": ts,
            "open": [100.0, 90.0, 90.0],
            "high": [100.0, 90.0, 90.0],
            "low": [100.0, 90.0, 90.0],
            "close": [100.0, 90.0, 90.0],
            "volume": [100.0, 100.0, 100.0],
        }
    )

    cfg = MTCConfig()
    cfg.signal_mode = "Range Filter Hybrid (ADX+Chop+BB)"
    cfg.trade.entry_mode = "Edge"
    cfg.trade.allow_flip = True
    cfg.trade.exit_on_opposite_signal = True
    cfg.trade.allow_same_bar_reentry = True
    cfg.trade.same_bar_reentry_requires_exit = True
    cfg.stop_loss.enabled = False
    cfg.take_profit.enabled = False
    cfg.break_even.enabled = False
    cfg.trailing.enabled = False
    cfg.multi_tp.enabled = False
    cfg.strategy.slippage_ticks = 0
    cfg.strategy.commission_percent = 0.04
    cfg.risk.risk_long_percent = 100.0
    cfg.risk.risk_short_percent = 100.0
    cfg.risk.fallback_qty_pct = 100.0
    cfg.risk.risk_equity_mode = "Realized"

    runner = MTCRunner(cfg)
    runner.signal_plugin = _StubSignal(
        long_values=[False, True, True],
        short_values=[True, False, False],
    )
    runner.filter_chain = _StubFilter()

    out = runner.run(df, warmup_bars=0)

    assert out["metrics"]["total_entries"] == 2
    assert runner.state.position is not None
    # First short entry commission = 100 * 100 * 0.04% = 4.0, so the next
    # same-bar reversal should size from 9,996 / 90, not from 10,000 / 90.
    assert runner.state.position.quantity == pytest.approx(111.066666, rel=0, abs=1e-6)
