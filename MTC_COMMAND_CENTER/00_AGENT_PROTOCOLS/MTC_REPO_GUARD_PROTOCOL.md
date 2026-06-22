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
