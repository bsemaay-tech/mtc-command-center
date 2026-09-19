# Serial exact-Sol chain for Sat 2026-09-19 (Codex Plus weekly reset 18:47 local). Armed by the session-7 Lead.
# Sleeps until -StartAt, then for each package: skip if C:\tmp\SOL_QUEUE_20260919\SKIP_<pkg>.txt exists or the lane
# already has launch.exit; wait while agy.exe (Gemini) runs; GENERATE the lane from the CURRENT Wednesday pin
# (make_sol_lane.ps1 refuses on drift); for DD06 append the binding safety rule; launch run.ps1 (one Codex lane at a
# time on 'secondary'); stop the whole chain on a usage cap. A sleeping host kills this chain - restart by hand.
param(
    [string]$StartAt = '2026-09-19T18:47:30',
    [string[]]$Order = @('P031', 'P1CAP', 'P026', 'P021S1', 'P012INTAKE', 'P030', 'DD06'),
    [string]$Account = 'secondary'
)
$ErrorActionPreference = 'Continue'
$root = 'C:\tmp\SOL_QUEUE_20260919'
$log = Join-Path $root 'SOL_CHAIN_LOG.txt'
function Log([string]$m) { "$((Get-Date).ToUniversalTime().ToString('o')) $m" | Add-Content -Path $log -Encoding ascii }
Log "armed: start at $StartAt local; account $Account; order $($Order -join ' > ')"
while ((Get-Date) -lt [datetime]$StartAt) { Start-Sleep -Seconds 30 }
Log 'start'
$safety = @"

## BINDING SAFETY RULE (added to every Sol brief after the 2026-09-17 lane-7 incident)
This workstation's user registry holds a live agent-wallet credential (HL_API_WALLET_KEY, HL_ACCOUNT_ADDRESS), readable by any process. You may NOT mutate a venue-facing tool's refusals and then run a test that calls the tool's real main() or builds real SDK objects. Mutants only in scratch copies; only fixture suites whose main() tests are structurally offline (tripwires for the resolver and the SDK constructors, cleared env); never set HL_LIVE_ACK, never read the registry, never dial the testnet or mainnet. You are documentary-only: no shell execution beyond reading files and running the fixture suite of a scratch copy with the pinned interpreter.
"@
foreach ($pkg in $Order) {
    $lane = Join-Path $root "$pkg\sol"
    if (Test-Path (Join-Path $root "SKIP_$pkg.txt")) { Log "$pkg skipped (SKIP file)"; continue }
    if (Test-Path (Join-Path $lane 'launch.exit')) { Log "$pkg already has launch.exit; skip"; continue }
    while (Get-Process agy -ErrorAction SilentlyContinue) { Log "$pkg waiting: agy.exe running"; Start-Sleep -Seconds 60 }
    $gen = & powershell -NoProfile -ExecutionPolicy Bypass -File (Join-Path $root 'make_sol_lane.ps1') -Pkg $pkg -Account $Account 2>&1 | Out-String
    Log "$pkg generate: $(($gen.Trim() -replace '\s+', ' ').Substring(0, [Math]::Min(300, ($gen.Trim() -replace '\s+', ' ').Length)))"
    if (-not (Test-Path (Join-Path $lane 'run.ps1')) -or $gen -match 'refuse|throw|drift|cannot find|is at') { Log "$pkg NOT launched (generator refused)"; continue }
    if ($pkg -eq 'DD06') { Add-Content -Path (Join-Path $lane 'BRIEF.md') -Value $safety -Encoding utf8; Log 'DD06 safety rule appended to the Sol brief' }
    Log "$pkg launching"
    $t0 = Get-Date
    & powershell -NoProfile -ExecutionPolicy Bypass -File (Join-Path $lane 'run.ps1') 2>&1 | Out-Null
    $exit = if (Test-Path (Join-Path $lane 'launch.exit')) { (Get-Content (Join-Path $lane 'launch.exit') -Raw).Trim() } else { 'no launch.exit' }
    Log "$pkg ended after $([int]((Get-Date) - $t0).TotalMinutes) min: $exit"
    $stream = if (Test-Path (Join-Path $lane 'stream.jsonl')) { Get-Content (Join-Path $lane 'stream.jsonl') -Raw } else { '' }
    # a cap shows up as a Codex ERROR event (or a turn.failed) carrying the usage text; report text that merely QUOTES
    # the words (a reviewer reading an old brief) must not stop the chain (false stop on P031, 2026-09-19 11:37)
    $capLines = @($stream -split "`n" | Where-Object { ($_ -match '"type":"(error|turn\.failed)"' -or $_ -match '"error":\{') -and $_ -match 'usage limit|try again at|rate_limit|insufficient_quota|usage_limit_reached|You.ve hit your' })
    $reportOk = (Test-Path (Join-Path $lane 'SOL_T0_REPORT.md')) -and ((Get-Content (Join-Path $lane 'SOL_T0_REPORT.md') -Raw) -match 'VERDICT: (PASS|PASS-WITH-NITS|REQUEST_CHANGES|BLOCK)')
    if ($capLines.Count -gt 0 -and -not $reportOk) { Log "$pkg CAPPED ($($capLines.Count) error events with usage text, no verdict) - chain stops; relaunch by hand after the bucket"; break }
    if ($capLines.Count -gt 0) { Log "${pkg}: usage text in $($capLines.Count) error events but the report carries a VERDICT - continuing" }
    if ($exit -match 'refuse') { Log "$pkg launcher refused; continuing" }
    Start-Sleep -Seconds 20
}
Log 'chain complete'
