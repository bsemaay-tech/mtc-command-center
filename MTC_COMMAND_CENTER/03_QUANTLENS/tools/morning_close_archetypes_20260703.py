#!/usr/bin/env python3
"""Mechanical close for the archetypes overnight run. Defensive; promotes nothing."""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

RUN = Path(r"C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\03_QUANTLENS\05_BACKTEST_RESULTS\overnight_archetypes_2026-07-03")
A = RUN / "archetypes" / "MEGA_walk_forward_results.json"
OUT = RUN / "MORNING_REPORT.md"


def _load(p):
    try:
        return json.loads(Path(p).read_text(encoding="utf-8"))
    except Exception:
        return None


def _cells(d):
    return d["results"] if isinstance(d, dict) and isinstance(d.get("results"), list) else (d if isinstance(d, list) else [])


def _lb(c):
    return ((c.get("summary") or {}).get("lockbox_oos") or {}).get("net_return_pct")


def main():
    ca = _cells(_load(A))
    L = ["# MORNING REPORT — new archetypes 2026-07-03", ""]
    L.append("**Scope (genuinely-new LOGIC):** 12 NEW strategy archetypes using signal sources the "
             "existing non-robust families ignore (volume, session gaps, volatility-regime, true-VWAP, "
             "inside-bar, range-expansion) × multiasset, then deep CPCV + PBO. **Promotes nothing — "
             "robust_final required.**")
    L.append("")
    for k in ("_A", "_B"):
        L.append(f"- Stage {k[1:]}: {'done' if (RUN / (k + '.done')).exists() else 'NOT done'}")
    L.append(f"- ALL_DONE: {'present' if (RUN / '_ALL_DONE.marker').exists() else 'ABSENT'}")
    L.append("")
    if not ca:
        L.append("## Results not available.")
    else:
        L.append(f"## Discovery — 12 archetypes × multiasset")
        L.append(f"- cells: {len(ca)} | archetypes: {len(set(c.get('strategy') for c in ca))} | "
                 f"classes: {dict(Counter(c.get('classification') for c in ca))}")
        L.append(f"- BH-FDR survivors: {sum(1 for c in ca if c.get('bh_fdr_survivor'))} | "
                 f"**robust_final: {sum(1 for c in ca if c.get('robust_final'))}**")
        L.append("")
        # per-archetype robustness roll-up
        L.append("| archetype | cells | PASS+STRONG | bh_surv | robust |")
        L.append("|---|---|---|---|---|")
        for sid in sorted(set(c.get("strategy") for c in ca)):
            s = [c for c in ca if c.get("strategy") == sid]
            ps = sum(1 for c in s if c.get("classification") in ("PASS", "STRONG_PASS"))
            L.append(f"| {sid} | {len(s)} | {ps} | {sum(1 for c in s if c.get('bh_fdr_survivor'))} | "
                     f"{sum(1 for c in s if c.get('robust_final'))} |")
        L.append("")
        top = sorted((c for c in ca if _lb(c) is not None and c.get("classification") in ("PASS", "STRONG_PASS")),
                     key=lambda c: -_lb(c))[:10]
        if top:
            L.append("### Top PASS/STRONG by lockbox return")
            L.append("| archetype | sym | tf | class | lockbox% | dsr | bh | robust |")
            L.append("|---|---|---|---|---|---|---|---|")
            for c in top:
                L.append(f"| {str(c.get('strategy'))[:26]} | {c.get('symbol')} | {c.get('timeframe')} | "
                         f"{c.get('classification')} | {round(_lb(c),1)} | {c.get('dsr_p_value')} | "
                         f"{c.get('bh_fdr_survivor')} | {c.get('robust_final')} |")
    L.append("")
    cj = _load(RUN / "cpcv_archetypes" / "cpcv_results.json")
    n = len(cj.get("results", cj)) if isinstance(cj, (list, dict)) else 0
    L.append(f"## Heavy tier\n- archetypes CPCV: {'present (' + str(n) + ')' if cj else 'n/a'}")
    rob = sum(1 for c in ca if c.get("robust_final"))
    L.append("")
    L.append(f"## Verdict\n- archetype robust_final: **{rob}**. "
             f"{'Nothing promotable — but check the per-archetype roll-up for any cross-symbol cluster worth a confirmation run.' if rob == 0 else 'ROBUST cells found — review for a pre-registered confirmation + human sign-off.'}")
    L.append("- These use NEW signal sources (volume/gaps/regime/VWAP) untested before — a genuinely-new "
             "data point beyond the confirmed-non-robust existing families.")
    L.append("_Mechanical close. Lessons/handoff next session._")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(L), encoding="utf-8")
    print(f"[close] wrote {OUT}")


if __name__ == "__main__":
    main()
