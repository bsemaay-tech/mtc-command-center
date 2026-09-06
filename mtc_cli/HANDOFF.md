# MTC CLI handoff

## Current state — 2026-08-25

- WP-P0-05 changes onboarding only; CLI code and behavior are untouched.
- D002 remains the architectural decision: CLI is the agent-native writer surface and dashboards
  wrap it rather than duplicate business logic.
- No CLI implementation, canonical write, migration, host, broker, or live command is authorized by
  this handoff.

## [Claude lane D] 2026-09-07 — audit path repair

- **Changes:** `mtc_cli/commands/audit.py` required-memory-files check dropped the two files
  commit 552a41ec (2026-08-25) moved to `_AI_MEMORY/history/` (`GLOBAL_HANDOFF.md`,
  `NEXT_STEPS.md`) and now checks the router-era current-state set instead: root `AGENTS.md`,
  `CONTEXT_MAP.md`, `DECISIONS.md`, `_AI_MEMORY/{START_HERE,AI_RULES,PROJECT_MEMORY,
  ACTIVE_FILES,SESSION_LOCK}.md`, and `00_AGENT_PROTOCOLS/HANDOFF.md`. Replaced the
  NEXT_STEPS-stale-in-progress check (silently passed once that file moved) with a check that
  the governance `00_AGENT_PROTOCOLS/HANDOFF.md` newest section (split on `## `) carries a
  `NEXT ACTION` line and a `WAITING FOR OWNER` line; a missing file or missing line is an ERROR
  finding, never a silent pass. Added `run(repo_root=...)` so tests can point the checks at a
  fixture tree; default call path (`repo_root=None`) is unchanged and still honors the existing
  `REQUIRED_MEMORY_FILES` monkeypatch test. No command/flag/exit-code contract change; CLI stays
  read-only.
- **Evidence:** RED — real CLI: `python -m mtc_cli audit repo` exit 2, findings
  `missing: MTC_COMMAND_CENTER/_AI_MEMORY/GLOBAL_HANDOFF.md` and `.../NEXT_STEPS.md`; 5 new
  regression tests failed against pre-fix `audit.py` (`TestRouterEraLayout`, via `git stash`).
  GREEN — `python -m pytest mtc_cli/tests -q`: 13 passed; real CLI: `python -m mtc_cli audit repo`
  exit 0, `memory_files_ok: True`, `handoff_next_actions: 1`, `handoff_waiting_for_owner: 0`,
  no findings. `git diff --check` clean.
- **NEXT ACTION:** open a PR from this worktree branch for protected-CI review; no further
  mtc_cli audit work pending from this task.
- **WAITING FOR OWNER:** Nothing.
