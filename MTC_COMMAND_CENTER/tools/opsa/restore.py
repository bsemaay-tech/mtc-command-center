"""OPS-A restore tool (WP-P0-26, local half) — restore a COMPLETED backup run, verifying byte-hashes.

Consumes one EXPLICIT run id (there is no "latest": greatest-started-run selection was
removed by the WP-P0-26 completion-marker repair because the newest run may be the
interrupted one). Before anything is verified or written the run must carry its completion
evidence — ``runs/<run_id>/COMPLETE.json`` plus ``runs/<run_id>/RUN_MANIFEST.jsonl`` whose
bytes hash to the digest recorded in the marker — and the per-run file records must equal
the run's records in the append-only global manifest. A run without that evidence, or with a
tampered marker/manifest, is REFUSED (rc 3) and nothing is restored.

Reads the append-only manifest, selects the ``file``/``dir`` records of one backup run,
and for every file:

1. hashes the file at its backup location and compares against the manifest SHA-256
   (a tampered or bit-rotted backup is REFUSED — the mismatch is reported, nothing is
   restored from an unverifiable source),
2. writes it to ``<target>/<store_id>/<rel>`` (parents created; existing files are
   overwritten — restore semantics; nothing outside the manifest is ever touched),
3. hashes the restored file and compares again (write-path verification).

``--check-only`` performs step 1 over the whole run and writes nothing — the isolated
integrity proof required before a backup "counts" (plan §12.6.2(c), map #96).

Guarantees: no delete code path (module-wide); UTC-only timestamps; inability to read
the manifest or a backup file is reported as a check-failure, never skipped silently.

Usage:
    python restore.py --config opsa_config.json --run <run_id> --to <target_dir> [--store ID ...]
    python restore.py --config opsa_config.json --run <run_id> --check-only
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from opsa_common import (  # noqa: E402
    RC_CHECK_FAILED, RC_OK, RequiredFieldError, RunNotComplete, load_complete_marker,
    read_jsonl, require_non_empty_string, require_non_empty_string_field,
    resolve_confined_path, run_manifest_path, sha256_file, utc_now_iso,
)

RC_ERROR = 1


def select_run(records: list[dict], run_id: str | None, store_filter: set[str] | None) -> tuple[str | None, list[dict]]:
    """Pick the run's ``file``/``dir`` records from the global manifest for an EXPLICIT run id.

    ``run_id=None`` (the former ``--latest`` selection) is refused with ``ValueError``: the
    newest run may be the interrupted one, so a run is only ever restored by its explicit id
    and only after its completion evidence is verified by the caller.
    Returns (run_id, records). Malformed manifest lines surface as ``record == "_malformed"``
    entries so callers report them instead of skipping.
    """
    if run_id is None:
        raise ValueError("an explicit run id is required; latest-run selection was removed")
    run_ids = [r.get("run_id") for r in records
               if r.get("record") == "run_start" and r.get("run_id")]
    if not run_ids:
        return None, []
    selected = [r for r in records
                if r.get("run_id") == run_id
                and (r.get("record") in ("file", "dir"))
                and (not store_filter or r.get("store_id") in store_filter)]
    return run_id, selected


def verify_completion_evidence(run_dir: Path, run_id: str, global_records: list[dict]) -> dict:
    """Refuse unless the run carries a valid COMPLETE.json + RUN_MANIFEST.jsonl pair whose
    file records equal the global manifest's file records for the run (same rel/sha256/size
    per store), whose declared file count matches, AND whose run the append-only global
    manifest itself closed successfully (exactly one ``run_end`` with ``status == "ok"`` and
    no errors, declaring the same file count). A hand-made pair inside ``runs/<run_id>/`` can
    never stand in for the backup tool's own terminal record. Returns the marker payload."""
    marker = load_complete_marker(run_dir, run_id)  # raises RunNotComplete
    ends = [r for r in global_records
            if r.get("record") == "run_end" and r.get("run_id") == run_id]
    if len(ends) != 1:
        raise RunNotComplete(f"run {run_id}: global manifest carries {len(ends)} run_end "
                             "records for the run (exactly one successful run_end is required)")
    end = ends[0]
    if end.get("status") != "ok" or end.get("errors") != []:
        raise RunNotComplete(f"run {run_id}: global manifest run_end is status="
                             f"{end.get('status')!r} with {len(end.get('errors') or [])} "
                             "error(s); only a run the backup tool closed successfully "
                             "may be restored")
    run_records = read_jsonl(run_manifest_path(run_dir))
    if any(r.get("record") == "_malformed" for r in run_records):
        raise RunNotComplete(f"run {run_id}: per-run manifest has malformed lines")
    header = run_records[0] if run_records else {}
    if header.get("record") != "run_manifest_header" or header.get("run_id") != run_id:
        raise RunNotComplete(f"run {run_id}: per-run manifest header missing or names another run")
    def _key(r: dict) -> tuple:
        return (r.get("store_id"), r.get("rel"), r.get("sha256"), r.get("size"))
    per_run_files = sorted(_key(r) for r in run_records if r.get("record") == "file")
    global_files = sorted(_key(r) for r in global_records
                          if r.get("record") == "file" and r.get("run_id") == run_id)
    if per_run_files != global_files:
        raise RunNotComplete(f"run {run_id}: per-run manifest file records differ from the global manifest")
    declared = marker.get("files")
    if not isinstance(declared, int) or isinstance(declared, bool) or declared != len(per_run_files):
        raise RunNotComplete(f"run {run_id}: completion marker declares files={declared!r}, "
                             f"per-run manifest lists {len(per_run_files)}")
    if end.get("files") != declared:
        raise RunNotComplete(f"run {run_id}: global manifest run_end declares files="
                             f"{end.get('files')!r}, completion marker declares {declared}")
    if any(r.get("readback") != "match" for r in run_records if r.get("record") == "file"):
        raise RunNotComplete(f"run {run_id}: per-run manifest carries a non-matching readback record")
    return marker


def verify_backup_file(record: dict, run_dir: Path) -> tuple[bool, str]:
    """Hash-check one file at its backup location against the manifest record."""
    backup_path = resolve_confined_path(run_dir, record["store_id"], record["rel"])
    try:
        actual = sha256_file(backup_path)
    except OSError as exc:
        return False, f"unreadable: {exc}"
    if actual != record.get("sha256"):
        return False, (f"sha256 mismatch: manifest={str(record.get('sha256'))[:16]}… "
                       f"actual={actual[:16]}…")
    return True, "match"


def run_restore(config_path: Path, run_id: str | None, target: Path | None,
                 check_only: bool = False, store_filter: set[str] | None = None) -> int:
    from opsa_common import load_backup_config  # local import keeps --help fast
    try:
        config = load_backup_config(config_path)
    except (OSError, ValueError) as exc:
        print(f"error: invalid backup config: {exc}", file=sys.stderr)
        return RC_CHECK_FAILED
    backup_root = Path(config["backup_root"])
    manifest_path = backup_root / "manifest.jsonl"
    if not manifest_path.exists():
        print(f"error: manifest not found: {manifest_path}", file=sys.stderr)
        return RC_ERROR

    records = read_jsonl(manifest_path)
    malformed = [r for r in records if r.get("record") == "_malformed"]
    available_run_ids = {r.get("run_id") for r in records
                         if r.get("record") == "run_start" and r.get("run_id")}
    if run_id is None:
        print("error: an explicit --run <run_id> is required (latest-run selection was removed)",
              file=sys.stderr)
        return RC_CHECK_FAILED
    if run_id not in available_run_ids:
        print(f"error: run id not found in manifest: {run_id}", file=sys.stderr)
        return RC_CHECK_FAILED
    resolved, selected = select_run(records, run_id, store_filter)
    if resolved is None:
        print("error: manifest contains no run_start records", file=sys.stderr)
        return RC_CHECK_FAILED
    try:
        resolved = require_non_empty_string(resolved, "run_id", "manifest run")
        validated_paths: list[tuple[str, str]] = []
        for record in selected:
            record_type = require_non_empty_string_field(
                record, "record", "manifest record")
            require_non_empty_string_field(record, "run_id", f"manifest {record_type} record")
            store_id = require_non_empty_string_field(
                record, "store_id", f"manifest {record_type} record")
            rel = require_non_empty_string_field(
                record, "rel", f"manifest {record_type} record")
            if record_type == "file":
                require_non_empty_string_field(record, "sha256", "manifest file record")
            validated_paths.append((store_id, rel))
        run_dir = resolve_confined_path(backup_root, "runs", resolved)
        for store_id, rel in validated_paths:
            resolve_confined_path(run_dir, store_id, rel)
            if not check_only and target is not None:
                resolve_confined_path(target, store_id, rel)
    except RequiredFieldError as exc:
        print(json.dumps({"status": "check_failed", "error": "invalid_manifest_record",
                          "field": exc.field, "detail": str(exc), "run_id": resolved},
                         ensure_ascii=False), file=sys.stderr)
        return RC_CHECK_FAILED
    except (TypeError, ValueError) as exc:
        print(f"error: unsafe manifest path for run {resolved}: {exc}", file=sys.stderr)
        return RC_CHECK_FAILED

    # Completion evidence gate (WP-P0-26 repair): no COMPLETE.json / no RUN_MANIFEST.jsonl /
    # tampered pair / records differing from the global manifest => refuse before any hash
    # check or write. Field and confinement validation above already ran on the manifest.
    try:
        marker = verify_completion_evidence(run_dir, resolved, records)
    except RunNotComplete as exc:
        print(json.dumps({"status": "check_failed", "error": "run_not_complete",
                          "detail": str(exc), "run_id": resolved}, ensure_ascii=False),
              file=sys.stderr)
        return RC_CHECK_FAILED

    mode = "check-only" if check_only else "restore"
    print(json.dumps({"mode": mode, "run_id": resolved, "manifest": str(manifest_path),
                      "target": str(target) if target else None,
                      "records_selected": len(selected),
                      "completion_marker": "verified",
                      "run_manifest_sha256": marker.get("run_manifest_sha256"),
                      "manifest_malformed_lines": len(malformed)}, ensure_ascii=False))

    errors: list[str] = [f"malformed manifest line {m.get('line_number')}" for m in malformed]
    verified = 0
    restored = 0
    overwritten = 0
    dirs_recreated = 0  # counted only when a directory is actually created (not in --check-only)

    file_records = [record for record in selected if record.get("record") == "file"]
    run_end = next((record for record in reversed(records)
                    if record.get("record") == "run_end"
                    and record.get("run_id") == resolved), {})
    declared_files = run_end.get("files", "unknown")
    declared_files_valid = (isinstance(declared_files, int)
                            and not isinstance(declared_files, bool)
                            and declared_files >= 0)
    declares_files = declared_files_valid and declared_files > 0
    incomplete_empty_run = (not run_end or run_end.get("status") != "ok"
                            or not declared_files_valid)
    if not file_records and (check_only or not selected or declares_files or incomplete_empty_run):
        msg = (f"run {resolved} has nothing to verify: selected zero file records "
               f"(manifest declares files={declared_files}, status={run_end.get('status', 'missing')})")
        errors.append(msg)
        print(f"ERROR {msg}", file=sys.stderr)
        print(json.dumps({"mode": mode, "run_id": resolved, "status": "failed",
                          "verified_against_manifest": 0, "restored": 0,
                          "overwritten": 0, "dirs_recreated": 0,
                          "errors": len(errors), "finished_at": utc_now_iso()},
                         ensure_ascii=False))
        return RC_CHECK_FAILED

    for record in selected:
        if record.get("record") == "dir":
            if not check_only and target is not None:
                resolve_confined_path(target, record["store_id"], record["rel"]).mkdir(
                    parents=True, exist_ok=True)
                dirs_recreated += 1
            continue

        ok, detail = verify_backup_file(record, run_dir)
        if not ok:
            msg = f"{record.get('store_id')}/{record.get('rel')}: {detail}"
            errors.append(msg)
            print(f"FAIL  {msg}", file=sys.stderr)
            continue
        verified += 1

        if check_only or target is None:
            print(f"VERIFIED {record['store_id']}/{record['rel']}")
            continue

        dest = resolve_confined_path(target, record["store_id"], record["rel"])
        existed = dest.exists()
        try:
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(
                resolve_confined_path(run_dir, record["store_id"], record["rel"]), dest)
            written_hash = sha256_file(dest)
        except OSError as exc:
            msg = f"{record.get('store_id')}/{record.get('rel')}: restore failed: {exc}"
            errors.append(msg)
            print(f"ERROR {msg}", file=sys.stderr)
            continue
        if written_hash != record.get("sha256"):
            msg = (f"{record.get('store_id')}/{record.get('rel')}: "
                   f"post-restore hash mismatch (write path)")
            errors.append(msg)
            print(f"ERROR {msg}", file=sys.stderr)
            continue
        restored += 1
        overwritten += 1 if existed else 0
        print(f"RESTORED {record['store_id']}/{record['rel']} sha256={record['sha256'][:16]}…"
              + (" (overwrote existing)" if existed else ""))

    status = "ok" if not errors else "failed"
    print(json.dumps({"mode": mode, "run_id": resolved, "status": status,
                      "verified_against_manifest": verified, "restored": restored,
                      "overwritten": overwritten, "dirs_recreated": dirs_recreated,
                      "errors": len(errors), "finished_at": utc_now_iso()},
                     ensure_ascii=False))
    if errors:
        for err in errors:
            print(f"error: {err}", file=sys.stderr)
    return RC_OK if not errors else RC_ERROR


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="OPS-A restore from manifest with byte-hash verification (no delete path)")
    parser.add_argument("--config", required=True, help="backup config JSON")
    # ``--latest`` no longer exists: a restore names one explicit COMPLETED run id.
    parser.add_argument("--run", required=True,
                        help="run_id to restore (explicit; must carry COMPLETE.json + RUN_MANIFEST.jsonl)")
    parser.add_argument("--to", help="target directory to restore into")
    parser.add_argument("--store", action="append", default=[],
                        help="restrict to this store id (repeatable)")
    parser.add_argument("--check-only", action="store_true",
                        help="verify the run's hashes without writing anything")
    args = parser.parse_args(argv)
    if not args.check_only and not args.to:
        parser.error("--to is required unless --check-only is given")
    store_filter = set(args.store) if args.store else None
    return run_restore(Path(args.config), run_id=args.run,
                       target=Path(args.to) if args.to else None,
                       check_only=args.check_only, store_filter=store_filter)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
