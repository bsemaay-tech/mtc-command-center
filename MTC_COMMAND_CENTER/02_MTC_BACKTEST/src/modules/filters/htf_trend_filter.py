"""
HTF Trend Filter.

Resamples lower timeframe bars to configured HTF and applies MA trend gating.
"""

from __future__ import annotations

from typing import Dict, Tuple

import pandas as pd

from .base import FilterPlugin
from ...engine.indicators import ma


def _tf_to_pandas_rule(tf: str) -> str:
    s = str(tf).strip()
    if not s:
        return "240min"
    if s.isdigit():
        return f"{int(s)}min"
    unit = s[-1].lower()
    val = s[:-1]
    if unit == "m" and val.isdigit():
        return f"{int(val)}min"
    if unit == "h" and val.isdigit():
        return f"{int(val)}h"
    if unit == "d" and val.isdigit():
        return f"{int(val)}d"
    if unit == "w" and val.isdigit():
        return f"{int(val)}w"
    return s


class HTFTrendFilter(FilterPlugin):
    """Higher-timeframe trend filter using HTF close vs HTF MA."""

    def __init__(
        self,
        enabled: bool = False,
        timeframe: str = "240",
        ma_type: str = "EMA",
        ma_len: int = 100,
        buffer_pct: float = 0.1,
    ):
        super().__init__(
            name="HTF_Trend_Filter",
            enabled=enabled,
            timeframe=timeframe,
            ma_type=ma_type,
            ma_len=ma_len,
            buffer_pct=buffer_pct,
        )
        self.timeframe = timeframe
        self.ma_type = ma_type
        self.ma_len = ma_len
        self.buffer_pct = buffer_pct
        self._debug: Dict[str, pd.Series] = {}

    def apply(self, df: pd.DataFrame, **context) -> Tuple[pd.Series, pd.Series]:
        if not self.enabled:
            allow = pd.Series(True, index=df.index)
            return allow, allow

        ts = pd.to_datetime(df["timestamp"], utc=True)
        ltf = df.copy()
        ltf.index = ts
        rule = _tf_to_pandas_rule(self.timeframe)

        htf = (
            ltf.resample(rule, label="right", closed="right")
            .agg(
                {
                    "open": "first",
                    "high": "max",
                    "low": "min",
                    "close": "last",
                    "volume": "sum",
                }
            )
            .dropna(subset=["close"])
        )
        if htf.empty:
            allow = pd.Series(True, index=df.index)
            return allow, allow

        htf_ma = ma(htf["close"], self.ma_len, self.ma_type)
        buffer = htf_ma * (self.buffer_pct / 100.0)
        htf_allow_long = htf["close"] >= (htf_ma + buffer)
        htf_allow_short = htf["close"] <= (htf_ma - buffer)

        aligned_long = htf_allow_long.reindex(ts, method="ffill").fillna(True)
        aligned_short = htf_allow_short.reindex(ts, method="ffill").fillna(True)
        allow_long = pd.Series(aligned_long.to_numpy(dtype=bool), index=df.index)
        allow_short = pd.Series(aligned_short.to_numpy(dtype=bool), index=df.index)

        self._debug = {
            "htf_close": htf["close"],
            "htf_ma": htf_ma,
            "htf_allow_long": htf_allow_long.astype(bool),
            "htf_allow_short": htf_allow_short.astype(bool),
            "aligned_allow_long": allow_long,
            "aligned_allow_short": allow_short,
        }
        return allow_long, allow_short

    def get_debug_series(self, df: pd.DataFrame) -> Dict[str, pd.Series]:
        if not self._debug:
            self.apply(df)
        return self._debug.copy()
