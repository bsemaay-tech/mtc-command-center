# Overnight Lessons — 2026-07-03 (12 NEW archetypes → 0 robust → methodological ceiling)

**Run:** `overnight_archetypes_resilient_2026-07-03.ps1`, 20 workers, 6 folds, 18:27→18:48 (~21 min),
zero crashes, released. Watchdog clean all night. 12 genuinely-new archetypes (volume/gaps/regime/
true-VWAP/inside-bar/range-expansion) × multiasset + deep CPCV/PBO. **4284 cells, robust_final 0.**

## G1 (the big one) — even genuinely-NEW signals are non-robust; the ceiling is METHODOLOGICAL
Over 4 nights we have now validated the **complete existing library (51 archetypes) AND 12 brand-new
archetypes using signal sources the library never touched (volume, gaps, volatility-regime, true
volume-weighted VWAP)**. Result: **63 archetypes, 0 robust_final** on any asset/TF. When new logic +
new signals STILL return 0, the bottleneck is almost certainly **not strategy selection** — it is
structural. Stop adding strategies; fix the methodology.

## G2 — the gates never line up (why DSR "passes" are illusory)
Several new archetypes hit **DSR ≥ 0.95 on individual cells** (RANGE_EXPANSION 0.99/LQD-30m,
HIGH_PROXIMITY 0.99/AMD-2h, VOL_REGIME 0.88/GOOGL-1h) — but every one is on an **INSUFFICIENT_TRADES**
cell (small-sample DSR lottery). Where trades are sufficient, DSR collapses. `robust_final =
PASS ∧ bh_fdr_survivor ∧ dsr_robust` is never simultaneously satisfied. High DSR + low trades is not
edge.

## Structural causes (the real ceiling)
1. **DSR trial-count deflation (A17):** DSR's trial count = grid size, so any grid ≥~15 nodes makes the
   0.95 bar nearly unreachable unless raw edge is huge. This alone caps almost everything.
2. **Fixed exit (global exec model):** 2R target / 96-bar limit / next-open entry, optimized by nothing.
   Likely the binding constraint — entry logic can't overcome a capped, un-tuned exit.
3. **Micro-price crypto (SHIBUSD/DOGEUSD/UNIUSD):** compounding artifacts dominate every leaderboard and
   pollute BH-FDR/DSR pooling (C8 at scale).
4. **Multi-asset pooling:** 51 heterogeneous symbols in one family dilute any per-regime edge.

## Pivot / next (methodology, not more archetypes) — [AI: Barış decision + Claude]
1. Exclude/winsorize micro-price crypto; re-score.
2. Enforce a hard MIN_TRADES floor + adopt the research-robust DSR bar (≥0.50 per rules) instead of 0.95.
3. **Make the exit a swept knob** (2R/3R/trailing/opposite-channel) — engine-core `simulate_slice` change
   = Faz 3b, approval-gated. This is the highest-leverage fix (the fixed exit is the most likely ceiling).
4. Single-asset-class subsets (liquid US equities only) instead of 51-symbol pooling.

## Resilience (held again)
Per-stage retry + PID lockfile + external watchdog Task: ran clean, no death, no false relaunch — the
A25/A26 fixes from 2026-07-02 are proven over a second night. This part of the pipeline is now solid.

## Meta — the "use the full night" tension is resolved honestly
The genuinely-new budget for 12 archetypes at 6 folds was ~21 min; the machine released (A22/A24) rather
than idling. Filling 14h with valid compute is impossible for a finite library — and the 4-night result
says the answer is **not** more compute/strategies but a **methodology change**. Vanity case-count is a
dead end.

## Artifacts
`overnight_archetypes_2026-07-03/` (git-ignored). 12 archetypes + runners + watchdog on
`feature/strategy-param-specs` (PR #15). Nothing promoted; nothing fabricated.
