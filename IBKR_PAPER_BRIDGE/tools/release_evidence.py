"""TS-P0-002 — release/rollback evidence manifest tool.

Builds on the TS-P0-001 hashing primitives (tools/check_runtime_baseline.py);
does not duplicate them. Two offline, read-only subcommands:

  create    build a release evidence manifest for the CURRENT repo HEAD
            (release commit must equal repo HEAD — evidence is created from
            the checked-out release, never synthesized) plus a rollback
            commit that must exist in the repository.
  validate  verify a manifest: schema version, required fields, integrity
            hash (tamper detection), rollback commit known to the repo, and
            current repo/runtime state still matching the recorded release.

Exit codes (same convention as check_runtime_baseline):
  0 valid / created; 2 validation failure (tamper, missing field, old
  version, unknown rollback, drift); 3 invalid evidence input (bad paths,
  malformed git output, corrupt/missing manifest file, bad arguments).

No deploy, no checkout, no network, no scheduler, no database, no process
control, no writes inside either root.

Contract: IBKR_PAPER_BRIDGE/docs/RELEASE_EVIDENCE_CONTRACT.md
(DRAFT — pending Barış approval).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

try:  # package-style import (tests, repo root on sys.path)
    from tools.check_runtime_baseline import (
        EvidenceError,
        _hash_file,
        _hash_side,
        _read_git_facts,
        _run_git,
    )
except ImportError:  # direct script invocation: sys.path[0] == tools/
    from check_runtime_baseline import (  # type: ignore[no-redef]
        EvidenceError,
        _hash_file,
        _hash_side,
        _read_git_facts,
        _run_git,
    )

SCHEMA_VERSION = "1.0.0"

# File whose hash pins the dependency set (no separate lockfile exists yet).
LOCK_FILE = "IBKR_PAPER_BRIDGE/requirements.txt"
# File that defines the persisted DB schema (schema proxy, see contract).
SCHEMA_FILE = "IBKR_PAPER_BRIDGE/bridge/store/db.py"

REQUIRED_FIELDS = (
    "schema_version",
    "tool",
    "generated_at_utc",
    "repo_root",
    "runtime_root",
    "release_commit",
    "rollback_commit",
    "hashes",
    "integrity_sha256",
)

REQUIRED_HASH_KEYS = (
    "source_tree_hash",
    "config_hash",
    "lock_hash",
    "schema_hash",
    "runtime_source_tree_hash",
    "runtime_config_hash",
)

_HEX40 = __import__("re").compile(r"^[0-9a-f]{40}$")
_TS_RE = __import__("re").compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")


def _integrity_hash(manifest: dict) -> str:
    """SHA-256 over the canonical manifest payload minus the integrity field."""
    payload = {k: v for k, v in manifest.items() if k != "integrity_sha256"}
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _to_json(obj: dict) -> str:
    return json.dumps(obj, indent=2, sort_keys=True) + "\n"


def _commit_exists(root: Path, commit: str) -> bool:
    try:
        out = _run_git(root, "cat-file", "-t", commit)
    except EvidenceError:
        return False
    return out.strip() == "commit"


def _utc_now() -> str:
    from datetime import datetime, timezone

    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _build_manifest(
    repo_root: Path,
    runtime_root: Path,
    release_commit: str,
    rollback_commit: str,
    timestamp: str,
) -> dict:
    if not repo_root.is_dir():
        raise EvidenceError(f"repo root does not exist: {repo_root}")
    if not runtime_root.is_dir():
        raise EvidenceError(f"runtime root does not exist: {runtime_root}")
    repo = _read_git_facts(repo_root, "repo")
    if repo["commit"] != release_commit:
        raise EvidenceError(
            "release commit must equal repo HEAD (create evidence from the "
            f"checked-out release): HEAD={repo['commit']} given={release_commit}"
        )
    if not _commit_exists(repo_root, rollback_commit):
        raise EvidenceError(f"rollback commit not found in repo: {rollback_commit}")
    if rollback_commit == release_commit:
        raise EvidenceError("rollback commit must differ from release commit")

    repo_hashes = _hash_side(repo_root)
    runtime_hashes = _hash_side(runtime_root)
    lock_path = repo_root / LOCK_FILE
    schema_path = repo_root / SCHEMA_FILE
    for label, p in (("lock", lock_path), ("schema", schema_path)):
        if not p.is_file():
            raise EvidenceError(f"{label} file missing in repo: {p}")

    manifest = {
        "schema_version": SCHEMA_VERSION,
        "tool": "release_evidence",
        "generated_at_utc": timestamp,
        "repo_root": repo_root.resolve().as_posix(),
        "runtime_root": runtime_root.resolve().as_posix(),
        "release_commit": release_commit,
        "rollback_commit": rollback_commit,
        "hashes": {
            "source_tree_hash": repo_hashes["source_tree_hash"],
            "config_hash": repo_hashes["config_hash"],
            "lock_hash": _hash_file(lock_path),
            "schema_hash": _hash_file(schema_path),
            "runtime_source_tree_hash": runtime_hashes["source_tree_hash"],
            "runtime_config_hash": runtime_hashes["config_hash"],
        },
    }
    manifest["integrity_sha256"] = _integrity_hash(manifest)
    return manifest


def _validate_manifest(manifest: dict, repo_root: Path, runtime_root: Path) -> dict:
    failures: list[str] = []

    for field in REQUIRED_FIELDS:
        if field not in manifest:
            failures.append(f"missing_field:{field}")
    if "hashes" in manifest and isinstance(manifest["hashes"], dict):
        for key in REQUIRED_HASH_KEYS:
            if key not in manifest["hashes"]:
                failures.append(f"missing_field:hashes.{key}")

    version = manifest.get("schema_version")
    if version is not None and version != SCHEMA_VERSION:
        failures.append(f"unsupported_schema_version:{version}")

    if "integrity_sha256" in manifest:
        if _integrity_hash(manifest) != manifest["integrity_sha256"]:
            failures.append("integrity_hash_mismatch")

    # Only compare against live state when the manifest is structurally sound.
    if not failures:
        repo = _read_git_facts(repo_root, "repo")
        rollback = manifest["rollback_commit"]
        if not (isinstance(rollback, str) and _commit_exists(repo_root, rollback)):
            failures.append(f"rollback_commit_unknown:{rollback}")
        if repo["commit"] != manifest["release_commit"]:
            failures.append("repo_head_not_release_commit")
        if repo["dirty"]:
            failures.append("repo_dirty")
        repo_hashes = _hash_side(repo_root)
        if repo_hashes["source_tree_hash"] != manifest["hashes"]["source_tree_hash"]:
            failures.append("source_tree_hash_mismatch")
        if repo_hashes["config_hash"] != manifest["hashes"]["config_hash"]:
            failures.append("config_hash_mismatch")
        lock_path = repo_root / LOCK_FILE
        schema_path = repo_root / SCHEMA_FILE
        if not lock_path.is_file() or _hash_file(lock_path) != manifest["hashes"]["lock_hash"]:
            failures.append("lock_hash_mismatch")
        if (
            not schema_path.is_file()
            or _hash_file(schema_path) != manifest["hashes"]["schema_hash"]
        ):
            failures.append("schema_hash_mismatch")
        if runtime_root.is_dir():
            runtime_hashes = _hash_side(runtime_root)
            if (
                runtime_hashes["source_tree_hash"]
                != manifest["hashes"]["runtime_source_tree_hash"]
            ):
                failures.append("runtime_source_tree_hash_mismatch")
            if runtime_hashes["config_hash"] != manifest["hashes"]["runtime_config_hash"]:
                failures.append("runtime_config_hash_mismatch")
        else:
            failures.append("runtime_missing")

    failures = sorted(set(failures))
    return {
        "tool": "release_evidence.validate",
        "schema_version": SCHEMA_VERSION,
        "failures": failures,
        "verdict": "VALID" if not failures else "INVALID",
        "exit_code": 0 if not failures else 2,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="release_evidence",
        description="Release/rollback evidence manifest tool (TS-P0-002).",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_create = sub.add_parser("create", help="Create a release evidence manifest.")
    p_create.add_argument("--repo-root", required=True)
    p_create.add_argument("--runtime-root", required=True)
    p_create.add_argument("--release-commit", required=True)
    p_create.add_argument("--rollback-commit", required=True)
    p_create.add_argument("--timestamp", default=None)
    p_create.add_argument("--out", required=True)

    p_val = sub.add_parser("validate", help="Validate a release evidence manifest.")
    p_val.add_argument("--manifest", required=True)
    p_val.add_argument("--repo-root", required=True)
    p_val.add_argument("--runtime-root", required=True)

    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        return 3 if exc.code != 0 else 0

    try:
        if args.command == "create":
            release = args.release_commit.strip().lower()
            rollback = args.rollback_commit.strip().lower()
            for label, value in (("release", release), ("rollback", rollback)):
                if not _HEX40.match(value):
                    print(
                        f"release_evidence: invalid --{label}-commit (want 40 hex): "
                        f"{value!r}",
                        file=sys.stderr,
                    )
                    return 3
            timestamp = args.timestamp if args.timestamp is not None else _utc_now()
            if not _TS_RE.match(timestamp):
                print(
                    f"release_evidence: invalid --timestamp: {timestamp!r}",
                    file=sys.stderr,
                )
                return 3
            manifest = _build_manifest(
                Path(args.repo_root),
                Path(args.runtime_root),
                release,
                rollback,
                timestamp,
            )
            Path(args.out).write_text(
                _to_json(manifest), encoding="utf-8", newline="\n"
            )
            sys.stdout.write(_to_json({"created": args.out, "verdict": "CREATED"}))
            return 0

        # validate
        manifest_path = Path(args.manifest)
        if not manifest_path.is_file():
            print(
                f"release_evidence: manifest not found: {manifest_path}",
                file=sys.stderr,
            )
            return 3
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            print(f"release_evidence: corrupt manifest JSON: {exc}", file=sys.stderr)
            return 3
        if not isinstance(manifest, dict):
            print("release_evidence: manifest is not a JSON object", file=sys.stderr)
            return 3
        report = _validate_manifest(
            manifest, Path(args.repo_root), Path(args.runtime_root)
        )
        sys.stdout.write(_to_json(report))
        return report["exit_code"]
    except EvidenceError as exc:
        print(f"release_evidence: invalid evidence input: {exc}", file=sys.stderr)
        return 3


if __name__ == "__main__":
    sys.exit(main())
