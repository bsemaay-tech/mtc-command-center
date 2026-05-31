import pandas as pd

from src.modules.signals.range_filter import RangeFilterHybridSignal


def _sample_df(rows: int = 120) -> pd.DataFrame:
    ts = pd.date_range("2026-01-01", periods=rows, freq="15min", tz="UTC")
    # Deterministic wave-shaped path to trigger trend/range windows.
    base = pd.Series(range(rows), dtype=float)
    close = 100.0 + (base % 20) * 0.2 - ((base // 20) % 2) * 1.5
    open_ = close.shift(1).fillna(close.iloc[0])
    high = pd.concat([open_, close], axis=1).max(axis=1) + 0.3
    low = pd.concat([open_, close], axis=1).min(axis=1) - 0.3
    return pd.DataFrame(
        {
            "timestamp": ts,
            "open": open_.to_numpy(),
            "high": high.to_numpy(),
            "low": low.to_numpy(),
            "close": close.to_numpy(),
            "volume": [100] * rows,
        }
    )


def test_range_filter_signal_returns_boolean_series_with_expected_length():
    df = _sample_df()
    sig = RangeFilterHybridSignal()
    long_raw, short_raw = sig.generate(df)

    assert len(long_raw) == len(df)
    assert len(short_raw) == len(df)
    assert long_raw.dtype == bool
    assert short_raw.dtype == bool


def test_range_filter_signal_debug_series_contains_core_keys():
    df = _sample_df()
    sig = RangeFilterHybridSignal(use_bb_filter=True)
    sig.generate(df)
    dbg = sig.get_debug_series(df)

    for key in ("adx", "chop", "rsi", "bb_upper", "bb_mid", "bb_lower", "regime_trend", "regime_range"):
        assert key in dbg


def test_range_filter_signal_supports_bb_disabled_mode():
    df = _sample_df()
    sig = RangeFilterHybridSignal(use_bb_filter=False)
    long_raw, short_raw = sig.generate(df)
    # No BB gate still must provide deterministic bool outputs.
    assert long_raw.dtype == bool
    assert short_raw.dtype == bool


def test_range_filter_signal_zero_guards_keep_dmi_debug_finite():
    rows = 80
    ts = pd.date_range("2026-01-01", periods=rows, freq="15min", tz="UTC")
    df = pd.DataFrame(
        {
            "timestamp": ts,
            "open": [100.0] * rows,
            "high": [100.0] * rows,
            "low": [100.0] * rows,
            "close": [100.0] * rows,
            "volume": [100] * rows,
        }
    )

    sig = RangeFilterHybridSignal()
    sig.generate(df)
    dbg = sig.get_debug_series(df)

    for key in ("adx", "plus_di", "minus_di"):
        series = dbg[key]
        tail = series.iloc[30:]
        assert tail.notna().all()
        assert (tail == 0).all()
