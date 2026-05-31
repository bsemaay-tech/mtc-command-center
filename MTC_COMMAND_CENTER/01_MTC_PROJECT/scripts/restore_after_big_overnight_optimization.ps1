$ErrorActionPreference = "Continue"

Add-Type -Namespace Win32 -Name NativeMethods -MemberDefinition @"
[System.Runtime.InteropServices.DllImport("kernel32.dll", SetLastError = true)]
public static extern uint SetThreadExecutionState(uint esFlags);
"@

$ES_CONTINUOUS = [Convert]::ToUInt32("80000000", 16)
[void][Win32.NativeMethods]::SetThreadExecutionState($ES_CONTINUOUS)

"$(Get-Date -Format o) restored SetThreadExecutionState continuous-only. Stop keep-awake PowerShell process if still running." | Write-Output
