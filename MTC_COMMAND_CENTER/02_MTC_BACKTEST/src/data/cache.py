"""
Dataset Cache Manager.

Manages caching of downloaded OHLCV data to avoid redundant downloads.
"""

import os
import hashlib
import json
import logging
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional, Dict

import pandas as pd

from .download import download_ohlcv
from .io import save_dataset, load_dataset

logger = logging.getLogger(__name__)


class CacheManager:
    """
    Manages caching of OHLCV datasets.
    
    Cache key is generated from: symbol + timeframe + start_date + end_date
    """
    
    def __init__(self, cache_dir: str = "./data"):
        """
        Initialize cache manager.
        
        Args:
            cache_dir: Directory for cached datasets
        """
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.index_path = self.cache_dir / ".cache_index.json"
        self._load_index()
    
    def _load_index(self):
        """Load or create cache index."""
        if self.index_path.exists():
            try:
                with open(self.index_path, 'r') as f:
                    self.index = json.load(f)
            except Exception as e:
                logger.warning(f"Failed to load cache index: {e}")
                self.index = {}
        else:
            self.index = {}
    
    def _save_index(self):
        """Save cache index to disk."""
        try:
            with open(self.index_path, 'w') as f:
                json.dump(self.index, f, indent=2, default=str)
        except Exception as e:
            logger.error(f"Failed to save cache index: {e}")
    
    def _generate_key(
        self,
        symbol: str,
        timeframe: str,
        start_date: datetime,
        end_date: datetime
    ) -> str:
        """Generate unique cache key for dataset."""
        key_str = f"{symbol}_{timeframe}_{start_date.isoformat()}_{end_date.isoformat()}"
        return hashlib.md5(key_str.encode()).hexdigest()[:12]
    
    def _generate_filename(
        self,
        symbol: str,
        timeframe: str,
        start_date: datetime,
        end_date: datetime
    ) -> str:
        """Generate human-readable filename for dataset."""
        start_str = start_date.strftime('%Y%m%d')
        end_str = end_date.strftime('%Y%m%d')
        return f"{symbol}_{timeframe}_{start_str}_{end_str}.parquet"
    
    def get_cached(
        self,
        symbol: str,
        timeframe: str,
        start_date: datetime,
        end_date: datetime
    ) -> Optional[pd.DataFrame]:
        """
        Get dataset from cache if available.
        
        Args:
            symbol: Trading symbol
            timeframe: Candle timeframe
            start_date: Start date (UTC)
            end_date: End date (UTC)
            
        Returns:
            DataFrame if cached, None otherwise
        """
        key = self._generate_key(symbol, timeframe, start_date, end_date)
        
        if key not in self.index:
            return None
        
        entry = self.index[key]
        file_path = Path(entry['path'])
        
        if not file_path.exists():
            logger.warning(f"Cache entry exists but file missing: {file_path}")
            del self.index[key]
            self._save_index()
            return None
        
        try:
            df = load_dataset(file_path)
            logger.info(f"Cache hit: {file_path.name}")
            return df
        except Exception as e:
            logger.error(f"Failed to load cached dataset: {e}")
            return None
    
    def cache_dataset(
        self,
        df: pd.DataFrame,
        symbol: str,
        timeframe: str,
        start_date: datetime,
        end_date: datetime
    ) -> str:
        """
        Save dataset to cache.
        
        Args:
            df: DataFrame to cache
            symbol: Trading symbol
            timeframe: Candle timeframe
            start_date: Start date (UTC)
            end_date: End date (UTC)
            
        Returns:
            Path to cached file
        """
        key = self._generate_key(symbol, timeframe, start_date, end_date)
        filename = self._generate_filename(symbol, timeframe, start_date, end_date)
        file_path = self.cache_dir / filename
        
        # Save dataset
        actual_path = save_dataset(df, file_path, format="parquet")
        
        # Update index
        self.index[key] = {
            'path': actual_path,
            'symbol': symbol,
            'timeframe': timeframe,
            'start_date': start_date.isoformat(),
            'end_date': end_date.isoformat(),
            'bar_count': len(df),
            'cached_at': datetime.now(timezone.utc).isoformat(),
        }
        self._save_index()
        
        logger.info(f"Cached dataset: {filename}")
        return actual_path
    
    def has_cached(
        self,
        symbol: str,
        timeframe: str,
        start_date: datetime,
        end_date: datetime
    ) -> bool:
        """Check if dataset is in cache."""
        key = self._generate_key(symbol, timeframe, start_date, end_date)
        
        if key not in self.index:
            return False
        
        file_path = Path(self.index[key]['path'])
        return file_path.exists()
    
    def get_info(self) -> Dict:
        """
        Get cache statistics.
        
        Returns:
            Dict with cache stats: total_files, total_size, entries
        """
        total_size = 0
        valid_entries = []
        
        for key, entry in list(self.index.items()):
            path = Path(entry['path'])
            if path.exists():
                entry['size_bytes'] = path.stat().st_size
                total_size += entry['size_bytes']
                valid_entries.append(entry)
            else:
                del self.index[key]
        
        self._save_index()
        
        return {
            'total_files': len(valid_entries),
            'total_size_bytes': total_size,
            'total_size_mb': round(total_size / (1024 * 1024), 2),
            'entries': valid_entries,
        }
    
    def clear(self, older_than_days: Optional[int] = None):
        """
        Clear cache.
        
        Args:
            older_than_days: Only clear files older than this many days.
                           If None, clear all.
        """
        removed = 0
        cutoff = None
        
        if older_than_days is not None:
            from datetime import timedelta
            cutoff = datetime.now(timezone.utc) - timedelta(days=older_than_days)
        
        for key, entry in list(self.index.items()):
            should_remove = False
            
            if cutoff is not None:
                cached_at = datetime.fromisoformat(entry['cached_at'])
                if cached_at.tzinfo is None:
                    cached_at = cached_at.replace(tzinfo=timezone.utc)
                should_remove = cached_at < cutoff
            else:
                should_remove = True
            
            if should_remove:
                path = Path(entry['path'])
                if path.exists():
                    path.unlink()
                del self.index[key]
                removed += 1
        
        self._save_index()
        logger.info(f"Cleared {removed} cached datasets")
        return removed


# Global cache manager instance
_cache_manager: Optional[CacheManager] = None


def get_cache_manager(cache_dir: str = "./data") -> CacheManager:
    """Get or create global cache manager."""
    global _cache_manager
    if _cache_manager is None or str(_cache_manager.cache_dir) != cache_dir:
        _cache_manager = CacheManager(cache_dir)
    return _cache_manager


def get_or_download(
    symbol: str,
    timeframe: str,
    start_date: datetime | str,
    end_date: datetime | str,
    force: bool = False,
    cache_dir: str = "./data",
    **kwargs
) -> pd.DataFrame:
    """
    Get dataset from cache or download if not available.
    
    Args:
        symbol: Trading symbol
        timeframe: Candle timeframe
        start_date: Start date (UTC)
        end_date: End date (UTC)
        force: Force redownload even if cached
        cache_dir: Cache directory
        **kwargs: Additional arguments for download_ohlcv
        
    Returns:
        DataFrame with OHLCV data
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
    
    cache = get_cache_manager(cache_dir)
    
    # Check cache first (unless force)
    if not force:
        df = cache.get_cached(symbol, timeframe, start_date, end_date)
        if df is not None:
            return df
    
    # Download
    logger.info(f"Downloading {symbol} {timeframe}...")
    df = download_ohlcv(symbol, timeframe, start_date, end_date, **kwargs)
    
    # Cache result
    cache.cache_dataset(df, symbol, timeframe, start_date, end_date)
    
    return df
