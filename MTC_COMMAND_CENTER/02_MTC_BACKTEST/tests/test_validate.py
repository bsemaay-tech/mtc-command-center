"""Unit tests for the data validator (validate.py checks)."""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

_PKG = Path(__file__).resolve().parent.parent
if str(_PKG) not in sys.path:
    sys.path.insert(0, str(_PKG))

from data_tools.validate import (
    check_duplicates,
    check_gaps,
    check_monotonic,
    check_ohlc_sanity,
    check_utc,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_df(n=20, freq="15min", tz="UTC", gaps: list[int] | None = None) -> pd.DataFrame:
    """Create a clean synthetic OHLCV DataFrame."""
    idx = pd.date_range("2023-01-01", periods=n, freq=freq, tz=tz)
    df = pd.DataFrame(
        {
            "open": np.linspace(100, 110, n),
            "high": np.linspace(105, 115, n),
            "low": np.linspace(95, 105, n),
            "close": np.linspace(102, 112, n),
            "volume": np.ones(n) * 500,
        },
        index=idx,
    )
    # Ensure OHLC sanity: high >= max(O,C), low <= min(O,C)
    df["high"] = df[["open", "close"]].max(axis=1) + 2
    df["low"] = df[["open", "close"]].min(axis=1) - 2
    if gaps:
        idx_list = list(df.index)
        for gap_pos in gaps:
            if gap_pos < len(idx_list):
                idx_list[gap_pos] = idx_list[gap_pos - 1] + pd.Timedelta(hours=6)  # large gap
        df.index = pd.DatetimeIndex(idx_list, tz=tz)
    return df


# ---------------------------------------------------------------------------
# check_monotonic
# ---------------------------------------------------------------------------

class TestCheckMonotonic:
    def test_clean_df_is_ok(self):
        df = _make_df(10)
        r = check_monotonic(df)
        assert r.status == "OK"

    def test_non_monotonic_returns_error(self):
        df = _make_df(10)
        idx = list(df.index)
        idx[5], idx[3] = idx[3], idx[5]  # swap
        df.index = pd.DatetimeIndex(idx, tz="UTC")
        r = check_monotonic(df)
        assert r.status == "ERROR"


# ---------------------------------------------------------------------------
# check_duplicates
# ---------------------------------------------------------------------------

class TestCheckDuplicates:
    def test_no_duplicates_ok(self):
        df = _make_df(10)
        r = check_duplicates(df)
        assert r.status == "OK"

    def test_duplicate_timestamp_error(self):
        df = _make_df(10)
        idx = list(df.index)
        idx[5] = idx[4]  # duplicate
        df.index = pd.DatetimeIndex(idx, tz="UTC")
        r = check_duplicates(df)
        assert r.status == "ERROR"
        assert "1" in r.message


# ---------------------------------------------------------------------------
# check_utc
# ---------------------------------------------------------------------------

class TestCheckUTC:
    def test_utc_is_ok(self):
        df = _make_df(10, tz="UTC")
        r = check_utc(df)
        assert r.status == "OK"

    def test_naive_is_error(self):
        df = _make_df(10, tz="UTC").tz_localize(None)
        r = check_utc(df)
        assert r.status == "ERROR"
        assert "no timezone" in r.message.lower()

    def test_non_utc_tz_error(self):
        df = _make_df(10, tz="Europe/London")
        r = check_utc(df)
        assert r.status == "ERROR"
        assert "UTC" in r.message


# ---------------------------------------------------------------------------
# check_gaps
# ---------------------------------------------------------------------------

class TestCheckGaps:
    def test_no_gaps_ok(self):
        df = _make_df(20, freq="15min")
        r = check_gaps(df, "15m", is_24_7=True)
        assert r.status == "OK"

    def test_session_market_skips_gap_check(self):
        # Session-based market — gap check must be skipped regardless
        df = _make_df(10, freq="15min")
        # Introduce a huge gap
        idx = list(df.index)
        idx[5] = idx[4] + pd.Timedelta(hours=48)
        df.index = pd.DatetimeIndex(idx, tz="UTC")
        r = check_gaps(df, "15m", is_24_7=False)
        assert r.status == "OK"
        assert "skipped" in r.message.lower()

    def test_warn_level_gap(self):
        # Gap of 3× interval (45m for 15m TF) → WARN
        df = _make_df(20, freq="15min")
        idx = list(df.index)
        idx[10] = idx[9] + pd.Timedelta(minutes=45)  # 3× gap
        df.index = pd.DatetimeIndex(idx, tz="UTC")
        r = check_gaps(df, "15m", is_24_7=True)
        assert r.status == "WARN"

    def test_error_level_gap(self):
        # Gap of 15× interval (225m for 15m TF) → ERROR
        df = _make_df(20, freq="15min")
        idx = list(df.index)
        idx[10] = idx[9] + pd.Timedelta(minutes=225)
        df.index = pd.DatetimeIndex(idx, tz="UTC")
        r = check_gaps(df, "15m", is_24_7=True)
        assert r.status == "ERROR"


# ---------------------------------------------------------------------------
# check_ohlc_sanity
# ---------------------------------------------------------------------------

class TestCheckOHLCSanity:
    def test_clean_df_ok(self):
        df = _make_df(10)
        r = check_ohlc_sanity(df)
        assert r.status == "OK"

    def test_high_less_than_close_error(self):
        df = _make_df(10)
        df.iloc[3, df.columns.get_loc("high")] = df.iloc[3]["close"] - 5  # high < close
        r = check_ohlc_sanity(df)
        assert r.status == "ERROR"
        assert "high" in r.message.lower()

    def test_low_greater_than_open_error(self):
        df = _make_df(10)
        df.iloc[2, df.columns.get_loc("low")] = df.iloc[2]["open"] + 5  # low > open
        r = check_ohlc_sanity(df)
        assert r.status == "ERROR"
        assert "low" in r.message.lower()

    def test_negative_volume_error(self):
        df = _make_df(10)
        df.iloc[1, df.columns.get_loc("volume")] = -1.0
        r = check_ohlc_sanity(df)
        assert r.status == "ERROR"
        assert "volume" in r.message.lower()
