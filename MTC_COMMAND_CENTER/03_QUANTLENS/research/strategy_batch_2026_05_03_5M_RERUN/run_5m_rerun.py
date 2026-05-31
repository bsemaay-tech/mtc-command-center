from __future__ import annotations

import json
import math
from dataclasses import dataclass
from datetime import UTC, datetime, time
from pathlib import Path
from zoneinfo import ZoneInfo

import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
ACQ_ROOT = ROOT / "06_QUANTLENS_LAB" / "research" / "data_acquisition_5m_2026_05_03"
BATCH_ROOT = ROOT / "06_QUANTLENS_LAB" / "research" / "strategy_batch_2026_05_03_5M_RERUN"
OLD_BATCH_ROOT = ROOT / "06_QUANTLENS_LAB" / "research" / "strategy_batch_2026_05_03"
MANIFEST_PATH = ACQ_ROOT / "manifest_5m_research.json"
NY = ZoneInfo("America/New_York")

INITIAL_EQUITY = 10_000.0
COMMISSION = 0.0004
SLIPPAGE = 0.0002
ASSETS = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT", "XRPUSDT"]


def markdown_table(frame: pd.DataFrame, columns: list[str] | None = None, max_rows: int = 50) -> str:
    if frame.empty:
        return "_No rows._"
    view = frame.copy()
    if columns is not None:
        view = view[[column for column in columns if column in view.columns]]
    view = view.head(max_rows)
    headers = list(view.columns)
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for _, row in view.iterrows():
        values = []
        for value in row:
            if isinstance(value, float):
                values.append(f"{value:.4f}")
            else:
                values.append(str(value))
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


@dataclass(frozen=True)
class Trade:
    strategy_id: str
    asset: str
    parameter_set: str
    direction: str
    entry_timestamp: str
    exit_timestamp: str
    entry_price: float
    exit_price: float
    gross_return_pct: float
    net_return_pct: float
    holding_bars: int


def load_manifest() -> dict:
    if not MANIFEST_PATH.exists():
        raise FileNotFoundError(f"Missing 5m research manifest: {MANIFEST_PATH}")
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def load_data(row: dict) -> pd.DataFrame:
    path = ACQ_ROOT / row["path"]
    frame = pd.read_csv(path)
    required = {"timestamp", "open", "high", "low", "close", "volume"}
    missing = required.difference(frame.columns)
    if missing:
        raise ValueError(f"{path} missing columns: {sorted(missing)}")
    frame["timestamp"] = pd.to_datetime(frame["timestamp"], utc=True)
    frame = frame.drop_duplicates("timestamp").sort_values("timestamp").reset_index(drop=True)
    frame["ny_datetime"] = frame["timestamp"].dt.tz_convert(NY)
    frame["ny_date"] = frame["ny_datetime"].dt.date.astype(str)
    frame["ny_time"] = frame["ny_datetime"].dt.time
    return frame


def adjusted_return(direction: str, raw_entry: float, raw_exit: float) -> tuple[float, float, float, float]:
    if direction == "long":
        entry = raw_entry * (1 + SLIPPAGE)
        exit_price = raw_exit * (1 - SLIPPAGE)
        gross = (raw_exit / raw_entry - 1) * 100
        net = (exit_price / entry - 1 - 2 * COMMISSION) * 100
    else:
        entry = raw_entry * (1 - SLIPPAGE)
        exit_price = raw_exit * (1 + SLIPPAGE)
        gross = (raw_entry / raw_exit - 1) * 100
        net = (entry / exit_price - 1 - 2 * COMMISSION) * 100
    return entry, exit_price, gross, net


def summarize(strategy_id: str, asset: str, parameter_set: str, trades: list[Trade], bar_count: int) -> dict:
    returns = pd.Series([trade.net_return_pct for trade in trades], dtype=float)
    wins = returns[returns > 0]
    losses = returns[returns < 0]
    profit_factor = float(wins.sum() / abs(losses.sum())) if abs(losses.sum()) > 0 else (math.inf if wins.sum() > 0 else 0.0)
    equity = INITIAL_EQUITY
    curve = [equity]
    for value in returns:
        equity *= 1 + value / 100
        curve.append(equity)
    equity_series = pd.Series(curve)
    drawdown = (equity_series / equity_series.cummax() - 1) * 100
    net_return = (equity / INITIAL_EQUITY - 1) * 100
    return {
        "strategy_id": strategy_id,
        "asset": asset,
        "timeframe": "5m",
        "parameter_set": parameter_set,
        "trade_count": int(len(trades)),
        "win_rate": float((returns > 0).mean() * 100) if len(returns) else 0.0,
        "average_win": float(wins.mean()) if len(wins) else 0.0,
        "average_loss": float(losses.mean()) if len(losses) else 0.0,
        "expectancy_per_trade": float(returns.mean()) if len(returns) else 0.0,
        "profit_factor": profit_factor,
        "net_return_pct": net_return,
        "max_drawdown_pct": float(drawdown.min()) if len(drawdown) else 0.0,
        "return_over_dd": float(net_return / abs(drawdown.min())) if len(drawdown) and drawdown.min() else math.inf,
        "average_holding_bars": float(pd.Series([trade.holding_bars for trade in trades]).mean()) if trades else 0.0,
        "exposure_pct": float(sum(trade.holding_bars for trade in trades) / bar_count * 100) if bar_count else 0.0,
    }


def aggregate(rows: pd.DataFrame, trades: pd.DataFrame) -> dict:
    if rows.empty:
        return {"trade_count": 0, "aggregate_pf": 0.0, "aggregate_net_return_pct": 0.0, "aggregate_max_dd_pct": 0.0}
    returns = trades["net_return_pct"] if not trades.empty else pd.Series(dtype=float)
    wins = returns[returns > 0].sum()
    losses = abs(returns[returns < 0].sum())
    pf = float(wins / losses) if losses else (math.inf if wins > 0 else 0.0)
    return {
        "trade_count": int(rows["trade_count"].sum()),
        "aggregate_pf": pf,
        "aggregate_net_return_pct": float(rows["net_return_pct"].mean()),
        "aggregate_max_dd_pct": float(rows["max_drawdown_pct"].mean()),
    }


def session_window(group: pd.DataFrame) -> pd.DataFrame:
    start = time(8, 0)
    end = time(16, 0)
    return group[(group["ny_time"] >= start) & (group["ny_time"] < end)].copy()


def backtest_orb(asset: str, data: pd.DataFrame, opening_range_minutes: int, holding_bars: int, stop_type: str) -> list[Trade]:
    trades: list[Trade] = []
    strategy_id = "QL_8AM_ET_OPENING_RANGE_BREAKOUT_v0"
    parameter_set = json.dumps({"opening_range_minutes": opening_range_minutes, "holding_bars": holding_bars, "stop_type": stop_type}, sort_keys=True)
    range_bars = max(1, opening_range_minutes // 5)
    for _, day in data.groupby("ny_date", sort=True):
        session = session_window(day)
        if len(session) <= range_bars + holding_bars:
            continue
        opening = session.iloc[:range_bars]
        after = session.iloc[range_bars:].reset_index(drop=True)
        or_high = float(opening["high"].max())
        or_low = float(opening["low"].min())
        for i, bar in after.iterrows():
            long_hit = float(bar["high"]) >= or_high
            short_hit = float(bar["low"]) <= or_low
            if long_hit and short_hit:
                break
            if not (long_hit or short_hit):
                continue
            direction = "long" if long_hit else "short"
            entry_raw = or_high if direction == "long" else or_low
            exit_raw = float(bar["close"])
            exit_index = min(i + holding_bars, len(after) - 1)
            stop_raw = or_low if direction == "long" else or_high
            stopped = False
            for j in range(i, exit_index + 1):
                test_bar = after.iloc[j]
                if stop_type == "opposite_OR_side":
                    if direction == "long" and float(test_bar["low"]) <= stop_raw:
                        exit_raw = stop_raw
                        exit_index = j
                        stopped = True
                        break
                    if direction == "short" and float(test_bar["high"]) >= stop_raw:
                        exit_raw = stop_raw
                        exit_index = j
                        stopped = True
                        break
            if not stopped:
                exit_raw = float(after.iloc[exit_index]["close"])
            entry, exit_price, gross, net = adjusted_return(direction, entry_raw, exit_raw)
            trades.append(
                Trade(strategy_id, asset, parameter_set, direction, str(bar["timestamp"]), str(after.iloc[exit_index]["timestamp"]), entry, exit_price, gross, net, int(exit_index - i + 1))
            )
            break
    return trades


def backtest_highbeta(asset: str, data: pd.DataFrame, lookback: int, confirmation_bars: int, exit_after_bars: int) -> list[Trade]:
    trades: list[Trade] = []
    strategy_id = "QL_HIGHBETA_OPENINGBAR_GAPANDGO_v0"
    parameter_set = json.dumps({"lookback_N": lookback, "confirmation_bars": confirmation_bars, "exit_after_bars": exit_after_bars}, sort_keys=True)
    sessions: list[tuple[str, pd.DataFrame, float]] = []
    for date, day in data.groupby("ny_date", sort=True):
        session = session_window(day).reset_index(drop=True)
        if len(session) < max(confirmation_bars + exit_after_bars + 2, 10):
            continue
        first = session.iloc[0]
        first_range = float(first["high"] - first["low"])
        sessions.append((date, session, first_range))
    ranges = pd.Series([item[2] for item in sessions])
    for idx in range(lookback, len(sessions)):
        _, session, first_range = sessions[idx]
        prior_max = float(ranges.iloc[idx - lookback : idx].max())
        first = session.iloc[0]
        if first_range < prior_max:
            continue
        if float(first["close"]) <= float(first["open"]):
            continue
        first_high = float(first["high"])
        first_low = float(first["low"])
        confirm = session.iloc[1 : 1 + confirmation_bars]
        if (confirm["low"] < first_low).any():
            continue
        after = session.iloc[1 + confirmation_bars :].reset_index(drop=True)
        for i, bar in after.iterrows():
            if float(bar["high"]) < first_high:
                continue
            entry_raw = first_high
            exit_index = min(i + exit_after_bars, len(after) - 1)
            exit_raw = float(after.iloc[exit_index]["close"])
            for j in range(i, exit_index + 1):
                if float(after.iloc[j]["low"]) <= first_low:
                    exit_raw = first_low
                    exit_index = j
                    break
            entry, exit_price, gross, net = adjusted_return("long", entry_raw, exit_raw)
            trades.append(
                Trade(strategy_id, asset, parameter_set, "long", str(bar["timestamp"]), str(after.iloc[exit_index]["timestamp"]), entry, exit_price, gross, net, int(exit_index - i + 1))
            )
            break
    return trades


def choose_best(summary: pd.DataFrame) -> str:
    return (
        summary.groupby("parameter_set", as_index=False)
        .agg(score=("profit_factor", "mean"), trades=("trade_count", "sum"))
        .sort_values(["score", "trades"], ascending=False)
        .iloc[0]["parameter_set"]
    )


def run_strategy(strategy_id: str, datasets: dict[str, dict]) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    summaries: list[dict] = []
    all_trades: list[Trade] = []
    for asset in ASSETS:
        if asset not in datasets:
            continue
        data = load_data(datasets[asset])
        if strategy_id == "QL_8AM_ET_OPENING_RANGE_BREAKOUT_v0":
            for opening_range_minutes in [15, 20, 30, 60]:
                for holding_bars in [3, 6, 10, 20]:
                    for stop_type in ["opposite_OR_side", "time_only"]:
                        trades = backtest_orb(asset, data, opening_range_minutes, holding_bars, stop_type)
                        parameter_set = json.dumps({"opening_range_minutes": opening_range_minutes, "holding_bars": holding_bars, "stop_type": stop_type}, sort_keys=True)
                        summaries.append(summarize(strategy_id, asset, parameter_set, trades, len(data)))
                        all_trades.extend(trades)
        else:
            for lookback in [10, 20]:
                for confirmation_bars in [3, 4, 5]:
                    for exit_after_bars in [6, 12, 24]:
                        trades = backtest_highbeta(asset, data, lookback, confirmation_bars, exit_after_bars)
                        parameter_set = json.dumps({"lookback_N": lookback, "confirmation_bars": confirmation_bars, "exit_after_bars": exit_after_bars}, sort_keys=True)
                        summaries.append(summarize(strategy_id, asset, parameter_set, trades, len(data)))
                        all_trades.extend(trades)
    summary = pd.DataFrame(summaries)
    trades = pd.DataFrame([trade.__dict__ for trade in all_trades])
    if summary.empty:
        return summary, trades, pd.DataFrame()
    best = choose_best(summary)
    primary = summary[summary["parameter_set"] == best].copy()
    primary_trades = trades[trades["parameter_set"] == best].copy() if not trades.empty else pd.DataFrame()
    return primary, primary_trades, summary


def write_strategy_outputs(strategy_id: str, summary: pd.DataFrame, trades: pd.DataFrame, sweep: pd.DataFrame) -> dict:
    out_dir = BATCH_ROOT / "strategies" / strategy_id / "results"
    out_dir.mkdir(parents=True, exist_ok=True)
    summary.to_csv(out_dir / "summary.csv", index=False)
    trades.to_csv(out_dir / "trades.csv", index=False)
    sweep.to_csv(out_dir / "parameter_sweep.csv", index=False)
    agg = aggregate(summary, trades)
    positive_assets = int((summary["net_return_pct"] > 0).sum()) if not summary.empty else 0
    classification = "WEAK_CANDIDATE_CRYPTO_PROXY" if agg["aggregate_pf"] > 1.10 and positive_assets >= 3 else "REJECT_CRYPTO_PROXY"
    if summary.empty:
        classification = "BLOCKED_DATA"
    report = [
        f"# {strategy_id} 5m Rerun",
        "",
        f"- Classification: `{classification}`.",
        f"- Aggregate PF: `{agg['aggregate_pf']:.4f}`.",
        f"- Aggregate net return pct: `{agg['aggregate_net_return_pct']:.2f}`.",
        f"- Aggregate max DD pct: `{agg['aggregate_max_dd_pct']:.2f}`.",
        f"- Trade count: `{agg['trade_count']}`.",
        "- Scope: crypto proxy only; not proof for equity/session-native edge.",
        "",
        "## Asset Breakdown",
        markdown_table(summary),
    ]
    (out_dir / "report.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    return {"strategy_id": strategy_id, **agg, "tested_assets_count": int(summary["asset"].nunique()) if not summary.empty else 0, "final_classification": classification}


def write_reports(index: pd.DataFrame, manifest: dict) -> None:
    BATCH_ROOT.mkdir(parents=True, exist_ok=True)
    index.to_csv(BATCH_ROOT / "summary.csv", index=False)
    old_index = pd.read_csv(OLD_BATCH_ROOT / "STRATEGY_CANDIDATE_INDEX.csv")
    old_blocked = old_index[old_index["strategy_id"].isin(index["strategy_id"].tolist() + ["QL_TY_MICROCAP_LIQUIDITY_REVERSION_SHORT_v0"])]
    comparison = old_blocked.merge(index, on="strategy_id", how="outer", suffixes=("_old", "_5m"))
    comparison.loc[comparison["strategy_id"] == "QL_TY_MICROCAP_LIQUIDITY_REVERSION_SHORT_v0", "final_classification_5m"] = "DATA_BLOCKED_US_MICROCAP"
    comparison.to_csv(BATCH_ROOT / "OLD_BLOCKED_VS_5M_RERUN_COMPARISON.csv", index=False)
    quality = pd.read_csv(ACQ_ROOT / "DATA_QUALITY_REPORT.csv")
    pass_count = int((quality["status"] == "PASS").sum())
    warn_count = int((quality["status"] != "PASS").sum())
    ty_reason = "Ty Rajnus remains blocked: needs US microcap 1m OHLCV, premarket/afterhours, market cap, borrow/locate, dilution and halt flags. Binance 5m crypto is not a valid proxy."
    limitations = [
        "# STRATEGY DATA LIMITATIONS",
        "",
        "- 8AM ORB and HighBeta GapAndGo are rerun as crypto 24/7 session proxies only.",
        "- 08:00 anchor uses `America/New_York` timezone with DST-aware conversion from UTC bars.",
        "- Crypto has no equity-style official regular session open, gap, premarket, afterhours, halt, market cap, borrow, or dilution context.",
        f"- {ty_reason}",
    ]
    (BATCH_ROOT / "STRATEGY_DATA_LIMITATIONS.md").write_text("\n".join(limitations) + "\n", encoding="utf-8")
    lines = [
        "# 5M RERUN MASTER REPORT",
        "",
        "## Executive Summary",
        f"- 5m data downloaded: `{len(manifest.get('datasets', [])) >= 5}`.",
        f"- Downloaded symbols: `{len(manifest.get('datasets', []))}`.",
        "- Strategies rerun: `QL_8AM_ET_OPENING_RANGE_BREAKOUT_v0`, `QL_HIGHBETA_OPENINGBAR_GAPANDGO_v0`.",
        "- Ty Rajnus microcap short: `DATA_BLOCKED_US_MICROCAP`.",
        "- Pine stage: `NO`.",
        "",
        "## Data Quality",
        markdown_table(quality, max_rows=30),
        "",
        "## Rerun Results",
        markdown_table(index),
        "",
        "## Reliability",
        "- These results are crypto proxy tests only. They can unblock exploratory research, not Pine/MTC production promotion.",
        "- 8AM ET anchor is DST-aware, but it is not a native crypto market open.",
        "- HighBeta GapAndGo is equity/opening-bar inspired; crypto proxy cannot validate equity gap behavior.",
        "",
        "## Answers",
        f"- 5m data successfully downloaded: yes for required minimum assets; quality status is {pass_count} PASS and {warn_count} non-PASS warning rows.",
        "- 8AM ORB tested: yes.",
        "- HighBeta GapAndGo tested: yes.",
        f"- Ty Rajnus still blocked: {ty_reason}",
        "- Pine phase: no strategy should move to Pine from this proxy rerun.",
        "- More data needed: Ty Rajnus needs US microcap-specific data; HighBeta needs US high-beta equity 5m with session/gap data for a non-proxy test.",
    ]
    (BATCH_ROOT / "5M_RERUN_MASTER_REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (BATCH_ROOT / "README.md").write_text("# Strategy Batch 2026-05-03 5M Rerun\n\nResearch-only crypto proxy rerun for formerly blocked intraday strategies.\n", encoding="utf-8")


def main() -> int:
    manifest = load_manifest()
    datasets = {row["symbol"]: row for row in manifest["datasets"] if row.get("timeframe") == "5m"}
    rows = []
    for strategy_id in ["QL_8AM_ET_OPENING_RANGE_BREAKOUT_v0", "QL_HIGHBETA_OPENINGBAR_GAPANDGO_v0"]:
        summary, trades, sweep = run_strategy(strategy_id, datasets)
        rows.append(write_strategy_outputs(strategy_id, summary, trades, sweep))
    index = pd.DataFrame(rows)
    write_reports(index, manifest)
    print(index.to_string(index=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
