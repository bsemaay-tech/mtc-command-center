param(
    [int]$TimeBudgetMinutes = 720
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$RepoRoot = "C:\LAB\tradingview-lab\01_MASTER TEMPLATE_V2"
$ScriptDir = Join-Path $RepoRoot "scripts"
$RunRoot = Join-Path $RepoRoot "reports\optimization\12h_backtesting_session"
$DetachedDir = Join-Path $RunRoot "detached"
$LogsDir = Join-Path $RunRoot "logs"
$HeartbeatDir = Join-Path $RunRoot "heartbeat"
$CheckpointsDir = Join-Path $RunRoot "checkpoints"
$ReportsDir = Join-Path $RunRoot "reports"
$ManifestPath = "C:\LAB\tradingview-lab\MTC_V2_OPTIMIZATION_DATA_BUNDLE_20260427\manifests\dataset_manifest.json"
$RegimesPath = "C:\LAB\tradingview-lab\MTC_V2_OPTIMIZATION_DATA_BUNDLE_20260427\regimes\regime_registry.json"
$RelativeOut = "reports/optimization/12h_backtesting_session"
$StdoutLog = Join-Path $LogsDir "stdout.log"
$StderrLog = Join-Path $LogsDir "stderr.log"
$PidPath = Join-Path $DetachedDir "run_process.pid"
$RunStatusJson = Join-Path $DetachedDir "run_status.json"
$InnerRunnerScript = Join-Path $DetachedDir "run_optimizer.ps1"
$KeepAwakeScript = Join-Path $ScriptDir "keep_awake_overnight_optimization.ps1"
$KeepAwakePidPath = Join-Path $DetachedDir "keep_awake_process.pid"

Set-Location $RepoRoot

foreach ($dir in @($RunRoot, $DetachedDir, $LogsDir, $HeartbeatDir, $CheckpointsDir, $ReportsDir)) {
    New-Item -ItemType Directory -Force -Path $dir | Out-Null
}

$env:OMP_NUM_THREADS = "1"
$env:MKL_NUM_THREADS = "1"
$env:OPENBLAS_NUM_THREADS = "1"
$env:NUMEXPR_NUM_THREADS = "1"

if (Test-Path -LiteralPath $KeepAwakeScript) {
    $keepAwakeSeconds = [Math]::Max(($TimeBudgetMinutes * 60) + 1800, 3600)
    $keepAwakeArguments = "-NoProfile -ExecutionPolicy Bypass -File `"$KeepAwakeScript`" -ReportRoot `"$RelativeOut`" -Seconds $keepAwakeSeconds"
    $keepAwakeProcess = Start-Process -FilePath "powershell.exe" -WindowStyle Hidden -PassThru -ArgumentList $keepAwakeArguments
    Set-Content -Path $KeepAwakePidPath -Value $keepAwakeProcess.Id -Encoding ascii
}

$initialStatus = [ordered]@{
    started_at = (Get-Date).ToString("o")
    status = "launching"
    launcher_pid = $PID
    max_workers = 16
    time_budget_minutes = $TimeBudgetMinutes
    manifest = $ManifestPath
    regimes = $RegimesPath
    out = $RelativeOut
    output_root = $RunRoot
    stdout = $StdoutLog
    stderr = $StderrLog
    thread_pinning = [ordered]@{
        OMP_NUM_THREADS = $env:OMP_NUM_THREADS
        MKL_NUM_THREADS = $env:MKL_NUM_THREADS
        OPENBLAS_NUM_THREADS = $env:OPENBLAS_NUM_THREADS
        NUMEXPR_NUM_THREADS = $env:NUMEXPR_NUM_THREADS
    }
}
$initialStatus | ConvertTo-Json -Depth 8 | Set-Content -Path $RunStatusJson -Encoding utf8

$optimizerScript = @"
Set-StrictMode -Version Latest
`$ErrorActionPreference = "Stop"
Set-Location "$RepoRoot"
`$env:OMP_NUM_THREADS = "1"
`$env:MKL_NUM_THREADS = "1"
`$env:OPENBLAS_NUM_THREADS = "1"
`$env:NUMEXPR_NUM_THREADS = "1"
python tools/run_12h_backtesting_session.py --manifest "$ManifestPath" --regimes "$RegimesPath" --out $RelativeOut --max-workers 16 --time-budget-minutes $TimeBudgetMinutes
`$exitCode = `$LASTEXITCODE
if (`$exitCode -ne 0) {
    `$status = @{
        status = "failed"
        ended_at = (Get-Date).ToString("o")
        exit_code = `$exitCode
        max_workers = 16
        time_budget_minutes = $TimeBudgetMinutes
        manifest = "$ManifestPath"
        regimes = "$RegimesPath"
        out = "$RelativeOut"
        output_root = "$RunRoot"
        thread_pinning = @{
            OMP_NUM_THREADS = `$env:OMP_NUM_THREADS
            MKL_NUM_THREADS = `$env:MKL_NUM_THREADS
            OPENBLAS_NUM_THREADS = `$env:OPENBLAS_NUM_THREADS
            NUMEXPR_NUM_THREADS = `$env:NUMEXPR_NUM_THREADS
        }
    }
    `$status | ConvertTo-Json -Depth 8 | Set-Content -Path "$RunStatusJson" -Encoding utf8
}
exit `$exitCode
"@

Set-Content -Path $InnerRunnerScript -Value $optimizerScript -Encoding utf8

foreach ($logPath in @($StdoutLog, $StderrLog)) {
    if (Test-Path -LiteralPath $logPath) {
        $stamp = Get-Date -Format "yyyyMMdd_HHmmss"
        Move-Item -LiteralPath $logPath -Destination "$logPath.previous_$stamp" -Force
    }
}

$optimizerArguments = "-NoProfile -ExecutionPolicy Bypass -File `"$InnerRunnerScript`""
$optimizerProcess = Start-Process -FilePath "powershell.exe" -WindowStyle Hidden -PassThru -RedirectStandardOutput $StdoutLog -RedirectStandardError $StderrLog -ArgumentList $optimizerArguments

Set-Content -Path $PidPath -Value $optimizerProcess.Id -Encoding ascii

Write-Host "Detached 12h backtesting session started."
Write-Host "PID: $($optimizerProcess.Id)"
Write-Host "stdout: $StdoutLog"
Write-Host "stderr: $StderrLog"
Write-Host "status: $RunStatusJson"
