# Dead Decision Panel Removal - Codex GPT-5 - 2026-06-08

Scope: display-only cleanup from the 2026-06-08 backlog item "delete dead `renderDecisionPanel()`".
No trading logic, Pine logic, MTC behavior, parity files, API readers, or score math changed.

## Result

Removed the unused `renderDecisionPanel()` function from `08_DASHBOARD_APP/apps/web/app.js`.
Removed the now-unused `.decision-panel` and `.decision-item` styles from `08_DASHBOARD_APP/apps/web/styles.css`.

## Verification

```powershell
node --check MTC_COMMAND_CENTER\08_DASHBOARD_APP\apps\web\app.js
```

PASS.

```powershell
rg -n "renderDecisionPanel|decision-panel|decision-item" MTC_COMMAND_CENTER\08_DASHBOARD_APP\apps\web\app.js MTC_COMMAND_CENTER\08_DASHBOARD_APP\apps\web\styles.css MTC_COMMAND_CENTER\08_DASHBOARD_APP\apps\web\index.html
```

PASS: no remaining references.

## Safety

The removed function was never called. It also contained stale fallback text paths such as legacy `blocked_reason`; deleting it removes a dormant stale-blocker source without changing the live Strategy Detail render.
