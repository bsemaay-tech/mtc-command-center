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
    return pd.DataFrame(
        {
            "timestamp": ts,
            "open": [100.0, 100.0, 100.1, 100.2, 100.3, 100.4],
            "high": [100.2, 101.5, 101.6, 100.8, 100.7, 100.7],
            "low": [99.8, 99.9, 100.0, 100.1, 100.2, 100.3],
            "close": [100.0, 100.2, 100.1, 100.3, 100.4, 100.5],
            "volume": [100] * 6,
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
    cfg.guards.use_dd_guard = True
    cfg.guards.dd_guard_pct = 0.0  # always blocks unless recovery bypasses
    cfg.guards.use_guard_recovery = True
    return cfg


def test_guard_recovery_bars_mode_allows_entry_after_n_blocked_signals():
    cfg = _base_cfg()
    cfg.guards.guard_recovery_mode = "Bars"
    cfg.guards.guard_recovery_bars = 1
    runner = MTCRunner(cfg)
    df = _df()
    runner.signal_plugin = _StubSignal(
        long_series=pd.Series([True, False, False, False, False, False]),
        short_series=pd.Series([False] * 6),
    )
    runner.filter_chain = _StubFilter()
    out = runner.run(df, warmup_bars=0)
    assert out["metrics"]["total_entries"] == 1


def test_guard_recovery_signals_mode_waits_for_signal_count():
    cfg = _base_cfg()
    cfg.guards.guard_recovery_mode = "Signals"
    cfg.guards.guard_recovery_signals = 2
    runner = MTCRunner(cfg)
    df = _df()
    runner.signal_plugin = _StubSignal(
        long_series=pd.Series([True, False, True, False, False, False]),
        short_series=pd.Series([False] * 6),
    )
    runner.filter_chain = _StubFilter()
    out = runner.run(df, warmup_bars=0)
    assert out["metrics"]["total_entries"] == 1


def test_guard_recovery_virtual_mode_allows_entry_after_virtual_tp():
    cfg = _base_cfg()
    cfg.trade.entry_mode = "Signal"
    cfg.guards.guard_recovery_mode = "Virtual Trade"
    runner = MTCRunner(cfg)
    df = _df()
    runner.signal_plugin = _StubSignal(
        long_series=pd.Series([True, True, True, False, False, False]),
        short_series=pd.Series([False] * 6),
    )
    runner.filter_chain = _StubFilter()
    out = runner.run(df, warmup_bars=0)
    assert out["metrics"]["total_entries"] >= 1
