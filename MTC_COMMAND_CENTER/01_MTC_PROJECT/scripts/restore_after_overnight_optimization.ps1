param(
    [string]$ReportRoot = "reports/optimization/overnight_optimization"
)

$ErrorActionPreference = "Continue"
$root = Resolve-Path -LiteralPath "."
$reportPath = Join-Path $root $ReportRoot
$statusPath = Join-Path $reportPath "power_prevention_status.md"

Add-Type -TypeDefinition @"
using System;
using System.Runtime.InteropServices;
public static class SleepUtilRestore {
    [DllImport("kernel32.dll", SetLastError = true)]
    public static extern uint SetThreadExecutionState(uint esFlags);
}
"@

$ES_CONTINUOUS = [uint32]"0x80000000"
[void][SleepUtilRestore]::SetThreadExecutionState($ES_CONTINUOUS)
"`nRestore script ran: $(Get-Date -Format o)" | Add-Content -Path $statusPath -Encoding UTF8
