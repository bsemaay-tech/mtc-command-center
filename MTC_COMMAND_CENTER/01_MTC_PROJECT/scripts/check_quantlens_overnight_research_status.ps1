Set-StrictMode -Version Latest
$ErrorActionPreference = "Continue"

$RepoRoot = "C:\LAB\tradingview-lab\01_MASTER TEMPLATE_V2"
$RunRoot = Join-Path $RepoRoot "06_QUANTLENS_LAB\05_BACKTEST_RESULTS\overnight_research_20260501"
$DetachedDir = Join-Path $RunRoot "detached"
$LogsDir = Join-Path $RunRoot "logs"
$PidPath = Join-Path $DetachedDir "run_process.pid"
$RunStatusJson = Join-Path $DetachedDir "run_status.json"
$StdoutLog = Join-Path $LogsDir "stdout.log"
$StderrLog = Join-Path $LogsDir "stderr.log"
$HeartbeatLog = Join-Path $RunRoot "heartbeat\heartbeat.log"
$Evaluations = Join-Path $RunRoot "results\all_evaluations.csv"
$Rollup = Join-Path $RunRoot "ranked\candidate_rollup.csv"
$Summary = Join-Path $RunRoot "reports\OVERNIGHT_RESEARCH_SUMMARY.md"

Write-Host "QuantLens overnight research status"
Write-Host "Output root: $RunRoot"

if (Test-Path -LiteralPath $PidPath) {
    $rawPid = Get-Content -Path $PidPath | Select-Object -First 1
    Write-Host "PID value: $rawPid"
    $parsedPid = 0
    if ([int]::TryParse($rawPid, [ref]$parsedPid)) {
        $process = Get-Process -Id $parsedPid -ErrorAction SilentlyContinue
        if ($null -eq $process) {
            Write-Host "Process status: completed_or_not_running"
        } else {
            Write-Host "Process status: running"
            Write-Host "Process name: $($process.ProcessName)"
            Write-Host "Process start: $($process.StartTime.ToString('o'))"
        }
    }
} else {
    Write-Host "PID value: not found"
}

if (Test-Path -LiteralPath $HeartbeatLog) {
    $heartbeatItem = Get-Item -LiteralPath $HeartbeatLog
    Write-Host "Latest heartbeat timestamp: $($heartbeatItem.LastWriteTime.ToString('o'))"
    Get-Content -Path $HeartbeatLog -Tail 3
} else {
    Write-Host "Heartbeat: not found"
}

if (Test-Path -LiteralPath $RunStatusJson) {
    Write-Host ""
    Write-Host "---- run_status.json ----"
    Get-Content -Path $RunStatusJson
} else {
    Write-Host "run_status.json: not found"
}

if (Test-Path -LiteralPath $Evaluations) {
    $rows = [Math]::Max(0, ((Get-Content -Path $Evaluations | Measure-Object -Line).Lines - 1))
    Write-Host "Evaluation rows: $rows"
}

if (Test-Path -LiteralPath $Rollup) {
    $rows = [Math]::Max(0, ((Get-Content -Path $Rollup | Measure-Object -Line).Lines - 1))
    Write-Host "Rollup rows: $rows"
}

if (Test-Path -LiteralPath $Summary) {
    Write-Host "Summary: $Summary"
    Get-Content -Path $Summary -Head 30
}

Write-Host ""
Write-Host "---- stderr last 20 lines ----"
if (Test-Path -LiteralPath $StderrLog) {
    Get-Content -Path $StderrLog -Tail 20
} else {
    Write-Host "not found"
}
