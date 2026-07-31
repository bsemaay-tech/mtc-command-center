# INCIDENT — Day 1 v1 monitoring window stopped by system sleep — 2026-07-20

Recorded by: Claude Fable 5 (found during TS-P0 repair audit; bridge API returned empty)

## Timeline (local time, +03:00; evidence from Task Scheduler Operational log — now
enabled per the 2026-07-16 decision — plus Kernel-Power events and the bridge log)

| Time | Evidence | Meaning |
| --- | --- | --- |
| 2026-07-19 21:50:25 | window record | Day 1 v1 opened; run `paper-20260719185026`; ARM 21:52 |
| 2026-07-19 23:10 (20:10Z) | `/api/status` | Last verified healthy: ARMED, reconcile fresh |
| 2026-07-20 07:17:41 | `bridge_20260719.log` last write | Bridge still alive |
| 2026-07-20 07:27:29 | TaskScheduler 201/102 | Task instance COMPLETED (supervisor died — no exit line in bridge log) |
| 2026-07-20 07:27:50 | Kernel-Power 42 | System entered sleep |
| 2026-07-20 08:57:27 | Kernel-Power 506/507 | Modern-standby exit |
| 2026-07-20 08:57:44 | TaskScheduler 119/100/129/200 | Task RESTARTED on user logon (PID 71004) |
| 2026-07-20 08:58:50 | TaskScheduler 201/102 | That instance COMPLETED too — died after ~66s; task result `0xC000013A` (console close) |
| audit time (~12:00) | Get-ScheduledTask + process list | Task `Ready`, no `bridge.app` process, port 8790 dead |

## Assessment

- Root cause: **system sleep** (lid close / standby), same failure family as the
  2026-07-16 battery incident but via sleep, which `StopIfGoingOnBatteries=False` does
  not and cannot prevent. The 08:57 logon-trigger restart then died within ~66s —
  consistent with a second standby cycle (`0xC000013A`).
- NOT related to any TS-P0/TSP0 session activity: the bridge outlived the Codex repair
  session by hours; no session touched P2RT, the scheduler, or bridge processes
  (P2RT porcelain clean at `008e065e` throughout).
- DB state: bridge dies fail-closed by design; no exposure expected (verify positions/
  orders on restart via normal reconcile).

## Window ruling (honest-window discipline)

Day 1 v1 continuous-window evidence ends at the sleep stop (~07:27 local, ~04:27Z).
Elapsed ARMED window: ~21:52 local (18:52Z) → ~07:27 local ≈ **9h35m**, minus nothing
(no earlier gap). The ~66s zombie restart at 08:57 does not extend it. Under TS-P0-003
semantics (built, not yet deployed) this is exactly an INTERRUPTED window; it must not
be presented as continuous soak beyond 07:27. Evidence categories: connectivity /
scheduler-reliability evidence YES (another real-world stop mode captured);
risk-gate-enforcement evidence only for the ~9.5h armed span.

## Decisions needed from Barış

1. **Restart Day 1 v2 window?** (Start-ScheduledTask + one ARM — same runbook as Day 1
   v1. Not done unilaterally; runtime actions stay owner-gated.)
2. **Sleep policy for the monitoring machine:** the task cannot survive sleep. Options:
   keep PC awake during windows (power settings / lid policy), accept interrupted
   windows until the VPS migration (end of month), or move the definitive window to VPS
   as already planned. Recommendation: treat local windows as validation-tier only (as
   already decided for D3) and prioritize VPS.
3. Optional: add wake/resume detection to the supervisor (restart-on-resume) — would be
   a small scheduler/task change, needs approval since it touches the runtime task.

## Boundary confirmation

No restart/ARM/scheduler modification performed by this session. Evidence gathering was
read-only (event logs, task info, process list, one status GET).
