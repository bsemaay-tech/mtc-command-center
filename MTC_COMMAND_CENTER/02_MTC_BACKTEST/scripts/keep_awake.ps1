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
        [void][KeepAwakeNative]::SetThreadExecutionState($ES_CONTINUOUS -bor $ES_SYSTEM_REQUIRED -bor $ES_DISPLAY_REQUIRED)
        Start-Sleep -Seconds 30
    }
}
finally {
    [void][KeepAwakeNative]::SetThreadExecutionState($ES_CONTINUOUS)
}
