"""OPS-A restore tool (WP-P0-26, local half) — restore a backup run, verifying byte-hashes.

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
    python restore.py --config opsa_config.json --latest --to <target_dir>
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
    RC_CHECK_FAILED, RC_OK, read_jsonl, resolve_confined_path, sha256_file,
    utc_now_iso,
)

RC_ERROR = 1


def select_run(records: list[dict], run_id: str | None, store_filter: set[str] | None) -> tuple[str | None, list[dict]]:
    """Pick the run's records. ``run_id=None`` means --latest (highest run_id string).

    Returns (resolved_run_id, records). Malformed manifest lines surface as
    ``record == "_malformed"`` entries so callers report them instead of skipping.
    """
    run_ids = [r.get("run_id") for r in records
               if r.get("record") == "run_start" and r.get("run_id")]
    if not run_ids:
        return None, []
    resolved = run_id if run_id is not None else max(run_ids)
    selected = [r for r in records
                if r.get("run_id") == resolved
                and (r.get("record") in ("file", "dir"))
                and (not store_filter or r.get("store_id") in store_filter)]
    return resolved, selected


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
    if run_id is not None and run_id not in available_run_ids:
        print(f"error: run id not found in manifest: {run_id}", file=sys.stderr)
        return RC_CHECK_FAILED
    resolved, selected = select_run(records, run_id, store_filter)
    if resolved is None:
        print("error: manifest contains no run_start records", file=sys.stderr)
        return RC_CHECK_FAILED
    try:
        run_dir = resolve_confined_path(backup_root, "runs", resolved)
        for record in selected:
            resolve_confined_path(run_dir, record.get("store_id"), record.get("rel"))
            if not check_only and target is not None:
                resolve_confined_path(target, record.get("store_id"), record.get("rel"))
    except (TypeError, ValueError) as exc:
        print(f"error: unsafe manifest path for run {resolved}: {exc}", file=sys.stderr)
        return RC_CHECK_FAILED

    mode = "check-only" if check_only else "restore"
    print(json.dumps({"mode": mode, "run_id": resolved, "manifest": str(manifest_path),
                      "target": str(target) if target else None,
                      "records_selected": len(selected),
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
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--run", help="run_id to restore (from manifest)")
    group.add_argument("--latest", action="store_true", help="use the newest run in the manifest")
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
