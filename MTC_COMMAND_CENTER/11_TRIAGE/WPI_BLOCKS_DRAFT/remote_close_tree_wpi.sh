# WP-I Stage 2 - closed evidence-tree hashing, remote side (PREREGISTERED).
#
# Transport ops 07 and 08. Delivered on ssh stdin to the pinned remote launch
# domain frozen in `transport_runner.ps1` and carried verbatim by the plan:
#   /usr/bin/env -i PATH=/usr/bin:/bin LC_ALL=C HOME=/home/gatea \
#     /usr/bin/bash --noprofile --norc -s -- <EV_DIR> <RUNID> <WORK_ROOT>
#
# DERIVATION. This file is the third `_wpi` derived script of section 4 and the
# fourth delivered derived shell file. Its derivation basis is the accepted
# Stage 2 artifact `02_PREREG/remote_close_tree.sh` (7470 B,
# 87157f0ea454df7c1f826a8c76a38f3045dd38efdd8fa347644f79251d3f3f0e), which is
# byte-frozen and is NOT edited. The accepted original stays recorded as the
# derivation basis; it no longer travels.
#
# The permitted semantic deltas against that original are EXACTLY derivation
# classes 2, 3, 5 and 6 of the section 4 contract, and nothing else:
#
#   class 2 - PROGRAM IDENTITY. Every executable this script invokes - stat,
#     sha256sum, tr, readlink, find, sort, cmp, rm, mkdir - plus the launch
#     domain's own `/usr/bin/env` and `/usr/bin/bash`, is resolved from a frozen
#     absolute /usr/bin pin and admitted only after a non-following kind check,
#     numeric 0:0 ownership and a not-group/other-writable mode. The inherited
#     PATH selects nothing.
#
#   class 3 - STOP-BEFORE-MUTATION PATH CLASSIFICATION (Codex final audit F3).
#     The accepted original classified ANY diagnostic containing the substring
#     `No such file or directory` as absence, so a mixed `No such file or
#     directory; Permission denied` diagnostic became `CLOSE_FAIL reason=
#     evidence_dir_absent` at rc 1 - a completed observation of missing evidence
#     manufactured out of an inability to evaluate. The absence sentence this
#     pinned `stat` emits is now calibrated ONCE in this run under an already
#     bound parent and every later classification must match that template as a
#     WHOLE string, corroborated by the kernel reporting neither object nor
#     link. Multiline, mixed, wrapped or unrecognised diagnostics STOP.
#     Directory identity is compared NUMERICALLY (`%u:%g`) against the
#     preregistered EXPECT_UID/EXPECT_GID with the rendered `%U:%G` name kept
#     diagnostic only: a resolver-rendered name is not an identity (Pattern 8).
#
#   class 5 - LAUNCH-DOMAIN ATTESTATION (Codex final audit F1). Before any
#     external program runs, and using shell builtins only, the script attests
#     that it is running under the pinned absolute interpreter, that the
#     environment is the explicitly constructed one and nothing else, that
#     BASH_ENV/ENV are unset, that no shell function was inherited, and that no
#     TMPDIR was inherited. Under the accepted bytes a `bash` first on PATH, or
#     an inherited BASH_ENV, ran a plant that ignored the delivered script and
#     forged its rc/marker pair.
#
#   class 6 - RUN-OWNED SCRATCH (Codex final audit F2). The accepted original
#     called `mktemp`, which honours an inherited TMPDIR: with TMPDIR set to the
#     evidence directory the script created and hashed its own files inside the
#     tree it was measuring while printing `wrote_into_evidence_tree=0`. There is
#     now no `mktemp` and no inherited scratch location at all. The script takes
#     a WORK_ROOT argument, proves canonical non-overlap with the evidence tree
#     BEFORE creating a create-once work directory under it, exports TMPDIR to
#     that proven directory, and removes it on every exit path.
#
# Everything else - the RUNID and EV_DIR grammar, the two-pass digest stability
# rule and the emitted record grammar - is the accepted logic unchanged.
#
# SCOPE LIMIT, STATED RATHER THAN IMPLIED (Pattern 9). The pins bind a locator
# and that object's metadata, NOT its bytes. Each admitted tool's SHA-256 is
# computed and emitted as evidence so the operator record carries what actually
# ran, but it is deliberately NOT compared against a frozen digest: no digest of
# a remote tool can be known before host contact, and a digest this run learned
# from the object it is attesting would not be an attestation. That limit now
# covers `/usr/bin/bash` and `/usr/bin/env` too: the launch-domain attestation
# establishes that THIS interpreter was reached by absolute path through a
# constructed environment, not that its bytes are the ones a deploy channel
# approved. Binding remote tool bytes requires a deploy-channel attestation and
# is a successor preregistration item, not a claim this script makes.
#
# It is READ-ONLY with respect to the evidence tree, and after class 6 that
# sentence is earned rather than asserted: the only directory this script
# creates is proven, before creation, to be canonically disjoint from EV_DIR.
#
# No service, unit, credential, port, network, broker/exchange/order/TESTNET/
# mainnet or economic action. No deletion, rename, truncation or chmod of any
# evidence object.
#
# rc contract: 0 = closed tree hashed, 1 = FAIL (predicate refused),
#              3 = STOP (could not evaluate -- never re-read as a binding).
set -Eeuo pipefail

# --- class 5: launch-domain attestation, shell builtins only -----------------
# This block runs BEFORE the first external program, so a plant that replaced
# the interpreter or injected a startup file is refused rather than measured.
# A launch-domain violation is an inability to evaluate, never a host finding:
# every arm here is rc 3.
EXPECT_INTERPRETER='/usr/bin/bash'
EXPECT_PATH='/usr/bin:/bin'
EXPECT_LC_ALL='C'

ld_stop() { printf 'CLOSE_STOP reason=%s\n' "$*" >&2; exit 3; }

[ "${BASH:-}" = "$EXPECT_INTERPRETER" ] \
    || ld_stop "launch_domain_interpreter=${BASH:-unset} expected=$EXPECT_INTERPRETER"
[ "${BASH_ENV+set}" != 'set' ] || ld_stop "launch_domain_bash_env_inherited"
[ "${ENV+set}" != 'set' ]      || ld_stop "launch_domain_env_variable_inherited"
[ "${TMPDIR+set}" != 'set' ]   || ld_stop "launch_domain_tmpdir_inherited"
[ "${PATH:-}" = "$EXPECT_PATH" ] \
    || ld_stop "launch_domain_path=${PATH:-unset} expected=$EXPECT_PATH"
[ "${LC_ALL:-}" = "$EXPECT_LC_ALL" ] \
    || ld_stop "launch_domain_lc_all=${LC_ALL:-unset} expected=$EXPECT_LC_ALL"
[ -n "${HOME:-}" ] || ld_stop "launch_domain_home_absent"
case "${HOME:-}" in /*) : ;; *) ld_stop "launch_domain_home_not_absolute value=${HOME:-}" ;; esac

# An exported shell function arrives as an ordinary environment entry, so the
# name sweep below already refuses it; this refuses a function defined by any
# other route as well. `declare -F` is a builtin and the command substitution is
# a subshell of this same interpreter - no external program is involved.
LD_FUNCS="$(declare -F)"
[ -z "$LD_FUNCS" ] || ld_stop "launch_domain_inherited_shell_function"

# The environment must be exactly the constructed set. Anything else - an
# inherited LD_PRELOAD, a BASH_FUNC_x%% entry, a stray TMPDIR spelling - is a
# name this sweep does not recognise, and it STOPs naming the offender.
LD_SEEN_HOME=0; LD_SEEN_PATH=0; LD_SEEN_LC_ALL=0
for LD_NAME in $(compgen -e); do
    case "$LD_NAME" in
        HOME)   LD_SEEN_HOME=1 ;;
        PATH)   LD_SEEN_PATH=1 ;;
        LC_ALL) LD_SEEN_LC_ALL=1 ;;
        PWD|SHLVL|OLDPWD|_) : ;;
        *) ld_stop "launch_domain_unexpected_environment_name=$LD_NAME" ;;
    esac
done
[ "$LD_SEEN_HOME" -eq 1 ]   || ld_stop "launch_domain_home_not_exported"
[ "$LD_SEEN_PATH" -eq 1 ]   || ld_stop "launch_domain_path_not_exported"
[ "$LD_SEEN_LC_ALL" -eq 1 ] || ld_stop "launch_domain_lc_all_not_exported"

# --- preregistered identities ------------------------------------------------
# Numeric, because a rendered owner name is a resolver answer and not an
# identity. The rendered pair is still emitted, as a diagnostic.
EXPECT_UID='<PIN-AT-FREEZE>'
EXPECT_GID='<PIN-AT-FREEZE>'
EXPECT_MODE='700'

fail() { printf 'CLOSE_FAIL reason=%s\n' "$*" >&2; exit 1; }
stop() { printf 'CLOSE_STOP reason=%s\n' "$*" >&2; exit 3; }
note() { printf 'CLOSE_NOTE %s\n' "$*"; }

note "launch_domain interpreter=$BASH path=$PATH lc_all=$LC_ALL bash_env=unset env=unset tmpdir=unset inherited_functions=0 attestation=builtins_only"

# --- pinned program identities (derivation class 2) --------------------------
# The absolute path IS the pin; the inherited PATH selects nothing. `stat` is
# the bootstrap root of trust and is the first object verified, including
# itself. Ownership is compared numerically.
TOOL_STAT='/usr/bin/stat'
TOOL_SHA256SUM='/usr/bin/sha256sum'
TOOL_TR='/usr/bin/tr'
TOOL_READLINK='/usr/bin/readlink'
TOOL_FIND='/usr/bin/find'
TOOL_SORT='/usr/bin/sort'
TOOL_CMP='/usr/bin/cmp'
TOOL_RM='/usr/bin/rm'
TOOL_MKDIR='/usr/bin/mkdir'
# The launch domain's own two programs are admitted under the same rule, so the
# interpreter this script is attesting is inside the pinned program domain
# rather than beside it.
TOOL_ENV='/usr/bin/env'
TOOL_BASH='/usr/bin/bash'

require_tool() {
    local t="$1" own mode g o
    case "$t" in /*) : ;; *) stop "tool_path_not_absolute path=$t" ;; esac
    [ ! -L "$t" ] || stop "tool_is_symlink path=$t"
    [ -f "$t" ]   || stop "tool_missing_or_not_regular path=$t"
    [ -x "$t" ]   || stop "tool_not_executable path=$t"
    own="$(LC_ALL=C "$TOOL_STAT" -c '%u:%g' -- "$t" </dev/null 2>/dev/null)" || stop "tool_owner_probe_failed path=$t"
    mode="$(LC_ALL=C "$TOOL_STAT" -c '%a' -- "$t" </dev/null 2>/dev/null)"   || stop "tool_mode_probe_failed path=$t"
    [ "$own" = '0:0' ] || stop "tool_owner_numeric=$own expected=0:0 path=$t"
    o="${mode#"${mode%?}"}"
    g="${mode%?}"; g="${g#"${g%?}"}"
    case "$o" in 2|3|6|7) stop "tool_other_writable mode=$mode path=$t" ;; esac
    case "$g" in 2|3|6|7) stop "tool_group_writable mode=$mode path=$t" ;; esac
    note "tool name=${t##*/} path=$t owner_numeric=$own mode=$mode resolution=pinned_absolute"
}

require_tool "$TOOL_STAT"
require_tool "$TOOL_SHA256SUM"
require_tool "$TOOL_TR"
require_tool "$TOOL_READLINK"
require_tool "$TOOL_FIND"
require_tool "$TOOL_SORT"
require_tool "$TOOL_CMP"
require_tool "$TOOL_RM"
require_tool "$TOOL_MKDIR"
require_tool "$TOOL_ENV"
require_tool "$TOOL_BASH"

# The attested interpreter must be the pinned object, not merely a path that
# spells the same characters: `$BASH` was compared as a string above, and the
# pin admitted `/usr/bin/bash` as a non-symlink root-owned regular file here.
[ "$BASH" = "$TOOL_BASH" ] || stop "launch_domain_interpreter_outside_pinned_set value=$BASH"

# --- runtime tool digests: EVIDENCE, not a comparison ------------------------
# Recorded so the operator-side record carries the identity of what actually
# ran. Not compared to anything: see the scope limit in the header.
record_tool_digest() {
    local t="$1" out rc=0
    out="$(LC_ALL=C "$TOOL_SHA256SUM" -- "$t" </dev/null 2>&1)" || rc=$?
    [ "$rc" -eq 0 ] || stop "tool_digest_failed path=$t rc=$rc"
    case "$out" in *$'\n'*|*$'\r'*) stop "tool_digest_output_multiline path=$t" ;; esac
    note "tool_digest name=${t##*/} sha256=${out%% *} binding=recorded_as_evidence_not_compared_to_a_frozen_pin"
}

for TOOL_PATH in "$TOOL_STAT" "$TOOL_SHA256SUM" "$TOOL_TR" "$TOOL_READLINK" \
                 "$TOOL_FIND" "$TOOL_SORT" "$TOOL_CMP" "$TOOL_RM" \
                 "$TOOL_MKDIR" "$TOOL_ENV" "$TOOL_BASH"; do
    record_tool_digest "$TOOL_PATH"
done
note "tool_digest_limit no_frozen_remote_tool_digest_can_be_known_before_host_contact"

[ "$#" -eq 3 ] || fail "usage remote_close_tree_wpi.sh <EV_DIR> <RUNID> <WORK_ROOT> argc=$#"
EV_DIR="$1"
RUNID="$2"
WORK_ROOT="$3"

# --- the preregistered numeric identities must be filled ---------------------
# An unfilled freeze pin is a missing input, not a deviant host: rc 3.
case "$EXPECT_UID" in ''|*[!0-9]*) stop "expect_uid_unfilled_or_not_numeric value=[$EXPECT_UID]" ;; esac
case "$EXPECT_GID" in ''|*[!0-9]*) stop "expect_gid_unfilled_or_not_numeric value=[$EXPECT_GID]" ;; esac

# --- the run identifier must still be ONE safe path component ---------------
case "$RUNID" in
    ""|"."|"..")       fail "runid_reserved value=[$RUNID]" ;;
    -*)                fail "runid_leading_dash value=[$RUNID]" ;;
    *[!A-Za-z0-9._-]*) fail "runid_charset value=[$RUNID]" ;;
esac

# --- EV_DIR must be spelled as a direct child leaf named exactly RUNID -------
# The binding is recorded against RUNID, so the directory being hashed must be
# the one the run allocated, not a sibling that merely looks similar.
EV_BASE="${EV_DIR##*/}"
[ "$EV_BASE" = "$RUNID" ] || fail "evdir_basename=$EV_BASE runid=$RUNID"

# --- WORK_ROOT grammar, before anything is created under it -----------------
case "$WORK_ROOT" in
    /*) : ;;
    *)  stop "work_root_not_absolute value=[$WORK_ROOT]" ;;
esac
case "$WORK_ROOT" in
    */)                 stop "work_root_trailing_slash value=[$WORK_ROOT]" ;;
    *[!A-Za-z0-9._/-]*) stop "work_root_charset value=[$WORK_ROOT]" ;;
    */../*|*/..)        stop "work_root_dot_dot value=[$WORK_ROOT]" ;;
    */./*|*/.)          stop "work_root_dot value=[$WORK_ROOT]" ;;
esac

# --- bind WORK_ROOT: it is a launch input, so every refusal here is STOP -----
[ ! -L "$WORK_ROOT" ] || stop "work_root_is_symlink path=$WORK_ROOT"
[ -d "$WORK_ROOT" ]   || stop "work_root_missing_or_not_directory path=$WORK_ROOT"
WORK_ROOT_CANON="$("$TOOL_READLINK" -f -- "$WORK_ROOT")" || stop "work_root_canonicalization_failed path=$WORK_ROOT"
[ "$WORK_ROOT_CANON" = "$WORK_ROOT" ] || stop "work_root_not_canonical path=$WORK_ROOT canonical=$WORK_ROOT_CANON"
WR_OWN_NUM="$(LC_ALL=C "$TOOL_STAT" -c '%u:%g' -- "$WORK_ROOT")" || stop "work_root_owner_probe_failed path=$WORK_ROOT"
WR_OWN_NAME="$(LC_ALL=C "$TOOL_STAT" -c '%U:%G' -- "$WORK_ROOT")" || stop "work_root_owner_name_probe_failed path=$WORK_ROOT"
WR_MODE="$(LC_ALL=C "$TOOL_STAT" -c '%a' -- "$WORK_ROOT")" || stop "work_root_mode_probe_failed path=$WORK_ROOT"
[ "$WR_OWN_NUM" = "$EXPECT_UID:$EXPECT_GID" ] \
    || stop "work_root_owner_numeric=$WR_OWN_NUM expected=$EXPECT_UID:$EXPECT_GID rendered=$WR_OWN_NAME path=$WORK_ROOT"
[ "$WR_MODE" = "$EXPECT_MODE" ] || stop "work_root_mode=$WR_MODE expected=$EXPECT_MODE path=$WORK_ROOT"
note "work_root_ok path=$WORK_ROOT owner_numeric=$WR_OWN_NUM owner_rendered=$WR_OWN_NAME mode=$WR_MODE"

# --- calibrate the absence diagnostic against the pinned tool itself --------
# Class 3. Substring-matching `No such file or directory` is what let a mixed
# ENOENT+EACCES diagnostic be read as absence. Instead the exact sentence this
# pinned `stat` emits for an absent name under an already-bound parent is
# measured once, in this run, and turned into a template. Every later
# classification must match that template as a WHOLE string, so any wrapper,
# prefix, suffix or second diagnostic fails the comparison.
ENOENT_TEMPLATE=''
calibrate_absence() {
    local probe="$1" diag rc=0
    if [ -e "$probe" ] || [ -L "$probe" ]; then stop "enoent_calibration_path_present path=$probe" ; fi
    diag="$(LC_ALL=C "$TOOL_STAT" -c '%F' -- "$probe" </dev/null 2>&1)" || rc=$?
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

calibrate_absence "$WORK_ROOT/.wpi_close_enoent_calibration_$RUNID"

# --- classify one path with the kernel, corroborated by the diagnostic -------
# Three independent statements must agree before a probe is called absence:
# `stat` failed, the kernel reports neither an object nor a link, and the
# diagnostic equals the calibrated template exactly. Anything else - multiline,
# mixed, wrapped, or unrecognised - is STOP, never "absent".
probe_path() {
    local p="$1" diag rc=0 expected
    [ -n "$ENOENT_TEMPLATE" ] || stop "path_probe_before_calibration path=$p"
    if [ -L "$p" ]; then printf 'link\n'; return 0; fi
    diag="$(LC_ALL=C "$TOOL_STAT" -c '%F' -- "$p" </dev/null 2>&1)" || rc=$?
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

KIND="$(probe_path "$EV_DIR")" || exit $?
case "$KIND" in
    dir)    : ;;
    absent) fail "evidence_dir_absent path=$EV_DIR" ;;
    link)   fail "evidence_dir_is_symlink path=$EV_DIR" ;;
    *)      fail "evidence_dir_kind=$KIND path=$EV_DIR" ;;
esac
CANON="$("$TOOL_READLINK" -f -- "$EV_DIR")" || stop "canonicalization_failed path=$EV_DIR"
[ "$CANON" = "$EV_DIR" ] || fail "evidence_dir_not_canonical path=$EV_DIR canonical=$CANON"
OWN_NUM="$(LC_ALL=C "$TOOL_STAT" -c '%u:%g' -- "$EV_DIR")" || stop "owner_probe_failed path=$EV_DIR"
OWN_NAME="$(LC_ALL=C "$TOOL_STAT" -c '%U:%G' -- "$EV_DIR")" || stop "owner_name_probe_failed path=$EV_DIR"
MODE="$(LC_ALL=C "$TOOL_STAT" -c '%a' -- "$EV_DIR")"   || stop "mode_probe_failed path=$EV_DIR"
[ "$OWN_NUM" = "$EXPECT_UID:$EXPECT_GID" ] \
    || fail "evidence_dir_owner_numeric=$OWN_NUM expected=$EXPECT_UID:$EXPECT_GID rendered=$OWN_NAME"
[ "$MODE" = "$EXPECT_MODE" ] || fail "evidence_dir_mode=$MODE expected=$EXPECT_MODE"
note "evidence_dir_ok path=$EV_DIR owner_numeric=$OWN_NUM owner_rendered=$OWN_NAME mode=$MODE"

# --- class 6: a run-owned work directory, proven disjoint BEFORE creation ----
# Non-overlap is decided on canonical spellings, both directions: the work
# directory may not BE the evidence tree, may not live inside it, and may not
# contain it. The proof happens before `mkdir`, and is repeated on the object
# that `mkdir` actually produced, so a path substituted between the two moments
# is refused rather than used.
WORK="$WORK_ROOT_CANON/close_work_$RUNID"

assert_disjoint_from_evidence() {
    local w="$1" phase="$2"
    [ "$w" != "$CANON" ] || stop "work_dir_is_evidence_dir phase=$phase path=$w"
    case "$w" in
        "$CANON"/*) stop "work_dir_inside_evidence_tree phase=$phase path=$w evidence=$CANON" ;;
    esac
    case "$CANON" in
        "$w"/*) stop "evidence_tree_inside_work_dir phase=$phase path=$w evidence=$CANON" ;;
    esac
}

assert_disjoint_from_evidence "$WORK" "before_create"

WORK_KIND="$(probe_path "$WORK")" || exit $?
[ "$WORK_KIND" = 'absent' ] || stop "work_dir_already_present kind=$WORK_KIND path=$WORK"

# `mkdir -m 0700`, no `-p`: the mode is applied explicitly so a permissive umask
# cannot widen it, and a missing intermediate fails loudly instead of being
# manufactured. Any diagnostic at all is STOP.
MKDIR_OUT="$(LC_ALL=C "$TOOL_MKDIR" -m 0700 -- "$WORK" </dev/null 2>&1)" || stop "work_dir_mkdir_failed path=$WORK"
[ -z "$MKDIR_OUT" ] || stop "work_dir_mkdir_diagnostics path=$WORK detail=$MKDIR_OUT"

# From here on the work directory exists, so every exit path removes it.
trap '[ -z "${WORK:-}" ] || "$TOOL_RM" -rf -- "$WORK" || :' EXIT

[ ! -L "$WORK" ] || stop "work_dir_is_symlink path=$WORK"
[ -d "$WORK" ]   || stop "work_dir_not_a_directory path=$WORK"
WORK_CANON="$("$TOOL_READLINK" -f -- "$WORK")" || stop "work_dir_canonicalization_failed path=$WORK"
[ "$WORK_CANON" = "$WORK" ] || stop "work_dir_not_canonical path=$WORK canonical=$WORK_CANON"
assert_disjoint_from_evidence "$WORK_CANON" "after_create"
WORK_OWN_NUM="$(LC_ALL=C "$TOOL_STAT" -c '%u:%g' -- "$WORK")" || stop "work_dir_owner_probe_failed path=$WORK"
WORK_MODE="$(LC_ALL=C "$TOOL_STAT" -c '%a' -- "$WORK")" || stop "work_dir_mode_probe_failed path=$WORK"
[ "$WORK_OWN_NUM" = "$EXPECT_UID:$EXPECT_GID" ] \
    || stop "work_dir_owner_numeric=$WORK_OWN_NUM expected=$EXPECT_UID:$EXPECT_GID path=$WORK"
[ "$WORK_MODE" = "$EXPECT_MODE" ] || stop "work_dir_mode=$WORK_MODE expected=$EXPECT_MODE path=$WORK"

# Nothing this script runs consults TMPDIR - there is no `mktemp` any more and
# every scratch name below is composed explicitly - but any future child that
# did would land in the proven directory rather than in an inherited location.
export TMPDIR="$WORK"
note "scratch work_dir=$WORK owner_numeric=$WORK_OWN_NUM mode=$WORK_MODE created=once tmpdir=run_owned canonical_non_overlap=proven_before_and_after_create removal=on_every_exit_path"

# --- the tree may contain ordinary directories and regular files only --------
# A symlink inside the tree would make the digest set attest to bytes that live
# somewhere else, which is exactly what the binding exists to prevent.
ODD="$(LC_ALL=C "$TOOL_FIND" "$EV_DIR" -mindepth 1 '!' -type d '!' -type f -print)" \
    || stop "evidence_tree_walk_failed path=$EV_DIR"
[ -z "$ODD" ] || fail "evidence_tree_non_regular_entries=[$ODD]"

# --- collect the file list, no pipeline -------------------------------------
# RP0 pipeline discipline: where a pipeline can be avoided it is avoided. `find`
# writes a NUL-delimited list to a file in the PROVEN work directory, `sort`
# reads and rewrites that file in place with -o, and the sorted records are read
# into an array. Nothing is written into EV_DIR at any point.
RAW="$WORK/raw.0"
SORTED="$WORK/sorted.0"

LC_ALL=C "$TOOL_FIND" "$EV_DIR" -type f -print0 > "$RAW" \
    || stop "evidence_file_inventory_failed path=$EV_DIR"
LC_ALL=C "$TOOL_SORT" -z "$RAW" -o "$SORTED" \
    || stop "evidence_file_sort_failed path=$EV_DIR"

FILES=()
while IFS= read -r -d '' f; do
    FILES+=("$f")
done < "$SORTED"

COUNT="${#FILES[@]}"
[ "$COUNT" -gt 0 ] || fail "evidence_tree_has_no_regular_file path=$EV_DIR"
note "evidence_files count=$COUNT"

# --- per-file digests, computed twice ---------------------------------------
# Pass 1 and pass 2 must be byte-identical. An evidence leaf that is still open
# and growing changes between the passes and is refused, so a still-open tree is
# never bound as if it were closed.
digest_pass() {
    local f rel out
    for f in "${FILES[@]}"; do
        out="$(LC_ALL=C "$TOOL_SHA256SUM" -- "$f")" || { stop "digest_failed path=$f"; }
        rel="${f#"$EV_DIR"/}"
        printf '%s  %s\n' "${out%% *}" "$rel"
    done
}

PASS1="$WORK/pass1.txt"
PASS2="$WORK/pass2.txt"
digest_pass > "$PASS1" || exit $?
digest_pass > "$PASS2" || exit $?
LC_ALL=C "$TOOL_CMP" -s "$PASS1" "$PASS2" \
    || fail "evidence_tree_not_quiescent digest_set_changed_between_passes"
note "digest_set_stable passes=2"

# --- emit the binding record -------------------------------------------------
# CLOSE_DIGEST lines are the canonical per-file digest set: `<sha256><2 spaces>
# <path relative to EV_DIR>`, in LC_ALL=C byte order of the absolute paths.
# CLOSE_SIZE lines are the §1.5 name/byte-count listing, same order.
printf 'CLOSE_BINDING runid=%s dir=%s files=%s\n' "$RUNID" "$EV_DIR" "$COUNT"
printf 'CLOSE_DIGEST_BEGIN runid=%s\n' "$RUNID"
while IFS= read -r line; do
    printf 'CLOSE_DIGEST %s\n' "$line"
done < "$PASS1"
printf 'CLOSE_DIGEST_END runid=%s\n' "$RUNID"

printf 'CLOSE_SIZE_BEGIN runid=%s\n' "$RUNID"
for f in "${FILES[@]}"; do
    SZ="$(LC_ALL=C "$TOOL_STAT" -c '%s' -- "$f")" || stop "size_probe_failed path=$f"
    printf 'CLOSE_SIZE %s %s\n' "${f#"$EV_DIR"/}" "$SZ"
done
printf 'CLOSE_SIZE_END runid=%s\n' "$RUNID"

# A digest OF the digest set, so the operator-side comparison has one value to
# quote in the record as well as the full set.
SET_SUM="$(LC_ALL=C "$TOOL_SHA256SUM" -- "$PASS1")" || stop "digest_set_hash_failed"
printf 'CLOSE_DIGEST_SET_SHA256 runid=%s %s\n' "$RUNID" "${SET_SUM%% *}"

"$TOOL_RM" -rf -- "$WORK"
printf 'CLOSE PASS runid=%s dir=%s files=%s wrote_into_evidence_tree=0\n' \
    "$RUNID" "$EV_DIR" "$COUNT"
