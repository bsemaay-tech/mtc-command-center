# C2: P2 supervisor wrapper - restarts the bridge on crash, logs to data/logs.
# Registered as Task Scheduler job "MTC-Bridge-P2" (at logon). Testnet only.
$ErrorActionPreference = 'Continue'
$root = Split-Path -Parent $PSScriptRoot
$logDir = Join-Path $root 'data\logs'
New-Item -ItemType Directory -Force $logDir | Out-Null
Set-Location $root
$env:PYTHONUTF8 = '1'
while ($true) {
    $stamp = Get-Date -Format 'yyyyMMdd'
    $log = Join-Path $logDir "bridge_$stamp.log"
    "[$(Get-Date -Format o)] supervisor: starting bridge" | Out-File -Append -Encoding utf8 $log
    & python -m bridge.app *>> $log
    "[$(Get-Date -Format o)] supervisor: bridge exited (code=$LASTEXITCODE); restarting in 10s" | Out-File -Append -Encoding utf8 $log
    Start-Sleep -Seconds 10
}
