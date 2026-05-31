param(
    [switch]$KeepDisplayOn,
    [int]$PulseSeconds = 30
)

Add-Type @"
using System;
using System.Runtime.InteropServices;
public static class KeepAwakeNative {
    [DllImport("kernel32.dll")]
    public static extern uint SetThreadExecutionState(uint esFlags);
}
"@

$ES_CONTINUOUS = [UInt32]2147483648
$ES_SYSTEM_REQUIRED = [UInt32]1
$ES_DISPLAY_REQUIRED = [UInt32]2

try {
    while ($true) {
        $flags = $ES_CONTINUOUS -bor $ES_SYSTEM_REQUIRED
        if ($KeepDisplayOn) {
            $flags = $flags -bor $ES_DISPLAY_REQUIRED
        }
        [void][KeepAwakeNative]::SetThreadExecutionState($flags)
        Start-Sleep -Seconds $PulseSeconds
    }
}
finally {
    [void][KeepAwakeNative]::SetThreadExecutionState($ES_CONTINUOUS)
}
