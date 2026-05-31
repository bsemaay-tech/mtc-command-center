param(
    [int]$TimeBudgetMinutes = 480,
    [int]$MaxParamsPerStrategy = 1000000
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$RepoRoot = "C:\LAB\tradingview-lab\01_MASTER TEMPLATE_V2"
$RunRoot = Join-Path $RepoRoot "06_QUANTLENS_LAB\05_BACKTEST_RESULTS\overnight_research_20260501"
$DetachedDir = Join-Path $RunRoot "detached"
$LogsDir = Join-Path $RunRoot "logs"
$StdoutLog = Join-Path $LogsDir "stdout.log"
$StderrLog = Join-Path $LogsDir "stderr.log"
$PidPath = Join-Path $DetachedDir "run_process.pid"
$RunStatusJson = Join-Path $DetachedDir "run_status.json"
$InnerRunnerScript = Join-Path $DetachedDir "run_quantlens_overnight_research.ps1"
$ManifestPath = "C:\LAB\tradingview-lab\MTC_V2_OPTIMIZATION_DATA_BUNDLE_20260427\manifests\dataset_manifest.json"
$RelativeOut = "06_QUANTLENS_LAB/05_BACKTEST_RESULTS/overnight_research_20260501"

Set-Location $RepoRoot

foreach ($dir in @($RunRoot, $DetachedDir, $LogsDir)) {
    New-Item -ItemType Directory -Force -Path $dir | Out-Null
}

$env:OMP_NUM_THREADS = "1"
$env:MKL_NUM_THREADS = "1"
$env:OPENBLAS_NUM_THREADS = "1"
$env:NUMEXPR_NUM_THREADS = "1"

$initialStatus = [ordered]@{
    started_at = (Get-Date).ToString("o")
    status = "launching"
    launcher_pid = $PID
    time_budget_minutes = $TimeBudgetMinutes
    max_params_per_strategy = $MaxParamsPerStrategy
    manifest = $ManifestPath
    out = $RelativeOut
    output_root = $RunRoot
    stdout = $StdoutLog
    stderr = $StderrLog
}
$initialStatus | ConvertTo-Json -Depth 6 | Set-Content -Path $RunStatusJson -Encoding utf8

$runnerScript = @"
Set-StrictMode -Version Latest
`$ErrorActionPreference = "Stop"
Set-Location "$RepoRoot"
`$env:OMP_NUM_THREADS = "1"
`$env:MKL_NUM_THREADS = "1"
`$env:OPENBLAS_NUM_THREADS = "1"
`$env:NUMEXPR_NUM_THREADS = "1"
python 06_QUANTLENS_LAB/tools/run_quantlens_overnight_research.py --manifest "$ManifestPath" --out "$RelativeOut" --time-budget-minutes $TimeBudgetMinutes --max-params-per-strategy $MaxParamsPerStrategy --no-verify-sha
`$exitCode = `$LASTEXITCODE
if (`$exitCode -ne 0) {
    `$status = @{
        status = "failed"
        ended_at = (Get-Date).ToString("o")
        exit_code = `$exitCode
        manifest = "$ManifestPath"
        out = "$RelativeOut"
        output_root = "$RunRoot"
    }
    `$status | ConvertTo-Json -Depth 6 | Set-Content -Path "$RunStatusJson" -Encoding utf8
}
exit `$exitCode
"@

Set-Content -Path $InnerRunnerScript -Value $runnerScript -Encoding utf8

foreach ($logPath in @($StdoutLog, $StderrLog)) {
    if (Test-Path -LiteralPath $logPath) {
        $stamp = Get-Date -Format "yyyyMMdd_HHmmss"
        Move-Item -LiteralPath $logPath -Destination "$logPath.previous_$stamp" -Force
    }
}

$arguments = "-NoProfile -ExecutionPolicy Bypass -File `"$InnerRunnerScript`""
$process = Start-Process -FilePath "powershell.exe" -WindowStyle Hidden -PassThru -RedirectStandardOutput $StdoutLog -RedirectStandardError $StderrLog -ArgumentList $arguments
Set-Content -Path $PidPath -Value $process.Id -Encoding ascii

Write-Host "Detached QuantLens overnight research started."
Write-Host "PID: $($process.Id)"
Write-Host "stdout: $StdoutLog"
Write-Host "stderr: $StderrLog"
Write-Host "status: $RunStatusJson"
