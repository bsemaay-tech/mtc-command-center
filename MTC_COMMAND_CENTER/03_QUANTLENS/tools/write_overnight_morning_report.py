"""Write a compact morning report from overnight MEGA iteration artifacts."""
from __future__ import annotations

import argparse
import json
import math
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from statistics import median


def _load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def _fmt_num(value, digits=2, suffix=""):
    if value is None:
        return "-"
    try:
        return f"{float(value):.{digits}f}{suffix}"
    except (TypeError, ValueError):
        return str(value)


def _class_rows(files):
    pass_counter = Counter()
    strong_counter = Counter()
    metrics = defaultdict(list)
    class_counts = Counter()
    config = {}
    generated = []

    for file in files:
        data = _load_json(file)
        config = data.get("config") or config
        generated.append(data.get("generated_utc"))
        for row in data.get("results", []):
            cls = row.get("classification", "")
            class_counts[cls] += 1
            key = (row.get("strategy", ""), row.get("symbol", ""), row.get("timeframe", ""))
            summary = row.get("summary") or {}
            lb = summary.get("lockbox_oos") or {}
            if cls in {"PASS", "STRONG_PASS"}:
                pass_counter[key] += 1
                if cls == "STRONG_PASS":
                    strong_counter[key] += 1
                metrics[key].append(
                    {
                        "ret": lb.get("net_return_pct"),
                        "pf": lb.get("profit_factor"),
                        "max_dd": lb.get("max_drawdown_pct"),
                        "trades": lb.get("num_trades"),
                        "sharpe": lb.get("sharpe"),
                        "boot_p": row.get("boot_p_value"),
                        "dsr_p": row.get("dsr_p_value"),
                    }
                )

    iter_total = len(files)
    threshold = math.ceil(iter_total * 0.5) if iter_total else 0
    robust = []
    for key, passed in pass_counter.items():
        vals = metrics[key]
        robust.append(
            {
                "strategy": key[0],
                "symbol": key[1],
                "timeframe": key[2],
                "iters_passed": passed,
                "iters_strong": strong_counter.get(key, 0),
                "ret_median": median([v["ret"] for v in vals if v["ret"] is not None]) if vals else None,
                "pf_median": median([v["pf"] for v in vals if v["pf"] is not None]) if vals else None,
                "max_dd_median": median([v["max_dd"] for v in vals if v["max_dd"] is not None]) if vals else None,
                "trades_median": median([v["trades"] for v in vals if v["trades"] is not None]) if vals else None,
                "boot_p_median": median([v["boot_p"] for v in vals if v["boot_p"] is not None]) if vals else None,
                "dsr_p_median": median([v["dsr_p"] for v in vals if v["dsr_p"] is not None]) if vals else None,
            }
        )
    robust.sort(key=lambda r: (-r["iters_passed"], -(r["ret_median"] or 0)))
    robust_winners = [r for r in robust if r["iters_passed"] >= threshold]
    return config, generated, class_counts, robust, robust_winners, threshold


def _alpha_by_key(path: Path):
    if not path.exists():
        return {}
    data = _load_json(path)
    rows = data.get("all_ranked_by_excess") or []
    return {(r["strategy"], r["symbol"], r["timeframe"]): r for r in rows}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runs-dir", type=Path, required=True)
    parser.add_argument("--results-dir", type=Path, required=True)
    parser.add_argument("--night-id", required=True)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()

    files = sorted(args.runs_dir.glob("MEGA_results_iter_*.json"))
    out = args.out or (args.results_dir / f"MORNING_REPORT_{args.night_id}.md")
    if not files:
        out.write_text(
            f"# MORNING REPORT - {args.night_id}\n\nNo completed MEGA iteration JSON files were found.\n",
            encoding="utf-8",
        )
        return

    config, generated, class_counts, robust, robust_winners, threshold = _class_rows(files)
    # A18 FIX (2026-06-04): alpha counts + tables come from the canonical
    # alpha_vs_buyhold lists = single source of truth that must match the
    # `ALPHA_DONE passes=.. beat_buyhold=.. down_market_alpha=..` log line.
    # The old code intersected robust_winners with all_ranked_by_excess and
    # filtered down-market on `alpha_in_down_market` alone (missing the
    # regime_robust AND param_stable gates), so it over-counted (reported 78
    # vs the true 8) and the down-market table was a copy of the beat-b&h table.
    alpha_path = args.results_dir / "alpha_summary.json"
    alpha_full = _load_json(alpha_path) if alpha_path.exists() else {}
    alpha_all = alpha_full.get("all_ranked_by_excess", [])
    canon_down = alpha_full.get("down_market_alpha", [])
    beat_bh_rows = sorted(
        (a for a in alpha_all if a.get("beat_buyhold")),
        key=lambda a: a.get("excess_alpha") or 0, reverse=True,
    )
    beat_bh_count = len(beat_bh_rows)
    down_count = len(canon_down)
    # Drift guard: recomputing the down-market filter from all_ranked must match
    # the canonical pre-filtered list. A mismatch means alpha_vs_buyhold and this
    # writer disagree on the definition -> investigate before trusting the report.
    recomputed_down = [a for a in alpha_all
                       if a.get("alpha_in_down_market")
                       and a.get("regime_robust") and a.get("param_stable")]
    if len(recomputed_down) != down_count:
        print(f"WARN A18: recomputed down-market {len(recomputed_down)} "
              f"!= canonical down_market_alpha {down_count}")
    dsr_research = [r for r in robust_winners if (r.get("dsr_p_median") or 0) >= 0.50]
    strategy_count = config.get("strategy_count") or 0
    param_sets = config.get("param_set_total") or 0
    results_per_iter = len(_load_json(files[0]).get("results", []))
    avg_params = max(1, param_sets // max(1, strategy_count))
    est_per_iter = results_per_iter * avg_params
    est_total = est_per_iter * len(files)

    lines = [
        f"# MORNING REPORT - Overnight QuantLens Sweep {args.night_id}",
        "",
        "> What changed / What matters / Next action",
        f"> - Changed: {len(files)} completed iterations, estimated {est_total:,} parameter evaluations, workers from artifact config: {config.get('workers', '-')}.",
        f"> - Matters: {len(robust_winners)} robust PASS cells at >={threshold}/{len(files)} iterations; {beat_bh_count} beat buy-and-hold; {down_count} are down-market alpha (regime-robust + param-stable). DSR research-threshold confirmations: {len(dsr_research)}.",
        "> - Next action: Treat results as research evidence only. No Pine, MTC, parity, defaults, or live-trading action is authorized by this report.",
        "",
        "## Executive Summary",
        "",
        f"The loop produced {len(files)} completed MEGA walk-forward iterations from `{args.runs_dir}`. "
        f"Each full iteration evaluates about {est_per_iter:,} strategy-cell parameter combinations "
        f"({results_per_iter} cells x average grid {avg_params}), for an estimated total of {est_total:,}.",
        "",
        "## Tested Universe",
        "",
        f"- Strategies: {strategy_count}",
        f"- Param sets total: {param_sets}",
        f"- Symbols: {len(config.get('selected_symbols') or config.get('symbols') or [])}",
        f"- Timeframes: {config.get('selected_timeframes') or config.get('timeframes') or []}",
        "",
        "## Classification Counts",
        "",
        "| Class | Count across all iterations |",
        "|---|---:|",
    ]
    for cls, count in class_counts.most_common():
        lines.append(f"| `{cls}` | {count} |")

    lines += [
        "",
        "## Robust Winners",
        "",
        f"Robust threshold: >={threshold}/{len(files)} iterations.",
        "",
        "| Strategy | Symbol | TF | Pass/N | Strong | Median Ret % | Median PF | Median DD % | Median Trades | Median DSR p |",
        "|---|---|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for r in robust_winners[:30]:
        lines.append(
            f"| `{r['strategy'][:38]}` | {r['symbol']} | {r['timeframe']} | "
            f"{r['iters_passed']}/{len(files)} | {r['iters_strong']} | "
            f"{_fmt_num(r['ret_median'])} | {_fmt_num(r['pf_median'], 3)} | "
            f"{_fmt_num(r['max_dd_median'])} | {_fmt_num(r['trades_median'], 0)} | "
            f"{_fmt_num(r['dsr_p_median'], 4)} |"
        )
    if not robust_winners:
        lines.append("| _(none)_ | | | | | | | | | |")

    lines += [
        "",
        "## Strategy vs Buy-and-Hold",
        "",
        "| Strategy | Symbol | TF | Strategy % | B&H % | Excess Alpha % | PF | Trades | DSR p |",
        "|---|---|---|---:|---:|---:|---:|---:|---:|",
    ]
    for a in beat_bh_rows[:20]:
        lines.append(
            f"| `{a['strategy'][:38]}` | {a['symbol']} | {a['timeframe']} | "
            f"{_fmt_num(a.get('strategy_lockbox_ret'))} | {_fmt_num(a.get('buyhold_lockbox_ret'))} | "
            f"{_fmt_num(a.get('excess_alpha'))} | {_fmt_num(a.get('pf'), 3)} | "
            f"{a.get('trades', '-')} | {_fmt_num(a.get('dsr_p'), 4)} |"
        )
    if not beat_bh_rows:
        lines.append("| _(alpha_summary.json missing or no beat-buyhold cells)_ | | | | | | | | |")

    lines += [
        "",
        "## Down-Market Alpha",
        "",
        "These cells made money while buy-and-hold was negative, AND survived "
        "regime-robustness (>=3/5 windows) + parameter-stability. They are still "
        "not approved for MTC_v2 integration.",
        "",
        "| Strategy | Symbol | TF | Strategy % | B&H % | Excess Alpha % | PF | Trades | DSR p |",
        "|---|---|---|---:|---:|---:|---:|---:|---:|",
    ]
    canon_down_sorted = sorted(canon_down, key=lambda a: a.get("excess_alpha") or 0, reverse=True)
    for a in canon_down_sorted[:20]:
        lines.append(
            f"| `{a['strategy'][:38]}` | {a['symbol']} | {a['timeframe']} | "
            f"{_fmt_num(a.get('strategy_lockbox_ret'))} | {_fmt_num(a.get('buyhold_lockbox_ret'))} | "
            f"{_fmt_num(a.get('excess_alpha'))} | {_fmt_num(a.get('pf'), 3)} | "
            f"{a.get('trades', '-')} | {_fmt_num(a.get('dsr_p'), 4)} |"
        )
    if not canon_down:
        lines.append("| _(none)_ | | | | | | | | |")

    lines += [
        "",
        "## Promotion Recommendations",
        "",
        "- Maximum level from this automated overnight report: `PROMOTE_TO_FORWARD_PAPER_TRADE` for the best robust down-market alpha cells.",
        "- `APPROVED_FOR_MTC_V2_INTEGRATION`: none.",
        "- No Pine changes, no MTC behavior changes, no parity changes, and no live trading action.",
        "",
        "## Artifact Index",
        "",
        f"- Iteration JSONs: `{args.runs_dir / 'MEGA_results_iter_*.json'}`",
        f"- Aggregate report: `{args.runs_dir / ('AGGREGATE_night_' + args.night_id + '.md')}`",
        f"- Alpha summary: `{args.results_dir / 'alpha_summary.json'}`",
        f"- This report: `{out}`",
        f"- Generated local time: `{datetime.now().isoformat(timespec='seconds')}`",
    ]
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    (args.results_dir / "MORNING_REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"MORNING_REPORT_DONE {out}")


if __name__ == "__main__":
    main()
