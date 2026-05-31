Set-StrictMode -Version Latest
$ErrorActionPreference = "Continue"

$RepoRoot = "C:\LAB\tradingview-lab\01_MASTER TEMPLATE_V2"
$RunRoot = Join-Path $RepoRoot "reports\optimization\12h_backtesting_session"
$DetachedDir = Join-Path $RunRoot "detached"
$LogsDir = Join-Path $RunRoot "logs"
$PidPath = Join-Path $DetachedDir "run_process.pid"
$RunStatusJson = Join-Path $DetachedDir "run_status.json"
$StdoutLog = Join-Path $LogsDir "stdout.log"
$StderrLog = Join-Path $LogsDir "stderr.log"
$HeartbeatLog = Join-Path $RunRoot "heartbeat\heartbeat.log"
$CheckpointDir = Join-Path $RunRoot "checkpoints"
$RuntimeSummary = Join-Path $LogsDir "runtime_summary.json"
$AllEvaluations = Join-Path $RunRoot "results\all_evaluations.csv"
$FailedEvaluations = Join-Path $RunRoot "failures\failed_evaluations.json"
$ResumeReport = Join-Path $RunRoot "reports\RESUME_DEDUP_REPORT.md"

function Show-LogTail {
    param(
        [string]$Label,
        [string]$Path
    )

    Write-Host ""
    Write-Host "---- $Label ----"
    if (Test-Path -LiteralPath $Path) {
        Get-Content -Path $Path -Tail 30 -ErrorAction SilentlyContinue
    } else {
        Write-Host "not found: $Path"
    }
}

Write-Host "12h backtesting session status"
Write-Host "Output root: $RunRoot"
Write-Host "PID file path: $PidPath"

$pidValue = $null
if (Test-Path -LiteralPath $PidPath) {
    $rawPid = Get-Content -Path $PidPath -ErrorAction SilentlyContinue | Select-Object -First 1
    Write-Host "PID value: $rawPid"
    $parsedPid = 0
    if ([int]::TryParse($rawPid, [ref]$parsedPid)) {
        $pidValue = $parsedPid
        $process = Get-Process -Id $pidValue -ErrorAction SilentlyContinue
        if ($null -eq $process) {
            Write-Host "Process status: completed_or_not_running"
        } else {
            Write-Host "Process status: running"
            Write-Host "Process name: $($process.ProcessName)"
            Write-Host "Process start: $($process.StartTime.ToString('o'))"
        }
    } else {
        Write-Host "Process status: invalid_pid"
    }
} else {
    Write-Host "PID value: not found"
    Write-Host "Process status: no_pid_file"
}

if (Test-Path -LiteralPath $HeartbeatLog) {
    $heartbeatItem = Get-Item -LiteralPath $HeartbeatLog
    Write-Host "Latest heartbeat timestamp: $($heartbeatItem.LastWriteTime.ToString('o'))"
    Write-Host "Latest heartbeat line:"
    Get-Content -Path $HeartbeatLog -Tail 1 -ErrorAction SilentlyContinue
} else {
    Write-Host "Latest heartbeat timestamp: not found"
}

if (Test-Path -LiteralPath $CheckpointDir) {
    $latestCheckpoint = Get-ChildItem -Path $CheckpointDir -File -ErrorAction SilentlyContinue | Sort-Object LastWriteTime -Descending | Select-Object -First 1
    if ($null -eq $latestCheckpoint) {
        Write-Host "Latest checkpoint: no checkpoint files"
    } else {
        Write-Host "Latest checkpoint: $($latestCheckpoint.FullName)"
        Write-Host "Latest checkpoint timestamp: $($latestCheckpoint.LastWriteTime.ToString('o'))"
    }
} else {
    Write-Host "Latest checkpoint: checkpoint directory not found"
}

Write-Host "stdout path: $StdoutLog"
Write-Host "stderr path: $StderrLog"

if (Test-Path -LiteralPath $RunStatusJson) {
    Write-Host ""
    Write-Host "---- run_status.json ----"
    Get-Content -Path $RunStatusJson -ErrorAction SilentlyContinue
} else {
    Write-Host "run_status.json: not found"
}

if (Test-Path -LiteralPath $RuntimeSummary) {
    try {
        $runtime = Get-Content -Path $RuntimeSummary -Raw | ConvertFrom-Json
        Write-Host "Completed evaluations: $($runtime.completed)"
        Write-Host "Failed evaluations: $($runtime.failed)"
        Write-Host "Duplicate conflicts: $($runtime.duplicate_conflicts)"
    } catch {
        Write-Host "Runtime metrics: unable to parse $RuntimeSummary"
    }
} else {
    Write-Host "Completed evaluations: metrics not found yet"
    Write-Host "Failed evaluations: metrics not found yet"
    Write-Host "Duplicate conflicts: metrics not found yet"
}

if (Test-Path -LiteralPath $AllEvaluations) {
    $completedRows = [Math]::Max(0, ((Get-Content -Path $AllEvaluations -ErrorAction SilentlyContinue | Measure-Object -Line).Lines - 1))
    Write-Host "Evaluation CSV rows: $completedRows"
}

if (Test-Path -LiteralPath $FailedEvaluations) {
    try {
        $failedRows = Get-Content -Path $FailedEvaluations -Raw | ConvertFrom-Json
        Write-Host "Failed evaluations file count: $($failedRows.Count)"
    } catch {
        Write-Host "Failed evaluations file count: unable to parse"
    }
}

if (Test-Path -LiteralPath $ResumeReport) {
    $duplicateLine = Select-String -Path $ResumeReport -Pattern "Duplicate" -SimpleMatch -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($null -ne $duplicateLine) {
        Write-Host "Resume duplicate summary: $($duplicateLine.Line)"
    }
}

Show-LogTail -Label "stdout last 30 lines" -Path $StdoutLog
Show-LogTail -Label "stderr last 30 lines" -Path $StderrLog
