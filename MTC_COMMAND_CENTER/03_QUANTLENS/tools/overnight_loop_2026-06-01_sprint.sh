#!/bin/bash
# overnight_loop_2026-06-01_sprint.sh
# 1-saat max-throughput sprint. 20 worker. OUTPUT_DIR patched (CLEAN repo).
# Deadline: 07:29 (NOW+1h cap).

cd "$(dirname "$0")"

export MEGA_WORKERS=20
export MEGA_OUTPUT_DIR="C:/LAB/Tradingview_LAB_CLEAN/MTC_COMMAND_CENTER/03_QUANTLENS/05_BACKTEST_RESULTS"

NOW=$(date +%s)
# 1h hard cap from launch
DEADLINE=$((NOW + 3600))

ITER=0
TOTAL_PASSES=0
TOTAL_CRASHES=0
EC=""

mkdir -p overnight_runs sprint_runs
LOOP_LOG="overnight_runs/sprint_loop_2026-06-01.log"
echo "[sprint] === LAUNCHED at $(date) | deadline=$(date -d @$DEADLINE 2>/dev/null) | workers=$MEGA_WORKERS ===" | tee -a "$LOOP_LOG"

HEARTBEAT="overnight_runs/_heartbeat_sprint.json"

write_heartbeat() {
  cat > "$HEARTBEAT" <<EOF
{
  "ts": "$(date -Iseconds)",
  "mode": "sprint_20w",
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
  LOG="sprint_runs/v2_iter_${ITER}_${ts}.log"
  echo "[sprint] === Iter $ITER start at $(date) ===" | tee -a "$LOOP_LOG"

  export MEGA_HEARTBEAT_PATH="$HEARTBEAT"
  export MEGA_HEARTBEAT_MODE="sprint_20w"
  export MEGA_HEARTBEAT_ITER="$ITER"
  export MEGA_HEARTBEAT_PASSES="$TOTAL_PASSES"
  export MEGA_HEARTBEAT_CRASHES="$TOTAL_CRASHES"
  export MEGA_HEARTBEAT_DEADLINE_TS="$DEADLINE"
  python overnight_v2_runner.py > "$LOG" 2>&1
  EC=$?

  echo "[sprint] Iter $ITER exit=$EC at $(date)" | tee -a "$LOOP_LOG"

  if [ $EC -ne 0 ]; then
    TOTAL_CRASHES=$((TOTAL_CRASHES + 1))
    echo "[sprint] CRASH (EC=$EC). tail:" | tee -a "$LOOP_LOG"
    tail -15 "$LOG" | tee -a "$LOOP_LOG"
    write_heartbeat
    sleep 5
    continue
  fi

  if grep -q "all jobs done" "$LOG"; then
    TOTAL_PASSES=$((TOTAL_PASSES + 1))
    if [ -f ../05_BACKTEST_RESULTS/MEGA_walk_forward_results.json ]; then
      cp ../05_BACKTEST_RESULTS/MEGA_walk_forward_results.json \
         sprint_runs/MEGA_results_iter_${ITER}_${ts}.json
    fi
    if [ -f ../05_BACKTEST_RESULTS/MEGA_walk_forward_report.md ]; then
      cp ../05_BACKTEST_RESULTS/MEGA_walk_forward_report.md \
         sprint_runs/MEGA_report_iter_${ITER}_${ts}.md
    fi
  fi
  echo "[sprint] passes=$TOTAL_PASSES crashes=$TOTAL_CRASHES" | tee -a "$LOOP_LOG"
  write_heartbeat
  sleep 2
done

echo "[sprint] === DEADLINE at $(date). passes=$TOTAL_PASSES crashes=$TOTAL_CRASHES ===" | tee -a "$LOOP_LOG"
write_heartbeat
