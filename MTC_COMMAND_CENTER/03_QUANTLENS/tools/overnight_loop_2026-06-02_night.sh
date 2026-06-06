#!/bin/bash
# overnight_loop_2026-06-02_night.sh
# Sabaha kadar QuantLens research sweep. 20 worker. ~172k config/iter.
# Target: >=1,000,000 param-evaluations overnight (~6+ iter). Deadline cap ~07:30.
# Proven recipe: 2026-06-01 night ran 13/13 iters, 0 crashes, identical runner.
# OUTPUT_DIR patched to CLEAN repo (A1 anti-pattern fix).

cd "$(dirname "$0")"

# Worker + output (runbook §5.1 sessiz oda gece = 20w)
export MEGA_WORKERS=20
export MEGA_OUTPUT_DIR="C:/LAB/Tradingview_LAB_CLEAN/MTC_COMMAND_CENTER/03_QUANTLENS/05_BACKTEST_RESULTS"

# Thread pinning (runbook §5.3) — BLAS thread'leri worker'larla çakışmasın
export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1

NOW=$(date +%s)
# ~11h hard cap from launch (~07:30 sabah)
DEADLINE=$((NOW + 39600))

ITER=0
TOTAL_PASSES=0
TOTAL_CRASHES=0
EC=""

mkdir -p overnight_runs night_runs
LOOP_LOG="overnight_runs/night_loop_2026-06-02.log"
echo "[night] === LAUNCHED at $(date) | deadline=$(date -d @$DEADLINE 2>/dev/null) | workers=$MEGA_WORKERS ===" | tee -a "$LOOP_LOG"

HEARTBEAT="overnight_runs/_heartbeat_tonight.json"

write_heartbeat() {
  cat > "$HEARTBEAT" <<EOF
{
  "ts": "$(date -Iseconds)",
  "mode": "night_20w_2026-06-02",
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
  LOG="night_runs/v2_iter_${ITER}_${ts}.log"
  echo "[night] === Iter $ITER start at $(date) ===" | tee -a "$LOOP_LOG"

  # intra-iter heartbeat env (mega print parse -> dakikalik hb, A4 fix)
  export MEGA_HEARTBEAT_PATH="$HEARTBEAT"
  export MEGA_HEARTBEAT_MODE="night_20w_2026-06-02"
  export MEGA_HEARTBEAT_ITER="$ITER"
  export MEGA_HEARTBEAT_PASSES="$TOTAL_PASSES"
  export MEGA_HEARTBEAT_CRASHES="$TOTAL_CRASHES"
  export MEGA_HEARTBEAT_DEADLINE_TS="$DEADLINE"

  python overnight_v2_runner.py > "$LOG" 2>&1
  EC=$?

  echo "[night] Iter $ITER exit=$EC at $(date)" | tee -a "$LOOP_LOG"

  if [ $EC -ne 0 ]; then
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
         night_runs/MEGA_results_iter_${ITER}_${ts}.json
    fi
    if [ -f ../05_BACKTEST_RESULTS/MEGA_walk_forward_report.md ]; then
      cp ../05_BACKTEST_RESULTS/MEGA_walk_forward_report.md \
         night_runs/MEGA_report_iter_${ITER}_${ts}.md
    fi
  fi
  echo "[night] passes=$TOTAL_PASSES crashes=$TOTAL_CRASHES" | tee -a "$LOOP_LOG"
  write_heartbeat
  sleep 2
done

echo "[night] === DEADLINE at $(date). passes=$TOTAL_PASSES crashes=$TOTAL_CRASHES ===" | tee -a "$LOOP_LOG"
write_heartbeat
