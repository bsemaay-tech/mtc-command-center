<#
.SYNOPSIS
  MTC Repo Guard - dry-run preflight. READ-ONLY: never modifies files, index, or remotes.
.DESCRIPTION
  Checks current branch, dirty files, staged files, protected-scope changes, risky untracked
  files, and unpushed commits. Prints per-check status and a final PASS / BLOCKED verdict.
  Enforces MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/MTC_REPO_GUARD_PROTOCOL.md.
.NOTES
  Exit code 0 = PASS, 1 = BLOCKED. Does not stage, commit, push, or write anything.
#>
[CmdletBinding()]
param()

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
  foreach ($f in $touched) { if ($f -like "$p*") { $hitProtected += $f } }
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
