"""
Multi-Window OOS + Parameter-Neighborhood Robustness
=====================================================
Second-pass validation that consumes MEGA_walk_forward_results.json and, for the
strongest candidates, answers two questions the single-lockbox WF cannot:

  1. REGIME ROBUSTNESS — does the SAME fixed best-params survive when the OOS
     window is placed at DIFFERENT points in history? We slice the series into
     4 quartiles (Q1..Q4) and the 2nd-half, score each independently. A real edge
     should be positive across most placements, not only the terminal slice.

  2. PARAMETER STABILITY — perturb each numeric param by +/-1 grid-ish step and
     re-score the terminal lockbox. A real edge has a smooth neighborhood; a spiky
     single-point peak is overfitting.

Outputs: MULTIWINDOW_OOS_REPORT.md
"""
from __future__ import annotations

import json
import math
import copy
from pathlib import Path

import numpy as np
import pandas as pd

import mega_walk_forward as M  # reuse data loaders, signals, simulate_slice

OUTPUT_DIR = M.OUTPUT_DIR
MIN_TR = 15  # lighter min-trades for sub-windows (they're ~1/4 the data)

def load_results():
    src = OUTPUT_DIR / "MEGA_walk_forward_results.json"
    data = json.loads(src.read_text(encoding="utf-8"))
    return data["results"], data

def candidate_set(results):
    """All PASS/STRONG with a half-decent bootstrap p-value, capped."""
    passes = [r for r in results if r.get("classification") in {"PASS","STRONG_PASS"}]
    # prioritise bootstrap-FDR survivors + lowest boot_p
    passes.sort(key=lambda r: (not r.get("bh_fdr_survivor"),
                               r.get("boot_p_value", 1.0) if r.get("boot_p_value") is not None else 1.0))
    # keep up to 80
    return passes[:80]

def windows(n):
    """Return named (start,end) index slices for placement tests."""
    q = n // 4
    return {
        "Q1_0-25":   (0, q),
        "Q2_25-50":  (q, 2*q),
        "Q3_50-75":  (2*q, 3*q),
        "Q4_75-100": (3*q, n),       # == terminal lockbox
        "H2_50-100": (2*q, n),
    }

def score_window(df, sig, stop, strategy, s, e, seed):
    stats, R = M.simulate_slice(df, sig, stop, strategy, s, e, return_trades=True)
    bp = M.bootstrap_p_positive(R, 1500, seed) if len(R) >= MIN_TR else float("nan")
    return {
        "ret": stats.net_return_pct, "trades": stats.num_trades,
        "sharpe": stats.sharpe, "pf": stats.profit_factor,
        "maxdd": stats.max_drawdown_pct,
        "boot_p": round(bp, 4) if bp == bp else None,
    }

def perturb_params(strategy, params):
    """Yield a few neighbor param dicts by scaling numeric values."""
    neigh = []
    keys = [k for k, v in params.items() if isinstance(v, (int, float))]
    for k in keys:
        for factor in (0.8, 1.25):
            p2 = copy.deepcopy(params)
            v = params[k]
            if isinstance(v, int):
                nv = max(1, int(round(v * factor)))
                if nv == v:
                    nv = v + (1 if factor > 1 else -1)
                    nv = max(1, nv)
                p2[k] = nv
            else:
                p2[k] = round(v * factor, 4)
            neigh.append((k, factor, p2))
    return neigh

def build_for(strategy, df, params, symbol):
    dmap = None
    if strategy == "QL_2026-05-01_SWING_1H_DUAL_RSI_60_40_PULLBACK":
        maps = M.build_daily_rsi(M._MANIFEST, symbol)
        dmap = maps.get(int(params["rsi_len"])) if maps else None
    return M.build_signals(strategy, df, params, dmap)

def main():
    M._MANIFEST = json.load(open(M.BUNDLE_MANIFEST, encoding="utf-8"))
    results, _ = load_results()
    cands = candidate_set(results)

    md = ["# Multi-Window OOS + Parameter-Stability Report", "",
          f"- Candidates analysed: {len(cands)} (top PASS by bootstrap-FDR / boot_p)",
          "- Windows: Q1(0-25%) Q2(25-50%) Q3(50-75%) Q4(75-100%=lockbox) H2(50-100%)",
          "- A config is **REGIME-ROBUST** if positive return in >=3 of 5 windows with >=15 trades each.",
          "- A config is **PARAM-STABLE** if >=70% of +/-step neighbors keep positive lockbox return.",
          "", "## Per-Candidate Robustness", "",
          "| Strategy | Sym | TF | Params | Q1 | Q2 | Q3 | Q4 | H2 | Win+/5 | Regime? | Param-Stable? |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|"]

    regime_robust = []
    df_cache = {}

    for r in cands:
        strat = r["strategy"]; sym = r["symbol"]; tf = r["timeframe"]
        params = r["summary"]["best_params"]
        ds = M.find_ds(M._MANIFEST, sym, tf)
        if ds is None:
            continue
        key = (sym, tf)
        if key not in df_cache:
            df_cache[key] = M.load_df(ds["normalized_path"])
        df = df_cache[key].copy()
        sig, stop = build_for(strat, df, params, sym)
        n = len(df)
        wins = windows(n)
        seed = abs(hash((strat, sym, tf))) % (2**31)
        wres = {name: score_window(df, sig, stop, strat, s, e, seed + i)
                for i, (name, (s, e)) in enumerate(wins.items())}
        pos = sum(1 for w in ["Q1_0-25","Q2_25-50","Q3_50-75","Q4_75-100","H2_50-100"]
                  if wres[w]["trades"] >= MIN_TR and wres[w]["ret"] > 0)
        regime = pos >= 3

        # neighborhood stability on terminal lockbox
        lb_s = n - (n // 4)
        neigh = perturb_params(strat, params)
        stable_pos = 0; stable_tot = 0
        for k, fac, p2 in neigh:
            sig2, stop2 = build_for(strat, df, p2, sym)
            st2 = M.simulate_slice(df, sig2, stop2, strat, lb_s, n)
            if st2.num_trades >= MIN_TR:
                stable_tot += 1
                if st2.net_return_pct > 0:
                    stable_pos += 1
        param_stable = (stable_tot > 0 and stable_pos / stable_tot >= 0.70)

        if regime:
            regime_robust.append((r, wres, pos, param_stable))

        def cell(w):
            x = wres[w]
            return f"{x['ret']:.0f}%/{x['trades']}t"
        md.append(
            f"| `{strat[:32]}` | {sym} | {tf} | "
            f"`{json.dumps(params, separators=(',',':'))[:50]}` | "
            f"{cell('Q1_0-25')} | {cell('Q2_25-50')} | {cell('Q3_50-75')} | "
            f"{cell('Q4_75-100')} | {cell('H2_50-100')} | {pos}/5 | "
            f"{'YES' if regime else 'no'} | {'YES' if param_stable else 'no'} "
            f"({stable_pos}/{stable_tot}) |"
        )

    # summary of best
    md += ["", "## REGIME-ROBUST + PARAM-STABLE (cross-window survivors)", ""]
    rr = [(r, wres, pos, ps) for (r, wres, pos, ps) in regime_robust if ps]
    rr.sort(key=lambda t: t[2], reverse=True)
    if rr:
        md += ["| Strategy | Sym | TF | Win+/5 | Lockbox Ret% | Boot p | DSR p | BH? | Final? |",
               "|---|---|---|---|---|---|---|---|---|"]
        for (r, wres, pos, ps) in rr:
            lb = r["summary"]["lockbox_oos"]
            md.append(
                f"| `{r['strategy'][:32]}` | {r['symbol']} | {r['timeframe']} | {pos}/5 | "
                f"{lb['net_return_pct']:.2f} | {r.get('boot_p_value')} | {r.get('dsr_p_value')} | "
                f"{'Y' if r.get('bh_fdr_survivor') else 'n'} | {'Y' if r.get('robust_final') else 'n'} |"
            )
    else:
        md.append("_(No candidate is both regime-robust across windows AND parameter-stable.)_")
    md.append("")

    (OUTPUT_DIR / "MULTIWINDOW_OOS_REPORT.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    # tiny JSON for morning report consumption
    summary = []
    for (r, wres, pos, ps) in regime_robust:
        lb = r["summary"]["lockbox_oos"]
        summary.append({
            "strategy": r["strategy"], "symbol": r["symbol"], "timeframe": r["timeframe"],
            "params": r["summary"]["best_params"],
            "windows_positive": pos, "param_stable": ps,
            "lockbox_ret": lb["net_return_pct"], "lockbox_pf": lb["profit_factor"],
            "boot_p": r.get("boot_p_value"), "dsr_p": r.get("dsr_p_value"),
            "bh_survivor": r.get("bh_fdr_survivor"), "robust_final": r.get("robust_final"),
            "window_returns": {k: wres[k]["ret"] for k in wres},
        })
    (OUTPUT_DIR / "multiwindow_summary.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8")
    print(f"MULTIWINDOW_DONE candidates={len(cands)} regime_robust={len(regime_robust)} regime_and_stable={len(rr)}")

if __name__ == "__main__":
    main()
