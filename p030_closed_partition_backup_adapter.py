"""P030 stable-prefix adapter over unchanged P026 backup/restore tools."""

from __future__ import annotations

import hashlib
import json
import math
import re
import sys
import tempfile
from contextlib import contextmanager
from pathlib import Path, PurePosixPath, PureWindowsPath
from urllib.parse import unquote


OPSA_TOOLS = Path(__file__).resolve().parent / "MTC_COMMAND_CENTER" / "tools" / "opsa"
sys.path.insert(0, str(OPSA_TOOLS))

import backup  # noqa: E402
import restore  # noqa: E402
from opsa_common import (  # noqa: E402
    COMPLETE_MARKER_NAME,
    RC_OK,
    MANIFEST_SCHEMA,
    RUN_MANIFEST_NAME,
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


def _reject_nonfinite_numbers(value: object) -> None:
    if isinstance(value, float) and not math.isfinite(value):
        raise ValueError("non-finite JSON number")
    if isinstance(value, dict):
        for nested in value.values():
            _reject_nonfinite_numbers(nested)
    elif isinstance(value, list):
        for nested in value:
            _reject_nonfinite_numbers(nested)


def _decode_json_object(raw: bytes, description: str) -> dict:
    try:
        payload = json.loads(
            raw.decode("utf-8"),
            parse_constant=_reject_nonfinite_json,
            object_pairs_hook=_reject_duplicate_json_keys,
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"invalid {description}") from exc
    if not isinstance(payload, dict):
        raise ValueError(f"invalid {description}")
    _reject_nonfinite_numbers(payload)
    return payload


def _read_json_object(path: Path, description: str) -> dict:
    try:
        raw = Path(path).read_bytes()
    except OSError as exc:
        raise ValueError(f"invalid {description}") from exc
    return _decode_json_object(raw, description)


def _decode_strict_jsonl(raw: bytes, description: str) -> list[dict]:
    try:
        lines = raw.decode("utf-8").splitlines()
    except UnicodeDecodeError as exc:
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
        _reject_nonfinite_numbers(record)
        records.append(record)
    return records


def _read_strict_jsonl(path: Path, description: str) -> list[dict]:
    try:
        raw = Path(path).read_bytes()
    except OSError as exc:
        raise ValueError(f"invalid {description}") from exc
    return _decode_strict_jsonl(raw, description)


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
            or not posix.parts
            or posix.as_posix() != candidate
            or any(part in {".", ".."} for part in posix.parts)
        ):
            raise ValueError(f"{field} must be a canonical relative POSIX path")
    return value


def _refuse_source_links(source_root: Path, source_rel: str) -> None:
    current = Path(source_root).absolute().joinpath(*PurePosixPath(source_rel).parts)
    while True:
        if current.is_symlink() or current.is_junction():
            raise ValueError(
                "source JSONL must not be a symlink or junction component"
            )
        parent = current.parent
        if parent == current:
            break
        current = parent


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
        _reject_nonfinite_numbers(record)
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
    include_bytes: bool = False,
) -> dict | tuple[dict, bytes, bytes]:
    stable_prefix = Path(stable_prefix).resolve()
    receipt_path = Path(receipt_path).resolve()
    if receipt_path != (stable_prefix / STABLE_RECEIPT_NAME).resolve():
        raise ValueError("stable receipt must belong to the stable prefix")
    try:
        receipt_raw = receipt_path.read_bytes()
    except OSError as exc:
        raise ValueError("invalid stable-prefix receipt") from exc
    receipt = _decode_json_object(receipt_raw, "stable-prefix receipt")
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
    if include_bytes:
        return receipt, receipt_raw, snapshot_prefix
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
    _validate_config_scope(config, stable_prefix=stable_prefix, store_id=store_id)
    return config


def _validate_config_scope(
    config: dict, *, stable_prefix: Path | None, store_id: str | None
) -> None:
    if store_id is None:
        return
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


@contextmanager
def _bound_strict_config(
    config_path: Path,
    *,
    stable_prefix: Path | None = None,
    store_id: str | None = None,
):
    try:
        raw = Path(config_path).read_bytes()
    except OSError as exc:
        raise ValueError("backup config is not runnable") from exc
    strict_object = _decode_json_object(raw, "backup config")
    with tempfile.TemporaryDirectory(prefix="p030-bound-config-") as temporary:
        bound_path = Path(temporary) / "config.json"
        bound_path.write_bytes(raw)
        if bound_path.read_bytes() != raw:
            raise ValueError("bound backup config bytes do not match validated input")
        try:
            config = load_backup_config(bound_path)
        except (OSError, TypeError, ValueError) as exc:
            raise ValueError("backup config is not runnable") from exc
        if config != strict_object:
            raise ValueError("bound backup config object does not match validated input")
        _validate_config_scope(
            config, stable_prefix=stable_prefix, store_id=store_id
        )
        yield bound_path, config


def _verify_isolated_config(
    config_path: Path, expected_raw: bytes, expected_config: dict
) -> None:
    try:
        raw = config_path.read_bytes()
    except OSError as exc:
        raise ValueError("isolated restore config is unavailable") from exc
    strict_config = _decode_json_object(raw, "isolated restore config")
    if raw != expected_raw:
        raise ValueError("isolated restore config bytes changed during P026 call")
    try:
        loaded_config = load_backup_config(config_path)
    except (OSError, TypeError, ValueError) as exc:
        raise ValueError("isolated restore config is not runnable") from exc
    if strict_config != expected_config or loaded_config != expected_config:
        raise ValueError("isolated restore config object changed during P026 call")


@contextmanager
def _bound_isolated_config(raw: bytes, config: dict):
    with tempfile.TemporaryDirectory(prefix="p030-bound-restore-config-") as temporary:
        config_path = Path(temporary) / "config.json"
        config_path.write_bytes(raw)
        _verify_isolated_config(config_path, raw, config)
        try:
            yield config_path
        finally:
            _verify_isolated_config(config_path, raw, config)


def _complete_p026_run(
    config: dict, records: list[dict], *, run_id: str, store_id: str
) -> tuple[dict, bytes, bytes]:
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
        type(end.get("files")) is not int
        or end["files"] != len(files)
        or any(
            type(record.get("size")) is not int or record["size"] < 0
            for record in files
        )
        or type(end.get("bytes")) is not int
        or end["bytes"] != sum(record["size"] for record in files)
        or any(record.get("store_id") != store_id for record in files)
        or any(record.get("readback") != "match" for record in files)
    ):
        raise ValueError(failure)
    backup_root = Path(config["backup_root"])
    archived_prefix = resolve_confined_path(backup_root, "runs", run_id, store_id)
    stable, receipt_raw, snapshot_raw = _verify_stable_receipt(
        archived_prefix,
        archived_prefix / STABLE_RECEIPT_NAME,
        verify_source=False,
        include_bytes=True,
    )
    expected = {STABLE_RECEIPT_NAME, stable["snapshot_rel"]}
    actual = [record.get("rel") for record in files]
    if (
        any(not isinstance(rel, str) for rel in actual)
        or len(actual) != len(expected)
        or set(actual) != expected
    ):
        raise ValueError(failure)
    return stable, receipt_raw, snapshot_raw


def _restore_manifest_snapshot(
    config: dict, *, run_id: str, store_id: str
) -> tuple[Path, bytes]:
    manifest_path = Path(config["backup_root"]) / "manifest.jsonl"
    try:
        raw = manifest_path.read_bytes()
    except OSError as exc:
        raise ValueError("invalid P026 manifest") from exc
    records = _decode_strict_jsonl(raw, "P026 manifest")
    _complete_p026_run(config, records, run_id=run_id, store_id=store_id)
    return manifest_path, raw


def _verify_manifest_snapshot(
    manifest_path: Path,
    expected: bytes,
    config: dict,
    *,
    run_id: str,
    store_id: str,
) -> None:
    try:
        actual = manifest_path.read_bytes()
    except OSError as exc:
        raise ValueError("invalid P026 manifest") from exc
    records = _decode_strict_jsonl(actual, "P026 manifest")
    if actual != expected:
        raise ValueError("P026 manifest bytes changed during P026 call")
    _complete_p026_run(config, records, run_id=run_id, store_id=store_id)


@contextmanager
def _isolated_restore_inputs(
    config: dict, manifest_raw: bytes, *, run_id: str, store_id: str
):
    source_run_dir = resolve_confined_path(Path(config["backup_root"]), "runs", run_id)
    source_prefix = resolve_confined_path(source_run_dir, store_id)
    # The P026 explicit-run restore verifies the run's COMPLETE.json + RUN_MANIFEST.jsonl
    # before it reads anything else, so the isolated root must carry the run's own
    # completion evidence byte-for-byte; a freshly written pair would defeat the gate.
    try:
        complete_raw = (source_run_dir / COMPLETE_MARKER_NAME).read_bytes()
        run_manifest_raw = (source_run_dir / RUN_MANIFEST_NAME).read_bytes()
    except OSError as exc:
        raise ValueError("P026 completion evidence is unavailable") from exc
    try:
        receipt_raw = (source_prefix / STABLE_RECEIPT_NAME).read_bytes()
    except OSError as exc:
        raise ValueError("stable-prefix receipt is unavailable") from exc
    receipt = _decode_json_object(receipt_raw, "stable-prefix receipt")
    snapshot_rel = _canonical_relative_posix(
        receipt.get("snapshot_rel"), "snapshot_rel"
    )
    try:
        snapshot_raw = resolve_confined_path(source_prefix, snapshot_rel).read_bytes()
    except OSError as exc:
        raise ValueError("snapshot prefix is unavailable") from exc

    with tempfile.TemporaryDirectory(prefix="p030-isolated-restore-") as temporary:
        isolated_root = Path(temporary) / "backup"
        isolated_run_dir = resolve_confined_path(isolated_root, "runs", run_id)
        isolated_prefix = resolve_confined_path(isolated_run_dir, store_id)
        isolated_prefix.mkdir(parents=True)
        (isolated_run_dir / COMPLETE_MARKER_NAME).write_bytes(complete_raw)
        (isolated_run_dir / RUN_MANIFEST_NAME).write_bytes(run_manifest_raw)
        (isolated_prefix / STABLE_RECEIPT_NAME).write_bytes(receipt_raw)
        isolated_snapshot = resolve_confined_path(isolated_prefix, snapshot_rel)
        isolated_snapshot.parent.mkdir(parents=True, exist_ok=True)
        isolated_snapshot.write_bytes(snapshot_raw)
        isolated_manifest = isolated_root / "manifest.jsonl"
        isolated_manifest.write_bytes(manifest_raw)

        isolated_config = {**config, "backup_root": str(isolated_root)}
        isolated_config_raw = (
            json.dumps(
                isolated_config,
                ensure_ascii=False,
                sort_keys=True,
                indent=2,
                allow_nan=False,
            )
            + "\n"
        ).encode("utf-8")
        strict_config = _decode_json_object(
            isolated_config_raw, "isolated restore config"
        )
        if strict_config != isolated_config:
            raise ValueError("isolated restore config object does not match snapshot")
        manifest_path, validated_raw = _restore_manifest_snapshot(
            isolated_config, run_id=run_id, store_id=store_id
        )
        if validated_raw != manifest_raw:
            raise ValueError("isolated P026 manifest bytes do not match validated input")
        yield (
            isolated_config_raw,
            isolated_config,
            manifest_path,
            validated_raw,
            receipt_raw,
            snapshot_rel,
            snapshot_raw,
        )


def backup_stable_prefix(
    config_path: Path, *, stable_receipt: Path, store_id: str, source_root: Path
) -> str:
    stable_prefix = Path(stable_receipt).resolve().parent
    with _bound_strict_config(
        Path(config_path), stable_prefix=stable_prefix, store_id=store_id
    ) as (bound_config_path, config):
        _, receipt_before, snapshot_before = _verify_stable_receipt(
            stable_prefix,
            stable_receipt,
            verify_source=True,
            source_root=source_root,
            include_bytes=True,
        )
        prevalidated_staging = receipt_before, snapshot_before
        manifest_path = Path(config["backup_root"]) / "manifest.jsonl"
        before_count = (
            len(_read_strict_jsonl(manifest_path, "P026 manifest"))
            if manifest_path.exists()
            else 0
        )
        result = backup.run_backup(
            bound_config_path, dry_run=False, store_filter={store_id}
        )
        if result != RC_OK:
            raise ValueError("P026 backup failed")
        _, receipt_after, snapshot_after = _verify_stable_receipt(
            stable_prefix,
            stable_receipt,
            verify_source=True,
            source_root=source_root,
            include_bytes=True,
        )
        if (receipt_after, snapshot_after) != prevalidated_staging:
            raise ValueError(
                "post-P026 stable prefix differs from prevalidated staging bytes"
            )
        records = _read_strict_jsonl(manifest_path, "P026 manifest")
        starts = [
            record
            for record in records[before_count:]
            if record.get("record") == "run_start"
            and isinstance(record.get("run_id"), str)
        ]
        if len(starts) != 1:
            raise ValueError("P026 backup did not produce one identifiable run")
        run_id = starts[0]["run_id"]
        _, archived_receipt, archived_snapshot = _complete_p026_run(
            config, records, run_id=run_id, store_id=store_id
        )
        if (archived_receipt, archived_snapshot) != prevalidated_staging:
            raise ValueError(
                "archived stable prefix differs from prevalidated staging bytes"
            )
        return run_id


def restore_verified_prefix(
    config_path: Path, *, run_id: str, store_id: str, target: Path
) -> Path:
    with _bound_strict_config(Path(config_path), store_id=store_id) as (_, config):
        target = Path(target).resolve()
        if not target.is_dir() or any(target.iterdir()):
            raise ValueError("restore target must be empty")
        manifest_path, manifest_before = _restore_manifest_snapshot(
            config, run_id=run_id, store_id=store_id
        )
        with _isolated_restore_inputs(
            config, manifest_before, run_id=run_id, store_id=store_id
        ) as (
            isolated_config_raw,
            isolated_config,
            isolated_manifest,
            isolated_manifest_raw,
            isolated_receipt_raw,
            isolated_snapshot_rel,
            isolated_snapshot_raw,
        ):
            with _bound_isolated_config(
                isolated_config_raw, isolated_config
            ) as check_config_path:
                check_result = restore.run_restore(
                    check_config_path,
                    run_id,
                    None,
                    check_only=True,
                    store_filter={store_id},
                )
            _verify_manifest_snapshot(
                isolated_manifest,
                isolated_manifest_raw,
                isolated_config,
                run_id=run_id,
                store_id=store_id,
            )
            _verify_manifest_snapshot(
                manifest_path,
                manifest_before,
                config,
                run_id=run_id,
                store_id=store_id,
            )
            if check_result != RC_OK:
                raise ValueError("P026 check-only failed; restore withheld")
            if not target.is_dir() or any(target.iterdir()):
                raise ValueError("restore target must be empty")
            with _bound_isolated_config(
                isolated_config_raw, isolated_config
            ) as restore_config_path:
                if not target.is_dir() or any(target.iterdir()):
                    raise ValueError("restore target must be empty")
                restore_result = restore.run_restore(
                    restore_config_path,
                    run_id,
                    target,
                    check_only=False,
                    store_filter={store_id},
                )
            _verify_manifest_snapshot(
                isolated_manifest,
                isolated_manifest_raw,
                isolated_config,
                run_id=run_id,
                store_id=store_id,
            )
            _verify_manifest_snapshot(
                manifest_path,
                manifest_before,
                config,
                run_id=run_id,
                store_id=store_id,
            )
            if restore_result != RC_OK:
                raise ValueError("P026 restore failed")
    restored_prefix = resolve_confined_path(target, store_id)
    stable, restored_receipt_raw, restored_snapshot_raw = _verify_stable_receipt(
        restored_prefix,
        restored_prefix / STABLE_RECEIPT_NAME,
        verify_source=False,
        include_bytes=True,
    )
    expected_files = {STABLE_RECEIPT_NAME, isolated_snapshot_rel}
    expected_directories = {
        parent.as_posix()
        for parent in PurePosixPath(isolated_snapshot_rel).parents
        if parent != PurePosixPath(".")
    }
    expected_entries = expected_files | expected_directories
    actual_entries = {
        path.relative_to(restored_prefix).as_posix(): path
        for path in restored_prefix.rglob("*")
    }
    if set(actual_entries) != expected_entries:
        raise ValueError("restored stable prefix differs from validated archive members")
    if any(
        actual_entries[rel].is_symlink()
        or actual_entries[rel].is_junction()
        or not actual_entries[rel].is_dir()
        for rel in expected_directories
    ) or any(
        actual_entries[rel].is_symlink()
        or actual_entries[rel].is_junction()
        or not actual_entries[rel].is_file()
        for rel in expected_files
    ):
        raise ValueError("restored stable prefix differs from validated archive members")
    if (
        restored_receipt_raw != isolated_receipt_raw
        or restored_snapshot_raw != isolated_snapshot_raw
    ):
        raise ValueError("restored stable prefix differs from validated archive bytes")
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
