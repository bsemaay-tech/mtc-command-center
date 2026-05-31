"""
Timeframe Utilities for MTC Backtest System.

Provides parsing and conversion functions for timeframe strings.
All datetime operations use UTC.
"""

from datetime import datetime, timedelta, timezone
from typing import Optional
import re

# ═══════════════════════════════════════════════════════════════════════════════
# CONSTANTS
# ═══════════════════════════════════════════════════════════════════════════════

VALID_TIMEFRAMES = [
    "1m", "3m", "5m", "15m", "30m",
    "1h", "2h", "4h", "6h", "12h",
    "1d", "3d", "1w", "1M"
]

# Timeframe to seconds mapping
TIMEFRAME_SECONDS = {
    "1m": 60,
    "3m": 180,
    "5m": 300,
    "15m": 900,
    "30m": 1800,
    "1h": 3600,
    "2h": 7200,
    "4h": 14400,
    "6h": 21600,
    "12h": 43200,
    "1d": 86400,
    "3d": 259200,
    "1w": 604800,
    "1M": 2592000,  # Approximation: 30 days
}

# Regex pattern for timeframe parsing
TIMEFRAME_PATTERN = re.compile(r'^(\d+)([mhdwM])$')


# ═══════════════════════════════════════════════════════════════════════════════
# PARSING FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def validate_timeframe(tf: str) -> bool:
    """
    Check if a timeframe string is valid.
    
    Args:
        tf: Timeframe string (e.g., "15m", "1h", "4h", "1d")
        
    Returns:
        True if valid timeframe
        
    Example:
        >>> validate_timeframe("15m")
        True
        >>> validate_timeframe("invalid")
        False
    """
    if tf in VALID_TIMEFRAMES:
        return True
    
    # Try pattern match for custom timeframes
    match = TIMEFRAME_PATTERN.match(tf)
    return match is not None


def parse_timeframe(tf: str) -> timedelta:
    """
    Parse a timeframe string to timedelta.
    
    Args:
        tf: Timeframe string (e.g., "15m", "1h", "4h", "1d")
        
    Returns:
        timedelta representing the timeframe duration
        
    Raises:
        ValueError: If timeframe format is invalid
        
    Example:
        >>> parse_timeframe("15m")
        datetime.timedelta(seconds=900)
        >>> parse_timeframe("4h")
        datetime.timedelta(seconds=14400)
    """
    # Check predefined
    if tf in TIMEFRAME_SECONDS:
        return timedelta(seconds=TIMEFRAME_SECONDS[tf])
    
    # Parse with regex
    match = TIMEFRAME_PATTERN.match(tf)
    if not match:
        raise ValueError(f"Invalid timeframe format: {tf}")
    
    value = int(match.group(1))
    unit = match.group(2)
    
    unit_map = {
        'm': 'minutes',
        'h': 'hours',
        'd': 'days',
        'w': 'weeks',
        'M': 'days',  # Months as 30 days
    }
    
    if unit == 'M':
        value *= 30  # Convert months to days
    
    return timedelta(**{unit_map[unit]: value})


def timeframe_to_seconds(tf: str) -> int:
    """
    Convert timeframe string to seconds.
    
    Args:
        tf: Timeframe string
        
    Returns:
        Duration in seconds
        
    Example:
        >>> timeframe_to_seconds("15m")
        900
        >>> timeframe_to_seconds("1h")
        3600
    """
    if tf in TIMEFRAME_SECONDS:
        return TIMEFRAME_SECONDS[tf]
    
    return int(parse_timeframe(tf).total_seconds())


def timeframe_to_ms(tf: str) -> int:
    """
    Convert timeframe string to milliseconds.
    
    Args:
        tf: Timeframe string
        
    Returns:
        Duration in milliseconds
        
    Example:
        >>> timeframe_to_ms("15m")
        900000
    """
    return timeframe_to_seconds(tf) * 1000


# ═══════════════════════════════════════════════════════════════════════════════
# TIMESTAMP FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def compute_close_time(open_time: datetime, tf: str) -> datetime:
    """
    Compute bar close time from open time and timeframe.
    
    Close time = Open time + Timeframe duration
    
    Args:
        open_time: Bar open time (should be UTC)
        tf: Timeframe string
        
    Returns:
        Bar close time (UTC)
        
    Example:
        >>> from datetime import datetime, timezone
        >>> open_time = datetime(2024, 1, 1, 0, 0, tzinfo=timezone.utc)
        >>> compute_close_time(open_time, "15m")
        datetime.datetime(2024, 1, 1, 0, 15, tzinfo=datetime.timezone.utc)
    """
    duration = parse_timeframe(tf)
    close_time = open_time + duration
    
    # Ensure UTC timezone
    if close_time.tzinfo is None:
        close_time = close_time.replace(tzinfo=timezone.utc)
    
    return close_time


def ensure_utc(dt: datetime) -> datetime:
    """
    Ensure datetime has UTC timezone.
    
    Args:
        dt: Datetime object (may be naive or have timezone)
        
    Returns:
        Datetime with UTC timezone
    """
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def timestamp_to_datetime(ts: int, unit: str = "ms") -> datetime:
    """
    Convert Unix timestamp to datetime (UTC).
    
    Args:
        ts: Unix timestamp
        unit: "s" for seconds, "ms" for milliseconds
        
    Returns:
        datetime object (UTC)
    """
    if unit == "ms":
        ts = ts / 1000
    
    return datetime.fromtimestamp(ts, tz=timezone.utc)


def datetime_to_timestamp(dt: datetime, unit: str = "ms") -> int:
    """
    Convert datetime to Unix timestamp.
    
    Args:
        dt: Datetime object
        unit: "s" for seconds, "ms" for milliseconds
        
    Returns:
        Unix timestamp
    """
    dt = ensure_utc(dt)
    ts = dt.timestamp()
    
    if unit == "ms":
        return int(ts * 1000)
    return int(ts)


# ═══════════════════════════════════════════════════════════════════════════════
# BAR ALIGNMENT FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def align_to_timeframe(dt: datetime, tf: str) -> datetime:
    """
    Align datetime to the start of the current bar.
    
    Args:
        dt: Datetime to align
        tf: Timeframe string
        
    Returns:
        Datetime aligned to bar start
        
    Example:
        >>> dt = datetime(2024, 1, 1, 0, 7, 30, tzinfo=timezone.utc)
        >>> align_to_timeframe(dt, "15m")
        datetime.datetime(2024, 1, 1, 0, 0, tzinfo=datetime.timezone.utc)
    """
    dt = ensure_utc(dt)
    seconds = timeframe_to_seconds(tf)
    
    # Align to midnight for daily/weekly
    if seconds >= 86400:
        return dt.replace(hour=0, minute=0, second=0, microsecond=0)
    
    # Align to interval start
    total_seconds = dt.hour * 3600 + dt.minute * 60 + dt.second
    aligned_seconds = (total_seconds // seconds) * seconds
    
    hours = aligned_seconds // 3600
    minutes = (aligned_seconds % 3600) // 60
    secs = aligned_seconds % 60
    
    return dt.replace(hour=hours, minute=minutes, second=secs, microsecond=0)


def get_bar_index(
    dt: datetime,
    start_dt: datetime,
    tf: str
) -> int:
    """
    Calculate bar index from start datetime.
    
    Args:
        dt: Current datetime
        start_dt: Dataset start datetime
        tf: Timeframe string
        
    Returns:
        Bar index (0-based)
    """
    dt = ensure_utc(dt)
    start_dt = ensure_utc(start_dt)
    
    seconds = timeframe_to_seconds(tf)
    diff = (dt - start_dt).total_seconds()
    
    return int(diff // seconds)


def bars_between(
    start_dt: datetime,
    end_dt: datetime,
    tf: str
) -> int:
    """
    Calculate number of bars between two datetimes.
    
    Args:
        start_dt: Start datetime
        end_dt: End datetime
        tf: Timeframe string
        
    Returns:
        Number of bars
    """
    start_dt = ensure_utc(start_dt)
    end_dt = ensure_utc(end_dt)
    
    if end_dt <= start_dt:
        return 0
    
    seconds = timeframe_to_seconds(tf)
    diff = (end_dt - start_dt).total_seconds()
    
    return int(diff // seconds)


# ═══════════════════════════════════════════════════════════════════════════════
# DISPLAY FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def format_timeframe(tf: str) -> str:
    """
    Format timeframe for display.
    
    Args:
        tf: Timeframe string
        
    Returns:
        Human-readable format
        
    Example:
        >>> format_timeframe("15m")
        "15 Minutes"
        >>> format_timeframe("1d")
        "1 Day"
    """
    match = TIMEFRAME_PATTERN.match(tf)
    if not match:
        return tf
    
    value = int(match.group(1))
    unit = match.group(2)
    
    unit_names = {
        'm': ('Minute', 'Minutes'),
        'h': ('Hour', 'Hours'),
        'd': ('Day', 'Days'),
        'w': ('Week', 'Weeks'),
        'M': ('Month', 'Months'),
    }
    
    singular, plural = unit_names.get(unit, (unit, unit))
    name = singular if value == 1 else plural
    
    return f"{value} {name}"
