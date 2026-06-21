# Dashboard Launcher Single-Instance Patch Audit - 2026-06-15

## 1. Executive verdict

**Verdict: ACCEPT WITH SMALL FOLLOW-UP**

The launcher now behaves as a single-instance read-only dashboard launcher. With one healthy server already bound to `127.0.0.1:8765`, two default invocations both logged `[skip] dashboard already running ... healthy read_only; skip launch`, exited cleanly, and left the strict MCC server process count at one `pythonw.exe`.

Small follow-up is warranted because `-StatusOnly` still appends a line to `08_DASHBOARD_APP/logs/dashboard_launcher.log` despite the advertised "No changes" behavior, and the patch report's startup-trigger statement is stale: this machine does have one user Startup VBS entry for the dashboard launcher.

## 2. Files inspected

- `08_DASHBOARD_APP/run_dashboard_server.ps1`
- `08_DASHBOARD_APP/START_DASHBOARD.bat`
- `08_DASHBOARD_APP/logs/dashboard_launcher.log`
- `08_DASHBOARD_APP/logs/dashboard_server.log`
- `11_TRIAGE/DASHBOARD_LAUNCHER_SINGLE_INSTANCE_PATCH_REPORT_2026-06-15.md`
- `11_TRIAGE/FIRST_PROFILE_RESULT_ARTIFACT_PILOT_REPORT_2026-06-15.md`
- `C:\Users\BarışSemaay\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\MTC_Command_Center_Dashboard.vbs`

Also inspected scheduled-task, Run-key, Startup-folder, current process, API, and protected-scope state.

## 3. Launcher chain verification

`08_DASHBOARD_APP/run_dashboard_server.ps1` is the persistent launcher. It targets:

- API directory: `08_DASHBOARD_APP/apps/api`
- executable: `C:\Python314\pythonw.exe`
- command: `pythonw -m mcc_readonly serve --host 127.0.0.1 --port 8765`
- logs: `08_DASHBOARD_APP/logs/dashboard_launcher.log` and `dashboard_server.log`

`08_DASHBOARD_APP/START_DASHBOARD.bat` remains a separate manual launcher using `python -m mcc_readonly`; it is not the persistent `pythonw ... serve` chain.

PowerShell parser check passed: `PARSE_OK`.

## 4. Single-instance guard verification

PASS. Default mode checks port `8765` before starting. If a listener exists and `/healthz` reports `mode=read_only`, it logs a skip message and exits `0`.

The supervisor loop also re-checks port ownership before each restart and exits if another healthy read-only instance owns the port. This addresses the previous churn pattern where repeat launchers kept attempting to bind an occupied port.

Default mode does not call `Stop-MccProcs`; it only warns and exits if the port is bound but unhealthy. Kill behavior is only reachable through explicit flags.

## 5. Repeated launch / process-count verification

Before repeated launch:

- `ProcessId 24720`
- `Name pythonw.exe`
- command line: `"C:\Python314\pythonw.exe" -m mcc_readonly serve --host 127.0.0.1 --port 8765`

Two default launcher invocations:

- `LAUNCH_1`: `[skip] dashboard already running (port 8765, pid 24720, healthy read_only); skip launch`
- `LAUNCH_2`: `[skip] dashboard already running (port 8765, pid 24720, healthy read_only); skip launch`

After repeated launch, strict process count remained one matching `pythonw.exe`. No duplicate server process was spawned.

## 6. StatusOnly / ForceRestart / KillStale behavior verification

`-StatusOnly` output:

- `port=8765`
- `listening=True`
- `ownerPid=24720`
- `healthy=True`
- `mcc_serve_procs=1`
- PID table containing `24720 pythonw.exe`

Issue: `-StatusOnly` routes through `Write-Launcher`, so it appends a `[status]` line to `dashboard_launcher.log`. That is a state change and conflicts with the documented "No changes" behavior if interpreted literally.

`-ForceRestart` and `-KillStaleMccOnly` were inspected but not executed. Their kill path is flag-gated and not reachable from default mode.

## 7. Kill-safety verification

PASS. The kill filter is strict:

- process name must be `python.exe` or `pythonw.exe`
- command line must contain `mcc_readonly`
- command line must contain word-boundary `serve`

`Stop-Process` is only called inside `Stop-MccProcs`, which is only invoked by `-ForceRestart` or `-KillStaleMccOnly`. Default launch and `-StatusOnly` do not kill processes.

## 8. Logging verification

PASS with one follow-up noted above.

`Limit-LogSize` caps logs at `262144` bytes and keeps the last 1000 lines when truncating. Current sizes:

- `dashboard_launcher.log`: 953 bytes
- `dashboard_server.log`: 74003 bytes

The skip launches only appended bounded launcher log lines. The server log still contains old churn entries, but the new skip path did not add new server churn.

## 9. Startup / scheduled task / Run key verification

Startup state:

- One user Startup entry exists: `MTC_Command_Center_Dashboard.vbs`
- Created/modified: `2026-06-15 11:49:31`
- Contents call:
  `powershell.exe -NoProfile -WindowStyle Hidden -NonInteractive -ExecutionPolicy Bypass -File "C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\08_DASHBOARD_APP\run_dashboard_server.ps1"`

No duplicate dashboard startup entry was found in the user Startup folder. No matching Run-key entry was found under the checked HKCU/HKLM Run keys.

Scheduled-task search found `MCC_Overnight_Monitor`, but its action targets `03_QUANTLENS\tools\monitor_overnight.ps1`; it is not the dashboard launcher.

Patch-report discrepancy: `DASHBOARD_LAUNCHER_SINGLE_INSTANCE_PATCH_REPORT_2026-06-15.md` says no dashboard auto-start was discoverable. Current machine state contradicts that: one Startup VBS exists and points at the new guarded launcher.

## 10. API/read-only verification

PASS.

- `/healthz`: HTTP 200, `mode=read_only`, `overall_ok=True`
- `POST /api/snapshot`: HTTP 405
- `/api/snapshot?refresh=1`: HTTP 200 with longer timeout

Operational note: one default snapshot request timed out at 20 seconds. Retrying with `-TimeoutSec 90` completed in 60.85 seconds and returned a 121,079,001-byte payload. This is not a write-safety failure, but it is a useful performance/size risk to track.

## 11. Test results

PASS.

- `node --check 08_DASHBOARD_APP\apps\web\app.js`: exit 0
- API tests from `08_DASHBOARD_APP\apps\api` with `PYTHONPATH=.`: `Ran 60 tests in 27.577s - OK`
- Launcher PowerShell parse check: `PARSE_OK`

Note: the patch report says 69 API tests passed. The current discovered suite run during this audit reported 60 tests.

## 12. Protected scope check

PASS for this launcher audit.

No tracked changes were reported under the checked protected execution paths:

- Pine pathspecs
- `MTC_V2` pathspecs
- `02_MTC_BACKTEST`
- `07_ADAPTERS`

No backtest was run. No broker/live/paper execution behavior was touched. API write behavior remains blocked.

Current repo state does contain one `backtest_profile_result.json` under:

`03_QUANTLENS/05_BACKTEST_RESULTS/pilot_profile_result_QL_2026-05-01_US_EQUITIES_10M_8EMA_PULLBACK_2026-06-16/backtest_profile_result.json`

That artifact is documented by `FIRST_PROFILE_RESULT_ARTIFACT_PILOT_REPORT_2026-06-15.md` as a separate pilot generated from existing source data, not by the launcher patch. No `top_results.json` was found.

## 13. Issues found

1. **StatusOnly is not fully no-change.** It appends to `dashboard_launcher.log`. If "StatusOnly makes no changes" is a strict contract, status output should avoid log writes or the documentation should say "no process/config changes."
2. **Patch report startup statement is stale.** The report says no dashboard auto-start exists, but current system state has one Startup VBS pointing at `run_dashboard_server.ps1`.
3. **Snapshot refresh is large/slow.** `/api/snapshot?refresh=1` passed but took 60.85 seconds and returned about 121 MB.
4. **Worktree remains broad/dirty.** `git status --short` still includes prior dashboard/API/report changes plus unrelated/untracked items. The launcher itself is untracked, so `git diff -- 08_DASHBOARD_APP/run_dashboard_server.ps1` shows no content.
5. **Current repo no longer has zero profile-result artifacts.** A separate pilot `backtest_profile_result.json` exists; it is not attributable to the launcher patch, but future audits should not rely on older "no profile result exists anywhere" assumptions.

## 14. Recommended next step

Apply a small follow-up to make `-StatusOnly` truly non-mutating or explicitly document that it writes a status log line. Update the launcher patch report or next handoff to reflect the actual single Startup VBS trigger. Then isolate/stage the launcher file and this audit/report set separately from unrelated dirty worktree items before final release review.
