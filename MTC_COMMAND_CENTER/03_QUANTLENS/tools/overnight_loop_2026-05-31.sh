#!/bin/bash
# overnight_loop_2026-05-31.sh
# 2-worker overnight loop until 08:00 local (~8 hours from launch ~midnight).
# Auto-restarts after non-zero exit. Logs every iter under overnight_runs/.

cd "$(dirname "$0")"

# Workers locked to 2 (fan-friendly).
export MEGA_WORKERS=2

# Deadline: sabah 08:00. If launched after 08:00 same day, run for 8h max anyway.
NOW=$(date +%s)
TODAY_8AM=$(date -d "today 08:00" +%s 2>/dev/null || date -v8H -v0M -v0S +%s)
if [ $TODAY_8AM -le $NOW ]; then
  TOMORROW_8AM=$(date -d "tomorrow 08:00" +%s 2>/dev/null || date -v+1d -v8H -v0M -v0S +%s)
  DEADLINE=$TOMORROW_8AM
else
  DEADLINE=$TODAY_8AM
fi

# Cap at +8h regardless to avoid runaway.
MAX_DEADLINE=$((NOW + 28800))
if [ $DEADLINE -gt $MAX_DEADLINE ]; then
  DEADLINE=$MAX_DEADLINE
fi

ITER=0
TOTAL_PASSES=0
TOTAL_CRASHES=0

mkdir -p overnight_runs
LOOP_LOG="overnight_runs/loop_2026-05-31.log"
echo "[loop] === LAUNCHED at $(date) | deadline=$(date -d @$DEADLINE 2>/dev/null || date -r $DEADLINE) | workers=$MEGA_WORKERS ===" | tee -a "$LOOP_LOG"

# Heartbeat file for external monitor.
HEARTBEAT="overnight_runs/_heartbeat.json"

write_heartbeat() {
  cat > "$HEARTBEAT" <<EOF
{
  "ts": "$(date -Iseconds)",
  "iter": $ITER,
  "passes": $TOTAL_PASSES,
  "crashes": $TOTAL_CRASHES,
  "deadline_ts": $DEADLINE,
  "last_exit_code": ${EC:-null}
}
EOF
}

write_heartbeat

while [ $(date +%s) -lt $DEADLINE ]; do
  ITER=$((ITER+1))
  ts=$(date +%Y%m%d_%H%M%S)
  LOG="overnight_runs/v2_iter_${ITER}_${ts}.log"
  echo "[loop] === Iteration $ITER start at $(date) ===" | tee -a "$LOOP_LOG"

  export MEGA_HEARTBEAT_PATH="$HEARTBEAT"
  export MEGA_HEARTBEAT_MODE="overnight"
  export MEGA_HEARTBEAT_ITER="$ITER"
  export MEGA_HEARTBEAT_PASSES="$TOTAL_PASSES"
  export MEGA_HEARTBEAT_CRASHES="$TOTAL_CRASHES"
  export MEGA_HEARTBEAT_DEADLINE_TS="$DEADLINE"
  python overnight_v2_runner.py > "$LOG" 2>&1
  EC=$?

  echo "[loop] Iteration $ITER exit=$EC at $(date)" | tee -a "$LOOP_LOG"

  if [ $EC -ne 0 ]; then
    TOTAL_CRASHES=$((TOTAL_CRASHES + 1))
    echo "[loop] CRASH detected (EC=$EC). tail of log:" | tee -a "$LOOP_LOG"
    tail -20 "$LOG" | tee -a "$LOOP_LOG"
    echo "[loop] auto-restart in 10s..." | tee -a "$LOOP_LOG"
    write_heartbeat
    sleep 10
    continue
  fi

  if grep -q "all jobs done" "$LOG"; then
    TOTAL_PASSES=$((TOTAL_PASSES + 1))
    if [ -f ../05_BACKTEST_RESULTS/MEGA_walk_forward_results.json ]; then
      cp ../05_BACKTEST_RESULTS/MEGA_walk_forward_results.json \
         overnight_runs/MEGA_results_iter_${ITER}_${ts}.json
    fi
    if [ -f ../05_BACKTEST_RESULTS/MEGA_walk_forward_report.md ]; then
      cp ../05_BACKTEST_RESULTS/MEGA_walk_forward_report.md \
         overnight_runs/MEGA_report_iter_${ITER}_${ts}.md
    fi
  fi
  echo "[loop] Total passes: $TOTAL_PASSES | crashes: $TOTAL_CRASHES" | tee -a "$LOOP_LOG"
  write_heartbeat
  sleep 5
done

echo "[loop] === DEADLINE REACHED at $(date). passes=$TOTAL_PASSES crashes=$TOTAL_CRASHES ===" | tee -a "$LOOP_LOG"
write_heartbeat
