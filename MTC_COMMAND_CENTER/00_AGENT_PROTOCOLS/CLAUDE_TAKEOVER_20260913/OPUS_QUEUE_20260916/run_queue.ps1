# Serial launcher for the Wednesday exact-Opus queue (P031 -> P1CAP -> P030). PREPARED 2026-09-15; start only after the
# Claude Pro weekly reset (2026-09-16 20:00Z) from the Lead session. Skips lanes with launch.exit; refuses while agy.exe runs;
# stops on a non-zero exit (a capped or failed lane must be looked at, not skipped over).
$ErrorActionPreference = 'Continue'
$root = 'C:\tmp\OPUS_QUEUE_20260916'
$log = Join-Path $root 'QUEUE_LOG.txt'
function Log($m) { $line = "$((Get-Date).ToUniversalTime().ToString('o')) $m"; [System.IO.File]::AppendAllText($log, $line + "`n", (New-Object System.Text.UTF8Encoding($false))); Write-Output $line }
$notBefore = [DateTime]::Parse('2026-09-16T20:00:00Z').ToUniversalTime()
if ((Get-Date).ToUniversalTime() -lt $notBefore) { Log "refuse: before the weekly reset $($notBefore.ToString('o'))"; exit 2 }
foreach ($pkg in 'P031', 'P1CAP', 'P030') {
  $lane = Join-Path $root "$pkg\opus"
  if (Test-Path (Join-Path $lane 'launch.exit')) { Log "skip $pkg (launch.exit exists)"; continue }
  if (Get-Process agy -ErrorAction SilentlyContinue) { Log "agy.exe running; waiting before $pkg"; while (Get-Process agy -ErrorAction SilentlyContinue) { Start-Sleep -Seconds 30 } }
  Log "launching $pkg"
  & powershell -NoProfile -ExecutionPolicy Bypass -File (Join-Path $lane 'run.ps1')
  $le = if (Test-Path (Join-Path $lane 'launch.exit')) { Get-Content (Join-Path $lane 'launch.exit') -Raw } else { 'NO launch.exit' }
  Log "finished $pkg : $($le.Trim())"
  if ($le -notmatch 'exit=0') { Log "stopping the queue after $pkg (non-zero or missing exit)"; break }
}
Log 'queue complete'
