"""CSV / Parquet provider for external datasets (gold, forex, indices, oil, etc.)."""
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from .base import OHLCVProvider

_REQUIRED_COLS = {"open", "high", "low", "close", "volume"}


class CsvProvider(OHLCVProvider):
    """
    Reads a user-supplied CSV or Parquet file.

    Expected columns (case-insensitive): ``timestamp, open, high, low, close, volume``

    The ``timestamp`` column must be parseable as UTC datetimes.
    If the column is ambiguous (no tz info), it is assumed UTC.

    Parameters
    ----------
    filepath : str | Path
        Path to the source file (.csv, .csv.gz, or .parquet).
    is_market_24_7 : bool
        Pass ``False`` for session-based markets (forex, equities, commodities).
        Affects gap-severity thresholds in the validator.
        Default ``False``.
    """

    def __init__(self, filepath: str | Path, is_market_24_7: bool = False) -> None:
        self._filepath = Path(filepath)
        self._is_24_7 = is_market_24_7
        self._df: pd.DataFrame | None = None  # lazy load cache

    @property
    def name(self) -> str:
        return "csv"

    @property
    def is_24_7(self) -> bool:
        return self._is_24_7

    # ------------------------------------------------------------------
    def fetch_ohlcv(
        self,
        symbol: str,   # informational only — not used to filter the file
        start: datetime,
        end: datetime,
        timeframe: str,  # informational only — not used to resample
    ) -> pd.DataFrame:
        """Return all bars from the file that fall within [*start*, *end*] UTC."""
        if self._df is None:
            self._df = self._load()

        start_utc = _to_utc(start)
        end_utc = _to_utc(end)

        mask = (self._df.index >= start_utc) & (self._df.index <= end_utc)
        return self._df.loc[mask].copy()

    # ------------------------------------------------------------------
    def _load(self) -> pd.DataFrame:
        ext = "".join(self._filepath.suffixes).lower()

        if ext in (".parquet",):
            raw = pd.read_parquet(self._filepath)
        elif ext in (".csv", ".gz", ".csv.gz"):
            raw = pd.read_csv(self._filepath)
        else:
            # Try reading as CSV anyway
            raw = pd.read_csv(self._filepath)

        # Normalize column names to lowercase
        raw.columns = [c.lower().strip() for c in raw.columns]

        # Check required columns
        missing = _REQUIRED_COLS - set(raw.columns)
        if missing and "timestamp" not in raw.columns:
            # Maybe timestamp is already the index
            if raw.index.name and raw.index.name.lower() == "timestamp":
                pass
            else:
                raise ValueError(
                    f"CsvProvider: file '{self._filepath}' is missing required columns: "
                    f"{missing | {'timestamp'}}. "
                    f"Required: timestamp, open, high, low, close, volume."
                )

        if missing:
            raise ValueError(
                f"CsvProvider: file '{self._filepath}' is missing OHLCV columns: {missing}."
            )

        # Set timestamp as index if it's a column
        if "timestamp" in raw.columns:
            raw["timestamp"] = pd.to_datetime(raw["timestamp"], utc=True, errors="coerce")
            raw = raw.set_index("timestamp")
        else:
            # Index is already timestamp — ensure UTC
            raw.index = pd.to_datetime(raw.index, utc=True, errors="coerce")
            raw.index.name = "timestamp"

        # Ensure UTC tz
        if raw.index.tz is None:
            raw.index = raw.index.tz_localize("UTC")
        elif str(raw.index.tz) != "UTC":
            raw.index = raw.index.tz_convert("UTC")

        df = raw[["open", "high", "low", "close", "volume"]].astype("float64")
        df = df[~df.index.duplicated(keep="last")]
        df = df.sort_index()
        return df


# ---------------------------------------------------------------------------
def _to_utc(dt: datetime) -> datetime:
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)
