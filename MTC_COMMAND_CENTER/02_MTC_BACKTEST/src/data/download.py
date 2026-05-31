"""
OHLCV Data Download Module.

Downloads historical OHLCV data from Binance USDT-M Futures via ccxt.
Implements robust error handling with exponential backoff.
"""

import time
import logging
from datetime import datetime, timezone
from typing import Optional, Callable

import ccxt
import pandas as pd
from tqdm import tqdm

# Configure logging
logger = logging.getLogger(__name__)


class DownloadError(Exception):
    """Error during data download."""
    pass


def get_exchange(
    exchange_id: str = "binance",
    sandbox: bool = False
) -> ccxt.Exchange:
    """
    Get configured ccxt exchange instance.
    
    Args:
        exchange_id: Exchange identifier (default: binance)
        sandbox: Use sandbox/testnet mode
        
    Returns:
        Configured ccxt Exchange instance
    """
    exchange_class = getattr(ccxt, exchange_id)
    exchange = exchange_class({
        'enableRateLimit': True,
        'options': {
            'defaultType': 'future',  # USDT-M Futures
            'adjustForTimeDifference': True,
        },
        'sandbox': sandbox,
    })
    
    return exchange


def _convert_symbol(symbol: str) -> str:
    """
    Convert symbol format for Binance Futures.
    
    Examples:
        BTCUSDT -> BTC/USDT:USDT
        ETHUSDT -> ETH/USDT:USDT
    """
    # Already in correct format
    if '/' in symbol:
        return symbol
    
    # Standard USDT pairs
    if symbol.endswith('USDT'):
        base = symbol[:-4]
        return f"{base}/USDT:USDT"
    
    # Standard BUSD pairs
    if symbol.endswith('BUSD'):
        base = symbol[:-4]
        return f"{base}/BUSD:BUSD"
    
    # Return as-is, may fail
    return symbol


def _parse_timeframe_to_ms(timeframe: str) -> int:
    """Convert timeframe string to milliseconds."""
    multipliers = {
        'm': 60 * 1000,
        'h': 60 * 60 * 1000,
        'd': 24 * 60 * 60 * 1000,
        'w': 7 * 24 * 60 * 60 * 1000,
    }
    
    unit = timeframe[-1]
    value = int(timeframe[:-1])
    
    if unit not in multipliers:
        raise ValueError(f"Unknown timeframe unit: {unit}")
    
    return value * multipliers[unit]


def download_ohlcv(
    symbol: str,
    timeframe: str,
    start_date: datetime | str,
    end_date: datetime | str,
    exchange_id: str = "binance",
    max_retries: int = 5,
    batch_size: int = 1000,
    progress_callback: Optional[Callable[[int, int], None]] = None,
    show_progress: bool = True,
) -> pd.DataFrame:
    """
    Download OHLCV data from exchange.
    
    Args:
        symbol: Trading symbol (e.g., "BTCUSDT" or "BTC/USDT:USDT")
        timeframe: Candle timeframe (e.g., "15m", "1h", "4h", "1d")
        start_date: Start date (UTC) as datetime or ISO string
        end_date: End date (UTC) as datetime or ISO string
        exchange_id: Exchange to use (default: binance)
        max_retries: Maximum retry attempts on error
        batch_size: Number of candles per request (max 1000 for Binance)
        progress_callback: Optional callback(current, total) for progress
        show_progress: Show tqdm progress bar
        
    Returns:
        DataFrame with columns: timestamp, open, high, low, close, volume
        
    Raises:
        DownloadError: If download fails after retries
    """
    # Parse dates
    if isinstance(start_date, str):
        start_date = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
    if isinstance(end_date, str):
        end_date = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
    
    # Ensure UTC
    if start_date.tzinfo is None:
        start_date = start_date.replace(tzinfo=timezone.utc)
    if end_date.tzinfo is None:
        end_date = end_date.replace(tzinfo=timezone.utc)
    
    # Convert to milliseconds
    start_ms = int(start_date.timestamp() * 1000)
    end_ms = int(end_date.timestamp() * 1000)
    
    # Get exchange
    exchange = get_exchange(exchange_id)
    
    # Convert symbol format
    ccxt_symbol = _convert_symbol(symbol)
    
    # Calculate expected bars for progress
    tf_ms = _parse_timeframe_to_ms(timeframe)
    expected_bars = (end_ms - start_ms) // tf_ms
    
    logger.info(f"Downloading {symbol} {timeframe} from {start_date} to {end_date}")
    logger.info(f"Expected bars: ~{expected_bars}")
    
    all_candles = []
    current_ms = start_ms
    retry_count = 0
    base_delay = 2.0
    
    # Progress bar
    pbar = None
    if show_progress:
        pbar = tqdm(total=expected_bars, desc=f"Downloading {symbol}", unit="bars")
    
    try:
        while current_ms < end_ms:
            try:
                # Fetch batch
                candles = exchange.fetch_ohlcv(
                    ccxt_symbol,
                    timeframe,
                    since=current_ms,
                    limit=batch_size
                )
                
                if not candles:
                    logger.warning(f"No candles returned for {current_ms}")
                    break
                
                # Filter candles within range
                filtered = [c for c in candles if c[0] < end_ms]
                all_candles.extend(filtered)
                
                # Update progress
                if pbar:
                    pbar.update(len(filtered))
                if progress_callback:
                    progress_callback(len(all_candles), expected_bars)
                
                # Move to next batch
                last_ts = candles[-1][0]
                if last_ts <= current_ms:
                    logger.warning(f"No progress made, breaking loop")
                    break
                current_ms = last_ts + 1
                
                # Reset retry count on success
                retry_count = 0
                
            except (ccxt.RequestTimeout, ccxt.DDoSProtection, 
                    ccxt.ExchangeNotAvailable, ccxt.NetworkError) as e:
                retry_count += 1
                if retry_count > max_retries:
                    raise DownloadError(f"Max retries exceeded: {e}")
                
                delay = base_delay * (2 ** retry_count)
                logger.warning(f"Retry {retry_count}/{max_retries} after {delay}s: {e}")
                time.sleep(delay)
                
            except ccxt.ExchangeError as e:
                raise DownloadError(f"Exchange error: {e}")
    
    finally:
        if pbar:
            pbar.close()
    
    if not all_candles:
        raise DownloadError(f"No data downloaded for {symbol} {timeframe}")
    
    # Create DataFrame
    df = pd.DataFrame(
        all_candles,
        columns=['timestamp', 'open', 'high', 'low', 'close', 'volume']
    )
    
    # Convert timestamp to datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms', utc=True)
    
    # Remove duplicates and sort
    df = df.drop_duplicates(subset=['timestamp']).sort_values('timestamp').reset_index(drop=True)
    
    # Ensure numeric types
    for col in ['open', 'high', 'low', 'close', 'volume']:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    logger.info(f"Downloaded {len(df)} bars from {df['timestamp'].min()} to {df['timestamp'].max()}")
    
    return df


def download_multiple_symbols(
    symbols: list[str],
    timeframe: str,
    start_date: datetime | str,
    end_date: datetime | str,
    **kwargs
) -> dict[str, pd.DataFrame]:
    """
    Download OHLCV data for multiple symbols.
    
    Args:
        symbols: List of trading symbols
        timeframe: Candle timeframe
        start_date: Start date (UTC)
        end_date: End date (UTC)
        **kwargs: Additional arguments for download_ohlcv
        
    Returns:
        Dict mapping symbol to DataFrame
    """
    results = {}
    
    for symbol in symbols:
        try:
            df = download_ohlcv(symbol, timeframe, start_date, end_date, **kwargs)
            results[symbol] = df
        except DownloadError as e:
            logger.error(f"Failed to download {symbol}: {e}")
            results[symbol] = None
    
    return results
