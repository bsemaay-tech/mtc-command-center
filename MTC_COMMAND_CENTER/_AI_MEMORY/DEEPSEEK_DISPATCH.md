# DeepSeek Dispatch Prompts

Generated: 2026-06-06 by Codex GPT-5. These are copy-paste prompts for read-only or bounded review. Do not send secrets. Do not authorize live trading, broker actions, Pine edits, parity edits, or promotion decisions.

## Task 1 - Strategy Family Mapping Audit

Context: `strat_extra_runner.py` added `QL_OLIVER_KELL_PRICE_CYCLE`, `QL_LBR_COIL_BREAKOUT_RANGE_EXPANSION`, and family templates `QL_FAM_PULLBACK_TO_MA`, `QL_FAM_CONSOLIDATION_BREAKOUT`, `QL_FAM_MOMENTUM_CONTINUATION`. B2 now parks STG047/STG054/STG055 because they require equity gap/session/float/halt data.

Files to inspect:
- `MTC_COMMAND_CENTER/03_QUANTLENS/tools/strat_extra_runner.py`
- `MTC_COMMAND_CENTER/_AI_MEMORY/PIPELINE_STATE.md`
- `MTC_COMMAND_CENTER/_AI_MEMORY/A3_GAP_MATRIX.md`
- `MTC_COMMAND_CENTER/03_QUANTLENS/strategies/STG047_brian_lee_smallcap_gap_mr_short/07_deterministic_spec.md`
- `MTC_COMMAND_CENTER/03_QUANTLENS/strategies/STG054_fishhook_ep_day1_retake/07_deterministic_spec.md`
- `MTC_COMMAND_CENTER/03_QUANTLENS/strategies/STG055_gon_lowfloat_momentum_daytrading/07_deterministic_spec.md`

Expected output:
| Family / strategy | Covered correctly | Partially covered | Not covered | Overgeneralization risk | Missing family | Recommended correction |

Be skeptical. Read-only. Do not make code changes unless explicitly asked.

## Task 2 - No-Lookahead / Anti-Repaint Review

Context: Extra-runner strategies must use closed-bar/shifted logic and must not leak future high/low/channel data.

Files to inspect:
- `MTC_COMMAND_CENTER/03_QUANTLENS/tools/strat_extra_runner.py`
- `MTC_COMMAND_CENTER/03_QUANTLENS/tools/mega_walk_forward.py`
- `MTC_COMMAND_CENTER/03_QUANTLENS/tools/cpcv_validator.py`

Check for:
- lookahead leakage
- shift errors
- same-bar entry/exit ambiguity
- future candles in rolling highs/lows
- rolling-window misuse
- CPCV compatibility
- degenerate signal risk

Expected output:
| Finding | Severity | File/line | Evidence | Recommended fix |

Read-only. Do not edit. No promotion decisions.

## Task 3 - Gate3 Dry-Run Adapter Review

Context: C3 added a dry-run-only LiveOps adapter. It proves alert/state/fail-safe behavior and raises Gate3 from 46 to 91, but Gate3 stays INCOMPLETE because MTC risk compatibility and backtest-to-live matching remain non-OK.

Files to inspect:
- `MTC_COMMAND_CENTER/07_ADAPTERS/liveops/dry_run_adapter.py`
- `MTC_COMMAND_CENTER/07_ADAPTERS/liveops/tests/test_dry_run_adapter.py`
- `MTC_COMMAND_CENTER/07_ADAPTERS/liveops/README.md`
- `MTC_COMMAND_CENTER/03_STATUS/LIVEOPS_STATUS.json`
- `MTC_COMMAND_CENTER/03_STATUS/dry_run_evidence_2026-06-06/readiness_artifacts/`
- `MTC_COMMAND_CENTER/06_SCHEMAS/production_readiness_artifact_v1.schema.json`

Check for:
- accidental live execution path
- unsafe defaults
- missing fail-safe
- disabled-trading guard weakness
- payload schema weakness
- state-machine gaps
- evidence inflation risk

Expected output:
| Finding | Severity | Evidence | Why it matters | Fix |

Read-only. Do not mark Gate3 complete. Do not promote.

## Task 4 - Documentation Cleanup Review

Context: Closure docs were updated after C3/B2/A3.

Files to inspect:
- `MTC_COMMAND_CENTER/_AI_MEMORY/PIPELINE_STATE.md`
- `MTC_COMMAND_CENTER/_AI_MEMORY/FORWARD_PAPER_QUEUE.md`
- `MTC_COMMAND_CENTER/_AI_MEMORY/A3_GAP_MATRIX.md`
- `MTC_COMMAND_CENTER/_AI_MEMORY/SESSION_LOG.md`
- `MTC_COMMAND_CENTER/_AI_MEMORY/NIGHT_BATCHES.md`
- `MTC_COMMAND_CENTER/_AI_MEMORY/GLOBAL_HANDOFF.md`
- `MTC_COMMAND_CENTER/_AI_MEMORY/NEXT_STEPS.md`

Expected output:
| File | Inconsistency/stale claim | Evidence | Suggested wording |

Read-only. Be skeptical about any claim that implies live readiness.

## Task 5 - Skeptical MOMENTUM_CONTINUATION 4h Review

Context: `MOMENTUM_CONTINUATION` 4h is the best current forward-paper cohort, not a promotion candidate. Key cells include TRX 4h DSR 0.492 CPCV 15/15, LINK 4h DSR 0.403 CPCV 15/15, BTC 4h CPCV 13/15. Gate3 remains incomplete.

Files to inspect:
- `MTC_COMMAND_CENTER/_AI_MEMORY/FORWARD_PAPER_QUEUE.md`
- `MTC_COMMAND_CENTER/03_QUANTLENS/05_BACKTEST_RESULTS/fam_templates_2026-06-06/HEAVY_TIER_MORNING_REPORT.md`
- `MTC_COMMAND_CENTER/03_QUANTLENS/05_BACKTEST_RESULTS/fam_templates_2026-06-06/scorecard_v2/`
- `MTC_COMMAND_CENTER/03_STATUS/dry_run_evidence_2026-06-06/scorecard_v2_clean/`

Questions:
- Is DSR 0.492 meaningful or near-threshold noise?
- Does cross-symbol CPCV robustness justify forward-paper observation only?
- What would falsify the candidate?
- What metrics should be monitored during forward-paper?
- What must prevent promotion?

Expected output:
| Claim challenged | Evidence for | Evidence against | Falsification rule | Recommendation |

Read-only. Do not recommend live trading.

## Task 6 - MEV QuantLens Producer Review

Context: Codex wired `QL_FAM_MOMENTUM_CONTINUATION` as a raw Python producer for MEV, added a standalone PineTS adapter, and ran exact same-data producer parity on TRXUSDT 4h. Parity is now PASS, performance was poor under MTC risk, and Gate3 remains INCOMPLETE because reverse/re-entry/cooldown lifecycle mapping tests are not clean.

Files to inspect:
- `MTC_COMMAND_CENTER/02_MTC_BACKTEST/src/modules/signals/producers/quantlens_momentum_continuation_producer.py`
- `MTC_COMMAND_CENTER/02_MTC_BACKTEST/src/modules/signals/producers/__init__.py`
- `MTC_COMMAND_CENTER/02_MTC_BACKTEST/tests/test_producer_adapter.py`
- `MTC_COMMAND_CENTER/02_MTC_BACKTEST/configs/producer_params/ql_fam_momentum_continuation_trx_4h.json`
- `MTC_COMMAND_CENTER/02_MTC_BACKTEST/results/mtc_engine_validation_runs/ql_fam_momentum_continuation_trx_4h_2026-06-06/results.json`
- `MTC_COMMAND_CENTER/01_MTC_PROJECT/parity_oracles/feature_adapters/pinets/producer_ql_fam_momentum_continuation_v1.pine`
- `MTC_COMMAND_CENTER/02_MTC_BACKTEST/tools/parity/run_quantlens_producer_parity.py`
- `MTC_COMMAND_CENTER/02_MTC_BACKTEST/results/producer_parity/ql_fam_momentum_continuation_trx_4h_2026-06-06_bridge/parity_compare.json`
- `MTC_COMMAND_CENTER/02_MTC_BACKTEST/results/mtc_engine_validation_runs/ql_fam_momentum_continuation_trx_4h_parity_csv_2026-06-06/parity_compare.json`
- `MTC_COMMAND_CENTER/03_STATUS/producer_parity_2026-06-06/readiness_artifacts/QL_FAM_MOMENTUM_CONTINUATION__TRXUSDT__4h.readiness.json`
- `MTC_COMMAND_CENTER/03_STATUS/producer_parity_2026-06-06/reverse_reentry_cooldown_mapping.md`

Check for:
- accidental exit/risk/lifecycle logic embedded in the producer
- mismatches versus `_signals_momentum_continuation`
- lookahead leakage in `chan_hi` or momentum logic
- evidence inflation in the readiness artifact
- any claim that poor MTC performance is promotion evidence
- whether lifecycle test failures correctly block Gate3 pass

Expected output:
| Finding | Severity | Evidence | Why it matters | Recommended fix |

Read-only. Do not edit Pine/parity/MTC_V2. Do not promote.
