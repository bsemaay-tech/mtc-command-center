"""
MACD Filter Hub.
"""

from __future__ import annotations

from typing import Dict, Tuple

import pandas as pd

from .base import FilterPlugin
from .htf_trend_filter import _tf_to_pandas_rule
from ...engine.indicators import ema


def _macd_series(close: pd.Series, fast_len: int, slow_len: int, signal_len: int):
    fast = ema(close, fast_len)
    slow = ema(close, slow_len)
    macd_line = fast - slow
    signal = ema(macd_line, signal_len)
    hist = macd_line - signal
    return macd_line, signal, hist


def _ppo_norm_series(close: pd.Series, fast_len: int, slow_len: int, signal_len: int):
    fast = ema(close, fast_len)
    slow = ema(close, slow_len)
    line = (fast - slow) / slow.replace(0, pd.NA) * 100.0
    signal = ema(line, signal_len)
    hist = line - signal
    return line, signal, hist


class MacdHubFilter(FilterPlugin):
    """Multi-mode MACD gating filter."""

    def __init__(
        self,
        enabled: bool = False,
        gate_mode: str = "Regime",
        source: str = "close",
        fast_len: int = 12,
        slow_len: int = 26,
        signal_len: int = 9,
        distance_pct: float = 0.0,
        htf_timeframe: str = "240",
        use_htf_bias: bool = False,
    ):
        super().__init__(
            name="MACD_Hub_Filter",
            enabled=enabled,
            gate_mode=gate_mode,
            source=source,
            fast_len=fast_len,
            slow_len=slow_len,
            signal_len=signal_len,
            distance_pct=distance_pct,
            htf_timeframe=htf_timeframe,
            use_htf_bias=use_htf_bias,
        )
        self.gate_mode = gate_mode
        self.source = source
        self.fast_len = fast_len
        self.slow_len = slow_len
        self.signal_len = signal_len
        self.distance_pct = distance_pct
        self.htf_timeframe = htf_timeframe
        self.use_htf_bias = use_htf_bias
        self._debug: Dict[str, pd.Series] = {}

    def apply(self, df: pd.DataFrame, **context) -> Tuple[pd.Series, pd.Series]:
        if not self.enabled:
            allow = pd.Series(True, index=df.index)
            return allow, allow

        # Resolve price source (Pine: input.source)
        if self.source == "hl2":
            src = (df["high"] + df["low"]) / 2.0
        elif self.source == "hlc3":
            src = (df["high"] + df["low"] + df["close"]) / 3.0
        elif self.source == "ohlc4":
            src = (df["open"] + df["high"] + df["low"] + df["close"]) / 4.0
        elif self.source == "open":
            src = df["open"]
        else:
            src = df["close"]
        close = src
        mode = self.gate_mode

        if mode == "PPO_NORM":
            macd_line, signal, hist = _ppo_norm_series(close, self.fast_len, self.slow_len, self.signal_len)
        else:
            macd_line, signal, hist = _macd_series(close, self.fast_len, self.slow_len, self.signal_len)

        # Calculate HTF Bias (used when mode=="HTF Bias" or use_htf_bias==True)
        htf_allow_long = None
        htf_allow_short = None
        if mode == "HTF Bias" or self.use_htf_bias:
            ts = pd.to_datetime(df["timestamp"], utc=True)
            rule = _tf_to_pandas_rule(self.htf_timeframe)
            ltf = df.copy()
            ltf_delta = ts.diff().dropna().median()
            if pd.isna(ltf_delta) or ltf_delta <= pd.Timedelta(0):
                ltf_delta = pd.Timedelta(minutes=15)
            # Engine bars are indexed by bar OPEN time. Pine evaluates logic on
            # bar close, so HTF request.security() effectively sees child bars
            # anchored by their CLOSE. Shift to close-time before resampling so
            # a 4H candle ending 20:00 includes the 19:45 15m bar, not 20:00.
            ltf.index = ts + ltf_delta
            htf_close = ltf["close"].resample(rule, label="right", closed="right").last()
            # Compute MACD on HTF close
            if mode == "PPO_NORM":
                htf_macd, _, _ = _ppo_norm_series(htf_close, self.fast_len, self.slow_len, self.signal_len)
            else:
                htf_macd, _, _ = _macd_series(htf_close, self.fast_len, self.slow_len, self.signal_len)
            # Pine parity: on the LAST child bar of an HTF candle, the newly
            # confirmed HTF value is already visible to the child bar whose
            # CLOSE reaches that HTF boundary. Convert the right-labeled HTF
            # close timestamp back to the corresponding child bar OPEN.
            htf_df = pd.DataFrame(
                {
                    "timestamp": htf_macd.index - ltf_delta,
                    "htf_macd": htf_macd.values,
                }
            )
            ltf_df = pd.DataFrame({"timestamp": ts})
            merged = pd.merge_asof(ltf_df, htf_df, on="timestamp", direction="backward")
            aligned = merged["htf_macd"]
            # Convert to boolean signals
            htf_allow_long = aligned > 0
            htf_allow_short = aligned < 0
            self._debug["htf_macd"] = aligned

        if mode == "Regime":
            allow_long = macd_line > 0
            allow_short = macd_line < 0
        elif mode == "Cross-State":
            allow_long = macd_line > signal
            allow_short = macd_line < signal
        elif mode == "Histogram":
            allow_long = hist > 0
            allow_short = hist < 0
        elif mode == "Distance":
            dist_pct = ((macd_line - signal).abs() / close.replace(0, pd.NA)) * 100.0
            allow_long = (macd_line > signal) & (dist_pct >= self.distance_pct)
            allow_short = (macd_line < signal) & (dist_pct >= self.distance_pct)
            self._debug["distance_pct"] = dist_pct
        elif mode == "HTF Bias":
            allow_long = htf_allow_long
            allow_short = htf_allow_short
        elif mode == "STANDARD":
            # Pine default bundle for STANDARD mode:
            # line calculation = classic MACD, gate = regime sign.
            allow_long = macd_line > 0
            allow_short = macd_line < 0
            if self.use_htf_bias and htf_allow_long is not None:
                allow_long = allow_long & htf_allow_long
                allow_short = allow_short & htf_allow_short
        elif mode == "PPO_NORM":
            # Pine default bundle for PPO_NORM:
            # line calculation = normalized MACD, gate = regime sign.
            allow_long = macd_line > 0
            allow_short = macd_line < 0
            self._debug["ppo"] = macd_line
            if self.use_htf_bias and htf_allow_long is not None:
                allow_long = allow_long & htf_allow_long
                allow_short = allow_short & htf_allow_short
        else:
            allow_long = pd.Series(True, index=df.index)
            allow_short = pd.Series(True, index=df.index)

        allow_long = allow_long.fillna(True).astype(bool)
        allow_short = allow_short.fillna(True).astype(bool)
        self._debug.update(
            {
                "macd_line": macd_line,
                "macd_signal": signal,
                "macd_hist": hist,
                "allow_long": allow_long,
                "allow_short": allow_short,
            }
        )
        return allow_long, allow_short

    def get_debug_series(self, df: pd.DataFrame) -> Dict[str, pd.Series]:
        if not self._debug:
            self.apply(df)
        return self._debug.copy()
