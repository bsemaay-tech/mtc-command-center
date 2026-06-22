# C2 Home Metric Invariants Test Only Audit - 2026-06-21

## 1. Executive Verdict

Verdict: `SAFE_TO_COMMIT_LATER`.

`MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api/tests/test_home_metric_invariants.py` is a pure Python dashboard/API invariant test. It is self-contained, uses synthetic in-memory snapshot data, imports only `unittest`, does not write durable files, does not start servers or subprocesses, and does not run builders, launchers, backtests, optimizations, or artifact writers.

The focused test was safe and lightweight, so it was run exactly as approved.

## 2. Preflight Result

- Repo: `C:\LAB\Tradingview_LAB_CLEAN`
- Branch: `feature/ui-impeccable-pilot`
- Preflight: PASS
- Index before report: empty
- Unpushed commits before report: `0`
- Dirty state before report: remaining untracked C2/C3/C4 candidates only

Reports read first:

- `MTC_COMMAND_CENTER/11_TRIAGE/BUCKET_C2_QUANTLENS_TOOLS_AND_TESTS_AUDIT_2026-06-21.md`
- `MTC_COMMAND_CENTER/11_TRIAGE/C2_DOCS_ONLY_GUIDES_EXECUTION_REPORT_2026-06-21.md`
- `MTC_COMMAND_CENTER/11_TRIAGE/C2_BUILDER_TOOLS_EXECUTION_BOUNDARY_REVIEW_2026-06-21.md`

## 3. Static Audit Findings

Scoped file:

- `MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api/tests/test_home_metric_invariants.py`

Static facts:

- Rough size: 6,067 bytes / 166 lines
- Imports: `__future__.annotations`, `unittest`
- Test class: `HomeMetricInvariantTests`
- Test count: 5
- Durable file writes: no
- Temp directory writes: no
- Server/process launch: no
- Backtest/optimization execution: no
- Builder/launcher/artifact-writer execution: no
- `top_results.json` generation: no
- Pine/MTC_V2/parity/protected-scope touch: no
- Broker/live/paper execution touch: no
- Fragile local absolute paths: no
- App/module imports: no; the test mirrors the JS aggregation contract using local helper functions and synthetic snapshot dictionaries

Classification checklist:

| question | finding |
|---|---|
| Pure API/dashboard invariant test? | yes |
| Imports only safe/read-only modules? | yes, only `unittest` plus future annotations |
| Writes durable files? | no |
| Starts servers or processes? | no |
| Runs backtests, optimizations, builders, launchers, or artifact writers? | no |
| Touches Pine, MTC_V2, parity, broker/live/paper execution, or protected scopes? | no |
| Relies on fragile local absolute paths? | no |
| Uses temp dirs only, if any? | no temp dirs used |
| Useful durable test coverage? | yes; guards Home dashboard strategy-count invariants against orphan scorecard inflation |

## 4. Focused Test Decision

Focused test was run because static inspection showed the file is self-contained and lightweight.

Command:

```powershell
cd MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api
$env:PYTHONPATH="."
python -m unittest tests.test_home_metric_invariants
```

## 5. Focused Test Result

Result: PASS.

```text
Ran 5 tests in 0.000s
OK
```

## 6. Secret / Sensitive Check

Result: PASS.

No sensitive assignment patterns or credential-shaped content were found. The only `paper` matches are metric-key text in the synthetic invariant calculation and do not imply paper-trading approval.

Checked patterns included:

- `api_key`
- `secret`
- `token =` / `token:`
- `password =` / `password:`
- `credential`
- `.env`
- broker/live/paper execution context

## 7. Commit Recommendation

`SAFE_TO_COMMIT_LATER`.

This test can be committed as its own small C2 test-only unit. It should not be mixed with launchers, dashboard server scripts, C3 UI references/screenshots, C4 side-project folders, or ignored/local-only C5 items.

## 8. Suggested Staged Set If Approved

Stage only:

- `MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api/tests/test_home_metric_invariants.py`
- `MTC_COMMAND_CENTER/11_TRIAGE/C2_HOME_METRIC_INVARIANTS_TEST_ONLY_AUDIT_2026-06-21.md`

Suggested commit message:

```text
Add home metric invariant test
```

## 9. Files That Must Not Be Staged

Do not stage in this unit:

- `MTC_COMMAND_CENTER/03_QUANTLENS/tools/night_1m_2026-06-07.sh`
- `MTC_COMMAND_CENTER/03_QUANTLENS/tools/overnight_loop_2026-06-08.sh`
- `MTC_COMMAND_CENTER/03_QUANTLENS/tools/start_night_1m_2026-06-07_keepawake.ps1`
- `MTC_COMMAND_CENTER/03_QUANTLENS/tools/start_night_3M_2026-06-08_keepawake.ps1`
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

## 10. Exact Next Execution Prompt

```text
You are executing C2_HOME_METRIC_INVARIANTS_TEST_ONLY_COMMIT.

This is a tiny test-only commit.

Do not touch launchers.
Do not touch dashboard server scripts.
Do not touch QuantLens builder tools.
Do not touch C3 UI screenshots/references.
Do not touch C4 HERMES/YT folders.
Do not touch ignored/local-only C5 items.
Do not touch Pine.
Do not touch MTC_V2.
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
MTC_COMMAND_CENTER/11_TRIAGE/C2_HOME_METRIC_INVARIANTS_TEST_ONLY_AUDIT_2026-06-21.md

Allowed files only:
MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api/tests/test_home_metric_invariants.py
MTC_COMMAND_CENTER/11_TRIAGE/C2_HOME_METRIC_INVARIANTS_TEST_ONLY_AUDIT_2026-06-21.md

Preflight:
git branch --show-current
git status --short
git status -sb
git diff --cached --stat
git rev-list --count '@{u}..HEAD'

Run only:
cd MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api
$env:PYTHONPATH="."
python -m unittest tests.test_home_metric_invariants

Stage exactly the two allowed files, verify cached name-only/stat, commit:
git commit -m "Add home metric invariant test"
git push
```
