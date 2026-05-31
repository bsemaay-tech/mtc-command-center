from __future__ import annotations

import math
from typing import Any

import numpy as np
import pandas as pd


def profit_factor(returns: pd.Series) -> float:
    clean = pd.to_numeric(returns, errors="coerce").dropna()
    wins = clean[clean > 0].sum()
    losses = -clean[clean <= 0].sum()
    if losses > 0:
        return float(wins / losses)
    return 999.0 if wins > 0 else 0.0


def equity_curve(returns: pd.Series) -> pd.Series:
    clean = pd.to_numeric(returns, errors="coerce").fillna(0.0)
    return (1.0 + clean / 100.0).cumprod()


def max_drawdown_pct(returns: pd.Series) -> float:
    eq = equity_curve(returns)
    if eq.empty:
        return 0.0
    dd = eq / eq.cummax() - 1.0
    return float(dd.min() * 100.0)


def metrics_from_trades(trades: pd.DataFrame, cost_pct: float = 0.12, assets_tested: int | None = None) -> dict[str, Any]:
    if trades.empty:
        return {
            "trade_count": 0,
            "assets_tested": assets_tested or 0,
            "net_return_after_costs": 0.0,
            "profit_factor": 0.0,
            "win_rate": 0.0,
            "average_trade": 0.0,
            "median_trade": 0.0,
            "expectancy": 0.0,
            "average_winner": 0.0,
            "average_loser": 0.0,
            "max_drawdown": 0.0,
            "return_over_dd": 0.0,
            "exposure": 0.0,
            "average_hold_bars": 0.0,
            "best_asset": "",
            "worst_asset": "",
            "concentration_warning": False,
        }
    data = trades.copy()
    if "net_return_pct" not in data:
        data["net_return_pct"] = pd.to_numeric(data["gross_return_pct"], errors="coerce") - cost_pct
    returns = pd.to_numeric(data["net_return_pct"], errors="coerce").dropna()
    eq = equity_curve(returns)
    net = float((eq.iloc[-1] - 1.0) * 100.0) if len(eq) else 0.0
    dd = max_drawdown_pct(returns)
    winners = returns[returns > 0]
    losers = returns[returns <= 0]
    per_asset = []
    if "asset" in data.columns:
        for asset, subset in data.groupby("asset"):
            r = pd.to_numeric(subset["net_return_pct"], errors="coerce").dropna()
            if not r.empty:
                per_asset.append((asset, float((equity_curve(r).iloc[-1] - 1.0) * 100.0)))
    best_asset = max(per_asset, key=lambda x: x[1])[0] if per_asset else ""
    worst_asset = min(per_asset, key=lambda x: x[1])[0] if per_asset else ""
    positive_sum = sum(v for _, v in per_asset if v > 0)
    concentration = False
    if positive_sum > 0 and per_asset:
        concentration = max(max(v, 0) for _, v in per_asset) / positive_sum > 0.50
    return {
        "trade_count": int(len(returns)),
        "assets_tested": int(assets_tested if assets_tested is not None else data["asset"].nunique() if "asset" in data else 0),
        "net_return_after_costs": round(net, 4),
        "profit_factor": round(profit_factor(returns), 4),
        "win_rate": round(float((returns > 0).mean() * 100.0), 4),
        "average_trade": round(float(returns.mean()), 4),
        "median_trade": round(float(returns.median()), 4),
        "expectancy": round(float(returns.mean()), 4),
        "average_winner": round(float(winners.mean()) if len(winners) else 0.0, 4),
        "average_loser": round(float(losers.mean()) if len(losers) else 0.0, 4),
        "max_drawdown": round(dd, 4),
        "return_over_dd": round(net / abs(dd), 4) if dd else 0.0,
        "exposure": round(float(data.get("hold_bars", pd.Series([0])).sum()) / max(len(data) * 100, 1) * 100.0, 4),
        "average_hold_bars": round(float(data.get("hold_bars", pd.Series([0])).mean()), 4),
        "best_asset": best_asset,
        "worst_asset": worst_asset,
        "concentration_warning": bool(concentration),
    }


def fee_stress(trades: pd.DataFrame, base_cost_pct: float = 0.12) -> list[dict[str, Any]]:
    rows = []
    if trades.empty:
        for mult in [1, 2, 3, 5]:
            rows.append({"cost_mult": mult, "profit_factor": 0.0, "net_return_after_costs": 0.0})
        return rows
    gross = pd.to_numeric(trades["gross_return_pct"], errors="coerce").fillna(0.0)
    for mult in [1, 2, 3, 5]:
        stressed = gross - base_cost_pct * mult
        eq = equity_curve(stressed)
        rows.append(
            {
                "cost_mult": mult,
                "profit_factor": round(profit_factor(stressed), 4),
                "net_return_after_costs": round(float((eq.iloc[-1] - 1.0) * 100.0), 4) if len(eq) else 0.0,
                "max_drawdown": round(max_drawdown_pct(stressed), 4),
            }
        )
    return rows


def monte_carlo(trades: pd.DataFrame, n: int = 200, seed: int = 42) -> dict[str, Any]:
    if trades.empty or "net_return_pct" not in trades:
        return {"mc_runs": 0, "p_negative": 1.0, "p5_return": 0.0, "median_return": 0.0, "p95_drawdown": 0.0}
    rng = np.random.default_rng(seed)
    returns = pd.to_numeric(trades["net_return_pct"], errors="coerce").dropna().to_numpy()
    if len(returns) == 0:
        return {"mc_runs": 0, "p_negative": 1.0, "p5_return": 0.0, "median_return": 0.0, "p95_drawdown": 0.0}
    finals = []
    dds = []
    for _ in range(n):
        sample = rng.choice(returns, size=len(returns), replace=True)
        s = pd.Series(sample)
        eq = equity_curve(s)
        finals.append(float((eq.iloc[-1] - 1.0) * 100.0))
        dds.append(max_drawdown_pct(s))
    return {
        "mc_runs": n,
        "p_negative": round(float(np.mean(np.array(finals) < 0)), 4),
        "p5_return": round(float(np.percentile(finals, 5)), 4),
        "median_return": round(float(np.percentile(finals, 50)), 4),
        "p95_drawdown": round(float(np.percentile(dds, 5)), 4),
    }
