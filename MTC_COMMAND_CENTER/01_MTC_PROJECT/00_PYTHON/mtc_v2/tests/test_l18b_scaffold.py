from __future__ import annotations

from datetime import datetime

import pytz

from mtc_v2.core.config import DEFAULT_CONFIG
from mtc_v2.core.runner import Runner
from mtc_v2.core.types import Bar, RawSignal


def _make_bar(close: float, idx: int) -> Bar:
    return Bar(
        bar_index=idx,
        timestamp=datetime.now(pytz.UTC),
        open=close,
        high=close,
        low=close,
        close=close,
        volume=100.0,
    )


def _make_runner(overrides: dict[str, object] | None = None) -> Runner:
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
    cfg["use_confirm_transform"] = False
    cfg["use_level_retest"] = False
    if overrides:
        cfg.update(overrides)
    return Runner(cfg)


def test_l18b_config_keys_exist() -> None:
    runner = _make_runner()
    assert "use_l18b_confirmation" in runner.config
    assert "l18b_swing_left" in runner.config
    assert "l18b_swing_right" in runner.config
    assert "l18b_timeout_bars" in runner.config
    assert "l18b_raw_event_mode" in runner.config
    assert runner.config["use_l18b_confirmation"] is False


def test_l18b_scaffold_is_noop_by_default() -> None:
    runner = _make_runner()

    def mock_calc(_: Bar) -> RawSignal:
        return RawSignal(long=True, short=False, line=10.0, reason="seed")

    runner.signal_producer.calculate = mock_calc
    outputs = runner.run([_make_bar(100.0, 1), _make_bar(101.0, 2)])
    assert outputs[0].long is True
    assert outputs[1].long is True


def test_l18b_scaffold_can_be_enabled_without_changing_output() -> None:
    runner = _make_runner({"use_l18b_confirmation": True})

    def mock_calc(_: Bar) -> RawSignal:
        return RawSignal(long=True, short=False, line=10.0, reason="seed")

    runner.signal_producer.calculate = mock_calc
    outputs = runner.run([_make_bar(100.0, 1), _make_bar(101.0, 2)])
    assert outputs[0].long is True
    assert outputs[1].long is True
    assert runner._l18b_state.direction == 1
    assert runner._l18b_snapshot.enabled is True
