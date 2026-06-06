# Overnight Lessons - 2026-06-05 confirmation follow-up

## Summary

- Scope: resumed the interrupted `2026-06-04` quiet confirmation run after Claude stopped on tokens.
- Run type: pre-registered confirmation, not wide discovery.
- Output: `03_QUANTLENS/05_BACKTEST_RESULTS/confirm_2026-06-04/`.
- Result: 306 cells, about 3,672 configs, 4 workers, 69.6s, 16 PASS/STRONG_PASS, 1 BH-FDR survivor, 0 DSR-robust, 0 final robust.
- Post-pipeline: multiwindow, alpha-vs-buyhold, A18-fixed morning report, aggregate, CPCV, PBO, evaluation artifacts, and scorecards completed.
- Watchdog: low-resource keep-awake/status watchdog runs until `2026-06-05T07:30:00` local.

## Findings

### C1 - Confirmation grids can finish very fast

The narrow pre-registered grid was intentionally small enough to restore DSR power and reduce fan noise. It completed in about 70 seconds, so "overnight" should not be interpreted as repeated identical deterministic loops. If the user asks for overnight duration after a deterministic confirmation run, keep a watchdog awake and spend extra compute only on non-identical validation stages.

### C2 - A18 fix worked on the confirmation report

The report now reads canonical alpha lists from `alpha_summary.json`: `ALPHA_DONE passes=16 beat_buyhold=11 premium=6 down_market_alpha=6`. The Down-Market Alpha table has 6 rows, matching the canonical count.

### C3 - Confirmation did not prove an edge

Even after shrinking the search space, DSR-robust remains 0 and Gate-2 scorecards are all INCOMPLETE. These are research artifacts only. No Pine, MTC, parity, or live-trading action is justified.

### C4 - Why repetition is worthless: the run is fully deterministic (mechanism)

The bootstrap seed is `int(md5(f"{strategy}|{symbol}|{tf}").hexdigest()[:8],16)` (mega_walk_forward.py:731), and walk-forward fold slicing + DSR are deterministic. Therefore re-running the SAME (strategy, symbol, tf, grid) produces byte-identical results. This also means the prior wide nights' "N iterations / 3.4M evaluations" were N identical copies, and the cross-iter `>=ceil(N/2)` robustness threshold was effectively all-or-nothing (a cell passes in N/N or 0/N). To gain information overnight you must change the TEST (seeds, bootstrap n, grid neighborhood, TF set, CPCV/PBO), not repeat it.

### C5 - Night under-utilization: narrow grid was right, idle watchdog was the waste (A19)

The narrow grid is methodologically required (see C6) and was correct. The mistake was leaving the machine idle-awake under a watchdog for hours after ~minutes of real compute. Given a deterministic confirmation, the remaining wall-clock should be spent on NON-IDENTICAL heavier validation that actually consumes compute and adds rigor:
  - 50k-resample bootstrap (vs default 2000) for tighter p-values.
  - Multi-seed bootstrap stability: vary the seed deliberately and report the DSR/boot-p distribution, not a single deterministic point.
  - CPCV across ALL pass cells (not a few) + PBO with more combinations.
  - Slightly wider but still pre-registered neighborhood (+/-2 grid steps) and the 4h/1D TFs.
Codex did run CPCV/PBO/Gate-2 (good), but those also finished in minutes because the universe is small; the rest of the night was idle. **Guideline:** a confirmation night's plan must include a compute-filling heavy-validation tier, sized to the available wall-clock, or it should explicitly release the machine (no pointless keep-awake).

### C6 - A17 fix confirmed working but bar not crossed (quantified)

Shrinking each grid (grid_n 60-75 -> 6-18) restored DSR power exactly as A17 predicted, because mega uses `grid_n = len(GRIDS[strat])` as the DSR trial count:

| Cell | DSR p wide (06-03) | DSR p narrow (06-05) |
|---|---|---|
| 8EMA LINK 1h | 0.068 | 0.178 |
| RSI LINK 2h | 0.000 | 0.189 |
| Donchian ETH 2h | (n/a) | 0.341 |
| TwoCandle ETH 2h | (n/a) | 0.381 |

DSR rose from ~0.0 to ~0.34-0.38 for the best cells, but NONE cleared the 0.50 crypto research threshold. Cross-symbol generalization was positive (edge appeared on LINK 1h+2h, ETH 2h, NEAR 1h while buy&hold was negative = real alpha, not beta), yet statistical confirmation failed. Verdict stands: `STATISTICALLY_UNCONFIRMED`, max `PROMOTE_TO_FORWARD_PAPER_TRADE`, no integration.

## Morning Review (DONE 2026-06-05, Claude)

- Watchdog confirmed awake until 07:30; all artifacts present (morning_report, mega, alpha, cpcv, pbo, 16 eval artifacts, 16 scorecards).
- Report A18 count verified: down_market_alpha=6 matches ALPHA_DONE.
- Gate-2: 16/16 INCOMPLETE (scores 32-46), 0 pass — INCOMPLETE is the honest status (MEGA lacks ~17 Gate-2 metrics, see NEXT_STEPS SP-004-METRIC-ENRICHMENT), not a FAIL.
- Decision: no candidate promoted. Forward-paper observation optional for the two least-weak cells (8EMA LINK 1h, Donchian ETH 2h). No Pine/MTC/parity/live action.
- Source review paths: `cpcv/CPCV_VALIDATION_REPORT.md`, `pbo/PBO_REPORT.md`, `scorecards/*.scorecard.json`.

## Heavy-Tier Night (DONE 2026-06-05 evening, Claude)

User asked for an overnight session "≥3,000,000 cases". Recognized the determinism
trap up front (seed=md5, mega:1130 — repeating an identical sweep is zero-info, A19)
and refused to loop-pad. Instead ran genuinely-new work, then released.

**What ran (run dir `05_BACKTEST_RESULTS/heavy_tier_2026-06-05/`):**
- First full **43-strategy** sweep under TODAY's committed enriched engine (today's
  prior sweeps were 20-strategy only). 3655 cells, 18 workers, 2109s. 52 PASS + 20
  STRONG_PASS = **72 candidate cells** (vs 38 in the 20-strategy run).
- **3×-deeper CPCV**: n_groups=10 → 45 splits/cell on all 72 (vs committed 15).
  37 cells ≥0.70 pass-rate, **24 ≥0.80**.
- PBO=0.0; eval artifacts 72; Gate-2 **53 OK/pass, 19 FAIL, 0 INCOMPLETE**
  (metrics fully scorable now); scorecard_v2 72, **promotable 0** (Gate3 INCOMPLETE).

### C7 - Deeper CPCV does NOT rescue DSR (key finding)
Combined bar Gate2 PASS ∧ CPCV-deep(45)≥0.80 ∧ DSR≥0.50 = **0 of 72**. 21 cells pass
Gate2 + CPCV≥0.80 yet **all have DSR<0.50**. More OOS splits raise CPCV confidence but
do nothing for DSR, because DSR's trial count = grid size (A17), not split count.
Broad 43-strategy discovery inflates the family → DSR floored. **Re-confirms
NIGHT-FOLLOWUP-002**: the productive next step is a narrow pre-registered confirmation
grid, not deeper/broader discovery. Least-weak: DEEPAK_SNAPBACK TRX 2h (DSR 0.418,
CPCV 0.867, G2 92); DEEPAK_259 TRX 4h (DSR 0.128, CPCV 1.0).

### C8 - Alpha short-trap
Top "excess alpha" rows were QL_QTREND_V1_SHORT shorts during −81% buy&hold crashes.
Regime-robust+param-stable `premium`/`down_market_alpha` filters = 0. Short-in-downtrend
is not durable alpha; the canonical filtered counts (0/0) are the honest read.

### A20 - PBO OOM at high CPCV split count
`probabilistic_pbo.estimate_pbo` enumerates the FULL `C(n_splits, n_splits/2)` combo
list before applying `--max-combinations` (slice happens after enumeration, pbo:63-68).
At n_groups=10 → 44 usable splits → C(44,22)≈2T → MemoryError; the `--max-combinations`
cap does NOT help. **Fix used:** feed PBO (and eval-artifacts, for score comparability)
from a standard 15-split CPCV (`cpcv15/`, C(14,7)=1716 combos); keep the deep 45-split
CPCV as a supplementary harder-OOS robustness table only. Long-term: make estimate_pbo
sample combos lazily (itertools.islice / random sample) when capped.
