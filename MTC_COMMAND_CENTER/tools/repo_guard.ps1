<#
.SYNOPSIS
  MTC Repo Guard - dry-run preflight. READ-ONLY: never modifies files, index, or remotes.
.DESCRIPTION
  Checks current branch, dirty files, staged files, protected-scope changes, risky untracked
  files, branch freshness against the local origin/master ref, and unpushed commits. Prints
  per-check status and a final PASS / BLOCKED verdict. The freshness check never fetches.
  Enforces MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/MTC_REPO_GUARD_PROTOCOL.md.
.PARAMETER MaxBehindCommits
  Maximum commits the branch merge-base may lag local origin/master before it is stale.
  Default: 30. MTC_REPO_GUARD_MAX_BEHIND_COMMITS overrides the default when this parameter
  is not supplied.
.PARAMETER WarnOnlyStaleBranch
  When present, a stale branch emits a warning instead of making the final result BLOCKED.
  Blocking remains the default.
.NOTES
  Exit code 0 = PASS, 1 = BLOCKED. Does not stage, commit, push, or write anything.
#>
[CmdletBinding()]
param(
  [ValidateRange(0, 2147483647)]
  [int]$MaxBehindCommits = 30,

  [switch]$WarnOnlyStaleBranch
)

$ErrorActionPreference = 'Stop'
$protected = @(
  'MTC_COMMAND_CENTER/02_MTC_BACKTEST',
  'MTC_COMMAND_CENTER/07_ADAPTERS',
  'MTC_COMMAND_CENTER/01_PINE',
  'MTC_COMMAND_CENTER/MTC_V2'
)
# untracked names that usually mean an artifact / launcher leaked into the tree
$riskyUntracked = @('top_results.json')
$riskyPatterns  = @('*_server.ps1','START_*','*.tmp','*.log')

$blocked = @()
$warn    = @()
$maxBehindConfigError = ''

if (-not $PSBoundParameters.ContainsKey('MaxBehindCommits') -and
    -not [string]::IsNullOrWhiteSpace($env:MTC_REPO_GUARD_MAX_BEHIND_COMMITS)) {
  $envMaxBehind = 0
  if ([int]::TryParse($env:MTC_REPO_GUARD_MAX_BEHIND_COMMITS, [ref]$envMaxBehind) -and
      $envMaxBehind -ge 0) {
    $MaxBehindCommits = $envMaxBehind
  } else {
    $maxBehindConfigError = "MTC_REPO_GUARD_MAX_BEHIND_COMMITS must be a non-negative integer (received '$($env:MTC_REPO_GUARD_MAX_BEHIND_COMMITS)')"
  }
}

function Line($s) { Write-Output $s }

# locate repo root (script lives in MTC_COMMAND_CENTER/tools)
$repoRoot = (git rev-parse --show-toplevel) 2>$null
if (-not $repoRoot) { Line 'BLOCKED: not a git repository.'; exit 1 }
Set-Location $repoRoot

Line '=== MTC Repo Guard (dry-run, read-only) ==='

# 1. branch
$branch = (git rev-parse --abbrev-ref HEAD).Trim()
Line "[branch]    $branch"
if ($branch -eq 'master' -or $branch -eq 'main') {
  $blocked += "on '$branch' - branch first (feature/<scope>)"
}

# branch freshness (offline: local origin/master only)
$originRef = 'refs/remotes/origin/master'
if ($maxBehindConfigError -ne '') {
  Line "[freshness] configuration error: $maxBehindConfigError"
  $blocked += "branch freshness cannot be evaluated: $maxBehindConfigError"
} else {
  git show-ref --verify --quiet $originRef
  if ($LASTEXITCODE -ne 0) {
    Line '[freshness] unavailable: local origin/master ref is missing (no fetch attempted)'
    $blocked += 'branch freshness cannot be evaluated: local origin/master ref is missing'
  } else {
    $freshnessInputsAvailable = $true
    try {
      $originTip = (git rev-parse $originRef 2>$null).Trim()
      if ($LASTEXITCODE -ne 0 -or $originTip -eq '') { throw 'could not resolve local origin/master tip' }
      $originEpochText = (git show -s --format=%ct $originRef 2>$null).Trim()
      if ($LASTEXITCODE -ne 0 -or $originEpochText -notmatch '^\d+$') { throw 'could not resolve local origin/master age' }
      $mergeBase = (git merge-base HEAD $originRef 2>$null).Trim()
      if ($LASTEXITCODE -ne 0 -or $mergeBase -eq '') { throw 'could not resolve merge-base' }
    } catch {
      $freshnessInputsAvailable = $false
    }
    if (-not $freshnessInputsAvailable) {
      Line '[freshness] unavailable: could not resolve merge-base or local origin/master age (no fetch attempted)'
      $blocked += 'branch freshness cannot be evaluated against local origin/master'
    } else {
      $behindCountAvailable = $true
      try {
        $behindText = (git rev-list --count "$mergeBase..$originRef" 2>$null).Trim()
        if ($LASTEXITCODE -ne 0 -or $behindText -notmatch '^\d+$') { throw 'could not count commits behind' }
      } catch {
        $behindCountAvailable = $false
      }
      if (-not $behindCountAvailable) {
        Line '[freshness] unavailable: could not count commits behind local origin/master (no fetch attempted)'
        $blocked += 'branch freshness cannot be evaluated against local origin/master'
      } else {
        $originAgeSeconds = [DateTimeOffset]::UtcNow.ToUnixTimeSeconds() - [int64]$originEpochText
        if ($originAgeSeconds -lt 0) { $originAgeSeconds = 0 }
        $originAgeDays = [math]::Floor($originAgeSeconds / 86400)
        $behind = [int64]$behindText
        Line "[freshness] local origin/master tip $originTip age=$originAgeDays day(s) (commit timestamp; no fetch attempted)"
        Line "[freshness] branch merge-base $mergeBase is $behind commit(s) behind local origin/master (limit $MaxBehindCommits)"
        if ($behind -gt $MaxBehindCommits) {
          $staleMessage = "STALE BRANCH: '$branch' is $behind commit(s) behind local origin/master (limit $MaxBehindCommits)"
          Line "[freshness] $staleMessage"
          if ($WarnOnlyStaleBranch) { $warn += "$staleMessage; blocking disabled by -WarnOnlyStaleBranch" }
          else { $blocked += $staleMessage }
        }
      }
    }
  }
}

# 2. dirty (tracked, unstaged or modified)
$dirty = @(git status --short)
if ($dirty.Count -gt 0) { Line "[dirty]     $($dirty.Count) entr(y/ies):"; $dirty | ForEach-Object { Line "            $_" } }
else { Line '[dirty]     clean' }

# 3. staged
$staged = @(git diff --cached --name-only)
if ($staged.Count -gt 0) { Line "[staged]    $($staged.Count) file(s):"; $staged | ForEach-Object { Line "            $_" } }
else { Line '[staged]    none' }

# 4. protected-scope changes (staged or unstaged or untracked)
$touched = @(git status --short | ForEach-Object { ($_ -replace '^.{3}','').Trim() -replace '"','' })
$hitProtected = @()
foreach ($p in $protected) {
  foreach ($f in $touched) { if ($f -eq $p -or $f -like "$p/*") { $hitProtected += $f } }
}
if ($hitProtected.Count -gt 0) {
  Line "[protected] CHANGES in protected scope:"; $hitProtected | Sort-Object -Unique | ForEach-Object { Line "            $_" }
  $blocked += "protected-scope change needs Baris approval ($((($hitProtected | Sort-Object -Unique) -join ', ')))"
} else { Line '[protected] none' }

# 5. risky untracked files
$untracked = @(git ls-files --others --exclude-standard)
$risky = @()
foreach ($u in $untracked) {
  $name = Split-Path $u -Leaf
  if ($riskyUntracked -contains $name) { $risky += $u; continue }
  foreach ($pat in $riskyPatterns) { if ($name -like $pat) { $risky += $u; break } }
}
if ($risky.Count -gt 0) {
  Line "[untracked] risky local-only file(s):"; $risky | Sort-Object -Unique | ForEach-Object { Line "            $_" }
  $warn += "risky untracked file(s) present - do NOT commit ($((($risky | Sort-Object -Unique) -join ', ')))"
} else { Line '[untracked] no risky files' }

# 6. unpushed commits
$ahead = ''
try { $ahead = (git rev-list --count "@{u}..HEAD" 2>$null).Trim() } catch { $ahead = '' }
if ($ahead -eq '') { Line '[unpushed]  no upstream set'; $warn += 'no upstream tracking branch' }
elseif ([int]$ahead -gt 0) { Line "[unpushed]  $ahead commit(s) ahead of upstream" }
else { Line '[unpushed]  in sync with upstream' }

# verdict
Line ''
if ($warn.Count -gt 0) { $warn | ForEach-Object { Line "WARN: $_" } }
if ($blocked.Count -gt 0) {
  $blocked | ForEach-Object { Line "BLOCK: $_" }
  Line 'RESULT: BLOCKED'
  exit 1
}
Line 'RESULT: PASS'
exit 0
