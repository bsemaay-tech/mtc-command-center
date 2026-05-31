"""MTC data providers — pluggable OHLCV source interface."""
from .base import OHLCVProvider
from .binance_provider import BinanceProvider
from .binance_usdm_provider import BinanceUsdmProvider
from .csv_provider import CsvProvider

__all__ = ["OHLCVProvider", "BinanceProvider", "BinanceUsdmProvider", "CsvProvider", "get_provider"]


def get_provider(name: str, **kwargs) -> OHLCVProvider:
    """
    Factory function.

    Parameters
    ----------
    name : str
        ``'binance'``, ``'binance_usdm'`` or ``'csv'``.
    **kwargs
        Forwarded to the provider constructor.

    Examples
    --------
    >>> p = get_provider("binance", sleep_ms=50)
    >>> p = get_provider("binance_usdm", sleep_ms=50)
    >>> p = get_provider("csv", filepath="data/gold.csv", is_market_24_7=False)
    """
    if name == "binance":
        return BinanceProvider(**kwargs)
    if name == "binance_usdm":
        return BinanceUsdmProvider(**kwargs)
    if name == "csv":
        return CsvProvider(**kwargs)
    raise ValueError(
        f"Unknown provider '{name}'. Valid values: 'binance', 'binance_usdm', 'csv'."
    )
