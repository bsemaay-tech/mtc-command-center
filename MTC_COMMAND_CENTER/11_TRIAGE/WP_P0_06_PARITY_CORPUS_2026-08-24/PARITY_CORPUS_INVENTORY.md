# WP-P0-06 Parity Corpus Inventory

Date: 2026-08-24
Audit tier: T1
Lane: C
Base: `fbb05d7f46bc78b2875aa6d029e7fb2f2a8b14d7`

## Decision result

The March/April discrepancy is **not evidence of a temporal regression**. Corpus B ran the legacy `MTCRunner` in `src.engine.mtc_runner`, while Corpus A ran the separate `mtc_v2.core.runner.Runner`; Corpus B's TradingView export is labelled `MT_CORE2`, while Corpus A's exports are labelled `MTCV2_1304`. The brief posed this implementation-identity test explicitly (`MTC_COMMAND_CENTER/11_TRIAGE/MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md:478-484`), and the executable call chains establish that the subjects differ (`MTC_COMMAND_CENTER/02_MTC_BACKTEST/scripts/run_case.py:23-29`, `MTC_COMMAND_CENTER/02_MTC_BACKTEST/scripts/run_case.py:348-354`, `MTC_COMMAND_CENTER/02_MTC_BACKTEST/parity_compare.py:23-38`, `MTC_COMMAND_CENTER/02_MTC_BACKTEST/parity_compare.py:1787-1800`).

This closes the narrow March-versus-April question as **different implementations, not regression evidence**. It does not prove that either implementation did or did not regress internally. A temporal-regression claim would require the same pinned Pine and Python source identities, the same corpus/data, and the same oracle contract at both dates; those conditions are not present.

No repository-wide parity percentage may be reported from these corpora. Besides the different subjects, Corpus A uses a three-way TradingView/PineTS/`mtc_v2` contract with numeric tolerances, Corpus B's default “strict” contract ignores price and quantity, Corpus C is unavailable, and Corpus D covers entry signals only (`MTC_COMMAND_CENTER/12_PARITY_PINETS/manual_tw_futures_audit.py:23-47`, `MTC_COMMAND_CENTER/02_MTC_BACKTEST/src/parity/compare_tv_trades.py:412-420`, `MTC_COMMAND_CENTER/02_MTC_BACKTEST/src/parity/compare_tv_trades.py:471-478`, `MTC_COMMAND_CENTER/11_TRIAGE/MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md:3509-3512`).

## Corpus A — April manual TradingView / PineTS / `mtc_v2` audit

Primary artifacts: `MTC_COMMAND_CENTER/12_PARITY_PINETS/parity_summary.md` and `parity_results.json`.

| Required field | Inventory result | Evidence |
|---|---|---|
| Exact Pine implementation and version | Export identity: `MTC_V2`, short-title label `MTCV2_1304`. **UNKNOWN — searched the case workbooks' recorded filenames, current `MTC_V2.pine`, all Git history for the corpus, and import-time blobs; no generation-time Pine commit/hash or `MTCV2_1304` source snapshot is recorded.** The tracked Pine snapshot is `MTCV2_1404`, so it cannot be substituted silently. | `MTC_COMMAND_CENTER/12_PARITY_PINETS/parity_results.json:19-23`; `MTC_COMMAND_CENTER/01_MTC_PROJECT/01_PINE/MTC_V2.pine:1-7` |
| Exact Python implementation and version | Implementation: `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core/runner.py::Runner`, resolved and called by `parity_compare.py`. **UNKNOWN — searched Git history and import-time blobs; no generation-time commit/hash is stored in the corpus.** The first tracked imported `parity_compare.py` blob is `9560195bab80987417c0d01590d5506d43863e87`, but import on 2026-05-31 does not prove the 2026-04-14 execution version. | `MTC_COMMAND_CENTER/02_MTC_BACKTEST/parity_compare.py:23-38`; `MTC_COMMAND_CENTER/02_MTC_BACKTEST/parity_compare.py:748-766`; `MTC_COMMAND_CENTER/02_MTC_BACKTEST/parity_compare.py:1787-1800` |
| PineTS version | `0.9.6`; the bridge loads its vendored minified PineTS build and records this literal in output metadata. | `MTC_COMMAND_CENTER/02_MTC_BACKTEST/mtc_bridge.mjs:16-22`; `MTC_COMMAND_CENTER/02_MTC_BACKTEST/mtc_bridge.mjs:552-565` |
| Generation date | `2026-04-14 14:40:47 UTC`. | `MTC_COMMAND_CENTER/12_PARITY_PINETS/parity_summary.md:1-5`; `MTC_COMMAND_CENTER/12_PARITY_PINETS/parity_results.json:1-9` |
| Data and case scope | Planned IDs `case_103` through `case_162` (60 IDs); 58 exports present, `case_160` and `case_161` absent. Export filenames identify `BINANCE:BTCUSDT.P`. **UNKNOWN — searched `parity_summary.md`, `parity_results.json`, all 60 `case_plan.json` files, and the audit script; the corpus aggregate does not preserve exact chart timeframe or backtest start/end, and the referenced per-case reports are absent.** | `MTC_COMMAND_CENTER/12_PARITY_PINETS/parity_summary.md:1-5`; `MTC_COMMAND_CENTER/12_PARITY_PINETS/parity_summary.md:470-480`; `MTC_COMMAND_CENTER/12_PARITY_PINETS/parity_results.json:19-23`; `MTC_COMMAND_CENTER/12_PARITY_PINETS/manual_tw_futures_audit.py:477-514` |
| Oracle identity and tolerances | TradingView Strategy Report workbooks are the reference oracle; their trades are compared with PineTS trades and `mtc_v2` Python trades. Strict trade tolerances: price `0.05`, quantity `0.001`; soft trade tolerances: price `0.05`, quantity `0.005`. Strict outcome tolerances: value/PnL/excursion `0.1`, PnL%/excursion% `0.02`; soft: value `50`, PnL `5`, PnL% `0.05`, excursion `250`, excursion% `0.25`. | `MTC_COMMAND_CENTER/12_PARITY_PINETS/manual_tw_futures_audit.py:23-47`; `MTC_COMMAND_CENTER/12_PARITY_PINETS/manual_tw_futures_audit.py:935-974`; `MTC_COMMAND_CENTER/12_PARITY_PINETS/manual_tw_futures_audit.py:979-1002` |
| Executable / skipped / not-comparable / reuse counts | 58 executed three-way comparisons; 0 reuses recorded; 2 planned IDs not executed because exports were missing; 0 cases labelled `SKIP`; 0 labelled `NOT_COMPARABLE`. Result: 50 overall strict-or-soft passes and 8 failures. Pairwise strict passes were TV=PineTS 33/58, TV=Python 27/58, PineTS=Python 50/58. | `MTC_COMMAND_CENTER/12_PARITY_PINETS/parity_summary.md:3-12`; `MTC_COMMAND_CENTER/12_PARITY_PINETS/parity_summary.md:478-480` |
| `tw_*` semantic vector | **UNKNOWN — searched the aggregate JSON/Markdown, all `case_103`-`case_162` plans, and `build_python_research_overrides`; no full per-corpus `tw_*` vector is recorded.** The script's only explicit `research` overrides apply to `case_010` and `case_023`, outside this corpus, but absence of that special override is not a complete vector. | `MTC_COMMAND_CENTER/12_PARITY_PINETS/manual_tw_futures_audit.py:442-449`; `MTC_COMMAND_CENTER/12_PARITY_PINETS/manual_tw_futures_audit.py:925-933` |

### Named unresolved mismatches

Eight cases remain `FAIL` under the corpus's overall strict-plus-soft classification:

| Case | Setting / pair | Recorded mismatch |
|---|---|---|
| `case_110` | `time_stop_eod` | TV, PineTS, and Python each have 142 trades, but all three pairwise strict comparisons fail. (`MTC_COMMAND_CENTER/12_PARITY_PINETS/parity_summary.md:70-76`) |
| `case_111` | `time_stop_eow` | TV, PineTS, and Python each have 136 trades, but all three pairwise strict comparisons fail. (`MTC_COMMAND_CENTER/12_PARITY_PINETS/parity_summary.md:78-84`) |
| `case_134` | `refresh_on_new_raw` | TV/PineTS have 0 trades; Python has 131. (`MTC_COMMAND_CENTER/12_PARITY_PINETS/parity_summary.md:262-268`) |
| `case_147` | `pair_htf_trend_exit` | TV/PineTS have 124 trades; Python has 126. (`MTC_COMMAND_CENTER/12_PARITY_PINETS/parity_summary.md:366-372`) |
| `case_153` | `pair_confirm_refresh` | TV/PineTS have 0 trades; Python has 146. (`MTC_COMMAND_CENTER/12_PARITY_PINETS/parity_summary.md:414-420`) |
| `case_154` | `pair_level_retest_confirm` | TV/PineTS have 27 trades; Python has 44. (`MTC_COMMAND_CENTER/12_PARITY_PINETS/parity_summary.md:422-428`) |
| `case_155` | `pair_macd_htf_regime` | TV/PineTS have 55 trades; Python has 76. (`MTC_COMMAND_CENTER/12_PARITY_PINETS/parity_summary.md:430-436`) |
| `case_162` | `pair_ma_htf_htf_trend` | TV/PineTS have 96 trades; Python has 94; the effect comparison used `case_159` because 160/161 were missing. (`MTC_COMMAND_CENTER/12_PARITY_PINETS/parity_summary.md:470-476`) |

Twenty-three additional cases have strict TradingView quantity mismatches but are classified `SOFT_PASS`: `case_103 use_candle_pattern_gate`, `104 use_level_proximity_gate`, `105 level_proximity_threshold_pct`, `106 level_proximity_lookback`, `109 time_stop_condition`, `112 use_daily_loss_limit`, `113 max_daily_loss_pct`, `114 use_max_trades_per_day`, `115 max_trades_per_day`, `126 guard_recovery_bars`, `127 guard_recovery_signals`, `128 use_trade_cooldown`, `129 cooldown_bars_after_exit`, `130 use_confirm_transform`, `132 confirm_close_crosses`, `133 require_raw_still_true`, `137 retest_buffer_pct`, `138 pair_sl_atr_be`, `139 pair_sl_atr_trail`, `140 pair_sl_atr_tp_atr`, `141 pair_sl_atr_tp_r`, `142 pair_sl_atr_tp_multi`, and `143 pair_sl_percent_tp_percent`. These are not counted among the eight unresolved corpus failures because they pass the corpus's soft quantity contract; the aggregate records 31 TV-versus-Python strict failures and 50/58 overall classifications (`MTC_COMMAND_CENTER/12_PARITY_PINETS/parity_results.json:10-17`). The corpus also records two accepted setup deviations: leverage cap 5 and an inert confirmation mismatch (`MTC_COMMAND_CENTER/12_PARITY_PINETS/parity_summary.md:482-484`).

## Corpus B — March `mtc_backtest` parity suite

Primary artifact: `MTC_COMMAND_CENTER/02_MTC_BACKTEST/parity_suite_350/PARITY_STATUS_FINAL_20260304.md`.

| Required field | Inventory result | Evidence |
|---|---|---|
| Exact Pine implementation and version | Export label `MT_CORE2`; the report later names `00_MASTER_TEMPLATE/MASTER_TEMPLATE_CORE.pine` as the Pine engine. **UNKNOWN — searched the suite, current tree, and all Git object paths; the named Pine source is absent and no generation-time Pine commit/hash is stored.** | `MTC_COMMAND_CENTER/02_MTC_BACKTEST/parity_suite_350/cases/parity_core_005_enable_long_trades_v01.json:1-9`; `MTC_COMMAND_CENTER/02_MTC_BACKTEST/parity_suite_350/PARITY_STATUS_FINAL_20260304.md:83-90` |
| Exact Python implementation and version | Implementation: `MTC_COMMAND_CENTER/02_MTC_BACKTEST/src/engine/mtc_runner.py::MTCRunner`, invoked by `scripts/run_case.py` for each case. **UNKNOWN — searched Git history and the corpus; no generation-time runner commit/hash is stored.** The first tracked imported runner blob is `a3d2e400f8ae08fef7ebb0fd5acaf5f672f3b935`, but import on 2026-05-31 does not prove the March execution version. | `MTC_COMMAND_CENTER/02_MTC_BACKTEST/parity_suite_350/scripts/run_and_compare_batch.py:40-50`; `MTC_COMMAND_CENTER/02_MTC_BACKTEST/scripts/run_case.py:23-29`; `MTC_COMMAND_CENTER/02_MTC_BACKTEST/scripts/run_case.py:348-354` |
| PineTS version | N/A — this corpus compares TradingView exports directly with `MTCRunner`; its execution and comparison call chain contains no PineTS leg. | `MTC_COMMAND_CENTER/02_MTC_BACKTEST/parity_suite_350/scripts/run_and_compare_batch.py:87-138` |
| Generation date | Report header: `2026-03-04`. **UNKNOWN — searched the report and Git history for an exact final aggregate timestamp; the file contains amendments through at least 2026-03-08 and only entered this repository in the 2026-05-31 migration.** | `MTC_COMMAND_CENTER/02_MTC_BACKTEST/parity_suite_350/PARITY_STATUS_FINAL_20260304.md:1-5`; `MTC_COMMAND_CENTER/02_MTC_BACKTEST/parity_suite_350/PARITY_STATUS_FINAL_20260304.md:83-96` |
| Data and case scope | 457 manifest cases on `BINANCE:BTCUSDT.P`, 15-minute bars, evaluation window `2025-06-30T05:15:00` to `2026-02-01T00:00:00`; case configs use `BTCUSDT_15m_20240101_20260213.parquet`, 200 warmup bars, and 365 preroll days. The manifest contains 180 core and 277 boundary rows. | `MTC_COMMAND_CENTER/02_MTC_BACKTEST/parity_suite_350/manifests/cases_manifest_all.csv:1-3`; `MTC_COMMAND_CENTER/02_MTC_BACKTEST/parity_suite_350/manifests/cases_manifest_all.csv:456-458`; `MTC_COMMAND_CENTER/02_MTC_BACKTEST/parity_suite_350/cases/parity_core_005_enable_long_trades_v01.json:1-9` |
| Oracle identity and tolerances | TradingView Strategy Report XLSX/list-of-trades output is the oracle; Python debug trades are the subject. The tracked batch/comparator snapshot's default raw “strict” requires normalized counts plus exact side, reason, entry time, and exit time, except duplicate BE exits may differ by up to 15 minutes. Although price tolerance `0.5` and quantity tolerance `1e-9` are calculated, default `strict_core=False` means price/quantity do **not** participate in that strict verdict. **UNKNOWN — searched the corpus and Git history for the exact generation-time comparator version; none is pinned.** | `MTC_COMMAND_CENTER/02_MTC_BACKTEST/parity_suite_350/scripts/run_and_compare_batch.py:87-138`; `MTC_COMMAND_CENTER/02_MTC_BACKTEST/src/parity/compare_tv_trades.py:412-420`; `MTC_COMMAND_CENTER/02_MTC_BACKTEST/src/parity/compare_tv_trades.py:428-478`; `MTC_COMMAND_CENTER/02_MTC_BACKTEST/src/parity/compare_tv_trades.py:481-507` |
| Executable / skipped / not-comparable / reuse counts | 457 total; 439 executable; 318 independently executed comparisons (`316 PASS` + `2 MISMATCH`); 121 `PASS(reuse)`; 18 `SKIP`; 0 `NOT_COMPARABLE` in the exhaustive status partition. Raw strict result 437/439 includes reuses; independently executed passes are 316. Clip-overlap view is 439/439. | `MTC_COMMAND_CENTER/02_MTC_BACKTEST/parity_suite_350/PARITY_STATUS_FINAL_20260304.md:13-31`; `MTC_COMMAND_CENTER/02_MTC_BACKTEST/parity_suite_350/PARITY_STATUS_FINAL_20260304.md:187-200` |
| `tw_*` semantic vector | **UNKNOWN — searched all 458 JSON files in the case directory and the suite scripts for `tw_*` / `tw_audit_semantics_mode`; no such vector is recorded.** This older `mtc_backtest` engine uses its own parity configuration (`fill_contract: touch`, 365-day warmup-only preroll, close-open-at-eval-start). | `MTC_COMMAND_CENTER/02_MTC_BACKTEST/parity_suite_350/cases/parity_core_005_enable_long_trades_v01.json:103-114` |

### Named unresolved mismatches

- `402 parity_bnd_211_swing_right_bars_v03`: TradingView 123 trades versus Python 236 (`MTC_COMMAND_CENTER/02_MTC_BACKTEST/parity_suite_350/PARITY_STATUS_FINAL_20260304.md:33-42`).
- `416 parity_bnd_217_dynamic_update_mode_v02`: TradingView 129 trades versus Python 189 (`MTC_COMMAND_CENTER/02_MTC_BACKTEST/parity_suite_350/PARITY_STATUS_FINAL_20260304.md:44-52`).

Both pass after overlap clipping and are tagged `TV_EARLY_TRADE_END_CANDIDATE`; the raw-count-versus-overlap policy remains unresolved (`MTC_COMMAND_CENTER/02_MTC_BACKTEST/parity_suite_350/PARITY_STATUS_FINAL_20260304.md:167-173`, `MTC_COMMAND_CENTER/02_MTC_BACKTEST/parity_suite_350/PARITY_STATUS_FINAL_20260304.md:187-200`). A later same-bar-flip fix touched both Pine and Python, but the report says the full rerun remained pending, so the aggregate cannot be treated as post-fix regression evidence (`MTC_COMMAND_CENTER/02_MTC_BACKTEST/parity_suite_350/PARITY_STATUS_FINAL_20260304.md:83-96`).

## Corpus C — factory regression suite

Expected artifact: `MTC_COMMAND_CENTER/01_MTC_PROJECT/reports/FACTORY_REGRESSION_SUITE_V1/full_current/FULL_FACTORY_SUITE_REPORT.md`.

| Required field | Inventory result | Evidence |
|---|---|---|
| Exact Pine implementation and version | **UNKNOWN — searched the expected report directory, the entire permitted worktree, migration manifest, and all Git object paths; the report and JSON are absent.** | `MTC_COMMAND_CENTER/11_TRIAGE/MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md:3509-3512`; `docs/migration_manifests/copy_manifest.csv:4938-4939` |
| Exact Python implementation and version | **UNKNOWN — searched the expected report directory, the entire permitted worktree, migration manifest, and all Git object paths; no executable report remains to identify the subject.** | `MTC_COMMAND_CENTER/11_TRIAGE/MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md:3509-3512`; `docs/migration_manifests/copy_manifest.csv:4938-4939` |
| PineTS version | **UNKNOWN — searched the expected report directory, the entire permitted worktree, migration manifest, and all Git object paths; no corpus report remains.** | `MTC_COMMAND_CENTER/11_TRIAGE/MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md:3509-3512` |
| Generation date | **UNKNOWN — searched the expected report directory, the entire permitted worktree, migration manifest, and all Git object paths; no corpus report remains.** | `MTC_COMMAND_CENTER/11_TRIAGE/MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md:3509-3512` |
| Data and case scope | **UNKNOWN — searched the expected report directory, the entire permitted worktree, migration manifest, and all Git object paths; the brief's “163 cases” statement is explicitly unverified at this commit.** | `MTC_COMMAND_CENTER/11_TRIAGE/MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md:469-472`; `MTC_COMMAND_CENTER/11_TRIAGE/MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md:3509-3512` |
| Oracle identity and tolerances | **UNKNOWN — searched the expected report directory, the entire permitted worktree, migration manifest, and all Git object paths; no oracle contract remains.** | `MTC_COMMAND_CENTER/11_TRIAGE/MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md:3509-3512` |
| Executable / skipped / not-comparable / reuse counts | **UNKNOWN — searched the expected report directory, the entire permitted worktree, migration manifest, and all Git object paths; the brief-reported 163 total / 2 pass / 0 fail / 160 `NOT_COMPARABLE` / 1 missing export is unavailable for verification and is not accepted as a corpus result.** | `MTC_COMMAND_CENTER/11_TRIAGE/MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md:469-472`; `MTC_COMMAND_CENTER/11_TRIAGE/MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md:3509-3512` |
| `tw_*` semantic vector | **UNKNOWN — searched the expected report directory, the entire permitted worktree, migration manifest, and all Git object paths; no corpus report remains.** | `MTC_COMMAND_CENTER/11_TRIAGE/MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md:3509-3512` |

The migration manifest records that a Markdown report (6,828 bytes, SHA-256 `0f87de...2570a9e7`) and JSON report (377,628 bytes, SHA-256 `574a05...a733da`) were intended for the canonical tree, but neither file is present and neither path exists in any Git ref (`docs/migration_manifests/copy_manifest.csv:4938-4939`). This is provenance of a planned copy, not recoverable result evidence.

### Named unresolved mismatch

`CORPUS_UNAVAILABLE`: the report and machine-readable JSON are missing. The alleged 160 `NOT_COMPARABLE` rows and one missing export cannot be named or audited. Corpus C remains unavailable, exactly as the brief allows WP-P0-06 to record (`MTC_COMMAND_CENTER/11_TRIAGE/MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md:3509-3512`).

## Corpus D — Bridge / QuantLens entry-signal golden

Primary artifacts: `IBKR_PAPER_BRIDGE/docs/18_GOLDEN_REPORT.md` and `IBKR_PAPER_BRIDGE/tests/fixtures/golden_signals.json`.

| Required field | Inventory result | Evidence |
|---|---|---|
| Exact Pine implementation and version | N/A — no Pine implementation participates. The oracle is the registered QuantLens Python signal function. | `IBKR_PAPER_BRIDGE/docs/18_GOLDEN_REPORT.md:14-25`; `IBKR_PAPER_BRIDGE/docs/18_GOLDEN_REPORT.md:50-58` |
| Exact Python implementation and version | Oracle: QuantLens `mega_walk_forward.py` strategy `keltner_trail_ema8`, engine version `faz3b-exit-mode-v1`; subject: `IBKR_PAPER_BRIDGE/bridge/engine/strategies/keltner_trail_ema8.py::KeltnerTrailEma8`. At fixture commit `04048a0b90650d54925feb2848d0a94e81dc05d1`, exact blobs are QuantLens `5ee830ea44c7f710c3c7d48699c4718a68fba106` and Bridge `eb55d7e4f435331012aa49aabcb41bdf63a3ba64`. | `IBKR_PAPER_BRIDGE/docs/18_GOLDEN_REPORT.md:14-25`; `IBKR_PAPER_BRIDGE/docs/18_GOLDEN_REPORT.md:40-41`; `IBKR_PAPER_BRIDGE/docs/18_GOLDEN_REPORT.md:72-81`; `IBKR_PAPER_BRIDGE/tests/fixtures/golden_signals.json:2-7` |
| PineTS version | N/A — PineTS does not participate. | `IBKR_PAPER_BRIDGE/docs/18_GOLDEN_REPORT.md:50-58`; `IBKR_PAPER_BRIDGE/tests/fixtures/golden_signals.json:2-7` |
| Generation date | `2026-07-13`; fixture commit `04048a0b90650d54925feb2848d0a94e81dc05d1` at `2026-07-13T11:25:41+03:00`. | `IBKR_PAPER_BRIDGE/docs/18_GOLDEN_REPORT.md:3-8` |
| Data and case scope | One pinned signal-replay corpus: BTCUSD 1h, 48,077 bars, `2021-01-01T06:00:00Z` through `2026-06-28T00:00:00Z`, 858 two-sided close-confirmed entry signals; run ID `QL_MEGA_KELTNER_TRAIL_EMA8_BTCUSD_1h_2026-06-28_01a3f1255e29`. | `IBKR_PAPER_BRIDGE/docs/18_GOLDEN_REPORT.md:30-44`; `IBKR_PAPER_BRIDGE/docs/18_GOLDEN_REPORT.md:60-70`; `IBKR_PAPER_BRIDGE/tests/fixtures/golden_signals.json:4-22` |
| Oracle identity and tolerances | QuantLens-derived `golden_signals.json` is the oracle. The Bridge replay must equal it exactly on `ts`, `symbol`, `direction`, `reason`, and `ref_price`; no numeric tolerance is applied. | `IBKR_PAPER_BRIDGE/docs/18_GOLDEN_REPORT.md:72-81`; `IBKR_PAPER_BRIDGE/tests/test_strategy.py:31-63` |
| Executable / skipped / not-comparable / reuse counts | 858 entry-event comparisons executed, 858 exact matches, 0 mismatches, 0 reuses, 0 skips, and 0 `NOT_COMPARABLE` within the declared entry-signal scope. These are signal events, not 858 strategy cases. Exit/lifecycle comparisons were not executed and have no count. | `IBKR_PAPER_BRIDGE/docs/18_GOLDEN_REPORT.md:72-87`; `IBKR_PAPER_BRIDGE/tests/fixtures/golden_signals.json:22-23` |
| `tw_*` semantic vector | N/A — this is not an `mtc_v2` TradingView audit and has no `tw_*` configuration surface. | `IBKR_PAPER_BRIDGE/tests/fixtures/golden_signals.json:2-22` |

### Named unresolved mismatches

None within the declared entry-signal fields: 858/858 are exact. Exit/lifecycle parity remains **outside the corpus**, not a pass: the report explicitly says the golden proves entry signals only, including after the Bridge's later SMA-to-EMA trail correction (`IBKR_PAPER_BRIDGE/docs/18_GOLDEN_REPORT.md:3-6`, `IBKR_PAPER_BRIDGE/docs/18_GOLDEN_REPORT.md:83-96`).

## Cross-corpus conclusion and remaining evidence gaps

| Question | Answer |
|---|---|
| Same Python subject in March and April? | **No.** March/Corpus B: `src.engine.mtc_runner.MTCRunner`. April/Corpus A: `mtc_v2.core.runner.Runner`. |
| Same Pine subject? | **No evidence of that, and recorded labels differ.** March files say `MT_CORE2`; April files say `MTCV2_1304`. Neither generation-time Pine source is pinned. |
| Same comparison contract? | **No.** Corpus A has strict/soft quantity and outcome thresholds across three engines. Corpus B's default strict decision is count/core-timing based and excludes price/quantity. |
| March-to-April regression established? | **No.** The published percentages compare different implementation pairs under different contracts. |
| Repository-wide parity number allowed? | **No.** The denominator, subject, oracle, tolerance, reuse policy, and covered lifecycle differ; Corpus C is unavailable and Corpus D is entry-only. |

Open evidence gaps are: generation-time Pine and Python commit/hash for A; exact A timeframe/date window and full `tw_*` vector; generation-time Pine and Python commit/hash plus final aggregate timestamp and `tw_*` vector for B; the entire Corpus C report/JSON; and exit/lifecycle parity beyond Corpus D's entry-event scope. Until those gaps are closed, every parity claim must remain corpus-qualified.
