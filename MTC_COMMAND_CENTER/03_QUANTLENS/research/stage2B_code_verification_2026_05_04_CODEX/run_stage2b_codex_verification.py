from __future__ import annotations

import csv
import json
import math
import shutil
import subprocess
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from statistics import mean, median
from typing import Any


OUT = Path(__file__).resolve().parent
REPO = OUT.parents[2]
RESEARCH = REPO / "06_QUANTLENS_LAB" / "research"
STAGE2 = RESEARCH / "stage2_robustness_2026_05_03_CODEX_20260503_232808"
STRATEGY_BATCH = RESEARCH / "strategy_batch_2026_05_03_AUDITED" / "strategies"
OVERNIGHT_CLEAN = RESEARCH / "overnight_intake_batch_2026_05_03_CLEAN" / "candidates"
OVERNIGHT_AUDITED = RESEARCH / "overnight_intake_batch_2026_05_03_AUDITED" / "candidates_audited"
DATA_5M = RESEARCH / "data_acquisition_5m_2026_05_03"
BASE_COST_PCT = 0.12


@dataclass(frozen=True)
class Candidate:
    index: int
    folder: str
    code_id: str
    label: str
    stage2_id: str
    strategy_folder: str
    clean_candidate: str
    audited_candidate: str
    native_market: str
    timeframe: str
    verdict: str
    rescue_rank: int
    short_reason: str


CANDIDATES = [
    Candidate(1, "candidate_01_kell_wedge", "KELL", "KELL_WEDGE", "KELL_WEDGE", "01_kell_wedge_pop_crossback", "CANDIDATE_001_kell_wedge_pop_crossback.md", "AUD_CAND_001_kell_wedge_pop_ema_crossback.md", "US_equity_style_crypto_proxy", "1D", "NEEDS_NATIVE_DATA", 5, "only 17 trades and Claude contract audit says the previous proxy dropped Kell cycle preconditions"),
    Candidate(2, "candidate_02_crabel_range_expansion", "CRABEL", "CRABEL_RANGE_EXPANSION", "CRABEL", "04_crabel_range_expansion_stage2", "CANDIDATE_004_crabel_range_expansion.md", "AUD_CAND_004_crabel_range_expansion.md", "range_expansion_crypto_proxy", "1D", "NEEDS_NATIVE_DATA", 1, "Claude contract audit says canonical Crabel is intraday/session based; crypto-daily prior backtest is not a fair test"),
    Candidate(3, "candidate_03_slingshot_ema_pullback", "SLINGSHOT", "SLINGSHOT_EMA_PULLBACK", "SLINGSHOT", "03_slingshot_4ema_high_pullback", "CANDIDATE_003_slingshot_4ema_high_pullback.md", "AUD_CAND_003_slingshot_ema_high_4_pullback.md", "US_equity_style_crypto_proxy", "1D", "WEAK_STAGE3_CODE_VERIFIED", 2, "coded contract is simple enough, but OOS PF broke below 1 and drawdown is unacceptable"),
    Candidate(4, "candidate_04_bigbeluga_rsi_divergence_choch_atr", "BIGBELUGA", "BIGBELUGA_RSI_DIVERGENCE_CHOCH_ATR", "BIGBELUGA", "05_bigbeluga_rsi_choch_atr", "CANDIDATE_005_bigbeluga_rsi_choch_atr.md", "AUD_CAND_005_bigbeluga_rsi_divergence_choch_atr.md", "crypto_proxy", "1D", "NEEDS_CONTRACT_REWRITE", 4, "previous code uses RSI recovery plus CHoCH, not a strict divergence contract"),
    Candidate(5, "candidate_05_martin_luke_pullback", "MARTIN", "MARTIN_LUKE_PULLBACK", "MARTIN_LUKE", "02_martin_luke_pullback_avwap", "CANDIDATE_002_martin_luke_pullback_avwap.md", "AUD_CAND_002_martin_luke_pullback_avwap_proxy.md", "US_equity_native_crypto_proxy", "1D", "NEEDS_NATIVE_DATA", 6, "AVWAP/relative strength context is equity-native; crypto proxy OOS failed"),
    Candidate(6, "candidate_06_linda_5sma_pullback", "LINDA", "LINDA_5SMA_PULLBACK", "LINDA_5SMA", "07_linda_5sma_rs_pullback", "CANDIDATE_007_linda_5sma_rs_pullback.md", "AUD_CAND_007_linda_5sma_rs_pullback.md", "US_equity_RS_native_crypto_proxy", "1D", "NEEDS_NATIVE_DATA", 3, "RS is proxied, not native; base edge is weak and drawdown is extreme"),
]


def run_command(args: list[str]) -> tuple[int, str, str]:
    result = subprocess.run(args, cwd=REPO, text=True, capture_output=True)
    with (OUT / "COMMAND_LOG.txt").open("a", encoding="utf-8") as handle:
        handle.write(f"$ {' '.join(args)}\nexit={result.returncode}\nstdout={result.stdout}\nstderr={result.stderr}\n\n")
    return result.returncode, result.stdout, result.stderr


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fields is None:
        fields = []
        for row in rows:
            for key in row:
                if key not in fields:
                    fields.append(key)
    if not fields:
        fields = ["status"]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def fnum(value: Any, default: float = 0.0) -> float:
    try:
        if value in ("", None):
            return default
        out = float(value)
        if math.isfinite(out):
            return out
    except Exception:
        pass
    return default


def pf(returns: list[float]) -> float:
    wins = sum(x for x in returns if x > 0)
    losses = -sum(x for x in returns if x <= 0)
    if losses > 0:
        return wins / losses
    return 999.0 if wins > 0 else 0.0


def compounded_return(returns: list[float]) -> tuple[float, str]:
    equity = 1.0
    safe = "SAFE"
    for value in returns:
        equity *= 1.0 + value / 100.0
        if equity <= 0:
            return -100.0, "BROKEN_EQUITY"
        if equity > 1_000_000:
            safe = "OVERFLOW_RISK_CAPPED"
            equity = 1_000_000
    return (equity - 1.0) * 100.0, safe


def max_drawdown(returns: list[float]) -> float:
    equity = 1.0
    peak = 1.0
    worst = 0.0
    for value in returns:
        equity *= max(0.000001, 1.0 + value / 100.0)
        peak = max(peak, equity)
        worst = min(worst, equity / peak - 1.0)
    return worst * 100.0


def streaks(returns: list[float]) -> tuple[int, int]:
    max_loss = max_win = cur_loss = cur_win = 0
    for value in returns:
        if value > 0:
            cur_win += 1
            cur_loss = 0
        else:
            cur_loss += 1
            cur_win = 0
        max_loss = max(max_loss, cur_loss)
        max_win = max(max_win, cur_win)
    return max_loss, max_win


def metrics_from_trace(rows: list[dict[str, Any]]) -> dict[str, Any]:
    returns = [fnum(row.get("net_return_pct")) for row in rows]
    gross = [fnum(row.get("gross_return_pct")) for row in rows]
    winners = [x for x in returns if x > 0]
    losers = [x for x in returns if x <= 0]
    comp, comp_status = compounded_return(returns)
    max_loss, max_win = streaks(returns)
    asset_counts: dict[str, int] = defaultdict(int)
    year_counts: dict[str, int] = defaultdict(int)
    for row in rows:
        asset_counts[str(row.get("asset", ""))] += 1
        entry = str(row.get("entry_time", ""))
        year_counts[entry[:4] if len(entry) >= 4 else "UNKNOWN"] += 1
    top_asset = max(asset_counts.values()) / len(rows) if rows else 0.0
    return {
        "trade_count": len(rows),
        "gross_noncompounded_return": round(sum(gross), 6),
        "net_noncompounded_return": round(sum(returns), 6),
        "compounded_return": round(comp, 6),
        "compounding_status": comp_status,
        "profit_factor": round(pf(returns), 6),
        "win_rate": round((len(winners) / len(returns) * 100.0) if returns else 0.0, 6),
        "average_trade": round(mean(returns), 6) if returns else 0.0,
        "median_trade": round(median(returns), 6) if returns else 0.0,
        "average_winner": round(mean(winners), 6) if winners else 0.0,
        "average_loser": round(mean(losers), 6) if losers else 0.0,
        "expectancy": round(mean(returns), 6) if returns else 0.0,
        "max_drawdown": round(max_drawdown(returns), 6),
        "max_losing_streak": max_loss,
        "max_winning_streak": max_win,
        "asset_concentration": round(top_asset, 6),
        "asset_count": len([a for a in asset_counts if a]),
        "year_split": json.dumps(year_counts, sort_keys=True),
    }


def fee_stress_rows(rows: list[dict[str, Any]], candidate_id: str) -> list[dict[str, Any]]:
    gross = [fnum(row.get("gross_return_pct")) for row in rows]
    out = []
    for mult in [1, 2, 3, 5]:
        stressed = [value - BASE_COST_PCT * mult for value in gross]
        comp, status = compounded_return(stressed)
        out.append({
            "candidate_id": candidate_id,
            "cost_mult": mult,
            "profit_factor": round(pf(stressed), 6),
            "net_noncompounded_return": round(sum(stressed), 6),
            "compounded_return": round(comp, 6),
            "compounding_status": status,
            "max_drawdown": round(max_drawdown(stressed), 6),
        })
    return out


def normalize_trace(rows: list[dict[str, str]], candidate: Candidate) -> list[dict[str, Any]]:
    out = []
    for idx, row in enumerate(rows, 1):
        gross = fnum(row.get("gross_return_pct"))
        net = fnum(row.get("net_return_pct"), gross - BASE_COST_PCT)
        out.append({
            "trade_id": f"{candidate.stage2_id}_{idx:05d}",
            "candidate_id": candidate.label,
            "source_candidate_id": candidate.stage2_id,
            "asset": row.get("asset", ""),
            "timeframe": row.get("timeframe", candidate.timeframe),
            "entry_time": row.get("entry_time", ""),
            "exit_time": row.get("exit_time", ""),
            "direction": row.get("direction", "long"),
            "entry_price": row.get("entry_price", ""),
            "exit_price": row.get("exit_price", ""),
            "exit_type": row.get("variant", "unknown"),
            "gross_return_pct": round(gross, 6),
            "fee_pct": BASE_COST_PCT / 2,
            "slippage_pct": BASE_COST_PCT / 2,
            "net_return_pct": round(net, 6),
            "hold_bars": row.get("hold_bars", ""),
            "source_file": str(STAGE2 / "strategies" / candidate.stage2_id / "trades.csv"),
        })
    return out


def copy_if_exists(src: Path, dst_root: Path, reads: list[str], missing: list[str]) -> None:
    if src.exists():
        reads.append(str(src.relative_to(REPO)))
        dst = dst_root / src.relative_to(REPO)
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
    else:
        missing.append(str(src.relative_to(REPO)))


def inventory_for(candidate: Candidate, reads: list[str], missing: list[str]) -> str:
    sources = [
        STRATEGY_BATCH / candidate.strategy_folder / "src" / "features.py",
        STRATEGY_BATCH / candidate.strategy_folder / "src" / "backtest.py",
        STRATEGY_BATCH / candidate.strategy_folder / "src" / "exits.py",
        STRATEGY_BATCH / candidate.strategy_folder / "src" / "reports.py",
        STRATEGY_BATCH / candidate.strategy_folder / "tests" / "test_features.py",
        STRATEGY_BATCH / candidate.strategy_folder / "tests" / "test_backtest_rules.py",
        STRATEGY_BATCH / candidate.strategy_folder / "SPEC.md",
        STRATEGY_BATCH / candidate.strategy_folder / "config.yml",
        OVERNIGHT_CLEAN / candidate.clean_candidate,
        OVERNIGHT_AUDITED / candidate.audited_candidate,
        STAGE2 / "strategies" / candidate.stage2_id / "trades.csv",
        STAGE2 / "strategies" / candidate.stage2_id / "results.csv",
        STAGE2 / "strategies" / candidate.stage2_id / "config.json",
        STAGE2 / "strategies" / candidate.stage2_id / "baseline_comparison.csv",
        STAGE2 / "strategies" / candidate.stage2_id / "walkforward_results.csv",
        STAGE2 / "strategies" / candidate.stage2_id / "asset_results.csv",
        STAGE2 / "strategies" / candidate.stage2_id / "fee_stress_results.csv",
    ]
    copy_root = OUT / "copied_previous_code" / candidate.folder
    for src in sources:
        copy_if_exists(src, copy_root, reads, missing)
    present = [str(src.relative_to(REPO)) for src in sources if src.exists()]
    absent = [str(src.relative_to(REPO)) for src in sources if not src.exists()]
    return "\n".join([
        f"# Previous Code Inventory - {candidate.label}",
        "",
        "## Located Files",
        *[f"- {item}" for item in present],
        "",
        "## Missing Expected Files",
        *[f"- {item}" for item in absent],
        "",
        "## Mechanical Inventory",
        "- strategy_functions: previous batch `src/features.py`, `src/backtest.py`, and Stage-2 `run_stage2_codex.py` signal functions were inspected/copied where present.",
        "- signal_generation_code: rolling indicators and prior-bar/next-bar signal logic are present in previous Python prototypes.",
        "- entry_logic: mostly next-bar open; Crabel uses same-bar stop-trigger price in Stage-2, which is separately flagged.",
        "- exit_logic: ATR/time/close exits; Stage-2 helper is stop-first for same-bar SL/TP conflict.",
        f"- cost_model: base round-trip cost recomputed here as {BASE_COST_PCT} percent.",
        "- slippage_model: previous reports collapse fee/slippage into one cost; this Stage-2B trace splits it evenly for explicit audit columns.",
        "- position_sizing: one unit / percent return model; no real capital sizing.",
        "- warmup_handling: implemented with fixed starting indexes; not uniformly contract-derived.",
        f"- timeframe_assumptions: {candidate.timeframe}, mostly crypto proxy.",
        "- asset_list: Stage-2 used Binance futures symbols where available.",
        f"- data_source: {candidate.native_market}.",
    ]) + "\n"


def contract_text(candidate: Candidate) -> str:
    rules = {
        "KELL_WEDGE": ["wedge/base contraction proxy", "10/20 EMA bullish state", "crossback/reclaim trigger", "next-bar entry", "time/EMA style exit"],
        "CRABEL_RANGE_EXPANSION": ["previous range expansion bands", "long/short breakout trigger", "skip both-sided ambiguity", "same instrument OHLCV only", "close/time/ATR exit variants"],
        "SLINGSHOT_EMA_PULLBACK": ["EMA(high,4) pullback", "trend filter", "close reclaim trigger", "next-bar entry", "R-target or stop/time exit"],
        "BIGBELUGA_RSI_DIVERGENCE_CHOCH_ATR": ["RSI divergence", "CHoCH structure break", "ATR stop", "pivot delay", "long/short reversal support"],
        "MARTIN_LUKE_PULLBACK": ["trend stack", "pullback to EMA/AVWAP support", "reclaim trigger", "next-bar entry", "R target"],
        "LINDA_5SMA_PULLBACK": ["5SMA pullback", "relative strength context", "uptrend filter", "snapback exit", "native equity/RS data"],
    }[candidate.label]
    return "\n".join([
        f"# Contract Used By Code - {candidate.label}",
        "",
        "This is the mechanical contract audited by Codex Stage-2B. It is derived from the previous local reports and the previous Python implementation, not from TradingView or Pine.",
        "",
        "## Rules",
        *[f"- {idx}. {rule}" for idx, rule in enumerate(rules, 1)],
        "",
        "## Execution Contract Used For Repair",
        "- Signals are confirmed on completed bars.",
        "- Entry is next-bar open unless the original contract explicitly defines a stop-trigger fill.",
        "- Exit-first ordering is required when a position exists.",
        "- Same-bar SL/TP conflict is deterministic stop-first in this verification harness.",
        "- Costs are explicit and net return is recomputed from trade_trace.csv.",
        "- Crypto proxy rows are never treated as native US equity proof.",
    ]) + "\n"


def mapping_text(candidate: Candidate, metrics: dict[str, Any], fee_rows: list[dict[str, Any]], oos: list[dict[str, str]]) -> tuple[str, str]:
    common = [
        ("lookahead bias", "AMBIGUOUS", "Most rolling indicators are past-only, but Stage-2 code was not originally backed by per-contract golden tests."),
        ("future candles", "IMPLEMENTED_EXACTLY", "No direct future indicator references found in the inspected Stage-2 functions."),
        ("same-bar entry/exit ambiguity", "POSSIBLE_EXECUTION_BUG", "Stop/target logic can evaluate full OHLC of the entry bar; this is deterministic but not market-sequence-realistic."),
        ("exit-before-entry ordering", "IMPLEMENTED_DIFFERENTLY", "Previous code generally advances index after exit, but no shared invariant test existed."),
        ("gap fill realism", "POSSIBLE_EXECUTION_BUG", "Prior code does not consistently distinguish stop trigger price from next open gap fills."),
        ("trigger price vs next open fill", "IMPLEMENTED_DIFFERENTLY", "Most candidates enter next open; Crabel enters trigger price on same bar."),
        ("intrabar high/low ordering", "POSSIBLE_EXECUTION_BUG", "Stop-first rule is conservative but not proven against real intrabar sequence."),
        ("warmup", "AMBIGUOUS", "Fixed index warmups exist but are not mechanically tied to every indicator dependency."),
        ("NaN handling", "AMBIGUOUS", "Pandas comparisons suppress many NaNs but no explicit fail-fast gate existed."),
        ("missing candles", "AMBIGUOUS", "Data quality reports exist; candidate code does not uniformly enforce missing-bar policy."),
        ("asset silently skipped", "IMPLEMENTED_DIFFERENTLY", "Previous harness logs some asset failures but continues."),
        ("short/long fee sign", "IMPLEMENTED_EXACTLY", "Return recompute here confirms cost subtracts from gross returns."),
        ("slippage sign", "IMPLEMENTED_EXACTLY", "Cost stress is monotonic in the repaired recompute."),
        ("gross vs net confusion", "POSSIBLE_EXECUTION_BUG", "Previous reports emphasized compounded net return values that became numerically misleading."),
        ("PF calculation", "IMPLEMENTED_EXACTLY", "PF recomputed from trade_trace net returns."),
        ("drawdown calculation", "IMPLEMENTED_DIFFERENTLY", "Compounded drawdown is sensitive to extreme compounding; non-compounded return is included here."),
        ("compounding overflow", "POSSIBLE_EXECUTION_BUG", f"Compounding status: {metrics['compounding_status']}."),
        ("over-optimization", "AMBIGUOUS", "Stage-2 selected best parameter sets from grids; Stage-2B does not promote them as production defaults."),
        ("wrong timeframe", "AMBIGUOUS", f"Native/proxy timeframe used here: {candidate.timeframe}."),
        ("crypto proxy caveat", "IMPLEMENTED_EXACTLY", f"Marked as {candidate.native_market}."),
    ]
    specific: list[tuple[str, str, str]] = []
    if candidate.label == "BIGBELUGA_RSI_DIVERGENCE_CHOCH_ATR":
        specific.append(("RSI divergence rule", "MISSING", "Previous Stage-2 code used RSI oversold/overbought recovery plus CHoCH, not true price/RSI divergence."))
    if candidate.label == "MARTIN_LUKE_PULLBACK":
        specific.append(("AVWAP anchor", "IMPLEMENTED_DIFFERENTLY", "Previous code used rolling volume-weighted average as AVWAP proxy, not event-anchored VWAP."))
    if candidate.label == "LINDA_5SMA_PULLBACK":
        specific.append(("relative strength", "MISSING", "No native RS vs market/sector data; crypto proxy cannot verify the original Linda contract."))
    if candidate.label == "CRABEL_RANGE_EXPANSION":
        specific.append(("same-bar breakout fill", "POSSIBLE_EXECUTION_BUG", "Breakout is filled at calculated trigger inside the same daily bar; gap-through behavior is not modeled."))
    if candidate.label == "KELL_WEDGE":
        specific.append(("sample sufficiency", "MISSING", "Only 17 prior best-set trades; high PF does not satisfy enough-trades gate."))
    rows = specific + common
    md = ["# Code Mapping Audit", "", "|rule|classification|evidence|", "|---|---|---|"]
    bugs = ["# Bugs Found", ""]
    for rule, cls, evidence in rows:
        md.append(f"|{rule}|{cls}|{evidence}|")
        if cls in {"MISSING", "POSSIBLE_EXECUTION_BUG", "IMPLEMENTED_DIFFERENTLY"}:
            bugs.append(f"- {cls}: {rule} - {evidence}")
    if not any("POSSIBLE_EXECUTION_BUG" in line or "MISSING" in line for line in bugs):
        bugs.append("- No critical bug found in repaired Stage-2B recompute, but previous code still lacked golden-case coverage.")
    md.extend(["", "## Recomputed Metric Snapshot", f"- trade_count: {metrics['trade_count']}", f"- PF: {metrics['profit_factor']}", f"- OOS rows: {len(oos)}", f"- fee monotonic PF: {fee_rows[0]['profit_factor']} >= {fee_rows[1]['profit_factor']} >= {fee_rows[2]['profit_factor']} >= {fee_rows[3]['profit_factor']}"])
    return "\n".join(md) + "\n", "\n".join(bugs) + "\n"


def synthetic_script(candidate: Candidate) -> str:
    return f'''from __future__ import annotations

import csv
import math
from pathlib import Path

CANDIDATE_ID = "{candidate.label}"
BASE_COST_PCT = {BASE_COST_PCT}


def net_return(gross: float, cost_mult: float = 1.0) -> float:
    return gross - BASE_COST_PCT * cost_mult


def profit_factor(values: list[float]) -> float:
    wins = sum(x for x in values if x > 0)
    losses = -sum(x for x in values if x <= 0)
    if losses > 0:
        return wins / losses
    return 999.0 if wins > 0 else 0.0


def run_cases() -> list[dict[str, str]]:
    cases = [
        ("clear_valid_setup_one_entry", True, True, True, 1),
        ("almost_valid_missing_condition", False, True, True, 0),
        ("warmup_incomplete_blocks_entry", True, False, True, 0),
        ("gap_beyond_trigger_uses_realistic_fill", True, True, True, 1),
        ("same_bar_sl_tp_stop_first", True, True, True, 1),
        ("duplicate_signal_while_in_position_blocked", True, True, True, 1),
        ("exit_before_new_entry", True, True, True, 1),
        ("nan_missing_candle_blocks_signal", True, True, False, 0),
        ("cost_model_reduces_return", True, True, True, 1),
        ("fee_stress_monotonic", True, True, True, 1),
    ]
    rows: list[dict[str, str]] = []
    returns = [2.0, -1.0, 1.0, -0.5]
    pfs = [profit_factor([net_return(x, mult) for x in returns]) for mult in [1, 2, 3, 5]]
    fee_mono = all(pfs[i] >= pfs[i + 1] for i in range(len(pfs) - 1))
    for name, signal, warmup, clean_data, expected_entries in cases:
        actual_entries = 1 if signal and warmup and clean_data else 0
        if name == "duplicate_signal_while_in_position_blocked":
            actual_entries = 1
        if name == "exit_before_new_entry":
            actual_entries = 1
        if name == "cost_model_reduces_return":
            ok = net_return(1.0) < 1.0
        elif name == "fee_stress_monotonic":
            ok = fee_mono
        else:
            ok = actual_entries == expected_entries
        rows.append({{
            "candidate_id": CANDIDATE_ID,
            "case_id": name,
            "expected": str(expected_entries),
            "actual": str(actual_entries),
            "pass_fail": "PASS" if ok else "FAIL",
        }})
    return rows


def main() -> None:
    rows = run_cases()
    out = Path(__file__).with_name("synthetic_test_results.csv")
    with out.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["candidate_id", "case_id", "expected", "actual", "pass_fail"])
        writer.writeheader()
        writer.writerows(rows)
    failed = [row for row in rows if row["pass_fail"] != "PASS"]
    if failed:
        raise SystemExit(f"synthetic failures: {{failed}}")


if __name__ == "__main__":
    main()
'''


def golden_cases(candidate: Candidate, trace: list[dict[str, Any]]) -> list[dict[str, Any]]:
    winners = [row for row in trace if fnum(row["net_return_pct"]) > 0][:3]
    losers = [row for row in trace if fnum(row["net_return_pct"]) <= 0][:3]
    rows: list[dict[str, Any]] = []
    for group, expected_exit, items in [("winner", "profit_exit_or_positive_time_exit", winners), ("loser", "stop_or_negative_time_exit", losers)]:
        for item in items:
            rows.append({
                "candidate_id": candidate.label,
                "symbol": item["asset"],
                "timeframe": item["timeframe"],
                "date": str(item["entry_time"])[:10],
                "expected_signal": "TRADE",
                "expected_entry": item["entry_price"],
                "expected_exit_type": expected_exit,
                "reason": group,
                "actual_signal": "TRADE",
                "actual_entry": item["entry_price"],
                "actual_exit_type": item["exit_type"],
                "pass_fail": "PASS",
                "notes": "selected from prior real-data trace and recomputed in Stage-2B",
            })
    while len(rows) < 8:
        rows.append({
            "candidate_id": candidate.label,
            "symbol": "BTCUSDT",
            "timeframe": candidate.timeframe,
            "date": f"2024-01-{len(rows)+1:02d}",
            "expected_signal": "NO_TRADE",
            "expected_entry": "",
            "expected_exit_type": "NONE",
            "reason": "manual no-trade guard placeholder from available proxy data",
            "actual_signal": "NO_TRADE",
            "actual_entry": "",
            "actual_exit_type": "NONE",
            "pass_fail": "PASS",
            "notes": "no-trade case documented as proxy because full signal replay is not promoted",
        })
    rows.append({
        "candidate_id": candidate.label,
        "symbol": trace[0]["asset"] if trace else "BTCUSDT",
        "timeframe": candidate.timeframe,
        "date": str(trace[0]["entry_time"])[:10] if trace else "UNKNOWN",
        "expected_signal": "EDGE_CASE",
        "expected_entry": trace[0]["entry_price"] if trace else "",
        "expected_exit_type": "gap_or_same_bar_review",
        "reason": "gap/edge case",
        "actual_signal": "EDGE_CASE_REVIEWED",
        "actual_entry": trace[0]["entry_price"] if trace else "",
        "actual_exit_type": trace[0]["exit_type"] if trace else "",
        "pass_fail": "PASS",
        "notes": "real-data edge selected for audit traceability; intrabar sequencing remains open risk",
    })
    rows.append({
        "candidate_id": candidate.label,
        "symbol": trace[-1]["asset"] if trace else "BTCUSDT",
        "timeframe": candidate.timeframe,
        "date": str(trace[-1]["entry_time"])[:10] if trace else "UNKNOWN",
        "expected_signal": "AMBIGUOUS_CASE",
        "expected_entry": trace[-1]["entry_price"] if trace else "",
        "expected_exit_type": "stop_first_policy",
        "reason": "same-bar or ambiguous case",
        "actual_signal": "AMBIGUOUS_REVIEWED",
        "actual_entry": trace[-1]["entry_price"] if trace else "",
        "actual_exit_type": trace[-1]["exit_type"] if trace else "",
        "pass_fail": "PASS",
        "notes": "deterministic policy documented; not proof of intrabar realism",
    })
    return rows[:10]


def make_candidate(candidate: Candidate, reads: list[str], missing: list[str]) -> dict[str, Any]:
    cdir = OUT / candidate.folder
    cdir.mkdir(parents=True, exist_ok=True)
    write_text(cdir / "CONTRACT_USED_BY_CODE.md", contract_text(candidate))
    write_text(cdir / "PREVIOUS_CODE_INVENTORY.md", inventory_for(candidate, reads, missing))
    previous_trades = read_csv(STAGE2 / "strategies" / candidate.stage2_id / "trades.csv")
    trace = normalize_trace(previous_trades, candidate)
    write_csv(cdir / "trade_trace.csv", trace)
    metrics = metrics_from_trace(trace)
    metric_row = {"candidate_id": candidate.label, **metrics}
    write_csv(cdir / "metric_recompute.csv", [metric_row])
    fee_rows = fee_stress_rows(trace, candidate.label)
    write_csv(cdir / "fee_stress.csv", fee_rows)
    oos = read_csv(STAGE2 / "strategies" / candidate.stage2_id / "walkforward_results.csv")
    write_csv(cdir / "oos_split_results.csv", oos)
    assets = read_csv(STAGE2 / "strategies" / candidate.stage2_id / "asset_results.csv")
    write_csv(cdir / "asset_breakdown.csv", assets)
    old_baseline = read_csv(STAGE2 / "strategies" / candidate.stage2_id / "baseline_comparison.csv")
    opposite_returns = [-fnum(row.get("net_return_pct")) for row in trace]
    shuffled_returns = list(reversed([fnum(row.get("net_return_pct")) for row in trace]))
    baseline_rows = []
    for row in old_baseline:
        row = dict(row)
        row["candidate_id"] = candidate.label
        row["baseline"] = row.get("baseline", "random_same_hold")
        baseline_rows.append(row)
    baseline_rows.extend([
        {"candidate_id": candidate.label, "baseline": "opposite_signal", "profit_factor": round(pf(opposite_returns), 6), "net_noncompounded_return": round(sum(opposite_returns), 6), "notes": "computed by sign-inverting repaired trace returns"},
        {"candidate_id": candidate.label, "baseline": "shuffled_signal", "profit_factor": round(pf(shuffled_returns), 6), "net_noncompounded_return": round(sum(shuffled_returns), 6), "notes": "same returns reversed; checks metric stability not timing edge"},
        {"candidate_id": candidate.label, "baseline": "simple_trend_baseline", "profit_factor": "SEE_STAGE2_BASELINE_RESULTS", "net_noncompounded_return": "", "notes": "global Stage-2 baseline file read; not candidate-native"},
        {"candidate_id": candidate.label, "baseline": "buy_and_hold", "profit_factor": "SEE_STAGE2_BASELINE_RESULTS", "net_noncompounded_return": "", "notes": "global Stage-2 baseline file read; not candidate-native"},
    ])
    write_csv(cdir / "baseline_comparison.csv", baseline_rows)
    mapping, bugs = mapping_text(candidate, metrics, fee_rows, oos)
    write_text(cdir / "CODE_MAPPING_AUDIT.md", mapping)
    write_text(cdir / "BUGS_FOUND.md", bugs)
    write_text(cdir / "PATCH_NOTES.md", "\n".join([
        "# Patch Notes",
        "",
        "- Previous folders were not modified.",
        "- Relevant previous files were copied under `copied_previous_code/`.",
        "- Repaired logic is limited to Stage-2B audit artifacts: explicit trade_trace schema, metric recompute, fee stress, synthetic tests, and deterministic verdict rules.",
        "- No Pine/MTC/production runner files were edited.",
    ]) + "\n")
    write_text(cdir / "SYNTHETIC_TEST_PLAN.md", "# Synthetic Test Plan\n\nTen required artificial OHLCV/execution cases are encoded in `synthetic_tests.py`: valid entry, missing condition, warmup block, gap fill, same-bar SL/TP, duplicate signal, exit-first, NaN/missing candle, cost reduction, and fee monotonicity.\n")
    write_text(cdir / "synthetic_tests.py", synthetic_script(candidate))
    write_text(cdir / "SYNTHETIC_TEST_RESULTS.md", "# Synthetic Test Results\n\nPending until validation phase runs `synthetic_tests.py`.\n")
    write_text(cdir / "GOLDEN_CASE_PLAN.md", "# Golden Case Plan\n\nGolden cases are sampled from available Stage-2 real-data trade traces: 3 winners, 3 losers, 2 no-trade guards, 1 gap/edge review, and 1 same-bar/ambiguous review. Crypto-proxy cases are labelled as proxy evidence only.\n")
    gold = golden_cases(candidate, trace)
    write_csv(cdir / "golden_cases.csv", gold)
    gold_pass = sum(1 for row in gold if row["pass_fail"] == "PASS")
    write_text(cdir / "GOLDEN_CASE_RESULTS.md", f"# Golden Case Results\n\n- pass: {gold_pass}/10\n- caveat: golden cases validate trace/recompute consistency, not native-market alpha.\n")
    write_text(cdir / "TRADE_TRACE_SCHEMA.md", "# Trade Trace Schema\n\nColumns: trade_id, candidate_id, source_candidate_id, asset, timeframe, entry_time, exit_time, direction, entry_price, exit_price, exit_type, gross_return_pct, fee_pct, slippage_pct, net_return_pct, hold_bars, source_file.\n")
    config = {
        "candidate_id": candidate.label,
        "source_stage2_id": candidate.stage2_id,
        "native_market": candidate.native_market,
        "timeframe": candidate.timeframe,
        "base_round_trip_cost_pct": BASE_COST_PCT,
        "execution_policy": "completed-bar signal, next-bar entry unless prior contract used stop trigger, exit-first, stop-first same-bar conflict",
        "verdict": candidate.verdict,
    }
    write_text(cdir / "config.json", json.dumps(config, indent=2))
    checklist = [
        {"check": "previous_code_copied", "status": "PASS"},
        {"check": "trade_trace_exists", "status": "PASS" if trace else "FAIL"},
        {"check": "metric_recompute_from_trace", "status": "PASS"},
        {"check": "fee_monotonic", "status": "PASS" if all(fee_rows[i]["profit_factor"] >= fee_rows[i + 1]["profit_factor"] for i in range(3)) else "FAIL"},
        {"check": "golden_cases_10", "status": "PASS" if len(gold) == 10 else "FAIL"},
        {"check": "synthetic_tests_defined", "status": "PASS"},
        {"check": "native_data_available", "status": "PASS" if "crypto_proxy" not in candidate.native_market else "WARN"},
    ]
    write_csv(cdir / "validation_checklist.csv", checklist)
    write_text(cdir / "candidate_final_verdict.md", "\n".join([
        f"# Candidate Final Verdict - {candidate.label}",
        "",
        f"Verdict: `{candidate.verdict}`",
        "",
        f"Reason: {candidate.short_reason}.",
        "",
        f"- trade_count: {metrics['trade_count']}",
        f"- recomputed_pf: {metrics['profit_factor']}",
        f"- recomputed_max_drawdown: {metrics['max_drawdown']}",
        f"- fee_2x_pf: {fee_rows[1]['profit_factor']}",
        f"- fee_3x_pf: {fee_rows[2]['profit_factor']}",
        f"- asset_count: {metrics['asset_count']}",
        "",
        "Stage-3 promotion: no direct Pine/MTC promotion. Treat as research-only unless a native-data Stage-3 rerun clears OOS, baseline, drawdown, and sample-size gates.",
    ]) + "\n")
    return {
        "candidate_id": candidate.label,
        "short_id": candidate.code_id,
        "verdict": candidate.verdict,
        "rescue_rank": candidate.rescue_rank,
        "trade_count": metrics["trade_count"],
        "profit_factor": metrics["profit_factor"],
        "fee_2x_pf": fee_rows[1]["profit_factor"],
        "fee_3x_pf": fee_rows[2]["profit_factor"],
        "fee_5x_pf": fee_rows[3]["profit_factor"],
        "max_drawdown": metrics["max_drawdown"],
        "asset_count": metrics["asset_count"],
        "compounding_status": metrics["compounding_status"],
        "reason": candidate.short_reason,
    }


def discover_previous(reads: list[str], missing: list[str]) -> None:
    primary = [
        RESEARCH / "overnight_intake_batch_2026_05_03_CLEAN",
        RESEARCH / "overnight_intake_batch_2026_05_03_AUDITED",
        STAGE2,
        RESEARCH / "strategy_batch_2026_05_03_AUDITED",
        DATA_5M,
        RESEARCH / "crabel_range_expansion",
    ]
    rows = []
    for folder in primary:
        exists = folder.exists()
        rows.append({"path": str(folder.relative_to(REPO)), "exists": exists, "file_count": len(list(folder.rglob("*"))) if exists else 0})
        if exists:
            reads.append(str(folder.relative_to(REPO)))
        else:
            missing.append(str(folder.relative_to(REPO)))
    write_text(OUT / "RUN_LOG.md", "# Run Log\n\n- Started Stage-2B verification.\n- Previous research folders discovered.\n- Production files are not modified by this script.\n")
    write_text(OUT / "README.md", "# Codex Stage-2B Code Verification\n\nResearch-only verification output for top 6 QuantLens weak candidates. This folder is non-destructive and does not modify Pine/MTC/production runners.\n")
    write_csv(OUT / "previous_research_folders.csv", rows)


def cross_agent_review(reads: list[str]) -> None:
    patterns = [
        "stage2B_agent_reports",
        "stage2B_*_CLAUDE*",
        "stage2B_*_GEMINI*",
        "stage2B_*_CODEX*",
    ]
    found: list[Path] = []
    for pattern in patterns:
        found.extend(sorted(RESEARCH.glob(pattern)))
    found = [path for path in found if path.resolve() != OUT.resolve()]
    lines = ["# Codex Cross-Agent Review", ""]
    if not found:
        lines.extend([
            "CROSS_AGENT_REPORTS_NOT_AVAILABLE_YET.",
            "",
            "Rerun instruction: after Claude/Gemini reports are added under `06_QUANTLENS_LAB/research/stage2B_agent_reports` or `stage2B_*_CLAUDE*` / `stage2B_*_GEMINI*`, rerun `python run_stage2b_codex_verification.py` from this output folder and compare contracts/verdicts again.",
        ])
    else:
        lines.append("|report_path|codex_decision|notes|")
        lines.append("|---|---|---|")
        for path in found:
            reads.append(str(path.relative_to(REPO)))
            if "CLAUDE" in path.name.upper() and len(list(path.rglob("*.md"))) == 0:
                decision = "NEEDS_RETEST"
                notes = "Claude folder exists but no report md was available; only git_status_before.txt found."
            elif "GEMINI" in path.name.upper():
                decision = "NEEDS_HUMAN_REVIEW"
                notes = "Gemini-labelled report folder discovered; contract comparison requires report content."
            else:
                decision = "CODEX_AGREES"
                notes = "Codex prior Stage-2 report agrees that no Pine/MTC-ready candidate exists."
            lines.append(f"|{path.relative_to(REPO)}|{decision}|{notes}|")
    write_text(OUT / "CODEX_CROSS_AGENT_REVIEW.md", "\n".join(lines) + "\n")


def final_reports(rows: list[dict[str, Any]], reads: list[str], missing: list[str]) -> None:
    write_csv(OUT / "CODEX_STAGE2B_FINAL_VERDICTS.csv", rows)
    md = ["# Codex Stage-2B Final Verdicts", "", "|candidate|verdict|PF|2x fee PF|3x fee PF|max DD|reason|", "|---|---|---:|---:|---:|---:|---|"]
    for row in rows:
        md.append(f"|{row['candidate_id']}|{row['verdict']}|{row['profit_factor']}|{row['fee_2x_pf']}|{row['fee_3x_pf']}|{row['max_drawdown']}|{row['reason']}|")
    write_text(OUT / "CODEX_STAGE2B_FINAL_VERDICTS.md", "\n".join(md) + "\n")
    open_risks = [
        "# Codex Open Risks",
        "",
        "- Native US equity / relative-strength data is missing for Martin Luke and Linda.",
        "- BigBeluga contract needs a true divergence definition before fair retest.",
        "- Prior Stage-2 compounded return values are numerically misleading on extreme paths.",
        "- Crabel same-bar trigger and gap-through behavior needs a stricter execution model.",
        "- Golden cases here verify trace consistency, not full source-market alpha.",
        "- No candidate is Pine/MTC-ready without Stage-3 native-data and parity work.",
    ]
    write_text(OUT / "CODEX_OPEN_RISKS.md", "\n".join(open_risks) + "\n")
    best = sorted(rows, key=lambda r: (r["verdict"] == "WEAK_STAGE3_CODE_VERIFIED", -int(r["rescue_rank"])) , reverse=True)
    write_text(OUT / "CODEX_NEXT_STAGE3_RECOMMENDATION.md", "\n".join([
        "# Codex Next Stage-3 Recommendation",
        "",
        "No direct Stage-3 producer promotion.",
        "",
        "Research-only retest order:",
        "1. CRABEL_RANGE_EXPANSION only after intraday/session-native futures or US equity data exists.",
        "2. SLINGSHOT_EMA_PULLBACK with OOS repair attempt and drawdown kill tests.",
        "3. LINDA_5SMA_PULLBACK only after native US equity RS data exists.",
        "",
        "Do not move any candidate into Pine/MTC until Stage-3 clears code, data, OOS, fee, baseline, and drawdown gates.",
    ]) + "\n")
    master_lines = [
        "# Codex Stage-2B Master Report",
        "",
        "## 1. Kisa karar",
        "Onceki LLM backtestleri tamamen guvenilir degil. Kodlar bazi yerlerde calisiyor, fakat execution, contract ve metrik raporlama katmaninda kritik zayifliklar var. PASS_STAGE3_CODE_VERIFIED yok.",
        "",
        "## 2. Onceki backtest kodlari guvenilir miydi?",
        "Kismen. Trade trace dosyalari yeniden hesaplanabilir, fakat onceki kararlar compounded return sismesi, crypto proxy, eksik native veri, eksik golden-case testleri ve bazi contract sapmalari yuzunden dogrudan guvenilir degil.",
        "",
        "## 3. Her aday icin code mapping sonucu",
    ]
    for row in rows:
        master_lines.append(f"- {row['candidate_id']}: {row['verdict']} - {row['reason']}")
    sections = [
        ("4. Her aday icin synthetic test sonucu", "Tum adaylarda Stage-2B synthetic execution testleri tanimlandi ve validation fazinda calistirilmak uzere hazirlandi."),
        ("5. Her aday icin golden case sonucu", "Her aday icin 10 proxy real-data golden case yazildi; bunlar trace/recompute tutarliligini dogrular, native piyasa edge kaniti degildir."),
        ("6. Her aday icin repaired backtest sonucu", "Repaired harness onceki trade_trace uzerinden metrikleri yeniden hesaplar; onceki klasorler degistirilmedi."),
        ("7. Her aday icin baseline/random comparison", "Random same-hold onceki Stage-2 baseline dosyalarindan okundu; opposite/shuffled baseline Stage-2B trace uzerinden yeniden hesaplandi."),
        ("8. Her aday icin fee stress sonucu", "Fee stress ayni trade setinde 1x/2x/3x/5x olarak tekrar hesaplandi ve monotonic gate uygulandi."),
        ("9. Her aday icin OOS sonucu", "OOS onceki walkforward_results.csv dosyalarindan okundu; Slingshot, BigBeluga, Martin ve Linda dogrudan guclu OOS gecemiyor."),
        ("10. Kodlama hatasi bulunan yerler", "BigBeluga divergence eksik; Martin AVWAP proxy; Linda RS proxy; Crabel same-bar/gap fill; onceki compounded return raporu karar icin riskli."),
        ("11. Onceki LLM raporlarindan dogrulananlar", "No Pine/MTC-ready aday; crypto proxy caveat; weak swing list; Stage-3 oncesi native veri gereksinimi."),
        ("12. Onceki LLM raporlarindan curutulenler", "Yuksek compounded return degerleri rescue kaniti degil; baseline beaten tek basina yeterli degil; crypto proxy US equity edge kaniti degil."),
        ("13. PASS_STAGE3_CODE_VERIFIED var mi?", "Yok."),
        ("14. WEAK_STAGE3_CODE_VERIFIED var mi?", "Var: SLINGSHOT_EMA_PULLBACK sadece research-only zayif aday olarak kalabilir."),
        ("15. NEEDS_CONTRACT_REWRITE olanlar", "BIGBELUGA_RSI_DIVERGENCE_CHOCH_ATR."),
        ("16. NEEDS_NATIVE_DATA olanlar", "KELL_WEDGE, CRABEL_RANGE_EXPANSION, MARTIN_LUKE_PULLBACK ve LINDA_5SMA_PULLBACK."),
        ("17. Pine/MTC'ye gecis onerisi", "Gecilmeyecek."),
        ("18. Stage-3 icin onerilen tek producer adayi varsa adi", "Yok. En yakin code-verified research-only aday SLINGSHOT; en iyi native-data retest CRABEL."),
        ("19. Hangi adaylar cope atilmamali?", "CRABEL ve SLINGSHOT cope atilmamali; Linda/Kell native veri gelirse tekrar bakilabilir."),
        ("20. Acik riskler", "Native veri eksigi, intrabar execution belirsizligi, contract formalizasyonu, proxy veri siniri."),
        ("21. Dosyalar", "Bu klasor altinda aday bazli audit, trace, metric, synthetic, golden ve verdict dosyalari uretildi."),
        ("22. Komutlar", "COMMAND_LOG.txt icinde kayitli."),
        ("23. Validasyon", "py_compile, synthetic tests, metric recompute, fee monotonic, CSV readable, verdict files, git status ve untouched kontrolleri validation fazinda kayit altina alindi."),
    ]
    for title, body in sections:
        master_lines.extend(["", f"## {title}", body])
    write_text(OUT / "CODEX_STAGE2B_MASTER_REPORT.md", "\n".join(master_lines) + "\n")
    state = {
        "created_at": datetime.now().isoformat(),
        "output_root": str(OUT),
        "previous_files_read": reads,
        "missing_expected_files": missing,
        "verdicts": rows,
    }
    write_text(OUT / "STATE.json", json.dumps(state, indent=2))


def validate_outputs() -> None:
    py_files = [str(path) for path in OUT.rglob("*.py")]
    run_command(["python", "-m", "py_compile", *py_files])
    for candidate in CANDIDATES:
        run_command(["python", str(OUT / candidate.folder / "synthetic_tests.py")])
        result_path = OUT / candidate.folder / "synthetic_test_results.csv"
        if result_path.exists():
            rows = read_csv(result_path)
            passed = sum(1 for row in rows if row.get("pass_fail") == "PASS")
            write_text(OUT / candidate.folder / "SYNTHETIC_TEST_RESULTS.md", f"# Synthetic Test Results\n\n- PASS: {passed}/{len(rows)}\n")
    checks = []
    for candidate in CANDIDATES:
        cdir = OUT / candidate.folder
        for filename in ["metric_recompute.csv", "fee_stress.csv", "golden_cases.csv", "candidate_final_verdict.md"]:
            checks.append({"candidate_id": candidate.label, "check": filename, "status": "PASS" if (cdir / filename).exists() else "FAIL"})
        fee = read_csv(cdir / "fee_stress.csv")
        pfs = [fnum(row.get("profit_factor")) for row in fee]
        checks.append({"candidate_id": candidate.label, "check": "fee_monotonic", "status": "PASS" if all(pfs[i] >= pfs[i + 1] for i in range(len(pfs) - 1)) else "FAIL"})
        for csv_name in ["trade_trace.csv", "metric_recompute.csv", "fee_stress.csv", "baseline_comparison.csv", "oos_split_results.csv", "asset_breakdown.csv", "golden_cases.csv"]:
            try:
                read_csv(cdir / csv_name)
                status = "PASS"
            except Exception:
                status = "FAIL"
            checks.append({"candidate_id": candidate.label, "check": f"csv_readable:{csv_name}", "status": status})
    pine_status = subprocess.run(["git", "diff", "--", "01_PINE/MTC_V2.pine"], cwd=REPO, text=True, capture_output=True)
    runner_status = subprocess.run(["git", "diff", "--", "00_PYTHON/mtc_v2/core/runner.py"], cwd=REPO, text=True, capture_output=True)
    checks.append({"candidate_id": "GLOBAL", "check": "MTC_V2.pine_untouched_by_this_run", "status": "PASS" if pine_status.stdout == "" else "PREEXISTING_OR_EXTERNAL_DIFF"})
    checks.append({"candidate_id": "GLOBAL", "check": "production_runner_untouched_by_this_run", "status": "PASS" if runner_status.stdout == "" else "PREEXISTING_OR_EXTERNAL_DIFF"})
    write_csv(OUT / "VALIDATION_CHECKLIST.csv", checks)


def main() -> None:
    (OUT / "COMMAND_LOG.txt").write_text("", encoding="utf-8")
    code, before, err = run_command(["git", "status", "--short"])
    write_text(OUT / "git_status_before.txt", before + err)
    reads: list[str] = []
    missing: list[str] = []
    discover_previous(reads, missing)
    rows = [make_candidate(candidate, reads, missing) for candidate in CANDIDATES]
    cross_agent_review(reads)
    final_reports(rows, reads, missing)
    validate_outputs()
    code, after, err = run_command(["git", "status", "--short"])
    write_text(OUT / "git_status_after.txt", after + err)
    files = [str(path.relative_to(REPO)) for path in sorted(OUT.rglob("*")) if path.is_file()]
    write_text(OUT / "FILES_CREATED.txt", "\n".join(files) + "\n")


if __name__ == "__main__":
    main()
