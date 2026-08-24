# Verified Clean Isolated Worktree Procedure

Use this procedure when an agent must start from a named commit without disturbing an existing
checkout. It is intentionally non-destructive: do not reset, stash, clean, prune, delete a branch,
or discard untracked files.

## Create and verify

Run from PowerShell. Set `$Repo` to a clean administrative worktree for the repository, not to a
dirty checkout that must be preserved.

```powershell
$Repo = 'C:\path\to\clean-repository-worktree'
$Worktree = 'C:\path\to\new-isolated-worktree'
$Branch = 'feature/<scope>'
$Target = '<full-or-abbreviated-commit-sha>'

# Refuse to reuse an existing destination.
if (Test-Path -LiteralPath $Worktree) {
    throw "Destination already exists: $Worktree"
}

# Verify that the target resolves to a commit, then inspect exactly what it is.
$ResolvedTarget = ''
try { $ResolvedTarget = (git -C $Repo rev-parse --verify "$Target^{commit}" 2>$null).Trim() }
catch { $ResolvedTarget = '' }
if ($LASTEXITCODE -ne 0 -or -not $ResolvedTarget) {
    throw "Target is not a valid local commit: $Target"
}
git -C $Repo log -1 --decorate --date=iso-strict --format=fuller $ResolvedTarget
if ($LASTEXITCODE -ne 0) { throw 'Could not inspect target commit.' }

# Require a new branch name so existing work is never overwritten.
git -C $Repo show-ref --verify --quiet "refs/heads/$Branch"
if ($LASTEXITCODE -eq 0) { throw "Branch already exists: $Branch" }

git -C $Repo worktree add -b $Branch $Worktree $ResolvedTarget
if ($LASTEXITCODE -ne 0) { throw 'git worktree add failed.' }

# The new worktree must be empty of changes and exactly at the requested commit.
$Dirty = @(git -C $Worktree status --porcelain)
if ($LASTEXITCODE -ne 0) { throw 'Could not inspect new worktree status.' }
if ($Dirty.Count -ne 0) {
    $Dirty
    throw 'New worktree is not clean. Stop; do not reset, stash, or clean it.'
}

$ActualHead = (git -C $Worktree rev-parse HEAD).Trim()
if ($LASTEXITCODE -ne 0) { throw 'Could not resolve new worktree HEAD.' }
if ($ActualHead -ne $ResolvedTarget) {
    throw "HEAD mismatch: expected $ResolvedTarget, found $ActualHead"
}

git -C $Worktree status --short --branch
git -C $Worktree log -1 --oneline --decorate
Write-Output "VERIFIED CLEAN WORKTREE: $Worktree at $ActualHead on $Branch"

# Link worktree verification to the offline branch-freshness gate before work begins. An old
# target can predate the freshness check, so never run the target checkout's guard. Extract the
# current guard from origin/master; until WP-P0-15 is merged, fall back to this feature branch.
$GuardPath = 'MTC_COMMAND_CENTER/tools/repo_guard.ps1'
$GuardSpec = "origin/master:$GuardPath"
$GuardLines = @(git -C $Worktree show $GuardSpec 2>$null)
$GuardText = $GuardLines -join [Environment]::NewLine
if ($LASTEXITCODE -ne 0 -or $GuardText -notmatch 'STALE BRANCH') {
    $GuardSpec = "feature/wp-p0-15-branch-freshness-20260824:$GuardPath"
    $GuardLines = @(git -C $Repo show $GuardSpec 2>$null)
    $GuardText = $GuardLines -join [Environment]::NewLine
}
if ($LASTEXITCODE -ne 0 -or $GuardText -notmatch 'STALE BRANCH') {
    throw "Could not extract the current branch-freshness guard from $GuardSpec"
}
$CurrentGuard = Join-Path $env:TEMP 'repo_guard_current.ps1'
$GuardText | Set-Content -LiteralPath $CurrentGuard -Encoding UTF8

Set-Location -LiteralPath $Worktree
powershell.exe -NoProfile -ExecutionPolicy Bypass -File $CurrentGuard
if ($LASTEXITCODE -ne 0) {
    throw 'Repo guard blocked the new worktree. Recreate it from current origin/master or rebase.'
}
```

Only begin work after the `VERIFIED CLEAN WORKTREE` line and a final `RESULT: PASS` from the
repo guard.

## Teardown

First verify the isolated worktree is clean:

```powershell
$Dirty = @(git -C $Worktree status --porcelain)
if ($LASTEXITCODE -ne 0) { throw 'Could not inspect worktree status.' }
if ($Dirty.Count -ne 0) {
    $Dirty
    throw 'Worktree is not clean. Preserve it and report the exact paths; do not remove it.'
}

git -C $Repo worktree remove $Worktree
if ($LASTEXITCODE -ne 0) { throw 'git worktree remove failed.' }
```

If the worktree is not clean, stop. Record `git -C $Worktree status --short`, the worktree path,
branch, and HEAD SHA for its owner. Do not use `--force`, `reset`, `stash`, `clean`, or manual file
deletion. Removing the worktree does not require deleting its branch; branch retention or deletion
is a separate, explicitly authorized decision.
