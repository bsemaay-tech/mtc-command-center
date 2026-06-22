# Dashboard Launcher Single-Instance — Follow-up Report — 2026-06-15

Follows audit `11_TRIAGE/DASHBOARD_LAUNCHER_SINGLE_INSTANCE_PATCH_AUDIT_2026-06-15.md`
(verdict: ACCEPT WITH SMALL FOLLOW-UP).

## 1. Executive summary
Two audit nits addressed; one tracked as a separate task.
- **`-StatusOnly` is now truly non-mutating.** It no longer truncates logs or appends to
  `dashboard_launcher.log`; it prints to stdout only and exits 0. Verified: log size +
  modified time unchanged across two consecutive `-StatusOnly` runs.
- **Startup auto-start corrected.** One per-user Startup VBS entry
  (`MTC_Command_Center_Dashboard.vbs`) exists and points to the guarded launcher. The prior
  patch report's "no auto-start found" was stale; documentation/handoff corrected here. No
  startup entry created, deleted, or modified.
- **Large snapshot (~121 MB / ~60 s) tracked as a separate performance task** in NEXT_STEPS;
  intentionally NOT addressed in this patch.

Core launcher behavior re-verified: repeated launches skip the healthy read-only server,
process count stays at one `pythonw.exe`, `POST /api/snapshot` → 405, 69 API tests pass.

## 2. Files changed
- `08_DASHBOARD_APP/run_dashboard_server.ps1` — `-StatusOnly` block moved ahead of the
  `Limit-LogSize` calls and switched from `Write-Launcher` (file append) to `Write-Output`
  (console only). No other launcher behavior changed.
- `11_TRIAGE/DASHBOARD_LAUNCHER_SINGLE_INSTANCE_FOLLOWUP_REPORT_2026-06-15.md` — this report.
- `_AI_MEMORY/SESSION_LOG.md`, `_AI_MEMORY/NEXT_STEPS.md`, `_AI_MEMORY/ACTIVE_FILES.md` —
  updated.

No Startup VBS / scheduled task / Run-key changes. No Pine / MTC_V2 / backtest engine /
broker / live / paper execution / API-write / data-contract / artifact changes.

## 3. StatusOnly no-change fix
Before: top-level `Limit-LogSize $serverLog` / `Limit-LogSize $launcherLog` ran for every
invocation (could truncate), and the StatusOnly branch logged via `Write-Launcher` (append).
After: the StatusOnly branch runs **before** the `Limit-LogSize` calls and emits with
`Write-Output`. Normal modes (skip/start/warn/force-restart/kill-stale/failure) still log via
`Write-Launcher` and still truncate oversized logs — only `-StatusOnly` is now no-change.

Verification:
```
BEFORE size=953 mtime=2026-06-16T13:36:09.0538583+03:00
[two -StatusOnly runs printed to console]
AFTER  size=953 mtime=2026-06-16T13:36:09.0538583+03:00
UNCHANGED: True
```
`-StatusOnly` does not start or kill processes and exits 0.

## 4. Startup VBS verification
- Path: `C:\Users\BarışSemaay\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\MTC_Command_Center_Dashboard.vbs`.
- Content runs:
  `powershell.exe -NoProfile -WindowStyle Hidden -NonInteractive -ExecutionPolicy Bypass -File "…\08_DASHBOARD_APP\run_dashboard_server.ps1"` (window 0, async).
- This is the **guarded** launcher, so logon start is now single-instance safe (the launcher
  self-skips if a healthy read-only server already owns port 8765).
- **No duplicate Startup VBS entries** were found. Other per-user Startup items
  (`GenuineService.lnk`, `HermesGateway.bat`, `Send to OneNote.lnk`, a `.disabled` autopilot
  cmd) are unrelated and do not reference the dashboard. All-users Startup has only
  `AnyDesk.lnk`.
- No new startup entries created. No startup entries deleted. No scheduled task created
  (not requested).

## 5. Repeated launcher / process-count verification
- Two consecutive default launches → both logged
  `[skip] dashboard already running (port 8765, pid 24720, healthy read_only); skip launch`.
- Strict server count after the test: `count=1` (PID 24720, `pythonw.exe`). No duplicate
  process spawned.

## 6. API / read-only validation
- `/healthz` → 200.
- `/api/snapshot?refresh=1` → 200 (bytes ≈ 121,079,001 — large; see §9 / NEXT_STEPS).
- `POST /api/snapshot` → **405** (write API unchanged).

## 7. Tests run
- PowerShell parse (`Parser::ParseFile`) → **PARSE_OK**.
- `node --check 08_DASHBOARD_APP/apps/web/app.js` → **JS_OK**.
- `python -m unittest discover tests` (apps/api) → **Ran 69 tests … OK**.

## 8. Safety confirmation
Only `run_dashboard_server.ps1` (StatusOnly logging) + report/handoff changed. No backtest,
optimization, or artifact generation. No Pine / MTC_V2 / backtest engine / broker / live /
paper execution touched. No POST/PUT/PATCH/DELETE behavior added (POST→405 verified). No
files staged, committed, deleted, reset, or moved. No Startup/scheduled-task mutation.

## 9. Remaining limitations
- **Snapshot payload is large/slow (~121 MB, ~60 s with extended timeout).** Tracked as a
  separate performance task; NOT addressed here. Likely candidates: trim/paginate scorecard
  rows in the snapshot, gzip the response, or split heavy sections behind dedicated
  endpoints. Needs its own scoped patch.
- Supervisor still relies on the Startup VBS (or a manual run) to (re)start after a real
  crash; that VBS now correctly targets the guarded launcher.
- `Get-PortOwner` PID is `-1` (unknown) only on the rare `Get-NetTCPConnection`-unavailable
  fallback; guard/skip logic is healthz-gated and still correct.

## 10. Recommended next phase
- Open a dedicated performance patch for the `/api/snapshot` size/latency (see §9).
- Leave the single Startup VBS as the sole auto-start path; do not add a scheduled task
  unless the user explicitly asks (would create a second, competing trigger).
