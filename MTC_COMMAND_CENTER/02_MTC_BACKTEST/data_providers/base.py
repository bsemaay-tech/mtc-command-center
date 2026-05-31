"""Abstract base class for all OHLCV data providers."""
from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime

import pandas as pd


class OHLCVProvider(ABC):
    """
    Interface contract for all market-data providers.

    Implementations must return a DataFrame whose index is a UTC-aware
    ``pd.DatetimeIndex`` (bar open time) and whose columns are exactly
    ``[open, high, low, close, volume]`` (all float64).
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Provider identifier, e.g. ``'binance'``, ``'csv'``."""
        ...

    @property
    @abstractmethod
    def is_24_7(self) -> bool:
        """
        ``True`` for 24/7 markets (crypto).
        ``False`` for session-based markets (equities, forex, commodities).
        Affects gap-severity thresholds in the validator.
        """
        ...

    @abstractmethod
    def fetch_ohlcv(
        self,
        symbol: str,
        start: datetime,
        end: datetime,
        timeframe: str,
    ) -> pd.DataFrame:
        """
        Fetch OHLCV bars for *symbol* in [*start*, *end*] (UTC, inclusive).

        Parameters
        ----------
        symbol : str
            Ticker as expected by the upstream source, e.g. ``'BTCUSDT'``.
        start : datetime
            Inclusive lower bound (UTC).
        end : datetime
            Inclusive upper bound (UTC).
        timeframe : str
            One of ``'5m'``, ``'15m'``, ``'1h'``, ``'2h'``, ``'4h'``, ``'1d'``.

        Returns
        -------
        pd.DataFrame
            index  : ``pd.DatetimeIndex`` with ``tz=UTC`` (bar open time)
            columns: ``[open, high, low, close, volume]`` — all ``float64``
        """
        ...

    # ------------------------------------------------------------------
    # Helpers shared across implementations
    # ------------------------------------------------------------------

    @staticmethod
    def _required_columns() -> list[str]:
        return ["open", "high", "low", "close", "volume"]

    @staticmethod
    def _assert_utc(df: pd.DataFrame) -> None:
        import pytz

        if df.index.tz is None:
            raise ValueError("DataFrame index has no timezone — must be UTC.")
        utc = pytz.UTC
        if df.index.tz != utc:
            raise ValueError(f"DataFrame index timezone is {df.index.tz!r}, expected UTC.")
