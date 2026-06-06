#!/bin/bash
# QuantLens overnight sweep for 2026-06-03 -> 2026-06-04.
# Target: >=3,000,000 parameter evaluations before morning.

set -u
cd "$(dirname "$0")"

NIGHT_ID="2026-06-03"
MODE="night_20w_${NIGHT_ID}"
EST_CONFIGS_PER_ITER=171785
TARGET_CONFIGS=3000000

export MEGA_WORKERS=20
export MEGA_OUTPUT_DIR="C:/LAB/Tradingview_LAB_CLEAN/MTC_COMMAND_CENTER/03_QUANTLENS/05_BACKTEST_RESULTS"
export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1

NOW=$(date +%s)
# 11h deadline cap: from 2026-06-03 evening into 2026-06-04 morning.
DEADLINE=$((NOW + 39600))

ITER=0
TOTAL_PASSES=0
TOTAL_CRASHES=0
EC=""

RUNS_DIR="night_runs/night_${NIGHT_ID}"
mkdir -p overnight_runs "$RUNS_DIR"
LOOP_LOG="overnight_runs/night_loop_${NIGHT_ID}.log"
HEARTBEAT_NIGHT="overnight_runs/_heartbeat_${NIGHT_ID}.json"
HEARTBEAT_CANON="overnight_runs/_heartbeat.json"
AGG_REPORT="${RUNS_DIR}/AGGREGATE_night_${NIGHT_ID}.md"
MORNING_REPORT="../05_BACKTEST_RESULTS/MORNING_REPORT_${NIGHT_ID}.md"

write_heartbeat() {
  EST_DONE=$((TOTAL_PASSES * EST_CONFIGS_PER_ITER))
  cat > "$HEARTBEAT_NIGHT" <<EOF
{
  "ts": "$(date -Iseconds)",
  "mode": "$MODE",
  "iter": $ITER,
  "passes": $TOTAL_PASSES,
  "crashes": $TOTAL_CRASHES,
  "estimated_param_evaluations": $EST_DONE,
  "target_param_evaluations": $TARGET_CONFIGS,
  "deadline_ts": $DEADLINE,
  "last_exit_code": ${EC:-null}
}
EOF
  cp "$HEARTBEAT_NIGHT" "$HEARTBEAT_CANON"
}

echo "[night] === LAUNCHED at $(date) | night_id=$NIGHT_ID | deadline=$(date -d @$DEADLINE 2>/dev/null) | workers=$MEGA_WORKERS | target=$TARGET_CONFIGS ===" | tee -a "$LOOP_LOG"
write_heartbeat

while [ "$(date +%s)" -lt "$DEADLINE" ]; do
  ITER=$((ITER + 1))
  ts=$(date +%Y%m%d_%H%M%S)
  LOG="${RUNS_DIR}/v2_iter_${ITER}_${ts}.log"
  echo "[night] === Iter $ITER start at $(date) ===" | tee -a "$LOOP_LOG"

  export MEGA_HEARTBEAT_PATH="$HEARTBEAT_CANON"
  export MEGA_HEARTBEAT_MODE="$MODE"
  export MEGA_HEARTBEAT_ITER="$ITER"
  export MEGA_HEARTBEAT_PASSES="$TOTAL_PASSES"
  export MEGA_HEARTBEAT_CRASHES="$TOTAL_CRASHES"
  export MEGA_HEARTBEAT_DEADLINE_TS="$DEADLINE"

  python overnight_v2_runner.py > "$LOG" 2>&1
  EC=$?
  echo "[night] Iter $ITER exit=$EC at $(date)" | tee -a "$LOOP_LOG"

  if [ "$EC" -ne 0 ]; then
    TOTAL_CRASHES=$((TOTAL_CRASHES + 1))
    echo "[night] CRASH (EC=$EC). tail:" | tee -a "$LOOP_LOG"
    tail -15 "$LOG" | tee -a "$LOOP_LOG"
    write_heartbeat
    sleep 10
    continue
  fi

  if grep -q "all jobs done" "$LOG"; then
    TOTAL_PASSES=$((TOTAL_PASSES + 1))
    if [ -f ../05_BACKTEST_RESULTS/MEGA_walk_forward_results.json ]; then
      cp ../05_BACKTEST_RESULTS/MEGA_walk_forward_results.json \
         "${RUNS_DIR}/MEGA_results_iter_${ITER}_${ts}.json"
    fi
    if [ -f ../05_BACKTEST_RESULTS/MEGA_walk_forward_report.md ]; then
      cp ../05_BACKTEST_RESULTS/MEGA_walk_forward_report.md \
         "${RUNS_DIR}/MEGA_report_iter_${ITER}_${ts}.md"
    fi
  fi
  EST_DONE=$((TOTAL_PASSES * EST_CONFIGS_PER_ITER))
  echo "[night] passes=$TOTAL_PASSES crashes=$TOTAL_CRASHES estimated_param_evaluations=$EST_DONE" | tee -a "$LOOP_LOG"
  write_heartbeat
  sleep 2
done

echo "[night] === DEADLINE at $(date). passes=$TOTAL_PASSES crashes=$TOTAL_CRASHES ===" | tee -a "$LOOP_LOG"
write_heartbeat

echo "[night] === POST: aggregate ===" | tee -a "$LOOP_LOG"
python aggregate_overnight_iters.py --runs-dir "$RUNS_DIR" --out "$AGG_REPORT" >> "$LOOP_LOG" 2>&1

echo "[night] === POST: alpha_vs_buyhold ===" | tee -a "$LOOP_LOG"
MEGA_OUTPUT_DIR="$MEGA_OUTPUT_DIR" python alpha_vs_buyhold.py >> "$LOOP_LOG" 2>&1

echo "[night] === POST: morning report ===" | tee -a "$LOOP_LOG"
python write_overnight_morning_report.py \
  --runs-dir "$RUNS_DIR" \
  --results-dir ../05_BACKTEST_RESULTS \
  --night-id "$NIGHT_ID" \
  --out "$MORNING_REPORT" >> "$LOOP_LOG" 2>&1

echo "[night] === POST DONE at $(date) ===" | tee -a "$LOOP_LOG"
write_heartbeat
