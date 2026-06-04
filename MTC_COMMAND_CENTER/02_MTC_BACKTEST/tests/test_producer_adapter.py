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
