#!/bin/bash
# Generic MCC overnight chain: smoke-gate -> sweep -> full gating/visibility tail -> release.
# Reusable operating flow (Codex item-5 / plan F3). Incorporates the season's discipline:
#   - determinism aware: a sweep runs ONCE (no loop-pad; repeat = zero info, A19).
#   - HARD smoke gate before the full sweep (runbook 2.4).
#   - deadline cap; RELEASE the machine when done (no idle keep-awake).
#   - tail = mcc_night_tail.sh (CPCV15+PBO+eval+Gate2+all-gate+C1 Gate3+scorecard_v2+
#     alpha+morning report+D1 dashboard verify).
#
# Usage:
#   night_runner.sh --runner <runner.py> --run-id <id> [--workers N] [--deadline-h H] \
#                   [-- <extra args passed to the runner, e.g. --strategy X --tf 4h>]
#
# Example (full 43-strategy enriched sweep):
#   night_runner.sh --runner overnight_v2_runner.py --run-id night_$(date +%F) --workers 18
# Example (single new strategy):
#   night_runner.sh --runner strat_extra_runner.py --run-id ok_$(date +%F) --workers 8 \
#       -- --strategy QL_OLIVER_KELL_PRICE_CYCLE --tf 4h --tf 1D
#
# No Pine/MTC/parity/live. No promotion. Gate3 honest (integration tiers N_A).
set -u
cd "$(dirname "$0")"
TOOLS="$(pwd)"

RUNNER=""; RUN_ID=""; WORKERS=8; DEADLINE_H=10
EXTRA=()
while [ $# -gt 0 ]; do
  case "$1" in
    --runner) RUNNER="$2"; shift 2;;
    --run-id) RUN_ID="$2"; shift 2;;
    --workers) WORKERS="$2"; shift 2;;
    --deadline-h) DEADLINE_H="$2"; shift 2;;
    --) shift; EXTRA=("$@"); break;;
    *) echo "unknown arg: $1"; exit 2;;
  esac
done
[ -n "$RUNNER" ] && [ -n "$RUN_ID" ] || { echo "need --runner and --run-id"; exit 2; }

RESULTS_ROOT="C:/LAB/Tradingview_LAB_CLEAN/MTC_COMMAND_CENTER/03_QUANTLENS/05_BACKTEST_RESULTS"
RUN_DIR="$RESULTS_ROOT/$RUN_ID"
LOGDIR="overnight_runs"; mkdir -p "$LOGDIR" "$RUN_DIR"
LOG="$LOGDIR/night_${RUN_ID}.log"
HB="$LOGDIR/_heartbeat.json"
export OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1

NOW=$(date +%s); DEADLINE=$((NOW + DEADLINE_H*3600))
log(){ echo "[night $(date +%H:%M:%S)] $*" | tee -a "$LOG"; }
hb(){ echo "{\"ts\":\"$(date -Iseconds)\",\"run\":\"$RUN_ID\",\"stage\":\"$1\",\"status\":\"$2\",\"deadline_ts\":$DEADLINE}" > "$HB"; }

log "=== LAUNCH runner=$RUNNER run_id=$RUN_ID workers=$WORKERS deadline=$(date -d @$DEADLINE 2>/dev/null) ==="
hb launch running

# 1. SMOKE GATE (HARD) — 2 cells into a throwaway dir
log "SMOKE gate"
hb smoke running
SMOKE=/c/tmp/smoke_$RUN_ID; rm -rf "$SMOKE"; mkdir -p "$SMOKE"
MEGA_WORKERS=2 MEGA_OUTPUT_DIR="$SMOKE" timeout 240 python "$RUNNER" "${EXTRA[@]}" --symbol BTCUSDT --symbol ETHUSDT --tf 4h >"$SMOKE/smoke.log" 2>&1
if ! grep -q "all jobs done" "$SMOKE/smoke.log" || [ ! -f "$SMOKE/MEGA_walk_forward_results.json" ]; then
  log "SMOKE FAIL — aborting. tail:"; tail -8 "$SMOKE/smoke.log" | tee -a "$LOG"; hb smoke failed; exit 1
fi
log "SMOKE PASS"

# 2. FULL SWEEP (once — determinism: no repeat)
[ "$(date +%s)" -lt "$DEADLINE" ] || { log "deadline before sweep"; hb sweep deadline_abort; exit 0; }
log "SWEEP -> $RUN_DIR"
hb sweep running
MEGA_WORKERS="$WORKERS" MEGA_OUTPUT_DIR="$RUN_DIR" python "$RUNNER" "${EXTRA[@]}" >"$RUN_DIR/sweep.log" 2>&1
EC=$?
if [ "$EC" -ne 0 ] || [ ! -f "$RUN_DIR/MEGA_walk_forward_results.json" ]; then
  log "SWEEP FAIL ec=$EC"; tail -12 "$RUN_DIR/sweep.log" | tee -a "$LOG"; hb sweep failed; exit 1
fi
CELLS=$(python -c "import json;print(len(json.load(open(r'$RUN_DIR/MEGA_walk_forward_results.json'))['results']))")
log "SWEEP OK: $CELLS cells"
hb sweep done

# 3. TAIL (gating + Gate3 + visibility)
log "TAIL"
hb tail running
bash mcc_night_tail.sh "$RUN_DIR" "$RUN_ID" 2>&1 | tee -a "$LOG"
hb tail done

# 4. RELEASE (no idle keep-awake — A19)
log "=== DONE $RUN_ID. Machine released (no idle-wait). ==="
hb complete done
