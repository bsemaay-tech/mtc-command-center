from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone

import pandas as pd

from src.config.defaults import MTCConfig
from src.engine.mtc_runner import MTCRunner


@dataclass
class _StubSignal:
    long_series: pd.Series
    short_series: pd.Series

    def generate(self, df: pd.DataFrame) -> tuple[pd.Series, pd.Series]:
        return self.long_series, self.short_series


class _StubFilter:
    def __init__(self, allow: pd.Series):
        self.allow = allow

    def apply_with_details(self, df: pd.DataFrame):
        return self.allow, self.allow, {}


def _base_df() -> pd.DataFrame:
    ts = pd.date_range(start=datetime(2026, 1, 1, tzinfo=timezone.utc), periods=3, freq="15min")
    return pd.DataFrame(
        {
            "timestamp": ts,
            "open": [100.0, 100.0, 100.0],
            "high": [100.0, 110.0, 110.0],
            "low": [100.0, 100.0, 100.0],
            "close": [100.0, 110.0, 110.0],
            "volume": [1.0, 1.0, 1.0],
        }
    )


def _run_one_trade(config: MTCConfig) -> dict:
    df = _base_df()
    runner = MTCRunner(config)
    allow = pd.Series([True] * len(df))
    runner.signal_plugin = _StubSignal(
        long_series=pd.Series([True, False, False]),
        short_series=pd.Series([False, False, False]),
    )
    runner.filter_chain = _StubFilter(allow)
    return runner.run(df, warmup_bars=0)


def _single_trade(out: dict):
    assert out["metrics"]["total_trades"] == 1
    return out["trades_all"][0]


def _base_config() -> MTCConfig:
    cfg = MTCConfig()
    cfg.trade.entry_mode = "Edge"
    cfg.stop_loss.enabled = False
    cfg.take_profit.enabled = False
    cfg.trailing.enabled = False
    cfg.break_even.enabled = False
    cfg.time_stop.enabled = True
    cfg.time_stop.bars = 1
    cfg.time_stop.condition = "Always"
    cfg.strategy.mintick = 1.0
    cfg.strategy.slippage_ticks = 0
    cfg.strategy.commission_percent = 0.0
    return cfg


def test_slippage_ticks_reduce_long_trade_pnl_deterministically():
    no_slip_cfg = _base_config()
    no_slip_out = _run_one_trade(no_slip_cfg)
    no_slip_trade = _single_trade(no_slip_out)

    with_slip_cfg = _base_config()
    with_slip_cfg.strategy.slippage_ticks = 2
    with_slip_out = _run_one_trade(with_slip_cfg)
    with_slip_trade = _single_trade(with_slip_out)

    # Buy entry worsens by +2, sell exit worsens by -2 => 4 points less per unit.
    assert with_slip_trade.entry_price == no_slip_trade.entry_price + 2.0
    assert with_slip_trade.exit_price == no_slip_trade.exit_price - 2.0
    expected_delta = -4.0 * no_slip_trade.quantity
    actual_delta = with_slip_trade.pnl - no_slip_trade.pnl
    assert abs(actual_delta - expected_delta) < 1e-9


def test_commission_percent_applies_entry_and_exit_fees():
    no_fee_cfg = _base_config()
    no_fee_out = _run_one_trade(no_fee_cfg)
    no_fee_trade = _single_trade(no_fee_out)

    fee_cfg = _base_config()
    fee_cfg.strategy.commission_percent = 0.1
    fee_out = _run_one_trade(fee_cfg)
    fee_trade = _single_trade(fee_out)

    commission_cost = (
        (no_fee_trade.entry_price * no_fee_trade.quantity * 0.1 / 100.0)
        + (no_fee_trade.exit_price * no_fee_trade.quantity * 0.1 / 100.0)
    )
    actual_delta = no_fee_trade.pnl - fee_trade.pnl
    assert abs(actual_delta - commission_cost) < 1e-9
