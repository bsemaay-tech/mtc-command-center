"""Phase 3 — score and tier all candidates.

Scoring model (per spec):
- rule_clarity 0..5
- mech_testability 0..5
- data_availability 0..5
- edge_plausibility 0..5
- robustness_expectation 0..5
- mtc_compat 0..5
- overfit_penalty 0..-5
- data_block_penalty 0..-10
- total
"""
from __future__ import annotations

import csv
import json
import re
from pathlib import Path

ROOT = Path(r"C:/LAB/tradingview-lab/01_MASTER TEMPLATE_V2/06_QUANTLENS_LAB")
OUT = ROOT / "research" / "overnight_intake_batch_2026_05_03"
INBOX = ROOT / "00_INBOX_REPORTS"


def score_record(rec: dict, body: str) -> dict:
    low = body.lower()

    # rule clarity: presence of explicit numeric thresholds and section headers
    rule_clarity = 0
    if re.search(r"\b\d+\s*(%|percent)\b", body):
        rule_clarity += 1
    if re.search(r"\b(close above|cross above|cross below|>=|<=)\b", low):
        rule_clarity += 1
    if "stop" in low and ("atr" in low or "swing" in low or "%" in body):
        rule_clarity += 1
    if "exit" in low or "take profit" in low or "trail" in low:
        rule_clarity += 1
    if "session" in low or "vwap" in low or "ema" in low or "rsi" in low:
        rule_clarity += 1
    rule_clarity = min(5, rule_clarity)

    # mechanical testability
    mech = 0
    if rec["kind"] == "STRATEGY":
        mech += 3
    if "discretion" not in low and "feel" not in low:
        mech += 1
    if "candle confirmation" not in low and "support/resistance" not in low:
        mech += 1
    mech = min(5, mech)

    # data availability
    ac = rec["asset_class"]
    tf = rec["primary_tf"]
    if ac == "CRYPTO" and tf in ("5m", "10m", "15m", "30m", "1h"):
        data_avail = 5
    elif ac == "CRYPTO":
        data_avail = 4
    elif ac == "US_EQUITY" and tf in ("daily", "weekly", "monthly", "swing", "position"):
        data_avail = 1  # would need US daily
    elif ac == "US_EQUITY":
        data_avail = 0  # need real intraday US equity data
    elif ac == "US_MICROCAP":
        data_avail = 0
    elif ac == "OPTIONS":
        data_avail = 0
    elif ac == "UNKNOWN":
        data_avail = 3  # generic — can crypto-proxy
    else:
        data_avail = 2

    # edge plausibility — heuristic: well-known patterns get +
    edge = 2
    for kw, w in (("vcp", 2), ("breakout", 1), ("vwap", 2), ("orb", 1), ("opening range", 1),
                  ("trend follow", 1), ("momentum", 1), ("mean revers", 1), ("rsi", 0.5),
                  ("ema pullback", 1), ("episodic pivot", 2), ("stage analysis", 1),
                  ("relative strength", 1)):
        if kw in low:
            edge += w
    edge = int(min(5, edge))

    # robustness expectation — favored if multi-timeframe / risk-managed
    robust = 1
    if "trail" in low: robust += 1
    if "fixed risk" in low or "risk per trade" in low: robust += 1
    if "regime" in low or "trend filter" in low: robust += 1
    if "stage" in low: robust += 1
    robust = min(5, robust)

    # MTC compat
    mtc = 2
    low_mtc = body.lower()
    if "session" in low_mtc or "htf" in low_mtc:
        mtc += 1
    if "stop" in low_mtc and ("atr" in low_mtc or "swing" in low_mtc):
        mtc += 1
    if "trail" in low_mtc:
        mtc += 1
    mtc = min(5, mtc)

    # overfit penalty
    overfit_pen = 0
    if "optim" in low or "best parameters" in low:
        overfit_pen -= 2
    if "i found" in low and ("works" in low or "best" in low):
        overfit_pen -= 1
    if rec["kind"] != "STRATEGY":
        overfit_pen -= 1

    # data block penalty
    block_pen = 0
    if ac in ("US_MICROCAP", "OPTIONS"):
        block_pen -= 10
    elif ac == "US_EQUITY":
        block_pen -= 6
    elif ac == "FOREX":
        block_pen -= 3

    # process-only ideas → flat score
    if rec["kind"] in ("PROCESS_ONLY", "RISK_MANAGEMENT_MODULE", "EXIT_MODULE", "FILTER_ONLY"):
        rule_clarity = max(rule_clarity, 2)
        mech = 1
        data_avail = 1
        edge = 1
        robust = 1
        mtc = max(mtc, 3)  # filters/exits can fit MTC
        overfit_pen = -1
        block_pen = max(block_pen, -2)

    total = rule_clarity + mech + data_avail + edge + robust + mtc + overfit_pen + block_pen
    return {
        "rule_clarity": rule_clarity, "mech_testability": mech,
        "data_availability": data_avail, "edge_plausibility": edge,
        "robustness_expectation": robust, "mtc_compat": mtc,
        "overfit_penalty": overfit_pen, "data_block_penalty": block_pen,
        "total": total,
    }


def main() -> None:
    cards_index = json.loads((OUT / "candidates_index.json").read_text(encoding="utf-8"))
    rows = []
    for entry in cards_index:
        try:
            text = (INBOX / entry["intake"]).read_text(encoding="utf-8", errors="replace")
        except Exception:
            text = ""
        s = score_record(entry, text)
        merged = {**entry, **s}
        rows.append(merged)

    rows.sort(key=lambda r: -r["total"])

    # tiering
    tier_a, tier_b, tier_c = [], [], []
    for r in rows:
        if r["mtc_relevance"] == "PROCESS_ONLY" or r["testability"] in (
            "REJECT_NOT_TESTABLE_AS_PRODUCER", "NEEDS_US_MICROCAP_DATA",
            "NEEDS_OPTIONS_DATA", "NEEDS_FX_DATA",
        ):
            tier_c.append(r)
        elif r["total"] >= 18 and r["data_availability"] >= 3 and len(tier_a) < 12:
            tier_a.append(r)
        elif r["total"] >= 14 and len(tier_b) < 12:
            tier_b.append(r)
        else:
            tier_c.append(r)

    for r in rows:
        if r in tier_a:
            r["tier"] = "A"
        elif r in tier_b:
            r["tier"] = "B"
        else:
            r["tier"] = "C"

    # CSV
    fieldnames = [
        "tier", "cand_id", "title", "asset_class", "primary_tf", "kind",
        "mtc_relevance", "testability",
        "rule_clarity", "mech_testability", "data_availability",
        "edge_plausibility", "robustness_expectation", "mtc_compat",
        "overfit_penalty", "data_block_penalty", "total",
        "card_path", "intake",
    ]
    with (OUT / "PRIORITY_MATRIX.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in fieldnames})

    # markdown
    md = ["# Priority Matrix", "",
          f"Total candidates: {len(rows)}",
          f"Tier A: {len(tier_a)}  |  Tier B: {len(tier_b)}  |  Tier C: {len(tier_c)}",
          "", "## Tier A — top mechanically-testable candidates", "",
          "| # | cand | title | asset | tf | total | testability |",
          "|---|------|-------|-------|----|-------|-------------|",
          ]
    for i, r in enumerate(tier_a, 1):
        md.append(f"| {i} | {r['cand_id']} | {r['title'][:70]} | {r['asset_class']} | {r['primary_tf']} | {r['total']} | {r['testability']} |")
    md.append("")
    md.append("## Tier B — secondary scan only")
    md.append("| # | cand | title | asset | tf | total |")
    md.append("|---|------|-------|-------|----|-------|")
    for i, r in enumerate(tier_b, 1):
        md.append(f"| {i} | {r['cand_id']} | {r['title'][:70]} | {r['asset_class']} | {r['primary_tf']} | {r['total']} |")
    md.append("")
    md.append("## Tier C — filter / process / data-blocked / reject")
    md.append(f"Count: {len(tier_c)} (see PRIORITY_MATRIX.csv for full list)")
    (OUT / "PRIORITY_MATRIX.md").write_text("\n".join(md), encoding="utf-8")

    # rejected/blocked
    blocked = [r for r in rows if r["data_block_penalty"] <= -6 or r["mtc_relevance"] == "DATA_BLOCKED"]
    rj_md = ["# Rejected / Data-blocked List", ""]
    for r in blocked:
        rj_md.append(f"- **{r['cand_id']}** — {r['title'][:80]} | {r['asset_class']} | reason: data_block_penalty={r['data_block_penalty']}")
    (OUT / "REJECTED_OR_BLOCKED_LIST.md").write_text("\n".join(rj_md), encoding="utf-8")

    # filter / exit / sizing modules
    mods = [r for r in rows if r["mtc_relevance"] in ("FILTER_CANDIDATE", "EXIT_CANDIDATE", "SIZING_CANDIDATE")]
    md2 = ["# Filter / Exit / Sizing Module Candidates", "",
           "These do not warrant standalone strategy backtests but should be evaluated as MTC modules.", ""]
    for r in mods:
        md2.append(f"- **{r['cand_id']}** [{r['mtc_relevance']}] — {r['title'][:80]}")
    (OUT / "FILTER_EXIT_SIZING_MODULES.md").write_text("\n".join(md2), encoding="utf-8")

    print(f"Tier A={len(tier_a)} Tier B={len(tier_b)} Tier C={len(tier_c)}")
    for r in tier_a:
        print(f"  A | total={r['total']:>2} | {r['cand_id']} | {r['asset_class']:>10} | {r['primary_tf']:>6} | {r['title'][:60]}")


if __name__ == "__main__":
    main()
