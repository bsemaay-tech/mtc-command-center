# MTC CLI handoff

## Current state — 2026-08-25

- WP-P0-05 changes onboarding only; CLI code and behavior are untouched.
- D002 remains the architectural decision: CLI is the agent-native writer surface and dashboards
  wrap it rather than duplicate business logic.
- No CLI implementation, canonical write, migration, host, broker, or live command is authorized by
  this handoff.

## [Claude lane D] 2026-09-07 — audit path repair (D9)

- `audit repo` no longer requires the two files 552a41ec moved to `_AI_MEMORY/history/`; the NEXT_STEPS
  check became a governance `00_AGENT_PROTOCOLS/HANDOFF.md` newest-section NEXT ACTION / WAITING FOR
  OWNER check; `run(repo_root=...)` added for fixtures. RED exit 2 -> GREEN 13 passed, CLI exit 0.

## [Claude Lead] 2026-09-07 — Gate-5 round-1 repair (gpt-5.6-sol REQUEST_CHANGES)

- **G3-01:** required set is now root `AGENTS.md`/`CONTEXT_MAP.md`/`DECISIONS.md`, the
  `00_AGENT_PROTOCOLS` five-file contract, `_AI_MEMORY/SESSION_LOCK.md` and `PROJECT_MEMORY.md`;
  compatibility pointers (`START_HERE`, `AI_RULES`, `ACTIVE_FILES`) are no longer required.
- **G3-02:** WAITING FOR OWNER presence/count are label-anchored (`**WAITING FOR OWNER**` or
  `WAITING FOR OWNER:`), same shape as NEXT ACTION; prose mentions no longer satisfy the check.
- **G3-03:** raw RED arms recorded (`C:/tmp/OVN_AUDIT_20260907/EV/G3_red_arms.log`): repaired tests
  vs pre-repair candidate 9 failed/27 passed; vs master 28 failed/8 passed. GREEN 36 passed; real
  CLI `audit repo` exit 0. Round-2 Sol audit dispatched.
- **NEXT ACTION:** land via PR after round-2 acceptance + Gemini corroboration + protected CI.
- **WAITING FOR OWNER:** Nothing.

## [Claude lane U] 2026-09-07 — audit nit repair

- No-ask tokens widened (`none`, `(none)`, `n/a`, `-`, `—`, empty); NEXT ACTION check label-anchored;
  newest-first ordering documented. RED 14 failed pre-fix -> GREEN 32 passed; CLI shape unchanged.
