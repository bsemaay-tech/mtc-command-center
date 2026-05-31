"""Binance OHLCV provider using ccxt (no API key required for public data)."""
from __future__ import annotations

import time
from datetime import datetime, timezone

import pandas as pd
from tqdm import tqdm

from .base import OHLCVProvider

# Map our canonical timeframe strings → ccxt / Binance timeframe strings
TIMEFRAME_MAP: dict[str, str] = {
    "5m": "5m",
    "15m": "15m",
    "1h": "1h",
    "2h": "2h",
    "4h": "4h",
    "1d": "1d",
}

# Binance returns max 1 000 bars per request
_BINANCE_LIMIT = 1000


class BinanceProvider(OHLCVProvider):
    """
    Fetches OHLCV data from Binance via ccxt.

    No API key is required for public market data.

    Parameters
    ----------
    sleep_ms : int
        Milliseconds to sleep between consecutive paginated requests to
        avoid Binance 429 rate-limit errors. Default 100 ms.
    """

    def __init__(self, sleep_ms: int = 100) -> None:
        import ccxt  # lazy import so tests can mock easily

        # Use Binance SPOT market — it has data from 2017 onwards.
        # fapi (binanceusdm, perpetual futures) only goes back to Sep 2019.
        self._exchange = ccxt.binance({
            "enableRateLimit": True,
            "options": {"defaultType": "spot"},
        })
        self._sleep_s = sleep_ms / 1000.0

    # ------------------------------------------------------------------
    @property
    def name(self) -> str:
        return "binance"

    @property
    def is_24_7(self) -> bool:
        return True

    # ------------------------------------------------------------------
    def fetch_ohlcv(
        self,
        symbol: str,
        start: datetime,
        end: datetime,
        timeframe: str,
    ) -> pd.DataFrame:
        """Fetch and return all bars between *start* and *end* (UTC, inclusive)."""
        if timeframe not in TIMEFRAME_MAP:
            raise ValueError(
                f"Unsupported timeframe '{timeframe}'. "
                f"Valid values: {sorted(TIMEFRAME_MAP)}"
            )

        # Convert start → UTC ms timestamp expected by ccxt
        start_utc = _to_utc(start)
        end_utc = _to_utc(end)
        since_ms = int(start_utc.timestamp() * 1000)
        end_ms = int(end_utc.timestamp() * 1000)

        ccxt_tf = TIMEFRAME_MAP[timeframe]
        tf_ms = self._timeframe_to_ms(timeframe)

        all_rows: list[list] = []

        pbar = tqdm(desc=f"[binance] {symbol}/{timeframe}", unit="bars", leave=False)
        current_since = since_ms

        while True:
            raw = self._exchange.fetch_ohlcv(
                symbol, ccxt_tf, since=current_since, limit=_BINANCE_LIMIT
            )
            if not raw:
                break

            # Filter out bars that exceed our end boundary
            raw = [row for row in raw if row[0] <= end_ms]
            all_rows.extend(raw)
            pbar.update(len(raw))

            # Check if we've reached or passed the end
            last_ts = raw[-1][0] if raw else current_since
            if last_ts >= end_ms or len(raw) < _BINANCE_LIMIT:
                break

            # Advance cursor past the last returned bar
            current_since = last_ts + tf_ms
            time.sleep(self._sleep_s)

        pbar.close()

        if not all_rows:
            return _empty_df()

        df = _rows_to_df(all_rows)
        return df

    # ------------------------------------------------------------------
    @staticmethod
    def _timeframe_to_ms(tf: str) -> int:
        """Return the duration of one bar in milliseconds."""
        mapping = {
            "5m": 5 * 60 * 1000,
            "15m": 15 * 60 * 1000,
            "1h": 60 * 60 * 1000,
            "2h": 2 * 60 * 60 * 1000,
            "4h": 4 * 60 * 60 * 1000,
            "1d": 24 * 60 * 60 * 1000,
        }
        return mapping[tf]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _to_utc(dt: datetime) -> datetime:
    """Ensure *dt* is UTC-aware."""
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def _rows_to_df(rows: list[list]) -> pd.DataFrame:
    """Convert ccxt raw rows → clean DataFrame."""
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
