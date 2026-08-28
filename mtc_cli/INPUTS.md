# MTC CLI inputs

- Exact command contract, arguments, exit codes, schema/version, target canonical path, and allowed
  mutation boundary.
- Relevant schemas under `MTC_COMMAND_CENTER/06_SCHEMAS/`, status/registry write protocols, and
  command allowlist.
- For any write: record branch, worktree, exact paths and live-dependency status; check
  `_AI_MEMORY/SESSION_LOCK.md` as mirror/history. Work reaches `master` only through a PR with
  `Bridge suite (Python 3.12)` green on an up-to-date head (ruleset 21444962, no bypass).
  **2026-08-26:** mandatory GitHub-issue claim retired per owner decision 6.
- Root `DECISIONS.md`, especially D002; explicit owner authority for any protected/operational path.

Use secret-free fixtures and isolated temp destinations for tests.
