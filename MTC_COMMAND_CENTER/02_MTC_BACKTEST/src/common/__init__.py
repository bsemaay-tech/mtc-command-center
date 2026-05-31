"""Common utilities package for MTC Backtest System."""

from .precision import (
    PRICE_PRECISION, QTY_PRECISION, EPSILON,
    round_price, round_qty,
    float_eq, float_lt, float_lte, float_gt, float_gte,
    get_tick_size
)
from .timeframes import (
    parse_timeframe, timeframe_to_seconds, timeframe_to_ms,
    compute_close_time, validate_timeframe, VALID_TIMEFRAMES
)

__all__ = [
    # Precision
    "PRICE_PRECISION", "QTY_PRECISION", "EPSILON",
    "round_price", "round_qty",
    "float_eq", "float_lt", "float_lte", "float_gt", "float_gte",
    "get_tick_size",
    # Timeframes
    "parse_timeframe", "timeframe_to_seconds", "timeframe_to_ms",
    "compute_close_time", "validate_timeframe", "VALID_TIMEFRAMES",
]
