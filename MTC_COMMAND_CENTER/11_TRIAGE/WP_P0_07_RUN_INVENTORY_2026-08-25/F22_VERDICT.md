# F-22 Verdict — WP-P0-07

## Verdict

**KEEP F-22 BOUNDED.** The inventory found no strict survivor, but the repository state available in this worktree is not complete enough to prove the all-time claim that no run has *ever* produced one.

The strongest statement supported here is:

> Every row in all **67 directly parseable tracked final result JSONs** has `robust_final=false`. These comprise 63 MEGA/confirmation iterations under `03_QUANTLENS/tools/{overnight_runs,night_runs}/`, one final smoke result, two FAZ3B passes, and the Donchian ladder. A separate 13-row derived sprint/CPCV input also has zero `robust_final=true` rows. No strict survivor was found in any other record inspected.

This materially broadens the evidence beyond the single 2026-05-30 snapshot, but it does not establish “ever.”

## Strict-survivor meaning

For MEGA result records, “strict survivor” means `robust_final=true`: a row classified `PASS` or `STRONG_PASS` that also survives BH-FDR and has DSR at least 0.95. The current engine defines that conjunction in `MTC_COMMAND_CENTER/03_QUANTLENS/tools/mega_walk_forward.py:1695-1725`. The original F-22 evidence is explicitly one dated snapshot in `MTC_COMMAND_CENTER/03_QUANTLENS/_user_guide/07_BACKTEST_AND_OPTIMIZATION_RULES.md:287-294` and was already narrowed accordingly in `MTC_COMMAND_CENTER/11_TRIAGE/MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md:752-765`.

## Evidence trail

1. The path-independent sweep found previously unprompted run-record trees at:
   - `MTC_COMMAND_CENTER/03_QUANTLENS/tools/overnight_runs/`
   - `MTC_COMMAND_CENTER/03_QUANTLENS/tools/night_runs/`
   - `MTC_COMMAND_CENTER/03_QUANTLENS/tools/smoke_runs/`
   - `MTC_COMMAND_CENTER/03_QUANTLENS/tools/sprint_runs/`
2. A complete JSON parse of the 67 final result files found that every result row contains `robust_final`, every value is false, and the total number of true values is zero. The per-file evidence is enumerated in `RUN_RESULT_INVENTORY.md`; the parser and grouped output are recorded in `SEARCH_LOG.md`.
3. The two present registered research trees agree: FAZ3B pass 1 has 420 rows / 7,371 recorded trials / zero strict survivors; pass 2 has 560 rows / 9,828 trials / zero; Donchian has 4 rows / 240 trials / zero. Their result files also record `engine_version=faz3b-exit-mode-v1`.
4. `MTC_COMMAND_CENTER/05_REGISTRY/RESEARCH_RUN_REGISTRY.json:4-83` contains six run records, but only FAZ3B and Donchian have present run directories in this worktree. The recorded directories for `overnight_multiasset_2026-06-29`, `turtle_heavy_2026-07-01`, `overnight_full_2026-07-02`, and `overnight_archetypes_2026-07-03` are absent.
5. `MTC_COMMAND_CENTER/05_REGISTRY/RESEARCH_BACKTEST_REGISTRY.json:1-4` remains empty, so it cannot establish completeness or a canonical all-time identity set.
6. The sole present file under `03_QUANTLENS/05_BACKTEST_RESULTS/` is a derived profile artefact. It points to absent `night_1m_2026-06-07/iter_05` inputs, contains one profiled result, and does not record `robust_final` or the original run's configuration count. Those fields are therefore `UNKNOWN — absent from the searched derived artefact and unavailable referenced source`, not zero.
7. The tracked `MTC_COMMAND_CENTER/11_TRIAGE/RESEARCH_TRUTH_LEDGER_INVENTORY_2026-08-17.md:1-95` records that 36 canonical MEGA result files existed during its earlier inspection, identifies several null families, and documents deterministic duplicates. Those bulk outputs are git-ignored and are absent from this worktree, so their primary bytes cannot be reparsed here.
8. The same truth-ledger inventory records a run-id/path identity conflict for `overnight_full_2026-07-02` and an unregistered `overnight_resilient_2026-07-02/variants` artefact. That conflict prevents a complete, normalized run census.
9. Pre-strict May research packages under `03_QUANTLENS/research/` record aggregate backtests but do not carry the later `robust_final` field. Their strict-survivor counts remain `UNKNOWN — strict survivor count not recorded in the searched pre-strict packages` rather than being inferred from older classifications.

## Acceptance-gate answer

| Possible outcome | Result |
|---|---|
| Upgrade F-22 to “ever” | **No.** Primary result bytes and normalized identities are missing for part of the recorded estate. |
| Refute F-22 with a strict survivor | **No.** No `robust_final=true` row or other defensible strict survivor was found. |
| Leave bounded and name the gap | **Yes.** F-22 remains sweep-scoped; separately record the broader 67-file zero-survivor observation. The gaps are absent git-ignored results, pre-strict records without comparable fields, an empty canonical backtest registry, and the `overnight_full` identity conflict. |

## Consequence

No result is promoted. No research was rerun. The correct follow-on is provenance recovery/normalization, not more compute: recover or intentionally archive the missing primary result estate, repair run identities, and populate a canonical run registry before making an all-time claim.
