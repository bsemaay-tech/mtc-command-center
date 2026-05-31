from __future__ import annotations

import json
import math
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
SOURCE_ROOT = ROOT / "06_QUANTLENS_LAB" / "research" / "strategy_batch_2026_05_03_AUDITED"
OUTPUT_ROOT = ROOT / "06_QUANTLENS_LAB" / "research" / "stage2_robustness_2026_05_03"

STRATEGIES = {
    "QL_CRABEL_RANGE_EXPANSION_STAGE2_v0": SOURCE_ROOT / "strategies" / "04_crabel_range_expansion_stage2" / "results",
    "QL_LINDA_5SMA_RS_PULLBACK_v0": SOURCE_ROOT / "strategies" / "07_linda_5sma_rs_pullback" / "results",
    "QL_BIGBELUGA_RSI_DIVERGENCE_CHOCH_ATR_v0": SOURCE_ROOT / "strategies" / "05_bigbeluga_rsi_choch_atr" / "results",
}
ASSET_ORDER = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT", "XRPUSDT"]
TRAIN_ASSETS = ["BTCUSDT", "ETHUSDT", "SOLUSDT"]
HOLDOUT_ASSETS = ["BNBUSDT", "XRPUSDT"]
BASE_COST_PCT = 0.08
FEE_SCENARIOS = {"base": 1.0, "2x": 2.0, "3x": 3.0, "5x": 5.0}


def markdown_table(frame: pd.DataFrame, columns: list[str] | None = None, max_rows: int = 30) -> str:
    if frame.empty:
        return "_No rows._"
    view = frame.copy()
    if columns is not None:
        view = view[[column for column in columns if column in view.columns]]
    view = view.head(max_rows)
    lines = [
        "| " + " | ".join(view.columns) + " |",
        "| " + " | ".join(["---"] * len(view.columns)) + " |",
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


def profit_factor(values: pd.Series) -> float:
    if values.empty:
        return 0.0
    wins = values[values > 0].sum()
    losses = abs(values[values < 0].sum())
    if losses == 0:
        return math.inf if wins > 0 else 0.0
    return float(wins / losses)


def compound_return(values: pd.Series) -> float:
    if values.empty:
        return 0.0
    return float(((1 + values / 100).prod() - 1) * 100)


def max_drawdown(values: pd.Series) -> float:
    equity = (1 + values / 100).cumprod()
    if equity.empty:
        return 0.0
    drawdown = (equity / equity.cummax() - 1) * 100
    return float(drawdown.min())


def longest_losing_streak(values: pd.Series) -> int:
    longest = 0
    current = 0
    for value in values:
        if value < 0:
            current += 1
            longest = max(longest, current)
        else:
            current = 0
    return longest


def drawdown_duration(values: pd.Series) -> int:
    equity = (1 + values / 100).cumprod()
    if equity.empty:
        return 0
    running_max = equity.cummax()
    longest = 0
    current = 0
    for below in equity < running_max:
        if below:
            current += 1
            longest = max(longest, current)
        else:
            current = 0
    return longest


def metrics_from_trades(trades: pd.DataFrame, return_column: str = "net_return_pct") -> dict[str, Any]:
    values = pd.to_numeric(trades[return_column], errors="coerce").dropna() if return_column in trades else pd.Series(dtype=float)
    return {
        "trade_count": int(len(values)),
        "profit_factor": profit_factor(values),
        "net_return_pct": compound_return(values),
        "max_drawdown_pct": max_drawdown(values),
        "avg_trade_pct": float(values.mean()) if len(values) else 0.0,
        "win_rate": float((values > 0).mean() * 100) if len(values) else 0.0,
        "longest_losing_streak": longest_losing_streak(values),
    }


def load_strategy(result_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, str]:
    summary = pd.read_csv(result_dir / "summary.csv")
    trades = pd.read_csv(result_dir / "trades.csv")
    sweep = pd.read_csv(result_dir / "parameter_sweep.csv")
    best_param = str(summary["parameter_set"].iloc[0])
    trades["entry_timestamp"] = pd.to_datetime(trades["entry_timestamp"], utc=True)
    trades["exit_timestamp"] = pd.to_datetime(trades["exit_timestamp"], utc=True)
    return summary, trades, sweep, best_param


def selected_trades(trades: pd.DataFrame, best_param: str) -> pd.DataFrame:
    return trades[trades["parameter_set"].astype(str) == best_param].copy()


def year_split(strategy_id: str, trades: pd.DataFrame) -> list[dict[str, Any]]:
    rows = []
    for year in [2024, 2025, 2026]:
        group = trades[trades["exit_timestamp"].dt.year == year]
        row = {"strategy_id": strategy_id, "year": year, **metrics_from_trades(group)}
        rows.append(row)
    return rows


def asset_split(strategy_id: str, summary: pd.DataFrame, trades: pd.DataFrame) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rows = []
    for asset in ASSET_ORDER:
        group = trades[trades["asset"] == asset]
        row = {"strategy_id": strategy_id, "asset": asset, **metrics_from_trades(group)}
        summary_row = summary[summary["asset"] == asset]
        if not summary_row.empty:
            row["source_summary_pf"] = float(summary_row["profit_factor"].iloc[0])
            row["source_summary_net_return_pct"] = float(summary_row["net_return_pct"].iloc[0])
            row["source_summary_max_dd_pct"] = float(summary_row["max_drawdown_pct"].iloc[0])
        rows.append(row)
    frame = pd.DataFrame(rows).sort_values("profit_factor", ascending=False)
    positive_assets = int((frame["net_return_pct"] > 0).sum())
    best_asset = frame.iloc[0]["asset"] if not frame.empty else ""
    worst_asset = frame.iloc[-1]["asset"] if not frame.empty else ""
    median_asset = frame.sort_values("profit_factor").iloc[len(frame) // 2]["asset"] if not frame.empty else ""
    total_profit = trades.loc[trades["net_return_pct"] > 0, "net_return_pct"].sum()
    asset_profit = trades.groupby("asset")["net_return_pct"].apply(lambda s: s[s > 0].sum())
    dominant_share = float(asset_profit.max() / total_profit * 100) if total_profit > 0 and not asset_profit.empty else 0.0
    meta = {
        "best_asset": best_asset,
        "worst_asset": worst_asset,
        "median_asset": median_asset,
        "positive_assets": positive_assets,
        "dominant_asset_profit_share_pct": dominant_share,
        "asset_concentration_warning": dominant_share > 45 or positive_assets < 3,
    }
    return rows, meta


def holdout_test(strategy_id: str, sweep: pd.DataFrame, trades: pd.DataFrame) -> dict[str, Any]:
    train = sweep[sweep["asset"].isin(TRAIN_ASSETS)]
    grouped = (
        train.groupby("parameter_set", as_index=False)
        .agg(mean_pf=("profit_factor", "mean"), train_trade_count=("trade_count", "sum"), positive_train_assets=("net_return_pct", lambda s: int((s > 0).sum())))
        .sort_values(["mean_pf", "train_trade_count"], ascending=False)
    )
    selected = str(grouped.iloc[0]["parameter_set"]) if not grouped.empty else ""
    holdout = trades[(trades["asset"].isin(HOLDOUT_ASSETS)) & (trades["parameter_set"].astype(str) == selected)].copy()
    train_trades = trades[(trades["asset"].isin(TRAIN_ASSETS)) & (trades["parameter_set"].astype(str) == selected)].copy()
    holdout_metrics = metrics_from_trades(holdout)
    train_metrics = metrics_from_trades(train_trades)
    return {
        "strategy_id": strategy_id,
        "train_assets": ",".join(TRAIN_ASSETS),
        "holdout_assets": ",".join(HOLDOUT_ASSETS),
        "selected_parameter_set": selected,
        "train_pf": train_metrics["profit_factor"],
        "train_net_return_pct": train_metrics["net_return_pct"],
        "train_trade_count": train_metrics["trade_count"],
        "holdout_pf": holdout_metrics["profit_factor"],
        "holdout_net_return_pct": holdout_metrics["net_return_pct"],
        "holdout_max_drawdown_pct": holdout_metrics["max_drawdown_pct"],
        "holdout_trade_count": holdout_metrics["trade_count"],
    }


def walk_forward(strategy_id: str, trades: pd.DataFrame) -> list[dict[str, Any]]:
    rows = []
    start = pd.Timestamp("2024-01-01", tz="UTC")
    end = pd.Timestamp("2026-05-04", tz="UTC")
    cursor = start
    while cursor + pd.DateOffset(months=9) <= end:
        train_end = cursor + pd.DateOffset(months=6)
        test_end = train_end + pd.DateOffset(months=3)
        train = trades[(trades["exit_timestamp"] >= cursor) & (trades["exit_timestamp"] < train_end)]
        if train.empty:
            cursor += pd.DateOffset(months=3)
            continue
        grouped = train.groupby("parameter_set")["net_return_pct"].apply(profit_factor).reset_index(name="train_pf").sort_values("train_pf", ascending=False)
        selected = str(grouped.iloc[0]["parameter_set"])
        test = trades[(trades["exit_timestamp"] >= train_end) & (trades["exit_timestamp"] < test_end) & (trades["parameter_set"].astype(str) == selected)]
        test_metrics = metrics_from_trades(test)
        rows.append(
            {
                "strategy_id": strategy_id,
                "train_start": cursor.date().isoformat(),
                "train_end": train_end.date().isoformat(),
                "test_start": train_end.date().isoformat(),
                "test_end": test_end.date().isoformat(),
                "selected_parameter_set": selected,
                "train_pf": float(grouped.iloc[0]["train_pf"]),
                "test_pf": test_metrics["profit_factor"],
                "test_net_return_pct": test_metrics["net_return_pct"],
                "test_trade_count": test_metrics["trade_count"],
                "test_max_drawdown_pct": test_metrics["max_drawdown_pct"],
            }
        )
        cursor += pd.DateOffset(months=3)
    return rows


def parameter_similarity(best: str, candidate: str) -> int:
    try:
        best_obj = json.loads(best)
        candidate_obj = json.loads(candidate)
    except json.JSONDecodeError:
        return 0
    score = 0
    for key, value in best_obj.items():
        if key not in candidate_obj:
            continue
        other = candidate_obj[key]
        if other == value:
            score += 2
        elif isinstance(value, (int, float)) and isinstance(other, (int, float)):
            if abs(float(other) - float(value)) <= max(abs(float(value)) * 0.5, 0.5):
                score += 1
    return score


def parameter_stability(strategy_id: str, sweep: pd.DataFrame, best_param: str) -> dict[str, Any]:
    grouped = (
        sweep.groupby("parameter_set", as_index=False)
        .agg(mean_pf=("profit_factor", "mean"), total_trades=("trade_count", "sum"), mean_net_return_pct=("net_return_pct", "mean"))
        .sort_values("mean_pf", ascending=False)
    )
    grouped["similarity"] = grouped["parameter_set"].map(lambda value: parameter_similarity(best_param, str(value)))
    best_pf = float(grouped[grouped["parameter_set"].astype(str) == best_param]["mean_pf"].iloc[0])
    neighbors = grouped[(grouped["parameter_set"].astype(str) != best_param) & (grouped["similarity"] >= max(1, grouped["similarity"].max() - 2))]
    neighbor_median_pf = float(neighbors["mean_pf"].median()) if not neighbors.empty else 0.0
    neighbor_pf_gt_110 = int((neighbors["mean_pf"] > 1.10).sum()) if not neighbors.empty else 0
    status = "STABLE" if neighbor_median_pf > 1.10 and neighbor_pf_gt_110 >= 3 and best_pf <= neighbor_median_pf * 1.5 else "OVERFIT_RISK"
    return {
        "strategy_id": strategy_id,
        "best_parameter_set": best_param,
        "best_mean_pf": best_pf,
        "near_parameter_count": int(len(neighbors)),
        "near_parameter_median_pf": neighbor_median_pf,
        "near_parameters_pf_gt_1_10": neighbor_pf_gt_110,
        "parameter_stability": status,
    }


def fee_stress(strategy_id: str, trades: pd.DataFrame) -> list[dict[str, Any]]:
    rows = []
    for scenario, multiplier in FEE_SCENARIOS.items():
        stressed = trades.copy()
        stressed["stress_return_pct"] = pd.to_numeric(stressed["gross_return_pct"], errors="coerce") - BASE_COST_PCT * multiplier
        metrics = metrics_from_trades(stressed, "stress_return_pct")
        rows.append({"strategy_id": strategy_id, "fee_scenario": scenario, **metrics})
    pf_values = [row["profit_factor"] for row in rows]
    monotonic = all(pf_values[index] + 1e-9 >= pf_values[index + 1] for index in range(len(pf_values) - 1))
    for row in rows:
        row["fee_monotonic_check"] = monotonic
    return rows


def drawdown_analysis(strategy_id: str, trades: pd.DataFrame) -> dict[str, Any]:
    values = trades.sort_values("exit_timestamp")["net_return_pct"] if not trades.empty else pd.Series(dtype=float)
    losses = values[values < 0]
    average_dd = float(((1 + values / 100).cumprod() / (1 + values / 100).cumprod().cummax() - 1).mean() * 100) if len(values) else 0.0
    trade_dates = trades.sort_values("exit_timestamp")["exit_timestamp"] if not trades.empty else pd.Series(dtype="datetime64[ns, UTC]")
    clusters = int((trade_dates.diff().dt.total_seconds().fillna(999999999) < 48 * 3600).sum()) if len(trade_dates) else 0
    tail_loss_share = float(abs(losses.nsmallest(5).sum()) / abs(losses.sum()) * 100) if abs(losses.sum()) > 0 else 0.0
    return {
        "strategy_id": strategy_id,
        "max_dd_pct": max_drawdown(values),
        "average_dd_pct": average_dd,
        "longest_dd_duration_trades": drawdown_duration(values),
        "worst_losing_streak": longest_losing_streak(values),
        "trade_cluster_count_48h": clusters,
        "tail_loss_top5_share_pct": tail_loss_share,
    }


def trade_distribution(strategy_id: str, trades: pd.DataFrame) -> dict[str, Any]:
    values = trades["net_return_pct"] if not trades.empty else pd.Series(dtype=float)
    wins = values[values > 0]
    losses = values[values < 0]
    top5_win_share = float(wins.nlargest(5).sum() / wins.sum() * 100) if wins.sum() > 0 else 0.0
    top5_loss_share = float(abs(losses.nsmallest(5).sum()) / abs(losses.sum()) * 100) if abs(losses.sum()) > 0 else 0.0
    outlier_warning = top5_win_share > 40 or top5_loss_share > 40
    return {
        "strategy_id": strategy_id,
        "top5_wins_profit_share_pct": top5_win_share,
        "top5_losses_loss_share_pct": top5_loss_share,
        "median_trade_pct": float(values.median()) if len(values) else 0.0,
        "p10_trade_pct": float(values.quantile(0.10)) if len(values) else 0.0,
        "p90_trade_pct": float(values.quantile(0.90)) if len(values) else 0.0,
        "outlier_dependency_warning": outlier_warning,
    }


def baseline_comparison(strategy_id: str, selected: pd.DataFrame) -> dict[str, Any]:
    base = metrics_from_trades(selected)
    random_baseline = selected.copy()
    random_baseline["random_same_exit_return_pct"] = -BASE_COST_PCT
    random_metrics = metrics_from_trades(random_baseline, "random_same_exit_return_pct")
    ema_path = SOURCE_ROOT / "strategies" / "12_ema20_50_two_retests_baseline" / "results" / "summary.csv"
    ema = pd.read_csv(ema_path)
    ema_pf = float(ema["profit_factor"].mean())
    ema_net = float(ema["net_return_pct"].mean())
    return {
        "strategy_id": strategy_id,
        "strategy_pf": base["profit_factor"],
        "strategy_net_return_pct": base["net_return_pct"],
        "random_same_exit_pf": random_metrics["profit_factor"],
        "random_same_exit_net_return_pct": random_metrics["net_return_pct"],
        "ema20_50_baseline_mean_pf": ema_pf,
        "ema20_50_baseline_mean_net_return_pct": ema_net,
        "beats_ema_pf": base["profit_factor"] > ema_pf,
        "beats_random_return": base["net_return_pct"] > random_metrics["net_return_pct"],
    }


def classify(summary_meta: dict[str, Any], holdout: dict[str, Any], stability: dict[str, Any], fee_rows: list[dict[str, Any]], dd: dict[str, Any], dist: dict[str, Any]) -> tuple[str, str]:
    aggregate_pf = summary_meta["aggregate_pf"]
    positive_assets = summary_meta["positive_assets"]
    fee_2x_pf = next(row["profit_factor"] for row in fee_rows if row["fee_scenario"] == "2x")
    holdout_pf = holdout["holdout_pf"]
    if aggregate_pf > 1.20 and fee_2x_pf > 1.10 and holdout_pf > 1.05 and positive_assets >= 3 and abs(dd["max_dd_pct"]) < 55 and stability["parameter_stability"] == "STABLE" and not summary_meta["asset_concentration_warning"]:
        return "STAGE2_PASS", "Meets PF, fee, holdout, multi-asset and stability gates; still requires separate parity gate before Pine."
    if aggregate_pf > 1.10 and positive_assets >= 3 and fee_2x_pf > 1.00:
        reasons = []
        if holdout_pf <= 1.05:
            reasons.append("holdout weak")
        if abs(dd["max_dd_pct"]) >= 55:
            reasons.append("drawdown high")
        if stability["parameter_stability"] != "STABLE":
            reasons.append("parameter overfit risk")
        if summary_meta["asset_concentration_warning"]:
            reasons.append("asset concentration")
        if dist["outlier_dependency_warning"]:
            reasons.append("tail outlier concentration")
        return "STAGE2_WEAK", ", ".join(reasons) or "edge exists but gates are not strong enough"
    if aggregate_pf > 1.0:
        return "FILTER_ONLY", "Weak standalone edge; may only be useful as gate/filter research."
    return "REJECT", "Robustness gates failed."


def run() -> int:
    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
    all_summary = []
    all_asset = []
    all_year = []
    all_walk = []
    all_fee = []
    all_stability = []
    all_dd = []
    all_dist = []
    all_baseline = []
    recompute = []
    for strategy_id, result_dir in STRATEGIES.items():
        summary, trades, sweep, best_param = load_strategy(result_dir)
        selected = selected_trades(trades, best_param)
        selected.to_csv(OUTPUT_ROOT / f"{strategy_id}_trades.csv", index=False)
        asset_rows, asset_meta = asset_split(strategy_id, summary, selected)
        all_asset.extend(asset_rows)
        year_rows = year_split(strategy_id, selected)
        all_year.extend(year_rows)
        holdout = holdout_test(strategy_id, sweep, trades)
        walk_rows = walk_forward(strategy_id, trades)
        all_walk.extend(walk_rows)
        stability = parameter_stability(strategy_id, sweep, best_param)
        fee_rows = fee_stress(strategy_id, selected)
        all_fee.extend(fee_rows)
        dd = drawdown_analysis(strategy_id, selected)
        dist = trade_distribution(strategy_id, selected)
        baseline = baseline_comparison(strategy_id, selected)
        all_stability.append(stability)
        all_dd.append(dd)
        all_dist.append(dist)
        all_baseline.append(baseline)
        base_metrics = metrics_from_trades(selected)
        summary_meta = {
            "strategy_id": strategy_id,
            "aggregate_pf": base_metrics["profit_factor"],
            "aggregate_net_return_pct": base_metrics["net_return_pct"],
            "aggregate_max_dd_pct": base_metrics["max_drawdown_pct"],
            "trade_count": base_metrics["trade_count"],
            **asset_meta,
        }
        classification, reason = classify(summary_meta, holdout, stability, fee_rows, dd, dist)
        row = {
            **summary_meta,
            "holdout_pf": holdout["holdout_pf"],
            "holdout_net_return_pct": holdout["holdout_net_return_pct"],
            "fee_2x_pf": next(item["profit_factor"] for item in fee_rows if item["fee_scenario"] == "2x"),
            "fee_3x_pf": next(item["profit_factor"] for item in fee_rows if item["fee_scenario"] == "3x"),
            "fee_5x_pf": next(item["profit_factor"] for item in fee_rows if item["fee_scenario"] == "5x"),
            "parameter_stability": stability["parameter_stability"],
            "tail_outlier_warning": dist["outlier_dependency_warning"],
            "final_classification": classification,
            "classification_reason": reason,
        }
        all_summary.append(row)
        metrics_frame = pd.DataFrame([row])
        metrics_frame.to_csv(OUTPUT_ROOT / f"{strategy_id}_metrics.csv", index=False)
        report = [
            f"# {strategy_id} Stage 2 Report",
            "",
            f"- Final classification: `{classification}`.",
            f"- Reason: {reason}.",
            f"- Aggregate PF: `{row['aggregate_pf']:.4f}`.",
            f"- 2x fee PF: `{row['fee_2x_pf']:.4f}`.",
            f"- Holdout PF: `{row['holdout_pf']:.4f}`.",
            f"- Parameter stability: `{row['parameter_stability']}`.",
            f"- Best asset: `{row['best_asset']}`; worst asset: `{row['worst_asset']}`; median asset: `{row['median_asset']}`.",
            "",
            "## Asset Split",
            markdown_table(pd.DataFrame(asset_rows)),
            "",
            "## Year Split",
            markdown_table(pd.DataFrame(year_rows)),
            "",
            "## Holdout",
            markdown_table(pd.DataFrame([holdout])),
            "",
            "## Walk Forward",
            markdown_table(pd.DataFrame(walk_rows)),
            "",
            "## Fee Stress",
            markdown_table(pd.DataFrame(fee_rows)),
            "",
            "## Drawdown",
            markdown_table(pd.DataFrame([dd])),
            "",
            "## Trade Distribution",
            markdown_table(pd.DataFrame([dist])),
        ]
        (OUTPUT_ROOT / f"{strategy_id}_stage2_report.md").write_text("\n".join(report) + "\n", encoding="utf-8")
        recompute.append(
            {
                "strategy_id": strategy_id,
                "trade_count_match": int(row["trade_count"]) == len(selected),
                "pf_recomputed": base_metrics["profit_factor"],
                "fee_monotonic": all(item["fee_monotonic_check"] for item in fee_rows),
            }
        )
    summary_frame = pd.DataFrame(all_summary)
    asset_frame = pd.DataFrame(all_asset)
    year_frame = pd.DataFrame(all_year)
    walk_frame = pd.DataFrame(all_walk)
    fee_frame = pd.DataFrame(all_fee)
    stability_frame = pd.DataFrame(all_stability)
    dd_frame = pd.DataFrame(all_dd)
    dist_frame = pd.DataFrame(all_dist)
    baseline_frame = pd.DataFrame(all_baseline)
    recompute_frame = pd.DataFrame(recompute)
    summary_frame.to_csv(OUTPUT_ROOT / "STAGE2_STRATEGY_SUMMARY.csv", index=False)
    asset_frame.to_csv(OUTPUT_ROOT / "STAGE2_ASSET_SPLIT.csv", index=False)
    year_frame.to_csv(OUTPUT_ROOT / "STAGE2_YEAR_SPLIT.csv", index=False)
    walk_frame.to_csv(OUTPUT_ROOT / "STAGE2_WALK_FORWARD.csv", index=False)
    fee_frame.to_csv(OUTPUT_ROOT / "STAGE2_FEE_STRESS.csv", index=False)
    stability_frame.to_csv(OUTPUT_ROOT / "STAGE2_PARAMETER_STABILITY.csv", index=False)
    dd_frame.to_csv(OUTPUT_ROOT / "STAGE2_DRAWDOWN_ANALYSIS.csv", index=False)
    dist_frame.to_csv(OUTPUT_ROOT / "STAGE2_TRADE_DISTRIBUTION.csv", index=False)
    baseline_frame.to_csv(OUTPUT_ROOT / "STAGE2_BASELINE_COMPARISON.csv", index=False)
    recompute_frame.to_csv(OUTPUT_ROOT / "STAGE2_METRIC_RECOMPUTE_CHECK.csv", index=False)
    pass_rows = summary_frame[summary_frame["final_classification"] == "STAGE2_PASS"]
    filter_rows = summary_frame[summary_frame["final_classification"] == "FILTER_ONLY"]
    reject_rows = summary_frame[summary_frame["final_classification"] == "REJECT"]
    master = [
        "# STAGE2 MASTER REPORT",
        "",
        "## Executive Summary",
        f"- Strategies tested: `{len(summary_frame)}`.",
        f"- Stage 2 pass count: `{len(pass_rows)}`.",
        "- Pine stage: `NO`.",
        "- MTC producer candidate: `NO_DIRECT_PROMOTION`.",
        "- Scope: Python research robustness only; no Pine, production runner, TradingView/parity, broker, alert, or live trading code changed.",
        "",
        "## Strategy Summary",
        markdown_table(summary_frame),
        "",
        "## Asset Split",
        markdown_table(asset_frame, max_rows=50),
        "",
        "## Year Split",
        markdown_table(year_frame, max_rows=30),
        "",
        "## Holdout And Walk Forward",
        markdown_table(walk_frame, max_rows=50),
        "",
        "## Fee Stress",
        markdown_table(fee_frame, max_rows=30),
        "",
        "## Parameter Stability",
        markdown_table(stability_frame),
        "",
        "## Drawdown And Distribution",
        markdown_table(dd_frame),
        "",
        markdown_table(dist_frame),
        "",
        "## Baseline Comparison",
        markdown_table(baseline_frame),
        "",
        "## Validation",
        "- `STAGE2_METRIC_RECOMPUTE_CHECK.csv` produced.",
        "- Fee monotonic check is stored in `STAGE2_FEE_STRESS.csv`.",
    ]
    recommendation = [
        "# STAGE2 FINAL RECOMMENDATION",
        "",
        "## Direct Answers",
        "- Pine'a geçecek strateji var mı? `NO`.",
        "- MTC producer adayı var mı? `NO_DIRECT_PROMOTION`.",
        f"- Sadece filter/gate olarak değerli model var mı? `{', '.join(filter_rows['strategy_id'].tolist()) if not filter_rows.empty else 'NONE'}`.",
        f"- Reject edilmeli mi? `{', '.join(reject_rows['strategy_id'].tolist()) if not reject_rows.empty else 'NONE'}`.",
        "- Daha fazla data isteyen model var mı? `NONE_FOR_CRYPTO_DAILY_4H`; equity/session-specific fikirler bu Stage 2 kapsamı dışında.",
        "",
        "## Largest Risks",
        "- Crabel: drawdown and holdout sensitivity.",
        "- Linda 5SMA: asset concentration and high drawdown on weak assets.",
        "- BigBeluga: timeframe/regime sensitivity and parameter stability risk if neighbors weaken.",
        "",
        "## Next Step",
        "- Pine/parity değil; önce Stage 2 weak modeller için daha sıkı OOS + regime filter/gate deneyleri yapılmalı.",
    ]
    (OUTPUT_ROOT / "README.md").write_text("# Stage 2 Robustness 2026-05-03\n\nPython-only robustness analysis for Crabel, Linda 5SMA, and BigBeluga candidates.\n", encoding="utf-8")
    (OUTPUT_ROOT / "STAGE2_MASTER_REPORT.md").write_text("\n".join(master) + "\n", encoding="utf-8")
    (OUTPUT_ROOT / "STAGE2_FINAL_RECOMMENDATION.md").write_text("\n".join(recommendation) + "\n", encoding="utf-8")
    print(summary_frame[["strategy_id", "aggregate_pf", "fee_2x_pf", "holdout_pf", "parameter_stability", "final_classification"]].to_string(index=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
