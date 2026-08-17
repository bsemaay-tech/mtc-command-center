# ===== BLOCK-ID: RP1-B3 ===== [EXECUTABLE PROPOSAL BLOCK]
# WP-L Phase 2 - B3 post-start permissions/ownership subcheck (PROPOSED DESIGN,
# B3-GAP-ENV design repair, Option 1, round 1).
# Candidate: 2ce41e34bceb599d80af24c5c33d835820ec321b. NOT host-authorized.
# Read-only `stat`/`find` only. No file content is printed, no
# credential value is read, no POST /api/arm, no broker/exchange/order/TESTNET/
# mainnet/economic action. Requires RP0-LIB sourced and RP0-BOOTSTRAP completed.
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
set -Eeuo pipefail

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

# Preregistered, never derived here:
# B3_RELEASE_MANIFEST_SHA256 is deliberately NO LONGER required by this block. It
# was only ever an input to the manifest-binding check, which now lives in
# RPD-VERIFY as RPD_RELEASE_MANIFEST_SHA256. Requiring it here would let a run of
# this block look like it bound a value that nothing in it tests.
: "${B3_SWEEP_BUDGET_S:?preregistered per-tree sweep budget in seconds is required}"

b3_stop() { printf 'B3_STOP reason=%s\n' "$*"; exit 3; }
b3_fail() { printf 'B3_FAIL reason=%s\n' "$*"; exit 1; }

# --- RP0-LIB precondition ---------------------------------------------------
# Sourcing RP0-LIB is a documented precondition of this block. Asserting it is
# what keeps the 0/1/3 rc contract honest: unsourced, the first predicate call
# would abort under `set -e` with rc 127 and no reason string, which is neither
# a FAIL nor a STOP.
command -v rp0_probe_path   >/dev/null 2>&1 || b3_stop "rp0_lib_not_sourced predicate=rp0_probe_path"
command -v rp0_monotonic_ms >/dev/null 2>&1 || b3_stop "rp0_lib_not_sourced predicate=rp0_monotonic_ms"

# --- exact mode + owner, candidate strength --------------------------------
# Reproduces candidate common.sh assert_mode_owner (:80-93): exact octal mode and
# exact owner:group. There is no accepted alternative mode.
b3_assert_mode_owner() {
    local p="$1" want_mode="${2#0}" want_own="$3" kind mode own
    kind="$(rp0_probe_path "$p")" || exit 3
    case "$kind" in
        regular|dir) : ;;
        absent)                  b3_fail "missing path=$p" ;;
        link_live|link_dangling) b3_fail "canonical deployment path is a symlink kind=$kind path=$p" ;;
        *)                       b3_fail "unexpected object kind=$kind path=$p" ;;
    esac
    mode="$(LC_ALL=C stat -c '%a' -- "$p")"   || b3_stop "mode_probe_failed path=$p"
    own="$(LC_ALL=C stat -c '%U:%G' -- "$p")" || b3_stop "owner_probe_failed path=$p"
    printf 'B3_stat path=%s owner=%s mode=%s\n' "$p" "$own" "$mode"
    [ "$mode" = "$want_mode" ] || b3_fail "path=$p mode=$mode expected=$want_mode"
    [ "$own"  = "$want_own"  ] || b3_fail "path=$p owner=$own expected=$want_own"
}

# --- candidate any-write-bit sweep, budgeted, fail-closed ------------------
# Candidate common.sh:95-105 predicate, reproduced verbatim:
#     find "$root" ! -type l -perm /222 -print -quit
# `/222` matches ANY write bit (owner, group OR other). `-perm -0200` is
# owner-write-only and silently passes a 0020 or 0002 offender - that was F2.
# Honest cost: `-quit` shortens only a FAILING sweep; a clean tree is a full
# walk. The operator preregisters B3_SWEEP_BUDGET_S; exceeding it is STOP.
b3_assert_no_writable_paths() {
    local root="$1" offenders errf rc=0 t0 t1 elapsed_s
    errf="$(mktemp)" || b3_stop "sweep_tempfile_failed root=$root"
    t0="$(rp0_monotonic_ms)" || exit 3
    offenders="$(find "$root" ! -type l -perm /222 -print -quit 2>"$errf")" || rc=$?
    t1="$(rp0_monotonic_ms)" || exit 3
    if [ "$rc" -ne 0 ]; then
        b3_stop "writable_inventory_failed root=$root rc=$rc detail=$(tr -d '\r\n' <"$errf") partial=[$offenders]"
    fi
    rm -f "$errf"
    elapsed_s=$(( (t1 - t0) / 1000 ))
    printf 'B3_sweep root=%s elapsed_s=%s budget_s=%s\n' "$root" "$elapsed_s" "$B3_SWEEP_BUDGET_S"
    [ "$elapsed_s" -le "$B3_SWEEP_BUDGET_S" ] \
        || b3_stop "sweep_budget_exceeded root=$root elapsed_s=$elapsed_s budget_s=$B3_SWEEP_BUDGET_S"
    [ -z "$offenders" ] || b3_fail "writable path inside immutable tree: $offenders"
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
# FAIL arm below therefore reports the OBSERVATION (entry was permitted) and
# names the accepted state it contradicts, leaving the cause to Lead
# adjudication instead of asserting one.
b3_assert_unprivileged() {
    local uid gids
    uid="$(id -u)"  || b3_stop "uid_probe_failed"
    gids="$(id -G)" || b3_stop "group_probe_failed"
    [ "$uid" != "0" ] || b3_stop "must_run_unprivileged uid=$uid"
    printf 'B3_identity uid=%s gids=[%s]\n' "$uid" "$gids"
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

# --- unprivileged boundary probe: CONF_DIR must be OPAQUE to the caller -----
# Accepted host state: CONF_DIR is 0750 root:root (asserted separately, below)
# and the caller is neither root nor in group root (asserted above). Under that
# state the kernel denies the directory search, so `stat` on ANY name under
# CONF_DIR fails with EACCES BEFORE the name is resolved. Under this design a
# SUCCESSFUL stat is therefore a FAIL: it means the caller entered a directory
# that the accepted state says it cannot enter, i.e. the directory is more open
# than the accepted host state. Three outcomes, fail-closed:
#   stat rc != 0, stderr EACCES  -> PASS arm, B3_conf_dir_opaque_to_operator
#   stat rc == 0                 -> FAIL, conf_dir_entry_permitted
#   any other error class        -> STOP, could not evaluate
# ENOENT carries its own STOP reason string because it ALSO proves the search
# succeeded; it is routed to STOP rather than FAIL to keep the rule "anything
# that is neither the EACCES arm nor a successful stat is could-not-evaluate",
# and because the two escalate identically (PREREGISTRATION.md sec. 8: any B3
# FAIL is itself a STOP requiring Lead adjudication). Whether the Lead prefers
# ENOENT rendered as a FAIL is recorded as an open item in DESIGN_NOTES.md.
# The PAIR of names passed by the caller is the falsification: EACCES is
# name-independent, so a name the design has no reason to create must be refused
# in exactly the same way. If entry were in fact permitted, the two names would
# diverge (success on one, ENOENT on the other) and both arms above catch it.
# HONEST LIMIT: this probe proves nothing about the existence, the spelling or
# the mode of any file under CONF_DIR. The sec. 8 #4 named risk (`bridge.env`
# vs `mtc-bridge.env`) stays UNRESOLVED until RPD-VERIFY runs as root.
# Nothing under CONF_DIR is ever opened, so no content can reach the evidence
# log: the only syscall attempted is a metadata probe expected to be refused.
b3_assert_conf_dir_opaque() {
    local p="$1" errf detail meta rc=0
    errf="$(mktemp)" || b3_stop "boundary_tempfile_failed path=$p"
    meta="$(LC_ALL=C stat -c '%F|%a|%U:%G' -- "$p" 2>"$errf")" || rc=$?
    detail="$(tr -d '\r\n' <"$errf")"
    rm -f "$errf"
    if [ "$rc" -eq 0 ]; then
        b3_fail "conf_dir_entry_permitted path=$p stat=[$meta] expected=EACCES"
    fi
    case "$detail" in
        *"Permission denied"*)
            printf 'B3_conf_dir_opaque_to_operator path=%s outcome=EACCES rc=%s\n' "$p" "$rc"
            return 0 ;;
        *"No such file or directory"*)
            b3_stop "conf_dir_search_permitted_name_absent path=$p rc=$rc expected=EACCES" ;;
    esac
    b3_stop "boundary_probe_unclassified path=$p rc=$rc detail=$detail"
}

printf 'B3_SECTION header candidate=%s\n' "$CAND"
b3_assert_unprivileged

printf 'B3_SECTION release_tree\n'
b3_assert_mode_owner "$REL" 0555 root:root
b3_assert_no_writable_paths "$REL"

printf 'B3_SECTION venv_tree\n'
b3_assert_mode_owner "$VENV" 0555 root:root
b3_assert_no_writable_paths "$VENV"

printf 'B3_SECTION ancillary_paths\n'
b3_assert_mode_owner "$STATE_DIR"        0750 mtc-bridge:mtc-bridge
b3_assert_mode_owner "$LOG_DIR"          0750 mtc-bridge:mtc-bridge
# `stat` on /etc/mtc-bridge ITSELF needs only search on /etc, which this caller
# has; ENTERING /etc/mtc-bridge needs search on /etc/mtc-bridge, which this
# caller does not have. That asymmetry is precisely why the next line survives
# unprivileged while the accepted block's lines 109-110 could not.
b3_assert_mode_owner "$CONF_DIR"         0750 root:root
b3_assert_mode_owner "$UNIT_FILE"        0644 root:root

printf 'B3_SECTION conf_dir_boundary\n'
b3_assert_not_in_dir_group "$CONF_DIR"
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
printf 'B3_claim scope=unprivileged_only deferred=3 conf_dir=opaque_to_operator\n'
printf 'B3 PASS\n'
