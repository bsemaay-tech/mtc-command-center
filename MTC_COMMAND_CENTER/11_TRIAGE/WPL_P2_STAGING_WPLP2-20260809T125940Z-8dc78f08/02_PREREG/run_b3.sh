# WP-L Phase 2 Stage 2 — B3 execution wrapper (PREREGISTERED, one-use).
#
# B3 is the FIRST proposal check executed in this staging run. Nothing in the
# proposal set runs before it.
#
# Every value below is a pinned constant. Nothing is derived at run time,
# nothing is defaulted, nothing is read from the target host to decide what to
# assert. In particular B3_RELEASE_MANIFEST_SHA256 was derived LOCALLY in Stage
# 2 by running the candidate's own `IBKR_PAPER_BRIDGE/deploy/linux/package.sh`
# in a clean detached clone at the frozen candidate, and is NEVER read back out
# of the target's /etc/mtc-bridge/install_manifest.json — a manifest cannot
# attest to its own acceptance.
#
# This wrapper performs read-only `stat`/`find`/silent `grep` work only, via
# RP1-B3. No service is started, stopped, enabled, disabled or masked; no unit
# file is written; no network call is made; no credential value is read; no
# POST /api/arm; no broker/exchange/order/TESTNET/mainnet/economic action.
#
# rc contract: 0 = B3 PASS, 1 = B3 FAIL, 3 = STOP (could not evaluate).
set -Eeuo pipefail

# --- pinned constants -------------------------------------------------------
BASE_RUN='WPLP2-20260809T125940Z-8dc78f08'
REMOTE_BASE='/home/gatea/wpl_p2_staging_WPLP2-20260809T125940Z-8dc78f08'
EXTRACT_DIR='/home/gatea/wpl_p2_staging_WPLP2-20260809T125940Z-8dc78f08/kit/extracted'

RUNID='WPLP2-20260809T125940Z-8dc78f08-B3'
EV_STAGE_ID='b3'
EV_PARENT='/home/gatea/wpl_p2_staging_WPLP2-20260809T125940Z-8dc78f08/evidence'
EV_PARENT_OWNER='gatea:gatea'
EV_PARENT_MODE='0700'
EV_RUNKIT='/home/gatea/wpl_p2_staging_WPLP2-20260809T125940Z-8dc78f08/evidence/runkit'
EV_RUNKIT_OWNER='gatea:gatea'
EV_RUNKIT_MODE='0700'

B3_RELEASE_MANIFEST_SHA256='edb0fd34e3d976b872868cc3dfbf745cbc4b08f6c4c5d21b8d6cda47a3e20d26'
B3_SWEEP_BUDGET_S='120'

RP0_LIB_SHA='4a404d7b90d83aef47b3593757f86e3699b3bc2dd772f51df63ead4f10d9ab48'
RP0_BOOTSTRAP_SHA='e7d748f6b41c6156de4d5c5e2d93c2b08729b1f85377b132660424024815bb33'
RP1_B3_SHA='f40411b053779b28ec9d970d7e5610fe5f363acbc48ee487d07ebce2638a69af'

b3w_stop() { printf 'B3W_STOP reason=%s\n' "$*" >&2; exit 3; }

# --- re-verify the exact bytes about to be SOURCED --------------------------
# op 04 already verified them; this repeats the check immediately before
# sourcing so that "the bytes that ran" and "the bytes that were verified" are
# the same read, not two reads separated by an unobserved window.
require_block() {
    local path="$1" want="$2" out got
    [ -f "$path" ] || b3w_stop "block_missing path=$path"
    out="$(LC_ALL=C sha256sum -- "$path")" || b3w_stop "block_hash_failed path=$path"
    got="${out%% *}"
    printf 'B3W_block path=%s sha256=%s\n' "$path" "$got"
    [ "$got" = "$want" ] || b3w_stop "block_sha256_mismatch path=$path actual=$got expected=$want"
}

printf 'B3W_header base_run=%s runid=%s stage=%s\n' "$BASE_RUN" "$RUNID" "$EV_STAGE_ID"
require_block "$EXTRACT_DIR/RP0-LIB.sh"       "$RP0_LIB_SHA"
require_block "$EXTRACT_DIR/RP0-BOOTSTRAP.sh" "$RP0_BOOTSTRAP_SHA"
require_block "$EXTRACT_DIR/RP1-B3.sh"        "$RP1_B3_SHA"

# --- source the verified library --------------------------------------------
# shellcheck source=/dev/null
. "$EXTRACT_DIR/RP0-LIB.sh"

# --- one-use evidence allocation --------------------------------------------
# RP0-BOOTSTRAP allocates $EV_RUNKIT/$RUNID with a single plain `mkdir -m 0700`
# and opens $EV_DIR/b3.log with O_CREAT|O_EXCL. The RUNID is one-use: any
# failure burns it and there is no retry pool. From the `exec` inside
# RP0-BOOTSTRAP onward, all output lands in that evidence leaf.
export RUNID EV_STAGE_ID EV_PARENT EV_PARENT_OWNER EV_PARENT_MODE \
       EV_RUNKIT EV_RUNKIT_OWNER EV_RUNKIT_MODE
# shellcheck source=/dev/null
. "$EXTRACT_DIR/RP0-BOOTSTRAP.sh"

printf 'B3W_evidence_open runid=%s stage=%s dir=%s leaf=%s\n' \
    "$RUNID" "$EV_STAGE_ID" "$EV_DIR" "$EV_LOG"
printf 'B3W_inputs release_manifest_sha256=%s sweep_budget_s=%s\n' \
    "$B3_RELEASE_MANIFEST_SHA256" "$B3_SWEEP_BUDGET_S"

# --- run B3 ------------------------------------------------------------------
export B3_RELEASE_MANIFEST_SHA256 B3_SWEEP_BUDGET_S
# shellcheck source=/dev/null
. "$EXTRACT_DIR/RP1-B3.sh"

printf 'B3W done runid=%s\n' "$RUNID"
