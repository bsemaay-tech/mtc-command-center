from __future__ import annotations

import math
import pandas as pd


INITIAL_EQUITY = 10_000.0


def profit_factor(trades: pd.DataFrame) -> float:
    if trades.empty:
        return 0.0
    returns = trades["net_return_pct"] / 100.0
    gross_profit = returns[returns > 0].sum()
    gross_loss = abs(returns[returns < 0].sum())
    if gross_loss == 0:
        return math.inf if gross_profit > 0 else 0.0
    return float(gross_profit / gross_loss)


def max_drawdown_pct(equity: pd.Series) -> float:
    if equity.empty:
        return 0.0
    return float(((equity / equity.cummax()) - 1.0).min() * 100)


def losing_streak(trades: pd.DataFrame) -> int:
    longest = 0
    current = 0
    for value in trades.get("net_return_pct", pd.Series(dtype=float)):
        if value < 0:
            current += 1
            longest = max(longest, current)
        else:
            current = 0
    return longest


def summarize_trades(asset: str, timeframe: str, parameter_set: str, trades: pd.DataFrame, equity_curve: pd.DataFrame, data: pd.DataFrame, direction: str = "both") -> dict[str, object]:
    final_equity = float(equity_curve["equity"].iloc[-1]) if not equity_curve.empty else INITIAL_EQUITY
    net_return = (final_equity / INITIAL_EQUITY - 1.0) * 100
    dd = max_drawdown_pct(equity_curve["equity"]) if not equity_curve.empty else 0.0
    years = max((data["timestamp"].iloc[-1] - data["timestamp"].iloc[0]).days / 365.25, 1 / 365.25)
    returns = trades["net_return_pct"] if not trades.empty else pd.Series(dtype=float)
    wins = returns[returns > 0]
    losses = returns[returns < 0]
    yearly = {}
    monthly = {}
    if not trades.empty:
        tmp = trades.copy()
        tmp["year"] = pd.to_datetime(tmp["exit_timestamp"]).dt.year
        tmp["month"] = pd.to_datetime(tmp["exit_timestamp"]).dt.strftime("%Y-%m")
        yearly = (((1 + tmp.groupby("year")["net_return_pct"].apply(lambda s: (1 + s / 100).prod() - 1)) - 1) * 100).to_dict()
        monthly = (((1 + tmp.groupby("month")["net_return_pct"].apply(lambda s: (1 + s / 100).prod() - 1)) - 1) * 100).to_dict()
    return {
        "asset": asset,
        "timeframe": timeframe,
        "parameter_set": parameter_set,
        "direction": direction,
        "trade_count": int(len(trades)),
        "win_rate": float((returns > 0).mean() * 100) if not trades.empty else 0.0,
        "average_win": float(wins.mean()) if not wins.empty else 0.0,
        "average_loss": float(losses.mean()) if not losses.empty else 0.0,
        "expectancy_per_trade": float(returns.mean()) if not returns.empty else 0.0,
        "profit_factor": profit_factor(trades),
        "net_return_pct": float(net_return),
        "CAGR": float(((final_equity / INITIAL_EQUITY) ** (1 / years) - 1) * 100),
        "max_drawdown_pct": dd,
        "return_over_dd": float(net_return / abs(dd)) if dd else math.inf,
        "average_R": float(returns.mean()) if not returns.empty else 0.0,
        "median_R": float(returns.median()) if not returns.empty else 0.0,
        "largest_win": float(returns.max()) if not returns.empty else 0.0,
        "largest_loss": float(returns.min()) if not returns.empty else 0.0,
        "longest_losing_streak": losing_streak(trades),
        "exposure_pct": float(trades["holding_bars"].sum() / len(data) * 100) if not trades.empty else 0.0,
        "monthly_returns": monthly,
        "yearly_returns": yearly,
        "fee_adjusted_return": float(net_return),
        "slippage_adjusted_return": float(net_return),
        "final_equity": final_equity,
    }
