#!/usr/bin/env bash
# WP-I P0 ssh-stdin wrapper (DRAFT - authoring only, not dispatchable).
#
# Stage 1 replaces every marked freeze placeholder, hashes these exact bytes,
# and records the resulting wrapper identity before any host contact. This file
# grants no host, RUNID, service, credential, broker, or trading authority.
#
# rc contract: 0 = PASS, 1 = FAIL (completed probe found deviant state),
#              3 = STOP (could not evaluate).
set -Eeuo pipefail
export LC_ALL=C

# --- allocation constants (filled only by the Lead at dispatch) ------------
BASE_RUN='<ALLOCATE-AT-DISPATCH>'
REMOTE_BASE='/home/gatea/wpi_staging_<ALLOCATE-AT-DISPATCH>'
EXTRACT_DIR='/home/gatea/wpi_staging_<ALLOCATE-AT-DISPATCH>/kit/extracted'
RUNID='<ALLOCATE-AT-DISPATCH>-P0'
EV_STAGE_ID='p0'
EV_PARENT='/home/gatea/wpi_staging_<ALLOCATE-AT-DISPATCH>/evidence'
EV_PARENT_OWNER='gatea:gatea'
EV_PARENT_MODE='0700'
EV_RUNKIT='/home/gatea/wpi_staging_<ALLOCATE-AT-DISPATCH>/evidence/runkit'
EV_RUNKIT_OWNER='gatea:gatea'
EV_RUNKIT_MODE='0700'

# --- block identities -------------------------------------------------------
RP0_LIB_SHA='4a404d7b90d83aef47b3593757f86e3699b3bc2dd772f51df63ead4f10d9ab48'
RP0_BOOTSTRAP_SHA='e7d748f6b41c6156de4d5c5e2d93c2b08729b1f85377b132660424024815bb33'
RP6_P0_SHA='<PIN-AT-FREEZE>'

# --- RP6 preregistered inputs ----------------------------------------------
P0_EXPECT_UID='<PIN-AT-FREEZE>'
P0_STATE_UID='999'
P0_STATE_GID='988'
P0_FORBIDDEN_GIDS='0 988'
P0_VENV_ROOT='/opt/mtc-bridge/venvs/2ce41e34bceb599d80af24c5c33d835820ec321b'
P0_TOOL_PINS='<PIN-AT-FREEZE>'

p0w_stop() { printf 'P0W_STOP reason=%s\n' "$*" >&2; exit 3; }

# Refuse a symlink before -f can dereference it. Capture the complete combined
# diagnostic, adjudicate rc and shape, and only then compare the digest.
require_block() {
    local path="$1" want="$2" out rc=0 got rest
    [ ! -L "$path" ] || p0w_stop "block_is_symlink path=$path"
    [ -f "$path" ] || p0w_stop "block_missing_or_not_regular path=$path"
    out="$(LC_ALL=C sha256sum -- "$path" </dev/null 2>&1)" || rc=$?
    [ "$rc" -eq 0 ] || p0w_stop "block_hash_failed path=$path rc=$rc"
    case "$out" in *$'\r'*|*$'\n'*) p0w_stop "block_hash_output_multiline path=$path" ;; esac
    got="${out%% *}"; rest="${out#*  }"
    [ "${#got}" -eq 64 ] || p0w_stop "block_hash_output_unparseable path=$path"
    case "$got" in *[!0-9a-f]*) p0w_stop "block_hash_output_unparseable path=$path" ;; esac
    [ "$rest" = "$path" ] || p0w_stop "block_hash_output_unparseable path=$path"
    printf 'P0W_block path=%s sha256=%s\n' "$path" "$got"
    [ "$got" = "$want" ] || p0w_stop "block_sha256_mismatch path=$path actual=$got expected=$want"
}

printf 'P0W_header base_run=%s runid=%s stage=%s\n' "$BASE_RUN" "$RUNID" "$EV_STAGE_ID"
require_block "$EXTRACT_DIR/RP0-LIB.sh" "$RP0_LIB_SHA"
require_block "$EXTRACT_DIR/RP0-BOOTSTRAP.sh" "$RP0_BOOTSTRAP_SHA"
require_block "$EXTRACT_DIR/RP6-P0.sh" "$RP6_P0_SHA"

# The wrapper itself is being read from ssh stdin. Every sourced child scope is
# therefore given /dev/null so no command can consume the remainder of it.
# shellcheck source=/dev/null
. "$EXTRACT_DIR/RP0-LIB.sh" </dev/null

export RUNID EV_STAGE_ID EV_PARENT EV_PARENT_OWNER EV_PARENT_MODE \
       EV_RUNKIT EV_RUNKIT_OWNER EV_RUNKIT_MODE
# shellcheck source=/dev/null
. "$EXTRACT_DIR/RP0-BOOTSTRAP.sh" </dev/null

printf 'P0W_evidence_open runid=%s stage=%s dir=%s leaf=%s\n' \
    "$RUNID" "$EV_STAGE_ID" "$EV_DIR" "$EV_LOG"

export P0_EXPECT_UID P0_STATE_UID P0_STATE_GID P0_FORBIDDEN_GIDS \
       P0_VENV_ROOT P0_TOOL_PINS
# shellcheck source=/dev/null
. "$EXTRACT_DIR/RP6-P0.sh" </dev/null

printf 'P0W done runid=%s\n' "$RUNID"
