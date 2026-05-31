Set-StrictMode -Version Latest
$ErrorActionPreference = "Continue"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $ScriptDir
$SmokeRoot = Join-Path $RepoRoot "reports\optimization\detached_resume_smoke\run"
$LogsDir = Join-Path $SmokeRoot "logs"
$PidPath = Join-Path $SmokeRoot "run_process.pid"
$StatusPath = Join-Path $SmokeRoot "run_status.json"
$MetricsPath = Join-Path $SmokeRoot "metrics.json"
$HeartbeatPath = Join-Path $SmokeRoot "heartbeat.log"
$StdoutLog = Join-Path $LogsDir "detached_smoke_stdout.log"
$StderrLog = Join-Path $LogsDir "detached_smoke_stderr.log"

function Get-SmokeProcessState {
    if (-not (Test-Path $PidPath)) {
        return [ordered]@{ pid = $null; state = "pid_missing"; process_name = $null }
    }

    $rawPid = Get-Content -Path $PidPath -ErrorAction SilentlyContinue | Select-Object -First 1
    $processId = 0
    if (-not [int]::TryParse($rawPid, [ref]$processId)) {
        return [ordered]@{ pid = $rawPid; state = "pid_invalid"; process_name = $null }
    }

    $process = Get-Process -Id $processId -ErrorAction SilentlyContinue
    if ($null -eq $process) {
        return [ordered]@{ pid = $processId; state = "completed_or_not_running"; process_name = $null }
    }

    return [ordered]@{ pid = $processId; state = "running"; process_name = $process.ProcessName; start_time = $process.StartTime.ToString("o") }
}

function Get-JsonIfPresent {
    param([string]$Path)
    if (-not (Test-Path $Path)) {
        return $null
    }
    try {
        return Get-Content -Path $Path -Raw -ErrorAction Stop | ConvertFrom-Json
    } catch {
        return $null
    }
}

function Get-ValueOrBlank {
    param(
        [object]$Object,
        [string]$Name
    )
    if ($null -eq $Object) {
        return ""
    }
    $property = $Object.PSObject.Properties[$Name]
    if ($null -eq $property) {
        return ""
    }
    return $property.Value
}

$processState = Get-SmokeProcessState
$status = Get-JsonIfPresent -Path $StatusPath
$metrics = Get-JsonIfPresent -Path $MetricsPath

Write-Host "Detached resume smoke status"
Write-Host "Output folder: $SmokeRoot"
Write-Host "PID exists: $(Test-Path $PidPath)"
Write-Host "Process state: $($processState.state)"
Write-Host "PID: $($processState.pid)"
if ($processState.process_name) {
    Write-Host "Process name: $($processState.process_name)"
}

if (Test-Path $HeartbeatPath) {
    $heartbeat = Get-Item $HeartbeatPath
    Write-Host "Heartbeat: $HeartbeatPath last_write=$($heartbeat.LastWriteTime.ToString('o'))"
} else {
    Write-Host "Heartbeat: not found"
}

Write-Host "stdout: $StdoutLog exists=$(Test-Path $StdoutLog)"
Write-Host "stderr: $StderrLog exists=$(Test-Path $StderrLog)"

if ($metrics) {
    Write-Host "Evaluation count: $(Get-ValueOrBlank -Object $metrics -Name 'completed_evaluations')"
    Write-Host "Failed evaluations: $(Get-ValueOrBlank -Object $metrics -Name 'failed_evaluations')"
    Write-Host "Duplicate conflicts: $(Get-ValueOrBlank -Object $metrics -Name 'duplicate_conflicts')"
    Write-Host "Rows have metadata: $(Get-ValueOrBlank -Object $metrics -Name 'rows_have_required_metadata')"
    Write-Host "Unique evaluation keys: $(Get-ValueOrBlank -Object $metrics -Name 'unique_evaluation_keys')"
} elseif ($status) {
    Write-Host "Evaluation count: $(Get-ValueOrBlank -Object $status -Name 'completed_evaluations')"
    Write-Host "Failed evaluations: $(Get-ValueOrBlank -Object $status -Name 'failed_evaluations')"
    Write-Host "Duplicate conflicts: $(Get-ValueOrBlank -Object $status -Name 'duplicate_conflicts')"
    Write-Host "Rows have metadata: $(Get-ValueOrBlank -Object $status -Name 'rows_have_required_metadata')"
    Write-Host "Unique evaluation keys: $(Get-ValueOrBlank -Object $status -Name 'unique_evaluation_keys')"
} else {
    Write-Host "Metrics/status: not complete yet"
}

Write-Host ""
Write-Host "---- stdout tail ----"
if (Test-Path $StdoutLog) {
    Get-Content -Path $StdoutLog -Tail 20 -ErrorAction SilentlyContinue
} else {
    Write-Host "not found"
}

Write-Host ""
Write-Host "---- stderr tail ----"
if (Test-Path $StderrLog) {
    Get-Content -Path $StderrLog -Tail 20 -ErrorAction SilentlyContinue
} else {
    Write-Host "not found"
}
