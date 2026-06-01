"""
vbt_enrichment.py — vectorbt post-processing enrichment layer.

Takes TradingView trade data (from data_get_trades MCP) + price series
and produces richer metrics not available in the 4-gate pipeline:
  - Calmar ratio
  - Sortino ratio
  - Omega ratio
  - Rolling Sharpe (30-trade window)
  - Underwater equity curve (drawdown over time)
  - Monte Carlo simulation (bootstrap confidence bands)

Does NOT replace mega_walk_forward.py, cpcv_validator.py, or MCP tools.
Optional post-step in single_strategy_backtest.py.

Usage:
    from vbt_enrichment import enrich_from_trades, enrich_from_mega_result

    # From TradingView MCP trade list
    stats = enrich_from_trades(tv_trades, price_df)

    # From mega_walk_forward lockbox_oos result
    stats = enrich_from_mega_result(lockbox_result, price_df)

    print(stats.to_dict())
"""
from __future__ import annotations

import json
import math
from dataclasses import dataclass, asdict, field
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

try:
    import vectorbt as vbt
    _VBT_AVAILABLE = True
except ImportError:
    _VBT_AVAILABLE = False

# ---------------------------------------------------------------------------
# Data models
# ---------------------------------------------------------------------------

@dataclass
class EnrichedStats:
    """Enriched post-processing statistics."""
    calmar_ratio: float | None = None
    sortino_ratio: float | None = None
    omega_ratio: float | None = None
    rolling_sharpe_mean: float | None = None
    rolling_sharpe_min: float | None = None
    max_underwater_pct: float | None = None
    total_return_pct: float | None = None
    num_trades: int = 0
    mc_p5_return_pct: float | None = None   # 5th percentile MC return
    mc_p95_return_pct: float | None = None  # 95th percentile MC return
    mc_median_return_pct: float | None = None
    notes: list[str] = field(default_factory=list)
    vbt_available: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent)


# ---------------------------------------------------------------------------
# Core helpers (work without vectorbt — pure numpy/pandas)
# ---------------------------------------------------------------------------

def _compound_returns(r: np.ndarray) -> float:
    """Compound a series of period returns (as decimal, e.g. 0.05 = 5%)."""
    return float(np.prod(1.0 + r) - 1.0)


def _equity_curve(r: np.ndarray) -> np.ndarray:
    return np.cumprod(1.0 + r)


def _max_drawdown(equity: np.ndarray) -> float:
    peak = np.maximum.accumulate(equity)
    dd = (equity - peak) / peak
    return float(dd.min())


def _sharpe(r: np.ndarray, risk_free: float = 0.0) -> float:
    excess = r - risk_free
    if excess.std() == 0:
        return 0.0
    return float(excess.mean() / excess.std() * math.sqrt(len(r)))


def _sortino(r: np.ndarray, risk_free: float = 0.0) -> float:
    excess = r - risk_free
    downside = r[r < risk_free]
    if len(downside) == 0 or downside.std() == 0:
        return float("inf") if excess.mean() > 0 else 0.0
    return float(excess.mean() / downside.std() * math.sqrt(len(r)))


def _omega(r: np.ndarray, threshold: float = 0.0) -> float:
    gains = r[r > threshold] - threshold
    losses = threshold - r[r < threshold]
    if losses.sum() == 0:
        return float("inf")
    return float(gains.sum() / losses.sum())


def _calmar(r: np.ndarray) -> float:
    eq = _equity_curve(r)
    total = _compound_returns(r) * 100.0
    mdd = abs(_max_drawdown(eq)) * 100.0
    if mdd == 0:
        return float("inf")
    return round(total / mdd, 4)


def _rolling_sharpe(r: np.ndarray, window: int = 30) -> np.ndarray:
    if len(r) < window:
        return np.array([])
    result = []
    for i in range(window, len(r) + 1):
        w = r[i - window:i]
        result.append(_sharpe(w))
    return np.array(result)


def _monte_carlo(r: np.ndarray, n_sim: int = 1000, seed: int = 42) -> dict[str, float]:
    rng = np.random.default_rng(seed)
    sim_returns = []
    for _ in range(n_sim):
        shuffled = rng.choice(r, size=len(r), replace=True)
        sim_returns.append(_compound_returns(shuffled) * 100.0)
    arr = np.array(sim_returns)
    return {
        "p5": float(np.percentile(arr, 5)),
        "p95": float(np.percentile(arr, 95)),
        "median": float(np.median(arr)),
    }


# ---------------------------------------------------------------------------
# Trade-list parsers
# ---------------------------------------------------------------------------

def _parse_tv_trades(tv_trades: list[dict]) -> np.ndarray:
    """Convert TradingView trade dicts to array of per-trade return decimals."""
    returns = []
    for t in tv_trades:
        pnl = t.get("profit_pct") or t.get("pnl_pct") or t.get("return_pct")
        if pnl is not None:
            returns.append(float(pnl) / 100.0)
    return np.array(returns, dtype=float)


def _parse_mega_lockbox(lockbox: dict) -> np.ndarray:
    """
    Approximate per-trade returns from mega_walk_forward lockbox stats.
    Uses win_rate, expectancy_R, and profit_factor to reconstruct a
    synthetic return distribution (NOT the original trade sequence).
    """
    trades = int(lockbox.get("num_trades", 0))
    if trades == 0:
        return np.array([])
    win_rate = float(lockbox.get("win_rate", 0.5))
    pf = float(lockbox.get("profit_factor", 1.0))
    # avg_win / avg_loss = pf / (win_rate / (1 - win_rate))
    if win_rate <= 0 or win_rate >= 1:
        return np.array([])
    loss_rate = 1.0 - win_rate
    # set avg_loss = 0.05 (5%) as baseline, solve for avg_win
    avg_loss = 0.05
    avg_win = pf * avg_loss * (loss_rate / win_rate)
    n_wins = max(1, int(round(trades * win_rate)))
    n_losses = trades - n_wins
    rng = np.random.default_rng(seed=42)
    wins = rng.normal(avg_win, avg_win * 0.3, n_wins).clip(0.001, 1.0)
    losses = rng.normal(avg_loss, avg_loss * 0.3, n_losses).clip(0.001, 1.0) * -1
    r = np.concatenate([wins, losses])
    rng.shuffle(r)
    return r


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def enrich_from_trades(tv_trades: list[dict], price_df: pd.DataFrame | None = None,
                       n_mc: int = 1000) -> EnrichedStats:
    """
    Enrich TradingView trade list with richer metrics.

    Args:
        tv_trades:  List of trade dicts from data_get_trades MCP tool.
                    Must have 'profit_pct' (or 'pnl_pct' / 'return_pct') field.
        price_df:   Optional OHLCV dataframe for vectorbt portfolio reconstruction.
        n_mc:       Monte Carlo simulations (default 1000).

    Returns:
        EnrichedStats dataclass.
    """
    r = _parse_tv_trades(tv_trades)
    return _compute(r, n_mc=n_mc, vbt_trades=tv_trades if _VBT_AVAILABLE and price_df is not None else None,
                    price_df=price_df)


def enrich_from_mega_result(lockbox_oos: dict, n_mc: int = 1000) -> EnrichedStats:
    """
    Enrich mega_walk_forward lockbox_oos dict with richer metrics.

    Args:
        lockbox_oos:  summary.lockbox_oos dict from a MEGA result JSON.
        n_mc:         Monte Carlo simulations (default 1000).

    Returns:
        EnrichedStats dataclass.
    """
    r = _parse_mega_lockbox(lockbox_oos)
    stats = _compute(r, n_mc=n_mc)
    stats.notes.append("trade_returns: reconstructed from win_rate/PF (not exact sequence)")
    return stats


def _compute(r: np.ndarray, n_mc: int = 1000,
             vbt_trades: list | None = None, price_df: pd.DataFrame | None = None) -> EnrichedStats:
    stats = EnrichedStats(vbt_available=_VBT_AVAILABLE)

    if len(r) == 0:
        stats.notes.append("no trade returns available")
        return stats

    stats.num_trades = len(r)
    eq = _equity_curve(r)

    # Core metrics
    stats.total_return_pct = round((_compound_returns(r)) * 100.0, 3)
    stats.calmar_ratio = _calmar(r)
    stats.sortino_ratio = round(_sortino(r), 4)
    stats.omega_ratio = round(_omega(r), 4)
    stats.max_underwater_pct = round(_max_drawdown(eq) * 100.0, 3)

    # Rolling Sharpe (30-trade window)
    rs = _rolling_sharpe(r, window=min(30, max(1, len(r) // 3)))
    if len(rs) > 0:
        stats.rolling_sharpe_mean = round(float(rs.mean()), 4)
        stats.rolling_sharpe_min = round(float(rs.min()), 4)

    # Monte Carlo
    mc = _monte_carlo(r, n_sim=n_mc)
    stats.mc_p5_return_pct = round(mc["p5"], 3)
    stats.mc_p95_return_pct = round(mc["p95"], 3)
    stats.mc_median_return_pct = round(mc["median"], 3)

    # vectorbt reconstruction (if available + price_df provided)
    if _VBT_AVAILABLE and vbt_trades and price_df is not None:
        try:
            _enrich_with_vbt(stats, vbt_trades, price_df)
        except Exception as exc:
            stats.notes.append(f"vbt enrichment failed: {exc}")

    return stats


def _enrich_with_vbt(stats: EnrichedStats, tv_trades: list[dict], price_df: pd.DataFrame) -> None:
    """Use vectorbt to reconstruct portfolio from trade list for additional metrics."""
    if "close" not in price_df.columns:
        stats.notes.append("vbt: price_df missing 'close' column")
        return

    close = price_df["close"].copy()

    # Build entry/exit signals from trade timestamps
    entries = pd.Series(False, index=close.index)
    exits = pd.Series(False, index=close.index)

    for t in tv_trades:
        entry_ts = t.get("entry_time") or t.get("entry_ts")
        exit_ts = t.get("exit_time") or t.get("exit_ts")
        if entry_ts and exit_ts:
            try:
                et = pd.Timestamp(entry_ts, tz="UTC")
                xt = pd.Timestamp(exit_ts, tz="UTC")
                if et in close.index:
                    entries.loc[et] = True
                if xt in close.index:
                    exits.loc[xt] = True
            except Exception:
                pass

    if not entries.any():
        stats.notes.append("vbt: no matching entry timestamps in price data")
        return

    pf = vbt.Portfolio.from_signals(close, entries, exits, init_cash=10000.0, fees=0.0008)
    stats.notes.append(f"vbt: portfolio reconstructed from {int(entries.sum())} entry signals")


# ---------------------------------------------------------------------------
# CLI for standalone use
# ---------------------------------------------------------------------------

def _cli_main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mega-json", type=Path, help="MEGA_walk_forward_results.json path")
    parser.add_argument("--strategy", help="filter by strategy ID")
    parser.add_argument("--symbol", help="filter by symbol")
    parser.add_argument("--tf", help="filter by timeframe")
    parser.add_argument("--n-mc", type=int, default=1000)
    parser.add_argument("--out", type=Path, help="output JSON path")
    args = parser.parse_args()

    if args.mega_json:
        data = json.loads(args.mega_json.read_text(encoding="utf-8"))
        results = data.get("results", [])
        target = None
        for r in results:
            if (args.strategy is None or r.get("strategy") == args.strategy) and \
               (args.symbol is None or r.get("symbol") == args.symbol) and \
               (args.tf is None or r.get("timeframe") == args.tf):
                if r.get("summary", {}).get("lockbox_oos"):
                    target = r
                    break

        if target is None:
            print("No matching PASS/STRONG_PASS result found.")
            return

        lb = target["summary"]["lockbox_oos"]
        stats = enrich_from_mega_result(lb, n_mc=args.n_mc)
        print(f"\n=== Enriched Stats: {target['strategy']} / {target['symbol']} / {target['timeframe']} ===")
        print(stats.to_json())

        if args.out:
            args.out.parent.mkdir(parents=True, exist_ok=True)
            args.out.write_text(stats.to_json(), encoding="utf-8")
            print(f"\nWritten -> {args.out}")
    else:
        parser.print_help()


if __name__ == "__main__":
    _cli_main()
