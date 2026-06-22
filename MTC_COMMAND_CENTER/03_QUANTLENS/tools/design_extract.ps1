<#
.SYNOPSIS
  Safe wrapper for Design-Extract (`designlang`) - normalizes its known cosmetic exit-1.
.DESCRIPTION
  designlang writes all artifacts, then a wrap-up step can throw and exit 1 even though the
  extraction succeeded (see 09_DOCS/AI_TOOLING/pilots/design-extract_pilot.md). For automation
  this wrapper treats a non-zero exit as SUCCESS when output files actually landed, and only
  fails when the output dir is empty.

  Inspiration tool only - outputs go OUTSIDE the repo (default C:\tmp). Never run it into the
  repo tree (35+ files = git noise). "Inspiration, not copy."
.PARAMETER Url
  Site to extract (e.g. https://linear.app). For a dashboard, target a real app screen, not a
  marketing landing; pass cookies via -Extra '--cookie-file','C:\path\cookies.json'.
.PARAMETER Out
  Output directory (default C:\tmp\design_extract_out). Must not be inside the repo.
.PARAMETER Name
  Output file prefix (default derived from URL host).
.PARAMETER Extra
  Extra args passed through to designlang (e.g. -Extra '--dark','--responsive').
.EXAMPLE
  pwsh -File design_extract.ps1 -Url https://linear.app -Name linear -Extra '--dark'
.NOTES
  Requires Node 20+ and npx. Uses --system-chrome (skips the 150MB Playwright download).
  Exit 0 = artifacts produced (PASS), 1 = real failure (no output).
#>
[CmdletBinding()]
param(
  [Parameter(Mandatory=$true)][string]$Url,
  [string]$Out = 'C:\tmp\design_extract_out',
  [string]$Name,
  [string[]]$Extra = @()
)

$ErrorActionPreference = 'Stop'

# refuse to write inside the repo (git-noise guard)
$repoRoot = (git rev-parse --show-toplevel) 2>$null
if ($repoRoot) {
  $full = [System.IO.Path]::GetFullPath($Out)
  $root = [System.IO.Path]::GetFullPath(($repoRoot -replace '/','\'))
  if ($full.ToLower().StartsWith($root.ToLower())) {
    Write-Output "BLOCKED: output dir '$Out' is inside the repo. Use C:\tmp (35+ files = git noise)."
    exit 1
  }
}

if (-not (Test-Path $Out)) { New-Item -ItemType Directory -Path $Out -Force | Out-Null }

$args = @('-y','designlang','-o',$Out)
if ($Name) { $args += @('-n',$Name) }
$args += @($Url,'--system-chrome')
$args += $Extra

Write-Output "[design_extract] npx $($args -join ' ')"
& npx @args
$code = $LASTEXITCODE

$produced = @(Get-ChildItem -Path $Out -File -ErrorAction SilentlyContinue)
Write-Output ""
Write-Output "[design_extract] designlang exit=$code ; output files=$($produced.Count) in $Out"

if ($produced.Count -gt 0) {
  if ($code -ne 0) {
    Write-Output "WARN: designlang exited $code but artifacts landed - treating as success (known cosmetic post-step crash)."
  }
  Write-Output "RESULT: PASS"
  exit 0
}
Write-Output "RESULT: FAIL (no artifacts produced)"
exit 1
