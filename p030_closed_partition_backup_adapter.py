"""P030 stable-prefix adapter over unchanged P026 backup/restore tools."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path, PurePosixPath, PureWindowsPath
from urllib.parse import unquote


OPSA_TOOLS = Path(__file__).resolve().parent / "MTC_COMMAND_CENTER" / "tools" / "opsa"
sys.path.insert(0, str(OPSA_TOOLS))

import backup  # noqa: E402
import restore  # noqa: E402
from opsa_common import (  # noqa: E402
    RC_OK,
    MANIFEST_SCHEMA,
    atomic_write_bytes,
    atomic_write_json,
    load_backup_config,
    parse_utc_iso,
    require_non_empty_string,
    resolve_confined_path,
)


STABLE_RECEIPT_NAME = "_P030_STABLE_PREFIX.json"
VERIFIED_RESTORE_RECEIPT_NAME = "_P030_VERIFIED_RESTORE.json"
_STABLE_FIELDS = {
    "schema",
    "state",
    "source_path",
    "snapshot_rel",
    "high_water_bytes",
    "record_count",
    "last_observation_id",
    "prefix_sha256",
    "captured_at_utc",
    "dataset_content_hash",
}
_DATASET_ID = re.compile(r"^p030ds-v1:[0-9a-f]{64}$")
_OBSERVATION_ID = re.compile(r"^p030obs-v1:[0-9a-f]{64}$")
_SHA256 = re.compile(r"^[0-9a-f]{64}$")


def _reject_nonfinite_json(value: str) -> None:
    raise ValueError(f"non-finite JSON constant: {value}")


def _reject_duplicate_json_keys(pairs: list[tuple[str, object]]) -> dict:
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _read_json_object(path: Path, description: str) -> dict:
    try:
        payload = json.loads(
            Path(path).read_text(encoding="utf-8"),
            parse_constant=_reject_nonfinite_json,
            object_pairs_hook=_reject_duplicate_json_keys,
        )
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"invalid {description}") from exc
    if not isinstance(payload, dict):
        raise ValueError(f"invalid {description}")
    return payload


def _read_strict_jsonl(path: Path, description: str) -> list[dict]:
    try:
        lines = Path(path).read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        raise ValueError(f"invalid {description}") from exc
    records = []
    for line_number, line in enumerate(lines, start=1):
        if not line.strip():
            continue
        try:
            record = json.loads(
                line,
                parse_constant=_reject_nonfinite_json,
                object_pairs_hook=_reject_duplicate_json_keys,
            )
        except json.JSONDecodeError as exc:
            raise ValueError(f"invalid {description} line {line_number}") from exc
        if not isinstance(record, dict):
            raise ValueError(f"invalid {description} line {line_number}")
        records.append(record)
    return records


def _utc_z(value: str, field: str) -> None:
    if not isinstance(value, str) or not value.endswith("Z"):
        raise ValueError(f"{field} must be a caller-supplied UTC Z timestamp")
    try:
        parsed = parse_utc_iso(value)
    except ValueError as exc:
        raise ValueError(f"{field} must be a caller-supplied UTC Z timestamp") from exc
    if parsed.microsecond:
        raise ValueError(f"{field} must use whole seconds")


def _canonical_relative_posix(value: object, field: str) -> str:
    if not isinstance(value, str) or not value or value != value.strip() or "\\" in value:
        raise ValueError(f"{field} must be a canonical relative POSIX path")
    decoded = value
    for _ in range(5):
        next_value = unquote(decoded)
        if next_value == decoded:
            break
        decoded = next_value
    if decoded != value:
        raise ValueError(f"{field} must be a canonical relative POSIX path")
    for candidate in (value, decoded):
        posix = PurePosixPath(candidate)
        windows = PureWindowsPath(candidate)
        if (
            posix.is_absolute()
            or windows.drive
            or windows.root
            or posix.as_posix() != candidate
            or any(part in {".", ".."} for part in posix.parts)
        ):
            raise ValueError(f"{field} must be a canonical relative POSIX path")
    return value


def _refuse_source_links(source_root: Path, source_rel: str) -> None:
    current = Path(source_root).absolute()
    candidates = [current]
    for part in PurePosixPath(source_rel).parts:
        current = current / part
        candidates.append(current)
    for candidate in candidates:
        if candidate.is_symlink() or candidate.is_junction():
            raise ValueError(
                "source JSONL must not be a symlink or junction component"
            )


def _prefix_facts(data: bytes) -> tuple[int, str]:
    if not data.endswith(b"\n"):
        raise ValueError("high-water prefix must end with newline")
    records: list[dict] = []
    for raw_line in data.splitlines(keepends=True):
        try:
            record = json.loads(
                raw_line,
                parse_constant=_reject_nonfinite_json,
                object_pairs_hook=_reject_duplicate_json_keys,
            )
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("prefix record is not canonical JSONL") from exc
        if not isinstance(record, dict):
            raise ValueError("prefix record is not a JSON object")
        canonical = (
            json.dumps(
                record,
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
                allow_nan=False,
            ).encode("utf-8")
            + b"\n"
        )
        if canonical != raw_line:
            raise ValueError("prefix record is not canonical JSONL")
        require_non_empty_string(
            record.get("observation_id"), "observation_id", "stable-prefix record"
        )
        if not _OBSERVATION_ID.fullmatch(record["observation_id"]):
            raise ValueError("observation_id must match p030obs-v1 identity")
        records.append(record)
    if not records:
        raise ValueError("stable prefix must contain at least one record")
    return len(records), records[-1]["observation_id"]


def capture_stable_prefix(
    source_jsonl: Path,
    stable_prefix: Path,
    *,
    source_root: Path,
    high_water_bytes: int,
    captured_at_utc: str,
    dataset_content_hash: str,
) -> Path:
    """Capture a caller-bounded canonical JSONL prefix without inferring closure."""

    source_root_literal = Path(source_root).absolute()
    source_literal = Path(source_jsonl).absolute()
    try:
        source_rel = source_literal.relative_to(source_root_literal).as_posix()
    except ValueError as exc:
        raise ValueError("source JSONL must be confined to source_root") from exc
    source_rel = _canonical_relative_posix(source_rel, "source_path")
    _refuse_source_links(source_root_literal, source_rel)
    source_root = source_root_literal.resolve()
    source_jsonl = source_literal.resolve()
    stable_prefix = Path(stable_prefix).resolve()
    if isinstance(high_water_bytes, bool) or not isinstance(high_water_bytes, int) or high_water_bytes <= 0:
        raise ValueError("high_water_bytes must be a positive integer")
    _utc_z(captured_at_utc, "captured_at_utc")
    dataset_content_hash = require_non_empty_string(
        dataset_content_hash, "dataset_content_hash", "stable-prefix capture"
    )
    if not _DATASET_ID.fullmatch(dataset_content_hash):
        raise ValueError("dataset_content_hash must match p030ds-v1 identity")
    try:
        source_jsonl.relative_to(source_root)
    except ValueError as exc:
        raise ValueError("source JSONL must be confined to source_root") from exc
    if not source_jsonl.is_file():
        raise ValueError("source JSONL must be a regular file")
    if stable_prefix.exists():
        raise ValueError("stable prefix must not already exist")
    if source_jsonl.name == STABLE_RECEIPT_NAME:
        raise ValueError("source JSONL name conflicts with stable receipt")
    with source_jsonl.open("rb") as handle:
        prefix = handle.read(high_water_bytes)
    if len(prefix) != high_water_bytes:
        raise ValueError("source prefix is truncated below high water")
    record_count, last_observation_id = _prefix_facts(prefix)
    prefix_sha256 = hashlib.sha256(prefix).hexdigest()

    stable_prefix.mkdir(parents=True)
    snapshot = resolve_confined_path(stable_prefix, source_jsonl.name)
    atomic_write_bytes(snapshot, prefix)
    with source_jsonl.open("rb") as handle:
        source_after = handle.read(high_water_bytes)
    if source_after != prefix:
        raise ValueError("source prefix changed during capture")
    if snapshot.read_bytes() != prefix:
        raise ValueError("snapshot prefix verification failed")
    receipt = {
        "schema": "p030.stable_prefix/v1",
        "state": "stable_prefix",
        "source_path": source_rel,
        "snapshot_rel": source_jsonl.name,
        "high_water_bytes": high_water_bytes,
        "record_count": record_count,
        "last_observation_id": last_observation_id,
        "prefix_sha256": prefix_sha256,
        "captured_at_utc": captured_at_utc,
        "dataset_content_hash": dataset_content_hash,
    }
    receipt_path = stable_prefix / STABLE_RECEIPT_NAME
    atomic_write_json(receipt_path, receipt)
    return receipt_path


def _verify_stable_receipt(
    stable_prefix: Path,
    receipt_path: Path,
    *,
    verify_source: bool,
    source_root: Path | None = None,
) -> dict:
    stable_prefix = Path(stable_prefix).resolve()
    receipt_path = Path(receipt_path).resolve()
    if receipt_path != (stable_prefix / STABLE_RECEIPT_NAME).resolve():
        raise ValueError("stable receipt must belong to the stable prefix")
    receipt = _read_json_object(receipt_path, "stable-prefix receipt")
    if set(receipt) != _STABLE_FIELDS:
        raise ValueError("stable-prefix receipt fields do not match contract")
    if receipt["schema"] != "p030.stable_prefix/v1":
        raise ValueError("stable-prefix receipt schema does not match contract")
    if receipt["state"] != "stable_prefix":
        raise ValueError("stable-prefix receipt state does not match contract")
    source_rel = _canonical_relative_posix(receipt["source_path"], "source_path")
    snapshot_rel = _canonical_relative_posix(receipt["snapshot_rel"], "snapshot_rel")
    _utc_z(receipt["captured_at_utc"], "captured_at_utc")
    require_non_empty_string(
        receipt["dataset_content_hash"], "dataset_content_hash", "stable-prefix receipt"
    )
    if not _DATASET_ID.fullmatch(receipt["dataset_content_hash"]):
        raise ValueError("dataset_content_hash must match p030ds-v1 identity")
    high_water = receipt["high_water_bytes"]
    if isinstance(high_water, bool) or not isinstance(high_water, int) or high_water <= 0:
        raise ValueError("high_water_bytes must be a positive integer")
    record_count = receipt["record_count"]
    if isinstance(record_count, bool) or not isinstance(record_count, int) or record_count <= 0:
        raise ValueError("record_count must be a positive integer")
    last_observation_id = receipt["last_observation_id"]
    if not isinstance(last_observation_id, str) or not _OBSERVATION_ID.fullmatch(
        last_observation_id
    ):
        raise ValueError("last_observation_id must match p030obs-v1 identity")
    prefix_sha256 = receipt["prefix_sha256"]
    if not isinstance(prefix_sha256, str) or not _SHA256.fullmatch(prefix_sha256):
        raise ValueError("prefix_sha256 must be 64 lowercase hex characters")
    snapshot = resolve_confined_path(stable_prefix, snapshot_rel)
    try:
        snapshot_prefix = snapshot.read_bytes()
    except OSError as exc:
        raise ValueError("snapshot prefix is unavailable") from exc
    if len(snapshot_prefix) != high_water:
        raise ValueError("snapshot prefix length does not match high water")
    count, last_id = _prefix_facts(snapshot_prefix)
    if hashlib.sha256(snapshot_prefix).hexdigest() != prefix_sha256:
        raise ValueError("snapshot prefix hash mismatch")
    if count != record_count or last_id != last_observation_id:
        raise ValueError("snapshot prefix record identity mismatch")
    if verify_source:
        if source_root is None:
            raise ValueError("source_root is required to verify source prefix")
        source_root = Path(source_root).absolute()
        _refuse_source_links(source_root, source_rel)
        source = resolve_confined_path(source_root, source_rel)
        try:
            with source.open("rb") as handle:
                source_prefix = handle.read(high_water)
        except OSError as exc:
            raise ValueError("source prefix is unavailable") from exc
        if len(source_prefix) != high_water:
            raise ValueError("source prefix is truncated below high water")
        if source_prefix != snapshot_prefix:
            raise ValueError("source prefix no longer matches stable snapshot")
    return receipt


def load_runnable_config(
    config_path: Path, *, stable_prefix: Path, store_id: str
) -> dict:
    return _load_strict_config(
        config_path, stable_prefix=stable_prefix, store_id=store_id
    )


def _load_strict_config(
    config_path: Path,
    *,
    stable_prefix: Path | None = None,
    store_id: str | None = None,
) -> dict:
    _read_json_object(Path(config_path), "backup config")
    try:
        config = load_backup_config(Path(config_path))
    except (OSError, TypeError, ValueError) as exc:
        raise ValueError("backup config is not runnable") from exc
    if store_id is not None:
        matches = [store for store in config["stores"] if store["id"] == store_id]
        if len(matches) != 1:
            raise ValueError("backup config must contain the explicit P030 store id")
        store = matches[0]
        if store["class"] != "protected":
            raise ValueError("P030 backup store class must be protected")
        if stable_prefix is not None and Path(store["path"]).resolve() != Path(
            stable_prefix
        ).resolve():
            raise ValueError("P030 backup store path must equal the stable prefix")
    return config


def _complete_p026_run(
    config: dict, records: list[dict], *, run_id: str, store_id: str
) -> dict:
    starts = [
        record
        for record in records
        if record.get("record") == "run_start" and record.get("run_id") == run_id
    ]
    ends = [
        record
        for record in records
        if record.get("record") == "run_end" and record.get("run_id") == run_id
    ]
    failure = "restore requires one complete successful P026 run"
    if len(starts) != 1 or len(ends) != 1:
        raise ValueError(failure)
    if starts[0].get("schema") != MANIFEST_SCHEMA or starts[0].get("dry_run") is not False:
        raise ValueError(failure)
    end = ends[0]
    if end.get("status") != "ok" or end.get("errors") != []:
        raise ValueError(failure)
    run_records = [record for record in records if record.get("run_id") == run_id]
    if any(
        record.get("record") not in {"run_start", "file", "run_end"}
        for record in run_records
    ):
        raise ValueError(failure)
    files = [record for record in run_records if record.get("record") == "file"]
    if (
        isinstance(end.get("files"), bool)
        or not isinstance(end.get("files"), int)
        or end["files"] != len(files)
        or any(record.get("store_id") != store_id for record in files)
        or any(record.get("readback") != "match" for record in files)
    ):
        raise ValueError(failure)
    backup_root = Path(config["backup_root"])
    archived_prefix = resolve_confined_path(backup_root, "runs", run_id, store_id)
    stable = _verify_stable_receipt(
        archived_prefix,
        archived_prefix / STABLE_RECEIPT_NAME,
        verify_source=False,
    )
    expected = {STABLE_RECEIPT_NAME, stable["snapshot_rel"]}
    actual = [record.get("rel") for record in files]
    if (
        any(not isinstance(rel, str) for rel in actual)
        or len(actual) != len(expected)
        or set(actual) != expected
    ):
        raise ValueError(failure)
    return stable


def _restore_preflight(config_path: Path, *, run_id: str, store_id: str) -> dict:
    config = _load_strict_config(config_path, store_id=store_id)
    manifest_path = Path(config["backup_root"]) / "manifest.jsonl"
    records = _read_strict_jsonl(manifest_path, "P026 manifest")
    _complete_p026_run(config, records, run_id=run_id, store_id=store_id)
    return config


def backup_stable_prefix(
    config_path: Path, *, stable_receipt: Path, store_id: str, source_root: Path
) -> str:
    stable_prefix = Path(stable_receipt).resolve().parent
    config = load_runnable_config(
        Path(config_path), stable_prefix=stable_prefix, store_id=store_id
    )
    _verify_stable_receipt(
        stable_prefix,
        stable_receipt,
        verify_source=True,
        source_root=source_root,
    )
    manifest_path = Path(config["backup_root"]) / "manifest.jsonl"
    before_count = (
        len(_read_strict_jsonl(manifest_path, "P026 manifest"))
        if manifest_path.exists()
        else 0
    )
    _load_strict_config(
        Path(config_path), stable_prefix=stable_prefix, store_id=store_id
    )
    result = backup.run_backup(Path(config_path), dry_run=False, store_filter={store_id})
    if result != RC_OK:
        raise ValueError("P026 backup failed")
    _verify_stable_receipt(
        stable_prefix,
        stable_receipt,
        verify_source=True,
        source_root=source_root,
    )
    records = _read_strict_jsonl(manifest_path, "P026 manifest")
    starts = [
        record
        for record in records[before_count:]
        if record.get("record") == "run_start" and isinstance(record.get("run_id"), str)
    ]
    if len(starts) != 1:
        raise ValueError("P026 backup did not produce one identifiable run")
    run_id = starts[0]["run_id"]
    _complete_p026_run(config, records, run_id=run_id, store_id=store_id)
    return run_id


def restore_verified_prefix(
    config_path: Path, *, run_id: str, store_id: str, target: Path
) -> Path:
    _restore_preflight(Path(config_path), run_id=run_id, store_id=store_id)
    target = Path(target).resolve()
    if not target.is_dir() or any(target.iterdir()):
        raise ValueError("restore target must be empty")
    if restore.run_restore(
        Path(config_path), run_id, None, check_only=True, store_filter={store_id}
    ) != RC_OK:
        raise ValueError("P026 check-only failed; restore withheld")
    _restore_preflight(Path(config_path), run_id=run_id, store_id=store_id)
    if restore.run_restore(
        Path(config_path), run_id, target, check_only=False, store_filter={store_id}
    ) != RC_OK:
        raise ValueError("P026 restore failed")
    restored_prefix = resolve_confined_path(target, store_id)
    stable = _verify_stable_receipt(
        restored_prefix, restored_prefix / STABLE_RECEIPT_NAME, verify_source=False
    )
    verified = {
        "schema": "p030.verified_restore/v1",
        "state": "verified_restore",
        "run_id": run_id,
        "store_id": store_id,
        "restored_prefix": str(restored_prefix),
        **{
            key: stable[key]
            for key in (
                "high_water_bytes",
                "record_count",
                "last_observation_id",
                "prefix_sha256",
                "captured_at_utc",
                "dataset_content_hash",
            )
        },
    }
    verified_path = target / VERIFIED_RESTORE_RECEIPT_NAME
    atomic_write_json(verified_path, verified)
    return verified_path
