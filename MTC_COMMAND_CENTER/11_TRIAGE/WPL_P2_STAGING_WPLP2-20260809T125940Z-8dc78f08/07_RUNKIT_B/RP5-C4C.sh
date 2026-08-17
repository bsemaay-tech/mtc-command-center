# ===== BLOCK-ID: RP5-C4C ===== [EXECUTABLE PROPOSAL BLOCK]
# WP-L Phase 2 — C4 stage C: verification and protected equality (PROPOSED DESIGN).
# Candidate: 2ce41e34bceb599d80af24c5c33d835820ec321b. NOT host-authorized.
# Mutation class: read-only. Reads the two create-once stage records, the rollback
# manifest, the accepted C3 manifest and the fresh bundle; writes nothing except
# its own RP0 evidence leaf. No service action, no credential read, no network,
# no POST /api/arm, no broker/exchange/order/TESTNET/mainnet/economic action.
# Requires RP0-LIB and RP0-BOOTSTRAP, and runs only after RP5-C4B.
#
# The three post-rollback digests ARE inputs here, and that is now sound: they
# were produced by stage B AFTER the rollback and are re-bound to stage B's
# create-once capture record and to the live artifact's own identity. String
# equality of two supplied variables is still NOT the predicate — it passes for
# stale values, for values never derived from any bundle, and for the accepted C3
# bundle handed back as its own "post" artifact. Filename and byte-count equality
# remain DIAGNOSTIC ONLY and are never described as byte equality.
set -Eeuo pipefail

RELEASE_ROOT="/opt/mtc-bridge/releases/2ce41e34bceb599d80af24c5c33d835820ec321b/IBKR_PAPER_BRIDGE"
ROLLBACK_MANIFEST="/etc/mtc-bridge/rollback_manifest.json"

: "${C4_STAGE_RECORD:?stage-A record path is required}"
: "${C4_STAGE_RECORD_SHA256:?externally recorded stage-A record sha256 is required}"
: "${C4_CAPTURE_RECORD:?stage-B capture record path is required}"
: "${C4_CAPTURE_RECORD_SHA256:?externally recorded stage-B capture record sha256 is required}"
: "${C4_STATE_MANIFEST_FILE:?accepted C3 bundle manifest file path is required}"
: "${C4_STATE_MANIFEST_SHA256:?externally recorded C3 manifest FILE sha256 is required}"
: "${C4_PRE_INVARIANTS_SHA256:?preregistered pre-rollback protected-invariant hash is required}"
: "${C4_POST_BUNDLE_DIR:?fresh post-rollback bundle directory is required}"
: "${C4_POST_MANIFEST_SHA256:?externally recorded fresh post-rollback manifest FILE sha256 is required}"
: "${C4_POST_BUNDLE_DB_SHA256:?externally recorded fresh post-rollback bundle db sha256 is required}"
: "${C4_POST_INVARIANTS_SHA256:?externally recorded fresh post-rollback invariants sha256 is required}"
: "${PY:?candidate venv interpreter path is required}"

c4c_stop() { printf 'C4C_STOP reason=%s\n' "$*"; exit 3; }
c4c_fail() { printf 'C4C_FAIL reason=%s\n' "$*"; exit 1; }

printf 'C4C_SECTION step0_prerequisites\n'
for p in "$C4_STAGE_RECORD" "$C4_CAPTURE_RECORD" "$C4_STATE_MANIFEST_FILE" "$ROLLBACK_MANIFEST"; do
    kind="$(rp0_probe_path "$p")" || exit 3
    [ "$kind" = "regular" ] || c4c_fail "expected a regular non-link file, kind=$kind path=$p"
done
kind="$(rp0_probe_path "$C4_POST_BUNDLE_DIR")" || exit 3
[ "$kind" = "dir" ] || c4c_fail "fresh bundle directory kind=$kind path=$C4_POST_BUNDLE_DIR"

printf 'C4C_SECTION step1_chain_verify_and_equality\n'
pbrc=0
"$PY" - "$RELEASE_ROOT" "$C4_STAGE_RECORD" "$C4_STAGE_RECORD_SHA256" "$C4_CAPTURE_RECORD" \
    "$C4_CAPTURE_RECORD_SHA256" "$C4_STATE_MANIFEST_FILE" "$C4_STATE_MANIFEST_SHA256" \
    "$C4_PRE_INVARIANTS_SHA256" "$C4_POST_BUNDLE_DIR" "$C4_POST_MANIFEST_SHA256" \
    "$C4_POST_BUNDLE_DB_SHA256" "$C4_POST_INVARIANTS_SHA256" "$ROLLBACK_MANIFEST" <<'PYEOF' || pbrc=$?
import hashlib, json, os, stat as statmod, sys
from pathlib import Path

(release_root, stage_record, stage_record_sha, capture_record, capture_record_sha,
 c3_manifest, c3_manifest_sha, pre_inv_sha, post_dir, post_manifest_sha,
 post_db_sha, post_inv_sha, rollback_manifest) = sys.argv[1:14]

PROTECTED_FIELDS = (
    "schema_version", "app_state", "counts", "open_trades", "live_orders",
    "closed_trades", "max_ids", "environments", "risk_days",
)


def stop(reason):
    print(f"C4C_STOP reason={reason}")
    raise SystemExit(3)


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
    from tools.wal_state_bundle import MANIFEST_NAME, verify_bundle
except Exception as exc:
    stop(f"candidate_api_import_failed: {exc.__class__.__name__}: {exc}")

problems = []

# 1. both create-once records are exactly the externally recorded ones, and the
#    capture record names the stage record it was produced from.
actual_stage_sha = sha256_file(stage_record)
actual_capture_sha = sha256_file(capture_record)
print(f"C4C_stage_record_sha256={actual_stage_sha}")
print(f"C4C_capture_record_sha256={actual_capture_sha}")
if actual_stage_sha != stage_record_sha.lower():
    problems.append("stage record sha256 does not match the externally recorded value")
if actual_capture_sha != capture_record_sha.lower():
    problems.append("capture record sha256 does not match the externally recorded value")
stage = load(stage_record)
capture = load(capture_record)
if stage.get("schema") != "wpl-p2-c4-stage-a/1" or capture.get("schema") != "wpl-p2-c4-stage-b/1":
    stop("record_schema_unrecognised")
if capture.get("stage_record_sha256") != actual_stage_sha:
    problems.append("capture record was not produced from this stage record")
if stage.get("capture_destination") != post_dir or capture.get("capture_destination") != post_dir:
    problems.append("the records do not agree with the bundle directory under verification")
if stage.get("c3_manifest_sha256") != c3_manifest_sha or stage.get("pre_invariants_sha256") != pre_inv_sha:
    problems.append("the accepted C3 identity supplied here is not the one stage A rolled back against")

# 2. the accepted C3 manifest is still exactly the accepted artifact.
actual_c3_sha = sha256_file(c3_manifest)
print(f"C4C_c3_manifest_sha256={actual_c3_sha}")
if actual_c3_sha != c3_manifest_sha.lower():
    problems.append("accepted C3 manifest FILE sha256 changed since stage A")

# 3. the SAME rollback event is still live and unrewritten.
try:
    rst = os.lstat(rollback_manifest)
except OSError as exc:
    stop(f"rollback_manifest_stat_failed {exc.__class__.__name__}: {exc}")
live_rollback = (rst.st_dev, rst.st_ino, rst.st_mtime_ns, sha256_file(rollback_manifest))
pinned_rollback = (stage.get("rollback_manifest_dev"), stage.get("rollback_manifest_ino"),
                   stage.get("rollback_manifest_mtime_ns"), stage.get("rollback_manifest_sha256"))
if live_rollback != pinned_rollback:
    problems.append("the rollback manifest changed after stage A: the chain no longer describes one rollback")

# 4. the artifact verified here is the one stage B created, unchanged since.
post_manifest_path = Path(post_dir) / MANIFEST_NAME
try:
    mst = os.lstat(post_manifest_path)
except OSError as exc:
    stop(f"post_manifest_stat_failed path={post_manifest_path} {exc.__class__.__name__}: {exc}")
if not statmod.S_ISREG(mst.st_mode):
    stop(f"post_bundle_manifest_not_a_regular_file path={post_manifest_path}")
actual_post_manifest_sha = sha256_file(post_manifest_path)
live_post = (mst.st_dev, mst.st_ino, mst.st_mtime_ns, actual_post_manifest_sha)
pinned_post = (capture.get("post_manifest_dev"), capture.get("post_manifest_ino"),
               capture.get("post_manifest_mtime_ns"), capture.get("post_manifest_sha256"))
print(f"C4C_post_identity_live={live_post}")
print(f"C4C_post_identity_pinned={pinned_post}")
if live_post != pinned_post:
    problems.append("the fresh bundle manifest is not the artifact stage B captured, or changed since")
print(f"C4C_post_manifest_file_sha256={actual_post_manifest_sha}")
if actual_post_manifest_sha != post_manifest_sha.lower():
    problems.append("fresh bundle manifest FILE sha256 does not match the recorded capture value")

# 5. the post bundle must be a DIFFERENT artifact from the accepted C3 bundle.
try:
    c3st = os.lstat(c3_manifest)
except OSError as exc:
    stop(f"identity_probe_failed: {exc.__class__.__name__}: {exc}")
print(f"C4C_post_bundle_identity=({mst.st_dev},{mst.st_ino}) c3_identity=({c3st.st_dev},{c3st.st_ino})")
if (c3st.st_dev, c3st.st_ino) == (mst.st_dev, mst.st_ino):
    problems.append("post bundle manifest IS the accepted C3 manifest: no fresh capture happened")

# 6. the recorded digests must be the capture's own, and the ordering witnesses
#    recorded by stage B must still hold. The structural proof stays stage A/B's
#    absent-then-create sequence; these are corroboration.
if capture.get("post_bundle_db_sha256") != post_db_sha.lower():
    problems.append("recorded post bundle db sha256 is not the value stage B captured")
if capture.get("post_invariants_sha256") != post_inv_sha.lower():
    problems.append("recorded post invariants sha256 is not the value stage B captured")
captured_at = str(capture.get("generated_at_utc") or "")
rolled_at = str(stage.get("rolled_back_at_utc") or "")
print(f"C4C_generated_at_utc={captured_at} rolled_back_at_utc={rolled_at} "
      f"post_mtime_ns={pinned_post[2]} rollback_mtime_ns={pinned_rollback[2]}")
if not captured_at or not rolled_at:
    stop("capture_or_rollback_timestamp_missing")
if not isinstance(pinned_post[2], int) or not isinstance(pinned_rollback[2], int):
    stop("recorded_mtime_ns_not_an_integer")
if pinned_post[2] <= pinned_rollback[2]:
    problems.append("the recorded capture is not strictly newer than the recorded rollback")
if captured_at < rolled_at:
    problems.append(f"the capture clock predates the rollback ({captured_at} < {rolled_at}): it is stale")

pre_manifest = load(c3_manifest)
post_manifest = load(post_manifest_path)

# 7. neither hash may be a free string: each must be its own bundle's value.
if pre_manifest.get("invariants_sha256") != pre_inv_sha:
    problems.append("preregistered pre-rollback hash is not bound to the accepted C3 bundle")
if post_manifest.get("invariants_sha256") != post_inv_sha:
    problems.append("recorded post-rollback hash is not the fresh bundle's own value")

# 8. candidate verification with BOTH exact expected hashes; fail-closed.
try:
    code, report = verify_bundle(bundle_dir=Path(post_dir),
                                 expect_bundle_sha256=post_db_sha,
                                 expect_invariants_sha256=post_inv_sha)
except Exception as exc:
    stop(f"candidate_verify_unevaluable: {exc.__class__.__name__}: {exc}")
print(f"C4C_post_bundle_verify_rc={code} verdict={report.get('verdict')} "
      f"failures={report.get('failures')}")
if code != 0 or report.get("verdict") != "VALID":
    problems.append(f"candidate verify rejected the fresh post-rollback bundle: {report.get('failures')}")

# 9. protected equality: the candidate hash AND every protected field.
if post_inv_sha != pre_inv_sha:
    problems.append(f"protected invariants changed across rollback (pre={pre_inv_sha} post={post_inv_sha})")
pre_inv = pre_manifest.get("invariants", {})
post_inv = post_manifest.get("invariants", {})
for field in PROTECTED_FIELDS:
    if pre_inv.get(field) != post_inv.get(field):
        problems.append(f"protected invariant field differs across rollback: {field}")

if problems:
    print("C4C_post_bundle_problems=" + "; ".join(problems))
    raise SystemExit(1)
print("C4C_post_rollback_bundle_verified=yes")
PYEOF
case "$pbrc" in
    0) : ;;
    1) c4c_fail "fresh post-rollback bundle binding failed (see C4C_post_bundle_problems)" ;;
    *) c4c_stop "post_rollback_bundle_unevaluable rc=$pbrc" ;;
esac
printf 'C4C_invariants_equal=yes sha256=%s\n' "$C4_POST_INVARIANTS_SHA256"

printf 'C4C_SECTION done\n'
printf 'C4C PASS (protected state preserved across the rollback, on a bundle captured downstream of\n'
printf '          it; no start, unmask or recovery is authorised by this result)\n'
