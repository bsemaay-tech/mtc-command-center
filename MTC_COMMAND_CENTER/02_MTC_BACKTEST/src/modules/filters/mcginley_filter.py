"""
McGinley Dynamic Trend Filter.
"""

from typing import Dict, Tuple

import pandas as pd

from .base import FilterPlugin
from .htf_trend_filter import _tf_to_pandas_rule
from ...engine.indicators import mcginley_dynamic


class McGinleyFilter(FilterPlugin):
    """Allow long above McGinley line and short below."""

    def __init__(
        self,
        enabled: bool = False,
        length: int = 20,
        k: float = 0.6,
        use_htf: bool = False,
        htf_timeframe: str = "60",
    ):
        super().__init__(
            name="McGinley_Filter",
            enabled=enabled,
            length=length,
            k=k,
            use_htf=use_htf,
            htf_timeframe=htf_timeframe,
        )
        self.length = length
        self.k = k
        self.use_htf = use_htf
        self.htf_timeframe = htf_timeframe
        self._line: pd.Series | None = None
        self._src: pd.Series | None = None  # comparison source (HTF close or LTF close)

    @staticmethod
    def _resample_offset(ts: pd.Series, rule: str) -> str:
        if len(ts) < 2:
            return "0min"
        try:
            ltf_delta = ts.diff().dropna().mode().iloc[0]
            htf_delta = pd.Timedelta(rule)
        except Exception:
            return "0min"
        if pd.isna(ltf_delta) or ltf_delta <= pd.Timedelta(0) or htf_delta <= ltf_delta:
            return "0min"
        offset = htf_delta - ltf_delta
        minutes = int(offset.total_seconds() // 60)
        return f"{minutes}min" if minutes > 0 else "0min"

    def apply(self, df: pd.DataFrame, **context) -> Tuple[pd.Series, pd.Series]:
        if not self.enabled:
            allow = pd.Series(True, index=df.index)
            return allow, allow
        if self.use_htf:
            ts = pd.to_datetime(df["timestamp"], utc=True)
            ltf = df.copy()
            ltf.index = ts
            rule = _tf_to_pandas_rule(self.htf_timeframe)
            offset = self._resample_offset(ts, rule)
            htf_close = (
                ltf["close"]
                .resample(rule, label="right", closed="right", offset=offset)
                .last()
                .dropna()
            )
            htf_line = mcginley_dynamic(htf_close, length=self.length, k=self.k)
            self._line = pd.Series(htf_line.reindex(ts, method="ffill").to_numpy(), index=df.index)
            # Pine parity: request.security(close, HTF) replays the HTF close
            # series on the LTF chart. With close-stamped LTF bars, using the
            # shifted resample offset keeps HTF closes aligned to TV bar labels.
            self._src = pd.Series(htf_close.reindex(ts, method="ffill").to_numpy(), index=df.index)
        else:
            self._line = mcginley_dynamic(df["close"], length=self.length, k=self.k)
            self._src = df["close"]
        allow_long = (self._src > self._line) | self._line.isna()
        allow_short = (self._src < self._line) | self._line.isna()
        return allow_long.fillna(True), allow_short.fillna(True)

    def get_debug_series(self, df: pd.DataFrame) -> Dict[str, pd.Series]:
        if self._line is None:
            self.apply(df)
        return {"mcginley_line": self._line}
