# Watchdog for the archetypes overnight run. Runs every ~15 min. Relaunches the
# orchestrator only if its PID lockfile is dead AND the run is not complete AND before
# deadline. PID-liveness (not CommandLine matching) per A26.
$ErrorActionPreference = "Continue"
$TOOLS = "C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\03_QUANTLENS\tools"
$RUN   = "C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\03_QUANTLENS\05_BACKTEST_RESULTS\overnight_archetypes_2026-07-03"
$ORCH  = "$TOOLS\overnight_archetypes_resilient_2026-07-03.ps1"
$LOCK  = "$RUN\orchestrator.lock"
$WLOG  = "$RUN\watchdog.log"
$DEADLINE = Get-Date "2026-07-04 08:30:00"
New-Item -ItemType Directory -Force -Path $RUN | Out-Null
function WLog($m){ "[watchdog $(Get-Date -Format 'MM-dd HH:mm:ss')] $m" | Tee-Object -FilePath $WLOG -Append }

if (Test-Path "$RUN\_ALL_DONE.marker") { WLog "run complete - nothing to do"; return }
if ((Get-Date) -ge $DEADLINE) { WLog "past deadline - stop"; return }
if (Test-Path $LOCK) {
  $lp = (Get-Content $LOCK -EA SilentlyContinue | Select-Object -First 1)
  if ($lp -and (Get-Process -Id ([int]$lp) -EA SilentlyContinue)) { WLog "orchestrator alive (PID $lp) - ok"; return }
}
WLog "orchestrator DEAD (no live lock PID) - relaunching"
Start-Process -FilePath "powershell.exe" -ArgumentList "-ExecutionPolicy","Bypass","-WindowStyle","Hidden","-File",$ORCH -WindowStyle Hidden | Out-Null
WLog "relaunched"
