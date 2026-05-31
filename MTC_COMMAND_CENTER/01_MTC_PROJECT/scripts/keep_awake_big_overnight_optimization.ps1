param(
    [string]$HeartbeatPath = "reports/optimization/big_overnight_multiasset/power/heartbeat.log",
    [int]$HeartbeatSeconds = 300
)

$ErrorActionPreference = "Continue"
$heartbeatFullPath = [System.IO.Path]::GetFullPath($HeartbeatPath)
$heartbeatDir = [System.IO.Path]::GetDirectoryName($heartbeatFullPath)
New-Item -ItemType Directory -Force -Path $heartbeatDir | Out-Null

Add-Type -Namespace Win32 -Name NativeMethods -MemberDefinition @"
[System.Runtime.InteropServices.DllImport("kernel32.dll", SetLastError = true)]
public static extern uint SetThreadExecutionState(uint esFlags);
"@

$ES_CONTINUOUS = [Convert]::ToUInt32("80000000", 16)
$ES_SYSTEM_REQUIRED = [Convert]::ToUInt32("00000001", 16)
$ES_DISPLAY_REQUIRED = [Convert]::ToUInt32("00000002", 16)

"$(Get-Date -Format o) keep-awake started pid=$PID heartbeat_seconds=$HeartbeatSeconds" | Out-File -FilePath $heartbeatFullPath -Encoding utf8 -Append

while ($true) {
    try {
        [void][Win32.NativeMethods]::SetThreadExecutionState($ES_CONTINUOUS -bor $ES_SYSTEM_REQUIRED -bor $ES_DISPLAY_REQUIRED)
        "$(Get-Date -Format o) awake heartbeat pid=$PID" | Out-File -FilePath $heartbeatFullPath -Encoding utf8 -Append
    } catch {
        "$(Get-Date -Format o) keep-awake error: $($_.Exception.Message)" | Out-File -FilePath $heartbeatFullPath -Encoding utf8 -Append
    }
    Start-Sleep -Seconds $HeartbeatSeconds
}
