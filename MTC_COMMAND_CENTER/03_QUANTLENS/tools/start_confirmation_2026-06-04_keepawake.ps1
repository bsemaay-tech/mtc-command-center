$ErrorActionPreference = "Stop"

$tools = "C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\03_QUANTLENS\tools"
$bash = "C:\Program Files\Git\bin\bash.exe"
$script = "./run_confirmation_2026-06-04.sh"
$out = Join-Path $tools "overnight_runs\confirm_master_2026-06-04.out"
$err = Join-Path $tools "overnight_runs\confirm_master_2026-06-04.err"
$wrapperPidFile = Join-Path $tools "overnight_runs\confirm_loop_2026-06-04.wrapper.pid"
$pidFile = Join-Path $tools "overnight_runs\confirm_loop_2026-06-04.pid"

New-Item -ItemType Directory -Force -Path (Split-Path $out) | Out-Null

Add-Type @"
using System;
using System.Runtime.InteropServices;
public static class AwakeConfirm {
    [DllImport("kernel32.dll")]
    public static extern uint SetThreadExecutionState(uint esFlags);
}
"@

$ES_CONTINUOUS = [Convert]::ToUInt32("80000000", 16)
$ES_SYSTEM_REQUIRED = [uint32]0x00000001
$ES_AWAYMODE_REQUIRED = [uint32]0x00000040

function Keep-Awake {
    [AwakeConfirm]::SetThreadExecutionState($ES_CONTINUOUS -bor $ES_SYSTEM_REQUIRED -bor $ES_AWAYMODE_REQUIRED) | Out-Null
}

if (-not (Test-Path $bash)) {
    throw "Git Bash not found at $bash"
}
if (-not (Test-Path (Join-Path $tools "run_confirmation_2026-06-04.sh"))) {
    throw "Confirmation launcher missing"
}

Set-Location $tools
Set-Content -Path $wrapperPidFile -Value $PID -Encoding ASCII
Keep-Awake

$proc = Start-Process -FilePath $bash -ArgumentList "-lc", $script -WorkingDirectory $tools -RedirectStandardOutput $out -RedirectStandardError $err -WindowStyle Hidden -PassThru
Set-Content -Path $pidFile -Value $proc.Id -Encoding ASCII

while (-not $proc.HasExited) {
    Keep-Awake
    Start-Sleep -Seconds 60
    try {
        $proc.Refresh()
    } catch {
        break
    }
}

[AwakeConfirm]::SetThreadExecutionState($ES_CONTINUOUS) | Out-Null
