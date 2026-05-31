import pandas as pd

from src.modules.filters.htf_trend_filter import HTFTrendFilter, _tf_to_pandas_rule


def _build_df(rows: int = 200) -> pd.DataFrame:
    ts = pd.date_range("2026-01-01", periods=rows, freq="15min", tz="UTC")
    close = pd.Series([100.0 + (i * 0.05) for i in range(rows)])
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


def test_tf_to_pandas_rule_supports_tv_numeric_minutes():
    assert _tf_to_pandas_rule("240") == "240min"
    assert _tf_to_pandas_rule("15m") == "15min"
    assert _tf_to_pandas_rule("4h") == "4h"


def test_htf_trend_filter_outputs_boolean_series():
    df = _build_df()
    f = HTFTrendFilter(enabled=True, timeframe="240", ma_type="EMA", ma_len=20, buffer_pct=0.0)
    allow_long, allow_short = f.apply(df)
    assert len(allow_long) == len(df)
    assert len(allow_short) == len(df)
    assert allow_long.dtype == bool
    assert allow_short.dtype == bool


def test_htf_trend_filter_has_debug_series():
    df = _build_df()
    f = HTFTrendFilter(enabled=True, timeframe="240", ma_type="EMA", ma_len=20, buffer_pct=0.1)
    f.apply(df)
    dbg = f.get_debug_series(df)
    for key in ("htf_close", "htf_ma", "htf_allow_long", "htf_allow_short", "aligned_allow_long", "aligned_allow_short"):
        assert key in dbg
