Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $ScriptDir
$SmokeRoot = Join-Path $RepoRoot "reports\optimization\detached_resume_smoke\run"
$LogsDir = Join-Path $SmokeRoot "logs"
$ManifestPath = "C:\LAB\tradingview-lab\MTC_V2_OPTIMIZATION_DATA_BUNDLE_20260427\manifests\dataset_manifest.json"
$RegimesPath = "C:\LAB\tradingview-lab\MTC_V2_OPTIMIZATION_DATA_BUNDLE_20260427\regimes\regime_registry.json"
$StdoutLog = Join-Path $LogsDir "detached_smoke_stdout.log"
$StderrLog = Join-Path $LogsDir "detached_smoke_stderr.log"
$RunStatusJson = Join-Path $SmokeRoot "run_status.json"
$PidPath = Join-Path $SmokeRoot "run_process.pid"
$ChildScript = Join-Path $SmokeRoot "detached_smoke_child.ps1"

New-Item -ItemType Directory -Force -Path $LogsDir | Out-Null

$env:OMP_NUM_THREADS = "1"
$env:MKL_NUM_THREADS = "1"
$env:OPENBLAS_NUM_THREADS = "1"
$env:NUMEXPR_NUM_THREADS = "1"

$smokeCommand = @"
Set-StrictMode -Version Latest
`$ErrorActionPreference = "Stop"
Set-Location -LiteralPath "$RepoRoot"
`$env:OMP_NUM_THREADS = "1"
`$env:MKL_NUM_THREADS = "1"
`$env:OPENBLAS_NUM_THREADS = "1"
`$env:NUMEXPR_NUM_THREADS = "1"
python -m tools.run_detached_resume_smoke --manifest "$ManifestPath" --regimes "$RegimesPath" --out reports/optimization/detached_resume_smoke/run --max-workers 2 --max-evaluations 12 --post-run-heartbeats 6 --heartbeat-interval-seconds 2
`$exitCode = `$LASTEXITCODE
if (Test-Path "$RunStatusJson") {
  `$status = Get-Content -Path "$RunStatusJson" -Raw | ConvertFrom-Json
  `$status | Add-Member -NotePropertyName detached_shell_exit_code -NotePropertyValue `$exitCode -Force
  `$status | ConvertTo-Json -Depth 8 | Set-Content -Path "$RunStatusJson" -Encoding utf8
}
exit `$exitCode
"@

Set-Content -Path $ChildScript -Value $smokeCommand -Encoding utf8

$argumentList = "-NoProfile -ExecutionPolicy Bypass -File `"$ChildScript`""
$smokeProcess = Start-Process -FilePath "powershell.exe" -WindowStyle Hidden -PassThru -RedirectStandardOutput $StdoutLog -RedirectStandardError $StderrLog -ArgumentList $argumentList

Set-Content -Path $PidPath -Value $smokeProcess.Id -Encoding ascii

Write-Host "Detached resume smoke started."
Write-Host "PID: $($smokeProcess.Id)"
Write-Host "Output: $SmokeRoot"
Write-Host "stdout: $StdoutLog"
Write-Host "stderr: $StderrLog"
Write-Host "status: $RunStatusJson"
