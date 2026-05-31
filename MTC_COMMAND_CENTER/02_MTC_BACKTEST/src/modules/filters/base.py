"""
Filter Plugin Base Class.

Defines the interface for all filter modules.
Filters output allowLong / allowShort boolean series.
"""

from abc import ABC, abstractmethod
from typing import Tuple, Dict, Any
import pandas as pd


class FilterPlugin(ABC):
    """
    Base class for filter plugins.
    
    Filters are applied after raw signals to produce:
    - allowLong: Can take long positions
    - allowShort: Can take short positions
    
    Multiple filters are combined with AND logic:
    finalAllow = filter1.allow AND filter2.allow AND ... AND filterN.allow
    
    Filters should be lightweight and not make complex calculations.
    Heavy indicators should be cached/precomputed.
    """
    
    def __init__(self, name: str = "BaseFilter", enabled: bool = True, **params):
        """
        Initialize filter plugin.
        
        Args:
            name: Filter identifier
            enabled: Whether filter is active
            **params: Filter-specific parameters
        """
        self.name = name
        self.enabled = enabled
        self.params = params
    
    @abstractmethod
    def apply(
        self,
        df: pd.DataFrame,
        **context
    ) -> Tuple[pd.Series, pd.Series]:
        """
        Apply filter to data.
        
        Args:
            df: OHLCV DataFrame
            **context: Additional context (e.g., current signals, indicators)
            
        Returns:
            Tuple of (allowLong, allowShort) as boolean Series
        """
        pass
    
    def is_enabled(self) -> bool:
        """Check if filter is active."""
        return self.enabled
    
    def get_debug_series(self, df: pd.DataFrame) -> Dict[str, pd.Series]:
        """Get internal series for debugging."""
        return {}
    
    def get_params(self) -> Dict[str, Any]:
        """Get current parameter values."""
        return {'enabled': self.enabled, **self.params}
    
    def set_params(self, **params):
        """Update parameters."""
        if 'enabled' in params:
            self.enabled = params.pop('enabled')
        self.params.update(params)


class PassThroughFilter(FilterPlugin):
    """
    Null filter that allows all signals.
    
    Used as a placeholder when filters are disabled.
    """
    
    def __init__(self):
        super().__init__(name="PassThrough", enabled=True)
    
    def apply(
        self,
        df: pd.DataFrame,
        **context
    ) -> Tuple[pd.Series, pd.Series]:
        """Allow all signals."""
        allow = pd.Series(True, index=df.index)
        return allow, allow


class CompositeFilter(FilterPlugin):
    """
    Combines multiple filters with AND logic.
    """
    
    def __init__(self, filters: list[FilterPlugin] = None):
        super().__init__(name="Composite", enabled=True)
        self.filters = filters or []
    
    def add_filter(self, filter_plugin: FilterPlugin):
        """Add a filter to the composite."""
        self.filters.append(filter_plugin)
    
    def apply(
        self,
        df: pd.DataFrame,
        **context
    ) -> Tuple[pd.Series, pd.Series]:
        """Apply all filters with AND logic."""
        allow_long, allow_short, _ = self.apply_with_details(df, **context)
        return allow_long, allow_short
    
    def apply_with_details(
        self,
        df: pd.DataFrame,
        **context
    ) -> Tuple[pd.Series, pd.Series, Dict[str, Tuple[pd.Series, pd.Series]]]:
        """
        Apply all filters and return per-filter decisions.
        
        Returns:
            (allow_long, allow_short, details)
            details: {filter_name: (allow_long_series, allow_short_series)}
        """
        allow_long = pd.Series(True, index=df.index)
        allow_short = pd.Series(True, index=df.index)
        details: Dict[str, Tuple[pd.Series, pd.Series]] = {}
        
        for f in self.filters:
            if not f.is_enabled():
                continue
            f_long, f_short = f.apply(df, **context)
            f_long = f_long.fillna(True)
            f_short = f_short.fillna(True)
            details[f.name] = (f_long, f_short)
            allow_long = allow_long & f_long
            allow_short = allow_short & f_short
        
        return allow_long, allow_short, details
    
    def get_debug_series(self, df: pd.DataFrame) -> Dict[str, pd.Series]:
        """Get debug series from all filters."""
        debug = {}
        for f in self.filters:
            for name, series in f.get_debug_series(df).items():
                debug[f"{f.name}_{name}"] = series
        return debug
