"""
Task 0 — HTF Data Infrastructure unit tests.
TDD: run BEFORE creating htf.py / HtfSnapshot to confirm ImportError,
     then run again after creation to confirm 6 green tests.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from mtc_v2.core.htf import build_htf_lookup, resample_ohlcv
from mtc_v2.core.types import HtfSnapshot


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_df(n: int = 24) -> pd.DataFrame:
    """n hourly bars starting 2025-01-01 UTC."""
    idx = pd.date_range("2025-01-01", periods=n, freq="1h", tz="UTC")
    rng = np.random.default_rng(42)
    close = 100.0 + np.cumsum(rng.standard_normal(n))
    return pd.DataFrame(
        {"open": close, "high": close + 1, "low": close - 1, "close": close, "volume": 1.0},
        index=idx,
    )


# ---------------------------------------------------------------------------
# resample_ohlcv
# ---------------------------------------------------------------------------

def test_resample_ohlcv_4h_bar_count() -> None:
    df = _make_df(24)
    result = resample_ohlcv(df, "240")
    assert len(result) == 6  # 24 h / 4 h = 6 bars


def test_resample_ohlcv_first_bar_open_equals_ltf_first_open() -> None:
    df = _make_df(24)
    result = resample_ohlcv(df, "240")
    assert result["open"].iloc[0] == pytest.approx(df["open"].iloc[0])


def test_resample_ohlcv_unsupported_tf_raises() -> None:
    df = _make_df(24)
    with pytest.raises(ValueError, match="Unsupported HTF timeframe"):
        resample_ohlcv(df, "999")


# ---------------------------------------------------------------------------
# build_htf_lookup — prior-closed contract
# ---------------------------------------------------------------------------

def test_build_htf_lookup_first_4_ltf_bars_return_none() -> None:
    """With prior-closed ``close[1]`` timing, 4h-on-1h data first appears
    when the next 4h window starts at bar index 4 = 04:00. Bars 0–3 are NaN.
    """
    df = _make_df(24)
    lookup = build_htf_lookup(df, "240")
    for ts in df.index[:4]:
        assert lookup[ts] is None, f"Expected None for warmup bar {ts}"


def test_build_htf_lookup_bar_4_onwards_have_data() -> None:
    """Bars 4+ (04:00 onward in 4h/1h setup) carry a confirmed HTF close."""
    df = _make_df(24)
    lookup = build_htf_lookup(df, "240")
    for ts in df.index[4:]:
        assert lookup[ts] is not None, f"Expected dict for bar {ts}"
        assert "close" in lookup[ts]


def test_build_htf_lookup_keys_cover_all_ltf_bars() -> None:
    df = _make_df(24)
    lookup = build_htf_lookup(df, "240")
    assert set(lookup.keys()) == set(df.index)


def test_build_htf_lookup_lower_than_ltf_returns_no_data() -> None:
    df = _make_df(24)
    lookup = build_htf_lookup(df, "30")
    assert set(lookup.keys()) == set(df.index)
    assert all(value is None for value in lookup.values())


# ---------------------------------------------------------------------------
# HtfSnapshot
# ---------------------------------------------------------------------------

def test_htf_snapshot_from_dict_none_returns_not_ready() -> None:
    snap = HtfSnapshot.from_dict(None)
    assert not snap.is_ready


def test_htf_snapshot_from_dict_with_data_is_ready() -> None:
    snap = HtfSnapshot.from_dict(
        {"close": 100.0, "open": 99.0, "high": 101.0, "low": 98.0, "volume": 5.0}
    )
    assert snap.is_ready
    assert snap.close == pytest.approx(100.0)


def test_htf_snapshot_default_not_ready() -> None:
    snap = HtfSnapshot()
    assert not snap.is_ready


def test_runner_htf_adx_updates_on_every_ltf_bar() -> None:
    import datetime as dt

    from mtc_v2.core.runner import Runner
    from mtc_v2.core.types import Bar

    runner = Runner(
        {
            "use_adx_filter": True,
            "adx_use_higher_timeframe": True,
            "adx_htf_timeframe": "240",
            "adx_length": 2,
            "st_atr_len": 2,
        }
    )

    start = dt.datetime(2025, 1, 1, tzinfo=dt.timezone.utc)
    bars = [
        Bar(
            timestamp=start + dt.timedelta(hours=index),
            open=100.0 + index,
            high=101.0 + index,
            low=99.0 + index,
            close=100.5 + index,
            volume=1_000.0,
            bar_index=index,
        )
        for index in range(12)
    ]
    repeated_htf = {
        "open": 100.0,
        "high": 104.0,
        "low": 98.0,
        "close": 103.0,
        "volume": 10_000.0,
    }
    htf_data = {bar.timestamp: repeated_htf for bar in bars}

    runner.run(bars, htf_data=htf_data)

    assert runner.adx_tracker.adx is not None
