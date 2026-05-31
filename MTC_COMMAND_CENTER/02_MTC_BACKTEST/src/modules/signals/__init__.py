"""Signal modules for MTC Backtest System."""

from .base import SignalPlugin
from .range_filter import RangeFilterHybridSignal
from .supertrend import SupertrendSignal

__all__ = ["SignalPlugin", "SupertrendSignal", "RangeFilterHybridSignal"]
