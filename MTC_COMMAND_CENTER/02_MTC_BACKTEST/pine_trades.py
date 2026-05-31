"""
pine_trades.py - trade list extractor from PineTS output.

MTC_V2.pine keeps its own trade state machine independent from strategy.* calls.
This script reconstructs one exit-event row per Pine close event, including
TP1 partial exits.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

REPO_ROOT = Path(__file__).resolve().parent

EXIT_REASON_MAP = {
    0.0: "none",
    1.0: "sl_atr_hit",
    2.0: "sl_percent_hit",
    3.0: "sl_swing_atr_hit",
    4.0: "opp_signal",
    5.0: "tp_atr_hit",
    6.0: "tp_percent_hit",
    7.0: "tp_r_hit",
    8.0: "tp1_hit",
    9.0: "tp2_hit",
    10.0: "be_hit",
    11.0: "trail_hit",
    12.0: "price_exit_ambiguous",
    13.0: "filter_block",
    14.0: "time_stop",
    15.0: "eod_exit",
    16.0: "eow_exit",
}


def load_signals(path: Path) -> tuple[dict, pd.DataFrame]:
    with open(path, encoding="utf-8") as handle:
        raw = json.load(handle)
    meta = raw["meta"]
    df = pd.DataFrame(raw["signals"])
    df["dt"] = pd.to_datetime(df["timestamp"], unit="ms", utc=True)
    return meta, df


def extract_trades(df: pd.DataFrame, initial_capital: float = 10_000.0) -> list[dict]:
    trades: list[dict] = []
    current: dict[str, Any] | None = None

    for index, row in df.iterrows():
        side = int((row.get("position_side", 0) or 0))
        lifecycle_id = int((row.get("lifecycle_id", 0) or 0))
        exit_code = float(row.get("exit_signal", 0) or 0)
        exit_reason = EXIT_REASON_MAP.get(exit_code, "unknown")
        opened_new_lifecycle_this_row = False

        if current is None and side != 0:
            current = _snapshot_trade(row, index)
        elif current is not None and side != 0 and lifecycle_id != int(current.get("lifecycle_id", -1)):
            exit_qty = _safe_float(row.get("last_exit_qty"), _safe_float(current.get("qty"), 0.0))
            trades.append(
                _close_trade_event(
                    current,
                    row=row,
                    exit_price=_safe_float(row.get("exit_price"), _safe_float(row.get("close"))),
                    exit_reason=exit_reason if exit_code > 0 else "opp_signal",
                    exit_qty=exit_qty,
                    initial_capital=initial_capital,
                )
            )
            current = _snapshot_trade(row, index)
            opened_new_lifecycle_this_row = True

        if current is None:
            continue

        tp1_processed = False
        tp1_qty = _safe_float(row.get("tp1_exit_qty"), 0.0)
        if int((row.get("tp1_hit", 0) or 0)) == 1 and tp1_qty > 0.0:
            tp1_fill = _safe_float(
                row.get("tp1_fill_price"),
                _safe_float(row.get("tp1_price"), _safe_float(row.get("exit_price"), _safe_float(row.get("close")))),
            )
            trades.append(
                _close_trade_event(
                    current,
                    row=row,
                    exit_price=tp1_fill,
                    exit_reason="tp1_hit",
                    exit_qty=tp1_qty,
                    initial_capital=initial_capital,
                )
            )
            current["qty"] = max(0.0, _safe_float(current.get("qty"), 0.0) - tp1_qty)
            current["active_tp_price"] = row.get("tp2_price")
            tp1_processed = True
            if _safe_float(current.get("qty"), 0.0) <= 1e-12:
                current = None

        if current is None:
            continue

        final_exit = False
        if exit_code > 0 and not opened_new_lifecycle_this_row and not (tp1_processed and exit_reason == "tp1_hit"):
            final_exit = True
        elif side == 0:
            final_exit = True

        if final_exit:
            exit_qty = _safe_float(row.get("last_exit_qty"), _safe_float(current.get("qty"), 0.0))
            exit_price = _safe_float(row.get("exit_price"), _pick_exit_price(row, current, exit_code))
            trades.append(
                _close_trade_event(
                    current,
                    row=row,
                    exit_price=exit_price,
                    exit_reason=exit_reason if exit_code > 0 else "unknown",
                    exit_qty=exit_qty,
                    initial_capital=initial_capital,
                )
            )
            current = None
            continue

        if side != 0:
            current["qty"] = _safe_float(row.get("qty"), _safe_float(current.get("qty"), 0.0))
            current["avg_entry_price"] = _coalesce_float(row.get("avg_entry_price"), current.get("avg_entry_price"))
            current["active_stop_price"] = row.get("active_stop_price")
            current["active_tp_price"] = row.get("active_tp_price")
            current["sizing_equity"] = row.get("sizing_equity")

    if current is not None:
        last = df.iloc[-1]
        trades.append(
            _close_trade_event(
                current,
                row=last,
                exit_price=_safe_float(last.get("close")),
                exit_reason="terminal_close",
                exit_qty=_safe_float(current.get("qty"), 0.0),
                initial_capital=initial_capital,
            )
        )

    return trades


def _snapshot_trade(row: pd.Series, fallback_index: int) -> dict[str, Any]:
    side = int((row.get("position_side", 0) or 0))
    return {
        "lifecycle_id": int((row.get("lifecycle_id", 0) or 0)),
        "direction": "long" if side > 0 else "short",
        "entry_bar": int(row.get("bar_index", fallback_index)),
        "entry_time": str(row["dt"]),
        "entry_price": row.get("entry_price"),
        "avg_entry_price": row.get("avg_entry_price"),
        "initial_stop": row.get("active_stop_price"),
        "initial_tp": row.get("active_tp_price"),
        "active_stop_price": row.get("active_stop_price"),
        "active_tp_price": row.get("active_tp_price"),
        "qty": _safe_float(row.get("qty"), 0.0),
        "sizing_equity": row.get("sizing_equity"),
        "open": row.get("open"),
        "high": row.get("high"),
        "low": row.get("low"),
        "close": row.get("close"),
    }


def _close_trade_event(
    trade: dict[str, Any],
    *,
    row: pd.Series,
    exit_price: float | None,
    exit_reason: str,
    exit_qty: float,
    initial_capital: float,
) -> dict[str, Any]:
    closed = dict(trade)
    closed["qty"] = exit_qty
    closed["exit_bar"] = int(row.get("bar_index", 0))
    closed["exit_time"] = str(row["dt"])
    closed["exit_price"] = exit_price
    closed["exit_reason"] = exit_reason
    closed["exit_close"] = row.get("close")
    _compute_pnl(closed, initial_capital)
    return closed


def _pick_exit_price(row: pd.Series, trade: dict[str, Any], ex_reason: float) -> float | None:
    reason = float(ex_reason or 0.0)
    direction = trade.get("direction", "long")
    stop = _safe_float(row.get("active_stop_price"), _safe_float(trade.get("active_stop_price")))
    tp = _safe_float(row.get("active_tp_price"), _safe_float(trade.get("active_tp_price")))
    open_ = _safe_float(row.get("open"))
    close_ = _safe_float(row.get("close"))

    if reason in {1.0, 2.0, 3.0, 10.0, 11.0} and stop is not None:
        if direction == "long":
            return open_ if open_ is not None and open_ <= stop else stop
        return open_ if open_ is not None and open_ >= stop else stop

    if reason in {5.0, 6.0, 7.0, 9.0} and tp is not None:
        if direction == "long":
            return open_ if open_ is not None and open_ >= tp else tp
        return open_ if open_ is not None and open_ <= tp else tp

    if reason == 4.0:
        return close_

    return close_


def _compute_pnl(trade: dict[str, Any], initial_capital: float) -> None:
    try:
        entry = float(trade.get("avg_entry_price") or trade.get("entry_price") or 0.0)
        exit_ = float(trade.get("exit_price") or 0.0)
        qty = float(trade.get("qty") or 0.0)
        side = 1 if trade["direction"] == "long" else -1

        if entry > 0 and exit_ > 0 and qty > 0:
            gross_pnl = side * (exit_ - entry) * qty
            trade["gross_pnl"] = round(gross_pnl, 6)
            trade["pnl_pct"] = round(gross_pnl / initial_capital * 100.0, 4)
            trade["win"] = gross_pnl > 0
            trade["duration_bars"] = int(trade.get("exit_bar", 0)) - int(trade.get("entry_bar", 0))
        else:
            trade["gross_pnl"] = None
            trade["pnl_pct"] = None
            trade["win"] = None
            trade["duration_bars"] = None
    except Exception:
        trade["gross_pnl"] = None
        trade["pnl_pct"] = None
        trade["win"] = None
        trade["duration_bars"] = None


def compute_metrics(trades: list[dict[str, Any]], initial_capital: float = 10_000.0) -> dict[str, Any]:
    if not trades:
        return {
            "total_trades": 0,
            "closed_trades": 0,
            "win_rate_pct": 0.0,
            "net_pnl": 0.0,
            "net_pnl_pct": 0.0,
            "profit_factor": 0.0,
            "max_drawdown_pct": 0.0,
            "gross_wins": 0.0,
            "gross_losses": 0.0,
            "avg_trade_pnl": 0.0,
            "long_trades": 0,
            "short_trades": 0,
            "exit_reasons": {},
        }

    closed = [trade for trade in trades if trade.get("gross_pnl") is not None]
    wins = [trade for trade in closed if trade.get("win")]
    losses = [trade for trade in closed if not trade.get("win") and trade.get("gross_pnl", 0.0) != 0.0]

    gross_wins = sum(float(trade["gross_pnl"]) for trade in wins)
    gross_losses = abs(sum(float(trade["gross_pnl"]) for trade in losses))
    net_pnl = sum(float(trade["gross_pnl"]) for trade in closed)
    net_pnl_pct = net_pnl / initial_capital * 100.0

    profit_factor = (gross_wins / gross_losses) if gross_losses > 0 else float("inf")
    win_rate = len(wins) / len(closed) * 100.0 if closed else 0.0

    equity = initial_capital
    peak = initial_capital
    max_dd = 0.0
    for trade in closed:
        equity += float(trade["gross_pnl"])
        if equity > peak:
            peak = equity
        dd = (peak - equity) / peak * 100.0 if peak > 0 else 0.0
        if dd > max_dd:
            max_dd = dd

    longs = [trade for trade in trades if trade["direction"] == "long"]
    shorts = [trade for trade in trades if trade["direction"] == "short"]

    return {
        "total_trades": len(trades),
        "closed_trades": len(closed),
        "win_rate_pct": round(win_rate, 2),
        "net_pnl": round(net_pnl, 4),
        "net_pnl_pct": round(net_pnl_pct, 4),
        "profit_factor": round(profit_factor, 4) if profit_factor != float("inf") else "inf",
        "max_drawdown_pct": round(max_dd, 2),
        "gross_wins": round(gross_wins, 4),
        "gross_losses": round(gross_losses, 4),
        "avg_trade_pnl": round(net_pnl / len(closed), 4) if closed else 0.0,
        "long_trades": len(longs),
        "short_trades": len(shorts),
        "exit_reasons": _count_exit_reasons(trades),
    }


def _count_exit_reasons(trades: list[dict[str, Any]]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for trade in trades:
        reason = str(trade.get("exit_reason", "unknown"))
        counts[reason] = counts.get(reason, 0) + 1
    return counts


def _safe_float(value: Any, default: float | None = None) -> float | None:
    if value is None:
        return default
    try:
        numeric = float(value)
    except (TypeError, ValueError):
        return default
    if not math.isfinite(numeric):
        return default
    return numeric


def _coalesce_float(value: Any, fallback: Any) -> float | None:
    parsed = _safe_float(value)
    if parsed is not None:
        return parsed
    return _safe_float(fallback)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--signals", default="data/mtc_signals.json")
    parser.add_argument("--capital", type=float, default=1_000_000.0, help="Initial capital (MTC_V2 default: 1,000,000)")
    parser.add_argument("--out-json", default="data/pine_trades.json")
    parser.add_argument("--out-csv", default="data/pine_trades.csv")
    args = parser.parse_args()

    signals_path = REPO_ROOT / args.signals

    print("=== Pine Trade Extractor ===\n")
    print(f"Signals: {signals_path}")

    meta, df = load_signals(signals_path)
    print(f"Bars   : {len(df)}  ({meta['symbol']} {meta['timeframe']})")
    print(f"Range  : {df['dt'].iloc[0].date()} -> {df['dt'].iloc[-1].date()}")

    trades = extract_trades(df, initial_capital=args.capital)
    metrics = compute_metrics(trades, initial_capital=args.capital)

    print("\n--- Pine Metrics (PineTS state machine) ---")
    print(f"  Total trades   : {metrics['total_trades']}")
    print(f"  Win rate       : {metrics['win_rate_pct']}%")
    print(f"  Net PnL        : ${metrics['net_pnl']:,.2f}  ({metrics['net_pnl_pct']}%)")
    print(f"  Profit factor  : {metrics['profit_factor']}")
    print(f"  Max drawdown   : {metrics['max_drawdown_pct']}%")
    print(f"  Long / Short   : {metrics['long_trades']} / {metrics['short_trades']}")
    print(f"  Exit reasons   : {metrics['exit_reasons']}")

    out_json = REPO_ROOT / args.out_json
    out_json.parent.mkdir(exist_ok=True)
    payload = {
        "meta": {
            **meta,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "initial_capital": args.capital,
            "extractor": "pine_trades.py",
        },
        "metrics": metrics,
        "trades": trades,
    }
    with open(out_json, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, default=str)

    out_csv = REPO_ROOT / args.out_csv
    if trades:
        pd.DataFrame(trades).to_csv(out_csv, index=False, encoding="utf-8")

    print(f"\nSaved: {out_json}")
    print(f"       {out_csv}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
