from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd


SYMBOLS = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT", "XRPUSDT"]
EXPANSION_MULTS = [0.50, 0.75, 0.90, 1.00, 1.25]
EXIT_VARIANTS = ["close_exit", "next_bar_close_exit", "previous_extreme_target_stop", "atr_stop_time_exit"]
SAME_BAR_BOTH_MODES = ["skip", "pessimistic", "open_distance"]
PRIMARY_EXPANSION_MULT = 0.90
PRIMARY_SAME_BAR_MODE = "skip"
INITIAL_EQUITY = 10_000.0
COMMISSION_RATE = 0.0004
SLIPPAGE_RATE = 0.0002
ATR_LENGTH = 14
ATR_STOP_MULT = 2.0
ATR_MAX_HOLD_BARS = 3


@dataclass(frozen=True)
class DatasetInfo:
    symbol: str
    dataset_id: str
    path: Path
    sha256: str
    source_type: str
    timeframe: str
    manifest_start: str
    manifest_end: str
    notes: str


@dataclass(frozen=True)
class TradeCandidate:
    direction: str
    entry_index: int
    entry_timestamp: pd.Timestamp
    raw_entry_price: float
    buy_stop: float
    sell_stop: float


def load_manifest_datasets(bundle_root: Path, symbols: Iterable[str]) -> dict[str, DatasetInfo]:
    manifest_path = bundle_root / "DATA_BUNDLE_MANIFEST.json"
    if not manifest_path.exists():
        raise FileNotFoundError(f"Missing manifest: {manifest_path}")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    datasets = manifest["datasets"]
    selected: dict[str, DatasetInfo] = {}
    wanted = set(symbols)
    for item in datasets:
        symbol = str(item.get("symbol", ""))
        timeframe = str(item.get("timeframe_normalized", item.get("timeframe", "")))
        if symbol not in wanted or timeframe.upper() != "1D":
            continue
        normalized_path = bundle_root / str(item["normalized_path"])
        selected[symbol] = DatasetInfo(
            symbol=symbol,
            dataset_id=str(item["dataset_id"]),
            path=normalized_path,
            sha256=str(item.get("sha256_normalized", "")),
            source_type=str(item.get("source_type", "")),
            timeframe="1D",
            manifest_start=str(item.get("start", "")),
            manifest_end=str(item.get("end", "")),
            notes=str(item.get("notes", "")),
        )
    missing = sorted(wanted - set(selected))
    if missing:
        raise FileNotFoundError(f"Missing 1D datasets for symbols: {', '.join(missing)}")
    return selected


def load_ohlcv(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Data file not found: {path}")
    data = pd.read_csv(path)
    rename_map = {}
    lower_to_original = {str(column).strip().lower(): column for column in data.columns}
    timestamp_column = next(
        (lower_to_original[key] for key in ("timestamp", "timestamp_utc", "time", "date", "datetime") if key in lower_to_original),
        None,
    )
    if timestamp_column is None:
        raise ValueError(f"{path} missing timestamp/time/date/datetime column")
    rename_map[timestamp_column] = "timestamp"
    for target in ("open", "high", "low", "close", "volume"):
        if target in lower_to_original:
            rename_map[lower_to_original[target]] = target
    data = data.rename(columns=rename_map)
    required = ["timestamp", "open", "high", "low", "close"]
    missing = [column for column in required if column not in data.columns]
    if missing:
        raise ValueError(f"{path} missing required columns: {', '.join(missing)}")
    if "volume" not in data.columns:
        data["volume"] = 0.0
    data = data[["timestamp", "open", "high", "low", "close", "volume"]].copy()
    if pd.api.types.is_numeric_dtype(data["timestamp"]):
        timestamp = pd.to_datetime(data["timestamp"], unit="s", utc=True)
    else:
        timestamp = pd.to_datetime(data["timestamp"], utc=True)
    data["timestamp"] = timestamp
    for column in ["open", "high", "low", "close", "volume"]:
        data[column] = pd.to_numeric(data[column], errors="coerce")
    data = data.dropna(subset=["timestamp", "open", "high", "low", "close"])
    data = data.sort_values("timestamp").drop_duplicates("timestamp", keep="last").reset_index(drop=True)
    return data


def calculate_signals(data: pd.DataFrame, expansion_mult: float) -> pd.DataFrame:
    signals = data.copy()
    signals["prev_high"] = signals["high"].shift(1)
    signals["prev_low"] = signals["low"].shift(1)
    signals["prev_close"] = signals["close"].shift(1)
    signals["prev_range"] = signals["prev_high"] - signals["prev_low"]
    signals["expansion"] = signals["prev_range"] * expansion_mult
    signals["buy_stop"] = signals["prev_close"] + signals["expansion"]
    signals["sell_stop"] = signals["prev_close"] - signals["expansion"]
    signals["long_trigger"] = signals["high"] >= signals["buy_stop"]
    signals["short_trigger"] = signals["low"] <= signals["sell_stop"]
    signals.loc[signals["prev_range"].isna() | (signals["prev_range"] <= 0), ["long_trigger", "short_trigger"]] = False
    true_range_parts = pd.concat(
        [
            signals["high"] - signals["low"],
            (signals["high"] - signals["close"].shift(1)).abs(),
            (signals["low"] - signals["close"].shift(1)).abs(),
        ],
        axis=1,
    )
    signals["atr14"] = true_range_parts.max(axis=1).rolling(ATR_LENGTH, min_periods=ATR_LENGTH).mean()
    return signals


def adjusted_entry(direction: str, price: float) -> float:
    return price * (1 + SLIPPAGE_RATE) if direction == "long" else price * (1 - SLIPPAGE_RATE)


def adjusted_exit(direction: str, price: float) -> float:
    return price * (1 - SLIPPAGE_RATE) if direction == "long" else price * (1 + SLIPPAGE_RATE)


def net_trade_return(direction: str, entry_price: float, exit_price: float) -> tuple[float, float]:
    gross = (exit_price / entry_price - 1.0) if direction == "long" else (entry_price / exit_price - 1.0)
    net = gross - (2 * COMMISSION_RATE)
    return gross, net


def exit_trade(signals: pd.DataFrame, candidate: TradeCandidate, exit_variant: str) -> dict[str, object]:
    entry_index = candidate.entry_index
    row = signals.iloc[entry_index]
    direction = candidate.direction
    entry_price = adjusted_entry(direction, candidate.raw_entry_price)
    reason = exit_variant
    if exit_variant == "close_exit":
        exit_index = entry_index
        raw_exit = float(row["close"])
        holding_bars = 1
    elif exit_variant == "next_bar_close_exit":
        exit_index = min(entry_index + 1, len(signals) - 1)
        raw_exit = float(signals.iloc[exit_index]["close"])
        holding_bars = max(1, exit_index - entry_index + 1)
    elif exit_variant == "previous_extreme_target_stop":
        stop = candidate.sell_stop if direction == "long" else candidate.buy_stop
        target = float(row["prev_high"]) if direction == "long" else float(row["prev_low"])
        stop_hit = row["low"] <= stop if direction == "long" else row["high"] >= stop
        target_hit = row["high"] >= target if direction == "long" else row["low"] <= target
        exit_index = entry_index
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
    elif exit_variant == "atr_stop_time_exit":
        atr = row["atr14"]
        if pd.isna(atr):
            exit_index = min(entry_index + ATR_MAX_HOLD_BARS - 1, len(signals) - 1)
            raw_exit = float(signals.iloc[exit_index]["close"])
            holding_bars = max(1, exit_index - entry_index + 1)
            reason = "atr_unavailable_time_exit"
        else:
            stop = candidate.raw_entry_price - (ATR_STOP_MULT * float(atr)) if direction == "long" else candidate.raw_entry_price + (ATR_STOP_MULT * float(atr))
            max_exit_index = min(entry_index + ATR_MAX_HOLD_BARS - 1, len(signals) - 1)
            exit_index = max_exit_index
            raw_exit = float(signals.iloc[max_exit_index]["close"])
            reason = "time_exit_3_bars"
            for scan_index in range(entry_index, max_exit_index + 1):
                scan = signals.iloc[scan_index]
                stop_hit = scan["low"] <= stop if direction == "long" else scan["high"] >= stop
                if stop_hit:
                    exit_index = scan_index
                    raw_exit = float(stop)
                    reason = "atr_stop"
                    break
            holding_bars = max(1, exit_index - entry_index + 1)
    else:
        raise ValueError(f"Unsupported exit variant: {exit_variant}")
    exit_price = adjusted_exit(direction, raw_exit)
    gross_return, net_return = net_trade_return(direction, entry_price, exit_price)
    return {
        "direction": direction,
        "entry_index": entry_index,
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


def build_candidate(signals: pd.DataFrame, index: int, direction: str) -> TradeCandidate:
    row = signals.iloc[index]
    raw_entry = float(row["buy_stop"] if direction == "long" else row["sell_stop"])
    return TradeCandidate(
        direction=direction,
        entry_index=index,
        entry_timestamp=row["timestamp"],
        raw_entry_price=raw_entry,
        buy_stop=float(row["buy_stop"]),
        sell_stop=float(row["sell_stop"]),
    )


def choose_same_bar_candidate(signals: pd.DataFrame, index: int, mode: str, exit_variant: str) -> TradeCandidate | None:
    if mode == "skip":
        return None
    if mode == "open_distance":
        row = signals.iloc[index]
        buy_distance = abs(float(row["open"]) - float(row["buy_stop"]))
        sell_distance = abs(float(row["open"]) - float(row["sell_stop"]))
        return build_candidate(signals, index, "long" if buy_distance <= sell_distance else "short")
    if mode == "pessimistic":
        long_candidate = build_candidate(signals, index, "long")
        short_candidate = build_candidate(signals, index, "short")
        long_trade = exit_trade(signals, long_candidate, exit_variant)
        short_trade = exit_trade(signals, short_candidate, exit_variant)
        return long_candidate if float(long_trade["net_return_pct"]) <= float(short_trade["net_return_pct"]) else short_candidate
    raise ValueError(f"Unsupported same_bar_both_mode: {mode}")


def run_backtest(
    symbol: str,
    data: pd.DataFrame,
    expansion_mult: float,
    exit_variant: str,
    same_bar_both_mode: str,
) -> tuple[dict[str, object], pd.DataFrame, pd.DataFrame]:
    signals = calculate_signals(data, expansion_mult)
    equity = INITIAL_EQUITY
    equity_points = [{"timestamp": signals.iloc[0]["timestamp"], "equity": equity}]
    trades: list[dict[str, object]] = []
    index = 1
    while index < len(signals):
        row = signals.iloc[index]
        long_trigger = bool(row["long_trigger"])
        short_trigger = bool(row["short_trigger"])
        candidate: TradeCandidate | None = None
        if long_trigger and short_trigger:
            candidate = choose_same_bar_candidate(signals, index, same_bar_both_mode, exit_variant)
        elif long_trigger:
            candidate = build_candidate(signals, index, "long")
        elif short_trigger:
            candidate = build_candidate(signals, index, "short")
        if candidate is None:
            index += 1
            continue
        trade = exit_trade(signals, candidate, exit_variant)
        trade["symbol"] = symbol
        trade["expansion_mult"] = expansion_mult
        trade["exit_variant"] = exit_variant
        trade["same_bar_both_mode"] = same_bar_both_mode
        trade["equity_before"] = equity
        equity *= 1.0 + (float(trade["net_return_pct"]) / 100.0)
        trade["equity_after"] = equity
        trades.append(trade)
        equity_points.append({"timestamp": trade["exit_timestamp"], "equity": equity})
        index = int(trade["exit_index"]) + 1
    trades_frame = pd.DataFrame(trades)
    equity_curve = pd.DataFrame(equity_points).drop_duplicates("timestamp", keep="last").reset_index(drop=True)
    metrics = calculate_metrics(symbol, signals, trades_frame, equity_curve, expansion_mult, exit_variant, same_bar_both_mode)
    return metrics, trades_frame, equity_curve


def max_drawdown_pct(equity: pd.Series) -> float:
    if equity.empty:
        return 0.0
    drawdown = (equity / equity.cummax()) - 1.0
    return float(drawdown.min() * 100)


def profit_factor(trades: pd.DataFrame) -> float:
    if trades.empty:
        return 0.0
    returns = trades["net_return_pct"] / 100.0
    gross_profit = returns[returns > 0].sum()
    gross_loss = abs(returns[returns < 0].sum())
    if gross_loss == 0:
        return float("inf") if gross_profit > 0 else 0.0
    return float(gross_profit / gross_loss)


def calculate_metrics(
    symbol: str,
    signals: pd.DataFrame,
    trades: pd.DataFrame,
    equity_curve: pd.DataFrame,
    expansion_mult: float,
    exit_variant: str,
    same_bar_both_mode: str,
) -> dict[str, object]:
    start = signals.iloc[0]["timestamp"]
    end = signals.iloc[-1]["timestamp"]
    years = max((end - start).days / 365.25, 1 / 365.25)
    final_equity = float(equity_curve.iloc[-1]["equity"]) if not equity_curve.empty else INITIAL_EQUITY
    net_return_pct = (final_equity / INITIAL_EQUITY - 1.0) * 100.0
    cagr = ((final_equity / INITIAL_EQUITY) ** (1.0 / years) - 1.0) * 100.0
    buy_hold = ((float(signals.iloc[-1]["close"]) / float(signals.iloc[0]["close"])) - 1.0) * 100.0
    if trades.empty:
        return {
            "symbol": symbol,
            "timeframe": "1D",
            "expansion_mult": expansion_mult,
            "exit_variant": exit_variant,
            "same_bar_both_mode": same_bar_both_mode,
            "bars_tested": len(signals),
            "start_date": start.date().isoformat(),
            "end_date": end.date().isoformat(),
            "total_trades": 0,
            "long_trades": 0,
            "short_trades": 0,
            "win_rate": 0.0,
            "gross_return_pct": 0.0,
            "net_return_pct": net_return_pct,
            "CAGR": cagr,
            "max_drawdown_pct": max_drawdown_pct(equity_curve["equity"]),
            "profit_factor": 0.0,
            "avg_trade_pct": 0.0,
            "median_trade_pct": 0.0,
            "avg_win_pct": 0.0,
            "avg_loss_pct": 0.0,
            "expectancy_pct": 0.0,
            "best_trade_pct": 0.0,
            "worst_trade_pct": 0.0,
            "average_holding_bars": 0.0,
            "exposure_pct": 0.0,
            "final_equity": final_equity,
            "buy_and_hold_return_pct": buy_hold,
            "beats_buy_and_hold": net_return_pct > buy_hold,
        }
    net_returns = trades["net_return_pct"]
    gross_returns = trades["gross_return_pct"]
    wins = net_returns[net_returns > 0]
    losses = net_returns[net_returns < 0]
    held_bars = trades["holding_bars"].sum()
    return {
        "symbol": symbol,
        "timeframe": "1D",
        "expansion_mult": expansion_mult,
        "exit_variant": exit_variant,
        "same_bar_both_mode": same_bar_both_mode,
        "bars_tested": len(signals),
        "start_date": start.date().isoformat(),
        "end_date": end.date().isoformat(),
        "total_trades": int(len(trades)),
        "long_trades": int((trades["direction"] == "long").sum()),
        "short_trades": int((trades["direction"] == "short").sum()),
        "win_rate": float((net_returns > 0).mean() * 100),
        "gross_return_pct": float(((1 + gross_returns / 100).prod() - 1) * 100),
        "net_return_pct": net_return_pct,
        "CAGR": cagr,
        "max_drawdown_pct": max_drawdown_pct(equity_curve["equity"]),
        "profit_factor": profit_factor(trades),
        "avg_trade_pct": float(net_returns.mean()),
        "median_trade_pct": float(net_returns.median()),
        "avg_win_pct": float(wins.mean()) if not wins.empty else 0.0,
        "avg_loss_pct": float(losses.mean()) if not losses.empty else 0.0,
        "expectancy_pct": float(net_returns.mean()),
        "best_trade_pct": float(net_returns.max()),
        "worst_trade_pct": float(net_returns.min()),
        "average_holding_bars": float(trades["holding_bars"].mean()),
        "exposure_pct": float(held_bars / len(signals) * 100),
        "final_equity": final_equity,
        "buy_and_hold_return_pct": buy_hold,
        "beats_buy_and_hold": bool(net_return_pct > buy_hold),
    }


def aggregate_portfolio(results: pd.DataFrame, trades: pd.DataFrame, expansion_mult: float, exit_variant: str, same_bar_both_mode: str) -> dict[str, object]:
    subset = results[
        (results["expansion_mult"] == expansion_mult)
        & (results["exit_variant"] == exit_variant)
        & (results["same_bar_both_mode"] == same_bar_both_mode)
    ].copy()
    trade_subset = trades[
        (trades["expansion_mult"] == expansion_mult)
        & (trades["exit_variant"] == exit_variant)
        & (trades["same_bar_both_mode"] == same_bar_both_mode)
    ].copy()
    if subset.empty:
        return {}
    aggregate_net = float(subset["net_return_pct"].mean())
    aggregate_final = INITIAL_EQUITY * (1.0 + aggregate_net / 100.0)
    return {
        "expansion_mult": expansion_mult,
        "exit_variant": exit_variant,
        "same_bar_both_mode": same_bar_both_mode,
        "symbols": int(len(subset)),
        "positive_symbols": int((subset["net_return_pct"] > 0).sum()),
        "aggregate_net_return_pct": aggregate_net,
        "aggregate_max_drawdown_pct": float(subset["max_drawdown_pct"].mean()),
        "aggregate_profit_factor": profit_factor(trade_subset),
        "aggregate_trade_count": int(subset["total_trades"].sum()),
        "aggregate_final_equity": aggregate_final,
    }


def decide_verdict(portfolio: dict[str, object], results: pd.DataFrame) -> str:
    if not portfolio:
        return "DATA_NOT_FOUND"
    positive_symbols = int(portfolio["positive_symbols"])
    net_return = float(portfolio["aggregate_net_return_pct"])
    pf_value = float(portfolio["aggregate_profit_factor"])
    max_dd = abs(float(portfolio["aggregate_max_drawdown_pct"]))
    trade_count = int(portfolio["aggregate_trade_count"])
    if positive_symbols >= 3 and net_return > 0 and pf_value > 1.10 and max_dd < 35 and trade_count >= 50:
        return "PASS_CANDIDATE"
    if net_return <= 0 or pf_value <= 1.0 or positive_symbols <= 1:
        return "REJECT_CANDIDATE"
    if net_return > 0 and (pf_value <= 1.10 or positive_symbols == 2):
        return "WEAK_CANDIDATE"
    if results["net_return_pct"].max() > 0 and positive_symbols <= 1:
        return "REJECT_CANDIDATE"
    return "WEAK_CANDIDATE"


def markdown_table(frame: pd.DataFrame, columns: list[str], max_rows: int | None = None) -> str:
    if frame.empty:
        return "_No rows._"
    output = frame[columns].copy()
    if max_rows is not None:
        output = output.head(max_rows)
    for column in output.columns:
        if pd.api.types.is_float_dtype(output[column]):
            output[column] = output[column].map(lambda value: f"{value:.2f}" if np.isfinite(value) else "inf")
    headers = [str(column) for column in output.columns]
    rows = [[str(value) for value in row] for row in output.to_numpy().tolist()]
    widths = [
        max(len(headers[index]), *(len(row[index]) for row in rows)) if rows else len(headers[index])
        for index in range(len(headers))
    ]
    header_line = "| " + " | ".join(headers[index].ljust(widths[index]) for index in range(len(headers))) + " |"
    separator = "| " + " | ".join("-" * widths[index] for index in range(len(headers))) + " |"
    row_lines = ["| " + " | ".join(row[index].ljust(widths[index]) for index in range(len(headers))) + " |" for row in rows]
    return "\n".join([header_line, separator, *row_lines])


def generate_report(
    report_path: Path,
    results: pd.DataFrame,
    trades: pd.DataFrame,
    datasets: dict[str, DatasetInfo],
    portfolio_rows: list[dict[str, object]],
    commands_run: list[str],
    git_status_before: str,
    git_status_after: str,
    git_diff_stat: str,
    verification_lines: list[str],
) -> str:
    primary = results[
        (results["expansion_mult"] == PRIMARY_EXPANSION_MULT)
        & (results["same_bar_both_mode"] == PRIMARY_SAME_BAR_MODE)
    ].copy()
    base = primary[primary["exit_variant"] == "close_exit"].copy()
    portfolio_primary = aggregate_portfolio(results, trades, PRIMARY_EXPANSION_MULT, "close_exit", PRIMARY_SAME_BAR_MODE)
    verdict = decide_verdict(portfolio_primary, base)
    best_symbol_row = base.sort_values("net_return_pct", ascending=False).head(1)
    worst_symbol_row = base.sort_values("net_return_pct", ascending=True).head(1)
    exit_comparison = primary.groupby("exit_variant", as_index=False).agg(
        aggregate_net_return_pct=("net_return_pct", "mean"),
        aggregate_max_drawdown_pct=("max_drawdown_pct", "mean"),
        total_trades=("total_trades", "sum"),
        positive_symbols=("net_return_pct", lambda values: int((values > 0).sum())),
    )
    trade_primary = trades[
        (trades["expansion_mult"] == PRIMARY_EXPANSION_MULT)
        & (trades["same_bar_both_mode"] == PRIMARY_SAME_BAR_MODE)
    ].copy()
    exit_comparison["aggregate_profit_factor"] = [
        profit_factor(trade_primary[trade_primary["exit_variant"] == variant]) for variant in exit_comparison["exit_variant"]
    ]
    best_exit = exit_comparison.sort_values(["aggregate_net_return_pct", "aggregate_profit_factor"], ascending=False).head(1)
    sensitivity = results[
        (results["same_bar_both_mode"] == PRIMARY_SAME_BAR_MODE)
        & (results["exit_variant"] == "close_exit")
    ].groupby("expansion_mult", as_index=False).agg(
        aggregate_net_return_pct=("net_return_pct", "mean"),
        total_trades=("total_trades", "sum"),
        positive_symbols=("net_return_pct", lambda values: int((values > 0).sum())),
        avg_max_drawdown_pct=("max_drawdown_pct", "mean"),
    )
    same_bar_compare = results[
        (results["expansion_mult"] == PRIMARY_EXPANSION_MULT)
        & (results["exit_variant"] == "close_exit")
    ].groupby("same_bar_both_mode", as_index=False).agg(
        aggregate_net_return_pct=("net_return_pct", "mean"),
        total_trades=("total_trades", "sum"),
        positive_symbols=("net_return_pct", lambda values: int((values > 0).sum())),
    )
    data_lines = [
        f"- {info.symbol}: `{info.path}`; dataset_id={info.dataset_id}; sha256={info.sha256}; range={info.manifest_start} to {info.manifest_end}; notes={info.notes}"
        for info in datasets.values()
    ]
    files = [
        report_path.parent.parent / "README.md",
        report_path.parent.parent / "crabel_range_expansion.py",
        report_path.parent.parent / "run_crabel_backtest.py",
        report_path,
        report_path.parent / "QL_CRABEL_RANGE_EXPANSION_RESULTS.csv",
        report_path.parent / "QL_CRABEL_RANGE_EXPANSION_TRADES.csv",
    ]
    lines = [
        "# QL_Crabel_Range_Expansion_v0 Report",
        "",
        "## 1. Executive Summary",
        f"- Final verdict: **{verdict}**.",
        f"- Primary test: expansion_mult={PRIMARY_EXPANSION_MULT}, exit_variant=close_exit, same_bar_both_mode=skip.",
        f"- Primary aggregate net return: {portfolio_primary.get('aggregate_net_return_pct', 0):.2f}%; PF: {portfolio_primary.get('aggregate_profit_factor', 0):.2f}; trades: {portfolio_primary.get('aggregate_trade_count', 0)}.",
        "",
        "## 2. Final Verdict",
        f"**{verdict}**",
        "",
        "## 3. What Was Implemented",
        "- Python-only research prototype with isolated loader, signal calculation, backtest engine, metrics, portfolio aggregation, CSV output, and markdown report generation.",
        "- No Pine Script and no production MTC integration were changed.",
        "",
        "## 4. Source Strategy Rule",
        "- previous_range = previous_high - previous_low",
        "- expansion = previous_range * expansion_mult",
        "- buy_stop = previous_close + expansion",
        "- sell_stop = previous_close - expansion",
        "- Long triggers when high >= buy_stop; short triggers when low <= sell_stop.",
        "",
        "## 5. Data Used",
        "- Source: repo-local `MTC_V2_OPTIMIZATION_DATA_BUNDLE_20260427`, normalized Binance futures 1D files.",
        "- Timeframe: 1D daily bars; no resampling was required.",
        "- Volume: source files mark volume as missing; loader fills volume=0 because this prototype does not use volume.",
        *data_lines,
        "",
        "## 6. Backtest Assumptions",
        f"- Initial equity: {INITIAL_EQUITY:.2f} USD; fixed notional: 1x current equity.",
        f"- Commission: {COMMISSION_RATE:.4%} per side; slippage: {SLIPPAGE_RATE:.4%} per side.",
        "- Shorts are supported; only one position is active at a time.",
        "- Same-bar both-trigger modes: skip, pessimistic, open_distance. Primary report uses skip.",
        "",
        "## 7. Base Model Results",
        markdown_table(
            base,
            ["symbol", "total_trades", "long_trades", "short_trades", "win_rate", "net_return_pct", "max_drawdown_pct", "profit_factor", "final_equity", "buy_and_hold_return_pct", "beats_buy_and_hold"],
        ),
        "",
        "## 8. Exit Variant Comparison",
        markdown_table(exit_comparison, ["exit_variant", "aggregate_net_return_pct", "aggregate_profit_factor", "aggregate_max_drawdown_pct", "total_trades", "positive_symbols"]),
        "",
        "## 9. Expansion Mult Sensitivity",
        markdown_table(sensitivity, ["expansion_mult", "aggregate_net_return_pct", "total_trades", "positive_symbols", "avg_max_drawdown_pct"]),
        "",
        "## 10. Portfolio Aggregate Result",
        markdown_table(pd.DataFrame(portfolio_rows), ["expansion_mult", "exit_variant", "same_bar_both_mode", "positive_symbols", "aggregate_net_return_pct", "aggregate_profit_factor", "aggregate_max_drawdown_pct", "aggregate_trade_count"]),
        "",
        "## 11. Buy & Hold Comparison",
        markdown_table(base, ["symbol", "net_return_pct", "buy_and_hold_return_pct", "beats_buy_and_hold"]),
        "",
        "## 12. Failure Modes",
        f"- Whipsaw: primary average win rate is {base['win_rate'].mean():.2f}% and costs are applied on both sides.",
        f"- Same-bar ambiguity: skip mode avoids ambiguous bars; comparison: {same_bar_compare.to_dict(orient='records')}.",
        f"- Drawdown: primary aggregate average max drawdown is {portfolio_primary.get('aggregate_max_drawdown_pct', 0):.2f}%.",
        f"- Insufficient trades: primary total trade count is {portfolio_primary.get('aggregate_trade_count', 0)}.",
        "",
        "## 13. Recommendation",
        f"- Continue to Pine/parity stage: {'yes' if verdict in {'PASS_CANDIDATE', 'WEAK_CANDIDATE'} else 'no'}.",
        f"- Best tested exit variant by aggregate net return: {best_exit.iloc[0]['exit_variant'] if not best_exit.empty else 'n/a'}.",
        "- Treat this as a research result only; no production defaults are implied.",
        "",
        "## 14. Next Steps",
        "- If promoted later, start with Python/Pine signal producer parity only after a separate approval gate.",
        "- If rejected, archive as a standalone QuantLens research result because costs and multi-symbol robustness did not clear the stated gate.",
        "",
        "## 15. Files Created / Modified",
        *[f"- `{path}`" for path in files],
        "",
        "## 16. Commands Run",
        *[f"- `{command}`" for command in commands_run],
        "",
        "## 17. Verification Checklist",
        *[f"- {line}" for line in verification_lines],
        "",
        "## Git Status Before",
        "```text",
        git_status_before.strip() or "clean",
        "```",
        "",
        "## Git Diff Stat After",
        "```text",
        git_diff_stat.strip() or "no diff",
        "```",
        "",
        "## Git Status After",
        "```text",
        git_status_after.strip() or "clean",
        "```",
        "",
        "## Final Short Answers",
        f"- Kisa karar: {verdict}",
        f"- En iyi sembol: {best_symbol_row.iloc[0]['symbol'] if not best_symbol_row.empty else 'n/a'}",
        f"- En kotu sembol: {worst_symbol_row.iloc[0]['symbol'] if not worst_symbol_row.empty else 'n/a'}",
        f"- En iyi exit variant: {best_exit.iloc[0]['exit_variant'] if not best_exit.empty else 'n/a'}",
        f"- 0.90 video ayari karli mi: {'yes' if portfolio_primary.get('aggregate_net_return_pct', 0) > 0 else 'no'}",
        f"- Komisyon/slippage sonrasi edge var mi: {'yes' if portfolio_primary.get('aggregate_profit_factor', 0) > 1.0 and portfolio_primary.get('aggregate_net_return_pct', 0) > 0 else 'no'}",
        f"- Pine/parity asamasina gecmeye deger mi: {'yes' if verdict in {'PASS_CANDIDATE', 'WEAK_CANDIDATE'} else 'no'}",
    ]
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return verdict
