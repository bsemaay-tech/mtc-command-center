# MTC Repo Guard Protocol

Canonical, short rules every agent follows for **any** repo change in MTC Command Center.
Companion to [`CLEAN_WORKTREE_AND_PUSH_PROTOCOL.md`](CLEAN_WORKTREE_AND_PUSH_PROTOCOL.md)
(how to push) and [`NO_PROMOTION_SAFETY_RULES.md`](NO_PROMOTION_SAFETY_RULES.md) (what not to
promote). This file is the **single entry rule set**; those two carry the detail.

## Rules (non-negotiable)

1. **Never work directly on `master`.** Branch first: `git checkout -b feature/<scope>`.
2. **Audit first.** Run read-only checks and confirm scope before editing anything.
3. **Exact staged files only.** Stage each path explicitly. **No `git add .` / `git add -A`.**
4. **Verify the index** before commit: `git diff --cached --name-only` must equal the intended
   set exactly. If unexpected paths appear → stop, report `BLOCKED`.
5. **No protected-scope changes without explicit Barış approval:**
   `MTC_COMMAND_CENTER/02_MTC_BACKTEST`, `07_ADAPTERS`, `01_PINE`, `MTC_V2`.
6. **No execution without explicit approval:** backtests, optimizations, servers, launchers,
   artifact generation, `top_results.json`, broker/live/paper actions.
7. **No force-push. No unrelated user files. No silent file delete/move.**
8. **Risky untracked files (launchers, `top_results.json`, `*_server.ps1`, `*.log`) are WARN,
   not BLOCK** — by design. Rule 3 (exact staged files only) already stops them reaching a
   commit; the warning just flags leaked local artifacts so you keep them out of the repo.

## Branch freshness

The guard checks the branch merge-base against local `origin/master` only: it is offline, never
fetches, and reports the local ref's commit age. More than 30 commits behind is BLOCKED by default.
Set the limit with `-MaxBehindCommits <n>` or, if that parameter is absent, the
`MTC_REPO_GUARD_MAX_BEHIND_COMMITS` environment variable. `-WarnOnlyStaleBranch` changes stale
to WARN for diagnostics. When BLOCKED stale, recreate the worktree from current `origin/master`
per [`CLEAN_WORKTREE_PROCEDURE.md`](../11_TRIAGE/WP_P0_15_FRESHNESS_2026-08-24/CLEAN_WORKTREE_PROCEDURE.md),
or rebase.

## Final report format (every task ends with this)

```
branch:            <name>
files changed:     <exact list>
checks run:        <commands>
guard:             PASS | BLOCKED (<reason>)
commit:            <hash | none>
pushed:            yes | no
remaining dirty:   <list | none>
next action:       <one line>
```

## Enforcement

Run `MTC_COMMAND_CENTER/tools/repo_guard.ps1` (dry-run) at preflight, before commit, and before
merge. See [`MTC_REPO_GUARD_USAGE.md`](MTC_REPO_GUARD_USAGE.md).
