# Clean Worktree and Push Protocol

Use this workflow before handing the repo to another agent through GitHub.

## Standard Workflow

1. Preflight.
2. Classify dirty files.
3. Stage exact files only.
4. Verify staged set.
5. Run protected scope checks.
6. Commit small logical units.
7. Push.
8. Verify branch is not ahead.
9. Create a handoff summary.

## Commands

```powershell
git status --short
git status -sb
git diff --cached --stat
git diff --cached --name-only
git diff --name-only -- MTC_COMMAND_CENTER/02_MTC_BACKTEST MTC_COMMAND_CENTER/07_ADAPTERS MTC_COMMAND_CENTER/01_PINE MTC_COMMAND_CENTER/MTC_V2
git diff --cached --name-only -- MTC_COMMAND_CENTER/02_MTC_BACKTEST MTC_COMMAND_CENTER/07_ADAPTERS MTC_COMMAND_CENTER/01_PINE MTC_COMMAND_CENTER/MTC_V2
git push
git status -sb
```

## Rules

- Do not stage by directory when the worktree is broad or dirty.
- Do not stage unrelated user files.
- Do not commit until `git diff --cached --name-only` matches the intended set exactly.
- Do not push before verifying the commit log and staged diff.
- Do not force-push.
- If the index is not empty at preflight, stop and report `BLOCKED - INDEX NOT EMPTY`.

## Protected Scope Check

The protected scope commands must return no unexpected files. Any Pine, MTC_V2, parity, broker/live/paper execution, or backtest engine execution change requires explicit user approval before staging.
