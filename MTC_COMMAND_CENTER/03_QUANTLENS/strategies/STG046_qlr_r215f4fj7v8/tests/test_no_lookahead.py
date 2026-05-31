from python_signal_model import SignalConfig, compute_signals


def _rows():
    rows = []
    for i in range(80):
        price = 100 + i * 0.05
        rows.append({"timestamp": f"2026-01-01T09:{i:02d}:00", "open": price, "high": price + 0.2, "low": price - 0.2, "close": price + 0.1, "volume": 1000})
    rows[60] = {"timestamp": "2026-01-01T10:00:00", "open": 104, "high": 104.2, "low": 96, "close": 96.5, "volume": 5000}
    rows[61] = {"timestamp": "2026-01-01T10:01:00", "open": 96.4, "high": 98.5, "low": 95.8, "close": 98.6, "volume": 3500}
    return rows


def test_signal_for_prefix_matches_full_run_at_same_bar():
    cfg = SignalConfig(warmup_bars=10, capitulation_vwap_distance_pct=1.0)
    full = compute_signals(_rows(), cfg)
    prefix = compute_signals(_rows()[:62], cfg)
    assert full[61]["raw_long_pulse"] == prefix[61]["raw_long_pulse"]
    assert full[61]["right_side_v_long"] == prefix[61]["right_side_v_long"]
