# MTC Repo Guard — Usage

Dry-run guard. Read-only; never modifies files. Run from repo root.

## Preflight (start of any task)

```powershell
cd C:\LAB\Tradingview_LAB_CLEAN
pwsh -File MTC_COMMAND_CENTER\tools\repo_guard.ps1
```

Confirms: not on `master`, clean/known dirty set, no protected-scope edits, no risky untracked
files. Branch first if it reports working on `master`.

## Branch freshness

The guard works offline against the locally known `origin/master`; it never fetches and prints
that ref's commit age. A branch is stale when its merge-base is more than 30 commits behind.
Override the limit with `-MaxBehindCommits <n>` or, when that parameter is absent,
`MTC_REPO_GUARD_MAX_BEHIND_COMMITS`. Use `-WarnOnlyStaleBranch` only for a diagnostic PASS with
a warning. If stale blocking fires, recreate the worktree from current `origin/master` using
[`CLEAN_WORKTREE_PROCEDURE.md`](../11_TRIAGE/WP_P0_15_FRESHNESS_2026-08-24/CLEAN_WORKTREE_PROCEDURE.md),
or rebase the branch.

## Before commit

```powershell
git status --short
git diff --cached --stat
git diff --cached --name-only
pwsh -File MTC_COMMAND_CENTER\tools\repo_guard.ps1
```

Stage exact files only (no `git add .`). The staged set must equal the intended set.

## Before merge / push

```powershell
pwsh -File MTC_COMMAND_CENTER\tools\repo_guard.ps1
git log --oneline origin/<branch>..HEAD
```

Proceed only on `PASS`. On `BLOCKED`, fix the reported item and re-run.

See [`MTC_REPO_GUARD_PROTOCOL.md`](MTC_REPO_GUARD_PROTOCOL.md) for the rules the script enforces.
