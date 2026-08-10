# WP-L Phase 2 Stage 2 — remote base allocation (PREREGISTERED, create-once).
#
# Transport op 01. Delivered on ssh stdin to `bash -s -- <REMOTE_BASE>`.
#
# Creates exactly four directories and nothing else. It never deletes, never
# renames, never chmods an existing object, never uses `mkdir -p`, never
# touches a service, a unit, a credential, the network or the bridge. It runs
# BEFORE the runkit exists on the host, so it deliberately depends on nothing
# from the runkit: no proposal block is sourced or executed here.
#
# rc contract: 0 = allocated, 1 = FAIL (predicate refused), 3 = STOP (could not
# evaluate — never re-read as "absent" or as success).
set -Eeuo pipefail

EXPECT_PREFIX='/home/gatea/wpi_staging_'
EXPECT_OWNER='gatea:gatea'
EXPECT_MODE='700'

fail() { printf 'SETUP_FAIL reason=%s\n' "$*" >&2; exit 1; }
stop() { printf 'SETUP_STOP reason=%s\n' "$*" >&2; exit 3; }
note() { printf 'SETUP_NOTE %s\n' "$*"; }

[ "$#" -eq 1 ] || fail "usage remote_setup.sh <REMOTE_BASE> argc=$#"
BASE="$1"

# --- the base must be EXACTLY /home/gatea/wpl_p2_staging_<one safe component>.
# A separator, `.`, `..`, a leading `-` or any character outside
# [A-Za-z0-9._-] in the suffix would place the whole evidence tree somewhere
# other than the preregistered path while every later check still "passed".
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

# --- lstat-fail-closed path classification ---------------------------------
# `stat -c %F` does NOT dereference, so a DANGLING symlink is still classified
# as a symlink and is never conflated with "absent". A probe error is STOP, not
# "absent": creating on top of an unreadable path is exactly the failure this
# script exists to prevent. Called as `kind="$(probe_path "$p")" || exit $?`
# so a subshell STOP/FAIL propagates instead of being read as empty output.
probe_path() {
    local p="$1" kind rc=0 err detail
    err="$(mktemp)" || stop "probe_tempfile_failed path=$p"
    kind="$(LC_ALL=C stat -c '%F' -- "$p" 2>"$err")" || rc=$?
    if [ "$rc" -eq 0 ]; then
        rm -f "$err"
        case "$kind" in
            "symbolic link")                    printf 'link\n';    return 0 ;;
            "regular file"|"regular empty file") printf 'regular\n'; return 0 ;;
            "directory")                        printf 'dir\n';     return 0 ;;
            *)                                  printf 'other\n';   return 0 ;;
        esac
    fi
    detail="$(tr -d '\r\n' <"$err")"; rm -f "$err"
    case "$detail" in
        *"No such file or directory"*) printf 'absent\n'; return 0 ;;
    esac
    stop "path_probe_error path=$p rc=$rc detail=$detail"
}

# --- allocate one directory with a plain, non-recursive mkdir --------------
# `mkdir -m 0700` applies the mode explicitly, so a permissive umask cannot
# widen it. No `-p`: a missing intermediate must fail loudly, never be
# manufactured. Any non-zero rc is STOP.
allocate() {
    local p="$1" out rc=0
    out="$(mkdir -m 0700 -- "$p" 2>&1)" || rc=$?
    [ "$rc" -eq 0 ] || stop "mkdir_failed path=$p rc=$rc detail=$out"
    note "allocated path=$p"
}

# --- prove the created directory is canonical, non-link, gatea:gatea 0700 ---
assert_dir() {
    local p="$1" kind canon own mode
    kind="$(probe_path "$p")" || exit $?
    [ "$kind" = "dir" ] || fail "created_kind=$kind path=$p"
    canon="$(readlink -f -- "$p")" || stop "canonicalization_failed path=$p"
    [ "$canon" = "$p" ] || fail "path_not_canonical path=$p canonical=$canon"
    own="$(LC_ALL=C stat -c '%U:%G' -- "$p")" || stop "owner_probe_failed path=$p"
    mode="$(LC_ALL=C stat -c '%a' -- "$p")"   || stop "mode_probe_failed path=$p"
    [ "$own"  = "$EXPECT_OWNER" ] || fail "owner=$own expected=$EXPECT_OWNER path=$p"
    [ "$mode" = "$EXPECT_MODE"  ] || fail "mode=$mode expected=$EXPECT_MODE path=$p"
    note "dir_ok path=$p owner=$own mode=$mode"
}

EV_PARENT="$BASE/evidence"
EV_RUNKIT="$EV_PARENT/runkit"
REMOTE_KIT="$BASE/kit"

# --- the base must be ABSENT as an object AND as a link --------------------
# `absent` here is the classified outcome, not "the test errored".
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
