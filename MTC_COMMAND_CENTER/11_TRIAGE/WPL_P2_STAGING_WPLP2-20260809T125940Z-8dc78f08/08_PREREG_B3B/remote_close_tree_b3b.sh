# WP-L Phase 2 Stage 2B - closed evidence-tree hashing (PREREGISTERED).
# Delivered on ssh stdin to: bash -s -- <EV_DIR> <RUNID>
# Read-only with respect to EV_DIR. rc: 0 PASS, 1 FAIL, 3 STOP.
set -Eeuo pipefail

EXPECT_OWNER='gatea:gatea'
EXPECT_MODE='700'
fail() { printf 'CLOSE_FAIL reason=%s\n' "$*" >&2; exit 1; }
stop() { printf 'CLOSE_STOP reason=%s\n' "$*" >&2; exit 3; }
note() { printf 'CLOSE_NOTE %s\n' "$*"; }

[ "$#" -eq 2 ] || fail "usage remote_close_tree_b3b.sh <EV_DIR> <RUNID> argc=$#"
EV_DIR="$1"
RUNID="$2"
case "$RUNID" in
    ""|"."|"..") fail "runid_reserved value=[$RUNID]" ;;
    -*) fail "runid_leading_dash value=[$RUNID]" ;;
    *[!A-Za-z0-9._-]*) fail "runid_charset value=[$RUNID]" ;;
esac
EV_BASE="${EV_DIR##*/}"
[ "$EV_BASE" = "$RUNID" ] || fail "evdir_basename=$EV_BASE runid=$RUNID"

probe_path() {
    local p="$1" kind rc=0 err detail
    err="$(mktemp)" || stop "probe_tempfile_failed path=$p"
    kind="$(LC_ALL=C stat -c '%F' -- "$p" 2>"$err")" || rc=$?
    if [ "$rc" -eq 0 ]; then
        rm -f "$err"
        case "$kind" in
            "symbolic link")                     printf 'link\n'; return 0 ;;
            "regular file"|"regular empty file") printf 'regular\n'; return 0 ;;
            "directory")                         printf 'dir\n'; return 0 ;;
            *)                                   printf 'other\n'; return 0 ;;
        esac
    fi
    detail="$(tr -d '\r\n' <"$err")"; rm -f "$err"
    case "$detail" in
        *"No such file or directory"*) printf 'absent\n'; return 0 ;;
    esac
    stop "path_probe_error path=$p rc=$rc detail=$detail"
}

KIND="$(probe_path "$EV_DIR")" || exit $?
case "$KIND" in
    dir) : ;;
    absent) fail "evidence_dir_absent path=$EV_DIR" ;;
    link) fail "evidence_dir_is_symlink path=$EV_DIR" ;;
    *) fail "evidence_dir_kind=$KIND path=$EV_DIR" ;;
esac
CANON="$(readlink -f -- "$EV_DIR")" || stop "canonicalization_failed path=$EV_DIR"
[ "$CANON" = "$EV_DIR" ] || fail "evidence_dir_not_canonical path=$EV_DIR canonical=$CANON"
OWN="$(LC_ALL=C stat -c '%U:%G' -- "$EV_DIR")" || stop "owner_probe_failed path=$EV_DIR"
MODE="$(LC_ALL=C stat -c '%a' -- "$EV_DIR")" || stop "mode_probe_failed path=$EV_DIR"
[ "$OWN" = "$EXPECT_OWNER" ] || fail "evidence_dir_owner=$OWN expected=$EXPECT_OWNER"
[ "$MODE" = "$EXPECT_MODE" ] || fail "evidence_dir_mode=$MODE expected=$EXPECT_MODE"
note "evidence_dir_ok path=$EV_DIR owner=$OWN mode=$MODE"

ODD="$(LC_ALL=C find "$EV_DIR" -mindepth 1 '!' -type d '!' -type f -print)" || stop "evidence_tree_walk_failed path=$EV_DIR"
[ -z "$ODD" ] || fail "evidence_tree_non_regular_entries=[$ODD]"
WORK="$(mktemp -d)" || stop "workdir_failed"
RAW="$WORK/raw.0"
SORTED="$WORK/sorted.0"
LC_ALL=C find "$EV_DIR" -type f -print0 >"$RAW" || stop "evidence_file_inventory_failed path=$EV_DIR"
LC_ALL=C sort -z "$RAW" -o "$SORTED" || stop "evidence_file_sort_failed path=$EV_DIR"
FILES=()
while IFS= read -r -d '' f; do FILES+=("$f"); done <"$SORTED"
COUNT="${#FILES[@]}"
[ "$COUNT" -gt 0 ] || fail "evidence_tree_has_no_regular_file path=$EV_DIR"

digest_pass() {
    local f rel out
    for f in "${FILES[@]}"; do
        out="$(LC_ALL=C sha256sum -- "$f")" || { stop "digest_failed path=$f"; }
        rel="${f#"$EV_DIR"/}"
        printf '%s  %s\n' "${out%% *}" "$rel"
    done
}
PASS1="$WORK/pass1.txt"
PASS2="$WORK/pass2.txt"
digest_pass >"$PASS1" || exit $?
digest_pass >"$PASS2" || exit $?
LC_ALL=C cmp -s "$PASS1" "$PASS2" || fail "evidence_tree_not_quiescent digest_set_changed_between_passes"

printf 'CLOSE_BINDING runid=%s dir=%s files=%s\n' "$RUNID" "$EV_DIR" "$COUNT"
printf 'CLOSE_DIGEST_BEGIN runid=%s\n' "$RUNID"
while IFS= read -r line; do printf 'CLOSE_DIGEST %s\n' "$line"; done <"$PASS1"
printf 'CLOSE_DIGEST_END runid=%s\n' "$RUNID"
printf 'CLOSE_SIZE_BEGIN runid=%s\n' "$RUNID"
for f in "${FILES[@]}"; do
    SZ="$(LC_ALL=C stat -c '%s' -- "$f")" || stop "size_probe_failed path=$f"
    printf 'CLOSE_SIZE %s %s\n' "${f#"$EV_DIR"/}" "$SZ"
done
printf 'CLOSE_SIZE_END runid=%s\n' "$RUNID"
SET_SUM="$(LC_ALL=C sha256sum -- "$PASS1")" || stop "digest_set_hash_failed"
printf 'CLOSE_DIGEST_SET_SHA256 runid=%s %s\n' "$RUNID" "${SET_SUM%% *}"
rm -rf -- "$WORK"
printf 'CLOSE PASS runid=%s dir=%s files=%s wrote_into_evidence_tree=0\n' "$RUNID" "$EV_DIR" "$COUNT"
