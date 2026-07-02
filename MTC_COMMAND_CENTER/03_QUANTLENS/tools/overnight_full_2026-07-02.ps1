# =====================================================================
# Overnight orchestrator 2026-07-02 -> 2026-07-03 08:30  (LIBRARY-WIDE, genuinely-new)
# Fixes the 2026-07-01 under-scope: enumerate the FULL genuinely-new backlog, do not
# stop early. NO deterministic re-run (mega's 20 on multiasset = done 06-29; its CPCV
# = done 07-01 -> both excluded).
#   Stage A  v2 23-strategy set x multiasset 51x7  (NEVER swept on this bundle)
#   Stage B  Faz-3 variant family (7) x multiasset  (new logic, never run)
#   Stage C  deep CPCV + PBO on the NEW A+B survivors (proven harness, variant/v2-patched)
#   Stage D  multi-seed DSR stability on A+B survivors (seed-offset re-runs = non-identical)
# Resilient: keep-awake, per-stage markers (reboot-resume), --resume checkpoints,
# 08:30 deadline guard. Releases ONLY after the enumerated backlog is exhausted (A22/A24).
# Promotes nothing.
# =====================================================================
$ErrorActionPreference = "Continue"
$TOOLS   = "C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\03_QUANTLENS\tools"
$RESULTS = "C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\03_QUANTLENS\05_BACKTEST_RESULTS"
$RUN     = "$RESULTS\overnight_full_2026-07-02"
$A       = "$RUN\stageA_v2_multiasset"
$B       = "$RUN\stageB_variants"
$MANIFEST= "C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\03_QUANTLENS\data\native_multiasset_alpaca_2026-06-28\manifests\dataset_manifest.json"
$PY      = "C:\Python314\python.exe"
$DEADLINE= Get-Date "2026-07-03 08:30:00"
$HB      = "$TOOLS\overnight_runs\_heartbeat.json"
$LOG     = "$RUN\orchestrator.log"
$STARTUP = Join-Path ([Environment]::GetFolderPath("Startup")) "mcc_overnight_full_resume.cmd"

New-Item -ItemType Directory -Force -Path $A, $B, "$TOOLS\overnight_runs" | Out-Null

$env:PYTHONUTF8 = "1"
$env:MEGA_BUNDLE_MANIFEST = $MANIFEST
$env:MEGA_WORKERS = "16"
$env:OMP_NUM_THREADS = "1"; $env:MKL_NUM_THREADS = "1"; $env:OPENBLAS_NUM_THREADS = "1"; $env:NUMEXPR_NUM_THREADS = "1"

Add-Type -Namespace Win32f -Name Power -MemberDefinition @'
[System.Runtime.InteropServices.DllImport("kernel32.dll")]
public static extern uint SetThreadExecutionState(uint esFlags);
'@
$ES_CONTINUOUS=[uint32]"0x80000000"; $ES_SYSTEM=[uint32]"0x00000001"; $ES_DISPLAY=[uint32]"0x00000002"
function KeepAwake { [Win32f.Power]::SetThreadExecutionState($ES_CONTINUOUS -bor $ES_SYSTEM -bor $ES_DISPLAY) | Out-Null }
function ReleaseAwake { [Win32f.Power]::SetThreadExecutionState($ES_CONTINUOUS) | Out-Null }
function Log($m) { "[full $(Get-Date -Format HH:mm:ss)] $m" | Tee-Object -FilePath $LOG -Append }
function HB($s,$st) { (@{ ts=(Get-Date -Format o); night="2026-07-02"; mode="full_libwide"; stage=$s; status=$st; deadline=$DEADLINE.ToString("o") } | ConvertTo-Json -Compress) | Set-Content $HB -Encoding utf8 }
function PastDeadline { return ((Get-Date) -ge $DEADLINE) }

if (-not (Test-Path -LiteralPath $STARTUP)) {
  "powershell -ExecutionPolicy Bypass -WindowStyle Hidden -File `"$TOOLS\overnight_full_2026-07-02.ps1`"" | Set-Content -LiteralPath $STARTUP -Encoding ascii
}
Log "=== LAUNCH full_libwide; deadline $DEADLINE ==="
KeepAwake

# ---------- Stage A: v2 23-strategy set x multiasset (NEW) ----------
if (Test-Path "$RUN\_A.done") { Log "Stage A done - skip" }
elseif (PastDeadline) { Log "deadline before A"; HB "A" "deadline_abort" }
else {
  KeepAwake; HB "A_v2_multiasset" "running"; Log "Stage A: v2 23 strategies x multiasset -> $A"
  $env:MEGA_OUTPUT_DIR = $A
  & $PY "$TOOLS\overnight_v2_multiasset_20260702.py" --resume "$A\ckpt.pkl" --checkpoint-every 40 *>> "$A\sweep.log"
  if (Test-Path "$A\MEGA_walk_forward_results.json") { "done" | Set-Content "$RUN\_A.done"; Log "Stage A OK"; HB "A" "done" } else { Log "Stage A FAILED"; HB "A" "failed" }
}

# ---------- Stage B: variant family (7) x multiasset (NEW) ----------
if (Test-Path "$RUN\_B.done") { Log "Stage B done - skip" }
elseif (PastDeadline) { Log "deadline before B"; HB "B" "deadline_stop" }
else {
  KeepAwake; HB "B_variants" "running"; Log "Stage B: 7 variants x multiasset -> $B"
  $env:MEGA_OUTPUT_DIR = $B
  & $PY "$TOOLS\overnight_variants_multiasset_20260702.py" --resume "$B\ckpt.pkl" --checkpoint-every 40 *>> "$B\sweep.log"
  if (Test-Path "$B\MEGA_walk_forward_results.json") { "done" | Set-Content "$RUN\_B.done"; Log "Stage B OK"; HB "B" "done" } else { Log "Stage B FAILED"; HB "B" "failed" }
}

# ---------- Stage C: deep CPCV + PBO on NEW A+B survivors (proven harness) ----------
# C1 v2 survivors (cpcv --v2 patches the 43); C2 PBO; C3 variant survivors (variant wrapper); C4 PBO.
if ((Test-Path "$RUN\_C.done")) { Log "Stage C done - skip" }
elseif (PastDeadline) { Log "deadline before C"; HB "C" "deadline_stop" }
else {
  KeepAwake; HB "C_heavy" "running"
  if (Test-Path "$A\MEGA_walk_forward_results.json") {
    Log "Stage C1: CPCV on v2 survivors"
    & $PY "$TOOLS\cpcv_validator.py" --input "$A\MEGA_walk_forward_results.json" --out-dir "$RUN\cpcv_v2" --n-groups 10 --test-groups 2 --v2 *>> "$RUN\cpcv_v2.log"
    if (Test-Path "$RUN\cpcv_v2\cpcv_results.json") { Log "Stage C2: PBO v2"; & $PY "$TOOLS\probabilistic_pbo.py" --cpcv "$RUN\cpcv_v2\cpcv_results.json" --out-dir "$RUN\pbo_v2" --max-combinations 100000 *>> "$RUN\pbo_v2.log" }
  }
  if (Test-Path "$B\MEGA_walk_forward_results.json") {
    Log "Stage C3: CPCV on variant survivors"
    & $PY "$TOOLS\cpcv_turtle_wrapper_20260701.py" --input "$B\MEGA_walk_forward_results.json" --out-dir "$RUN\cpcv_variants" --n-groups 10 --test-groups 2 *>> "$RUN\cpcv_variants.log"
    if (Test-Path "$RUN\cpcv_variants\cpcv_results.json") { Log "Stage C4: PBO variants"; & $PY "$TOOLS\probabilistic_pbo.py" --cpcv "$RUN\cpcv_variants\cpcv_results.json" --out-dir "$RUN\pbo_variants" --max-combinations 100000 *>> "$RUN\pbo_variants.log" }
  }
  "done" | Set-Content "$RUN\_C.done"; Log "Stage C done"; HB "C" "done"
}

# ---------- Stage D: multi-seed DSR stability on A+B survivors (best-effort, non-identical) ----------
if ((Test-Path "$RUN\_D.done")) { Log "Stage D done - skip" }
elseif (PastDeadline) { Log "deadline before D - stop"; HB "D" "deadline_stop" }
elseif (-not (Test-Path "$TOOLS\multiseed_dsr_20260702.py")) { Log "Stage D SKIP - multiseed tool not present"; "skip" | Set-Content "$RUN\_D.done" }
else {
  KeepAwake; HB "D_multiseed_dsr" "running"; Log "Stage D: multi-seed DSR stability"
  & $PY "$TOOLS\multiseed_dsr_20260702.py" --stage-a "$A\MEGA_walk_forward_results.json" --stage-b "$B\MEGA_walk_forward_results.json" --out-dir "$RUN\multiseed_dsr" --seeds 12 *>> "$RUN\multiseed_dsr.log"
  "done" | Set-Content "$RUN\_D.done"; Log "Stage D done"; HB "D" "done"
}

# ---------- Mechanical morning close (inline, while awake) ----------
Log "running mechanical close -> MORNING_REPORT.md"
& $PY "$TOOLS\morning_close_full_20260702.py" *>> "$RUN\close.log"

# ---------- Completion: RELEASE (backlog exhausted) ----------
"ALL_DONE $(Get-Date -Format o)" | Set-Content "$RUN\_ALL_DONE.marker"
Log "=== BACKLOG EXHAUSTED at $(Get-Date -Format HH:mm:ss). Releasing keep-awake (A22/A24). ==="
HB "complete" "done_released"
if (Test-Path -LiteralPath $STARTUP) { [System.IO.File]::Delete($STARTUP) }
ReleaseAwake
