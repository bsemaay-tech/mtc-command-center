"""Auto-generated prototype skeleton — QL_VCP_RICHARD_1D

Source: https://www.youtube.com/watch?v=Tm0dkf8_giA
Source candidate: QLR_Tm0dkf8_giA

HIGH-confidence rules from triage:
  - 2+ successive lower-amplitude contractions within a base
  - volume declines on each contraction, surges on breakout
  - entry at pivot-point breakout (prior resistance)
  - stop at low of base OR low of breakout day
  - trail under 21 EMA

Status: FIRST_PASS_AUTO_GENERATED
Generated: 2026-05-31T00:09:34

Rule code below is a first-pass implementation. Sabah review için yeterli;
production parity için her kuralın detayı tekrar gözden geçirilmeli.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

CANDIDATE_ID = "QL_VCP_RICHARD_1D"
DIRECTION = "long_only"
DEFAULT_PARAMS = {'sma_short': 20, 'sma_long': 50, 'ema_trail': 21, 'atr_length': 14, 'stop_atr_mult': 1.5}

PARAM_GRID = {'sma_short': [10, 20, 50], 'sma_long': [100, 200], 'ema_trail': [9, 21, 50], 'atr_length': [14], 'stop_atr_mult': [1.0, 1.5, 2.0], 'min_volume_mult': [1.0, 1.5, 2.0], 'gap_pct_thresh': [3.0, 5.0, 8.0], 'vol_rank_thresh': [0.8, 0.9, 0.95]}


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
      contractions>=2 AND close>pivot AND vol>1.5*avg20
    """
    sma_s = _sma(df['close'], params.get('sma_short', 20))
    sma_l = _sma(df['close'], params.get('sma_long', 50))
    vol_ok = df['volume'] > params.get('min_volume_mult', 1.5) * df['volume'].rolling(20, min_periods=1).mean()
    cross = (df['close'] > sma_s) & (df['close'].shift(1) <= sma_s.shift(1))
    trend = sma_s > sma_l
    return cross & trend & vol_ok



def signal_long_exit(df: pd.DataFrame, params: dict, entry_index: int) -> bool:
    """Return True if exit conditions met at the current bar.

    Pseudocode from triage:
      close<EMA21 OR close<stop
    """
    trail = _ema(df['close'], params.get('ema_trail', 21))
    atr = _atr(df, params.get('atr_length', 14))
    stop_mult = params.get('stop_atr_mult', 1.5)
    entry_price = df['close'].iloc[entry_index]
    current = df['close'].iloc[-1]
    return bool(current < trail.iloc[-1] or current < entry_price - stop_mult * atr.iloc[entry_index])



def is_filter_overlay() -> bool:
    return False


def is_exit_overlay() -> bool:
    return False
