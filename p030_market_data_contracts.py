"""Pure, offline identity contracts for P030 market-data evidence."""
from __future__ import annotations

import hashlib
import json
import math
import re
from decimal import Decimal, InvalidOperation
from typing import Any, Iterable, Mapping, Sequence


class ContractRefused(ValueError):
    """Input cannot be identified without violating the frozen contract."""


ALGORITHM = "sha256"
CANONICALIZATION_VERSION = "p030-json-array-v1"
EVENT_SCHEMA_VERSION = "mtc.p030_event/v1"
PROVENANCE_SCHEMA_VERSION = "mtc.p030_provenance/v1"
SOURCE_PRODUCERS = frozenset({"WS_LIVE", "CANDLE_SNAPSHOT", "PROXY_DOWNLOAD"})
TRACKS = frozenset({"NATIVE", "PROXY"})

EVENT_FAMILIES = frozenset({
    "GAP",
    "FEED_DIVERGENCE",
    "RECONNECT",
    "FRESHNESS_TRANSITION",
    "BACKFILL_RUN",
    "PROXY_NATIVE_DIVERGENCE",
    "RECONCILIATION_STATUS",
    "CORRECTION",
    "ARCHIVE_DISPOSITION",
})

PAYLOAD_FIELDS = (
    "venue", "source_producer", "symbol", "interval", "bar_open_time",
    "bar_close_time", "open", "high", "low", "close", "volume", "venue_seq",
)
OBSERVATION_FIELDS = (
    "venue", "track", "proxy_source", "source_producer", "symbol", "interval",
    "bar_open_time", "producer_payload_hash", "observation_type",
    "supersedes_observation_id",
)
EVENT_FIELDS = (
    "schema_version", "record_type", "producer", "symbol", "interval", "slot_id",
    "observation_ids", "window_start", "window_end", "detected_at", "detail",
    "env_lineage_id", "deployment_identity_hash",
)
DATASET_DESCRIPTOR_FIELDS = (
    "venue", "track", "proxy_source", "window_start", "window_end",
    "content_hash_algorithm", "canonicalization_version",
)
DATASET_ROW_FIELDS = (
    "observation_id", "producer_payload_hash", "symbol", "interval", "bar_open_time",
    "bar_close_time", "open", "high", "low", "close", "volume", "venue", "track",
    "proxy_source", "source_producer", "observation_type", "supersedes_observation_id",
    "ingest_time", "venue_seq", "env_lineage_id", "schema_version",
)
MANIFEST_FIELDS = (
    "schema_version", "venue", "track", "proxy_source", "window_start", "window_end",
    "native_fraction", "proxy_fraction", "archive_schema_version", "env_lineage_id",
    "dataset_content_hash", "content_hash_algorithm", "canonicalization_version",
    "partitions",
)
PARTITION_FIELDS = (
    "path", "file_sha256", "size_bytes", "partition_state", "high_water_bytes",
    "record_count", "last_observation_id",
)

_HASH = re.compile(r"^[0-9a-f]{64}$")
_WINDOWS_DRIVE = re.compile(r"^[A-Za-z]:")
def _mapping(value: object, label: str) -> dict[str, Any]:
    if type(value) is not dict:
        raise ContractRefused(f"{label} must be an exact object")
    return dict(value)


def _exact(record: Mapping[str, Any], fields: Sequence[str], label: str) -> None:
    if any(type(key) is not str for key in record):
        raise ContractRefused(f"{label} keys must be strings")
    missing = [field for field in fields if field not in record]
    extra = sorted(set(record) - set(fields))
    if missing or extra:
        raise ContractRefused(f"{label} fields mismatch: missing={missing}, extra={extra}")


def _string(value: object, label: str, *, nullable: bool = False) -> str | None:
    if value is None and nullable:
        return None
    if type(value) is not str or not value:
        raise ContractRefused(f"{label} must be a non-empty string")
    return value


def _source_producer(value: object, label: str) -> None:
    if _string(value, label) not in SOURCE_PRODUCERS:
        raise ContractRefused(f"{label} is unknown")


def _track_proxy(record: Mapping[str, Any], label: str) -> None:
    track = _string(record["track"], f"{label}.track")
    proxy = _string(record["proxy_source"], f"{label}.proxy_source", nullable=True)
    if track not in TRACKS:
        raise ContractRefused(f"{label}.track is unknown")
    if track == "NATIVE" and proxy is not None:
        raise ContractRefused(f"{label}.proxy_source must be null for NATIVE track")
    if track == "PROXY" and proxy is None:
        raise ContractRefused(f"{label}.proxy_source is required for PROXY track")


def _producer_track_proxy(record: Mapping[str, Any], label: str) -> None:
    _source_producer(record["source_producer"], f"{label}.source_producer")
    _track_proxy(record, label)
    expected_track = "PROXY" if record["source_producer"] == "PROXY_DOWNLOAD" else "NATIVE"
    if record["track"] != expected_track:
        raise ContractRefused(f"{label}.source_producer does not match track")


def _integer(value: object, label: str, *, nullable: bool = False) -> int | None:
    if value is None and nullable:
        return None
    if type(value) is not int:
        raise ContractRefused(f"{label} must be an integer")
    return value


def _decimal_string(value: object, label: str) -> str:
    if type(value) is not str or not value:
        raise ContractRefused(f"{label} must be a decimal string")
    try:
        number = Decimal(value)
    except InvalidOperation as error:
        raise ContractRefused(f"{label} must be a decimal string") from error
    if not number.is_finite():
        raise ContractRefused(f"{label} must be finite")
    return value


def _json_native(value: object, label: str) -> None:
    value_type = type(value)
    if value is None or value_type in {str, bool, int}:
        return
    if value_type is float:
        if not math.isfinite(value):
            raise ContractRefused(f"{label} must contain only finite numbers")
        return
    if value_type is list:
        for index, item in enumerate(value):
            _json_native(item, f"{label}[{index}]")
        return
    if value_type is dict:
        for key, item in value.items():
            if type(key) is not str:
                raise ContractRefused(f"{label} object keys must be strings")
            _json_native(item, f"{label}.{key}")
        return
    raise ContractRefused(f"{label} contains an unsupported JSON value")


def _hash(value: object, label: str, *, prefix: str | None = None) -> str:
    value = _string(value, label)
    assert value is not None
    if prefix is None:
        valid = bool(_HASH.fullmatch(value))
    else:
        valid = value.startswith(prefix + ":") and bool(_HASH.fullmatch(value[len(prefix) + 1 :]))
    if not valid:
        raise ContractRefused(f"{label} has invalid hash identity")
    return value


def _canonical_id(prefix: str, domain: str, values: Sequence[Any]) -> str:
    try:
        payload = json.dumps(
            [domain, *values], ensure_ascii=False, allow_nan=False,
            separators=(",", ":"), sort_keys=True,
        ).encode("utf-8")
    except (TypeError, ValueError) as error:
        raise ContractRefused(f"{domain} contains a non-canonical value") from error
    return f"{prefix}:{hashlib.sha256(payload).hexdigest()}"


def _record_id(prefix: str, domain: str, record: Mapping[str, Any], fields: Sequence[str]) -> str:
    return _canonical_id(prefix, domain, [record[field] for field in fields])


def producer_payload_hash(record: Mapping[str, Any]) -> str:
    record = _mapping(record, "producer payload")
    _exact(record, PAYLOAD_FIELDS, "producer payload")
    for field in ("venue", "symbol", "interval"):
        _string(record[field], f"producer payload.{field}")
    _source_producer(record["source_producer"], "producer payload.source_producer")
    for field in ("bar_open_time", "bar_close_time"):
        _integer(record[field], f"producer payload.{field}")
    for field in ("open", "high", "low", "close", "volume"):
        _decimal_string(record[field], f"producer payload.{field}")
    _integer(record["venue_seq"], "producer payload.venue_seq", nullable=True)
    return _record_id("p030payload-v1", "p030-payload-v1", record, PAYLOAD_FIELDS)


def _validate_observation(record: Mapping[str, Any]) -> None:
    _exact(record, OBSERVATION_FIELDS, "observation")
    for field in ("venue", "symbol", "interval"):
        _string(record[field], f"observation.{field}")
    _producer_track_proxy(record, "observation")
    _integer(record["bar_open_time"], "observation.bar_open_time")
    _hash(record["producer_payload_hash"], "observation.producer_payload_hash",
          prefix="p030payload-v1")
    kind = _string(record["observation_type"], "observation.observation_type")
    if kind not in {"INITIAL", "CORRECTION"}:
        raise ContractRefused("observation.observation_type is invalid")
    predecessor = record["supersedes_observation_id"]
    if kind == "INITIAL" and predecessor is not None:
        raise ContractRefused("INITIAL observation cannot supersede another observation")
    if kind == "CORRECTION":
        _hash(predecessor, "observation.supersedes_observation_id", prefix="p030obs-v1")


def observation_id(record: Mapping[str, Any]) -> str:
    record = _mapping(record, "observation")
    _validate_observation(record)
    return _record_id("p030obs-v1", "p030-observation-v1", record, OBSERVATION_FIELDS)


def event_id(record: Mapping[str, Any]) -> str:
    record = _mapping(record, "event")
    _exact(record, EVENT_FIELDS, "event")
    schema_version = _string(record["schema_version"], "event.schema_version")
    if schema_version != EVENT_SCHEMA_VERSION:
        raise ContractRefused("event schema_version is unknown")
    record_type = _string(record["record_type"], "event.record_type")
    if record_type not in EVENT_FAMILIES:
        raise ContractRefused("event record_type is unknown")
    _source_producer(record["producer"], "event.producer")
    for field in ("symbol", "interval", "slot_id", "env_lineage_id"):
        _string(record[field], f"event.{field}")
    ids = record["observation_ids"]
    if not isinstance(ids, list) or not ids:
        raise ContractRefused("event.observation_ids must be a non-empty unique list")
    for value in ids:
        _hash(value, "event.observation_ids[]", prefix="p030obs-v1")
    if len(ids) != len(set(ids)):
        raise ContractRefused("event.observation_ids must be a non-empty unique list")
    if record_type == "CORRECTION" and len(ids) != 2:
        raise ContractRefused("CORRECTION event requires predecessor and successor ids")
    for field in ("window_start", "window_end", "detected_at"):
        _integer(record[field], f"event.{field}")
    if record["window_start"] >= record["window_end"]:
        raise ContractRefused("event window must be non-empty and increasing")
    if not isinstance(record["detail"], dict):
        raise ContractRefused("event.detail must be an object")
    _json_native(record["detail"], "event.detail")
    if record["deployment_identity_hash"] is not None:
        _hash(record["deployment_identity_hash"], "event.deployment_identity_hash")
    return _record_id("p030evt-v1", "p030-event-v1", record, EVENT_FIELDS)


def validate_correction_chain(records: Iterable[Mapping[str, Any]]) -> None:
    records = list(records)
    indexed: dict[str, Mapping[str, Any]] = {}
    slots: dict[tuple[Any, ...], str] = {}
    children: dict[str, str] = {}
    for candidate in records:
        candidate = _mapping(candidate, "correction-chain observation")
        _exact(candidate, ("observation_id", *OBSERVATION_FIELDS), "correction-chain observation")
        identity = _hash(candidate["observation_id"], "observation_id", prefix="p030obs-v1")
        body = {field: candidate[field] for field in OBSERVATION_FIELDS}
        if observation_id(body) != identity:
            raise ContractRefused("observation_id does not match observation bytes")
        if identity in indexed:
            raise ContractRefused("duplicate observation_id")
        indexed[identity] = candidate
        slot = tuple(candidate[field] for field in (
            "venue", "track", "proxy_source", "source_producer", "symbol", "interval",
            "bar_open_time",
        ))
        if candidate["observation_type"] == "INITIAL":
            if slot in slots:
                raise ContractRefused("second INITIAL observation for one producer slot")
            slots[slot] = identity

    if not indexed:
        raise ContractRefused("correction chain must contain an observation")

    for identity, candidate in indexed.items():
        if candidate["observation_type"] != "CORRECTION":
            continue
        predecessor_id = candidate["supersedes_observation_id"]
        predecessor = indexed.get(predecessor_id)
        if predecessor is None:
            raise ContractRefused("correction predecessor is missing")
        for field in ("venue", "track", "proxy_source", "source_producer", "symbol", "interval",
                      "bar_open_time"):
            if candidate[field] != predecessor[field]:
                raise ContractRefused("correction crosses producer or slot")
        if predecessor_id in children:
            raise ContractRefused("correction chain forks")
        children[predecessor_id] = identity

    for start in indexed:
        seen: set[str] = set()
        current = start
        while current in children:
            if current in seen:
                raise ContractRefused("correction chain cycles")
            seen.add(current)
            current = children[current]


def _validate_dataset_row(row: Mapping[str, Any]) -> None:
    _exact(row, DATASET_ROW_FIELDS, "dataset row")
    for field in ("bar_open_time", "bar_close_time", "ingest_time"):
        _integer(row[field], f"dataset row.{field}")
    _integer(row["venue_seq"], "dataset row.venue_seq", nullable=True)
    for field in ("open", "high", "low", "close", "volume"):
        _decimal_string(row[field], f"dataset row.{field}")
    if row["bar_close_time"] <= row["bar_open_time"]:
        raise ContractRefused("dataset row bar_close_time must be after bar_open_time")
    payload = {field: row[field] for field in PAYLOAD_FIELDS}
    if producer_payload_hash(payload) != row["producer_payload_hash"]:
        raise ContractRefused("dataset row producer_payload_hash does not match payload fields")
    body = {field: row[field] for field in OBSERVATION_FIELDS}
    if observation_id(body) != row["observation_id"]:
        raise ContractRefused("dataset row observation_id does not match row bytes")
    for field in ("env_lineage_id", "schema_version"):
        _string(row[field], f"dataset row.{field}")


def dataset_content_hash(
    slice_descriptor: Mapping[str, Any], observations: Iterable[Mapping[str, Any]]
) -> str:
    observations = list(observations)
    descriptor = _mapping(slice_descriptor, "dataset descriptor")
    _exact(descriptor, DATASET_DESCRIPTOR_FIELDS, "dataset descriptor")
    _string(descriptor["venue"], "dataset descriptor.venue")
    _track_proxy(descriptor, "dataset descriptor")
    for field in ("window_start", "window_end"):
        _integer(descriptor[field], f"dataset descriptor.{field}")
    if descriptor["window_start"] >= descriptor["window_end"]:
        raise ContractRefused("dataset window must be non-empty and increasing")
    algorithm = _string(
        descriptor["content_hash_algorithm"], "dataset content_hash_algorithm"
    )
    if algorithm != ALGORITHM:
        raise ContractRefused("dataset content_hash_algorithm is unknown")
    canonicalization = _string(
        descriptor["canonicalization_version"], "dataset canonicalization_version"
    )
    if canonicalization != CANONICALIZATION_VERSION:
        raise ContractRefused("dataset canonicalization_version is unknown")

    rows = []
    identities: set[str] = set()
    for candidate in observations:
        row = _mapping(candidate, "dataset row")
        _validate_dataset_row(row)
        for field in ("venue", "track", "proxy_source"):
            if row[field] != descriptor[field]:
                raise ContractRefused(f"dataset row {field} does not match descriptor")
        identity = row["observation_id"]
        if identity in identities:
            raise ContractRefused("duplicate observation_id in dataset")
        if not descriptor["window_start"] <= row["bar_open_time"] < descriptor["window_end"]:
            raise ContractRefused("dataset row is outside the declared window")
        identities.add(identity)
        rows.append(row)
    if not rows:
        raise ContractRefused("dataset must contain an observation")
    rows.sort(key=lambda row: (
        row["venue"], row["track"], row["source_producer"], row["symbol"], row["interval"],
        row["bar_open_time"], row["observation_id"],
    ))
    values = [descriptor[field] for field in DATASET_DESCRIPTOR_FIELDS]
    values.append([[row[field] for field in DATASET_ROW_FIELDS] for row in rows])
    return _canonical_id("p030ds-v1", "p030-dataset-v1", values)


def _fraction(value: object, label: str) -> Decimal:
    text = _decimal_string(value, label)
    number = Decimal(text)
    if number < 0 or number > 1:
        raise ContractRefused(f"{label} must be between zero and one")
    return number


def venue_provenance_manifest_hash(manifest: Mapping[str, Any]) -> str:
    manifest = _mapping(manifest, "provenance manifest")
    _exact(manifest, MANIFEST_FIELDS, "provenance manifest")
    schema_version = _string(manifest["schema_version"], "provenance.schema_version")
    if schema_version != PROVENANCE_SCHEMA_VERSION:
        raise ContractRefused("provenance schema_version is unknown")
    for field in ("venue", "archive_schema_version", "env_lineage_id"):
        _string(manifest[field], f"provenance.{field}")
    _track_proxy(manifest, "provenance")
    for field in ("window_start", "window_end"):
        _integer(manifest[field], f"provenance.{field}")
    if manifest["window_start"] >= manifest["window_end"]:
        raise ContractRefused("provenance window must be non-empty and increasing")
    if _fraction(manifest["native_fraction"], "provenance.native_fraction") + _fraction(
        manifest["proxy_fraction"], "provenance.proxy_fraction"
    ) != 1:
        raise ContractRefused("provenance fractions must sum to one")
    _hash(manifest["dataset_content_hash"], "provenance.dataset_content_hash", prefix="p030ds-v1")
    algorithm = _string(
        manifest["content_hash_algorithm"], "provenance.content_hash_algorithm"
    )
    if algorithm != ALGORITHM:
        raise ContractRefused("provenance content_hash_algorithm is unknown")
    canonicalization = _string(
        manifest["canonicalization_version"], "provenance.canonicalization_version"
    )
    if canonicalization != CANONICALIZATION_VERSION:
        raise ContractRefused("provenance canonicalization_version is unknown")

    raw_partitions = manifest["partitions"]
    if not isinstance(raw_partitions, list) or not raw_partitions:
        raise ContractRefused("provenance.partitions must be a non-empty list")
    partitions = []
    paths: set[str] = set()
    for candidate in raw_partitions:
        part = _mapping(candidate, "provenance partition")
        _exact(part, PARTITION_FIELDS, "provenance partition")
        path = _string(part["path"], "provenance partition.path")
        assert path is not None
        segments = path.split("/")
        if (
            path.startswith("/")
            or "\\" in path
            or "\0" in path
            or _WINDOWS_DRIVE.match(path)
            or any(segment in {"", ".", ".."} for segment in segments)
        ):
            raise ContractRefused(
                "provenance partition.path must be a canonical relative POSIX path"
            )
        if path in paths:
            raise ContractRefused("duplicate provenance partition path")
        paths.add(path)
        _hash(part["file_sha256"], "provenance partition.file_sha256")
        size = _integer(part["size_bytes"], "provenance partition.size_bytes")
        high_water = _integer(part["high_water_bytes"], "provenance partition.high_water_bytes")
        count = _integer(part["record_count"], "provenance partition.record_count")
        assert size is not None and high_water is not None and count is not None
        if size < 0 or high_water < 0 or high_water > size or count < 0:
            raise ContractRefused("provenance partition counts are invalid")
        partition_state = _string(
            part["partition_state"], "provenance partition.partition_state"
        )
        if partition_state not in {"closed", "live"}:
            raise ContractRefused("provenance partition_state is unknown")
        if partition_state == "closed" and high_water != size:
            raise ContractRefused("closed partition high-water must equal its byte size")
        if part["last_observation_id"] is not None:
            _hash(part["last_observation_id"], "provenance partition.last_observation_id",
                  prefix="p030obs-v1")
        partitions.append(part)
    partitions.sort(key=lambda part: part["path"])

    values = [manifest[field] for field in MANIFEST_FIELDS[:-1]]
    values.append([[part[field] for field in PARTITION_FIELDS] for part in partitions])
    return _canonical_id("p030prov-v1", "p030-provenance-v1", values)
