# WP-L Phase 2 Stage 2 — R4-5 execution wrapper (PREREGISTERED, one-use).
#
# Allocates the R45 evidence leaf through the accepted RP0 bootstrap, then runs
# R4_5_runner.py against the byte-exact extracted RP4-C3.py.
#
# There is NO C3 prerequisite here on purpose: R4-5 is a function-level D026
# Arm 1 falsification of ONE guard inside `restore_into`. It needs no accepted
# bundle, no bundle path, no manifest hash, no db hash, no invariants hash and
# no candidate release tree. C3 itself stays BLOCKED and unexecuted in this
# staging run (see PREREGISTRATION.md).
#
# No service, unit, credential, port, network, broker/exchange/order/TESTNET/
# mainnet or economic action.
#
# rc contract: 0 = both R4-5 arms produced their expected outcome,
#              1 = an arm contradicted it, 3 = could not evaluate.
set -Eeuo pipefail

# --- pinned constants -------------------------------------------------------
BASE_RUN='WPLP2-20260809T125940Z-8dc78f08'
REMOTE_BASE='/home/gatea/wpl_p2_staging_WPLP2-20260809T125940Z-8dc78f08'
EXTRACT_DIR='/home/gatea/wpl_p2_staging_WPLP2-20260809T125940Z-8dc78f08/kit/extracted'
RUNNER='/home/gatea/wpl_p2_staging_WPLP2-20260809T125940Z-8dc78f08/R4_5_runner.py'
RP4_PATH='/home/gatea/wpl_p2_staging_WPLP2-20260809T125940Z-8dc78f08/kit/extracted/RP4-C3.py'

RUNID='WPLP2-20260809T125940Z-8dc78f08-R45'
EV_STAGE_ID='r45'
EV_PARENT='/home/gatea/wpl_p2_staging_WPLP2-20260809T125940Z-8dc78f08/evidence'
EV_PARENT_OWNER='gatea:gatea'
EV_PARENT_MODE='0700'
EV_RUNKIT='/home/gatea/wpl_p2_staging_WPLP2-20260809T125940Z-8dc78f08/evidence/runkit'
EV_RUNKIT_OWNER='gatea:gatea'
EV_RUNKIT_MODE='0700'

RP0_LIB_SHA='4a404d7b90d83aef47b3593757f86e3699b3bc2dd772f51df63ead4f10d9ab48'
RP0_BOOTSTRAP_SHA='e7d748f6b41c6156de4d5c5e2d93c2b08729b1f85377b132660424024815bb33'
RP4_C3_SHA='0520cc901e56a66fe61e0df9edc0ed33fa4b05c09d62ba8f7471ef9ff688e4a5'
# The runner is transferred by transport op 03 and is the only executed artifact
# that is not a frozen proposal block, so its bytes are pinned here too. An
# existence test would have let a truncated or altered upload run.
R45_RUNNER_SHA='8519e2bfc9bf2105bbb8e8c33fa4f271aa8852c7d7b18ad10286e19deddf68d5'

r45w_stop() { printf 'R45W_STOP reason=%s\n' "$*" >&2; exit 3; }

require_file() {
    local path="$1" want="$2" out got
    # `-f` dereferences: refuse the link itself first, so the bytes verified and
    # the bytes read are the same object.
    [ ! -L "$path" ] || r45w_stop "file_is_symlink path=$path"
    [ -f "$path" ] || r45w_stop "file_missing path=$path"
    out="$(LC_ALL=C sha256sum -- "$path")" || r45w_stop "file_hash_failed path=$path"
    got="${out%% *}"
    printf 'R45W_file path=%s sha256=%s\n' "$path" "$got"
    [ "$got" = "$want" ] || r45w_stop "file_sha256_mismatch path=$path actual=$got expected=$want"
}

printf 'R45W_header base_run=%s runid=%s stage=%s\n' "$BASE_RUN" "$RUNID" "$EV_STAGE_ID"
require_file "$EXTRACT_DIR/RP0-LIB.sh"       "$RP0_LIB_SHA"
require_file "$EXTRACT_DIR/RP0-BOOTSTRAP.sh" "$RP0_BOOTSTRAP_SHA"
require_file "$RP4_PATH"                     "$RP4_C3_SHA"
require_file "$RUNNER"                       "$R45_RUNNER_SHA"

command -v python3 >/dev/null 2>&1 || r45w_stop "python3_not_found"

# shellcheck source=/dev/null
. "$EXTRACT_DIR/RP0-LIB.sh"

# One-use evidence allocation. Any failure burns this RUNID; there is no retry
# pool and no second RUNID preregistered for R4-5.
export RUNID EV_STAGE_ID EV_PARENT EV_PARENT_OWNER EV_PARENT_MODE \
       EV_RUNKIT EV_RUNKIT_OWNER EV_RUNKIT_MODE
# shellcheck source=/dev/null
. "$EXTRACT_DIR/RP0-BOOTSTRAP.sh"

printf 'R45W_evidence_open runid=%s stage=%s dir=%s leaf=%s\n' \
    "$RUNID" "$EV_STAGE_ID" "$EV_DIR" "$EV_LOG"
printf 'R45W_command python3 %s %s\n' "$RUNNER" "$RP4_PATH"
printf 'R45W_python_version %s\n' "$(python3 -V 2>&1 </dev/null)"

# stdin is CLOSED for every child. This wrapper is delivered on ssh stdin, so
# bash is still reading its own script text from that stream; a child that read
# stdin would swallow the rest of the script. The runner does not read stdin,
# and with this redirection it structurally cannot.
RC=0
python3 "$RUNNER" "$RP4_PATH" </dev/null || RC=$?
printf 'R45W_runner_rc=%s\n' "$RC"
exit "$RC"
