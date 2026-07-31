# INCIDENT — P2 bridge stopped by scheduled-task battery policy (2026-07-16)

Recorded: 2026-07-18 (Claude Fable 5, from Barış-supplied investigation results).
Status: root cause identified with high confidence; no runtime action taken; monitoring window RESET.

## Summary

The Day 0 v5 monitoring window (ARM at `2026-07-16T13:41:26.908952Z`) did not survive to the
planned 2026-07-18 PC-off boundary. The bridge process was stopped automatically by Windows Task
Scheduler when the machine switched to battery power. This was not a manual shutdown, not a code
failure, and not an exchange/feed incident.

## Evidence (as investigated 2026-07-18)

- Scheduled task `MTC-Bridge-P2` has `StopIfGoingOnBatteries = true`.
- Bridge log ends around 2026-07-16 17:32 (local; timezone not explicitly recorded).
- Windows `Kernel-Power` event 105 recorded `AcOnline = false` at 17:33:46.
- Task last result: `0x8007042B` (HRESULT for Win32 error 1067, "the process terminated
  unexpectedly" — consistent with the scheduler killing the process).
- Task Scheduler history was disabled, so the exact task-termination event is unavailable; the
  correlation above is the strongest available evidence.
- Roadmap baseline (2026-07-17, read-only) independently observed: no listener on port 8790,
  `/api/status` timeout, task state `Ready` — consistent with a stop on 2026-07-16 and no restart.

## Impact

- **Day 0 v5 window is CLOSED/RESET.** It ran from `2026-07-16T13:41:26.908952Z` until the
  battery stop (~17:32 local on 2026-07-16). It cannot be cited as an uninterrupted soak window.
- No trading impact expected: run was testnet/paper; prior daily checks showed positions/orders
  `[]`/`[]`. Current exchange/DB state was NOT queried for this note (read-only, no runtime action).
- There is currently **no active monitoring window**.

## Follow-ups (require approval; none executed)

1. **Scheduler policy change (Barış approval required — runtime config):** set
   `StopIfGoingOnBatteries = false` (and review `DisallowStartIfOnBatteries`) on `MTC-Bridge-P2`,
   or accept battery stops as window boundaries. Moot on the planned VPS deployment.
2. **Enable Task Scheduler history** so future terminations are directly attributable.
3. Next window start requires the standard deploy/ARM approval path; nothing here authorizes it.
4. Per Barış decision 2026-07-18: the next risk-control monitoring window must not start before
   the expedited interim TS-P1-007 wiring (daily-loss / consecutive-loss gates are currently inert
   through the operational engine path — see `09_DOCS/ROADMAPS/TRADING_SYSTEM/05_IMPLEMENTATION_BACKLOG.md`
   amendment log and GLOBAL_HANDOFF 2026-07-18).
