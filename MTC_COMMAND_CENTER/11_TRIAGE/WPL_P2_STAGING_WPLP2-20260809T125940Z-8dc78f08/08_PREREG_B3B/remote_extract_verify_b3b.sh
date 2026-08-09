# WP-L Phase 2 Stage 2B - archive verification and extraction (PREREGISTERED).
# Delivered on ssh stdin to:
#   bash -s -- <REMOTE_ARCHIVE> <EXTRACT_DIR> <EXPECTED_ARCHIVE_SHA256>
# rc: 0 PASS, 1 FAIL, 3 STOP. Executes no block.
set -Eeuo pipefail

fail() { printf 'EXTRACT_FAIL reason=%s\n' "$*" >&2; exit 1; }
stop() { printf 'EXTRACT_STOP reason=%s\n' "$*" >&2; exit 3; }
note() { printf 'EXTRACT_NOTE %s\n' "$*"; }

[ "$#" -eq 3 ] || fail "usage remote_extract_verify_b3b.sh <archive> <extract_dir> <archive_sha256> argc=$#"
ARCHIVE="$1"
EXTRACT_DIR="$2"
EXPECT_ARCHIVE_SHA="$3"

EXPECT_ARCHIVE_BYTES='184320'
MEMBERS='RP0-LIB.sh
RP0-BOOTSTRAP.sh
RP1-B3.sh
RP3-C2A-POST.sh
RP3-C2B-POST.sh
RP4-C3.py
RP5-C4A.sh
RP5-C4B.sh
RP5-C4C.sh
RPD-VERIFY.sh'
HASHES='4a404d7b90d83aef47b3593757f86e3699b3bc2dd772f51df63ead4f10d9ab48  RP0-LIB.sh
e7d748f6b41c6156de4d5c5e2d93c2b08729b1f85377b132660424024815bb33  RP0-BOOTSTRAP.sh
6f3ea022b68d80a552c4ebcb771bbb2a707bdab46a383d605ffc5b88b884becc  RP1-B3.sh
e233d29b005964e84cd6cbc2af50deccd83bb281dac39696e47de1c8890b5a27  RP3-C2A-POST.sh
26a1010cd9380289c5b90c08845b2af6ec31074fc5145241978a714b930bb412  RP3-C2B-POST.sh
0520cc901e56a66fe61e0df9edc0ed33fa4b05c09d62ba8f7471ef9ff688e4a5  RP4-C3.py
a5b1b2e4d4e5227b3bb1f0ea31e9e547040231913445970efe1046f4eba9e0f2  RP5-C4A.sh
10c4b3231042101ed9049dbf57ec3123ce902e9b18136769728a1a2e92f4037e  RP5-C4B.sh
de7301f1deb752bcc63d818348c2fdc33372a6b7d7d4f377b62bdf27d313e3a8  RP5-C4C.sh
3b9e78e87cecdc10ab1a10d14e79dbff530968e4075277117743c88976fa813c  RPD-VERIFY.sh'

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

KIND="$(probe_path "$ARCHIVE")" || exit $?
[ "$KIND" = "regular" ] || fail "archive_kind=$KIND path=$ARCHIVE"
ARCHIVE_BYTES="$(LC_ALL=C stat -c '%s' -- "$ARCHIVE")" || stop "archive_size_probe_failed path=$ARCHIVE"
[ "$ARCHIVE_BYTES" = "$EXPECT_ARCHIVE_BYTES" ] || fail "archive_bytes=$ARCHIVE_BYTES expected=$EXPECT_ARCHIVE_BYTES path=$ARCHIVE"
SUM_OUT="$(LC_ALL=C sha256sum -- "$ARCHIVE")" || stop "archive_hash_failed path=$ARCHIVE"
ACTUAL_ARCHIVE_SHA="${SUM_OUT%% *}"
[ "$ACTUAL_ARCHIVE_SHA" = "$EXPECT_ARCHIVE_SHA" ] || fail "archive_sha256_mismatch actual=$ACTUAL_ARCHIVE_SHA expected=$EXPECT_ARCHIVE_SHA"
printf 'EXTRACT_archive path=%s bytes=%s sha256=%s\n' "$ARCHIVE" "$ARCHIVE_BYTES" "$ACTUAL_ARCHIVE_SHA"

TYPE_LIST="$(LC_ALL=C tar -tvf "$ARCHIVE")" || stop "tar_type_listing_failed path=$ARCHIVE"
NAME_LIST="$(LC_ALL=C tar -tf "$ARCHIVE")" || stop "tar_name_listing_failed path=$ARCHIVE"
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
[ "$TYPE_COUNT" -eq 10 ] || fail "tar_member_count=$TYPE_COUNT expected=10"

NAME_COUNT=0
while IFS= read -r name; do
    NAME_COUNT=$((NAME_COUNT + 1))
    case "$name" in
        /*) fail "tar_member_absolute name=[$name]" ;;
        ..|../*|*/..|*/../*) fail "tar_member_traversal name=[$name]" ;;
        */*) fail "tar_member_not_basename name=[$name]" ;;
        "") fail "tar_member_empty_name" ;;
    esac
done <<EOF
$NAME_LIST
EOF
[ "$NAME_COUNT" -eq 10 ] || fail "tar_name_count=$NAME_COUNT expected=10"
[ "$NAME_LIST" = "$MEMBERS" ] || fail "tar_member_set_or_order_differs_from_stage1b"
note "members_exact count=10 order=stage1b"

KIND="$(probe_path "$EXTRACT_DIR")" || exit $?
[ "$KIND" = "absent" ] || fail "extract_dir_already_present kind=$KIND path=$EXTRACT_DIR"
MK_OUT="$(mkdir -m 0700 -- "$EXTRACT_DIR" 2>&1)" || stop "extract_dir_mkdir_failed path=$EXTRACT_DIR detail=$MK_OUT"
CANON="$(readlink -f -- "$EXTRACT_DIR")" || stop "canonicalization_failed path=$EXTRACT_DIR"
[ "$CANON" = "$EXTRACT_DIR" ] || fail "extract_dir_not_canonical path=$EXTRACT_DIR canonical=$CANON"

TAR_OUT="$(LC_ALL=C tar -xf "$ARCHIVE" -C "$EXTRACT_DIR" 2>&1)" || stop "tar_extract_failed rc=$? detail=$TAR_OUT"
[ -z "$TAR_OUT" ] || stop "tar_extract_stderr detail=$TAR_OUT"
EXTRA="$(LC_ALL=C find "$EXTRACT_DIR" -mindepth 1 '!' -type f -print)" || stop "extract_tree_walk_failed path=$EXTRACT_DIR"
[ -z "$EXTRA" ] || fail "extract_tree_non_regular_entries=[$EXTRA]"
FILE_COUNT="$(LC_ALL=C find "$EXTRACT_DIR" -mindepth 1 -type f -print | LC_ALL=C wc -l)" || stop "extract_tree_count_failed path=$EXTRACT_DIR"
[ "$FILE_COUNT" -eq 10 ] || fail "extracted_file_count=$FILE_COUNT expected=10"

while IFS= read -r name; do
    chmod 0444 -- "$EXTRACT_DIR/$name" || stop "chmod_failed path=$EXTRACT_DIR/$name"
    MODE="$(LC_ALL=C stat -c '%a' -- "$EXTRACT_DIR/$name")" || stop "mode_probe_failed path=$EXTRACT_DIR/$name"
    [ "$MODE" = "444" ] || fail "extracted_mode=$MODE expected=444 path=$EXTRACT_DIR/$name"
done <<EOF
$MEMBERS
EOF

CHECK_RC=0
( cd -- "$EXTRACT_DIR" && LC_ALL=C sha256sum -c --strict - ) <<EOF || CHECK_RC=$?
$HASHES
EOF
[ "$CHECK_RC" -eq 0 ] || fail "block_hash_verification_failed rc=$CHECK_RC"
while IFS= read -r name; do
    SUM_OUT="$(LC_ALL=C sha256sum -- "$EXTRACT_DIR/$name")" || stop "block_hash_failed path=$EXTRACT_DIR/$name"
    printf 'EXTRACT_block name=%s sha256=%s\n' "$name" "${SUM_OUT%% *}"
done <<EOF
$MEMBERS
EOF
printf 'EXTRACT PASS archive=%s archive_sha256=%s dir=%s members=10 verified=10 executed=0\n' "$ARCHIVE" "$ACTUAL_ARCHIVE_SHA" "$EXTRACT_DIR"
