# CLAUDE AUDIT PROMPT — Artifact Contract Universe-Mismatch Boolean

You are auditing a completed, narrow artifact-contract follow-up in:

`C:\LAB\Tradingview_LAB_CLEAN`

Read first:

1. `AGENTS.md`
2. `MTC_COMMAND_CENTER\_AI_MEMORY\START_HERE.md`
3. `MTC_COMMAND_CENTER\_AI_MEMORY\AI_RULES.md`
4. `MTC_COMMAND_CENTER\_AI_MEMORY\NEXT_STEPS.md` lines around the "DASHBOARD night-artifact contract" section

Task:

Audit Codex's patch for `NEXT_STEPS.md` item 11(e): make universe mismatch a strict boolean in the profile-result converter/read model while preserving the human-readable reason and backward compatibility with legacy artifacts.

Intended changed files:

- `MTC_COMMAND_CENTER\03_QUANTLENS\tools\build_profile_result_artifact.py`
- `MTC_COMMAND_CENTER\08_DASHBOARD_APP\apps\api\mcc_readonly\night_artifacts_reader.py`
- `MTC_COMMAND_CENTER\08_DASHBOARD_APP\apps\web\app.js`
- `MTC_COMMAND_CENTER\08_DASHBOARD_APP\apps\api\tests\test_build_profile_result_artifact.py`
- `MTC_COMMAND_CENTER\08_DASHBOARD_APP\apps\api\tests\test_night_artifacts_reader.py`
- `_AI_MEMORY` handoff files only

Audit questions:

1. Does new converter output use `provenance.universe_mismatch` as a boolean and `provenance.universe_mismatch_reason` for text?
2. Does the reader normalize older artifacts where `universe_mismatch` was a string, without rewriting artifact files?
3. Does the frontend still show universe-mismatch flags and detail text for both new boolean artifacts and legacy string artifacts?
4. Is the change backward-compatible with existing `backtest_profile_result.json` files under `05_BACKTEST_RESULTS`?
5. Are tests adequate for converter output and reader legacy normalization?
6. Did the patch avoid schemas, existing result artifacts, backtest execution, Pine, MTC_V2, parity, broker/execution, scorecard semantics, and trading logic?
7. Do validation commands pass?

Suggested commands:

```powershell
git status --short --branch
git diff -- MTC_COMMAND_CENTER/03_QUANTLENS/tools/build_profile_result_artifact.py MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api/mcc_readonly/night_artifacts_reader.py MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/web/app.js MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api/tests/test_build_profile_result_artifact.py MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api/tests/test_night_artifacts_reader.py MTC_COMMAND_CENTER/_AI_MEMORY/GLOBAL_HANDOFF.md MTC_COMMAND_CENTER/_AI_MEMORY/NEXT_STEPS.md MTC_COMMAND_CENTER/_AI_MEMORY/SESSION_LOG.md
python -m py_compile MTC_COMMAND_CENTER\03_QUANTLENS\tools\build_profile_result_artifact.py MTC_COMMAND_CENTER\08_DASHBOARD_APP\apps\api\mcc_readonly\night_artifacts_reader.py
node --check MTC_COMMAND_CENTER\08_DASHBOARD_APP\apps\web\app.js
cd MTC_COMMAND_CENTER\08_DASHBOARD_APP\apps\api
$env:PYTHONPATH="."
python -m unittest tests.test_build_profile_result_artifact tests.test_night_artifacts_reader
python -m unittest discover tests
```

Report output:

Write your report to:

`MTC_COMMAND_CENTER\11_TRIAGE\CLAUDE_AUDIT_REPORT_ARTIFACT_UNIVERSE_MISMATCH_2026-06-28.md`

Report format:

1. Verdict: PASS / PASS WITH NITS / FAIL
2. Findings ordered by severity, with file/line references
3. Commands run and results
4. Any fixes applied
5. Protected-scope confirmation

Do not stage, commit, push, merge, create a branch, or run destructive git commands.
