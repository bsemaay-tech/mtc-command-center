# WP-I Stage 2 — closed evidence-tree hashing, remote side (PREREGISTERED).
#
# Transport ops 07 and 08. Delivered on ssh stdin to:
#   bash -s -- <EV_DIR> <RUNID>
#
# DERIVATION. This file is the fourth derived script of section 4. Its
# derivation basis is the accepted Stage 2 artifact
# `02_PREREG/remote_close_tree.sh` (7470 B,
# 87157f0ea454df7c1f826a8c76a38f3045dd38efdd8fa347644f79251d3f3f0e), which is
# byte-frozen and is NOT edited. The accepted original stays recorded as the
# derivation basis; it no longer travels.
#
# The ONLY permitted semantic delta against that original is derivation class 2,
# program identity (Codex round-2 transport re-audit F3): every executable this
# script invokes - mktemp, stat, tr, readlink, find, sort, sha256sum, cmp and rm
# - is resolved from a frozen absolute /usr/bin pin and admitted only after a
# non-following kind check, numeric 0:0 ownership and a not-group/other-writable
# mode. The inherited PATH selects nothing. Everything else - the RUNID and
# EV_DIR grammar, the lstat-fail-closed classification, the name-rendered owner
# comparison, the two-pass digest stability rule, the temporary-work-directory
# shape and the emitted record grammar - is the accepted logic unchanged.
#
# WHY THE DERIVATION EXISTS. Executed under the accepted bytes, a `sha256sum`
# planted first on the inherited PATH appended to a closed evidence leaf and
# then delegated to the real tool. Both digest passes observed the post-mutation
# bytes, agreed, and the script printed
# `CLOSE PASS ... wrote_into_evidence_tree=0` at rc 0. That sentence was false
# under the delivered execution environment. With the pins below, the planted
# program is never consulted and the sentence is earned.
#
# SCOPE LIMIT, STATED RATHER THAN IMPLIED (Pattern 9). The pins bind a locator
# and that object's metadata, NOT its bytes. Each admitted tool's SHA-256 is
# computed and emitted as evidence so the operator record carries what actually
# ran, but it is deliberately NOT compared against a frozen digest: no digest of
# a remote tool can be known before host contact, and a digest this run learned
# from the object it is attesting would not be an attestation. Binding remote
# tool bytes requires a deploy-channel attestation and is a successor
# preregistration item, not a claim this script makes.
#
# A second inherited residual, disclosed rather than repaired: `mktemp` honours
# TMPDIR from the login environment, so the work directory's LOCATION is still
# inherited. It is created outside EV_DIR by construction and nothing is written
# into the evidence tree either way. Removing mktemp would be a class 3 change
# and is outside this derivation's permitted delta.
#
# It is READ-ONLY with respect to the evidence tree. It writes nothing into
# EV_DIR -- writing a digest file into the directory being hashed would change
# the very bytes the binding attests to. All output goes to stdout, which the
# operator-side transport record captures.
#
# No service, unit, credential, port, network, broker/exchange/order/TESTNET/
# mainnet or economic action. No deletion, rename, truncation or chmod of any
# evidence object.
#
# rc contract: 0 = closed tree hashed, 1 = FAIL (predicate refused),
#              3 = STOP (could not evaluate -- never re-read as a binding).
set -Eeuo pipefail

EXPECT_OWNER='gatea:gatea'
EXPECT_MODE='700'

fail() { printf 'CLOSE_FAIL reason=%s\n' "$*" >&2; exit 1; }
stop() { printf 'CLOSE_STOP reason=%s\n' "$*" >&2; exit 3; }
note() { printf 'CLOSE_NOTE %s\n' "$*"; }

# --- pinned program identities (derivation class 2) --------------------------
# The absolute path IS the pin; the inherited PATH selects nothing. `stat` is
# the bootstrap root of trust and is the first object verified, including
# itself. Ownership is compared numerically.
TOOL_STAT='/usr/bin/stat'
TOOL_SHA256SUM='/usr/bin/sha256sum'
TOOL_MKTEMP='/usr/bin/mktemp'
TOOL_TR='/usr/bin/tr'
TOOL_READLINK='/usr/bin/readlink'
TOOL_FIND='/usr/bin/find'
TOOL_SORT='/usr/bin/sort'
TOOL_CMP='/usr/bin/cmp'
TOOL_RM='/usr/bin/rm'

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
require_tool "$TOOL_MKTEMP"
require_tool "$TOOL_TR"
require_tool "$TOOL_READLINK"
require_tool "$TOOL_FIND"
require_tool "$TOOL_SORT"
require_tool "$TOOL_CMP"
require_tool "$TOOL_RM"

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

for TOOL_PATH in "$TOOL_STAT" "$TOOL_SHA256SUM" "$TOOL_MKTEMP" "$TOOL_TR" \
                 "$TOOL_READLINK" "$TOOL_FIND" "$TOOL_SORT" "$TOOL_CMP" "$TOOL_RM"; do
    record_tool_digest "$TOOL_PATH"
done
note "tool_digest_limit no_frozen_remote_tool_digest_can_be_known_before_host_contact"

[ "$#" -eq 2 ] || fail "usage remote_close_tree_wpi.sh <EV_DIR> <RUNID> argc=$#"
EV_DIR="$1"
RUNID="$2"

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

# --- lstat-fail-closed classification: a probe error is never "absent" -------
probe_path() {
    local p="$1" kind rc=0 err detail
    err="$("$TOOL_MKTEMP")" || stop "probe_tempfile_failed path=$p"
    kind="$(LC_ALL=C "$TOOL_STAT" -c '%F' -- "$p" 2>"$err")" || rc=$?
    if [ "$rc" -eq 0 ]; then
        "$TOOL_RM" -f "$err"
        case "$kind" in
            "symbolic link")                     printf 'link\n';    return 0 ;;
            "regular file"|"regular empty file") printf 'regular\n'; return 0 ;;
            "directory")                         printf 'dir\n';     return 0 ;;
            *)                                   printf 'other\n';   return 0 ;;
        esac
    fi
    detail="$("$TOOL_TR" -d '\r\n' <"$err")"; "$TOOL_RM" -f "$err"
    case "$detail" in
        *"No such file or directory"*) printf 'absent\n'; return 0 ;;
    esac
    stop "path_probe_error path=$p rc=$rc detail=$detail"
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
OWN="$(LC_ALL=C "$TOOL_STAT" -c '%U:%G' -- "$EV_DIR")" || stop "owner_probe_failed path=$EV_DIR"
MODE="$(LC_ALL=C "$TOOL_STAT" -c '%a' -- "$EV_DIR")"   || stop "mode_probe_failed path=$EV_DIR"
[ "$OWN"  = "$EXPECT_OWNER" ] || fail "evidence_dir_owner=$OWN expected=$EXPECT_OWNER"
[ "$MODE" = "$EXPECT_MODE"  ] || fail "evidence_dir_mode=$MODE expected=$EXPECT_MODE"
note "evidence_dir_ok path=$EV_DIR owner=$OWN mode=$MODE"

# --- the tree may contain ordinary directories and regular files only --------
# A symlink inside the tree would make the digest set attest to bytes that live
# somewhere else, which is exactly what the binding exists to prevent.
ODD="$(LC_ALL=C "$TOOL_FIND" "$EV_DIR" -mindepth 1 '!' -type d '!' -type f -print)" \
    || stop "evidence_tree_walk_failed path=$EV_DIR"
[ -z "$ODD" ] || fail "evidence_tree_non_regular_entries=[$ODD]"

# --- collect the file list, no pipeline -------------------------------------
# RP0 pipeline discipline: where a pipeline can be avoided it is avoided. `find`
# writes a NUL-delimited list to a temp file OUTSIDE the evidence tree, `sort`
# reads and rewrites that file in place with -o, and the sorted records are read
# into an array. Nothing is written into EV_DIR at any point.
WORK="$("$TOOL_MKTEMP" -d)" || stop "workdir_failed"
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
