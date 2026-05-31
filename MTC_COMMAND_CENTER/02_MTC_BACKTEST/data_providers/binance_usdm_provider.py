"""Binance USD-M perpetual futures OHLCV provider using ccxt."""
from __future__ import annotations

import time
from datetime import datetime, timezone

import pandas as pd
from tqdm import tqdm

from .base import OHLCVProvider

TIMEFRAME_MAP: dict[str, str] = {
    "5m": "5m",
    "15m": "15m",
    "1h": "1h",
    "2h": "2h",
    "4h": "4h",
    "1d": "1d",
}

_BINANCE_LIMIT = 1000


class BinanceUsdmProvider(OHLCVProvider):
    """
    Fetches OHLCV data from Binance USD-M perpetual futures via ccxt.

    Expected upstream symbol forms:
    - ``BTCUSDT.P`` (TradingView workbook symbol)
    - ``BTCUSDT``   (normalized internally to perpetual futures market)
    - ``BTC/USDT:USDT`` (native ccxt symbol)
    """

    def __init__(self, sleep_ms: int = 100) -> None:
        import ccxt  # lazy import

        self._exchange = ccxt.binanceusdm({
            "enableRateLimit": True,
            "options": {"defaultType": "future"},
        })
        self._sleep_s = sleep_ms / 1000.0

    @property
    def name(self) -> str:
        return "binance_usdm"

    @property
    def is_24_7(self) -> bool:
        return True

    def fetch_ohlcv(
        self,
        symbol: str,
        start: datetime,
        end: datetime,
        timeframe: str,
    ) -> pd.DataFrame:
        if timeframe not in TIMEFRAME_MAP:
            raise ValueError(
                f"Unsupported timeframe '{timeframe}'. Valid values: {sorted(TIMEFRAME_MAP)}"
            )

        start_utc = _to_utc(start)
        end_utc = _to_utc(end)
        since_ms = int(start_utc.timestamp() * 1000)
        end_ms = int(end_utc.timestamp() * 1000)

        ccxt_tf = TIMEFRAME_MAP[timeframe]
        tf_ms = self._timeframe_to_ms(timeframe)
        market_symbol = self._normalize_symbol(symbol)
        all_rows: list[list] = []

        pbar = tqdm(desc=f"[binance_usdm] {market_symbol}/{timeframe}", unit="bars", leave=False)
        current_since = since_ms

        while True:
            raw = self._exchange.fetch_ohlcv(
                market_symbol, ccxt_tf, since=current_since, limit=_BINANCE_LIMIT
            )
            if not raw:
                break

            raw = [row for row in raw if row[0] <= end_ms]
            all_rows.extend(raw)
            pbar.update(len(raw))

            last_ts = raw[-1][0] if raw else current_since
            if last_ts >= end_ms or len(raw) < _BINANCE_LIMIT:
                break

            current_since = last_ts + tf_ms
            time.sleep(self._sleep_s)

        pbar.close()

        if not all_rows:
            return _empty_df()

        return _rows_to_df(all_rows)

    @staticmethod
    def _normalize_symbol(symbol: str) -> str:
        s = symbol.strip()
        if "/" in s and ":" in s:
            return s
        if s.endswith(".P"):
            s = s[:-2]
        if s.endswith(".PERP"):
            s = s[:-5]
        s = s.replace("/", "").replace(":", "")
        if s.endswith("USDT"):
            base = s[:-4]
            return f"{base}/USDT:USDT"
        raise ValueError(f"Unsupported Binance USD-M symbol format: {symbol}")

    @staticmethod
    def _timeframe_to_ms(tf: str) -> int:
        mapping = {
            "5m": 5 * 60 * 1000,
            "15m": 15 * 60 * 1000,
            "1h": 60 * 60 * 1000,
            "2h": 2 * 60 * 60 * 1000,
            "4h": 4 * 60 * 60 * 1000,
            "1d": 24 * 60 * 60 * 1000,
        }
        return mapping[tf]


def _to_utc(dt: datetime) -> datetime:
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def _rows_to_df(rows: list[list]) -> pd.DataFrame:
    df = pd.DataFrame(rows, columns=["timestamp", "open", "high", "low", "close", "volume"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms", utc=True)
    df = df.set_index("timestamp")
    df = df[["open", "high", "low", "close", "volume"]].astype("float64")
    df = df[~df.index.duplicated(keep="last")]
    df = df.sort_index()
    return df


def _empty_df() -> pd.DataFrame:
    idx = pd.DatetimeIndex([], tz="UTC", name="timestamp")
    return pd.DataFrame(columns=["open", "high", "low", "close", "volume"], index=idx, dtype="float64")
