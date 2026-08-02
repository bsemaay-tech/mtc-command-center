---
name: mtc-repo-guard
description: Use whenever a task touches the MTC Command Center repo - any git, branch, commit, stage, push, merge, audit, cleanup, worktree, or handoff action, and any work on the dashboard, QuantLens, Strategy Intelligence web app, Pine, MTC_V2, backtest, or optimization. Loads the repo guard rules so changes are safe-by-default and hard to misuse. Not for non-repo questions.
user-invocable: true
argument-hint: "[preflight | precommit | premerge]"
license: Apache 2.0
allowed-tools:
  - Bash(git status*)
  - Bash(git diff*)
  - Bash(git log*)
  - Bash(git rev-list*)
  - Bash(pwsh -File *repo_guard.ps1*)
---

# MTC Repo Guard

Make MTC repo work automatic and hard to misuse. Before any repo change, follow the canonical
protocol: `MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/MTC_REPO_GUARD_PROTOCOL.md`.

## Always

1. **Never edit on `master`** - branch first (`feature/<scope>`).
2. **Audit first** - run the dry-run guard and read-only git checks; confirm scope before editing.
3. **Exact staged files only** - explicit paths, **never `git add .` / `-A`**; verify
   `git diff --cached --name-only` equals the intended set.
4. **Protected scopes need Barış approval:** `02_MTC_BACKTEST`, `07_ADAPTERS`, `01_PINE`, `MTC_V2`.
5. **No execution without approval:** backtests, optimizations, servers, launchers, artifact
   generation, `top_results.json`, broker/live/paper actions.
6. End with the protocol's **final report format**.

## Run the guard (dry-run, read-only)

```
pwsh -File MTC_COMMAND_CENTER/tools/repo_guard.ps1
```

Use at **preflight**, **before commit**, and **before merge**. Proceed only on `PASS`; on
`BLOCKED`, fix the reported item and re-run. Full command set:
`MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/MTC_REPO_GUARD_USAGE.md`.
