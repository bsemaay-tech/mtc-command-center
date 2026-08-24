#!/usr/bin/env python3
"""Build and verify the WP-P0-03 append-only migration ledger.

The accepted Tier-A classification, freeze-tag manifest, and every file payload are
read from Git objects at FIXED_COMMIT. Worktree bytes therefore cannot change the
result.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import BinaryIO, Iterable


FIXED_COMMIT = "88eab9c93b7c285b990d07502ea1ec476034e8d5"
FIXED_COMMIT_SHORT = "88eab9c9"
EXPECTED_CANONICAL_ROWS = 2_641
INVENTORY_REL = (
    "MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_01_INVENTORY_2026-08-24/"
    "tier_a_classification.csv"
)
TAG_MANIFEST_REL = (
    "MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_02_TAG_FREEZES_2026-08-25/"
    "TAG_MANIFEST.txt"
)
OUT_DIR = Path(__file__).resolve().parent
REPO_ROOT = OUT_DIR.parents[2]
DEFAULT_LEDGER = REPO_ROOT / "MTC_COMMAND_CENTER" / "MIGRATION_LEDGER.json"


@dataclass(frozen=True)
class TreeBlob:
    mode: str
    oid: str
    size: int


class GitBatchReader:
    """Stream blob payloads from one ``git cat-file --batch`` process."""

    def __init__(self, repo: Path) -> None:
        self._process = subprocess.Popen(
            ["git", "-C", str(repo), "cat-file", "--batch"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

    def read_blob(self, oid: str, *, capture: bool = False) -> tuple[str, bytes | None]:
        stdin = self._required_pipe(self._process.stdin, "stdin")
        stdout = self._required_pipe(self._process.stdout, "stdout")
        stdin.write(oid.encode("ascii") + b"\n")
        stdin.flush()

        header = stdout.readline()
        if not header:
            raise RuntimeError(f"git cat-file returned no header for {oid}")
        fields = header.rstrip(b"\n").split()
        if len(fields) != 3 or fields[1] != b"blob":
            raise RuntimeError(
                f"git cat-file returned an unexpected header for {oid}: {header!r}"
            )
        size = int(fields[2])
        digest = hashlib.sha256()
        captured = bytearray() if capture else None
        remaining = size
        while remaining:
            chunk = stdout.read(min(remaining, 1024 * 1024))
            if not chunk:
                raise RuntimeError(f"truncated git blob {oid}; {remaining} bytes missing")
            digest.update(chunk)
            if captured is not None:
                captured.extend(chunk)
            remaining -= len(chunk)
        if stdout.read(1) != b"\n":
            raise RuntimeError(f"git cat-file blob delimiter missing for {oid}")
        return digest.hexdigest(), bytes(captured) if captured is not None else None

    def close(self) -> None:
        stdin = self._required_pipe(self._process.stdin, "stdin")
        stdout = self._required_pipe(self._process.stdout, "stdout")
        stderr = self._required_pipe(self._process.stderr, "stderr")
        stdin.close()
        extra = stdout.read()
        error = stderr.read().decode("utf-8", errors="replace")
        return_code = self._process.wait()
        if return_code != 0 or extra:
            raise RuntimeError(
                "git cat-file --batch did not close cleanly: "
                f"return_code={return_code}, extra_stdout={extra!r}, stderr={error!r}"
            )

    @staticmethod
    def _required_pipe(pipe: BinaryIO | None, name: str) -> BinaryIO:
        if pipe is None:
            raise RuntimeError(f"git cat-file {name} pipe is unavailable")
        return pipe

    def __enter__(self) -> GitBatchReader:
        return self

    def __exit__(self, exc_type: object, exc: object, traceback: object) -> None:
        if self._process.poll() is None:
            try:
                self.close()
            except Exception:
                if exc_type is None:
                    raise


def run_git(args: list[str], *, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        ["git", "-C", str(REPO_ROOT), *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=check,
    )


def validate_repository() -> None:
    top = run_git(["rev-parse", "--show-toplevel"]).stdout.decode().strip()
    if Path(top).resolve() != REPO_ROOT.resolve():
        raise RuntimeError(f"repository root mismatch: {top!r} != {str(REPO_ROOT)!r}")
    commit_check = run_git(
        ["cat-file", "-e", f"{FIXED_COMMIT}^{{commit}}"], check=False
    )
    if commit_check.returncode != 0:
        error = commit_check.stderr.decode("utf-8", errors="replace").strip()
        raise RuntimeError(f"pinned commit {FIXED_COMMIT} is unavailable: {error}")


def fixed_tree() -> dict[str, TreeBlob]:
    raw = run_git(
        ["ls-tree", "-r", "-l", "-z", "--full-tree", FIXED_COMMIT]
    ).stdout
    result: dict[str, TreeBlob] = {}
    for record in raw.split(b"\0"):
        if not record:
            continue
        metadata, raw_path = record.split(b"\t", 1)
        mode, object_type, oid, size_raw = metadata.decode("ascii").split()
        if object_type != "blob":
            continue
        path = raw_path.decode("utf-8", errors="strict").replace("\\", "/")
        if path in result:
            raise RuntimeError(f"duplicate path in fixed tree: {path}")
        result[path] = TreeBlob(mode=mode, oid=oid, size=int(size_raw))
    return result


def parse_canonical_paths(inventory_bytes: bytes) -> list[str]:
    text = inventory_bytes.decode("utf-8-sig", errors="strict")
    reader = csv.DictReader(io.StringIO(text, newline=""))
    required = {"source", "path", "classification"}
    if reader.fieldnames is None or not required.issubset(reader.fieldnames):
        raise RuntimeError(
            f"inventory columns {reader.fieldnames!r} do not include {sorted(required)!r}"
        )
    canonical_paths: list[str] = []
    for row_number, row in enumerate(reader, start=2):
        if row["classification"] != "CANONICAL":
            continue
        if row["source"] != "TRACKED_FIXED_SHA":
            raise RuntimeError(
                f"CANONICAL row {row_number} has non-fixed source {row['source']!r}"
            )
        path = row["path"]
        if not path or "\\" in path:
            raise RuntimeError(f"invalid canonical path on row {row_number}: {path!r}")
        canonical_paths.append(path)
    if len(canonical_paths) != EXPECTED_CANONICAL_ROWS:
        raise RuntimeError(
            f"CANONICAL row count {len(canonical_paths)} != {EXPECTED_CANONICAL_ROWS}"
        )
    if len(set(canonical_paths)) != len(canonical_paths):
        raise RuntimeError("Tier-A CANONICAL paths are not unique")
    return canonical_paths


def parse_freeze_manifest(manifest_bytes: bytes) -> int:
    text = manifest_bytes.decode("utf-8-sig", errors="strict")
    reader = csv.DictReader(io.StringIO(text, newline=""), delimiter="\t")
    expected_header = ["status", "tag", "target_sha", "target_description"]
    if reader.fieldnames != expected_header:
        raise RuntimeError(
            f"freeze manifest header {reader.fieldnames!r} != {expected_header!r}"
        )
    rows = list(reader)
    if not rows or any(row["status"] != "CREATED" for row in rows):
        raise RuntimeError("freeze manifest is empty or contains a non-CREATED row")
    return len(rows)


def build_ledger() -> dict[str, object]:
    validate_repository()
    tree = fixed_tree()
    for source_path in (INVENTORY_REL, TAG_MANIFEST_REL):
        if source_path not in tree:
            raise RuntimeError(f"required input is absent at {FIXED_COMMIT}: {source_path}")

    with GitBatchReader(REPO_ROOT) as blobs:
        inventory_sha256, inventory_bytes = blobs.read_blob(
            tree[INVENTORY_REL].oid, capture=True
        )
        manifest_sha256, manifest_bytes = blobs.read_blob(
            tree[TAG_MANIFEST_REL].oid, capture=True
        )
        assert inventory_bytes is not None
        assert manifest_bytes is not None
        canonical_paths = parse_canonical_paths(inventory_bytes)
        freeze_tag_count = parse_freeze_manifest(manifest_bytes)

        hash_by_oid: dict[str, str] = {}
        entries: list[dict[str, object]] = []
        for entry_id, path in enumerate(canonical_paths, start=1):
            tree_blob = tree.get(path)
            if tree_blob is None:
                raise RuntimeError(f"CANONICAL path is absent at {FIXED_COMMIT}: {path}")
            sha256 = hash_by_oid.get(tree_blob.oid)
            if sha256 is None:
                sha256, _ = blobs.read_blob(tree_blob.oid)
                hash_by_oid[tree_blob.oid] = sha256
            entries.append(
                {
                    "old_path": path,
                    "new_location": None,
                    "sha256": sha256,
                    "status": "NOT_MIGRATED",
                    "entry_id": entry_id,
                }
            )

    return {
        "schema_version": "1.0.0",
        "generated_at_commit": FIXED_COMMIT,
        "generated_at_commit_short": FIXED_COMMIT_SHORT,
        "append_only_contract": {
            "entries_are_immutable": (
                "Existing rows are never edited, reordered, or deleted."
            ),
            "corrections_and_state_changes": (
                "Append a row with a new entry_id and supersedes_entry_id pointing to "
                "the prior row; the prior row then has effective state SUPERSEDED while "
                "its stored bytes and stored status remain unchanged."
            ),
            "resolution_rule": (
                "Resolve either old_path or non-null new_location to the newest applicable "
                "row, then return that row's old_path and effective location."
            ),
            "null_new_location_rule": (
                "A null new_location means no move has occurred; its effective location is "
                "old_path, so forward and reverse resolution both resolve to old_path itself."
            ),
            "initial_entry_order": (
                "entry_id follows Tier-A CANONICAL source-inventory order, starting at 1."
            ),
            "future_optional_field": (
                "supersedes_entry_id is omitted from initial rows and is required on a "
                "future appended row that corrects or changes an earlier row."
            ),
        },
        "status_enum": {
            "NOT_MIGRATED": (
                "Initial state: no real migration has assigned a new location."
            ),
            "MIGRATED": (
                "Future state: a real migration assigned and verified a non-null new_location."
            ),
            "SUPERSEDED": (
                "Effective future state of an immutable prior row identified by a later "
                "row's supersedes_entry_id."
            ),
        },
        "inputs": {
            "tier_a_classification": {
                "path": INVENTORY_REL,
                "git_blob_oid": tree[INVENTORY_REL].oid,
                "sha256": inventory_sha256,
                "canonical_row_count": len(canonical_paths),
            },
            "freeze_tag_manifest": {
                "path": TAG_MANIFEST_REL,
                "git_blob_oid": tree[TAG_MANIFEST_REL].oid,
                "sha256": manifest_sha256,
                "created_tag_count": freeze_tag_count,
            },
        },
        "entries": entries,
    }


def serialize_ledger(ledger: dict[str, object]) -> bytes:
    return (
        json.dumps(ledger, ensure_ascii=False, indent=2, separators=(",", ": ")) + "\n"
    ).encode("utf-8")


def sampled_indices(row_count: int, sample_size: int) -> list[int]:
    if sample_size < 1 or sample_size > row_count:
        raise ValueError(f"sample size must be between 1 and {row_count}")
    if sample_size == 1:
        return [0]
    return [round(index * (row_count - 1) / (sample_size - 1)) for index in range(sample_size)]


def resolve_row(entries: Iterable[dict[str, object]], query: str) -> dict[str, object]:
    matches = [
        row
        for row in entries
        if query == row["old_path"]
        or query == (row["new_location"] or row["old_path"])
    ]
    if not matches:
        raise KeyError(query)
    return max(matches, key=lambda row: int(row["entry_id"]))


def verify_ledger(path: Path, expected: dict[str, object], sample_size: int) -> None:
    actual_bytes = path.read_bytes()
    expected_bytes = serialize_ledger(expected)
    if actual_bytes != expected_bytes:
        raise RuntimeError(f"ledger is not byte-identical to regenerated output: {path}")
    actual = json.loads(actual_bytes.decode("utf-8"))
    entries = actual["entries"]
    expected_count = actual["inputs"]["tier_a_classification"]["canonical_row_count"]
    if len(entries) != expected_count:
        raise RuntimeError(f"ledger rows {len(entries)} != inventory rows {expected_count}")

    print(
        "VERIFY PASS "
        f"inventory_canonical={expected_count} ledger_rows={len(entries)} "
        f"unique_old_paths={len({row['old_path'] for row in entries})}"
    )
    print(
        "BYTE_IDENTITY PASS "
        f"ledger_sha256={hashlib.sha256(actual_bytes).hexdigest()}"
    )

    for index in sampled_indices(len(entries), sample_size):
        row = entries[index]
        old_path = str(row["old_path"])
        effective_location = str(row["new_location"] or old_path)
        forward = resolve_row(entries, old_path)
        reverse = resolve_row(entries, effective_location)
        if forward["entry_id"] != row["entry_id"] or reverse["old_path"] != old_path:
            raise RuntimeError(f"bidirectional resolution failed for entry {row['entry_id']}")
        print(
            "SAMPLE PASS "
            f"entry_id={row['entry_id']} "
            f"old_path={json.dumps(old_path, ensure_ascii=False)} "
            f"forward_entry_id={forward['entry_id']} "
            f"effective_location={json.dumps(effective_location, ensure_ascii=False)} "
            f"reverse_old={json.dumps(reverse['old_path'], ensure_ascii=False)}"
        )
    print(
        "BIDIRECTIONAL_SAMPLE PASS "
        f"sample_size={sample_size} old_to_row_to_old={sample_size} "
        f"effective_location_to_row_to_old={sample_size} null_self_resolutions={sample_size}"
    )

    simulated = {
        "old_path": "__WP_P0_03_SIMULATION__/old/location.txt",
        "new_location": "__WP_P0_03_SIMULATION__/future/location.txt",
        "sha256": "0" * 64,
        "status": "MIGRATED",
        "entry_id": len(entries) + 1,
        "supersedes_entry_id": 1,
    }
    by_old = resolve_row([simulated], str(simulated["old_path"]))
    by_new = resolve_row([simulated], str(simulated["new_location"]))
    if by_old != simulated or by_new != simulated:
        raise RuntimeError("simulated future bidirectional resolution failed")
    print(
        "SIMULATED_FUTURE PASS "
        f"old={json.dumps(simulated['old_path'])} "
        f"new={json.dumps(simulated['new_location'])} "
        f"old_lookup_entry_id={by_old['entry_id']} "
        f"new_lookup_entry_id={by_new['entry_id']} "
        f"both_return_old={json.dumps(simulated['old_path'])}"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_LEDGER,
        help=f"ledger path to write (default: {DEFAULT_LEDGER})",
    )
    mode.add_argument("--check", type=Path, help="verify an existing ledger without writing")
    parser.add_argument(
        "--sample-size",
        type=int,
        default=20,
        help="number of deterministic, evenly-spaced rows checked by --check",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        ledger = build_ledger()
        if args.check is not None:
            verify_ledger(args.check.resolve(), ledger, args.sample_size)
            return 0
        output = args.output.resolve()
        output.parent.mkdir(parents=True, exist_ok=True)
        data = serialize_ledger(ledger)
        with output.open("wb") as handle:
            handle.write(data)
        print(
            "BUILD PASS "
            f"output={output} rows={len(ledger['entries'])} "
            f"sha256={hashlib.sha256(data).hexdigest()}"
        )
        return 0
    except (OSError, RuntimeError, ValueError, KeyError, json.JSONDecodeError) as error:
        print(f"BUILD BLOCKED: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
