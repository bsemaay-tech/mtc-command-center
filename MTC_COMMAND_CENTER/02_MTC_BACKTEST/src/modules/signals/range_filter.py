"""
Range Filter Hybrid Signal Plugin.

Implements a deterministic ADX+Chop+RSI(+optional BB) signal module.
"""

from typing import Dict, Tuple

import pandas as pd
import numpy as np

from .base import SignalPlugin
from ...engine.indicators import bollinger_bands, choppiness, rsi, rma, tr


class RangeFilterHybridSignal(SignalPlugin):
    """Range/Trend hybrid raw signal generator."""

    def __init__(
        self,
        adx_trend_threshold: int = 25,
        adx_range_threshold: int = 20,
        chop_trend_threshold: int = 50,
        chop_range_threshold: int = 62,
        rsi_len: int = 14,
        rsi_oversold: int = 30,
        rsi_overbought: int = 70,
        bb_len: int = 20,
        bb_mult: float = 2.0,
        use_bb_filter: bool = True,
    ):
        super().__init__(
            name="RangeFilterHybrid",
            adx_trend_threshold=adx_trend_threshold,
            adx_range_threshold=adx_range_threshold,
            chop_trend_threshold=chop_trend_threshold,
            chop_range_threshold=chop_range_threshold,
            rsi_len=rsi_len,
            rsi_oversold=rsi_oversold,
            rsi_overbought=rsi_overbought,
            bb_len=bb_len,
            bb_mult=bb_mult,
            use_bb_filter=use_bb_filter,
        )
        self.adx_trend_threshold = adx_trend_threshold
        self.adx_range_threshold = adx_range_threshold
        self.chop_trend_threshold = chop_trend_threshold
        self.chop_range_threshold = chop_range_threshold
        self.rsi_len = rsi_len
        self.rsi_oversold = rsi_oversold
        self.rsi_overbought = rsi_overbought
        self.bb_len = bb_len
        self.bb_mult = bb_mult
        self.use_bb_filter = use_bb_filter
        self._last_debug: Dict[str, pd.Series] = {}

    def generate(self, df: pd.DataFrame) -> Tuple[pd.Series, pd.Series]:
        close = df["close"]
        high = df["high"]
        low = df["low"]

        # Pine parity: ta.dmi() based ADX + DI pair (length=14)
        up_move = high.diff()
        down_move = -low.diff()
        plus_dm = pd.Series(
            np.where((up_move > down_move) & (up_move > 0), up_move, 0.0),
            index=df.index,
        )
        minus_dm = pd.Series(
            np.where((down_move > up_move) & (down_move > 0), down_move, 0.0),
            index=df.index,
        )
        tr_v = tr(high, low, close)
        smoothed_tr = rma(tr_v, 14)
        smoothed_plus_dm = rma(plus_dm, 14)
        smoothed_minus_dm = rma(minus_dm, 14)
        # Pine parity: match MASTER_TEMPLATE_CORE guards:
        # plusDI = trRma != 0 ? 100 * plusRma / trRma : 0
        # dxVal  = (plusDI + minusDI != 0) ? ... : 0
        plus_di = pd.Series(
            np.where(smoothed_tr != 0, 100.0 * smoothed_plus_dm / smoothed_tr, 0.0),
            index=df.index,
            dtype=float,
        )
        minus_di = pd.Series(
            np.where(smoothed_tr != 0, 100.0 * smoothed_minus_dm / smoothed_tr, 0.0),
            index=df.index,
            dtype=float,
        )
        dx = pd.Series(
            np.where(
                (plus_di + minus_di) != 0,
                100.0 * (plus_di - minus_di).abs() / (plus_di + minus_di),
                0.0,
            ),
            index=df.index,
            dtype=float,
        )
        adx_v = rma(dx, 14)
        chop_v = choppiness(high, low, close, length=14)
        rsi_v = rsi(close, length=self.rsi_len)
        bb_upper, bb_mid, bb_lower = bollinger_bands(close, length=self.bb_len, mult=self.bb_mult)

        regime_trend = (adx_v > float(self.adx_trend_threshold)) & (chop_v < float(self.chop_trend_threshold))
        regime_range = (adx_v < float(self.adx_range_threshold)) & (chop_v > float(self.chop_range_threshold))

        if self.use_bb_filter:
            # Pine parity: +/-2% proximity to BB envelopes in range mode.
            range_long_gate = close <= (bb_lower * 1.02)
            range_short_gate = close >= (bb_upper * 0.98)
        else:
            always = pd.Series(True, index=df.index)
            range_long_gate = always
            range_short_gate = always

        adx_prev = adx_v.shift(1).fillna(adx_v)
        long_trend = regime_trend & (plus_di > minus_di) & (adx_v > adx_prev)
        short_trend = regime_trend & (minus_di > plus_di) & (adx_v > adx_prev)

        long_range = regime_range & (rsi_v < float(self.rsi_oversold)) & range_long_gate
        short_range = regime_range & (rsi_v > float(self.rsi_overbought)) & range_short_gate

        long_raw = (long_trend | long_range).fillna(False)
        short_raw = (short_trend | short_range).fillna(False)

        self._last_debug = {
            "adx": adx_v,
            "plus_di": plus_di,
            "minus_di": minus_di,
            "chop": chop_v,
            "rsi": rsi_v,
            "bb_upper": bb_upper,
            "bb_mid": bb_mid,
            "bb_lower": bb_lower,
            "regime_trend": regime_trend.astype(bool),
            "regime_range": regime_range.astype(bool),
            "long_raw": long_raw,
            "short_raw": short_raw,
        }
        return long_raw, short_raw

    def get_debug_series(self, df: pd.DataFrame) -> Dict[str, pd.Series]:
        if not self._last_debug:
            self.generate(df)
        return self._last_debug.copy()
