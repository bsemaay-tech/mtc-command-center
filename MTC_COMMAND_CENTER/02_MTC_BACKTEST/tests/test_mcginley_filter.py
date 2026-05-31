import pandas as pd

from src.engine.indicators import mcginley_dynamic
from src.modules.filters.mcginley_filter import McGinleyFilter


def _df(rows: int = 120) -> pd.DataFrame:
    ts = pd.date_range("2026-01-01", periods=rows, freq="15min", tz="UTC")
    close = pd.Series([100.0 + i * 0.1 for i in range(rows)])
    open_ = close.shift(1).fillna(close.iloc[0])
    high = pd.concat([open_, close], axis=1).max(axis=1) + 0.2
    low = pd.concat([open_, close], axis=1).min(axis=1) - 0.2
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


def test_mcginley_dynamic_outputs_series():
    src = pd.Series([100.0, 101.0, 102.0, 103.0, 104.0])
    out = mcginley_dynamic(src, length=5, k=0.6)
    assert len(out) == len(src)
    assert out.notna().sum() >= 1


def test_mcginley_filter_returns_bool_series():
    df = _df()
    f = McGinleyFilter(enabled=True, length=20, k=0.6)
    allow_long, allow_short = f.apply(df)
    assert len(allow_long) == len(df)
    assert len(allow_short) == len(df)
    assert allow_long.dtype == bool
    assert allow_short.dtype == bool


def test_mcginley_filter_debug_contains_line():
    df = _df()
    f = McGinleyFilter(enabled=True, length=20, k=0.6)
    f.apply(df)
    dbg = f.get_debug_series(df)
    assert "mcginley_line" in dbg


def test_mcginley_filter_htf_resample_changes_line_shape():
    df = _df()
    base = McGinleyFilter(enabled=True, length=20, k=0.6)
    htf = McGinleyFilter(enabled=True, length=20, k=0.6, use_htf=True, htf_timeframe="60")
    base.apply(df)
    htf.apply(df)
    base_line = base.get_debug_series(df)["mcginley_line"]
    htf_line = htf.get_debug_series(df)["mcginley_line"]
    assert len(htf_line) == len(df)
    assert not base_line.equals(htf_line)
