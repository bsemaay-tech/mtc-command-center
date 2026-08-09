# ===== BLOCK-ID: RP5-C4A ===== [EXECUTABLE PROPOSAL BLOCK]
# WP-L Phase 2 — C4 stage A: rollback stop+mask-only, no rebind (PROPOSED DESIGN).
# Candidate: 2ce41e34bceb599d80af24c5c33d835820ec321b. NOT host-authorized.
# Mutation class: mutating-host. Requires its own explicit named authority and
# budget lift; this document grants none. No credential read, no POST /api/arm,
# no broker/exchange/order/TESTNET/mainnet/economic action, no start, no unmask.
# Requires RP0-LIB and RP0-BOOTSTRAP.
#
# This stage captures, verifies and compares NOTHING, and therefore establishes
# nothing about state preservation. It ends by proving the capture destination is
# still absent and writing ONE create-once stage record that stages B and C bind
# to. That is the point of the split: a post-rollback artifact can only be shown
# to postdate the rollback if the rollback stage first proved its destination
# empty and then handed that proof forward.
set -Eeuo pipefail

UNIT="mtc-bridge-first-start.service"
MASK_PATH="/etc/systemd/system/$UNIT"
UNIT_FILE="/usr/local/lib/systemd/system/$UNIT"
RELEASE_ROOT="/opt/mtc-bridge/releases/2ce41e34bceb599d80af24c5c33d835820ec321b/IBKR_PAPER_BRIDGE"
ROLLBACK_SH="$RELEASE_ROOT/deploy/linux/rollback.sh"
ROLLBACK_MANIFEST="/etc/mtc-bridge/rollback_manifest.json"
STEADY_UNIT_A="/usr/local/lib/systemd/system/mtc-bridge-steady.service"
STEADY_UNIT_B="/etc/systemd/system/mtc-bridge-steady.service"
PORT="8790"

# Preregistered, never derived here:
: "${C4_STATE_MANIFEST_FILE:?accepted C3 bundle manifest file path is required}"
: "${C4_STATE_MANIFEST_SHA256:?externally recorded C3 manifest FILE sha256 is required}"
: "${C4_ROLLBACK_SH_SHA256:?preregistered candidate rollback.sh sha256 is required}"
: "${C4_EXPECT_UNIT_SHA256:?preregistered installed first-start unit sha256, or the literal ABSENT_PREREGISTERED}"
: "${C4_START_ACTIVE:?preregistered starting ActiveState is required}"
: "${C4_START_ENABLED:?preregistered starting is-enabled token is required}"
: "${C4_PRE_INVARIANTS_SHA256:?preregistered pre-rollback protected-invariant hash is required}"
# The post side is preregistered as an EMPTY DESTINATION — a path, its parent, and
# the parent's expected owner/mode. No post-rollback hash may be supplied here:
# a value available before the rollback necessarily describes a bundle that
# existed before the rollback, which was exactly the accepted-bypass defect.
: "${C4_POST_BUNDLE_DIR:?post-rollback capture destination path is required, and must be absent}"
: "${C4_POST_BUNDLE_PARENT:?capture destination parent directory is required}"
: "${C4_POST_BUNDLE_PARENT_OWNER:?capture destination parent owner:group is required}"
: "${C4_POST_BUNDLE_PARENT_MODE:?capture destination parent octal mode is required}"
: "${C4_STAGE_RECORD:?create-once stage-A record path is required}"
: "${PY:?candidate venv interpreter path is required}"

c4_stop() { printf 'C4_STOP reason=%s\n' "$*"; exit 3; }
c4_fail() { printf 'C4_FAIL reason=%s\n' "$*"; exit 1; }

# Three outcomes, like every other predicate: a hash that CANNOT be taken is
# never rendered as a value. Callers adjudicate rc 3 themselves.
c4_sha256() {
    local p="$1" out rc=0
    out="$(LC_ALL=C sha256sum -- "$p" 2>&1)" || rc=$?
    if [ "$rc" -ne 0 ]; then
        printf 'C4_STOP reason=sha256_failed path=%s rc=%s detail=%s\n' "$p" "$rc" "$out" >&2
        return 3
    fi
    printf '%s\n' "${out%% *}"
    return 0
}

# Digest of an inventory STRING. `<<<` avoids a pipeline, so there is no
# component status to lose; the added trailing newline is deterministic.
c4_sha256_string() {
    local label="$1" data="$2" out rc=0
    out="$(LC_ALL=C sha256sum <<<"$data" 2>&1)" || rc=$?
    if [ "$rc" -ne 0 ]; then
        printf 'C4_STOP reason=inventory_hash_failed label=%s rc=%s detail=%s\n' "$label" "$rc" "$out" >&2
        return 3
    fi
    printf '%s\n' "${out%% *}"
    return 0
}

# Fingerprint used to prove the dry run mutated NOTHING.
# EVERY component is evaluated and adjudicated in its OWN assignment before the
# final `printf`. Nesting a probe or a hash inside the printf arguments makes
# `printf`'s status the function status, so a STOP is rendered as an empty field
# and the function still succeeds — that was the first defect here.
# The writers, listeners and cgroup members are compared as canonical fail-closed
# INVENTORIES, not as a status code and two counts: a same-count replacement left
# a status/count fingerprint identical, so "nothing was mutated" was satisfiable
# by a mutated host — that was the second defect. The full inventories go to the
# evidence log on stderr; their digests go into the compared string, so an
# inequality is both detected and diagnosable.
c4_fingerprint() {
    local a e m r c w l g wd ld gd
    a="$(rp0_show_property "$UNIT" ActiveState)"       || return 3
    e="$(rp0_is_enabled_token "$UNIT")"                || return 3
    m="$(rp0_probe_path "$MASK_PATH")"                 || return 3
    r="$(rp0_probe_path "$ROLLBACK_MANIFEST")"         || return 3
    c="$(c4_sha256 "$C4_STATE_MANIFEST_FILE")"         || return 3
    w="$(rp0_writer_inventory 'bridge\.app')"          || return 3
    l="$(rp0_listener_inventory "$PORT")"              || return 3
    g="$(rp0_cgroup_inventory "$UNIT")"                || return 3
    wd="$(c4_sha256_string writers   "$w")"            || return 3
    ld="$(c4_sha256_string listeners "$l")"            || return 3
    gd="$(c4_sha256_string cgroup    "$g")"            || return 3
    printf 'C4_INVENTORY writers_begin\n%s\nC4_INVENTORY writers_end\n'     "$w" >&2
    printf 'C4_INVENTORY listeners_begin\n%s\nC4_INVENTORY listeners_end\n' "$l" >&2
    printf 'C4_INVENTORY cgroup_begin\n%s\nC4_INVENTORY cgroup_end\n'       "$g" >&2
    printf 'active=%s enabled=%s mask=%s manifest=%s c3=%s writers=%s listeners=%s cgroup=%s\n' \
        "$a" "$e" "$m" "$r" "$c" "$wd" "$ld" "$gd"
    return 0
}

printf 'C4_SECTION step0_prerequisites\n'

# 1. accepted C3 manifest file plus its externally recorded FILE sha256.
kind="$(rp0_probe_path "$C4_STATE_MANIFEST_FILE")" || exit 3
[ "$kind" = "regular" ] || c4_fail "C3 manifest kind=$kind path=$C4_STATE_MANIFEST_FILE"
got="$(c4_sha256 "$C4_STATE_MANIFEST_FILE")" || c4_stop "c3_manifest_hash_unevaluable path=$C4_STATE_MANIFEST_FILE"
[ "$got" = "$C4_STATE_MANIFEST_SHA256" ] || c4_fail "C3 manifest file sha256=$got expected=$C4_STATE_MANIFEST_SHA256"
printf 'C4_c3_manifest_sha256=%s\n' "$got"

# 2. rollback-manifest path proven absent as OBJECT AND LINK, immediately before use.
#    The candidate guard (:70-71) rejects a symlink only; it supplies NO regular-file
#    no-clobber protection, and :157-180 overwrites with an unconditional `cat >`.
kind="$(rp0_probe_path "$ROLLBACK_MANIFEST")" || exit 3
printf 'C4_rollback_manifest_pre_kind=%s\n' "$kind"
[ "$kind" = "absent" ] || c4_fail "rollback manifest must be absent as object AND link, found $kind"

# 3. steady unit absent at both paths; candidate script and C3 manifest re-hashed.
for p in "$STEADY_UNIT_A" "$STEADY_UNIT_B"; do
    kind="$(rp0_probe_path "$p")" || exit 3
    [ "$kind" = "absent" ] || c4_fail "unexpected steady unit kind=$kind path=$p"
done
got="$(c4_sha256 "$ROLLBACK_SH")" || c4_stop "rollback_sh_hash_unevaluable path=$ROLLBACK_SH"
[ "$got" = "$C4_ROLLBACK_SH_SHA256" ] || c4_fail "rollback.sh sha256=$got expected=$C4_ROLLBACK_SH_SHA256"

# 4. preregistered starting state captured and matched.
active="$(rp0_show_property "$UNIT" ActiveState)" || exit 3
enabled="$(rp0_is_enabled_token "$UNIT")"         || exit 3
printf 'C4_start_active=%s C4_start_enabled=%s\n' "$active" "$enabled"
[ "$active"  = "$C4_START_ACTIVE"  ] || c4_fail "starting ActiveState=$active expected=$C4_START_ACTIVE"
[ "$enabled" = "$C4_START_ENABLED" ] || c4_fail "starting is-enabled=$enabled expected=$C4_START_ENABLED"

unit_kind="$(rp0_probe_path "$UNIT_FILE")" || exit 3
if [ "$unit_kind" = "regular" ]; then
    installed_unit_sha="$(c4_sha256 "$UNIT_FILE")" || c4_stop "installed_unit_hash_unevaluable path=$UNIT_FILE"
    [ "$C4_EXPECT_UNIT_SHA256" != "ABSENT_PREREGISTERED" ] \
        || c4_fail "installed unit present but its absence was preregistered"
    [ "$installed_unit_sha" = "$C4_EXPECT_UNIT_SHA256" ] \
        || c4_fail "installed unit sha256=$installed_unit_sha expected=$C4_EXPECT_UNIT_SHA256"
    expect_manifest_unit_sha="$C4_EXPECT_UNIT_SHA256"
elif [ "$unit_kind" = "absent" ]; then
    [ "$C4_EXPECT_UNIT_SHA256" = "ABSENT_PREREGISTERED" ] \
        || c4_fail "installed unit absent but a hash was preregistered"
    expect_manifest_unit_sha=""
else
    c4_fail "installed unit kind=$unit_kind path=$UNIT_FILE"
fi
printf 'C4_installed_unit_kind=%s\n' "$unit_kind"

# 5. THE CAPTURE DESTINATION MUST BE EMPTY BEFORE ANY MUTATION.
#    This is the structural half of the freshness proof: whatever stage B later
#    finds there cannot be an artifact that predates this rollback. The parent is
#    proven canonical, non-link, with preregistered owner/mode, and the
#    destination is proven a DIRECT child of it, so no symlinked intermediate and
#    no manufactured intermediate can redirect the capture.
rp0_require_canonical_dir "$C4_POST_BUNDLE_PARENT" "$C4_POST_BUNDLE_PARENT_OWNER" "$C4_POST_BUNDLE_PARENT_MODE" \
    || exit $?
rp0_require_leaf_inside "$C4_POST_BUNDLE_PARENT" "$C4_POST_BUNDLE_DIR" || exit $?
kind="$(rp0_probe_path "$C4_POST_BUNDLE_DIR")" || exit 3
printf 'C4_post_dest_pre_kind=%s\n' "$kind"
[ "$kind" = "absent" ] \
    || c4_fail "capture destination must be absent as object AND link before any mutation, found $kind"
kind="$(rp0_probe_path "$C4_STAGE_RECORD")" || exit 3
[ "$kind" = "absent" ] || c4_fail "stage record path must be absent, found $kind"

printf 'C4_SECTION step1_mutation_free_dry_run\n'
fp_before="$(c4_fingerprint)" || c4_stop "fingerprint_unevaluable phase=before"
dry_out="$(MTC_DRY_RUN=1 "$ROLLBACK_SH" --dry-run \
    --state-manifest-file "$C4_STATE_MANIFEST_FILE" \
    --state-manifest-sha256 "$C4_STATE_MANIFEST_SHA256" 2>&1)" || c4_fail "rollback.sh --dry-run exited nonzero"
printf 'C4_dry_run_output_begin\n%s\nC4_dry_run_output_end\n' "$dry_out"
LC_ALL=C grep -qF -- "[dry-run] systemctl stop $UNIT" <<<"$dry_out" \
    || c4_fail "dry run did not print the expected stop line"
LC_ALL=C grep -qF -- "[dry-run] systemctl mask $UNIT" <<<"$dry_out" \
    || c4_fail "dry run did not print the expected mask line"
fp_after="$(c4_fingerprint)" || c4_stop "fingerprint_unevaluable phase=after"
[ "$fp_before" = "$fp_after" ] || c4_fail "dry run mutated observable state: [$fp_before] -> [$fp_after]"
kind="$(rp0_probe_path "$ROLLBACK_MANIFEST")" || exit 3
[ "$kind" = "absent" ] || c4_fail "dry run created a rollback manifest ($kind)"
printf 'C4_dry_run_mutation_free=yes\n'

printf 'C4_SECTION step2_single_real_invocation\n'
# Exactly one invocation. No --to-release-sha, no --to-manifest-sha256: no rebind.
"$ROLLBACK_SH" \
    --state-manifest-file "$C4_STATE_MANIFEST_FILE" \
    --state-manifest-sha256 "$C4_STATE_MANIFEST_SHA256" \
    || c4_fail "rollback.sh (stop+mask-only) exited nonzero"

printf 'C4_SECTION step3_postconditions\n'
active="$(rp0_show_property "$UNIT" ActiveState)" || exit 3
enabled="$(rp0_is_enabled_token "$UNIT")"         || exit 3
printf 'C4_post_active=%s C4_post_enabled=%s\n' "$active" "$enabled"
[ "$active"  = "inactive" ] || c4_fail "ActiveState=$active expected inactive"
[ "$enabled" = "masked"   ] || c4_fail "is-enabled=$enabled expected exactly masked"

mask_kind="$(rp0_probe_path "$MASK_PATH")" || exit 3
[ "$mask_kind" = "link_live" ] || c4_fail "mask path kind=$mask_kind expected a live symlink"
raw_target="$(readlink -- "$MASK_PATH")" || c4_stop "mask_link_read_failed path=$MASK_PATH"
printf 'C4_mask_raw_target=%s\n' "$raw_target"
[ "$raw_target" = "/dev/null" ] || c4_fail "mask link raw target=$raw_target expected exactly /dev/null"

procs=""; prc=0
procs="$(rp0_pgrep_status 'bridge\.app')" || prc=$?
case "$prc" in
    0) printf 'C4_dangling_procs_begin\n%s\nC4_dangling_procs_end\n' "$procs"
       c4_fail "a bridge.app process survived rollback stop+mask" ;;
    1) printf 'C4_writers=0\n' ;;
    *) exit 3 ;;
esac
listeners="$(rp0_listener_count "$PORT")" || exit 3
printf 'C4_listener_count=%s\n' "$listeners"
[ "$listeners" -eq 0 ] || c4_fail "control port $PORT still has a listener after rollback"

# Third survivor class, fail-closed: a stopped-and-masked unit whose cgroup
# still holds a process has not been stopped.
cgsurv="$(rp0_cgroup_survivors "$UNIT")" || exit 3
printf 'C4_cgroup_survivors=%s\n' "$cgsurv"
[ "$cgsurv" -eq 0 ] || c4_fail "the unit cgroup still holds $cgsurv process(es) after rollback stop+mask"

printf 'C4_SECTION step4_rollback_manifest\n'
kind="$(rp0_probe_path "$ROLLBACK_MANIFEST")" || exit 3
[ "$kind" = "regular" ] || c4_fail "rollback manifest kind=$kind expected a newly created regular file"
rm_mode="$(LC_ALL=C stat -c '%a' -- "$ROLLBACK_MANIFEST")"   || c4_stop "rollback_manifest_mode_probe_failed"
rm_own="$(LC_ALL=C stat -c '%U:%G' -- "$ROLLBACK_MANIFEST")" || c4_stop "rollback_manifest_owner_probe_failed"
printf 'C4_rollback_manifest_mode=%s owner=%s\n' "$rm_mode" "$rm_own"
[ "$rm_mode" = "640" ]      || c4_fail "rollback manifest mode=$rm_mode expected 640"
[ "$rm_own"  = "root:root" ] || c4_fail "rollback manifest owner=$rm_own expected root:root"

# Every expected field and value validated. In no-rebind mode the candidate
# leaves rollback_release_sha and rollback_release_manifest_sha256 EMPTY
# (rollback.sh:164-165 with unset TARGET_*), while first_start_unit_sha256 is
# the INSTALLED unit hash when that unit is present (:113-116, :168) and empty
# only when the unit file is absent.
"$PY" - "$ROLLBACK_MANIFEST" "$C4_STATE_MANIFEST_SHA256" "$UNIT" "$expect_manifest_unit_sha" <<'PYEOF' \
    || c4_fail "rollback manifest field validation failed"
import json, re, sys
path, state_sha, unit, expect_unit_sha = sys.argv[1:5]
with open(path, "r", encoding="utf-8") as handle:
    m = json.load(handle)
expected = {
    "schema_version": "1.0.0",
    "rollback_release_sha": "",
    "rollback_release_manifest_sha256": "",
    "state_bundle_manifest_sha256": state_sha,
    "first_start_unit": unit,
    "first_start_unit_sha256": expect_unit_sha,
    "first_start_unit_state": "masked",
    "service_active": False,
    "service_enabled": False,
    "service_started_by_this_script": False,
    "state_dir_preserved": True,
    "secrets_touched": False,
    "firewall_modified": False,
    "windows_writer_restored": False,
}
problems = []
missing = sorted((set(expected) | {"rolled_back_at_utc"}) - set(m))
if missing:
    problems.append(f"missing_fields={missing}")
extra = sorted(set(m) - set(expected) - {"rolled_back_at_utc"})
if extra:
    problems.append(f"unexpected_fields={extra}")
for key, want in expected.items():
    got = m.get(key)
    if got != want or type(got) is not type(want):
        problems.append(f"{key}={got!r} expected {want!r}")
if not re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", str(m.get("rolled_back_at_utc", ""))):
    problems.append(f"rolled_back_at_utc={m.get('rolled_back_at_utc')!r}")
if problems:
    print("C4_manifest_problems=" + "; ".join(problems))
    raise SystemExit(1)
print("C4_manifest_fields_validated=all")
PYEOF

printf 'C4_SECTION step5_stage_record_handoff\n'
# The destination must STILL be absent AFTER the rollback: the rollback is not
# permitted to leave anything at the capture path, and stage B must be able to
# attribute whatever it finds there to its own capture and to nothing else.
kind="$(rp0_probe_path "$C4_POST_BUNDLE_DIR")" || exit 3
printf 'C4_post_dest_post_kind=%s\n' "$kind"
[ "$kind" = "absent" ] || c4_fail "capture destination is no longer absent after the rollback ($kind)"

# ONE create-once stage record. It pins the rollback manifest by content hash AND
# by (st_dev, st_ino, st_mtime_ns), so stage B can prove it is binding itself to
# THIS rollback event and not to a later rewrite of the same path.
srrc=0
"$PY" - "$C4_STAGE_RECORD" "$ROLLBACK_MANIFEST" "$C4_STATE_MANIFEST_FILE" \
    "$C4_STATE_MANIFEST_SHA256" "$C4_PRE_INVARIANTS_SHA256" "$C4_POST_BUNDLE_DIR" "$UNIT" <<'PYEOF' || srrc=$?
import hashlib, json, os, stat as statmod, sys

(record, rollback_manifest, c3_manifest, c3_sha, pre_inv_sha, post_dir, unit) = sys.argv[1:8]


def stop(reason):
    print(f"C4_STOP reason={reason}")
    raise SystemExit(3)


def fail(reason):
    print(f"C4_FAIL reason={reason}")
    raise SystemExit(1)


def sha256_file(path):
    try:
        digest = hashlib.sha256()
        with open(path, "rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
        return digest.hexdigest()
    except OSError as exc:
        stop(f"hash_failed path={path} {exc.__class__.__name__}: {exc}")


try:
    st = os.lstat(rollback_manifest)
except OSError as exc:
    stop(f"rollback_manifest_stat_failed {exc.__class__.__name__}: {exc}")
if not statmod.S_ISREG(st.st_mode):
    fail(f"rollback manifest is not a regular non-link file: mode={st.st_mode:#o}")
try:
    with open(rollback_manifest, "r", encoding="utf-8") as handle:
        rollback = json.load(handle)
except Exception as exc:
    stop(f"rollback_manifest_unreadable {exc.__class__.__name__}: {exc}")

payload = {
    "schema": "wpl-p2-c4-stage-a/1",
    "unit": unit,
    "c3_manifest_path": c3_manifest,
    "c3_manifest_sha256": c3_sha,
    "pre_invariants_sha256": pre_inv_sha,
    "capture_destination": post_dir,
    "capture_destination_absent_before_mutation": True,
    "capture_destination_absent_after_rollback": True,
    "rollback_manifest_path": rollback_manifest,
    "rollback_manifest_sha256": sha256_file(rollback_manifest),
    "rollback_manifest_dev": st.st_dev,
    "rollback_manifest_ino": st.st_ino,
    "rollback_manifest_mtime_ns": st.st_mtime_ns,
    "rolled_back_at_utc": rollback.get("rolled_back_at_utc"),
}
blob = (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode("utf-8")
# Create-once: O_CREAT|O_EXCL refuses an existing regular file and an existing
# symlink, live or dangling. No append, no truncation, no rename-aside, no retry.
# The write is BINARY: a text-mode write translates newlines on some platforms,
# after which the digest printed below would not be the digest of the bytes on
# disk and the external recording would bind nothing.
try:
    handle_fd = os.open(record, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
except FileExistsError:
    fail(f"stage record already exists: {record}")
except OSError as exc:
    stop(f"stage_record_not_creatable path={record} {exc.__class__.__name__}: {exc}")
with os.fdopen(handle_fd, "wb") as handle:
    handle.write(blob)
print("C4_stage_record_path=" + record)
print("C4_stage_record_sha256=" + hashlib.sha256(blob).hexdigest())
print("C4_rollback_manifest_mtime_ns=" + str(payload["rollback_manifest_mtime_ns"]))
PYEOF
case "$srrc" in
    0) : ;;
    1) c4_fail "stage record handoff refused" ;;
    *) c4_stop "stage_record_unevaluable rc=$srrc" ;;
esac

printf 'C4_SECTION done\n'
printf 'C4A PASS (unit stopped and masked; capture destination proven empty; NOTHING about state\n'
printf '          preservation is established yet, and no start, unmask or recovery is authorised)\n'
