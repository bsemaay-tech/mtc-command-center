# Overnight Lessons — 2026-07-02 (resilient run: A25/A26 resilience, full universe 0 robust)

**Run:** `overnight_resilient_2026-07-02_2100.ps1`, 20 workers (cpu_count), 21:03→22:44 (~1h42m),
zero crashes, machine released. Queue: STG001/STG002 confirmation → 8-variant family → finished the
18:30-interrupted v2 23-strategy sweep → deep CPCV+PBO. **11,781 new cells + heavy tier. robust_final 0
everywhere.**

## G1 — resilience worked; the 18:30 crash-and-idle was NOT repeated
Earlier the same evening, the 18:30 scheduled run's orchestrator **died mid-Stage-A (~19:00) and stayed
dead ~2h** (machine idle) because the orchestrator had no crash-restart. Tonight's run added per-stage
retry + an external watchdog Task + a PID lockfile, and ran clean end-to-end; the watchdog logged
"run complete — nothing to do" every 15 min with zero false relaunches. Unattended overnight runs need
**external** liveness recovery, not just in-process retry.

## A25 (NEW) — unattended overnight orchestrator MUST have crash-restart + external watchdog
An orchestrator that `& python`-blocks per stage dies silently if the process is killed (sleep, OOM,
crash) and does not come back → wasted night. **Fix:** (1) per-stage RETRY loop (checkpoint-resume makes
retries cheap); (2) an external Windows Task Scheduler **watchdog** (every ~15 min) that relaunches the
orchestrator if it is dead — this survives the orchestrator process dying AND the AI session ending;
(3) a Startup reboot hook for power loss. In-process retry alone is insufficient (it dies with the
process).

## A26 (NEW) — watchdog liveness via CommandLine matching is FLAKY → use a PID lockfile
The first watchdog checked `Get-CimInstance ... CommandLine -match <script>`. CommandLine can be null /
unmatched transiently, so the watchdog false-positively judged a LIVE orchestrator dead and launched a
**second** instance → two orchestrators writing the same `--resume` checkpoint = corruption risk. **Fix:**
the orchestrator writes its `$PID` to `orchestrator.lock` at start and refuses to run if the lock's PID
is alive (single-instance); the watchdog relaunches only when the lock PID is dead (`Get-Process -Id`).
PID-liveness is robust where CommandLine matching is not.

## G4 — complete executable universe now validated: 0 robust; micro-price crypto artifact at scale
The 23 v2 strategies were swept on multiasset for the FIRST time (8211 cells) + 8 new variants (2856) +
STG001/STG002 finer confirmation (714). **robust_final 0 in all of them.** Combined with the 06-29 mega
20, the **entire executable library (~51 archetypes) is non-robust on this universe.** Every eye-catching
return is a **micro-price crypto compounding artifact** (SHIBUSD +12153%/+7875%, DOGEUSD, UNIUSD; dsr≈0
or STRONG_PASS-but-not-robust) — the C8 short-trap/compounding family, now dominating leaderboards at
scale. **Action:** exclude or winsorize/cap micro-price assets in future sweeps so top lists are
readable. **Path forward:** genuinely-new strategy LOGIC (new archetypes), not more variants/grids on
the existing families — those are conclusively non-robust.

## A24 confirmed — enumerate the full backlog, release only when exhausted
Unlike 07-01 (stopped at 31 min), tonight enumerated the full genuinely-new backlog (STG + variants +
v2 completion + heavy = 11,781 cells) and released at 22:44 only after it was exhausted. The remaining
~10h to 08:30 is NOT fillable with valid deterministic compute — that needs new-strategy R&D (design),
not more sweeps.

## Artifacts
`overnight_resilient_2026-07-02/` + `overnight_full_2026-07-02/stageA_v2_multiasset/` (git-ignored).
Runners + variants + watchdog on `feature/strategy-param-specs` (PR #15). Nothing promoted; no
profile_result/top_results fabricated.
