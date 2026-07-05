# Prevent the machine from sleeping while the overnight sweep runs (no admin needed).
Add-Type -Namespace Win32 -Name Power -MemberDefinition @'
[System.Runtime.InteropServices.DllImport("kernel32.dll")]
public static extern uint SetThreadExecutionState(uint esFlags);
'@
$ES_CONTINUOUS = [uint32]"0x80000000"
$ES_SYSTEM     = [uint32]"0x00000001"
$ES_DISPLAY    = [uint32]"0x00000002"
$deadline = Get-Date "2026-06-30 08:35:00"
while ((Get-Date) -lt $deadline) {
    [Win32.Power]::SetThreadExecutionState($ES_CONTINUOUS -bor $ES_SYSTEM -bor $ES_DISPLAY) | Out-Null
    Start-Sleep -Seconds 50
}
[Win32.Power]::SetThreadExecutionState($ES_CONTINUOUS) | Out-Null
