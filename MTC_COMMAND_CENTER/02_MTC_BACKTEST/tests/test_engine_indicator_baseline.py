import pandas as pd
import pytest

from src.engine.indicators import atr, rma, supertrend


def test_rma_seed_and_recursive_step():
    src = pd.Series([1.0, 2.0, 3.0, 4.0])
    out = rma(src, 3)

    # Seed at index=2 is SMA(1,2,3)=2
    assert out.iloc[2] == pytest.approx(2.0)
    # Next step: (1/3)*4 + (2/3)*2 = 2.666...
    assert out.iloc[3] == pytest.approx(2.6666667, rel=1e-6)


def test_atr_produces_expected_length_and_non_negative():
    high = pd.Series([10.0, 11.0, 12.0, 13.0, 12.0])
    low = pd.Series([9.0, 9.5, 10.5, 11.5, 11.0])
    close = pd.Series([9.5, 10.0, 11.0, 12.5, 11.5])
    out = atr(high, low, close, 3)

    assert len(out) == 5
    assert out.dropna().ge(0).all()


def test_supertrend_direction_domain():
    open_ = pd.Series([10.0, 10.2, 10.5, 10.8, 11.0, 10.9, 10.7, 10.6])
    high = pd.Series([10.3, 10.6, 10.9, 11.1, 11.2, 11.0, 10.9, 10.8])
    low = pd.Series([9.8, 10.0, 10.2, 10.6, 10.8, 10.5, 10.4, 10.3])
    close = pd.Series([10.1, 10.4, 10.7, 10.9, 10.95, 10.7, 10.5, 10.4])
    _, direction = supertrend(open_, high, low, close, atr_length=3, factor=2.0, use_wicks=True)

    vals = set(direction.dropna().astype(int).tolist())
    assert vals.issubset({-1, 1})
