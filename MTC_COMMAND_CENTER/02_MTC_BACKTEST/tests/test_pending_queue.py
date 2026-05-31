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
    def apply_with_details(self, df: pd.DataFrame):
        allow = pd.Series([True] * len(df))
        return allow, allow, {}


def _df() -> pd.DataFrame:
    ts = pd.date_range("2026-01-01", periods=6, freq="15min", tz="UTC")
    close = [100.0, 100.2, 100.1, 99.9, 99.7, 99.6]
    open_ = [100.0, 100.0, 100.2, 100.1, 99.9, 99.7]
    high = [100.2, 100.3, 100.3, 100.1, 99.9, 99.8]
    low = [99.8, 99.9, 99.9, 99.7, 99.5, 99.4]
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


def _base_cfg() -> MTCConfig:
    cfg = MTCConfig()
    cfg.trade.entry_mode = "Edge"
    cfg.stop_loss.enabled = False
    cfg.take_profit.enabled = False
    cfg.trailing.enabled = False
    cfg.break_even.enabled = False
    cfg.time_stop.enabled = True
    cfg.time_stop.bars = 2
    cfg.time_stop.condition = "Always"
    cfg.strategy.slippage_ticks = 0
    return cfg


def test_pending_queue_opens_opposite_after_flat_when_allow_flip_false():
    cfg = _base_cfg()
    cfg.trade.allow_flip = False
    runner = MTCRunner(cfg)
    df = _df()
    runner.signal_plugin = _StubSignal(
        long_series=pd.Series([True, False, False, False, False, False]),
        short_series=pd.Series([False, True, False, False, False, False]),
    )
    runner.filter_chain = _StubFilter()
    out = runner.run(df, warmup_bars=0)

    assert out["metrics"]["total_entries"] == 2
    assert out["trades_all"][0].direction.value == "long"
    assert out["trades_all"][1].direction.value == "short"


def test_pending_queue_not_used_when_allow_flip_true():
    cfg = _base_cfg()
    cfg.trade.allow_flip = True
    runner = MTCRunner(cfg)
    df = _df()
    runner.signal_plugin = _StubSignal(
        long_series=pd.Series([True, False, False, False, False, False]),
        short_series=pd.Series([False, True, False, False, False, False]),
    )
    runner.filter_chain = _StubFilter()
    out = runner.run(df, warmup_bars=0)

    assert out["metrics"]["total_entries"] == 1
