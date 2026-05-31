import pandas as pd

from src.config.defaults import MTCConfig
from src.engine.mtc_runner import MTCRunner
from src.modules.signals.base import SignalPlugin


class StubSignal(SignalPlugin):
    def __init__(self, long_values, short_values):
        super().__init__(name="Stub")
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


def _df_same_bar_opposite_reentry() -> pd.DataFrame:
    ts = pd.date_range("2026-01-01T00:00:00Z", periods=4, freq="15min", tz="UTC")
    return pd.DataFrame(
        {
            "timestamp": ts,
            "open": [100.0, 100.0, 98.5, 98.0],
            "high": [101.0, 100.2, 98.7, 98.2],
            "low": [99.8, 98.5, 97.8, 97.9],
            "close": [100.0, 98.9, 98.0, 98.1],
            "volume": [100, 100, 100, 100],
        }
    )


def test_same_bar_opposite_reentry_after_sl_is_allowed_without_flip():
    cfg = MTCConfig()
    cfg.signal_mode = "Range Filter Hybrid (ADX+Chop+BB)"
    cfg.strategy.slippage_ticks = 0
    cfg.strategy.commission_percent = 0.0
    cfg.trade.allow_flip = False
    cfg.trade.exit_on_opposite_signal = False
    cfg.trade.allow_same_bar_reentry = True
    cfg.trade.same_bar_reentry_requires_exit = True
    cfg.trade.signal_mode_max_entries = 1
    cfg.stop_loss.enabled = True
    cfg.stop_loss.mode = "%"
    cfg.stop_loss.percent = 1.0
    cfg.take_profit.enabled = False
    cfg.break_even.enabled = False
    cfg.trailing.enabled = False
    cfg.multi_tp.enabled = False

    runner = MTCRunner(cfg)
    runner.signal_plugin = StubSignal(
        long_values=[True, False, False, False],
        short_values=[False, True, True, False],
    )

    df = _df_same_bar_opposite_reentry()
    runner.run(df, warmup_bars=0)

    assert runner.state.position is not None
    assert runner.state.is_short
    assert runner.state.position.entry_bar == 1
    assert len(runner.state.trades) == 1
    assert runner.state.trades[0].direction.value == "long"
    assert runner.state.trades[0].exit_reason.value == "SL"


def test_dynamic_capital_guard_does_not_lock_low_balance_by_initial_pct():
    cfg = MTCConfig()
    cfg.risk.max_leverage_cap = 5.0
    runner = MTCRunner(cfg)
    runner.state.balance = 400.0
    runner.state.equity = 400.0

    assert runner._is_capital_exhausted(87000.0) is False

    runner.state.balance = 0.0
    runner.state.equity = 0.0
    assert runner._is_capital_exhausted(87000.0) is True
