# Parity Suite 350 - Restart Execution Plan

## Phase 0 - Baseline Freeze (Hard Gate)
- Purpose: lock a single reference baseline before any generation.
- Required baseline record:
  - `baseline_case_id`
  - TV XLSX source: `MT_CORE2_BINANCE_BTCUSDT.P_2026-02-25_afc89_FILLED_v6.xlsx`
  - Source folder: `mtc_backtest/parity_suite_340/tv_manual_inputs/TW Ekran goruntusu/`
  - Symbol: `BINANCE:BTCUSDT.P`
  - Timeframe: `15 minutes`
  - Trading range: `Jun 30, 2025 06:15 -> Feb 01, 2026 00:00`
  - Backtesting range: `Jun 30, 2025 01:00 -> Feb 01, 2026 00:00`
  - Python commit hash
  - Frozen case JSON snapshot
- Gate: Phase 1 cannot start until all fields above are written.

## Phase 1 - Dependency Graph + Rules Contract
- Build full parent-child dependency graph from:
  - TV `Properties` keys
  - `mtc_backtest/src/config/defaults.py`
  - `mtc_backtest/src/engine/mtc_runner.py`
- Define `case_rules.json` contract for generator.
- Include `exclude_when` rules for incompatible settings (example: time-stop/timeframe mismatch).

`case_rules.json` minimal schema:
```json
{
  "param_id": "use_time_stop",
  "ui_key": "Use Time Stop (Position Duration Exit)",
  "testable": true,
  "active_when": null,
  "children": ["time_stop_bars", "time_stop_eod", "time_stop_eow", "time_stop_condition"],
  "exclude_when": ["timeframe_not_compatible"],
  "notes": ""
}
```

`canonical_config_hash` algorithm:
1. Keep only active (behavioral) params.
2. Remove parent-off child params.
3. Normalize to sorted canonical JSON.
4. Compute `sha256(canonical_json)`.
5. Use together with `semantic_fingerprint` to dedupe.

## Phase 2 - Case Generation (No Duplicate, No Inert)
- Packages: `core`, `boundary`, `pairwise`.
- Fixed case counts are not mandatory.
- Coverage rule:
  - every testable UI input must be varied at least once
  - non-UI / code-embedded settings are excluded
  - Python-runner internal toggles are excluded
  - no inert case
  - no baseline-equivalent case
  - no semantically duplicate case
- Pairwise sampling (if needed) must be deterministic:
  - `RANDOM_SEED=42`
- Outputs:
  - `cases/*.json`
  - `manifests/cases_manifest_all.csv`
  - `manifests/cases_manifest_core.csv`
  - `manifests/cases_manifest_boundary.csv`
  - `manifests/cases_manifest_pairwise.csv`
  - `manifests/coverage_report.csv`

## Phase 3 - TV XLSX Collection and Auto Routing
- Build user-friendly tracker:
  - `CASE_SETUP_GUIDE.xlsx` generated from manifest by `scripts/build_case_setup_guide.py`.
  - This file is the human-facing tracker for:
    - UI changes per case
    - XLSX download status
    - setup parity check status
    - compare status
- User drops all TV files into `tv_manual_inputs/raw_tv_exports/`.
- `scripts/route_tv_xlsx.py`:
  - parses `Properties`
  - matches against manifest expectations
  - moves matched files to `tv_manual_inputs/{run_order}_{case_id}/`
  - moves unmatched files to `tv_manual_inputs/unmatched/`
  - updates `CASE_SETUP_GUIDE.xlsx` tracker columns for routed files
- Outputs:
  - `manifests/tv_collection_status.csv`
  - `manifests/tv_unmatched.csv`

## Phase 4 - Python Batch Run
- Run order: `core -> boundary -> pairwise`.
- Case outputs:
  - `metrics.json`
  - `trades.csv`
  - `signals.csv` (optional)
- Resilience:
  - continue on case-level failures
  - circuit breaker: stop batch after 5 consecutive case exceptions

## Phase 5 - TV vs Python Comparison
- Mandatory sequence:
  1. setup parity (`Properties` vs expected inputs)
  2. exact trade count
  3. trade-level matching
  4. aggregate metrics
- Default tolerances:
  - `time_tolerance_bars = 0`
  - `price_tolerance = 0.01 * mintick`
  - aggregate metrics exact by default (`0` tolerance unless case-specific override exists)
- `NO_TRADE_EXPECTED_PASS`:
  - only when case declares `expected_trade_behavior=ZERO_TRADE_EXPECTED`
  - TV trades = 0 and Python trades = 0

## Phase 6 - Mismatch Triage
- Single taxonomy only:
  - `SETUP`, `DEPENDENCY_MODEL`, `MISSING_TRADES`, `EXTRA_TRADES`,
    `TIMING`, `PRICE_PNL`, `EXIT_REASON`, `UNKNOWN`
- Outputs:
  - `triage/mismatch_bucket_board.csv`
  - `triage/top_root_causes.md`

## Phase 7 - Correction Loop
- One bucket at a time:
  1. root cause
  2. patch
  3. affected-case rerun
  4. core smoke rerun
  5. closure note
- Outputs:
  - `triage/fix_log.md`
  - `triage/regression_status.csv`

## Phase 8 - Release Gate
- Acceptance:
  - core package 100% PASS
  - total PASS >= 95%
  - no open P0/P1 mismatch
- Final:
  - `FINAL_PARITY_REPORT.md`
  - baseline freeze record
  - suite freeze record

## Immediate Next Actions
1. Populate `manifests/cases_manifest_all.csv` with generated case set.
2. Run `scripts/build_case_setup_guide.py` to refresh tracker workbook.
3. Drop TV exports into `tv_manual_inputs/raw_tv_exports/`.
4. Run `scripts/route_tv_xlsx.py` and review `tv_unmatched.csv`.
5. Start Python batch + comparison phases.
