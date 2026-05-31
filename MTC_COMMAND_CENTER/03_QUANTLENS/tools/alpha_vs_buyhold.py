"""
Alpha vs Buy & Hold — the decisive null-hypothesis filter.
==========================================================
A long-biased strategy that returns +100% on an asset that itself rose +108%
has NO edge — it merely captured beta (the asset's uptrend). The real question:
does the strategy beat simply holding the asset over the SAME out-of-sample window?

For every PASS candidate we compute:
  - strategy lockbox compound return (already in results)
  - buy&hold compound return of that symbol over the identical lockbox slice
  - EXCESS (alpha) = strategy - buy&hold
The most valuable candidates have POSITIVE excess — especially where buy&hold was
NEGATIVE (strategy made money while the asset fell = genuine, beta-neutral alpha).

Outputs: alpha_summary.json (+ console summary). Consumed by generate_morning_report.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import mega_walk_forward as M

OUTPUT_DIR = M.OUTPUT_DIR

def main():
    M._MANIFEST = json.load(open(M.BUNDLE_MANIFEST, encoding="utf-8"))
    data = json.loads((OUTPUT_DIR / "MEGA_walk_forward_results.json").read_text(encoding="utf-8"))
    results = data["results"]

    # regime-robust set (from multiwindow)
    mw_path = OUTPUT_DIR / "multiwindow_summary.json"
    mw = json.loads(mw_path.read_text(encoding="utf-8")) if mw_path.exists() else []
    regime_keys = {(x["strategy"], x["symbol"], x["timeframe"]): x for x in mw}

    bh_cache = {}
    def buyhold_lockbox(sym, tf):
        key = (sym, tf)
        if key in bh_cache:
            return bh_cache[key]
        ds = M.find_ds(M._MANIFEST, sym, tf)
        if ds is None:
            bh_cache[key] = None; return None
        df = M.load_df(ds["normalized_path"])
        n = len(df); s = n - n // 4
        bh = float((df["close"].iloc[-1] / df["close"].iloc[s] - 1.0) * 100.0)
        bh_cache[key] = bh
        return bh

    passes = [r for r in results if r.get("classification") in {"PASS","STRONG_PASS"}]
    rows = []
    for r in passes:
        sym, tf, strat = r["symbol"], r["timeframe"], r["strategy"]
        lb = r["summary"]["lockbox_oos"]
        bh = buyhold_lockbox(sym, tf)
        if bh is None:
            continue
        strat_ret = lb["net_return_pct"]
        excess = strat_ret - bh
        mwx = regime_keys.get((strat, sym, tf))
        rows.append({
            "strategy": strat, "symbol": sym, "timeframe": tf,
            "params": r["summary"]["best_params"],
            "strategy_lockbox_ret": round(strat_ret, 2),
            "buyhold_lockbox_ret": round(bh, 2),
            "excess_alpha": round(excess, 2),
            "trades": lb["num_trades"], "pf": lb["profit_factor"],
            "maxdd": lb["max_drawdown_pct"], "sharpe": lb["sharpe"],
            "boot_p_hires": r.get("boot_p_hires", r.get("boot_p_value")),
            "dsr_p": r.get("dsr_p_value"),
            "bh_survivor_mpass": r.get("bh_survivor_mpass", False),
            "bh_survivor_mfull": r.get("bh_survivor_mfull", False),
            "regime_robust": bool(mwx and mwx.get("windows_positive", 0) >= 3),
            "param_stable": bool(mwx and mwx.get("param_stable")),
            "windows_positive": (mwx.get("windows_positive") if mwx else None),
            # genuine alpha = beat buy&hold AND made money while asset fell, OR strong outperformance
            "beat_buyhold": bool(excess > 0),
            "alpha_in_down_market": bool(excess > 0 and bh < 0 and strat_ret > 0),
        })

    rows.sort(key=lambda x: x["excess_alpha"], reverse=True)

    # The premium tier: positive strategy return, beats buy&hold, regime-robust + param-stable
    premium = [x for x in rows
               if x["strategy_lockbox_ret"] > 0 and x["beat_buyhold"]
               and x["regime_robust"] and x["param_stable"]]
    # Genuine alpha in DOWN markets (most valuable - true edge)
    down_alpha = [x for x in rows if x["alpha_in_down_market"] and x["regime_robust"] and x["param_stable"]]
    down_alpha.sort(key=lambda x: x["excess_alpha"], reverse=True)

    (OUTPUT_DIR / "alpha_summary.json").write_text(json.dumps({
        "all_ranked_by_excess": rows,
        "premium": premium,
        "down_market_alpha": down_alpha,
    }, indent=2), encoding="utf-8")

    print(f"ALPHA_DONE passes={len(rows)} beat_buyhold={sum(1 for x in rows if x['beat_buyhold'])} "
          f"premium={len(premium)} down_market_alpha={len(down_alpha)}")
    print("Top 12 by excess alpha (strategy - buyhold), regime-robust+stable only:")
    for x in [r for r in rows if r['regime_robust'] and r['param_stable']][:12]:
        print(f"  {x['strategy'][:30]:30} {x['symbol']:8} {x['timeframe']:3} "
              f"strat={x['strategy_lockbox_ret']:+7.1f}% b&h={x['buyhold_lockbox_ret']:+7.1f}% "
              f"alpha={x['excess_alpha']:+7.1f}% PF={x['pf']} trades={x['trades']}")

if __name__ == "__main__":
    main()
