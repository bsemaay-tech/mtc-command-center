import numpy as np
import pandas as pd

from src.modules.signals.producers import create_producer


def _wave_df(n: int = 300) -> pd.DataFrame:
    idx = pd.date_range("2025-01-01", periods=n, freq="15min", tz="UTC")
    close = 100.0 + np.cumsum(np.sin(np.arange(n) / 5.0))
    return pd.DataFrame(
        {
            "timestamp": idx,
            "open": close - 0.1,
            "high": close + 0.5,
            "low": close - 0.5,
            "close": close,
            "volume": 1000.0,
        }
    )


def test_producer_generate_returns_aligned_boolean_signals():
    producer = create_producer("supertrend")
    df = _wave_df()

    long_raw, short_raw = producer.generate(df)

    assert long_raw.dtype == bool
    assert short_raw.dtype == bool
    assert len(long_raw) == len(df)
    assert len(short_raw) == len(df)
    # Supertrend direction is exclusive: a bar is never both long and short.
    assert not (long_raw & short_raw).any()
    # No NaN leaked into the boolean stream.
    assert not long_raw.isna().any()
    assert not short_raw.isna().any()


def test_producer_generate_is_deterministic():
    producer = create_producer("supertrend")
    df = _wave_df()

    l1, s1 = producer.generate(df)
    l2, s2 = producer.generate(df)

    assert l1.equals(l2)
    assert s1.equals(s2)


def test_quantlens_momentum_continuation_returns_long_only_aligned_signals():
    producer = create_producer(
        "ql_fam_momentum_continuation",
        {"mom_lb": 3, "trend_ema": 5, "breakout_lb": 4},
    )
    df = _wave_df(120)

    long_raw, short_raw = producer.generate(df)

    assert producer.name == "producer_ql_fam_momentum_continuation"
    assert long_raw.dtype == bool
    assert short_raw.dtype == bool
    assert len(long_raw) == len(df)
    assert len(short_raw) == len(df)
    assert not short_raw.any()
    assert not long_raw.isna().any()
    assert not short_raw.isna().any()


def test_quantlens_momentum_continuation_uses_prior_breakout_channel():
    producer = create_producer(
        "ql_fam_momentum_continuation",
        {"mom_lb": 2, "trend_ema": 3, "breakout_lb": 3},
    )
    idx = pd.date_range("2025-01-01", periods=8, freq="4h", tz="UTC")
    close = pd.Series([10.0, 10.1, 10.2, 10.3, 10.4, 10.45, 11.0, 11.3])
    df = pd.DataFrame(
        {
            "timestamp": idx,
            "open": close - 0.05,
            "high": [10.1, 10.2, 10.3, 10.4, 10.5, 11.2, 11.1, 11.35],
            "low": close - 0.2,
            "close": close,
            "volume": 1000.0,
        }
    )

    long_raw, short_raw = producer.generate(df)
    debug = producer.get_debug_series(df)

    assert not short_raw.any()
    assert not bool(long_raw.iloc[5])
    assert not bool(long_raw.iloc[6])
    assert bool(long_raw.iloc[7])
    assert debug["chan_hi"].iloc[6] == df["high"].iloc[3:6].max()
