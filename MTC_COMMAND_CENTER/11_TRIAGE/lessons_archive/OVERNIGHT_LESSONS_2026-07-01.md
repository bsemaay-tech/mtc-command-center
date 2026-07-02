# Overnight Lessons — 2026-07-01 (turtle_heavy: A22 done RIGHT, +A23, A21 re-confirmed)

**Run:** `overnight_turtle_heavy_2026-07-01.ps1`, 16 workers, bundle
`native_multiasset_alpaca_2026-06-28`. 5 stages, 18:45→19:16 (~31 min), zero crashes, machine
**released on completion** (deadline was 08:30). Output: `05_BACKTEST_RESULTS/turtle_heavy_2026-07-01/`.

**Result:** TURTLE 357 cells → 36 PASS/STRONG, 5 BH-FDR survivors, **robust_final 0**. Deep 45-split
CPCV: 156 base + 24 turtle cells pass_rate≥0.80, PBO≈0 — yet **0 robust_final**. Nothing promotable.

## G1 — A22 applied CORRECTLY (the 06-29 failure was NOT repeated)
Given the same 14h "work till morning, don't waste it" prompt that produced the 06-29 idle-waste, this
time: (1) Gate-0 pre-read done; (2) recognized re-running the base sweep = deterministic = zero info and
**refused it**; (3) ran genuinely-NEW work instead — validation of the new `GEN_DONCHIAN_TURTLE`
variant + the first deep CPCV/PBO on the 06-29 survivors; (4) work finished in 31 min and the
orchestrator **released keep-awake** rather than idling the box to 08:30. This is A22 working as
designed: long budget → heavy-validation tier on non-identical targets → release when nothing
non-identical remains. The "morning report" is an artifact generated at completion (auto close watcher),
not a reason to hold the machine awake.

## G2 / A23 (NEW anti-pattern) — mega's sweep universe is hardcoded LEGACY
`mega_walk_forward.py` `SYMBOLS` (line 81 = 17 crypto USDT pairs) and `TIMEFRAMES` (line 87 =
`15m,1h,2h,4h,1D`) are HARDCODED. `MEGA_BUNDLE_MANIFEST` only binds where DATA is loaded from — it does
**not** set the sweep universe. A launcher that sets only the manifest still sweeps the legacy 17×5
universe (partially matching the multi-asset crypto symbols → misleading 85-cell "results"). This bit
the first launch tonight (caught pre-commit via the banner "symbols=17 tfs=[...1D]"). **Fix:** the
runner derives the universe from the manifest and overrides `mw.SYMBOLS`/`mw.TIMEFRAMES` (see
`overnight_turtle_sweep_20260701.py`), OR pass explicit `--symbol`/`--tf` for the full universe. Also:
runner must guard `mw.main()` under `if __name__ == "__main__"` (variant patch stays module-level so
Windows-spawn workers inherit it) — otherwise workers recurse ("Safe importing of main module").

## G3 — A21 re-confirmed at 51×7 multi-asset scale
Deep 45-split CPCV pass_rate looks strong (median 0.76 base / 0.87 turtle; 156+24 cells ≥0.80) and PBO
is ~0 — but **robust_final stayed 0**. CPCV/PBO measure OOS-split stability, not multiple-testing
robustness; `robust_final = PASS ∧ bh_fdr_survivor ∧ dsr_robust` and **DSR (trial-count deflation, A17)
is the binding gate**. High CPCV + low PBO is false comfort. Do not read it as promotable.

## G4 — new logic ≠ better: Turtle structural stop shows no systematic edge
The opposite-channel structural stop beat the base short-rolling-low stop in only **40%** of 315
comparable cells (12/36 PASS cells beat buy&hold). Big single-cell wins are small-sample noise (DSR≈0).
The breakout family remains non-robust; adding stop variants does not change that. Path forward is NEW
strategy logic with real edge, not more variants on this family. A TRUE trailing opposite-channel exit
(Faz 3b) needs an engine-core `simulate_slice` change and is NOT motivated by this result.

## Artifacts
`05_BACKTEST_RESULTS/turtle_heavy_2026-07-01/` (git-ignored, regenerable). Runners + variant on
`feature/strategy-param-specs` (PR #15). Dashboard: run left as research output (NOT promoted — 0
robust_final; no profile_result/top_results fabricated).
