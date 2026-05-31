import pandas as pd

from src.modules.filters.range_regime_filter import RangeRegimeFilter


def _df(rows: int = 160) -> pd.DataFrame:
    ts = pd.date_range("2026-01-01", periods=rows, freq="15min", tz="UTC")
    close = pd.Series([100.0 + (i % 25) * 0.08 for i in range(rows)])
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


def test_range_regime_filter_returns_bool_series():
    df = _df()
    f = RangeRegimeFilter(enabled=True, adx_min=10.0, chop_max=70.0, hold_bars=3)
    allow_long, allow_short = f.apply(df)
    assert len(allow_long) == len(df)
    assert len(allow_short) == len(df)
    assert allow_long.dtype == bool
    assert allow_short.dtype == bool


def test_range_regime_filter_debug_keys():
    df = _df()
    f = RangeRegimeFilter(enabled=True)
    f.apply(df)
    dbg = f.get_debug_series(df)
    for key in ("adx", "chop", "raw_regime_ok", "held_regime_ok"):
        assert key in dbg


def test_range_regime_count_mode_is_not_stricter_than_and():
    df = _df()
    and_filter = RangeRegimeFilter(enabled=True, hold_bars=0, agg_mode="AND", min_pass=2)
    count_filter = RangeRegimeFilter(enabled=True, hold_bars=0, agg_mode="COUNT", min_pass=1)
    allow_and, _ = and_filter.apply(df)
    allow_count, _ = count_filter.apply(df)
    assert int(allow_count.sum()) >= int(allow_and.sum())
