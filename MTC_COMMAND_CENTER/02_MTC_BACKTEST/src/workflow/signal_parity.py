"""Producer-level raw-signal parity comparison.

Compares Python producer raw long/short signals against the PineTS feature-adapter
export (raw_long / raw_short columns). This is L0-L3 producer-level parity only —
it does NOT assert full lifecycle (L4-L6) parity.
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

import pandas as pd

RAW_LONG_TITLE = "FEATURE__producer_supertrend_v1__signal__raw_long"
RAW_SHORT_TITLE = "FEATURE__producer_supertrend_v1__signal__raw_short"


def _as_bool_series(values: Iterable) -> pd.Series:
    return pd.Series(list(values)).astype(bool).reset_index(drop=True)


def compare_signals(
    py_long: Iterable,
    py_short: Iterable,
    pine_long: Iterable,
    pine_short: Iterable,
    min_match_rate: float = 1.0,
) -> dict:
    """Compare Python vs Pine raw long/short signal streams.

    Streams are aligned from the start and truncated to the shorter length.
    Returns match counts/rates, the mismatching bar indices, and a PASS/FAIL
    status. PASS requires both long and short match rates >= ``min_match_rate``.
    """
    pl = _as_bool_series(py_long)
    ps = _as_bool_series(py_short)
    kl = _as_bool_series(pine_long)
    ks = _as_bool_series(pine_short)

    n = min(len(pl), len(kl), len(ps), len(ks))
    if n == 0:
        raise ValueError("No bars to compare (one of the signal streams is empty)")

    pl, ps, kl, ks = pl.iloc[:n], ps.iloc[:n], kl.iloc[:n], ks.iloc[:n]

    long_eq = pl.values == kl.values
    short_eq = ps.values == ks.values
    long_match = int(long_eq.sum())
    short_match = int(short_eq.sum())
    long_rate = long_match / n
    short_rate = short_match / n

    return {
        "bars": n,
        "long_match": long_match,
        "short_match": short_match,
        "long_match_rate": long_rate,
        "short_match_rate": short_rate,
        "long_mismatch_bars": [i for i in range(n) if not long_eq[i]],
        "short_mismatch_bars": [i for i in range(n) if not short_eq[i]],
        "min_match_rate": min_match_rate,
        "status": "PASS" if (long_rate >= min_match_rate and short_rate >= min_match_rate) else "FAIL",
    }


def load_pine_signals_csv(
    path: str | Path,
    long_title: str = RAW_LONG_TITLE,
    short_title: str = RAW_SHORT_TITLE,
) -> tuple[pd.Series, pd.Series]:
    """Load raw_long / raw_short boolean streams from a PineTS export CSV.

    Columns are matched by exact plotted title first, then by a suffix fallback
    (the trailing ``signal__raw_long`` / ``signal__raw_short`` segment).
    """
    df = pd.read_csv(path)

    def pick(title: str) -> pd.Series:
        if title in df.columns:
            return (df[title].astype(float) > 0.5).reset_index(drop=True)
        suffix = title.split("__signal__")[-1]
        for col in df.columns:
            if str(col).strip().endswith(suffix):
                return (df[col].astype(float) > 0.5).reset_index(drop=True)
        raise KeyError(f"Signal column not found for title {title!r}. Columns: {list(df.columns)}")

    return pick(long_title), pick(short_title)
