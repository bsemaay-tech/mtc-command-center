# Bucket C2 QuantLens Tools And Tests Audit - 2026-06-21

## 1. Executive Verdict

This was a read-only classification pass over the 12 approved C2 candidates. No tests, backtests, optimizations, scripts, servers, artifact generation, `top_results.json`, Pine, MTC_V2, C3, C4, or ignored/local-only C5 paths were touched.

Verdict:

- The two Turkish guide docs are durable repo documentation candidates.
- The three API/unit tests are reasonable commit candidates only when paired with their owning feature/tool unit.
- The two Python builder tools are not launchers and include dry-run/schema/refusal guards, but they write planning/result artifacts under `03_QUANTLENS/05_BACKTEST_RESULTS`; they need a separate execution-boundary review before commit.
- The dated overnight shell scripts and keep-awake wrappers are local/date-specific execution launchers and should not be staged in a normal C2 commit.
- The dashboard server launcher starts/stops local processes and needs a separate operational review before any commit.

Recommended next cleanup unit: `C2_DOCS_ONLY_GUIDES`.

## 2. Preflight Result

- Repo: `C:\LAB\Tradingview_LAB_CLEAN`
- Branch: `feature/ui-impeccable-pilot`
- Preflight: PASS
- Index before report: empty
- Unpushed commits before report: `0`
- Dirty state before report: remaining untracked C2/C3/C4 candidates only

## 3. C2 Item Table

| path | type | rough size | purpose | writes files? | launches process? | backtest/optimization risk | artifact-generation risk | secret risk | recommended action | commit allowed later? | reason |
|---|---|---:|---|---|---|---|---|---|---|---|---|
| `MTC_COMMAND_CENTER/03_QUANTLENS/_user_guide/13_GATE_SCORECARD_V2_TR.md` | Turkish guide doc | 17.1 KB / 377 lines | Canonical gate-based scorecard v2 design and file map. | no | no | medium: describes backtest, promotion, Pine/Python parity, and paper/forward flow | low: references artifact schemas but does not generate | low: generic broker/API wording only; no secret-shaped values found | `SAFE_TO_COMMIT_LATER` | yes | Durable docs in the right guide path; commit only as docs-only unit after quick wording review. |
| `MTC_COMMAND_CENTER/03_QUANTLENS/_user_guide/14_OPTIMIZASYON_SKORLAMA_TR.md` | Turkish guide doc | 13.3 KB / 487 lines | Optimization scoring framework, promotion levels, reporting standards, and planned file structure. | no | no | medium-high: optimization policy and promotion semantics | low: describes reports/results but does not generate | low: no secret-shaped values found | `SAFE_TO_COMMIT_LATER` | yes | Durable docs in the right guide path; must be committed as documentation only, not as approval to run optimizations. |
| `MTC_COMMAND_CENTER/03_QUANTLENS/tools/build_profile_result_artifact.py` | Python CLI tool | 12.5 KB / 288 lines | Converts real soak/backtest source JSON into one schema-valid `backtest_profile_result.json`. | yes | no | medium: consumes backtest-result source data | high: writes `backtest_profile_result.json` under `03_QUANTLENS/05_BACKTEST_RESULTS` unless `--dry-run` | low: no secret-shaped values found | `NEEDS_USER_DECISION` | no | Has useful guards (`--dry-run`, schema validation, refuses empty/fake source rows) but writes artifact files; needs a focused execution-boundary review before commit. |
| `MTC_COMMAND_CENTER/03_QUANTLENS/tools/build_run_plan.py` | Python CLI tool | 17.0 KB / 419 lines | Generates review-only `run_plan.json`, `artifact_index.json`, and `run_plan.md` for one strategy. | yes | no | medium: creates backtest planning files; not an executor | high: writes run-plan artifacts under `03_QUANTLENS/05_BACKTEST_RESULTS`; references expected `top_results.json` but does not create it | low: generic credential wording only; no secret-shaped values found | `NEEDS_USER_DECISION` | no | Good safety language and no execution import, but it writes artifacts and touches planning/execution boundary; review separately with schemas. |
| `MTC_COMMAND_CENTER/03_QUANTLENS/tools/night_1m_2026-06-07.sh` | dated Bash launcher | 7.4 KB / 231 lines | Runs a quiet 1M overnight sweep plus validation/report tail. | yes | yes | high: launches backtest/validation scripts and overnight loop work | high: writes logs, run dirs, validation outputs, reports under `05_BACKTEST_RESULTS`/`overnight_runs` | low: no secret-shaped values found | `LOCAL_ONLY` | no | Date-specific execution launcher; not durable normal repo content without explicit operational approval. |
| `MTC_COMMAND_CENTER/03_QUANTLENS/tools/overnight_loop_2026-06-08.sh` | dated Bash launcher | 7.0 KB / 203 lines | Runs long overnight loop, selects best iteration, then validation/scoring/report phases. | yes | yes | high: launches sweeps, validation, scorecards, reports; includes process cleanup wording | high: writes results, scorecards, reports, and a dated result JSON under `05_BACKTEST_RESULTS` | low: no secret-shaped values found | `DO_NOT_COMMIT` | no | Date-specific operational script with long-running execution and old-Python-process cleanup behavior; keep out unless Baris explicitly reopens it. |
| `MTC_COMMAND_CENTER/03_QUANTLENS/tools/start_night_1m_2026-06-07_keepawake.ps1` | dated PowerShell wrapper | 1.6 KB / 55 lines | Starts the 2026-06-07 Bash overnight script and keeps the machine awake. | yes | yes | high: launches overnight backtest script | medium: creates `overnight_runs` and logs through child script | low: no secret-shaped values found | `LOCAL_ONLY` | no | Local machine keep-awake/execution wrapper; not durable repo content by default. |
| `MTC_COMMAND_CENTER/03_QUANTLENS/tools/start_night_3M_2026-06-08_keepawake.ps1` | dated PowerShell wrapper | 1.8 KB / 57 lines | Starts the 2026-06-08 Bash overnight loop and keeps the machine awake. | yes | yes | high: launches overnight backtest script | medium: creates `overnight_runs` and logs through child script | low: no secret-shaped values found | `LOCAL_ONLY` | no | Local machine keep-awake/execution wrapper; not durable repo content by default. |
| `MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api/tests/test_build_profile_result_artifact.py` | Python unit test | 7.9 KB / 171 lines | Tests profile-result builder schema, dry-run, no fake KPIs, non-promotable handling, and reader discovery. | yes, temp dirs only | no | low-medium: test data models backtest artifacts but does not run backtests | medium: writes temp `backtest_profile_result.json` fixtures only | low: no secret-shaped values found | `SAFE_TO_COMMIT_LATER` | yes | Good paired coverage for the builder, but should be committed with or after the approved builder unit. |
| `MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api/tests/test_build_run_plan.py` | Python unit test | 5.6 KB / 128 lines | Tests run-plan schema, review-only status, no fake KPIs, dry-run, universe handling, and safety fields. | no durable writes | no | low-medium: planning logic only, no backtest execution | low-medium: validates artifact-index/run-plan structures in memory | low: no secret-shaped values found | `SAFE_TO_COMMIT_LATER` | yes | Good paired coverage for the run-plan builder, but should be committed with or after the approved builder unit. |
| `MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api/tests/test_home_metric_invariants.py` | Python unit test | 5.9 KB / 165 lines | Tests dashboard home metric invariants for canonical/orphan strategy counts and fallback behavior. | no | no | low | low | low: no secret-shaped values found | `SAFE_TO_COMMIT_LATER` | yes | Pure invariant test; likely safe in a focused dashboard-test commit. |
| `MTC_COMMAND_CENTER/08_DASHBOARD_APP/run_dashboard_server.ps1` | PowerShell launcher | 7.2 KB / 190 lines | Persistent single-instance read-only dashboard server launcher on `127.0.0.1:8765`. | yes, logs | yes | low for backtests; high for local process behavior | low: runtime logs only | low: no secret-shaped values found | `NEEDS_USER_DECISION` | no | Operational launcher starts, monitors, and can stop matching local Python server processes; needs explicit launcher/process-safety review before commit. |

## 4. Safe Commit Candidates

Potentially safe later, after a small focused diff review:

- `MTC_COMMAND_CENTER/03_QUANTLENS/_user_guide/13_GATE_SCORECARD_V2_TR.md`
- `MTC_COMMAND_CENTER/03_QUANTLENS/_user_guide/14_OPTIMIZASYON_SKORLAMA_TR.md`
- `MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api/tests/test_build_profile_result_artifact.py`
- `MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api/tests/test_build_run_plan.py`
- `MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api/tests/test_home_metric_invariants.py`

Note: the two builder tests should not be committed alone if their target builder tools remain uncommitted, unless Baris explicitly wants pending tests.

## 5. User-Decision Candidates

- `MTC_COMMAND_CENTER/03_QUANTLENS/tools/build_profile_result_artifact.py`
- `MTC_COMMAND_CENTER/03_QUANTLENS/tools/build_run_plan.py`
- `MTC_COMMAND_CENTER/08_DASHBOARD_APP/run_dashboard_server.ps1`

These may be useful repo content, but each needs a focused review because it writes artifacts or controls local processes.

## 6. Do-Not-Commit / Local-Only Candidates

Local-only:

- `MTC_COMMAND_CENTER/03_QUANTLENS/tools/night_1m_2026-06-07.sh`
- `MTC_COMMAND_CENTER/03_QUANTLENS/tools/start_night_1m_2026-06-07_keepawake.ps1`
- `MTC_COMMAND_CENTER/03_QUANTLENS/tools/start_night_3M_2026-06-08_keepawake.ps1`

Do not commit:

- `MTC_COMMAND_CENTER/03_QUANTLENS/tools/overnight_loop_2026-06-08.sh`

Reason: these are date-specific execution/overnight/keep-awake scripts. They launch backtest or validation flows and write logs/results.

## 7. Files That Must Not Be Staged Without Explicit Approval

- `MTC_COMMAND_CENTER/03_QUANTLENS/tools/build_profile_result_artifact.py`
- `MTC_COMMAND_CENTER/03_QUANTLENS/tools/build_run_plan.py`
- `MTC_COMMAND_CENTER/03_QUANTLENS/tools/night_1m_2026-06-07.sh`
- `MTC_COMMAND_CENTER/03_QUANTLENS/tools/overnight_loop_2026-06-08.sh`
- `MTC_COMMAND_CENTER/03_QUANTLENS/tools/start_night_1m_2026-06-07_keepawake.ps1`
- `MTC_COMMAND_CENTER/03_QUANTLENS/tools/start_night_3M_2026-06-08_keepawake.ps1`
- `MTC_COMMAND_CENTER/08_DASHBOARD_APP/run_dashboard_server.ps1`

Also do not stage the paired builder tests unless the owning builder tool commit plan is explicitly approved.

## 8. Recommended Next Cleanup Unit

`C2_DOCS_ONLY_GUIDES`

This is the smallest safe unit: audit/stage/commit only the two Turkish guide docs as documentation, with no scripts, tests, launchers, artifact writers, backtests, optimizations, Pine, MTC_V2, or dashboard process behavior.

## 9. Suggested Exact Next Execution Prompt

```text
You are executing C2_DOCS_ONLY_GUIDES.

Do not touch QuantLens tools, launchers, tests, dashboard server scripts, C3, C4, C5, Pine, MTC_V2, backtests, optimizations, generated artifacts, or top_results.json.

Repo: C:\LAB\Tradingview_LAB_CLEAN
Branch must be: feature/ui-impeccable-pilot

Read:
MTC_COMMAND_CENTER/11_TRIAGE/BUCKET_C2_QUANTLENS_TOOLS_AND_TESTS_AUDIT_2026-06-21.md

Allowed files only:
MTC_COMMAND_CENTER/03_QUANTLENS/_user_guide/13_GATE_SCORECARD_V2_TR.md
MTC_COMMAND_CENTER/03_QUANTLENS/_user_guide/14_OPTIMIZASYON_SKORLAMA_TR.md

Preflight: branch, status, empty index, no unpushed commits.

Inspect only these two docs for stale or misleading claims that would imply live/paper/promotable approval, backtest execution, optimization execution, Pine/MTC_V2 changes, or current active runs.

If safe docs-only content, stage exactly these two files and commit:
git commit -m "Add QuantLens scoring guide docs"

Push normally. Do not force-push.
```
