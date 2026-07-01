# =====================================================================
# Overnight orchestrator 2026-07-01 -> 2026-07-02 08:30
# GENUINELY-NEW compute only (A19/A22 compliant — NO deterministic re-run
# of the 2026-06-29 base sweep):
#   Stage 1  GEN_DONCHIAN_TURTLE full-universe walk-forward (new Faz-3 variant)
#   Stage 2  deep CPCV (n_groups=10) on the 2026-06-29 base BH-FDR survivors
#            (that run never got CPCV -> non-identical)
#   Stage 3  PBO on Stage-2 CPCV
#   Stage 4  deep CPCV on the TURTLE survivors (variant-patched)
#   Stage 5  PBO on Stage-4 CPCV
# Resilient: keep-awake, per-stage markers (reboot-resume skips done stages),
# mega --resume checkpoint, deadline guard. RELEASES the machine on completion
# (A22 — never hold an idle box awake). Promotes nothing.
# =====================================================================
$ErrorActionPreference = "Continue"

$TOOLS   = "C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\03_QUANTLENS\tools"
$RESULTS = "C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\03_QUANTLENS\05_BACKTEST_RESULTS"
$HEAVY   = "$RESULTS\turtle_heavy_2026-07-01"
$TURTLE  = "$HEAVY\turtle_sweep"
$SURV29  = "$RESULTS\overnight_multiasset_2026-06-29\MEGA_walk_forward_results.json"
$MANIFEST= "C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\03_QUANTLENS\data\native_multiasset_alpaca_2026-06-28\manifests\dataset_manifest.json"
$PY      = "C:\Python314\python.exe"
$DEADLINE= Get-Date "2026-07-02 08:30:00"
$HB      = "$TOOLS\overnight_runs\_heartbeat.json"
$LOG     = "$HEAVY\orchestrator.log"
$STARTUP = [Environment]::GetFolderPath("Startup") + "\mcc_overnight_turtle_resume.cmd"

New-Item -ItemType Directory -Force -Path $HEAVY, $TURTLE, "$TOOLS\overnight_runs" | Out-Null

# --- environment (thread-pinned; correct multi-asset data) ---
$env:PYTHONUTF8 = "1"
$env:MEGA_BUNDLE_MANIFEST = $MANIFEST
$env:MEGA_WORKERS = "16"
$env:OMP_NUM_THREADS = "1"; $env:MKL_NUM_THREADS = "1"
$env:OPENBLAS_NUM_THREADS = "1"; $env:NUMEXPR_NUM_THREADS = "1"

# --- keep-awake (no admin) ---
Add-Type -Namespace Win32 -Name Power -MemberDefinition @'
[System.Runtime.InteropServices.DllImport("kernel32.dll")]
public static extern uint SetThreadExecutionState(uint esFlags);
'@
$ES_CONTINUOUS = [uint32]"0x80000000"; $ES_SYSTEM = [uint32]"0x00000001"; $ES_DISPLAY = [uint32]"0x00000002"
function KeepAwake { [Win32.Power]::SetThreadExecutionState($ES_CONTINUOUS -bor $ES_SYSTEM -bor $ES_DISPLAY) | Out-Null }
function ReleaseAwake { [Win32.Power]::SetThreadExecutionState($ES_CONTINUOUS) | Out-Null }

function Log($m) { $line = "[orch $(Get-Date -Format HH:mm:ss)] $m"; $line | Tee-Object -FilePath $LOG -Append }
function HB($stage, $status) {
  $o = @{ ts = (Get-Date -Format o); night = "2026-07-01"; mode = "turtle_heavy"; stage = $stage; status = $status; deadline = ($DEADLINE.ToString("o")) }
  ($o | ConvertTo-Json -Compress) | Set-Content -Path $HB -Encoding utf8
}
function PastDeadline { return ((Get-Date) -ge $DEADLINE) }

# --- reboot-resume Startup hook (self-removed on completion) ---
if (-not (Test-Path $STARTUP)) {
  "powershell -ExecutionPolicy Bypass -WindowStyle Hidden -File `"$TOOLS\overnight_turtle_heavy_2026-07-01.ps1`"" | Set-Content -Path $STARTUP -Encoding ascii
}

Log "=== LAUNCH turtle_heavy; deadline $DEADLINE ==="
KeepAwake

# ---------- Stage 1: TURTLE full-universe sweep (NEW) ----------
if ((Test-Path "$HEAVY\_stage1.done")) { Log "Stage 1 already done (marker) - skip" }
elseif (PastDeadline) { Log "deadline before Stage 1 - abort"; HB "stage1" "deadline_abort" }
else {
  KeepAwake; HB "stage1_turtle_sweep" "running"; Log "Stage 1: TURTLE full-universe sweep -> $TURTLE"
  $env:MEGA_OUTPUT_DIR = $TURTLE
  & $PY "$TOOLS\overnight_turtle_sweep_20260701.py" --resume "$TURTLE\turtle_ckpt.pkl" --checkpoint-every 20 *>> "$TURTLE\sweep.log"
  if (Test-Path "$TURTLE\MEGA_walk_forward_results.json") { "done $(Get-Date -Format o)" | Set-Content "$HEAVY\_stage1.done"; Log "Stage 1 OK"; HB "stage1" "done" }
  else { Log "Stage 1 FAILED (no results json) - see $TURTLE\sweep.log"; HB "stage1" "failed" }
}

# ---------- Stage 2: deep CPCV on 2026-06-29 base survivors (NEW) ----------
if ((Test-Path "$HEAVY\_stage2.done")) { Log "Stage 2 already done - skip" }
elseif (PastDeadline) { Log "deadline before Stage 2 - stop"; HB "stage2" "deadline_stop" }
elseif (-not (Test-Path $SURV29)) { Log "Stage 2 SKIP - 06-29 results missing" }
else {
  KeepAwake; HB "stage2_cpcv_base" "running"; Log "Stage 2: deep CPCV (n_groups=10) on 06-29 survivors"
  & $PY "$TOOLS\cpcv_validator.py" --input "$SURV29" --out-dir "$HEAVY\cpcv_base" --n-groups 10 --test-groups 2 *>> "$HEAVY\cpcv_base.log"
  if (Test-Path "$HEAVY\cpcv_base\cpcv_results.json") { "done" | Set-Content "$HEAVY\_stage2.done"; Log "Stage 2 OK"; HB "stage2" "done" }
  else { Log "Stage 2 no cpcv json - see cpcv_base.log"; HB "stage2" "failed" }
}

# ---------- Stage 3: PBO on Stage-2 CPCV ----------
if ((Test-Path "$HEAVY\_stage3.done")) { Log "Stage 3 already done - skip" }
elseif (PastDeadline) { Log "deadline before Stage 3 - stop"; HB "stage3" "deadline_stop" }
elseif (-not (Test-Path "$HEAVY\cpcv_base\cpcv_results.json")) { Log "Stage 3 SKIP - no base CPCV" }
else {
  KeepAwake; HB "stage3_pbo_base" "running"; Log "Stage 3: PBO on base CPCV"
  & $PY "$TOOLS\probabilistic_pbo.py" --cpcv "$HEAVY\cpcv_base\cpcv_results.json" --out-dir "$HEAVY\pbo_base" --max-combinations 100000 *>> "$HEAVY\pbo_base.log"
  "done" | Set-Content "$HEAVY\_stage3.done"; Log "Stage 3 done (exit best-effort)"; HB "stage3" "done"
}

# ---------- Stage 4: deep CPCV on TURTLE survivors (variant-patched, NEW) ----------
if ((Test-Path "$HEAVY\_stage4.done")) { Log "Stage 4 already done - skip" }
elseif (PastDeadline) { Log "deadline before Stage 4 - stop"; HB "stage4" "deadline_stop" }
elseif (-not (Test-Path "$TURTLE\MEGA_walk_forward_results.json")) { Log "Stage 4 SKIP - no TURTLE results" }
else {
  KeepAwake; HB "stage4_cpcv_turtle" "running"; Log "Stage 4: deep CPCV on TURTLE survivors"
  & $PY "$TOOLS\cpcv_turtle_wrapper_20260701.py" --input "$TURTLE\MEGA_walk_forward_results.json" --out-dir "$HEAVY\cpcv_turtle" --n-groups 10 --test-groups 2 *>> "$HEAVY\cpcv_turtle.log"
  if (Test-Path "$HEAVY\cpcv_turtle\cpcv_results.json") { "done" | Set-Content "$HEAVY\_stage4.done"; Log "Stage 4 OK"; HB "stage4" "done" }
  else { Log "Stage 4 no cpcv json (TURTLE may have 0 PASS) - see cpcv_turtle.log"; "done" | Set-Content "$HEAVY\_stage4.done"; HB "stage4" "empty" }
}

# ---------- Stage 5: PBO on TURTLE CPCV ----------
if ((Test-Path "$HEAVY\_stage5.done")) { Log "Stage 5 already done - skip" }
elseif (PastDeadline) { Log "deadline before Stage 5 - stop"; HB "stage5" "deadline_stop" }
elseif (-not (Test-Path "$HEAVY\cpcv_turtle\cpcv_results.json")) { Log "Stage 5 SKIP - no TURTLE CPCV"; "skip" | Set-Content "$HEAVY\_stage5.done" }
else {
  KeepAwake; HB "stage5_pbo_turtle" "running"; Log "Stage 5: PBO on TURTLE CPCV"
  & $PY "$TOOLS\probabilistic_pbo.py" --cpcv "$HEAVY\cpcv_turtle\cpcv_results.json" --out-dir "$HEAVY\pbo_turtle" --max-combinations 100000 *>> "$HEAVY\pbo_turtle.log"
  "done" | Set-Content "$HEAVY\_stage5.done"; Log "Stage 5 done"; HB "stage5" "done"
}

# ---------- Completion: RELEASE the machine (A22) ----------
"ALL_DONE $(Get-Date -Format o)" | Set-Content "$HEAVY\_ALL_DONE.marker"
Log "=== ALL STAGES COMPLETE at $(Get-Date -Format HH:mm:ss) (deadline was $DEADLINE). Releasing keep-awake (A22: no idle-awake). ==="
HB "complete" "done_released"
if (Test-Path $STARTUP) { Remove-Item $STARTUP -Force -ErrorAction SilentlyContinue }
ReleaseAwake
