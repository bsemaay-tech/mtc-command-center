# Dashboard Launcher Single-Instance Patch — Report — 2026-06-15

## 1. Executive summary
The read-only dashboard launcher (`08_DASHBOARD_APP/run_dashboard_server.ps1`) had no
single-instance guard. Root cause of the ~150-process pile-up is now confirmed from
`logs/dashboard_server.log`: the `while($true)` supervisor restarted `pythonw -m mcc_readonly
serve` every 5s, but when port 8765 was **already bound** by a live instance each new
`pythonw` failed to bind and exited in the **same second** — an endless churn. Multiple
launcher copies (one per manual/logon start, no guard) raced for the port and accumulated.

Patched the launcher to be **idempotent**: before starting it checks whether port 8765 is
already listening and `/healthz` reports `mode=read_only`; if so it logs
`already running; skip launch` and exits 0. The supervised restart loop now also re-checks
the port each iteration and exits cleanly instead of churning when another healthy instance
owns the port. Added `-StatusOnly`, `-ForceRestart`, `-KillStaleMccOnly` flags, a bounded
launcher log, and a strict kill filter that can only ever target `python`/`pythonw`
processes whose command line contains both `mcc_readonly` and `serve`.

Verified: repeated launcher calls do not spawn duplicates (process count stays at 1), API
stays read-only (`POST → 405`), `/healthz` and `/api/snapshot?refresh=1` both 200, all 69
API tests pass. No protected execution path touched.

## 2. Preflight worktree scope
`git status --short` / `git diff --stat` run (read-only; nothing cleaned/reset/staged).
Working tree already carried prior accepted dashboard work (app.js / index.html / styles.css
modified; new schemas, tools, tests, and 11_TRIAGE reports untracked). The launcher
`run_dashboard_server.ps1` was **untracked** (status `??`) before this patch. This patch
touches only the launcher and adds this report; no source/data/contract file changed.

## 3. Launcher chain discovered
- `08_DASHBOARD_APP/run_dashboard_server.ps1` — persistent supervisor; `while($true)` →
  `& pythonw -m mcc_readonly serve --host 127.0.0.1 --port 8765`; logs to
  `logs/dashboard_server.log`. **This is the real server launcher.**
- `08_DASHBOARD_APP/START_DASHBOARD.bat` — manual one-click (`python -m mcc_readonly` +
  `pause`); interactive, not the persistence path. Left unchanged.
- `03_QUANTLENS/tools/monitor_overnight.ps1` (scheduled task `MCC_Overnight_Monitor`,
  every 30 min) — independent overnight **health monitor**; does NOT launch the dashboard.
- **No discoverable auto-start for the dashboard:** the launcher header comments reference a
  scheduled task `MTC_Command_Center_Dashboard`, but that task does not exist. Scanned all
  scheduled tasks, `HKCU`/`HKLM` `...\Run` keys, and per-user + all-users Startup folders —
  none start `run_dashboard_server.ps1`. No `.vbs` launcher exists anywhere in the repo.
  Conclusion: the supervisor is currently started **manually**; on this machine there is no
  active logon trigger, so the historical pile-up came from repeated manual starts each
  spawning an unguarded loop.

Runtime state at patch time: one healthy `pythonw` (PID 24720) bound to 8765
(`/healthz` `overall_ok:true`, `mode:read_only`); one stale supervisor loop was still
churning and has since exited.

## 4. Files changed
- `08_DASHBOARD_APP/run_dashboard_server.ps1` — rewritten with single-instance guard, flags,
  strict kill filter, port-aware supervised loop, bounded logs.
- `11_TRIAGE/DASHBOARD_LAUNCHER_SINGLE_INSTANCE_PATCH_REPORT_2026-06-15.md` — this report.
- `_AI_MEMORY/*` handoff files updated.

No changes to Pine, MTC_V2, backtest engine, broker/live/paper execution, API write
behavior, data contracts, profile-result artifacts, or strategy logic.

## 5. Single-instance guard behavior
Default (no flags):
1. Truncate oversized logs (bounded, see §7).
2. `Get-PortOwner` → is 8765 listening? (`Get-NetTCPConnection`, TcpClient probe fallback).
3. If listening **and** `/healthz` `mode=read_only` → log `[skip] already running …`, exit 0.
4. If listening but **not** healthy → log `[warn] … not killing. Use -ForceRestart`, exit 0
   (never auto-kills an unknown owner).
5. If free → enter supervised loop. Each iteration re-checks the port first; if another
   healthy instance has taken it, log `[skip] … exiting supervisor` and exit 0 (kills the
   5s churn). Otherwise start one server (blocks); on exit, if the port is now held by a
   healthy instance, exit cleanly instead of retrying.

## 6. Status / ForceRestart / KillStale behavior
- `-StatusOnly` — reports `port`, `listening`, `ownerPid`, `healthy`, matching
  `mcc_serve_procs` count + PID table. No changes. Exit 0.
- `-ForceRestart` — stops **all** strictly-matched MCC server processes, waits 2s, then
  starts a fresh supervised instance. Use to deliberately replace a running/stale server.
- `-KillStaleMccOnly` — stops matched duplicate MCC server processes **except** the healthy
  port owner; reports `matched` / `killed_count`; does not start. Cleanup-only mode.

Kill safety (all modes): `Stop-MccProcs` only acts on processes where
`Name ∈ {python.exe, pythonw.exe}` **and** `CommandLine ~ mcc_readonly` **and**
`CommandLine ~ \bserve\b`. No other process can be stopped; unrelated Python is never
touched. The `powershell` supervisor process itself is intentionally **not** a kill target.

## 7. Logging behavior
- `logs/dashboard_launcher.log` — one bounded line per launcher action
  (`skip` / `start` / `warn` / `force-restart` / `kill-stale` / `kill-fail` / `status`) with
  ISO timestamp + port/healthz/PID detail.
- `logs/dashboard_server.log` — retained for server start/exit lines.
- Both truncated at startup to the last 1000 lines when over 256 KB (`Limit-LogSize`) —
  fixes the prior unbounded growth (the server log had reached ~481 KB / 6505 lines from the
  5s churn). No heavy logging infrastructure added.

## 8. Process-count verification
- `-StatusOnly`: `port=8765 listening=True ownerPid=24720 healthy=True mcc_serve_procs=1`.
- Two consecutive default launches → both logged `[skip] dashboard already running …`,
  exit 0; **no new `pythonw` spawned**.
- Strict count after the test: `python mcc serve count: 1`; total `pythonw` on machine: `1`.
- The historical churn loop (old supervisor) has exited; no pile-up remains.

## 9. Dashboard / API validation
- `/healthz` → 200, `overall_ok:true`, `mode:read_only`.
- `/api/snapshot?refresh=1` → 200.
- `POST /api/snapshot` → **405** (write API still blocked).

## 10. Tests run
- `node --check 08_DASHBOARD_APP/apps/web/app.js` → **JS_OK**.
- `python -m unittest discover tests` (apps/api) → **Ran 69 tests … OK**.
- PowerShell parse check of the launcher (`Parser::ParseFile`) → **PARSE_OK**.

## 11. Safety confirmation
No backtest, optimization, or artifact generation. No Pine / MTC_V2 / backtest engine /
broker / live / paper execution touched. No POST/PUT/PATCH/DELETE behavior added; API
remains read-only (POST→405 verified). Kill logic is strictly scoped to MCC `mcc_readonly
serve` Python processes; default mode never kills anything. No startup entries created or
deleted automatically.

## 12. Remaining limitations
- The supervisor still relies on an external trigger to (re)start it after a real crash;
  with the old churn loop gone there is currently no automatic restarter running. See §13.
- `Get-PortOwner` PID detection uses `Get-NetTCPConnection`; on hosts where that is
  unavailable it falls back to a connect probe that confirms "listening" but returns PID
  `-1` (unknown). Guard/skip logic still works (healthz-gated); only the logged PID is
  unknown in that fallback.
- A single-element function return unrolls in PowerShell; call sites wrap `@(...)` so
  `.Count` is reliable (fixed during validation after StatusOnly first reported a blank
  count).

## 13. Manual user actions
- **No duplicate startup entries were found to remove** — there is currently no auto-start
  trigger for the dashboard. If you want the dashboard to start automatically at logon,
  register **one** guarded entry that calls this launcher (it self-skips if already
  running), e.g. a scheduled task:
  `powershell.exe -NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File
  "…\08_DASHBOARD_APP\run_dashboard_server.ps1"`. Creating that task is a persistent-config
  change and is left for you to do (not auto-created by this patch). Do **not** add more than
  one such trigger.
- The launcher header comment naming task `MTC_Command_Center_Dashboard` is stale (no such
  task exists); ignore it or register the single task above.

## 14. Recommended next phase
- If auto-start is desired, register the single guarded scheduled task (above) and confirm
  via `-StatusOnly` that only one instance runs after logon.
- Optionally add a lightweight watchdog (or rely on the scheduled task's repetition) to
  re-invoke the guarded launcher periodically — it is now safe to call repeatedly.
- Resume product work (e.g. native US-equities-10m profile-result regeneration) from
  NEXT_STEPS once ops is stable.
