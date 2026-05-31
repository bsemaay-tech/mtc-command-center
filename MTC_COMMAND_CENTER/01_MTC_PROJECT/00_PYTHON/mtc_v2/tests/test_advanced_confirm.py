import pytest
from mtc_v2.core.runner import Runner
from mtc_v2.core.config import DEFAULT_CONFIG
from mtc_v2.core.types import Bar

def _make_runner(overrides: dict) -> Runner:
    cfg = dict(DEFAULT_CONFIG)
    cfg["use_ma_filter"] = False
    cfg["use_ma_slope_filter"] = False
    cfg["use_mcginley_filter"] = False
    cfg["use_volume_filter"] = False
    cfg["use_adx_filter"] = False
    cfg["use_chop_filter"] = False
    cfg["use_atr_vol_floor"] = False
    cfg["use_macd_regime_filter"] = False
    cfg["use_macd_cross_filter"] = False
    cfg["use_macd_hist_filter"] = False
    cfg["use_macd_zero_dist_filter"] = False
    cfg["use_candle_pattern_gate"] = False
    cfg["use_level_proximity_gate"] = False
    cfg.update(overrides)
    return Runner(cfg)

def _make_bar(close: float, idx: int) -> Bar:
    from datetime import datetime
    import pytz
    return Bar(
        bar_index=idx,
        timestamp=datetime.now(pytz.UTC),
        open=close,
        high=close,
        low=close,
        close=close,
        volume=100.0,
    )

def test_require_raw_still_true_blocks_when_raw_gone():
    runner = _make_runner({"use_confirm_transform": True, "confirm_bars": 2, "require_raw_still_true": True, "confirm_close_crosses": False})
    
    # Use a dummy wrapper for signal_producer
    def mock_calc(bar):
        from mtc_v2.core.types import RawSignal
        # Long only on bar 1
        return RawSignal(long=(bar.bar_index == 1), short=False, line=10, reason="")
    runner.signal_producer.calculate = mock_calc

    outputs = runner.run([_make_bar(100, 1), _make_bar(100, 2)])
    assert len(outputs) == 2
    assert not outputs[1].long  # Blocked because bar 2 raw.long is False

def test_require_raw_still_true_passes_when_raw_active():
    runner = _make_runner({"use_confirm_transform": True, "confirm_bars": 2, "require_raw_still_true": True, "confirm_close_crosses": False})
    
    def mock_calc(bar):
        from mtc_v2.core.types import RawSignal
        # Long on both bar 1, 2
        return RawSignal(long=(bar.bar_index <= 2), short=False, line=10, reason="")
    runner.signal_producer.calculate = mock_calc

    outputs = runner.run([_make_bar(100, 1), _make_bar(100, 2)])
    assert outputs[1].long  # Passes

def test_refresh_on_new_raw_resets_count():
    # Pine-correct behavior: refresh runs unconditionally (outside if/else), so on the
    # direction-change bar the count is set to 1 then immediately reset to 0.
    # With confirm_bars=2 and a level signal (long from bar 30 onwards, past warmup):
    #   Bar 30: direction→1, count=1, refresh resets count=0  → not armed
    #   Bar 31: count=1, prev_long=T → no refresh reset → not armed (1 < 2)
    #   Bar 32: count=2 → armed → fires
    # Use st_atr_len=2 so warmup completes within the first few bars.
    runner = _make_runner({"use_confirm_transform": True, "confirm_bars": 2,
                           "refresh_on_new_raw": True, "confirm_close_crosses": False,
                           "st_atr_len": 2})

    flip_bar = 30
    def mock_calc(bar):
        from mtc_v2.core.types import RawSignal
        is_long = bar.bar_index >= flip_bar
        # direction must be non-None so warmup_ready=True (see _signal_indicator_snapshot fallback)
        return RawSignal(long=is_long, short=False, line=10.0, reason="", direction=1 if is_long else -1)
    runner.signal_producer.calculate = mock_calc
    # Null out indicator_snapshot so _signal_indicator_snapshot uses the fallback path
    # (warmup_ready = raw.direction is not None), preventing real Supertrend warmup from blocking.
    runner.signal_producer.indicator_snapshot = None

    bars = [_make_bar(100, i) for i in range(1, flip_bar + 3)]
    outputs = runner.run(bars)
    # bar at index flip_bar-1 (0-based): direction-change bar, count reset to 0 by refresh
    assert not outputs[flip_bar - 1].long   # bar 30: count=0 after refresh, not armed
    assert not outputs[flip_bar].long       # bar 31: count=1, below confirm_bars=2
    assert outputs[flip_bar + 1].long       # bar 32: count=2, armed and fires

def test_both_options_disabled_unchanged_behavior():
    runner = _make_runner({"use_confirm_transform": True, "confirm_bars": 2, "require_raw_still_true": False, "refresh_on_new_raw": False, "confirm_close_crosses": False})
    
    def mock_calc(bar):
        from mtc_v2.core.types import RawSignal
        return RawSignal(long=True, short=False, line=10, reason="")
    runner.signal_producer.calculate = mock_calc

    outputs = runner.run([_make_bar(100, 1), _make_bar(100, 2)])
    assert outputs[1].long

