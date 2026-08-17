# ===== BLOCK-ID: RPD-VERIFY ===== [EXECUTABLE PROPOSAL BLOCK]
# WP-L Phase 2 - root-side deploy-time admission verify (PROPOSED DESIGN, NEW in
# the B3-GAP-ENV repair, Option 1, ROUND 2: audit 1 findings F1/F2/F3/F4/F6 and
# rulings O2/O3/O5 applied). NOT host-authorized.
# DESIGN ONLY IN THIS UNIT: no execution path exists for this block tonight. It
# enters the runkit as a frozen, NON-EXECUTED block exactly like RP3/RP5, and it
# is intended to run as root at install/deploy time through the deploy channel.
# Candidate: 2ce41e34bceb599d80af24c5c33d835820ec321b (identifier arrives as an
# input, see below; it is never derived on the host).
#
# It carries the two admissions an unprivileged operator cannot evaluate on this
# host (03_TRANSPORT/B3_STOP_ADJUDICATION.md): the env file's mode/owner, and the
# install manifest's mode/owner plus BOTH of its bindings. Those checks are moved
# here unweakened, and round 2 makes three of them STRONGER than the accepted
# block was, because audit 1 showed the accepted formulations did not support the
# admission claim:
#   F1 - the two `grep -qsF` binding tests admitted a manifest whose top-level
#        bindings were both wrong (values present only in a nested decoy object),
#        and admitted duplicate keys. They are replaced by a silent structural
#        JSON verification.
#   F2 - the configuration parent was never checked, so both leaves could be
#        reached through a symlinked /etc/mtc-bridge. It is now required to be
#        the literal canonical non-symlink directory, 0750, numerically 0:0, with
#        no mount target at or under it.
#   F3 - ownership was compared by NAME (`%U:%G`), which an NSS database can
#        render as `root:root` for a nonzero uid, and `id -u = 0` proves only
#        namespace-local root. Ownership is now numeric and execution is bound to
#        the initial user/mount namespaces, fail-closed.
#
# MUTATION SURFACE: NONE (F4, O3). This block creates no file, no directory and
# no temporary file, opens nothing for writing, and changes no mode, owner, ACL,
# group, service or network state. Round 1 could not honestly say that: every
# `rp0_probe_path` call allocated a `mktemp` file (RP0-LIB:31), and with
# TMPDIR=/etc/mtc-bridge a ROOT execution of this block would have created that
# file inside the very directory it verifies.
#
# RP0-LIB is NOT required by this block any more, and is deliberately not
# sourced-checked:
#   - `rp0_probe_path` (RP0-LIB:29-55) allocates a temp file at RP0-LIB:31 and
#     sanitizes captured stderr with an UNADJUDICATED `tr` at RP0-LIB:39 and
#     RP0-LIB:49 - defects F4 and F6. `rpd_probe_kind` below is a local,
#     temp-free, fully adjudicated replacement emitting the same six tokens.
#   - No other library helper was used, so this block is now self-contained,
#     which also suits its runtime: the deploy channel executes it at a different
#     time and from a different context than the staging runkit, and a block that
#     needs nothing sourced cannot half-run because something was not.
#
# Read-only: `stat`, `readlink`, `id`, `command -v`, shell builtins, and one
# `python3` reader that opens the install manifest read-only. No sudo, no
# group/ACL change, no service action, no network, no POST /api/arm, no
# broker/exchange/order/TESTNET/mainnet/economic action. No file content is
# printed and no credential value is read: the env file's METADATA is probed and
# the file itself is never opened; the manifest is read only by the parser, which
# can emit nothing but a fixed lowercase token from a closed set.
#
# rc contract: 0 = admitted, 1 = FAIL (deviant state), 3 = STOP (could not
# evaluate). A STOP is never re-read as a PASS. No raw tool status may escape as
# this block's exit code (F6, O5): every capture is adjudicated at its call site,
# and the ERR trap below converts anything still unadjudicated into a reasoned
# STOP with rc 3.
set -Eeuo pipefail
export LC_ALL=C

RPD_KIND=""
RPD_SAFE=""

rpd_stop() { printf 'RPD_STOP reason=%s\n' "$*"; exit 3; }
rpd_fail() { printf 'RPD_FAIL reason=%s\n' "$*"; exit 1; }

# --- fail-closed backstop for unadjudicated statuses (F6, O5) ---------------
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

# --- diagnostic sanitization, builtins only (F6, O5) ------------------------
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
# Bound on the manifest read. A root-side reader that will happily pull an
# arbitrary number of bytes into memory because a file was renamed onto that path
# is an availability defect, not a verification; over the bound is STOP.
MANIFEST_MAX_BYTES="4194304"

# Preregistered, never derived here. The candidate release SHA and the accepted
# RELEASE_SHA256SUMS sha256 arrive as required environment variables from the
# operator's preregistration. Deriving either from the host would let the host
# attest to its own acceptance; PREREGISTRATION.md sec. 2 states the rule for the
# second value directly - a manifest cannot attest to its own acceptance - and it
# applies with equal force to the release SHA the manifest is tested against.
#
# O2: a missing preregistered input is operator plumbing failure, not host
# deviation, so it is a reasoned STOP with rc 3. The accepted `:?` guard form is
# retained BEHIND the pre-checks: a bare `: "${VAR:?msg}"` aborts a
# non-interactive shell with rc 1, i.e. exactly the code this contract reserves
# for "the host state is deviant", and prints no RPD reason at all.
[ -n "${RPD_CANDIDATE_SHA:-}" ] \
    || rpd_stop "input_missing name=RPD_CANDIDATE_SHA detail=preregistered candidate release sha, 40 lowercase hex, never derived here"
[ -n "${RPD_RELEASE_MANIFEST_SHA256:-}" ] \
    || rpd_stop "input_missing name=RPD_RELEASE_MANIFEST_SHA256 detail=preregistered accepted RELEASE_SHA256SUMS sha256, 64 lowercase hex, never derived here"
: "${RPD_CANDIDATE_SHA:?preregistered candidate release sha is required, 40 lowercase hex, never derived here}"
: "${RPD_RELEASE_MANIFEST_SHA256:?preregistered accepted RELEASE_SHA256SUMS sha256 is required, 64 lowercase hex, never derived here}"

# --- root precondition ------------------------------------------------------
# Every check in this block is exactly the set an unprivileged caller cannot
# evaluate on this host. Running unprivileged is therefore COULD NOT EVALUATE and
# it must never degrade into a silent skip or a partial pass: that degradation is
# what would let a deploy believe the env file had been admitted when nothing
# looked at it. Non-root is STOP.
# Identity is read NUMERICALLY: `id -un` needs a name-service lookup that can fail
# on a healthy host, and on hosts whose account names are not ASCII it would also
# put non-ASCII bytes into an evidence log that is required to be ASCII. uid 0 is
# the predicate; a name adds nothing and can be made to lie (F3 scenario 1).
rpd_require_root() {
    local uid
    uid="$(id -u)"   || rpd_stop "uid_probe_failed"
    [ "$uid" = "0" ] || rpd_stop "must_run_as_root uid=$uid"
    printf 'RPD_identity uid=%s\n' "$uid"
}

# --- namespace binding, fail-closed (F3) ------------------------------------
# F3 scenario 2: a rootless user namespace maps host uid 1000 to namespace uid 0
# and can present operator-controlled files through its own mount namespace. `id
# -u` prints 0, those files render as `root:root`, and every metadata check in
# this block passes without any host-root authority behind it. Numeric ownership
# does not fix that on its own, because 0:0 is also namespace-local.
# Two predicates, both STOP-on-failure and STOP-on-mismatch, each with its own
# reason:
#   1. /proc/self/uid_map must be the initial-namespace identity map, exactly one
#      line `0 0 4294967295`. A rootless namespace cannot produce it: mapping the
#      whole uid space onto itself is what the initial user namespace IS.
#   2. /proc/self/ns/user and /proc/self/ns/mnt must be the same namespaces as
#      pid 1's, which is the check the audit named.
# DISCLOSED RESIDUAL: predicate 2 compares against pid 1 AS VISIBLE HERE. Inside
# a container with its own pid namespace, pid 1 is that container's init, so
# predicate 2 alone can be satisfied without being on the host; predicate 1 is
# what makes the rootless case fail, and a full binding still belongs in the
# deploy channel's attestation, exactly as the audit's minimal fix says.
rpd_assert_initial_namespaces() {
    local a b c extra lines=0 self_u self_m init_u init_m
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
    init_u="$(readlink -- /proc/1/ns/user 2>/dev/null)"    || rpd_stop "namespace_unreadable ns=user path=/proc/1/ns/user"
    init_m="$(readlink -- /proc/1/ns/mnt  2>/dev/null)"    || rpd_stop "namespace_unreadable ns=mnt path=/proc/1/ns/mnt"
    { [ -n "$self_u" ] && [ -n "$self_m" ] && [ -n "$init_u" ] && [ -n "$init_m" ]; } \
        || rpd_stop "namespace_identity_empty self=[$self_u $self_m] init=[$init_u $init_m]"
    case "$self_u$self_m$init_u$init_m" in
        *[![:print:]]*) rpd_stop "namespace_identity_unprintable" ;;
    esac
    [ "$self_u" = "$init_u" ] || rpd_stop "namespace_not_initial ns=user self=$self_u init=$init_u"
    [ "$self_m" = "$init_m" ] || rpd_stop "namespace_not_initial ns=mnt self=$self_m init=$init_m"
    printf 'RPD_namespace user=%s mnt=%s bound=initial uid_map=identity\n' "$self_u" "$self_m"
}

# --- preregistered input format guard ---------------------------------------
# args: <variable name> <value> <expected length>
# Constraining the charset to lowercase hex and the length to the preregistered
# width removes every quoting, line-break and injection surprise before the value
# is handed to anything. It mattered more in round 1, where the value became a
# `grep -F` pattern and a multi-line value silently turned each binding test into
# a match against an unrelated manifest line; the structural parser below does an
# exact string comparison instead, so a malformed value can no longer manufacture
# a match. The guard is kept anyway: it is the cheapest place to refuse an input
# that was never preregistered, and over-constraint is fail-closed - an
# identifier of a different width STOPs and forces a new preregistration.
# The value is NOT printed on either STOP arm - a mis-plumbed variable may hold
# something that must not reach an evidence log. It is printed only after it has
# been proven to be pure lowercase hex of the preregistered width.
rpd_require_hex() {
    local name="$1" val="$2" want_len="$3"
    case "$val" in
        *[!0-9a-f]*) rpd_stop "input_charset name=$name expected=lowercase_hex" ;;
    esac
    [ "${#val}" = "$want_len" ] || rpd_stop "input_length name=$name len=${#val} expected=$want_len"
    printf 'RPD_input name=%s value=%s\n' "$name" "$val"
}

# --- local, temp-free path classification (F4, O3) --------------------------
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

# --- the configuration parent, before either leaf is touched (F2) -----------
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

# --- mount-boundary predicate, fail-closed (F2) -----------------------------
# Path canonicalization does not detect a filesystem mounted AT or UNDER the
# configuration directory: a tmpfs mounted over /etc/mtc-bridge can present 0750
# 0:0 and hold leaves with the requested modes and the requested bindings, so
# every predicate in this block would be true of an object the accepted state
# never described. The accepted state records no mount topology, so a mount at or
# under CONF_DIR is not rendered as a host FAIL: it is COULD NOT EVALUATE (rc 3),
# because what would be admitted is not identified. Fail-closed both ways: an
# unreadable /proc/self/mounts is also a STOP, never "no mounts found".
# Mount targets are octal-escaped by the kernel (\040 for space and so on); the
# literal ASCII prefix compared here contains no character that is escaped, and
# any escaped target under it still carries that prefix, so escaping cannot hide
# a target from this predicate.
# If the Lead later preregisters the mount topology, this predicate becomes a
# comparison against it instead of a rejection; that is a preregistration change,
# not a code relaxation, and is recorded in DESIGN_NOTES.md section 6.
rpd_assert_no_mount_at_or_under() {
    local d="$1" src tgt rest hits=0 first=""
    { exec 9< "$MOUNTS"; } 2>/dev/null || rpd_stop "mounts_unreadable path=$MOUNTS"
    while IFS=' ' read -r src tgt rest <&9; do
        case "$tgt" in
            "$d"|"$d"/*)
                hits=$(( hits + 1 ))
                [ -n "$first" ] || first="$tgt" ;;
        esac
    done
    exec 9<&-
    if [ "$hits" -ne 0 ]; then
        rpd_sanitize "$first"
        rpd_stop "mount_boundary_at_or_under_conf_dir path=$d mounts=$hits first_target=$RPD_SAFE"
    fi
    printf 'RPD_conf_dir_no_mount_boundary path=%s source=%s\n' "$d" "$MOUNTS"
}

# --- exact mode + numeric owner on a REGULAR file, candidate strength -------
# Reproduces candidate common.sh assert_mode_owner (:80-93) with two deliberate
# tightenings: both paths here are files, so `dir` is NOT an accepted kind; and
# ownership is compared numerically against 0:0 (F3 scenario 1 - GNU `stat` with
# `%U:%G` prints whatever the name service maps the ids to, so an NSS database
# that renders a nonzero uid as `root` made round 1's comparison pass on files
# root does not own). The name is still PRINTED, because a mismatch between the
# numeric and the rendered form is exactly the evidence an adjudicator wants; it
# is sanitized first, since account names are not required to be ASCII.
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

# --- install-manifest binding: structural JSON, silent, three-outcome (F1) --
# The accepted formulation was two `LC_ALL=C grep -qsF` fixed-string searches.
# Audit 1 refuted it with a valid manifest whose two TOP-LEVEL values are both
# wrong and whose accepted values appear only inside a nested `decoy` object:
# both greps returned 0. Duplicate top-level keys produce the same false pass
# when an accepted value precedes the effective later one, and a fixed-string
# search never establishes that the file is JSON at all. grep cannot prove the
# stated binding, so the check is now a structural verification:
#   - the WHOLE file is parsed, so trailing garbage after a valid document is a
#     parse failure rather than an unread tail;
#   - `object_pairs_hook` rejects a duplicate key at any depth, so an ambiguous
#     manifest can never be adjudicated as bound;
#   - the top level must be a single JSON object;
#   - each expected value is compared exactly, as a STRING, against the
#     TOP-LEVEL key of that name - a nested occurrence is not reachable.
# rc mapping, unchanged in spirit from the accepted three-outcome handling:
#   rc 1 = semantic mismatch: a value differs, is not a string, or the key is
#          absent at the top level. That is deviant state, not an evaluation
#          failure.
#   rc 3 = read, parse, structural-ambiguity or tool failure, INCLUDING python3
#          being absent. Nothing here silently degrades to a weaker check: there
#          is no grep fallback, because the fallback is what F1 refuted.
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
    command -v python3 >/dev/null 2>&1 \
        || rpd_stop "manifest_parser_absent tool=python3 path=$manifest detail=structural JSON verification is required and has no weaker fallback"
    out="$(RPD_MF="$manifest" \
           RPD_WANT_RELEASE="$release_sha" \
           RPD_WANT_MANIFEST="$manifest_sha" \
           RPD_WANT_MODE="$want_mode" \
           RPD_WANT_UID="${ROOT_OWNER%%:*}" \
           RPD_WANT_GID="${ROOT_OWNER##*:}" \
           RPD_MAX_BYTES="$MANIFEST_MAX_BYTES" \
           python3 -c '
import json, os, stat, sys

class Dup(Exception):
    pass

def pairs(seq):
    d = {}
    for k, v in seq:
        if k in d:
            raise Dup()
        d[k] = v
    return d

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
    doc = json.loads(b"".join(chunks).decode("utf-8"), object_pairs_hook=pairs)
except Dup:
    out("duplicate_key", 3)
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
            printf 'RPD_manifest_binding path=%s bound=both parser=python3_json_structural keys=top_level_exact\n' "$manifest"
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
        3:top_level_not_object)             rpd_stop "install_manifest_not_single_top_level_object path=$manifest" ;;
        3:parse_error)                      rpd_stop "install_manifest_unparsable path=$manifest" ;;
    esac
    rpd_stop "manifest_parser_unadjudicable path=$manifest rc=$rc token=[$token]"
}

printf 'RPD_SECTION identity\n'
rpd_require_root
rpd_assert_initial_namespaces

# Guarded BEFORE anything prints either value.
printf 'RPD_SECTION preregistered_inputs\n'
rpd_require_hex RPD_CANDIDATE_SHA           "$RPD_CANDIDATE_SHA"           40
rpd_require_hex RPD_RELEASE_MANIFEST_SHA256 "$RPD_RELEASE_MANIFEST_SHA256" 64

printf 'RPD_SECTION header candidate=%s\n' "$RPD_CANDIDATE_SHA"

# F2: the parent is admitted BEFORE either leaf is touched.
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
printf 'RPD_claim scope=root_side_deploy_time checks=conf_dir_identity,env_mode_owner,manifest_mode_owner,manifest_binding_structural mutation=none\n'
printf 'RPD PASS\n'
