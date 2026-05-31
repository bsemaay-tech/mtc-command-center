"""
Performance Metrics Calculator.

Calculates comprehensive backtest performance metrics.
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import numpy as np
import pandas as pd

from .mtc_state import Trade


@dataclass
class BacktestMetrics:
    """Complete backtest performance metrics."""
    
    # Core metrics
    net_profit: float = 0.0
    net_profit_pct: float = 0.0
    gross_profit: float = 0.0
    gross_loss: float = 0.0
    
    # Drawdown
    max_drawdown: float = 0.0
    max_drawdown_pct: float = 0.0
    avg_drawdown: float = 0.0
    
    # Ratios
    profit_dd_ratio: float = 0.0
    profit_factor: float = 0.0
    sharpe_ratio: Optional[float] = None
    sortino_ratio: Optional[float] = None
    calmar_ratio: Optional[float] = None
    
    # Trade statistics
    total_trades: int = 0
    winning_trades: int = 0
    losing_trades: int = 0
    win_rate: float = 0.0
    
    # Long/Short breakdown
    long_trades: int = 0
    short_trades: int = 0
    long_win_rate: float = 0.0
    short_win_rate: float = 0.0
    
    # Averages
    avg_win: float = 0.0
    avg_loss: float = 0.0
    avg_trade: float = 0.0
    largest_win: float = 0.0
    largest_loss: float = 0.0
    
    # Consecutive
    max_consecutive_wins: int = 0
    max_consecutive_losses: int = 0
    
    # Time-based
    avg_bars_in_trade: float = 0.0
    avg_bars_in_winning_trade: float = 0.0
    avg_bars_in_losing_trade: float = 0.0
    
    # Risk metrics
    expectancy: float = 0.0
    risk_reward_ratio: float = 0.0
    avg_r_multiple: float = 0.0


def calculate_metrics(
    trades: List[Trade],
    equity_curve: List[float],
    initial_capital: float,
    risk_free_rate: float = 0.0,
) -> BacktestMetrics:
    """
    Calculate comprehensive backtest metrics.
    
    Args:
        trades: List of completed trades
        equity_curve: Equity values over time
        initial_capital: Starting capital
        risk_free_rate: Annual risk-free rate for Sharpe calculation
        
    Returns:
        BacktestMetrics object
    """
    metrics = BacktestMetrics()
    
    if not trades:
        return metrics
    
    # Separate winners and losers
    winners = [t for t in trades if t.pnl > 0]
    losers = [t for t in trades if t.pnl <= 0]
    
    # Core metrics
    metrics.gross_profit = sum(t.pnl for t in winners)
    metrics.gross_loss = abs(sum(t.pnl for t in losers))
    metrics.net_profit = metrics.gross_profit - metrics.gross_loss
    metrics.net_profit_pct = (metrics.net_profit / initial_capital) * 100
    
    # Trade counts
    metrics.total_trades = len(trades)
    metrics.winning_trades = len(winners)
    metrics.losing_trades = len(losers)
    metrics.win_rate = (len(winners) / len(trades)) * 100 if trades else 0.0
    
    # Long/Short breakdown
    long_trades = [t for t in trades if t.direction.value == "long"]
    short_trades = [t for t in trades if t.direction.value == "short"]
    long_winners = [t for t in long_trades if t.pnl > 0]
    short_winners = [t for t in short_trades if t.pnl > 0]
    
    metrics.long_trades = len(long_trades)
    metrics.short_trades = len(short_trades)
    metrics.long_win_rate = (len(long_winners) / len(long_trades) * 100) if long_trades else 0.0
    metrics.short_win_rate = (len(short_winners) / len(short_trades) * 100) if short_trades else 0.0
    
    # Averages
    metrics.avg_win = metrics.gross_profit / len(winners) if winners else 0.0
    metrics.avg_loss = metrics.gross_loss / len(losers) if losers else 0.0
    metrics.avg_trade = metrics.net_profit / len(trades)
    metrics.largest_win = max((t.pnl for t in winners), default=0.0)
    metrics.largest_loss = min((t.pnl for t in losers), default=0.0)
    
    # Profit factor
    metrics.profit_factor = (
        metrics.gross_profit / metrics.gross_loss 
        if metrics.gross_loss > 0 else float('inf')
    )
    
    # Risk/Reward
    metrics.risk_reward_ratio = (
        metrics.avg_win / metrics.avg_loss 
        if metrics.avg_loss > 0 else float('inf')
    )
    
    # Expectancy
    win_prob = metrics.win_rate / 100
    loss_prob = 1 - win_prob
    metrics.expectancy = (win_prob * metrics.avg_win) - (loss_prob * metrics.avg_loss)
    
    # R-multiple average
    r_values = [t.pnl_r for t in trades if t.pnl_r != 0]
    metrics.avg_r_multiple = np.mean(r_values) if r_values else 0.0
    
    # Consecutive wins/losses
    metrics.max_consecutive_wins = _max_consecutive(trades, is_winner=True)
    metrics.max_consecutive_losses = _max_consecutive(trades, is_winner=False)
    
    # Time-based
    all_bars = [t.bars_held for t in trades]
    win_bars = [t.bars_held for t in winners]
    loss_bars = [t.bars_held for t in losers]
    
    metrics.avg_bars_in_trade = np.mean(all_bars) if all_bars else 0.0
    metrics.avg_bars_in_winning_trade = np.mean(win_bars) if win_bars else 0.0
    metrics.avg_bars_in_losing_trade = np.mean(loss_bars) if loss_bars else 0.0
    
    # Drawdown metrics (from equity curve)
    if equity_curve:
        dd_info = _calculate_drawdown_metrics(equity_curve, initial_capital)
        metrics.max_drawdown = dd_info['max_dd_value']
        metrics.max_drawdown_pct = dd_info['max_dd_pct']
        metrics.avg_drawdown = dd_info['avg_dd_pct']
        
        # Profit/DD ratio
        metrics.profit_dd_ratio = (
            metrics.net_profit_pct / metrics.max_drawdown_pct 
            if metrics.max_drawdown_pct > 0 else float('inf')
        )
        
        # Calmar ratio (annualized return / max DD)
        # Assuming daily equity
        if len(equity_curve) > 252:
            annual_return = (equity_curve[-1] / equity_curve[0]) ** (252 / len(equity_curve)) - 1
            metrics.calmar_ratio = annual_return / (metrics.max_drawdown_pct / 100) if metrics.max_drawdown_pct > 0 else 0.0
    
    # Sharpe and Sortino ratios
    if len(equity_curve) > 1:
        returns = pd.Series(equity_curve).pct_change().dropna()
        
        if len(returns) > 0 and returns.std() > 0:
            # Annualized Sharpe (assuming daily data)
            excess_returns = returns - (risk_free_rate / 252)
            metrics.sharpe_ratio = (
                np.sqrt(252) * excess_returns.mean() / returns.std()
            )
            
            # Sortino (downside deviation)
            downside = returns[returns < 0]
            if len(downside) > 0:
                downside_std = downside.std()
                if downside_std > 0:
                    metrics.sortino_ratio = (
                        np.sqrt(252) * excess_returns.mean() / downside_std
                    )
    
    return metrics


def _max_consecutive(trades: List[Trade], is_winner: bool) -> int:
    """Calculate maximum consecutive wins or losses."""
    max_streak = 0
    current_streak = 0
    
    for trade in trades:
        trade_is_win = trade.pnl > 0
        
        if trade_is_win == is_winner:
            current_streak += 1
            max_streak = max(max_streak, current_streak)
        else:
            current_streak = 0
    
    return max_streak


def _calculate_drawdown_metrics(
    equity_curve: List[float],
    initial_capital: float
) -> Dict[str, float]:
    """Calculate drawdown metrics from equity curve."""
    equity = np.array(equity_curve)
    peak = np.maximum.accumulate(equity)
    drawdown = peak - equity
    drawdown_pct = (drawdown / peak) * 100
    
    return {
        'max_dd_value': np.max(drawdown),
        'max_dd_pct': np.max(drawdown_pct),
        'avg_dd_pct': np.mean(drawdown_pct[drawdown_pct > 0]) if np.any(drawdown_pct > 0) else 0.0,
    }


def metrics_to_dict(metrics: BacktestMetrics) -> Dict[str, Any]:
    """Convert BacktestMetrics to dictionary."""
    return {
        'net_profit': metrics.net_profit,
        'net_profit_pct': metrics.net_profit_pct,
        'gross_profit': metrics.gross_profit,
        'gross_loss': metrics.gross_loss,
        'profit_factor': metrics.profit_factor,
        'profit_dd_ratio': metrics.profit_dd_ratio,
        'max_drawdown': metrics.max_drawdown,
        'max_drawdown_pct': metrics.max_drawdown_pct,
        'total_trades': metrics.total_trades,
        'winning_trades': metrics.winning_trades,
        'losing_trades': metrics.losing_trades,
        'win_rate': metrics.win_rate,
        'avg_win': metrics.avg_win,
        'avg_loss': metrics.avg_loss,
        'avg_trade': metrics.avg_trade,
        'largest_win': metrics.largest_win,
        'largest_loss': metrics.largest_loss,
        'sharpe_ratio': metrics.sharpe_ratio,
        'sortino_ratio': metrics.sortino_ratio,
        'expectancy': metrics.expectancy,
        'avg_r_multiple': metrics.avg_r_multiple,
        'max_consecutive_wins': metrics.max_consecutive_wins,
        'max_consecutive_losses': metrics.max_consecutive_losses,
        'avg_bars_in_trade': metrics.avg_bars_in_trade,
        'long_trades': metrics.long_trades,
        'short_trades': metrics.short_trades,
        'long_win_rate': metrics.long_win_rate,
        'short_win_rate': metrics.short_win_rate,
    }
