"""Auto-generated prototype skeleton — QL_DEEPAK_259_RISK_OVERLAY

Source: https://www.youtube.com/watch?v=oPeTkxTnooA
Source candidate: QLR_oPeTkxTnooA

HIGH-confidence rules from triage:
  - Position sizing: 1% portfolio risk per trade
  - Calculated stop distance → share count = portfolio*0.01/stop_distance
  - Cap stops at technical levels OR 8% generic, whichever tighter

Status: FIRST_PASS_AUTO_GENERATED
Generated: 2026-05-31T00:09:34

Rule code below is a first-pass implementation. Sabah review için yeterli;
production parity için her kuralın detayı tekrar gözden geçirilmeli.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

CANDIDATE_ID = "QL_DEEPAK_259_RISK_OVERLAY"
DIRECTION = "long_only"
DEFAULT_PARAMS = {'sma_short': 20, 'sma_long': 50, 'ema_trail': 21, 'atr_length': 14, 'stop_atr_mult': 1.5}

PARAM_GRID = {'trail_sma': [10, 20, 50], 'trim_pct': [0.5, 1.0]}


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
      N/A (sizing overlay)
    """
    return pd.Series(False, index=df.index)  # overlay has no entry


def signal_long_exit(df: pd.DataFrame, params: dict, entry_index: int) -> bool:
    """Return True if exit conditions met at the current bar.

    Pseudocode from triage:
      N/A (sizing overlay)
    """
    trail = _sma(df['close'], params.get('trail_sma', 20))
    return bool(df['close'].iloc[entry_index] < trail.iloc[entry_index])


def is_filter_overlay() -> bool:
    return False


def is_exit_overlay() -> bool:
    return True
