"""
Optuna Optimization Runner.

Runs parameter optimization using Optuna TPE sampler.
"""

import logging
from typing import Dict, Any, List, Optional, Callable
from datetime import datetime
import copy

import optuna
from optuna.samplers import TPESampler, RandomSampler
import pandas as pd

from ..config.defaults import MTCConfig
from ..config.schema import OptimizeConfig, ParamRange
from ..engine.mtc_runner import MTCRunner

logger = logging.getLogger(__name__)


class OptimizationRunner:
    """
    Optuna-based parameter optimization for MTC strategy.
    
    Uses TPE (Tree-structured Parzen Estimator) for efficient
    Bayesian optimization.
    """
    
    def __init__(
        self,
        df: pd.DataFrame,
        base_config: MTCConfig,
        param_space: Dict[str, ParamRange],
        objective: str = "profit_dd_ratio",
        min_trades: int = 30,
        warmup_bars: int = 200,
        eval_start: Optional[datetime] = None,
        eval_end: Optional[datetime] = None,
    ):
        """
        Initialize optimization runner.

        Args:
            df: OHLCV DataFrame
            base_config: Base MTC configuration
            param_space: Parameter space definitions
            objective: Objective to optimize
            min_trades: Minimum trades required
            warmup_bars: Indicator warmup period
            eval_start: UTC start of evaluation window (excludes preroll from metrics)
            eval_end: UTC end of evaluation window
        """
        self.df = df
        self.base_config = base_config
        self.param_space = param_space
        self.objective = objective
        self.min_trades = min_trades
        self.warmup_bars = warmup_bars
        self.eval_start = eval_start
        self.eval_end = eval_end
        
        self.study: Optional[optuna.Study] = None
        self.best_params: Dict[str, Any] = {}
        self.best_value: float = 0.0
        self.all_trials: List[Dict] = []
    
    def _create_objective(self) -> Callable:
        """Create Optuna objective function."""
        
        def objective_fn(trial: optuna.Trial) -> float:
            # Sample parameters
            params = self._sample_params(trial)
            
            # Create config with sampled params
            config = self._apply_params(params)
            
            # FORCE DISABLE DEBUG EXPORT for trials to save IO
            # We only export the best trial at the end of the run
            config.parity.export_debug_csv = False
            
            # Run backtest
            try:
                runner = MTCRunner(config)
                results = runner.run(
                    self.df,
                    warmup_bars=self.warmup_bars,
                    eval_start=self.eval_start,
                    eval_end=self.eval_end,
                )
                
                metrics = results['metrics']
                total_trades = metrics.get('total_trades', 0)
                
                # Prune if insufficient trades
                if total_trades < self.min_trades:
                    raise optuna.TrialPruned(f"Only {total_trades} trades")
                
                # Get objective value
                if self.objective == "profit_dd_ratio":
                    value = metrics.get('profit_dd_ratio', 0.0)
                    if value == float('inf'):
                        value = metrics.get('net_profit_pct', 0.0)
                elif self.objective == "net_profit":
                    value = metrics.get('net_profit', 0.0)
                elif self.objective == "net_profit_pct":
                    value = metrics.get('net_profit_pct', 0.0)
                elif self.objective == "sharpe":
                    value = metrics.get('sharpe_ratio', 0.0) or 0.0
                elif self.objective == "profit_factor":
                    value = metrics.get('profit_factor', 0.0)
                    if value == float('inf'):
                        value = 10.0  # Cap
                else:
                    value = metrics.get(self.objective, 0.0)
                
                # Store additional metrics as user attributes
                trial.set_user_attr('total_trades', total_trades)
                trial.set_user_attr('win_rate', metrics.get('win_rate', 0.0))
                trial.set_user_attr('net_profit_pct', metrics.get('net_profit_pct', 0.0))
                trial.set_user_attr('max_drawdown_pct', metrics.get('max_drawdown_pct', 0.0))
                
                return value if not pd.isna(value) else 0.0
                
            except Exception as e:
                logger.warning(f"Trial failed: {e}")
                raise optuna.TrialPruned(str(e))
        
        return objective_fn
    
    def _sample_params(self, trial: optuna.Trial) -> Dict[str, Any]:
        """Sample parameters for a trial."""
        params = {}
        
        for name, space in self.param_space.items():
            if space.param_type == "int":
                step = int(space.step) if space.step else 1
                params[name] = trial.suggest_int(
                    name, int(space.low), int(space.high), step=step
                )
            elif space.param_type == "float":
                if space.step:
                    # Discrete float
                    params[name] = trial.suggest_float(
                        name, space.low, space.high, step=space.step
                    )
                else:
                    params[name] = trial.suggest_float(
                        name, space.low, space.high
                    )
            elif space.param_type == "bool":
                params[name] = trial.suggest_categorical(name, [True, False])
            elif space.param_type == "categorical":
                params[name] = trial.suggest_categorical(name, space.choices)
        
        return params
    
    def _apply_params(self, params: Dict[str, Any]) -> MTCConfig:
        """Apply sampled parameters to base config."""
        # Deep copy base config
        # Preserve alias-backed fields such as stop_loss.use_sl when rebuilding
        # configs from an existing model instance.
        config_dict = self.base_config.model_dump(by_alias=True)
        
        # Apply each parameter
        for name, value in params.items():
            # Handle nested params (e.g., "supertrend.atr_len")
            parts = name.split('.')
            target = config_dict
            
            for part in parts[:-1]:
                target = target[part]
            
            target[parts[-1]] = value
        
        return MTCConfig.model_validate(config_dict)
    
    def run(
        self,
        n_trials: int = 100,
        n_jobs: int = 1,
        timeout_seconds: Optional[int] = None,
        sampler: str = "tpe",
        progress_callback: Optional[Callable[[int, int], None]] = None,
    ) -> Dict[str, Any]:
        """
        Run optimization.
        
        Args:
            n_trials: Number of trials
            n_jobs: Parallel jobs (not fully supported yet)
            timeout_seconds: Optional timeout
            sampler: Sampler type ("tpe" or "random")
            progress_callback: Optional callback(completed, total)
            
        Returns:
            Dict with optimization results
        """
        import time
        start_time = time.time()
        
        # Create sampler
        if sampler == "random":
            optuna_sampler = RandomSampler(seed=42)
        else:
            optuna_sampler = TPESampler(seed=42)
        
        # Create study
        self.study = optuna.create_study(
            direction="maximize",
            sampler=optuna_sampler,
        )
        
        # Optimize
        logger.info(f"Starting optimization: {n_trials} trials, objective={self.objective}")
        logger.info(f"Base Strategy Config: Cap=${self.base_config.strategy.initial_capital:,.2f}, Comm={self.base_config.strategy.commission_percent}%, Slip={self.base_config.strategy.slippage_ticks}, Pyr={self.base_config.strategy.pyramiding}")
        logger.info(f"Base Risk Config: Long={self.base_config.risk.risk_long_percent}%, Short={self.base_config.risk.risk_short_percent}%, Lev={self.base_config.risk.max_leverage_cap}x, EquityMode={self.base_config.risk.risk_equity_mode}")
        
        
        def callback(study, trial):
            if progress_callback:
                progress_callback(len(study.trials), n_trials)
        
        self.study.optimize(
            self._create_objective(),
            n_trials=n_trials,
            timeout=timeout_seconds,
            n_jobs=n_jobs,
            callbacks=[callback],
            show_progress_bar=True,
        )
        
        # Get results
        self.best_params = self.study.best_params
        self.best_value = self.study.best_value
        
        # Compile all trials
        self.all_trials = []
        for trial in self.study.trials:
            self.all_trials.append({
                'number': trial.number,
                'params': trial.params,
                'value': trial.value if trial.value is not None else 0.0,
                'state': str(trial.state.name),
                'duration_seconds': (
                    (trial.datetime_complete - trial.datetime_start).total_seconds()
                    if trial.datetime_complete and trial.datetime_start else 0.0
                ),
                'total_trades': trial.user_attrs.get('total_trades', 0),
                'win_rate': trial.user_attrs.get('win_rate', 0.0),
                'net_profit_pct': trial.user_attrs.get('net_profit_pct', 0.0),
                'max_drawdown_pct': trial.user_attrs.get('max_drawdown_pct', 0.0),
            })
        
        # --- Run Best Trial with Debug Export (if enabled) ---
        if self.base_config.parity.export_debug_csv and self.best_params:
            logger.info("Running BEST TRIAL with debug export enabled...")
            try:
                best_config = self._apply_params(self.best_params)
                best_config.parity.export_debug_csv = True
                best_config.parity.debug_dir = self.base_config.parity.debug_dir
                
                # Ensure directory exists
                from pathlib import Path
                Path(best_config.parity.debug_dir).mkdir(parents=True, exist_ok=True)
                
                best_runner = MTCRunner(best_config)
                best_results = best_runner.run(
                    self.df,
                    warmup_bars=self.warmup_bars,
                    eval_start=self.eval_start,
                    eval_end=self.eval_end,
                )
                
                # Save Optimizer Summary
                import json
                summary = {
                    "objective": self.objective,
                    "best_value": self.best_value,
                    "best_params": self.best_params,
                    "metrics": best_results['metrics'],
                    "timestamp": datetime.now().isoformat(),
                }
                summary_path = Path(best_config.parity.debug_dir) / "optimizer_summary.json"
                with open(summary_path, "w") as f:
                    json.dump(summary, f, indent=4)
                    
                logger.info(f"Saved optimizer summary to {summary_path}")
                
            except Exception as e:
                logger.error(f"Failed to run best trial debug export: {e}")

        runtime = time.time() - start_time
        
        # Results
        completed = len([t for t in self.all_trials if t['state'] == 'COMPLETE'])
        pruned = len([t for t in self.all_trials if t['state'] == 'PRUNED'])
        
        logger.info(
            f"Optimization complete: {completed} completed, {pruned} pruned, "
            f"best={self.best_value:.4f} in {runtime:.1f}s"
        )
        
        return {
            'best_params': self.best_params,
            'best_value': self.best_value,
            'all_trials': self.all_trials,
            'completed_trials': completed,
            'pruned_trials': pruned,
            'total_trials': n_trials,
            'runtime_seconds': runtime,
        }
    
    def get_top_n(self, n: int = 10) -> List[Dict]:
        """Get top N trial results."""
        sorted_trials = sorted(
            [t for t in self.all_trials if t['state'] == 'COMPLETE'],
            key=lambda x: x['value'],
            reverse=True
        )
        return sorted_trials[:n]
    
    def generate_pine_preset(self, params: Optional[Dict] = None) -> str:
        """Generate Pine Script preset for params."""
        if params is None:
            params = self.best_params
        
        lines = [
            "// ═══════════════════════════════════════════════════════════",
            "// OPTIMIZED PARAMETERS - MTC Python Backtest",
            f"// Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"// Objective: {self.objective} = {self.best_value:.4f}",
            "// ═══════════════════════════════════════════════════════════",
            "",
        ]
        
        for name, value in params.items():
            # Format value
            if isinstance(value, bool):
                val_str = "true" if value else "false"
            elif isinstance(value, float):
                val_str = f"{value:.4f}".rstrip('0').rstrip('.')
            elif isinstance(value, str):
                val_str = f'"{value}"'
            else:
                val_str = str(value)
            
            # Convert to Pine variable name
            pine_name = name.replace('.', '_').replace('__', '_')
            lines.append(f"// {pine_name} = {val_str}")
        
        return "\n".join(lines)
    
    def trials_to_dataframe(self) -> pd.DataFrame:
        """Convert trials to DataFrame for analysis."""
        return pd.DataFrame(self.all_trials)


def run_optimization(
    df: pd.DataFrame,
    param_space: Dict[str, ParamRange],
    base_config: Optional[MTCConfig] = None,
    n_trials: int = 100,
    objective: str = "profit_dd_ratio",
    min_trades: int = 30,
) -> Dict[str, Any]:
    """
    Convenience function to run optimization.
    
    Args:
        df: OHLCV DataFrame
        param_space: Parameters to optimize
        base_config: Base configuration
        n_trials: Number of trials
        objective: Optimization objective
        min_trades: Minimum trades required
        
    Returns:
        Optimization results
    """
    if base_config is None:
        base_config = MTCConfig()
    
    runner = OptimizationRunner(
        df=df,
        base_config=base_config,
        param_space=param_space,
        objective=objective,
        min_trades=min_trades,
    )
    
    return runner.run(n_trials=n_trials)
