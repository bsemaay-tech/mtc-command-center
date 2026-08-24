"""OPS-A backup tool (WP-P0-26, local half) — copy evidence stores to a second location.

Copies every configured evidence-store tree into a per-run directory under the
configured ``backup_root``, hashing every file (SHA-256, raw bytes) and appending one
record per file to the append-only manifest ``<backup_root>/manifest.jsonl``.

Guarantees (see opsa_common module docstring):
- **No delete code path.** This tool only creates and overwrites files. It can never
  delete or truncate anything — protected classes are safe by construction.
- **Append-only manifest.** Opened in append mode; never rewritten or truncated.
- **Read-back verification.** Every copied file is re-hashed at its backup location and
  compared to the source hash before the record is marked ``readback=match``.
- **Honest partial-failure reporting.** A missing store, unreadable file or readback
  mismatch is recorded and reported, never silently skipped; the run exits rc 1.

Dry-run (``--dry-run``) walks and hashes the sources and prints the plan but writes
nothing — no run directory, no manifest records.

Usage:
    python backup.py --config opsa_config.json [--dry-run] [--store STORE_ID ...]

Config schema: see config.example.json (``mtc.opsa_backup_config/v1``).

Reuse record: CLI subcommand shape and UTC-stamped run naming adapted from
``02_MTC_BACKTEST/scripts/backup_restore.py``; the tarball format was NOT reused —
this tool needs per-file hashes, an append-only manifest and byte-verification, which
a monolithic tar.gz cannot give without re-inventing a manifest inside the archive.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from opsa_common import (  # noqa: E402
    MANIFEST_SCHEMA, RC_CHECK_FAILED, RC_OK, append_jsonl, load_backup_config,
    resolve_confined_path, run_id_for, sha256_file, utc_now, utc_now_iso,
)

RC_ERROR = 1


def iter_tree(base: Path):
    """Deterministic (sorted) walk of a directory tree, never following links/junctions.

    Yields ("file", path, rel) / ("dir", path, rel) / ("skipped", path, rel, reason).
    ``rel`` is POSIX-style relative to ``base``.
    """
    def _walk(dir_path: Path, prefix: str):
        try:
            entries = sorted(dir_path.iterdir(), key=lambda p: p.name)
        except OSError as exc:
            yield ("skipped", dir_path, prefix, f"unreadable_dir: {exc}")
            return
        for entry in entries:
            rel = f"{prefix}{entry.name}"
            if entry.is_symlink():
                yield ("skipped", entry, rel, "symlink")
                continue
            if hasattr(os.path, "isjunction") and os.path.isjunction(entry):
                yield ("skipped", entry, rel, "junction")
                continue
            if entry.is_dir():
                children = list(_walk(entry, rel + "/"))
                if not any(item[0] in ("file", "dir") for item in children):
                    yield ("dir", entry, rel)  # preserve empty directories
                yield from children
            elif entry.is_file():
                yield ("file", entry, rel)
            else:
                yield ("skipped", entry, rel, "special_file")

    yield from _walk(Path(base), "")


def run_backup(config_path: Path, dry_run: bool = False, store_filter: set[str] | None = None) -> int:
    try:
        config = load_backup_config(config_path)
    except (OSError, ValueError) as exc:
        print(f"error: invalid backup config: {exc}", file=sys.stderr)
        return RC_CHECK_FAILED
    backup_root = Path(config["backup_root"])
    stores = config["stores"]
    if store_filter:
        known = {s["id"] for s in stores}
        unknown = store_filter - known
        if unknown:
            print(f"error: --store ids not in config: {sorted(unknown)}", file=sys.stderr)
            return RC_ERROR
        stores = [s for s in stores if s["id"] in store_filter]

    started = utc_now()
    run_id = run_id_for(started)
    run_dir = resolve_confined_path(backup_root, "runs", run_id)
    manifest_path = backup_root / "manifest.jsonl"

    print(json.dumps({"mode": "dry-run" if dry_run else "backup", "run_id": run_id,
                      "backup_root": str(backup_root), "stores": [s["id"] for s in stores],
                      "started_at": utc_now_iso()}, ensure_ascii=False))
    if not dry_run:
        append_jsonl(manifest_path, {
            "record": "run_start", "schema": MANIFEST_SCHEMA, "run_id": run_id,
            "started_at": utc_now_iso(), "config": str(Path(config_path).resolve()),
            "dry_run": False,
        })

    errors: list[str] = []
    files_copied = 0
    bytes_copied = 0

    for store in stores:
        store_id, store_class = store["id"], store.get("class", "unknown")
        src_root = Path(store["path"]).expanduser()
        if not src_root.exists():
            msg = f"store {store_id!r}: source path does not exist: {src_root}"
            errors.append(msg)
            print(f"ERROR {msg}", file=sys.stderr)
            continue
        if not src_root.is_dir():
            msg = f"store {store_id!r}: source path is not a directory: {src_root}"
            errors.append(msg)
            print(f"ERROR {msg}", file=sys.stderr)
            continue

        for item in iter_tree(src_root):
            kind = item[0]
            if kind == "skipped":
                _, path, rel, reason = item
                print(f"SKIP  {store_id}/{rel} ({reason})")
                if not dry_run:
                    append_jsonl(manifest_path, {"record": "skipped", "run_id": run_id,
                                                 "store_id": store_id, "class": store_class,
                                                 "rel": rel, "reason": reason})
                continue
            if kind == "dir":
                _, path, rel = item
                if not dry_run:
                    append_jsonl(manifest_path, {"record": "dir", "run_id": run_id,
                                                 "store_id": store_id, "class": store_class,
                                                 "rel": rel})
                continue

            _, src_file, rel = item
            try:
                dest_file = resolve_confined_path(run_dir, store_id, rel)
            except ValueError as exc:
                msg = f"store {store_id!r}: unsafe destination for {rel!r}: {exc}"
                errors.append(msg)
                print(f"ERROR {msg}", file=sys.stderr)
                continue
            try:
                src_hash = sha256_file(src_file)
                size = src_file.stat().st_size
            except OSError as exc:
                msg = f"store {store_id!r}: cannot hash source {src_file}: {exc}"
                errors.append(msg)
                print(f"ERROR {msg}", file=sys.stderr)
                continue

            if dry_run:
                print(f"PLAN  {store_id}/{rel} size={size} sha256={src_hash[:16]}…")
                continue

            try:
                dest_file.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(src_file, dest_file)
                dest_hash = sha256_file(dest_file)
            except OSError as exc:
                msg = f"store {store_id!r}: copy/verify failed for {src_file}: {exc}"
                errors.append(msg)
                print(f"ERROR {msg}", file=sys.stderr)
                continue

            readback = "match" if dest_hash == src_hash else "MISMATCH"
            if readback == "MISMATCH":
                msg = f"store {store_id!r}: readback hash mismatch for {src_file}"
                errors.append(msg)
                print(f"ERROR {msg}", file=sys.stderr)

            append_jsonl(manifest_path, {
                "record": "file", "run_id": run_id, "store_id": store_id,
                "class": store_class, "src": str(src_file.resolve()), "rel": rel,
                "size": size, "sha256": src_hash, "readback": readback,
                "copied_at": utc_now_iso(),
            })
            files_copied += 1
            bytes_copied += size
            print(f"OK    {store_id}/{rel} size={size} sha256={src_hash[:16]}… readback={readback}")

    status = "ok" if not errors else "partial"
    finished_at = utc_now_iso()
    if not dry_run:
        append_jsonl(manifest_path, {"record": "run_end", "run_id": run_id,
                                     "finished_at": finished_at, "files": files_copied,
                                     "bytes": bytes_copied, "errors": errors,
                                     "status": status})
    print(json.dumps({"run_id": run_id, "status": status, "files": files_copied,
                      "bytes": bytes_copied, "errors": len(errors),
                      "finished_at": finished_at}, ensure_ascii=False))
    return RC_OK if not errors else RC_ERROR


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="OPS-A evidence-store backup (copy + hash + append-only manifest)")
    parser.add_argument("--config", required=True, help="backup config JSON (see config.example.json)")
    parser.add_argument("--dry-run", action="store_true", help="walk + hash sources, write nothing")
    parser.add_argument("--store", action="append", default=[],
                        help="restrict to this store id (repeatable)")
    args = parser.parse_args(argv)
    store_filter = set(args.store) if args.store else None
    return run_backup(Path(args.config), dry_run=args.dry_run, store_filter=store_filter)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
