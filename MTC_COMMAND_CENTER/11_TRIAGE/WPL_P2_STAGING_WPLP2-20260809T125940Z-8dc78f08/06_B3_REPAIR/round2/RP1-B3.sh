# ===== BLOCK-ID: RP1-B3 ===== [EXECUTABLE PROPOSAL BLOCK]
# WP-L Phase 2 - B3 post-start permissions/ownership subcheck (PROPOSED DESIGN,
# B3-GAP-ENV design repair, Option 1, ROUND 2: audit 1 findings F3/F4/F5/F6 and
# rulings O1/O2/O3/O5 applied).
# Candidate: 2ce41e34bceb599d80af24c5c33d835820ec321b. NOT host-authorized.
# Read-only `stat`/`find`/`readlink` and shell builtins only. No file content is
# printed, no credential value is read, no POST /api/arm, no broker/exchange/
# order/TESTNET/mainnet/economic action. Requires RP0-LIB sourced.
#
# MUTATION SURFACE: NONE (F4, O3). This block creates no file, no directory and
# no temporary file, opens nothing for writing, and changes no mode, owner, ACL,
# group, service or network state. Round 1 could not honestly say that: its
# sweep and its boundary probe each allocated a `mktemp` file under TMPDIR, and
# every `rp0_probe_path` call allocated a third (RP0-LIB:31). All three call
# sites are gone; stderr is now captured into a shell variable instead.
#
# RP0-LIB helpers deliberately NOT used here, per the round 2 kickoff:
#   - `rp0_probe_path` (RP0-LIB:29-55) allocates a temp file at RP0-LIB:31 and
#     sanitizes captured stderr with an UNADJUDICATED `tr` at RP0-LIB:39 and
#     RP0-LIB:49. Those are exactly F4 and F6. `b3_probe_kind` below is a local,
#     temp-free, fully adjudicated replacement emitting the same six tokens
#     (absent regular dir link_live link_dangling other).
#   - The only RP0-LIB helper still called is `rp0_monotonic_ms`
#     (RP0-LIB:18-22): it reads /proc/uptime, allocates nothing, runs no `tr`.
#
# SCOPE REDUCTION (defect B3-GAP-ENV, adjudicated in
# 03_TRANSPORT/B3_STOP_ADJUDICATION.md). This block executes as the unprivileged
# login user of the recorded route. /etc/mtc-bridge is 0750 root:root and that
# user is neither root nor in group root, so the kernel denies the directory
# SEARCH: `stat` on ANY name under /etc/mtc-bridge returns EACCES before the name
# is resolved, and the install manifest cannot be read at all. The env-file
# mode/owner admission, the install-manifest mode/owner admission and the
# manifest-binding admission are not evaluable here; they moved, unweakened, into
# the NEW root-side deploy-time block RPD-VERIFY. What is added here instead is
# the one positive statement an unprivileged operator can honestly make about
# that directory: it is opaque to this caller.
#
# HOW A DENIAL IS CLASSIFIED (audit section 2; round 2 kickoff item 9). The PASS
# decision of the boundary section is taken from the kernel's own access(2)
# answer through the shell builtins `[ -x ]` and `[ -r ]` on CONF_DIR - a
# permission decision, not a string. The two per-name `stat` probes that
# corroborate it are still classified from the diagnostic TEXT, because GNU
# coreutils returns rc 1 for every `stat` error and exposes no errno to a shell
# caller. That residual is acceptable here only because: (a) LC_ALL=C is
# exported for the whole block AND pinned on every producer, so the message
# shape is the C-locale one; (b) an unrecognised message is a STOP, never a
# PASS; and (c) the PASS arm additionally requires the access(2) predicate to
# have DENIED search, so a manufactured "Permission denied" string on its own
# cannot manufacture a PASS. A block that had to classify the errno itself
# would need a non-shell reader; RPD-VERIFY takes that dependency (python3)
# because its binding check needs a parser anyway, this block does not, and
# adding one here would turn an interpreter-less host into a new B3 STOP.
#
# rc contract: 0 = admitted, 1 = FAIL (deviant host state), 3 = STOP (could not
# evaluate). No raw tool status may escape as this block's exit code (F6, O5):
# every capture is adjudicated at its call site, and the ERR trap below converts
# anything that is still unadjudicated into a reasoned STOP with rc 3.
set -Eeuo pipefail
export LC_ALL=C

B3_KIND=""
B3_SAFE=""

b3_stop() { printf 'B3_STOP reason=%s\n' "$*"; exit 3; }
b3_fail() { printf 'B3_FAIL reason=%s\n' "$*"; exit 1; }

# --- fail-closed backstop for unadjudicated statuses (F6, O5) ---------------
# `set -e` alone exits with the failing tool's own status: 1 (misreadable as a
# host-state FAIL), 126, or 127. This trap guarantees that every path out of the
# block is 0, 1 or 3 and that a non-zero exit always carries a reason string.
# It is a backstop, not the mechanism: every capture below is adjudicated
# explicitly, and this trap should be unreachable.
b3_on_err() {
    local rc=$?
    printf 'B3_STOP reason=unadjudicated_command_status rc=%s line=%s cmd=[%s]\n' \
        "$rc" "${BASH_LINENO[0]}" "$BASH_COMMAND"
    exit 3
}
trap 'b3_on_err' ERR

# --- diagnostic sanitization, builtins only (F6, O5) ------------------------
# Round 1 sanitized captured stderr with `tr -d '\r\n'` inside the argument of a
# STOP call. If `tr` was missing or failed, `set -e` exited with tr's own status
# and printed no reason at all - that was F6. This replacement uses parameter
# expansion only: no external tool, no subshell, no exit status to adjudicate.
# Order matters: the classifiers below match on the SANITIZED text, so a
# diagnostic carrying a non-printable byte is suppressed to a fixed marker and
# therefore lands in a STOP arm instead of being pattern-matched - fail-closed.
# The 400-byte cap bounds what a diagnostic can push into the evidence leaf; all
# probe paths in this block are short literals, so the C-locale errno phrase is
# always well inside it.
b3_sanitize() {
    local s="${1-}"
    s="${s//$'\r'/ }"
    s="${s//$'\n'/ }"
    case "$s" in
        *[![:print:]]*) s="[non_printable_detail_suppressed]" ;;
    esac
    B3_SAFE="${s:0:400}"
}

# --- preregistered inputs, reasoned STOP on absence (O2) --------------------
# B3_RELEASE_MANIFEST_SHA256 is deliberately NO LONGER required by this block. It
# was only ever an input to the manifest-binding check, which now lives in
# RPD-VERIFY as RPD_RELEASE_MANIFEST_SHA256. Requiring it here would let a run of
# this block look like it bound a value that nothing in it tests.
# O2: a missing or malformed operator input is COULD NOT EVALUATE, not deviant
# host state. Round 1 kept the accepted bare `: "${VAR:?}"` form, which aborts a
# non-interactive shell with rc 1 - the code this contract reserves for "the host
# is deviant" - and prints no B3 reason. The rc-3 pre-checks below classify it,
# and the accepted `:?` line is retained behind them so the guard still fails
# closed if a pre-check is ever edited out.
[ -n "${B3_SWEEP_BUDGET_S:-}" ] \
    || b3_stop "input_missing name=B3_SWEEP_BUDGET_S detail=preregistered per-tree sweep budget in seconds, positive integer, never derived here"
case "$B3_SWEEP_BUDGET_S" in
    *[!0-9]*) b3_stop "input_charset name=B3_SWEEP_BUDGET_S expected=decimal_digits" ;;
esac
[ "$B3_SWEEP_BUDGET_S" -gt 0 ] \
    || b3_stop "input_range name=B3_SWEEP_BUDGET_S value=$B3_SWEEP_BUDGET_S expected=positive_integer"
: "${B3_SWEEP_BUDGET_S:?preregistered per-tree sweep budget in seconds is required}"

CAND="2ce41e34bceb599d80af24c5c33d835820ec321b"
REL="/opt/mtc-bridge/releases/$CAND"
VENV="/opt/mtc-bridge/venvs/$CAND"
STATE_DIR="/var/lib/mtc-bridge"
LOG_DIR="/var/log/mtc-bridge"
CONF_DIR="/etc/mtc-bridge"
# BOUNDARY PROBE TARGETS ONLY, never opened. Both names are EXPECTED to be
# refused with EACCES. ENV_FILE is the preregistered env path (PREREGISTRATION.md
# sec. 8 #4); CONF_ABSENT_PROBE is a name the accepted design has no reason to
# create, and the pair is what makes the probe a falsification rather than an
# assertion (see b3_assert_conf_dir_opaque).
ENV_FILE="/etc/mtc-bridge/mtc-bridge.env"
CONF_ABSENT_PROBE="/etc/mtc-bridge/.b3-boundary-probe-absent-name"
# Recorded for the deferral log line only. This block never probes it.
DEFERRED_INSTALL_MANIFEST="/etc/mtc-bridge/install_manifest.json"
UNIT_FILE="/usr/local/lib/systemd/system/mtc-bridge-first-start.service"
MOUNTS="/proc/self/mounts"

# --- RP0-LIB precondition ---------------------------------------------------
# Sourcing RP0-LIB is a documented precondition of this block. Asserting it is
# what keeps the 0/1/3 rc contract honest: unsourced, the call would abort under
# `set -e` with rc 127. Only ONE predicate is still required - `rp0_probe_path`
# is no longer called (F4/O3), so its guard is gone with it.
command -v rp0_monotonic_ms >/dev/null 2>&1 || b3_stop "rp0_lib_not_sourced predicate=rp0_monotonic_ms"

# --- local, temp-free path classification (F4, O3) --------------------------
# Replaces `rp0_probe_path` (RP0-LIB:29-55) for this block: same six tokens,
# same "a probe error is NEVER absent, a dangling link is NEVER absent" rule, no
# temp file (RP0-LIB:31) and no unadjudicated `tr` (RP0-LIB:39, RP0-LIB:49).
# Sets B3_KIND instead of printing it: a classifier that PRINTS its result must
# be called in `$( )`, and any STOP it raised inside that subshell would be
# captured into the caller's variable instead of reaching the evidence leaf.
# `2>&1` merges the streams deliberately and safely: GNU `stat` writes the kind
# to stdout on success and the diagnostic to stderr on failure, never both, and
# an rc-0 capture that does not match a known kind token is a STOP rather than a
# guess. `stat` is not given -L, so a symlink AT the path is classified, not
# followed.
b3_probe_kind() {
    local p="$1" out rc=0 sub subrc=0 safe
    out="$(LC_ALL=C stat -c '%F' -- "$p" 2>&1)" || rc=$?
    b3_sanitize "$out"; safe="$B3_SAFE"
    if [ "$rc" -eq 0 ]; then
        case "$safe" in
            "symbolic link")
                sub="$(LC_ALL=C stat -L -c '%F' -- "$p" 2>&1)" || subrc=$?
                b3_sanitize "$sub"
                if [ "$subrc" -eq 0 ]; then B3_KIND="link_live"; return 0; fi
                case "$B3_SAFE" in
                    *"No such file or directory"*) B3_KIND="link_dangling"; return 0 ;;
                esac
                b3_stop "link_target_probe_error path=$p rc=$subrc detail=$B3_SAFE" ;;
            "regular file"|"regular empty file") B3_KIND="regular"; return 0 ;;
            "directory")                         B3_KIND="dir";     return 0 ;;
            "")                                  b3_stop "path_probe_empty path=$p rc=0" ;;
            *)                                   B3_KIND="other";   return 0 ;;
        esac
    fi
    case "$safe" in
        *"No such file or directory"*) B3_KIND="absent"; return 0 ;;
    esac
    b3_stop "path_probe_error path=$p rc=$rc detail=$safe"
}

# --- exact mode + owner, candidate strength --------------------------------
# Reproduces candidate common.sh assert_mode_owner (:80-93): exact octal mode and
# exact owner. There is no accepted alternative mode.
# F3: ownership is compared NUMERICALLY. GNU `stat -c '%U:%G'` renders whatever
# the name service maps the ids to, so an NSS database that maps a nonzero uid to
# the name `root` made round 1's `root:root` comparison pass on files that are
# not owned by uid 0. Every root-owned expectation in this block is therefore
# spelled `0:0` and compared against `%u:%g`.
# Residual, disclosed: STATE_DIR and LOG_DIR are owned by the service account
# `mtc-bridge`, whose numeric ids are host-assigned and are NOT preregistered, so
# those two comparisons remain name-based. They are hardened instead by refusing
# a service account that resolves to uid 0 or gid 0 - the exact substitution the
# numeric form would otherwise catch - and both forms are printed so the Lead can
# preregister the numeric ids in the next freeze cycle.
b3_assert_mode_owner() {
    local p="$1" want_mode="${2#0}" want_own="$3" mode own_num own_name safe_name
    b3_probe_kind "$p"
    case "$B3_KIND" in
        regular|dir) : ;;
        absent)                  b3_fail "missing path=$p" ;;
        link_live|link_dangling) b3_fail "canonical deployment path is a symlink kind=$B3_KIND path=$p" ;;
        *)                       b3_fail "unexpected object kind=$B3_KIND path=$p" ;;
    esac
    mode="$(LC_ALL=C stat -c '%a' -- "$p")"     || b3_stop "mode_probe_failed path=$p"
    own_num="$(LC_ALL=C stat -c '%u:%g' -- "$p")" || b3_stop "owner_probe_failed path=$p"
    own_name="$(LC_ALL=C stat -c '%U:%G' -- "$p")" || b3_stop "owner_name_probe_failed path=$p"
    b3_sanitize "$own_name"; safe_name="$B3_SAFE"
    printf 'B3_stat path=%s owner_numeric=%s owner_name=%s mode=%s\n' "$p" "$own_num" "$safe_name" "$mode"
    [ "$mode" = "$want_mode" ] || b3_fail "path=$p mode=$mode expected=$want_mode"
    case "$want_own" in
        *[!0-9:]*)
            [ "$safe_name" = "$want_own" ] || b3_fail "path=$p owner_name=$safe_name expected=$want_own"
            case "$own_num" in
                0:*|*:0) b3_fail "path=$p owner_numeric=$own_num expected=nonzero_service_account name=$safe_name" ;;
            esac ;;
        *)
            [ "$own_num" = "$want_own" ] || b3_fail "path=$p owner_numeric=$own_num expected=$want_own" ;;
    esac
}

# --- candidate any-write-bit sweep, budgeted, fail-closed ------------------
# Candidate common.sh:95-105 predicate, reproduced verbatim:
#     find "$root" ! -type l -perm /222 -print -quit
# `/222` matches ANY write bit (owner, group OR other). `-perm -0200` is
# owner-write-only and silently passes a 0020 or 0002 offender - that was F2 of
# the original audit series. Honest cost: `-quit` shortens only a FAILING sweep;
# a clean tree is a full walk. The operator preregisters B3_SWEEP_BUDGET_S;
# exceeding it is STOP.
# ROUND 2 (F4, O3, F6, O5): the predicate line is unchanged, but the accepted
# `mktemp` stderr file and the `tr` that read it are gone. Consequences, stated
# rather than hidden:
#   - on the STOP path stdout and stderr are merged into one `detail` field,
#     where round 1 had `detail=` and `partial=[]` separately. Diagnostic text
#     only; no predicate reads it.
#   - `-print -quit` emits at most one path, so an rc-0 capture that is neither
#     empty nor a path under `root` is now a STOP. Round 1 discarded rc-0 stderr
#     unread, which could only ever have been silence about an error.
b3_assert_no_writable_paths() {
    local root="$1" out rc=0 t0 t1 elapsed_s safe
    t0="$(rp0_monotonic_ms)" || b3_stop "monotonic_clock_unevaluable root=$root phase=start"
    out="$(find "$root" ! -type l -perm /222 -print -quit 2>&1)" || rc=$?
    t1="$(rp0_monotonic_ms)" || b3_stop "monotonic_clock_unevaluable root=$root phase=end"
    b3_sanitize "$out"; safe="$B3_SAFE"
    if [ "$rc" -ne 0 ]; then
        b3_stop "writable_inventory_failed root=$root rc=$rc detail=$safe"
    fi
    case "$t0:$t1" in
        *[!0-9:]*|:*|*:) b3_stop "monotonic_clock_unparsable root=$root t0=[$t0] t1=[$t1]" ;;
    esac
    elapsed_s=$(( (t1 - t0) / 1000 ))
    printf 'B3_sweep root=%s elapsed_s=%s budget_s=%s\n' "$root" "$elapsed_s" "$B3_SWEEP_BUDGET_S"
    [ "$elapsed_s" -le "$B3_SWEEP_BUDGET_S" ] \
        || b3_stop "sweep_budget_exceeded root=$root elapsed_s=$elapsed_s budget_s=$B3_SWEEP_BUDGET_S"
    if [ -n "$out" ]; then
        case "$out" in
            "$root"|"$root"/*) b3_fail "writable path inside immutable tree: $safe" ;;
            *)                 b3_stop "writable_inventory_unparsable root=$root rc=0 out=$safe" ;;
        esac
    fi
    printf 'B3_no_write_bit root=%s\n' "$root"
}

# --- caller identity: a denial claim is about a (path, caller) PAIR ---------
# "The directory refused entry" is an admission only if the caller is the
# accepted unprivileged route identity. Exactly two identities would make the
# boundary probe below succeed for reasons that say nothing about host state:
# uid 0, and membership in CONF_DIR's group. Both are STOP (could not evaluate as
# an unprivileged operator) - never a silent skip, and never a FAIL, because
# neither observation is evidence about the host. uid 0 is excluded here; the
# group exclusion is asserted next to the boundary probe, because it needs
# CONF_DIR's own gid.
# Identity is read NUMERICALLY (`id -u`, `id -G`) on purpose. `id -nG` fails
# (rc 1, "cannot find name for group ID <n>") whenever any supplementary gid has
# no name-service entry, which is a healthy-host condition on directory-backed
# hosts; classifying that as STOP would have added a brand-new could-not-evaluate
# arm to a path the accepted block completed. Numeric ids need no name service.
# Residual, disclosed: a POSIX ACL entry, a MAC policy or a file capability on
# the shell could also grant entry without appearing in this identity line. The
# FAIL arms below therefore report the OBSERVATION (entry was permitted) and name
# the accepted state it contradicts, leaving the cause to Lead adjudication
# instead of asserting one (ruling O4, accepted as-is).
b3_assert_unprivileged() {
    local uid gids
    uid="$(id -u)"  || b3_stop "uid_probe_failed"
    gids="$(id -G)" || b3_stop "group_probe_failed"
    [ "$uid" != "0" ] || b3_stop "must_run_unprivileged uid=$uid"
    printf 'B3_identity uid=%s gids=[%s]\n' "$uid" "$gids"
}

# --- namespace context of the claim (F3, unprivileged half) -----------------
# F3 scenario 2: inside a rootless user namespace, `id -u` and a file's rendered
# ownership are namespace-local, so an identity claim that does not name its
# namespace is not falsifiable. RPD-VERIFY binds itself to the initial
# namespaces and STOPs otherwise, because it runs as root and can read
# /proc/1/ns/*. This block CANNOT do that: reading /proc/1/ns/* requires
# PTRACE_MODE_READ on pid 1, which an unprivileged caller does not have, so a
# comparison here would STOP on every healthy host. What it does instead is
# RECORD its own namespace identities, so the B3 claim is explicitly a claim
# made inside those namespaces and a later reader can compare them with the
# deploy-time RPD_namespace line. Unreadable is STOP, not a silent omission.
b3_record_namespaces() {
    local nsu nsm
    nsu="$(readlink -- /proc/self/ns/user 2>/dev/null)" || b3_stop "namespace_unreadable ns=user path=/proc/self/ns/user"
    nsm="$(readlink -- /proc/self/ns/mnt  2>/dev/null)" || b3_stop "namespace_unreadable ns=mnt path=/proc/self/ns/mnt"
    { [ -n "$nsu" ] && [ -n "$nsm" ]; } || b3_stop "namespace_identity_empty user=[$nsu] mnt=[$nsm]"
    case "$nsu$nsm" in
        *[![:print:]]*) b3_stop "namespace_identity_unprintable" ;;
    esac
    printf 'B3_namespace user=%s mnt=%s scope=self_only note=initial_ns_comparison_needs_root\n' "$nsu" "$nsm"
}

# --- CONF_DIR must be the literal canonical path (F2, symmetry) -------------
# F2 was raised against the ROOT-side block, whose leaves could be reached
# through a symlinked configuration parent. The same reasoning applies to the
# object this block makes its boundary claim about: `stat` on a final-component
# symlink is rejected by b3_probe_kind, but an INTERMEDIATE symlink (say /etc ->
# elsewhere) is followed silently. Requiring `readlink -f` to return the literal
# path proves that no component of the path is a symlink, so the mode/owner
# admission and the denial below are about the object the accepted state names.
b3_assert_literal_canonical_dir() {
    local d="$1" canon safe
    b3_probe_kind "$d"
    [ "$B3_KIND" = "dir" ] || b3_fail "conf_dir_kind=$B3_KIND path=$d expected=dir"
    canon="$(LC_ALL=C readlink -f -- "$d" 2>/dev/null)" || b3_stop "canonicalization_failed path=$d"
    b3_sanitize "$canon"; safe="$B3_SAFE"
    [ "$canon" = "$d" ] || b3_fail "conf_dir_not_literal_canonical path=$d canonical=$safe"
    printf 'B3_conf_dir_canonical path=%s\n' "$d"
}

# --- CONF_DIR must not be a mount boundary (F2, symmetry) -------------------
# Path canonicalization does not detect a filesystem mounted AT or UNDER the
# directory: a tmpfs mounted over /etc/mtc-bridge can present 0750 0:0 and deny
# this caller exactly as the accepted object would, so the boundary claim would
# be true of an object the accepted state never described. The accepted state
# records no mount topology, so a mount target at or under CONF_DIR is not
# rendered as a host FAIL: it is COULD NOT EVALUATE (rc 3), because what the
# block would be admitting is not identified. Fail-closed both ways: an
# unreadable /proc/self/mounts is also a STOP, never "no mounts found".
# Mount targets are octal-escaped by the kernel (\040 for space and so on); the
# literal ASCII prefix compared here contains no character that is escaped, and
# any escaped target under it still carries that prefix, so escaping cannot hide
# a target from this predicate.
b3_assert_no_mount_at_or_under() {
    local d="$1" src tgt rest hits=0 first="" safe
    { exec 9< "$MOUNTS"; } 2>/dev/null || b3_stop "mounts_unreadable path=$MOUNTS"
    while IFS=' ' read -r src tgt rest <&9; do
        case "$tgt" in
            "$d"|"$d"/*)
                hits=$(( hits + 1 ))
                [ -n "$first" ] || first="$tgt" ;;
        esac
    done
    exec 9<&-
    if [ "$hits" -ne 0 ]; then
        b3_sanitize "$first"; safe="$B3_SAFE"
        b3_stop "mount_boundary_at_or_under_conf_dir path=$d mounts=$hits first_target=$safe"
    fi
    printf 'B3_conf_dir_no_mount_boundary path=%s source=%s\n' "$d" "$MOUNTS"
}

# --- caller must NOT be in CONF_DIR's group ---------------------------------
# The group that 0750 grants search to is taken from CONF_DIR ITSELF (`stat %g`),
# not from a literal in this block: comparing numeric gids assumes neither that
# the group is spelled `root` nor that `root` is gid 0. Whole-word match on the
# space-padded numeric list, so gid 0 does not match gid 10. CONF_DIR's own
# mode/owner are asserted separately by b3_assert_mode_owner; this predicate only
# establishes that the accepted 0750 grant does not reach this caller.
b3_assert_not_in_dir_group() {
    local d="$1" gid gids
    gid="$(LC_ALL=C stat -c '%g' -- "$d")" || b3_stop "dir_gid_probe_failed path=$d"
    gids="$(id -G)"                        || b3_stop "group_probe_failed"
    case " $gids " in
        *" $gid "*) b3_stop "caller_in_conf_dir_group path=$d gid=$gid caller_gids=[$gids]" ;;
    esac
    printf 'B3_not_in_conf_dir_group path=%s gid=%s\n' "$d" "$gid"
}

# --- the access(2) predicate: is search DENIED to this caller? --------------
# Round 2 kickoff item 9. `[ -x ]` and `[ -r ]` are shell builtins over
# access(2): the kernel answers the permission question itself, including POSIX
# ACLs, capabilities and LSM policy for THIS caller, and no diagnostic string is
# involved. Under the accepted state both must be false. Either being true is a
# FAIL, not a STOP: the directory is demonstrably more open to this caller than
# the accepted host state says, which is a host-state observation and not an
# inability to evaluate.
# HONEST LIMIT, unchanged from round 1 (ruling O4): this says nothing about WHO
# else may enter, and access(2) answers for the real uid/gid of this process
# only. It is a caller-specific statement and is logged as one.
b3_assert_conf_dir_search_denied() {
    local d="$1"
    if [ -x "$d" ]; then
        b3_fail "conf_dir_search_permitted path=$d mechanism=access_builtin_x expected=denied"
    fi
    if [ -r "$d" ]; then
        b3_fail "conf_dir_read_permitted path=$d mechanism=access_builtin_r expected=denied"
    fi
    printf 'B3_conf_dir_search_denied path=%s mechanism=access_builtin\n' "$d"
}

# --- unprivileged boundary probe: CONF_DIR must be OPAQUE to the caller -----
# Accepted host state: CONF_DIR is 0750 root:root (asserted separately, above)
# and the caller is neither root nor in group root (asserted above). Under that
# state the kernel denies the directory search, so `stat` on ANY name under
# CONF_DIR fails with EACCES BEFORE the name is resolved. Four outcomes,
# fail-closed:
#   stat rc == 0                 -> FAIL, conf_dir_entry_permitted
#   stat rc != 0, EACCES text    -> PASS arm, B3_conf_dir_opaque_to_operator
#   stat rc != 0, ENOENT text    -> FAIL, conf_dir_search_permitted_name_absent
#   any other error class        -> STOP, could not evaluate
# ROUND 2 (F5, O1): ENOENT is now a FAIL. Round 1 routed it to STOP on the
# kickoff's literal "any other error class is STOP". The audit is right: an
# ENOENT positively PROVES that the directory search succeeded, which is the same
# host-state contradiction a successful `stat` is, and it is not an inability to
# evaluate. STOP is now reserved for outcomes that do not establish whether entry
# was permitted. The reason string is unchanged, so an existing expectation table
# row still matches; only its class moved from STOP to FAIL.
# The PAIR of names passed by the caller is the falsification: EACCES is
# name-independent, so a name the design has no reason to create must be refused
# in exactly the same way. If entry were in fact permitted, the two names would
# diverge (success on one, ENOENT on the other) and both FAIL arms catch it.
# HONEST LIMIT: this probe proves nothing about the existence, the spelling or
# the mode of any file under CONF_DIR, and two names are not a proof over every
# name under a name-sensitive MAC policy (audit section 2, ruling O4). The
# sec. 8 #4 named risk (`bridge.env` vs `mtc-bridge.env`) stays UNRESOLVED until
# RPD-VERIFY runs as root.
# Nothing under CONF_DIR is ever opened, so no content can reach the evidence
# log: the only syscall attempted is a metadata probe expected to be refused.
b3_assert_conf_dir_opaque() {
    local p="$1" out rc=0 safe
    out="$(LC_ALL=C stat -c '%F|%a|%u:%g' -- "$p" 2>&1)" || rc=$?
    b3_sanitize "$out"; safe="$B3_SAFE"
    if [ "$rc" -eq 0 ]; then
        b3_fail "conf_dir_entry_permitted path=$p stat=[$safe] expected=EACCES"
    fi
    case "$safe" in
        *"Permission denied"*)
            printf 'B3_conf_dir_opaque_to_operator path=%s outcome=EACCES rc=%s mechanism=message_lc_all_c\n' "$p" "$rc"
            return 0 ;;
        *"No such file or directory"*)
            b3_fail "conf_dir_search_permitted_name_absent path=$p rc=$rc expected=EACCES" ;;
    esac
    b3_stop "boundary_probe_unclassified path=$p rc=$rc detail=$safe"
}

printf 'B3_SECTION header candidate=%s\n' "$CAND"
b3_assert_unprivileged
b3_record_namespaces

printf 'B3_SECTION release_tree\n'
b3_assert_mode_owner "$REL" 0555 0:0
b3_assert_no_writable_paths "$REL"

printf 'B3_SECTION venv_tree\n'
b3_assert_mode_owner "$VENV" 0555 0:0
b3_assert_no_writable_paths "$VENV"

printf 'B3_SECTION ancillary_paths\n'
b3_assert_mode_owner "$STATE_DIR"        0750 mtc-bridge:mtc-bridge
b3_assert_mode_owner "$LOG_DIR"          0750 mtc-bridge:mtc-bridge
# `stat` on /etc/mtc-bridge ITSELF needs only search on /etc, which this caller
# has; ENTERING /etc/mtc-bridge needs search on /etc/mtc-bridge, which this
# caller does not have. That asymmetry is precisely why the next line survives
# unprivileged while the accepted block's lines 109-110 could not.
b3_assert_mode_owner "$CONF_DIR"         0750 0:0
b3_assert_mode_owner "$UNIT_FILE"        0644 0:0

printf 'B3_SECTION conf_dir_boundary\n'
b3_assert_literal_canonical_dir "$CONF_DIR"
b3_assert_no_mount_at_or_under "$CONF_DIR"
b3_assert_not_in_dir_group "$CONF_DIR"
b3_assert_conf_dir_search_denied "$CONF_DIR"
b3_assert_conf_dir_opaque "$ENV_FILE"
b3_assert_conf_dir_opaque "$CONF_ABSENT_PROBE"

# The reduced claim is stated IN the evidence, so a later reader cannot re-read
# `B3 PASS` as the accepted block's wider claim. Silence about a moved check is
# how a scope reduction turns into an unnoticed coverage loss.
printf 'B3_SECTION deferred\n'
printf 'B3_deferred check=env_file_mode_owner path=%s to=RPD-VERIFY reason=conf_dir_not_searchable_unprivileged\n' "$ENV_FILE"
printf 'B3_deferred check=install_manifest_mode_owner path=%s to=RPD-VERIFY reason=conf_dir_not_searchable_unprivileged\n' "$DEFERRED_INSTALL_MANIFEST"
printf 'B3_deferred check=install_manifest_binding path=%s to=RPD-VERIFY reason=conf_dir_not_readable_unprivileged\n' "$DEFERRED_INSTALL_MANIFEST"

printf 'B3_SECTION done\n'
printf 'B3_claim scope=unprivileged_only deferred=3 conf_dir=opaque_to_operator mutation=none\n'
printf 'B3 PASS\n'
