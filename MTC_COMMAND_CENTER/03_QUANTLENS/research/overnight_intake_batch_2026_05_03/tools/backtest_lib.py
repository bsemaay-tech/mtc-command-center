"""Shared minimal backtest utilities for QuantLens overnight prototypes.

Conventions:
- All inputs are pandas DataFrames with columns: open, high, low, close, volume,
  datetime index in UTC.
- Trades are dict rows: entry_ts, exit_ts, side, entry, exit, qty (1-unit per trade
  for normalized PF), bars_held, reason, sl, tp, mfe, mae, pnl_R.
- Position size is fixed risk: stop distance = abs(entry - sl); pnl is in R.
- Fees: per-side bps applied on notional. Default 4 bps (taker on Binance USDT-M).
"""
from __future__ import annotations

import math
from dataclasses import dataclass, asdict, field
from pathlib import Path

import pandas as pd
import numpy as np


def load_5m(symbol: str, base: Path) -> pd.DataFrame:
    p = base / "binance_futures" / symbol / "5m" / f"BINANCE_FUTURES_{symbol}_5m_20240101_RESEARCH.csv"
    df = pd.read_csv(p)
    # auto-detect timestamp col
    ts_col = next((c for c in df.columns if c.lower() in ("ts", "timestamp", "datetime", "open_time")), df.columns[0])
    df["dt"] = pd.to_datetime(df[ts_col], utc=True, errors="coerce")
    if df["dt"].isna().any():
        # numeric ms
        df["dt"] = pd.to_datetime(df[ts_col], unit="ms", utc=True, errors="coerce")
    df = df.set_index("dt").sort_index()
    keep = [c for c in df.columns if c.lower() in ("open", "high", "low", "close", "volume")]
    df = df[keep].rename(columns={c: c.lower() for c in keep})
    return df.astype(float)


def resample_daily(df5: pd.DataFrame) -> pd.DataFrame:
    o = df5["open"].resample("1D").first()
    h = df5["high"].resample("1D").max()
    l = df5["low"].resample("1D").min()
    c = df5["close"].resample("1D").last()
    v = df5["volume"].resample("1D").sum()
    out = pd.concat({"open": o, "high": h, "low": l, "close": c, "volume": v}, axis=1).dropna()
    return out


@dataclass
class Trade:
    entry_ts: pd.Timestamp
    exit_ts: pd.Timestamp
    side: str
    entry: float
    exit: float
    sl: float
    tp: float
    bars_held: int
    reason: str
    pnl_R: float
    pnl_pct: float


def fee_pct(bps: float) -> float:
    return bps / 10000.0


def metrics(trades: list[Trade], fee_bps: float) -> dict:
    if not trades:
        return {"trades": 0, "pf": float("nan"), "win_rate": float("nan"),
                "avg_R": float("nan"), "median_R": float("nan"),
                "max_dd_R": float("nan"), "expectancy_R": float("nan"),
                "net_R": float("nan"), "fee_bps_per_side": fee_bps}
    rs = np.array([t.pnl_R for t in trades])
    # apply round-trip fee in R: cost ~ 2 * fee_pct / risk_pct_per_trade
    # we don't know per-trade risk%; use proxy: for each trade, fee_R = 2*fee_pct/(stop_dist/entry)
    fee_Rs = []
    for t in trades:
        risk_pct = abs(t.entry - t.sl) / t.entry if t.entry else 0.01
        if risk_pct == 0:
            risk_pct = 0.005
        fee_Rs.append(2 * fee_pct(fee_bps) / risk_pct)
    fee_Rs = np.array(fee_Rs)
    rs_after = rs - fee_Rs
    wins = rs_after[rs_after > 0]
    losses = rs_after[rs_after < 0]
    pf = (wins.sum() / -losses.sum()) if losses.size and losses.sum() < 0 else float("inf")
    cum = np.cumsum(rs_after)
    peak = np.maximum.accumulate(cum)
    dd = peak - cum
    return {
        "trades": len(rs_after),
        "win_rate": float((rs_after > 0).mean()),
        "avg_R": float(rs_after.mean()),
        "median_R": float(np.median(rs_after)),
        "max_dd_R": float(dd.max()) if dd.size else 0.0,
        "expectancy_R": float(rs_after.mean()),
        "net_R": float(rs_after.sum()),
        "pf": float(pf),
        "fee_bps_per_side": fee_bps,
    }


def fee_stress(trades: list[Trade]) -> dict:
    out = {}
    for bps, label in ((4, "1x"), (8, "2x"), (12, "3x")):
        m = metrics(trades, bps)
        out[label] = m
    out["monotonic"] = (out["1x"]["pf"] >= out["2x"]["pf"] >= out["3x"]["pf"])
    return out
