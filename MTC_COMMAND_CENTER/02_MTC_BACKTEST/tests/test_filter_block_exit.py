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


class _StubFilterChain:
    def __init__(self, allow_long: pd.Series, allow_short: pd.Series, name: str = "MA_Filter"):
        self.allow_long = allow_long
        self.allow_short = allow_short
        self.name = name

    def apply_with_details(self, df: pd.DataFrame):
        details = {self.name: (self.allow_long, self.allow_short)}
        return self.allow_long, self.allow_short, details


def _df() -> pd.DataFrame:
    ts = pd.date_range("2026-01-01", periods=4, freq="15min", tz="UTC")
    close = [100.0, 100.1, 100.2, 100.3]
    open_ = [100.0, 100.0, 100.1, 100.2]
    high = [100.2, 100.3, 100.4, 100.5]
    low = [99.8, 99.9, 100.0, 100.1]
    return pd.DataFrame(
        {
            "timestamp": ts,
            "open": open_,
            "high": high,
            "low": low,
            "close": close,
            "volume": [100, 100, 100, 100],
        }
    )


def _base_cfg() -> MTCConfig:
    cfg = MTCConfig()
    cfg.trade.entry_mode = "Edge"
    cfg.stop_loss.enabled = False
    cfg.take_profit.enabled = False
    cfg.trailing.enabled = False
    cfg.break_even.enabled = False
    cfg.time_stop.enabled = False
    cfg.strategy.slippage_ticks = 0
    return cfg


def test_filter_block_exit_global_switch_closes_position():
    cfg = _base_cfg()
    cfg.trade.exit_on_filter_block = True
    runner = MTCRunner(cfg)
    df = _df()

    runner.signal_plugin = _StubSignal(
        pd.Series([True, False, False, False]),
        pd.Series([False, False, False, False]),
    )
    runner.filter_chain = _StubFilterChain(
        allow_long=pd.Series([True, False, False, False]),
        allow_short=pd.Series([True, True, True, True]),
    )
    out = runner.run(df, warmup_bars=0)
    assert out["metrics"]["total_trades"] == 1
    assert out["trades_all"][0].exit_reason.value == "FILTER_BLOCK"


def test_filter_block_exit_granular_switch_closes_position():
    cfg = _base_cfg()
    cfg.trade.exit_on_filter_block = False
    cfg.exit_filter_block.exit_on_ma_block = True
    runner = MTCRunner(cfg)
    df = _df()

    runner.signal_plugin = _StubSignal(
        pd.Series([True, False, False, False]),
        pd.Series([False, False, False, False]),
    )
    runner.filter_chain = _StubFilterChain(
        allow_long=pd.Series([True, False, False, False]),
        allow_short=pd.Series([True, True, True, True]),
        name="MA_Filter",
    )
    out = runner.run(df, warmup_bars=0)
    assert out["metrics"]["total_trades"] == 1
    assert out["trades_all"][0].exit_reason.value == "FILTER_BLOCK"
