# ===== BLOCK-ID: RP4-C3 ===== [EXECUTABLE PROPOSAL BLOCK]
"""WP-L Phase 2 — C3 restore-into-temp verification (PROPOSED DESIGN).

Candidate: 2ce41e34bceb599d80af24c5c33d835820ec321b. NOT host-authorized.

Uses only the candidate's public API. Never invents a `restore` subcommand, never
copies files and calls it a restore, never deletes an artifact, never touches the
production database read-write, never reads a credential, never issues POST /api/arm.

rc contract: 0 = PASS, 1 = FAIL, 3 = COULD NOT EVALUATE (STOP).
"""

import hashlib
import json
import os
import sqlite3
import sys
from pathlib import Path

PASS_RC, FAIL_RC, STOP_RC = 0, 1, 3

# Protected invariant fields, exactly the keys candidate collect_invariants
# returns (wal_state_bundle.py:457-467).
PROTECTED_FIELDS = (
    "schema_version", "app_state", "counts", "open_trades", "live_orders",
    "closed_trades", "max_ids", "environments", "risk_days",
)


class Fail(Exception):
    """A genuine predicate failure."""


class Stop(Exception):
    """Could not evaluate — always stops the stage, never re-read as FAIL."""


def load_candidate_api(release_root: Path):
    """Import the candidate's own public API. No reimplementation of its logic."""
    sys.path.insert(0, str(release_root))
    try:
        from tools.wal_state_bundle import (  # noqa: E402
            BUNDLE_DB_NAME, FORBIDDEN_SIDECARS, MANIFEST_NAME,
            collect_invariants, invariants_hash, verify_bundle,
        )
    except Exception as exc:  # import/tool error is never a FAIL
        raise Stop(f"candidate_api_import_failed: {exc.__class__.__name__}: {exc}") from exc
    return {
        "collect_invariants": collect_invariants,
        "invariants_hash": invariants_hash,
        "verify_bundle": verify_bundle,
        "MANIFEST_NAME": MANIFEST_NAME,
        "BUNDLE_DB_NAME": BUNDLE_DB_NAME,
        "FORBIDDEN_SIDECARS": FORBIDDEN_SIDECARS,
    }


def candidate_verify(api, bundle_dir: Path, expect_bundle_db_sha256: str,
                     expect_invariants_sha256: str, out=print) -> None:
    """Re-verify the accepted bundle with the CANDIDATE's own verification, in
    THIS evaluation, with both exact expected hashes.

    `verify_bundle(bundle_dir, expect_bundle_sha256, expect_invariants_sha256)`
    (wal_state_bundle.py:1125-1205) additionally validates the full manifest
    contract, the manifest integrity hash, the source/arrival snapshot contract,
    the sidecar-hash contract, source and bundle integrity/FK cleanliness, and
    the re-derived invariants. A prior `verify` PASS is a statement about a past
    run; the local checks further down are a partial reimplementation. Neither
    is this predicate, and neither replaces it.

    Fail-closed adjudication: an exception is COULD NOT EVALUATE, and only the
    exact accepted verdict `(0, "VALID")` may proceed. Both expected hashes are
    REQUIRED by the candidate itself: it raises `BundleError` when either is
    missing or is not 64 hex characters.
    """
    try:
        code, report = api["verify_bundle"](
            bundle_dir=bundle_dir,
            expect_bundle_sha256=expect_bundle_db_sha256,
            expect_invariants_sha256=expect_invariants_sha256,
        )
    except Exception as exc:
        raise Stop(f"candidate_verify_unevaluable: {exc.__class__.__name__}: {exc}") from exc
    verdict = report.get("verdict")
    failures = report.get("failures")
    out(f"C3_candidate_verify_rc={code} verdict={verdict} failures={failures}")
    if code != 0 or verdict != "VALID":
        raise Fail(
            f"candidate verify did not return the accepted verdict "
            f"(rc={code} verdict={verdict} failures={failures})"
        )


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def identity(path: Path):
    """(device, inode) from lstat — never follows a link."""
    st = os.lstat(path)
    return (st.st_dev, st.st_ino)


def open_readonly(db_path: Path) -> sqlite3.Connection:
    """Open the bundle DB strictly read-only, in the candidate's own URI form
    (`mode=ro`, wal_state_bundle.py:342-381). The source is never mutated."""
    try:
        uri = f"{db_path.resolve().as_uri()}?mode=ro"
        conn = sqlite3.connect(uri, uri=True)
        conn.execute("SELECT name FROM sqlite_master LIMIT 1").fetchone()
    except (OSError, ValueError, sqlite3.Error) as exc:
        raise Stop(f"readonly_open_failed: {exc.__class__.__name__}: {exc}") from exc
    return conn


def restore_into(src_conn: sqlite3.Connection, dst_path: Path) -> sqlite3.Connection:
    """Restore through the EXACT candidate primitive `src_conn.backup(dst_conn)`
    (wal_state_bundle.py:797-806) into a FRESH destination. A file copy is not a
    restore. The destination must not pre-exist as an object OR as a link."""
    if dst_path.is_symlink():
        raise Fail(f"restore destination is a symlink: {dst_path}")
    if dst_path.exists():
        raise Fail(f"restore destination already exists: {dst_path}")
    try:
        dst_conn = sqlite3.connect(str(dst_path))
        src_conn.backup(dst_conn)
        dst_conn.execute("PRAGMA journal_mode=DELETE")
        dst_conn.commit()
    except (OSError, sqlite3.Error) as exc:
        raise Stop(f"backup_failed: {exc.__class__.__name__}: {exc}") from exc
    return dst_conn


def integrity_and_fk(conn: sqlite3.Connection):
    """quick_check and foreign_key_check on the RESTORED connection."""
    try:
        qc = ";".join(str(r[0]) for r in conn.execute("PRAGMA quick_check").fetchall())
        fk = len(conn.execute("PRAGMA foreign_key_check").fetchall())
    except sqlite3.Error as exc:
        raise Stop(f"integrity_probe_failed: {exc.__class__.__name__}: {exc}") from exc
    return qc, fk


def assert_no_sidecars(db_path: Path, forbidden) -> None:
    """No `-wal`/`-shm`/`-journal` beside the bundle or restored database
    (candidate forbidden set, wal_state_bundle.py:87, :568-569)."""
    present = [
        db_path.with_name(db_path.name + suffix).name
        for suffix in forbidden
        if db_path.with_name(db_path.name + suffix).exists()
    ]
    if present:
        raise Fail(f"sidecar present beside {db_path.name}: {','.join(present)}")


def run(source_db: Path, bundle_dir: Path, restore_root: Path, release_root: Path,
        expect_manifest_file_sha256: str, expect_bundle_db_sha256: str,
        expect_invariants_sha256: str, out=print) -> int:
    """One evaluation. Preserves EVERY artifact: nothing is deleted on any path.

    The three `expect_*` arguments are the externally recorded acceptance values
    for this bundle. They are inputs, never read back out of the manifest: a
    manifest cannot attest to its own acceptance.
    """
    api = load_candidate_api(release_root)
    manifest_path = bundle_dir / api["MANIFEST_NAME"]
    bundle_db = bundle_dir / api["BUNDLE_DB_NAME"]

    # 1. External manifest-FILE sha, recorded separately from the hashes the
    #    manifest embeds. A manifest cannot attest to its own file identity.
    if not manifest_path.is_file():
        raise Stop(f"bundle manifest is not a regular file: {manifest_path}")
    actual_manifest_file_sha = sha256_file(manifest_path)
    out(f"C3_manifest_file_sha256={actual_manifest_file_sha}")
    if actual_manifest_file_sha != expect_manifest_file_sha256:
        raise Fail("bundle manifest FILE sha256 does not match the accepted value")

    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise Stop(f"manifest_unreadable: {exc.__class__.__name__}: {exc}") from exc

    expect_bundle_db_sha = manifest["bundle"]["db_sha256"]
    expect_invariants_sha = manifest["invariants_sha256"]
    expect_invariants = manifest["invariants"]

    # 2. The manifest's own hashes must be the externally recorded accepted
    #    ones. Without this, every check below would be self-referential.
    if expect_bundle_db_sha != expect_bundle_db_sha256:
        raise Fail("manifest bundle db_sha256 is not the externally recorded accepted value")
    if expect_invariants_sha != expect_invariants_sha256:
        raise Fail("manifest invariants_sha256 is not the externally recorded accepted value")

    # 3. MANDATORY candidate re-verification, with both exact expected hashes,
    #    BEFORE anything is restored. Nothing below may run if it does not
    #    return the exact accepted verdict.
    candidate_verify(api, bundle_dir, expect_bundle_db_sha256,
                     expect_invariants_sha256, out=out)

    # 4. Bundle DB hash equality, and no sidecar in the bundle root.
    if not bundle_db.is_file() or bundle_db.is_symlink():
        raise Fail(f"bundle database is not a regular file: {bundle_db}")
    actual_bundle_db_sha = sha256_file(bundle_db)
    out(f"C3_bundle_db_sha256={actual_bundle_db_sha}")
    if actual_bundle_db_sha != expect_bundle_db_sha:
        raise Fail("bundle database sha256 does not match the accepted manifest value")
    assert_no_sidecars(bundle_db, api["FORBIDDEN_SIDECARS"])

    # 5. Fresh, no-clobber restore root. NEVER deleted, on any exit path.
    if restore_root.is_symlink():
        raise Fail(f"restore root is a symlink: {restore_root}")
    if restore_root.exists():
        raise Fail(f"restore root already exists: {restore_root}")
    try:
        restore_root.mkdir(mode=0o700)
    except OSError as exc:
        raise Stop(f"restore_root_allocation_failed: {exc.__class__.__name__}: {exc}") from exc
    restored_db = restore_root / "restored.db"

    # 6. Read-only source connection; restore via src_conn.backup(dst_conn).
    src_conn = open_readonly(bundle_db)
    try:
        dst_conn = restore_into(src_conn, restored_db)
    finally:
        src_conn.close()

    try:
        # 7. quick_check and foreign_key_check on the RESTORED connection.
        qc, fk = integrity_and_fk(dst_conn)
        out(f"C3_restored_quick_check={qc}")
        out(f"C3_restored_fk_violations={fk}")
        if qc != "ok":
            raise Fail(f"restored quick_check != ok ({qc})")
        if fk != 0:
            raise Fail(f"restored foreign_key_check found {fk} violation(s)")

        # 8. Candidate public API on the RESTORED CONNECTION, then candidate hash.
        try:
            restored_invariants = api["collect_invariants"](dst_conn)
            restored_hash = api["invariants_hash"](restored_invariants)
        except Exception as exc:
            raise Stop(f"invariant_derivation_failed: {exc.__class__.__name__}: {exc}") from exc
        out(f"C3_restored_invariants_sha256={restored_hash}")
    finally:
        dst_conn.close()

    # 9. Protected equality: the candidate hash AND every protected field.
    if restored_hash != expect_invariants_sha:
        raise Fail("restored invariants hash does not equal the accepted bundle value")
    for field in PROTECTED_FIELDS:
        if restored_invariants.get(field) != expect_invariants.get(field):
            raise Fail(f"protected invariant field differs after restore: {field}")
    out("C3_protected_fields_equal=yes")

    # 10. Identity separation and sidecar absence in the restore root.
    idents = {
        "source": identity(source_db),
        "bundle": identity(bundle_db),
        "restored": identity(restored_db),
    }
    out("C3_identity=" + json.dumps({k: list(v) for k, v in idents.items()}, sort_keys=True))
    if len(set(idents.values())) != 3:
        raise Fail(f"source/bundle/restored are not three distinct files: {idents}")
    assert_no_sidecars(restored_db, api["FORBIDDEN_SIDECARS"])
    out("C3_sidecars_absent=yes")

    out("C3 PASS")
    return PASS_RC


def main(argv) -> int:
    """Artifacts are preserved under distinct labels; nothing is published as
    accepted on a failing path and nothing partial is ever deleted."""
    (source_db, bundle_dir, restore_root, release_root, expect_manifest_file_sha256,
     expect_bundle_db_sha256, expect_invariants_sha256) = argv[1:8]
    try:
        return run(Path(source_db), Path(bundle_dir), Path(restore_root),
                   Path(release_root), expect_manifest_file_sha256,
                   expect_bundle_db_sha256, expect_invariants_sha256)
    except Fail as exc:
        print(f"C3_FAIL reason={exc}")
        print(f"C3_ARTIFACTS_PRESERVED label=failed root={restore_root}")
        return FAIL_RC
    except Stop as exc:
        print(f"C3_STOP reason={exc}")
        print(f"C3_ARTIFACTS_PRESERVED label=stopped root={restore_root}")
        return STOP_RC


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
