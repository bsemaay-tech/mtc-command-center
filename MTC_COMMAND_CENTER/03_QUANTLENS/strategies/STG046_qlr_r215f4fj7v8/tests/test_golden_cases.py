from python_signal_model import SignalConfig, compute_signals
from mtc_compatible_risk_adapter import RiskConfig, run_visual_debug_trades


def test_right_side_v_long_synthetic_case():
    rows = []
    for i in range(60):
        price = 100 + i * 0.03
        rows.append({"timestamp": f"2026-01-01T09:{i:02d}:00", "open": price, "high": price + 0.2, "low": price - 0.2, "close": price + 0.05, "volume": 1000})
    rows.append({"timestamp": "2026-01-01T10:00:00", "open": 98.0, "high": 98.2, "low": 94.0, "close": 94.5, "volume": 7000})
    rows.append({"timestamp": "2026-01-01T10:01:00", "open": 94.4, "high": 98.6, "low": 94.0, "close": 98.7, "volume": 4000})
    signals = compute_signals(rows, SignalConfig(warmup_bars=10, capitulation_vwap_distance_pct=1.0, enable_short=False))
    assert signals[-1]["raw_long_pulse"] is True
    assert signals[-1]["initial_stop_long"] != ""


def test_range_bound_no_signal_synthetic_case():
    rows = []
    for i in range(70):
        price = 100 + (0.05 if i % 2 == 0 else -0.05)
        rows.append({"timestamp": f"2026-01-01T09:{i:02d}:00", "open": price, "high": price + 0.1, "low": price - 0.1, "close": price, "volume": 1000})
    signals = compute_signals(rows, SignalConfig(warmup_bars=10, compression_width_pct=1.0))
    assert not any(row["raw_long_pulse"] or row["raw_short_pulse"] for row in signals[20:])


def test_debug_trade_exits_on_prior_bar_stop():
    rows = []
    for i in range(60):
        price = 100 + i * 0.03
        rows.append({"timestamp": f"2026-01-01T09:{i:02d}:00", "open": price, "high": price + 0.2, "low": price - 0.2, "close": price + 0.05, "volume": 1000})
    rows.append({"timestamp": "2026-01-01T10:00:00", "open": 98.0, "high": 98.2, "low": 94.0, "close": 94.5, "volume": 7000})
    rows.append({"timestamp": "2026-01-01T10:01:00", "open": 94.4, "high": 98.6, "low": 94.0, "close": 98.7, "volume": 4000})
    rows.append({"timestamp": "2026-01-01T10:02:00", "open": 98.6, "high": 98.8, "low": 93.5, "close": 94.0, "volume": 3000})
    signals = compute_signals(rows, SignalConfig(warmup_bars=10, capitulation_vwap_distance_pct=1.0, enable_short=False))
    trades, _ = run_visual_debug_trades(signals, RiskConfig(time_exit_bars=20))
    assert trades
    assert trades[0]["exit_reason"] == "prior_bar_low_trailing_stop"
