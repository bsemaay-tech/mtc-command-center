"""
Volume Filter.

Filters signals based on volume relative to average.
Matches MTC's Volume Participation filter.
"""

from typing import Tuple, Dict
import pandas as pd

from .base import FilterPlugin
from ...engine.indicators import sma


class VolumeFilter(FilterPlugin):
    """
    Volume participation filter.
    
    Requires volume to be above a multiple of the average volume.
    
    - allowLong = volume > (avg_volume * mult)
    - allowShort = volume > (avg_volume * mult)
    
    Parameters:
        length: Lookback period for average volume
        mult: Minimum multiple of average volume required
    """
    
    def __init__(
        self,
        enabled: bool = True,
        length: int = 50,
        mult: float = 0.5,
    ):
        super().__init__(
            name="Volume_Filter",
            enabled=enabled,
            length=length,
            mult=mult,
        )
        self.length = length
        self.mult = mult
        
        self._avg_volume: pd.Series = None
        self._threshold: pd.Series = None
    
    def apply(
        self,
        df: pd.DataFrame,
        **context
    ) -> Tuple[pd.Series, pd.Series]:
        """
        Apply volume filter.
        
        Returns:
            (allowLong, allowShort) - same for both directions
        """
        if not self.enabled:
            allow = pd.Series(True, index=df.index)
            return allow, allow
        
        # Calculate average volume
        self._avg_volume = sma(df['volume'], self.length)
        self._threshold = self._avg_volume * self.mult
        
        # Pine parity:
        # - Warmup/na bars should pass through (true)
        # - Comparison uses >=
        allow = (df['volume'] >= self._threshold) | self._threshold.isna()
        
        return allow, allow
    
    def get_debug_series(self, df: pd.DataFrame) -> Dict[str, pd.Series]:
        if self._avg_volume is None:
            self.apply(df)
        return {
            'avg_volume': self._avg_volume,
            'volume_threshold': self._threshold,
        }


class ATRVolatilityFilter(FilterPlugin):
    """
    ATR Volatility Floor filter.
    
    Requires current ATR to be above a baseline level.
    Prevents trading in low-volatility conditions.
    
    - allowLong = atr > (baseline_atr * floor_mult)
    - allowShort = atr > (baseline_atr * floor_mult)
    
    Parameters:
        atr_len: ATR calculation period
        smooth_len: Baseline smoothing period
        floor_mult: Minimum ATR ratio required
    """
    
    def __init__(
        self,
        enabled: bool = True,
        atr_len: int = 14,
        smooth_len: int = 100,
        floor_mult: float = 1.2,
    ):
        super().__init__(
            name="ATR_Vol_Filter",
            enabled=enabled,
            atr_len=atr_len,
            smooth_len=smooth_len,
            floor_mult=floor_mult,
        )
        self.atr_len = atr_len
        self.smooth_len = smooth_len
        self.floor_mult = floor_mult
        
        self._atr: pd.Series = None
        self._baseline: pd.Series = None
    
    def apply(
        self,
        df: pd.DataFrame,
        **context
    ) -> Tuple[pd.Series, pd.Series]:
        """Apply ATR volatility filter."""
        if not self.enabled:
            allow = pd.Series(True, index=df.index)
            return allow, allow
        
        from ...engine.indicators import atr as calc_atr
        
        # Calculate ATR
        self._atr = calc_atr(df['high'], df['low'], df['close'], self.atr_len)
        
        # Calculate baseline (smoothed ATR)
        self._baseline = sma(self._atr, self.smooth_len)
        
        # Pine parity:
        # - Warmup/na bars pass through (true)
        # - Ratio check uses >=
        baseline_safe = self._baseline.clip(lower=1e-12)
        ratio = self._atr / baseline_safe
        allow = (ratio >= self.floor_mult) | self._atr.isna() | self._baseline.isna()
        
        return allow, allow
    
    def get_debug_series(self, df: pd.DataFrame) -> Dict[str, pd.Series]:
        if self._atr is None:
            self.apply(df)
        return {
            'atr': self._atr,
            'atr_baseline': self._baseline,
            'atr_floor': self._baseline * self.floor_mult if self._baseline is not None else None,
        }
