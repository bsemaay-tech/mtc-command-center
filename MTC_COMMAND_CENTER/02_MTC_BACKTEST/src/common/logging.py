"""
Unified Logging Configuration for MTC Backtest System.

Provides consistent logging setup across all modules.
"""

import sys
import logging
import json
import uuid
import contextvars
from pathlib import Path
from typing import Optional
from datetime import datetime, timezone

# ═══════════════════════════════════════════════════════════════════════════════
# CONSTANTS
# ═══════════════════════════════════════════════════════════════════════════════

DEFAULT_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
DETAILED_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'

LOG_LEVELS = {
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
    'WARNING': logging.WARNING,
    'ERROR': logging.ERROR,
    'CRITICAL': logging.CRITICAL,
}

_CORRELATION_ID: contextvars.ContextVar[str] = contextvars.ContextVar("correlation_id", default="-")


def set_correlation_id(correlation_id: str) -> None:
    _CORRELATION_ID.set(correlation_id)


def get_correlation_id() -> str:
    return _CORRELATION_ID.get()


def new_correlation_id(prefix: str = "run") -> str:
    value = f"{prefix}-{uuid.uuid4().hex[:8]}"
    _CORRELATION_ID.set(value)
    return value


class CorrelationIdFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.correlation_id = get_correlation_id()
        return True


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "correlation_id": getattr(record, "correlation_id", get_correlation_id()),
        }
        if record.exc_info:
            payload["exc_info"] = self.formatException(record.exc_info)
        return json.dumps(payload, ensure_ascii=True)


# ═══════════════════════════════════════════════════════════════════════════════
# SETUP FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def setup_logging(
    level: str = 'INFO',
    log_file: Optional[str] = None,
    log_dir: str = 'logs',
    format_string: Optional[str] = None,
    detailed: bool = False,
    structured: bool = False,
    correlation_id: Optional[str] = None,
) -> logging.Logger:
    """
    Configure unified logging for the application.
    
    Args:
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional log file name (auto-generated if None)
        log_dir: Directory for log files
        format_string: Custom format string
        detailed: Use detailed format with file/line info
        
    Returns:
        Root logger instance
    """
    # Create log directory
    log_path = Path(log_dir)
    log_path.mkdir(exist_ok=True)
    
    if correlation_id:
        set_correlation_id(correlation_id)
    else:
        new_correlation_id()

    # Determine format
    if not structured:
        if format_string is None:
            format_string = DETAILED_FORMAT if detailed else DEFAULT_FORMAT
    
    # Get log level
    log_level = LOG_LEVELS.get(level.upper(), logging.INFO)
    
    # Generate log file name if not provided
    if log_file is None:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        log_file = f'mtc_{timestamp}.log'
    
    log_file_path = log_path / log_file
    
    # Configure root logger
    handlers = [
        logging.FileHandler(log_file_path),
        logging.StreamHandler(sys.stdout),
    ]
    
    logging.basicConfig(
        level=log_level,
        format=format_string if not structured else "%(message)s",
        handlers=handlers,
        force=True,  # Override any existing configuration
    )

    # Get root logger
    logger = logging.getLogger()
    corr_filter = CorrelationIdFilter()
    logger.addFilter(corr_filter)
    for h in logger.handlers:
        h.addFilter(corr_filter)
        if structured:
            h.setFormatter(JsonFormatter())
    logger.info(f"Logging initialized. Level: {level}, File: {log_file_path}")
    
    return logger


def get_logger(name: str) -> logging.Logger:
    """
    Get a named logger.
    
    Args:
        name: Logger name (typically __name__)
        
    Returns:
        Logger instance
    """
    return logging.getLogger(name)


def set_level(level: str, logger_name: Optional[str] = None) -> None:
    """
    Set log level for a logger.
    
    Args:
        level: Log level string
        logger_name: Logger name (None for root)
    """
    log_level = LOG_LEVELS.get(level.upper(), logging.INFO)
    
    if logger_name:
        logger = logging.getLogger(logger_name)
    else:
        logger = logging.getLogger()
    
    logger.setLevel(log_level)


def disable_debug_loggers() -> None:
    """Disable verbose debug loggers from libraries."""
    noisy_loggers = [
        'urllib3',
        'ccxt',
        'asyncio',
        'chardet',
        'filelock',
    ]
    
    for name in noisy_loggers:
        logging.getLogger(name).setLevel(logging.WARNING)
