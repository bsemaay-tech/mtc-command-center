from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RiskConfig:
    enable_long: bool = True
    enable_short: bool = True
    fixed_qty: float = 1.0
    time_exit_bars: int = 20
    cost_bps: float = 0.0


def run_visual_debug_trades(signals: list[dict], config: RiskConfig | None = None) -> tuple[list[dict], list[dict]]:
    cfg = config or RiskConfig()
    position = 0
    entry_price = 0.0
    entry_time = ""
    entry_index = -1
    active_stop = None
    trades: list[dict] = []
    equity: list[dict] = []
    realized_points = 0.0

    for i, row in enumerate(signals):
        close = float(row["close"])
        high = float(row["high"])
        low = float(row["low"])
        exit_reason = ""
        if position > 0:
            prior_low = float(signals[i - 1]["low"]) if i > 0 else low
            active_stop = max(active_stop if active_stop is not None else prior_low, prior_low)
            if low <= active_stop:
                exit_reason = "prior_bar_low_trailing_stop"
            elif i - entry_index >= cfg.time_exit_bars:
                exit_reason = "time_exit"
            if exit_reason:
                pnl = (active_stop - entry_price) * cfg.fixed_qty
                realized_points += pnl
                trades.append({"entry_time": entry_time, "exit_time": row["timestamp"], "side": "LONG", "entry_price": entry_price, "exit_price": active_stop, "qty": cfg.fixed_qty, "pnl_points": round(pnl, 6), "exit_reason": exit_reason})
                position = 0
                active_stop = None
        elif position < 0:
            prior_high = float(signals[i - 1]["high"]) if i > 0 else high
            active_stop = min(active_stop if active_stop is not None else prior_high, prior_high)
            if high >= active_stop:
                exit_reason = "prior_bar_high_trailing_stop"
            elif i - entry_index >= cfg.time_exit_bars:
                exit_reason = "time_exit"
            if exit_reason:
                pnl = (entry_price - active_stop) * cfg.fixed_qty
                realized_points += pnl
                trades.append({"entry_time": entry_time, "exit_time": row["timestamp"], "side": "SHORT", "entry_price": entry_price, "exit_price": active_stop, "qty": cfg.fixed_qty, "pnl_points": round(pnl, 6), "exit_reason": exit_reason})
                position = 0
                active_stop = None

        if position == 0 and cfg.enable_long and row["raw_long_pulse"] in (True, "True", "true", "1"):
            position = 1
            entry_price = close
            entry_time = row["timestamp"]
            entry_index = i
            active_stop = float(row["initial_stop_long"] or low)
        elif position == 0 and cfg.enable_short and row["raw_short_pulse"] in (True, "True", "true", "1"):
            position = -1
            entry_price = close
            entry_time = row["timestamp"]
            entry_index = i
            active_stop = float(row["initial_stop_short"] or high)

        unrealized = 0.0
        if position > 0:
            unrealized = (close - entry_price) * cfg.fixed_qty
        elif position < 0:
            unrealized = (entry_price - close) * cfg.fixed_qty
        equity.append({"timestamp": row["timestamp"], "position": position, "active_stop": active_stop if active_stop is not None else "", "realized_points": round(realized_points, 6), "unrealized_points": round(unrealized, 6), "debug_total_points": round(realized_points + unrealized, 6)})

    return trades, equity
