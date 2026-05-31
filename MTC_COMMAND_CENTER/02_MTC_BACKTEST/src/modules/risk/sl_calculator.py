"""
Stop Loss Calculator.

Calculates SL prices based on different modes matching MTC's SL logic.
"""

from typing import Optional, Literal
import pandas as pd
import numpy as np

from ...engine.indicators import atr


class SLCalculator:
    """
    Stop Loss price calculator.
    
    Supports all MTC SL modes:
    - ATR: SL = entry ± (ATR * mult)
    - %: SL = entry ± (entry * percent)
    - Swing+ATR: SL = swing low/high ± ATR buffer
    - SWING_ATR: Combined swing and ATR logic
    """
    
    def __init__(
        self,
        mode: Literal["ATR", "%", "Swing+ATR", "SWING_ATR"] = "ATR",
        atr_len: int = 14,
        atr_mult: float = 4.0,
        percent: float = 1.0,
        swing_lookback: int = 20,
        swing_atr_len: int = 14,
        swing_atr_mult: float = 0.5,
        swing_basis: Literal["Wick", "Body"] = "Wick",
    ):
        self.mode = mode
        self.atr_len = atr_len
        self.atr_mult = atr_mult
        self.percent = percent
        self.swing_lookback = swing_lookback
        self.swing_atr_len = swing_atr_len
        self.swing_atr_mult = swing_atr_mult
        self.swing_basis = swing_basis
    
    def calculate(
        self,
        df: pd.DataFrame,
        bar_index: int,
        direction: str,
        entry_price: float,
        atr_cache: dict = None,
    ) -> float:
        """
        Calculate SL price for a trade.
        
        Args:
            df: OHLCV DataFrame
            bar_index: Current bar index
            direction: "long" or "short"
            entry_price: Entry price
            atr_cache: Pre-computed ATR series keyed by length
            
        Returns:
            Stop loss price
        """
        is_long = direction == "long"
        
        if self.mode == "ATR":
            return self._calc_atr_sl(df, bar_index, entry_price, is_long, atr_cache=atr_cache)
        elif self.mode == "%":
            return self._calc_percent_sl(entry_price, is_long)
        elif self.mode in ("Swing+ATR", "SWING_ATR"):
            return self._calc_swing_sl(df, bar_index, entry_price, is_long, atr_cache=atr_cache)
        else:
            # Default to ATR
            return self._calc_atr_sl(df, bar_index, entry_price, is_long, atr_cache=atr_cache)
    
    def _calc_atr_sl(
        self,
        df: pd.DataFrame,
        bar_index: int,
        entry_price: float,
        is_long: bool,
        atr_cache: dict = None,
    ) -> float:
        """Calculate ATR-based SL."""
        # Get ATR value at bar (use cache if available)
        if atr_cache and self.atr_len in atr_cache:
            atr_series = atr_cache[self.atr_len]
        else:
            atr_series = atr(df['high'], df['low'], df['close'], self.atr_len)
        atr_val = atr_series.iloc[bar_index]
        
        if pd.isna(atr_val):
            atr_val = 0.01  # Fallback
        
        sl_distance = atr_val * self.atr_mult
        
        if is_long:
            return entry_price - sl_distance
        else:
            return entry_price + sl_distance
    
    def _calc_percent_sl(
        self,
        entry_price: float,
        is_long: bool
    ) -> float:
        """Calculate percentage-based SL."""
        sl_distance = entry_price * (self.percent / 100)
        
        if is_long:
            return entry_price - sl_distance
        else:
            return entry_price + sl_distance
    
    def _calc_swing_sl(
        self,
        df: pd.DataFrame,
        bar_index: int,
        entry_price: float,
        is_long: bool,
        atr_cache: dict = None,
    ) -> float:
        """Calculate swing-based SL with optional ATR buffer."""
        # Determine price source based on basis
        if self.swing_basis == "Wick":
            high_src = df['high']
            low_src = df['low']
        else:  # Body
            high_src = df[['open', 'close']].max(axis=1)
            low_src = df[['open', 'close']].min(axis=1)
        
        # Get lookback range
        start_idx = max(0, bar_index - self.swing_lookback)
        end_idx = bar_index + 1
        
        # Find swing point
        if is_long:
            swing_price = low_src.iloc[start_idx:end_idx].min()
        else:
            swing_price = high_src.iloc[start_idx:end_idx].max()
        
        # Apply ATR buffer if mode includes ATR
        if self.mode == "SWING_ATR" or self.swing_atr_mult > 0:
            if atr_cache and self.swing_atr_len in atr_cache:
                atr_series = atr_cache[self.swing_atr_len]
            else:
                atr_series = atr(df['high'], df['low'], df['close'], self.swing_atr_len)
            atr_val = atr_series.iloc[bar_index]
            
            if pd.isna(atr_val):
                atr_val = 0
            
            buffer = atr_val * self.swing_atr_mult
            
            if is_long:
                swing_price = swing_price - buffer
            else:
                swing_price = swing_price + buffer
        
        return swing_price
    
    def get_r_distance(
        self,
        entry_price: float,
        sl_price: float,
    ) -> float:
        """Calculate R distance (entry to SL)."""
        return abs(entry_price - sl_price)
