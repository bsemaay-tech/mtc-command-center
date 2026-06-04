from src.config.defaults import MTCConfig
from src.config.profiles.light_risk import build_light_risk_config


def test_light_risk_profile_filters_guards_off_and_risk_on():
    cfg = build_light_risk_config()

    filter_flags = [
        cfg.filters.use_ma_filter,
        cfg.filters.ma_use_higher_timeframe,
        cfg.filters.use_ma_slope_filter,
        cfg.filters.use_volume_filter,
        cfg.filters.use_atr_vol_filter,
        cfg.filters.use_mcginley_filter,
        cfg.filters.use_mcginley_htf,
        cfg.filters.use_htf_trend_filter,
        cfg.filters.use_macd_filter,
        cfg.filters.macd_use_htf_bias,
        cfg.filters.use_range_filters,
        cfg.filters.use_range_regime_filter,
        cfg.filters.adx_use_higher_timeframe,
        cfg.filters.chop_use_higher_timeframe,
    ]
    guard_flags = [
        cfg.guards.use_dd_guard,
        cfg.guards.use_consec_loss_guard,
        cfg.guards.use_cooldown_guard,
        cfg.guards.use_eq_curve_guard,
        cfg.guards.use_mae_guard,
        cfg.guards.use_guard_recovery,
        cfg.risk.use_daily_loss_limit,
        cfg.risk.use_max_trades_per_day,
        cfg.time_stop.enabled,
        cfg.time_stop.use_bars,
        cfg.time_stop.eod,
        cfg.time_stop.eow,
        cfg.trade.use_regime_lock,
        cfg.trade.exit_on_filter_block,
    ]

    assert not any(filter_flags)
    assert not any(guard_flags)
    assert cfg.stop_loss.enabled is True
    assert cfg.take_profit.enabled is True
    assert cfg.break_even.enabled is True
    assert cfg.multi_tp.enabled is True
    assert cfg.trailing.enabled is True


def test_light_risk_profile_overrides_do_not_mutate_defaults():
    default = MTCConfig()
    cfg = build_light_risk_config(
        {
            "stop_loss.mode": "%",
            "stop_loss.percent": 2.5,
            "take_profit": {"mode": "%", "percent": 5.0},
            "multi_tp.use_multi_tp": False,
        }
    )

    assert cfg.stop_loss.mode == "%"
    assert cfg.stop_loss.percent == 2.5
    assert cfg.take_profit.mode == "%"
    assert cfg.take_profit.percent == 5.0
    assert cfg.multi_tp.enabled is False
    assert default.stop_loss.mode == "ATR"
    assert default.multi_tp.enabled is True
