"""Tests for L22 Candle Pattern Gate and L20 Level Proximity Gate."""
from types import SimpleNamespace
from mtc_v2.core.gates import (
    evaluate_candle_pattern_gate,
    evaluate_level_proximity_gate,
    GATE_CANDLE_PATTERN,
    GATE_LEVEL_PROXIMITY,
)

CFG_CP_ON  = {"use_candle_pattern_gate": True}
CFG_CP_OFF = {"use_candle_pattern_gate": False}
CFG_LP_ON  = {"use_level_proximity_gate": True, "level_proximity_threshold_pct": 1.0}
CFG_LP_OFF = {"use_level_proximity_gate": False}


def _bar(o, h, l, c):
    return SimpleNamespace(open=o, high=h, low=l, close=c)


def _cp_result(bar_open, bar_high, bar_low, bar_close, prev_open=None, prev_high=None, prev_low=None, prev_close=None, cfg=None):
    if prev_open is None:
        recent = []
    else:
        recent = [
            _bar(prev_open, prev_high or prev_open, prev_low or prev_open, prev_close),
            _bar(bar_open, bar_high, bar_low, bar_close),
        ]
    return evaluate_candle_pattern_gate(cfg or CFG_CP_ON, recent_bars=recent)


def test_gate_disabled_always_pass():
    r = _cp_result(100, 105, 95, 102, prev_open=103, prev_high=106, prev_low=98, prev_close=99, cfg=CFG_CP_OFF)
    assert r.long_ok and r.short_ok


def test_no_prev_bar_pass_through():
    r = _cp_result(100, 105, 95, 102)
    assert r.long_ok and r.short_ok


def test_bullish_engulf_allows_long():
    # prev: bearish (open=105, close=100), curr: bullish engulf (open=99, close=106)
    r = _cp_result(99, 107, 98, 106, prev_open=105, prev_high=106, prev_low=99, prev_close=100)
    assert r.long_ok
    assert not r.short_ok


def test_hammer_allows_long():
    # open=100, close=100.2 (body=0.2), high=100.3 (upper_wick=0.1 < 0.5*0.2=0.1, boundary — use stricter)
    # Use: open=100, close=100.2, high=100.25 (upper=0.05 < 0.5*0.2=0.1 OK), low=98 (lower=2.0 > 2*0.2=0.4 OK)
    r2 = _cp_result(100, 100.25, 98, 100.2, prev_open=103, prev_high=104, prev_low=102, prev_close=102.5)
    assert r2.long_ok


def test_bearish_engulf_allows_short():
    # prev: bullish (open=100, close=105), curr: bearish engulf (open=106, close=99)
    r = _cp_result(106, 107, 98, 99, prev_open=100, prev_high=106, prev_low=99, prev_close=105)
    assert r.short_ok
    assert not r.long_ok


def test_shooting_star_allows_short():
    # Large upper wick, small body, bearish close: open=100, close=99.8 (body=0.2), high=102 (upper=2.0), low=99.7
    # lower_wick = min(100, 99.8) - 99.7 = 99.8 - 99.7 = 0.1 < 0.5*0.2=0.1 boundary
    # Use low=99.75: lower_wick=0.05 < 0.1 OK
    r = _cp_result(100, 102, 99.75, 99.8, prev_open=100, prev_high=101, prev_low=99, prev_close=100.5)
    assert r.short_ok


def test_no_pattern_blocks_both():
    # Doji-like with equal open/close — no pattern
    r = _cp_result(100, 101, 99, 100, prev_open=100, prev_high=101, prev_low=99, prev_close=100)
    assert not r.long_ok
    assert not r.short_ok


# --- Level Proximity Gate ---

def test_lp_disabled_pass():
    r = evaluate_level_proximity_gate(CFG_LP_OFF, close=50, recent_highs=[60], recent_lows=[40])
    assert r.long_ok and r.short_ok


def test_lp_no_history_pass():
    r = evaluate_level_proximity_gate(CFG_LP_ON, close=50, recent_highs=[], recent_lows=[])
    assert r.long_ok and r.short_ok


def test_near_support_long_ok():
    # swing_low=100, close=100.5, threshold=1.0% -> dist=0.5% <= 1.0% -> long OK
    r = evaluate_level_proximity_gate(CFG_LP_ON, close=100.5, recent_highs=[120], recent_lows=[100])
    assert r.long_ok


def test_far_from_support_long_blocked():
    # swing_low=100, close=103, dist=3% > 1.0% -> long blocked
    r = evaluate_level_proximity_gate(CFG_LP_ON, close=103, recent_highs=[120], recent_lows=[100])
    assert not r.long_ok


def test_near_resistance_short_ok():
    # swing_high=120, close=119.5, dist=0.42% <= 1% -> short OK
    r = evaluate_level_proximity_gate(CFG_LP_ON, close=119.5, recent_highs=[120], recent_lows=[100])
    assert r.short_ok


def test_far_from_resistance_short_blocked():
    # swing_high=120, close=116, dist=3.3% > 1% -> short blocked
    r = evaluate_level_proximity_gate(CFG_LP_ON, close=116, recent_highs=[120], recent_lows=[100])
    assert not r.short_ok


def test_gate_names():
    r_cp = evaluate_candle_pattern_gate(CFG_CP_OFF, recent_bars=[])
    assert r_cp.gate_name == GATE_CANDLE_PATTERN
    r_lp = evaluate_level_proximity_gate(CFG_LP_OFF, close=50, recent_highs=[], recent_lows=[])
    assert r_lp.gate_name == GATE_LEVEL_PROXIMITY
