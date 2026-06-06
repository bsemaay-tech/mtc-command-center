"""Honest heavy-validation-tier morning report.

Reads the heavy_tier run dir artifacts and writes a markdown summary with
HONEST counts only. No promotion claims, no inflation, no Pine/MTC/parity/live
action. Determinism caveat is stated explicitly.
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import re
import sys
from datetime import datetime, timezone

sys.stdout.reconfigure(encoding="utf-8")  # A11


def _load(path):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-dir", required=True)
    ap.add_argument("--night-id", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args(argv)
    rd = a.run_dir

    L = []
    L.append(f"# Heavy-Validation Tier — Morning Report ({a.night_id})")
    L.append("")
    L.append(f"_Generated {datetime.now(timezone.utc).isoformat()}._")
    L.append("")
    L.append("> **Honesty note.** The backtest engine is deterministic "
             "(seed = md5(strategy|symbol|tf), `mega_walk_forward.py:1130`). "
             "Repeating an identical sweep N times yields identical results — "
             "the old 'N iters = 3.6M evals' accounting is statistically empty "
             "(runbook A19 / lessons C4-C5). This night therefore did NOT "
             "loop-pad. It ran genuinely-new work: the **first full "
             "43-strategy sweep under today's enriched engine** (today only 20 "
             "strategies were swept enriched) plus a **3×-deeper CPCV** "
             "(45 splits vs the committed 15) + uncapped PBO + full gate "
             "scorecards. No Pine / MTC / parity / live-trading action is "
             "authorized by any number below.")
    L.append("")

    # ---- sweep -----------------------------------------------------------
    mega = _load(os.path.join(rd, "MEGA_walk_forward_results.json"))
    L.append("## 1. Sweep (43-strategy, enriched engine)")
    if mega:
        rows = mega.get("results", [])
        cls = {}
        robust = 0
        dsr_ge_50 = 0
        for r in rows:
            c = r.get("classification", "?")
            cls[c] = cls.get(c, 0) + 1
            if r.get("robust_final"):
                robust += 1
            dp = r.get("dsr_p_value")
            if isinstance(dp, (int, float)) and dp >= 0.50:
                dsr_ge_50 += 1
        cfg = mega.get("config", {})
        L.append(f"- runtime: {mega.get('runtime_seconds')}s | workers: {mega.get('workers')}")
        L.append(f"- cells: **{len(rows)}** | strategies: {cfg.get('strategy_count')} "
                 f"| symbols: {len(cfg.get('selected_symbols', []))} "
                 f"| TFs: {cfg.get('selected_timeframes')}")
        L.append(f"- classification: " + ", ".join(f"{k}={v}" for k, v in sorted(cls.items())))
        L.append(f"- robust_final: **{robust}** | DSR p≥0.50: **{dsr_ge_50}**")
        passcells = [r for r in rows if r.get("classification") in ("PASS", "STRONG_PASS")]
    else:
        L.append("- MEGA results: **MISSING**")
        passcells = []
    L.append("")

    # ---- honest evaluation accounting -----------------------------------
    sweep_log = os.path.join(rd, "sweep.log")
    cfg_evals = None
    if os.path.exists(sweep_log):
        try:
            txt = open(sweep_log, encoding="utf-8", errors="ignore").read()
            m = re.findall(r"configs evaluated ~(\d+)", txt)
            if m:
                cfg_evals = int(m[-1])
        except Exception:
            pass

    # ---- CPCV deep -------------------------------------------------------
    cpcv = _load(os.path.join(rd, "cpcv", "cpcv_results.json"))
    L.append("## 2. Deeper CPCV (n_groups=10 → 45 splits/cell)")
    cpcv_rows = []
    cpcv_split_total = 0
    if cpcv:
        cpcv_rows = cpcv.get("results", [])
        for r in cpcv_rows:
            cpcv_split_total += int(r.get("splits", 0) or 0)
        surv70 = [r for r in cpcv_rows if (r.get("pass_rate") or 0) >= 0.70]
        surv80 = [r for r in cpcv_rows if (r.get("pass_rate") or 0) >= 0.80]
        L.append(f"- cells evaluated: **{len(cpcv_rows)}** | total splits: **{cpcv_split_total}**")
        L.append(f"- pass_rate ≥0.70: **{len(surv70)}** | ≥0.80: **{len(surv80)}**")
        L.append("")
        top = sorted(cpcv_rows, key=lambda r: r.get("pass_rate") or 0, reverse=True)[:12]
        L.append("| Strategy | Sym | TF | Pass | Rate | Med Ret% | Min Ret% |")
        L.append("|---|---|---|---|---|---|---|")
        for r in top:
            L.append(f"| `{str(r.get('strategy',''))[:42]}` | {r.get('symbol')} | "
                     f"{r.get('timeframe')} | {r.get('pass_count')}/{r.get('splits')} | "
                     f"{r.get('pass_rate')} | {r.get('return_median_pct')} | {r.get('return_min_pct')} |")
    else:
        L.append("- CPCV results: **MISSING**")
    L.append("")

    # ---- PBO -------------------------------------------------------------
    pbo = _load(os.path.join(rd, "pbo", "pbo_results.json"))
    L.append("## 3. PBO (uncapped)")
    if pbo:
        val = pbo.get("pbo", pbo.get("pbo_value"))
        L.append(f"- PBO: **{val}** | CSCV combinations: {pbo.get('cscv_combinations')} "
                 f"| splits: {pbo.get('split_count')} | candidates: {pbo.get('candidate_count')}")
    else:
        L.append("- PBO results: **MISSING**")
    L.append("")

    # ---- Gate2 -----------------------------------------------------------
    g2 = glob.glob(os.path.join(rd, "gate2_scorecards", "*.json"))
    L.append("## 4. Gate-2 scorecards")
    if g2:
        npass = nfail = ninc = 0
        scores = []
        for p in g2:
            s = _load(p) or {}
            gg = s.get("gate2", {})
            st = gg.get("status")
            if gg.get("pass"):
                npass += 1
            elif st == "INCOMPLETE":
                ninc += 1
            else:
                nfail += 1
            sc = gg.get("score")
            if isinstance(sc, (int, float)):
                scores.append((sc, s.get("strategy_id", os.path.basename(p))))
        L.append(f"- total: {len(g2)} | **PASS={npass}** | FAIL={nfail} | INCOMPLETE={ninc}")
        if scores:
            scores.sort(reverse=True)
            L.append("- top scores: " + "; ".join(f"{sc:.1f} {sid[:46]}" for sc, sid in scores[:5]))
    else:
        L.append("- Gate-2 scorecards: **MISSING**")
    L.append("")

    # ---- all-gate / promotable ------------------------------------------
    v2 = glob.glob(os.path.join(rd, "scorecard_v2", "*.json"))
    if not v2:
        v2 = [p for p in glob.glob(os.path.join(rd, "all_gate", "**", "*.json"), recursive=True)
              if "scorecard" in os.path.basename(p).lower()]
    L.append("## 5. All-gate (scorecard_v2)")
    if v2:
        promo = 0
        blocking = {}
        for p in v2:
            s = _load(p) or {}
            gs = s.get("gate_summary", {})
            if gs.get("promotable"):
                promo += 1
            for b in gs.get("blocking", []):
                blocking[b] = blocking.get(b, 0) + 1
        L.append(f"- scorecards: {len(v2)} | **promotable: {promo}**")
        if blocking:
            L.append(f"- blocking gates: " + ", ".join(f"{k}={v}" for k, v in sorted(blocking.items())))
        L.append("- (Gate-3 production-readiness is the standing real blocker; "
                 "not fabricated — needs alert/adapter/state-sync/fail-safe evidence.)")
    else:
        L.append("- scorecard_v2: **MISSING**")
    L.append("")

    # ---- alpha -----------------------------------------------------------
    alpha = _load(os.path.join(rd, "alpha_summary.json"))
    L.append("## 6. Alpha vs Buy&Hold (lockbox window)")
    if alpha:
        prem = alpha.get("premium", [])
        dma = alpha.get("down_market_alpha", [])
        ranked = alpha.get("all_ranked_by_excess", [])
        L.append(f"- premium (beats B&H risk-adjusted): **{len(prem)}** | "
                 f"down-market alpha: **{len(dma)}** | ranked cells: {len(ranked)}")
        if ranked:
            L.append("")
            L.append("| Strategy | Sym | TF | Strat% | B&H% | Excess% | DSR p | DownMkt |")
            L.append("|---|---|---|---|---|---|---|---|")
            for r in ranked[:12]:
                L.append(f"| `{str(r.get('strategy',''))[:40]}` | {r.get('symbol')} | "
                         f"{r.get('timeframe')} | {r.get('strategy_lockbox_ret')} | "
                         f"{r.get('buyhold_lockbox_ret')} | {r.get('excess_alpha')} | "
                         f"{r.get('dsr_p')} | {r.get('alpha_in_down_market')} |")
    else:
        L.append("- alpha_summary: **MISSING**")
    L.append("")

    # ---- honest tally ----------------------------------------------------
    L.append("## 7. Honest evaluation tally")
    L.append(f"- sweep param-config evaluations (approx, from sweep log): "
             f"**{cfg_evals if cfg_evals is not None else 'n/a'}** × 6 folds")
    if cfg_evals:
        L.append(f"  → ≈ **{cfg_evals * 6:,}** slice-evaluations (single deterministic pass)")
    L.append(f"- CPCV deep splits computed: **{cpcv_split_total}** "
             f"(× per-split grid re-selection)")
    L.append("- These are **distinct** evaluations. No repeat-padding was done. "
             "Reaching a literal 3,000,000 *distinct* configs would require widening "
             "the param grids — which harms DSR power (A17) and needs design + Barış "
             "approval, so it was deliberately NOT done autonomously.")
    L.append("")
    L.append("_End of report._")

    with open(a.out, "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")
    print(f"wrote {a.out} ({len(L)} lines)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
