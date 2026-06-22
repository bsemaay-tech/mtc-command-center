# HOME_CANONICAL_UNIVERSE_PATCH Audit - 2026-06-15

## 1. Executive verdict

Verdict: ACCEPT WITH SMALL FOLLOW-UP

The patch satisfies the core product decision: `Total Strategies` is now the canonical pipeline strategy universe, with registry candidates used only as fallback when pipeline rows are unavailable. Scorecard-only IDs are excluded from strategy totals and surfaced separately as evidence/orphan data. Live snapshot verification matches the expected current values and no strategy-level metric exceeds `Total Strategies`.

Small follow-up: the worktree remains dirty beyond this patch scope, with prior modified/untracked files and staged prototype renames. Isolate/stage/commit the intended Home patch set before final release review.

## 2. Files inspected

- `08_DASHBOARD_APP/apps/web/app.js`
- `08_DASHBOARD_APP/apps/web/index.html`
- `08_DASHBOARD_APP/apps/web/styles.css`
- `08_DASHBOARD_APP/apps/api/tests/test_home_metric_invariants.py`
- `11_TRIAGE/HOME_CANONICAL_UNIVERSE_PATCH_REPORT_2026-06-15.md`

Related safety/context checks:
- `08_DASHBOARD_APP/apps/api/mcc_readonly/server.py`
- `08_DASHBOARD_APP/apps/api/mcc_readonly/night_artifacts_reader.py`
- `03_QUANTLENS/05_BACKTEST_RESULTS` artifact tree

## 3. Canonical universe verification

PASS.

`app.js` defines:
- `canonicalStrategyIds()`: uses unique base IDs from `candidate_pipeline.rows`.
- Registry fallback: only runs when the pipeline ID set is empty.
- `strategyUniverse()`: aliases `canonicalStrategyIds()`.

Live snapshot verification:
- `Total Strategies`: 176
- Universe source: pipeline
- Pipeline rows: 176
- Registry entries: 14

The Python invariant test also covers the fallback branch where pipeline rows are empty and registry candidates become the universe.

## 4. Scorecard-only/orphan ID verification

PASS.

`orphanScorecardIds()` computes unique scorecard base IDs absent from the canonical universe. Those IDs are not unioned into `Total Strategies`.

Live snapshot verification:
- `Scorecard-only Strategy IDs`: 36
- `Any Orphan In Canonical`: false

The Home UI renders the orphan/evidence metric as `Scorecard-only Strategy IDs` under `Evidence / System Volume`.

## 5. Strategy-level metric verification

PASS.

All strategy-level metrics iterate `strategyUniverse()` / canonical IDs:
- `Gate 1 Passed Strategies`
- `Gate 1B Passed Strategies`
- `Gate 2 Passed Strategies`
- `Gate 2 Failed Strategies`
- `Paper Ready Strategies`
- `Needs Review Strategies` (renamed from Needs Attention with explanatory tooltip)

Live snapshot values:
- `Total Strategies`: 176
- `Gate 1 Passed Strategies`: 10
- `Gate 1B Passed Strategies`: 10
- `Gate 2 Passed Strategies`: 5
- `Gate 2 Failed Strategies`: 5
- `Paper Ready Strategies`: 0
- `Needs Review Strategies`: 176

Invariant:
- No strategy-level count exceeds `Total Strategies`: true.

## 6. Evidence/system row metric verification

PASS.

Raw evidence/system metrics remain visibly labelled as rows/runs/indexed/errors/scorecard-only:
- `Scorecard Rows`: 837
- `Gate 1 Passed Rows`: 646
- `Benchmark Candidate Rows`: 344
- `Gate 2 Failed Rows`: 143
- `Backtest Runs`: 80
- `Reports Indexed`: 13
- `Scorecard-only Strategy IDs`: 36
- `Artifact Errors`: present as an explicit system metric

The Home note states that strategy counts use the canonical pipeline/registry universe, scorecard-only IDs are orphan evidence until promoted, and row counts may exceed strategy counts.

## 7. Strategy Intelligence preservation check

PASS.

The Strategy Intelligence Gate 1 section is preserved:
- `bestGate1PassingVersion(id)` is still present.
- The UI still renders `Primary Gate 1 Version`.
- The status badge still shows `Showing best Gate 1 passing version` or `No Gate 1 passing version found`.
- The `Advanced / All Versions` table remains present with asset/timeframe, profile, G1 score, Gate 1, Gate 1B, Gate 2, and run columns.

## 8. API/read-only safety verification

PASS.

Commands run:
- `git status --short`
- `git diff --stat`
- `node --check 08_DASHBOARD_APP\apps\web\app.js` - PASS
- `python -m unittest discover tests` from `08_DASHBOARD_APP/apps/api` - PASS, 60 tests
- `GET /healthz` - PASS, `mode=read_only`, `overall_ok=true`
- `GET /api/snapshot?refresh=1` - PASS, HTTP 200
- `POST /api/snapshot` - blocked, HTTP 405

No fake profile-result artifacts were found:
- no `backtest_profile_result.json`
- no `top_results.json`

Protected execution scope:
- no modified tracked Pine, MTC_V2, `02_MTC_BACKTEST`, `07_ADAPTERS`, or protected execution files were reported in the protected-path status check.

## 9. Issues found

1. Worktree scope remains dirty.
   - Modified tracked files include web/API files and `_AI_MEMORY` handoff files.
   - Staged prototype renames remain from prior work.
   - Many untracked reports, schemas, tools, tests, screenshots, and external folders remain present.
   - This does not invalidate the Home metric behavior, but it prevents a clean scope claim from `git status` alone.

2. Registry fallback is covered by unit test, not live data.
   - Live data has pipeline rows, so the production snapshot exercises the primary pipeline path.
   - This is acceptable for the current state, but the fallback should stay test-covered.

No blocker was found in the canonical strategy universe logic, scorecard-only separation, strategy metric invariants, read-only API behavior, or protected execution scope.

## 10. Recommended next step

Accept the patch, then isolate the intended review unit: `app.js`, `index.html`, `test_home_metric_invariants.py`, the patch report, and any intended handoff updates. Keep the optional follow-up as a small UI/data-quality improvement: add a drill-down list for the 36 scorecard-only strategy IDs and a promotion path into pipeline/registry when those IDs become canonical.
