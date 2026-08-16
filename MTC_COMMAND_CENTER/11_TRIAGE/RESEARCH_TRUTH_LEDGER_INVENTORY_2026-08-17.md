# Research Truth-Ledger Inventory — 2026-08-17

## 1. Purpose and boundary

This is **Package 0 preparation only**. It inventories historical QuantLens research evidence so a later, separately authorized package can populate the empty backtest truth ledger without counting deterministic reruns as new evidence.

No backtest, optimization, Pine/MTC/Bridge change, registry edit, promotion, or Git action was performed. The inventory is evidence-bounded: an absent field is recorded as unknown rather than reconstructed by assumption.

Current control facts:

- `05_REGISTRY/RESEARCH_RUN_REGISTRY.json:4-83` contains six run-level records.
- `05_REGISTRY/RESEARCH_BACKTEST_REGISTRY.json:1-4` has `generated_at: null` and an empty `results` array.
- The canonical result tree contains 36 files named `MEGA_walk_forward_results.json`; only four of those result families are directly named by current run-registry paths, while FAZ3B and Donchian live under `03_QUANTLENS/research/`.
- The canonical rules require parameters, date ranges, symbols, timeframes, metrics, runtime, workers and artifact identity to be documented (`03_QUANTLENS/_user_guide/07_BACKTEST_AND_OPTIMIZATION_RULES.md:186-193`) and dataset manifest fields/hashes to be preserved (`.../07_BACKTEST_AND_OPTIMIZATION_RULES.md:285`).
- The engine selects its dataset through `MEGA_BUNDLE_MANIFEST` (`03_QUANTLENS/data/README.md:8-16`); therefore a result file that does not stamp its manifest/hash cannot, by itself, prove the exact input bytes.

## 2. Proposed identity rule

One ledger evaluation family should be identified by the following immutable tuple, with `UNKNOWN` used when old evidence cannot supply a field:

`strategy implementation hash + literal parameter set/grid + symbol + timeframe + dataset manifest hash + normalized-data SHA256 + data window + exit mode + costs/slippage + engine version/commit + fold/lockbox rules`

Two artifacts are not independent evidence when that tuple is identical. Sorting output rows differently, changing a generated timestamp, moving a file, or rerunning a deterministic seed does not create a new evaluation.

The primary multi-asset manifest does contain per-dataset `normalized_sha256` values (for example `03_QUANTLENS/data/native_multiasset_alpaca_2026-06-28/manifests/dataset_manifest.json:17-29`), but older result files do not embed the manifest hash or those data hashes. Those hashes are therefore **candidate join evidence**, not yet a proven historical pin.

## 3. Registered run families

| Run/family | Known identity and scope | Disposition | Registration readiness | Exact evidence |
|---|---|---|---|---|
| `overnight_multiasset_2026-06-29` | 20 strategies × 51 symbols × 7 TFs = 7,140 cells; primary 2026-06-28 multi-asset bundle; 8 bps cost; per-row data window, trial count and winning parameters are present. Older schema does not stamp exit mode, engine version, grid stride, manifest hash, data SHA or code hash. | **NULL / NOT PROMOTABLE**: `robust_final=0`. | **PARTIAL** — safe at run/cell summary level; exact literal-evaluation ledger needs historical engine/code/data pin reconstruction. | Run registry `05_REGISTRY/RESEARCH_RUN_REGISTRY.json:6-18`; result cost/window/trials `03_QUANTLENS/05_BACKTEST_RESULTS/overnight_multiasset_2026-06-29/MEGA_walk_forward_results.json:7,4420-4422`; outcome `.../MORNING_REPORT.md:7-24,44-45`. |
| `faz3b_stage1_20260705` | 20 strategies; SPY/QQQ/AAPL/MSFT/NVDA/AMZN/TSLA; 10m pass = 420 rows over three new exits; 1h pass = 560 rows over four exits. Explicit `exit_mode`, `engine_version=faz3b-exit-mode-v1`, `grid_stride=3`; engine commit `b4b11daf`; 8 bps cost. | **RESEARCH-ROBUST ONLY / NOT PROMOTABLE**: three new-mode 1h cells met the research threshold; `robust_final=0`. The discarded 60-row malformed-launch block is not evidence. | **HIGH-PARTIAL** — exit/engine/stride are pinned, but manifest hash, normalized-data SHA and strategy implementation hash are not embedded in each result. | Run registry `05_REGISTRY/RESEARCH_RUN_REGISTRY.json:21-30`; report `03_QUANTLENS/research/faz3b_stage1_20260705/STAGE1_REPORT.md:5,12-19,24-29,71`; result stamps `.../pass1_10m/MEGA_walk_forward_results.json:7,64-96`. |
| `turtle_heavy_2026-07-01` | `GEN_DONCHIAN_TURTLE`; 51 × 7 = 357 cells; structural opposite-channel stop; grid 24; 8 bps. Deep CPCV/PBO is derived validation of the same base/turtle survivors, not a new signal sweep. | **VALIDATED_NULL / NOT PROMOTABLE**: 0 DSR robust, 0 robust final. | **PARTIAL** — run/cell summaries can be recorded; older result schema lacks immutable data/code/exit stamps. | Variant registry `05_REGISTRY/VARIANT_LOG_REGISTRY.json:167-179`; report `03_QUANTLENS/05_BACKTEST_RESULTS/turtle_heavy_2026-07-01/MORNING_REPORT.md:6-20,37-46,53-63`. |
| `overnight_full_2026-07-02` registry record | Registry says “6 missing-knob tuned variants” and points to `stageA_v2_multiasset`; that artifact actually contains 23 different `QL_*` strategies and 8,211 cells. | **IDENTITY CONFLICT — DO NOT REGISTER UNDER THIS RUN ID**. Artifact itself is null (`robust_final=0`) but does not prove the registry claim. | **BLOCKED** pending run-id/path repair with provenance. | Registry claim/path `05_REGISTRY/RESEARCH_RUN_REGISTRY.json:43-50`; pointed report says 23 strategies/8,211 cells and `robust_final=0` at `03_QUANTLENS/05_BACKTEST_RESULTS/overnight_full_2026-07-02/stageA_v2_multiasset/HEAVY_TIER_MORNING_REPORT.md:7-17`. |
| `overnight_resilient_2026-07-02/variants` unregistered artifact | Actual related result contains eight strategies and 2,856 cells: the six missing-knob variants plus `GEN_DONCHIAN_TURTLE` and `GEN_TWOCANDLE_CONFIRM`; 51 × 7, 8 bps. | **NULL / NOT PROMOTABLE**: `robust_final=0`; CPCV marked missing in its morning report. | **PARTIAL, UNREGISTERED** — likely source evidence for the six variant records, but it cannot silently replace the mismatched registered path. Needs a new/proven run identity or documented repair. | Actual report `03_QUANTLENS/05_BACKTEST_RESULTS/overnight_resilient_2026-07-02/variants/HEAVY_TIER_MORNING_REPORT.md:7-25`; six variant claims point to the conflicting run ID at `05_REGISTRY/VARIANT_LOG_REGISTRY.json:182-263`. |
| `overnight_archetypes_2026-07-03` | 12 new archetypes × 51 × 7 = 4,284 cells; six-fold WF; 8 bps. | **TESTED NULL / NOT PROMOTABLE**: `robust_final=0`. Current variant registry still labels all 12 `UNVALIDATED`; that is a reconciliation issue, not permission to rewrite status. | **PARTIAL** — record null run/cell summaries; resolve whether canonical status should become `VALIDATED_NULL` under current vocabulary. | Run registry `05_REGISTRY/RESEARCH_RUN_REGISTRY.json:53-60`; result report `03_QUANTLENS/05_BACKTEST_RESULTS/overnight_archetypes_2026-07-03/MORNING_REPORT.md:6-19,41-53`; variant status examples and run links `05_REGISTRY/VARIANT_LOG_REGISTRY.json:6-164`. |
| `donchian_crypto_ladder_2026-07-13` | `GEN_DONCHIAN_BREAKOUT`; BTCUSD/ETHUSD × 1h/4h; grid 60; explicit `fixed_2R`, `faz3b-exit-mode-v1`, stride 1; 8 bps round-trip plus documented 2 bps/side slippage; windows 2021-01-01–2026-06-28. | **VALIDATED_NULL**: 3 rejected, 1 insufficient; 0 BH-FDR, DSR robust or robust final. | **HIGHEST READINESS** — four cell summaries and the 60-combination family can be registered after joining/proving the exact manifest/data/code hashes. | Run registry `05_REGISTRY/RESEARCH_RUN_REGISTRY.json:63-82`; result stamps `03_QUANTLENS/research/donchian_crypto_ladder_2026-07-13/MEGA_walk_forward_results.json:7,58-60,143-145`; grid/cost/outcome `11_TRIAGE/DONCHIAN_CRYPTO_LADDER_VERDICT_2026-07-13.md:25-26,45-68,96-109`. |

## 4. Deterministic duplicate and overlap findings

### 4.1 Proven deterministic duplicate cluster

A keyed semantic hash was computed read-only by sorting every result row by `strategy|symbol|timeframe` and hashing the complete sorted rows. All files below produced the same SHA256:

`E276C78D7B28F38D6DE3B26CDD92E0B40C7134DE734B6D5FA2E87CE05D17A9CF`

- `03_QUANTLENS/05_BACKTEST_RESULTS/full_sweep_2026-06-07/MEGA_walk_forward_results.json`
- `.../night_1m_2026-06-07/iter_01` through `iter_05`
- `.../night_3M_2026-06-08/iter_01` through `iter_09`

Each contains the same 5,015 keyed rows: 59 strategies × 17 symbols × 5 timeframes, with 0 robust-final rows. Raw file SHA256 values differ because generated metadata and row order differ; keyed contents do not. Truth-ledger treatment: **one evaluation family and 14 deterministic duplicate artifacts**, not 15 independent trials.

This is exactly the failure mode prohibited by runbook A19/A22: deterministic repetition adds zero information (`11_TRIAGE/BACKTEST_OPTIMIZATION_RUNBOOK.md:398-401`).

### 4.2 Proven partition/aggregation overlap

The union of:

- `batch023_034_2026-06-07/MEGA_walk_forward_results.json` — 4,590 rows / 54 strategies; and
- `remaining_2026-06-07-recovery/MEGA_walk_forward_results.json` — 425 rows / 5 strategies

is exactly the same 5,015 keyed rows as `full_sweep_2026-06-07`. These are source partitions/assembly evidence, not three independent research families. A later ledger should keep provenance links but count each cell once.

### 4.3 Historical-control reuse, not new discovery

- Turtle `cpcv_base/` and `pbo_base/` reuse 2026-06-29 base survivors for deeper validation. They add a validation method, not new strategy/symbol/timeframe signal evaluations (`turtle_heavy.../MORNING_REPORT.md:37-46,58-63`).
- FAZ3B 10m historical `fixed_2R` control rows are reused from earlier evidence; only the three explicitly swept exits are new in pass 1.
- FAZ3B’s report calls the 1h fixed-2R baseline “first time ever” (`STAGE1_REPORT.md:40-42,58`), but the run registry says the 2026-06-29 sweep already evaluated all 51 symbols/7 TFs and specifically all Keltner 1h cells (`RESEARCH_RUN_REGISTRY.json:11-16`). Because Stage1 used stride 3 and a newer engine, the aggregate run is not automatically a duplicate, but the historical-novelty statement is conflicted and trial-family accounting must be reconstructed before registration.
- The Donchian crypto report states deterministic reruns reproduce byte-identically (`11_TRIAGE/DONCHIAN_CRYPTO_LADDER_VERDICT_2026-07-13.md:132`). No second canonical result artifact was found, so there is no duplicate file to register.

## 5. Legacy result families absent from the run registry

These artifacts are real evidence but are not safe to bulk-register merely from directory names. They should be reconciled in bounded clusters:

| Cluster | Artifact evidence | Preliminary treatment |
|---|---|---|
| Early 43-strategy baseline/heavy | root `05_BACKTEST_RESULTS/MEGA_walk_forward_results.json` and `heavy_tier_2026-06-05/` — each 3,655 rows, 43 × 17 × 5. | Compare keyed rows, engine version and report lineage; likely baseline/enrichment generations rather than independent signal families. |
| 20-strategy metric/enrichment chain | `enriched_metrics_2026-06-05`, `bh_benchmark_...`, `worst_window_...`, `annualized_risk_...`, `slippage_...`, `final_gate2_...` — each 1,700 rows, 20 × 17 × 5. | Treat as one underlying signal-evaluation cohort with successive metric/cost/enrichment passes until tuple differences are proven. Slippage may be a genuinely distinct cost scenario; do not merge it without field-level verification. |
| Narrow confirmation | `confirm_2026-06-04` — 306 rows, 6 × 17 × 3; `FOCUSED_VALIDATION_2026-05-31` — 680 rows, 8 × 17 × 5. | Candidate distinct confirmation families; recover prereg, grid, data and code pins before registration. Old aggregated reports may be superseded by the current strict-majority rule (`07_BACKTEST_AND_OPTIMIZATION_RULES.md:275`). |
| New/family templates | `new_strategies_2026-06-06` (68 rows), `lbr_coil_2026-06-06` (68), `fam_templates_2026-06-06` (204). | Candidate unique logic families; verify strategy identities and whether template rows are discovery-only/null/blocked. |
| Full 59-strategy sweep | `full_sweep_2026-06-07` plus its exact partitions and 14 deterministic reruns. | Register once after identity reconstruction; link all redundant artifacts as provenance only. |
| Smoke | `smoke_night_1m_2026-06-07` — one row. | Operational smoke evidence only; do not treat as a research conclusion unless its prereg and full identity exist. |
| Resilient eight-variant sweep | `overnight_resilient_2026-07-02/variants` — 2,856 rows. | Preserve separately; repair the current `overnight_full` identity conflict before associating the six variant records. |

All 36 canonical result files had different raw SHA256 hashes. That does **not** mean 36 unique families: the semantic comparison above proves that ordering/metadata can hide deterministic duplicates.

## 6. Null, rejected and blocked dispositions

| Disposition | Families |
|---|---|
| **Validated/tested null** | 2026-06-29 multi-asset; Turtle; resilient eight-variant artifact; 23-strategy stageA artifact; 12 archetypes; Donchian crypto ladder. All report `robust_final=0`. |
| **Research-only positive, not promotable** | FAZ3B Stage1 has three 1h new-exit research-robust cells, but `robust_final=0`; no production/paper promotion follows. |
| **Rejected/insufficient cells** | Donchian ladder: three rejected and one insufficient. Other broad sweeps contain many FAIL/NO_DATA/INSUFFICIENT cells; preserve cell dispositions, never compress them into “not run.” |
| **Blocked from exact registration** | `overnight_full_2026-07-02` identity/path conflict; older artifacts missing immutable data/code/exit identity; FAZ3B historical-novelty conflict; archetype `UNVALIDATED` status versus completed-null report. |
| **Excluded operational artifact** | FAZ3B’s discarded 60 all-NO_DATA malformed launch and the one-row smoke are not independent research results. |

## 7. Gaps that prevent exact registration

1. **No historical evaluation key.** The empty backtest registry has no populated canonical key to enforce deduplication (`05_REGISTRY/RESEARCH_BACKTEST_REGISTRY.json:1-4`).
2. **No result-embedded manifest or data hash in old runs.** A dated bundle name is not proof of exact bytes. The current manifest’s per-file hashes can only be joined after its historical immutability/pin is proven.
3. **No strategy implementation hash.** A strategy ID can refer to changed Python logic over time.
4. **No engine commit/version on old rows.** FAZ3B added explicit engine stamps; older runs generally lack them.
5. **Implicit exit mode in old runs.** Contemporary reports may imply `fixed_2R`, but the row itself does not.
6. **Costs are incomplete.** `cost_bps=8` is usually present; slippage is often only described in prose and not stamped as an immutable row field.
7. **Literal grid evaluations are not persisted.** Older rows preserve `trial_count` and the winning `best_params`, not every tested literal parameter tuple. Exact trial-level registration cannot be reconstructed from the summary alone.
8. **Run-id/artifact mismatch.** `overnight_full` cannot be accepted until the six-variant claim is bound to the actual eight-variant artifact or superseded by a documented identity repair.
9. **Disposition vocabulary drift.** Completed null archetypes remain `UNVALIDATED`, while Turtle and Donchian use `VALIDATED_NULL`.
10. **Historical trial-family conflict.** FAZ3B’s “first-ever 1h” claim conflicts with the 2026-06-29 all-TF sweep and can affect DSR trial counting.

## 8. Fastest safe Package 0 follow-on order

No step below authorizes compute or registry writes; each is a documentation/reconciliation package first.

1. **Define the ledger schema and evaluation key.** Require explicit unknowns; never manufacture hashes.
2. **Register Donchian ladder first.** It has the best exit/engine/grid/window/cost evidence and only four cells.
3. **Register FAZ3B Stage1 second.** Preserve pass1/pass2 separately, exclude the discarded launch, and resolve historical fixed-2R overlap before setting trial-family counts.
4. **Register 2026-06-29 and Turtle summaries.** Link Turtle base CPCV/PBO to the prior base family rather than duplicating cells.
5. **Repair the 2026-07-02 identity split.** Create distinct identities for the 23-strategy stageA artifact and the eight-variant resilient artifact; only then reconcile the six variant records.
6. **Reconcile archetype statuses.** Keep the completed-null evidence; choose vocabulary through an explicit registry maintenance decision.
7. **Collapse the 59-strategy duplicate cluster.** One family, source partitions as provenance, 14 deterministic reruns as duplicates.
8. **Forensically process the remaining legacy clusters.** Use keyed semantic comparison plus prereg/report/commit lookup; do not infer identity from matching row counts alone.

## 9. Bottom line

The repository has substantial historical research evidence, but the truth ledger is empty and exact identity is uneven. The safest immediate conclusion is not “research was forgotten”; it is that run-level reports exist while cell/trial-level provenance was never normalized into the current ledger.

The highest-value correction is a provenance-first registration pass, starting with Donchian and FAZ3B. It should explicitly collapse deterministic repeats, preserve null/rejected results, and quarantine identity conflicts. No old result in this inventory authorizes promotion, paper trading, live trading, Pine/MTC changes, or a fresh backtest.
