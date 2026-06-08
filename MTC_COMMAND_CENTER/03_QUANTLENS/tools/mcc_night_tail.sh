#!/bin/bash
# Reusable MCC validation + gating + visibility tail for a finished MEGA run dir.
# Incorporates this session's work: deeper-CPCV-safe PBO (A20), C1 Gate3 enrichment
# (honest, spec-derivable only), full gate scorecards, and D1 auto-visibility.
#
# Usage: mcc_night_tail.sh <RUN_DIR_ABS> [RUN_ID]
#   RUN_DIR must contain MEGA_walk_forward_results.json (from a sweep).
#
# Produces (in RUN_DIR): cpcv15/ pbo/ evaluation_artifacts/ gate2_scorecards/
#   all_gate/ all_gate_g3enriched/ gate3_scorecards/ scorecard_v2/ alpha_summary.json
#   HEAVY_TIER_MORNING_REPORT.md
# Then verifies the run is dashboard-visible (D1: backtest_reader scans run subdirs).
#
# No Pine/MTC/parity/live. No promotion. Gate3 honest: integration tiers stay N_A.
set -u
cd "$(dirname "$0")"
TOOLS="$(pwd)"
RUN_DIR="${1:?need RUN_DIR}"
RUN_ID="${2:-$(basename "$RUN_DIR")}"
MEGA="$RUN_DIR/MEGA_walk_forward_results.json"
RUNPY="python run_python_clean.py"
export OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
log() { echo "[tail $(date +%H:%M:%S)] $*"; }

[ -f "$MEGA" ] || { log "FATAL: no $MEGA"; exit 1; }
log "RUN_ID=$RUN_ID"

# 1. Standard CPCV (15-split, feeds PBO + eval — A20: never feed PBO from deep CPCV)
# Load strat_extra_runner (it imports v2 + the extra-runner families) so CPCV knows
# every strategy in the run — plain `--v2` only knows the 43 v2 strats and would
# return 0 trades (degenerate) for extra-runner strategies.
$RUNPY -c "
import sys, strat_extra_runner  # noqa: F401  (loads v2 + extra strategies)
sys.argv=['cpcv','--input',r'$MEGA','--out-dir',r'$RUN_DIR/cpcv15','--n-groups','6','--test-groups','2']
import cpcv_validator; cpcv_validator.main()
" >/dev/null 2>&1
log "cpcv15: $([ -f $RUN_DIR/cpcv15/cpcv_results.json ] && echo OK || echo MISSING)"

# 2. PBO (D008: never use --max-combinations 0)
$RUNPY probabilistic_pbo.py --cpcv "$RUN_DIR/cpcv15/cpcv_results.json" --out-dir "$RUN_DIR/pbo" --max-combinations 100000 >/dev/null 2>&1
log "pbo: $([ -f $RUN_DIR/pbo/pbo_results.json ] && echo OK || echo MISSING)"

# 3. Eval artifacts (+cpcv +pbo only if present)
EXTRA=""
[ -f "$RUN_DIR/cpcv15/cpcv_results.json" ] && EXTRA="$EXTRA --cpcv $RUN_DIR/cpcv15/cpcv_results.json"
[ -f "$RUN_DIR/pbo/pbo_results.json" ] && EXTRA="$EXTRA --pbo $RUN_DIR/pbo/pbo_results.json"
$RUNPY build_evaluation_artifact.py --mega "$MEGA" $EXTRA --out-dir "$RUN_DIR/evaluation_artifacts" >/dev/null 2>&1
NART=$(ls "$RUN_DIR/evaluation_artifacts"/*.eval.json 2>/dev/null | wc -l)
log "eval artifacts: $NART"

# 4. Gate2
$RUNPY score_gate2.py --in-dir "$RUN_DIR/evaluation_artifacts" --out-dir "$RUN_DIR/gate2_scorecards" >/dev/null 2>&1
log "gate2 scorecards: $(ls $RUN_DIR/gate2_scorecards/*.json 2>/dev/null | wc -l)"

# 5. All-gate evidence (emits Gate1/1B/3 sections)
$RUNPY build_all_gate_evidence.py --eval-dir "$RUN_DIR/evaluation_artifacts" --mega "$MEGA" --out-dir "$RUN_DIR/all_gate" >/dev/null 2>&1
log "all_gate: $(ls $RUN_DIR/all_gate/*.json 2>/dev/null | wc -l)"

# 6. C1 — honest Gate3 evidence enrichment (spec-derivable → OK; integration → N_A)
$RUNPY enrich_gate3_evidence.py --in-dir "$RUN_DIR/all_gate" --out-dir "$RUN_DIR/all_gate_g3enriched" --run-id "$RUN_ID" 2>&1 | tail -1
$RUNPY score_gate3.py --in-dir "$RUN_DIR/all_gate_g3enriched" --out-dir "$RUN_DIR/gate3_scorecards" >/dev/null 2>&1
log "gate3 scorecards: $(ls $RUN_DIR/gate3_scorecards/*.json 2>/dev/null | wc -l)"

# 7. Composed scorecard_v2 (from enriched all-gate → real Gate3 partial)
$RUNPY score_all_gates.py --in-dir "$RUN_DIR/all_gate_g3enriched" --out-dir "$RUN_DIR/scorecard_v2" 2>&1 | grep SUMMARY | tail -1

# 8. Alpha vs buy&hold (canonical)
MEGA_OUTPUT_DIR="$RUN_DIR" $RUNPY alpha_vs_buyhold.py >/dev/null 2>&1
log "alpha: $([ -f $RUN_DIR/alpha_summary.json ] && echo OK || echo MISSING)"

# 9. Morning report
$RUNPY heavy_night_report.py --run-dir "$RUN_DIR" --night-id "$RUN_ID" --out "$RUN_DIR/HEAVY_TIER_MORNING_REPORT.md" >/dev/null 2>&1
log "report: $([ -f $RUN_DIR/HEAVY_TIER_MORNING_REPORT.md ] && echo OK || echo MISSING)"

# 10. D1 dashboard visibility verify (backtest_reader auto-scans run subdirs)
# Derive MCC root (Windows-form) from RUN_DIR: .../MTC_COMMAND_CENTER/03_QUANTLENS/05_BACKTEST_RESULTS/<run>
API_REL="../../08_DASHBOARD_APP/apps/api"
PYTHONPATH="$TOOLS/$API_REL" $RUNPY -c "
from mcc_readonly.backtest_reader import build_backtest_status
from pathlib import Path
root=Path(r'$RUN_DIR').parents[2]   # MTC_COMMAND_CENTER
bs=build_backtest_status(root)
hit=[r for r in bs['runs'] if r['run_id']==r'$RUN_ID']
print('[tail] dashboard visible:', 'YES' if hit else 'NO', '| status', hit[0]['status'] if hit else '-')
" 2>&1 | tail -1

log "=== TAIL DONE for $RUN_ID ==="
