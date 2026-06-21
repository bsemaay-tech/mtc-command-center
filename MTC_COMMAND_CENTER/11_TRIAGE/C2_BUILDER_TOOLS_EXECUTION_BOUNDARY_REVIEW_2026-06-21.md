# C2 Builder Tools Execution Boundary Review - 2026-06-21

## 1. Executive Verdict

This was a read-only static review of only the two C2 QuantLens builder tools and their paired tests. No builders, tests, backtests, optimizations, launchers, dashboard server scripts, artifacts, `top_results.json`, Pine, MTC_V2, C3, C4, or ignored/local-only C5 paths were run or modified.

Verdict: `SAFE_AFTER_SMALL_PATCH`.

The builders are not executors: they do not import subprocess modules, do not call backtest/optimization engines, do not touch brokers, do not touch Pine, and do not touch MTC_V2. Their paired tests are appropriate and should be committed with the builders once the builder write boundary is tightened.

However, both builders currently write files when run without `--dry-run`, and both accept caller-controlled output paths. Before committing them as durable repo tools, add a small safety patch so writes require explicit operator intent and cannot silently overwrite or write outside the intended QuantLens result area.

## 2. Preflight Result

- Repo: `C:\LAB\Tradingview_LAB_CLEAN`
- Branch: `feature/ui-impeccable-pilot`
- Preflight: PASS
- Index before report: empty
- Unpushed commits before report: `0`
- Current pushed HEAD at review time: `cdecbda Add QuantLens scoring guide docs`
- Prior reports read:
  - `MTC_COMMAND_CENTER/11_TRIAGE/BUCKET_C2_QUANTLENS_TOOLS_AND_TESTS_AUDIT_2026-06-21.md`
  - `MTC_COMMAND_CENTER/11_TRIAGE/C2_DOCS_ONLY_GUIDES_EXECUTION_REPORT_2026-06-21.md`

## 3. File-By-File Table

| path | purpose | writes files? | exact outputs | dry-run default? | subprocess/process launch? | backtest/optimization risk | artifact-generation risk | `top_results.json` risk | fake-KPI risk | protected-scope risk | overwrite/path risk | secret risk | paired test present? | commit recommendation |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `MTC_COMMAND_CENTER/03_QUANTLENS/tools/build_profile_result_artifact.py` | Converts existing deterministic-soak source rows into one schema-valid profile result document. | yes | `backtest_profile_result.json` under default `MTC_COMMAND_CENTER/03_QUANTLENS/05_BACKTEST_RESULTS/pilot_profile_result_<strategy_id>_<date>/`, or caller-provided `--output-dir`. | no; `--dry-run` must be supplied | no | low-medium: consumes existing backtest/soak data but does not run backtests or optimizations | high: writes a dashboard-consumed result artifact | none: no `top_results.json` reference or write | low: copies real source metrics, keeps absent metrics null, refuses no-lockbox rows | low: no Pine/MTC_V2/protected execution imports; writes under QuantLens results by default | medium-high: `--output-dir` can target arbitrary paths and existing `backtest_profile_result.json` is overwritten | low: no key/token/env/credential assignment found | yes | `SAFE_AFTER_SMALL_PATCH`; commit with paired test after write-boundary hardening |
| `MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api/tests/test_build_profile_result_artifact.py` | Unit tests for profile-result builder schema, dry-run, no fake KPI, refusal, provenance, and reader discovery. | temp only | temp source/result fixtures inside `TemporaryDirectory`; no durable repo writes when run normally | n/a | no | low | medium in temp fixtures only | none | low; explicitly tests absent KPI stays null and non-robust remains research-only | low | low | low | yes | safe paired test; commit with builder after builder patch |
| `MTC_COMMAND_CENTER/03_QUANTLENS/tools/build_run_plan.py` | Generates review-only run plan, artifact index, and Markdown plan for dashboard discovery. | yes | `run_plan.json`, `artifact_index.json`, `run_plan.md` under default `MTC_COMMAND_CENTER/03_QUANTLENS/05_BACKTEST_RESULTS/<run_id>/`, or caller-provided `--output-root/<run_id>`. | no; `--dry-run` must be supplied | no | low-medium: plans backtest work but declares no execution and `execution_allowed=false` | high: writes planning artifacts consumed by the dashboard | low: lists expected `top_results.json` in the artifact contract but does not create it | low: does not generate KPI result rows; unresolved parameters are `needs_freeze` | low: explicit no Pine/MTC_V2/backtest-engine/broker language and no protected execution imports | medium-high: `--output-root` can target arbitrary paths and existing files are overwritten | low: no key/token/env/credential assignment found | yes | `SAFE_AFTER_SMALL_PATCH`; commit with paired test after write-boundary hardening |
| `MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api/tests/test_build_run_plan.py` | Unit tests for schema validity, review-only approval fields, no fake KPI/default symbol injection, dry-run, and required safety fields. | no durable writes | none; calls `main(... --dry-run ...)` and pure builder functions | n/a | no | low | low | none; no top-results generation | low; explicitly tests no fake sweeps and no default BTCUSDT injection | low | low | low | yes | safe paired test; commit with builder after builder patch |

## 4. Builder Safety Verdict

`SAFE_AFTER_SMALL_PATCH`

Reasons:

- No subprocess/process launch paths were found.
- No backtest or optimization engine invocation was found.
- No broker/live/paper execution path was found.
- No Pine, MTC_V2, parity, `02_MTC_BACKTEST`, `07_ADAPTERS`, or `01_PINE` write/touch path was found.
- Schema validation is present before writes.
- Empty/fake source rows are refused in `build_profile_result_artifact.py`.
- `build_run_plan.py` marks plans as review-only with `approval.execution_allowed = false`.
- Paired tests cover dry-run no-write behavior, no fake KPI/default-symbol behavior, schema validity, and review-only approval fields.

Boundary gaps before commit:

- `--dry-run` is not the default in either builder.
- Existing output files are overwritten without an explicit `--force`.
- Caller-controlled `--output-dir` / `--output-root` can point outside `03_QUANTLENS/05_BACKTEST_RESULTS`.
- `build_profile_result_artifact.py` describes itself as "read-only converter" even though it writes a result artifact when not dry-run; this should be clarified.

## 5. Required Patches Before Commit

Required small patch set before staging the builders:

1. Add an explicit apply/write gate:
   - Prefer `--apply` for writes and make default behavior dry-run/no-write, or at minimum require an explicit confirmation flag before writing.
2. Add overwrite protection:
   - Refuse if any destination file already exists unless `--force` is supplied.
3. Add output path containment:
   - Require default or custom output paths to resolve under `MTC_COMMAND_CENTER/03_QUANTLENS/05_BACKTEST_RESULTS`, unless a separate explicit escape hatch is approved.
4. Clarify wording/banner:
   - State that these are review/artifact writers, not execution tools.
   - For `build_profile_result_artifact.py`, avoid "read-only converter" as the sole description because non-dry-run mode writes `backtest_profile_result.json`.
5. Extend paired tests:
   - Assert default invocation without apply/force does not write.
   - Assert existing output files are refused without `--force`.
   - Assert output paths outside `05_BACKTEST_RESULTS` are refused.

## 6. Suggested Staged Set If Approved

After the small patch is made and reviewed, stage only:

- `MTC_COMMAND_CENTER/03_QUANTLENS/tools/build_profile_result_artifact.py`
- `MTC_COMMAND_CENTER/03_QUANTLENS/tools/build_run_plan.py`
- `MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api/tests/test_build_profile_result_artifact.py`
- `MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api/tests/test_build_run_plan.py`
- `MTC_COMMAND_CENTER/11_TRIAGE/C2_BUILDER_TOOLS_EXECUTION_BOUNDARY_REVIEW_2026-06-21.md`

Suggested commit message after the patch:

```text
Harden QuantLens builder write boundaries
```

## 7. Files That Must Not Be Staged

Do not stage any of these in the builder-boundary unit:

- `MTC_COMMAND_CENTER/03_QUANTLENS/tools/night_1m_2026-06-07.sh`
- `MTC_COMMAND_CENTER/03_QUANTLENS/tools/overnight_loop_2026-06-08.sh`
- `MTC_COMMAND_CENTER/03_QUANTLENS/tools/start_night_1m_2026-06-07_keepawake.ps1`
- `MTC_COMMAND_CENTER/03_QUANTLENS/tools/start_night_3M_2026-06-08_keepawake.ps1`
- `MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api/tests/test_home_metric_invariants.py`
- `MTC_COMMAND_CENTER/08_DASHBOARD_APP/run_dashboard_server.ps1`
- `MTC_COMMAND_CENTER/11_TRIAGE/UI_AUDITS/`
- `MTC_COMMAND_CENTER/11_TRIAGE/ui_references/google_strategy_intelligence_v2_final/`
- `MTC_COMMAND_CENTER/11_TRIAGE/ui_references/strategy_intelligence_lovable/`
- `MTC_COMMAND_CENTER/_AI_MEMORY/UI Reviev/`
- `HERMES/`
- `HERMES_MTC_MEMORY_IMPORT/`
- `_HERMES_MEMORY_IMPORT/`
- `YT_TRANSCRIPT_COLLECTOR/`
- ignored/local-only C5 scratch files and folders

## 8. Exact Next Execution Prompt

```text
You are executing C2_BUILDER_TOOLS_SMALL_PATCH.

This is a small builder safety patch only.

Do not touch launchers, dashboard server scripts, C3 UI screenshots/references, C4 HERMES/YT folders, ignored/local-only C5 items, Pine, MTC_V2, parity, 02_MTC_BACKTEST, 07_ADAPTERS, or 01_PINE.
Do not run builders except with --dry-run if needed for a lightweight verification after patching.
Do not run backtests.
Do not run optimizations.
Do not generate artifacts.
Do not generate top_results.json.
Do not force-push.

Repo root:
cd C:\LAB\Tradingview_LAB_CLEAN

Branch must be:
feature/ui-impeccable-pilot

Read first:
MTC_COMMAND_CENTER/11_TRIAGE/C2_BUILDER_TOOLS_EXECUTION_BOUNDARY_REVIEW_2026-06-21.md

Allowed files only:
MTC_COMMAND_CENTER/03_QUANTLENS/tools/build_profile_result_artifact.py
MTC_COMMAND_CENTER/03_QUANTLENS/tools/build_run_plan.py
MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api/tests/test_build_profile_result_artifact.py
MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api/tests/test_build_run_plan.py
MTC_COMMAND_CENTER/11_TRIAGE/C2_BUILDER_TOOLS_EXECUTION_BOUNDARY_REVIEW_2026-06-21.md

Goal:
Patch only the builder write boundary:
1. Make default behavior no-write unless an explicit apply/write flag is supplied.
2. Refuse overwriting existing destination files unless an explicit force flag is supplied.
3. Refuse output paths outside MTC_COMMAND_CENTER/03_QUANTLENS/05_BACKTEST_RESULTS.
4. Clarify builder wording so "read-only" cannot be mistaken for "never writes".
5. Update only the paired tests needed for those boundary rules.

Stage exactly the allowed files and commit:
git commit -m "Harden QuantLens builder write boundaries"
git push
```

## 9. Patch Applied

Patch summary:

- `build_profile_result_artifact.py` now behaves as a review/artifact writer with default no-write behavior.
- `build_run_plan.py` now behaves as a review-only planning artifact writer with default no-write behavior.
- Both builders now accept explicit `--apply` for writes and `--force` for approved overwrites.
- Paired tests now cover default no-write, dry-run no-write, explicit apply writes, overwrite refusal, force overwrite, output containment, schema preservation, and no-fake-result behavior.

Write gate behavior:

- Without `--apply`, both builders validate inputs and schemas, print the intended output path, and exit without writing.
- `--dry-run` remains supported and also exits without writing, even if `--apply` is supplied.

Overwrite behavior:

- `build_profile_result_artifact.py` refuses to overwrite an existing `backtest_profile_result.json` unless `--force` is supplied.
- `build_run_plan.py` refuses to overwrite any existing `run_plan.json`, `artifact_index.json`, or `run_plan.md` unless `--force` is supplied.

Output containment behavior:

- `build_profile_result_artifact.py` rejects `--output-dir` values that do not resolve under `MTC_COMMAND_CENTER/03_QUANTLENS/05_BACKTEST_RESULTS`.
- `build_run_plan.py` rejects `--output-root` values that do not resolve under `MTC_COMMAND_CENTER/03_QUANTLENS/05_BACKTEST_RESULTS`.

Focused test result:

```text
cd MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api
$env:PYTHONPATH="."
python -m unittest tests.test_build_profile_result_artifact tests.test_build_run_plan

Ran 28 tests in 0.223s
OK
```

Remaining risk:

- These builders still write dashboard-consumed QuantLens review/result artifacts when explicitly invoked with `--apply`; they should remain operator-run tools, not launchers.
- `build_run_plan.py` continues to list `top_results.json` only as an expected future artifact in `artifact_index.json`; it does not create `top_results.json`.
- No launchers, dashboard server scripts, backtests, optimizations, Pine, MTC_V2, parity, protected scopes, C3, C4, or ignored/local-only C5 files were touched by this patch.
