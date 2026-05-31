"""
Deterministic 4H regime labeler — method_v1.

Algorithm
---------
Inputs  : 4H OHLCV DataFrame
Outputs : per-bar pd.Series[str] with labels:
          "TREND_BULL", "TREND_BEAR", "CHOPPY", "RANGE"

Label rules (first match wins, evaluated left to right):
  1. ADX(14) > 25  AND  EMA50_slope5 > +0.005  →  TREND_BULL
  2. ADX(14) > 25  AND  EMA50_slope5 < -0.005  →  TREND_BEAR
  3. CHOP(14) > 61.8                            →  CHOPPY
  4. else                                       →  RANGE

All thresholds are pinned in DEFAULT_THRESHOLDS.
The fingerprint (SHA-256 of data_hash + sorted_thresholds_json) guarantees that
identical inputs + thresholds always produce identical outputs.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd

# ---------------------------------------------------------------------------
METHOD_VERSION = "method_v1"

DEFAULT_THRESHOLDS: dict[str, float | int] = {
    "adx_period": 14,
    "adx_threshold": 25.0,
    "ema_period": 50,
    "slope_window": 5,
    "slope_threshold": 0.005,
    "chop_period": 14,
    "chop_threshold": 61.8,
}

LABEL_TREND_BULL = "TREND_BULL"
LABEL_TREND_BEAR = "TREND_BEAR"
LABEL_CHOPPY = "CHOPPY"
LABEL_RANGE = "RANGE"

ALL_LABELS = [LABEL_TREND_BULL, LABEL_TREND_BEAR, LABEL_CHOPPY, LABEL_RANGE]
LABEL_DISPLAY = {
    LABEL_TREND_BULL: "Trend Bull",
    LABEL_TREND_BEAR: "Trend Bear",
    LABEL_CHOPPY: "Choppy",
    LABEL_RANGE: "Range",
}


# ---------------------------------------------------------------------------
class RegimeLabeler:
    """
    Deterministic 4H regime labeler.

    Parameters
    ----------
    thresholds : dict, optional
        Override individual thresholds. Unknown keys are ignored.
        Unspecified keys fall back to DEFAULT_THRESHOLDS.
    """

    def __init__(self, thresholds: dict | None = None) -> None:
        self.thresholds = {**DEFAULT_THRESHOLDS, **(thresholds or {})}

    # ------------------------------------------------------------------
    def label(self, df: pd.DataFrame) -> pd.Series:
        """
        Label each bar in *df*.

        Parameters
        ----------
        df : pd.DataFrame
            Must contain columns: open, high, low, close.

        Returns
        -------
        pd.Series[str]
            Same index as *df*. Values are TREND_BULL | TREND_BEAR | CHOPPY | RANGE.
        """
        th = self.thresholds
        adx = self._compute_adx(df, int(th["adx_period"]))
        ema = self._compute_ema(df["close"], int(th["ema_period"]))
        slope = ema.pct_change(int(th["slope_window"]))
        chop = self._compute_choppiness(df, int(th["chop_period"]))

        labels = pd.Series(LABEL_RANGE, index=df.index, dtype=object)

        # Apply in reverse priority (RANGE is default, overwrite with higher specificity)
        labels[chop > float(th["chop_threshold"])] = LABEL_CHOPPY
        labels[(adx > float(th["adx_threshold"])) & (slope < -float(th["slope_threshold"]))] = LABEL_TREND_BEAR
        labels[(adx > float(th["adx_threshold"])) & (slope > float(th["slope_threshold"]))] = LABEL_TREND_BULL

        return labels

    # ------------------------------------------------------------------
    def compress_to_windows(self, label_series: pd.Series) -> list[dict]:
        """
        Convert a per-bar label series into a list of contiguous windows.

        Returns
        -------
        list of dicts with keys: start, end, label, label_display, bars, source
        """
        if label_series.empty:
            return []

        windows: list[dict] = []
        cur_label = label_series.iloc[0]
        cur_start = label_series.index[0]
        count = 1

        for ts, lbl in label_series.iloc[1:].items():
            if lbl == cur_label:
                count += 1
            else:
                windows.append(self._make_window(cur_start, label_series.index[label_series.index.get_loc(ts) - 1], cur_label, count))  # noqa: E501
                cur_label = lbl
                cur_start = ts
                count = 1

        # last window
        windows.append(self._make_window(cur_start, label_series.index[-1], cur_label, count))
        return windows

    # ------------------------------------------------------------------
    def compute_fingerprint(self, data_hash: str) -> str:
        """
        Deterministic fingerprint: SHA-256(data_hash + sorted_thresholds_json).
        Changes whenever data or thresholds change.
        """
        th_json = json.dumps(self.thresholds, sort_keys=True)
        raw = f"{data_hash}|{METHOD_VERSION}|{th_json}"
        return hashlib.sha256(raw.encode()).hexdigest()

    # ------------------------------------------------------------------
    # Indicator implementations
    # ------------------------------------------------------------------

    @staticmethod
    def _compute_ema(series: pd.Series, period: int) -> pd.Series:
        return series.ewm(span=period, adjust=False).mean()

    @staticmethod
    def _compute_adx(df: pd.DataFrame, period: int) -> pd.Series:
        """Wilder's ADX (standard 14-period implementation)."""
        high = df["high"]
        low = df["low"]
        close = df["close"]

        # True Range
        hl = high - low
        hc = (high - close.shift(1)).abs()
        lc = (low - close.shift(1)).abs()
        tr = pd.concat([hl, hc, lc], axis=1).max(axis=1)

        # Directional movement
        up_move = high.diff()
        down_move = -low.diff()
        plus_dm = (up_move.where((up_move > down_move) & (up_move > 0), 0.0))
        minus_dm = (down_move.where((down_move > up_move) & (down_move > 0), 0.0))

        # Wilder smoothing (RMA)
        def rma(s: pd.Series, n: int) -> pd.Series:
            result = s.copy()
            result.iloc[:n] = np.nan
            seed = s.iloc[:n].mean()
            alpha = 1.0 / n
            val = seed
            out = []
            for x in s:
                val = alpha * x + (1 - alpha) * val
                out.append(val)
            return pd.Series(out, index=s.index)

        atr = rma(tr, period)
        plus_di = 100 * rma(plus_dm, period) / atr
        minus_di = 100 * rma(minus_dm, period) / atr
        dx = 100 * (plus_di - minus_di).abs() / (plus_di + minus_di)
        adx = rma(dx, period)
        return adx

    @staticmethod
    def _compute_choppiness(df: pd.DataFrame, period: int) -> pd.Series:
        """
        Choppiness Index:
          CHOP = 100 * log10(Sum(ATR(1), period) / (HH(period) - LL(period))) / log10(period)
        """
        high = df["high"]
        low = df["low"]
        close = df["close"]

        tr = pd.concat(
            [high - low, (high - close.shift(1)).abs(), (low - close.shift(1)).abs()], axis=1
        ).max(axis=1)

        atr_sum = tr.rolling(period).sum()
        hh = high.rolling(period).max()
        ll = low.rolling(period).min()
        denom = hh - ll
        denom = denom.replace(0, np.nan)

        chop = 100 * np.log10(atr_sum / denom) / np.log10(period)
        return chop

    # ------------------------------------------------------------------
    @staticmethod
    def _make_window(start: pd.Timestamp, end: pd.Timestamp, label: str, bars: int) -> dict:
        return {
            "start": start.isoformat(),
            "end": end.isoformat(),
            "label": label,
            "label_display": LABEL_DISPLAY.get(label, label),
            "bars": bars,
            "source": "auto",
        }
