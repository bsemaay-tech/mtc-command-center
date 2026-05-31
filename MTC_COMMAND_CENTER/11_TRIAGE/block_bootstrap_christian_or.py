"""Deeper validation for QL_OPEN_RANGE_5PCT_STOP_CHRISTIAN_5M.

Uses the focused validation JSON to recover each cell's best params, then
replays the strategy against the original OHLCV bundle to run:
  - circular block bootstrap over lockbox trade R series
  - 5-fold expanding rolling-origin OOS with param re-selection on train
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path
from typing import Any

import numpy as np


MCC_ROOT = Path(__file__).resolve().parents[1]
QLAB_ROOT = MCC_ROOT.parent / "01_MASTER TEMPLATE_V2" / "06_QUANTLENS_LAB"
TOOLS_ROOT = QLAB_ROOT / "tools"
FOCUSED_RESULTS = QLAB_ROOT / "05_BACKTEST_RESULTS" / "FOCUSED_VALIDATION_2026-05-31" / "MEGA_walk_forward_results.json"
OUT = MCC_ROOT / "11_TRIAGE" / "christian_or_validation_2026-05-31.md"

STRATEGY = "QL_OPEN_RANGE_5PCT_STOP_CHRISTIAN_5M"
CELLS = [
    ("OPUSDT", "1h"),
    ("ETHUSDT", "1h"),
    ("NEARUSDT", "4h"),
    ("TRXUSDT", "2h"),
    ("BTCUSDT", "15m"),
    ("BTCUSDT", "4h"),
]
N_BOOT = 10_000
ROLLING_FOLDS = 5


def main() -> int:
    sys.path.insert(0, str(TOOLS_ROOT))
    import mega_walk_forward as mw  # noqa: PLC0415
    import overnight_v2_runner as _v2  # noqa: F401, PLC0415

    focused = json.loads(FOCUSED_RESULTS.read_text(encoding="utf-8"))
    focused_rows = {
        (row.get("symbol"), row.get("timeframe")): row
        for row in focused.get("results", [])
        if row.get("strategy") == STRATEGY
    }
    manifest = json.loads(mw.BUNDLE_MANIFEST.read_text(encoding="utf-8"))
    grid = [
        {"or_bars": 1, "stop_pct": 0.05, "target_pct": 0.15},
        {"or_bars": 3, "stop_pct": 0.05, "target_pct": 0.15},
        {"or_bars": 5, "stop_pct": 0.05, "target_pct": 0.15},
        {"or_bars": 3, "stop_pct": 0.03, "target_pct": 0.10},
        {"or_bars": 3, "stop_pct": 0.07, "target_pct": 0.25},
    ]

    results = []
    for symbol, tf in CELLS:
        source_row = focused_rows[(symbol, tf)]
        params = source_row["summary"]["best_params"]
        df = _load_df(mw, manifest, symbol, tf)
        sig, stop = mw.build_signals(STRATEGY, df.copy(), params, None)
        lockbox_start = len(df) - int(len(df) * mw.LOCKBOX_FRACTION)
        lb_stats, lb_r = mw.simulate_slice(df, sig, stop, STRATEGY, lockbox_start, len(df), return_trades=True)
        block_size = max(1, int(round(math.sqrt(max(1, len(lb_r))))))
        block_p = _block_bootstrap_p(lb_r, block_size, N_BOOT, seed=abs(hash((symbol, tf))) % (2**31))
        roll = _rolling_origin(mw, df, grid)
        results.append(
            {
                "symbol": symbol,
                "timeframe": tf,
                "params": params,
                "focused_boot_p": source_row.get("boot_p_value"),
                "dsr_p": source_row.get("dsr_p_value"),
                "lockbox_return": lb_stats.net_return_pct,
                "lockbox_trades": lb_stats.num_trades,
                "lockbox_pf": lb_stats.profit_factor,
                "block_size": block_size,
                "block_bootstrap_p": block_p,
                "rolling_positive": sum(1 for item in roll if item["test_return_pct"] > 0),
                "rolling_folds": len(roll),
                "rolling_avg_return": round(float(np.mean([item["test_return_pct"] for item in roll])), 3) if roll else 0.0,
                "rolling": roll,
            }
        )

    OUT.write_text(_render_report(results), encoding="utf-8")
    print(OUT)
    return 0


def _load_df(mw: Any, manifest: dict[str, Any], symbol: str, tf: str):
    ds = mw.find_ds(manifest, symbol, tf)
    if ds is None:
        raise RuntimeError(f"No dataset for {symbol} {tf}")
    return mw.load_df(ds["normalized_path"])


def _block_bootstrap_p(values: np.ndarray, block_size: int, n_boot: int, seed: int) -> float:
    arr = np.asarray(values, dtype=float)
    n = len(arr)
    if n < 5:
        return float("nan")
    rng = np.random.default_rng(seed)
    means = np.empty(n_boot, dtype=float)
    starts_needed = int(math.ceil(n / block_size))
    for i in range(n_boot):
        starts = rng.integers(0, n, size=starts_needed)
        sample = np.concatenate([np.take(arr, np.arange(s, s + block_size) % n) for s in starts])[:n]
        means[i] = sample.mean()
    return round(float((means <= 0).mean()), 5)


def _rolling_origin(mw: Any, df, grid: list[dict[str, Any]]) -> list[dict[str, Any]]:
    n = len(df)
    lockbox_start = n - int(n * mw.LOCKBOX_FRACTION)
    min_train = int(lockbox_start * 0.40)
    test_size = max(200, int((lockbox_start - min_train) / ROLLING_FOLDS))
    out = []
    for fold in range(ROLLING_FOLDS):
        train_end = min_train + fold * test_size
        test_end = min(train_end + test_size, lockbox_start)
        if test_end - train_end < 200:
            continue
        best = None
        for params in grid:
            sig, stop = mw.build_signals(STRATEGY, df.copy(), params, None)
            train = mw.simulate_slice(df, sig, stop, STRATEGY, 0, train_end)
            if best is None or train.net_return_pct > best["train_return_pct"]:
                test = mw.simulate_slice(df, sig, stop, STRATEGY, train_end, test_end)
                best = {
                    "fold": fold + 1,
                    "params": params,
                    "train_return_pct": train.net_return_pct,
                    "test_return_pct": test.net_return_pct,
                    "test_trades": test.num_trades,
                    "test_pf": test.profit_factor,
                }
        if best:
            out.append(best)
    return out


def _render_report(results: list[dict[str, Any]]) -> str:
    block_pass = sum(1 for r in results if r["block_bootstrap_p"] <= 0.10)
    joint_pass = sum(
        1
        for r in results
        if r["block_bootstrap_p"] <= 0.10 and r["rolling_positive"] >= max(1, math.ceil(r["rolling_folds"] / 2))
    )
    decision = (
        "PROMOTE_TO_PINETS_PARITY_REVIEW"
        if block_pass >= 4
        else "HOLD_FOR_MORE_VALIDATION"
    )
    lines = [
        "# Christian Open Range 5% Stop Validation - 2026-05-31",
        "",
        f"- Strategy: `{STRATEGY}`",
        f"- Cells tested: {len(results)}",
        f"- Block bootstrap: {N_BOOT} resamples, block_size = round(sqrt(lockbox trades))",
        f"- Rolling-origin OOS: {ROLLING_FOLDS} expanding folds, param re-selected on train from focused grid",
        f"- Decision rule from handoff: >=4/6 cells with block_bootstrap p <= 0.10 => propose parity promotion",
        f"- Result: {block_pass}/6 block-pass, {joint_pass}/6 block+rolling-pass",
        f"- Recommendation: **{decision}**",
        "",
        "| Symbol | TF | Params | Trades | Ret % | PF | Focused p | DSR p | Block | Block p | Roll + | Roll avg % | Verdict |",
        "|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for r in results:
        verdict = "PASS" if r["block_bootstrap_p"] <= 0.10 else "WATCH"
        lines.append(
            f"| {r['symbol']} | {r['timeframe']} | `{json.dumps(r['params'], separators=(',', ':'))}` | "
            f"{r['lockbox_trades']} | {r['lockbox_return']:.2f} | {r['lockbox_pf']:.3f} | "
            f"{r['focused_boot_p']} | {r['dsr_p']} | {r['block_size']} | {r['block_bootstrap_p']:.5f} | "
            f"{r['rolling_positive']}/{r['rolling_folds']} | {r['rolling_avg_return']:.2f} | {verdict} |"
        )
    lines += ["", "## Rolling-Origin Fold Detail", ""]
    for r in results:
        lines += [f"### {r['symbol']} {r['timeframe']}", "", "| Fold | Train ret % | Test ret % | Test trades | Test PF | Params |", "|---:|---:|---:|---:|---:|---|"]
        for item in r["rolling"]:
            lines.append(
                f"| {item['fold']} | {item['train_return_pct']:.2f} | {item['test_return_pct']:.2f} | "
                f"{item['test_trades']} | {item['test_pf']:.3f} | `{json.dumps(item['params'], separators=(',', ':'))}` |"
            )
        lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    raise SystemExit(main())
