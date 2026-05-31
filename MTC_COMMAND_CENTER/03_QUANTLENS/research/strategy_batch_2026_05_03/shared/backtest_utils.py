from __future__ import annotations

import pandas as pd

from metrics import INITIAL_EQUITY, summarize_trades


def run_signal_backtest(
    data: pd.DataFrame,
    signal: pd.DataFrame,
    asset: str,
    timeframe: str,
    parameter_set: str,
    commission: float = 0.0004,
    slippage: float = 0.0002,
    max_hold: int = 20,
) -> tuple[dict[str, object], pd.DataFrame, pd.DataFrame]:
    equity = INITIAL_EQUITY
    trades = []
    equity_rows = [{"timestamp": data["timestamp"].iloc[0], "equity": equity}]
    index = 1
    while index < len(data) - 1:
        row = signal.iloc[index]
        direction = "long" if bool(row.get("long_entry", False)) else "short" if bool(row.get("short_entry", False)) else ""
        if not direction:
            index += 1
            continue
        entry_index = index + 1
        entry_raw = float(data["open"].iloc[entry_index])
        entry = entry_raw * (1 + slippage) if direction == "long" else entry_raw * (1 - slippage)
        stop = row.get("stop", pd.NA)
        target = row.get("target", pd.NA)
        exit_index = min(entry_index + max_hold, len(data) - 1)
        exit_raw = float(data["close"].iloc[exit_index])
        reason = "time_exit"
        for scan in range(entry_index, min(entry_index + max_hold, len(data) - 1) + 1):
            bar = data.iloc[scan]
            if pd.notna(stop):
                if direction == "long" and bar["low"] <= float(stop):
                    exit_index = scan
                    exit_raw = float(stop)
                    reason = "stop"
                    break
                if direction == "short" and bar["high"] >= float(stop):
                    exit_index = scan
                    exit_raw = float(stop)
                    reason = "stop"
                    break
            if pd.notna(target):
                if direction == "long" and bar["high"] >= float(target):
                    exit_index = scan
                    exit_raw = float(target)
                    reason = "target"
                    break
                if direction == "short" and bar["low"] <= float(target):
                    exit_index = scan
                    exit_raw = float(target)
                    reason = "target"
                    break
            if bool(signal.iloc[scan].get("exit_long", False)) and direction == "long":
                exit_index = scan
                exit_raw = float(bar["close"])
                reason = "rule_exit"
                break
            if bool(signal.iloc[scan].get("exit_short", False)) and direction == "short":
                exit_index = scan
                exit_raw = float(bar["close"])
                reason = "rule_exit"
                break
        exit_price = exit_raw * (1 - slippage) if direction == "long" else exit_raw * (1 + slippage)
        gross = exit_price / entry - 1 if direction == "long" else entry / exit_price - 1
        net = gross - 2 * commission
        before = equity
        equity *= 1 + net
        trades.append(
            {
                "asset": asset,
                "timeframe": timeframe,
                "parameter_set": parameter_set,
                "direction": direction,
                "entry_timestamp": data["timestamp"].iloc[entry_index],
                "exit_timestamp": data["timestamp"].iloc[exit_index],
                "entry_price": entry,
                "exit_price": exit_price,
                "gross_return_pct": gross * 100,
                "net_return_pct": net * 100,
                "holding_bars": max(1, exit_index - entry_index + 1),
                "exit_reason": reason,
                "equity_before": before,
                "equity_after": equity,
            }
        )
        equity_rows.append({"timestamp": data["timestamp"].iloc[exit_index], "equity": equity})
        index = exit_index + 1
    trade_frame = pd.DataFrame(trades)
    equity_curve = pd.DataFrame(equity_rows)
    return summarize_trades(asset, timeframe, parameter_set, trade_frame, equity_curve, data), trade_frame, equity_curve
