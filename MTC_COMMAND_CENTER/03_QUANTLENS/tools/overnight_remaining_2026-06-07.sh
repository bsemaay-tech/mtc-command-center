#!/bin/bash
# QuantLens overnight batch — STG028/033/034/046/053 remaining CODEABLE sweep.
# 2026-06-07 (daytime run — small grid, ~46 configs × 17 sym × 5 TF × 5 folds)
#
# New strategies (5 families):
#   QL_CANSLIM_SHAKEOUT_v1   (STG028)  6 configs
#   QL_ANTI_CHASE_CRABEL_v1  (STG033) 12 configs
#   QL_EMA_RETEST_v1         (STG034)  4 configs
#   QL_VWAP_TREND_CONT_v1    (STG046) 18 configs
#   QL_HARRIS_50DMA_v1       (STG053)  6 configs
#
# Total: 46 configs × ~17 sym × 5 TF × 5 folds ≈ ~20,000 cell-evals.
# This is a small grid — one sweep + full validation pipeline is sufficient.
# No loop-padding needed.
#
# STG061/063 NOT included: specs state "thresholds unknown, formalize first".

set -u
cd "$(dirname "$0")"

NIGHT_ID="2026-06-07-remaining"
MODE="remaining_${NIGHT_ID}"

export MEGA_WORKERS=18
export OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1

RUN_DIR="C:/LAB/Tradingview_LAB_CLEAN/MTC_COMMAND_CENTER/03_QUANTLENS/05_BACKTEST_RESULTS/remaining_${NIGHT_ID}"
export MEGA_OUTPUT_DIR="$RUN_DIR"
LOGDIR="overnight_runs"
mkdir -p "$LOGDIR" "$RUN_DIR"

LOG="${LOGDIR}/remaining_${NIGHT_ID}.log"
HB="${LOGDIR}/_heartbeat.json"

NOW=$(date +%s)
DEADLINE=$((NOW + 14400))   # 4h hard cap

log() { echo "[remaining $(date +%H:%M:%S)] $*" | tee -a "$LOG"; }
guard() { [ "$(date +%s)" -lt "$DEADLINE" ] || { log "DEADLINE reached — stopping"; exit 0; } }

log "=== LAUNCH remaining STG028/033/034/046/053 workers=${MEGA_WORKERS} ==="
log "RUN_DIR=${RUN_DIR}"

# D009 fix: kill lingering Python processes from previous sessions before sweep.
# scipy.sparse/.stats hangs if old MEGA batch Python procs still alive (BLAS global state).
log "Killing any lingering Python procs from previous sessions..."
powershell.exe -NoProfile -Command "
Get-Process python* -ErrorAction SilentlyContinue |
  Where-Object { \$_.StartTime -ne \$null -and \$_.StartTime.Date -lt (Get-Date).Date } |
  ForEach-Object { Write-Host \"Killing old PID \$(\$_.Id) started \$(\$_.StartTime)\"; Stop-Process -Id \$_.Id -Force -ErrorAction SilentlyContinue }
" 2>/dev/null || true
log "Python proc cleanup done."

# ============================================================
# Phase 1 — single MEGA sweep (small grid, one pass is enough)
# D009: python from bash hangs on scipy. Run via PowerShell if MEGA JSON missing.
# ============================================================
MEGA_JSON="${RUN_DIR}/MEGA_walk_forward_results.json"
if [ -f "$MEGA_JSON" ]; then
  log "=== PHASE 1: MEGA JSON already exists — skipping sweep ==="
  EC=0
else
  log "=== PHASE 1: MEGA sweep (via PowerShell to avoid scipy/bash hang) ==="
  powershell.exe -NoProfile -Command "
    Set-Location 'C:/LAB/Tradingview_LAB_CLEAN/MTC_COMMAND_CENTER/03_QUANTLENS/tools'
    \$env:MEGA_WORKERS = '18'
    \$env:MEGA_OUTPUT_DIR = '${RUN_DIR}'
    \$env:OMP_NUM_THREADS = '1'; \$env:MKL_NUM_THREADS = '1'; \$env:OPENBLAS_NUM_THREADS = '1'
    python strat_batch_remaining.py
  " > "${RUN_DIR}/sweep.log" 2>&1
  EC=$?
  log "Phase 1 exit=${EC}"

  if [ "$EC" -ne 0 ] || [ ! -f "$MEGA_JSON" ]; then
    log "FATAL: sweep failed or no MEGA JSON. tail:"; tail -20 "${RUN_DIR}/sweep.log" | tee -a "$LOG"
    exit 1
  fi
fi

SWEEP_CELLS=$(python -c "
import json
try:
    d = json.load(open(r'${MEGA_JSON}'))
    print(len(d.get('results', [])))
except Exception as e:
    print(f'error:{e}')
" 2>/dev/null)
log "MEGA result cells: ${SWEEP_CELLS}"

# ============================================================
# Phase 2 — Validation pipeline
# ============================================================
log "=== PHASE 2: Validation ==="

# 2a: CPCV n_groups=10
guard "cpcv"
log "2a: CPCV n_groups=10"
python cpcv_validator.py \
  --input "$MEGA_JSON" \
  --out-dir "${RUN_DIR}/cpcv" \
  --n-groups 10 --test-groups 2 --v2 >> "$LOG" 2>&1
log "2a CPCV exit=$? json=$([ -f ${RUN_DIR}/cpcv/cpcv_results.json ] && echo OK || echo MISSING)"

# 2b: PBO capped (D008 fix — early-exit, never uncapped)
guard "pbo"
log "2b: PBO max-combinations=100000"
python probabilistic_pbo.py \
  --cpcv "${RUN_DIR}/cpcv/cpcv_results.json" \
  --out-dir "${RUN_DIR}/pbo" \
  --max-combinations 100000 >> "$LOG" 2>&1
log "2b PBO exit=$?"

# 2c: Evaluation artifacts
guard "artifacts"
log "2c: eval artifacts"
python build_evaluation_artifact.py \
  --mega "$MEGA_JSON" \
  --cpcv "${RUN_DIR}/cpcv/cpcv_results.json" \
  --pbo  "${RUN_DIR}/pbo/pbo_results.json" \
  --out-dir "${RUN_DIR}/evaluation_artifacts" >> "$LOG" 2>&1
NART=$(ls "${RUN_DIR}/evaluation_artifacts"/*.eval.json 2>/dev/null | wc -l)
log "2c eval artifacts: ${NART}"

# 2d: Gate2 scorecards
guard "gate2"
log "2d: Gate2 scorecards"
python score_gate2.py \
  --in-dir  "${RUN_DIR}/evaluation_artifacts" \
  --out-dir "${RUN_DIR}/gate2_scorecards" >> "$LOG" 2>&1
NG2=$(ls "${RUN_DIR}/gate2_scorecards"/*.gate2.json 2>/dev/null | wc -l || ls "${RUN_DIR}/gate2_scorecards"/*.scorecard.json 2>/dev/null | wc -l)
log "2d Gate2 scorecards: ${NG2}"

# 2e: All-gate evidence
guard "allgate"
log "2e: all-gate evidence"
python build_all_gate_evidence.py \
  --eval-dir "${RUN_DIR}/evaluation_artifacts" \
  --mega "$MEGA_JSON" \
  --out-dir "${RUN_DIR}/all_gate" >> "$LOG" 2>&1
log "2e all-gate exit=$?"

# 2f: Alpha vs buy&hold
guard "alpha"
log "2f: alpha vs buy&hold"
MEGA_OUTPUT_DIR="$RUN_DIR" python alpha_vs_buyhold.py >> "$LOG" 2>&1
log "2f alpha exit=$?"

# ============================================================
# Phase 3 — Report
# ============================================================
guard "report"
log "=== PHASE 3: Report ==="
python heavy_night_report.py \
  --run-dir "$RUN_DIR" \
  --night-id "$NIGHT_ID" \
  --out "${RUN_DIR}/REPORT_remaining_${NIGHT_ID}.md" >> "$LOG" 2>&1
REPORT_OK=$([ -f "${RUN_DIR}/REPORT_remaining_${NIGHT_ID}.md" ] && echo "OK" || echo "MISSING")
log "Phase 3 report: ${REPORT_OK}"

log "=== ALL DONE at $(date). cells=${SWEEP_CELLS} artifacts=${NART} gate2=${NG2} ==="
