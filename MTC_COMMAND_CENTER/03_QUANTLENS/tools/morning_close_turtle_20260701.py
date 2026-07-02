#!/usr/bin/env python3
"""
morning_close_turtle_20260701.py

Mechanical morning close for the 2026-07-01 turtle_heavy overnight run. Reads the
persisted artifacts and writes MORNING_REPORT.md. Defensive: never crashes; any
missing artifact becomes a "not available" line. Judgment-heavy lessons write-back
and handoff updates are done by the operator/agent afterwards.

Promotes NOTHING (robust_final still required). No backtest is run here.
"""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

RESULTS = Path(r"C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\03_QUANTLENS\05_BACKTEST_RESULTS")
HEAVY = RESULTS / "turtle_heavy_2026-07-01"
TURTLE_JSON = HEAVY / "turtle_sweep" / "MEGA_walk_forward_results.json"
BASE_JSON = RESULTS / "overnight_multiasset_2026-06-29" / "MEGA_walk_forward_results.json"
OUT = HEAVY / "MORNING_REPORT.md"


def _load(p: Path):
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return None


def _cells(d):
    if isinstance(d, dict) and isinstance(d.get("results"), list):
        return d["results"]
    return d if isinstance(d, list) else []


def _lb_ret(c):
    return ((c.get("summary") or {}).get("lockbox_oos") or {}).get("net_return_pct")


def main():
    lines = []
    lines.append("# MORNING REPORT — turtle_heavy 2026-07-01")
    lines.append("")
    lines.append("**Scope:** genuinely-new overnight compute (A22): Faz-3 variant `GEN_DONCHIAN_TURTLE` "
                 "full-universe validation + heavy-validation tier (deep CPCV + PBO) on the 2026-06-29 "
                 "base survivors and the TURTLE survivors. NO deterministic re-run of the base sweep. "
                 "**Promotes nothing — robust_final required.**")
    lines.append("")

    # --- Stage markers ---
    lines.append("## Run status")
    for i in range(1, 6):
        m = HEAVY / f"_stage{i}.done"
        lines.append(f"- Stage {i}: {'done' if m.exists() else 'NOT done'}")
    lines.append(f"- ALL_DONE marker: {'present' if (HEAVY / '_ALL_DONE.marker').exists() else 'ABSENT'}")
    lines.append("")

    # --- TURTLE discovery ---
    td = _load(TURTLE_JSON)
    tc = _cells(td)
    lines.append("## Stage 1 — GEN_DONCHIAN_TURTLE full-universe (NEW)")
    if tc:
        cls = dict(Counter(c.get("classification") for c in tc))
        surv = [c for c in tc if c.get("bh_fdr_survivor")]
        robust = [c for c in tc if c.get("robust_final")]
        lines.append(f"- cells: {len(tc)} | classifications: {cls}")
        lines.append(f"- BH-FDR survivors: {len(surv)} | dsr_robust: {sum(1 for c in tc if c.get('dsr_robust'))} | "
                     f"**robust_final: {len(robust)}**")
        top = sorted((c for c in tc if _lb_ret(c) is not None), key=lambda c: -_lb_ret(c))[:8]
        if top:
            lines.append("")
            lines.append("| symbol | tf | class | lockbox ret% | bh_surv | dsr |")
            lines.append("|---|---|---|---|---|---|")
            for c in top:
                lines.append(f"| {c.get('symbol')} | {c.get('timeframe')} | {c.get('classification')} | "
                             f"{round(_lb_ret(c), 1)} | {c.get('bh_fdr_survivor')} | {c.get('dsr_p_value')} |")
    else:
        lines.append("- TURTLE results not available.")
    lines.append("")

    # --- Base vs Turtle (did the structural stop help?) ---
    lines.append("## Turtle STRUCTURAL stop vs base GEN_DONCHIAN_BREAKOUT (same cells)")
    bd = _cells(_load(BASE_JSON))
    if tc and bd:
        base_don = {(c.get("symbol"), c.get("timeframe")): _lb_ret(c)
                    for c in bd if c.get("strategy") == "GEN_DONCHIAN_BREAKOUT"}
        rows = []
        for c in tc:
            k = (c.get("symbol"), c.get("timeframe"))
            br, tr = base_don.get(k), _lb_ret(c)
            if br is not None and tr is not None:
                rows.append((k, br, tr, tr - br))
        if rows:
            better = sum(1 for _, br, tr, d in rows if d > 0)
            lines.append(f"- comparable cells: {len(rows)} | TURTLE better than base: {better} "
                         f"({round(100 * better / len(rows))}%)")
            rows.sort(key=lambda r: -r[3])
            lines.append("")
            lines.append("| symbol | tf | base ret% | turtle ret% | delta |")
            lines.append("|---|---|---|---|---|")
            for (sym, tf), br, tr, d in rows[:8]:
                lines.append(f"| {sym} | {tf} | {round(br, 1)} | {round(tr, 1)} | {round(d, 1)} |")
        else:
            lines.append("- no overlapping cells with lockbox returns.")
    else:
        lines.append("- base or turtle results not available for comparison.")
    lines.append("")

    # --- Heavy tier (CPCV / PBO) ---
    lines.append("## Heavy-validation tier (deep CPCV + PBO)")
    for label, cpath, ppath in [
        ("06-29 base survivors", HEAVY / "cpcv_base" / "cpcv_results.json", HEAVY / "pbo_base" / "pbo_results.json"),
        ("TURTLE survivors", HEAVY / "cpcv_turtle" / "cpcv_results.json", HEAVY / "pbo_turtle" / "pbo_results.json"),
    ]:
        cj = _load(cpath)
        pj = _load(ppath)
        n = len(cj.get("results", cj)) if isinstance(cj, (list, dict)) else 0
        lines.append(f"- **{label}**: CPCV {'present (' + str(n) + ' entries)' if cj else 'not available'}; "
                     f"PBO {'present' if pj else 'not available'}")
    lines.append("")

    lines.append("## Verdict")
    robust_n = len([c for c in tc if c.get("robust_final")]) if tc else 0
    lines.append(f"- TURTLE variant robust_final cells: **{robust_n}**. "
                 f"{'Nothing promotable.' if robust_n == 0 else 'Review before any promotion — robust_final still needs cross-symbol + human sign-off.'}")
    lines.append("- Consistent with the library-wide finding (no robust edge) unless the table above shows a "
                 "cross-symbol robust cluster. This is a first honest data point on the Turtle structural stop.")
    lines.append("- A22: machine released on completion (not idled to 08:30). See orchestrator log.")
    lines.append("")
    lines.append("_Mechanical close. Lessons write-back + handoff done by the operator/agent next session._")

    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"[close] wrote {OUT}")


if __name__ == "__main__":
    main()
