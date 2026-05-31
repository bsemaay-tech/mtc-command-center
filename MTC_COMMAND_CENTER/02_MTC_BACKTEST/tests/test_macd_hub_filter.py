import pandas as pd

from src.modules.filters.macd_hub_filter import MacdHubFilter


def _df(rows: int = 220) -> pd.DataFrame:
    ts = pd.date_range("2026-01-01", periods=rows, freq="15min", tz="UTC")
    close = pd.Series([100.0 + (i * 0.03) + ((i // 40) % 2) * 0.8 for i in range(rows)])
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


def test_macd_hub_filter_modes_output_bool_series():
    df = _df()
    modes = ["Regime", "Cross-State", "Histogram", "Distance", "HTF Bias", "STANDARD", "PPO_NORM"]
    for mode in modes:
        f = MacdHubFilter(enabled=True, gate_mode=mode, distance_pct=0.01, htf_timeframe="240")
        allow_long, allow_short = f.apply(df)
        assert len(allow_long) == len(df)
        assert len(allow_short) == len(df)
        assert allow_long.dtype == bool
        assert allow_short.dtype == bool


def test_macd_hub_filter_debug_contains_core_lines():
    df = _df()
    f = MacdHubFilter(enabled=True, gate_mode="Regime")
    f.apply(df)
    dbg = f.get_debug_series(df)
    for key in ("macd_line", "macd_signal", "macd_hist", "allow_long", "allow_short"):
        assert key in dbg


def test_macd_standard_and_ppo_norm_use_regime_sign_not_cross_state():
    df = _df()
    f_std = MacdHubFilter(enabled=True, gate_mode="STANDARD")
    f_ppo = MacdHubFilter(enabled=True, gate_mode="PPO_NORM")
    std_long, std_short = f_std.apply(df)
    ppo_long, ppo_short = f_ppo.apply(df)

    dbg_std = f_std.get_debug_series(df)
    dbg_ppo = f_ppo.get_debug_series(df)

    # Pine defaults for both modes gate by line sign.
    assert std_long.equals((dbg_std["macd_line"] > 0).fillna(True).astype(bool))
    assert std_short.equals((dbg_std["macd_line"] < 0).fillna(True).astype(bool))
    assert ppo_long.equals((dbg_ppo["macd_line"] > 0).fillna(True).astype(bool))
    assert ppo_short.equals((dbg_ppo["macd_line"] < 0).fillna(True).astype(bool))
