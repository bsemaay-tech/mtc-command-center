# WP-P0-06 Search Log

Date: 2026-08-24
Worktree: `C:\WPP006_20260824`
Branch: `feature/wp-p0-06-parity-corpus-20260824`

All commands were read-only unless explicitly identified as creating the three lane deliverables. No parity corpus, Pine file, Python implementation, test, fixture, report, or generated result was modified or regenerated. No external network, host, WSL, Docker, broker, exchange, testnet, live-trading, AI CLI, or subagent command was used.

## 1. Gate and repository checks

```powershell
git status --short
git branch --show-current
git rev-parse HEAD
git rev-parse origin/master
codeburn status
```

Observed: clean worktree; expected lane branch; `HEAD == origin/master == fbb05d7f46bc78b2875aa6d029e7fb2f2a8b14d7` before lane edits.

The lane prompt was read in full from `C:\tmp\LANE_PROMPTS_20260824\LANE_C_WP_P0_06.md`. Repository onboarding and rules were then read from the isolated worktree, beginning with `AGENTS.md` and `MTC_COMMAND_CENTER/_AI_MEMORY/START_HERE.md`.

One combined numbered-read command initially used incorrect prefixes for the brief and Bridge files; it still returned the requested Corpus B extracts, reported `Get-Content` path errors for the other inputs, and made no changes. `rg --files` then located the correct paths (`MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md` and root-level `IBKR_PAPER_BRIDGE/...`), which were read successfully in the next command.

## 2. Brief-first discovery

```powershell
rg -n "F-7|Corpus A|Corpus B|Corpus C|Corpus D|Parity Corpus Inventory|FULL_FACTORY_SUITE_REPORT" MTC_COMMAND_CENTER/11_TRIAGE/MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md
Get-Content ...MASTER_ARCHITECTURE_AND_IMPLEMENTATION_BRIEF_2026-08-21.md  # numbered extracts 438-497 and 3505-3513
```

The sweep used the four paths in brief section F-7 and the explicit Appendix F availability warning as its starting set.

## 3. Corpus A sweep

```powershell
Get-Content MTC_COMMAND_CENTER/12_PARITY_PINETS/parity_summary.md
Get-Content MTC_COMMAND_CENTER/12_PARITY_PINETS/parity_results.json
Get-Content MTC_COMMAND_CENTER/12_PARITY_PINETS/manual_tw_futures_audit.py
Get-Content MTC_COMMAND_CENTER/02_MTC_BACKTEST/parity_compare.py
Get-Content MTC_COMMAND_CENTER/02_MTC_BACKTEST/mtc_bridge.mjs
Get-Content MTC_COMMAND_CENTER/01_MTC_PROJECT/01_PINE/MTC_V2.pine
rg -n "BTCUSDT|timeframe|date_from|date_to|start_date|end_date|tw_audit_semantics_mode" <Corpus-A aggregate, plans, and audit script>
rg --files MTC_COMMAND_CENTER/12_PARITY_PINETS | rg "case_(103|162)|plan|manifest"
```

PowerShell parsed `parity_results.json` to count all 58 rows, aggregate each pairwise strict flag, list all 31 rows with any strict mismatch, distinguish the 23 `SOFT_PASS` rows from the eight `FAIL` rows, and verify that every workbook filename uses the `MTCV2_1304` label. The two endpoint case plans were line-inspected, and all `case_103`-`case_162` plans were searched for retained dataset/window metadata.

Git provenance checks:

```powershell
git log --all --follow --format='%H|%aI|%s' -- MTC_COMMAND_CENTER/12_PARITY_PINETS/parity_results.json
git ls-tree 77a10e6573d93f8aaf777010ea507bbec0a7668b <A artifact and implementation paths>
```

First tracked import was `77a10e6573d93f8aaf777010ea507bbec0a7668b` on 2026-05-31. Import-time blobs found: Pine `96cb361e...`, audit `b251e3ea...`, results `90373143...`, bridge `ce3bb456...`, comparator `9560195b...`. These were recorded only as imported snapshots, not asserted as 2026-04-14 execution versions.

## 4. Corpus B sweep

```powershell
Get-Content MTC_COMMAND_CENTER/02_MTC_BACKTEST/parity_suite_350/PARITY_STATUS_FINAL_20260304.md
Get-Content MTC_COMMAND_CENTER/02_MTC_BACKTEST/parity_suite_350/CURRENT_STATUS_HANDOFF_20260304.md
Get-Content MTC_COMMAND_CENTER/02_MTC_BACKTEST/parity_suite_350/scripts/run_and_compare_batch.py
Get-Content MTC_COMMAND_CENTER/02_MTC_BACKTEST/scripts/run_case.py
Get-Content MTC_COMMAND_CENTER/02_MTC_BACKTEST/src/parity/compare_tv_trades.py
Get-Content MTC_COMMAND_CENTER/02_MTC_BACKTEST/parity_suite_350/manifests/cases_manifest_all.csv
Get-Content MTC_COMMAND_CENTER/02_MTC_BACKTEST/parity_suite_350/cases/parity_core_005_enable_long_trades_v01.json
rg -n "MASTER_TEMPLATE_CORE|MT_CORE2|MTCRunner|build_report|strict_core|PASS\(reuse\)|MISMATCH|SKIP" MTC_COMMAND_CENTER/02_MTC_BACKTEST/parity_suite_350 MTC_COMMAND_CENTER/02_MTC_BACKTEST/scripts MTC_COMMAND_CENTER/02_MTC_BACKTEST/src
```

PowerShell parsed all 457 manifest rows and verified one symbol (`BINANCE:BTCUSDT.P`), one timeframe (`15`), one start/end window, 180 core rows, 277 boundary rows, 456 `NORMAL` cases, and one `ZERO_TRADE_EXPECTED` case. It also searched all 458 JSON files present in the case directory for `tw_*` fields; none were found. The canonical manifest, not the extra debug JSON, defines the 457-case scope.

Git provenance and missing-Pine checks:

```powershell
git log --all --follow --format='%H|%aI|%s' -- MTC_COMMAND_CENTER/02_MTC_BACKTEST/parity_suite_350/PARITY_STATUS_FINAL_20260304.md
git ls-tree 77a10e6573d93f8aaf777010ea507bbec0a7668b <B report, runner, comparator, and batch paths>
git rev-list --all --objects | rg 'MASTER_TEMPLATE_CORE\.pine$'
```

No `MASTER_TEMPLATE_CORE.pine` path was found in any Git object. First tracked import was 2026-05-31. Import-time blobs found: report `6fc4ab24...`, batch `06549d05...`, runner `a3d2e400...`, comparator `a82537f3...`; these do not prove the March execution versions.

## 5. Corpus C sweep

```powershell
Test-Path MTC_COMMAND_CENTER/01_MTC_PROJECT/reports/FACTORY_REGRESSION_SUITE_V1/full_current/FULL_FACTORY_SUITE_REPORT.md
Test-Path MTC_COMMAND_CENTER/01_MTC_PROJECT/reports/FACTORY_REGRESSION_SUITE_V1/full_current/FULL_FACTORY_SUITE_REPORT.json
rg --files | rg 'FULL_FACTORY_SUITE_REPORT|FACTORY_REGRESSION_SUITE_V1'
rg -n 'FULL_FACTORY_SUITE_REPORT|FACTORY_REGRESSION_SUITE_V1' docs/migration_manifests/copy_manifest.csv MTC_COMMAND_CENTER
git log --all --full-history -- <expected Markdown and JSON paths>
git rev-list --all --objects | rg 'FULL_FACTORY_SUITE_REPORT\.(md|json)$'
```

Both expected files returned false. No matching Git object exists. The migration manifest contains the intended target rows and hashes, but target files are absent. A metadata-only parse of manifest rows under `FACTORY_REGRESSION_SUITE_V1/full_current` found 747 intended copied files across 161 case directories plus top-level reports; it was not used to reconstruct or validate the missing result counts.

The frozen legacy repository named in migration source paths was not read.

## 6. Corpus D sweep

```powershell
Get-Content IBKR_PAPER_BRIDGE/docs/18_GOLDEN_REPORT.md
Get-Content IBKR_PAPER_BRIDGE/tests/fixtures/golden_signals.json
Get-Content IBKR_PAPER_BRIDGE/tests/test_strategy.py
Get-Content IBKR_PAPER_BRIDGE/tests/test_golden_generation.py
Get-Content IBKR_PAPER_BRIDGE/tools/generate_golden.py
Get-Content IBKR_PAPER_BRIDGE/bridge/engine/strategies/keltner_trail_ema8.py
git log --all --follow --format='%H|%aI|%s' -- IBKR_PAPER_BRIDGE/tests/fixtures/golden_signals.json
git ls-tree 04048a0b90650d54925feb2848d0a94e81dc05d1 <golden implementation and artifact paths>
```

The exact fixture commit was `04048a0b90650d54925feb2848d0a94e81dc05d1` (2026-07-13T11:25:41+03:00). Its relevant blobs were Bridge strategy `eb55d7e4...`, fixture `31bdafae...`, equality test `8d64f91e...`, generator `ceb4e511...`, and QuantLens engine `5ee830ea...`.

## 7. Negative-scope and integrity checks

No backtest, parity harness, test suite, fixture generator, Pine command, network command, or live-system command was run. Existing XLSX files were not opened or converted because the lane permits writes only under its new documentation directory and the repository's binary-ingest workflow would create derived files. Their filenames and already-extracted tracked JSON/Markdown metadata were used instead.

Before commit, the following checks are required and recorded in `LANE_REPORT.md`:

```powershell
git status --short
git diff --check
git diff --name-only
git diff -- <three exact lane files>
git add -- <three exact lane files>
git diff --cached --name-only
git diff --cached --check
```
