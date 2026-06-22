# MTC Repo Guard — Usage

Dry-run guard. Read-only; never modifies files. Run from repo root.

## Preflight (start of any task)

```powershell
cd C:\LAB\Tradingview_LAB_CLEAN
pwsh -File MTC_COMMAND_CENTER\tools\repo_guard.ps1
```

Confirms: not on `master`, clean/known dirty set, no protected-scope edits, no risky untracked
files. Branch first if it reports working on `master`.

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
