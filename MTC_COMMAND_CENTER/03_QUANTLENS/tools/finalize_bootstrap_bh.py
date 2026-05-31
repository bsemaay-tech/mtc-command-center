"""
Finalize: high-resolution bootstrap on candidates + honest BH-FDR recompute.
============================================================================
The first pass used 2000 bootstrap resamples → p floor = 1/2000 = 0.0005.
With a family of m≈855 cells, the BH threshold for the very best config is
0.10/855 ≈ 0.000117 — UNREACHABLE at 2000 resamples even for a genuine edge.

This is a resolution artifact, not evidence of no-edge. Fix WITHOUT p-hacking:
  - Re-bootstrap every PASS candidate's lockbox with 50,000 resamples to resolve
    its true p-value below the floor.
  - Recompute Benjamini-Hochberg under TWO transparent family definitions:
      m_full = all cells with a valid lockbox bootstrap (honest search space)
      m_pass = only configs that cleared the walk-forward gate (PASS set)
  - Update flags in MEGA_walk_forward_results.json in place.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import mega_walk_forward as M

OUTPUT_DIR = M.OUTPUT_DIR
HIRES_BOOT = 50000

def hires_boot_p(R, seed):
    R = np.asarray(R, dtype=float)
    n = len(R)
    if n < 5:
        return float("nan")
    rng = np.random.default_rng(seed)
    # chunk to bound memory: 50k x n could be large for n~900 → ~45M floats, ok but chunk anyway
    neg = 0
    done = 0
    BATCH = 5000
    while done < HIRES_BOOT:
        b = min(BATCH, HIRES_BOOT - done)
        idx = rng.integers(0, n, size=(b, n))
        means = R[idx].mean(axis=1)
        neg += int((means <= 0).sum())
        done += b
    return neg / HIRES_BOOT

def build_for(strategy, df, params, symbol):
    dmap = None
    if strategy == "QL_2026-05-01_SWING_1H_DUAL_RSI_60_40_PULLBACK":
        maps = M.build_daily_rsi(M._MANIFEST, symbol)
        dmap = maps.get(int(params["rsi_len"])) if maps else None
    return M.build_signals(strategy, df, params, dmap)

def bh_survivors(pvals_idx, m, q=0.10):
    """pvals_idx: list of (key, p). Returns set of keys surviving BH at family size m."""
    ordered = sorted(pvals_idx, key=lambda t: t[1])
    k_max = 0
    for k, (_, p) in enumerate(ordered, start=1):
        if p <= (k / m) * q:
            k_max = k
    return set(key for key, _ in ordered[:k_max]), ((k_max / m) * q if k_max else 0.0)

def main():
    M._MANIFEST = json.load(open(M.BUNDLE_MANIFEST, encoding="utf-8"))
    src = OUTPUT_DIR / "MEGA_walk_forward_results.json"
    data = json.loads(src.read_text(encoding="utf-8"))
    results = data["results"]

    passes = [r for r in results if r.get("classification") in {"PASS","STRONG_PASS"}]
    df_cache = {}
    print(f"Refining {len(passes)} PASS candidates with {HIRES_BOOT} resamples...", flush=True)

    for i, r in enumerate(passes):
        strat, sym, tf = r["strategy"], r["symbol"], r["timeframe"]
        ds = M.find_ds(M._MANIFEST, sym, tf)
        if ds is None:
            continue
        key = (sym, tf)
        if key not in df_cache:
            df_cache[key] = M.load_df(ds["normalized_path"])
        df = df_cache[key].copy()
        sig, stop = build_for(strat, df, r["summary"]["best_params"], sym)
        n = len(df)
        lb_s = n - (n // 4)
        _stats, R = M.simulate_slice(df, sig, stop, strat, lb_s, n, return_trades=True)
        seed = abs(hash((strat, sym, tf, "hires"))) % (2**31)
        p_hi = hires_boot_p(R, seed) if len(R) >= M.MIN_TRADES_FOR_PASS else float("nan")
        r["boot_p_hires"] = round(p_hi, 6) if p_hi == p_hi else None

    # Family p-values: use hires where available, else original boot_p_value
    def eff_p(r):
        if r.get("boot_p_hires") is not None:
            return r["boot_p_hires"]
        return r.get("boot_p_value")

    # m_full family: all cells with valid bootstrap (passes have hires; others original)
    full_family = [(id(r), eff_p(r)) for r in results if eff_p(r) is not None]
    m_full = len(full_family)
    surv_full, thr_full = bh_survivors(full_family, m_full)

    # m_pass family: only PASS configs
    pass_family = [(id(r), eff_p(r)) for r in passes if eff_p(r) is not None]
    m_pass = len(pass_family)
    surv_pass, thr_pass = bh_survivors(pass_family, m_pass)

    for r in results:
        r["bh_survivor_mfull"] = bool(id(r) in surv_full)
        r["bh_survivor_mpass"] = bool(id(r) in surv_pass)
        # primary bh_fdr_survivor = honest full-family
        r["bh_fdr_survivor"] = r["bh_survivor_mfull"]
        cls = r.get("classification")
        r["robust_final"] = bool(cls in {"PASS","STRONG_PASS"}
                                 and r["bh_survivor_mfull"] and r.get("dsr_robust"))

    data["bh_meta"] = {
        "m_full": m_full, "bh_threshold_full": thr_full, "survivors_full": len(surv_full),
        "m_pass": m_pass, "bh_threshold_pass": thr_pass, "survivors_pass": len(surv_pass),
        "hires_resamples": HIRES_BOOT,
    }
    src.write_text(json.dumps(data, indent=2), encoding="utf-8")
    print(f"FINALIZE_DONE m_full={m_full} surv_full={len(surv_full)} (thr={thr_full:.6f}) | "
          f"m_pass={m_pass} surv_pass={len(surv_pass)} (thr={thr_pass:.6f})", flush=True)

if __name__ == "__main__":
    main()
