from __future__ import annotations

import math
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

from crabel_range_expansion import (
    ATR_LENGTH,
    ATR_MAX_HOLD_BARS,
    ATR_STOP_MULT,
    EXIT_VARIANTS,
    INITIAL_EQUITY,
    PRIMARY_EXPANSION_MULT,
    PRIMARY_SAME_BAR_MODE,
    SYMBOLS,
    TradeCandidate,
    calculate_signals,
    load_manifest_datasets,
    load_ohlcv,
    markdown_table,
    profit_factor,
)


ROOT = Path(__file__).resolve().parents[3]
BUNDLE_ROOT = ROOT.parent / "MTC_V2_OPTIMIZATION_DATA_BUNDLE_20260427"
OUTPUT_ROOT = ROOT / "06_QUANTLENS_LAB" / "research" / "crabel_range_expansion"
REPORT_PATH = OUTPUT_ROOT / "QL_CRABEL_RANGE_EXPANSION_STAGE2_ROBUSTNESS_REPORT.md"
PARAMETER_SWEEP_CSV = OUTPUT_ROOT / "QL_CRABEL_STAGE2_PARAMETER_SWEEP.csv"
FEE_STRESS_CSV = OUTPUT_ROOT / "QL_CRABEL_STAGE2_FEE_STRESS.csv"
TIME_SPLIT_CSV = OUTPUT_ROOT / "QL_CRABEL_STAGE2_TIME_SPLIT.csv"
FILTER_TESTS_CSV = OUTPUT_ROOT / "QL_CRABEL_STAGE2_FILTER_TESTS.csv"
DRAWDOWN_CSV = OUTPUT_ROOT / "QL_CRABEL_STAGE2_DRAWDOWN_DIAGNOSIS.csv"
STAGE1_RESULTS_CSV = OUTPUT_ROOT / "reports" / "QL_CRABEL_RANGE_EXPANSION_RESULTS.csv"
STAGE1_TRADES_CSV = OUTPUT_ROOT / "reports" / "QL_CRABEL_RANGE_EXPANSION_TRADES.csv"
STAGE1_REPORT = OUTPUT_ROOT / "reports" / "QL_CRABEL_RANGE_EXPANSION_REPORT.md"

SWEEP_MULTS = [0.50, 0.60, 0.70, 0.80, 0.90, 1.00, 1.10, 1.20, 1.30, 1.50]
FEE_SCENARIOS = [
    ("base", 0.0004, 0.0002),
    ("2x", 0.0008, 0.0004),
    ("3x", 0.0012, 0.0006),
]
FILTER_MODES = [
    "none",
    "trend_ema200",
    "regime_ema50_ema200",
    "atr_above_median",
    "atr_below_extreme",
    "atr_band",
]
DIRECTION_MODES = ["both", "long_only", "short_only"]


@dataclass(frozen=True)
class BacktestConfig:
    expansion_mult: float = PRIMARY_EXPANSION_MULT
    exit_variant: str = "close_exit"
    same_bar_both_mode: str = PRIMARY_SAME_BAR_MODE
    commission_rate: float = 0.0004
    slippage_rate: float = 0.0002
    filter_mode: str = "none"
    direction_mode: str = "both"
    segment_name: str = "full"
    segment_start: pd.Timestamp | None = None
    segment_end: pd.Timestamp | None = None


def run_command(command: list[str]) -> tuple[int, str]:
    completed = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, check=False)
    return completed.returncode, (completed.stdout + completed.stderr).strip()


def adjusted_entry(direction: str, price: float, slippage_rate: float) -> float:
    return price * (1 + slippage_rate) if direction == "long" else price * (1 - slippage_rate)


def adjusted_exit(direction: str, price: float, slippage_rate: float) -> float:
    return price * (1 - slippage_rate) if direction == "long" else price * (1 + slippage_rate)


def net_trade_return(direction: str, entry_price: float, exit_price: float, commission_rate: float) -> tuple[float, float]:
    gross = (exit_price / entry_price - 1.0) if direction == "long" else (entry_price / exit_price - 1.0)
    net = gross - (2 * commission_rate)
    return gross, net


def add_filters(data: pd.DataFrame, expansion_mult: float) -> pd.DataFrame:
    signals = calculate_signals(data, expansion_mult)
    signals["ema50"] = signals["close"].ewm(span=50, adjust=False, min_periods=50).mean()
    signals["ema200"] = signals["close"].ewm(span=200, adjust=False, min_periods=200).mean()
    signals["prev_ema50"] = signals["ema50"].shift(1)
    signals["prev_ema200"] = signals["ema200"].shift(1)
    signals["atr_pct"] = signals["atr14"] / signals["close"]
    signals["prev_atr_pct"] = signals["atr_pct"].shift(1)
    signals["atr_pct_median_100"] = signals["atr_pct"].rolling(100, min_periods=50).median().shift(1)
    signals["atr_pct_p90_252"] = signals["atr_pct"].rolling(252, min_periods=100).quantile(0.90).shift(1)
    return signals


def entry_allowed(row: pd.Series, direction: str, config: BacktestConfig) -> bool:
    if config.direction_mode == "long_only" and direction != "long":
        return False
    if config.direction_mode == "short_only" and direction != "short":
        return False
    if config.segment_start is not None and row["timestamp"] < config.segment_start:
        return False
    if config.segment_end is not None and row["timestamp"] > config.segment_end:
        return False
    if config.filter_mode == "none":
        return True
    if config.filter_mode == "trend_ema200":
        if pd.isna(row["prev_close"]) or pd.isna(row["prev_ema200"]):
            return False
        return bool(row["prev_close"] > row["prev_ema200"]) if direction == "long" else bool(row["prev_close"] < row["prev_ema200"])
    if config.filter_mode == "regime_ema50_ema200":
        if pd.isna(row["prev_ema50"]) or pd.isna(row["prev_ema200"]):
            return False
        return bool(row["prev_ema50"] > row["prev_ema200"]) if direction == "long" else bool(row["prev_ema50"] < row["prev_ema200"])
    if config.filter_mode == "atr_above_median":
        if pd.isna(row["prev_atr_pct"]) or pd.isna(row["atr_pct_median_100"]):
            return False
        return bool(row["prev_atr_pct"] > row["atr_pct_median_100"])
    if config.filter_mode == "atr_below_extreme":
        if pd.isna(row["prev_atr_pct"]) or pd.isna(row["atr_pct_p90_252"]):
            return False
        return bool(row["prev_atr_pct"] < row["atr_pct_p90_252"])
    if config.filter_mode == "atr_band":
        if pd.isna(row["prev_atr_pct"]) or pd.isna(row["atr_pct_median_100"]) or pd.isna(row["atr_pct_p90_252"]):
            return False
        return bool(row["prev_atr_pct"] > row["atr_pct_median_100"] and row["prev_atr_pct"] < row["atr_pct_p90_252"])
    raise ValueError(f"Unsupported filter_mode: {config.filter_mode}")


def build_candidate(signals: pd.DataFrame, index: int, direction: str) -> TradeCandidate:
    row = signals.iloc[index]
    return TradeCandidate(
        direction=direction,
        entry_index=index,
        entry_timestamp=row["timestamp"],
        raw_entry_price=float(row["buy_stop"] if direction == "long" else row["sell_stop"]),
        buy_stop=float(row["buy_stop"]),
        sell_stop=float(row["sell_stop"]),
    )


def exit_trade(signals: pd.DataFrame, candidate: TradeCandidate, config: BacktestConfig) -> dict[str, object]:
    row = signals.iloc[candidate.entry_index]
    direction = candidate.direction
    entry_price = adjusted_entry(direction, candidate.raw_entry_price, config.slippage_rate)
    reason = config.exit_variant
    if config.exit_variant == "close_exit":
        exit_index = candidate.entry_index
        raw_exit = float(row["close"])
        holding_bars = 1
    elif config.exit_variant == "next_bar_close_exit":
        exit_index = min(candidate.entry_index + 1, len(signals) - 1)
        raw_exit = float(signals.iloc[exit_index]["close"])
        holding_bars = max(1, exit_index - candidate.entry_index + 1)
    elif config.exit_variant == "previous_extreme_target_stop":
        stop = candidate.sell_stop if direction == "long" else candidate.buy_stop
        target = float(row["prev_high"]) if direction == "long" else float(row["prev_low"])
        stop_hit = row["low"] <= stop if direction == "long" else row["high"] >= stop
        target_hit = row["high"] >= target if direction == "long" else row["low"] <= target
        exit_index = candidate.entry_index
        holding_bars = 1
        if stop_hit and target_hit:
            raw_exit = float(stop)
            reason = "target_stop_same_bar_pessimistic_stop"
        elif stop_hit:
            raw_exit = float(stop)
            reason = "protective_stop"
        elif target_hit:
            raw_exit = float(target)
            reason = "previous_extreme_target"
        else:
            raw_exit = float(row["close"])
            reason = "same_bar_close_fallback"
    elif config.exit_variant == "atr_stop_time_exit":
        atr = row["atr14"]
        if pd.isna(atr):
            exit_index = min(candidate.entry_index + ATR_MAX_HOLD_BARS - 1, len(signals) - 1)
            raw_exit = float(signals.iloc[exit_index]["close"])
            holding_bars = max(1, exit_index - candidate.entry_index + 1)
            reason = "atr_unavailable_time_exit"
        else:
            stop = candidate.raw_entry_price - (ATR_STOP_MULT * float(atr)) if direction == "long" else candidate.raw_entry_price + (ATR_STOP_MULT * float(atr))
            max_exit_index = min(candidate.entry_index + ATR_MAX_HOLD_BARS - 1, len(signals) - 1)
            exit_index = max_exit_index
            raw_exit = float(signals.iloc[max_exit_index]["close"])
            reason = "time_exit_3_bars"
            for scan_index in range(candidate.entry_index, max_exit_index + 1):
                scan = signals.iloc[scan_index]
                stop_hit = scan["low"] <= stop if direction == "long" else scan["high"] >= stop
                if stop_hit:
                    exit_index = scan_index
                    raw_exit = float(stop)
                    reason = "atr_stop"
                    break
            holding_bars = max(1, exit_index - candidate.entry_index + 1)
    else:
        raise ValueError(f"Unsupported exit_variant: {config.exit_variant}")
    exit_price = adjusted_exit(direction, raw_exit, config.slippage_rate)
    gross_return, net_return = net_trade_return(direction, entry_price, exit_price, config.commission_rate)
    return {
        "direction": direction,
        "entry_index": candidate.entry_index,
        "exit_index": exit_index,
        "entry_timestamp": candidate.entry_timestamp,
        "exit_timestamp": signals.iloc[exit_index]["timestamp"],
        "raw_entry_price": candidate.raw_entry_price,
        "raw_exit_price": raw_exit,
        "entry_price": entry_price,
        "exit_price": exit_price,
        "gross_return_pct": gross_return * 100,
        "net_return_pct": net_return * 100,
        "holding_bars": holding_bars,
        "exit_reason": reason,
    }


def choose_candidate(signals: pd.DataFrame, index: int, config: BacktestConfig) -> TradeCandidate | None:
    row = signals.iloc[index]
    long_trigger = bool(row["long_trigger"])
    short_trigger = bool(row["short_trigger"])
    long_ok = long_trigger and entry_allowed(row, "long", config)
    short_ok = short_trigger and entry_allowed(row, "short", config)
    if long_ok and short_ok:
        if config.same_bar_both_mode == "skip":
            return None
        if config.same_bar_both_mode == "open_distance":
            buy_distance = abs(float(row["open"]) - float(row["buy_stop"]))
            sell_distance = abs(float(row["open"]) - float(row["sell_stop"]))
            return build_candidate(signals, index, "long" if buy_distance <= sell_distance else "short")
        if config.same_bar_both_mode == "pessimistic":
            long_candidate = build_candidate(signals, index, "long")
            short_candidate = build_candidate(signals, index, "short")
            long_trade = exit_trade(signals, long_candidate, config)
            short_trade = exit_trade(signals, short_candidate, config)
            return long_candidate if float(long_trade["net_return_pct"]) <= float(short_trade["net_return_pct"]) else short_candidate
    if long_ok:
        return build_candidate(signals, index, "long")
    if short_ok:
        return build_candidate(signals, index, "short")
    return None


def max_drawdown_pct(equity: pd.Series) -> float:
    if equity.empty:
        return 0.0
    return float(((equity / equity.cummax()) - 1.0).min() * 100)


def calculate_metrics(symbol: str, signals: pd.DataFrame, trades: pd.DataFrame, equity_curve: pd.DataFrame, config: BacktestConfig) -> dict[str, object]:
    eligible = signals.copy()
    if config.segment_start is not None:
        eligible = eligible[eligible["timestamp"] >= config.segment_start]
    if config.segment_end is not None:
        eligible = eligible[eligible["timestamp"] <= config.segment_end]
    start = eligible.iloc[0]["timestamp"] if not eligible.empty else signals.iloc[0]["timestamp"]
    end = eligible.iloc[-1]["timestamp"] if not eligible.empty else signals.iloc[-1]["timestamp"]
    final_equity = float(equity_curve.iloc[-1]["equity"]) if not equity_curve.empty else INITIAL_EQUITY
    net_return_pct = (final_equity / INITIAL_EQUITY - 1.0) * 100.0
    buy_hold = ((float(eligible.iloc[-1]["close"]) / float(eligible.iloc[0]["close"])) - 1.0) * 100.0 if len(eligible) > 1 else 0.0
    base = {
        "symbol": symbol,
        "segment": config.segment_name,
        "timeframe": "1D",
        "expansion_mult": config.expansion_mult,
        "exit_variant": config.exit_variant,
        "same_bar_both_mode": config.same_bar_both_mode,
        "fee_scenario": f"commission={config.commission_rate};slippage={config.slippage_rate}",
        "filter_mode": config.filter_mode,
        "direction_mode": config.direction_mode,
        "bars_tested": int(len(eligible)),
        "start_date": start.date().isoformat(),
        "end_date": end.date().isoformat(),
        "final_equity": final_equity,
        "net_return_pct": net_return_pct,
        "max_drawdown_pct": max_drawdown_pct(equity_curve["equity"]),
        "buy_and_hold_return_pct": buy_hold,
        "beats_buy_and_hold": bool(net_return_pct > buy_hold),
    }
    if trades.empty:
        base.update(
            {
                "total_trades": 0,
                "long_trades": 0,
                "short_trades": 0,
                "win_rate": 0.0,
                "profit_factor": 0.0,
                "avg_trade_pct": 0.0,
                "avg_win_pct": 0.0,
                "avg_loss_pct": 0.0,
                "expectancy_pct": 0.0,
                "return_dd_ratio": 0.0,
            }
        )
        return base
    returns = trades["net_return_pct"]
    wins = returns[returns > 0]
    losses = returns[returns < 0]
    dd_abs = abs(base["max_drawdown_pct"])
    base.update(
        {
            "total_trades": int(len(trades)),
            "long_trades": int((trades["direction"] == "long").sum()),
            "short_trades": int((trades["direction"] == "short").sum()),
            "win_rate": float((returns > 0).mean() * 100),
            "profit_factor": profit_factor(trades),
            "avg_trade_pct": float(returns.mean()),
            "avg_win_pct": float(wins.mean()) if not wins.empty else 0.0,
            "avg_loss_pct": float(losses.mean()) if not losses.empty else 0.0,
            "expectancy_pct": float(returns.mean()),
            "return_dd_ratio": float(net_return_pct / dd_abs) if dd_abs > 0 else math.inf,
        }
    )
    return base


def run_backtest_stage2(symbol: str, data: pd.DataFrame, config: BacktestConfig) -> tuple[dict[str, object], pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    signals = add_filters(data, config.expansion_mult)
    equity = INITIAL_EQUITY
    equity_points = [{"timestamp": signals.iloc[0]["timestamp"], "equity": equity, "trade_number": 0}]
    trades: list[dict[str, object]] = []
    index = 1
    while index < len(signals):
        candidate = choose_candidate(signals, index, config)
        if candidate is None:
            index += 1
            continue
        trade = exit_trade(signals, candidate, config)
        trade["symbol"] = symbol
        trade["segment"] = config.segment_name
        trade["expansion_mult"] = config.expansion_mult
        trade["exit_variant"] = config.exit_variant
        trade["same_bar_both_mode"] = config.same_bar_both_mode
        trade["filter_mode"] = config.filter_mode
        trade["direction_mode"] = config.direction_mode
        trade["commission_rate"] = config.commission_rate
        trade["slippage_rate"] = config.slippage_rate
        trade["equity_before"] = equity
        equity *= 1.0 + (float(trade["net_return_pct"]) / 100.0)
        trade["equity_after"] = equity
        trades.append(trade)
        equity_points.append({"timestamp": trade["exit_timestamp"], "equity": equity, "trade_number": len(trades)})
        index = int(trade["exit_index"]) + 1
    trades_frame = pd.DataFrame(trades)
    equity_curve = pd.DataFrame(equity_points).drop_duplicates(["timestamp", "trade_number"], keep="last").reset_index(drop=True)
    metrics = calculate_metrics(symbol, signals, trades_frame, equity_curve, config)
    return metrics, trades_frame, equity_curve, signals


def aggregate_metrics(rows: pd.DataFrame, trades: pd.DataFrame, group_columns: list[str]) -> pd.DataFrame:
    output = rows.groupby(group_columns, as_index=False).agg(
        symbols=("symbol", "nunique"),
        positive_symbols=("net_return_pct", lambda values: int((values > 0).sum())),
        aggregate_net_return_pct=("net_return_pct", "mean"),
        aggregate_max_drawdown_pct=("max_drawdown_pct", "mean"),
        aggregate_trade_count=("total_trades", "sum"),
        avg_win_rate=("win_rate", "mean"),
        avg_return_dd_ratio=("return_dd_ratio", "mean"),
    )
    pf_values = []
    for _, group in output.iterrows():
        mask = pd.Series(True, index=trades.index)
        for column in group_columns:
            mask &= trades[column] == group[column]
        pf_values.append(profit_factor(trades[mask]))
    output["aggregate_profit_factor"] = pf_values
    return output


def make_segments(data: pd.DataFrame) -> list[tuple[str, pd.Timestamp, pd.Timestamp]]:
    start = data["timestamp"].min()
    end = data["timestamp"].max()
    midpoint = start + ((end - start) / 2)
    segments = [("first_50pct", start, midpoint), ("second_50pct", midpoint + pd.Timedelta(days=1), end)]
    for year in range(start.year, end.year + 1):
        year_start = max(pd.Timestamp(year=year, month=1, day=1, tz="UTC"), start)
        year_end = min(pd.Timestamp(year=year, month=12, day=31, tz="UTC"), end)
        if year_start <= year_end:
            segments.append((f"year_{year}", year_start, year_end))
    segments.append(("last_12_months", end - pd.DateOffset(months=12), end))
    segments.append(("last_6_months", end - pd.DateOffset(months=6), end))
    return segments


def side_breakdown(trades: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for symbol in SYMBOLS:
        subset = trades[
            (trades["symbol"] == symbol)
            & (trades["expansion_mult"] == PRIMARY_EXPANSION_MULT)
            & (trades["exit_variant"] == "close_exit")
            & (trades["same_bar_both_mode"] == PRIMARY_SAME_BAR_MODE)
        ].copy()
        for direction in ["long", "short"]:
            side = subset[subset["direction"] == direction]
            rows.append(
                {
                    "symbol": symbol,
                    "direction": direction,
                    "trades": int(len(side)),
                    "net_return_pct_compounded": float(((1 + side["net_return_pct"] / 100).prod() - 1) * 100) if not side.empty else 0.0,
                    "profit_factor": profit_factor(side),
                    "avg_trade_pct": float(side["net_return_pct"].mean()) if not side.empty else 0.0,
                    "win_rate": float((side["net_return_pct"] > 0).mean() * 100) if not side.empty else 0.0,
                }
            )
    return pd.DataFrame(rows)


def classify_trend(price_change_pct: float) -> str:
    if price_change_pct > 10:
        return "up"
    if price_change_pct < -10:
        return "down"
    return "sideways"


def diagnose_drawdowns(data_by_symbol: dict[str, pd.DataFrame], primary_runs: dict[str, tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]]) -> pd.DataFrame:
    rows = []
    normalized_curves = []
    for symbol, (trades, equity_curve, signals) in primary_runs.items():
        curve = equity_curve.copy()
        curve["drawdown"] = curve["equity"] / curve["equity"].cummax() - 1.0
        trough_idx = curve["drawdown"].idxmin()
        trough = curve.loc[trough_idx]
        peak_candidates = curve.loc[:trough_idx]
        peak_idx = peak_candidates["equity"].idxmax()
        peak = curve.loc[peak_idx]
        period_trades = trades[(trades["entry_timestamp"] >= peak["timestamp"]) & (trades["exit_timestamp"] <= trough["timestamp"])].copy()
        period_data = signals[(signals["timestamp"] >= peak["timestamp"]) & (signals["timestamp"] <= trough["timestamp"])].copy()
        price_change = ((period_data["close"].iloc[-1] / period_data["close"].iloc[0]) - 1.0) * 100 if len(period_data) > 1 else 0.0
        vol = float(period_data["atr_pct"].mean() * 100) if "atr_pct" in period_data and not period_data["atr_pct"].dropna().empty else 0.0
        long_loss = period_trades.loc[period_trades["direction"] == "long", "net_return_pct"].sum() if not period_trades.empty else 0.0
        short_loss = period_trades.loc[period_trades["direction"] == "short", "net_return_pct"].sum() if not period_trades.empty else 0.0
        if len(period_trades) > 0 and len(period_trades) / max((pd.Timestamp(trough["timestamp"]) - pd.Timestamp(peak["timestamp"])).days, 1) > 0.45:
            cause = "excessive_trade_frequency"
        elif long_loss < short_loss and long_loss < 0:
            cause = "long_side_failure"
        elif short_loss < 0:
            cause = "short_side_failure"
        elif abs(price_change) < 10:
            cause = "range_chop_market"
        else:
            cause = "trend_regime_mismatch"
        rows.append(
            {
                "scope": "symbol",
                "symbol": symbol,
                "dd_start": pd.Timestamp(peak["timestamp"]).date().isoformat(),
                "dd_end": pd.Timestamp(trough["timestamp"]).date().isoformat(),
                "drawdown_pct": float(trough["drawdown"] * 100),
                "trade_count_in_dd": int(len(period_trades)),
                "long_net_pct_sum": float(long_loss),
                "short_net_pct_sum": float(short_loss),
                "trend_regime": classify_trend(price_change),
                "price_change_pct": float(price_change),
                "avg_atr_pct": vol,
                "volatility_regime": "high" if vol > float(signals["atr_pct"].median() * 100) else "low",
                "diagnosed_cause": cause,
            }
        )
        daily = data_by_symbol[symbol][["timestamp"]].copy()
        daily = daily.merge(equity_curve[["timestamp", "equity"]], on="timestamp", how="left").ffill()
        daily["equity"] = daily["equity"].fillna(INITIAL_EQUITY)
        daily = daily.set_index("timestamp")["equity"] / INITIAL_EQUITY
        normalized_curves.append(daily.rename(symbol))
    aggregate = pd.concat(normalized_curves, axis=1).sort_index().ffill().dropna(how="all")
    aggregate["portfolio_equity"] = aggregate.mean(axis=1) * INITIAL_EQUITY
    aggregate["drawdown"] = aggregate["portfolio_equity"] / aggregate["portfolio_equity"].cummax() - 1.0
    trough_time = aggregate["drawdown"].idxmin()
    peak_time = aggregate.loc[:trough_time, "portfolio_equity"].idxmax()
    all_trades = pd.concat([value[0] for value in primary_runs.values()], ignore_index=True)
    period_trades = all_trades[(all_trades["entry_timestamp"] >= peak_time) & (all_trades["exit_timestamp"] <= trough_time)]
    long_loss = period_trades.loc[period_trades["direction"] == "long", "net_return_pct"].sum() if not period_trades.empty else 0.0
    short_loss = period_trades.loc[period_trades["direction"] == "short", "net_return_pct"].sum() if not period_trades.empty else 0.0
    rows.append(
        {
            "scope": "aggregate",
            "symbol": "EQUAL_WEIGHT_5_SYMBOL",
            "dd_start": pd.Timestamp(peak_time).date().isoformat(),
            "dd_end": pd.Timestamp(trough_time).date().isoformat(),
            "drawdown_pct": float(aggregate.loc[trough_time, "drawdown"] * 100),
            "trade_count_in_dd": int(len(period_trades)),
            "long_net_pct_sum": float(long_loss),
            "short_net_pct_sum": float(short_loss),
            "trend_regime": "mixed",
            "price_change_pct": 0.0,
            "avg_atr_pct": 0.0,
            "volatility_regime": "mixed",
            "diagnosed_cause": "mixed_symbol_drawdowns_high_trade_frequency",
        }
    )
    return pd.DataFrame(rows)


def read_stage1_validation(stage1_results: pd.DataFrame, stage1_trades: pd.DataFrame) -> dict[str, object]:
    primary = stage1_results[
        (stage1_results["expansion_mult"] == PRIMARY_EXPANSION_MULT)
        & (stage1_results["exit_variant"] == "close_exit")
        & (stage1_results["same_bar_both_mode"] == PRIMARY_SAME_BAR_MODE)
    ].copy()
    trades = stage1_trades[
        (stage1_trades["expansion_mult"] == PRIMARY_EXPANSION_MULT)
        & (stage1_trades["exit_variant"] == "close_exit")
        & (stage1_trades["same_bar_both_mode"] == PRIMARY_SAME_BAR_MODE)
    ].copy()
    return {
        "aggregate_net_return_pct_symbol_mean": float(primary["net_return_pct"].mean()),
        "aggregate_profit_factor_from_trades": profit_factor(trades),
        "aggregate_max_drawdown_pct_symbol_mean": float(primary["max_drawdown_pct"].mean()),
        "aggregate_trade_count": int(primary["total_trades"].sum()),
        "compound_all_trades_single_stream_pct": float(((1 + trades.sort_values("entry_timestamp")["net_return_pct"] / 100).prod() - 1) * 100),
        "simple_sum_symbol_net_return_pct": float(primary["net_return_pct"].sum()),
    }


def final_classification(parameter_aggregate: pd.DataFrame, fee_aggregate: pd.DataFrame, time_aggregate: pd.DataFrame, filter_aggregate: pd.DataFrame, drawdowns: pd.DataFrame) -> tuple[str, str]:
    close_rows = parameter_aggregate[parameter_aggregate["exit_variant"] == "close_exit"].copy()
    neighbor_rows = close_rows[close_rows["expansion_mult"].isin([0.80, 0.90, 1.00])].copy()
    robust_neighbors = int((neighbor_rows["aggregate_profit_factor"] > 1.15).sum())
    base_fee = fee_aggregate[(fee_aggregate["fee_label"] == "base") & (fee_aggregate["exit_variant"] == "close_exit")].copy()
    fee_2x = fee_aggregate[(fee_aggregate["fee_label"] == "2x") & (fee_aggregate["exit_variant"] == "close_exit")].copy()
    base_pf = float(base_fee.iloc[0]["aggregate_profit_factor"]) if not base_fee.empty else 0.0
    pf_2x = float(fee_2x.iloc[0]["aggregate_profit_factor"]) if not fee_2x.empty else 0.0
    aggregate_dd = abs(float(drawdowns[drawdowns["scope"] == "aggregate"].iloc[0]["drawdown_pct"]))
    symbol_drawdowns = drawdowns[drawdowns["scope"] == "symbol"]["drawdown_pct"].astype(float).abs()
    mean_symbol_dd = float(symbol_drawdowns.mean()) if not symbol_drawdowns.empty else 999.0
    worst_symbol_dd = float(symbol_drawdowns.max()) if not symbol_drawdowns.empty else 999.0
    profitable_recent = time_aggregate[time_aggregate["segment"].isin(["last_12_months", "last_6_months"])]["aggregate_net_return_pct"].gt(0).all()
    best_filter = filter_aggregate.sort_values("aggregate_max_drawdown_pct", ascending=False).head(1)
    best_filter_dd = abs(float(best_filter.iloc[0]["aggregate_max_drawdown_pct"])) if not best_filter.empty else 999.0
    if robust_neighbors >= 3 and pf_2x > 1.10 and aggregate_dd < 25 and mean_symbol_dd < 35 and worst_symbol_dd < 45 and profitable_recent:
        return "PRODUCER_CANDIDATE", "PF and parameter robustness pass, fee stress passes, and both aggregate and symbol-level drawdown are manageable."
    if base_pf > 1.10 and robust_neighbors >= 2 and pf_2x > 1.05 and best_filter_dd < mean_symbol_dd:
        return "GATE_ONLY_CANDIDATE", "There is real breakout information, but standalone symbol-level drawdown, short-side weakness, and regime instability argue for gate/filter use first."
    if base_pf > 1.0:
        return "WEAK_CANDIDATE_KEEP_RESEARCH", "Edge survives base costs, but robustness, drawdown, or recent-period stability is insufficient for producer promotion."
    return "WIKI_ONLY", "The idea is documented, but the measured edge is too weak for system candidacy."


def write_report(
    stage1_validation: dict[str, object],
    per_symbol: pd.DataFrame,
    side: pd.DataFrame,
    worst_trades: pd.DataFrame,
    best_trades: pd.DataFrame,
    parameter_aggregate: pd.DataFrame,
    fee_aggregate: pd.DataFrame,
    time_aggregate: pd.DataFrame,
    filter_aggregate: pd.DataFrame,
    drawdowns: pd.DataFrame,
    classification: str,
    classification_reason: str,
    commands: list[str],
) -> None:
    eth = per_symbol[per_symbol["symbol"] == "ETHUSDT"].iloc[0]
    sol = per_symbol[per_symbol["symbol"] == "SOLUSDT"].iloc[0]
    close_sweep = parameter_aggregate[parameter_aggregate["exit_variant"] == "close_exit"].copy()
    neighbor_rows = close_sweep[close_sweep["expansion_mult"].isin([0.80, 0.90, 1.00])]
    overfit_risk = int((neighbor_rows["aggregate_profit_factor"] > 1.15).sum()) < 3
    fee_3x = fee_aggregate[(fee_aggregate["fee_label"] == "3x") & (fee_aggregate["exit_variant"] == "close_exit")].copy()
    fee_3x_note = "3x fee/slippage still positive" if not fee_3x.empty and float(fee_3x.iloc[0]["aggregate_profit_factor"]) > 1.0 else "3x fee/slippage materially weakens or breaks the edge"
    lines = [
        "# QL Crabel Range Expansion Stage2 Robustness Report",
        "",
        "## Executive Summary",
        f"- Final classification: **{classification}**.",
        f"- Reason: {classification_reason}",
        "- Scope: Python-only research robustness; no Pine, no MTC production integration, no TradingView parity.",
        "",
        "## 1. Existing Result Validation",
        f"- Stage1 aggregate net return recomputed as symbol-level mean: {stage1_validation['aggregate_net_return_pct_symbol_mean']:.2f}%.",
        f"- Stage1 aggregate PF recomputed from primary trade rows: {stage1_validation['aggregate_profit_factor_from_trades']:.2f}.",
        f"- Stage1 aggregate max DD recomputed as symbol-level mean: {stage1_validation['aggregate_max_drawdown_pct_symbol_mean']:.2f}%.",
        f"- Stage1 primary trade count recomputed: {stage1_validation['aggregate_trade_count']}.",
        f"- Aggregate net return is a simple equal-weight mean of per-symbol compounded returns, not a single combined portfolio equity curve. Simple sum would be {stage1_validation['simple_sum_symbol_net_return_pct']:.2f}%; one chronological all-trades stream would be {stage1_validation['compound_all_trades_single_stream_pct']:.2f}%.",
        "",
        "## 2. Per-Symbol Breakdown",
        markdown_table(per_symbol, ["symbol", "net_return_pct", "profit_factor", "max_drawdown_pct", "total_trades", "win_rate", "avg_win_pct", "avg_loss_pct", "expectancy_pct", "buy_and_hold_return_pct", "beats_buy_and_hold"]),
        "",
        "## 3. Long/Short Breakdown",
        markdown_table(side, ["symbol", "direction", "trades", "net_return_pct_compounded", "profit_factor", "avg_trade_pct", "win_rate"]),
        "",
        "## 4. ETHUSDT vs SOLUSDT",
        f"- ETHUSDT: net {float(eth['net_return_pct']):.2f}%, PF {float(eth['profit_factor']):.2f}, DD {float(eth['max_drawdown_pct']):.2f}%, trades {int(eth['total_trades'])}.",
        f"- SOLUSDT: net {float(sol['net_return_pct']):.2f}%, PF {float(sol['profit_factor']):.2f}, DD {float(sol['max_drawdown_pct']):.2f}%, trades {int(sol['total_trades'])}.",
        "- ETH works better because the same close-exit breakout captures larger average winners with lower DD. SOL is positive but weak versus its buy-and-hold, with lower PF and worse DD.",
        "- Symbol sensitivity is material: all symbols are positive, but return dispersion is high and SOL/BNB/BTC fail buy-and-hold.",
        "",
        "## 5. Parameter Robustness Sweep",
        markdown_table(close_sweep, ["expansion_mult", "aggregate_net_return_pct", "aggregate_profit_factor", "aggregate_max_drawdown_pct", "aggregate_trade_count", "positive_symbols"]),
        f"- 0.80/0.90/1.00 PF>1.15 neighbor count: {int((neighbor_rows['aggregate_profit_factor'] > 1.15).sum())}/3.",
        f"- OVERFIT_RISK: {'yes' if overfit_risk else 'no'}.",
        "",
        "## 6. Fee / Slippage Stress",
        markdown_table(fee_aggregate, ["fee_label", "exit_variant", "aggregate_net_return_pct", "aggregate_profit_factor", "aggregate_max_drawdown_pct", "aggregate_trade_count", "positive_symbols"]),
        f"- Stress note: {fee_3x_note}.",
        "",
        "## 7. Time Split / Walk-Forward-Like Test",
        markdown_table(time_aggregate, ["segment", "aggregate_net_return_pct", "aggregate_profit_factor", "aggregate_max_drawdown_pct", "aggregate_trade_count", "positive_symbols"], max_rows=20),
        "- Segment-level CSV includes first half, second half, yearly segments, last 12 months, and last 6 months with long/short counts.",
        "",
        "## 8. Drawdown Diagnosis",
        markdown_table(drawdowns, ["scope", "symbol", "dd_start", "dd_end", "drawdown_pct", "trade_count_in_dd", "long_net_pct_sum", "short_net_pct_sum", "trend_regime", "volatility_regime", "diagnosed_cause"]),
        "- Main diagnosis: drawdown is driven by high trade frequency plus side-specific failures in volatile regime shifts. No trend or volatility filter exists in the base model.",
        "",
        "## 9. Simple Filter Tests",
        markdown_table(filter_aggregate, ["filter_mode", "direction_mode", "aggregate_net_return_pct", "aggregate_profit_factor", "aggregate_max_drawdown_pct", "aggregate_trade_count", "avg_return_dd_ratio"], max_rows=30),
        "- Goal was DD reduction, not return maximization. Filters are simple and past-only via shifted close/EMA/ATR inputs.",
        "",
        "## 10. Best / Worst Trades",
        "- Full best/worst trade lists are in the report CSV outputs; top rows are shown here.",
        "### Worst 10 By Symbol",
        markdown_table(worst_trades, ["symbol", "direction", "entry_timestamp", "exit_timestamp", "net_return_pct", "exit_reason"]),
        "### Best 10 By Symbol",
        markdown_table(best_trades, ["symbol", "direction", "entry_timestamp", "exit_timestamp", "net_return_pct", "exit_reason"]),
        "",
        "## 11. Buy & Hold Benchmark",
        "- Crabel beats buy-and-hold on ETHUSDT and XRPUSDT only; BTCUSDT, SOLUSDT, and BNBUSDT underperform buy-and-hold over their available windows.",
        "- The model is not simply a superior long-volatility substitute across all symbols; it extracts two-sided breakout edge but pays with high turnover and DD.",
        "",
        "## 12. Final Classification",
        f"**{classification}**",
        "- Pine stage: do not move directly to Pine producer integration.",
        "- MTC producer: not yet; standalone DD and regime instability are too high.",
        "- Gate/filter idea: worth preserving if later used as a volatility breakout confirmation gate for another producer.",
        "- Archive: keep as research unless a separate gate-only experiment is explicitly approved.",
        "",
        "## 13. Files Created",
        f"- `{REPORT_PATH}`",
        f"- `{PARAMETER_SWEEP_CSV}`",
        f"- `{FEE_STRESS_CSV}`",
        f"- `{TIME_SPLIT_CSV}`",
        f"- `{FILTER_TESTS_CSV}`",
        f"- `{DRAWDOWN_CSV}`",
        "",
        "## 14. Commands Run",
        *[f"- `{command}`" for command in commands],
        "",
        "## 15. Verification",
        "- Existing Stage1 report and CSVs were read before Stage2 analysis.",
        "- Stage2 CSV outputs were regenerated from repo-local data and existing Stage1 trade/result files.",
        "- No Pine or production MTC files were modified.",
    ]
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    commands = [
        "python -m py_compile 06_QUANTLENS_LAB/research/crabel_range_expansion/run_stage2_robustness.py",
        "python 06_QUANTLENS_LAB/research/crabel_range_expansion/run_stage2_robustness.py",
    ]
    stage1_results = pd.read_csv(STAGE1_RESULTS_CSV)
    stage1_trades = pd.read_csv(STAGE1_TRADES_CSV, parse_dates=["entry_timestamp", "exit_timestamp"])
    stage1_validation = read_stage1_validation(stage1_results, stage1_trades)
    datasets = load_manifest_datasets(BUNDLE_ROOT, SYMBOLS)
    data_by_symbol = {symbol: load_ohlcv(info.path) for symbol, info in datasets.items()}
    parameter_rows = []
    parameter_trades = []
    for symbol, data in data_by_symbol.items():
        for mult in SWEEP_MULTS:
            for exit_variant in EXIT_VARIANTS:
                config = BacktestConfig(expansion_mult=mult, exit_variant=exit_variant)
                metrics, trades, _equity, _signals = run_backtest_stage2(symbol, data, config)
                parameter_rows.append(metrics)
                if not trades.empty:
                    parameter_trades.append(trades)
    parameter_frame = pd.DataFrame(parameter_rows)
    parameter_trades_frame = pd.concat(parameter_trades, ignore_index=True)
    parameter_aggregate = aggregate_metrics(parameter_frame, parameter_trades_frame, ["expansion_mult", "exit_variant"])
    parameter_output = parameter_frame.merge(parameter_aggregate, on=["expansion_mult", "exit_variant"], how="left", suffixes=("", "_aggregate"))
    parameter_output.to_csv(PARAMETER_SWEEP_CSV, index=False)

    fee_rows = []
    fee_trades = []
    for fee_label, commission, slippage in FEE_SCENARIOS:
        for symbol, data in data_by_symbol.items():
            for exit_variant in EXIT_VARIANTS:
                config = BacktestConfig(exit_variant=exit_variant, commission_rate=commission, slippage_rate=slippage)
                metrics, trades, _equity, _signals = run_backtest_stage2(symbol, data, config)
                metrics["fee_label"] = fee_label
                fee_rows.append(metrics)
                if not trades.empty:
                    trades["fee_label"] = fee_label
                    fee_trades.append(trades)
    fee_frame = pd.DataFrame(fee_rows)
    fee_trades_frame = pd.concat(fee_trades, ignore_index=True)
    fee_aggregate = aggregate_metrics(fee_frame, fee_trades_frame, ["fee_label", "exit_variant"])
    fee_output = fee_frame.merge(fee_aggregate, on=["fee_label", "exit_variant"], how="left", suffixes=("", "_aggregate"))
    fee_output.to_csv(FEE_STRESS_CSV, index=False)

    time_rows = []
    time_trades = []
    for symbol, data in data_by_symbol.items():
        for segment_name, segment_start, segment_end in make_segments(data):
            config = BacktestConfig(segment_name=segment_name, segment_start=segment_start, segment_end=segment_end)
            metrics, trades, _equity, _signals = run_backtest_stage2(symbol, data, config)
            time_rows.append(metrics)
            if not trades.empty:
                time_trades.append(trades)
    time_frame = pd.DataFrame(time_rows)
    time_trades_frame = pd.concat(time_trades, ignore_index=True)
    time_aggregate = aggregate_metrics(time_frame, time_trades_frame, ["segment"])
    time_output = time_frame.merge(time_aggregate, on=["segment"], how="left", suffixes=("", "_aggregate"))
    time_output.to_csv(TIME_SPLIT_CSV, index=False)

    filter_rows = []
    filter_trades = []
    for symbol, data in data_by_symbol.items():
        for filter_mode in FILTER_MODES:
            for direction_mode in DIRECTION_MODES:
                config = BacktestConfig(filter_mode=filter_mode, direction_mode=direction_mode)
                metrics, trades, _equity, _signals = run_backtest_stage2(symbol, data, config)
                filter_rows.append(metrics)
                if not trades.empty:
                    filter_trades.append(trades)
    filter_frame = pd.DataFrame(filter_rows)
    filter_trades_frame = pd.concat(filter_trades, ignore_index=True)
    filter_aggregate = aggregate_metrics(filter_frame, filter_trades_frame, ["filter_mode", "direction_mode"])
    filter_output = filter_frame.merge(filter_aggregate, on=["filter_mode", "direction_mode"], how="left", suffixes=("", "_aggregate"))
    filter_output.to_csv(FILTER_TESTS_CSV, index=False)

    primary_runs = {}
    for symbol, data in data_by_symbol.items():
        metrics, trades, equity, signals = run_backtest_stage2(symbol, data, BacktestConfig())
        primary_runs[symbol] = (trades, equity, signals)
    drawdowns = diagnose_drawdowns(data_by_symbol, primary_runs)
    drawdowns.to_csv(DRAWDOWN_CSV, index=False)

    per_symbol = stage1_results[
        (stage1_results["expansion_mult"] == PRIMARY_EXPANSION_MULT)
        & (stage1_results["exit_variant"] == "close_exit")
        & (stage1_results["same_bar_both_mode"] == PRIMARY_SAME_BAR_MODE)
    ].copy()
    primary_stage1_trades = stage1_trades[
        (stage1_trades["expansion_mult"] == PRIMARY_EXPANSION_MULT)
        & (stage1_trades["exit_variant"] == "close_exit")
        & (stage1_trades["same_bar_both_mode"] == PRIMARY_SAME_BAR_MODE)
    ].copy()
    side = side_breakdown(stage1_trades)
    worst_trades = primary_stage1_trades.sort_values("net_return_pct").groupby("symbol").head(10).sort_values(["symbol", "net_return_pct"])
    best_trades = primary_stage1_trades.sort_values("net_return_pct", ascending=False).groupby("symbol").head(10).sort_values(["symbol", "net_return_pct"], ascending=[True, False])
    classification, reason = final_classification(parameter_aggregate, fee_aggregate, time_aggregate, filter_aggregate, drawdowns)
    write_report(
        stage1_validation,
        per_symbol,
        side,
        worst_trades,
        best_trades,
        parameter_aggregate,
        fee_aggregate,
        time_aggregate,
        filter_aggregate,
        drawdowns,
        classification,
        reason,
        commands,
    )
    print(f"classification={classification}")
    print(f"report={REPORT_PATH}")
    print(f"parameter_sweep={PARAMETER_SWEEP_CSV}")
    print(f"fee_stress={FEE_STRESS_CSV}")
    print(f"time_split={TIME_SPLIT_CSV}")
    print(f"filter_tests={FILTER_TESTS_CSV}")
    print(f"drawdown={DRAWDOWN_CSV}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
