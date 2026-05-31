import pytest
from mtc_v2.core.runner import Runner
from mtc_v2.core.types import Bar, RawSignal
from mtc_v2.core.config import DEFAULT_CONFIG

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

def _make_bar(close: float, idx: int, high: float = None, low: float = None, volume: float = 100.0) -> Bar:
    from datetime import datetime
    import pytz
    if high is None: high = close
    if low is None: low = close
    return Bar(
        bar_index=idx,
        timestamp=datetime.now(pytz.UTC),
        open=close,
        high=high,
        low=low,
        close=close,
        volume=volume
    )

def test_disabled_passthrough():
    runner = _make_runner({"use_level_retest": False})
    def mock_calc(bar):
        from mtc_v2.core.types import RawSignal
        return RawSignal(long=True, short=False, line=100.0, reason="")
    runner.signal_producer.calculate = mock_calc

    outputs = runner.run([_make_bar(100, 1)])
    assert outputs[0].long


def test_signal_suppressed_until_retest():
    runner = _make_runner({"use_level_retest": True, "retest_timeout_bars": 50, "retest_buffer_pct": 0.1, "use_confirm_transform": False})
    def mock_calc(bar):
        from mtc_v2.core.types import RawSignal
        # Fire signal at line 100
        return RawSignal(long=True, short=False, line=100.0, reason="")
    runner.signal_producer.calculate = mock_calc

    # Bar 1: close = 105 (signal fires, but L21 grabs it, output long is False)
    # L21 Break level = 100.0
    outputs = runner.run([_make_bar(105, 1)])
    assert not outputs[0].long

def test_retest_confirms_long():
    runner = _make_runner({"use_level_retest": True, "retest_timeout_bars": 50, "retest_buffer_pct": 1.0, "use_confirm_transform": False})
    def mock_calc(bar):
        from mtc_v2.core.types import RawSignal
        return RawSignal(long=True, short=False, line=100.0, reason="")
    runner.signal_producer.calculate = mock_calc

    # Bar 1: close 105 (fires, waits). Bar 2: close 103 (waits). Bar 3: close 100.5 (within 1% of 100.0), long should fire
    outputs = runner.run([_make_bar(105, 1), _make_bar(103, 2), _make_bar(100.5, 3)])
    assert not outputs[0].long
    assert not outputs[1].long
    assert outputs[2].long

def test_timeout_cancels_waiting():
    runner = _make_runner({"use_level_retest": True, "retest_timeout_bars": 2, "retest_buffer_pct": 1.0, "use_confirm_transform": False})
    def mock_calc(bar):
        from mtc_v2.core.types import RawSignal
        return RawSignal(long=True, short=False, line=100.0, reason="")
    runner.signal_producer.calculate = mock_calc

    # Bar 1: close 105 -> wait, bars_waiting=0
    # Bar 2: close 105 -> wait, bars_waiting=1
    # Bar 3: close 105 -> wait, bars_waiting=2 (timeout reached, resets, no entry)
    outputs = runner.run([_make_bar(105, 1), _make_bar(105, 2), _make_bar(105, 3)])
    assert not any(o.long for o in outputs)
    assert not runner._l21_waiting

def test_opposing_signal_cancels():
    runner = _make_runner({"use_level_retest": True, "retest_timeout_bars": 10, "retest_buffer_pct": 1.0, "use_confirm_transform": False})
    def mock_calc(bar):
        from mtc_v2.core.types import RawSignal
        if bar.bar_index == 1:
            return RawSignal(long=True,  short=False, line=100.0, reason="")
        elif bar.bar_index == 2:
            return RawSignal(long=False, short=True,  line=100.0, reason="")
        return RawSignal(long=False, short=False, line=100.0, reason="")
    runner.signal_producer.calculate = mock_calc

    outputs = runner.run([_make_bar(105, 1), _make_bar(105, 2)])
    assert not runner._l21_waiting  # Opposing signal cancelled the long wait state

