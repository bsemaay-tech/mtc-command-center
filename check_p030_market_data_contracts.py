"""Independent executable contract checks for P030 market-data identities."""
from __future__ import annotations

import argparse
import copy
import hashlib
import inspect
import json
import socket
from collections.abc import Mapping
from typing import Any, Callable


EVENT_FAMILIES = (
    "GAP",
    "FEED_DIVERGENCE",
    "RECONNECT",
    "FRESHNESS_TRANSITION",
    "BACKFILL_RUN",
    "PROXY_NATIVE_DIVERGENCE",
    "RECONCILIATION_STATUS",
    "CORRECTION",
    "ARCHIVE_DISPOSITION",
)

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


class EvilProducer(str):
    def __new__(cls):
        return super().__new__(cls, "EVIL_PRODUCER")

    def __hash__(self) -> int:
        return hash("WS_LIVE")

    def __eq__(self, other: object) -> bool:
        return type(other) is str and other == "WS_LIVE"


class StatefulEventMapping(Mapping):
    def __init__(self, record: dict[str, Any]):
        self.record = record
        self.producer_reads = 0

    def __getitem__(self, key: str) -> Any:
        if key == "producer":
            self.producer_reads += 1
            return "WS_LIVE" if self.producer_reads == 1 else "EVIL_AFTER_VALIDATION"
        return self.record[key]

    def __iter__(self):
        return iter(self.record)

    def __len__(self) -> int:
        return len(self.record)

    def __contains__(self, key: object) -> bool:
        return key in self.record

# Frozen output of this checker's independent oracle; never computed by the subject.
GOLDEN_PAYLOAD = "p030payload-v1:8653c7ea1416f6cc2a7f170966c9be31da58780d3db30d6c679fdbd106868c28"
GOLDEN_INITIAL = "p030obs-v1:ba4ee258065990a144aabdcebb416cabcde617d57dc7bc7f793449f344cbe115"
GOLDEN_CORRECTION = "p030obs-v1:df1e71d5dc81db01b17e444c38c1ad3babfa6d2664757c5d09ef782fcd0ccaf6"
GOLDEN_EVENTS = {
    "GAP": "p030evt-v1:baa891227c18d4b0b8b867ab33f89303c79eb4cd2a6a813d30739833f475412c",
    "FEED_DIVERGENCE": "p030evt-v1:bfa4577c0db35cfa053fb1b285db99dfb25d8e03639ebece5054d87d77f349e3",
    "RECONNECT": "p030evt-v1:af62d5f74e32e93c33d24dd782b9eb620a991ffe1675356cee9c33138a4a3f67",
    "FRESHNESS_TRANSITION": "p030evt-v1:72ec4a3d8373cbf0a68f31dafe889363f9c434124756c65af1b574272f19b184",
    "BACKFILL_RUN": "p030evt-v1:50bc030c1e79bff75f4dd26dd28c7b87c2458035cad2cf1f359494e5d75defc3",
    "PROXY_NATIVE_DIVERGENCE": "p030evt-v1:6ddafc346661c14fc7da4d531120f1b47023397fb23e7fd479d8eeed1cace141",
    "RECONCILIATION_STATUS": "p030evt-v1:e47ba26dba1d005c685064a02f21eadcf5bf30ce3855b09bceb1cff0cff5128f",
    "CORRECTION": "p030evt-v1:a7f6a1a433a95295e809824af1373f6428646915403e5df247e594eebefffe7d",
    "ARCHIVE_DISPOSITION": "p030evt-v1:4a6e10a7b75e01587f4d61693ea5c80b82be5a4e9462e53f57e713bfa88531d2",
}
GOLDEN_DATASET = "p030ds-v1:6588c17b996d3b4ea7e7a7cdfd5341ea0a6a967c88568df412aedab504438630"
GOLDEN_MANIFEST = "p030prov-v1:2ac2b33da292e4cee1c74e4e94511a10691bf4c25a44614731b9d050a71b1f03"


def oracle_id(prefix: str, domain: str, values: list[Any]) -> str:
    payload = json.dumps(
        [domain, *values], ensure_ascii=False, allow_nan=False,
        separators=(",", ":"), sort_keys=True,
    ).encode("utf-8")
    return f"{prefix}:{hashlib.sha256(payload).hexdigest()}"


def oracle_record_id(prefix: str, domain: str, record: dict[str, Any], fields) -> str:
    return oracle_id(prefix, domain, [record[field] for field in fields])


def payload() -> dict[str, Any]:
    return {
        "venue": "HYPERLIQUID", "source_producer": "WS_LIVE", "symbol": "BTC",
        "interval": "15m", "bar_open_time": 1769903100000,
        "bar_close_time": 1769904000000, "open": "100", "high": "103",
        "low": "99", "close": "102", "volume": "12.5", "venue_seq": None,
    }


def initial_observation(payload_hash: str) -> dict[str, Any]:
    return {
        "venue": "HYPERLIQUID", "track": "NATIVE", "proxy_source": None,
        "source_producer": "WS_LIVE", "symbol": "BTC", "interval": "15m",
        "bar_open_time": 1769903100000, "producer_payload_hash": payload_hash,
        "observation_type": "INITIAL", "supersedes_observation_id": None,
    }


def correction_observation(payload_hash: str, predecessor: str) -> dict[str, Any]:
    record = initial_observation(payload_hash)
    record.update(observation_type="CORRECTION", supersedes_observation_id=predecessor)
    return record


def event(family: str, observation_ids: list[str]) -> dict[str, Any]:
    return {
        "schema_version": "mtc.p030_event/v1", "record_type": family,
        "producer": "WS_LIVE", "symbol": "BTC", "interval": "15m",
        "slot_id": "HYPERLIQUID.BTC.15m.1769903100000",
        "observation_ids": observation_ids, "window_start": 1769903100000,
        "window_end": 1769904000000, "detected_at": 1769904001000,
        "detail": {"message": "fixture-ç", "missing_bars": 1},
        "env_lineage_id": "fixture-lineage", "deployment_identity_hash": None,
    }


def dataset_row(
    observation: dict[str, Any], observation_id: str, payload_record: dict[str, Any]
) -> dict[str, Any]:
    return {
        "observation_id": observation_id,
        "producer_payload_hash": observation["producer_payload_hash"],
        "symbol": observation["symbol"], "interval": observation["interval"],
        "bar_open_time": observation["bar_open_time"],
        "bar_close_time": payload_record["bar_close_time"],
        "open": payload_record["open"], "high": payload_record["high"],
        "low": payload_record["low"], "close": payload_record["close"],
        "volume": payload_record["volume"], "venue": observation["venue"],
        "track": observation["track"],
        "proxy_source": observation["proxy_source"],
        "source_producer": observation["source_producer"],
        "observation_type": observation["observation_type"],
        "supersedes_observation_id": observation["supersedes_observation_id"],
        "ingest_time": 1769904001000, "venue_seq": payload_record["venue_seq"],
        "env_lineage_id": "fixture-lineage", "schema_version": "0.1.0",
    }


def descriptor() -> dict[str, Any]:
    return {
        "venue": "HYPERLIQUID", "track": "NATIVE", "proxy_source": None,
        "window_start": 1769903100000, "window_end": 1769904900000,
        "content_hash_algorithm": "sha256",
        "canonicalization_version": "p030-json-array-v1",
    }


def manifest(dataset_hash: str) -> dict[str, Any]:
    return {
        "schema_version": "mtc.p030_provenance/v1", "venue": "HYPERLIQUID",
        "track": "NATIVE", "proxy_source": None, "window_start": 1769903100000,
        "window_end": 1769904900000, "native_fraction": "1",
        "proxy_fraction": "0", "archive_schema_version": "0.1.0",
        "env_lineage_id": "fixture-lineage", "dataset_content_hash": dataset_hash,
        "content_hash_algorithm": "sha256",
        "canonicalization_version": "p030-json-array-v1",
        "partitions": [{
            "path": "bars/HYPERLIQUID/BTC/15m/2026-01.jsonl",
            "file_sha256": "a" * 64, "size_bytes": 321,
            "partition_state": "closed", "high_water_bytes": 321,
            "record_count": 1, "last_observation_id": None,
        }],
    }


def expect_refused(call: Callable[[], Any], label: str, error_type: type[Exception]) -> None:
    try:
        call()
    except error_type:
        return
    raise AssertionError((label, "accepted"))


def prove_cycle_guard_load_bearing(subject: Any, payload_hash: str) -> None:
    """Reach graph validation in memory, then remove only its cycle refusal."""
    first_id = "p030obs-v1:" + "a" * 64
    second_id = "p030obs-v1:" + "b" * 64
    cycle = [
        dict(correction_observation(payload_hash, second_id), observation_id=first_id),
        dict(correction_observation(payload_hash, first_id), observation_id=second_id),
    ]
    source = inspect.getsource(subject.validate_correction_chain)
    identity_guard = (
        "        if observation_id(body) != identity:\n"
        "            raise ContractRefused(\"observation_id does not match observation bytes\")\n"
    )
    assert source.count(identity_guard) == 1
    graph_reachable_source = source.replace(
        identity_guard, "        observation_id(body)\n", 1
    )

    namespace: dict[str, Any] = {}
    exec(compile(graph_reachable_source, "<cycle-graph-reachable>", "exec"),
         dict(vars(subject)), namespace)
    try:
        namespace["validate_correction_chain"](cycle)
    except subject.ContractRefused as error:
        assert str(error) == "correction chain cycles"
    else:
        raise AssertionError(("graph_cycle_guard", "accepted"))

    cycle_guard = '                raise ContractRefused("correction chain cycles")\n'
    assert graph_reachable_source.count(cycle_guard) == 1
    guard_removed_source = graph_reachable_source.replace(cycle_guard, "                return\n", 1)
    namespace = {}
    exec(compile(guard_removed_source, "<cycle-guard-removed>", "exec"),
         dict(vars(subject)), namespace)
    namespace["validate_correction_chain"](cycle)


def prove_second_initial_guard_load_bearing(subject: Any, records: list[dict]) -> None:
    """Verify the same-slot INITIAL refusal, then remove only that guard in memory."""
    try:
        subject.validate_correction_chain(records)
    except subject.ContractRefused as error:
        assert str(error) == "second INITIAL observation for one producer slot"
    else:
        raise AssertionError(("second_initial_guard", "accepted"))

    source = inspect.getsource(subject.validate_correction_chain)
    guard = (
        "            if slot in slots:\n"
        "                raise ContractRefused("
        "\"second INITIAL observation for one producer slot\")\n"
    )
    assert source.count(guard) == 1
    namespace: dict[str, Any] = {}
    exec(
        compile(source.replace(guard, "", 1), "<second-initial-guard-removed>", "exec"),
        dict(vars(subject)), namespace,
    )
    namespace["validate_correction_chain"](records)


def prove_event_producer_guard_load_bearing(subject: Any, record: dict) -> None:
    """Verify the producer refusal, then remove only that allowlist call in memory."""
    try:
        subject.event_id(record)
    except subject.ContractRefused as error:
        assert str(error) == "event.producer is unknown"
    else:
        raise AssertionError(("event_producer_guard", "accepted"))

    source = inspect.getsource(subject.event_id)
    guard = '    _source_producer(record["producer"], "event.producer")\n'
    assert source.count(guard) == 1
    namespace: dict[str, Any] = {}
    exec(
        compile(source.replace(guard, "", 1), "<event-producer-guard-removed>", "exec"),
        dict(vars(subject)), namespace,
    )
    namespace["event_id"](record)


def prove_scalar_and_carrier_guards_load_bearing(
    subject: Any, evil_record: dict, stateful_record: StatefulEventMapping,
) -> None:
    """Restore each rejected pre-fix seam in memory and prove it accepts the deviant."""
    original_string = subject._string

    def permissive_string(value: object, label: str, *, nullable: bool = False) -> str | None:
        if value is None and nullable:
            return None
        if not isinstance(value, str) or not value:
            raise subject.ContractRefused(f"{label} must be a non-empty string")
        return value

    subject._string = permissive_string
    try:
        mutant_evil_id = subject.event_id(evil_record)
    finally:
        subject._string = original_string
    expected_evil_id = oracle_record_id(
        "p030evt-v1", "p030-event-v1", evil_record, EVENT_FIELDS,
    )
    assert mutant_evil_id == expected_evil_id

    original_mapping = subject._mapping

    def permissive_mapping(value: object, label: str) -> Mapping:
        if not isinstance(value, Mapping):
            raise subject.ContractRefused(f"{label} must be an object")
        return value

    subject._mapping = permissive_mapping
    try:
        mutant_stateful_id = subject.event_id(stateful_record)
    finally:
        subject._mapping = original_mapping
    expected_stateful = event("GAP", ["p030obs-v1:" + "a" * 64])
    expected_stateful["producer"] = "EVIL_AFTER_VALIDATION"
    expected_stateful_id = oracle_record_id(
        "p030evt-v1", "p030-event-v1", expected_stateful, EVENT_FIELDS,
    )
    assert stateful_record.producer_reads == 2
    assert mutant_stateful_id == expected_stateful_id


def meaningful_correction_red() -> None:
    """Pre-implementation deviant: correction identity ignores its predecessor link."""
    payload_hash = oracle_record_id("p030payload-v1", "p030-payload-v1", payload(), PAYLOAD_FIELDS)
    first = oracle_record_id(
        "p030obs-v1", "p030-observation-v1", initial_observation(payload_hash),
        OBSERVATION_FIELDS,
    )
    correction_a = correction_observation(payload_hash, first)
    correction_b = correction_observation(payload_hash, "p030obs-v1:" + "f" * 64)
    omitted = OBSERVATION_FIELDS[:-1]
    observed = (
        oracle_record_id("p030obs-v1", "p030-observation-v1", correction_a, omitted),
        oracle_record_id("p030obs-v1", "p030-observation-v1", correction_b, omitted),
    )
    assert observed[0] != observed[1], ("correction_predecessor_not_bound", observed)


def meaningful_dataset_red() -> None:
    """Equivalent deviant hashes a row without binding its producer payload fields."""
    payload_record = payload()
    payload_hash = oracle_record_id(
        "p030payload-v1", "p030-payload-v1", payload_record, PAYLOAD_FIELDS
    )
    observation = initial_observation(payload_hash)
    identity = oracle_record_id(
        "p030obs-v1", "p030-observation-v1", observation, OBSERVATION_FIELDS
    )
    row = dataset_row(observation, identity, payload_record)
    row["close"] = "999"
    values = [descriptor()[field] for field in DATASET_DESCRIPTOR_FIELDS]
    values.append([[row[field] for field in DATASET_ROW_FIELDS]])
    observed = oracle_id("p030ds-v1", "p030-dataset-v1", values)
    raise AssertionError(("dataset_payload_mismatch_accepted", observed))


def meaningful_path_red() -> None:
    """Equivalent deviant hashes an absolute partition path without validation."""
    dataset_hash = "p030ds-v1:" + "c" * 64
    provenance = manifest(dataset_hash)
    provenance["partitions"][0]["path"] = "C:/archive/2026-01.jsonl"
    values = [provenance[field] for field in MANIFEST_FIELDS[:-1]]
    values.append([[provenance["partitions"][0][field] for field in PARTITION_FIELDS]])
    observed = oracle_id("p030prov-v1", "p030-provenance-v1", values)
    raise AssertionError(("absolute_provenance_path_accepted", observed))


def meaningful_event_detail_red() -> None:
    """Pre-repair deviant aliases an integer object key with its string spelling."""
    observation_id = "p030obs-v1:" + "a" * 64
    integer_key = event("GAP", [observation_id])
    integer_key["detail"] = {1: "same"}
    string_key = event("GAP", [observation_id])
    string_key["detail"] = {"1": "same"}
    observed = (
        oracle_record_id("p030evt-v1", "p030-event-v1", integer_key, EVENT_FIELDS),
        oracle_record_id("p030evt-v1", "p030-event-v1", string_key, EVENT_FIELDS),
    )
    assert observed[0] != observed[1], ("event_detail_key_collision", observed)


def meaningful_producer_track_red() -> None:
    """Equivalent deviant identities omit the producer-to-track invariant."""
    payload_record = dict(payload(), source_producer="PROXY_DOWNLOAD")
    payload_hash = oracle_record_id(
        "p030payload-v1", "p030-payload-v1", payload_record, PAYLOAD_FIELDS
    )
    observation = dict(
        initial_observation(payload_hash), source_producer="PROXY_DOWNLOAD"
    )
    provenance = manifest("p030ds-v1:" + "c" * 64)
    provenance["track"] = "UNKNOWN"
    provenance_values = [provenance[field] for field in MANIFEST_FIELDS[:-1]]
    provenance_values.append([
        [provenance["partitions"][0][field] for field in PARTITION_FIELDS]
    ])
    observed = (
        oracle_record_id(
            "p030obs-v1", "p030-observation-v1", observation, OBSERVATION_FIELDS
        ),
        oracle_id("p030prov-v1", "p030-provenance-v1", provenance_values),
    )
    raise AssertionError(("producer_track_mapping_not_enforced", observed))


def meaningful_iterable_mutation_red() -> None:
    """Equivalent mutants remove only the one-time iterable materialization."""
    import p030_market_data_contracts as subject

    payload_record = payload()
    payload_hash = subject.producer_payload_hash(payload_record)
    initial = initial_observation(payload_hash)
    initial_id = subject.observation_id(initial)
    first_row = dataset_row(initial, initial_id, payload_record)
    second_payload = dict(
        payload_record, bar_open_time=1769904000000, bar_close_time=1769904900000
    )
    second_observation = dict(
        initial, bar_open_time=1769904000000,
        producer_payload_hash=subject.producer_payload_hash(second_payload),
    )
    second_id = subject.observation_id(second_observation)
    second_row = dataset_row(second_observation, second_id, second_payload)

    def mutating_rows():
        yield first_row
        first_row["close"] = "999"
        yield second_row

    dataset_source = inspect.getsource(subject.dataset_content_hash)
    materialization = "    observations = list(observations)\n"
    assert dataset_source.count(materialization) == 1
    namespace: dict[str, Any] = {}
    exec(
        compile(dataset_source.replace(materialization, "", 1),
                "<dataset-materialization-removed>", "exec"),
        dict(vars(subject)), namespace,
    )
    dataset_id = namespace["dataset_content_hash"](descriptor(), mutating_rows())

    first_chain_record = dict(initial, observation_id=initial_id)
    candle_payload = dict(payload_record, source_producer="CANDLE_SNAPSHOT", close="101")
    candle_hash = subject.producer_payload_hash(candle_payload)
    candle_correction = dict(
        correction_observation(candle_hash, initial_id),
        source_producer="CANDLE_SNAPSHOT",
    )
    candle_id = subject.observation_id(candle_correction)

    def mutating_chain():
        yield first_chain_record
        first_chain_record["source_producer"] = "CANDLE_SNAPSHOT"
        yield dict(candle_correction, observation_id=candle_id)

    chain_source = inspect.getsource(subject.validate_correction_chain)
    materialization = "    records = list(records)\n"
    assert chain_source.count(materialization) == 1
    namespace = {}
    exec(
        compile(chain_source.replace(materialization, "", 1),
                "<chain-materialization-removed>", "exec"),
        dict(vars(subject)), namespace,
    )
    namespace["validate_correction_chain"](mutating_chain())
    raise AssertionError(("iterable_mutation_after_validation_accepted", dataset_id))


def meaningful_event_producer_red() -> None:
    """Equivalent deviant binds an event identity without enforcing its producer allowlist."""
    record = event("GAP", ["p030obs-v1:" + "a" * 64])
    record["producer"] = "p030-fixture"
    observed = oracle_record_id(
        "p030evt-v1", "p030-event-v1", record, EVENT_FIELDS
    )
    raise AssertionError(("unknown_event_producer_accepted", observed))


def meaningful_scalar_carrier_red() -> None:
    """Equivalent deviant accepts a spoofed scalar and a value-flipping mapping."""
    evil_record = event("GAP", ["p030obs-v1:" + "a" * 64])
    evil_record["producer"] = EvilProducer()
    evil_id = oracle_record_id(
        "p030evt-v1", "p030-event-v1", evil_record, EVENT_FIELDS
    )
    stateful = StatefulEventMapping(event("GAP", ["p030obs-v1:" + "a" * 64]))
    validated_producer = stateful["producer"]
    drifted_id = oracle_record_id(
        "p030evt-v1", "p030-event-v1", stateful, EVENT_FIELDS
    )
    raise AssertionError((
        "spoofed_scalar_or_stateful_mapping_accepted",
        (str(evil_record["producer"]), evil_id, validated_producer, drifted_id),
    ))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--red",
        choices=(
            "correction-link", "dataset-row-integrity", "provenance-path", "event-detail",
            "producer-track", "iterable-mutation", "event-producer",
            "scalar-carrier",
        ),
    )
    args = parser.parse_args()
    if args.red == "correction-link":
        meaningful_correction_red()
        return
    if args.red == "dataset-row-integrity":
        meaningful_dataset_red()
        return
    if args.red == "provenance-path":
        meaningful_path_red()
        return
    if args.red == "event-detail":
        meaningful_event_detail_red()
        return
    if args.red == "producer-track":
        meaningful_producer_track_red()
        return
    if args.red == "iterable-mutation":
        meaningful_iterable_mutation_red()
        return
    if args.red == "event-producer":
        meaningful_event_producer_red()
        return
    if args.red == "scalar-carrier":
        meaningful_scalar_carrier_red()
        return

    import p030_market_data_contracts as subject

    attempts: list[object] = []
    original_connect = socket.socket.connect
    original_create = socket.create_connection
    socket.socket.connect = lambda *a, **k: attempts.append((a, k))  # type: ignore[method-assign]
    socket.create_connection = lambda *a, **k: attempts.append((a, k))  # type: ignore[assignment]
    try:
        payload_record = payload()
        payload_hash = subject.producer_payload_hash(payload_record)
        assert payload_hash == GOLDEN_PAYLOAD
        assert payload_hash == oracle_record_id(
            "p030payload-v1", "p030-payload-v1", payload_record, PAYLOAD_FIELDS)

        initial = initial_observation(payload_hash)
        initial_id = subject.observation_id(initial)
        assert initial_id == GOLDEN_INITIAL
        correction_payload = dict(payload_record, close="101")
        correction_hash = subject.producer_payload_hash(correction_payload)
        correction = correction_observation(correction_hash, initial_id)
        correction_id = subject.observation_id(correction)
        assert correction_id == GOLDEN_CORRECTION
        assert correction_id == oracle_record_id(
            "p030obs-v1", "p030-observation-v1", correction, OBSERVATION_FIELDS)

        other_predecessor = "p030obs-v1:" + "f" * 64
        assert subject.observation_id(
            correction_observation(correction_hash, other_predecessor)
        ) != correction_id
        payload_omitted = oracle_record_id(
            "p030payload-v1", "p030-payload-v1", payload_record, PAYLOAD_FIELDS[:-1])
        payload_reordered = oracle_record_id(
            "p030payload-v1", "p030-payload-v1", payload_record,
            (*PAYLOAD_FIELDS[1:], PAYLOAD_FIELDS[0]),
        )
        assert payload_omitted != payload_hash and payload_reordered != payload_hash
        print("PAYLOAD MUTANTS (omitted/reordered member): DETECTED")
        mixed_key_payload = dict(payload_record)
        mixed_key_payload[1] = "integer-key"
        mixed_key_payload["extra"] = "string-key"
        expect_refused(
            lambda: subject.producer_payload_hash(mixed_key_payload),
            "mixed_non_string_mapping_keys", subject.ContractRefused,
        )
        invalid_source_payload = dict(payload_record, source_producer="REST_BACKFILL")
        expect_refused(
            lambda: subject.producer_payload_hash(invalid_source_payload),
            "unknown_payload_source_producer", subject.ContractRefused,
        )
        subject.producer_payload_hash(
            dict(payload_record, source_producer="CANDLE_SNAPSHOT")
        )
        proxy_payload = dict(payload_record, source_producer="PROXY_DOWNLOAD")
        proxy_payload_hash = subject.producer_payload_hash(proxy_payload)
        proxy_observation = dict(
            initial_observation(proxy_payload_hash), track="PROXY",
            proxy_source="FIXTURE_PROXY", source_producer="PROXY_DOWNLOAD",
        )
        proxy_observation_id = subject.observation_id(proxy_observation)
        candle_payload = dict(payload_record, source_producer="CANDLE_SNAPSHOT")
        candle_payload_hash = subject.producer_payload_hash(candle_payload)
        candle_observation = dict(
            initial_observation(candle_payload_hash), source_producer="CANDLE_SNAPSHOT"
        )
        subject.observation_id(candle_observation)
        for label, changes in (
            ("unknown_observation_source", {"source_producer": "REST_BACKFILL"}),
            ("unknown_observation_track", {"track": "ARCHIVE"}),
            ("native_with_proxy", {"proxy_source": "FIXTURE_PROXY"}),
            ("proxy_without_source", {"track": "PROXY", "proxy_source": None}),
        ):
            changed_observation = dict(initial, **changes)
            expect_refused(
                lambda value=changed_observation: subject.observation_id(value),
                label, subject.ContractRefused,
            )
        for label, source_producer, track, proxy_source, producer_hash in (
            ("proxy_producer_on_native", "PROXY_DOWNLOAD", "NATIVE", None,
             proxy_payload_hash),
            ("ws_producer_on_proxy", "WS_LIVE", "PROXY", "FIXTURE_PROXY",
             payload_hash),
            ("candle_producer_on_proxy", "CANDLE_SNAPSHOT", "PROXY", "FIXTURE_PROXY",
             candle_payload_hash),
        ):
            mismatched_observation = dict(
                initial_observation(producer_hash), source_producer=source_producer,
                track=track, proxy_source=proxy_source,
            )
            expect_refused(
                lambda value=mismatched_observation: subject.observation_id(value),
                label, subject.ContractRefused,
            )
        print("MAPPING KEY/SOURCE/TRACK/PROXY REFUSALS: PASS")
        print("OBSERVATION/CORRECTION GOLDENS: PASS")

        chain = [dict(initial, observation_id=initial_id),
                 dict(correction, observation_id=correction_id)]
        subject.validate_correction_chain(chain)
        second_initial = initial_observation(correction_hash)
        second_initial_id = subject.observation_id(second_initial)
        prove_second_initial_guard_load_bearing(
            subject,
            [dict(initial, observation_id=initial_id),
             dict(second_initial, observation_id=second_initial_id)],
        )
        print("SECOND INITIAL GUARD MUTATION: DETECTED")
        mutated_initial = copy.deepcopy(chain[0])
        candle_correction_payload = dict(candle_payload, close="101")
        candle_correction_hash = subject.producer_payload_hash(candle_correction_payload)
        candle_correction = dict(
            correction_observation(candle_correction_hash, initial_id),
            source_producer="CANDLE_SNAPSHOT",
        )
        candle_correction_id = subject.observation_id(candle_correction)

        def mutating_chain():
            yield mutated_initial
            mutated_initial["source_producer"] = "CANDLE_SNAPSHOT"
            yield dict(candle_correction, observation_id=candle_correction_id)

        expect_refused(
            lambda: subject.validate_correction_chain(mutating_chain()),
            "correction_generator_mutated_after_identity_pass", subject.ContractRefused,
        )
        print("CORRECTION GENERATOR MUTATION: DETECTED")
        expect_refused(lambda: subject.validate_correction_chain([]),
                       "empty_chain", subject.ContractRefused)
        missing = copy.deepcopy(chain); missing[1]["supersedes_observation_id"] = other_predecessor
        missing[1]["observation_id"] = subject.observation_id(
            {field: missing[1][field] for field in OBSERVATION_FIELDS})
        cross_slot = copy.deepcopy(chain); cross_slot[1]["bar_open_time"] += 900000
        cross_slot[1]["observation_id"] = subject.observation_id(
            {field: cross_slot[1][field] for field in OBSERVATION_FIELDS})
        fork = copy.deepcopy(chain); fork.append(copy.deepcopy(chain[1]))
        fork[2]["producer_payload_hash"] = subject.producer_payload_hash(dict(payload_record, close="100"))
        fork[2]["observation_id"] = subject.observation_id({field: fork[2][field] for field in OBSERVATION_FIELDS})
        for label, deviant in (("missing_predecessor", missing), ("cross_slot", cross_slot),
                               ("fork", fork)):
            expect_refused(lambda d=deviant: subject.validate_correction_chain(d), label, subject.ContractRefused)
            print(f"CORRECTION MUTANT ({label}): DETECTED")
        prove_cycle_guard_load_bearing(subject, payload_hash)
        print("CORRECTION GRAPH CYCLE GUARD MUTATION: DETECTED")

        assert subject.EVENT_FAMILIES == frozenset(EVENT_FAMILIES)
        unknown_event_producer = event("GAP", [initial_id])
        unknown_event_producer["producer"] = "p030-fixture"
        prove_event_producer_guard_load_bearing(subject, unknown_event_producer)
        print("EVENT PRODUCER ALLOWLIST MUTATION: DETECTED")
        evil_event_producer = event("GAP", [initial_id])
        evil_event_producer["producer"] = EvilProducer()
        expect_refused(
            lambda: subject.event_id(evil_event_producer),
            "evil_event_producer_subclass", subject.ContractRefused,
        )
        stateful_event = StatefulEventMapping(event("GAP", [initial_id]))
        expect_refused(
            lambda: subject.event_id(stateful_event),
            "stateful_event_mapping", subject.ContractRefused,
        )
        prove_scalar_and_carrier_guards_load_bearing(
            subject,
            evil_event_producer,
            StatefulEventMapping(event("GAP", ["p030obs-v1:" + "a" * 64])),
        )
        print("EXACT SCALAR/CARRIER GUARD MUTANTS: DETECTED")
        unhashable_id = event("GAP", [initial_id])
        unhashable_id["observation_ids"] = [[initial_id]]
        expect_refused(
            lambda: subject.event_id(unhashable_id),
            "unhashable_observation_id", subject.ContractRefused,
        )
        for malformed_deployment_hash in ("not-a-sha256", "A" * 64):
            malformed_deployment = event("GAP", [initial_id])
            malformed_deployment["deployment_identity_hash"] = malformed_deployment_hash
            expect_refused(
                lambda value=malformed_deployment: subject.event_id(value),
                "malformed_deployment_identity_hash", subject.ContractRefused,
            )
        valid_deployment = event("GAP", [initial_id])
        valid_deployment["deployment_identity_hash"] = "a" * 64
        subject.event_id(valid_deployment)
        print("EVENT MEMBER/DEPLOYMENT HASH REFUSALS: PASS")
        event_ids = {}
        for family in EVENT_FAMILIES:
            record = event(family, [initial_id, correction_id] if family == "CORRECTION" else [initial_id])
            event_ids[family] = subject.event_id(record)
            assert event_ids[family] == GOLDEN_EVENTS[family]
            assert event_ids[family] == oracle_record_id(
                "p030evt-v1", "p030-event-v1", record, EVENT_FIELDS)
        assert len(set(event_ids.values())) == len(EVENT_FAMILIES)
        correction_reversed = event("CORRECTION", [correction_id, initial_id])
        reversed_id = subject.event_id(correction_reversed)
        assert reversed_id != event_ids["CORRECTION"]
        sorted_mutant = oracle_record_id(
            "p030evt-v1", "p030-event-v1",
            dict(correction_reversed, observation_ids=sorted(correction_reversed["observation_ids"])),
            EVENT_FIELDS,
        )
        assert sorted_mutant == event_ids["CORRECTION"] and sorted_mutant != reversed_id
        print("EVENT MUTANT (sorted correction ids): DETECTED")
        expect_refused(lambda: subject.event_id(event("CORRECTION", [initial_id])),
                       "short_correction_event", subject.ContractRefused)
        expect_refused(lambda: subject.event_id(event("EIGHTH_STATE", [initial_id])),
                       "unknown_event_family", subject.ContractRefused)
        print("NINE EVENT FAMILY GOLDENS: PASS")

        row = dataset_row(initial, initial_id, payload_record)
        second_observation = dict(initial)
        second_observation["bar_open_time"] += 900000
        second_payload = dict(
            payload_record, bar_open_time=1769904000000, bar_close_time=1769904900000
        )
        second_observation["producer_payload_hash"] = subject.producer_payload_hash(second_payload)
        second_id = subject.observation_id(second_observation)
        second_row = dataset_row(second_observation, second_id, second_payload)
        dataset_hash = subject.dataset_content_hash(descriptor(), [second_row, row])
        assert dataset_hash == GOLDEN_DATASET
        assert dataset_hash == subject.dataset_content_hash(descriptor(), [row, second_row])
        mutated_row = copy.deepcopy(row)

        def mutating_rows():
            yield mutated_row
            mutated_row["close"] = "999"
            yield second_row

        expect_refused(
            lambda: subject.dataset_content_hash(descriptor(), mutating_rows()),
            "dataset_generator_mutated_after_validation", subject.ContractRefused,
        )
        print("DATASET GENERATOR MUTATION: DETECTED")
        ordered_rows = sorted(
            [second_row, row],
            key=lambda item: (
                item["venue"], item["track"], item["source_producer"], item["symbol"],
                item["interval"], item["bar_open_time"], item["observation_id"],
            ),
        )
        dataset_oracle_values = [descriptor()[field] for field in DATASET_DESCRIPTOR_FIELDS]
        dataset_oracle_values.append([
            [item[field] for field in DATASET_ROW_FIELDS] for item in ordered_rows
        ])
        assert dataset_hash == oracle_id(
            "p030ds-v1", "p030-dataset-v1", dataset_oracle_values)
        input_order_mutant = [descriptor()[field] for field in DATASET_DESCRIPTOR_FIELDS]
        input_order_mutant.append([
            [item[field] for field in DATASET_ROW_FIELDS] for item in [second_row, row]
        ])
        assert oracle_id("p030ds-v1", "p030-dataset-v1", input_order_mutant) != dataset_hash
        print("DATASET MUTANT (input-order hash): DETECTED")
        for label, changes in (
            ("unknown_descriptor_track", {"track": "ARCHIVE"}),
            ("native_descriptor_with_proxy", {"proxy_source": "FIXTURE_PROXY"}),
            ("proxy_descriptor_without_source", {"track": "PROXY", "proxy_source": None}),
        ):
            changed_descriptor = dict(descriptor(), **changes)
            expect_refused(
                lambda value=changed_descriptor: subject.dataset_content_hash(value, [row]),
                label, subject.ContractRefused,
            )
        proxy_descriptor = dict(
            descriptor(), track="PROXY", proxy_source="FIXTURE_PROXY"
        )
        proxy_row = dataset_row(proxy_observation, proxy_observation_id, proxy_payload)
        subject.dataset_content_hash(proxy_descriptor, [proxy_row])
        for label, payload_value, observation_value, descriptor_value in (
            (
                "dataset_proxy_producer_on_native", proxy_payload,
                dict(initial_observation(proxy_payload_hash),
                     source_producer="PROXY_DOWNLOAD"), descriptor(),
            ),
            (
                "dataset_ws_producer_on_proxy", payload_record,
                dict(initial, track="PROXY", proxy_source="FIXTURE_PROXY"),
                proxy_descriptor,
            ),
        ):
            mismatched_row = dataset_row(
                observation_value,
                oracle_record_id(
                    "p030obs-v1", "p030-observation-v1",
                    observation_value, OBSERVATION_FIELDS,
                ),
                payload_value,
            )
            expect_refused(
                lambda row_value=mismatched_row, desc_value=descriptor_value:
                    subject.dataset_content_hash(desc_value, [row_value]),
                label, subject.ContractRefused,
            )
        for label, changes in (
            ("dataset_row_unknown_source", {"source_producer": "REST_BACKFILL"}),
            ("dataset_row_unknown_track", {"track": "ARCHIVE"}),
            ("dataset_native_with_proxy", {"proxy_source": "FIXTURE_PROXY"}),
            ("dataset_proxy_without_source", {"track": "PROXY", "proxy_source": None}),
        ):
            changed_row = dict(row, **changes)
            expect_refused(
                lambda value=changed_row: subject.dataset_content_hash(descriptor(), [value]),
                label, subject.ContractRefused,
            )
        expect_refused(lambda: subject.dataset_content_hash(descriptor(), [row, row]),
                       "duplicate_observation", subject.ContractRefused)
        expect_refused(lambda: subject.dataset_content_hash(descriptor(), []),
                       "empty_dataset", subject.ContractRefused)
        payload_field_mutants = {
            "venue": "OTHER_VENUE", "source_producer": "CANDLE_SNAPSHOT",
            "symbol": "ETH", "interval": "5m", "bar_open_time": 1769903100001,
            "bar_close_time": 1769904000001, "open": "101", "high": "104",
            "low": "98", "close": "999", "volume": "13.5", "venue_seq": 7,
        }
        for field, replacement in payload_field_mutants.items():
            changed = copy.deepcopy(row)
            changed[field] = replacement
            if field in OBSERVATION_FIELDS:
                changed["observation_id"] = subject.observation_id(
                    {name: changed[name] for name in OBSERVATION_FIELDS}
                )
            expect_refused(
                lambda value=changed: subject.dataset_content_hash(descriptor(), [value]),
                f"dataset_payload_field_{field}", subject.ContractRefused,
            )
        bad_order_payload = dict(
            payload_record, bar_close_time=payload_record["bar_open_time"]
        )
        bad_order_observation = initial_observation(
            subject.producer_payload_hash(bad_order_payload)
        )
        bad_order_row = dataset_row(
            bad_order_observation,
            subject.observation_id(bad_order_observation),
            bad_order_payload,
        )
        expect_refused(
            lambda: subject.dataset_content_hash(descriptor(), [bad_order_row]),
            "non_increasing_bar_window", subject.ContractRefused,
        )

        other_venue_payload = dict(payload_record, venue="OTHER_VENUE")
        other_venue_observation = initial_observation(
            subject.producer_payload_hash(other_venue_payload)
        )
        other_venue_observation["venue"] = "OTHER_VENUE"
        descriptor_mismatch_rows = []
        descriptor_mismatch_rows.append((descriptor(), dataset_row(
            other_venue_observation,
            subject.observation_id(other_venue_observation),
            other_venue_payload,
        )))
        other_proxy_observation = dict(
            proxy_observation, proxy_source="OTHER_PROXY"
        )
        descriptor_mismatch_rows.extend((
            (descriptor(), proxy_row),
            (proxy_descriptor, dataset_row(
                other_proxy_observation,
                subject.observation_id(other_proxy_observation),
                proxy_payload,
            )),
        ))
        for field, (expected_descriptor, changed) in zip(
            ("venue", "track", "proxy_source"), descriptor_mismatch_rows, strict=True
        ):
            expect_refused(
                lambda row_value=changed, descriptor_value=expected_descriptor:
                    subject.dataset_content_hash(descriptor_value, [row_value]),
                f"dataset_descriptor_{field}", subject.ContractRefused,
            )
        print("DATASET PAYLOAD/SLOT/DESCRIPTOR MUTANTS: DETECTED")
        print("DATASET IDENTITY GOLDEN/PERMUTATION: PASS")

        provenance = manifest(dataset_hash)
        provenance["partitions"][0]["last_observation_id"] = second_id
        manifest_hash = subject.venue_provenance_manifest_hash(provenance)
        assert manifest_hash == GOLDEN_MANIFEST
        manifest_oracle_values = [provenance[field] for field in MANIFEST_FIELDS[:-1]]
        manifest_oracle_values.append([
            [part[field] for field in PARTITION_FIELDS]
            for part in sorted(provenance["partitions"], key=lambda item: item["path"])
        ])
        assert manifest_hash == oracle_id(
            "p030prov-v1", "p030-provenance-v1", manifest_oracle_values)
        for label, changes in (
            ("provenance_unknown_track", {"track": "UNKNOWN"}),
            ("provenance_native_with_proxy", {"proxy_source": "FIXTURE_PROXY"}),
            ("provenance_proxy_without_source", {"track": "PROXY", "proxy_source": None}),
        ):
            changed_provenance = dict(provenance, **changes)
            expect_refused(
                lambda value=changed_provenance:
                    subject.venue_provenance_manifest_hash(value),
                label, subject.ContractRefused,
            )
        proxy_provenance = dict(
            provenance, track="PROXY", proxy_source="FIXTURE_PROXY",
            native_fraction="0", proxy_fraction="1",
        )
        subject.venue_provenance_manifest_hash(proxy_provenance)
        print("PRODUCER/TRACK/PROXY MAPPING MUTANTS: DETECTED")
        unsafe_paths = (
            "", "/archive/part.jsonl", "C:/archive/part.jsonl", "C:part.jsonl",
            r"archive\part.jsonl", "./archive/part.jsonl", "archive/../part.jsonl",
            "archive//part.jsonl", "archive/./part.jsonl", "archive/",
            "archive/\0part.jsonl",
        )
        for unsafe_path in unsafe_paths:
            changed = copy.deepcopy(provenance)
            changed["partitions"][0]["path"] = unsafe_path
            expect_refused(
                lambda value=changed: subject.venue_provenance_manifest_hash(value),
                f"unsafe_path_{unsafe_path!r}", subject.ContractRefused,
            )
        print("PROVENANCE CANONICAL RELATIVE POSIX PATH REFUSALS: PASS")
        for field, replacement in (
            ("path", "bars/HYPERLIQUID/BTC/15m/other.jsonl"),
            ("size_bytes", 322), ("partition_state", "live"),
            ("high_water_bytes", 320), ("file_sha256", "b" * 64),
        ):
            changed = copy.deepcopy(provenance)
            changed["partitions"][0][field] = replacement
            try:
                changed_hash = subject.venue_provenance_manifest_hash(changed)
            except subject.ContractRefused:
                changed_hash = None
            assert changed_hash != manifest_hash, field
            print(f"PROVENANCE MUTANT ({field}): DETECTED")
            omitted = copy.deepcopy(provenance)
            omitted["partitions"][0].pop(field)
            expect_refused(lambda value=omitted: subject.venue_provenance_manifest_hash(value),
                           f"omitted_{field}", subject.ContractRefused)
        changed_dataset = copy.deepcopy(provenance)
        changed_dataset["dataset_content_hash"] = "p030ds-v1:" + "c" * 64
        assert subject.venue_provenance_manifest_hash(changed_dataset) != manifest_hash
        print("PROVENANCE MUTANT (dataset_content_hash): DETECTED")
        bad_last_id = copy.deepcopy(provenance)
        bad_last_id["partitions"][0]["last_observation_id"] = "not-an-observation-id"
        expect_refused(lambda: subject.venue_provenance_manifest_hash(bad_last_id),
                       "bad_last_observation_id", subject.ContractRefused)

        # Explicit discriminating mutants from the contract defects.
        omitted_link = oracle_record_id(
            "p030obs-v1", "p030-observation-v1", correction, OBSERVATION_FIELDS[:-1])
        assert omitted_link != correction_id
        print("IDENTITY MUTANT (omitted predecessor): DETECTED")
        four_family_set = frozenset(EVENT_FAMILIES[:4])
        assert subject.EVENT_FAMILIES != four_family_set
        print("EVENT MUTANT (four-family allowlist): DETECTED")
        record_hash_only = oracle_id(
            "p030prov-v1", "p030-provenance-v1",
            [part["file_sha256"] for part in provenance["partitions"]],
        )
        assert record_hash_only != manifest_hash
        print("PROVENANCE MUTANT (file-hashes only): DETECTED")

        bad_payload = dict(payload_record, extra="uncontracted")
        expect_refused(lambda: subject.producer_payload_hash(bad_payload),
                       "extra_payload_field", subject.ContractRefused)
        bad_event = event("GAP", [initial_id]); bad_event["detected_at"] = True
        expect_refused(lambda: subject.event_id(bad_event), "bool_timestamp", subject.ContractRefused)
        bad_event = event("GAP", [initial_id]); bad_event["detail"] = {"value": float("nan")}
        expect_refused(lambda: subject.event_id(bad_event), "nan_detail", subject.ContractRefused)
        integer_key = event("GAP", [initial_id]); integer_key["detail"] = {1: "same"}
        string_key = event("GAP", [initial_id]); string_key["detail"] = {"1": "same"}
        assert oracle_record_id(
            "p030evt-v1", "p030-event-v1", integer_key, EVENT_FIELDS
        ) == oracle_record_id("p030evt-v1", "p030-event-v1", string_key, EVENT_FIELDS)
        expect_refused(
            lambda: subject.event_id(integer_key), "integer_detail_key", subject.ContractRefused
        )
        nested_integer_key = event("GAP", [initial_id])
        nested_integer_key["detail"] = {"nested": [{2: "same"}]}
        expect_refused(
            lambda: subject.event_id(nested_integer_key),
            "nested_integer_detail_key", subject.ContractRefused,
        )
        tuple_detail = event("GAP", [initial_id]); tuple_detail["detail"] = {"values": (1,)}
        list_detail = event("GAP", [initial_id]); list_detail["detail"] = {"values": [1]}
        assert oracle_record_id(
            "p030evt-v1", "p030-event-v1", tuple_detail, EVENT_FIELDS
        ) == oracle_record_id("p030evt-v1", "p030-event-v1", list_detail, EVENT_FIELDS)
        expect_refused(
            lambda: subject.event_id(tuple_detail), "tuple_detail", subject.ContractRefused
        )
        supported_detail = event("GAP", [initial_id])
        supported_detail["detail"] = {
            "values": [None, True, 1, 1.5, "text", {"nested": False}]
        }
        subject.event_id(supported_detail)
        bool_detail = event("GAP", [initial_id]); bool_detail["detail"] = {"value": True}
        int_detail = event("GAP", [initial_id]); int_detail["detail"] = {"value": 1}
        assert subject.event_id(bool_detail) != subject.event_id(int_detail)
        print("EVENT DETAIL COLLISION/TYPE MUTANTS: DETECTED")
        print("TYPE/CANONICALIZATION REFUSALS: PASS")
    finally:
        socket.socket.connect = original_connect  # type: ignore[method-assign]
        socket.create_connection = original_create  # type: ignore[assignment]

    assert attempts == [], ("network_attempts", attempts)
    print("NETWORK ATTEMPTS: 0")
    print("P030 MARKET DATA CONTRACTS CHECK: PASS")


if __name__ == "__main__":
    main()
