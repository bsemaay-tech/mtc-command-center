# ===== BLOCK-ID: RP1-B3 ===== [EXECUTABLE PROPOSAL BLOCK]
# WP-L Phase 2 - B3 post-start permissions/ownership subcheck (PROPOSED DESIGN,
# B3-GAP-ENV design repair, Option 1, ROUND 3: audit 2 findings A2-F3, A2-F5 and
# A2-F6 applied on top of round 2).
# Candidate: 2ce41e34bceb599d80af24c5c33d835820ec321b. NOT host-authorized.
# Read-only `stat`/`find`/`readlink` and shell builtins only. No file content is
# printed, no credential value is read, no POST /api/arm, no broker/exchange/
# order/TESTNET/mainnet/economic action. Requires RP0-LIB sourced.
#
# ROUND 3 CHANGES, each one an audit-2 REQUIRED item:
#   A2-F3 - STATE_DIR and LOG_DIR ownership was still compared by NAME against
#           `mtc-bridge:mtc-bridge`, with only uid/gid 0 refused numerically. An
#           NSS database that renders the WRONG nonzero numeric owner as that name
#           therefore passed. The numeric uid and gid of the service account are
#           now REQUIRED preregistered inputs (B3_SVC_UID, B3_SVC_GID) and every
#           ownership comparison in this block is numeric. Names are printed as
#           diagnostics and decide nothing.
#   A2-F5 - the mount-table reader dropped a FINAL record with no terminating
#           newline, because `read` populates its variables and THEN returns
#           nonzero at EOF. A matching mount on that last line was reported as
#           "no mount boundary". The reader now processes that record, validates
#           the field count of every record, and STOPs on malformed, truncated or
#           read-error input.
#   A2-F6 - the boundary classifier sanitized CR/LF to spaces BEFORE matching, so
#           a two-line diagnostic carrying `Permission denied` and `No such file
#           or directory` collapsed into one string whose first substring match
#           selected the PASS arm. Raw diagnostics containing CR or LF, or more
#           than one error class, are now rejected BEFORE sanitization, and the
#           surviving text must be exactly one recognised C-locale diagnostic
#           shape. Ambiguous is STOP rc 3.
# Round 2's own repairs (no temp files, builtin sanitization, ERR trap, reasoned
# input STOPs, ENOENT as FAIL, parent canonicality, access(2) denial predicate)
# are carried forward unweakened.
#
# MUTATION SURFACE: NONE. This block creates no file, no directory and no
# temporary file, opens nothing for writing, and changes no mode, owner, ACL,
# group, service or network state. Round 1 could not honestly say that: its
# sweep and its boundary probe each allocated a `mktemp` file under TMPDIR, and
# every `rp0_probe_path` call allocated a third (RP0-LIB:31). All three call
# sites are gone; stderr is captured into a shell variable instead.
#
# RP0-LIB helpers deliberately NOT used here:
#   - `rp0_probe_path` (RP0-LIB:29-55) allocates a temp file at RP0-LIB:31 and
#     sanitizes captured stderr with an UNADJUDICATED `tr` at RP0-LIB:39 and
#     RP0-LIB:49. Those are exactly F4 and F6 of audit 1. `b3_probe_kind` below
#     is a local, temp-free, fully adjudicated replacement emitting the same six
#     tokens (absent regular dir link_live link_dangling other).
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
# HOW A DENIAL IS CLASSIFIED (audit 1 section 2; A2-F6). The PASS decision of the
# boundary section is taken from the kernel's own access(2) answer through the
# shell builtins `[ -x ]` and `[ -r ]` on CONF_DIR - a permission decision, not a
# string. The two per-name `stat` probes that corroborate it are still classified
# from the diagnostic TEXT, because GNU coreutils returns rc 1 for every `stat`
# error and exposes no errno to a shell caller. That residual is acceptable here
# only because: (a) LC_ALL=C is exported for the whole block AND pinned on every
# producer, so the message shape is the C-locale one; (b) round 3 requires the
# WHOLE captured diagnostic to be exactly one recognised C-locale shape naming
# the probed path, rejects CR/LF and multi-class text before that comparison, and
# treats anything else as STOP - so a wrapper, a loader diagnostic or mixed
# producer output can no longer select an arm by substring; and (c) the PASS arm
# additionally requires the access(2) predicate to have DENIED search, so a
# manufactured "Permission denied" string on its own cannot manufacture a PASS.
# A block that had to classify the errno itself would need a non-shell reader;
# RPD-VERIFY takes that dependency (a pinned python3) because its binding check
# needs a parser anyway, this block does not, and adding one here would turn an
# interpreter-less host into a new B3 STOP.
#
# rc contract: 0 = admitted, 1 = FAIL (deviant host state), 3 = STOP (could not
# evaluate). No raw tool status may escape as this block's exit code: every
# capture is adjudicated at its call site, and the ERR trap below converts
# anything that is still unadjudicated into a reasoned STOP with rc 3.
set -Eeuo pipefail
export LC_ALL=C

B3_KIND=""
B3_SAFE=""
B3_COUNT=0
B3_SHAPE=""

b3_stop() { printf 'B3_STOP reason=%s\n' "$*"; exit 3; }
b3_fail() { printf 'B3_FAIL reason=%s\n' "$*"; exit 1; }

# --- fail-closed backstop for unadjudicated statuses ------------------------
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

# --- diagnostic sanitization, builtins only ---------------------------------
# Round 1 sanitized captured stderr with `tr -d '\r\n'` inside the argument of a
# STOP call. If `tr` was missing or failed, `set -e` exited with tr's own status
# and printed no reason at all - that was F6. This replacement uses parameter
# expansion only: no external tool, no subshell, no exit status to adjudicate.
# It is an OUTPUT filter: it bounds and de-fangs what a diagnostic can push into
# the evidence leaf. It is NOT a classifier input any more - A2-F6 showed that
# folding CR/LF into spaces before matching is what let a two-line diagnostic
# select an arm by substring. The boundary classifier now inspects the RAW text
# first and only sanitizes for printing.
b3_sanitize() {
    local s="${1-}"
    s="${s//$'\r'/ }"
    s="${s//$'\n'/ }"
    case "$s" in
        *[![:print:]]*) s="[non_printable_detail_suppressed]" ;;
    esac
    B3_SAFE="${s:0:400}"
}

# --- literal substring counter, builtins only (A2-F6) -----------------------
# Sets B3_COUNT to the number of non-overlapping occurrences of a LITERAL needle.
# No `grep -c`, no pipeline, no subshell: nothing here has an exit status that
# could escape while an ambiguity is being adjudicated. The needle is always a
# block literal, never captured text, so the empty-needle non-termination case is
# unreachable by construction.
b3_count_substr() {
    local needle="$2" n=0 rest="$1"
    while [ "${rest#*"$needle"}" != "$rest" ]; do
        rest="${rest#*"$needle"}"
        n=$(( n + 1 ))
    done
    B3_COUNT="$n"
}

# --- preregistered inputs, reasoned STOP on absence -------------------------
# B3_RELEASE_MANIFEST_SHA256 is deliberately NOT required by this block. It was
# only ever an input to the manifest-binding check, which now lives in
# RPD-VERIFY as RPD_RELEASE_MANIFEST_SHA256. Requiring it here would let a run of
# this block look like it bound a value that nothing in it tests.
# A missing or malformed operator input is COULD NOT EVALUATE, not deviant host
# state. Round 1 kept the accepted bare `: "${VAR:?}"` form, which aborts a
# non-interactive shell with rc 1 - the code this contract reserves for "the host
# is deviant" - and prints no B3 reason. The rc-3 pre-checks below classify it,
# and the accepted `:?` line is retained behind them so the guard still fails
# closed if a pre-check is ever edited out.
#
# A2-F3, NEW REQUIRED INPUTS. B3_SVC_UID and B3_SVC_GID are the numeric uid and
# gid of the `mtc-bridge` service account, minted by the same provisioning step
# that creates the account and carried in preregistration exactly like every
# other value this block is not allowed to derive. They exist because the account
# NAME is not an identity: NSS renders whatever the directory or passwd database
# maps, so `mtc-bridge:mtc-bridge` can be the rendering of any uid:gid pair.
# Deriving them here (`id -u mtc-bridge`) would ask the same database the attack
# controls, so it is not done. Zero is refused as an input, not merely as an
# observation: the accepted state has no root-owned STATE_DIR or LOG_DIR, so a
# preregistration that says otherwise is a plumbing error.
[ -n "${B3_SWEEP_BUDGET_S:-}" ] \
    || b3_stop "input_missing name=B3_SWEEP_BUDGET_S detail=preregistered per-tree sweep budget in seconds, positive integer, never derived here"
case "$B3_SWEEP_BUDGET_S" in
    *[!0-9]*) b3_stop "input_charset name=B3_SWEEP_BUDGET_S expected=decimal_digits" ;;
esac
[ "$B3_SWEEP_BUDGET_S" -gt 0 ] \
    || b3_stop "input_range name=B3_SWEEP_BUDGET_S value=$B3_SWEEP_BUDGET_S expected=positive_integer"
: "${B3_SWEEP_BUDGET_S:?preregistered per-tree sweep budget in seconds is required}"

[ -n "${B3_SVC_UID:-}" ] \
    || b3_stop "input_missing name=B3_SVC_UID detail=preregistered numeric uid of the mtc-bridge service account, never derived here"
case "$B3_SVC_UID" in
    *[!0-9]*) b3_stop "input_charset name=B3_SVC_UID expected=decimal_digits" ;;
esac
[ "$B3_SVC_UID" -gt 0 ] \
    || b3_stop "input_range name=B3_SVC_UID value=$B3_SVC_UID expected=nonzero_service_account_uid"
: "${B3_SVC_UID:?preregistered numeric uid of the mtc-bridge service account is required}"

[ -n "${B3_SVC_GID:-}" ] \
    || b3_stop "input_missing name=B3_SVC_GID detail=preregistered numeric gid of the mtc-bridge service account, never derived here"
case "$B3_SVC_GID" in
    *[!0-9]*) b3_stop "input_charset name=B3_SVC_GID expected=decimal_digits" ;;
esac
[ "$B3_SVC_GID" -gt 0 ] \
    || b3_stop "input_range name=B3_SVC_GID value=$B3_SVC_GID expected=nonzero_service_account_gid"
: "${B3_SVC_GID:?preregistered numeric gid of the mtc-bridge service account is required}"

CAND="2ce41e34bceb599d80af24c5c33d835820ec321b"
REL="/opt/mtc-bridge/releases/$CAND"
VENV="/opt/mtc-bridge/venvs/$CAND"
STATE_DIR="/var/lib/mtc-bridge"
LOG_DIR="/var/log/mtc-bridge"
CONF_DIR="/etc/mtc-bridge"
ROOT_OWNER="0:0"
SVC_OWNER="$B3_SVC_UID:$B3_SVC_GID"
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
# `set -e` with rc 127. Only ONE predicate is required - `rp0_probe_path` is no
# longer called, so its guard is gone with it.
command -v rp0_monotonic_ms >/dev/null 2>&1 || b3_stop "rp0_lib_not_sourced predicate=rp0_monotonic_ms"

# --- local, temp-free path classification -----------------------------------
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

# --- exact mode + NUMERIC owner, candidate strength (A2-F3) ----------------
# Reproduces candidate common.sh assert_mode_owner (:80-93): exact octal mode and
# exact owner. There is no accepted alternative mode.
# EVERY ownership comparison in this block is now numeric, with no exceptions and
# no name branch. GNU `stat -c '%U:%G'` renders whatever the name service maps
# the ids to, so a name comparison is a comparison against the attacker's own
# database: audit 2 defeated the round-2 service-account branch with numeric
# 999:999 rendered as `mtc-bridge:mtc-bridge` while the preregistered account was
# a different nonzero pair. `%U:%G` is still READ and PRINTED because a
# divergence between the numeric and the rendered form is exactly the evidence an
# adjudicator wants for the NSS scenario, but nothing is decided on it.
# The expectation itself is shape-checked: a caller that passes anything other
# than `<digits>:<digits>` is a coding error in this block, and it STOPs rather
# than comparing against something unintended.
b3_assert_mode_owner() {
    local p="$1" want_mode="${2#0}" want_own="$3" mode own_num own_name safe_name
    case "$want_own" in
        *[!0-9:]*|*:*:*|:*|*:) b3_stop "owner_expectation_malformed path=$p expected=[$want_own] shape=<uid>:<gid>" ;;
        *:*) : ;;
        *)   b3_stop "owner_expectation_malformed path=$p expected=[$want_own] shape=<uid>:<gid>" ;;
    esac
    b3_probe_kind "$p"
    case "$B3_KIND" in
        regular|dir) : ;;
        absent)                  b3_fail "missing path=$p" ;;
        link_live|link_dangling) b3_fail "canonical deployment path is a symlink kind=$B3_KIND path=$p" ;;
        *)                       b3_fail "unexpected object kind=$B3_KIND path=$p" ;;
    esac
    mode="$(LC_ALL=C stat -c '%a' -- "$p")"        || b3_stop "mode_probe_failed path=$p"
    own_num="$(LC_ALL=C stat -c '%u:%g' -- "$p")"  || b3_stop "owner_probe_failed path=$p"
    own_name="$(LC_ALL=C stat -c '%U:%G' -- "$p")" || b3_stop "owner_name_probe_failed path=$p"
    b3_sanitize "$own_name"; safe_name="$B3_SAFE"
    printf 'B3_stat path=%s owner_numeric=%s owner_name=%s mode=%s\n' "$p" "$own_num" "$safe_name" "$mode"
    [ "$mode" = "$want_mode" ]     || b3_fail "path=$p mode=$mode expected=$want_mode"
    [ "$own_num" = "$want_own" ]   || b3_fail "path=$p owner_numeric=$own_num expected=$want_own owner_name=$safe_name"
}

# --- candidate any-write-bit sweep, budgeted, fail-closed ------------------
# Candidate common.sh:95-105 predicate, reproduced verbatim:
#     find "$root" ! -type l -perm /222 -print -quit
# `/222` matches ANY write bit (owner, group OR other). `-perm -0200` is
# owner-write-only and silently passes a 0020 or 0002 offender - that was F2 of
# the original audit series. Honest cost: `-quit` shortens only a FAILING sweep;
# a clean tree is a full walk. The operator preregisters B3_SWEEP_BUDGET_S;
# exceeding it is STOP.
# The accepted `mktemp` stderr file and the `tr` that read it are gone.
# Consequences, stated rather than hidden:
#   - on the STOP path stdout and stderr are merged into one `detail` field,
#     where round 1 had `detail=` and `partial=[]` separately. Diagnostic text
#     only; no predicate reads it.
#   - `-print -quit` emits at most one path, so an rc-0 capture that is neither
#     empty nor a path under `root` is a STOP. Round 1 discarded rc-0 stderr
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

# --- namespace context of the claim -----------------------------------------
# Inside a rootless user namespace, `id -u` and a file's rendered ownership are
# namespace-local, so an identity claim that does not name its namespace is not
# falsifiable. RPD-VERIFY binds itself to the host namespaces by comparing
# against DEPLOY-CHANNEL ATTESTED identities (audit 2's A2-F2 fix). This block
# cannot do that: no such attestation exists for the staging route, and an
# unprivileged caller cannot read /proc/1/ns/* anyway. What it does instead is
# RECORD its own namespace identities, so the B3 claim is explicitly a claim made
# inside those namespaces and a later reader can compare them with the
# deploy-time RPD_namespace line. Unreadable is STOP, not a silent omission.
# It is deliberately NOT an assertion: this block claims nothing about which
# namespace it is in, only which one it observed itself to be in.
b3_record_namespaces() {
    local nsu nsm
    nsu="$(readlink -- /proc/self/ns/user 2>/dev/null)" || b3_stop "namespace_unreadable ns=user path=/proc/self/ns/user"
    nsm="$(readlink -- /proc/self/ns/mnt  2>/dev/null)" || b3_stop "namespace_unreadable ns=mnt path=/proc/self/ns/mnt"
    { [ -n "$nsu" ] && [ -n "$nsm" ]; } || b3_stop "namespace_identity_empty user=[$nsu] mnt=[$nsm]"
    case "$nsu$nsm" in
        *[![:print:]]*) b3_stop "namespace_identity_unprintable" ;;
    esac
    printf 'B3_namespace user=%s mnt=%s scope=self_only note=host_binding_is_attested_only_in_RPD-VERIFY\n' "$nsu" "$nsm"
}

# --- CONF_DIR must be the literal canonical path ----------------------------
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

# --- CONF_DIR must not be a mount boundary (A2-F5) --------------------------
# Path canonicalization does not detect a filesystem mounted AT or UNDER the
# directory: a tmpfs mounted over /etc/mtc-bridge can present 0750 0:0 and deny
# this caller exactly as the accepted object would, so the boundary claim would
# be true of an object the accepted state never described. The accepted state
# records no mount topology, so a mount target at or under CONF_DIR is not
# rendered as a host FAIL: it is COULD NOT EVALUATE (rc 3), because what the
# block would be admitting is not identified. Fail-closed both ways: an
# unreadable /proc/self/mounts is also a STOP, never "no mounts found".
#
# A2-F5 - THE READ LOOP, repaired identically in both blocks. Round 2 used
# `while read -r src tgt rest`, which drops a FINAL record with no terminating
# newline: `read` fills its variables and THEN returns nonzero at EOF, so the
# loop body never ran for that record and a matching mount on the last line was
# reported as "no mount boundary". Truncated proc reads and short reads produce
# exactly that shape. Round 3 processes a populated record even when the read
# returned nonzero, requires exactly the six fields of a mount record, and treats
# an unterminated final record as evidence that the source was truncated - which
# is COULD NOT EVALUATE for the whole table, reported together with the hit count
# it did observe.
# Mount targets are octal-escaped by the kernel (\040 for space and so on); the
# literal ASCII prefix compared here contains no character that is escaped, and
# any escaped target under it still carries that prefix, so escaping cannot hide
# a target from this predicate.
b3_assert_no_mount_at_or_under() {
    local d="$1" f1 f2 f3 f4 f5 f6 extra rrc records=0 hits=0 first="" truncated=0
    { exec 9< "$MOUNTS"; } 2>/dev/null || b3_stop "mounts_unreadable path=$MOUNTS"
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
            b3_sanitize "$f1 $f2 $f3 $f4 $f5 $f6 $extra"
            exec 9<&-
            b3_stop "mount_record_malformed path=$MOUNTS record=$records expected_fields=6 got=[$B3_SAFE]"
        fi
        case "$f2" in
            "$d"|"$d"/*)
                hits=$(( hits + 1 ))
                [ -n "$first" ] || first="$f2" ;;
        esac
        [ "$truncated" -eq 0 ] || break
    done
    exec 9<&-
    b3_sanitize "$first"
    if [ "$truncated" -ne 0 ]; then
        b3_stop "mount_table_unterminated_final_record path=$MOUNTS records=$records hits=$hits first_target=$B3_SAFE"
    fi
    if [ "$hits" -ne 0 ]; then
        b3_stop "mount_boundary_at_or_under_conf_dir path=$d mounts=$hits first_target=$B3_SAFE"
    fi
    printf 'B3_conf_dir_no_mount_boundary path=%s source=%s records=%s\n' "$d" "$MOUNTS" "$records"
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
# `[ -x ]` and `[ -r ]` are shell builtins over access(2): the kernel answers the
# permission question itself, including POSIX ACLs, capabilities and LSM policy
# for THIS caller, and no diagnostic string is involved. Under the accepted state
# both must be false. Either being true is a FAIL, not a STOP: the directory is
# demonstrably more open to this caller than the accepted host state says, which
# is a host-state observation and not an inability to evaluate.
# HONEST LIMIT (ruling O4): this says nothing about WHO else may enter, and
# access(2) answers for the real uid/gid of this process only. It is a
# caller-specific statement and is logged as one.
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
# CONF_DIR fails with EACCES BEFORE the name is resolved. Outcomes, fail-closed:
#   stat rc == 0                          -> FAIL, conf_dir_entry_permitted
#   raw diagnostic contains CR or LF      -> STOP, boundary_diagnostic_multiline
#   raw diagnostic carries != 1 errno     -> STOP, boundary_diagnostic_ambiguous
#   raw diagnostic == exact EACCES shape  -> PASS arm, B3_conf_dir_opaque_to_operator
#   raw diagnostic == exact ENOENT shape  -> FAIL, conf_dir_search_permitted_name_absent
#   anything else                         -> STOP, boundary_probe_unclassified
#
# A2-F6 - WHY THE ORDER MATTERS. Round 2 sanitized first and then matched with
# `case *"Permission denied"*`. A producer emitting two diagnostic lines - one
# EACCES, one ENOENT - had its newline folded into a space, and the first
# substring match won, so an AMBIGUOUS observation selected the PASS arm and
# returned 0. Wrappers, dynamic-loader diagnostics and mixed producer output all
# generate that shape. Round 3 therefore:
#   1. inspects the RAW capture before any transformation, and rejects it outright
#      if it contains CR or LF - one probe of one path yields one line;
#   2. counts errno phrases in the RAW capture and requires exactly one, so a
#      single line naming two classes is also rejected;
#   3. compares the whole remaining string against the exact C-locale GNU
#      coreutils shapes for THIS path - not a substring, and the path must be the
#      one that was probed. `statx` and `stat` spellings are both accepted
#      because coreutils switched producers; nothing else is.
# Anything unrecognised keeps round 2's reason string `boundary_probe_unclassified`
# at rc 3, so the existing expectation-table row still matches.
# ENOENT stays a FAIL (audit 1 F5/O1): an ENOENT positively PROVES that the
# directory search succeeded, which is the same host-state contradiction a
# successful `stat` is. STOP is reserved for outcomes that do not establish
# whether entry was permitted.
# The PAIR of names passed by the caller is the falsification: EACCES is
# name-independent, so a name the design has no reason to create must be refused
# in exactly the same way. If entry were in fact permitted, the two names would
# diverge (success on one, ENOENT on the other) and both FAIL arms catch it.
# HONEST LIMIT: this probe proves nothing about the existence, the spelling or
# the mode of any file under CONF_DIR, and two names are not a proof over every
# name under a name-sensitive MAC policy (ruling O4). The sec. 8 #4 named risk
# (`bridge.env` vs `mtc-bridge.env`) stays UNRESOLVED until RPD-VERIFY runs as
# root.
# Nothing under CONF_DIR is ever opened, so no content can reach the evidence
# log: the only syscall attempted is a metadata probe expected to be refused.
B3_EACCES_TEXT="Permission denied"
B3_ENOENT_TEXT="No such file or directory"

b3_classify_boundary_shape() {
    local p="$1" raw="$2"
    B3_SHAPE=""
    case "$raw" in
        "stat: cannot statx '$p': $B3_EACCES_TEXT"|"stat: cannot stat '$p': $B3_EACCES_TEXT")
            B3_SHAPE="eacces" ;;
        "stat: cannot statx '$p': $B3_ENOENT_TEXT"|"stat: cannot stat '$p': $B3_ENOENT_TEXT")
            B3_SHAPE="enoent" ;;
    esac
}

b3_assert_conf_dir_opaque() {
    local p="$1" out rc=0 safe n_eacces n_enoent classes
    out="$(LC_ALL=C stat -c '%F|%a|%u:%g' -- "$p" 2>&1)" || rc=$?
    if [ "$rc" -eq 0 ]; then
        b3_sanitize "$out"
        b3_fail "conf_dir_entry_permitted path=$p stat=[$B3_SAFE] expected=EACCES"
    fi
    # --- raw inspection, BEFORE sanitization (A2-F6) ---
    case "$out" in
        *$'\r'*|*$'\n'*)
            b3_sanitize "$out"
            b3_stop "boundary_diagnostic_multiline path=$p rc=$rc detail=$B3_SAFE" ;;
    esac
    b3_count_substr "$out" "$B3_EACCES_TEXT"; n_eacces="$B3_COUNT"
    b3_count_substr "$out" "$B3_ENOENT_TEXT"; n_enoent="$B3_COUNT"
    classes=$(( n_eacces + n_enoent ))
    if [ "$classes" -gt 1 ]; then
        b3_sanitize "$out"
        b3_stop "boundary_diagnostic_ambiguous path=$p rc=$rc classes=$classes eacces=$n_eacces enoent=$n_enoent detail=$B3_SAFE"
    fi
    b3_classify_boundary_shape "$p" "$out"
    b3_sanitize "$out"; safe="$B3_SAFE"
    case "$B3_SHAPE" in
        eacces)
            printf 'B3_conf_dir_opaque_to_operator path=%s outcome=EACCES rc=%s mechanism=message_lc_all_c_exact_shape\n' "$p" "$rc"
            return 0 ;;
        enoent)
            b3_fail "conf_dir_search_permitted_name_absent path=$p rc=$rc expected=EACCES" ;;
    esac
    b3_stop "boundary_probe_unclassified path=$p rc=$rc detail=$safe"
}

printf 'B3_SECTION header candidate=%s\n' "$CAND"
b3_assert_unprivileged
b3_record_namespaces

printf 'B3_SECTION preregistered_inputs\n'
printf 'B3_input name=B3_SWEEP_BUDGET_S value=%s\n' "$B3_SWEEP_BUDGET_S"
printf 'B3_input name=B3_SVC_UID value=%s\n' "$B3_SVC_UID"
printf 'B3_input name=B3_SVC_GID value=%s\n' "$B3_SVC_GID"

printf 'B3_SECTION release_tree\n'
b3_assert_mode_owner "$REL" 0555 "$ROOT_OWNER"
b3_assert_no_writable_paths "$REL"

printf 'B3_SECTION venv_tree\n'
b3_assert_mode_owner "$VENV" 0555 "$ROOT_OWNER"
b3_assert_no_writable_paths "$VENV"

printf 'B3_SECTION ancillary_paths\n'
b3_assert_mode_owner "$STATE_DIR"        0750 "$SVC_OWNER"
b3_assert_mode_owner "$LOG_DIR"          0750 "$SVC_OWNER"
# `stat` on /etc/mtc-bridge ITSELF needs only search on /etc, which this caller
# has; ENTERING /etc/mtc-bridge needs search on /etc/mtc-bridge, which this
# caller does not have. That asymmetry is precisely why the next line survives
# unprivileged while the accepted block's lines 109-110 could not.
b3_assert_mode_owner "$CONF_DIR"         0750 "$ROOT_OWNER"
b3_assert_mode_owner "$UNIT_FILE"        0644 "$ROOT_OWNER"

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
printf 'B3_claim scope=unprivileged_only deferred=3 conf_dir=opaque_to_operator ownership=numeric_only mutation=none\n'
printf 'B3 PASS\n'
