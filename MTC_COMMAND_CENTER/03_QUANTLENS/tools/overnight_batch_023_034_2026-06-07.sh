#!/bin/bash
# QuantLens overnight batch — STG023-034 signal families first sweep.
# 2026-06-07 -> 2026-06-08.
#
# New strategies in this run (never previously evaluated in MEGA):
#   QL_KELL_BATCH_v1, QL_MARTIN_AVWAP_v1, QL_SLINGSHOT_v1 (256 configs),
#   QL_CRABEL_RANGE_EXP_v1, QL_BIGBELUGA_RSI_v1, QL_LINDA_5SMA_v1
# Total GRIDS: 54 strategies, 2494 configs.
#
# Structure:
#   Phase 1 (MEGA iters)  — run until TARGET_CONFIGS reached or PHASE1_DEADLINE.
#   Phase 2 (validation)  — CPCV(n_groups=10) + PBO + eval artifacts + Gate2 +
#                           all-gate evidence + scorecard_v2.
#   Phase 3 (report)      — morning report.
#
# EST_CONFIGS_PER_ITER: ~420,000 (54 strategies × ~9 sym × 4 TF × 46 cfg × 5 folds).
# TARGET_CONFIGS: 3,000,000 → ~7-8 iters × ~32 min = ~4h MEGA compute.
# Validation pipeline: ~2.5-3h.
# Total wall clock: ~7-8h.

set -u
cd "$(dirname "$0")"

NIGHT_ID="2026-06-07"
MODE="batch023_034_${NIGHT_ID}"
EST_CONFIGS_PER_ITER=420000
TARGET_CONFIGS=3000000

export MEGA_WORKERS=18
export OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1

RUN_DIR="C:/LAB/Tradingview_LAB_CLEAN/MTC_COMMAND_CENTER/03_QUANTLENS/05_BACKTEST_RESULTS/batch023_034_${NIGHT_ID}"
export MEGA_OUTPUT_DIR="$RUN_DIR"
LOGDIR="overnight_runs"
mkdir -p "$LOGDIR" "$RUN_DIR"

LOG="${LOGDIR}/batch023_034_${NIGHT_ID}.log"
HB="${LOGDIR}/_heartbeat.json"
MEGA_JSON="${RUN_DIR}/MEGA_walk_forward_results.json"
ITER_DIR="${RUN_DIR}/iters"
mkdir -p "$ITER_DIR"

NOW=$(date +%s)
DEADLINE=$((NOW + 36000))        # 10h hard cap
PHASE1_DEADLINE=$((NOW + 18000)) # 5h for MEGA iters; rest for validation

ITER=0
TOTAL_PASSES=0
TOTAL_CRASHES=0
EC=""

hb() {
  EST_DONE=$((TOTAL_PASSES * EST_CONFIGS_PER_ITER))
  cat > "$HB" <<EOF
{
  "ts": "$(date -Iseconds)",
  "mode": "$MODE",
  "iter": $ITER,
  "passes": $TOTAL_PASSES,
  "crashes": $TOTAL_CRASHES,
  "estimated_param_evaluations": $EST_DONE,
  "target_param_evaluations": $TARGET_CONFIGS,
  "deadline_ts": $DEADLINE,
  "phase1_deadline_ts": $PHASE1_DEADLINE,
  "last_exit_code": ${EC:-null}
}
EOF
}

log() { echo "[batch023 $(date +%H:%M:%S)] $*" | tee -a "$LOG"; }
guard() { [ "$(date +%s)" -lt "$DEADLINE" ] || { log "DEADLINE reached before $1 - stopping"; hb; exit 0; } }

log "=== LAUNCH night=${NIGHT_ID} workers=${MEGA_WORKERS} target=${TARGET_CONFIGS} ==="
log "RUN_DIR=${RUN_DIR}"
hb

# =====================================================================
# PHASE 1 — MEGA sweep loop (strat_extra_batch_023_034.py)
# =====================================================================
log "=== PHASE 1: MEGA sweep iters ==="
while [ "$(date +%s)" -lt "$PHASE1_DEADLINE" ]; do
  EST_DONE=$((TOTAL_PASSES * EST_CONFIGS_PER_ITER))
  if [ "$EST_DONE" -ge "$TARGET_CONFIGS" ]; then
    log "TARGET_CONFIGS reached ($EST_DONE >= $TARGET_CONFIGS). Moving to Phase 2."
    break
  fi

  ITER=$((ITER + 1))
  ts=$(date +%Y%m%d_%H%M%S)
  ITER_LOG="${ITER_DIR}/iter_${ITER}_${ts}.log"
  log "--- Iter ${ITER} start (est_done=${EST_DONE}) ---"

  export MEGA_HEARTBEAT_PATH="$HB"
  export MEGA_HEARTBEAT_MODE="$MODE"
  export MEGA_HEARTBEAT_ITER="$ITER"
  export MEGA_HEARTBEAT_PASSES="$TOTAL_PASSES"
  export MEGA_HEARTBEAT_CRASHES="$TOTAL_CRASHES"
  export MEGA_HEARTBEAT_DEADLINE_TS="$DEADLINE"

  python strat_extra_batch_023_034.py > "$ITER_LOG" 2>&1
  EC=$?
  log "Iter ${ITER} exit=${EC}"

  if [ "$EC" -ne 0 ]; then
    TOTAL_CRASHES=$((TOTAL_CRASHES + 1))
    log "CRASH iter=${ITER}. tail:"; tail -15 "$ITER_LOG" | tee -a "$LOG"
    hb; sleep 15; continue
  fi

  if grep -q "all jobs done\|results written\|MEGA.*done" "$ITER_LOG" 2>/dev/null || [ -f "$MEGA_JSON" ]; then
    TOTAL_PASSES=$((TOTAL_PASSES + 1))
    # Save first iter canonical result; subsequent iters archive for confirmation
    cp "$MEGA_JSON" "${ITER_DIR}/MEGA_results_iter_${ITER}_${ts}.json" 2>/dev/null || true
    log "Iter ${ITER} PASS. passes=${TOTAL_PASSES} est_done=$((TOTAL_PASSES * EST_CONFIGS_PER_ITER))"
  else
    log "Iter ${ITER}: MEGA JSON missing or incomplete. Treating as crash."
    TOTAL_CRASHES=$((TOTAL_CRASHES + 1))
  fi
  hb; sleep 2
done

log "=== PHASE 1 DONE. passes=${TOTAL_PASSES} crashes=${TOTAL_CRASHES} est_done=$((TOTAL_PASSES * EST_CONFIGS_PER_ITER)) ==="

# Use final MEGA JSON for pipeline (deterministic — last iter = same as first)
if [ ! -f "$MEGA_JSON" ]; then
  log "FATAL: no MEGA_walk_forward_results.json after Phase 1. Aborting pipeline."
  hb; exit 1
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

# =====================================================================
# PHASE 2 — Validation pipeline
# =====================================================================
log "=== PHASE 2: Validation pipeline ==="

# --- 2a: Deep CPCV (n_groups=10, 45 splits) ---
guard "cpcv"
log "2a: CPCV n_groups=10"
python cpcv_validator.py \
  --input "$MEGA_JSON" \
  --out-dir "${RUN_DIR}/cpcv" \
  --n-groups 10 --test-groups 2 --v2 >> "$LOG" 2>&1
log "2a CPCV exit=$? cpcv_json=$([ -f ${RUN_DIR}/cpcv/cpcv_results.json ] && echo OK || echo MISSING)"

# --- 2b: PBO (capped at 100k — uncapped causes MemoryError on large sweeps) ---
guard "pbo"
log "2b: PBO max-combinations=100000"
python probabilistic_pbo.py \
  --cpcv "${RUN_DIR}/cpcv/cpcv_results.json" \
  --out-dir "${RUN_DIR}/pbo" \
  --max-combinations 100000 >> "$LOG" 2>&1
log "2b PBO exit=$?"

# --- 2c: Evaluation artifacts ---
guard "artifacts"
log "2c: eval artifacts"
python build_evaluation_artifact.py \
  --mega "$MEGA_JSON" \
  --cpcv "${RUN_DIR}/cpcv/cpcv_results.json" \
  --pbo  "${RUN_DIR}/pbo/pbo_results.json" \
  --out-dir "${RUN_DIR}/evaluation_artifacts" >> "$LOG" 2>&1
NART=$(ls "${RUN_DIR}/evaluation_artifacts"/*.eval.json 2>/dev/null | wc -l)
log "2c eval artifacts: ${NART}"

# --- 2d: Gate2 scorecards ---
guard "gate2"
log "2d: Gate2 scorecards"
python score_gate2.py \
  --in-dir  "${RUN_DIR}/evaluation_artifacts" \
  --out-dir "${RUN_DIR}/gate2_scorecards" >> "$LOG" 2>&1
NG2=$(ls "${RUN_DIR}/gate2_scorecards"/*.gate2.json 2>/dev/null | wc -l)
log "2d Gate2 scorecards: ${NG2}"

# --- 2e: All-gate evidence + scorecard_v2 ---
guard "allgate"
log "2e: all-gate evidence + scorecard_v2"
python build_all_gate_evidence.py \
  --eval-dir "${RUN_DIR}/evaluation_artifacts" \
  --mega "$MEGA_JSON" \
  --out-dir "${RUN_DIR}/all_gate" >> "$LOG" 2>&1
log "2e all-gate exit=$?"

# --- 2f: Alpha vs buy&hold ---
guard "alpha"
log "2f: alpha vs buy&hold"
MEGA_OUTPUT_DIR="$RUN_DIR" python alpha_vs_buyhold.py >> "$LOG" 2>&1
log "2f alpha exit=$?"

# =====================================================================
# PHASE 3 — Morning report
# =====================================================================
guard "report"
log "=== PHASE 3: Morning report ==="

python heavy_night_report.py \
  --run-dir "$RUN_DIR" \
  --night-id "$NIGHT_ID" \
  --out "${RUN_DIR}/MORNING_REPORT_batch023_034_${NIGHT_ID}.md" >> "$LOG" 2>&1
REPORT_OK=$([ -f "${RUN_DIR}/MORNING_REPORT_batch023_034_${NIGHT_ID}.md" ] && echo "OK" || echo "MISSING")
log "Phase 3 report: ${REPORT_OK}"

# Final heartbeat
cat > "$HB" <<EOF
{
  "ts": "$(date -Iseconds)",
  "mode": "$MODE",
  "iter": $ITER,
  "passes": $TOTAL_PASSES,
  "crashes": $TOTAL_CRASHES,
  "estimated_param_evaluations": $((TOTAL_PASSES * EST_CONFIGS_PER_ITER)),
  "target_param_evaluations": $TARGET_CONFIGS,
  "deadline_ts": $DEADLINE,
  "status": "complete",
  "run_dir": "${RUN_DIR}",
  "sweep_cells": "${SWEEP_CELLS}",
  "eval_artifacts": "${NART}",
  "gate2_scorecards": "${NG2}",
  "report": "${REPORT_OK}"
}
EOF

log "=== ALL DONE at $(date). est_param_eval=$((TOTAL_PASSES * EST_CONFIGS_PER_ITER)) ==="
