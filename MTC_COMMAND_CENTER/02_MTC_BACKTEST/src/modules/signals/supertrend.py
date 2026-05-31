"""
Supertrend Signal Plugin.

Implements the Supertrend signal module matching MTC's LIB_Signal_Supertrend_Fix.
Generates longSignal_raw and shortSignal_raw based on Supertrend direction state.
"""

from typing import Tuple, Dict
import pandas as pd
import numpy as np

from .base import SignalPlugin
from ...engine.indicators import atr, supertrend as calc_supertrend, heikin_ashi


class SupertrendSignal(SignalPlugin):
    """
    Supertrend signal generator.
    
    Matches MTC Section 4 Supertrend mode:
    - Uses ATR-based Supertrend indicator
    - Optional Heikin Ashi candles
    - Raw outputs are level signals (dir state), matching Pine library contract
    
    Parameters:
        atr_len: ATR length for Supertrend (default: 21)
        factor: Supertrend factor/multiplier (default: 4.0)
        use_wicks: Use high/low for band touches (default: True)
        use_ha: Use Heikin Ashi candles (default: True)
    """
    
    def __init__(
        self,
        atr_len: int = 21,
        factor: float = 4.0,
        use_wicks: bool = True,
        use_ha: bool = True,
    ):
        super().__init__(
            name="Supertrend",
            atr_len=atr_len,
            factor=factor,
            use_wicks=use_wicks,
            use_ha=use_ha,
        )
        self.atr_len = atr_len
        self.factor = factor
        self.use_wicks = use_wicks
        self.use_ha = use_ha
        
        # Cache for debug series
        self._last_debug: Dict[str, pd.Series] = {}
    
    def generate(
        self,
        df: pd.DataFrame
    ) -> Tuple[pd.Series, pd.Series]:
        """
        Generate raw Supertrend signals.
        
        Args:
            df: OHLCV DataFrame
            
        Returns:
            (longSignal_raw, shortSignal_raw) - level signals from direction state
        """
        # Get OHLC data
        if self.use_ha:
            ha_open, ha_high, ha_low, ha_close = heikin_ashi(
                df['open'], df['high'], df['low'], df['close']
            )
            open_ = ha_open
            high = ha_high
            low = ha_low
            close = ha_close
        else:
            open_ = df['open']
            high = df['high']
            low = df['low']
            close = df['close']
        
        # Calculate Supertrend
        st_line, st_direction = calc_supertrend(
            open_=open_,
            high=high,
            low=low,
            close=close,
            atr_length=self.atr_len,
            factor=self.factor,
            use_wicks=self.use_wicks
        )
        
        # Store for debug
        self._last_debug = {
            'supertrend_line': st_line,
            'supertrend_direction': st_direction,
            'atr': atr(high, low, close, self.atr_len),
        }
        
        if self.use_ha:
            self._last_debug.update({
                'ha_open': ha_open,
                'ha_high': ha_high,
                'ha_low': ha_low,
                'ha_close': ha_close,
            })
        
        # Pine contract: Supertrend module exports level/raw trend state.
        # Edge conversion belongs to entry_mode handling in the engine.
        long_signal_raw = st_direction == 1
        short_signal_raw = st_direction == -1
        
        long_signal_raw = long_signal_raw.fillna(False)
        short_signal_raw = short_signal_raw.fillna(False)
        
        return long_signal_raw, short_signal_raw
    
    def get_debug_series(self, df: pd.DataFrame) -> Dict[str, pd.Series]:
        """
        Get internal series for parity debugging.
        
        Returns:
            Dict with:
            - supertrend_line: The Supertrend line values
            - supertrend_direction: Direction (1=bullish, -1=bearish)
            - atr: ATR values
            - ha_*: Heikin Ashi OHLC (if use_ha=True)
        """
        if not self._last_debug:
            # Generate to populate debug series
            self.generate(df)
        
        return self._last_debug.copy()
    
    def get_direction(self, df: pd.DataFrame) -> pd.Series:
        """
        Get Supertrend direction series.
        
        Returns:
            Series with 1 for bullish, -1 for bearish
        """
        if 'supertrend_direction' not in self._last_debug:
            self.generate(df)
        return self._last_debug['supertrend_direction']
    
    @classmethod
    def get_param_space(cls) -> Dict[str, Dict]:
        """Get optimization parameter space."""
        return {
            'atr_len': {
                'type': 'int',
                'low': 7,
                'high': 50,
                'step': 1,
            },
            'factor': {
                'type': 'float',
                'low': 1.0,
                'high': 8.0,
                'step': 0.5,
            },
            'use_wicks': {
                'type': 'bool',
            },
            'use_ha': {
                'type': 'bool',
            },
        }
    
    def validate_params(self) -> Tuple[bool, str]:
        """Validate Supertrend parameters."""
        if self.atr_len < 1:
            return False, "atr_len must be >= 1"
        if self.factor <= 0:
            return False, "factor must be > 0"
        return True, None
    
    def __repr__(self):
        return (
            f"SupertrendSignal(atr_len={self.atr_len}, factor={self.factor}, "
            f"use_wicks={self.use_wicks}, use_ha={self.use_ha})"
        )
