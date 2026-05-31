from __future__ import annotations

import pandas as pd


def remove_best_asset(trades: pd.DataFrame) -> pd.DataFrame:
    if trades.empty or "asset" not in trades:
        return trades.copy()
    perf = trades.groupby("asset")["net_return_pct"].sum().sort_values(ascending=False)
    if perf.empty:
        return trades.copy()
    return trades[trades["asset"] != perf.index[0]].copy()


def remove_best_year(trades: pd.DataFrame) -> pd.DataFrame:
    if trades.empty:
        return trades.copy()
    data = trades.copy()
    data["year"] = pd.to_datetime(data["entry_time"], utc=True).dt.year
    perf = data.groupby("year")["net_return_pct"].sum().sort_values(ascending=False)
    if perf.empty:
        return trades.copy()
    return data[data["year"] != perf.index[0]].drop(columns=["year"]).copy()


def remove_top_trades(trades: pd.DataFrame, n: int = 5) -> pd.DataFrame:
    if trades.empty:
        return trades.copy()
    return trades.sort_values("net_return_pct", ascending=False).iloc[n:].copy()
