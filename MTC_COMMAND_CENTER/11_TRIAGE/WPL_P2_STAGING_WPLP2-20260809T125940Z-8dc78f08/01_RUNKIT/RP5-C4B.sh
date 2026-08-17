# ===== BLOCK-ID: RP5-C4B ===== [EXECUTABLE PROPOSAL BLOCK]
# WP-L Phase 2 — C4 stage B: fresh post-rollback capture (PROPOSED DESIGN).
# Candidate: 2ce41e34bceb599d80af24c5c33d835820ec321b. NOT host-authorized.
# Mutation class: mutating-filesystem. Creates exactly ONE new bundle directory,
# at a path proven absent, and reads the state database READ-ONLY through the
# candidate's own capture API. No service action, no start, no unmask, no
# daemon-reload, no credential read, no POST /api/arm, no network, no broker/
# exchange/order/TESTNET/mainnet/economic action. Requires its own explicit named
# authority; this document grants none. Requires RP0-LIB and RP0-BOOTSTRAP.
#
# Runs ONLY after RP5-C4A completed and wrote its stage record. The capture is
# performed HERE, into a destination this block proves absent immediately
# beforehand, so the artifact is causally downstream of the rollback pinned in
# that record. No post-rollback hash is an INPUT: all three are OUTPUTS, printed
# for external recording, and stage C consumes them.
#
# Capture must run AFTER the stop+mask, never before. With allow_live_source unset
# — and this block never sets it — the candidate REJECTS a capture whose source
# changed while it was being captured (`source_changed_during_capture`,
# wal_state_bundle.py:840-842). A stopped, masked unit is what makes that
# predicate satisfiable at all; a running writer would earn the rejection.
set -Eeuo pipefail

RELEASE_ROOT="/opt/mtc-bridge/releases/2ce41e34bceb599d80af24c5c33d835820ec321b/IBKR_PAPER_BRIDGE"
ROLLBACK_MANIFEST="/etc/mtc-bridge/rollback_manifest.json"

: "${C4_STAGE_RECORD:?stage-A record path is required}"
: "${C4_STAGE_RECORD_SHA256:?externally recorded stage-A record sha256 is required}"
: "${C4_POST_BUNDLE_DIR:?capture destination is required, and must still be absent}"
: "${C4_POST_BUNDLE_PARENT:?capture destination parent directory is required}"
: "${C4_POST_BUNDLE_PARENT_OWNER:?capture destination parent owner:group is required}"
: "${C4_POST_BUNDLE_PARENT_MODE:?capture destination parent octal mode is required}"
: "${C4_STATE_DB:?live state database path is required}"
: "${C4_CAPTURE_RECORD:?create-once stage-B capture record path is required}"
: "${PY:?candidate venv interpreter path is required}"

c4b_stop() { printf 'C4B_STOP reason=%s\n' "$*"; exit 3; }
c4b_fail() { printf 'C4B_FAIL reason=%s\n' "$*"; exit 1; }

printf 'C4B_SECTION step0_prerequisites\n'
for p in "$C4_STAGE_RECORD" "$C4_STATE_DB"; do
    kind="$(rp0_probe_path "$p")" || exit 3
    [ "$kind" = "regular" ] || c4b_fail "expected a regular non-link file, kind=$kind path=$p"
done
kind="$(rp0_probe_path "$C4_CAPTURE_RECORD")" || exit 3
[ "$kind" = "absent" ] || c4b_fail "capture record path must be absent, found $kind"

# Same parent-chain and direct-child proof as stage A, re-run here: between the
# two stages the parent could have been replaced by a symlink.
rp0_require_canonical_dir "$C4_POST_BUNDLE_PARENT" "$C4_POST_BUNDLE_PARENT_OWNER" "$C4_POST_BUNDLE_PARENT_MODE" \
    || exit $?
rp0_require_leaf_inside "$C4_POST_BUNDLE_PARENT" "$C4_POST_BUNDLE_DIR" || exit $?
kind="$(rp0_probe_path "$C4_POST_BUNDLE_DIR")" || exit 3
printf 'C4B_dest_pre_capture_kind=%s\n' "$kind"
[ "$kind" = "absent" ] \
    || c4b_fail "capture destination is not absent ($kind): a pre-existing artifact is never adopted as the fresh capture"

printf 'C4B_SECTION step1_bind_rollback_then_capture\n'
cbrc=0
"$PY" - "$RELEASE_ROOT" "$C4_STAGE_RECORD" "$C4_STAGE_RECORD_SHA256" "$C4_POST_BUNDLE_DIR" \
    "$C4_POST_BUNDLE_PARENT" "$C4_STATE_DB" "$C4_CAPTURE_RECORD" "$ROLLBACK_MANIFEST" <<'PYEOF' || cbrc=$?
import hashlib, json, os, stat as statmod, sys
from pathlib import Path

(release_root, stage_record, stage_record_sha, post_dir, post_parent, state_db,
 capture_record, rollback_manifest) = sys.argv[1:9]


def stop(reason):
    print(f"C4B_STOP reason={reason}")
    raise SystemExit(3)


def fail(reason):
    print(f"C4B_FAIL reason={reason}")
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


def load(path):
    try:
        with open(path, "r", encoding="utf-8") as handle:
            return json.load(handle)
    except Exception as exc:
        stop(f"unreadable_json path={path} {exc.__class__.__name__}: {exc}")


sys.path.insert(0, release_root)
try:
    from tools.wal_state_bundle import MANIFEST_NAME, create_bundle
except Exception as exc:
    stop(f"candidate_api_import_failed: {exc.__class__.__name__}: {exc}")

# 1. the stage record is exactly the externally recorded one.
actual_stage_sha = sha256_file(stage_record)
print(f"C4B_stage_record_sha256={actual_stage_sha}")
if actual_stage_sha != stage_record_sha.lower():
    fail("stage record sha256 does not match the externally recorded value")
record = load(stage_record)
if record.get("schema") != "wpl-p2-c4-stage-a/1":
    fail(f"stage record schema={record.get('schema')!r} is not the stage-A contract")
if record.get("capture_destination") != post_dir:
    fail("stage record names a different capture destination than this stage was given")
if record.get("capture_destination_absent_before_mutation") is not True:
    fail("stage record does not assert the destination was absent before the mutation")
if record.get("capture_destination_absent_after_rollback") is not True:
    fail("stage record does not assert the destination was absent after the rollback")

# 2. the SAME rollback event, not a later rewrite of the same path.
try:
    rst = os.lstat(rollback_manifest)
except OSError as exc:
    stop(f"rollback_manifest_stat_failed {exc.__class__.__name__}: {exc}")
if not statmod.S_ISREG(rst.st_mode):
    fail(f"rollback manifest is not a regular non-link file: mode={rst.st_mode:#o}")
live = (rst.st_dev, rst.st_ino, rst.st_mtime_ns, sha256_file(rollback_manifest))
pinned = (record.get("rollback_manifest_dev"), record.get("rollback_manifest_ino"),
          record.get("rollback_manifest_mtime_ns"), record.get("rollback_manifest_sha256"))
print(f"C4B_rollback_identity_live={live}")
print(f"C4B_rollback_identity_pinned={pinned}")
# A malformed record is COULD NOT EVALUATE, not FALSE: without this the type error
# below would surface as a Python traceback and be adjudicated as a plain FAIL.
if not isinstance(pinned[2], int):
    stop(f"pinned_rollback_mtime_ns_not_an_integer: {pinned[2]!r}")
if live != pinned:
    fail("the rollback manifest changed since stage A: this capture cannot be bound to that rollback")
rolled = str(record.get("rolled_back_at_utc") or "")
if not rolled:
    stop("stage_record_missing_rolled_back_at_utc")

# 3. the parent must ALREADY be a real directory, so the candidate's
#    out_dir.mkdir(parents=True) has no intermediate left to manufacture.
try:
    pst = os.lstat(post_parent)
except OSError as exc:
    stop(f"parent_stat_failed path={post_parent} {exc.__class__.__name__}: {exc}")
if not statmod.S_ISDIR(pst.st_mode):
    fail(f"capture destination parent is not a real directory: mode={pst.st_mode:#o}")

# 4. destination absent as OBJECT AND LINK immediately before the capture. This
#    is the structural freshness proof: an artifact at a path that was empty one
#    instruction earlier was produced by the capture that follows.
try:
    dst = os.lstat(post_dir)
except FileNotFoundError:
    pass
except OSError as exc:
    stop(f"destination_probe_failed path={post_dir} {exc.__class__.__name__}: {exc}")
else:
    fail(f"capture destination exists immediately before capture: mode={dst.st_mode:#o}")

# 5. the state database must be a regular non-link file.
try:
    sst = os.lstat(state_db)
except OSError as exc:
    stop(f"state_db_stat_failed path={state_db} {exc.__class__.__name__}: {exc}")
if not statmod.S_ISREG(sst.st_mode):
    fail(f"state database is not a regular non-link file: mode={sst.st_mode:#o}")

# 6. the capture itself, through the candidate's own API. timestamp is NOT passed:
#    _validate_timestamp(None) uses datetime.now(UTC), so generated_at_utc is the
#    candidate's own clock and not an operator-chosen string. force is NOT passed,
#    so an unexpected artifact at the destination is refused by the candidate too.
try:
    code, report = create_bundle(source=Path(state_db), out_dir=Path(post_dir))
except Exception as exc:
    stop(f"candidate_create_unevaluable: {exc.__class__.__name__}: {exc}")
print(f"C4B_capture_rc={code} verdict={report.get('verdict')} failures={report.get('failures')}")
if code != 0 or report.get("verdict") != "CAPTURED":
    fail(f"candidate capture did not produce a bundle: {report.get('failures')}")

manifest_path = Path(post_dir) / MANIFEST_NAME
try:
    mst = os.lstat(manifest_path)
except OSError as exc:
    stop(f"fresh_manifest_stat_failed {exc.__class__.__name__}: {exc}")
if not statmod.S_ISREG(mst.st_mode):
    fail(f"fresh bundle manifest is not a regular non-link file: mode={mst.st_mode:#o}")
manifest = load(manifest_path)
manifest_sha = sha256_file(manifest_path)
captured = str(manifest.get("generated_at_utc", ""))
if not captured:
    stop("fresh_manifest_missing_generated_at_utc")

# 7. corroborating ordering witnesses. The OS-set nanosecond mtime is strict; the
#    candidate's own second-truncated timestamp may legitimately land inside the
#    rollback's second, so only an EARLIER second is a failure there. Neither is
#    the primary proof — step 4 is.
print(f"C4B_fresh_manifest_mtime_ns={mst.st_mtime_ns} rollback_mtime_ns={pinned[2]}")
print(f"C4B_generated_at_utc={captured} rolled_back_at_utc={rolled}")
if mst.st_mtime_ns <= pinned[2]:
    fail("fresh bundle manifest is not strictly newer than the rollback manifest")
if captured < rolled:
    fail(f"candidate capture clock predates the rollback ({captured} < {rolled})")

payload = {
    "schema": "wpl-p2-c4-stage-b/1",
    "stage_record_path": stage_record,
    "stage_record_sha256": actual_stage_sha,
    "capture_destination": post_dir,
    "post_manifest_path": str(manifest_path),
    "post_manifest_sha256": manifest_sha,
    "post_manifest_dev": mst.st_dev,
    "post_manifest_ino": mst.st_ino,
    "post_manifest_mtime_ns": mst.st_mtime_ns,
    "post_bundle_db_sha256": manifest.get("bundle", {}).get("db_sha256"),
    "post_invariants_sha256": manifest.get("invariants_sha256"),
    "generated_at_utc": captured,
    "rolled_back_at_utc": rolled,
}
for key in ("post_bundle_db_sha256", "post_invariants_sha256"):
    if not isinstance(payload[key], str) or len(payload[key]) != 64:
        fail(f"fresh manifest {key}={payload[key]!r} is not a sha256")
blob = (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode("utf-8")
# Create-once, and BINARY for the same reason as the stage record: the digest
# printed below must be the digest of the bytes actually on disk.
try:
    handle_fd = os.open(capture_record, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
except FileExistsError:
    fail(f"capture record already exists: {capture_record}")
except OSError as exc:
    stop(f"capture_record_not_creatable path={capture_record} {exc.__class__.__name__}: {exc}")
with os.fdopen(handle_fd, "wb") as handle:
    handle.write(blob)
print("C4_POST_MANIFEST_SHA256=" + manifest_sha)
print("C4_POST_BUNDLE_DB_SHA256=" + payload["post_bundle_db_sha256"])
print("C4_POST_INVARIANTS_SHA256=" + payload["post_invariants_sha256"])
print("C4B_capture_record_path=" + capture_record)
print("C4B_capture_record_sha256=" + hashlib.sha256(blob).hexdigest())
PYEOF
case "$cbrc" in
    0) : ;;
    1) c4b_fail "fresh capture refused" ;;
    *) c4b_stop "capture_unevaluable rc=$cbrc" ;;
esac

printf 'C4B_SECTION done\n'
printf 'C4B PASS (one fresh bundle captured downstream of the recorded rollback; the three digests\n'
printf '          above are OUTPUTS to be recorded externally, and NOTHING is verified or compared yet)\n'
