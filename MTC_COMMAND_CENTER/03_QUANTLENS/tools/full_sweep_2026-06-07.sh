#!/bin/bash
# QuantLens FULL sweep — all 59 strategies via strat_batch_remaining.py chain
# (includes overnight_v2_runner + strat_extra_batch_023_034 + strat_batch_remaining)
# 2026-06-07 (daytime run — full grid, all 59 strategies)
#
# 59 strategies via strat_batch_remaining.py chain (includes overnight_v2_runner +
# strat_extra_batch_023_034 + strat_batch_remaining)

set -u
cd "$(dirname "$0")"

NIGHT_ID="full-2026-06-07"
MODE="full"

export MEGA_WORKERS=18
export OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1

RUN_DIR="C:/LAB/Tradingview_LAB_CLEAN/MTC_COMMAND_CENTER/03_QUANTLENS/05_BACKTEST_RESULTS/full_sweep_2026-06-07"
export MEGA_OUTPUT_DIR="$RUN_DIR"
LOGDIR="overnight_runs"
mkdir -p "$LOGDIR" "$RUN_DIR"

LOG="${LOGDIR}/${NIGHT_ID}.log"
HB="${LOGDIR}/_heartbeat.json"

NOW=$(date +%s)
DEADLINE=$((NOW + 14400))   # 4h hard cap

log() { echo "[full $(date +%H:%M:%S)] $*" | tee -a "$LOG"; }
guard() { [ "$(date +%s)" -lt "$DEADLINE" ] || { log "DEADLINE reached — stopping"; exit 0; } }

log "=== LAUNCH full sweep all 59 strategies workers=${MEGA_WORKERS} ==="
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
# Phase 1 — single MEGA sweep (full grid, one pass is enough)
# D009: python from bash hangs on scipy. Run via PowerShell if MEGA JSON missing.
# ============================================================
MEGA_JSON="${RUN_DIR}/MEGA_walk_forward_results.json"
if [ -f "$MEGA_JSON" ]; then
  log "=== PHASE 1: MEGA JSON already exists — skipping sweep ==="
  EC=0
else
  log "=== PHASE 1: MEGA sweep (via run_python_clean.py — strips MSYS2 PATH/vars, D009 fix) ==="
  MEGA_WORKERS=18 MEGA_OUTPUT_DIR="${RUN_DIR}" python run_python_clean.py strat_batch_remaining.py > "${RUN_DIR}/sweep.log" 2>&1
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
# D009: cpcv_validator imports mega_walk_forward → scipy. Use run_python_clean.py wrapper.
guard "cpcv"
log "2a: CPCV n_groups=10"
python run_python_clean.py cpcv_validator.py \
  --input "${MEGA_JSON}" \
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
# D009: alpha_vs_buyhold imports mega_walk_forward → scipy. Use run_python_clean.py wrapper.
guard "alpha"
log "2f: alpha vs buy&hold"
MEGA_OUTPUT_DIR="${RUN_DIR}" python run_python_clean.py alpha_vs_buyhold.py >> "$LOG" 2>&1
log "2f alpha exit=$?"

# ============================================================
# Phase 3 — Report
# ============================================================
guard "report"
log "=== PHASE 3: Report ==="
python heavy_night_report.py \
  --run-dir "$RUN_DIR" \
  --night-id "$NIGHT_ID" \
  --out "${RUN_DIR}/REPORT_${NIGHT_ID}.md" >> "$LOG" 2>&1
REPORT_OK=$([ -f "${RUN_DIR}/REPORT_${NIGHT_ID}.md" ] && echo "OK" || echo "MISSING")
log "Phase 3 report: ${REPORT_OK}"

log "=== ALL DONE at $(date). cells=${SWEEP_CELLS} artifacts=${NART} gate2=${NG2} ==="
