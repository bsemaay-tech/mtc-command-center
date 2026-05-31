Set-StrictMode -Version Latest
$ErrorActionPreference = "Continue"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $ScriptDir
$RunRoot = Join-Path $RepoRoot "reports\optimization\big_overnight_multiasset"
$LogsDir = Join-Path $RunRoot "logs"
$PidPath = Join-Path $RunRoot "run_process.pid"
$KeepAwakePidPath = Join-Path $RunRoot "keep_awake_process.pid"
$RunStatusJson = Join-Path $LogsDir "detached_resume_status.json"
$StdoutLog = Join-Path $LogsDir "detached_resume_stdout.log"
$StderrLog = Join-Path $LogsDir "detached_resume_stderr.log"
$CheckpointDir = Join-Path $RunRoot "checkpoints"
$HeartbeatCandidates = @(
    (Join-Path $RunRoot "heartbeat.log"),
    (Join-Path $LogsDir "heartbeat.log"),
    (Join-Path $LogsDir "keep_awake_heartbeat.log")
)

function Show-ProcessStatus {
    param(
        [string]$Label,
        [string]$Path
    )

    if (-not (Test-Path $Path)) {
        Write-Host "${Label} PID: not found"
        return
    }

    $rawPid = (Get-Content -Path $Path -ErrorAction SilentlyContinue | Select-Object -First 1)
    $processId = 0
    if (-not [int]::TryParse($rawPid, [ref]$processId)) {
        Write-Host "${Label} PID: invalid value '$rawPid'"
        return
    }

    $process = Get-Process -Id $processId -ErrorAction SilentlyContinue
    if ($null -eq $process) {
        Write-Host "${Label} PID: $processId (not running)"
    } else {
        Write-Host "${Label} PID: $processId (running, process=$($process.ProcessName), started=$($process.StartTime))"
    }
}

function Show-LatestFile {
    param(
        [string]$Label,
        [string[]]$Paths
    )

    $existing = $Paths | Where-Object { Test-Path $_ } | ForEach-Object { Get-Item $_ }
    if (-not $existing) {
        Write-Host "${Label}: not found"
        return
    }

    $latest = $existing | Sort-Object LastWriteTime -Descending | Select-Object -First 1
    Write-Host "${Label}: $($latest.FullName) last_write=$($latest.LastWriteTime.ToString('o'))"
}

function Show-LogTail {
    param(
        [string]$Label,
        [string]$Path
    )

    Write-Host ""
    Write-Host "---- $Label ----"
    if (-not (Test-Path $Path)) {
        Write-Host "not found: $Path"
        return
    }
    Get-Content -Path $Path -Tail 20 -ErrorAction SilentlyContinue
}

Write-Host "Big overnight resume status"
Write-Host "Run root: $RunRoot"

Show-ProcessStatus -Label "Optimizer" -Path $PidPath
Show-ProcessStatus -Label "Keep-awake" -Path $KeepAwakePidPath
Show-LatestFile -Label "Heartbeat" -Paths $HeartbeatCandidates

if (Test-Path $CheckpointDir) {
    $latestCheckpoint = Get-ChildItem -Path $CheckpointDir -File -ErrorAction SilentlyContinue | Sort-Object LastWriteTime -Descending | Select-Object -First 1
    if ($null -eq $latestCheckpoint) {
        Write-Host "Latest checkpoint: no checkpoint files"
    } else {
        Write-Host "Latest checkpoint: $($latestCheckpoint.FullName) last_write=$($latestCheckpoint.LastWriteTime.ToString('o'))"
    }
} else {
    Write-Host "Latest checkpoint: checkpoint directory not found"
}

if (Test-Path $RunStatusJson) {
    Write-Host "Run status json: $RunStatusJson"
    Get-Content -Path $RunStatusJson -ErrorAction SilentlyContinue
} else {
    Write-Host "Run status json: not found"
}

Show-LogTail -Label "stdout tail" -Path $StdoutLog
Show-LogTail -Label "stderr tail" -Path $StderrLog
