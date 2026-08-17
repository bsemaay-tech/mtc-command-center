# Phase-watch Hermes env scrub — D026 RED/GREEN record — 2026-08-17

**Repair (owner instruction 2026-08-17, item 1):** hermes.exe must be launched with
`TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` explicitly removed from the child
environment; values never read or printed.

**Implementation:** `Invoke-SanitizedProcess` in
`C:\LAB\HERMES_WATCH\phase_watch_check.ps1` — `System.Diagnostics.ProcessStartInfo`
with `EnvironmentVariables.Remove(<name>)` for both names (removal by NAME; a
`StringDictionary.Remove` never reads the value), redirected stdout/stderr, 10-min
timeout kill. The Hermes invocation path (`Invoke-HermesBounded`) uses this
launcher exclusively. A `-EnvProbe` switch runs the demo through the REAL launcher
— not a reimplementation (D026 discipline: invoke the mechanism under audit).

**Stub (harmless, presence booleans only, never values):**
`C:\LAB\HERMES_WATCH\env_probe_stub.ps1`:

```powershell
"STUB TELEGRAM_BOT_TOKEN present: $([bool]$env:TELEGRAM_BOT_TOKEN)"
"STUB TELEGRAM_CHAT_ID present: $([bool]$env:TELEGRAM_CHAT_ID)"
```

**Command executed (2026-08-17, parent process verified to carry both names —
presence booleans only):**

```
powershell.exe -NoProfile -ExecutionPolicy Bypass -File C:\LAB\HERMES_WATCH\phase_watch_check.ps1 -EnvProbe
```

**Real output, verbatim:**

```
RED - ordinary child (inherits parent environment):
STUB TELEGRAM_BOT_TOKEN present: True
STUB TELEGRAM_CHAT_ID present: True
GREEN - sanitized launch path (Invoke-SanitizedProcess, same function hermes uses):
STUB TELEGRAM_BOT_TOKEN present: False
STUB TELEGRAM_CHAT_ID present: False
```

**Reading:** RED shows the defect is real — an ordinary child inherits both names.
GREEN shows the sanitized path (the exact function the hermes launch uses) strips
both. No credential value was read, displayed, or logged at any step; the demo
deals in presence booleans only.

**Regression check after the wrapper changes:** parse errors 0; a normal cron run
logged `PENDING - watch inactive (PHASE: 0-PRE-DEPLOY, checklist from
origin/master). No AI call.` — behavior unchanged. No Telegram message was sent
during any of this (the one delivered TEST message of 2026-08-16 23:48:18 remains
the only send).

**D026 status:** RED demonstrated against the real inheriting path, GREEN with the
fix, commands and real output recorded above → qualifies as closure evidence for
the child-inheritance sub-item of T0 finding 6. Independent verification by the T0
reviewers is still required before the notifier is called accepted.
