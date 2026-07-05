# Watchdog for the resilient 2026-07-02 21:00 overnight run. Runs every ~15 min (Task
# Scheduler). If the orchestrator process is dead AND the run is not complete AND we are
# before the deadline, relaunch it (it resumes via stage markers + mega --resume). This is
# the fix for the 18:30 failure (orchestrator died mid-stage and stayed dead ~2h).
$ErrorActionPreference = "Continue"
$TOOLS = "C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\03_QUANTLENS\tools"
$RUN   = "C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\03_QUANTLENS\05_BACKTEST_RESULTS\overnight_resilient_2026-07-02"
$ORCH  = "$TOOLS\overnight_resilient_2026-07-02_2100.ps1"
$WLOG  = "$RUN\watchdog.log"
$DEADLINE = Get-Date "2026-07-03 08:30:00"
New-Item -ItemType Directory -Force -Path $RUN | Out-Null
function WLog($m){ "[watchdog $(Get-Date -Format 'MM-dd HH:mm:ss')] $m" | Tee-Object -FilePath $WLOG -Append }

if (Test-Path "$RUN\_ALL_DONE.marker") { WLog "run complete - nothing to do"; return }
if ((Get-Date) -ge $DEADLINE) { WLog "past deadline - stop"; return }

# Liveness via the orchestrator's PID lockfile (robust; CommandLine matching was flaky
# and caused a false-positive double-launch on the first attempt).
$LOCK = "$RUN\orchestrator.lock"
if (Test-Path $LOCK) {
  $lp = (Get-Content $LOCK -ErrorAction SilentlyContinue | Select-Object -First 1)
  if ($lp -and (Get-Process -Id ([int]$lp) -ErrorAction SilentlyContinue)) { WLog "orchestrator alive (PID $lp) - ok"; return }
}
WLog "orchestrator DEAD (no live lock PID) - relaunching (resumes via markers + checkpoint)"
Start-Process -FilePath "powershell.exe" -ArgumentList "-ExecutionPolicy","Bypass","-WindowStyle","Hidden","-File",$ORCH -WindowStyle Hidden | Out-Null
WLog "relaunched"
