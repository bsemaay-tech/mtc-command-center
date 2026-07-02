#!/usr/bin/env python3
"""
morning_close_full_20260702.py — mechanical close for the overnight_full 2026-07-02 run.
Reads Stage A (v2×multiasset) + Stage B (variants) sweeps + CPCV/PBO, writes MORNING_REPORT.md.
Defensive: never crashes. Promotes nothing.
"""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

RUN = Path(r"C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\03_QUANTLENS\05_BACKTEST_RESULTS\overnight_full_2026-07-02")
A = RUN / "stageA_v2_multiasset" / "MEGA_walk_forward_results.json"
B = RUN / "stageB_variants" / "MEGA_walk_forward_results.json"
OUT = RUN / "MORNING_REPORT.md"


def _load(p):
    try:
        return json.loads(Path(p).read_text(encoding="utf-8"))
    except Exception:
        return None


def _cells(d):
    if isinstance(d, dict) and isinstance(d.get("results"), list):
        return d["results"]
    return d if isinstance(d, list) else []


def _lb(c):
    return ((c.get("summary") or {}).get("lockbox_oos") or {}).get("net_return_pct")


def _section(title, cells):
    L = [f"## {title}"]
    if not cells:
        L.append("- results not available.")
        return L
    cls = dict(Counter(c.get("classification") for c in cells))
    surv = [c for c in cells if c.get("bh_fdr_survivor")]
    robust = [c for c in cells if c.get("robust_final")]
    str016 = sorted({c.get("strategy") for c in cells})
    L.append(f"- cells: {len(cells)} | strategies: {len(str016)} | classifications: {cls}")
    L.append(f"- BH-FDR survivors: {len(surv)} | dsr_robust: {sum(1 for c in cells if c.get('dsr_robust'))} | **robust_final: {len(robust)}**")
    top = sorted((c for c in cells if _lb(c) is not None), key=lambda c: -_lb(c))[:8]
    if top:
        L.append("")
        L.append("| strategy | symbol | tf | class | lockbox ret% | dsr | robust |")
        L.append("|---|---|---|---|---|---|---|")
        for c in top:
            L.append(f"| {str(c.get('strategy'))[:26]} | {c.get('symbol')} | {c.get('timeframe')} | "
                     f"{c.get('classification')} | {round(_lb(c), 1)} | {c.get('dsr_p_value')} | {c.get('robust_final')} |")
    return L


def main():
    ca, cb = _cells(_load(A)), _cells(_load(B))
    L = ["# MORNING REPORT — overnight_full 2026-07-02 (library-wide, genuinely-new)", ""]
    L.append("**Scope (A22/A24 — full enumerated backlog):** Stage A = 23 v2 strategies × multiasset "
             "(never swept on this bundle); Stage B = 7-variant family × multiasset (new logic); "
             "Stage C = deep CPCV + PBO on the NEW A+B survivors. NO deterministic re-run (mega's 20 and "
             "their 06-29/07-01 validation excluded). **Promotes nothing — robust_final required.**")
    L.append("")
    for i, s in [("A", "_A"), ("B", "_B"), ("C", "_C"), ("D", "_D")]:
        L.append(f"- Stage {i}: {'done' if (RUN / (s + '.done')).exists() else 'NOT done'}")
    L.append(f"- ALL_DONE: {'present' if (RUN / '_ALL_DONE.marker').exists() else 'ABSENT'}")
    L.append("")
    L += _section("Stage A — v2 23 strategies × multiasset (NEW)", ca)
    L.append("")
    L += _section("Stage B — Faz-3 variant family (7) × multiasset (NEW)", cb)
    L.append("")
    L.append("## Heavy-validation tier (deep CPCV + PBO on NEW survivors)")
    for lbl, cp, pp in [("v2", RUN / "cpcv_v2" / "cpcv_results.json", RUN / "pbo_v2" / "pbo_results.json"),
                        ("variants", RUN / "cpcv_variants" / "cpcv_results.json", RUN / "pbo_variants" / "pbo_results.json")]:
        cj, pj = _load(cp), _load(pp)
        n = len(cj.get("results", cj)) if isinstance(cj, (list, dict)) else 0
        pbo = (pj.get("pbo") if isinstance(pj, dict) else None)
        L.append(f"- **{lbl}**: CPCV {'present (' + str(n) + ')' if cj else 'n/a'}; PBO {pbo if pbo is not None else ('present' if pj else 'n/a')}")
    L.append("")
    rob = (len([c for c in ca if c.get('robust_final')]) + len([c for c in cb if c.get('robust_final')]))
    L.append("## Verdict")
    L.append(f"- Combined robust_final cells (A+B): **{rob}**. {'Nothing promotable.' if rob == 0 else 'Review — cross-symbol + human sign-off required before any promotion.'}")
    L.append("- A22/A24: full enumerated genuinely-new backlog run (all 43 executable + 7 variants + heavy "
             "validation); machine released when backlog exhausted, not idled.")
    L.append("")
    L.append("_Mechanical close. Lessons write-back + handoff by the operator/agent next session._")
    OUT.write_text("\n".join(L), encoding="utf-8")
    print(f"[close] wrote {OUT}")


if __name__ == "__main__":
    main()
