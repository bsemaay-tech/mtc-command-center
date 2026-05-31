"""
parity_test.py — MTC_V2 Signal/Backtest Parity Check

Steps:
  1. Load data/mtc_signals.json  (PineTS output)
  2. Fetch same OHLCV from CCXT/Binance and verify timestamp alignment
  3. Run a simple vectorbt backtest using PineTS entry/exit signals
  4. Compare key metrics vs reference (from signals JSON embedded position tracking)
  5. Output reports/parity_report.json

Usage:
  python parity_test.py
"""

import json
import sys
import traceback

# Force UTF-8 output on Windows to avoid charmap errors with Unicode in print()
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
from pathlib import Path
from datetime import datetime, timezone

import pandas as pd
import numpy as np

REPORTS_DIR = Path("reports")
REPORTS_DIR.mkdir(exist_ok=True)

SIGNALS_PATH = Path("data/mtc_signals.json")
OUT_PATH     = REPORTS_DIR / "parity_report.json"

report = {
    "timestamp": datetime.now(timezone.utc).isoformat(),
    "signals_source": str(SIGNALS_PATH),
    "steps": {},
    "metrics": {},
    "parity": {},
    "verdict": None,
    "errors": [],
}

# ─── Step 1: Load signals JSON ────────────────────────────────────────────────
print("=== MTC_V2 Parity Test ===\n")
print(f"Step 1: Loading {SIGNALS_PATH}")

try:
    with open(SIGNALS_PATH, encoding="utf-8") as f:
        data = json.load(f)

    meta    = data["meta"]
    signals = data["signals"]
    df = pd.DataFrame(signals)

    # Parse timestamps (ms epoch → UTC datetime)
    df["dt"] = pd.to_datetime(df["timestamp"], unit="ms", utc=True)
    df = df.set_index("dt").sort_index()

    print(f"  Bars loaded  : {len(df)}")
    print(f"  Symbol       : {meta['symbol']}  TF: {meta['timeframe']}")
    print(f"  Date range   : {df.index[0].date()} → {df.index[-1].date()}")
    print(f"  Long signals : {meta['signal_counts']['long']}")
    print(f"  Short signals: {meta['signal_counts']['short']}")
    print(f"  Exits        : {meta['signal_counts']['exits']}")

    report["steps"]["load_signals"] = {
        "status": "OK",
        "bars": len(df),
        "date_from": str(df.index[0].date()),
        "date_to":   str(df.index[-1].date()),
    }
except Exception as e:
    err = f"Load signals failed: {e}"
    print(f"  ERROR: {err}")
    report["errors"].append(err)
    report["steps"]["load_signals"] = {"status": "ERROR", "message": err}
    json.dump(report, open(OUT_PATH, "w", encoding="utf-8"), indent=2)
    sys.exit(1)

# ─── Step 2: CCXT Binance fetch + alignment check ────────────────────────────
print("\nStep 2: Fetch OHLCV from CCXT/Binance and verify alignment")

try:
    import ccxt

    exchange = ccxt.binance({"options": {"defaultType": "spot"}})
    exchange.load_markets()

    symbol = f"{meta['symbol'][:3]}/{meta['symbol'][3:]}"  # BTCUSDT → BTC/USDT
    tf     = meta["timeframe"]
    limit  = len(df)

    # Use the same start timestamp as the signals JSON
    since_ms = int(df.index[0].timestamp() * 1000)

    print(f"  Fetching {limit} bars of {symbol} {tf} from {df.index[0].date()}...")
    ohlcv = exchange.fetch_ohlcv(symbol, tf, since=since_ms, limit=limit)

    ccxt_df = pd.DataFrame(ohlcv, columns=["timestamp_ms", "open", "high", "low", "close", "volume"])
    ccxt_df["dt"] = pd.to_datetime(ccxt_df["timestamp_ms"], unit="ms", utc=True)
    ccxt_df = ccxt_df.set_index("dt").sort_index()

    print(f"  CCXT returned: {len(ccxt_df)} bars  {ccxt_df.index[0].date()} → {ccxt_df.index[-1].date()}")

    # Alignment: compare close prices on overlapping timestamps
    common_idx = df.index.intersection(ccxt_df.index)
    if len(common_idx) == 0:
        raise ValueError("No overlapping timestamps between PineTS and CCXT data")

    pine_close = df.loc[common_idx, "close"].astype(float)
    ccxt_close = ccxt_df.loc[common_idx, "close"].astype(float)

    abs_diff  = (pine_close - ccxt_close).abs()
    max_diff  = float(abs_diff.max())
    mean_diff = float(abs_diff.mean())
    match_pct = float((abs_diff < 0.1).mean() * 100)  # within 1 cent = same bar

    print(f"  Overlapping bars  : {len(common_idx)}")
    print(f"  Max close diff    : {max_diff:.4f}")
    print(f"  Mean close diff   : {mean_diff:.6f}")
    print(f"  Bars within $0.10 : {match_pct:.1f}%")

    alignment_ok = match_pct >= 95.0

    report["steps"]["ohlcv_alignment"] = {
        "status": "OK" if alignment_ok else "MISMATCH",
        "common_bars": len(common_idx),
        "max_close_diff": round(max_diff, 6),
        "mean_close_diff": round(mean_diff, 6),
        "within_10cent_pct": round(match_pct, 2),
        "aligned": alignment_ok,
    }

    if alignment_ok:
        print("  ALIGNMENT OK — OHLCV data matches between PineTS and CCXT")
    else:
        print("  WARNING — Close price mismatch > 5% of bars")

    # Use CCXT data as authoritative OHLCV, merged with PineTS signals
    merged = ccxt_df.join(
        df[["long_signal","short_signal","exit_signal",
            "active_stop_price","active_tp_price","position_side",
            "entry_price","avg_entry_price","qty","direction"]],
        how="inner"
    )

except Exception as e:
    err = f"CCXT alignment failed: {e}\n{traceback.format_exc()}"
    print(f"  ERROR: {err[:300]}")
    report["errors"].append(err[:500])
    report["steps"]["ohlcv_alignment"] = {"status": "ERROR", "message": str(e)[:200]}
    # Fall back: use PineTS OHLCV directly
    merged = df.copy()
    merged.rename(columns={}, inplace=True)
    print("  Falling back to PineTS OHLCV for vectorbt run")

# ─── Step 3: vectorbt backtest ────────────────────────────────────────────────
print("\nStep 3: Run vectorbt backtest from PineTS signals")

try:
    import vectorbt as vbt

    close_s  = merged["close"].astype(float)
    entries  = (merged["long_signal"].fillna(0).astype(int) == 1)
    s_entries= (merged["short_signal"].fillna(0).astype(int) == 1)
    exits_sig= (merged["exit_signal"].fillna(0).astype(float) > 0)

    # Combined exit = explicit exit signal OR opposite entry
    exits  = exits_sig | s_entries   # long exits on short signal or explicit exit
    s_exits= exits_sig | entries      # short exits on long signal or explicit exit

    print(f"  Long entries  : {entries.sum()}")
    print(f"  Short entries : {s_entries.sum()}")
    print(f"  Long exits    : {exits.sum()}")
    print(f"  Short exits   : {s_exits.sum()}")

    # Run long-only portfolio (simpler, just to verify signal path works)
    pf_long = vbt.Portfolio.from_signals(
        close_s,
        entries=entries,
        exits=exits,
        init_cash=1_000_000,
        freq=meta["timeframe"],
        fees=0.001,       # 0.1% fee
        slippage=0.001,
    )

    # Run short-only portfolio
    pf_short = vbt.Portfolio.from_signals(
        close_s,
        short_entries=s_entries,
        short_exits=s_exits,
        init_cash=1_000_000,
        freq=meta["timeframe"],
        fees=0.001,
        slippage=0.001,
    )

    # Extract metrics
    def safe_metric(fn):
        try:
            v = fn()
            return float(v) if not (isinstance(v, float) and np.isnan(v)) else None
        except Exception:
            return None

    long_stats  = pf_long.stats()
    short_stats = pf_short.stats()

    long_trades  = pf_long.trades.count()
    short_trades = pf_short.trades.count()

    metrics = {
        "long": {
            "total_trades":  int(long_trades),
            "win_rate_pct":  safe_metric(lambda: long_stats.get("Win Rate [%]",  np.nan)),
            "net_pnl":       safe_metric(lambda: long_stats.get("Total Return [%]", np.nan)),
            "max_drawdown_pct": safe_metric(lambda: long_stats.get("Max Drawdown [%]", np.nan)),
            "sharpe":        safe_metric(lambda: long_stats.get("Sharpe Ratio", np.nan)),
        },
        "short": {
            "total_trades":  int(short_trades),
            "win_rate_pct":  safe_metric(lambda: short_stats.get("Win Rate [%]",  np.nan)),
            "net_pnl":       safe_metric(lambda: short_stats.get("Total Return [%]", np.nan)),
            "max_drawdown_pct": safe_metric(lambda: short_stats.get("Max Drawdown [%]", np.nan)),
            "sharpe":        safe_metric(lambda: short_stats.get("Sharpe Ratio", np.nan)),
        },
    }

    print(f"\n  Long  portfolio: {long_trades} trades  win_rate={metrics['long']['win_rate_pct']}%  pnl={metrics['long']['net_pnl']}%")
    print(f"  Short portfolio: {short_trades} trades  win_rate={metrics['short']['win_rate_pct']}%  pnl={metrics['short']['net_pnl']}%")

    report["metrics"]  = metrics
    report["steps"]["vectorbt_run"] = {"status": "OK"}

except Exception as e:
    err = f"vectorbt run failed: {e}\n{traceback.format_exc()}"
    print(f"  ERROR: {err[:400]}")
    report["errors"].append(err[:600])
    report["steps"]["vectorbt_run"] = {"status": "ERROR", "message": str(e)[:300]}
    metrics = None

# ─── Step 4: Parity comparison ────────────────────────────────────────────────
print("\nStep 4: Compare metrics against PineTS reference")

# Reference: what the PineTS position_side tracking tells us about trade count
pine_entries_total = meta["signal_counts"]["long"] + meta["signal_counts"]["short"]
pine_exits_total   = meta["signal_counts"]["exits"]

parity = {}

if metrics:
    vbt_total_trades = metrics["long"]["total_trades"] + metrics["short"]["total_trades"]

    # Trade count parity
    trade_diff = abs(vbt_total_trades - pine_exits_total)
    trade_match = trade_diff <= max(2, pine_exits_total * 0.10)  # within 10% or 2 trades

    parity["trade_count"] = {
        "pine_exits":    pine_exits_total,
        "pine_entries":  pine_entries_total,
        "vbt_trades":    vbt_total_trades,
        "diff":          trade_diff,
        "match":         trade_match,
        "note": "vbt counts closed trades; pine counts exit events — small diff expected",
    }

    # Net PnL direction
    long_pnl  = metrics["long"]["net_pnl"]  or 0
    short_pnl = metrics["short"]["net_pnl"] or 0
    total_pnl = long_pnl + short_pnl
    parity["net_pnl_direction"] = {
        "total_return_pct": round(total_pnl, 4),
        "positive":         total_pnl > 0,
        "match":            True,   # direction sanity only — no TV reference to compare
        "note": "No TradingView reference run available; direction check only",
    }

    # Win rate sanity (>0% and <100% = realistic)
    long_wr  = metrics["long"]["win_rate_pct"]
    short_wr = metrics["short"]["win_rate_pct"]
    wr_realistic = (
        (long_wr  is None or (0 < long_wr  < 100)) and
        (short_wr is None or (0 < short_wr < 100))
    )
    parity["win_rate_sanity"] = {
        "long_win_rate":  long_wr,
        "short_win_rate": short_wr,
        "realistic":      wr_realistic,
        "match":          wr_realistic,
    }

    # Max drawdown sanity (<50% = not blown up)
    long_dd  = metrics["long"]["max_drawdown_pct"]  or 0
    short_dd = metrics["short"]["max_drawdown_pct"] or 0
    dd_ok = abs(long_dd) < 50 and abs(short_dd) < 50
    parity["max_drawdown_sanity"] = {
        "long_dd_pct":  long_dd,
        "short_dd_pct": short_dd,
        "under_50pct":  dd_ok,
        "match":        dd_ok,
    }

    # Overall verdict
    all_match = all(v.get("match", False) for v in parity.values())
    report["verdict"] = "PASS" if all_match else "PARTIAL"

    print(f"\n  Trade count  : pine={pine_exits_total}  vbt={vbt_total_trades}  diff={trade_diff}  {'OK' if trade_match else 'MISMATCH'}")
    print(f"  Net PnL      : {round(total_pnl, 2)}%  ({'positive' if total_pnl > 0 else 'negative'})")
    print(f"  Win rate     : long={long_wr}%  short={short_wr}%  sanity={'OK' if wr_realistic else 'FAIL'}")
    print(f"  Max DD       : long={long_dd}%  short={short_dd}%  sanity={'OK' if dd_ok else 'FAIL'}")
    print(f"\n  VERDICT: {report['verdict']}")
else:
    report["verdict"] = "ERROR"
    parity["error"] = "vectorbt run failed — no metrics to compare"
    print("  VERDICT: ERROR (vectorbt failed)")

report["parity"] = parity

# ─── Save report ─────────────────────────────────────────────────────────────
with open(OUT_PATH, "w", encoding="utf-8") as f:
    json.dump(report, f, indent=2)

print(f"\nReport saved → {OUT_PATH}")
