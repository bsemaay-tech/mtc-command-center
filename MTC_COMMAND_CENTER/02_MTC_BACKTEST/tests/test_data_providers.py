"""Unit tests for data_providers (BinanceProvider and CsvProvider)."""
from __future__ import annotations

import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

# Ensure the package root is on sys.path
_PKG = Path(__file__).resolve().parent.parent
if str(_PKG) not in sys.path:
    sys.path.insert(0, str(_PKG))

from data_providers.binance_provider import BinanceProvider, _rows_to_df
from data_providers.binance_usdm_provider import BinanceUsdmProvider
from data_providers.csv_provider import CsvProvider
from data_providers import get_provider


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_raw_row(ts_ms: int, o=100.0, h=105.0, lo=98.0, c=102.0, v=1000.0):
    return [ts_ms, o, h, lo, c, v]


def _make_rows(n=5, start_ms=1_530_403_200_000, interval_ms=15 * 60 * 1000):
    return [_make_raw_row(start_ms + i * interval_ms) for i in range(n)]


# ---------------------------------------------------------------------------
# BinanceProvider
# ---------------------------------------------------------------------------

class TestBinanceProvider:

    @patch("data_providers.binance_provider.ccxt")
    def _make_provider(self, mock_ccxt):
        mock_exchange = MagicMock()
        mock_ccxt.binance.return_value = mock_exchange
        provider = BinanceProvider.__new__(BinanceProvider)
        provider._exchange = mock_exchange
        provider._sleep_s = 0.0
        return provider, mock_exchange

    def test_rows_to_df_utc_index(self):
        rows = _make_rows(5)
        df = _rows_to_df(rows)
        assert df.index.tz is not None
        assert str(df.index.tz) == "UTC"

    def test_rows_to_df_columns(self):
        rows = _make_rows(3)
        df = _rows_to_df(rows)
        assert list(df.columns) == ["open", "high", "low", "close", "volume"]

    def test_rows_to_df_dtypes(self):
        rows = _make_rows(3)
        df = _rows_to_df(rows)
        for col in df.columns:
            assert df[col].dtype == "float64", f"{col} should be float64"

    def test_rows_to_df_deduplicates(self):
        rows = _make_rows(5)
        duplicated = rows + rows[:2]  # 2 duplicate timestamps
        df = _rows_to_df(duplicated)
        assert not df.index.duplicated().any()
        assert len(df) == 5

    def test_rows_to_df_sorted(self):
        rows = _make_rows(5)
        shuffled = list(reversed(rows))
        df = _rows_to_df(shuffled)
        assert df.index.is_monotonic_increasing

    def test_invalid_timeframe_raises(self):
        import ccxt as _ccxt
        real_provider = BinanceProvider.__new__(BinanceProvider)
        real_provider._exchange = MagicMock()
        real_provider._sleep_s = 0.0
        with pytest.raises(ValueError, match="Unsupported timeframe"):
            real_provider.fetch_ohlcv(
                "BTCUSDT",
                datetime(2023, 1, 1, tzinfo=timezone.utc),
                datetime(2023, 1, 2, tzinfo=timezone.utc),
                "3m",
            )

    def test_fetch_ohlcv_returns_utc_df(self):
        provider = BinanceProvider.__new__(BinanceProvider)
        mock_exchange = MagicMock()
        provider._exchange = mock_exchange
        provider._sleep_s = 0.0

        rows = _make_rows(3)
        # Return rows once, then empty (to stop pagination)
        mock_exchange.fetch_ohlcv.side_effect = [rows, []]

        start = datetime(2018, 7, 1, tzinfo=timezone.utc)
        end = datetime(2018, 7, 2, tzinfo=timezone.utc)
        df = provider.fetch_ohlcv("BTCUSDT", start, end, "15m")

        assert isinstance(df.index, pd.DatetimeIndex)
        assert str(df.index.tz) == "UTC"
        assert len(df) == 3


# ---------------------------------------------------------------------------
# CsvProvider
# ---------------------------------------------------------------------------

class TestCsvProvider:

    def _make_csv(self, tmp_path: Path, n=10) -> Path:
        rows = []
        for i in range(n):
            ts = pd.Timestamp("2023-01-01", tz="UTC") + pd.Timedelta(hours=i)
            rows.append({
                "timestamp": ts.isoformat(),
                "open": 100.0 + i,
                "high": 105.0 + i,
                "low": 98.0 + i,
                "close": 102.0 + i,
                "volume": 1000.0 + i,
            })
        df = pd.DataFrame(rows)
        p = tmp_path / "test_data.csv"
        df.to_csv(p, index=False)
        return p

    def test_reads_csv_correctly(self, tmp_path):
        p = self._make_csv(tmp_path, n=10)
        provider = CsvProvider(p)
        start = datetime(2023, 1, 1, tzinfo=timezone.utc)
        end = datetime(2023, 1, 2, tzinfo=timezone.utc)
        df = provider.fetch_ohlcv("TEST", start, end, "1h")
        assert list(df.columns) == ["open", "high", "low", "close", "volume"]
        assert str(df.index.tz) == "UTC"

    def test_csv_date_filter(self, tmp_path):
        p = self._make_csv(tmp_path, n=24)
        provider = CsvProvider(p)
        start = datetime(2023, 1, 1, 5, tzinfo=timezone.utc)
        end = datetime(2023, 1, 1, 9, tzinfo=timezone.utc)
        df = provider.fetch_ohlcv("TEST", start, end, "1h")
        # Should return bars at 5h, 6h, 7h, 8h, 9h = 5 bars
        assert len(df) == 5

    def test_missing_columns_raises(self, tmp_path):
        p = tmp_path / "bad.csv"
        p.write_text("timestamp,open,high\n2023-01-01,100,105\n")
        provider = CsvProvider(p)
        with pytest.raises(ValueError, match="missing OHLCV columns"):
            provider.fetch_ohlcv("TEST", datetime(2023, 1, 1, tzinfo=timezone.utc),
                                 datetime(2023, 1, 2, tzinfo=timezone.utc), "1d")

    def test_is_24_7_default_false(self, tmp_path):
        p = self._make_csv(tmp_path, n=3)
        provider = CsvProvider(p)
        assert provider.is_24_7 is False

    def test_is_24_7_configurable(self, tmp_path):
        p = self._make_csv(tmp_path, n=3)
        provider = CsvProvider(p, is_market_24_7=True)
        assert provider.is_24_7 is True


# ---------------------------------------------------------------------------
# get_provider factory
# ---------------------------------------------------------------------------

class TestGetProvider:

    def test_binance(self):
        p = get_provider("binance", sleep_ms=0)
        assert p.name == "binance"
        assert p.is_24_7 is True

    def test_csv(self, tmp_path):
        f = tmp_path / "dummy.csv"
        f.write_text("timestamp,open,high,low,close,volume\n")
        p = get_provider("csv", filepath=str(f))
        assert p.name == "csv"

    def test_binance_usdm_symbol_normalization(self):
        assert BinanceUsdmProvider._normalize_symbol("BTCUSDT.P") == "BTC/USDT:USDT"
        assert BinanceUsdmProvider._normalize_symbol("BTCUSDT") == "BTC/USDT:USDT"
        assert BinanceUsdmProvider._normalize_symbol("BTC/USDT:USDT") == "BTC/USDT:USDT"

    def test_binance_usdm_factory(self):
        p = get_provider("binance_usdm", sleep_ms=0)
        assert p.name == "binance_usdm"
        assert p.is_24_7 is True

    def test_unknown_raises(self):
        with pytest.raises(ValueError, match="Unknown provider"):
            get_provider("unknown_source")
