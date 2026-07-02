#!/usr/bin/env python3
"""Mechanical close for the resilient 2026-07-02 21:00 run. Defensive; promotes nothing."""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

RES = Path(r"C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\03_QUANTLENS\05_BACKTEST_RESULTS")
RUN = RES / "overnight_resilient_2026-07-02"
VAR = RUN / "variants" / "MEGA_walk_forward_results.json"
V2 = RES / "overnight_full_2026-07-02" / "stageA_v2_multiasset" / "MEGA_walk_forward_results.json"
OUT = RUN / "MORNING_REPORT.md"
STG = ("GEN_TWOCANDLE_CONFIRM", "GEN_EMA_PULLBACK_TUNED")


def _load(p):
    try:
        return json.loads(Path(p).read_text(encoding="utf-8"))
    except Exception:
        return None


def _cells(d):
    return d["results"] if isinstance(d, dict) and isinstance(d.get("results"), list) else (d if isinstance(d, list) else [])


def _lb(c):
    return ((c.get("summary") or {}).get("lockbox_oos") or {}).get("net_return_pct")


def _sec(title, cells):
    L = [f"## {title}"]
    if not cells:
        L.append("- not available.")
        return L
    L.append(f"- cells: {len(cells)} | strategies: {len(set(c.get('strategy') for c in cells))} | "
             f"classes: {dict(Counter(c.get('classification') for c in cells))}")
    L.append(f"- BH-FDR survivors: {sum(1 for c in cells if c.get('bh_fdr_survivor'))} | "
             f"**robust_final: {sum(1 for c in cells if c.get('robust_final'))}**")
    top = sorted((c for c in cells if _lb(c) is not None), key=lambda c: -_lb(c))[:8]
    if top:
        L.append("")
        L.append("| strategy | sym | tf | class | lockbox% | dsr | robust |")
        L.append("|---|---|---|---|---|---|---|")
        for c in top:
            L.append(f"| {str(c.get('strategy'))[:24]} | {c.get('symbol')} | {c.get('timeframe')} | "
                     f"{c.get('classification')} | {round(_lb(c),1)} | {c.get('dsr_p_value')} | {c.get('robust_final')} |")
    return L


def main():
    cv, c2 = _cells(_load(VAR)), _cells(_load(V2))
    stg = [c for c in cv if c.get("strategy") in STG]
    L = ["# MORNING REPORT — resilient 2026-07-02 21:00 -> 08:30", ""]
    L.append("**Scope (A22/A24, genuinely-new):** STG001/STG002 confirmation first, then the 8-variant "
             "family + the finished v2 23-strategy sweep + deep CPCV/PBO. Crash-resilient (per-stage retry "
             "+ external /loop relaunch). **Promotes nothing — robust_final required.**")
    L.append("")
    for k in ("_P", "_1", "_2", "_3"):
        L.append(f"- Stage {k[1:]}: {'done' if (RUN / (k + '.done')).exists() else 'NOT done'}")
    L.append(f"- ALL_DONE: {'present' if (RUN / '_ALL_DONE.marker').exists() else 'ABSENT'}")
    L.append("")
    L += _sec("PRIORITY — STG001 (two-candle) + STG002 (8ema) confirmation", stg)
    L.append("")
    L += _sec("Variant family (all 8) x multiasset", cv)
    L.append("")
    L += _sec("v2 23-strategy sweep x multiasset", c2)
    L.append("")
    L.append("## Heavy tier")
    for lbl, cp in [("variants", RUN / "cpcv_variants" / "cpcv_results.json"), ("v2", RUN / "cpcv_v2" / "cpcv_results.json")]:
        cj = _load(cp)
        n = len(cj.get("results", cj)) if isinstance(cj, (list, dict)) else 0
        L.append(f"- {lbl} CPCV: {'present (' + str(n) + ')' if cj else 'n/a'}")
    rob = sum(1 for c in cv if c.get("robust_final")) + sum(1 for c in c2 if c.get("robust_final"))
    L.append("")
    L.append(f"## Verdict\n- combined robust_final: **{rob}**. {'Nothing promotable.' if rob == 0 else 'Review before promotion.'}")
    L.append("_Mechanical close. Lessons/handoff next session._")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(L), encoding="utf-8")
    print(f"[close] wrote {OUT}")


if __name__ == "__main__":
    main()
