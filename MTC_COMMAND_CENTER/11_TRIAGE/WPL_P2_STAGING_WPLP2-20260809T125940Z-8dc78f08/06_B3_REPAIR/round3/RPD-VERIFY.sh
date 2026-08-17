# ===== BLOCK-ID: RPD-VERIFY ===== [EXECUTABLE PROPOSAL BLOCK]
# WP-L Phase 2 - root-side deploy-time admission verify (PROPOSED DESIGN, NEW in
# the B3-GAP-ENV repair, Option 1, ROUND 3: audit 2 findings A2-F1, A2-F2, A2-F4
# and A2-F5 applied on top of round 2). NOT host-authorized.
# DESIGN ONLY IN THIS UNIT: no execution path exists for this block tonight. It
# enters the runkit as a frozen, NON-EXECUTED block exactly like RP3/RP5, and it
# is intended to run as root at install/deploy time through the deploy channel.
# Candidate: 2ce41e34bceb599d80af24c5c33d835820ec321b (identifier arrives as an
# input, see below; it is never derived on the host).
#
# It carries the two admissions an unprivileged operator cannot evaluate on this
# host (03_TRANSPORT/B3_STOP_ADJUDICATION.md): the env file's mode/owner, and the
# install manifest's mode/owner plus BOTH of its bindings.
#
# ROUND 3 CHANGES, each one an audit-2 REQUIRED item:
#   A2-F1 - the round-2 reader ran `python3` resolved from an operator-controlled
#           PATH, with the operator's environment and cwd inherited. A PYTHONPATH
#           or cwd holding `json.py` replaced `json.loads`, returned the two
#           expected values for a manifest that is not JSON at all, and executed
#           attacker code with this block's ROOT authority - which also refuted
#           the `mutation=none` claim. The interpreter is now PINNED to an
#           absolute path, required to exist, be executable and be root-owned and
#           not group/other writable, and is launched through `env -i` with an
#           explicit minimal child environment, in isolated mode (`-I -S -E`),
#           from a fixed safe cwd.
#   A2-F2 - the round-2 namespace check compared /proc/self/ns/* against
#           /proc/1/ns/*, i.e. against pid 1 AS VISIBLE HERE, and then printed
#           `bound=initial`. Inside a rootful container with an identity uid map
#           that comparison is satisfied without being on the host. Local
#           inference is replaced by DEPLOY-CHANNEL ATTESTATION: the expected host
#           user namespace, mount namespace and root-filesystem identity arrive as
#           preregistered inputs, and this block compares itself against them.
#           `bound=initial` is never printed again.
#   A2-F4 - `json.loads` accepts NaN, Infinity and -Infinity, which are not JSON
#           values, so a manifest carrying one was still adjudicated as valid
#           structural JSON. A `parse_constant` callback now raises.
#   A2-F5 - the mount reader let a matching FINAL record with no terminating
#           newline through unexamined, because `read` returns nonzero at EOF
#           even when it populated its variables. The reader now processes that
#           record, validates the field count of every record, and STOPs on
#           malformed, truncated or read-error input.
# Round 2's own repairs (structural JSON parse, duplicate-key rejection,
# top-level-exact comparison, parent canonicality, numeric ownership, no temp
# files, builtin sanitization, ERR trap, reasoned input STOPs) are carried
# forward unweakened.
#
# MUTATION SURFACE: NONE. This block creates no file, no directory and no
# temporary file, opens nothing for writing, and changes no mode, owner, ACL,
# group, service or network state. Round 2 could say that only of the SHELL: its
# unisolated interpreter could execute imported attacker code as root, so the
# claim did not hold for the process tree. With the pinned, isolated, env-scrubbed
# child of round 3 the claim covers the whole block again.
#
# RP0-LIB is NOT required by this block and is deliberately not sourced-checked:
#   - `rp0_probe_path` (RP0-LIB:29-55) allocates a temp file at RP0-LIB:31 and
#     sanitizes captured stderr with an UNADJUDICATED `tr` at RP0-LIB:39 and
#     RP0-LIB:49 - defects F4 and F6 of audit 1. `rpd_probe_kind` below is a
#     local, temp-free, fully adjudicated replacement emitting the same six
#     tokens.
#   - No other library helper was used, so this block is self-contained, which
#     also suits its runtime: the deploy channel executes it at a different time
#     and from a different context than the staging runkit, and a block that needs
#     nothing sourced cannot half-run because something was not.
#
# Read-only: `stat`, `readlink`, `id`, shell builtins, and one pinned `python3`
# reader that opens the install manifest read-only. No sudo, no group/ACL change,
# no service action, no network, no POST /api/arm, no broker/exchange/order/
# TESTNET/mainnet/economic action. No file content is printed and no credential
# value is read: the env file's METADATA is probed and the file itself is never
# opened; the manifest is read only by the parser, which can emit nothing but a
# fixed lowercase token from a closed set.
#
# rc contract: 0 = admitted, 1 = FAIL (deviant state), 3 = STOP (could not
# evaluate). A STOP is never re-read as a PASS. No raw tool status may escape as
# this block's exit code: every capture is adjudicated at its call site, and the
# ERR trap below converts anything still unadjudicated into a reasoned STOP with
# rc 3.
set -Eeuo pipefail
export LC_ALL=C
# `cd` prints the resolved directory when CDPATH is set, which would inject a
# path into the reader's captured stdout. The child launcher below does one `cd`.
unset CDPATH

RPD_KIND=""
RPD_SAFE=""

rpd_stop() { printf 'RPD_STOP reason=%s\n' "$*"; exit 3; }
rpd_fail() { printf 'RPD_FAIL reason=%s\n' "$*"; exit 1; }

# --- fail-closed backstop for unadjudicated statuses ------------------------
# `set -e` alone exits with the failing tool's own status: 1 (misreadable as a
# host-state FAIL), 126, or 127. This trap guarantees that every path out of the
# block is 0, 1 or 3 and that a non-zero exit always carries a reason string. It
# is a backstop, not the mechanism: every capture below is adjudicated
# explicitly, and this trap should be unreachable.
rpd_on_err() {
    local rc=$?
    printf 'RPD_STOP reason=unadjudicated_command_status rc=%s line=%s cmd=[%s]\n' \
        "$rc" "${BASH_LINENO[0]}" "$BASH_COMMAND"
    exit 3
}
trap 'rpd_on_err' ERR

# --- diagnostic sanitization, builtins only ---------------------------------
# No `tr`, no subshell, no external tool, therefore no tool status to adjudicate
# and nothing that can exit with a raw rc while composing a reason string. The
# classifiers below match on the SANITIZED text, so a diagnostic carrying a
# non-printable byte is suppressed to a fixed marker and lands in a STOP arm
# instead of being pattern-matched - fail-closed. The 400-byte cap bounds what a
# diagnostic can push into the evidence leaf; every path here is a short literal.
rpd_sanitize() {
    local s="${1-}"
    s="${s//$'\r'/ }"
    s="${s//$'\n'/ }"
    case "$s" in
        *[![:print:]]*) s="[non_printable_detail_suppressed]" ;;
    esac
    RPD_SAFE="${s:0:400}"
}

CONF_DIR="/etc/mtc-bridge"
ENV_FILE="/etc/mtc-bridge/mtc-bridge.env"
INSTALL_MANIFEST="/etc/mtc-bridge/install_manifest.json"
CONF_DIR_MODE="750"
ENV_FILE_MODE="600"
INSTALL_MANIFEST_MODE="640"
ROOT_OWNER="0:0"
MOUNTS="/proc/self/mounts"
ROOTFS="/"
# Bound on the manifest read. A root-side reader that will happily pull an
# arbitrary number of bytes into memory because a file was renamed onto that path
# is an availability defect, not a verification; over the bound is STOP.
MANIFEST_MAX_BYTES="4194304"

# --- A2-F1: the pinned child toolchain --------------------------------------
# Both are ABSOLUTE and are never resolved through PATH. Audit 2's minimal fix
# names the interpreter; `env` gets the same treatment because an `env` taken
# from an operator-controlled PATH would be the identical hole one level up - it
# is the program that builds the isolated environment.
# CHILD_PATH is what the child gets, and it is only there so that a PATH exists
# at all: nothing in the reader execs anything.
# CHILD_CWD is a directory the reader never reads from. It matters because a
# `python3 -c` inherits the caller's cwd as an import directory unless isolated;
# `-I` removes it from sys.path AND this `cd` removes it from the process, so
# neither mechanism alone is load-bearing.
PYTHON_BIN="/usr/bin/python3"
ENV_BIN="/usr/bin/env"
CHILD_PATH="/usr/bin:/bin"
CHILD_CWD="/"

# Preregistered, never derived here. Five required inputs now, in two families.
#
# FAMILY 1 - candidate identity (unchanged from round 2). The candidate release
# SHA and the accepted RELEASE_SHA256SUMS sha256 arrive from the operator's
# preregistration. Deriving either from the host would let the host attest to its
# own acceptance; PREREGISTRATION.md sec. 2 states the rule for the second value
# directly - a manifest cannot attest to its own acceptance - and it applies with
# equal force to the release SHA the manifest is tested against.
#
# FAMILY 2 - host attestation (NEW, A2-F2). RPD_EXPECT_NS_USER, RPD_EXPECT_NS_MNT
# and RPD_EXPECT_ROOTFS_ID are minted by the DEPLOY CHANNEL at provisioning time,
# on the host, before this block runs, as the exact `readlink /proc/<pid>/ns/user`
# and `.../ns/mnt` tokens of the host's initial namespaces and the exact
# `stat -c '%d:%i' /` identity of the host root filesystem. They exist because a
# process CANNOT establish from inside that the namespace it is in is the host's:
# every local witness (pid 1, uid_map, mount table) is namespace-local and can be
# reproduced by a rootful container. The value must come from outside the
# container boundary or the claim is unfalsifiable, which is exactly what audit 2
# refuted. See DESIGN_NOTES.md section 1 (A2-F2) for the provenance contract.
#
# A missing preregistered input is operator plumbing failure, not host deviation,
# so it is a reasoned STOP with rc 3. The accepted `:?` guard form is retained
# BEHIND the pre-checks: a bare `: "${VAR:?msg}"` aborts a non-interactive shell
# with rc 1, i.e. exactly the code this contract reserves for "the host state is
# deviant", and prints no RPD reason at all.
[ -n "${RPD_CANDIDATE_SHA:-}" ] \
    || rpd_stop "input_missing name=RPD_CANDIDATE_SHA detail=preregistered candidate release sha, 40 lowercase hex, never derived here"
[ -n "${RPD_RELEASE_MANIFEST_SHA256:-}" ] \
    || rpd_stop "input_missing name=RPD_RELEASE_MANIFEST_SHA256 detail=preregistered accepted RELEASE_SHA256SUMS sha256, 64 lowercase hex, never derived here"
[ -n "${RPD_EXPECT_NS_USER:-}" ] \
    || rpd_stop "input_missing name=RPD_EXPECT_NS_USER detail=deploy-channel attested host user namespace token, exact readlink form user:[<inode>], never derived here"
[ -n "${RPD_EXPECT_NS_MNT:-}" ] \
    || rpd_stop "input_missing name=RPD_EXPECT_NS_MNT detail=deploy-channel attested host mount namespace token, exact readlink form mnt:[<inode>], never derived here"
[ -n "${RPD_EXPECT_ROOTFS_ID:-}" ] \
    || rpd_stop "input_missing name=RPD_EXPECT_ROOTFS_ID detail=deploy-channel attested host root filesystem identity, exact stat -c %d:%i form, never derived here"
: "${RPD_CANDIDATE_SHA:?preregistered candidate release sha is required, 40 lowercase hex, never derived here}"
: "${RPD_RELEASE_MANIFEST_SHA256:?preregistered accepted RELEASE_SHA256SUMS sha256 is required, 64 lowercase hex, never derived here}"
: "${RPD_EXPECT_NS_USER:?deploy-channel attested host user namespace token is required, never derived here}"
: "${RPD_EXPECT_NS_MNT:?deploy-channel attested host mount namespace token is required, never derived here}"
: "${RPD_EXPECT_ROOTFS_ID:?deploy-channel attested host root filesystem identity is required, never derived here}"

# --- root precondition ------------------------------------------------------
# Every check in this block is exactly the set an unprivileged caller cannot
# evaluate on this host. Running unprivileged is therefore COULD NOT EVALUATE and
# it must never degrade into a silent skip or a partial pass: that degradation is
# what would let a deploy believe the env file had been admitted when nothing
# looked at it. Non-root is STOP.
# Identity is read NUMERICALLY: `id -un` needs a name-service lookup that can fail
# on a healthy host, and on hosts whose account names are not ASCII it would also
# put non-ASCII bytes into an evidence log that is required to be ASCII. uid 0 is
# the predicate; a name adds nothing and can be made to lie.
rpd_require_root() {
    local uid
    uid="$(id -u)"   || rpd_stop "uid_probe_failed"
    [ "$uid" = "0" ] || rpd_stop "must_run_as_root uid=$uid"
    printf 'RPD_identity uid=%s\n' "$uid"
}

# --- preregistered input format guards --------------------------------------
# Constraining the charset and the shape removes every quoting, line-break and
# injection surprise before a value is handed to anything, and it is the cheapest
# place to refuse an input that was never preregistered. Over-constraint is
# fail-closed: a value of a different shape STOPs and forces a new
# preregistration.
# A rejected value is NOT printed on any STOP arm - a mis-plumbed variable may
# hold something that must not reach an evidence log. It is printed only after it
# has been proven to have the preregistered shape.

# args: <variable name> <value> <expected length>
rpd_require_hex() {
    local name="$1" val="$2" want_len="$3"
    case "$val" in
        *[!0-9a-f]*) rpd_stop "input_charset name=$name expected=lowercase_hex" ;;
    esac
    [ "${#val}" = "$want_len" ] || rpd_stop "input_length name=$name len=${#val} expected=$want_len"
    printf 'RPD_input name=%s value=%s\n' "$name" "$val"
}

# args: <variable name> <value> <namespace kind: user|mnt>
# The attested token is compared to `readlink` output BYTE FOR BYTE later, so the
# guard requires exactly the kernel's rendering: `<kind>:[<decimal inode>]`.
rpd_require_ns_token() {
    local name="$1" val="$2" kind="$3" inner pfx
    # NOT folded into the `local` line above: bash expands every word of a
    # `local` command before it assigns any of them, so `pfx="$kind:["` there
    # would read `kind` while it is still unset and abort under `set -u` with no
    # reason string - the exact class of raw exit this block's rc contract bans.
    pfx="$kind:["
    case "$val" in
        "$pfx"*"]") : ;;
        *)          rpd_stop "input_shape name=$name expected=${kind}:[<decimal_inode>]" ;;
    esac
    inner="${val#"$pfx"}"
    inner="${inner%]}"
    [ -n "$inner" ] || rpd_stop "input_shape name=$name expected=${kind}:[<decimal_inode>] detail=empty_inode"
    case "$inner" in
        *[!0-9]*) rpd_stop "input_charset name=$name expected=decimal_inode" ;;
    esac
    printf 'RPD_input name=%s value=%s\n' "$name" "$val"
}

# args: <variable name> <value>
# `stat -c '%d:%i'` renders both fields in decimal, so the attested root-filesystem
# identity is two decimal fields separated by exactly one colon.
rpd_require_devino() {
    local name="$1" val="$2" dev ino
    case "$val" in
        *:*:*) rpd_stop "input_shape name=$name expected=<decimal_dev>:<decimal_inode>" ;;
        *:*)   dev="${val%%:*}"; ino="${val#*:}" ;;
        *)     rpd_stop "input_shape name=$name expected=<decimal_dev>:<decimal_inode>" ;;
    esac
    { [ -n "$dev" ] && [ -n "$ino" ]; } \
        || rpd_stop "input_shape name=$name expected=<decimal_dev>:<decimal_inode> detail=empty_field"
    case "$dev$ino" in
        *[!0-9]*) rpd_stop "input_charset name=$name expected=decimal_dev_and_inode" ;;
    esac
    printf 'RPD_input name=%s value=%s\n' "$name" "$val"
}

# --- A2-F2: host binding by deploy-channel attestation ----------------------
# What round 2 did and why it was refuted: it required /proc/self/uid_map to be
# the initial-namespace identity map AND /proc/self/ns/{user,mnt} to equal
# /proc/1/ns/{user,mnt}. Inside a rootful container with its own pid namespace,
# pid 1 IS that container's init and the uid map IS `0 0 4294967295`, so both
# predicates hold while /etc/mtc-bridge is the container's filesystem and not the
# host object the admission names. A chroot in the same namespaces changes what
# the literal /etc resolves to without changing either link. No predicate
# evaluated from inside can close that: every local witness is namespace-local.
# What round 3 does: it compares self against values MINTED OUTSIDE, by the deploy
# channel, at provisioning time. Three independent comparisons, each a STOP with
# its own reason:
#   1. /proc/self/ns/user must equal RPD_EXPECT_NS_USER, byte for byte;
#   2. /proc/self/ns/mnt  must equal RPD_EXPECT_NS_MNT,  byte for byte;
#   3. `stat -c '%d:%i' /` must equal RPD_EXPECT_ROOTFS_ID - the namespace tokens
#      alone do not identify what `/` resolves to, and a chroot or a bind mount
#      over `/` is exactly the case they miss.
# The uid_map identity predicate is KEPT from round 2. It is no longer the load-
# bearing check, but it is a cheap independent refutation of the rootless case and
# removing it would be a weakening.
# The evidence line says `bound=attested` and names its source. `bound=initial`
# was a claim this block cannot make about itself and is not printed anywhere.
rpd_assert_attested_namespaces() {
    local a b c extra lines=0 self_u self_m rootfs
    { exec 9< /proc/self/uid_map; } 2>/dev/null || rpd_stop "uid_map_unreadable path=/proc/self/uid_map"
    while read -r a b c extra <&9; do
        lines=$(( lines + 1 ))
        [ "$lines" -eq 1 ] || rpd_stop "user_namespace_not_initial reason=multiple_uid_map_lines lines=$lines"
        { [ "$a" = "0" ] && [ "$b" = "0" ] && [ "$c" = "4294967295" ] && [ -z "${extra:-}" ]; } \
            || rpd_stop "user_namespace_not_initial reason=uid_map_not_identity map=[$a $b $c]"
    done
    exec 9<&-
    [ "$lines" -eq 1 ] || rpd_stop "user_namespace_not_initial reason=empty_uid_map lines=$lines"
    self_u="$(readlink -- /proc/self/ns/user 2>/dev/null)" || rpd_stop "namespace_unreadable ns=user path=/proc/self/ns/user"
    self_m="$(readlink -- /proc/self/ns/mnt  2>/dev/null)" || rpd_stop "namespace_unreadable ns=mnt path=/proc/self/ns/mnt"
    { [ -n "$self_u" ] && [ -n "$self_m" ]; } \
        || rpd_stop "namespace_identity_empty self=[$self_u $self_m]"
    case "$self_u$self_m" in
        *[![:print:]]*) rpd_stop "namespace_identity_unprintable" ;;
    esac
    [ "$self_u" = "$RPD_EXPECT_NS_USER" ] \
        || rpd_stop "namespace_not_attested ns=user self=$self_u attested=$RPD_EXPECT_NS_USER"
    [ "$self_m" = "$RPD_EXPECT_NS_MNT" ] \
        || rpd_stop "namespace_not_attested ns=mnt self=$self_m attested=$RPD_EXPECT_NS_MNT"
    rootfs="$(LC_ALL=C stat -c '%d:%i' -- "$ROOTFS")" || rpd_stop "rootfs_identity_unreadable path=$ROOTFS"
    case "$rootfs" in
        ""|*[!0-9:]*) rpd_stop "rootfs_identity_unparsable path=$ROOTFS detail=non_decimal_dev_inode" ;;
    esac
    [ "$rootfs" = "$RPD_EXPECT_ROOTFS_ID" ] \
        || rpd_stop "rootfs_not_attested path=$ROOTFS self=$rootfs attested=$RPD_EXPECT_ROOTFS_ID"
    printf 'RPD_namespace user=%s mnt=%s rootfs=%s bound=attested source=deploy_channel_preregistration uid_map=identity\n' \
        "$self_u" "$self_m" "$rootfs"
}

# --- local, temp-free path classification -----------------------------------
# Replaces `rp0_probe_path` (RP0-LIB:29-55) for this block: same six tokens, same
# "a probe error is NEVER absent, a dangling link is NEVER absent" rule, no temp
# file (RP0-LIB:31) and no unadjudicated `tr` (RP0-LIB:39, RP0-LIB:49). Sets
# RPD_KIND instead of printing it: a classifier that PRINTS its result must be
# called in `$( )`, and any STOP it raised inside that subshell would be captured
# into the caller's variable instead of reaching the evidence leaf.
# `2>&1` merges the streams deliberately and safely: GNU `stat` writes the kind to
# stdout on success and the diagnostic to stderr on failure, never both, and an
# rc-0 capture that does not match a known kind token is a STOP rather than a
# guess. `stat` is not given -L, so a symlink AT the path is classified, not
# followed.
rpd_probe_kind() {
    local p="$1" out rc=0 sub subrc=0 safe
    out="$(LC_ALL=C stat -c '%F' -- "$p" 2>&1)" || rc=$?
    rpd_sanitize "$out"; safe="$RPD_SAFE"
    if [ "$rc" -eq 0 ]; then
        case "$safe" in
            "symbolic link")
                sub="$(LC_ALL=C stat -L -c '%F' -- "$p" 2>&1)" || subrc=$?
                rpd_sanitize "$sub"
                if [ "$subrc" -eq 0 ]; then RPD_KIND="link_live"; return 0; fi
                case "$RPD_SAFE" in
                    *"No such file or directory"*) RPD_KIND="link_dangling"; return 0 ;;
                esac
                rpd_stop "link_target_probe_error path=$p rc=$subrc detail=$RPD_SAFE" ;;
            "regular file"|"regular empty file") RPD_KIND="regular"; return 0 ;;
            "directory")                         RPD_KIND="dir";     return 0 ;;
            "")                                  rpd_stop "path_probe_empty path=$p rc=0" ;;
            *)                                   RPD_KIND="other";   return 0 ;;
        esac
    fi
    case "$safe" in
        *"No such file or directory"*) RPD_KIND="absent"; return 0 ;;
    esac
    rpd_stop "path_probe_error path=$p rc=$rc detail=$safe"
}

# --- the configuration parent, before either leaf is touched ----------------
# Round 1 stat'ed both leaves without ever looking at the directory they live in.
# Make /etc/mtc-bridge a symlink to a decoy directory holding regular files with
# the requested modes and the requested strings and every round-1 check passed:
# the leaf `lstat` saw regular files because the intermediate symlink had already
# been followed. Three independent requirements, all before any leaf is probed:
#   1. the final component is a directory, not a symlink (rpd_probe_kind);
#   2. `readlink -f` returns the LITERAL path, which proves that no component of
#      it - not just the last - is a symlink;
#   3. its own mode is exactly 0750 and its ownership is numerically 0:0.
# The unprivileged block asserts the same three things, but it does so at a
# different time and in a different process, so this block does not rely on it;
# the audit's point that a cross-block admission is neither self-contained nor
# atomic is the reason these are duplicated rather than referenced.
rpd_assert_conf_dir() {
    local d="$1" canon mode own_num own_name safe
    rpd_probe_kind "$d"
    case "$RPD_KIND" in
        dir) : ;;
        absent)                  rpd_fail "conf_dir_missing path=$d" ;;
        link_live|link_dangling) rpd_fail "conf_dir_is_symlink kind=$RPD_KIND path=$d" ;;
        *)                       rpd_fail "conf_dir_kind=$RPD_KIND path=$d expected=dir" ;;
    esac
    canon="$(LC_ALL=C readlink -f -- "$d" 2>/dev/null)" || rpd_stop "canonicalization_failed path=$d"
    rpd_sanitize "$canon"; safe="$RPD_SAFE"
    [ "$canon" = "$d" ] || rpd_fail "conf_dir_not_literal_canonical path=$d canonical=$safe"
    mode="$(LC_ALL=C stat -c '%a' -- "$d")"        || rpd_stop "mode_probe_failed path=$d"
    own_num="$(LC_ALL=C stat -c '%u:%g' -- "$d")"  || rpd_stop "owner_probe_failed path=$d"
    own_name="$(LC_ALL=C stat -c '%U:%G' -- "$d")" || rpd_stop "owner_name_probe_failed path=$d"
    rpd_sanitize "$own_name"
    printf 'RPD_stat path=%s owner_numeric=%s owner_name=%s mode=%s\n' "$d" "$own_num" "$RPD_SAFE" "$mode"
    [ "$mode" = "$CONF_DIR_MODE" ]  || rpd_fail "path=$d mode=$mode expected=$CONF_DIR_MODE"
    [ "$own_num" = "$ROOT_OWNER" ]  || rpd_fail "path=$d owner_numeric=$own_num expected=$ROOT_OWNER"
    printf 'RPD_conf_dir_canonical path=%s\n' "$d"
}

# --- mount-boundary predicate, fail-closed (A2-F5) --------------------------
# Path canonicalization does not detect a filesystem mounted AT or UNDER the
# configuration directory: a tmpfs mounted over /etc/mtc-bridge can present 0750
# 0:0 and hold leaves with the requested modes and the requested bindings, so
# every predicate in this block would be true of an object the accepted state
# never described. The accepted state records no mount topology, so a mount at or
# under CONF_DIR is not rendered as a host FAIL: it is COULD NOT EVALUATE (rc 3),
# because what would be admitted is not identified. Fail-closed both ways: an
# unreadable /proc/self/mounts is also a STOP, never "no mounts found".
#
# A2-F5 - THE READ LOOP. Round 2 used `while read -r src tgt rest`, which drops a
# FINAL record that has no terminating newline: `read` fills its variables and
# THEN returns nonzero at EOF, so the loop body never runs for that record and the
# predicate printed "no mount boundary" for a table whose last line was exactly
# the mount it exists to find. Truncated proc reads and short reads produce that
# shape. Round 3:
#   - reads one record at a time and PROCESSES a populated record even when the
#     read returned nonzero;
#   - requires exactly the six fields of a mount record, so a short, empty or
#     over-long record is `mount_record_malformed` (STOP) rather than a silently
#     unmatched line;
#   - treats an unterminated final record as evidence that the source was
#     truncated or read short, which is COULD NOT EVALUATE for the whole table:
#     it is reported with the hit count it did observe, so an operator sees both
#     facts.
# Mount targets are octal-escaped by the kernel (\040 for space and so on); the
# literal ASCII prefix compared here contains no character that is escaped, and
# any escaped target under it still carries that prefix, so escaping cannot hide
# a target from this predicate.
# If the Lead later preregisters the mount topology, this predicate becomes a
# comparison against it instead of a rejection; that is a preregistration change,
# not a code relaxation, and is recorded in DESIGN_NOTES.md section 7.
rpd_assert_no_mount_at_or_under() {
    local d="$1" f1 f2 f3 f4 f5 f6 extra rrc records=0 hits=0 first="" truncated=0
    { exec 9< "$MOUNTS"; } 2>/dev/null || rpd_stop "mounts_unreadable path=$MOUNTS"
    while : ; do
        f1=""; f2=""; f3=""; f4=""; f5=""; f6=""; extra=""; rrc=0
        IFS=' ' read -r f1 f2 f3 f4 f5 f6 extra <&9 || rrc=$?
        if [ "$rrc" -ne 0 ]; then
            if [ -z "$f1$f2$f3$f4$f5$f6$extra" ]; then break; fi
            truncated=1
        fi
        records=$(( records + 1 ))
        if [ -z "$f1" ] || [ -z "$f2" ] || [ -z "$f3" ] || [ -z "$f4" ] \
           || [ -z "$f5" ] || [ -z "$f6" ] || [ -n "$extra" ]; then
            rpd_sanitize "$f1 $f2 $f3 $f4 $f5 $f6 $extra"
            exec 9<&-
            rpd_stop "mount_record_malformed path=$MOUNTS record=$records expected_fields=6 got=[$RPD_SAFE]"
        fi
        case "$f2" in
            "$d"|"$d"/*)
                hits=$(( hits + 1 ))
                [ -n "$first" ] || first="$f2" ;;
        esac
        [ "$truncated" -eq 0 ] || break
    done
    exec 9<&-
    rpd_sanitize "$first"
    if [ "$truncated" -ne 0 ]; then
        rpd_stop "mount_table_unterminated_final_record path=$MOUNTS records=$records hits=$hits first_target=$RPD_SAFE"
    fi
    if [ "$hits" -ne 0 ]; then
        rpd_stop "mount_boundary_at_or_under_conf_dir path=$d mounts=$hits first_target=$RPD_SAFE"
    fi
    printf 'RPD_conf_dir_no_mount_boundary path=%s source=%s records=%s\n' "$d" "$MOUNTS" "$records"
}

# --- exact mode + numeric owner on a REGULAR file, candidate strength -------
# Reproduces candidate common.sh assert_mode_owner (:80-93) with two deliberate
# tightenings: both paths here are files, so `dir` is NOT an accepted kind; and
# ownership is compared numerically against 0:0 (GNU `stat` with `%U:%G` prints
# whatever the name service maps the ids to, so an NSS database that renders a
# nonzero uid as `root` made round 1's comparison pass on files root does not
# own). The name is still PRINTED, because a mismatch between the numeric and the
# rendered form is exactly the evidence an adjudicator wants; it is sanitized
# first, since account names are not required to be ASCII.
rpd_assert_regular_mode_owner() {
    local p="$1" want_mode="${2#0}" mode own_num own_name
    rpd_probe_kind "$p"
    case "$RPD_KIND" in
        regular) : ;;
        absent)                  rpd_fail "missing path=$p" ;;
        dir)                     rpd_fail "expected a regular file kind=dir path=$p" ;;
        link_live|link_dangling) rpd_fail "canonical deployment path is a symlink kind=$RPD_KIND path=$p" ;;
        *)                       rpd_fail "unexpected object kind=$RPD_KIND path=$p" ;;
    esac
    mode="$(LC_ALL=C stat -c '%a' -- "$p")"        || rpd_stop "mode_probe_failed path=$p"
    own_num="$(LC_ALL=C stat -c '%u:%g' -- "$p")"  || rpd_stop "owner_probe_failed path=$p"
    own_name="$(LC_ALL=C stat -c '%U:%G' -- "$p")" || rpd_stop "owner_name_probe_failed path=$p"
    rpd_sanitize "$own_name"
    printf 'RPD_stat path=%s owner_numeric=%s owner_name=%s mode=%s\n' "$p" "$own_num" "$RPD_SAFE" "$mode"
    [ "$mode" = "$want_mode" ]     || rpd_fail "path=$p mode=$mode expected=$want_mode"
    [ "$own_num" = "$ROOT_OWNER" ] || rpd_fail "path=$p owner_numeric=$own_num expected=$ROOT_OWNER"
}

# --- A2-F1: the pinned child tool precondition ------------------------------
# args: <short name> <absolute path>
# A pin is only a pin if the pinned object is the one the design named. Four
# requirements, all STOP on failure because none of them is a statement about the
# ADMITTED host state - they are statements about whether this block can evaluate
# anything at all:
#   1. it exists at the ABSOLUTE path (never `command -v`, never PATH);
#   2. it is a regular file or a live symlink to one (distributions ship
#      /usr/bin/python3 as a symlink to the versioned binary, so refusing a
#      symlink here would refuse every stock host; the target is what gets
#      stat'ed, and /usr/bin itself being writable is out of scope for any check
#      this block could make - DESIGN_NOTES section 8);
#   3. it is executable by this caller;
#   4. its TARGET is owned 0:0 and is not group- or other-writable. A pinned path
#      that anyone can rewrite is not pinned; this is the cheapest predicate that
#      says so, and it is a metadata read like every other check here.
rpd_require_pinned_tool() {
    local name="$1" path="$2" mode own last prev
    rpd_probe_kind "$path"
    case "$RPD_KIND" in
        regular|link_live) : ;;
        absent) rpd_stop "manifest_tool_absent name=$name path=$path detail=pinned absolute interpreter toolchain is required and has no PATH fallback" ;;
        *)      rpd_stop "manifest_tool_kind name=$name path=$path kind=$RPD_KIND expected=regular_or_live_symlink" ;;
    esac
    [ -x "$path" ] || rpd_stop "manifest_tool_not_executable name=$name path=$path"
    own="$(LC_ALL=C stat -L -c '%u:%g' -- "$path")" || rpd_stop "manifest_tool_owner_probe_failed name=$name path=$path"
    mode="$(LC_ALL=C stat -L -c '%a' -- "$path")"   || rpd_stop "manifest_tool_mode_probe_failed name=$name path=$path"
    [ "$own" = "$ROOT_OWNER" ] \
        || rpd_stop "manifest_tool_not_root_owned name=$name path=$path owner_numeric=$own expected=$ROOT_OWNER"
    last="${mode: -1}"
    prev="${mode: -2:1}"
    case "$last" in
        2|3|6|7) rpd_stop "manifest_tool_other_writable name=$name path=$path mode=$mode" ;;
    esac
    case "$prev" in
        2|3|6|7) rpd_stop "manifest_tool_group_writable name=$name path=$path mode=$mode" ;;
    esac
    printf 'RPD_tool name=%s path=%s mode=%s owner_numeric=%s resolution=pinned_absolute\n' \
        "$name" "$path" "$mode" "$own"
}

# --- install-manifest binding: structural JSON, silent, three-outcome -------
# The accepted formulation was two `LC_ALL=C grep -qsF` fixed-string searches.
# Audit 1 refuted it with a valid manifest whose two TOP-LEVEL values are both
# wrong and whose accepted values appear only inside a nested `decoy` object:
# both greps returned 0. Duplicate top-level keys produce the same false pass
# when an accepted value precedes the effective later one, and a fixed-string
# search never establishes that the file is JSON at all. grep cannot prove the
# stated binding, so the check is a structural verification:
#   - the WHOLE file is parsed, so trailing garbage after a valid document is a
#     parse failure rather than an unread tail;
#   - `object_pairs_hook` rejects a duplicate key at any depth, so an ambiguous
#     manifest can never be adjudicated as bound;
#   - `parse_constant` REJECTS NaN, Infinity and -Infinity (A2-F4). Python's
#     json module accepts those three by default even though they are not JSON
#     values, so round 2 called a file containing one "valid structural JSON";
#   - the top level must be a single JSON object;
#   - each expected value is compared exactly, as a STRING, against the
#     TOP-LEVEL key of that name - a nested occurrence is not reachable.
#
# A2-F1 - HOW THE CHILD IS LAUNCHED, and why each piece is load-bearing:
#   `rpd_require_pinned_tool`  the interpreter and `env` exist at absolute paths,
#                              are executable, root-owned and not group/other
#                              writable. Round 2 used `command -v python3`, so an
#                              operator PATH chose which binary ran as root.
#   `env -i`                   the child gets a NEW environment containing only
#                              the variables listed here. That is what removes
#                              PYTHONPATH, PYTHONHOME, PYTHONSTARTUP,
#                              PYTHONUSERBASE, PYTHONNOUSERSITE, LD_PRELOAD,
#                              LD_LIBRARY_PATH, LD_AUDIT and everything else
#                              unnamed - a deny-list would have to be complete to
#                              work, an allow-list does not.
#   `-I`                       isolated mode: ignores PYTHON* variables, drops
#                              the user site directory, and removes the cwd from
#                              sys.path. `-S` additionally skips `site`, so no
#                              .pth file executes at startup. `-E` is implied by
#                              `-I` and is spelled out so the intent survives an
#                              edit that touches one flag.
#   `cd "$CHILD_CWD"`          the process cwd is a directory the reader never
#                              reads from, so the cwd-shadow variant of the same
#                              attack has nothing to shadow WITH even if a future
#                              edit loses `-I`. Two independent mechanisms, by
#                              design, because this one is a root child.
# The `cd` runs in the command-substitution subshell only; the block's own cwd is
# unchanged. If it were ever to fail, the subshell yields no token and the
# unadjudicable STOP below fires - fail-closed.
#
# rc mapping, unchanged in spirit from the accepted three-outcome handling:
#   rc 1 = semantic mismatch: a value differs, is not a string, or the key is
#          absent at the top level. That is deviant state, not an evaluation
#          failure.
#   rc 3 = read, parse, structural-ambiguity or tool failure, INCLUDING the
#          pinned interpreter being absent. Nothing here silently degrades to a
#          weaker check: there is no grep fallback and no PATH fallback, because
#          a fallback is what audit 1 refuted.
# NOTHING FROM THE MANIFEST CAN REACH THE EVIDENCE LOG. The reader writes only
# one token from a closed lowercase set and never echoes a value, its stderr is
# discarded so that not even a parser diagnostic (which can carry a line and
# column) is logged, and the shell additionally refuses to print any token that
# is not pure [a-z0-9_] before it appears in a STOP reason.
# The reader also binds the metadata admission to the bytes it actually reads:
# it opens with O_NOFOLLOW (a symlink swapped onto the path after the stat above
# is refused) and O_NONBLOCK (a fifo swapped onto the path cannot hang a
# deploy-time verifier), then fstats the OPEN DESCRIPTOR and requires the same
# kind, mode and numeric ownership this block just admitted. Without that, the
# window between the `stat` above and the read is a swap window.
rpd_assert_manifest_binding() {
    local manifest="$1" release_sha="$2" manifest_sha="$3" want_mode="${4#0}" out rc=0 token
    rpd_require_pinned_tool env     "$ENV_BIN"
    rpd_require_pinned_tool python3 "$PYTHON_BIN"
    out="$(cd -- "$CHILD_CWD" >/dev/null && "$ENV_BIN" -i \
           PATH="$CHILD_PATH" \
           LC_ALL=C \
           RPD_MF="$manifest" \
           RPD_WANT_RELEASE="$release_sha" \
           RPD_WANT_MANIFEST="$manifest_sha" \
           RPD_WANT_MODE="$want_mode" \
           RPD_WANT_UID="${ROOT_OWNER%%:*}" \
           RPD_WANT_GID="${ROOT_OWNER##*:}" \
           RPD_MAX_BYTES="$MANIFEST_MAX_BYTES" \
           "$PYTHON_BIN" -I -S -E -c '
import json, os, stat, sys

class Dup(Exception):
    pass

class BadConst(Exception):
    pass

def pairs(seq):
    d = {}
    for k, v in seq:
        if k in d:
            raise Dup()
        d[k] = v
    return d

def constant(_name):
    raise BadConst()

def out(tok, code):
    sys.stdout.write(tok + "\n")
    sys.exit(code)

path = os.environ["RPD_MF"]
want_mode = int(os.environ["RPD_WANT_MODE"], 8)
want_uid = int(os.environ["RPD_WANT_UID"])
want_gid = int(os.environ["RPD_WANT_GID"])
limit = int(os.environ["RPD_MAX_BYTES"])
try:
    fd = os.open(path, os.O_RDONLY | getattr(os, "O_NONBLOCK", 0) | getattr(os, "O_NOFOLLOW", 0))
except Exception:
    out("read_error", 3)
chunks = []
try:
    st = os.fstat(fd)
    if not stat.S_ISREG(st.st_mode):
        out("open_kind_not_regular", 3)
    if stat.S_IMODE(st.st_mode) != want_mode:
        out("open_mode_mismatch", 3)
    if st.st_uid != want_uid or st.st_gid != want_gid:
        out("open_owner_mismatch", 3)
    if st.st_size > limit:
        out("too_large", 3)
    total = 0
    while True:
        try:
            buf = os.read(fd, 65536)
        except Exception:
            out("read_error", 3)
        if not buf:
            break
        total = total + len(buf)
        if total > limit:
            out("too_large", 3)
        chunks.append(buf)
finally:
    try:
        os.close(fd)
    except Exception:
        pass
try:
    doc = json.loads(b"".join(chunks).decode("utf-8"), object_pairs_hook=pairs, parse_constant=constant)
except Dup:
    out("duplicate_key", 3)
except BadConst:
    out("non_json_constant", 3)
except Exception:
    out("parse_error", 3)
if not isinstance(doc, dict):
    out("top_level_not_object", 3)
for key, want in (("release_sha", os.environ["RPD_WANT_RELEASE"]), ("release_manifest_sha256", os.environ["RPD_WANT_MANIFEST"])):
    if key not in doc:
        out("absent_" + key, 1)
    got = doc[key]
    if not isinstance(got, str) or got != want:
        out("mismatch_" + key, 1)
out("bound", 0)
' 2>/dev/null)" || rc=$?
    token="$out"
    case "$token" in
        ""|*[!a-z0-9_]*) token="unexpected_reader_output" ;;
    esac
    case "$rc:$token" in
        0:bound)
            printf 'RPD_manifest_binding path=%s bound=both parser=python3_json_structural keys=top_level_exact isolation=pinned_env_i\n' "$manifest"
            return 0 ;;
        1:absent_release_sha)               rpd_fail "install manifest does not bind release_sha" ;;
        1:absent_release_manifest_sha256)   rpd_fail "install manifest does not bind release_manifest_sha256" ;;
        1:mismatch_release_sha)             rpd_fail "install manifest binds a different release_sha" ;;
        1:mismatch_release_manifest_sha256) rpd_fail "install manifest binds a different release_manifest_sha256" ;;
        3:read_error)                       rpd_stop "install_manifest_unreadable path=$manifest" ;;
        3:too_large)                        rpd_stop "install_manifest_oversize path=$manifest limit_bytes=$MANIFEST_MAX_BYTES" ;;
        3:open_kind_not_regular)            rpd_stop "install_manifest_kind_changed_between_stat_and_read path=$manifest" ;;
        3:open_mode_mismatch)               rpd_stop "install_manifest_mode_changed_between_stat_and_read path=$manifest" ;;
        3:open_owner_mismatch)              rpd_stop "install_manifest_owner_changed_between_stat_and_read path=$manifest" ;;
        3:duplicate_key)                    rpd_stop "install_manifest_ambiguous_duplicate_key path=$manifest" ;;
        3:non_json_constant)                rpd_stop "install_manifest_non_json_constant path=$manifest detail=NaN_Infinity_-Infinity_are_not_JSON_values" ;;
        3:top_level_not_object)             rpd_stop "install_manifest_not_single_top_level_object path=$manifest" ;;
        3:parse_error)                      rpd_stop "install_manifest_unparsable path=$manifest" ;;
    esac
    rpd_stop "manifest_parser_unadjudicable path=$manifest rc=$rc token=[$token]"
}

printf 'RPD_SECTION identity\n'
rpd_require_root

# Guarded BEFORE anything prints either value and BEFORE the attestation section
# consumes the three new inputs.
printf 'RPD_SECTION preregistered_inputs\n'
rpd_require_hex      RPD_CANDIDATE_SHA           "$RPD_CANDIDATE_SHA"           40
rpd_require_hex      RPD_RELEASE_MANIFEST_SHA256 "$RPD_RELEASE_MANIFEST_SHA256" 64
rpd_require_ns_token RPD_EXPECT_NS_USER          "$RPD_EXPECT_NS_USER"          user
rpd_require_ns_token RPD_EXPECT_NS_MNT           "$RPD_EXPECT_NS_MNT"           mnt
rpd_require_devino   RPD_EXPECT_ROOTFS_ID        "$RPD_EXPECT_ROOTFS_ID"

printf 'RPD_SECTION attestation\n'
rpd_assert_attested_namespaces

printf 'RPD_SECTION header candidate=%s\n' "$RPD_CANDIDATE_SHA"

# The parent is admitted BEFORE either leaf is touched.
printf 'RPD_SECTION conf_dir\n'
rpd_assert_conf_dir "$CONF_DIR"
rpd_assert_no_mount_at_or_under "$CONF_DIR"

# Metadata only. The env file is stat'ed and never opened: its mode and owner are
# the admission, its content is out of scope for every block in this unit.
printf 'RPD_SECTION conf_metadata\n'
rpd_assert_regular_mode_owner "$ENV_FILE"         "$ENV_FILE_MODE"
rpd_assert_regular_mode_owner "$INSTALL_MANIFEST" "$INSTALL_MANIFEST_MODE"

printf 'RPD_SECTION manifest_binding\n'
rpd_assert_manifest_binding "$INSTALL_MANIFEST" "$RPD_CANDIDATE_SHA" "$RPD_RELEASE_MANIFEST_SHA256" "$INSTALL_MANIFEST_MODE"

printf 'RPD_SECTION done\n'
printf 'RPD_claim scope=root_side_deploy_time host_binding=attested checks=conf_dir_identity,env_mode_owner,manifest_mode_owner,manifest_binding_structural mutation=none\n'
printf 'RPD PASS\n'
