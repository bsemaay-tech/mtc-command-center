# WP-L Phase 2 Stage 2B - repaired B3 execution wrapper (PREREGISTERED).
# Read-only staging check. rc: 0 PASS, 1 FAIL, 3 STOP.
set -Eeuo pipefail

UNIT='WPLP2B-20260809T210610Z-834380c5'
BASE_RUN="$UNIT"
REMOTE_BASE="/home/gatea/wpl_p2b_staging_$UNIT"
EXTRACT_DIR="$REMOTE_BASE/kit/extracted"
RUNID="$UNIT-B3B"
EV_STAGE_ID='b3b'
EV_PARENT="$REMOTE_BASE/evidence"
EV_PARENT_OWNER='gatea:gatea'
EV_PARENT_MODE='0700'
EV_RUNKIT="$EV_PARENT/runkit"
EV_RUNKIT_OWNER='gatea:gatea'
EV_RUNKIT_MODE='0700'

B3_SWEEP_BUDGET_S='120'
B3_SVC_UID='999'
B3_SVC_GID='988'

RP0_LIB_SHA='4a404d7b90d83aef47b3593757f86e3699b3bc2dd772f51df63ead4f10d9ab48'
RP0_BOOTSTRAP_SHA='e7d748f6b41c6156de4d5c5e2d93c2b08729b1f85377b132660424024815bb33'
RP1_B3_SHA='6f3ea022b68d80a552c4ebcb771bbb2a707bdab46a383d605ffc5b88b884becc'

b3w_stop() { printf 'B3W_STOP reason=%s\n' "$*" >&2; exit 3; }

case "$UNIT$B3_SVC_UID$B3_SVC_GID" in
    *'<'*|*'>'*) b3w_stop 'dispatch_placeholders_unresolved' ;;
esac

require_block() {
    local path="$1" want="$2" out got
    [ ! -L "$path" ] || b3w_stop "block_is_symlink path=$path"
    [ -f "$path" ] || b3w_stop "block_missing path=$path"
    out="$(LC_ALL=C sha256sum -- "$path")" || b3w_stop "block_hash_failed path=$path"
    got="${out%% *}"
    printf 'B3W_block path=%s sha256=%s\n' "$path" "$got"
    [ "$got" = "$want" ] || b3w_stop "block_sha256_mismatch path=$path actual=$got expected=$want"
}

printf 'B3W_header base_run=%s runid=%s stage=%s\n' "$BASE_RUN" "$RUNID" "$EV_STAGE_ID"
require_block "$EXTRACT_DIR/RP0-LIB.sh" "$RP0_LIB_SHA"
require_block "$EXTRACT_DIR/RP0-BOOTSTRAP.sh" "$RP0_BOOTSTRAP_SHA"
require_block "$EXTRACT_DIR/RP1-B3.sh" "$RP1_B3_SHA"

. "$EXTRACT_DIR/RP0-LIB.sh"
export RUNID EV_STAGE_ID EV_PARENT EV_PARENT_OWNER EV_PARENT_MODE \
       EV_RUNKIT EV_RUNKIT_OWNER EV_RUNKIT_MODE
. "$EXTRACT_DIR/RP0-BOOTSTRAP.sh"

printf 'B3W_evidence_open runid=%s stage=%s dir=%s leaf=%s\n' "$RUNID" "$EV_STAGE_ID" "$EV_DIR" "$EV_LOG"
printf 'B3W_inputs sweep_budget_s=%s svc_uid=%s svc_gid=%s\n' \
    "$B3_SWEEP_BUDGET_S" "$B3_SVC_UID" "$B3_SVC_GID"

# These are exactly the three repaired RP1-B3 preregistered inputs.
export B3_SWEEP_BUDGET_S B3_SVC_UID B3_SVC_GID
. "$EXTRACT_DIR/RP1-B3.sh"
printf 'B3W done runid=%s\n' "$RUNID"
