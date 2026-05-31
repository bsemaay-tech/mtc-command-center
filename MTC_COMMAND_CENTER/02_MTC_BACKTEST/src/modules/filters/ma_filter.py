"""
Moving Average Trend Filter.

Filters signals based on price position relative to a moving average.
Matches MTC's MA Filter implementation.
"""

from typing import Tuple, Dict, Literal
import pandas as pd

from .base import FilterPlugin
from .htf_trend_filter import _tf_to_pandas_rule
from ...engine.indicators import ma


class MAFilter(FilterPlugin):
    """
    Moving Average trend filter.
    
    - allowLong = close > MA (uptrend)
    - allowShort = close < MA (downtrend)
    
    Parameters:
        ma_type: Type of MA (SMA, EMA, RMA, WMA, HMA)
        length: MA period
        buffer_pct: Buffer percentage around MA (optional)
    """
    
    def __init__(
        self,
        enabled: bool = False,
        ma_type: Literal["SMA", "EMA", "DEMA", "TEMA", "RMA", "WMA", "VWMA", "KAMA", "HMA"] = "EMA",
        length: int = 200,
        buffer_pct: float = 0.0,
        use_htf: bool = False,
        htf_timeframe: str = "60",
    ):
        super().__init__(
            name="MA_Filter",
            enabled=enabled,
            ma_type=ma_type,
            length=length,
            buffer_pct=buffer_pct,
            use_htf=use_htf,
            htf_timeframe=htf_timeframe,
        )
        self.ma_type = ma_type
        self.length = length
        self.buffer_pct = buffer_pct
        self.use_htf = use_htf
        self.htf_timeframe = htf_timeframe

        self._ma_line: pd.Series = None

    def _calc_ma(self, close: pd.Series, volume: pd.Series = None) -> pd.Series:
        """Calculate MA using configured type."""
        if self.ma_type == "VWMA" and volume is not None:
            vol_sum = volume.rolling(window=self.length, min_periods=self.length).sum()
            pv_sum = (close * volume).rolling(window=self.length, min_periods=self.length).sum()
            return pv_sum / vol_sum.replace(0, pd.NA)
        return ma(close, self.length, self.ma_type)

    def apply(
        self,
        df: pd.DataFrame,
        **context
    ) -> Tuple[pd.Series, pd.Series]:
        """
        Apply MA filter.

        Returns:
            (allowLong, allowShort) based on price vs MA
        """
        if not self.enabled:
            allow = pd.Series(True, index=df.index)
            return allow, allow

        if self.use_htf and "timestamp" in df.columns:
            ts = pd.to_datetime(df["timestamp"], utc=True)
            ltf = df.copy()
            ltf.index = ts
            rule = _tf_to_pandas_rule(self.htf_timeframe)
            htf_close = ltf["close"].resample(rule, label="right", closed="right").last().dropna()
            htf_ma = ma(htf_close, self.length, self.ma_type)
            # Align back to LTF using forward-fill
            self._ma_line = pd.Series(
                htf_ma.reindex(ts, method="ffill").to_numpy(), index=df.index
            )
            compare_close = pd.Series(
                htf_close.reindex(ts, method="ffill").to_numpy(), index=df.index
            )
        else:
            self._ma_line = self._calc_ma(df['close'], df.get('volume'))
            compare_close = df['close']

        # Apply buffer
        buffer = self._ma_line * (self.buffer_pct / 100)
        upper_band = self._ma_line + buffer
        lower_band = self._ma_line - buffer

        # Filter logic
        allow_long = (compare_close > upper_band) | self._ma_line.isna()
        allow_short = (compare_close < lower_band) | self._ma_line.isna()

        return allow_long.fillna(True), allow_short.fillna(True)
    
    def get_debug_series(self, df: pd.DataFrame) -> Dict[str, pd.Series]:
        """Get MA line for debugging."""
        if self._ma_line is None:
            self.apply(df)
        return {'ma_line': self._ma_line}


class MASlopeFilter(FilterPlugin):
    """
    MA Slope filter - requires MA to be sloping in trade direction.
    
    - allowLong = MA is rising (MA > MA[1])
    - allowShort = MA is falling (MA < MA[1])
    
    More strict: requires minimum slope percentage.
    """
    
    def __init__(
        self,
        enabled: bool = False,
        ma_type: Literal["SMA", "EMA", "DEMA", "TEMA", "RMA", "WMA", "VWMA", "KAMA", "HMA"] = "EMA",
        length: int = 200,
        min_slope_pct: float = 0.005,
    ):
        super().__init__(
            name="MA_Slope_Filter",
            enabled=enabled,
            ma_type=ma_type,
            length=length,
            min_slope_pct=min_slope_pct,
        )
        self.ma_type = ma_type
        self.length = length
        self.min_slope_pct = min_slope_pct
        
        self._ma_line: pd.Series = None
        self._slope: pd.Series = None
    
    def apply(
        self,
        df: pd.DataFrame,
        **context
    ) -> Tuple[pd.Series, pd.Series]:
        """Apply MA slope filter."""
        if not self.enabled:
            allow = pd.Series(True, index=df.index)
            return allow, allow
        
        # Calculate MA (VWMA requires volume-aware formula)
        if self.ma_type == "VWMA":
            vol_sum = df['volume'].rolling(window=self.length, min_periods=self.length).sum()
            pv_sum = (df['close'] * df['volume']).rolling(window=self.length, min_periods=self.length).sum()
            self._ma_line = pv_sum / vol_sum.replace(0, pd.NA)
        else:
            self._ma_line = ma(df['close'], self.length, self.ma_type)
        
        # Calculate slope as percentage change
        self._slope = (self._ma_line - self._ma_line.shift(1)) / self._ma_line.shift(1) * 100
        
        # Filter logic
        allow_long = self._slope > self.min_slope_pct
        allow_short = self._slope < -self.min_slope_pct
        
        return allow_long, allow_short
    
    def get_debug_series(self, df: pd.DataFrame) -> Dict[str, pd.Series]:
        if self._ma_line is None:
            self.apply(df)
        return {
            'ma_line': self._ma_line,
            'slope_pct': self._slope,
        }
