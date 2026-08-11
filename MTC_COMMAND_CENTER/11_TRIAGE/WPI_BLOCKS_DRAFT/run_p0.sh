#!/usr/bin/env bash
# WP-I P0 ssh-stdin wrapper (DRAFT - authoring only, not dispatchable).
#
# Stage 1 replaces every marked freeze placeholder, hashes these exact bytes,
# and records the resulting wrapper identity before any host contact. This file
# grants no host, RUNID, service, credential, broker, or trading authority.
#
# Transport op 04. Delivered on ssh stdin to the frozen remote launch domain,
# which `transport_runner.ps1` holds as a constant and every plan row must carry
# verbatim:
#   /usr/bin/env -i PATH=/usr/bin:/bin LC_ALL=C HOME=/home/gatea \
#     /usr/bin/bash --noprofile --norc -s --
#
# rc contract: 0 = PASS, 1 = FAIL (completed probe found deviant state),
#              3 = STOP (could not evaluate).
set -Eeuo pipefail

# --- class 5: launch-domain attestation --------------------------------------
# This block runs BEFORE the first external program, so a plant that replaced
# the interpreter or injected a startup file is refused rather than measured. A
# launch-domain violation is an inability to evaluate, never a host finding:
# every arm here is rc 3.
EXPECT_INTERPRETER='/usr/bin/bash'
EXPECT_LAUNCH_PATH='/usr/bin:/bin'
EXPECT_LAUNCH_LC_ALL='C'
EXPECT_LAUNCH_HOME='/home/gatea'
LD_ENVIRON='/proc/self/environ'

# The inherited-function sweep runs BEFORE this script defines a function of its
# own, so `declare -F` describes only what the launch domain delivered rather
# than this program's own names. `declare -F` exits 1 when there is nothing to
# list, which under `set -e` would end the run with no marker at all, so its
# status is consumed deliberately and the emptiness is tested afterwards.
LD_FUNCS="$(declare -F 2>/dev/null || :)"
if [ -n "$LD_FUNCS" ]; then
    printf 'P0W_STOP reason=launch_domain_inherited_shell_function detail=[%s]\n' "$LD_FUNCS" >&2
    exit 3
fi

# MEASURED SCOPE LIMIT (round 4, recorded rather than implied). `bash` reads
# `$BASH_ENV` before the first byte of a stdin-delivered script, and
# `--norc`/`--noprofile` do not disable that channel, so a startup plant that
# EXITS forges the record before anything here runs. No in-script attestation
# can close that. It is closed on the operator side, by the frozen `env -i`
# launch domain with an explicit complete variable list that
# `transport_runner.ps1` enforces verbatim on every plan row, so no plan row can
# introduce `BASH_ENV` at all - which is why the domain is stated on both sides.
# A plant that lets the script RUN, the only kind that could forge a
# real-looking record, is refused by the sweep below: `BASH_ENV` is still in the
# exec environment the kernel recorded. Both cases are executed in self-QA.
ld_stop() { printf 'P0W_STOP reason=%s\n' "$*" >&2; exit 3; }

[ "${BASH:-}" = "$EXPECT_INTERPRETER" ] \
    || ld_stop "launch_domain_interpreter=${BASH:-unset} expected=$EXPECT_INTERPRETER"
if shopt -q login_shell; then ld_stop "launch_domain_login_shell_startup_files_were_read"; fi

# The exec environment is read from the kernel's own copy rather than from the
# shell's exported-name list: `/proc/self/environ` is what `execve` received, so
# names the shell adds for its children (PWD, SHLVL, _) cannot mask an entry the
# launch domain actually delivered. Each expected entry is matched as a WHOLE
# `name=value` string and must appear exactly once; anything else - BASH_ENV,
# ENV, LD_PRELOAD, a BASH_FUNC_x%% exported function, an inherited TMPDIR - is a
# name this sweep does not recognise, and it STOPs naming the offender. The read
# is a redirection, not an external program. The wrapper's own later exports are
# not covered by this sweep and are not meant to be: it describes the domain the
# operator delivered, not the environment this wrapper deliberately constructs
# for the block it sources.
[ ! -L "$LD_ENVIRON" ] || ld_stop "launch_domain_environ_is_symlink path=$LD_ENVIRON"
[ -r "$LD_ENVIRON" ]   || ld_stop "launch_domain_environ_unreadable path=$LD_ENVIRON"
LD_SEEN_PATH=0; LD_SEEN_LC_ALL=0; LD_SEEN_HOME=0; LD_ENTRIES=0
LD_ENTRY=''
while IFS= read -r -d '' LD_ENTRY || [ -n "$LD_ENTRY" ]; do
    [ -n "$LD_ENTRY" ] || continue
    LD_ENTRIES=$((LD_ENTRIES + 1))
    case "$LD_ENTRY" in
        "PATH=$EXPECT_LAUNCH_PATH")     LD_SEEN_PATH=$((LD_SEEN_PATH + 1)) ;;
        "LC_ALL=$EXPECT_LAUNCH_LC_ALL") LD_SEEN_LC_ALL=$((LD_SEEN_LC_ALL + 1)) ;;
        "HOME=$EXPECT_LAUNCH_HOME")     LD_SEEN_HOME=$((LD_SEEN_HOME + 1)) ;;
        *) ld_stop "launch_domain_unexpected_environment_entry name=[${LD_ENTRY%%=*}]" ;;
    esac
    LD_ENTRY=''
done < "$LD_ENVIRON"
[ "$LD_ENTRIES" -eq 3 ]     || ld_stop "launch_domain_environment_size=$LD_ENTRIES expected=3"
[ "$LD_SEEN_PATH" -eq 1 ]   || ld_stop "launch_domain_path_entries=$LD_SEEN_PATH expected=1 value=$EXPECT_LAUNCH_PATH"
[ "$LD_SEEN_LC_ALL" -eq 1 ] || ld_stop "launch_domain_lc_all_entries=$LD_SEEN_LC_ALL expected=1 value=$EXPECT_LAUNCH_LC_ALL"
[ "$LD_SEEN_HOME" -eq 1 ]   || ld_stop "launch_domain_home_entries=$LD_SEEN_HOME expected=1 value=$EXPECT_LAUNCH_HOME"

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

# --- RP6 row-8 deploy-channel execution-domain attestation ------------------
# `RP6-P0.sh` requires all five of these before it observes anything about the
# login, and STOPs with `execution_domain_unattested ...
# detail=preregistered_value_missing` when the prelude supplies none of them.
# Round 3 defined and exported none, so the composition could not have reached a
# host observation even with every other pin filled (successor-skeleton review
# gap 1 / round-4 item T5). Grammars, enforced by the block itself:
#   *_NS            `<label>:[<digits>]` with label user|mnt|pid|net
#   ROOT_MOUNT_ID   `<dev>:<inode>`, digits and exactly one colon
# These are DEPLOY-CHANNEL values (owner grant #6): they are attested outside
# the login session being tested and are never learned from it. The block
# additionally requires each value to equal its own frozen
# `P0_FIXED_ATTESTED_*` literal, so filling one side only is a STOP, not a pass.
P0_ATTESTED_USER_NS='<PIN-AT-FREEZE>'
P0_ATTESTED_MNT_NS='<PIN-AT-FREEZE>'
P0_ATTESTED_PID_NS='<PIN-AT-FREEZE>'
P0_ATTESTED_NET_NS='<PIN-AT-FREEZE>'
P0_ATTESTED_ROOT_MOUNT_ID='<PIN-AT-FREEZE>'

p0w_stop() { printf 'P0W_STOP reason=%s\n' "$*" >&2; exit 3; }

# --- pinned program identities ----------------------------------------------
# No executable this wrapper runs is selected by the inherited PATH: the
# absolute path IS the pin. `stat` is the bootstrap root of trust and is the
# first object it verifies, including itself. Ownership is compared numerically
# (`%u:%g`); a resolver-rendered name is never an identity.
TOOL_STAT='/usr/bin/stat'
TOOL_SHA256SUM='/usr/bin/sha256sum'
# The launch domain's own two programs are admitted under the same rule, so the
# interpreter attested above is inside the pinned program domain rather than
# beside it (derivation class 5).
TOOL_ENV='/usr/bin/env'
TOOL_BASH='/usr/bin/bash'

require_tool() {
    local t="$1" own mode g o
    case "$t" in /*) : ;; *) p0w_stop "tool_path_not_absolute path=$t" ;; esac
    [ ! -L "$t" ] || p0w_stop "tool_is_symlink path=$t"
    [ -f "$t" ]   || p0w_stop "tool_missing_or_not_regular path=$t"
    [ -x "$t" ]   || p0w_stop "tool_not_executable path=$t"
    own="$(LC_ALL=C "$TOOL_STAT" -c '%u:%g' -- "$t" </dev/null 2>/dev/null)" \
        || p0w_stop "tool_owner_probe_failed path=$t"
    mode="$(LC_ALL=C "$TOOL_STAT" -c '%a' -- "$t" </dev/null 2>/dev/null)" \
        || p0w_stop "tool_mode_probe_failed path=$t"
    [ "$own" = '0:0' ] || p0w_stop "tool_owner_numeric=$own expected=0:0 path=$t"
    o="${mode#"${mode%?}"}"
    g="${mode%?}"; g="${g#"${g%?}"}"
    case "$o" in 2|3|6|7) p0w_stop "tool_other_writable mode=$mode path=$t" ;; esac
    case "$g" in 2|3|6|7) p0w_stop "tool_group_writable mode=$mode path=$t" ;; esac
    printf 'P0W_tool name=%s path=%s owner_numeric=%s mode=%s resolution=pinned_absolute\n' \
        "${t##*/}" "$t" "$own" "$mode"
}

require_tool "$TOOL_STAT"
require_tool "$TOOL_SHA256SUM"
require_tool "$TOOL_ENV"
require_tool "$TOOL_BASH"

# The attested interpreter must be the pinned OBJECT, not merely a path that
# spells the same characters.
[ "$BASH" = "$TOOL_BASH" ] || p0w_stop "launch_domain_interpreter_outside_pinned_set value=$BASH"
printf 'P0W_launch_domain interpreter=%s path=%s lc_all=%s home=%s exec_environment_entries=%s inherited_functions=0 bash_env=absent env=absent tmpdir=absent attestation=builtins_and_proc_self_environ\n' \
    "$BASH" "$PATH" "$EXPECT_LAUNCH_LC_ALL" "$HOME" "$LD_ENTRIES"

# Refuse a symlink before -f can dereference it. Capture the complete combined
# diagnostic, adjudicate rc and shape, and only then compare the digest.
require_block() {
    local path="$1" want="$2" out rc=0 got rest
    [ ! -L "$path" ] || p0w_stop "block_is_symlink path=$path"
    [ -f "$path" ] || p0w_stop "block_missing_or_not_regular path=$path"
    out="$(LC_ALL=C "$TOOL_SHA256SUM" -- "$path" </dev/null 2>&1)" || rc=$?
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
       P0_VENV_ROOT P0_TOOL_PINS \
       P0_ATTESTED_USER_NS P0_ATTESTED_MNT_NS P0_ATTESTED_PID_NS \
       P0_ATTESTED_NET_NS P0_ATTESTED_ROOT_MOUNT_ID
printf 'P0W_attested_inputs user_ns=%s mnt_ns=%s pid_ns=%s net_ns=%s root_mount_id=%s origin=deploy_channel_grant_6_never_learned_from_this_login\n' \
    "$P0_ATTESTED_USER_NS" "$P0_ATTESTED_MNT_NS" "$P0_ATTESTED_PID_NS" \
    "$P0_ATTESTED_NET_NS" "$P0_ATTESTED_ROOT_MOUNT_ID"
# shellcheck source=/dev/null
. "$EXTRACT_DIR/RP6-P0.sh" </dev/null

printf 'P0W done runid=%s\n' "$RUNID"
