#!/usr/bin/env python3
"""Validate the sanitized KVM2 evidence ledger and its three row types."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime
from pathlib import Path, PurePosixPath
from typing import Any

PROGRAM_PREFIX = "MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PROGRAM/"
REQUIRED_FIELDS = {
    "task_id",
    "description",
    "prerequisite_task_ids",
    "authorizer",
    "executor",
    "independent_verifier",
    "publishable_artifact_path",
    "restricted_raw_evidence_logical_id",
    "artifact_sha256",
    "utc_timestamp",
    "data_classification",
    "verdict",
    "stop_retry_history",
}
CLASSIFICATIONS = {"public-sanitized", "restricted-encrypted", "mixed"}
VERDICTS = {"PASS", "FAIL", "BLOCKED", "OPEN"}
SHA_RE = re.compile(r"^[0-9a-f]{64}$")
LOGICAL_ID_RE = re.compile(r"^RAW-[A-Z0-9-]+$")
IPV4_RE = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
WINDOWS_PATH_RE = re.compile(r"(?i)\b[a-z]:[\\/]")
HOME_PATH_RE = re.compile(r"(?i)/(?:home|users|root)/")
HOSTNAME_RE = re.compile(
    r"(?i)\b[a-z0-9](?:[a-z0-9-]{0,62}[a-z0-9])?\."
    r"(?:local|internal|lan|example|invalid|test)\b"
)
CREDENTIAL_RE = re.compile(
    r"(?i)(?:-----BEGIN .+ PRIVATE KEY-----|(?:api|private|wallet)[_-]?key\s*=|"
    r"bot[_-]?token\s*=|0x[0-9a-f]{40,}|sk-[a-z0-9_-]{16,})"
)


class LedgerValidationError(ValueError):
    pass


def _walk_strings(value: Any):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for key, item in value.items():
            yield str(key)
            yield from _walk_strings(item)
    elif isinstance(value, list):
        for item in value:
            yield from _walk_strings(item)


def _reject_private_values(row: dict[str, Any]) -> None:
    for value in _walk_strings(row):
        if IPV4_RE.search(value):
            raise LedgerValidationError("IP literal is forbidden")
        if WINDOWS_PATH_RE.search(value) or HOME_PATH_RE.search(value):
            raise LedgerValidationError("private filesystem path is forbidden")
        if HOSTNAME_RE.search(value):
            raise LedgerValidationError("hostname is forbidden")
        if CREDENTIAL_RE.search(value):
            raise LedgerValidationError("credential-like value is forbidden")
        if "ssh://" in value.lower() or value.lower().startswith("ssh "):
            raise LedgerValidationError("host connection detail is forbidden")


def _valid_timestamp(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    try:
        datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")
    except ValueError:
        return False
    return True


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_row(
    row: dict[str, Any],
    *,
    repo_root: Path | None = None,
    verify_artifact: bool = False,
) -> None:
    if set(row) != REQUIRED_FIELDS:
        missing = sorted(REQUIRED_FIELDS - set(row))
        extra = sorted(set(row) - REQUIRED_FIELDS)
        raise LedgerValidationError(f"field mismatch missing={missing} extra={extra}")
    _reject_private_values(row)

    for field in ("task_id", "description", "authorizer", "executor", "independent_verifier"):
        if not isinstance(row[field], str) or not row[field].strip():
            raise LedgerValidationError(f"{field} must be a non-empty string")
    if not isinstance(row["prerequisite_task_ids"], list) or not all(
        isinstance(item, str) and item for item in row["prerequisite_task_ids"]
    ):
        raise LedgerValidationError("prerequisite_task_ids must be a string list")
    if not isinstance(row["stop_retry_history"], list) or not all(
        isinstance(item, str) and item for item in row["stop_retry_history"]
    ):
        raise LedgerValidationError("stop_retry_history must be a string list")
    if row["data_classification"] not in CLASSIFICATIONS:
        raise LedgerValidationError("invalid data_classification")
    if row["verdict"] not in VERDICTS:
        raise LedgerValidationError("invalid verdict")
    if not _valid_timestamp(row["utc_timestamp"]):
        raise LedgerValidationError("invalid utc_timestamp")
    if not isinstance(row["artifact_sha256"], str) or not SHA_RE.fullmatch(
        row["artifact_sha256"]
    ):
        raise LedgerValidationError("invalid artifact_sha256")

    publishable = row["publishable_artifact_path"]
    restricted = row["restricted_raw_evidence_logical_id"]
    classification = row["data_classification"]
    if classification == "public-sanitized" and not (
        isinstance(publishable, str) and restricted is None
    ):
        raise LedgerValidationError("public-sanitized row contract violated")
    if classification == "restricted-encrypted" and not (
        publishable is None and isinstance(restricted, str)
    ):
        raise LedgerValidationError("restricted-encrypted row contract violated")
    if classification == "mixed" and not (
        isinstance(publishable, str) and isinstance(restricted, str)
    ):
        raise LedgerValidationError("mixed row contract violated")

    if publishable is not None:
        pure = PurePosixPath(publishable)
        if (
            not publishable.startswith(PROGRAM_PREFIX)
            or pure.is_absolute()
            or ".." in pure.parts
            or "\\" in publishable
        ):
            raise LedgerValidationError("publishable path escapes the program root")
        if verify_artifact:
            if repo_root is None:
                raise LedgerValidationError("repo_root required for artifact verification")
            artifact = repo_root / Path(*pure.parts)
            if not artifact.is_file():
                raise LedgerValidationError("publishable artifact is missing")
            if _sha256_file(artifact) != row["artifact_sha256"]:
                raise LedgerValidationError("publishable artifact hash mismatch")
    if restricted is not None and not LOGICAL_ID_RE.fullmatch(restricted):
        raise LedgerValidationError("invalid restricted evidence logical id")


def load_rows(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line_number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip():
            continue
        try:
            row = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise LedgerValidationError(f"invalid JSON at line {line_number}") from exc
        if not isinstance(row, dict):
            raise LedgerValidationError(f"line {line_number} is not an object")
        rows.append(row)
    if not rows:
        raise LedgerValidationError("ledger has no rows")
    return rows


def validate_file(
    path: Path,
    *,
    repo_root: Path | None = None,
    verify_artifacts: bool = False,
) -> int:
    rows = load_rows(path)
    for row in rows:
        validate_row(row, repo_root=repo_root, verify_artifact=verify_artifacts)
    return len(rows)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ledger", required=True, type=Path)
    parser.add_argument("--repo-root", type=Path)
    parser.add_argument("--verify-artifacts", action="store_true")
    args = parser.parse_args()
    try:
        count = validate_file(
            args.ledger,
            repo_root=args.repo_root,
            verify_artifacts=args.verify_artifacts,
        )
    except (OSError, UnicodeError, LedgerValidationError) as exc:
        print(f"ledger validation FAIL: {exc}", file=sys.stderr)
        return 1
    print(f"ledger validation PASS: rows={count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
