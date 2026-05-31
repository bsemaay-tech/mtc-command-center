#!/usr/bin/env python3
"""Quick parity check between Pine logic and Python logic."""

import math
from datetime import datetime
from mtc_v2.core.runner import Runner
from mtc_v2.core.types import Bar


def _build_config(**overrides):
    config = {
        "enable_long": True,
        "enable_short": True,
        "allow_flip": True,
        "regime_lock": False,
        "max_entries": 1,
        "cooldown_bars": 0,
        "warmup_bars_override": None,
        "signal_mode": "Supertrend",
        "st_atr_len": 3,
        "st_factor": 1.0,
        "st_use_wicks": False,
        "st_use_ha": False,
    }
    config.update(overrides)
    return config


def test_basic_sequence():
    """Test a basic sequence that should produce deterministic results."""
    bars = [
        Bar(datetime(2025, 1, 1), 100.0, 105.0, 95.0, 102.0, 1000, 0),
        Bar(datetime(2025, 1, 2), 102.0, 108.0, 101.0, 107.0, 1100, 1),
        Bar(datetime(2025, 1, 3), 107.0, 112.0, 106.0, 110.0, 1200, 2),
        Bar(datetime(2025, 1, 4), 110.0, 115.0, 109.0, 114.0, 1300, 3),
        Bar(datetime(2025, 1, 5), 114.0, 116.0, 110.0, 112.0, 1400, 4),
        Bar(datetime(2025, 1, 6), 112.0, 113.0, 108.0, 109.0, 1500, 5),
    ]
    
    runner = Runner(_build_config(st_atr_len=3, st_factor=2.0))
    signals = runner.run(bars)
    
    print("Python outputs:")
    for i, sig in enumerate(signals):
        line_str = f"{sig.line:.4f}" if sig.line is not None else "None"
        print(f"  Bar {i}: long={sig.long}, short={sig.short}, dir={sig.direction}, "
              f"line={line_str}, reason={sig.reason}")
    
    # Expected based on Pine logic (manually calculated)
    # Bar 0-1: warmup (ATR len=3)
    # Bar 2: first ATR, direction init to 1
    # Bar 3: hold long
    # Bar 4: potential flip? need to calculate
    
    print("\nChecking warmup behavior:")
    assert signals[0].reason == "st_warmup"
    assert signals[1].reason == "st_warmup"
    assert signals[2].reason == "st_direction_init"
    assert signals[2].direction == 1
    assert not signals[2].long and not signals[2].short
    
    print("Warmup and first direction correct.")


def test_invalid_bar_preserves_state():
    """Test that invalid bars preserve previous state."""
    bars = [
        Bar(datetime(2025, 1, 1), 100.0, 105.0, 95.0, 102.0, 1000, 0),
        Bar(datetime(2025, 1, 2), 102.0, 108.0, 101.0, 107.0, 1100, 1),
        Bar(datetime(2025, 1, 3), 107.0, 112.0, 106.0, 110.0, 1200, 2),  # warmup completes
        Bar(datetime(2025, 1, 4), 110.0, 115.0, 109.0, 114.0, 1300, 3),  # valid, direction=1
        Bar(datetime(2025, 1, 5), math.nan, math.nan, math.nan, math.nan, 0, 4),  # invalid
        Bar(datetime(2025, 1, 6), 114.0, 116.0, 113.0, 115.0, 1400, 5),  # should continue from bar 3 state
    ]
    
    runner = Runner(_build_config(st_atr_len=3))
    signals = runner.run(bars)
    
    print("\nInvalid bar test:")
    for i, sig in enumerate(signals):
        print(f"  Bar {i}: reason={sig.reason}, dir={sig.direction}")
    
    # Bar 4 should be invalid
    assert signals[4].reason == "st_invalid_bar"
    # Bar 5 should have same direction as bar 3 (long)
    assert signals[5].direction == 1
    assert signals[5].reason == "st_hold_long"
    
    print("Invalid bar preserves state correctly.")


if __name__ == "__main__":
    test_basic_sequence()
    test_invalid_bar_preserves_state()
    print("\nAll parity checks passed.")