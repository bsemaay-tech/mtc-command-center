"""Filter modules for MTC Backtest System."""

from .base import FilterPlugin
from .htf_trend_filter import HTFTrendFilter
from .ma_filter import MAFilter
from .macd_hub_filter import MacdHubFilter
from .mcginley_filter import McGinleyFilter
from .range_regime_filter import RangeRegimeFilter
from .volume_filter import VolumeFilter

__all__ = [
    "FilterPlugin",
    "MAFilter",
    "VolumeFilter",
    "HTFTrendFilter",
    "McGinleyFilter",
    "MacdHubFilter",
    "RangeRegimeFilter",
]
