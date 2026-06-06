$ErrorActionPreference = "Stop"

$tools = "C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\03_QUANTLENS\tools"
$bash = "C:\Program Files\Git\bin\bash.exe"
$script = "./overnight_loop_2026-06-03_night.sh"
$out = Join-Path $tools "overnight_runs\night_master_2026-06-03.out"
$err = Join-Path $tools "overnight_runs\night_master_2026-06-03.err"
$pidFile = Join-Path $tools "overnight_runs\night_loop_2026-06-03.wrapper.pid"

New-Item -ItemType Directory -Force -Path (Split-Path $out) | Out-Null

Add-Type @"
using System;
using System.Runtime.InteropServices;
public static class Awake {
    [DllImport("kernel32.dll")]
    public static extern uint SetThreadExecutionState(uint esFlags);
}
"@

$ES_CONTINUOUS = [Convert]::ToUInt32("80000000", 16)
$ES_SYSTEM_REQUIRED = [uint32]0x00000001
$ES_AWAYMODE_REQUIRED = [uint32]0x00000040

function Keep-Awake {
    [Awake]::SetThreadExecutionState($ES_CONTINUOUS -bor $ES_SYSTEM_REQUIRED -bor $ES_AWAYMODE_REQUIRED) | Out-Null
}

Set-Location $tools
Set-Content -Path $pidFile -Value $PID -Encoding ASCII
Keep-Awake

$proc = Start-Process -FilePath $bash -ArgumentList "-lc", $script -WorkingDirectory $tools -RedirectStandardOutput $out -RedirectStandardError $err -WindowStyle Hidden -PassThru
Set-Content -Path (Join-Path $tools "overnight_runs\night_loop_2026-06-03.pid") -Value $proc.Id -Encoding ASCII

while (-not $proc.HasExited) {
    Keep-Awake
    Start-Sleep -Seconds 60
    try {
        $proc.Refresh()
    } catch {
        break
    }
}

[Awake]::SetThreadExecutionState($ES_CONTINUOUS) | Out-Null
