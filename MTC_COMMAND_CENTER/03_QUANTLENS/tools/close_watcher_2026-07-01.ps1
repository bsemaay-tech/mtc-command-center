# Waits for the turtle_heavy run to complete, then runs the mechanical morning close
# WHILE the machine is still awake (right after the orchestrator releases keep-awake).
# Near-zero CPU while polling; asserts keep-awake only during the brief close.
$ErrorActionPreference = "Continue"
$TOOLS   = "C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\03_QUANTLENS\tools"
$HEAVY   = "C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\03_QUANTLENS\05_BACKTEST_RESULTS\turtle_heavy_2026-07-01"
$PY      = "C:\Python314\python.exe"
$DONE    = "$HEAVY\_ALL_DONE.marker"
$CLOSED  = "$HEAVY\_CLOSE_DONE.marker"
$LOG     = "$HEAVY\close_watcher.log"
$DEADLINE= Get-Date "2026-07-02 08:30:00"

Add-Type -Namespace Win32b -Name Power -MemberDefinition @'
[System.Runtime.InteropServices.DllImport("kernel32.dll")]
public static extern uint SetThreadExecutionState(uint esFlags);
'@
$ES_CONTINUOUS=[uint32]"0x80000000"; $ES_SYSTEM=[uint32]"0x00000001"

function Log($m){ "[watch $(Get-Date -Format HH:mm:ss)] $m" | Tee-Object -FilePath $LOG -Append }

if (Test-Path $CLOSED) { Log "already closed - exit"; return }
Log "watcher up; waiting for $DONE (deadline $DEADLINE)"
while (-not (Test-Path $DONE)) {
  if ((Get-Date) -ge $DEADLINE) { Log "deadline reached before ALL_DONE - closing on partial artifacts"; break }
  Start-Sleep -Seconds 60
}
# Keep awake through the (brief) close, then release.
[Win32b.Power]::SetThreadExecutionState($ES_CONTINUOUS -bor $ES_SYSTEM) | Out-Null
Log "running mechanical close"
& $PY "$TOOLS\morning_close_turtle_20260701.py" *>> $LOG
"closed $(Get-Date -Format o)" | Set-Content $CLOSED
Log "close done -> $HEAVY\MORNING_REPORT.md ; releasing keep-awake"
[Win32b.Power]::SetThreadExecutionState($ES_CONTINUOUS) | Out-Null
