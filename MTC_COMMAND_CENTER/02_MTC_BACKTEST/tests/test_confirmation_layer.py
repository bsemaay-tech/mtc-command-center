from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from src.config.defaults import MTCConfig
from src.engine.mtc_runner import MTCRunner


@dataclass
class _StubSignal:
    long_series: pd.Series
    short_series: pd.Series

    def generate(self, df: pd.DataFrame):
        return self.long_series, self.short_series


class _StubFilter:
    def __init__(self, allow: pd.Series):
        self.allow = allow

    def apply_with_details(self, df: pd.DataFrame):
        return self.allow, self.allow, {}


def _build_df() -> pd.DataFrame:
    ts = pd.date_range("2026-01-01", periods=16, freq="15min", tz="UTC")
    close = [100.0, 100.2, 100.1, 100.3, 100.4, 100.2, 100.5, 100.8, 101.2, 101.8, 102.4, 103.0, 103.8, 104.5, 105.2, 106.0]
    open_ = [close[0]] + close[:-1]
    high = [max(o, c) + 0.2 for o, c in zip(open_, close)]
    low = [min(o, c) - 0.2 for o, c in zip(open_, close)]
    return pd.DataFrame(
        {
            "timestamp": ts,
            "open": open_,
            "high": high,
            "low": low,
            "close": close,
            "volume": [100] * len(ts),
        }
    )


def _run(cfg: MTCConfig, long_raw: list[bool]) -> dict:
    df = _build_df()
    return _run_on_df(cfg, df, long_raw)


def _run_on_df(cfg: MTCConfig, df: pd.DataFrame, long_raw: list[bool]) -> dict:
    runner = MTCRunner(cfg)
    allow = pd.Series([True] * len(df))
    runner.signal_plugin = _StubSignal(pd.Series(long_raw), pd.Series([False] * len(df)))
    runner.filter_chain = _StubFilter(allow)
    return runner.run(df, warmup_bars=0)


def test_confirmation_layer_disabled_allows_edge_entry():
    cfg = MTCConfig()
    cfg.trade.entry_mode = "Edge"
    cfg.stop_loss.enabled = False
    cfg.take_profit.enabled = False
    cfg.trailing.enabled = False
    cfg.break_even.enabled = False
    cfg.time_stop.enabled = False
    cfg.strategy.slippage_ticks = 0
    cfg.confirmation.enabled = False

    out = _run(cfg, long_raw=[False] * 5 + [True] + [False] * 10)
    assert out["metrics"]["total_entries"] == 1


def test_confirmation_layer_blocks_when_breakout_and_momentum_not_met():
    cfg = MTCConfig()
    cfg.trade.entry_mode = "Edge"
    cfg.stop_loss.enabled = False
    cfg.take_profit.enabled = False
    cfg.trailing.enabled = False
    cfg.break_even.enabled = False
    cfg.time_stop.enabled = False
    cfg.strategy.slippage_ticks = 0
    cfg.confirmation.enabled = True
    cfg.confirmation.p_left = 2
    cfg.confirmation.p_right = 2
    cfg.confirmation.atr_len = 3
    cfg.confirmation.mom_atr_mult = 10.0

    out = _run(cfg, long_raw=[False] * 5 + [True] + [False] * 10)
    assert out["metrics"]["total_entries"] == 0


def test_confirmation_layer_allows_when_conditions_met():
    cfg = MTCConfig()
    cfg.trade.entry_mode = "Edge"
    cfg.stop_loss.enabled = False
    cfg.take_profit.enabled = False
    cfg.trailing.enabled = False
    cfg.break_even.enabled = False
    cfg.time_stop.enabled = False
    cfg.strategy.slippage_ticks = 0
    cfg.confirmation.enabled = True
    cfg.confirmation.p_left = 1
    cfg.confirmation.p_right = 1
    cfg.confirmation.atr_len = 2
    cfg.confirmation.mom_atr_mult = 0.0
    cfg.confirmation.raw_event_mode = "LEVEL"

    ts = pd.date_range("2026-01-01", periods=8, freq="15min", tz="UTC")
    close = [100.0, 101.0, 100.8, 101.2, 100.9, 101.0, 101.6, 102.0]
    open_ = [close[0]] + close[:-1]
    high = [max(o, c) + 0.1 for o, c in zip(open_, close)]
    low = [min(o, c) - 0.1 for o, c in zip(open_, close)]
    df = pd.DataFrame(
        {
            "timestamp": ts,
            "open": open_,
            "high": high,
            "low": low,
            "close": close,
            "volume": [100] * len(ts),
        }
    )
    long = [False, False, False, False, False, True, True, True]
    out = _run_on_df(cfg, df, long_raw=long)
    assert out["metrics"]["total_entries"] == 1


def test_confirmation_break_buffer_ticks_can_block_entry():
    cfg = MTCConfig()
    cfg.trade.entry_mode = "Edge"
    cfg.stop_loss.enabled = False
    cfg.take_profit.enabled = False
    cfg.trailing.enabled = False
    cfg.break_even.enabled = False
    cfg.time_stop.enabled = False
    cfg.strategy.slippage_ticks = 0
    cfg.strategy.mintick = 1.0
    cfg.confirmation.enabled = True
    cfg.confirmation.p_left = 2
    cfg.confirmation.p_right = 2
    cfg.confirmation.atr_len = 3
    cfg.confirmation.mom_atr_mult = 0.0
    cfg.confirmation.break_buffer_ticks = 1

    long = [False] * 12 + [True] + [False] * 3
    out = _run(cfg, long_raw=long)
    assert out["metrics"]["total_entries"] == 0

