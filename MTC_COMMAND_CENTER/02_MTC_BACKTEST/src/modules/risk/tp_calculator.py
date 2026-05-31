"""
Take Profit Calculator.

Calculates TP prices including Multi-TP logic matching MTC.
"""

from typing import Optional, Literal, Tuple
import pandas as pd

from ...engine.indicators import atr


class TPCalculator:
    """
    Take Profit price calculator.
    
    Supports all MTC TP modes:
    - ATR: TP = entry ± (ATR * mult)
    - %: TP = entry ± (entry * percent)
    - R: TP = entry ± (R * rr_multiple)
    
    Also supports Multi-TP (TP1 partial, TP2 remainder).
    """
    
    def __init__(
        self,
        mode: Literal["ATR", "%", "R"] = "ATR",
        atr_len: int = 14,
        atr_mult: float = 3.0,
        percent: float = 2.0,
        rr: float = 2.0,
        # Multi-TP
        use_multi_tp: bool = True,
        tp1_rr: float = 3.0,
        tp1_pct: float = 50.0,
        tp2_rr: float = 5.5,
    ):
        self.mode = mode
        self.atr_len = atr_len
        self.atr_mult = atr_mult
        self.percent = percent
        self.rr = rr
        self.use_multi_tp = use_multi_tp
        self.tp1_rr = tp1_rr
        self.tp1_pct = tp1_pct
        self.tp2_rr = tp2_rr
    
    def calculate(
        self,
        df: pd.DataFrame,
        bar_index: int,
        direction: str,
        entry_price: float,
        sl_price: Optional[float] = None,
        atr_cache: dict = None,
    ) -> float:
        """
        Calculate single TP price.
        
        Args:
            df: OHLCV DataFrame
            bar_index: Current bar index
            direction: "long" or "short"
            entry_price: Entry price
            sl_price: Stop loss price (required for R mode)
            atr_cache: Pre-computed ATR series keyed by length
            
        Returns:
            Take profit price
        """
        is_long = direction == "long"
        
        if self.mode == "ATR":
            return self._calc_atr_tp(df, bar_index, entry_price, is_long, atr_cache=atr_cache)
        elif self.mode == "%":
            return self._calc_percent_tp(entry_price, is_long)
        elif self.mode == "R":
            return self._calc_r_tp(entry_price, sl_price, is_long, self.rr)
        else:
            return self._calc_atr_tp(df, bar_index, entry_price, is_long, atr_cache=atr_cache)
    
    def calculate_multi(
        self,
        df: pd.DataFrame,
        bar_index: int,
        direction: str,
        entry_price: float,
        sl_price: float,
        atr_cache: dict = None,
    ) -> Tuple[Optional[float], Optional[float], float]:
        """
        Calculate Multi-TP prices (TP1 and TP2).
        
        Args:
            df: OHLCV DataFrame
            bar_index: Current bar index
            direction: "long" or "short"
            entry_price: Entry price
            sl_price: Stop loss price
            atr_cache: Pre-computed ATR series keyed by length
            
        Returns:
            (tp1_price, tp2_price, tp1_close_pct)
        """
        if not self.use_multi_tp:
            tp = self.calculate(df, bar_index, direction, entry_price, sl_price, atr_cache=atr_cache)
            return None, tp, 100.0
        
        is_long = direction == "long"
        
        # Calculate TP1 and TP2 based on R-multiples
        tp1 = self._calc_r_tp(entry_price, sl_price, is_long, self.tp1_rr)
        tp2 = self._calc_r_tp(entry_price, sl_price, is_long, self.tp2_rr)
        
        return tp1, tp2, self.tp1_pct
    
    def _calc_atr_tp(
        self,
        df: pd.DataFrame,
        bar_index: int,
        entry_price: float,
        is_long: bool,
        atr_cache: dict = None,
    ) -> float:
        """Calculate ATR-based TP."""
        if atr_cache and self.atr_len in atr_cache:
            atr_series = atr_cache[self.atr_len]
        else:
            atr_series = atr(df['high'], df['low'], df['close'], self.atr_len)
        atr_val = atr_series.iloc[bar_index]
        
        if pd.isna(atr_val):
            atr_val = 0.01
        
        tp_distance = atr_val * self.atr_mult
        
        if is_long:
            return entry_price + tp_distance
        else:
            return entry_price - tp_distance
    
    def _calc_percent_tp(
        self,
        entry_price: float,
        is_long: bool
    ) -> float:
        """Calculate percentage-based TP."""
        tp_distance = entry_price * (self.percent / 100)
        
        if is_long:
            return entry_price + tp_distance
        else:
            return entry_price - tp_distance
    
    def _calc_r_tp(
        self,
        entry_price: float,
        sl_price: Optional[float],
        is_long: bool,
        rr_mult: float
    ) -> float:
        """Calculate R-multiple based TP."""
        if sl_price is None:
            # Fallback to 2% if no SL
            return self._calc_percent_tp(entry_price, is_long)
        
        r_distance = abs(entry_price - sl_price)
        tp_distance = r_distance * rr_mult
        
        if is_long:
            return entry_price + tp_distance
        else:
            return entry_price - tp_distance


class BreakEvenCalculator:
    """
    Break-Even price calculator.
    
    Calculates when to move SL to break-even and at what price.
    """
    
    def __init__(
        self,
        enabled: bool = True,
        trigger_rr: float = 1.0,
        buffer_r: float = 0.1,
    ):
        self.enabled = enabled
        self.trigger_rr = trigger_rr
        self.buffer_r = buffer_r
    
    def should_trigger(
        self,
        entry_price: float,
        sl_price: float,
        current_price: float,
        direction: str,
    ) -> bool:
        """
        Check if BE should be triggered.

        Args:
            entry_price: Entry price
            sl_price: Original SL price
            current_price: Current market price
            direction: "long" or "short"

        Returns:
            True if price has moved enough to trigger BE
        """
        if not self.enabled:
            return False
        if sl_price is None:
            return False  # No R-reference when SL disabled

        r_distance = abs(entry_price - sl_price)
        trigger_distance = r_distance * self.trigger_rr
        
        if direction == "long":
            return current_price >= entry_price + trigger_distance
        else:
            return current_price <= entry_price - trigger_distance
    
    def calculate_be_price(
        self,
        entry_price: float,
        sl_price: float,
        direction: str,
    ) -> float:
        """
        Calculate break-even price with buffer.

        Args:
            entry_price: Entry price
            sl_price: Original SL price
            direction: "long" or "short"

        Returns:
            Break-even price (entry + buffer)
        """
        if sl_price is None:
            return entry_price  # No R-reference when SL disabled
        r_distance = abs(entry_price - sl_price)
        buffer = r_distance * self.buffer_r
        
        if direction == "long":
            return entry_price + buffer
        else:
            return entry_price - buffer


class TrailingStopCalculator:
    """
    Trailing Stop calculator.
    
    Calculates trailing stop activation and distance.
    """
    
    def __init__(
        self,
        enabled: bool = True,
        start_r: float = 2.5,
        dist_r: float = 2.0,
    ):
        self.enabled = enabled
        self.start_r = start_r
        self.dist_r = dist_r
    
    def should_activate(
        self,
        entry_price: float,
        sl_price: float,
        current_price: float,
        direction: str,
    ) -> bool:
        """Check if trailing stop should activate."""
        if not self.enabled:
            return False
        if sl_price is None:
            return False  # No R-reference when SL disabled

        r_distance = abs(entry_price - sl_price)
        activation_distance = r_distance * self.start_r
        
        if direction == "long":
            return current_price >= entry_price + activation_distance
        else:
            return current_price <= entry_price - activation_distance
    
    def calculate_trailing_stop(
        self,
        entry_price: float,
        sl_price: float,
        highest_price: float,
        lowest_price: float,
        direction: str,
    ) -> float:
        """
        Calculate trailing stop price.
        
        Args:
            entry_price: Entry price
            sl_price: Original SL price
            highest_price: Highest price since entry (for longs)
            lowest_price: Lowest price since entry (for shorts)
            direction: "long" or "short"
            
        Returns:
            Trailing stop price
        """
        if sl_price is None:
            return None  # No R-reference when SL disabled
        r_distance = abs(entry_price - sl_price)
        trail_distance = r_distance * self.dist_r
        
        if direction == "long":
            return highest_price - trail_distance
        else:
            return lowest_price + trail_distance
