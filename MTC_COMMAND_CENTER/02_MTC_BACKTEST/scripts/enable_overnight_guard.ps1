param(
    [string]$StatePath = "$PSScriptRoot\overnight_guard_state.json",
    [switch]$KeepDisplayOn
)

$ErrorActionPreference = "Stop"

function Get-ActiveSchemeGuid {
    $output = powercfg /getactivescheme
    if ($output -match "GUID:\s+([a-fA-F0-9-]+)") {
        return $matches[1]
    }
    throw "Unable to detect active power scheme."
}

function Get-PowerIndex {
    param(
        [string]$SchemeGuid,
        [string]$SubGroup,
        [string]$Setting,
        [ValidateSet("AC", "DC")]
        [string]$Line
    )

    $output = (powercfg /query $SchemeGuid $SubGroup $Setting) -join "`n"
    $pattern = if ($Line -eq "AC") {
        "Current AC Power Setting Index:\s+0x([0-9a-fA-F]+)"
    } else {
        "Current DC Power Setting Index:\s+0x([0-9a-fA-F]+)"
    }
    $match = [regex]::Match($output, $pattern)
    if ($match.Success) {
        return [Convert]::ToInt32($match.Groups[1].Value, 16)
    }
    throw "Unable to read $Line value for $SubGroup/$Setting."
}

function Start-GuardProcess {
    param(
        [string]$FilePath,
        [string[]]$Arguments
    )

    return Start-Process -FilePath "powershell.exe" -WindowStyle Hidden -PassThru -ArgumentList $Arguments
}

if (Test-Path $StatePath) {
    & "$PSScriptRoot\restore_overnight_guard.ps1" -StatePath $StatePath | Out-Null
}

$schemeGuid = Get-ActiveSchemeGuid
$state = @{
    created_at = (Get-Date).ToString("o")
    scheme_guid = $schemeGuid
    power = @{
        standby_ac = Get-PowerIndex -SchemeGuid $schemeGuid -SubGroup "SUB_SLEEP" -Setting "STANDBYIDLE" -Line "AC"
        standby_dc = Get-PowerIndex -SchemeGuid $schemeGuid -SubGroup "SUB_SLEEP" -Setting "STANDBYIDLE" -Line "DC"
        hibernate_ac = Get-PowerIndex -SchemeGuid $schemeGuid -SubGroup "SUB_SLEEP" -Setting "HIBERNATEIDLE" -Line "AC"
        hibernate_dc = Get-PowerIndex -SchemeGuid $schemeGuid -SubGroup "SUB_SLEEP" -Setting "HIBERNATEIDLE" -Line "DC"
        rtcwake_ac = Get-PowerIndex -SchemeGuid $schemeGuid -SubGroup "SUB_SLEEP" -Setting "RTCWAKE" -Line "AC"
        rtcwake_dc = Get-PowerIndex -SchemeGuid $schemeGuid -SubGroup "SUB_SLEEP" -Setting "RTCWAKE" -Line "DC"
    }
}

powercfg /setacvalueindex $schemeGuid SUB_SLEEP STANDBYIDLE 0 | Out-Null
powercfg /setdcvalueindex $schemeGuid SUB_SLEEP STANDBYIDLE 0 | Out-Null
powercfg /setacvalueindex $schemeGuid SUB_SLEEP HIBERNATEIDLE 0 | Out-Null
powercfg /setdcvalueindex $schemeGuid SUB_SLEEP HIBERNATEIDLE 0 | Out-Null
powercfg /setacvalueindex $schemeGuid SUB_SLEEP RTCWAKE 0 | Out-Null
powercfg /setdcvalueindex $schemeGuid SUB_SLEEP RTCWAKE 0 | Out-Null
powercfg /setactive $schemeGuid | Out-Null

$keepArgs = @(
    "-NoProfile",
    "-ExecutionPolicy", "Bypass",
    "-File", (Join-Path $PSScriptRoot "keep_system_awake.ps1")
)
if ($KeepDisplayOn) {
    $keepArgs += "-KeepDisplayOn"
}
$keepProc = Start-GuardProcess -FilePath "powershell.exe" -Arguments $keepArgs

$abortArgs = @(
    "-NoProfile",
    "-ExecutionPolicy", "Bypass",
    "-File", (Join-Path $PSScriptRoot "shutdown_abort_watchdog.ps1")
)
$abortProc = Start-GuardProcess -FilePath "powershell.exe" -Arguments $abortArgs

$state.processes = @{
    keep_awake_pid = $keepProc.Id
    shutdown_abort_pid = $abortProc.Id
}
$state.keep_display_on = [bool]$KeepDisplayOn
$state.user = [Environment]::UserName
$state.machine = $env:COMPUTERNAME

$state | ConvertTo-Json -Depth 5 | Set-Content -Path $StatePath -Encoding UTF8

Write-Output "overnight_guard=ENABLED"
Write-Output "state_path=$StatePath"
Write-Output "scheme_guid=$schemeGuid"
Write-Output "keep_awake_pid=$($keepProc.Id)"
Write-Output "shutdown_abort_pid=$($abortProc.Id)"
