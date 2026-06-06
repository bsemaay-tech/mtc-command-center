$ErrorActionPreference = "Stop"

$tools = "C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\03_QUANTLENS\tools"
$results = "C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\03_QUANTLENS\05_BACKTEST_RESULTS\confirm_2026-06-04"
$heartbeat = Join-Path $tools "overnight_runs\_heartbeat_confirm_morning_watchdog.json"
$log = Join-Path $tools "overnight_runs\confirm_morning_watchdog_2026-06-04.log"
$done = Join-Path $tools "overnight_runs\confirm_morning_watchdog_2026-06-04.DONE"
$deadline = [datetime]"2026-06-05T07:30:00"

New-Item -ItemType Directory -Force -Path (Split-Path $log) | Out-Null
Remove-Item -Path $done -ErrorAction SilentlyContinue

Add-Type @"
using System;
using System.Runtime.InteropServices;
public static class AwakeConfirmWatchdog {
    [DllImport("kernel32.dll")]
    public static extern uint SetThreadExecutionState(uint esFlags);
}
"@

$ES_CONTINUOUS = [Convert]::ToUInt32("80000000", 16)
$ES_SYSTEM_REQUIRED = [uint32]0x00000001
$ES_AWAYMODE_REQUIRED = [uint32]0x00000040

function Keep-Awake {
    [AwakeConfirmWatchdog]::SetThreadExecutionState($ES_CONTINUOUS -bor $ES_SYSTEM_REQUIRED -bor $ES_AWAYMODE_REQUIRED) | Out-Null
}

function Count-Files([string]$path, [string]$filter) {
    if (-not (Test-Path $path)) { return 0 }
    return @(Get-ChildItem -Path $path -Filter $filter -File -ErrorAction SilentlyContinue).Count
}

function Write-WatchdogStatus([string]$status) {
    Keep-Awake
    $payload = [ordered]@{
        ts = (Get-Date).ToString("o")
        mode = "confirm_morning_watchdog_2026-06-04"
        status = $status
        deadline = $deadline.ToString("o")
        artifacts = [ordered]@{
            morning_report = Test-Path (Join-Path $results "MORNING_REPORT_confirm_2026-06-04.md")
            mega_results = Test-Path (Join-Path $results "MEGA_walk_forward_results.json")
            alpha_summary = Test-Path (Join-Path $results "alpha_summary.json")
            cpcv_results = Test-Path (Join-Path $results "cpcv\cpcv_results.json")
            pbo_results = Test-Path (Join-Path $results "pbo\pbo_results.json")
            evaluation_artifacts = Count-Files (Join-Path $results "evaluation_artifacts") "*.eval.json"
            scorecards = Count-Files (Join-Path $results "scorecards") "*.scorecard.json"
        }
    } | ConvertTo-Json -Depth 5
    Set-Content -Path $heartbeat -Value $payload -Encoding ASCII
    Add-Content -Path $log -Value ("[{0}] {1}" -f (Get-Date).ToString("s"), $status) -Encoding ASCII
}

try {
    while ((Get-Date) -lt $deadline) {
        Write-WatchdogStatus "awake"
        Start-Sleep -Seconds 600
    }
    Write-WatchdogStatus "complete"
    New-Item -ItemType File -Path $done -Force | Out-Null
} finally {
    [AwakeConfirmWatchdog]::SetThreadExecutionState($ES_CONTINUOUS) | Out-Null
}
