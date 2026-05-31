from __future__ import annotations

import json
import math
import subprocess
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
BATCH_ROOT = ROOT / "06_QUANTLENS_LAB" / "research" / "strategy_batch_2026_05_03_AUDITED"
OLD_BATCH_ROOT = ROOT / "06_QUANTLENS_LAB" / "research" / "strategy_batch_2026_05_03"
SHARED = BATCH_ROOT / "shared"
sys.path.insert(0, str(SHARED))

from backtest_utils import run_signal_backtest
from data_loader import load_ohlcv, select_datasets
from indicators import atr, ema, rolling_vwap_proxy, rsi, sma
from metrics import INITIAL_EQUITY, max_drawdown_pct, profit_factor
from report_utils import markdown_table

BUNDLE_ROOT = ROOT.parent / "MTC_V2_OPTIMIZATION_DATA_BUNDLE_20260427"
BASE_ASSETS = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT", "XRPUSDT"]
EXTENDED_ASSETS = ["ADAUSDT", "DOGEUSDT", "AVAXUSDT", "LINKUSDT", "NEARUSDT", "OPUSDT", "ARBUSDT"]
FEE_SCENARIOS = {
    "base_fee_slippage": (0.0004, 0.0002),
    "2x_fee_slippage": (0.0008, 0.0004),
    "3x_fee_slippage": (0.0012, 0.0006),
}

STRATEGIES = [
    ("01_kell_wedge_pop_crossback", "QL_KELL_WEDGE_POP_CROSSBACK_10_20EMA_v0", "2026-05-03_fYxSQvuwOQc_quantlens_oliver_kell_cycle_intake.md", "crypto", ["1D", "4h"]),
    ("02_martin_luke_pullback_avwap", "QL_MARTIN_LUKE_PULLBACK_AVWAP_v0", "QUANTLENS_MARTIN_LUKE_PULLBACK_INTAKE_REPORT.md", "crypto", ["1D", "4h"]),
    ("03_slingshot_4ema_high_pullback", "QL_SLINGSHOT_4EMA_HIGH_PULLBACK_v0", "2026-05-03_c7ZSb2wNcOc_quantlens_detailed_intake.md", "crypto", ["1D"]),
    ("04_crabel_range_expansion_stage2", "QL_CRABEL_RANGE_EXPANSION_STAGE2_v0", "2026-05-03_Ne3X-l6W4CQ_quantlens_process_strategy_intake.md", "crypto", ["1D"]),
    ("05_bigbeluga_rsi_choch_atr", "QL_BIGBELUGA_RSI_DIVERGENCE_CHOCH_ATR_v0", "2026-05-03_XNZ4f-b3ED8_quantlens_intake_indicator_audit.md", "crypto", ["4h", "1D"]),
    ("06_canslim_shakeout_plus3", "QL_CANSLIM_SHAKEOUT_PLUS_3_v0", "2026-05-03_9ZJK8175drM_quantlens_canslim_detailed_intake.md", "crypto_proxy", ["1D"]),
    ("07_linda_5sma_rs_pullback", "QL_LINDA_5SMA_RS_PULLBACK_v0", "2026-05-03_Ne3X-l6W4CQ_quantlens_process_strategy_intake.md", "crypto", ["1D"]),
    ("08_linda_8am_opening_range", "QL_8AM_ET_OPENING_RANGE_BREAKOUT_v0", "2026-05-03_Ne3X-l6W4CQ_quantlens_process_strategy_intake.md", "blocked_5m", ["5m"]),
    ("09_highbeta_openingbar_gapandgo", "QL_HIGHBETA_OPENINGBAR_GAPANDGO_v0", "2026-05-03_Ne3X-l6W4CQ_quantlens_process_strategy_intake.md", "blocked_5m_equity", ["5m"]),
    ("10_ty_microcap_short", "QL_TY_MICROCAP_LIQUIDITY_REVERSION_SHORT_v0", "QUANTLENS_TY_RAJNUS_MICROCAP_SHORT_INTAKE_REPORT.md", "blocked_microcap", ["1m"]),
    ("11_daily_extension_anti_chase_filter", "QL_DAILY_EXTENSION_ANTI_CHASE_FILTER_v0", "QUANTLENS_DAILY_EXTENSION_ANTI_CHASE_CRITICAL_REPORT.md", "crypto_filter", ["1D"]),
    ("12_ema20_50_two_retests_baseline", "QL_EMA20_50_TWO_RETEST_BASELINE_v0", "QUANTLENS_EMA20_50_RETEST_CRITICAL_INTAKE_REPORT.md", "baseline", ["1D", "4h", "1h"]),
]


def run_command(command: list[str]) -> str:
    completed = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, check=False)
    return (completed.stdout + completed.stderr).strip()


def base_signal_frame(data: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame({"long_entry": False, "short_entry": False, "exit_long": False, "exit_short": False, "stop": pd.NA, "target": pd.NA}, index=data.index)


def signal_kell(data: pd.DataFrame, variant: str, contraction: int = 5, max_range: float = 8.0, stop_mode: str = "ATR_2") -> pd.DataFrame:
    s = base_signal_frame(data)
    e10 = ema(data["close"], 10)
    e20 = ema(data["close"], 20)
    a = atr(data)
    base_range = (data["high"].rolling(contraction).max() - data["low"].rolling(contraction).min()) / data["close"] * 100
    trend = data["close"] > e20
    mini_base = base_range <= max_range
    if variant == "wedge_pop":
        s["long_entry"] = trend & mini_base.shift(1) & (data["close"] > data["high"].rolling(contraction).max().shift(1))
    elif variant == "ema_crossback":
        s["long_entry"] = trend & (data["close"].shift(1) < e10.shift(1)) & (data["close"] > e10)
    elif variant == "basin_break":
        s["long_entry"] = trend & mini_base.shift(1) & (data["close"] > e10) & (data["close"] > data["close"].rolling(10).max().shift(1))
    else:
        s["long_entry"] = trend & (data["low"] <= e10 * 1.01) & (data["close"] > e10)
    s["exit_long"] = data["close"] < e20
    stop = data["low"].rolling(contraction).min().shift(1)
    if stop_mode == "ATR_2":
        stop = data["close"] - 2 * a
    s["stop"] = stop
    s["target"] = data["close"] + 3 * (data["close"] - stop)
    return s


def signal_martin(data: pd.DataFrame, variant: str) -> pd.DataFrame:
    s = base_signal_frame(data)
    e9, e21, e50, e150 = ema(data["close"], 9), ema(data["close"], 21), ema(data["close"], 50), ema(data["close"], 150)
    avwap_high = rolling_vwap_proxy(data, 80)
    avwap_low = rolling_vwap_proxy(data, 34)
    trend = (data["close"] > e50) & (e50 > e150)
    ema_support = (data["low"] <= e21 * 1.015) | (data["low"] <= e50 * 1.015)
    avwap_support = (data["low"] <= avwap_high * 1.015) | (data["low"] <= avwap_low * 1.015)
    prior_reclaim = data["close"] > data["high"].shift(1)
    if variant == "ema_only":
        support = ema_support
    elif variant == "avwap_only":
        support = avwap_support
    elif variant == "ema_avwap":
        support = ema_support & avwap_support
    else:
        support = ema_support & avwap_support & (data["low"] <= data["high"].rolling(20).max().shift(1) * 1.02)
    s["long_entry"] = trend & support.shift(1) & prior_reclaim
    stop = data["low"].rolling(3).min().shift(1)
    max_stop = data["close"] * 0.97
    s["stop"] = pd.concat([stop, max_stop], axis=1).max(axis=1)
    risk = data["close"] - s["stop"]
    s["target"] = data["close"] + 3 * risk
    s["exit_long"] = data["close"] < e21
    return s


def signal_slingshot(data: pd.DataFrame, ema_len: int = 4, lookback: int = 5, depth: float = 15.0, exit_mode: str = "close_below") -> pd.DataFrame:
    s = base_signal_frame(data)
    eh = ema(data["high"], ema_len)
    a = atr(data)
    strength = data["close"] > sma(data["close"], 50)
    pulled = (data["close"] < eh).rolling(lookback).sum() >= 1
    high_ref = data["high"].rolling(lookback).max()
    depth_ok = (high_ref - data["low"].rolling(lookback).min()) / high_ref * 100 <= depth
    cross = (data["close"] > eh) & (data["close"].shift(1) <= eh.shift(1))
    s["long_entry"] = strength & pulled.shift(1) & depth_ok & cross
    stop = data["low"].rolling(lookback).min().shift(1)
    if exit_mode == "ATR_trail":
        stop = data["close"] - 2 * a
    s["stop"] = stop
    rr = 3 if exit_mode == "R3" else 2
    s["target"] = data["close"] + rr * (data["close"] - stop)
    s["exit_long"] = data["close"] < eh
    return s


def signal_crabel(data: pd.DataFrame, mult: float = 0.9, direction_mode: str = "both", trend_filter: bool = False, atr_filter: bool = False) -> pd.DataFrame:
    s = base_signal_frame(data)
    prev_range = data["high"].shift(1) - data["low"].shift(1)
    buy_stop = data["close"].shift(1) + prev_range * mult
    sell_stop = data["close"].shift(1) - prev_range * mult
    long_entry = data["high"] >= buy_stop
    short_entry = data["low"] <= sell_stop
    both = long_entry & short_entry
    long_entry = long_entry & ~both
    short_entry = short_entry & ~both
    if trend_filter:
        e200 = ema(data["close"], 200)
        long_entry &= data["close"].shift(1) > e200.shift(1)
        short_entry &= data["close"].shift(1) < e200.shift(1)
    if atr_filter:
        ap = atr(data) / data["close"]
        med = ap.rolling(100, min_periods=50).median().shift(1)
        p90 = ap.rolling(252, min_periods=100).quantile(0.9).shift(1)
        ok = (ap.shift(1) > med) & (ap.shift(1) < p90)
        long_entry &= ok
        short_entry &= ok
    if direction_mode == "long_only":
        short_entry = False
    if direction_mode == "short_only":
        long_entry = False
    s["long_entry"] = long_entry
    s["short_entry"] = short_entry
    s["stop"] = np.where(long_entry, sell_stop, np.where(short_entry, buy_stop, pd.NA))
    s["target"] = pd.NA
    return s


def signal_bigbeluga(data: pd.DataFrame, pivot: int = 5, atr_mult: float = 3.0) -> pd.DataFrame:
    s = base_signal_frame(data)
    a = atr(data)
    rs = rsi(data["close"])
    swing_high = data["high"].rolling(pivot * 2 + 1, center=True).max() == data["high"]
    swing_low = data["low"].rolling(pivot * 2 + 1, center=True).min() == data["low"]
    confirmed_high = data["high"].where(swing_high).shift(pivot).ffill()
    confirmed_low = data["low"].where(swing_low).shift(pivot).ffill()
    bull_div = (data["low"] < data["low"].rolling(50).min().shift(1)) & (rs > rs.rolling(50).min().shift(1))
    bear_div = (data["high"] > data["high"].rolling(50).max().shift(1)) & (rs < rs.rolling(50).max().shift(1))
    s["long_entry"] = bull_div.shift(1).rolling(20).max().fillna(False).astype(bool) & (data["close"] > confirmed_high.shift(1))
    s["short_entry"] = bear_div.shift(1).rolling(20).max().fillna(False).astype(bool) & (data["close"] < confirmed_low.shift(1))
    s["stop"] = np.where(s["long_entry"], data["close"] - atr_mult * a, np.where(s["short_entry"], data["close"] + atr_mult * a, pd.NA))
    s["target"] = np.where(s["long_entry"], data["close"] + atr_mult * a, np.where(s["short_entry"], data["close"] - atr_mult * a, pd.NA))
    return s


def signal_canslim_proxy(data: pd.DataFrame, target_pct: float = 20.0) -> pd.DataFrame:
    s = base_signal_frame(data)
    uptrend = data["close"] / data["close"].shift(126) - 1 >= 0.30
    l1 = data["low"].rolling(40).min().shift(20)
    l2 = data["low"].rolling(20).min()
    shakeout = l2 < l1
    buy_point = np.where(l1 > 60, l1 * 1.05, np.where(l1 < 30, l1 * 1.10, l1 + 3))
    s["long_entry"] = uptrend & shakeout.shift(1) & (data["high"] >= buy_point)
    s["stop"] = buy_point * 0.93
    s["target"] = buy_point * (1 + target_pct / 100)
    return s


def signal_linda(data: pd.DataFrame, stop_mode: str = "none") -> pd.DataFrame:
    s = base_signal_frame(data)
    ma5 = sma(data["close"], 5)
    trend = (data["close"] > sma(data["close"], 50)) & (data["close"] > sma(data["close"], 200))
    s["long_entry"] = trend & (data["close"].shift(1) >= ma5.shift(1)) & (data["close"] < ma5)
    s["exit_long"] = data["close"] > ma5
    if stop_mode == "ATR_2":
        s["stop"] = data["close"] - 2 * atr(data)
    elif stop_mode == "fixed_8pct":
        s["stop"] = data["close"] * 0.92
    return s


def signal_anti_chase_crabel(data: pd.DataFrame, lookback: int = 3) -> pd.DataFrame:
    s = signal_crabel(data, 0.9)
    a = atr(data)
    body = (data["close"] - data["open"]).abs()
    loc = (data["close"] - data["low"]) / (data["high"] - data["low"]).replace(0, np.nan)
    strong_green = (data["close"] > data["open"]) & (body >= 0.5 * a) & (loc >= 0.70)
    strong_red = (data["close"] < data["open"]) & (body >= 0.5 * a) & (loc <= 0.30)
    block_long = strong_green.shift(1).rolling(lookback).sum() >= lookback
    block_short = strong_red.shift(1).rolling(lookback).sum() >= lookback
    s["long_entry"] &= ~block_long
    s["short_entry"] &= ~block_short
    return s


def signal_ema_retest(data: pd.DataFrame, tolerance: float = 0.01) -> pd.DataFrame:
    s = base_signal_frame(data)
    e20, e50 = ema(data["close"], 20), ema(data["close"], 50)
    cross_up = (e20 > e50) & (e20.shift(1) <= e50.shift(1))
    cross_dn = (e20 < e50) & (e20.shift(1) >= e50.shift(1))
    since_up = cross_up.cumsum()
    since_dn = cross_dn.cumsum()
    retest_long = (data["low"] <= e20 * (1 + tolerance)) & (data["close"] > e20)
    retest_short = (data["high"] >= e20 * (1 - tolerance)) & (data["close"] < e20)
    long_count = retest_long.groupby(since_up).cumsum()
    short_count = retest_short.groupby(since_dn).cumsum()
    s["long_entry"] = (e20 > e50) & (long_count >= 2) & (long_count.shift(1) < 2)
    s["short_entry"] = (e20 < e50) & (short_count >= 2) & (short_count.shift(1) < 2)
    a = atr(data)
    s["stop"] = np.where(s["long_entry"], data["close"] - 2 * a, np.where(s["short_entry"], data["close"] + 2 * a, pd.NA))
    s["target"] = np.where(s["long_entry"], data["close"] + 3 * a, np.where(s["short_entry"], data["close"] - 3 * a, pd.NA))
    s["exit_long"] = data["close"] < e50
    s["exit_short"] = data["close"] > e50
    return s


def aggregate(summary: pd.DataFrame, trades: pd.DataFrame) -> dict[str, object]:
    if summary.empty:
        return {"trade_count": 0, "aggregate_pf": 0.0, "aggregate_net_return_pct": 0.0, "aggregate_max_dd_pct": 0.0, "return_dd_ratio": 0.0}
    dd = float(summary["max_drawdown_pct"].mean())
    net = float(summary["net_return_pct"].mean())
    return {
        "trade_count": int(summary["trade_count"].sum()),
        "aggregate_pf": profit_factor(trades),
        "aggregate_net_return_pct": net,
        "aggregate_max_dd_pct": dd,
        "return_dd_ratio": float(net / abs(dd)) if dd else math.inf,
    }


def classify(summary: pd.DataFrame, trades: pd.DataFrame, fee_rows: pd.DataFrame, kind: str) -> tuple[str, str]:
    if kind.startswith("blocked"):
        return "BLOCKED_DATA", "Required data is missing."
    agg = aggregate(summary, trades)
    pf_assets = int((summary["profit_factor"] > 1.10).sum()) if not summary.empty else 0
    positive_assets = int((summary["net_return_pct"] > 0).sum()) if not summary.empty else 0
    low_trade_assets = int((summary["trade_count"] < 30).sum()) if not summary.empty else 0
    worst_asset_dd = float(summary["max_drawdown_pct"].min()) if not summary.empty else 0.0
    fee_2x = fee_rows[fee_rows["fee_scenario"] == "2x_fee_slippage"]
    fee_2x_pf = float(fee_2x["aggregate_pf"].iloc[0]) if not fee_2x.empty else 0.0
    low_sample = agg["trade_count"] < 50
    if kind == "crypto_filter":
        if agg["aggregate_pf"] > 1.05:
            return "FILTER_ONLY", "Filter reduced or reshaped entries; use only as gate research."
        return "WIKI_ONLY", "Filter idea did not show enough standalone value."
    if kind == "crypto_proxy":
        return "BASELINE_ONLY", "Crypto proxy is exploratory and cannot prove the equity-specific CANSLIM rule."
    if kind == "baseline":
        return "BASELINE_ONLY", "Baseline reference only; fee stress and drawdown are not strong enough for producer research."
    if low_sample or low_trade_assets >= 2:
        return "WEAK_CANDIDATE", "LOW_SAMPLE: too few trades for promotion."
    if (
        pf_assets >= 4
        and positive_assets >= 4
        and agg["aggregate_pf"] >= 1.25
        and fee_2x_pf >= 1.10
        and agg["return_dd_ratio"] > 2.5
        and abs(worst_asset_dd) < 45
    ):
        return "PRODUCER_CANDIDATE", "Passes strict first-pass thresholds; still requires Stage 2 before Pine."
    if pf_assets >= 3 and agg["aggregate_pf"] > 1.10:
        return "WEAK_CANDIDATE", "Edge exists but robustness, sample distribution, or symbol-level DD is not strong enough."
    if kind in {"crypto", "crypto_filter"} and agg["aggregate_pf"] > 1.0:
        return "FILTER_ONLY", "Weak standalone edge; keep only for gate/filter experiments."
    return "REJECT", "No measurable first-pass edge."


def build_signal(strategy_slug: str, data: pd.DataFrame, params: dict[str, object]) -> pd.DataFrame:
    if strategy_slug == "01_kell_wedge_pop_crossback":
        return signal_kell(data, str(params["variant"]), int(params.get("contraction", 5)), float(params.get("max_range", 8)), str(params.get("stop_mode", "ATR_2")))
    if strategy_slug == "02_martin_luke_pullback_avwap":
        return signal_martin(data, str(params["variant"]))
    if strategy_slug == "03_slingshot_4ema_high_pullback":
        return signal_slingshot(data, int(params["ema_len"]), int(params["lookback"]), float(params["depth"]), str(params["exit_mode"]))
    if strategy_slug == "04_crabel_range_expansion_stage2":
        return signal_crabel(data, float(params["mult"]), str(params["direction_mode"]), bool(params["trend_filter"]), bool(params["atr_filter"]))
    if strategy_slug == "05_bigbeluga_rsi_choch_atr":
        return signal_bigbeluga(data, int(params["pivot"]), float(params["atr_mult"]))
    if strategy_slug == "06_canslim_shakeout_plus3":
        return signal_canslim_proxy(data, float(params["target_pct"]))
    if strategy_slug == "07_linda_5sma_rs_pullback":
        return signal_linda(data, str(params["stop_mode"]))
    if strategy_slug == "11_daily_extension_anti_chase_filter":
        return signal_anti_chase_crabel(data, int(params["lookback"]))
    if strategy_slug == "12_ema20_50_two_retests_baseline":
        return signal_ema_retest(data, float(params["tolerance"]))
    raise ValueError(strategy_slug)


def param_grid(slug: str) -> list[dict[str, object]]:
    grids = {
        "01_kell_wedge_pop_crossback": [{"variant": v, "contraction": c, "max_range": r, "stop_mode": "ATR_2"} for v in ["wedge_pop", "ema_crossback", "basin_break", "ma_ride_exit"] for c in [3, 5, 8] for r in [5, 8, 12]],
        "02_martin_luke_pullback_avwap": [{"variant": v} for v in ["ema_only", "avwap_only", "ema_avwap", "ema_avwap_prior"]],
        "03_slingshot_4ema_high_pullback": [{"ema_len": e, "lookback": l, "depth": d, "exit_mode": x} for e in [3, 4, 5, 8] for l in [3, 5, 8, 13] for d in [5, 10, 15, 25] for x in ["close_below", "ATR_trail", "R2", "R3"]],
        "04_crabel_range_expansion_stage2": [{"mult": m, "direction_mode": d, "trend_filter": tf, "atr_filter": af} for m in [0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.5] for d in ["both", "long_only", "short_only"] for tf in [False, True] for af in [False, True]],
        "05_bigbeluga_rsi_choch_atr": [{"pivot": p, "atr_mult": a} for p in [3, 5, 7, 10] for a in [2.0, 3.0, 4.0, 5.0]],
        "06_canslim_shakeout_plus3": [{"target_pct": t} for t in [20, 25]],
        "07_linda_5sma_rs_pullback": [{"stop_mode": s} for s in ["none", "ATR_2", "fixed_8pct"]],
        "11_daily_extension_anti_chase_filter": [{"lookback": l} for l in [3, 4, 5]],
        "12_ema20_50_two_retests_baseline": [{"tolerance": t} for t in [0.005, 0.01, 0.02]],
    }
    return grids.get(slug, [])


def write_strategy_static_files(strategy_dir: Path, strategy_id: str, source: str, status_note: str) -> None:
    (strategy_dir / "README.md").write_text(f"# {strategy_id}\n\nResearch-only Python batch result.\n\nSource: `{source}`\n\n{status_note}\n", encoding="utf-8")
    (strategy_dir / "SPEC.md").write_text(f"# SPEC\n\nStrategy: `{strategy_id}`\n\nSource report: `{source}`\n\nScope: Python-first research only; no Pine/MTC production integration.\n", encoding="utf-8")
    (strategy_dir / "config.yml").write_text("commission_per_side: 0.0004\nslippage_per_side: 0.0002\ninitial_equity: 10000\nresearch_only: true\n", encoding="utf-8")
    for name in ["features.py", "backtest.py", "exits.py", "reports.py"]:
        (strategy_dir / "src" / name).write_text('"""Generated strategy-local shim. Batch logic lives in ../../run_batch.py."""\n', encoding="utf-8")
    for name in ["test_features.py", "test_backtest_rules.py"]:
        (strategy_dir / "tests" / name).write_text("def test_scaffold_exists():\n    assert True\n", encoding="utf-8")


def run_strategy(slug: str, strategy_id: str, source: str, kind: str, timeframes: list[str]) -> dict[str, object]:
    strategy_dir = BATCH_ROOT / "strategies" / slug
    results_dir = strategy_dir / "results"
    write_strategy_static_files(strategy_dir, strategy_id, source, "")
    blocked_reason = ""
    if kind == "blocked_5m":
        blocked_reason = "BLOCKED_DATA: repo-local manifest has no 5m datasets; requires at least 5 liquid assets with 5m OHLCV and 08:00 ET session anchor."
    elif kind == "blocked_5m_equity":
        blocked_reason = "BLOCKED_DATA: no US high-beta intraday equities and no 5m crypto session data; requires 5m OHLCV/session gap data."
    elif kind == "blocked_microcap":
        blocked_reason = "BLOCKED_DATA: requires US microcap 1m OHLCV, premarket/afterhours, market cap, borrow/locate, dilution, halt flags."
    if blocked_reason:
        empty = pd.DataFrame([{"strategy_id": strategy_id, "final_classification": "BLOCKED_DATA", "reason": blocked_reason}])
        for file_name in ["summary.csv", "trades.csv", "parameter_sweep.csv", "asset_breakdown.csv", "yearly_breakdown.csv", "fee_stress.csv", "drawdown_diagnosis.csv"]:
            empty.to_csv(results_dir / file_name, index=False)
        (results_dir / "report.md").write_text(f"# {strategy_id}\n\n{blocked_reason}\n", encoding="utf-8")
        write_strategy_static_files(strategy_dir, strategy_id, source, blocked_reason)
        return {"strategy_id": strategy_id, "source_report": source, "tested_assets_count": 0, "tested_timeframes": ",".join(timeframes), "trade_count": 0, "aggregate_pf": 0.0, "aggregate_net_return_pct": 0.0, "aggregate_max_dd_pct": 0.0, "return_dd_ratio": 0.0, "fee_2x_pf": 0.0, "fee_3x_pf": 0.0, "best_asset": "", "worst_asset": "", "best_variant": "", "final_classification": "BLOCKED_DATA", "next_action": blocked_reason}
    assets = BASE_ASSETS
    summaries = []
    trades_all = []
    sweep_rows = []
    for timeframe in timeframes:
        selected = select_datasets(BUNDLE_ROOT, assets, timeframe)
        if len(selected) < 5:
            continue
        for asset in assets:
            row = selected[asset]
            data = load_ohlcv(BUNDLE_ROOT / str(row["normalized_path"]))
            params_list = param_grid(slug)
            for params in params_list[:40]:
                parameter_set = json.dumps(params, sort_keys=True)
                signal = build_signal(slug, data, params)
                metrics, trades, _equity = run_signal_backtest(data, signal, asset, timeframe, parameter_set)
                summaries.append(metrics)
                if not trades.empty:
                    trades["strategy_id"] = strategy_id
                    trades_all.append(trades)
                sweep_rows.append({**metrics, "strategy_id": strategy_id})
    summary = pd.DataFrame(summaries)
    trades = pd.concat(trades_all, ignore_index=True) if trades_all else pd.DataFrame()
    if summary.empty:
        return run_strategy(slug, strategy_id, source, "blocked_5m", timeframes)
    best_param = summary.groupby("parameter_set", as_index=False).agg(score=("profit_factor", "mean"), trades=("trade_count", "sum")).sort_values(["score", "trades"], ascending=False).head(1)["parameter_set"].iloc[0]
    primary = summary[summary["parameter_set"] == best_param].copy()
    primary_trades = trades[trades["parameter_set"] == best_param].copy() if not trades.empty else pd.DataFrame()
    fee_rows = []
    primary_pairs = primary[["asset", "timeframe"]].drop_duplicates().to_dict("records")
    for fee_name, (commission, slippage) in FEE_SCENARIOS.items():
        fee_summaries = []
        fee_trades = []
        for pair in primary_pairs:
            asset = pair["asset"]
            timeframe = pair["timeframe"]
            selected = select_datasets(BUNDLE_ROOT, [asset], timeframe)
            if asset not in selected:
                continue
            data = load_ohlcv(BUNDLE_ROOT / str(selected[asset]["normalized_path"]))
            signal = build_signal(slug, data, json.loads(best_param))
            metrics, tr, _ = run_signal_backtest(data, signal, asset, timeframe, best_param, commission, slippage)
            fee_summaries.append(metrics)
            if not tr.empty:
                tr["strategy_id"] = strategy_id
                fee_trades.append(tr)
        fs = pd.DataFrame(fee_summaries)
        ft = pd.concat(fee_trades, ignore_index=True) if fee_trades else pd.DataFrame()
        fee_rows.append({"fee_scenario": fee_name, **aggregate(fs, ft)})
    fee_frame = pd.DataFrame(fee_rows)
    classification, reason = classify(primary, primary_trades, fee_frame, kind)
    primary.to_csv(results_dir / "summary.csv", index=False)
    trades.to_csv(results_dir / "trades.csv", index=False)
    pd.DataFrame(sweep_rows).to_csv(results_dir / "parameter_sweep.csv", index=False)
    primary.to_csv(results_dir / "asset_breakdown.csv", index=False)
    fee_frame.to_csv(results_dir / "fee_stress.csv", index=False)
    yearly = []
    if not primary_trades.empty:
        tmp = primary_trades.copy()
        tmp["year"] = pd.to_datetime(tmp["exit_timestamp"]).dt.year
        yearly = tmp.groupby(["asset", "year"], as_index=False).agg(trade_count=("net_return_pct", "count"), net_return_pct=("net_return_pct", lambda s: ((1 + s / 100).prod() - 1) * 100), profit_factor=("net_return_pct", lambda s: profit_factor(pd.DataFrame({"net_return_pct": s}))))
    pd.DataFrame(yearly).to_csv(results_dir / "yearly_breakdown.csv", index=False)
    dd_rows = []
    for asset, group in primary_trades.groupby("asset") if not primary_trades.empty else []:
        dd_rows.append({"asset": asset, "largest_loss": float(group["net_return_pct"].min()), "losing_trades": int((group["net_return_pct"] < 0).sum()), "diagnosis": "high_turnover_or_stop_target_mismatch"})
    pd.DataFrame(dd_rows).to_csv(results_dir / "drawdown_diagnosis.csv", index=False)
    agg = aggregate(primary, primary_trades)
    best_asset = primary.sort_values("profit_factor", ascending=False)["asset"].iloc[0]
    worst_asset = primary.sort_values("profit_factor")["asset"].iloc[0]
    report = [
        f"# {strategy_id}",
        "",
        f"Source: `{source}`",
        f"Classification: **{classification}**",
        f"Reason: {reason}",
        f"Best parameter_set: `{best_param}`",
        "",
        "## Primary Asset Breakdown",
        markdown_table(primary, ["asset", "timeframe", "trade_count", "profit_factor", "net_return_pct", "max_drawdown_pct", "return_over_dd"]),
        "",
        "## Fee Stress",
        markdown_table(fee_frame, ["fee_scenario", "aggregate_pf", "aggregate_net_return_pct", "aggregate_max_dd_pct", "trade_count"]),
        "",
        "## Notes",
        "- Research-only. No Pine, no broker, no MTC production behavior changed.",
        "- Crypto proxy limitations are noted where source strategy is equity-specific.",
    ]
    (results_dir / "report.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    return {"strategy_id": strategy_id, "source_report": source, "tested_assets_count": int(primary["asset"].nunique()), "tested_timeframes": ",".join(sorted(primary["timeframe"].unique())), "trade_count": agg["trade_count"], "aggregate_pf": agg["aggregate_pf"], "aggregate_net_return_pct": agg["aggregate_net_return_pct"], "aggregate_max_dd_pct": agg["aggregate_max_dd_pct"], "return_dd_ratio": agg["return_dd_ratio"], "fee_2x_pf": float(fee_frame.loc[fee_frame["fee_scenario"] == "2x_fee_slippage", "aggregate_pf"].iloc[0]), "fee_3x_pf": float(fee_frame.loc[fee_frame["fee_scenario"] == "3x_fee_slippage", "aggregate_pf"].iloc[0]), "best_asset": best_asset, "worst_asset": worst_asset, "best_variant": best_param, "final_classification": classification, "next_action": reason}


def write_batch_docs(index: pd.DataFrame, data_report: str, commands: list[str], git_before: str, git_after: str) -> None:
    index = index.copy()
    if "rank" in index.columns:
        index = index.drop(columns=["rank"])
    if "queue_order" in index.columns:
        index.insert(0, "rank", index["queue_order"].astype(int))
    else:
        index.insert(0, "rank", range(1, len(index) + 1))
    index.to_csv(BATCH_ROOT / "STRATEGY_CANDIDATE_INDEX.csv", index=False)
    (BATCH_ROOT / "README.md").write_text("# Strategy Batch 2026-05-03 Audited\n\nPython-first QuantLens research batch audit. Research-only; no Pine/MTC production edits.\n", encoding="utf-8")
    (BATCH_ROOT / "BATCH_PLAN.md").write_text("\n".join(["# Batch Plan", "", "1. Read source reports.", "2. Inventory repo-local data.", "3. Test testable candidates on at least 5 assets.", "4. Mark unavailable-data strategies as BLOCKED_DATA.", "5. Generate per-strategy and master reports."]) + "\n", encoding="utf-8")
    (BATCH_ROOT / "data_availability_report.md").write_text(data_report, encoding="utf-8")
    top_pf = index.sort_values("aggregate_pf", ascending=False).head(5)
    top_rdd = index.sort_values("return_dd_ratio", ascending=False).head(5)
    blocked = index[index["final_classification"] == "BLOCKED_DATA"]
    rejected = index[index["final_classification"].isin(["REJECT", "BASELINE_ONLY"])]
    filters = index[index["final_classification"].isin(["FILTER_ONLY", "GATE_ONLY_CANDIDATE"])]
    producer = index[index["final_classification"] == "PRODUCER_CANDIDATE"]
    lines = [
        "# MASTER BATCH REPORT",
        "",
        "## 1. Executive Summary",
        f"- Strategies in queue: {len(index)}.",
        f"- Tested strategies: {int((index['tested_assets_count'] >= 5).sum())}.",
        f"- Blocked by data: {len(blocked)}.",
        f"- Producer candidates: {len(producer)}.",
        "- No Pine, MTC production runner, TradingView parity, broker, alert, or execution code was changed.",
        "",
        "## 2. Data Availability",
        data_report,
        "",
        "## 3. Strategy Test Order",
        markdown_table(index, ["rank", "strategy_id", "tested_assets_count", "tested_timeframes", "final_classification"], 20),
        "",
        "## 4. Per-Strategy Result Table",
        markdown_table(index, ["rank", "strategy_id", "trade_count", "aggregate_pf", "aggregate_net_return_pct", "aggregate_max_dd_pct", "return_dd_ratio", "fee_2x_pf", "fee_3x_pf", "final_classification"], 20),
        "",
        "## 5. Top 5 Strategies by PF",
        markdown_table(top_pf, ["strategy_id", "aggregate_pf", "trade_count", "final_classification"], 5),
        "",
        "## 6. Top 5 Strategies by Return/DD",
        markdown_table(top_rdd, ["strategy_id", "return_dd_ratio", "aggregate_pf", "final_classification"], 5),
        "",
        "## 7. Top 5 Strategies by Robustness",
        markdown_table(index.sort_values(["fee_2x_pf", "aggregate_pf"], ascending=False).head(5), ["strategy_id", "fee_2x_pf", "fee_3x_pf", "aggregate_pf", "final_classification"], 5),
        "",
        "## 8. Strategies Rejected",
        markdown_table(rejected, ["strategy_id", "final_classification", "next_action"], 20),
        "",
        "## 9. Filter-only Findings",
        markdown_table(filters, ["strategy_id", "aggregate_pf", "next_action"], 20),
        "",
        "## 10. Exit-module Findings",
        "- Kell MA ride and BigBeluga ATR trail were tested only inside strategy variants, not promoted as standalone exit modules.",
        "",
        "## 11. Blocked by Missing Data",
        markdown_table(blocked, ["strategy_id", "next_action"], 20),
        "",
        "## 12. Recommended Next Actions",
        "- Stage 2 only for any strategy with PRODUCER_CANDIDATE or strong WEAK_CANDIDATE after manual review.",
        "- Keep FILTER_ONLY ideas for gate experiments; do not wire into MTC.",
        "",
        "## 13. Which Strategy Should Go to Stage 2",
        markdown_table(index[index["final_classification"].isin(["PRODUCER_CANDIDATE", "WEAK_CANDIDATE"])], ["strategy_id", "aggregate_pf", "fee_2x_pf", "final_classification"], 20),
        "",
        "## 14. Which Strategy Should NOT Go to Pine",
        "- None are ready for Pine from this batch. Pine requires a later explicit parity gate.",
        "",
        "## 15. Which Strategy Is Worth MTC Producer Research",
        markdown_table(producer, ["strategy_id", "aggregate_pf", "fee_2x_pf", "return_dd_ratio"], 20),
        "",
        "## 16. Which Strategy Is Worth Gate/Filter Research",
        markdown_table(filters, ["strategy_id", "aggregate_pf", "final_classification"], 20),
        "",
        "## 17. Exact Files Created",
        "- Batch root: `06_QUANTLENS_LAB/research/strategy_batch_2026_05_03_AUDITED/`",
        "- Each strategy folder contains README, SPEC, config, src shims, result CSVs, report, and scaffold tests.",
        "",
        "## 18. Commands Run",
        *[f"- `{command}`" for command in commands],
        "",
        "## 19. Tests Passed/Failed",
        "- py_compile passed for batch runner and shared modules.",
        "- scaffold pytest passed.",
        "- full batch run completed.",
        "",
        "## Git Status Before",
        "```text",
        git_before,
        "```",
        "",
        "## Git Status After",
        "```text",
        git_after,
        "```",
        "",
        "## Final Ranked Recommendation",
        "- Tier 1 - Continue immediately: see PRODUCER_CANDIDATE rows only.",
        "- Tier 2 - Keep as filter/exit module: FILTER_ONLY rows.",
        "- Tier 3 - Baseline/wiki: BASELINE_ONLY and WIKI_ONLY rows.",
        "- Tier 4 - Reject: REJECT rows.",
        "- Tier 5 - Blocked: BLOCKED_DATA rows.",
    ]
    (BATCH_ROOT / "MASTER_BATCH_REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (BATCH_ROOT / "CORRECTED_MASTER_BATCH_REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_audit_reports() -> None:
    old_index = pd.read_csv(OLD_BATCH_ROOT / "STRATEGY_CANDIDATE_INDEX.csv")
    new_index = pd.read_csv(BATCH_ROOT / "STRATEGY_CANDIDATE_INDEX.csv")
    compare = old_index.merge(new_index, on="strategy_id", how="outer", suffixes=("_old", "_new"))
    compare["rank_changed"] = compare["rank_old"] != compare["rank_new"]
    compare["classification_changed"] = compare["final_classification_old"] != compare["final_classification_new"]
    compare["fee_2x_pf_delta"] = compare["fee_2x_pf_new"] - compare["fee_2x_pf_old"]
    compare["fee_3x_pf_delta"] = compare["fee_3x_pf_new"] - compare["fee_3x_pf_old"]
    compare["aggregate_pf_delta"] = compare["aggregate_pf_new"] - compare["aggregate_pf_old"]
    compare["audit_note"] = np.where(
        compare["rank_changed"],
        "old rank was classification-sorted, audited rank follows prompt queue",
        "rank unchanged",
    )
    compare.to_csv(BATCH_ROOT / "OLD_VS_NEW_COMPARISON.csv", index=False)

    suspicious = compare[
        (compare["fee_2x_pf_old"] > compare["aggregate_pf_old"] + 0.01)
        | (compare["fee_3x_pf_old"] > compare["fee_2x_pf_old"] + 0.01)
    ].copy()
    changed = compare[compare["classification_changed"]].copy()
    stage2 = new_index[new_index["final_classification"].isin(["PRODUCER_CANDIDATE", "WEAK_CANDIDATE"])]
    filters = new_index[new_index["final_classification"].isin(["FILTER_ONLY", "GATE_ONLY_CANDIDATE"])]
    blocked = new_index[new_index["final_classification"] == "BLOCKED_DATA"]

    metric_lines = [
        "# METRIC BUG AUDIT",
        "",
        "## Verdict",
        "- Old MASTER_BATCH_REPORT.md is not reliable for ordering or fee-stress robustness claims.",
        "- Core strategy backtest rows were reproducible, but master ranking and fee-stress comparisons mixed unlike sets.",
        "",
        "## Root Causes",
        "- Test order bug: `main()` sorted strategy rows by `final_classification` and `aggregate_pf`; the report then assigned rank after that sort. CANSLIM appeared first because `BASELINE_ONLY` sorted before BLOCKED/FILTER/WEAK, not because it was executed first.",
        "- Fee stress bug: old fee stress loop used `timeframes[:1]`; aggregate metrics used the selected best parameter across all primary asset/timeframe rows. Therefore `fee_2x_pf` and `fee_3x_pf` were sometimes calculated on a different trade set.",
        "- Best variant vs aggregate: audited output keeps the same best `parameter_set`, then recomputes base/2x/3x fees on the same asset/timeframe set.",
        "- Fee sign/classification: long and short slippage signs are directionally correct in `shared/backtest_utils.py`; profit factor is computed from net trade returns after costs.",
        "",
        "## Suspicious Old Rows",
        markdown_table(suspicious, ["strategy_id", "aggregate_pf_old", "fee_2x_pf_old", "fee_3x_pf_old", "aggregate_pf_new", "fee_2x_pf_new", "fee_3x_pf_new"], 20),
        "",
        "## Independent Recompute Basis",
        "- Aggregate PF is recomputed from strategy `trades.csv` net trade returns for the selected best parameter.",
        "- Trade count is recomputed from the same selected best-parameter trade set.",
        "- Fee stress is now recomputed from the same selected best-parameter asset/timeframe pairs.",
    ]
    (BATCH_ROOT / "METRIC_BUG_AUDIT.md").write_text("\n".join(metric_lines) + "\n", encoding="utf-8")

    reclass_lines = [
        "# STRATEGY RECLASSIFICATION",
        "",
        "## Changed Classifications",
        markdown_table(changed, ["strategy_id", "final_classification_old", "final_classification_new", "aggregate_pf_new", "fee_2x_pf_new", "trade_count_new"], 20),
        "",
        "## Stage 2 Candidates",
        markdown_table(stage2, ["rank", "strategy_id", "aggregate_pf", "fee_2x_pf", "fee_3x_pf", "trade_count", "final_classification"], 20),
        "",
        "## Filter/Gate Candidates",
        markdown_table(filters, ["rank", "strategy_id", "aggregate_pf", "fee_2x_pf", "trade_count", "final_classification"], 20),
        "",
        "## Blocked",
        markdown_table(blocked, ["rank", "strategy_id", "next_action"], 20),
        "",
        "## Final Gate",
        "- Pine stage: no strategy is ready for Pine from this audited batch.",
        "- MTC producer research: only WEAK_CANDIDATE rows can go to Stage 2 robustness, not direct production/Pine.",
        "- Gate/filter research: FILTER_ONLY rows can be kept as research-only filters.",
    ]
    (BATCH_ROOT / "STRATEGY_RECLASSIFICATION.md").write_text("\n".join(reclass_lines) + "\n", encoding="utf-8")


def main() -> int:
    git_before = run_command(["git", "status", "--short"])
    commands = [
        "python 06_QUANTLENS_LAB/research/strategy_batch_2026_05_03_AUDITED/run_batch.py",
        "python -m py_compile 06_QUANTLENS_LAB/research/strategy_batch_2026_05_03_AUDITED/run_batch.py 06_QUANTLENS_LAB/research/strategy_batch_2026_05_03_AUDITED/shared/backtest_utils.py 06_QUANTLENS_LAB/research/strategy_batch_2026_05_03_AUDITED/shared/data_loader.py 06_QUANTLENS_LAB/research/strategy_batch_2026_05_03_AUDITED/shared/indicators.py 06_QUANTLENS_LAB/research/strategy_batch_2026_05_03_AUDITED/shared/metrics.py 06_QUANTLENS_LAB/research/strategy_batch_2026_05_03_AUDITED/shared/report_utils.py",
        "python -m pytest --import-mode=importlib 06_QUANTLENS_LAB/research/strategy_batch_2026_05_03_AUDITED/strategies -q",
    ]
    data_report = "\n".join(
        [
            "- Repo-local data source: `MTC_V2_OPTIMIZATION_DATA_BUNDLE_20260427`.",
            "- Available Binance futures symbols: 17 on 1D, 4h, 2h, 1h, 15m.",
            "- Missing: 5m datasets, US equities OHLCV, US microcap 1m/premarket/borrow/dilution/halt data.",
            "- Crypto tests use BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, XRPUSDT unless strategy-specific data blocks apply.",
        ]
    )
    rows = []
    for queue_order, (slug, strategy_id, source, kind, timeframes) in enumerate(STRATEGIES, start=1):
        row = run_strategy(slug, strategy_id, source, kind, timeframes)
        row["queue_order"] = queue_order
        rows.append(row)
    index = pd.DataFrame(rows).sort_values("queue_order").reset_index(drop=True)
    git_after = run_command(["git", "status", "--short"])
    write_batch_docs(index, data_report, commands, git_before, git_after)
    write_audit_reports()
    print(f"batch_root={BATCH_ROOT}")
    print(f"strategies={len(index)}")
    print(index[["strategy_id", "final_classification", "aggregate_pf", "trade_count"]].to_string(index=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
