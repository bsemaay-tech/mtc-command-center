# =====================================================================
# Resilient overnight 2026-07-03 (16:30 -> 08:30) — NEW ARCHETYPES validation.
# 20 workers. Genuinely-new LOGIC (12 archetypes using volume/gaps/regime/VWAP/etc that
# the confirmed-non-robust existing families ignore). Resilient: per-stage retry + PID
# lockfile (single-instance) + external watchdog + reboot hook. Promotes nothing.
#   Stage A  12 archetypes x multiasset 51x7, 6 rolling folds (deep discovery)
#   Stage B  deep CPCV + PBO on the archetype survivors (heavy validation)
# Inline close + RELEASE when the backlog is exhausted (A22/A24).
# =====================================================================
$ErrorActionPreference = "Continue"
$TOOLS   = "C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\03_QUANTLENS\tools"
$RESULTS = "C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\03_QUANTLENS\05_BACKTEST_RESULTS"
$RUN     = "$RESULTS\overnight_archetypes_2026-07-03"
$ARCH    = "$RUN\archetypes"
$MANIFEST= "C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\03_QUANTLENS\data\native_multiasset_alpaca_2026-06-28\manifests\dataset_manifest.json"
$PY      = "C:\Python314\python.exe"
$DEADLINE= Get-Date "2026-07-04 08:30:00"
$HB      = "$TOOLS\overnight_runs\_heartbeat.json"
$LOG     = "$RUN\orchestrator.log"
$LOCK    = "$RUN\orchestrator.lock"
$STARTUP = Join-Path ([Environment]::GetFolderPath("Startup")) "mcc_archetypes_resume.cmd"

New-Item -ItemType Directory -Force -Path $ARCH, "$TOOLS\overnight_runs" | Out-Null
$env:PYTHONUTF8 = "1"
$env:MEGA_BUNDLE_MANIFEST = $MANIFEST
$env:MEGA_WORKERS = "20"
$env:OMP_NUM_THREADS = "1"; $env:MKL_NUM_THREADS = "1"; $env:OPENBLAS_NUM_THREADS = "1"; $env:NUMEXPR_NUM_THREADS = "1"

Add-Type -Namespace Win32a -Name Power -MemberDefinition @'
[System.Runtime.InteropServices.DllImport("kernel32.dll")]
public static extern uint SetThreadExecutionState(uint esFlags);
'@
$ES_CONTINUOUS=[uint32]"0x80000000"; $ES_SYSTEM=[uint32]"0x00000001"; $ES_DISPLAY=[uint32]"0x00000002"
function KeepAwake { [Win32a.Power]::SetThreadExecutionState($ES_CONTINUOUS -bor $ES_SYSTEM -bor $ES_DISPLAY) | Out-Null }
function ReleaseAwake { [Win32a.Power]::SetThreadExecutionState($ES_CONTINUOUS) | Out-Null }
function Log($m) { "[arch $(Get-Date -Format HH:mm:ss)] $m" | Tee-Object -FilePath $LOG -Append }
function HB($s,$st) { (@{ ts=(Get-Date -Format o); night="2026-07-03-arch"; mode="archetypes"; stage=$s; status=$st; deadline=$DEADLINE.ToString("o") } | ConvertTo-Json -Compress) | Set-Content $HB -Encoding utf8 }
function PastDeadline { return ((Get-Date) -ge $DEADLINE) }
function RunRetry($label, $argList, $outFile, $log, $maxTries) {
  for ($t=1; $t -le $maxTries; $t++) {
    if (PastDeadline) { Log "$label - deadline"; return $false }
    KeepAwake; Log "$label (try $t/$maxTries)"
    & $PY @argList *>> $log
    if (Test-Path $outFile) { Log "$label OK"; return $true }
    Log "$label FAILED try $t"; Start-Sleep -Seconds 10
  }
  return $false
}

# single-instance lock
if (Test-Path $LOCK) {
  $op = (Get-Content $LOCK -EA SilentlyContinue | Select-Object -First 1)
  if ($op -and (Get-Process -Id ([int]$op) -EA SilentlyContinue)) { Log "another instance alive (PID $op) - exit"; return }
}
$PID | Set-Content $LOCK -Encoding ascii
if (-not (Test-Path -LiteralPath $STARTUP)) {
  "powershell -ExecutionPolicy Bypass -WindowStyle Hidden -File `"$TOOLS\overnight_archetypes_resilient_2026-07-03.ps1`"" | Set-Content -LiteralPath $STARTUP -Encoding ascii
}
Log "=== LAUNCH archetypes; 20 workers; deadline $DEADLINE (PID $PID) ==="
KeepAwake

# ---------- Stage A: 12 archetypes x multiasset, 6 folds ----------
if (-not (Test-Path "$RUN\_A.done")) {
  $env:MEGA_OUTPUT_DIR = $ARCH; $env:MEGA_FOLDS = "6"
  HB "A_archetypes" "running"
  $ok = RunRetry "Stage A (12 archetypes x multiasset, 6 folds)" `
    @("$TOOLS\overnight_archetypes_20260703.py","--resume","$ARCH\ckpt.pkl","--checkpoint-every","40") `
    "$ARCH\MEGA_walk_forward_results.json" "$ARCH\sweep.log" 4
  if ($ok) { "done" | Set-Content "$RUN\_A.done"; HB "A" "done" }
} else { Log "Stage A done - skip" }

# ---------- Stage B: deep CPCV + PBO on archetype survivors ----------
if (-not (Test-Path "$RUN\_B.done") -and -not (PastDeadline)) {
  HB "B_heavy" "running"
  if (Test-Path "$ARCH\MEGA_walk_forward_results.json") {
    RunRetry "Stage B CPCV archetypes" @("$TOOLS\cpcv_archetypes_wrapper_20260703.py","--input","$ARCH\MEGA_walk_forward_results.json","--out-dir","$RUN\cpcv_archetypes","--n-groups","10","--test-groups","2") "$RUN\cpcv_archetypes\cpcv_results.json" "$RUN\cpcv_archetypes.log" 3 | Out-Null
    if (Test-Path "$RUN\cpcv_archetypes\cpcv_results.json") { Log "Stage B PBO"; & $PY "$TOOLS\probabilistic_pbo.py" --cpcv "$RUN\cpcv_archetypes\cpcv_results.json" --out-dir "$RUN\pbo_archetypes" --max-combinations 100000 *>> "$RUN\pbo_archetypes.log" }
  }
  "done" | Set-Content "$RUN\_B.done"; HB "B" "done"
}

# ---------- Close + RELEASE ----------
& $PY "$TOOLS\morning_close_archetypes_20260703.py" *>> "$RUN\close.log"
"ALL_DONE $(Get-Date -Format o)" | Set-Content "$RUN\_ALL_DONE.marker"
Log "=== BACKLOG EXHAUSTED $(Get-Date -Format HH:mm:ss). Releasing (A22/A24). ==="
HB "complete" "done_released"
if (Test-Path -LiteralPath $STARTUP) { [System.IO.File]::Delete($STARTUP) }
if (Test-Path $LOCK) { Remove-Item $LOCK -Force -EA SilentlyContinue }
ReleaseAwake
