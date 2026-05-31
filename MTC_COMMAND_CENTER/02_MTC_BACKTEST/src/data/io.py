"""
Dataset I/O Module.

Handles reading and writing OHLCV datasets in CSV and Parquet formats.
"""

import os
import logging
from pathlib import Path
from datetime import datetime
from typing import Optional, Tuple, List, Dict

import pandas as pd

logger = logging.getLogger(__name__)

# Standard schema for OHLCV data
OHLCV_COLUMNS = ['timestamp', 'open', 'high', 'low', 'close', 'volume']


def save_dataset(
    df: pd.DataFrame,
    path: str | Path,
    format: str = "parquet"
) -> str:
    """
    Save dataset to file.
    
    Args:
        df: DataFrame with OHLCV data
        path: Output file path (extension will be adjusted if needed)
        format: Output format - "parquet" or "csv"
        
    Returns:
        Actual path where file was saved
    """
    path = Path(path)
    
    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)
    
    # Adjust extension if needed
    if format == "parquet":
        if path.suffix != ".parquet":
            path = path.with_suffix(".parquet")
        df.to_parquet(path, index=False, engine='pyarrow')
    elif format == "csv":
        if path.suffix != ".csv":
            path = path.with_suffix(".csv")
        # Convert timestamp to ISO format for CSV
        df_copy = df.copy()
        if 'timestamp' in df_copy.columns:
            df_copy['timestamp'] = df_copy['timestamp'].dt.strftime('%Y-%m-%dT%H:%M:%SZ')
        df_copy.to_csv(path, index=False)
    else:
        raise ValueError(f"Unsupported format: {format}. Use 'parquet' or 'csv'")
    
    logger.info(f"Saved {len(df)} rows to {path}")
    return str(path)


def load_dataset(path: str | Path) -> pd.DataFrame:
    """
    Load dataset from file.
    
    Auto-detects format based on extension.
    
    Args:
        path: Path to dataset file
        
    Returns:
        DataFrame with OHLCV data
        
    Raises:
        FileNotFoundError: If file doesn't exist
        ValueError: If format is unsupported
    """
    path = Path(path)
    
    if not path.exists():
        raise FileNotFoundError(f"Dataset not found: {path}")
    
    suffix = path.suffix.lower()
    
    if suffix == ".parquet":
        df = pd.read_parquet(path, engine='pyarrow')
    elif suffix == ".csv":
        df = pd.read_csv(path)
    else:
        raise ValueError(f"Unsupported file format: {suffix}")
    
    # Parse timestamp if needed
    if 'timestamp' in df.columns:
        if df['timestamp'].dtype == 'object':
            df['timestamp'] = pd.to_datetime(df['timestamp'], utc=True)
        elif not hasattr(df['timestamp'].dtype, 'tz'):
            df['timestamp'] = pd.to_datetime(df['timestamp'], utc=True)
    
    # Ensure numeric columns
    for col in ['open', 'high', 'low', 'close', 'volume']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    logger.info(f"Loaded {len(df)} rows from {path}")
    return df


def validate_dataset(df: pd.DataFrame) -> Tuple[bool, List[str]]:
    """
    Validate dataset schema and data quality.
    
    Args:
        df: DataFrame to validate
        
    Returns:
        Tuple of (is_valid, error_messages)
    """
    errors = []
    warnings = []
    
    # Check required columns
    missing_cols = set(OHLCV_COLUMNS) - set(df.columns)
    if missing_cols:
        errors.append(f"Missing required columns: {missing_cols}")
    
    if errors:
        return False, errors
    
    # Check for empty dataset
    if len(df) == 0:
        errors.append("Dataset is empty")
        return False, errors
    
    # Check for NaN values
    for col in OHLCV_COLUMNS:
        nan_count = df[col].isna().sum()
        if nan_count > 0:
            if col == 'volume':
                warnings.append(f"Column '{col}' has {nan_count} NaN values (may be acceptable)")
            else:
                errors.append(f"Column '{col}' has {nan_count} NaN values")
    
    # Check timestamp ordering
    if not df['timestamp'].is_monotonic_increasing:
        # Check for duplicates
        dup_count = df['timestamp'].duplicated().sum()
        if dup_count > 0:
            errors.append(f"Found {dup_count} duplicate timestamps")
        else:
            errors.append("Timestamps are not in ascending order")
    
    # Check for gaps (warning only)
    if len(df) > 1:
        time_diffs = df['timestamp'].diff().dropna()
        most_common_diff = time_diffs.mode().iloc[0]
        gap_count = (time_diffs > most_common_diff * 1.5).sum()
        if gap_count > 0:
            warnings.append(f"Found {gap_count} potential gaps in data")
    
    # Check OHLC consistency
    invalid_ohlc = (
        (df['high'] < df['low']) |
        (df['high'] < df['open']) |
        (df['high'] < df['close']) |
        (df['low'] > df['open']) |
        (df['low'] > df['close'])
    ).sum()
    
    if invalid_ohlc > 0:
        errors.append(f"Found {invalid_ohlc} bars with invalid OHLC relationships")
    
    # Combine errors and warnings
    all_messages = errors + [f"[WARNING] {w}" for w in warnings]
    
    return len(errors) == 0, all_messages


def list_datasets(data_dir: str = "./data") -> List[Dict]:
    """
    List available datasets in data directory.
    
    Args:
        data_dir: Directory to scan for datasets
        
    Returns:
        List of dicts with dataset metadata:
        - filename: str
        - path: str
        - format: str
        - size_bytes: int
        - bar_count: int (if readable)
        - start_date: datetime (if readable)
        - end_date: datetime (if readable)
        - symbol: str (inferred from filename)
        - timeframe: str (inferred from filename)
    """
    data_path = Path(data_dir)
    
    if not data_path.exists():
        return []
    
    datasets = []
    
    for file_path in data_path.iterdir():
        if file_path.suffix.lower() not in ['.csv', '.parquet']:
            continue
        
        info = {
            'filename': file_path.name,
            'path': str(file_path),
            'format': file_path.suffix[1:].lower(),
            'size_bytes': file_path.stat().st_size,
        }
        
        # Try to extract symbol/timeframe from filename
        # Expected format: SYMBOL_TIMEFRAME_*.csv/parquet
        name_parts = file_path.stem.split('_')
        if len(name_parts) >= 2:
            info['symbol'] = name_parts[0]
            info['timeframe'] = name_parts[1]
        
        # Try to load and get metadata
        try:
            df = load_dataset(file_path)
            info['bar_count'] = len(df)
            if 'timestamp' in df.columns and len(df) > 0:
                info['start_date'] = df['timestamp'].min()
                info['end_date'] = df['timestamp'].max()
        except Exception as e:
            logger.warning(f"Could not read metadata from {file_path}: {e}")
            info['bar_count'] = None
            info['error'] = str(e)
        
        datasets.append(info)
    
    # Sort by filename
    datasets.sort(key=lambda x: x['filename'])
    
    return datasets


def get_dataset_info(path: str | Path) -> Dict:
    """
    Get detailed information about a dataset.
    
    Args:
        path: Path to dataset file
        
    Returns:
        Dict with dataset metadata
    """
    path = Path(path)
    
    if not path.exists():
        raise FileNotFoundError(f"Dataset not found: {path}")
    
    df = load_dataset(path)
    is_valid, messages = validate_dataset(df)
    
    info = {
        'path': str(path),
        'filename': path.name,
        'format': path.suffix[1:].lower(),
        'size_bytes': path.stat().st_size,
        'bar_count': len(df),
        'is_valid': is_valid,
        'validation_messages': messages,
    }
    
    if 'timestamp' in df.columns and len(df) > 0:
        info['start_date'] = df['timestamp'].min()
        info['end_date'] = df['timestamp'].max()
        
        # Calculate timeframe
        if len(df) > 1:
            time_diff = (df['timestamp'].iloc[1] - df['timestamp'].iloc[0]).total_seconds()
            info['timeframe_seconds'] = time_diff
            
            # Convert to human-readable
            if time_diff == 60:
                info['timeframe'] = '1m'
            elif time_diff == 180:
                info['timeframe'] = '3m'
            elif time_diff == 300:
                info['timeframe'] = '5m'
            elif time_diff == 900:
                info['timeframe'] = '15m'
            elif time_diff == 1800:
                info['timeframe'] = '30m'
            elif time_diff == 3600:
                info['timeframe'] = '1h'
            elif time_diff == 14400:
                info['timeframe'] = '4h'
            elif time_diff == 86400:
                info['timeframe'] = '1d'
            else:
                info['timeframe'] = f'{int(time_diff)}s'
    
    return info
