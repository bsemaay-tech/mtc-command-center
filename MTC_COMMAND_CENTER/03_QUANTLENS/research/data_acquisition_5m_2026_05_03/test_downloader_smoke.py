from __future__ import annotations

import importlib.util
from pathlib import Path


MODULE_PATH = Path(__file__).with_name("download_binance_futures_5m.py")


def load_module():
    spec = importlib.util.spec_from_file_location("download_binance_futures_5m", MODULE_PATH)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_normalize_klines_smoke():
    module = load_module()
    rows = [
        [
            1704067200000,
            "100.0",
            "101.0",
            "99.5",
            "100.5",
            "42.0",
            1704067499999,
            "0",
            1,
            "0",
            "0",
            "0",
        ]
    ]
    frame = module.normalize_klines(rows)
    assert list(frame.columns) == ["timestamp", "open", "high", "low", "close", "volume"]
    assert frame.loc[0, "timestamp"] == "2024-01-01T00:00:00+00:00"
    assert frame.loc[0, "close"] == 100.5


def test_bundle_symbol_list_contains_minimum_assets():
    module = load_module()
    symbols = set(module.bundle_symbols())
    assert {"BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT", "XRPUSDT"}.issubset(symbols)
