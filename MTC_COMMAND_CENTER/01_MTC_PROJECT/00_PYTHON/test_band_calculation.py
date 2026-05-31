#!/usr/bin/env python3
"""Test band calculation parity between Pine and Python."""

import math
from datetime import datetime
from mtc_v2.core.runner import Runner
from mtc_v2.core.types import Bar
from mtc_v2.signals.supertrend import SupertrendSignal


def test_band_calculation_edge_case():
    """Test the edge case where prev_close is None vs current close."""
    # Create a scenario where:
    # 1. Warmup completes
    # 2. First band calculation occurs
    # 3. Check if band logic uses correct previous close
    
    config = {
        "st_atr_len": 2,
        "st_factor": 1.0,
        "st_use_wicks": False,
        "st_use_ha": False,
    }
    
    signal = SupertrendSignal(config)
    
    # Manually simulate Pine logic for first band calculation
    # Bar 0: warmup bar 1
    bar0 = Bar(datetime(2025, 1, 1), 100.0, 105.0, 95.0, 102.0, 1000, 0)
    sig0 = signal.calculate(bar0)
    print(f"Bar 0: reason={sig0.reason}, prev_close={signal._prev_close}")
    
    # Bar 1: warmup completes (ATR len=2)
    bar1 = Bar(datetime(2025, 1, 2), 102.0, 108.0, 101.0, 107.0, 1100, 1)
    sig1 = signal.calculate(bar1)
    print(f"Bar 1: reason={sig1.reason}, prev_close={signal._prev_close}, "
          f"prev_upper={signal._prev_upper_band}, prev_lower={signal._prev_lower_band}")
    
    # Bar 2: first band calculation with previous bands available
    bar2 = Bar(datetime(2025, 1, 3), 107.0, 112.0, 106.0, 110.0, 1200, 2)
    sig2 = signal.calculate(bar2)
    print(f"Bar 2: reason={sig2.reason}, prev_close={signal._prev_close}, "
          f"prev_upper={signal._prev_upper_band}, prev_lower={signal._prev_lower_band}")
    
    # Calculate what Pine would do:
    # Pine uses st_prev_close_for_bands = na(st_prev_close_state) ? close : st_prev_close_state
    # At bar 2, st_prev_close_state is bar1's close (107.0), not na
    # So st_prev_close_for_bands = 107.0
    # Python uses self._prev_close which is also 107.0
    
    # The condition for upper band:
    # Pine: basic_upper < prev_upper or st_prev_close_for_bands > prev_upper
    # Python: basic_upper < prev_upper or self._prev_close > prev_upper
    
    # They should be identical in this case
    print("\nBand calculation should match between Pine and Python for this case.")
    
    # Now test a case where prev_close_state is na (shouldn't happen in normal flow)
    # Reset signal
    signal = SupertrendSignal(config)
    
    # Manually set state to simulate Pine's na(st_prev_close_state) scenario
    signal._prev_close = None
    signal._prev_upper_band = 110.0
    signal._prev_lower_band = 90.0
    signal._prev_atr = 5.0
    signal._prev_direction = 1
    signal._trs = deque([4.0, 6.0])  # ATR len=2
    
    # Calculate a bar
    bar = Bar(datetime(2025, 1, 1), 100.0, 105.0, 95.0, 102.0, 1000, 0)
    
    # In Pine, st_prev_close_for_bands would use current close (102.0)
    # In Python, self._prev_close is None, so _next_upper_band returns basic_upper
    # This is a divergence!
    
    print("\nEdge case with prev_close=None:")
    print("Pine would use current close for band comparison")
    print("Python returns basic_upper (no comparison)")
    print("This could cause divergence in band values.")
    

if __name__ == "__main__":
    from collections import deque
    test_band_calculation_edge_case()