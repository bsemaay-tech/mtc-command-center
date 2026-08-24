# WP-P0-03 migration ledger verification

## Result

**PASS — implementer self-QA.** The generated ledger contains one immutable initial row
for every Tier-A `CANONICAL` path, resolves the sampled paths in both directions, and is
byte-reproducible from Git objects at commit
`88eab9c93b7c285b990d07502ea1ec476034e8d5` (`88eab9c9`). No file was moved.

## Exact build command

Run from repository root `C:\WPP003_20260825`:

```powershell
python MTC_COMMAND_CENTER\11_TRIAGE\WP_P0_03_MIGRATION_LEDGER_2026-08-25\build_migration_ledger.py
```

Actual output:

```text
BUILD PASS output=C:\WPP003_20260825\MTC_COMMAND_CENTER\MIGRATION_LEDGER.json rows=2641 sha256=89740bcb59771b332d284e2acc7b19078f068767ed2233675173b144c8c3faeb
```

The script executes these read-only Git-object operations internally:

```text
git -C C:\WPP003_20260825 ls-tree -r -l -z --full-tree 88eab9c93b7c285b990d07502ea1ec476034e8d5
git -C C:\WPP003_20260825 cat-file --batch
```

The accepted classification CSV, freeze-tag manifest, and all 2,641 file payloads are
read as blobs from the pinned tree. Worktree bytes are not used for ledger hashes.

## Row-count equality and complete-content check

Exact command:

```powershell
python MTC_COMMAND_CENTER\11_TRIAGE\WP_P0_03_MIGRATION_LEDGER_2026-08-25\build_migration_ledger.py --check MTC_COMMAND_CENTER\MIGRATION_LEDGER.json --sample-size 20
```

The check regenerates the complete expected serialization from the pinned Git tree and
requires byte equality before it evaluates samples. Summary output:

```text
VERIFY PASS inventory_canonical=2641 ledger_rows=2641 unique_old_paths=2641
BYTE_IDENTITY PASS ledger_sha256=89740bcb59771b332d284e2acc7b19078f068767ed2233675173b144c8c3faeb
BIDIRECTIONAL_SAMPLE PASS sample_size=20 old_to_row_to_old=20 effective_location_to_row_to_old=20 null_self_resolutions=20
SIMULATED_FUTURE PASS old="__WP_P0_03_SIMULATION__/old/location.txt" new="__WP_P0_03_SIMULATION__/future/location.txt" old_lookup_entry_id=2642 new_lookup_entry_id=2642 both_return_old="__WP_P0_03_SIMULATION__/old/location.txt"
```

Count comparison:

| Measure | Count |
|---|---:|
| Tier-A `CANONICAL` rows in the accepted inventory | 2,641 |
| Rows in `MIGRATION_LEDGER.json` | 2,641 |
| Unique ledger `old_path` values | 2,641 |
| Initial `NOT_MIGRATED` rows | 2,641 |
| Initial rows with `new_location: null` | 2,641 |

## Bidirectional sampled resolution

The verifier deterministically selects 20 evenly spaced entry indices, resolves
`old_path -> row -> effective location`, then resolves
`effective location -> row -> old_path`. For an initial null `new_location`, the
effective location is the unchanged `old_path`, as defined by the ledger header.

| Entry | `old_path` / effective location | Forward row | Reverse result |
|---:|---|---:|---|
| 1 | `.chatgpt-instructions.md` | 1 | `.chatgpt-instructions.md` |
| 140 | `IBKR_PAPER_BRIDGE/tests/test_partial_fill_protection.py` | 140 | same `old_path` |
| 279 | `MTC_COMMAND_CENTER/01_MTC_PROJECT/docs/PORTABLE_HANDOFF_PACKAGE_SCOPE.md` | 279 | same `old_path` |
| 418 | `MTC_COMMAND_CENTER/02_MTC_BACKTEST/_AI_MEMORY/DECISIONS.md` | 418 | same `old_path` |
| 557 | `MTC_COMMAND_CENTER/02_MTC_BACKTEST/configs/cases/history_sweeps_60d0b_q15/case_20250629_2030.json` | 557 | same `old_path` |
| 696 | `MTC_COMMAND_CENTER/02_MTC_BACKTEST/configs/cases/supertrend_be_wf_target2_20260309.json` | 696 | same `old_path` |
| 835 | `MTC_COMMAND_CENTER/02_MTC_BACKTEST/data/history_sweeps_60d0b_hourly/20250630_0000.parquet` | 835 | same `old_path` |
| 974 | `MTC_COMMAND_CENTER/02_MTC_BACKTEST/scripts/compare_tv_web_trades.py` | 974 | same `old_path` |
| 1113 | `MTC_COMMAND_CENTER/02_MTC_BACKTEST/tests/test_optimizer_migration_script.py` | 1113 | same `old_path` |
| 1252 | `MTC_COMMAND_CENTER/03_QUANTLENS/00_INBOX_REPORTS/Transcrips/259% Return in 1 Year The Risk Management Strategy YOU Need for Consistent Returns.md` | 1252 | same `old_path` |
| 1390 | `MTC_COMMAND_CENTER/03_QUANTLENS/11_TRADER_WIKI/2026_05_04_restart_import/README.md` | 1390 | same `old_path` |
| 1529 | `MTC_COMMAND_CENTER/03_QUANTLENS/strategies/STG002_ql_alpha_link_8ema_1h/README.md` | 1529 | same `old_path` |
| 1668 | `MTC_COMMAND_CENTER/03_QUANTLENS/strategies/STG027_05_bigbeluga_rsi_choch_atr/SPEC.md` | 1668 | same `old_path` |
| 1807 | `MTC_COMMAND_CENTER/03_QUANTLENS/strategies/STG040_ql_2026_05_01_swing_1h_dual_rsi_60_40_pullback/04_experiment_plan.md` | 1807 | same `old_path` |
| 1946 | `MTC_COMMAND_CENTER/03_QUANTLENS/strategies/STG056_oliver_kell_price_cycle/producer_spec.json` | 1946 | same `old_path` |
| 2085 | `MTC_COMMAND_CENTER/03_QUANTLENS/tools/night_runs/night_2026-06-03/MEGA_results_iter_15_20260604_034151.json` | 2085 | same `old_path` |
| 2224 | `MTC_COMMAND_CENTER/03_QUANTLENS/tools/score_gate2.py` | 2224 | same `old_path` |
| 2363 | `MTC_COMMAND_CENTER/04_SHARED/prompts/02_youtube_strategy/07_development_prompt_5_double_check_behavior_after_feature_integration_vs_code.md` | 2363 | same `old_path` |
| 2502 | `MTC_COMMAND_CENTER/09_DOCS/ADR/ADR-0001-command-dash-as-reference.md` | 2502 | same `old_path` |
| 2641 | `verify_migration.ps1` | 2641 | `verify_migration.ps1` |

The separate simulated future row has `old_path` and a distinct non-null
`new_location`. Both keys resolve to entry 2,642 and return the same old path. The row is
created only in memory by the verifier and is not written to the ledger.

## Reproducibility

Two independent output paths were generated with the same command shape:

```powershell
python MTC_COMMAND_CENTER\11_TRIAGE\WP_P0_03_MIGRATION_LEDGER_2026-08-25\build_migration_ledger.py --output MTC_COMMAND_CENTER\11_TRIAGE\WP_P0_03_MIGRATION_LEDGER_2026-08-25\repro_run_a.json
python MTC_COMMAND_CENTER\11_TRIAGE\WP_P0_03_MIGRATION_LEDGER_2026-08-25\build_migration_ledger.py --output MTC_COMMAND_CENTER\11_TRIAGE\WP_P0_03_MIGRATION_LEDGER_2026-08-25\repro_run_b.json
Get-FileHash -Algorithm SHA256 MTC_COMMAND_CENTER\11_TRIAGE\WP_P0_03_MIGRATION_LEDGER_2026-08-25\repro_run_*.json
```

Actual result:

```text
RUN_A_SHA256=89740bcb59771b332d284e2acc7b19078f068767ed2233675173b144c8c3faeb
RUN_B_SHA256=89740bcb59771b332d284e2acc7b19078f068767ed2233675173b144c8c3faeb
RUN_A_BYTES=761472
RUN_B_BYTES=761472
BYTE_IDENTICAL=True
```

The two temporary ledgers were removed after the comparison. The committed ledger is
UTF-8 without BOM, contains LF line endings only (`CR_BYTES=0`), and has the same SHA-256.

## Falsification arm

The verifier was pointed at the generator source instead of a ledger. This deliberately
wrong artifact returned exit code 1:

```powershell
python MTC_COMMAND_CENTER\11_TRIAGE\WP_P0_03_MIGRATION_LEDGER_2026-08-25\build_migration_ledger.py --check MTC_COMMAND_CENTER\11_TRIAGE\WP_P0_03_MIGRATION_LEDGER_2026-08-25\build_migration_ledger.py
```

```text
BUILD BLOCKED: ledger is not byte-identical to regenerated output: C:\WPP003_20260825\MTC_COMMAND_CENTER\11_TRIAGE\WP_P0_03_MIGRATION_LEDGER_2026-08-25\build_migration_ledger.py
RED_RC=1
```

This proves the published complete-content check does not accept arbitrary bytes.
