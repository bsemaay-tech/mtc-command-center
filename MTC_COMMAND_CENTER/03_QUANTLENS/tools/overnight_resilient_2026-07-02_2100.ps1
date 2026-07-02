# =====================================================================
# Resilient overnight 2026-07-02 21:00 -> 2026-07-03 08:30
# Fixes the 18:30 failure (orchestrator died mid-Stage-A and STAYED dead ~2h):
# every stage runs under a RETRY loop (checkpoint-resume makes retries cheap), plus an
# external /loop monitor relaunches this whole script if the process dies.
# 20 workers (cpu_count). Genuinely-new only (A22/A24). Promotes nothing.
#   Stage P  STG001/STG002 confirmation FIRST (GEN_TWOCANDLE_CONFIRM + GEN_EMA_PULLBACK_TUNED)
#   Stage 1  full 8-variant family x multiasset (checkpoint skips the 2 done in P)
#   Stage 2  v2 23-strategy sweep RESUME (18:30 run got ~2840/8211 -> finish it, genuinely-new)
#   Stage 3  deep CPCV + PBO on the NEW survivors (variants + v2)
# Then inline close + RELEASE (A22 — release only when backlog exhausted).
# =====================================================================
$ErrorActionPreference = "Continue"
$TOOLS   = "C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\03_QUANTLENS\tools"
$RESULTS = "C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\03_QUANTLENS\05_BACKTEST_RESULTS"
$RUN     = "$RESULTS\overnight_resilient_2026-07-02"
$VAR     = "$RUN\variants"
$V2      = "$RESULTS\overnight_full_2026-07-02\stageA_v2_multiasset"   # resume the 18:30 partial
$MANIFEST= "C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\03_QUANTLENS\data\native_multiasset_alpaca_2026-06-28\manifests\dataset_manifest.json"
$PY      = "C:\Python314\python.exe"
$DEADLINE= Get-Date "2026-07-03 08:30:00"
$HB      = "$TOOLS\overnight_runs\_heartbeat.json"
$LOG     = "$RUN\orchestrator.log"
$STARTUP = Join-Path ([Environment]::GetFolderPath("Startup")) "mcc_resilient_2100_resume.cmd"

New-Item -ItemType Directory -Force -Path $RUN, $VAR, "$TOOLS\overnight_runs" | Out-Null

$env:PYTHONUTF8 = "1"
$env:MEGA_BUNDLE_MANIFEST = $MANIFEST
$env:MEGA_WORKERS = "20"
$env:OMP_NUM_THREADS = "1"; $env:MKL_NUM_THREADS = "1"; $env:OPENBLAS_NUM_THREADS = "1"; $env:NUMEXPR_NUM_THREADS = "1"

Add-Type -Namespace Win32r -Name Power -MemberDefinition @'
[System.Runtime.InteropServices.DllImport("kernel32.dll")]
public static extern uint SetThreadExecutionState(uint esFlags);
'@
$ES_CONTINUOUS=[uint32]"0x80000000"; $ES_SYSTEM=[uint32]"0x00000001"; $ES_DISPLAY=[uint32]"0x00000002"
function KeepAwake { [Win32r.Power]::SetThreadExecutionState($ES_CONTINUOUS -bor $ES_SYSTEM -bor $ES_DISPLAY) | Out-Null }
function ReleaseAwake { [Win32r.Power]::SetThreadExecutionState($ES_CONTINUOUS) | Out-Null }
function Log($m) { "[resil $(Get-Date -Format HH:mm:ss)] $m" | Tee-Object -FilePath $LOG -Append }
function HB($s,$st) { (@{ ts=(Get-Date -Format o); night="2026-07-02-2100"; mode="resilient"; stage=$s; status=$st; deadline=$DEADLINE.ToString("o") } | ConvertTo-Json -Compress) | Set-Content $HB -Encoding utf8 }
function PastDeadline { return ((Get-Date) -ge $DEADLINE) }

function RunRetry($label, $argList, $outFile, $log, $maxTries) {
  for ($t=1; $t -le $maxTries; $t++) {
    if (PastDeadline) { Log "$label - deadline, stop"; return $false }
    KeepAwake; Log "$label (try $t/$maxTries)"
    & $PY @argList *>> $log
    if (Test-Path $outFile) { Log "$label OK"; return $true }
    Log "$label FAILED try $t (missing $outFile)"; Start-Sleep -Seconds 10
  }
  return $false
}

if (-not (Test-Path -LiteralPath $STARTUP)) {
  "powershell -ExecutionPolicy Bypass -WindowStyle Hidden -File `"$TOOLS\overnight_resilient_2026-07-02_2100.ps1`"" | Set-Content -LiteralPath $STARTUP -Encoding ascii
}
# Single-instance lock: prevents the watchdog (or a double launch) from running two
# orchestrators against the same checkpoint (which would corrupt it).
$LOCK = "$RUN\orchestrator.lock"
if (Test-Path $LOCK) {
  $oldpid = (Get-Content $LOCK -ErrorAction SilentlyContinue | Select-Object -First 1)
  if ($oldpid -and (Get-Process -Id ([int]$oldpid) -ErrorAction SilentlyContinue)) {
    Log "another orchestrator alive (PID $oldpid) - this instance exits"; return
  }
}
$PID | Set-Content $LOCK -Encoding ascii

Log "=== LAUNCH resilient 2100; 20 workers; deadline $DEADLINE (PID $PID) ==="
KeepAwake

# ---------- Stage P: STG001/STG002 confirmation FIRST ----------
if (-not (Test-Path "$RUN\_P.done")) {
  $env:MEGA_OUTPUT_DIR = $VAR
  HB "P_stg_confirm" "running"
  $ok = RunRetry "Stage P (STG001 two-candle + STG002 8ema confirm)" `
    @("$TOOLS\overnight_variants_multiasset_20260702.py","--strategy","GEN_TWOCANDLE_CONFIRM","--strategy","GEN_EMA_PULLBACK_TUNED","--resume","$VAR\ckpt.pkl","--checkpoint-every","30") `
    "$VAR\MEGA_walk_forward_results.json" "$VAR\sweep.log" 3
  if ($ok) { "done" | Set-Content "$RUN\_P.done"; HB "P" "done" }
} else { Log "Stage P done - skip" }

# ---------- Stage 1: full 8-variant family (checkpoint skips the 2 from P) ----------
if (-not (Test-Path "$RUN\_1.done")) {
  $env:MEGA_OUTPUT_DIR = $VAR
  HB "1_variants_all" "running"
  $ok = RunRetry "Stage 1 (all 8 variants x multiasset)" `
    @("$TOOLS\overnight_variants_multiasset_20260702.py","--resume","$VAR\ckpt.pkl","--checkpoint-every","40") `
    "$VAR\MEGA_walk_forward_results.json" "$VAR\sweep.log" 3
  if ($ok) { "done" | Set-Content "$RUN\_1.done"; HB "1" "done" }
} else { Log "Stage 1 done - skip" }

# ---------- Stage 2: finish the v2 23-strategy sweep (resume 18:30 partial) ----------
if (-not (Test-Path "$RUN\_2.done")) {
  $env:MEGA_OUTPUT_DIR = $V2
  HB "2_v2_resume" "running"
  $ok = RunRetry "Stage 2 (v2 23 x multiasset, resume)" `
    @("$TOOLS\overnight_v2_multiasset_20260702.py","--resume","$V2\ckpt.pkl","--checkpoint-every","40") `
    "$V2\MEGA_walk_forward_results.json" "$V2\sweep.log" 4
  if ($ok) { "done" | Set-Content "$RUN\_2.done"; HB "2" "done" }
} else { Log "Stage 2 done - skip" }

# ---------- Stage 3: deep CPCV + PBO on NEW survivors ----------
if (-not (Test-Path "$RUN\_3.done") -and -not (PastDeadline)) {
  HB "3_heavy" "running"
  if (Test-Path "$VAR\MEGA_walk_forward_results.json") {
    RunRetry "Stage 3a CPCV variants" @("$TOOLS\cpcv_turtle_wrapper_20260701.py","--input","$VAR\MEGA_walk_forward_results.json","--out-dir","$RUN\cpcv_variants","--n-groups","10","--test-groups","2") "$RUN\cpcv_variants\cpcv_results.json" "$RUN\cpcv_variants.log" 2 | Out-Null
    if (Test-Path "$RUN\cpcv_variants\cpcv_results.json") { & $PY "$TOOLS\probabilistic_pbo.py" --cpcv "$RUN\cpcv_variants\cpcv_results.json" --out-dir "$RUN\pbo_variants" --max-combinations 100000 *>> "$RUN\pbo_variants.log" }
  }
  if (Test-Path "$V2\MEGA_walk_forward_results.json") {
    RunRetry "Stage 3b CPCV v2" @("$TOOLS\cpcv_validator.py","--input","$V2\MEGA_walk_forward_results.json","--out-dir","$RUN\cpcv_v2","--n-groups","10","--test-groups","2","--v2") "$RUN\cpcv_v2\cpcv_results.json" "$RUN\cpcv_v2.log" 2 | Out-Null
    if (Test-Path "$RUN\cpcv_v2\cpcv_results.json") { & $PY "$TOOLS\probabilistic_pbo.py" --cpcv "$RUN\cpcv_v2\cpcv_results.json" --out-dir "$RUN\pbo_v2" --max-combinations 100000 *>> "$RUN\pbo_v2.log" }
  }
  "done" | Set-Content "$RUN\_3.done"; HB "3" "done"
}

# ---------- Close + RELEASE ----------
& $PY "$TOOLS\morning_close_resilient_20260702.py" *>> "$RUN\close.log"
"ALL_DONE $(Get-Date -Format o)" | Set-Content "$RUN\_ALL_DONE.marker"
Log "=== BACKLOG EXHAUSTED $(Get-Date -Format HH:mm:ss). Releasing (A22/A24). ==="
HB "complete" "done_released"
if (Test-Path -LiteralPath $STARTUP) { [System.IO.File]::Delete($STARTUP) }
if (Test-Path $LOCK) { Remove-Item $LOCK -Force -ErrorAction SilentlyContinue }
ReleaseAwake
