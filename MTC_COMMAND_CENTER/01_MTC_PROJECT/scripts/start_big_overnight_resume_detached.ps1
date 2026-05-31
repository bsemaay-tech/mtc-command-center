Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $ScriptDir
$RunRoot = Join-Path $RepoRoot "reports\optimization\big_overnight_multiasset"
$LogsDir = Join-Path $RunRoot "logs"
$ManifestPath = "C:\LAB\tradingview-lab\MTC_V2_OPTIMIZATION_DATA_BUNDLE_20260427\manifests\dataset_manifest.json"
$RegimesPath = "C:\LAB\tradingview-lab\MTC_V2_OPTIMIZATION_DATA_BUNDLE_20260427\regimes\regime_registry.json"
$StdoutLog = Join-Path $LogsDir "detached_resume_stdout.log"
$StderrLog = Join-Path $LogsDir "detached_resume_stderr.log"
$RunStatusJson = Join-Path $LogsDir "detached_resume_status.json"
$PidPath = Join-Path $RunRoot "run_process.pid"
$KeepAwakeScript = Join-Path $ScriptDir "keep_awake_big_overnight_optimization.ps1"
$KeepAwakePidPath = Join-Path $RunRoot "keep_awake_process.pid"

New-Item -ItemType Directory -Force -Path $LogsDir | Out-Null

$env:OMP_NUM_THREADS = "1"
$env:MKL_NUM_THREADS = "1"
$env:OPENBLAS_NUM_THREADS = "1"
$env:NUMEXPR_NUM_THREADS = "1"

if (Test-Path $KeepAwakeScript) {
    $keepAwakeProcess = Start-Process -FilePath "powershell.exe" -WindowStyle Hidden -PassThru -ArgumentList @(
        "-NoProfile",
        "-ExecutionPolicy",
        "Bypass",
        "-File",
        $KeepAwakeScript
    )
    Set-Content -Path $KeepAwakePidPath -Value $keepAwakeProcess.Id -Encoding ascii
}

$optimizerCommand = @"
Set-StrictMode -Version Latest
`$ErrorActionPreference = "Stop"
Set-Location "$RepoRoot"
`$env:OMP_NUM_THREADS = "1"
`$env:MKL_NUM_THREADS = "1"
`$env:OPENBLAS_NUM_THREADS = "1"
`$env:NUMEXPR_NUM_THREADS = "1"
`$status = [ordered]@{
  started_at = (Get-Date).ToString("o")
  status = "running"
  max_workers = 16
  time_budget_minutes = 480
  max_assets = 8
  manifest = "$ManifestPath"
  regimes = "$RegimesPath"
  out = "reports/optimization/big_overnight_multiasset"
}
`$status | ConvertTo-Json -Depth 4 | Set-Content -Path "$RunStatusJson" -Encoding utf8
python tools/run_big_overnight_multiasset_optimization.py --manifest "$ManifestPath" --regimes "$RegimesPath" --out reports/optimization/big_overnight_multiasset --max-workers 16 --time-budget-minutes 480 --max-assets 8
`$exitCode = `$LASTEXITCODE
`$status.status = if (`$exitCode -eq 0) { "completed" } else { "failed" }
`$status.ended_at = (Get-Date).ToString("o")
`$status.exit_code = `$exitCode
`$status | ConvertTo-Json -Depth 4 | Set-Content -Path "$RunStatusJson" -Encoding utf8
exit `$exitCode
"@

$optimizerProcess = Start-Process -FilePath "powershell.exe" -WindowStyle Hidden -PassThru -RedirectStandardOutput $StdoutLog -RedirectStandardError $StderrLog -ArgumentList @(
    "-NoProfile",
    "-ExecutionPolicy",
    "Bypass",
    "-Command",
    $optimizerCommand
)

Set-Content -Path $PidPath -Value $optimizerProcess.Id -Encoding ascii

Write-Host "Detached big overnight resume started."
Write-Host "PID: $($optimizerProcess.Id)"
Write-Host "stdout: $StdoutLog"
Write-Host "stderr: $StderrLog"
Write-Host "status: $RunStatusJson"
