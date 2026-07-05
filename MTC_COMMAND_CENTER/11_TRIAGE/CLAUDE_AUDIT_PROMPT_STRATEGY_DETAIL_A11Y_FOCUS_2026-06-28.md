# Claude Audit Prompt - Strategy Detail P1 A11y Focus

Repo: `C:\LAB\Tradingview_LAB_CLEAN`

Task: audit the Codex patch for the Impeccable Strategy Detail P1 a11y-focus follow-up.

## Required Read Order

1. `AGENTS.md`
2. `MTC_COMMAND_CENTER\_AI_MEMORY\START_HERE.md`
3. `MTC_COMMAND_CENTER\_AI_MEMORY\NEXT_STEPS.md`
4. `MTC_COMMAND_CENTER\_AI_MEMORY\GLOBAL_HANDOFF.md`

## Scope

Audit only this intended UI/a11y change:

- `MTC_COMMAND_CENTER\08_DASHBOARD_APP\apps\web\app.js`
- `MTC_COMMAND_CENTER\08_DASHBOARD_APP\apps\web\styles.css`
- `MTC_COMMAND_CENTER\08_DASHBOARD_APP\apps\api\tests\test_strategy_detail_a11y_static.py`
- handoff updates in `_AI_MEMORY`

Do not edit files unless you find a concrete regression. Do not touch Pine, MTC_V2, parity, backtest, schemas, broker/execution, scorecard math, artifact semantics, or trading logic.

## Questions To Answer

1. Are the four Strategy Detail workflow/STAGE cards now keyboard-focusable native controls?
2. Does the change preserve the existing scroll behavior and visual layout?
3. Is the global `:focus-visible` ring visible and not likely to create obvious layout shifts?
4. Does `.workflow-card:focus-visible` provide a clear focused state?
5. Does `prefers-reduced-motion: reduce` disable the amber pulse animation?
6. Is the new static test meaningful and not overbroad?
7. Did Codex stay inside UI/a11y scope?
8. Are the handoff/NEXT_STEPS updates accurate?

## Verification Commands

From `MTC_COMMAND_CENTER\08_DASHBOARD_APP\apps\api`:

```powershell
$env:PYTHONPATH='.'
python -m unittest tests.test_strategy_detail_a11y_static
python -m unittest discover tests
```

From repo root:

```powershell
node --check MTC_COMMAND_CENTER\08_DASHBOARD_APP\apps\web\app.js
git diff --check -- MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/web/app.js MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/web/styles.css MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api/tests/test_strategy_detail_a11y_static.py MTC_COMMAND_CENTER/_AI_MEMORY/GLOBAL_HANDOFF.md MTC_COMMAND_CENTER/_AI_MEMORY/NEXT_STEPS.md MTC_COMMAND_CENTER/_AI_MEMORY/SESSION_LOG.md
```

## Output

Write the audit report to:

`MTC_COMMAND_CENTER\11_TRIAGE\CLAUDE_AUDIT_REPORT_STRATEGY_DETAIL_A11Y_FOCUS_2026-06-28.md`

Use this verdict format:

- `PASS`
- `PASS WITH NITS`
- `FAIL - FIX REQUIRED`

Include exact file/line references for any finding.
