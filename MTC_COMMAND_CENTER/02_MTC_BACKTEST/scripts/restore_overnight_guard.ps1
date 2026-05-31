param(
    [string]$StatePath = "$PSScriptRoot\overnight_guard_state.json"
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path $StatePath)) {
    Write-Output "overnight_guard=NO_STATE"
    exit 0
}

$state = Get-Content -Path $StatePath -Raw | ConvertFrom-Json
$schemeGuid = [string]$state.scheme_guid

foreach ($procId in @($state.processes.keep_awake_pid, $state.processes.shutdown_abort_pid)) {
    if ($procId) {
        Stop-Process -Id ([int]$procId) -ErrorAction SilentlyContinue
    }
}

powercfg /setacvalueindex $schemeGuid SUB_SLEEP STANDBYIDLE ([int]$state.power.standby_ac) | Out-Null
powercfg /setdcvalueindex $schemeGuid SUB_SLEEP STANDBYIDLE ([int]$state.power.standby_dc) | Out-Null
powercfg /setacvalueindex $schemeGuid SUB_SLEEP HIBERNATEIDLE ([int]$state.power.hibernate_ac) | Out-Null
powercfg /setdcvalueindex $schemeGuid SUB_SLEEP HIBERNATEIDLE ([int]$state.power.hibernate_dc) | Out-Null
powercfg /setacvalueindex $schemeGuid SUB_SLEEP RTCWAKE ([int]$state.power.rtcwake_ac) | Out-Null
powercfg /setdcvalueindex $schemeGuid SUB_SLEEP RTCWAKE ([int]$state.power.rtcwake_dc) | Out-Null
powercfg /setactive $schemeGuid | Out-Null

if (Test-Path $StatePath) {
    Remove-Item -Path $StatePath -Force
}

Write-Output "overnight_guard=RESTORED"
Write-Output "scheme_guid=$schemeGuid"
