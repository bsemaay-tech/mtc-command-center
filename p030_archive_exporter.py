"""Shape-B exporter from collector archive JSONL to P030 canonical JSONL."""

from __future__ import annotations

import hashlib
import json
import math
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

from p030_market_data_contracts import (
    ALGORITHM,
    CANONICALIZATION_VERSION,
    DATASET_ROW_FIELDS,
    OBSERVATION_FIELDS,
    PAYLOAD_FIELDS,
    ContractRefused,
    dataset_content_hash,
    observation_id,
    producer_payload_hash,
)


class ExportRefused(ValueError):
    """Exporter refused to create a backup-facing partition."""

    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code


@dataclass(frozen=True)
class ExportReceipt:
    path: Path
    schema: str
    source_path: str
    source_sha256: str
    source_record_count: int
    exporter_sha256: str
    exported_sha256: str
    exported_record_count: int
    dataset_content_hash: str
    exported_at_utc: str
    identity_recomputed: bool

    def as_dict(self) -> dict[str, Any]:
        return {
            "schema": self.schema,
            "source_path": self.source_path,
            "source_sha256": self.source_sha256,
            "source_record_count": self.source_record_count,
            "exporter_sha256": self.exporter_sha256,
            "exported_sha256": self.exported_sha256,
            "exported_record_count": self.exported_record_count,
            "dataset_content_hash": self.dataset_content_hash,
            "exported_at_utc": self.exported_at_utc,
            "identity_recomputed": self.identity_recomputed,
        }


_BARE_SHA256 = re.compile(r"^[0-9a-f]{64}$")
_PAYLOAD_ID = re.compile(r"^p030payload-v1:[0-9a-f]{64}$")
_OBSERVATION_ID = re.compile(r"^p030obs-v1:[0-9a-f]{64}$")


def _refuse(code: str, message: str) -> None:
    raise ExportRefused(code, message)


def _reject_nonfinite_json(value: str) -> None:
    raise ValueError(f"non-finite JSON constant: {value}")


def _reject_duplicate_json_keys(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
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


def _utc_z(value: str) -> str:
    if not isinstance(value, str) or not value.endswith("Z"):
        _refuse(
            "invalid_timestamp",
            "exported_at_utc must be a caller-supplied UTC Z timestamp",
        )
    try:
        parsed = datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError as exc:
        raise ExportRefused(
            "invalid_timestamp",
            "exported_at_utc must be a caller-supplied UTC Z timestamp",
        ) from exc
    if parsed.utcoffset() is None:
        _refuse(
            "invalid_timestamp",
            "exported_at_utc must be a caller-supplied UTC Z timestamp",
        )
    # The backup adapter's whole-second convention (p030_closed_partition_backup_adapter.py
    # `_utc_z`: "must use whole seconds"); a sub-second receipt timestamp would be refused there.
    if parsed.microsecond:
        _refuse("invalid_timestamp", "exported_at_utc must use whole seconds")
    return value


def _source_rel(source_jsonl: Path, source_root: Path) -> str:
    source_root_abs = Path(source_root).absolute()
    source_abs = Path(source_jsonl).absolute()
    try:
        return source_abs.relative_to(source_root_abs).as_posix()
    except ValueError as exc:
        raise ExportRefused(
            "source_outside_root", "source_path must be relative to source_root"
        ) from exc


def _read_source_once(source_jsonl: Path) -> bytes:
    path = Path(source_jsonl)
    try:
        expected_size = path.stat().st_size
        with path.open("rb") as handle:
            data = handle.read()
            observed_size = handle.tell()
    except OSError as exc:
        raise ExportRefused(
            "source_unreadable", "source partition is unreadable"
        ) from exc
    if observed_size != expected_size or len(data) != expected_size:
        _refuse("short_read", "source partition read was short or partial")
    if not data:
        _refuse("empty_partition", "source partition is empty")
    if not data.endswith(b"\n"):
        _refuse("short_read", "source partition ends with a partial line")
    return data


def _decode_source_line(raw_line: bytes, line_number: int) -> dict[str, Any]:
    line_break = b"\r\n" if raw_line.endswith(b"\r\n") else b"\n"
    try:
        record = json.loads(
            raw_line,
            parse_constant=_reject_nonfinite_json,
            object_pairs_hook=_reject_duplicate_json_keys,
        )
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
        raise ExportRefused(
            "source_line_invalid", f"source line {line_number} is not parseable JSON"
        ) from exc
    if type(record) is not dict:
        _refuse(
            "source_line_invalid", f"source line {line_number} is not a JSON object"
        )
    try:
        # json.loads turns an overflowing token such as 1e999 into inf without consulting
        # parse_constant; the walk below is the only guard, so its ValueError must surface
        # as the same refusal code as a NaN/Infinity literal.
        _reject_nonfinite_numbers(record)
    except ValueError as exc:
        raise ExportRefused(
            "source_line_invalid",
            f"source line {line_number} carries a non-finite number",
        ) from exc
    try:
        canonical = (
            json.dumps(
                record,
                ensure_ascii=False,
                allow_nan=False,
                separators=(",", ":"),
            ).encode("utf-8")
            + line_break
        )
    except (TypeError, ValueError) as exc:
        raise ExportRefused(
            "source_line_noncanonical",
            f"source line {line_number} is not canonical JSONL",
        ) from exc
    if canonical != raw_line:
        _refuse(
            "source_line_noncanonical",
            f"source line {line_number} is not canonical JSONL",
        )
    return record


def _reidentify(row: dict[str, Any], line_number: int) -> dict[str, Any]:
    missing = [field for field in DATASET_ROW_FIELDS if field not in row]
    extra = sorted(set(row) - set(DATASET_ROW_FIELDS))
    if missing or extra:
        _refuse(
            "source_fields_mismatch",
            f"source line {line_number} fields mismatch: missing={missing}, extra={extra}",
        )

    payload = {field: row[field] for field in PAYLOAD_FIELDS}
    try:
        payload_hash = producer_payload_hash(payload)
    except ContractRefused as exc:
        raise ExportRefused("contract_refused", str(exc)) from exc

    old_payload_hash = row["producer_payload_hash"]
    if (
        _PAYLOAD_ID.fullmatch(str(old_payload_hash))
        and old_payload_hash != payload_hash
    ):
        _refuse(
            "identity_mismatch",
            "stored prefixed producer_payload_hash disagrees with payload fields",
        )
    if not (
        _BARE_SHA256.fullmatch(str(old_payload_hash))
        or old_payload_hash == payload_hash
    ):
        _refuse(
            "identity_mismatch",
            "producer_payload_hash is neither collector bare hex nor recomputed P030 identity",
        )

    candidate = dict(row)
    candidate["producer_payload_hash"] = payload_hash
    observation = {field: candidate[field] for field in OBSERVATION_FIELDS}
    try:
        obs_id = observation_id(observation)
    except ContractRefused as exc:
        raise ExportRefused("contract_refused", str(exc)) from exc

    old_obs_id = row["observation_id"]
    if _OBSERVATION_ID.fullmatch(str(old_obs_id)) and old_obs_id != obs_id:
        _refuse(
            "identity_mismatch",
            "stored prefixed observation_id disagrees with row bytes",
        )
    if not (_BARE_SHA256.fullmatch(str(old_obs_id)) or old_obs_id == obs_id):
        _refuse(
            "identity_mismatch",
            "observation_id is neither collector bare hex nor recomputed P030 identity",
        )

    candidate["observation_id"] = obs_id
    return {field: candidate[field] for field in DATASET_ROW_FIELDS}


def _descriptor(rows: list[dict[str, Any]]) -> dict[str, Any]:
    first = rows[0]
    descriptor = {
        "venue": first["venue"],
        "track": first["track"],
        "proxy_source": first["proxy_source"],
        "window_start": min(row["bar_open_time"] for row in rows),
        "window_end": max(row["bar_close_time"] for row in rows),
        "content_hash_algorithm": ALGORITHM,
        "canonicalization_version": CANONICALIZATION_VERSION,
    }
    for row in rows:
        for field in ("venue", "track", "proxy_source"):
            if row[field] != descriptor[field]:
                _refuse(
                    "mixed_dataset_descriptor",
                    f"dataset row {field} does not match descriptor",
                )
    return descriptor


def _receipt_path(target_jsonl: Path) -> Path:
    return Path(str(target_jsonl) + ".p030export.json")


def export_partition(
    source_jsonl: Path,
    target_jsonl: Path,
    *,
    source_root: Path,
    exported_at_utc: str,
) -> ExportReceipt:
    source_jsonl = Path(source_jsonl)
    target_jsonl = Path(target_jsonl)
    if target_jsonl.exists():
        _refuse("target_exists", "target partition already exists")
    receipt_path = _receipt_path(target_jsonl)
    if receipt_path.exists():
        _refuse("receipt_exists", "export receipt already exists")

    exported_at_utc = _utc_z(exported_at_utc)
    source_rel = _source_rel(source_jsonl, source_root)
    source_bytes = _read_source_once(source_jsonl)

    rows = [
        _reidentify(_decode_source_line(raw_line, line_number), line_number)
        for line_number, raw_line in enumerate(
            source_bytes.splitlines(keepends=True), start=1
        )
    ]
    if not rows:
        _refuse("empty_partition", "source partition is empty")

    exported = b"".join(
        (
            json.dumps(
                row,
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
                allow_nan=False,
            )
            + "\n"
        ).encode("utf-8")
        for row in rows
    )
    try:
        # whole-slice validations (window ordering, duplicate observation ids, ...) live in the
        # contracts module; their refusal must carry the exporter's code, never leak raw
        dataset_hash = dataset_content_hash(_descriptor(rows), rows)
    except ContractRefused as exc:
        raise ExportRefused("contract_refused", str(exc)) from exc
    try:
        target_jsonl.parent.mkdir(parents=True, exist_ok=True)
        with target_jsonl.open("xb") as handle:
            handle.write(exported)
            handle.flush()
    except FileExistsError as exc:
        raise ExportRefused("target_exists", "target partition already exists") from exc
    except OSError as exc:
        raise ExportRefused(
            "target_unwritable", "target partition is unwritable"
        ) from exc
    try:
        reread = target_jsonl.read_bytes()
    except OSError as exc:
        raise ExportRefused(
            "target_verify_failed", "target partition cannot be re-read"
        ) from exc
    if reread != exported:
        _refuse(
            "target_verify_failed",
            "target partition re-read differs from exported bytes",
        )

    receipt = ExportReceipt(
        path=receipt_path,
        schema="p030.archive_export/v1",
        source_path=source_rel,
        source_sha256=hashlib.sha256(source_bytes).hexdigest(),
        source_record_count=len(rows),
        exporter_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        exported_sha256=hashlib.sha256(exported).hexdigest(),
        exported_record_count=len(rows),
        dataset_content_hash=dataset_hash,
        exported_at_utc=exported_at_utc,
        identity_recomputed=True,
    )
    receipt_raw = (
        json.dumps(
            receipt.as_dict(),
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        )
        + "\n"
    ).encode("utf-8")
    try:
        with receipt_path.open("xb") as handle:
            handle.write(receipt_raw)
            handle.flush()
    except FileExistsError as exc:
        raise ExportRefused("receipt_exists", "export receipt already exists") from exc
    except OSError as exc:
        raise ExportRefused(
            "receipt_unwritable", "export receipt is unwritable"
        ) from exc
    return receipt
