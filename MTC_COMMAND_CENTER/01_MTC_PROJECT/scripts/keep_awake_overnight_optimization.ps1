param(
    [string]$ReportRoot = "reports/optimization/overnight_optimization",
    [int]$Seconds = 25200
)

$ErrorActionPreference = "Continue"
$root = Resolve-Path -LiteralPath "."
$reportPath = Join-Path $root $ReportRoot
New-Item -ItemType Directory -Force -Path $reportPath | Out-Null
$statusPath = Join-Path $reportPath "power_prevention_status.md"
$settingsPath = Join-Path $reportPath "power_settings_before.txt"
$logPath = Join-Path $reportPath "logs/keep_awake.log"
New-Item -ItemType Directory -Force -Path (Split-Path $logPath) | Out-Null

"# Power Prevention Status`n" | Set-Content -Path $statusPath -Encoding UTF8
"Started: $(Get-Date -Format o)" | Add-Content -Path $statusPath -Encoding UTF8

try {
    powercfg /query > $settingsPath 2>&1
    "- powercfg query captured: yes" | Add-Content -Path $statusPath -Encoding UTF8
} catch {
    "- powercfg query captured: no - $($_.Exception.Message)" | Add-Content -Path $statusPath -Encoding UTF8
}

Add-Type -TypeDefinition @"
using System;
using System.Runtime.InteropServices;
public static class SleepUtil {
    [DllImport("kernel32.dll", SetLastError = true)]
    public static extern uint SetThreadExecutionState(uint esFlags);
}
"@

$ES_CONTINUOUS = [uint32]"0x80000000"
$ES_SYSTEM_REQUIRED = [uint32]"0x00000001"
$ES_DISPLAY_REQUIRED = [uint32]"0x00000002"
$flags = $ES_CONTINUOUS -bor $ES_SYSTEM_REQUIRED -bor $ES_DISPLAY_REQUIRED
$end = (Get-Date).AddSeconds($Seconds)

try {
    "- SetThreadExecutionState loop: active" | Add-Content -Path $statusPath -Encoding UTF8
    while ((Get-Date) -lt $end) {
        [void][SleepUtil]::SetThreadExecutionState($flags)
        "$(Get-Date -Format o) keep-awake pulse" | Add-Content -Path $logPath -Encoding UTF8
        Start-Sleep -Seconds 55
    }
    "- Completed: $(Get-Date -Format o)" | Add-Content -Path $statusPath -Encoding UTF8
} finally {
    [void][SleepUtil]::SetThreadExecutionState($ES_CONTINUOUS)
    "- Restored SetThreadExecutionState continuous state: $(Get-Date -Format o)" | Add-Content -Path $statusPath -Encoding UTF8
}
