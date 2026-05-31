from __future__ import annotations

import pandas as pd


def ema(series: pd.Series, length: int) -> pd.Series:
    return series.ewm(span=length, adjust=False, min_periods=length).mean()


def sma(series: pd.Series, length: int) -> pd.Series:
    return series.rolling(length, min_periods=length).mean()


def atr(data: pd.DataFrame, length: int = 14) -> pd.Series:
    parts = pd.concat(
        [
            data["high"] - data["low"],
            (data["high"] - data["close"].shift(1)).abs(),
            (data["low"] - data["close"].shift(1)).abs(),
        ],
        axis=1,
    )
    return parts.max(axis=1).rolling(length, min_periods=length).mean()


def rsi(close: pd.Series, length: int = 14) -> pd.Series:
    delta = close.diff()
    gain = delta.clip(lower=0).rolling(length, min_periods=length).mean()
    loss = (-delta.clip(upper=0)).rolling(length, min_periods=length).mean()
    rs = gain / loss.replace(0, pd.NA)
    return 100 - (100 / (1 + rs))


def rolling_vwap_proxy(data: pd.DataFrame, length: int = 50) -> pd.Series:
    typical = (data["high"] + data["low"] + data["close"]) / 3
    volume = data["volume"].replace(0, 1.0)
    return (typical * volume).rolling(length, min_periods=length).sum() / volume.rolling(length, min_periods=length).sum()
