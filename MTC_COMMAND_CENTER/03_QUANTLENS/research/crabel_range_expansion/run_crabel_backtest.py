from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pandas as pd

from crabel_range_expansion import (
    EXIT_VARIANTS,
    EXPANSION_MULTS,
    PRIMARY_EXPANSION_MULT,
    PRIMARY_SAME_BAR_MODE,
    SAME_BAR_BOTH_MODES,
    SYMBOLS,
    aggregate_portfolio,
    generate_report,
    load_manifest_datasets,
    load_ohlcv,
    run_backtest,
)


ROOT = Path(__file__).resolve().parents[3]
PROJECT_PARENT = ROOT.parent
BUNDLE_ROOT = PROJECT_PARENT / "MTC_V2_OPTIMIZATION_DATA_BUNDLE_20260427"
OUTPUT_ROOT = ROOT / "06_QUANTLENS_LAB" / "research" / "crabel_range_expansion"
REPORTS_DIR = OUTPUT_ROOT / "reports"
RESULTS_CSV = REPORTS_DIR / "QL_CRABEL_RANGE_EXPANSION_RESULTS.csv"
TRADES_CSV = REPORTS_DIR / "QL_CRABEL_RANGE_EXPANSION_TRADES.csv"
REPORT_MD = REPORTS_DIR / "QL_CRABEL_RANGE_EXPANSION_REPORT.md"


def run_command(command: list[str]) -> str:
    completed = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, check=False)
    output = (completed.stdout + completed.stderr).strip()
    if completed.returncode != 0:
        return f"EXIT {completed.returncode}\n{output}"
    return output


def main() -> int:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    commands_run = [
        "git status --short",
        "python -m py_compile 06_QUANTLENS_LAB/research/crabel_range_expansion/crabel_range_expansion.py 06_QUANTLENS_LAB/research/crabel_range_expansion/run_crabel_backtest.py",
        "python 06_QUANTLENS_LAB/research/crabel_range_expansion/run_crabel_backtest.py",
        "git diff --stat",
        "git status --short",
    ]
    git_status_before = run_command(["git", "status", "--short"])
    datasets = load_manifest_datasets(BUNDLE_ROOT, SYMBOLS)
    results: list[dict[str, object]] = []
    all_trades: list[pd.DataFrame] = []
    data_by_symbol = {symbol: load_ohlcv(info.path) for symbol, info in datasets.items()}
    for symbol in SYMBOLS:
        data = data_by_symbol[symbol]
        for expansion_mult in EXPANSION_MULTS:
            for exit_variant in EXIT_VARIANTS:
                for same_bar_mode in SAME_BAR_BOTH_MODES:
                    metrics, trades, _equity = run_backtest(symbol, data, expansion_mult, exit_variant, same_bar_mode)
                    results.append(metrics)
                    if not trades.empty:
                        all_trades.append(trades)
    results_frame = pd.DataFrame(results)
    trades_frame = pd.concat(all_trades, ignore_index=True) if all_trades else pd.DataFrame()
    portfolio_rows = [
        aggregate_portfolio(results_frame, trades_frame, PRIMARY_EXPANSION_MULT, exit_variant, PRIMARY_SAME_BAR_MODE)
        for exit_variant in EXIT_VARIANTS
    ]
    portfolio_rows.extend(
        aggregate_portfolio(results_frame, trades_frame, PRIMARY_EXPANSION_MULT, "close_exit", same_bar_mode)
        for same_bar_mode in SAME_BAR_BOTH_MODES
        if same_bar_mode != PRIMARY_SAME_BAR_MODE
    )
    results_frame.to_csv(RESULTS_CSV, index=False)
    trades_frame.to_csv(TRADES_CSV, index=False)
    verification_lines = [
        "Backtest command completed and generated result CSV, trade CSV, and markdown report.",
        f"Results rows: {len(results_frame)}.",
        f"Trade rows: {len(trades_frame)}.",
        f"Primary grid: expansion_mult={PRIMARY_EXPANSION_MULT}, same_bar_both_mode={PRIMARY_SAME_BAR_MODE}.",
    ]
    generate_report(
        REPORT_MD,
        results_frame,
        trades_frame,
        datasets,
        [row for row in portfolio_rows if row],
        commands_run,
        git_status_before,
        "pending final status refresh",
        "pending final diff refresh",
        verification_lines,
    )
    git_diff_stat = run_command(["git", "diff", "--stat"])
    git_status_after = run_command(["git", "status", "--short"])
    verdict = generate_report(
        REPORT_MD,
        results_frame,
        trades_frame,
        datasets,
        [row for row in portfolio_rows if row],
        commands_run,
        git_status_before,
        git_status_after,
        git_diff_stat,
        verification_lines,
    )
    print(f"verdict={verdict}")
    print(f"results={RESULTS_CSV}")
    print(f"trades={TRADES_CSV}")
    print(f"report={REPORT_MD}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
