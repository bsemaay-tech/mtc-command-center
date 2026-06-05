#!/usr/bin/env python
"""Combinatorial Purged Cross-Validation validator for MEGA result artifacts."""

from __future__ import annotations

import argparse
import itertools
import json
import sys
from pathlib import Path
from statistics import median

import numpy as np

TOOLS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS_DIR))

import mega_walk_forward as mw  # noqa: E402


def contiguous_groups(n_rows: int, n_groups: int) -> list[tuple[int, int]]:
    edges = np.linspace(0, n_rows, n_groups + 1, dtype=int)
    return [(int(edges[i]), int(edges[i + 1])) for i in range(n_groups) if edges[i + 1] > edges[i]]


def purged_train_bars(groups: list[tuple[int, int]], test_ids: tuple[int, ...], embargo_bars: int) -> int:
    test_windows = [(groups[i][0] - embargo_bars, groups[i][1] + embargo_bars) for i in test_ids]
    total = 0
    for idx, (start, end) in enumerate(groups):
        if idx in test_ids:
            continue
        overlaps = any(start < test_end and end > test_start for test_start, test_end in test_windows)
        if not overlaps:
            total += end - start
    return total


def compound_returns(returns_pct: list[float]) -> float:
    eq = 1.0
    for ret in returns_pct:
        eq *= 1.0 + (ret / 100.0)
    return (eq - 1.0) * 100.0


def evaluate_split(df, sig, stop, strategy: str, ranges: list[tuple[int, int]], direction: str = "long") -> dict:
    stats = [mw.simulate_slice(df, sig, stop, strategy, start, end, direction=direction) for start, end in ranges]
    returns = [float(s.net_return_pct) for s in stats]
    trades = sum(int(s.num_trades) for s in stats)
    drawdown = min((float(s.max_drawdown_pct) for s in stats), default=0.0)
    pfs = [float(s.profit_factor) for s in stats if s.num_trades > 0]
    return {
        "return_pct": round(compound_returns(returns), 3),
        "trades": trades,
        "max_drawdown_pct": round(drawdown, 3),
        "profit_factor_median": round(median(pfs), 3) if pfs else 0.0,
    }


def load_rows(path: Path) -> list[dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    rows = data.get("results", data) if isinstance(data, dict) else data
    return [r for r in rows if r.get("classification") in {"PASS", "STRONG_PASS"} and r.get("summary", {}).get("best_params")]


def validate_candidate(row: dict, manifest: dict, args) -> dict:
    strategy = row["strategy"]
    symbol = row["symbol"]
    tf = row["timeframe"]
    params = row["summary"]["best_params"]

    ds = mw.find_ds(manifest, symbol, tf)
    if ds is None:
        return {"strategy": strategy, "symbol": symbol, "timeframe": tf, "status": "N_A",
                "reason": "No dataset found in manifest for this symbol/timeframe"}

    df = mw.load_df(ds["normalized_path"])
    groups = contiguous_groups(len(df), args.n_groups)
    if len(groups) < args.n_groups:
        return {"strategy": strategy, "symbol": symbol, "timeframe": tf, "status": "INSUFFICIENT_DATA",
                "reason": f"Only {len(groups)} groups available, need {args.n_groups}"}

    try:
        dmap = None
        if strategy == "QL_2026-05-01_SWING_1H_DUAL_RSI_60_40_PULLBACK":
            daily = mw.build_daily_rsi(manifest, symbol)
            dmap = daily.get(int(params["rsi_len"])) if daily else None

        df_w = df.copy()
        result = mw.build_signals(strategy, df_w, params, dmap)
        if isinstance(result, tuple) and len(result) == 3 and result[2] in {"long", "short"}:
            sig, stop, direction = result
        else:
            sig, stop = result[:2]
            direction = "long"

        embargo_bars = max(1, int(len(df_w) * args.embargo_pct))
        split_rows = []
        for test_ids in itertools.combinations(range(args.n_groups), args.test_groups):
            test_ranges = [groups[i] for i in test_ids]
            split = evaluate_split(df_w, sig, stop, strategy, test_ranges, direction=direction)
            split["test_groups"] = list(test_ids)
            split["train_bars_after_purge"] = purged_train_bars(groups, test_ids, embargo_bars)
            split["pass"] = bool(
                split["trades"] >= args.min_trades
                and split["return_pct"] > 0
                and split["profit_factor_median"] >= args.min_pf
                and split["max_drawdown_pct"] > args.max_dd_floor
            )
            split_rows.append(split)

        pass_count = sum(1 for s in split_rows if s["pass"])
        returns = [s["return_pct"] for s in split_rows]
        trades = [s["trades"] for s in split_rows]
        return {
            "strategy": strategy,
            "symbol": symbol,
            "timeframe": tf,
            "status": "OK",
            "params": params,
            "n_groups": args.n_groups,
            "test_groups_per_split": args.test_groups,
            "embargo_bars": embargo_bars,
            "splits": len(split_rows),
            "pass_count": pass_count,
            "pass_rate": round(pass_count / len(split_rows), 4) if split_rows else 0.0,
            "return_median_pct": round(median(returns), 3) if returns else 0.0,
            "return_min_pct": round(min(returns), 3) if returns else 0.0,
            "trades_median": round(median(trades), 3) if trades else 0.0,
            "split_results": split_rows,
        }
    except Exception as exc:
        return {
            "strategy": strategy,
            "symbol": symbol,
            "timeframe": tf,
            "status": "TOOL_FAILED",
            "reason": f"{type(exc).__name__}: {exc}",
        }


def write_markdown(path: Path, results: list[dict], args) -> None:
    lines = [
        "# CPCV Validation Report",
        "",
        f"- Input: `{args.input}`",
        f"- Groups: `{args.n_groups}` | test groups per split: `{args.test_groups}` | embargo: `{args.embargo_pct}`",
        f"- Candidates evaluated: `{len(results)}`",
        "",
        "| Strategy | Symbol | TF | Status | Splits Pass | Pass Rate | Median Ret % | Min Ret % | Median Trades |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for r in results:
        lines.append(
            f"| `{r.get('strategy','')[:42]}` | {r.get('symbol','')} | {r.get('timeframe','')} | "
            f"{r.get('status')} | {r.get('pass_count',0)}/{r.get('splits',0)} | "
            f"{r.get('pass_rate',0):.2f} | {r.get('return_median_pct',0):.2f} | "
            f"{r.get('return_min_pct',0):.2f} | {r.get('trades_median',0):.0f} |"
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=TOOLS_DIR / "sprint_runs" / "MEGA_results_iter_1_20260601_054633.json")
    parser.add_argument("--out-dir", type=Path, default=TOOLS_DIR / "cpcv_runs")
    parser.add_argument("--max-candidates", type=int, default=0, help="Maximum PASS/STRONG_PASS candidates to validate; 0 means no cap")
    parser.add_argument("--n-groups", type=int, default=6)
    parser.add_argument("--test-groups", type=int, default=2)
    parser.add_argument("--embargo-pct", type=float, default=0.01)
    parser.add_argument("--min-trades", type=int, default=mw.MIN_TRADES_FOR_PASS)
    parser.add_argument("--min-pf", type=float, default=1.0)
    parser.add_argument("--max-dd-floor", type=float, default=-50.0)
    parser.add_argument("--v2", action="store_true", help="import overnight_v2_runner to patch newer strategies")
    args = parser.parse_args()

    if args.v2:
        import overnight_v2_runner  # noqa: F401

    manifest = json.load(open(mw.BUNDLE_MANIFEST, encoding="utf-8"))
    rows = load_rows(args.input)
    if args.max_candidates and args.max_candidates > 0:
        rows = rows[: args.max_candidates]
    results = [validate_candidate(row, manifest, args) for row in rows]

    args.out_dir.mkdir(parents=True, exist_ok=True)
    out_json = args.out_dir / "cpcv_results.json"
    out_md = args.out_dir / "CPCV_VALIDATION_REPORT.md"
    out_json.write_text(json.dumps({"input": str(args.input), "results": results}, indent=2), encoding="utf-8")
    write_markdown(out_md, results, args)
    print(f"Wrote {out_json}")
    print(f"Wrote {out_md}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
