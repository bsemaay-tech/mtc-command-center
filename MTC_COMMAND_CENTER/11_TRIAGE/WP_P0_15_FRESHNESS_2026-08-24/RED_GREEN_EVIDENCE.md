# WP-P0-15 D026 RED/GREEN Evidence

Date: 2026-08-24. All commands were executed locally and offline. The source worktree was
`C:\WPP015_20260824`; the only demo worktree was `C:\WPP015_TMP_STALE` on the temporary branch
`tmp/wp-p0-15-stale-demo-20260824`.

The old commit selected for the stale branch was
`3bfe62a5ecb1f61bbac7f4dbdeef0239884adb8f`, which was 528 commits behind the locally known
`origin/master` tip `fbb05d7f46bc78b2875aa6d029e7fb2f2a8b14d7`.

## Fixture creation

Working directory: `C:\WPP015_20260824`.

```powershell
git worktree add -b 'tmp/wp-p0-15-stale-demo-20260824' 'C:\WPP015_TMP_STALE' '3bfe62a5ecb1f61bbac7f4dbdeef0239884adb8f'
Write-Output "WORKTREE_ADD_RC=$LASTEXITCODE"
git -C 'C:\WPP015_TMP_STALE' status --porcelain
Write-Output "STALE_STATUS_RC=$LASTEXITCODE"
git -C 'C:\WPP015_TMP_STALE' rev-parse HEAD
git -C 'C:\WPP015_TMP_STALE' branch --show-current
$base = (git -C 'C:\WPP015_TMP_STALE' merge-base HEAD origin/master).Trim()
git -C 'C:\WPP015_TMP_STALE' rev-list --count "$base..origin/master"
```

Real output (Git's repetitive checkout progress lines omitted; the terminal state is retained):

```text
Preparing worktree (new branch 'tmp/wp-p0-15-stale-demo-20260824')
HEAD is now at 3bfe62a5 test(wpl-p2): audit 5 doc-closure kickoff + milestone log
WORKTREE_ADD_RC=0
STALE_STATUS_RC=0
3bfe62a5ecb1f61bbac7f4dbdeef0239884adb8f
tmp/wp-p0-15-stale-demo-20260824
528
```

The empty output before `STALE_STATUS_RC=0` is the real `git status --porcelain` result.

## RED: exact pre-change guard does not detect the stale branch

Working directory: `C:\WPP015_TMP_STALE`. The command loads the guard directly from the exact
pre-change Git object into memory; it does not run the stale worktree's own file by assumption.

```powershell
git -C 'C:\WPP015_20260824' rev-parse 'fbb05d7f:MTC_COMMAND_CENTER/tools/repo_guard.ps1'
powershell.exe -NoProfile -ExecutionPolicy Bypass -Command '$source = @(git -C "C:\WPP015_20260824" show "fbb05d7f:MTC_COMMAND_CENTER/tools/repo_guard.ps1"); if ($LASTEXITCODE -ne 0) { exit 99 }; $script = [scriptblock]::Create(($source -join [Environment]::NewLine)); & $script'
Write-Output "RED_RC=$LASTEXITCODE"
```

Real output:

```text
75ff5e3b3afb030291bfeb95ff4c0312af6a3ea1
=== MTC Repo Guard (dry-run, read-only) ===
[branch]    tmp/wp-p0-15-stale-demo-20260824
[dirty]     clean
[staged]    none
[protected] none
[untracked] no risky files
[unpushed]  no upstream set

WARN: no upstream tracking branch
RESULT: PASS
RED_RC=0
```

RED adjudication: the exact unmodified guard passed a clean branch that was 528 commits behind
local `origin/master`; it emitted no `STALE BRANCH` line. This is the defect state required by
D026.

## GREEN: modified guard detects and blocks the same stale branch

Working directory: `C:\WPP015_TMP_STALE`.

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File 'C:\WPP015_20260824\MTC_COMMAND_CENTER\tools\repo_guard.ps1'
Write-Output "GREEN_RC=$LASTEXITCODE"
```

Real output:

```text
=== MTC Repo Guard (dry-run, read-only) ===
[branch]    tmp/wp-p0-15-stale-demo-20260824
[freshness] local origin/master tip fbb05d7f46bc78b2875aa6d029e7fb2f2a8b14d7 age=0 day(s) (commit timestamp; no fetch attempted)
[freshness] branch merge-base 3bfe62a5ecb1f61bbac7f4dbdeef0239884adb8f is 528 commit(s) behind local origin/master (limit 30)
[freshness] STALE BRANCH: 'tmp/wp-p0-15-stale-demo-20260824' is 528 commit(s) behind local origin/master (limit 30)
[dirty]     clean
[staged]    none
[protected] none
[untracked] no risky files
[unpushed]  no upstream set

WARN: no upstream tracking branch
BLOCK: STALE BRANCH: 'tmp/wp-p0-15-stale-demo-20260824' is 528 commit(s) behind local origin/master (limit 30)
RESULT: BLOCKED
GREEN_RC=1
```

GREEN adjudication: the modified guard evaluated the same branch and same locally known origin
tip, emitted the required `STALE BRANCH` line, set `RESULT: BLOCKED`, and exited 1.

## Control: modified guard still passes a clean fresh worktree

This control ran after substantive commit
`37b055b6702cb04d089ff4b5a989129b61c3d93b`, so the worktree was genuinely clean and the guard
bytes were the committed modified bytes. Working directory: `C:\WPP015_20260824`.

```powershell
git status --porcelain
Write-Output "PRE_CONTROL_STATUS_RC=$LASTEXITCODE"
powershell.exe -NoProfile -ExecutionPolicy Bypass -File 'MTC_COMMAND_CENTER\tools\repo_guard.ps1'
Write-Output "CLEAN_CONTROL_RC=$LASTEXITCODE"
git rev-parse HEAD
```

Real output:

```text
PRE_CONTROL_STATUS_RC=0
=== MTC Repo Guard (dry-run, read-only) ===
[branch]    feature/wp-p0-15-branch-freshness-20260824
[freshness] local origin/master tip fbb05d7f46bc78b2875aa6d029e7fb2f2a8b14d7 age=0 day(s) (commit timestamp; no fetch attempted)
[freshness] branch merge-base fbb05d7f46bc78b2875aa6d029e7fb2f2a8b14d7 is 0 commit(s) behind local origin/master (limit 30)
[dirty]     clean
[staged]    none
[protected] none
[untracked] no risky files
[unpushed]  1 commit(s) ahead of upstream

RESULT: PASS
CLEAN_CONTROL_RC=0
37b055b6702cb04d089ff4b5a989129b61c3d93b
```

The empty output before `PRE_CONTROL_STATUS_RC=0` is the real clean-status result.

## Override checks

Working directory for all three checks: `C:\WPP015_TMP_STALE`. Every guard invocation used the
canonical Windows PowerShell 5.1 `-File` route. The GREEN section above freshly proves default
blocking mode through the same route (`RESULT: BLOCKED`, exit 1).

### Warn-only switch

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File 'C:\WPP015_20260824\MTC_COMMAND_CENTER\tools\repo_guard.ps1' -WarnOnlyStaleBranch
Write-Output "WARN_ONLY_RC=$LASTEXITCODE"
```

Real output:

```text
=== MTC Repo Guard (dry-run, read-only) ===
[branch]    tmp/wp-p0-15-stale-demo-20260824
[freshness] local origin/master tip fbb05d7f46bc78b2875aa6d029e7fb2f2a8b14d7 age=0 day(s) (commit timestamp; no fetch attempted)
[freshness] branch merge-base 3bfe62a5ecb1f61bbac7f4dbdeef0239884adb8f is 528 commit(s) behind local origin/master (limit 30)
[freshness] STALE BRANCH: 'tmp/wp-p0-15-stale-demo-20260824' is 528 commit(s) behind local origin/master (limit 30)
[dirty]     clean
[staged]    none
[protected] none
[untracked] no risky files
[unpushed]  no upstream set

WARN: STALE BRANCH: 'tmp/wp-p0-15-stale-demo-20260824' is 528 commit(s) behind local origin/master (limit 30); blocking disabled by -WarnOnlyStaleBranch
WARN: no upstream tracking branch
RESULT: PASS
WARN_ONLY_RC=0
```

### Environment threshold override

```powershell
$env:MTC_REPO_GUARD_MAX_BEHIND_COMMITS = '600'
powershell.exe -NoProfile -ExecutionPolicy Bypass -File 'C:\WPP015_20260824\MTC_COMMAND_CENTER\tools\repo_guard.ps1'
Write-Output "ENV_OVERRIDE_RC=$LASTEXITCODE"
Remove-Item Env:\MTC_REPO_GUARD_MAX_BEHIND_COMMITS
```

Real output:

```text
=== MTC Repo Guard (dry-run, read-only) ===
[branch]    tmp/wp-p0-15-stale-demo-20260824
[freshness] local origin/master tip fbb05d7f46bc78b2875aa6d029e7fb2f2a8b14d7 age=0 day(s) (commit timestamp; no fetch attempted)
[freshness] branch merge-base 3bfe62a5ecb1f61bbac7f4dbdeef0239884adb8f is 528 commit(s) behind local origin/master (limit 600)
[dirty]     clean
[staged]    none
[protected] none
[untracked] no risky files
[unpushed]  no upstream set

WARN: no upstream tracking branch
RESULT: PASS
ENV_OVERRIDE_RC=0
```

### Parameter threshold override and precedence

The environment is deliberately set to zero here. The explicit parameter still selects 600,
proving parameter precedence as well as successful `-File` binding.

```powershell
$env:MTC_REPO_GUARD_MAX_BEHIND_COMMITS = '0'
powershell.exe -NoProfile -ExecutionPolicy Bypass -File 'C:\WPP015_20260824\MTC_COMMAND_CENTER\tools\repo_guard.ps1' -MaxBehindCommits 600
Write-Output "PARAM_OVERRIDE_RC=$LASTEXITCODE"
Remove-Item Env:\MTC_REPO_GUARD_MAX_BEHIND_COMMITS
```

Real output:

```text
=== MTC Repo Guard (dry-run, read-only) ===
[branch]    tmp/wp-p0-15-stale-demo-20260824
[freshness] local origin/master tip fbb05d7f46bc78b2875aa6d029e7fb2f2a8b14d7 age=0 day(s) (commit timestamp; no fetch attempted)
[freshness] branch merge-base 3bfe62a5ecb1f61bbac7f4dbdeef0239884adb8f is 528 commit(s) behind local origin/master (limit 600)
[dirty]     clean
[staged]    none
[protected] none
[untracked] no risky files
[unpushed]  no upstream set

WARN: no upstream tracking branch
RESULT: PASS
PARAM_OVERRIDE_RC=0
```

## Fixture removal

Working directory: `C:\WPP015_20260824`. Clean status and exact identity were checked before
removal. `-D` was used only for the self-created, deliberately unmerged demo branch, as expressly
authorized by the lane contract.

```powershell
git -C 'C:\WPP015_TMP_STALE' status --porcelain
Write-Output "PRE_REMOVE_STATUS_RC=$LASTEXITCODE"
git -C 'C:\WPP015_TMP_STALE' rev-parse HEAD
git -C 'C:\WPP015_TMP_STALE' branch --show-current
git worktree remove 'C:\WPP015_TMP_STALE'
Write-Output "WORKTREE_REMOVE_RC=$LASTEXITCODE"
git show-ref --verify --hash 'refs/heads/tmp/wp-p0-15-stale-demo-20260824'
git branch -D 'tmp/wp-p0-15-stale-demo-20260824'
Write-Output "BRANCH_DELETE_RC=$LASTEXITCODE"
Write-Output "TEMP_PATH_EXISTS=$(Test-Path -LiteralPath 'C:\WPP015_TMP_STALE')"
git show-ref --verify --quiet 'refs/heads/tmp/wp-p0-15-stale-demo-20260824'
Write-Output "TEMP_BRANCH_POSTCHECK_RC=$LASTEXITCODE"
```

Real output:

```text
PRE_REMOVE_STATUS_RC=0
3bfe62a5ecb1f61bbac7f4dbdeef0239884adb8f
tmp/wp-p0-15-stale-demo-20260824
WORKTREE_REMOVE_RC=0
3bfe62a5ecb1f61bbac7f4dbdeef0239884adb8f
Deleted branch tmp/wp-p0-15-stale-demo-20260824 (was 3bfe62a5).
BRANCH_DELETE_RC=0
TEMP_PATH_EXISTS=False
TEMP_BRANCH_POSTCHECK_RC=1
```

The empty output before `PRE_REMOVE_STATUS_RC=0` is the real clean-status result. Postcheck rc 1
is the expected `show-ref --verify --quiet` result proving the temporary branch no longer exists.

## D026 verdict

PASS. RED and GREEN executed different guard bytes against the identical deliberately stale
worktree. RED passed without detecting staleness; GREEN emitted `STALE BRANCH`, blocked, and
returned 1. The committed modified guard separately passed from a clean, fresh control worktree.
