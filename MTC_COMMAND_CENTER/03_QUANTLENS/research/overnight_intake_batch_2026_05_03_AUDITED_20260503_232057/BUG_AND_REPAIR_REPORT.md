# Bug & Repair Report

## Bugs found in first run
1. **Inventory schema mismatch / count drift.** First-run `INTAKE_INVENTORY.csv` reported 73 valid intakes but used a different dedupe heuristic. Audited inventory shows 56 unique-by-title valid intakes plus 30 title-duplicates and 1 video-ID duplicate. Difference is dedupe heuristic, not data corruption.
2. **None of the metric recomputations failed.** All 10 audited strategy folders' aggregated PF/net/DD/win-rate match independently recomputed values within rounding tolerance.
3. **Fee-stress monotonicity holds for all 10 audited strategies.** No fee-stress bug detected.
4. **Classification was conservatively WEAK on CANDIDATE_001 (Kell Wedge).** Audit re-run with explicit Stage-2 criteria (PF≥1.20 base, ≥1.10 at 2x, ≥1.0 at 3x, DD<60%, ≥30 trades, ≥5 assets) qualifies it for **PASS_STAGE2**. This is a classification *upgrade*, not a bug.
5. **CANDIDATE_011 first labeled simply REJECT.** Audit confirms REJECT_NO_EDGE as standalone but flags it explicitly as a *filter overlay candidate* — this is metadata enrichment, not a corrected bug.

## Repairs / additions in audited folder
- Independent `audit_recompute.py` recomputes every metric from raw trades.
- Independent fee-stress sweep at base / 2x / 3x of inferred per-trade base cost.
- New master comparison ranks candidates by audit class and PF.
- MTC role mapping per candidate; explicit DO_NOT_INTEGRATE_YET list.
- Source-quality heuristic per candidate.
- Horizon-split reports: day-trade / swing / position.

## Remaining unresolved issues
- US-equity-native data still missing → CANSLIM, Weinstein, Minervini-style, HighBeta cannot be honestly tested.
- Microcap short data missing → Ty Rajnus / Brian Lee remain DATA_BLOCKED.
- Crypto-proxy results for US-equity-native setups (CANDIDATE_002 Martin Luke AVWAP) carry an unresolved validity gap and must not be cited as edge proof.
- 5m day-trade candidates (CANDIDATE_008/009) tested on only 5 crypto symbols; expand to 10 in a rerun if pursued.