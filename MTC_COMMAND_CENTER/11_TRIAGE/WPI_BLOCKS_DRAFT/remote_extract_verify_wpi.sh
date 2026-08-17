# WP-I Stage 2 — runkit archive verification + extraction (PREREGISTERED).
#
# Transport op 03. Delivered on ssh stdin to the frozen remote launch domain,
# which `transport_runner.ps1` holds as a constant and every plan row must carry
# verbatim:
#   /usr/bin/env -i PATH=/usr/bin:/bin LC_ALL=C HOME=/home/gatea \
#     /usr/bin/bash --noprofile --norc -s -- \
#       <REMOTE_ARCHIVE> <EXTRACT_DIR> <EXPECTED_ARCHIVE_SHA256>
#
# It re-hashes the archive BEFORE reading its member list, refuses any member
# that is not one of the preregistered basenames, extracts into a fresh
# create-once directory, makes every extracted file read-only, and verifies the
# block hashes frozen in Stage 1.
#
# It NEVER executes a proposal block. Sourcing, running, `bash -n`-ing or
# `python3`-ing a block is out of scope here: this operation ends with the
# preregistered member set as verified read-only files on disk and nothing
# having been evaluated.
#
# Round 2 repairs (Codex F3/F6, Codex F7 / Claude F5):
#   * every executable is a verified absolute pin - nothing is selected by the
#     inherited PATH, and no `mktemp`/`TMPDIR` object is created at all;
#   * every listing/walk is adjudicated for rc, complete diagnostic stream, and
#     final-record termination BEFORE one byte of its stdout is parsed - the
#     sentinel byte appended inside the same command substitution is what keeps
#     the trailing-newline evidence alive (Patterns 6 and 7);
#   * the archive is re-hashed after the listings, so a listing cannot describe
#     different bytes from the ones that were hashed;
#   * NO member-count literal exists anywhere: the count is derived from the
#     MEMBERS constant, which is inside the permitted archive-constants block,
#     so there is no second constant that can drift out of step with it.
#
# Round 4 repair (Codex final audit F1, derivation class 5): the remote
# interpreter and its startup environment are now inside the pinned program
# domain rather than selected by the login shell's PATH, and this script attests
# that domain before its first external program.
#
# rc contract: 0 = PASS, 1 = FAIL (predicate refused), 3 = STOP (could not
# evaluate — never re-read as PASS).
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
# than this program's own names.
#
# CORRECTION, round 5 (Codex round-4 Band A, BA-2). An earlier comment here said
# that `declare -F` exits 1 when there is nothing to list and would therefore end
# the run under `set -e`. That is FALSE for the no-argument enumeration form used
# below, and it was never executed: in a function-free `--noprofile --norc` child
# on GNU Bash 5.3.9 the bare form returns 0 and the unguarded assignment under
# `set -Eeuo pipefail` runs straight through. Only a NAMED lookup of a missing
# function returns 1. The `2>/dev/null || :` is therefore explicit no-op
# hardening covering the named/errored forms, kept because it costs nothing - it
# is NOT a repair for an observed defect, and it does not weaken the sweep: an
# inherited exported function is listed identically with and without it. An
# overclaimed DEFECT is still a false evidence claim, so the claim is withdrawn
# rather than softened.
LD_FUNCS="$(declare -F 2>/dev/null || :)"
if [ -n "$LD_FUNCS" ]; then
    printf 'EXTRACT_STOP reason=launch_domain_inherited_shell_function detail=[%s]\n' "$LD_FUNCS" >&2
    exit 3
fi

# F1 IS OPEN - INNER CHILD CLOSED, OUTER SSH ACCOUNT-SHELL BOUNDARY OPEN
# (round 5; Codex round-4 Band B). `bash` reads `$BASH_ENV` before the first
# byte of a stdin-delivered script, and `--norc`/`--noprofile` do not disable
# that channel, so a startup plant that EXITS forges the record before anything
# here runs. Round 4 called that case unreachable, on the ground that the frozen
# `env -i` domain lists every variable the CHILD receives and no plan row can
# add `BASH_ENV`. THAT CLAIM IS WITHDRAWN. `sshd` does not execute the command
# string itself: it hands the string to the account's shell, and that shell
# processes its own startup environment BEFORE the string's first token,
# `/usr/bin/env`, ever runs. A server-supplied `BASH_ENV`/`ENV` therefore acts
# one interpreter EARLIER than the domain attested here; it can emit this
# program's record and exit with the delivered bytes never running at all, and
# no command inside the same shell string - here or in `transport_runner.ps1` -
# can act before it. What the frozen domain and the sweep below DO establish is
# narrower and still load-bearing: the inner `/usr/bin/bash` child's exec
# environment is exactly the three constructed entries, so the stealthier plant
# - the only kind that lets this script run and could forge a REAL-looking
# record - is refused by name, executed in self-QA. Closing the outer boundary
# needs an enforcement point that acts before account-shell startup processing
# (a deploy-channel-attested forced-command or execution contract, or a
# transport path with no unbound shell); that is a successor item, not a claim
# made here. A DISCLOSURE IS NOT A CONTROL.
ld_stop() { printf 'EXTRACT_STOP reason=%s\n' "$*" >&2; exit 3; }

[ "${BASH:-}" = "$EXPECT_INTERPRETER" ] \
    || ld_stop "launch_domain_interpreter=${BASH:-unset} expected=$EXPECT_INTERPRETER"
if shopt -q login_shell; then ld_stop "launch_domain_login_shell_startup_files_were_read"; fi

# The exec environment is read from the kernel's own copy rather than from the
# shell's exported-name list: `/proc/self/environ` is what `execve` received, so
# names the shell adds for its children (PWD, SHLVL, _) cannot mask an entry the
# launch domain actually delivered. Each expected entry is matched as a WHOLE
# `name=value` string and must appear exactly once; anything else — BASH_ENV,
# ENV, LD_PRELOAD, a BASH_FUNC_x%% exported function, an inherited TMPDIR — is a
# name this sweep does not recognise, and it STOPs naming the offender. The read
# is a redirection, not an external program.
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

fail() { printf 'EXTRACT_FAIL reason=%s\n' "$*" >&2; exit 1; }
stop() { printf 'EXTRACT_STOP reason=%s\n' "$*" >&2; exit 3; }
note() { printf 'EXTRACT_NOTE %s\n' "$*"; }

# --- pinned program identities ----------------------------------------------
TOOL_STAT='/usr/bin/stat'
TOOL_SHA256SUM='/usr/bin/sha256sum'
TOOL_TAR='/usr/bin/tar'
TOOL_MKDIR='/usr/bin/mkdir'
TOOL_READLINK='/usr/bin/readlink'
TOOL_FIND='/usr/bin/find'
TOOL_CHMOD='/usr/bin/chmod'
# The launch domain's own two programs are admitted under the same rule, so the
# interpreter this script attested above is inside the pinned program domain
# rather than beside it (derivation class 5).
TOOL_ENV='/usr/bin/env'
TOOL_BASH='/usr/bin/bash'

require_tool() {
    local t="$1" own mode g o
    case "$t" in /*) : ;; *) stop "tool_path_not_absolute path=$t" ;; esac
    [ ! -L "$t" ] || stop "tool_is_symlink path=$t"
    [ -f "$t" ]   || stop "tool_missing_or_not_regular path=$t"
    [ -x "$t" ]   || stop "tool_not_executable path=$t"
    own="$("$TOOL_STAT" -c '%u:%g' -- "$t" </dev/null 2>/dev/null)" || stop "tool_owner_probe_failed path=$t"
    mode="$("$TOOL_STAT" -c '%a' -- "$t" </dev/null 2>/dev/null)"   || stop "tool_mode_probe_failed path=$t"
    [ "$own" = '0:0' ] || stop "tool_owner_numeric=$own expected=0:0 path=$t"
    o="${mode#"${mode%?}"}"
    g="${mode%?}"; g="${g#"${g%?}"}"
    case "$o" in 2|3|6|7) stop "tool_other_writable mode=$mode path=$t" ;; esac
    case "$g" in 2|3|6|7) stop "tool_group_writable mode=$mode path=$t" ;; esac
    note "tool name=${t##*/} path=$t owner_numeric=$own mode=$mode resolution=pinned_absolute"
}

require_tool "$TOOL_STAT"
require_tool "$TOOL_SHA256SUM"
require_tool "$TOOL_TAR"
require_tool "$TOOL_MKDIR"
require_tool "$TOOL_READLINK"
require_tool "$TOOL_FIND"
require_tool "$TOOL_CHMOD"
require_tool "$TOOL_ENV"
require_tool "$TOOL_BASH"

# The attested interpreter must be the pinned OBJECT, not merely a path that
# spells the same characters: `$BASH` was compared as a string in the class 5
# block, and the pin admitted `/usr/bin/bash` as a non-symlink root-owned
# regular file here.
[ "$BASH" = "$TOOL_BASH" ] || stop "launch_domain_interpreter_outside_pinned_set value=$BASH"
note "launch_domain interpreter=$BASH path=$PATH lc_all=$EXPECT_LAUNCH_LC_ALL home=$HOME exec_environment_entries=$LD_ENTRIES inherited_functions=0 bash_env=absent env=absent tmpdir=absent attestation=builtins_and_proc_self_environ"

[ "$#" -eq 3 ] || fail "usage remote_extract_verify_wpi.sh <archive> <extract_dir> <archive_sha256> argc=$#"
ARCHIVE="$1"
EXTRACT_DIR="$2"
EXPECT_ARCHIVE_SHA="$3"

# --- WP-I STAGE 1 FREEZE CONSTANTS: replace placeholders, change no logic ---
EXPECT_ARCHIVE_BYTES='<PIN-AT-FREEZE>'
MEMBERS='RP0-LIB.sh
RP0-BOOTSTRAP.sh
RP6-P0.sh
RP7-WPI-RO.sh
run_p0.sh
run_ro.sh'
HASHES='<PIN-AT-FREEZE>  RP0-LIB.sh
<PIN-AT-FREEZE>  RP0-BOOTSTRAP.sh
<PIN-AT-FREEZE>  RP6-P0.sh
<PIN-AT-FREEZE>  RP7-WPI-RO.sh
<PIN-AT-FREEZE>  run_p0.sh
<PIN-AT-FREEZE>  run_ro.sh'

# Every count in this script is derived here, from the member list itself.
# There is no literal to keep in step with MEMBERS and therefore nothing that
# can drift when the member set changes.
count_records() {
    local body="$1" n=0 discard
    [ -n "$body" ] || { printf '0\n'; return 0; }
    while IFS= read -r discard; do n=$((n + 1)); done <<EOF
$body
EOF
    printf '%s\n' "$n"
}

MEMBER_COUNT="$(count_records "$MEMBERS")"
[ "$MEMBER_COUNT" -ge 1 ] || stop "member_constant_empty"
while IFS= read -r m; do
    case "$m" in
        ""|.|..)              stop "member_constant_reserved value=[$m]" ;;
        */*|-*)               stop "member_constant_not_basename value=[$m]" ;;
        *[!A-Za-z0-9._-]*)    stop "member_constant_charset value=[$m]" ;;
    esac
done <<EOF
$MEMBERS
EOF
note "member_constant count=$MEMBER_COUNT source=MEMBERS"

# --- adjudicate status, diagnostics and completion before any stdout --------
# CAPTURE_OUT is only assigned after: both passes agreed on rc, rc was 0, the
# complete diagnostic stream was empty, and the stream ended on a record
# boundary. The `S<rc>` sentinel is appended INSIDE the substitution so command
# substitution's trailing-newline stripping cannot destroy the evidence that
# decides the completion class.
CAPTURE_OUT=''
run_capture() {
    local label="$1" presence="$2"; shift 2
    local both out rc_both rc_out
    both="$( "$@" 2>&1; printf 'S%s' "$?" )"
    rc_both="${both##*S}"; both="${both%S$rc_both}"
    out="$( "$@" 2>/dev/null; printf 'S%s' "$?" )"
    rc_out="${out##*S}"; out="${out%S$rc_out}"
    [ "$rc_both" = "$rc_out" ] || stop "${label}_rc_unstable first=$rc_both second=$rc_out"
    [ "$rc_both" = "0" ]       || stop "${label}_failed rc=$rc_both detail=$both"
    [ "$both" = "$out" ]       || stop "${label}_diagnostics detail=$both"
    if [ -z "$out" ]; then
        [ "$presence" = "optional" ] || stop "${label}_empty"
        CAPTURE_OUT=''
        return 0
    fi
    case "$out" in
        *$'\n') : ;;
        *) stop "${label}_unterminated_final_record" ;;
    esac
    case "$out" in
        *$'\r'*) stop "${label}_carriage_return_not_allowed" ;;
    esac
    CAPTURE_OUT="${out%$'\n'}"
}

# --- bind the container before the contents (Pattern 3) ---------------------
bind_dir() {
    local p="$1" canon own mode g o
    [ ! -L "$p" ] || stop "parent_is_symlink path=$p"
    [ -d "$p" ]   || stop "parent_not_a_directory path=$p"
    [ -x "$p" ]   || stop "parent_not_searchable path=$p"
    canon="$("$TOOL_READLINK" -f -- "$p" </dev/null 2>/dev/null)" || stop "parent_canonicalization_failed path=$p"
    [ "$canon" = "$p" ] || fail "parent_not_canonical path=$p canonical=$canon"
    own="$("$TOOL_STAT" -c '%u' -- "$p" </dev/null 2>/dev/null)"  || stop "parent_owner_probe_failed path=$p"
    mode="$("$TOOL_STAT" -c '%a' -- "$p" </dev/null 2>/dev/null)" || stop "parent_mode_probe_failed path=$p"
    [ "$own" = "$EUID" ] || fail "parent_owner_uid=$own expected=$EUID path=$p"
    o="${mode#"${mode%?}"}"
    g="${mode%?}"; g="${g#"${g%?}"}"
    case "$o" in 2|3|6|7) fail "parent_other_writable mode=$mode path=$p" ;; esac
    case "$g" in 2|3|6|7) fail "parent_group_writable mode=$mode path=$p" ;; esac
    note "parent_bound path=$p owner_uid=$own mode=$mode"
}

# --- calibrate the absence diagnostic against the pinned tool itself --------
# The exact sentence this pinned `stat` emits for an absent name under an
# already-bound parent is measured once, in this run, and becomes a template
# that later classifications must match as a WHOLE string. A mixed, wrapped or
# doubled diagnostic cannot satisfy it, so it can never be read as absence.
ENOENT_TEMPLATE=''
calibrate_absence() {
    local probe="$1" diag rc=0
    if [ -e "$probe" ] || [ -L "$probe" ]; then stop "enoent_calibration_path_present path=$probe" ; fi
    diag="$("$TOOL_STAT" -c '%F' -- "$probe" </dev/null 2>&1)" || rc=$?
    [ "$rc" -ne 0 ] || stop "enoent_calibration_probe_succeeded path=$probe"
    case "$diag" in *$'\n'*|*$'\r'*) stop "enoent_calibration_multiline path=$probe" ;; esac
    case "$diag" in
        *"No such file or directory"*) : ;;
        *) stop "enoent_calibration_unrecognised path=$probe rc=$rc detail=$diag" ;;
    esac
    ENOENT_TEMPLATE="${diag//"$probe"/@PATH@}"
    [ "$ENOENT_TEMPLATE" != "$diag" ] || stop "enoent_calibration_no_path_in_diagnostic detail=$diag"
    note "enoent_calibration rc=$rc template=$ENOENT_TEMPLATE"
}

# --- classify one path with the kernel, corroborated by the diagnostic -------
# No temporary file is created and no diagnostic prose is substring-matched: a
# multiline, mixed or unrecognised diagnostic is STOP, never "absent".
probe_path() {
    local p="$1" diag rc=0 expected
    [ -n "$ENOENT_TEMPLATE" ] || stop "path_probe_before_calibration path=$p"
    if [ -L "$p" ]; then printf 'link\n'; return 0; fi
    diag="$("$TOOL_STAT" -c '%F' -- "$p" </dev/null 2>&1)" || rc=$?
    case "$diag" in *$'\n'*|*$'\r'*) stop "path_probe_multiline path=$p rc=$rc" ;; esac
    if [ "$rc" -eq 0 ]; then
        case "$diag" in
            "symbolic link")                     printf 'link\n' ;;
            "regular file"|"regular empty file") printf 'regular\n' ;;
            "directory")                         printf 'dir\n' ;;
            *)                                   printf 'other\n' ;;
        esac
        return 0
    fi
    if [ -e "$p" ] || [ -L "$p" ]; then
        stop "path_probe_error path=$p rc=$rc detail=$diag"
    fi
    expected="${ENOENT_TEMPLATE//@PATH@/$p}"
    [ "$diag" = "$expected" ] || stop "path_probe_unclassified path=$p rc=$rc detail=$diag"
    printf 'absent\n'
}

# --- 0. bind both containers, then calibrate --------------------------------
ARCHIVE_PARENT="${ARCHIVE%/*}"
EXTRACT_PARENT="${EXTRACT_DIR%/*}"
case "$ARCHIVE" in /*) : ;; *) stop "archive_path_not_absolute path=$ARCHIVE" ;; esac
case "$EXTRACT_DIR" in /*) : ;; *) stop "extract_dir_not_absolute path=$EXTRACT_DIR" ;; esac
bind_dir "$ARCHIVE_PARENT"
[ "$EXTRACT_PARENT" = "$ARCHIVE_PARENT" ] || bind_dir "$EXTRACT_PARENT"
calibrate_absence "$EXTRACT_PARENT/.wpi_enoent_calibration_probe"

# --- 1. RE-HASH THE ARCHIVE FIRST -------------------------------------------
# Nothing about the archive's contents is read or trusted until its bytes are
# proven to be the Stage 1 bytes. An upload that landed truncated, appended to,
# or replaced is refused here, before `tar` ever parses a header.
KIND="$(probe_path "$ARCHIVE")" || exit $?
[ "$KIND" = "regular" ] || fail "archive_kind=$KIND path=$ARCHIVE"

ARCHIVE_BYTES="$("$TOOL_STAT" -c '%s' -- "$ARCHIVE" </dev/null 2>/dev/null)" || stop "archive_size_probe_failed path=$ARCHIVE"
printf 'EXTRACT_archive path=%s bytes=%s\n' "$ARCHIVE" "$ARCHIVE_BYTES"
[ "$ARCHIVE_BYTES" = "$EXPECT_ARCHIVE_BYTES" ] \
    || fail "archive_bytes=$ARCHIVE_BYTES expected=$EXPECT_ARCHIVE_BYTES path=$ARCHIVE"

archive_digest() {
    local out rc=0
    out="$("$TOOL_SHA256SUM" -- "$ARCHIVE" </dev/null 2>&1)" || rc=$?
    [ "$rc" -eq 0 ] || stop "archive_hash_failed path=$ARCHIVE rc=$rc detail=$out"
    case "$out" in *$'\n'*|*$'\r'*) stop "archive_hash_output_multiline path=$ARCHIVE" ;; esac
    printf '%s\n' "${out%% *}"
}

ACTUAL_ARCHIVE_SHA="$(archive_digest)" || exit $?
printf 'EXTRACT_archive_sha256 actual=%s expected=%s\n' "$ACTUAL_ARCHIVE_SHA" "$EXPECT_ARCHIVE_SHA"
[ "$ACTUAL_ARCHIVE_SHA" = "$EXPECT_ARCHIVE_SHA" ] \
    || fail "archive_sha256_mismatch actual=$ACTUAL_ARCHIVE_SHA expected=$EXPECT_ARCHIVE_SHA"

# --- 2. member list: exactly the preregistered regular members, exact order --
# `tar -tvf` carries the type character; `tar -tf` carries the names. Both are
# adjudicated only after run_capture has proved the listing completed with no
# diagnostics and ended on a record boundary. An absolute path, a `..`
# component, any `/`, a directory member or a member count other than the
# derived one is a FAIL, not a warning.
run_capture "tar_type_listing" required "$TOOL_TAR" -tvf "$ARCHIVE"
TYPE_LIST="$CAPTURE_OUT"
run_capture "tar_name_listing" required "$TOOL_TAR" -tf "$ARCHIVE"
NAME_LIST="$CAPTURE_OUT"

# The listings and the digest must describe the same bytes.
RECHECK_SHA="$(archive_digest)" || exit $?
[ "$RECHECK_SHA" = "$ACTUAL_ARCHIVE_SHA" ] \
    || stop "archive_changed_during_listing first=$ACTUAL_ARCHIVE_SHA second=$RECHECK_SHA"

TYPE_COUNT=0
while IFS= read -r line; do
    TYPE_COUNT=$((TYPE_COUNT + 1))
    case "$line" in
        -*) : ;;
        d*) fail "tar_member_is_directory line=[$line]" ;;
        l*|h*) fail "tar_member_is_link line=[$line]" ;;
        *) fail "tar_member_not_regular line=[$line]" ;;
    esac
done <<EOF
$TYPE_LIST
EOF
[ "$TYPE_COUNT" -eq "$MEMBER_COUNT" ] || fail "tar_member_count=$TYPE_COUNT expected=$MEMBER_COUNT"

NAME_COUNT=0
while IFS= read -r name; do
    NAME_COUNT=$((NAME_COUNT + 1))
    case "$name" in
        /*)        fail "tar_member_absolute name=[$name]" ;;
        ..|../*|*/..|*/../*) fail "tar_member_traversal name=[$name]" ;;
        */*)       fail "tar_member_not_basename name=[$name]" ;;
        "")        fail "tar_member_empty_name" ;;
    esac
done <<EOF
$NAME_LIST
EOF
[ "$NAME_COUNT" -eq "$MEMBER_COUNT" ] || fail "tar_name_count=$NAME_COUNT expected=$MEMBER_COUNT"

[ "$NAME_LIST" = "$MEMBERS" ] || {
    printf 'EXTRACT_actual_members\n%s\n' "$NAME_LIST" >&2
    fail "tar_member_set_or_order_differs_from_stage1"
}
note "members_exact count=$MEMBER_COUNT order=stage1"

# --- 3. fresh create-once extraction directory ------------------------------
KIND="$(probe_path "$EXTRACT_DIR")" || exit $?
[ "$KIND" = "absent" ] || fail "extract_dir_already_present kind=$KIND path=$EXTRACT_DIR"
MK_OUT="$("$TOOL_MKDIR" -m 0700 -- "$EXTRACT_DIR" </dev/null 2>&1)" || stop "extract_dir_mkdir_failed path=$EXTRACT_DIR detail=$MK_OUT"
[ -z "$MK_OUT" ] || stop "extract_dir_mkdir_diagnostics path=$EXTRACT_DIR detail=$MK_OUT"
CANON="$("$TOOL_READLINK" -f -- "$EXTRACT_DIR" </dev/null 2>/dev/null)" || stop "canonicalization_failed path=$EXTRACT_DIR"
[ "$CANON" = "$EXTRACT_DIR" ] || fail "extract_dir_not_canonical path=$EXTRACT_DIR canonical=$CANON"
note "extract_dir_allocated path=$EXTRACT_DIR"

# --- 4. extract -------------------------------------------------------------
TAR_RC=0
TAR_OUT="$("$TOOL_TAR" -xf "$ARCHIVE" -C "$EXTRACT_DIR" </dev/null 2>&1)" || TAR_RC=$?
[ "$TAR_RC" -eq 0 ] || stop "tar_extract_failed rc=$TAR_RC detail=$TAR_OUT"
[ -z "$TAR_OUT" ] || stop "tar_extract_stderr detail=$TAR_OUT"

# The extracted tree must be exactly the preregistered member set and nothing
# else: no directory, no symlink, no extra member that the listing above did
# not show.
run_capture "extract_tree_walk" optional "$TOOL_FIND" "$EXTRACT_DIR" -mindepth 1 '!' -type f -print
EXTRA="$CAPTURE_OUT"
[ -z "$EXTRA" ] || fail "extract_tree_non_regular_entries=[$EXTRA]"

run_capture "extract_tree_count" optional "$TOOL_FIND" "$EXTRACT_DIR" -mindepth 1 -type f -print
FILE_COUNT="$(count_records "$CAPTURE_OUT")"
[ "$FILE_COUNT" -eq "$MEMBER_COUNT" ] || fail "extracted_file_count=$FILE_COUNT expected=$MEMBER_COUNT"

# --- 5. read-only ------------------------------------------------------------
while IFS= read -r name; do
    CH_OUT="$("$TOOL_CHMOD" 0444 -- "$EXTRACT_DIR/$name" </dev/null 2>&1)" || stop "chmod_failed path=$EXTRACT_DIR/$name detail=$CH_OUT"
    [ -z "$CH_OUT" ] || stop "chmod_diagnostics path=$EXTRACT_DIR/$name detail=$CH_OUT"
    MODE="$("$TOOL_STAT" -c '%a' -- "$EXTRACT_DIR/$name" </dev/null 2>/dev/null)" || stop "mode_probe_failed path=$EXTRACT_DIR/$name"
    [ "$MODE" = "444" ] || fail "extracted_mode=$MODE expected=444 path=$EXTRACT_DIR/$name"
done <<EOF
$MEMBERS
EOF
note "extracted_files_readonly mode=0444"

# --- 6. the Stage 1 hashes ---------------------------------------------------
# Verified against constants frozen in this script, in the extraction
# directory, on the extracted bytes — not against anything the archive or the
# host supplies at run time.
CHECK_RC=0
CHECK_OUT="$( ( cd -- "$EXTRACT_DIR" && "$TOOL_SHA256SUM" -c --strict - ) <<EOF 2>&1
$HASHES
EOF
)" || CHECK_RC=$?
[ "$CHECK_RC" -eq 0 ] || fail "block_hash_verification_failed rc=$CHECK_RC detail=$CHECK_OUT"

while IFS= read -r name; do
    SUM_OUT="$("$TOOL_SHA256SUM" -- "$EXTRACT_DIR/$name" </dev/null 2>&1)" || stop "block_hash_failed path=$EXTRACT_DIR/$name detail=$SUM_OUT"
    case "$SUM_OUT" in *$'\n'*|*$'\r'*) stop "block_hash_output_multiline path=$EXTRACT_DIR/$name" ;; esac
    printf 'EXTRACT_block name=%s sha256=%s\n' "$name" "${SUM_OUT%% *}"
done <<EOF
$MEMBERS
EOF

printf 'EXTRACT PASS archive=%s archive_sha256=%s dir=%s members=%s verified=%s executed=0\n' \
    "$ARCHIVE" "$ACTUAL_ARCHIVE_SHA" "$EXTRACT_DIR" "$MEMBER_COUNT" "$MEMBER_COUNT"
