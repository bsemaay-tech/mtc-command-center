#!/bin/bash
# Heavy-validation night 2026-06-05 -> 2026-06-06.
# Genuinely-NEW compute (no redundant deterministic repeats; A19/C4/C5):
#   1. First full 43-strategy sweep under TODAY's committed enriched engine
#      (today only 20 strategies were swept enriched; v2 adds 23 more).
#   2. 3x-deeper CPCV (n_groups=10 -> 45 splits vs committed 15).
#   3. Uncapped PBO.
#   4. Eval artifacts + Gate2 scorecards + all-gate evidence.
#   5. Alpha vs buy&hold + honest morning report.
# Determinism is real (seed=md5, mega:1130): run ONCE, do NOT loop-pad.
set -u
cd "$(dirname "$0")"

NIGHT_ID="2026-06-05"
RUN_DIR="C:/LAB/Tradingview_LAB_CLEAN/MTC_COMMAND_CENTER/03_QUANTLENS/05_BACKTEST_RESULTS/heavy_tier_${NIGHT_ID}"
LOGDIR="overnight_runs"
mkdir -p "$LOGDIR" "$RUN_DIR"
LOG="${LOGDIR}/heavy_night_${NIGHT_ID}.log"
HB="${LOGDIR}/_heartbeat.json"
MEGA_JSON="${RUN_DIR}/MEGA_walk_forward_results.json"

export OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
export MEGA_WORKERS=18
export MEGA_OUTPUT_DIR="$RUN_DIR"

# Deadline guard: do not run past ~07:00. 10h cap from launch.
NOW=$(date +%s)
DEADLINE=$((NOW + 36000))

hb() {  # hb <stage> <status>
  cat > "$HB" <<EOF
{"ts":"$(date -Iseconds)","night":"${NIGHT_ID}","mode":"heavy_validation_tier","stage":"$1","status":"$2","deadline_ts":${DEADLINE}}
EOF
}
log() { echo "[heavy $(date +%H:%M:%S)] $*" | tee -a "$LOG"; }
guard() { [ "$(date +%s)" -lt "$DEADLINE" ] || { log "DEADLINE reached before stage $1 - stopping"; hb "$1" "deadline_abort"; exit 0; } }

log "=== LAUNCH night=${NIGHT_ID} workers=${MEGA_WORKERS} deadline=$(date -d @$DEADLINE 2>/dev/null) ==="
hb "launch" "running"

# ----------------------------------------------------------------------
# STAGE 1 - full 43-strategy enriched sweep (genuinely new vs today's 20)
# ----------------------------------------------------------------------
guard "sweep"
log "STAGE 1: 43-strategy enriched sweep -> $RUN_DIR"
hb "sweep" "running"
python overnight_v2_runner.py >> "${RUN_DIR}/sweep.log" 2>&1
EC=$?
log "STAGE 1 exit=$EC"
if [ "$EC" -ne 0 ] || [ ! -f "$MEGA_JSON" ]; then
  log "FATAL: sweep failed or no MEGA json. tail:"; tail -20 "${RUN_DIR}/sweep.log" | tee -a "$LOG"
  hb "sweep" "failed"; exit 1
fi
SWEEP_CELLS=$(python -c "import json;print(len(json.load(open(r'${RUN_DIR}/MEGA_walk_forward_results.json'))['results']))")
log "STAGE 1 OK: $SWEEP_CELLS cells swept"
hb "sweep" "done"

# ----------------------------------------------------------------------
# STAGE 2 - 3x-deeper CPCV (45 splits) on all PASS/STRONG_PASS cells
# ----------------------------------------------------------------------
guard "cpcv"
log "STAGE 2: deeper CPCV (n_groups=10, 45 splits)"
hb "cpcv" "running"
python cpcv_validator.py --input "$MEGA_JSON" --out-dir "${RUN_DIR}/cpcv" \
  --n-groups 10 --test-groups 2 --v2 >> "$LOG" 2>&1
log "STAGE 2 exit=$? cpcv json: $([ -f ${RUN_DIR}/cpcv/cpcv_results.json ] && echo OK || echo MISSING)"
hb "cpcv" "done"

# ----------------------------------------------------------------------
# STAGE 3 - uncapped PBO
# ----------------------------------------------------------------------
guard "pbo"
log "STAGE 3: PBO (max-combinations=100000 — uncapped causes MemoryError on large sweeps)"
hb "pbo" "running"
python probabilistic_pbo.py --cpcv "${RUN_DIR}/cpcv/cpcv_results.json" \
  --out-dir "${RUN_DIR}/pbo" --max-combinations 100000 >> "$LOG" 2>&1
log "STAGE 3 exit=$? pbo json: $([ -f ${RUN_DIR}/pbo/pbo_results.json ] && echo OK || echo MISSING)"
hb "pbo" "done"

# ----------------------------------------------------------------------
# STAGE 4 - eval artifacts + Gate2 scorecards + all-gate evidence
# ----------------------------------------------------------------------
guard "artifacts"
log "STAGE 4: eval artifacts"
hb "artifacts" "running"
python build_evaluation_artifact.py --mega "$MEGA_JSON" \
  --cpcv "${RUN_DIR}/cpcv/cpcv_results.json" \
  --pbo "${RUN_DIR}/pbo/pbo_results.json" \
  --out-dir "${RUN_DIR}/evaluation_artifacts" >> "$LOG" 2>&1
NART=$(ls "${RUN_DIR}/evaluation_artifacts"/*.eval.json 2>/dev/null | wc -l)
log "STAGE 4a eval artifacts: $NART"
python score_gate2.py --in-dir "${RUN_DIR}/evaluation_artifacts" \
  --out-dir "${RUN_DIR}/gate2_scorecards" >> "$LOG" 2>&1
log "STAGE 4b gate2 exit=$?"
python build_all_gate_evidence.py --eval-dir "${RUN_DIR}/evaluation_artifacts" \
  --mega "$MEGA_JSON" --out-dir "${RUN_DIR}/all_gate" >> "$LOG" 2>&1
log "STAGE 4c all-gate exit=$?"
hb "artifacts" "done"

# ----------------------------------------------------------------------
# STAGE 5 - alpha vs buy&hold (canonical alpha_summary.json in RUN_DIR)
# ----------------------------------------------------------------------
guard "alpha"
log "STAGE 5: alpha vs buy&hold"
hb "alpha" "running"
MEGA_OUTPUT_DIR="$RUN_DIR" python alpha_vs_buyhold.py >> "$LOG" 2>&1
log "STAGE 5 exit=$? alpha json: $([ -f ${RUN_DIR}/alpha_summary.json ] && echo OK || echo MISSING)"
hb "alpha" "done"

# ----------------------------------------------------------------------
# STAGE 6 - honest heavy-tier morning summary (raw counts, no inflation)
# ----------------------------------------------------------------------
guard "report"
log "STAGE 6: morning summary"
hb "report" "running"
python heavy_night_report.py --run-dir "$RUN_DIR" --night-id "$NIGHT_ID" \
  --out "${RUN_DIR}/HEAVY_TIER_MORNING_REPORT.md" >> "$LOG" 2>&1
log "STAGE 6 exit=$? report: $([ -f ${RUN_DIR}/HEAVY_TIER_MORNING_REPORT.md ] && echo OK || echo MISSING)"
hb "report" "done"

log "=== ALL STAGES DONE at $(date) ==="
hb "complete" "done"
