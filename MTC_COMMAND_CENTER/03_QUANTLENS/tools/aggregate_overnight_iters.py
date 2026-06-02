"""Aggregate PASS/STRONG_PASS results across all overnight_runs iterations.

Outputs a Markdown report ranking candidates by how many iterations they
PASS — true robustness comes from CONSISTENCY across resamples, not from
a single lucky run.
"""

from __future__ import annotations

import json
import argparse
import math
import shutil
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean, median, stdev

DEFAULT_RUNS_DIR = Path(__file__).resolve().parent / "overnight_runs"
DEFAULT_OUT_PATH = DEFAULT_RUNS_DIR.parent / "OVERNIGHT_AGGREGATED_REPORT.md"
# Dashboard backtest_reader scans this dir for *_results.json (matrix WF format).
BACKTEST_RESULTS_DIR = Path(__file__).resolve().parent.parent / "05_BACKTEST_RESULTS"


def export_to_backtest_results(files, dest_dir=BACKTEST_RESULTS_DIR):
    """Copy aggregated MEGA iteration JSONs into the dashboard's
    05_BACKTEST_RESULTS dir so backtest_reader picks them up.

    Each file is renamed to end with `_results.json` because the reader's
    glob is `*_results.json`; MEGA filenames otherwise wouldn't match.
    """
    dest_dir.mkdir(parents=True, exist_ok=True)
    count = 0
    for src in files:
        target = dest_dir / f"{src.stem}_results.json"
        shutil.copy2(src, target)
        count += 1
    return count


def load_results(runs_dir: Path):
    files = sorted(runs_dir.glob("MEGA_results_iter_*.json"))
    return files


def iter_classifications(results_json):
    """Yield row dicts with correctly-nested metrics from MEGA results JSON."""
    data = json.loads(Path(results_json).read_text(encoding="utf-8"))
    rows = data.get("results", data) if isinstance(data, dict) else data
    for r in rows:
        summary = r.get("summary") or {}
        lb = summary.get("lockbox_oos") or {}
        yield {
            "strategy": r.get("strategy", ""),
            "sym": r.get("symbol", ""),
            "tf": r.get("timeframe", ""),
            "class": r.get("classification", ""),
            "ret": lb.get("net_return_pct"),
            "sharpe": lb.get("sharpe_pt"),
            "trades": lb.get("num_trades"),
            "boot_p": r.get("boot_p_value"),
            "dsr_p": r.get("dsr_p_value"),
            "pf": lb.get("profit_factor"),
            "max_dd": lb.get("max_drawdown_pct"),
            "folds_pos": summary.get("folds_positive"),
            "robust_final": r.get("robust_final"),
            "bh_fdr": r.get("bh_fdr_survivor"),
            "dsr_robust": r.get("dsr_robust"),
        }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runs-dir", type=Path, default=DEFAULT_RUNS_DIR)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT_PATH)
    args = parser.parse_args()

    runs_dir = args.runs_dir.resolve()
    out_path = args.out.resolve()
    files = load_results(runs_dir)
    print(f"Aggregating {len(files)} iteration result files...")
    if not files:
        print("No results found.")
        return

    # key = (strategy, sym, tf)
    pass_counter: dict[tuple, int] = Counter()
    strong_pass_counter: dict[tuple, int] = Counter()
    metric_acc: dict[tuple, list] = defaultdict(list)
    iter_total = 0

    for f in files:
        iter_total += 1
        for row in iter_classifications(f):
            key = (row["strategy"], row["sym"], row["tf"])
            if row["class"] == "PASS":
                pass_counter[key] += 1
            elif row["class"] == "STRONG_PASS":
                strong_pass_counter[key] += 1
                pass_counter[key] += 1  # STRONG_PASS counts as PASS too
            if row["class"] in ("PASS", "STRONG_PASS"):
                if row["ret"] is not None and row["sharpe"] is not None:
                    metric_acc[key].append({
                        "ret": float(row["ret"]),
                        "sharpe": float(row["sharpe"]) if row["sharpe"] is not None else None,
                        "trades": int(row["trades"] or 0),
                        "boot_p": float(row["boot_p"]) if row["boot_p"] is not None else None,
                        "dsr_p": float(row["dsr_p"]) if row["dsr_p"] is not None else None,
                        "pf": float(row["pf"]) if row["pf"] is not None else None,
                        "max_dd": float(row["max_dd"]) if row["max_dd"] is not None else None,
                        "folds_pos": row.get("folds_pos"),
                    })

    # Build summary rows
    rows_summary = []
    for key, n in pass_counter.items():
        strategy, sym, tf = key
        metrics = metric_acc.get(key, [])
        if not metrics:
            continue
        rets = [m["ret"] for m in metrics if m["ret"] is not None]
        sharpes = [m["sharpe"] for m in metrics if m["sharpe"] is not None]
        boots = [m["boot_p"] for m in metrics if m["boot_p"] is not None]
        dsrs = [m["dsr_p"] for m in metrics if m["dsr_p"] is not None]
        pfs = [m["pf"] for m in metrics if m["pf"] is not None]
        dds = [m["max_dd"] for m in metrics if m["max_dd"] is not None]
        trades = [m["trades"] for m in metrics if m["trades"] is not None]

        rows_summary.append({
            "strategy": strategy, "sym": sym, "tf": tf,
            "iters_passed": n,
            "iters_strong": strong_pass_counter.get(key, 0),
            "pass_rate": n / iter_total,
            "ret_median": median(rets) if rets else None,
            "ret_stdev": stdev(rets) if len(rets) >= 2 else None,
            "sharpe_median": median(sharpes) if sharpes else None,
            "boot_p_median": median(boots) if boots else None,
            "dsr_p_median": median(dsrs) if dsrs else None,
            "pf_median": median(pfs) if pfs else None,
            "max_dd_median": median(dds) if dds else None,
            "trades_median": median(trades) if trades else None,
        })

    rows_summary.sort(key=lambda r: (-r["iters_passed"], -(r["ret_median"] or 0)))

    out = []
    out.append("# OVERNIGHT AGGREGATED REPORT — cross-iteration robustness\n")
    out.append(f"- Iterations aggregated: **{iter_total}**")
    out.append(f"- Distinct (strategy × sym × tf) cells that PASSed at least once: **{len(rows_summary)}**")
    out.append("")
    out.append("## Methodology")
    out.append("")
    out.append("Each row below is a (strategy, symbol, timeframe) cell. `iters_passed` counts how many of "
               f"the {iter_total} independent runs classified this cell as PASS or STRONG_PASS. "
               "True robustness = high iters_passed AND tight ret_stdev. Single-iter PASSes that don't repeat "
               "are likely noise.\n")
    out.append("## ROBUST winners (iters_passed >= 50% of runs)\n")
    threshold = math.ceil(iter_total * 0.5)
    winners = [r for r in rows_summary if r["iters_passed"] >= threshold]
    if winners:
        out.append("| Strategy | Sym | TF | Pass×/N | Strong× | Ret median % | Ret stdev | Sharpe med | Boot p med | DSR p med | PF med | DD med % | Trades med |")
        out.append("|---|---|---|---|---|---|---|---|---|---|---|---|---|")
        for r in winners:
            out.append(
                f"| `{r['strategy']}` | {r['sym']} | {r['tf']} | "
                f"**{r['iters_passed']}/{iter_total}** | {r['iters_strong']} | "
                f"{r['ret_median']:.2f} | {r['ret_stdev'] or 0:.2f} | "
                f"{r['sharpe_median'] or 0:.2f} | {r['boot_p_median'] if r['boot_p_median'] is not None else 1:.4f} | "
                f"{r['dsr_p_median'] if r['dsr_p_median'] is not None else 1:.4f} | {r['pf_median'] or 0:.3f} | "
                f"{r['max_dd_median'] or 0:.1f} | {r['trades_median'] or 0:.0f} |"
            )
    else:
        out.append("_None — no (strategy × sym × tf) cell PASSed in the majority of iterations._\n")
    out.append("")

    out.append(f"## All PASS cells (any iteration count)\n")
    out.append("| Strategy | Sym | TF | Pass×/N | Strong× | Ret med % | Ret stdev | Sharpe med | Boot p med | PF med | DD med % | Trades med |")
    out.append("|---|---|---|---|---|---|---|---|---|---|---|---|")
    for r in rows_summary[:200]:
        out.append(
            f"| `{r['strategy']}` | {r['sym']} | {r['tf']} | "
            f"{r['iters_passed']}/{iter_total} | {r['iters_strong']} | "
            f"{r['ret_median']:.2f} | {r['ret_stdev'] or 0:.2f} | "
            f"{r['sharpe_median'] or 0:.2f} | {r['boot_p_median'] if r['boot_p_median'] is not None else 1:.4f} | "
            f"{r['pf_median'] or 0:.3f} | {r['max_dd_median'] or 0:.1f} | "
            f"{r['trades_median'] or 0:.0f} |"
        )
    if len(rows_summary) > 200:
        out.append(f"\n_(showing top 200 of {len(rows_summary)} total cells)_\n")

    # Per-strategy pass-rate summary
    by_strat = defaultdict(list)
    for r in rows_summary:
        by_strat[r["strategy"]].append(r)
    out.append("\n## Per-strategy summary\n")
    out.append("| Strategy | Cells PASSed ≥ 1× | Cells PASSed ≥ 50% iters | Best (sym/tf) | Best ret med % |")
    out.append("|---|---|---|---|---|")
    strat_rows = []
    for strat, items in by_strat.items():
        cells_any = len(items)
        cells_robust = sum(1 for it in items if it["iters_passed"] >= threshold)
        best = max(items, key=lambda r: (r["iters_passed"], r["ret_median"] or 0))
        strat_rows.append((strat, cells_any, cells_robust, best))
    strat_rows.sort(key=lambda x: -x[2])
    for strat, cells_any, cells_robust, best in strat_rows:
        out.append(f"| `{strat}` | {cells_any} | **{cells_robust}** | {best['sym']} {best['tf']} | {best['ret_median']:.2f} |")

    out_path.write_text("\n".join(out), encoding="utf-8")
    print(f"Wrote {out_path}")
    print(f"  iters: {iter_total}")
    print(f"  distinct PASS cells: {len(rows_summary)}")
    print(f"  robust winners (>= {threshold}/{iter_total} iters): {len([r for r in rows_summary if r['iters_passed'] >= threshold])}")

    exported = export_to_backtest_results(files)
    print(f"Exported {exported} files to 05_BACKTEST_RESULTS")


if __name__ == "__main__":
    main()
