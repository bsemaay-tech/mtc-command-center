"""
Schema definitions for datasets, backtests, and optimization.

Provides Pydantic validation schemas for all configuration types.
"""

from datetime import datetime
from typing import Optional, List, Dict, Any, Union, Literal
from pydantic import BaseModel, Field, field_validator, model_validator

from .defaults import MTCConfig


class ParamRange(BaseModel):
    """Parameter range for optimization."""
    
    param_type: Literal["int", "float", "bool", "categorical"] = Field(
        description="Type of parameter"
    )
    low: Optional[float] = Field(default=None, description="Minimum value (int/float)")
    high: Optional[float] = Field(default=None, description="Maximum value (int/float)")
    step: Optional[float] = Field(default=None, description="Step size (int/float)")
    choices: Optional[List[Any]] = Field(default=None, description="Choices (categorical)")
    
    @model_validator(mode="after")
    def validate_range(self):
        """Validate that appropriate fields are set for each type."""
        if self.param_type in ("int", "float"):
            if self.low is None or self.high is None:
                raise ValueError(f"low and high required for {self.param_type} type")
            if self.low > self.high:
                raise ValueError("low must be <= high")
        elif self.param_type == "categorical":
            if not self.choices or len(self.choices) < 2:
                raise ValueError("categorical requires at least 2 choices")
        return self


class DatasetConfig(BaseModel):
    """Dataset configuration for data loading/downloading."""
    
    symbol: str = Field(default="BTCUSDT", description="Trading symbol")
    timeframe: str = Field(default="15m", description="Candle timeframe")
    start_date: datetime = Field(description="Start date (UTC)")
    end_date: datetime = Field(description="End date (UTC)")
    source: Literal["binance", "csv"] = Field(default="binance")
    csv_path: Optional[str] = Field(default=None, description="Path for CSV source")
    
    @field_validator("timeframe")
    @classmethod
    def validate_timeframe(cls, v: str) -> str:
        valid = ["1m", "3m", "5m", "15m", "30m", "1h", "2h", "4h", "6h", "8h", "12h", "1d", "3d", "1w"]
        if v not in valid:
            raise ValueError(f"timeframe must be one of {valid}")
        return v
    
    @model_validator(mode="after")
    def validate_dates(self):
        """Ensure end_date is after start_date."""
        if self.end_date <= self.start_date:
            raise ValueError("end_date must be after start_date")
        return self
    
    @model_validator(mode="after")
    def validate_csv_path(self):
        """Ensure csv_path is set when source is csv."""
        if self.source == "csv" and not self.csv_path:
            raise ValueError("csv_path required when source is 'csv'")
        return self


class BacktestConfig(BaseModel):
    """Backtest configuration combining dataset and strategy settings."""
    
    dataset: DatasetConfig = Field(description="Dataset configuration")
    strategy: MTCConfig = Field(default_factory=MTCConfig, description="Strategy parameters")
    seed: int = Field(default=42, description="Random seed for reproducibility")
    
    # Backtest-specific settings
    warmup_bars: int = Field(default=200, ge=0, description="Bars to skip for indicator warmup")


class OptimizeConfig(BaseModel):
    """Optimization configuration."""
    
    backtest: BacktestConfig = Field(description="Base backtest configuration")
    param_space: Dict[str, ParamRange] = Field(
        default_factory=dict,
        description="Parameters to optimize with their ranges"
    )
    
    # Optimization settings
    objective: Literal["profit_dd_ratio", "net_profit", "sharpe", "profit_factor"] = Field(
        default="profit_dd_ratio",
        description="Optimization objective"
    )
    direction: Literal["maximize", "minimize"] = Field(
        default="maximize",
        description="Optimization direction"
    )
    
    # Constraints
    min_trades: int = Field(default=30, ge=1, description="Minimum trades required")
    max_drawdown_pct: Optional[float] = Field(
        default=None, ge=0, le=100,
        description="Maximum allowed drawdown %"
    )
    
    # Optuna settings
    n_trials: int = Field(default=100, ge=1, description="Number of optimization trials")
    n_jobs: int = Field(default=1, ge=1, description="Parallel jobs")
    timeout_seconds: Optional[int] = Field(default=None, description="Timeout in seconds")
    sampler: Literal["tpe", "random", "grid"] = Field(default="tpe")
    
    @field_validator("param_space")
    @classmethod
    def validate_param_space(cls, v: Dict[str, ParamRange]) -> Dict[str, ParamRange]:
        if not v:
            raise ValueError("param_space cannot be empty for optimization")
        return v


class TradeRecord(BaseModel):
    """Single trade record from backtest."""
    
    trade_id: int
    direction: Literal["long", "short"]
    entry_bar: int
    entry_time: datetime
    entry_price: float
    exit_bar: int
    exit_time: datetime
    exit_price: float
    quantity: float
    pnl: float
    pnl_pct: float
    exit_reason: Literal[
        "SL", "TP", "TP1", "TP2", "TRAIL", 
        "OPP_SIGNAL", "FILTER_BLOCK", "TIME_STOP", "BE", "MANUAL", "EVAL_START_FLATTEN"
    ]
    
    # Optional detailed info
    sl_price: Optional[float] = None
    tp_price: Optional[float] = None
    max_favorable_excursion: Optional[float] = None
    max_adverse_excursion: Optional[float] = None
    bars_held: Optional[int] = None
    exit_id: Optional[str] = None
    lifecycle_id: Optional[str] = None
    event_seq_in_bar: Optional[int] = None
    execution_profile_id: Optional[str] = None
    working_exit_book_version: Optional[int] = None


class BacktestMetrics(BaseModel):
    """Backtest performance metrics."""
    
    # Core metrics
    net_profit: float
    net_profit_pct: float
    gross_profit: float
    gross_loss: float
    
    # Drawdown
    max_drawdown: float
    max_drawdown_pct: float
    avg_drawdown: float
    
    # Ratios
    profit_dd_ratio: float
    profit_factor: float
    sharpe_ratio: Optional[float] = None
    sortino_ratio: Optional[float] = None
    
    # Trade statistics
    total_trades: int
    winning_trades: int
    losing_trades: int
    win_rate: float
    
    # Averages
    avg_win: float
    avg_loss: float
    avg_trade: float
    largest_win: float
    largest_loss: float
    
    # Time-based
    avg_bars_in_trade: float
    avg_bars_in_winning_trade: float
    avg_bars_in_losing_trade: float
    
    # Risk metrics
    expectancy: float
    risk_reward_ratio: float


class BacktestResult(BaseModel):
    """Complete backtest result."""
    
    config: BacktestConfig
    metrics: BacktestMetrics
    trades: List[TradeRecord]
    equity_curve: List[float]
    drawdown_curve: List[float]
    timestamps: List[datetime]
    
    # Metadata
    runtime_seconds: float
    bar_count: int
    warmup_bars: int
    
    class Config:
        arbitrary_types_allowed = True


class OptimizationTrial(BaseModel):
    """Single optimization trial result."""
    
    trial_number: int
    params: Dict[str, Any]
    value: float
    metrics: Dict[str, float]
    state: Literal["complete", "pruned", "failed"]
    duration_seconds: float


class OptimizationResult(BaseModel):
    """Complete optimization result."""
    
    config: OptimizeConfig
    best_params: Dict[str, Any]
    best_value: float
    best_metrics: BacktestMetrics
    all_trials: List[OptimizationTrial]
    
    # Metadata
    total_trials: int
    completed_trials: int
    pruned_trials: int
    runtime_seconds: float
    
    def generate_pine_preset(self) -> str:
        """Generate Pine Script preset block for optimized parameters."""
        lines = [
            "// ═══════════════════════════════════════════",
            "// OPTIMIZED PARAMETERS (MTC Python Backtest)",
            f"// Generated: {datetime.now().isoformat()}",
            f"// Objective: {self.config.objective} = {self.best_value:.4f}",
            "// ═══════════════════════════════════════════",
            "",
        ]
        
        for param, value in self.best_params.items():
            # Format value based on type
            if isinstance(value, bool):
                val_str = "true" if value else "false"
            elif isinstance(value, float):
                val_str = f"{value:.4f}".rstrip('0').rstrip('.')
            elif isinstance(value, str):
                val_str = f'"{value}"'
            else:
                val_str = str(value)
            
            # Convert Python param path to Pine input name
            pine_name = param.replace(".", "_").replace("__", "_")
            lines.append(f"// {pine_name} = {val_str}")
        
        return "\n".join(lines)
