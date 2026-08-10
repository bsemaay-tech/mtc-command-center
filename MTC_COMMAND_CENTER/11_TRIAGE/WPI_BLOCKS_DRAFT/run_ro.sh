#!/usr/bin/env bash
# WP-I RO ssh-stdin wrapper (DRAFT - authoring only, not dispatchable).
# Stage 1 fills every marked pin and hashes the resulting exact bytes.
set -Eeuo pipefail
export LC_ALL=C

# --- allocation constants --------------------------------------------------
BASE_RUN='<ALLOCATE-AT-DISPATCH>'
REMOTE_BASE='/home/gatea/wpi_staging_<ALLOCATE-AT-DISPATCH>'
EXTRACT_DIR='/home/gatea/wpi_staging_<ALLOCATE-AT-DISPATCH>/kit/extracted'
RUNID='<ALLOCATE-AT-DISPATCH>-RO'
EV_STAGE_ID='ro'
EV_PARENT='/home/gatea/wpi_staging_<ALLOCATE-AT-DISPATCH>/evidence'
EV_PARENT_OWNER='gatea:gatea'
EV_PARENT_MODE='0700'
EV_RUNKIT='/home/gatea/wpi_staging_<ALLOCATE-AT-DISPATCH>/evidence/runkit'
EV_RUNKIT_OWNER='gatea:gatea'
EV_RUNKIT_MODE='0700'

# --- block identities -------------------------------------------------------
RP0_LIB_SHA='4a404d7b90d83aef47b3593757f86e3699b3bc2dd772f51df63ead4f10d9ab48'
RP0_BOOTSTRAP_SHA='e7d748f6b41c6156de4d5c5e2d93c2b08729b1f85377b132660424024815bb33'
RP7_WPI_RO_SHA='<PIN-AT-FREEZE>'

# --- RP7 preregistered inputs ----------------------------------------------
WPI_CANDIDATE_SHA='2ce41e34bceb599d80af24c5c33d835820ec321b'
WPI_RELEASE_ROOT='/opt/mtc-bridge/releases/2ce41e34bceb599d80af24c5c33d835820ec321b'
WPI_VENV_ROOT='/opt/mtc-bridge/venvs/2ce41e34bceb599d80af24c5c33d835820ec321b'
WPI_UNIT_FRAGMENT='/usr/local/lib/systemd/system/mtc-bridge-first-start.service'
WPI_UNIT_FRAGMENT_BYTES='3736'
WPI_UNIT_FRAGMENT_SHA256='<PIN-AT-FREEZE>'
WPI_EXPECTED_LOCK_SHA256='a1881296c8cb6e0e9df33554aa2a25652cfeba2506530c74c7845ba2f58bf66e'
WPI_EXPECTED_LOCK_BYTES='117762'
WPI_EXPECTED_PACKAGES='56'
WPI_STATE_DIR='/var/lib/mtc-bridge'
WPI_STATE_UID='999'
WPI_STATE_GID='988'
WPI_LOG_DIR='/var/log/mtc-bridge'
WPI_CONF_DIR='/etc/mtc-bridge'
WPI_CONTROL_ENDPOINT='http://127.0.0.1:8790/api/status'
WPI_SWEEP_BUDGET_S='120'
WPI_TOOL_PINS='<PIN-AT-FREEZE>'
WPI_ATTESTED_MOUNTINFO_SHA256='<PIN-AT-FREEZE>'
WPI_MAINPID='189813'
WPI_INTERPRETER_TARGET='<PIN-AT-FREEZE>'
WPI_VERIFY_LOCK_SHA256='d951e0eea01ec1a89bcfbe9d9630949b31bb316faae2ba6bcae39be794a451e5'

row_stop() { printf 'ROW_STOP reason=%s\n' "$*" >&2; exit 3; }

# --- pinned program identities ----------------------------------------------
# No executable this wrapper runs is selected by the inherited PATH: the
# absolute path IS the pin. `stat` is the bootstrap root of trust and is the
# first object it verifies, including itself. Ownership is compared numerically
# (`%u:%g`); a resolver-rendered name is never an identity.
TOOL_STAT='/usr/bin/stat'
TOOL_SHA256SUM='/usr/bin/sha256sum'

require_tool() {
    local t="$1" own mode g o
    case "$t" in /*) : ;; *) row_stop "tool_path_not_absolute path=$t" ;; esac
    [ ! -L "$t" ] || row_stop "tool_is_symlink path=$t"
    [ -f "$t" ]   || row_stop "tool_missing_or_not_regular path=$t"
    [ -x "$t" ]   || row_stop "tool_not_executable path=$t"
    own="$(LC_ALL=C "$TOOL_STAT" -c '%u:%g' -- "$t" </dev/null 2>/dev/null)" \
        || row_stop "tool_owner_probe_failed path=$t"
    mode="$(LC_ALL=C "$TOOL_STAT" -c '%a' -- "$t" </dev/null 2>/dev/null)" \
        || row_stop "tool_mode_probe_failed path=$t"
    [ "$own" = '0:0' ] || row_stop "tool_owner_numeric=$own expected=0:0 path=$t"
    o="${mode#"${mode%?}"}"
    g="${mode%?}"; g="${g#"${g%?}"}"
    case "$o" in 2|3|6|7) row_stop "tool_other_writable mode=$mode path=$t" ;; esac
    case "$g" in 2|3|6|7) row_stop "tool_group_writable mode=$mode path=$t" ;; esac
    printf 'ROW_tool name=%s path=%s owner_numeric=%s mode=%s resolution=pinned_absolute\n' \
        "${t##*/}" "$t" "$own" "$mode"
}

require_tool "$TOOL_STAT"
require_tool "$TOOL_SHA256SUM"

require_block() {
    local path="$1" want="$2" out rc=0 got rest
    [ ! -L "$path" ] || row_stop "block_is_symlink path=$path"
    [ -f "$path" ] || row_stop "block_missing_or_not_regular path=$path"
    out="$(LC_ALL=C "$TOOL_SHA256SUM" -- "$path" </dev/null 2>&1)" || rc=$?
    [ "$rc" -eq 0 ] || row_stop "block_hash_failed path=$path rc=$rc"
    case "$out" in *$'\r'*|*$'\n'*) row_stop "block_hash_output_multiline path=$path" ;; esac
    got="${out%% *}"; rest="${out#*  }"
    [ "${#got}" -eq 64 ] || row_stop "block_hash_output_unparseable path=$path"
    case "$got" in *[!0-9a-f]*) row_stop "block_hash_output_unparseable path=$path" ;; esac
    [ "$rest" = "$path" ] || row_stop "block_hash_output_unparseable path=$path"
    printf 'ROW_block path=%s sha256=%s\n' "$path" "$got"
    [ "$got" = "$want" ] || row_stop "block_sha256_mismatch path=$path actual=$got expected=$want"
}

printf 'ROW_header base_run=%s runid=%s stage=%s\n' "$BASE_RUN" "$RUNID" "$EV_STAGE_ID"
require_block "$EXTRACT_DIR/RP0-LIB.sh" "$RP0_LIB_SHA"
require_block "$EXTRACT_DIR/RP0-BOOTSTRAP.sh" "$RP0_BOOTSTRAP_SHA"
require_block "$EXTRACT_DIR/RP7-WPI-RO.sh" "$RP7_WPI_RO_SHA"

# Every sourced scope inherits /dev/null as stdin. This is structural: a child
# cannot consume the ssh-stdin bytes from which this wrapper is still parsed.
# shellcheck source=/dev/null
. "$EXTRACT_DIR/RP0-LIB.sh" </dev/null

export RUNID EV_STAGE_ID EV_PARENT EV_PARENT_OWNER EV_PARENT_MODE \
       EV_RUNKIT EV_RUNKIT_OWNER EV_RUNKIT_MODE
# shellcheck source=/dev/null
. "$EXTRACT_DIR/RP0-BOOTSTRAP.sh" </dev/null

printf 'ROW_evidence_open runid=%s stage=%s dir=%s leaf=%s\n' \
    "$RUNID" "$EV_STAGE_ID" "$EV_DIR" "$EV_LOG"

export WPI_CANDIDATE_SHA WPI_RELEASE_ROOT WPI_VENV_ROOT WPI_UNIT_FRAGMENT \
       WPI_UNIT_FRAGMENT_BYTES WPI_UNIT_FRAGMENT_SHA256 \
       WPI_EXPECTED_LOCK_SHA256 WPI_EXPECTED_LOCK_BYTES WPI_EXPECTED_PACKAGES \
       WPI_STATE_DIR WPI_STATE_UID WPI_STATE_GID WPI_LOG_DIR WPI_CONF_DIR \
       WPI_CONTROL_ENDPOINT WPI_SWEEP_BUDGET_S WPI_TOOL_PINS \
       WPI_ATTESTED_MOUNTINFO_SHA256 WPI_MAINPID WPI_INTERPRETER_TARGET \
       WPI_VERIFY_LOCK_SHA256
# shellcheck source=/dev/null
. "$EXTRACT_DIR/RP7-WPI-RO.sh" </dev/null

printf 'ROW done runid=%s\n' "$RUNID"
