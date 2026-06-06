#!/bin/bash
# Confirmation run — 2026-06-04 (Option B, pre-registered narrow grid).
# Single deterministic pipeline (NOT a loop — results are byte-identical per run).
# Resilient: retries the core run up to 3x, writes heartbeat + markers, and runs
# the full post-pipeline (multiwindow -> alpha -> A18-fixed morning report).
# Low workers (4) on purpose: user is asleep in the same room -> minimal fan.
set -u
cd "$(dirname "$0")"

NIGHT_ID="2026-06-04"
export MEGA_WORKERS=4
export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1

# Isolated output dir so the wide-run (2026-06-03) artifacts stay intact (A10).
CONFIRM_DIR="C:/LAB/Tradingview_LAB_CLEAN/MTC_COMMAND_CENTER/03_QUANTLENS/05_BACKTEST_RESULTS/confirm_${NIGHT_ID}"
export MEGA_OUTPUT_DIR="$CONFIRM_DIR"
mkdir -p "$CONFIRM_DIR"

RUNS_DIR="night_runs/confirm_${NIGHT_ID}"
mkdir -p overnight_runs "$RUNS_DIR"
LOG_DIR="$RUNS_DIR"
LOOP_LOG="overnight_runs/confirm_${NIGHT_ID}.log"
HEARTBEAT="overnight_runs/_heartbeat.json"
MORNING_REPORT="${CONFIRM_DIR}/MORNING_REPORT_confirm_${NIGHT_ID}.md"
DONE_MARKER="overnight_runs/confirm_${NIGHT_ID}.DONE"
FAIL_MARKER="overnight_runs/confirm_${NIGHT_ID}.FAILED"
RESULTS_JSON="${CONFIRM_DIR}/MEGA_walk_forward_results.json"

write_heartbeat() {
  cat > "$HEARTBEAT" <<EOF
{
  "ts": "$(date -Iseconds)",
  "mode": "confirm_${NIGHT_ID}",
  "stage": "$1",
  "attempt": ${2:-0},
  "status": "$3"
}
EOF
}

log() { echo "[confirm] $*" | tee -a "$LOOP_LOG"; }

rm -f "$DONE_MARKER" "$FAIL_MARKER"
log "=== LAUNCHED at $(date) | night_id=$NIGHT_ID | workers=$MEGA_WORKERS | out=$CONFIRM_DIR ==="
write_heartbeat "run" 0 "starting"

# ---- Core run (retry up to 3x). Doubles as the smoke gate: we hard-verify the
#      'all jobs done' marker AND a fresh results JSON before continuing.
OK=0
for ATTEMPT in 1 2 3; do
  ts=$(date +%Y%m%d_%H%M%S)
  RUN_LOG="${LOG_DIR}/confirm_run_attempt${ATTEMPT}_${ts}.log"
  log "--- run attempt $ATTEMPT at $(date) ---"
  write_heartbeat "run" "$ATTEMPT" "running"
  python confirmation_runner_2026-06-04.py > "$RUN_LOG" 2>&1
  EC=$?
  log "attempt $ATTEMPT exit=$EC"
  if [ "$EC" -eq 0 ] && grep -q "all jobs done" "$RUN_LOG" && [ -f "$RESULTS_JSON" ]; then
    log "run OK (exit 0 + 'all jobs done' + results JSON present)"
    cp "$RESULTS_JSON" "${RUNS_DIR}/MEGA_results_iter_1_${ts}.json"
    OK=1
    break
  fi
  log "attempt $ATTEMPT FAILED. tail:"; tail -15 "$RUN_LOG" | tee -a "$LOOP_LOG"
  sleep 10
done

if [ "$OK" -ne 1 ]; then
  log "=== CORE RUN FAILED after 3 attempts. Aborting post-pipeline. ==="
  write_heartbeat "run" 3 "failed"
  touch "$FAIL_MARKER"
  exit 1
fi

# ---- Post-pipeline (each step honors MEGA_OUTPUT_DIR=$CONFIRM_DIR) ----
log "=== POST: multiwindow_oos (regime + parameter stability) ==="
write_heartbeat "multiwindow" 0 "running"
python multiwindow_oos.py >> "$LOOP_LOG" 2>&1 || log "WARN multiwindow_oos nonzero exit"

log "=== POST: alpha_vs_buyhold ==="
write_heartbeat "alpha" 0 "running"
python alpha_vs_buyhold.py >> "$LOOP_LOG" 2>&1 || log "WARN alpha_vs_buyhold nonzero exit"

log "=== POST: morning report (A18-fixed) ==="
write_heartbeat "report" 0 "running"
python write_overnight_morning_report.py \
  --runs-dir "$RUNS_DIR" \
  --results-dir "$CONFIRM_DIR" \
  --night-id "confirm_${NIGHT_ID}" \
  --out "$MORNING_REPORT" >> "$LOOP_LOG" 2>&1 || log "WARN morning report nonzero exit"

log "=== DONE at $(date) ==="
log "report: $MORNING_REPORT"
write_heartbeat "done" 0 "complete"
touch "$DONE_MARKER"
