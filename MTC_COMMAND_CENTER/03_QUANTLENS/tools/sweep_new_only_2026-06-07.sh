#!/bin/bash
# Targeted sweep: ONLY the 5 new strategies from strat_batch_remaining.py
# STG028/033/034/046/053 — 425 jobs (5 strat × 17 sym × 5 tf)
# Run via bash→powershell→python to satisfy D009 (scipy/bash-handle fix).
# 2026-06-07

set -u
cd "$(dirname "$0")"

RUN_DIR="C:/LAB/Tradingview_LAB_CLEAN/MTC_COMMAND_CENTER/03_QUANTLENS/05_BACKTEST_RESULTS/remaining_2026-06-07-remaining"
LOGDIR="overnight_runs"
mkdir -p "$LOGDIR" "$RUN_DIR"

LOG="${LOGDIR}/sweep_new_only_2026-06-07.log"
MEGA_JSON="${RUN_DIR}/MEGA_walk_forward_results.json"

log() { echo "[new-only $(date +%H:%M:%S)] $*" | tee -a "$LOG"; }

log "=== SWEEP new-only STG028/033/034/046/053 ==="
log "RUN_DIR=${RUN_DIR}"

if [ -f "$MEGA_JSON" ]; then
  log "MEGA_JSON already exists — skip sweep"
  exit 0
fi

# Kill lingering Python procs from previous sessions (D009 cleanup)
log "Killing old Python procs..."
powershell.exe -NoProfile -Command "
Get-Process python* -ErrorAction SilentlyContinue |
  Where-Object { \$_.StartTime -ne \$null -and \$_.StartTime.Date -lt (Get-Date).Date } |
  ForEach-Object { Write-Host \"Killing old PID \$(\$_.Id)\"; Stop-Process -Id \$_.Id -Force -ErrorAction SilentlyContinue }
" 2>/dev/null || true
log "Cleanup done."

log "Launching 5-strategy sweep via run_python_clean.py (D009 fix: strips MSYS2 PATH+vars)..."
MEGA_WORKERS=8 MEGA_OUTPUT_DIR="${RUN_DIR}" \
  python run_python_clean.py strat_batch_remaining.py \
    --strategy QL_CANSLIM_SHAKEOUT_v1 \
    --strategy QL_ANTI_CHASE_CRABEL_v1 \
    --strategy QL_EMA_RETEST_v1 \
    --strategy QL_VWAP_TREND_CONT_v1 \
    --strategy QL_HARRIS_50DMA_v1 > "${RUN_DIR}/sweep_new_only.log" 2>&1
EC=$?
log "Sweep exit=${EC}"

if [ "$EC" -ne 0 ] || [ ! -f "$MEGA_JSON" ]; then
  log "FATAL: sweep failed or MEGA JSON missing. tail:"
  tail -20 "${RUN_DIR}/sweep_new_only.log" | tee -a "$LOG"
  exit 1
fi

N=$(python -c "import json; d=json.load(open(r'${MEGA_JSON}')); print(len(d.get('results',[])))" 2>/dev/null)
log "Done. MEGA results: ${N}"
log "MEGA_JSON: ${MEGA_JSON}"
