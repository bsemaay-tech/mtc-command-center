"""
Signal Plugin Base Class.

Defines the interface for all signal generation modules.
Mirrors MTC Section 4 signal plugin architecture.
"""

from abc import ABC, abstractmethod
from typing import Tuple, Dict, Any, Optional
import pandas as pd


class SignalPlugin(ABC):
    """
    Base class for signal generation plugins.
    
    All signal plugins must implement the generate() method that produces
    raw long and short signals (`longSignal_raw`, `shortSignal_raw`).
    
    These raw signals are then processed by the MTC engine with:
    - Filters (MA, Volume, HTF, etc.)
    - Guards (DD, Consecutive Loss, etc.)
    - Entry mode (Edge vs Signal)
    - Regime lock
    
    The plugin should NOT apply filters or make entry decisions.
    """
    
    def __init__(self, name: str = "BaseSignal", **params):
        """
        Initialize signal plugin.
        
        Args:
            name: Plugin identifier
            **params: Plugin-specific parameters
        """
        self.name = name
        self.params = params
    
    @abstractmethod
    def generate(
        self,
        df: pd.DataFrame
    ) -> Tuple[pd.Series, pd.Series]:
        """
        Generate raw signals.
        
        Args:
            df: DataFrame with columns: timestamp, open, high, low, close, volume
            
        Returns:
            Tuple of (longSignal_raw, shortSignal_raw) as boolean Series
        """
        pass
    
    @abstractmethod
    def get_debug_series(self, df: pd.DataFrame) -> Dict[str, pd.Series]:
        """
        Get internal series for parity debugging.
        
        Returns dict of named Series for comparison with TradingView:
        - indicator lines
        - intermediate calculations
        - direction signals
        
        Args:
            df: OHLCV DataFrame
            
        Returns:
            Dict mapping series name to Series data
        """
        pass
    
    def get_params(self) -> Dict[str, Any]:
        """Get current parameter values."""
        return self.params.copy()
    
    def set_params(self, **params):
        """Update parameters."""
        self.params.update(params)
    
    @classmethod
    def get_param_space(cls) -> Dict[str, Dict]:
        """
        Get parameter space for optimization.
        
        Returns dict mapping param name to range definition:
        {
            'param_name': {
                'type': 'int' | 'float' | 'bool' | 'categorical',
                'low': min_value,  # for int/float
                'high': max_value,  # for int/float
                'step': step_size,  # optional for int/float
                'choices': [...]    # for categorical
            }
        }
        """
        return {}
    
    def validate_params(self) -> Tuple[bool, Optional[str]]:
        """
        Validate current parameters.
        
        Returns:
            (is_valid, error_message)
        """
        return True, None


class NullSignal(SignalPlugin):
    """
    Null signal plugin that generates no signals.
    
    Used when signal_mode is "None".
    """
    
    def __init__(self):
        super().__init__(name="None")
    
    def generate(self, df: pd.DataFrame) -> Tuple[pd.Series, pd.Series]:
        """Return all-False signals."""
        false_series = pd.Series(False, index=df.index)
        return false_series, false_series
    
    def get_debug_series(self, df: pd.DataFrame) -> Dict[str, pd.Series]:
        return {}
