"""Auto-generated prototype skeleton — QL_DEEPAK_153_FILTER_1D

Source: https://www.youtube.com/watch?v=lpjTNygfnzM
Source candidate: QLR_lpjTNygfnzM

HIGH-confidence rules from triage:
  - price > 200-day MA
  - price > 50-day MA
  - 50-day MA > 200-day MA
  - price > $75 (or quote-currency equivalent)

Status: FIRST_PASS_AUTO_GENERATED
Generated: 2026-05-31T00:09:34

Rule code below is a first-pass implementation. Sabah review için yeterli;
production parity için her kuralın detayı tekrar gözden geçirilmeli.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

CANDIDATE_ID = "QL_DEEPAK_153_FILTER_1D"
DIRECTION = "long_only"
DEFAULT_PARAMS = {'sma_short': 20, 'sma_long': 50, 'ema_trail': 21, 'atr_length': 14, 'stop_atr_mult': 1.5}

PARAM_GRID = {'sma_short': [50], 'sma_long': [200], 'min_price': [10.0, 50.0, 75.0]}


def _ema(s: pd.Series, length: int) -> pd.Series:
    return s.ewm(span=length, adjust=False).mean()


def _sma(s: pd.Series, length: int) -> pd.Series:
    return s.rolling(length, min_periods=1).mean()


def _atr(df: pd.DataFrame, length: int) -> pd.Series:
    tr = pd.concat([
        df["high"] - df["low"],
        (df["high"] - df["close"].shift(1)).abs(),
        (df["low"] - df["close"].shift(1)).abs(),
    ], axis=1).max(axis=1)
    return tr.rolling(length, min_periods=1).mean()


def signal_long_entry(df: pd.DataFrame, params: dict) -> pd.Series:
    """Return boolean entry signal series.

    Pseudocode from triage:
      long_ok = price>SMA200 AND price>SMA50 AND SMA50>SMA200 AND price>min_price
    """
    sma_s = _sma(df['close'], params.get('sma_short', 50))
    sma_l = _sma(df['close'], params.get('sma_long', 200))
    ok = (df['close'] > sma_s) & (df['close'] > sma_l) & (sma_s > sma_l)
    if 'min_price' in params:
        ok &= df['close'] >= params['min_price']
    return ok


def signal_long_exit(df: pd.DataFrame, params: dict, entry_index: int) -> bool:
    """Return True if exit conditions met at the current bar.

    Pseudocode from triage:
      N/A (filter overlay)
    """
    return False  # overlay does not emit exits


def is_filter_overlay() -> bool:
    return True


def is_exit_overlay() -> bool:
    return False
