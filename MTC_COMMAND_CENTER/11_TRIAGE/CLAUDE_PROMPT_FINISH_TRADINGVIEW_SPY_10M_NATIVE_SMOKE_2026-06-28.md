# Claude Prompt - Finish TradingView SPY 10m Native Smoke

Repo: `C:\LAB\Tradingview_LAB_CLEAN`

User context: Baris exported TradingView Chart Data CSV files for `BATS:SPY` on the `10m` timeframe. Codex credit is low; continue from the current repo state and finish the next safe step for the native US-equities-10m blocker.

## Required Read Order

Read these first, in order:

1. `AGENTS.md`
2. `MTC_COMMAND_CENTER\_AI_MEMORY\START_HERE.md`
3. `MTC_COMMAND_CENTER\_AI_MEMORY\AI_RULES.md`
4. `MTC_COMMAND_CENTER\03_QUANTLENS\_user_guide\07_BACKTEST_AND_OPTIMIZATION_RULES.md`
5. `MTC_COMMAND_CENTER\11_TRIAGE\BACKTEST_OPTIMIZATION_RUNBOOK.md`
6. `MTC_COMMAND_CENTER\04_SHARED\prompts\05_ai_workflow\08_backtest_launch.md`
7. `MTC_COMMAND_CENTER\11_TRIAGE\_tmp_native_us_equities_10m_audit_2026-06-28\WORKER_REPORT.md`
8. `MTC_COMMAND_CENTER\11_TRIAGE\NATIVE_US_EQUITIES_10M_CODEX_ASSESSMENT_2026-06-28.md`
9. `MTC_COMMAND_CENTER\_AI_MEMORY\NEXT_STEPS.md`
10. `MTC_COMMAND_CENTER\_AI_MEMORY\GLOBAL_HANDOFF.md`

## Current Known State

- The native US-equities-10m soak was blocked because there was no US equities provider/data/symbol universe.
- Baris has now supplied TradingView chart-data CSV exports for `BATS:SPY` 10m.
- Files currently present:
  - `MTC_COMMAND_CENTER\00_INBOX\USER_INTAKE\BATS_SPY, 10_99744.csv`
  - `MTC_COMMAND_CENTER\00_INBOX\USER_INTAKE\BATS_SPY, 10_d73fa.csv`
  - `MTC_COMMAND_CENTER\00_INBOX\USER_INTAKE\BATS_SPY, 10_70bb3.csv`
  - `MTC_COMMAND_CENTER\00_INBOX\USER_INTAKE\BATS_SPY, 10_9eac5.csv`
  - `MTC_COMMAND_CENTER\00_INBOX\USER_INTAKE\BATS_SPY, 10_474cc.csv`
  - `MTC_COMMAND_CENTER\00_INBOX\USER_INTAKE\BATS_SPY, 10_594c5.csv`
  - `MTC_COMMAND_CENTER\00_INBOX\USER_INTAKE\BATS_SPY, 10_6024d.csv`
  - `MTC_COMMAND_CENTER\00_INBOX\USER_INTAKE\BATS_SPY, 10_624c3.csv`
  - `MTC_COMMAND_CENTER\00_INBOX\USER_INTAKE\BATS_SPY, 10_e98c7.csv`
- Sample header seen by Codex: `time,open,high,low,close`
- The `time` column appears to be Unix epoch seconds.
- Volume is not present in the exports. Do not pretend volume exists.
- For the first smoke, Baris has effectively chosen:
  - provider/source: local TradingView CSV export
  - initial universe: `SPY`
  - timeframe: `10m`
  - session policy: infer from CSV timestamps; document whether it appears RTH-only or includes ETH
  - price adjustment: unknown from CSV; document as TradingView-exported OHLC, adjustment status unknown unless file metadata proves otherwise

## Goal

Finish the next safe step: consolidate and validate the TradingView `SPY 10m` CSV exports, then prepare a native SPY 10m data bundle/manifest and run only the smallest safe smoke if validation passes.

Do **not** jump directly to a full soak.

## Hard Safety Rails

- Do not edit Pine files.
- Do not edit `MTC_V2`.
- Do not edit parity files.
- Do not change trading logic or strategy rules.
- Do not place trades, connect broker, or touch broker/live/paper execution code.
- Do not fabricate `backtest_profile_result.json` or `top_results.json`.
- Do not claim native validation unless real SPY 10m data is validated and a smoke actually runs.
- Do not delete the original TradingView CSV exports.
- Do not use `git checkout`, `git reset`, or `git stash`.
- The working tree already has uncommitted changes from Codex/DeepSeek/Claude tasks. Preserve them.

## Work Plan

### Phase 1 - Inspect And Consolidate CSV

1. Read the CSV files from `00_INBOX\USER_INTAKE`.
2. Confirm all files have compatible columns.
3. Convert `time` from Unix seconds to UTC timestamp.
4. Concatenate all rows.
5. Sort by timestamp.
6. Drop exact duplicate timestamps, preserving one row per timestamp.
7. Produce a validation report with:
   - source files and row counts
   - total raw rows
   - total unique timestamps
   - first timestamp UTC
   - last timestamp UTC
   - count of duplicate timestamps
   - inferred bar interval distribution
   - missing 10m gaps
   - whether timestamps appear RTH-only, ETH, or mixed
   - whether bars are monotonic and numeric
   - whether any OHLC sanity failures exist, e.g. high < max(open,close), low > min(open,close)
   - whether volume is missing

Write the report to:

`MTC_COMMAND_CENTER\11_TRIAGE\TRADINGVIEW_SPY_10M_DATA_VALIDATION_2026-06-28.md`

### Phase 2 - Normalize Data If Validation Passes

If validation is acceptable:

1. Create a repo-local native data bundle under:

   `MTC_COMMAND_CENTER\03_QUANTLENS\data\native_us_equities_10m_spy_tradingview_2026-06-28\`

2. Write normalized CSV:

   `normalized\BATS_SPY_10m.csv`

3. Normalized CSV should use the fields the QuantLens runner expects:

   - `timestamp_utc`
   - `open`
   - `high`
   - `low`
   - `close`

   If existing runner code requires `volume`, add `volume` as blank or `0` only after proving the target strategy does not use volume. If you add placeholder volume, document it loudly in the validation report and manifest as `volume_source: missing_from_tradingview_export_placeholder`.

4. Write a bundle manifest:

   `manifests\dataset_manifest.json`

   It must include at least:

   - `symbol: "SPY"`
   - `source_symbol: "BATS:SPY"`
   - `exchange: "BATS"`
   - `asset_class: "US_EQUITY"`
   - `timeframe_normalized: "10m"`
   - `normalized_path: "normalized/BATS_SPY_10m.csv"`
   - `ohlcv_validation_status: "PASS"` only if validation truly passed
   - `provider: "tradingview_chart_data_export"`
   - `is_24_7: false`
   - `first_timestamp_utc`
   - `last_timestamp_utc`
   - `bar_count`
   - `volume_available: false` unless volume exists
   - `adjustment_policy: "unknown_tradingview_export"` unless proven otherwise
   - `session_policy_inferred`

5. Do not overwrite existing data unless the new output path is unique.

### Phase 3 - Smoke Only If Safe

If and only if:

- CSV validation passes,
- manifest is valid enough for `mega_walk_forward.py`,
- bar count satisfies the repo minimum after filtering,
- and no protected-scope edits are needed,

then run the smallest smoke:

```powershell
$env:MEGA_BUNDLE_MANIFEST = "C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\03_QUANTLENS\data\native_us_equities_10m_spy_tradingview_2026-06-28\manifests\dataset_manifest.json"
$env:MEGA_WORKERS = "1"
python MTC_COMMAND_CENTER\03_QUANTLENS\tools\mega_walk_forward.py --strategy QL_2026-05-01_US_EQUITIES_10M_8EMA_PULLBACK --symbol SPY --tf 10m
```

If the smoke command needs an output directory override and the runner does not support one, do not hack engine logic. Use the existing runner behavior and document output location. If running the smoke would create large/uncontrolled outputs, stop and write the exact command Baris should approve.

If smoke runs, classify the result as **SMOKE ONLY / NOT PROMOTABLE**. It does not satisfy full Gate 2 promotion requirements.

### Phase 4 - Do Not Generate Native Profile Artifact Yet Unless Evidence Exists

Only generate `backtest_profile_result.json` if the smoke produces real usable result rows with the exact target:

- strategy: `QL_2026-05-01_US_EQUITIES_10M_8EMA_PULLBACK`
- symbol: `SPY`
- timeframe: `10m`
- data source: TradingView CSV normalized bundle

Even then, mark it as `SMOKE_ONLY` / `RESEARCH_ONLY` unless full Gate 2 validation is run.

Do not generate `top_results.json` from a one-symbol one-row smoke. It requires a real same-bucket multi-row result set.

## Expected Outputs

At minimum:

1. `MTC_COMMAND_CENTER\11_TRIAGE\TRADINGVIEW_SPY_10M_DATA_VALIDATION_2026-06-28.md`
2. If validation passes:
   - `MTC_COMMAND_CENTER\03_QUANTLENS\data\native_us_equities_10m_spy_tradingview_2026-06-28\normalized\BATS_SPY_10m.csv`
   - `MTC_COMMAND_CENTER\03_QUANTLENS\data\native_us_equities_10m_spy_tradingview_2026-06-28\manifests\dataset_manifest.json`
3. If smoke runs:
   - exact output path(s) from the smoke
   - a short smoke report:
     `MTC_COMMAND_CENTER\11_TRIAGE\SPY_10M_NATIVE_SMOKE_REPORT_2026-06-28.md`

Always update:

- `MTC_COMMAND_CENTER\_AI_MEMORY\GLOBAL_HANDOFF.md`
- `MTC_COMMAND_CENTER\_AI_MEMORY\NEXT_STEPS.md`
- `MTC_COMMAND_CENTER\_AI_MEMORY\SESSION_LOG.md`

Use `## Claude Opus 4.8 2026-06-28 — ...` section headers in `GLOBAL_HANDOFF.md`.

## Acceptance Criteria

The task is complete when one of these is true:

### Success Path

- TradingView CSVs are consolidated and validated.
- A normalized SPY 10m bundle + manifest exists.
- A one-symbol SPY 10m smoke either ran successfully or the exact safe command is prepared.
- All outputs are explicitly labeled `SMOKE ONLY / NOT PROMOTABLE`.
- No fake native artifact or `top_results.json` is created.

### Blocked Path

- Validation proves the TradingView export is unusable, insufficient, duplicated beyond repair, missing required OHLC fields, or too short.
- You write a clear report explaining exactly what Baris must re-export.
- No smoke or artifact generation is attempted.

## Final Response To Baris

Keep it short:

- say whether CSV validation passed
- say whether a normalized bundle was created
- say whether smoke ran
- list report paths
- list the next required human decision if blocked

