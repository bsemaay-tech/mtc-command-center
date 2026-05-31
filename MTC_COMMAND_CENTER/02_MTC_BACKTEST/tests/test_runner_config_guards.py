from src.config.defaults import MTCConfig
from src.engine.mtc_runner import MTCRunner
import pytest


def test_runner_uses_strategy_mintick_default_and_custom():
    cfg_default = MTCConfig()
    r_default = MTCRunner(cfg_default)
    assert r_default.mintick == 0.1

    cfg_custom = MTCConfig()
    cfg_custom.strategy.mintick = 0.01
    r_custom = MTCRunner(cfg_custom)
    assert r_custom.mintick == 0.01


def test_runner_allows_filter_block_exit_switches():
    cfg = MTCConfig()
    cfg.trade.exit_on_filter_block = True
    cfg.exit_filter_block.exit_on_ma_block = True
    cfg.exit_filter_block.exit_on_range_block = True
    MTCRunner(cfg)


def test_runner_allows_daily_and_mae_guards_now():
    cfg = MTCConfig()
    cfg.signal_mode = "Range Filter Hybrid"
    cfg.filters.use_htf_trend_filter = True
    cfg.risk.use_daily_loss_limit = True
    cfg.risk.use_max_trades_per_day = True
    cfg.guards.use_mae_guard = True
    cfg.time_stop.eod = True
    cfg.time_stop.eow = True
    MTCRunner(cfg)


@pytest.mark.parametrize(
    "field_name, value",
    [
        ("strategy.pyramiding", 2),
        ("trade.max_pyramid_positions", 2),
        ("trade.same_bar_reentry_max_per_bar", 2),
    ],
)
def test_runner_rejects_non_enforced_trade_limits(field_name: str, value: int):
    cfg = MTCConfig()
    if field_name == "strategy.pyramiding":
        cfg.strategy.pyramiding = value
    elif field_name == "trade.max_pyramid_positions":
        cfg.trade.max_pyramid_positions = value
    elif field_name == "trade.same_bar_reentry_max_per_bar":
        cfg.trade.same_bar_reentry_max_per_bar = value

    with pytest.raises(NotImplementedError):
        MTCRunner(cfg)
