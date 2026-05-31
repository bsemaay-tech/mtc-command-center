from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone

import pandas as pd

from src.config.defaults import MTCConfig
from src.engine.mtc_runner import MTCRunner
from src.modules.signals.base import SignalPlugin


@dataclass
class _StubSignal:
    long_series: pd.Series
    short_series: pd.Series

    def generate(self, df: pd.DataFrame) -> tuple[pd.Series, pd.Series]:
        return self.long_series, self.short_series


class _FlipStubSignal(SignalPlugin):
    def __init__(self, long_values: list[bool], short_values: list[bool]):
        super().__init__(name="FlipStub")
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
    def __init__(self, allow: pd.Series):
        self.allow = allow

    def apply_with_details(self, df: pd.DataFrame):
        return self.allow, self.allow, {}


def _df_for_guards() -> pd.DataFrame:
    ts = pd.date_range(start=datetime(2026, 1, 1, tzinfo=timezone.utc), periods=6, freq="15min")
    return pd.DataFrame(
        {
            "timestamp": ts,
            "open": [100.0, 100.2, 100.0, 99.0, 98.5, 98.0],
            "high": [100.4, 100.5, 100.2, 99.2, 98.7, 98.2],
            "low": [99.8, 99.9, 99.6, 95.0, 98.2, 97.8],
            "close": [100.2, 100.0, 99.0, 98.5, 98.0, 97.9],
            "volume": [10, 10, 10, 10, 10, 10],
        }
    )


def _run_with_stub(
    config: MTCConfig,
    long_raw: list[bool],
    short_raw: list[bool],
    df: pd.DataFrame | None = None,
) -> dict:
    df = _df_for_guards() if df is None else df
    runner = MTCRunner(config)
    allow = pd.Series([True] * len(df))
    runner.signal_plugin = _StubSignal(pd.Series(long_raw), pd.Series(short_raw))
    runner.filter_chain = _StubFilter(allow)
    return runner.run(df, warmup_bars=0)


def test_daily_loss_limit_blocks_later_entries_same_day():
    cfg = MTCConfig()
    cfg.trade.entry_mode = "Edge"
    cfg.trade.signal_mode_max_entries = 1
    cfg.risk.use_daily_loss_limit = True
    cfg.risk.max_daily_loss_percent = 0.05
    cfg.stop_loss.enabled = False
    cfg.take_profit.enabled = False
    cfg.trailing.enabled = False
    cfg.break_even.enabled = False
    cfg.time_stop.enabled = True
    cfg.time_stop.bars = 1
    cfg.time_stop.condition = "Always"

    out = _run_with_stub(
        cfg,
        long_raw=[False, True, False, True, False, False],
        short_raw=[False, False, False, False, False, False],
    )
    assert out["metrics"]["total_entries"] == 1


def test_max_trades_per_day_blocks_after_limit():
    cfg = MTCConfig()
    cfg.trade.entry_mode = "Edge"
    cfg.trade.signal_mode_max_entries = 1
    cfg.risk.use_max_trades_per_day = True
    cfg.risk.max_trades_per_day = 1
    cfg.stop_loss.enabled = False
    cfg.take_profit.enabled = False
    cfg.trailing.enabled = False
    cfg.break_even.enabled = False
    cfg.time_stop.enabled = True
    cfg.time_stop.bars = 1
    cfg.time_stop.condition = "Always"

    out = _run_with_stub(
        cfg,
        long_raw=[False, True, False, True, False, False],
        short_raw=[False, False, False, False, False, False],
    )
    assert out["metrics"]["total_entries"] == 1


def test_mae_guard_blocks_signal_mode_addon_when_drawdown_exceeds_limit():
    base = MTCConfig()
    base.trade.entry_mode = "Signal"
    base.trade.signal_mode_max_entries = 3
    base.trade.signal_mode_cooldown_bars = 1
    base.stop_loss.enabled = False
    base.take_profit.enabled = False
    base.trailing.enabled = False
    base.break_even.enabled = False
    base.time_stop.enabled = False
    base.strategy.slippage_ticks = 0

    no_guard = _run_with_stub(
        base,
        long_raw=[False, True, True, True, True, True],
        short_raw=[False, False, False, False, False, False],
    )
    no_guard_entries = no_guard["metrics"]["total_entries"]
    assert no_guard_entries > 1

    with_guard = base.model_copy(deep=True)
    with_guard.guards.use_mae_guard = True
    with_guard.guards.mae_max_pct = 0.01
    with_guard_out = _run_with_stub(
        with_guard,
        long_raw=[False, True, True, True, True, True],
        short_raw=[False, False, False, False, False, False],
    )
    with_guard_entries = with_guard_out["metrics"]["total_entries"]
    assert with_guard_entries == 1


def test_time_stop_eod_closes_position_at_day_boundary():
    df = pd.DataFrame(
        {
            "timestamp": pd.to_datetime(
                [
                    "2026-01-01T23:30:00Z",
                    "2026-01-01T23:45:00Z",
                    "2026-01-02T00:00:00Z",
                    "2026-01-02T00:15:00Z",
                ],
                utc=True,
            ),
            "open": [100.0, 100.1, 100.2, 100.1],
            "high": [100.2, 100.2, 100.3, 100.2],
            "low": [99.9, 100.0, 100.0, 99.9],
            "close": [100.1, 100.1, 100.2, 100.1],
            "volume": [10, 10, 10, 10],
        }
    )

    cfg = MTCConfig()
    cfg.trade.entry_mode = "Edge"
    cfg.time_stop.enabled = False
    cfg.time_stop.eod = True
    cfg.stop_loss.enabled = False
    cfg.take_profit.enabled = False
    cfg.trailing.enabled = False
    cfg.break_even.enabled = False
    cfg.strategy.slippage_ticks = 0

    out = _run_with_stub(
        cfg,
        long_raw=[True, False, False, False],
        short_raw=[False, False, False, False],
        df=df,
    )
    assert out["metrics"]["total_trades"] == 1
    assert pd.Timestamp(out["trades_all"][0].exit_time).date().isoformat() == "2026-01-01"


def test_time_stop_eow_closes_position_at_week_boundary():
    df = pd.DataFrame(
        {
            "timestamp": pd.to_datetime(
                [
                    "2026-01-04T23:30:00Z",  # Sunday
                    "2026-01-04T23:45:00Z",  # Sunday end-of-week bar
                    "2026-01-05T00:00:00Z",  # Monday
                    "2026-01-05T00:15:00Z",
                ],
                utc=True,
            ),
            "open": [100.0, 100.1, 100.2, 100.1],
            "high": [100.2, 100.2, 100.3, 100.2],
            "low": [99.9, 100.0, 100.0, 99.9],
            "close": [100.1, 100.1, 100.2, 100.1],
            "volume": [10, 10, 10, 10],
        }
    )

    cfg = MTCConfig()
    cfg.trade.entry_mode = "Edge"
    cfg.time_stop.enabled = False
    cfg.time_stop.eow = True
    cfg.stop_loss.enabled = False
    cfg.take_profit.enabled = False
    cfg.trailing.enabled = False
    cfg.break_even.enabled = False
    cfg.strategy.slippage_ticks = 0

    out = _run_with_stub(
        cfg,
        long_raw=[True, False, False, False],
        short_raw=[False, False, False, False],
        df=df,
    )
    assert out["metrics"]["total_trades"] == 1
    assert pd.Timestamp(out["trades_all"][0].exit_time).date().isoformat() == "2026-01-04"


def test_consec_loss_reset_daily_allows_new_day_entry():
    df = pd.DataFrame(
        {
            "timestamp": pd.to_datetime(
                [
                    "2026-01-01T23:00:00Z",
                    "2026-01-01T23:15:00Z",
                    "2026-01-02T00:00:00Z",
                    "2026-01-02T00:15:00Z",
                    "2026-01-02T00:30:00Z",
                ],
                utc=True,
            ),
            "open": [100.0, 99.8, 100.0, 100.4, 100.4],
            "high": [100.1, 99.9, 100.5, 100.6, 100.5],
            "low": [99.9, 99.6, 99.8, 100.2, 100.3],
            "close": [100.0, 99.7, 100.4, 100.5, 100.4],
            "volume": [10, 10, 10, 10, 10],
        }
    )

    cfg_base = MTCConfig()
    cfg_base.trade.entry_mode = "Edge"
    cfg_base.guards.use_consec_loss_guard = True
    cfg_base.guards.consec_loss_max = 1
    cfg_base.stop_loss.enabled = False
    cfg_base.take_profit.enabled = False
    cfg_base.trailing.enabled = False
    cfg_base.break_even.enabled = False
    cfg_base.time_stop.enabled = True
    cfg_base.time_stop.bars = 1
    cfg_base.time_stop.condition = "Always"
    cfg_base.strategy.slippage_ticks = 0

    no_reset = cfg_base.model_copy(deep=True)
    no_reset.guards.consec_loss_reset_daily = False
    out_no_reset = _run_with_stub(
        no_reset,
        long_raw=[True, False, True, False, False],
        short_raw=[False, False, False, False, False],
        df=df,
    )
    assert out_no_reset["metrics"]["total_entries"] == 1

    with_reset = cfg_base.model_copy(deep=True)
    with_reset.guards.consec_loss_reset_daily = True
    out_with_reset = _run_with_stub(
        with_reset,
        long_raw=[True, False, True, False, False],
        short_raw=[False, False, False, False, False],
        df=df,
    )
    assert out_with_reset["metrics"]["total_entries"] == 2


def _df_same_bar_sl_reentry() -> pd.DataFrame:
    ts = pd.date_range("2026-01-01T00:00:00Z", periods=4, freq="15min", tz="UTC")
    return pd.DataFrame(
        {
            "timestamp": ts,
            "open": [100.0, 100.0, 98.5, 98.0],
            "high": [101.0, 100.2, 98.7, 98.2],
            "low": [99.8, 89.0, 97.8, 97.9],
            "close": [100.0, 90.0, 98.0, 98.1],
            "volume": [100, 100, 100, 100],
        }
    )


def test_daily_loss_limit_blocks_same_bar_reentry_after_sl():
    cfg = MTCConfig()
    cfg.signal_mode = "Range Filter Hybrid (ADX+Chop+BB)"
    cfg.trade.allow_flip = False
    cfg.trade.exit_on_opposite_signal = False
    cfg.trade.allow_same_bar_reentry = True
    cfg.trade.same_bar_reentry_requires_exit = True
    cfg.trade.signal_mode_max_entries = 1
    cfg.stop_loss.enabled = True
    cfg.stop_loss.mode = "%"
    cfg.stop_loss.percent = 10.0
    cfg.take_profit.enabled = False
    cfg.break_even.enabled = False
    cfg.trailing.enabled = False
    cfg.multi_tp.enabled = False
    cfg.strategy.slippage_ticks = 0
    cfg.strategy.commission_percent = 0.0
    cfg.risk.risk_long_percent = 100.0
    cfg.risk.risk_short_percent = 100.0
    cfg.risk.use_daily_loss_limit = True
    cfg.risk.max_daily_loss_percent = 5.0

    runner = MTCRunner(cfg)
    runner.signal_plugin = _FlipStubSignal(
        long_values=[True, False, False, False],
        short_values=[False, True, False, False],
    )
    runner.filter_chain = _StubFilter(pd.Series([True] * 4))

    out = runner.run(_df_same_bar_sl_reentry(), warmup_bars=0)

    assert out["metrics"]["total_entries"] == 1
    assert len(runner.state.trades) == 1
    assert runner.state.trades[0].exit_reason.value == "SL"
    assert runner.state.position is None


def test_cooldown_guard_blocks_same_bar_reentry_after_sl():
    cfg = MTCConfig()
    cfg.signal_mode = "Range Filter Hybrid (ADX+Chop+BB)"
    cfg.trade.allow_flip = False
    cfg.trade.exit_on_opposite_signal = False
    cfg.trade.allow_same_bar_reentry = True
    cfg.trade.same_bar_reentry_requires_exit = True
    cfg.trade.signal_mode_max_entries = 1
    cfg.stop_loss.enabled = True
    cfg.stop_loss.mode = "%"
    cfg.stop_loss.percent = 10.0
    cfg.take_profit.enabled = False
    cfg.break_even.enabled = False
    cfg.trailing.enabled = False
    cfg.multi_tp.enabled = False
    cfg.strategy.slippage_ticks = 0
    cfg.strategy.commission_percent = 0.0
    cfg.guards.use_cooldown_guard = True
    cfg.guards.cooldown_bars = 1

    runner = MTCRunner(cfg)
    runner.signal_plugin = _FlipStubSignal(
        long_values=[True, False, False, False],
        short_values=[False, True, False, False],
    )
    runner.filter_chain = _StubFilter(pd.Series([True] * 4))

    out = runner.run(_df_same_bar_sl_reentry(), warmup_bars=0)

    assert out["metrics"]["total_entries"] == 1
    assert len(runner.state.trades) == 1
    assert runner.state.trades[0].exit_reason.value == "SL"
    assert runner.state.position is None
