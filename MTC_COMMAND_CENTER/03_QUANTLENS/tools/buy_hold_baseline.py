"""
buy_hold_baseline.py — Sprint ROBUST winners için buy&hold karşılaştırması.

Sprint JSON'larını okur, her PASS/STRONG_PASS hücresi için:
  - Aynı lockbox döneminde buy&hold return hesaplar
  - Excess return = strategy lockbox return - B&H lockbox return
  - SPRINT_AGGREGATED_REPORT.md'e B&H sütunu ekler

Kullanım:
    python buy_hold_baseline.py [--sprint-dir sprint_runs] [--out sprint_runs/BH_BASELINE.md]
"""
from __future__ import annotations

import argparse
import json
import math
from collections import defaultdict
from pathlib import Path

import numpy as np
import pandas as pd

# ---------------------------------------------------------------------------
# Config — same as mega_walk_forward.py
# ---------------------------------------------------------------------------
BUNDLE_MANIFEST = Path(
    r"C:\LAB\_MTC_V2_REPO_CLEANUP_ARCHIVE_20260529"
    r"\MTC_V2_OPTIMIZATION_DATA_BUNDLE_20260427\manifests\dataset_manifest.json"
)
LOCKBOX_FRACTION = 0.25

# ---------------------------------------------------------------------------
# Data helpers
# ---------------------------------------------------------------------------

def load_manifest() -> dict:
    return json.loads(BUNDLE_MANIFEST.read_text(encoding="utf-8"))


def find_ds(manifest: dict, symbol: str, tf: str) -> dict | None:
    return next(
        (d for d in manifest["datasets"]
         if d["symbol"] == symbol
         and d["timeframe_normalized"] == tf
         and d.get("ohlcv_validation_status") == "PASS"),
        None,
    )


def load_close(ds_path: str) -> pd.Series:
    root = BUNDLE_MANIFEST.parents[1]
    df = pd.read_csv(root / ds_path)
    df["timestamp"] = pd.to_datetime(df["timestamp_utc"], utc=True)
    df = df.sort_values("timestamp").reset_index(drop=True)
    return df["close"]


def bh_lockbox_return(close: pd.Series) -> float:
    """Buy&hold return (%) over the last LOCKBOX_FRACTION of bars."""
    n = len(close)
    lb_start = n - int(n * LOCKBOX_FRACTION)
    lb_start = max(lb_start, 0)
    if lb_start >= n - 1:
        return 0.0
    entry = close.iloc[lb_start]
    exit_ = close.iloc[-1]
    if entry <= 0:
        return 0.0
    return round((exit_ / entry - 1) * 100, 3)


# ---------------------------------------------------------------------------
# Sprint aggregation helpers
# ---------------------------------------------------------------------------

CellKey = tuple[str, str, str]  # (strategy, symbol, tf)


def read_sprint_results(sprint_dir: Path) -> list[dict]:
    jsons = sorted(sprint_dir.glob("MEGA_results_iter_*.json"))
    if not jsons:
        raise FileNotFoundError(f"No MEGA_results_iter_*.json in {sprint_dir}")
    all_results: list[dict] = []
    for jf in jsons:
        data = json.loads(jf.read_text(encoding="utf-8"))
        all_results.extend(data.get("results", []))
    return all_results


def aggregate_pass_cells(results: list[dict]) -> dict[CellKey, dict]:
    """Collect all PASS/STRONG_PASS cells with lockbox return, aggregated across iters."""
    cell_iters: dict[CellKey, list[float]] = defaultdict(list)
    cell_strong: dict[CellKey, int] = defaultdict(int)
    cell_meta: dict[CellKey, dict] = {}

    for r in results:
        clf = r.get("classification", "")
        if clf not in ("PASS", "STRONG_PASS"):
            continue
        key: CellKey = (r["strategy"], r["symbol"], r["timeframe"])
        lb = r.get("summary", {}).get("lockbox_oos", {})
        ret = lb.get("net_return_pct")
        if ret is None:
            continue
        cell_iters[key].append(ret)
        if clf == "STRONG_PASS":
            cell_strong[key] += 1
        if key not in cell_meta:
            cell_meta[key] = {
                "sharpe": lb.get("sharpe"),
                "profit_factor": lb.get("profit_factor"),
                "max_drawdown_pct": lb.get("max_drawdown_pct"),
                "num_trades": lb.get("num_trades"),
                "boot_p": r.get("boot_p_value"),
                "dsr_p": r.get("dsr_p_value"),
            }

    out: dict[CellKey, dict] = {}
    for key, rets in cell_iters.items():
        n_iters = len(rets)
        ret_med = float(np.median(rets))
        ret_std = round(float(np.std(rets)), 3) if len(rets) > 1 else 0.0
        out[key] = {
            "iters_passed": n_iters,
            "strong_pass_count": cell_strong[key],
            "ret_median": ret_med,
            "ret_stdev": ret_std,
            **cell_meta[key],
        }
    return out


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sprint-dir", default="sprint_runs")
    ap.add_argument("--out", default="sprint_runs/BH_BASELINE.md")
    ap.add_argument("--min-iters", type=int, default=2,
                    help="Min iter passes to include in report (default 2 = ROBUST)")
    args = ap.parse_args()

    sprint_dir = Path(args.sprint_dir)
    out_path = Path(args.out)

    print("[B&H] Loading manifest...")
    manifest = load_manifest()

    print("[B&H] Reading sprint results...")
    results = read_sprint_results(sprint_dir)
    print(f"[B&H] {len(results)} total result rows across all iters")

    cells = aggregate_pass_cells(results)
    n_total = len(cells)
    print(f"[B&H] {n_total} distinct PASS/STRONG_PASS cells")

    # Filter ROBUST (pass >= min_iters)
    robust = {k: v for k, v in cells.items() if v["iters_passed"] >= args.min_iters}
    print(f"[B&H] {len(robust)} ROBUST cells (>= {args.min_iters} iter passes)")

    # Compute B&H for each unique (symbol, tf)
    bh_cache: dict[tuple[str, str], float] = {}
    ds_missing: set[tuple[str, str]] = set()

    sym_tf_needed = {(k[1], k[2]) for k in robust}
    for sym, tf in sorted(sym_tf_needed):
        if (sym, tf) in bh_cache or (sym, tf) in ds_missing:
            continue
        ds = find_ds(manifest, sym, tf)
        if ds is None:
            print(f"  [warn] No dataset for {sym}/{tf}")
            ds_missing.add((sym, tf))
            continue
        try:
            close = load_close(ds["normalized_path"])
            bh = bh_lockbox_return(close)
            bh_cache[(sym, tf)] = bh
            print(f"  {sym:12} {tf:4} B&H lockbox: {bh:+.1f}%")
        except Exception as e:
            print(f"  [warn] {sym}/{tf} load error: {e}")
            ds_missing.add((sym, tf))

    # Build report rows
    rows = []
    for key, v in sorted(robust.items(), key=lambda x: -x[1]["ret_median"]):
        strat, sym, tf = key
        bh = bh_cache.get((sym, tf))
        if bh is None:
            excess = None
            alpha_flag = "?"
        else:
            excess = round(v["ret_median"] - bh, 2)
            alpha_flag = "✓" if excess > 0 else "✗"

        rows.append({
            "strategy": strat,
            "symbol": sym,
            "tf": tf,
            "iters": v["iters_passed"],
            "strong": v["strong_pass_count"],
            "ret_med": v["ret_median"],
            "ret_std": v["ret_stdev"],
            "bh_ret": bh,
            "excess": excess,
            "alpha": alpha_flag,
            "sharpe": v["sharpe"],
            "pf": v["profit_factor"],
            "dd": v["max_drawdown_pct"],
            "trades": v["num_trades"],
            "boot_p": v["boot_p"],
            "dsr_p": v["dsr_p"],
        })

    # --- write markdown ---
    n_iters_total = len({jf for jf in sprint_dir.glob("MEGA_results_iter_*.json")})
    lines = [
        "# Buy & Hold Baseline — Sprint ROBUST Winners",
        "",
        f"- Sprint JSON files: {n_iters_total}",
        f"- Total PASS/STRONG_PASS cells: {n_total}",
        f"- ROBUST (>= {args.min_iters} iters): {len(robust)}",
        f"- B&H lockbox fraction: {LOCKBOX_FRACTION} (last {int(LOCKBOX_FRACTION*100)}% of data)",
        "",
        "## Results (sorted by strategy lockbox return descending)",
        "",
        "| Strategy | Sym | TF | Pass×/N | Strong× | Strat ret% | BH ret% | Excess% | α | Sharpe | PF | DD% | Trades | Boot p | DSR p |",
        "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|",
    ]

    for r in rows:
        bh_str = f"{r['bh_ret']:+.1f}" if r["bh_ret"] is not None else "?"
        ex_str = f"{r['excess']:+.1f}" if r["excess"] is not None else "?"
        lines.append(
            f"| `{r['strategy']}` | {r['symbol']} | {r['tf']} "
            f"| **{r['iters']}/{n_iters_total}** | {r['strong']} "
            f"| {r['ret_med']:.1f} | {bh_str} | {ex_str} | {r['alpha']} "
            f"| {r['sharpe'] or '?'} | {r['pf'] or '?'} | {r['dd'] or '?'} "
            f"| {r['trades'] or '?'} | {r['boot_p'] or '?'} | {r['dsr_p'] or '?'} |"
        )

    alpha_yes = sum(1 for r in rows if r["alpha"] == "✓")
    alpha_no  = sum(1 for r in rows if r["alpha"] == "✗")
    alpha_unk = sum(1 for r in rows if r["alpha"] == "?")

    lines += [
        "",
        "## Alpha Summary",
        "",
        f"- Strategies with positive alpha over B&H: **{alpha_yes}** / {len(rows)}",
        f"- Strategies below B&H: {alpha_no}",
        f"- No B&H data available: {alpha_unk}",
        "",
        "## Gate 2 Status",
        "",
        "Gate 2 = alpha over buy&hold. Cells without positive alpha are NOT promotable.",
        "Cells with ✓ still need Gate 3 (DSR) + Gate 4 (multi-window) + Gate 5 (CPCV) + Gate 6 (PBO) to be promotable.",
    ]

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"\n[B&H] Report written -> {out_path}")
    print(f"[B&H] Alpha > 0: {alpha_yes}/{len(rows)} ROBUST cells")


if __name__ == "__main__":
    main()
