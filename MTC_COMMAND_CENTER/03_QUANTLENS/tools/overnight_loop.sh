#!/bin/bash
# overnight_loop.sh — run overnight_v2_runner.py iteratively for ~8 hours
# Each iteration produces timestamped output; aggregate analysis tomorrow.

cd "$(dirname "$0")"
DEADLINE=$(( $(date +%s) + 27000 ))  # 7.5 hours from now
ITER=0
TOTAL_PASSES=0

mkdir -p overnight_runs

while [ $(date +%s) -lt $DEADLINE ]; do
  ITER=$((ITER+1))
  ts=$(date +%Y%m%d_%H%M%S)
  LOG="overnight_runs/v2_iter_${ITER}_${ts}.log"
  echo "[loop] === Iteration $ITER start at $(date) ===" | tee -a overnight_loop.log
  python overnight_v2_runner.py > "$LOG" 2>&1
  EC=$?
  echo "[loop] Iteration $ITER exit=$EC at $(date)" | tee -a overnight_loop.log
  if grep -q "DONE_MARKER" "$LOG"; then
    TOTAL_PASSES=$((TOTAL_PASSES + 1))
    # Preserve the timestamped output JSON/MD so successive runs don't overwrite
    if [ -f ../05_BACKTEST_RESULTS/MEGA_walk_forward_results.json ]; then
      cp ../05_BACKTEST_RESULTS/MEGA_walk_forward_results.json \
         overnight_runs/MEGA_results_iter_${ITER}_${ts}.json
    fi
    if [ -f ../05_BACKTEST_RESULTS/MEGA_walk_forward_report.md ]; then
      cp ../05_BACKTEST_RESULTS/MEGA_walk_forward_report.md \
         overnight_runs/MEGA_report_iter_${ITER}_${ts}.md
    fi
  fi
  echo "[loop] Total successful passes so far: $TOTAL_PASSES" | tee -a overnight_loop.log
  # Small gap between iterations to let OS clean up worker handles
  sleep 5
done

echo "[loop] === DEADLINE REACHED at $(date). Total passes: $TOTAL_PASSES ===" | tee -a overnight_loop.log
