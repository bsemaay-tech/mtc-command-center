# WP-L Phase 2 Stage 2B - create-once remote allocation (PREREGISTERED).
# Delivered on ssh stdin to: bash -s -- <REMOTE_BASE>
# rc: 0 PASS, 1 FAIL, 3 STOP. Creates only the run's four directories.
set -Eeuo pipefail

EXPECT_PREFIX='/home/gatea/wpl_p2b_staging_'
EXPECT_OWNER='gatea:gatea'
EXPECT_MODE='700'

fail() { printf 'SETUP_FAIL reason=%s\n' "$*" >&2; exit 1; }
stop() { printf 'SETUP_STOP reason=%s\n' "$*" >&2; exit 3; }
note() { printf 'SETUP_NOTE %s\n' "$*"; }

[ "$#" -eq 1 ] || fail "usage remote_setup_b3b.sh <REMOTE_BASE> argc=$#"
BASE="$1"

case "$BASE" in
    "$EXPECT_PREFIX"*) SUFFIX="${BASE#"$EXPECT_PREFIX"}" ;;
    *) fail "base_prefix base=[$BASE] expected_prefix=[$EXPECT_PREFIX]" ;;
esac
case "$SUFFIX" in
    ""|"."|"..")       fail "base_component_reserved value=[$SUFFIX]" ;;
    -*)                fail "base_component_leading_dash value=[$SUFFIX]" ;;
    *[!A-Za-z0-9._-]*) fail "base_component_charset value=[$SUFFIX]" ;;
esac
note "base_component_ok value=$SUFFIX"

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

allocate() {
    local p="$1" out rc=0
    out="$(mkdir -m 0700 -- "$p" 2>&1)" || rc=$?
    [ "$rc" -eq 0 ] || stop "mkdir_failed path=$p rc=$rc detail=$out"
    note "allocated path=$p"
}

assert_dir() {
    local p="$1" kind canon own mode
    kind="$(probe_path "$p")" || exit $?
    [ "$kind" = "dir" ] || fail "created_kind=$kind path=$p"
    canon="$(readlink -f -- "$p")" || stop "canonicalization_failed path=$p"
    [ "$canon" = "$p" ] || fail "path_not_canonical path=$p canonical=$canon"
    own="$(LC_ALL=C stat -c '%U:%G' -- "$p")" || stop "owner_probe_failed path=$p"
    mode="$(LC_ALL=C stat -c '%a' -- "$p")" || stop "mode_probe_failed path=$p"
    [ "$own" = "$EXPECT_OWNER" ] || fail "owner=$own expected=$EXPECT_OWNER path=$p"
    [ "$mode" = "$EXPECT_MODE" ] || fail "mode=$mode expected=$EXPECT_MODE path=$p"
    note "dir_ok path=$p owner=$own mode=$mode"
}

EV_PARENT="$BASE/evidence"
EV_RUNKIT="$EV_PARENT/runkit"
REMOTE_KIT="$BASE/kit"

KIND="$(probe_path "$BASE")" || exit $?
[ "$KIND" = "absent" ] || fail "base_already_present kind=$KIND path=$BASE"
note "base_absent path=$BASE"

allocate "$BASE"
allocate "$EV_PARENT"
allocate "$EV_RUNKIT"
allocate "$REMOTE_KIT"
assert_dir "$BASE"
assert_dir "$EV_PARENT"
assert_dir "$EV_RUNKIT"
assert_dir "$REMOTE_KIT"

printf 'SETUP PASS base=%s evidence=%s runkit=%s kit=%s owner=%s mode=%s\n' \
    "$BASE" "$EV_PARENT" "$EV_RUNKIT" "$REMOTE_KIT" "$EXPECT_OWNER" "$EXPECT_MODE"
