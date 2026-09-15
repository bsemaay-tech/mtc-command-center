"""P0-12 D1 offline MTC funding materializer — synthetic-only contract suite.

Everything in this file is explicitly synthetic. The event hashes, symbols,
amounts, rates, oracle prices, provenance strings and completion witnesses are
invented for the test. None of them is a Hyperliquid capture, a venue fact, or
a claim about any real account, interval or payment. The suite therefore proves
one narrow property only: *given* synthetic caller facts, the exporter builds a
deterministic, physically non-admittable synthetic candidate — or refuses.

It deliberately does **not** prove real-world completeness, a real settlement
time/rate association, or a production ``source_event_digest`` byte domain.
Those remain open venue evidence dependencies.

Each test builds its own throwaway snapshot under pytest's ``tmp_path``. No
live database is opened, no broker/host/network is contacted, and the snapshot
bytes are asserted unchanged after every run.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path

import pytest

from bridge.engine.types import (
    FundingAttribution,
    FundingEventRecord,
    ReconcileAttemptState,
    canonical_reconcile_json,
)
from bridge.store.db import (
    SCHEMA_VERSION_BASELINE,
    SCHEMA_VERSION_FUNDING_PAYLOAD,
    Store,
)
from tools import export_mtc_funding as exporter


# ---------------------------------------------------------------------------
# Synthetic fixture material
# ---------------------------------------------------------------------------

SYMBOL = "BTC"
SCHEDULE_ID = "SYNTH-P012-D1-MATERIALIZER-V1"
START = "2026-09-11T12:00:00Z"
END = "2026-09-11T13:00:00Z"
ACCOUNT_SCOPE = "SYNTHETIC-ACCOUNT-SCOPE-0001"
WITNESS = "SYNTHETIC-WITNESS-0001"

# Two invented BTC payments. EVENT_A is later in UTF-8 id order but earlier in
# event time, so a correct ordering must prefer time over identity.
ID_A = "0xsynthetic0002"
ID_B = "0xsynthetic0001"
TS_A = "2026-09-11T12:00:00.031527Z"
TS_B = "2026-09-11T12:30:00Z"

RECORDED = datetime(2026, 9, 11, 12, 0, tzinfo=UTC)

def synthetic_event(
    *,
    event_id: str,
    effective_ts: datetime,
    amount_usdc: float = -1.25,
    funding_rate: float | None = 0.0000125,
    position_szi: float | None = 0.1,
    n_samples: int | None = 1,
    attribution: FundingAttribution = FundingAttribution.ATTRIBUTED,
) -> FundingEventRecord:
    """One invented retained funding event."""
    return FundingEventRecord(
        event_id=event_id,
        symbol=SYMBOL,
        amount_usdc=amount_usdc,
        effective_ts=effective_ts,
        source="HL_USER_FUNDING",
        attribution=attribution,
        funding_rate=funding_rate,
        position_szi=position_szi,
        n_samples=n_samples,
    )


EVENT_A = synthetic_event(
    event_id=ID_A,
    effective_ts=datetime(2026, 9, 11, 12, 0, 0, 31527, tzinfo=UTC),
)
EVENT_B = synthetic_event(
    event_id=ID_B,
    effective_ts=datetime(2026, 9, 11, 12, 30, tzinfo=UTC),
    amount_usdc=-2.5,
    funding_rate=0.000025,
)


def retained_row(
    event: FundingEventRecord,
    *,
    payload: dict | None = ...,
    payload_digest: str | None = None,
    payload_reason: str | None = None,
    attribution: str | None = None,
    ledger_effective_ts: str | None = None,
) -> dict:
    """The closed retained-row shape the CLI hands to the pure function."""
    body = event.authoritative() if payload is ... else payload
    if payload_reason is None:
        payload_reason = (
            exporter.PAYLOAD_RETAINED
            if body is not None
            else exporter.CANDIDATE_PAYLOAD_UNAVAILABLE
        )
    return {
        "event_id": event.event_id,
        "symbol": event.symbol,
        "attribution": attribution or event.attribution.value,
        "ledger_effective_ts": (
            ledger_effective_ts
            or event.effective_ts.astimezone(UTC).isoformat()
        ),
        "payload_digest": payload_digest or event.digest,
        "payload": body,
        "payload_reason": payload_reason,
    }


def provenance(*, source_sha256: str) -> dict:
    """Closed synthetic provenance; every value is invented for the test."""
    return {
        "evidence_kind": exporter.SYNTHETIC_EVIDENCE_KIND,
        "extraction_method": "DIRECT_SYNTHETIC_VECTOR_V1",
        "source_locator": "synthetic://p012-d1/fixture",
        "source_sha256": source_sha256,
        "source_title": "SYNTHETIC-D1-FIXTURE",
    }


def synthetic_source_bytes(item: dict) -> bytes:
    """The exact canonical synthetic event-byte domain for one binding."""
    fields = {
        key: item[key]
        for key in exporter.SOURCE_BINDING_KEYS
    }
    try:
        fields["event_timestamp"] = exporter._parse_instant(
            fields["event_timestamp"], "synthetic source event_timestamp"
        ).text
    except exporter._Refusal:
        pass
    return canonical_reconcile_json(fields).encode("utf-8")


def binding(
    *,
    funding_event_id: str,
    event_timestamp: str,
    raw_rate: object = "0.0000125",
    oracle_price: object = "60000.50",
    positive_rate_payer: str = "LONG",
    oracle_price_source: str = "SYNTHETIC_SPOT_ORACLE",
    source_event_digest: str | None = None,
    provenance_override: dict | None = None,
) -> dict:
    """The eight current MTC input fields, all synthetic."""
    item = {
        "event_timestamp": event_timestamp,
        "funding_event_id": funding_event_id,
        "raw_rate": raw_rate,
        "positive_rate_payer": positive_rate_payer,
        "oracle_price": oracle_price,
        "oracle_price_source": oracle_price_source,
    }
    digest = source_event_digest or hashlib.sha256(
        synthetic_source_bytes(item)
    ).hexdigest()
    return {
        **item,
        "provenance": (
            provenance(source_sha256=digest)
            if provenance_override is None
            else provenance_override
        ),
        "source_event_digest": digest,
    }


def source_witnesses(items: object) -> dict[str, str]:
    if not isinstance(items, list):
        return {}
    return {
        item["funding_event_id"]: synthetic_source_bytes(item).hex()
        for item in items
        if all(key in item for key in exporter.SOURCE_BINDING_KEYS)
    }


DIGEST_A = binding(funding_event_id=ID_A, event_timestamp=TS_A)[
    "source_event_digest"
]
DIGEST_B = binding(funding_event_id=ID_B, event_timestamp=TS_B)[
    "source_event_digest"
]


def coverage(
    *,
    expected_event_ids: list[str] | None = None,
    unattributed_event_ids: list[str] | None = None,
    complete: object = True,
    evidence_kind: str = exporter.SYNTHETIC_EVIDENCE_KIND,
    start: str = START,
    end: str = END,
    symbol: str = SYMBOL,
    account_scope: str = ACCOUNT_SCOPE,
    witness_identity: str = WITNESS,
    source_witnesses_override: dict[str, str] | None = None,
) -> dict:
    """The explicit entire-interval inventory/scope/identity witness."""
    return {
        "evidence_kind": evidence_kind,
        "complete": complete,
        "interval_start_inclusive": start,
        "interval_end_exclusive": end,
        "symbol": symbol,
        "account_scope": account_scope,
        "witness_identity": witness_identity,
        "source_witnesses": (
            source_witnesses([
                binding(funding_event_id=ID_A, event_timestamp=TS_A),
                binding(funding_event_id=ID_B, event_timestamp=TS_B),
            ])
            if source_witnesses_override is None
            else source_witnesses_override
        ),
        "expected_event_ids": (
            [ID_A, ID_B] if expected_event_ids is None else expected_event_ids
        ),
        "unattributed_event_ids": (
            [] if unattributed_event_ids is None else unattributed_event_ids
        ),
    }


def build(**kwargs):
    """The approved pure entry point with the standard synthetic defaults."""
    witness_override = kwargs.pop("source_witnesses", None)
    params = {
        "retained_rows": [retained_row(EVENT_A), retained_row(EVENT_B)],
        "approved_event_bindings": [
            binding(funding_event_id=ID_A, event_timestamp=TS_A),
            binding(funding_event_id=ID_B, event_timestamp=TS_B),
        ],
        "coverage": coverage(),
        "schedule_id": SCHEDULE_ID,
        "start_inclusive": START,
        "end_exclusive": END,
    }
    params.update(kwargs)
    if isinstance(params["coverage"], dict):
        cover = dict(params["coverage"])
        cover["source_witnesses"] = (
            source_witnesses(params["approved_event_bindings"])
            if witness_override is None
            else witness_override
        )
        params["coverage"] = cover
    return exporter.build_funding_candidate(**params)


# ---------------------------------------------------------------------------
# Snapshot fixtures (offline, quiescent, never a live database)
# ---------------------------------------------------------------------------


def write_snapshot(
    path: Path,
    *events: FundingEventRecord,
    schema_version: int = SCHEMA_VERSION_FUNDING_PAYLOAD,
) -> Path:
    """Create one throwaway offline snapshot and close it quiescent."""
    store = Store(path)
    store.initialize(target_schema_version=schema_version)
    if events:
        attempt_id = store.reserve_reconcile_attempt(
            run_id="run-p012-d1", started_ts=RECORDED, deadline_s=5.0, max_skew_s=5.0
        )
        store.finalize_reconcile_attempt(
            attempt_id=attempt_id,
            state=ReconcileAttemptState.INCOMPLETE,
            ended_ts=RECORDED,
            duration_ms=1,
            canonical_hash=None,
            reason_code="SYNTHETIC_FIXTURE",
            funding_events=events,
            accepted=False,
            fresh=False,
        )
    store.close()
    return path


def packet_bytes(*, bindings: list[dict] | None = None, cover: dict | None = None) -> bytes:
    selected_bindings = [
        binding(funding_event_id=ID_A, event_timestamp=TS_A),
        binding(funding_event_id=ID_B, event_timestamp=TS_B),
    ] if bindings is None else bindings
    selected_coverage = dict(coverage() if cover is None else cover)
    selected_coverage["source_witnesses"] = source_witnesses(selected_bindings)
    packet = {
        "packet_version": exporter.PACKET_VERSION,
        "coverage": selected_coverage,
        "bindings": selected_bindings,
    }
    return json.dumps(packet, sort_keys=True).encode("utf-8")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


_ANY_TIMESTAMP = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})")


def _timestamps_in(value) -> set[str]:
    """Every RFC 3339 instant anywhere inside a nested structure."""
    if isinstance(value, str):
        return set(_ANY_TIMESTAMP.findall(value))
    if isinstance(value, dict):
        found = set()
        for key, item in value.items():
            found |= _timestamps_in(key) | _timestamps_in(item)
        return found
    if isinstance(value, (list, tuple)):
        found = set()
        for item in value:
            found |= _timestamps_in(item)
        return found
    return set()


def sidecar_files(path: Path) -> list[str]:
    """Any WAL/SHM/journal companion that appeared beside the snapshot."""
    return sorted(
        child.name
        for child in path.parent.iterdir()
        if child.name.startswith(path.name) and child.name != path.name
    )


def run_cli(
    tmp_path: Path,
    *,
    snapshot: Path,
    staging: Path,
    packet: bytes | None = None,
    symbol: str = SYMBOL,
    start: str = START,
    end: str = END,
    schedule_id: str = SCHEDULE_ID,
    bindings_path: Path | None = None,
) -> int:
    if bindings_path is None:
        bindings_path = tmp_path / "bindings.json"
        bindings_path.write_bytes(packet_bytes() if packet is None else packet)
    return exporter.main([
        "--snapshot", str(snapshot),
        "--bindings", str(bindings_path),
        "--symbol", symbol,
        "--start", start,
        "--end", end,
        "--schedule-id", schedule_id,
        "--staging", str(staging),
    ])


@pytest.fixture()
def snapshot(tmp_path: Path) -> Path:
    return write_snapshot(tmp_path / "offline" / "snapshot.db", EVENT_A, EVENT_B)


# ---------------------------------------------------------------------------
# The accepted synthetic candidate — exact bytes, exact order
# ---------------------------------------------------------------------------


def expected_event(
    event: FundingEventRecord,
    *,
    event_timestamp: str,
    raw_rate: str,
    oracle_price: str,
    source_event_digest: str,
    ts_matches: bool,
) -> dict:
    return {
        "binding": {
            "event_timestamp": event_timestamp,
            "funding_event_id": event.event_id,
            "oracle_price": oracle_price,
            "oracle_price_source": "SYNTHETIC_SPOT_ORACLE",
            "positive_rate_payer": "LONG",
            "provenance": provenance(source_sha256=source_event_digest),
            "raw_rate": raw_rate,
            "source_event_digest": source_event_digest,
        },
        "binding_notes": {
            "bridge_effective_ts_equals_binding_event_timestamp": ts_matches,
            "settlement_rate_source": exporter.SETTLEMENT_SOURCE,
            "settlement_time_source": exporter.SETTLEMENT_SOURCE,
        },
        "bridge_evidence": {
            "attribution": event.attribution.value,
            "event_id": event.event_id,
            "ledger_effective_ts": event.effective_ts.astimezone(UTC)
            .isoformat()
            .replace("+00:00", "Z"),
            "payload": event.authoritative(),
            "payload_digest": event.digest,
        },
    }


def expected_candidate() -> dict:
    return {
        "admission_status": exporter.ADMISSION_STATUS,
        "artifact_kind": exporter.ARTIFACT_KIND,
        "bridge_payload_digest_domain": exporter.BRIDGE_PAYLOAD_DIGEST_DOMAIN,
        "not_a_production_record": exporter.NOT_A_PRODUCTION_RECORD,
        "numeric_representation": exporter.NUMERIC_REPRESENTATION,
        "source_event_digest_domain": exporter.SOURCE_EVENT_DIGEST_DOMAIN,
        "synthetic_candidate": {
            "account_scope": ACCOUNT_SCOPE,
            "coverage_witness": {
                "account_scope": ACCOUNT_SCOPE,
                "complete": True,
                "evidence_kind": exporter.SYNTHETIC_EVIDENCE_KIND,
                "expected_event_ids": [ID_B, ID_A],
                "interval_end_exclusive": END,
                "interval_start_inclusive": START,
                "symbol": SYMBOL,
                "source_witnesses": source_witnesses([
                    binding(funding_event_id=ID_A, event_timestamp=TS_A),
                    binding(funding_event_id=ID_B, event_timestamp=TS_B),
                ]),
                "unattributed_event_ids": [],
                "witness_identity": WITNESS,
            },
            "effective_interval": {
                "end_exclusive": END,
                "start_inclusive": START,
            },
            "event_count": 2,
            "symbol_scope": SYMBOL,
            "synthetic_events": [
                expected_event(
                    EVENT_A,
                    event_timestamp=TS_A,
                    raw_rate="0.0000125",
                    oracle_price="60000.50",
                    source_event_digest=DIGEST_A,
                    ts_matches=True,
                ),
                expected_event(
                    EVENT_B,
                    event_timestamp=TS_B,
                    raw_rate="0.0000125",
                    oracle_price="60000.50",
                    source_event_digest=DIGEST_B,
                    ts_matches=True,
                ),
            ],
            "synthetic_schedule_id": SCHEDULE_ID,
        },
        "synthetic_only": True,
    }


def test_two_retained_payments_produce_the_exact_candidate_bytes():
    result = build()

    assert result.accepted is True
    assert result.reason_code == exporter.SYNTHETIC_CANDIDATE_BUILT
    expected_bytes = (
        canonical_reconcile_json(expected_candidate()).encode("utf-8") + b"\n"
    )
    assert result.candidate_bytes == expected_bytes
    assert result.candidate_sha256 == hashlib.sha256(expected_bytes).hexdigest()


def test_candidate_bytes_are_utf8_sorted_compact_and_lf_terminated():
    body = build().candidate_bytes

    assert body.endswith(b"\n")
    assert body.count(b"\n") == 1
    assert b"\r" not in body
    assert b"NaN" not in body and b"Infinity" not in body
    decoded = body.decode("utf-8")
    # Sorted keys and compact separators, proven by exact re-serialization.
    assert canonical_reconcile_json(json.loads(decoded)) + "\n" == decoded


def test_subsecond_precision_and_z_spelling_are_preserved():
    body = build().candidate_bytes.decode("utf-8")

    assert '"event_timestamp":"2026-09-11T12:00:00.031527Z"' in body
    # The retained payload stays verbatim evidence, +00:00 spelling included,
    # because altering it would stop it reproducing its ledger digest.
    assert '"effective_ts":"2026-09-11T12:00:00.031527+00:00"' in body
    assert '"ledger_effective_ts":"2026-09-11T12:00:00.031527Z"' in body


def test_event_order_is_time_then_utf8_event_id_bytes():
    ids = [
        event["binding"]["funding_event_id"]
        for event in json.loads(build().candidate_bytes)["synthetic_candidate"][
            "synthetic_events"
        ]
    ]
    # ID_B sorts first as bytes but settles later, so time must win.
    assert ID_B < ID_A
    assert ids == [ID_A, ID_B]


def test_identical_instants_break_ties_on_event_id_not_on_fraction_text():
    """``.1`` and ``.10`` are the same instant; only the id may order them."""
    early = synthetic_event(
        event_id="zzz-later-id", effective_ts=datetime(2026, 9, 11, 12, 0, tzinfo=UTC)
    )
    late = synthetic_event(
        event_id="aaa-earlier-id",
        effective_ts=datetime(2026, 9, 11, 12, 0, tzinfo=UTC),
    )
    result = build(
        retained_rows=[retained_row(early), retained_row(late)],
        approved_event_bindings=[
                binding(
                    funding_event_id="zzz-later-id",
                    event_timestamp="2026-09-11T12:00:00.10Z",
                ),
                binding(
                    funding_event_id="aaa-earlier-id",
                    event_timestamp="2026-09-11T12:00:00.1Z",
                ),
        ],
        coverage=coverage(expected_event_ids=["zzz-later-id", "aaa-earlier-id"]),
    )

    assert result.accepted is True, result.report
    ids = [
        event["binding"]["funding_event_id"]
        for event in json.loads(result.candidate_bytes)["synthetic_candidate"][
            "synthetic_events"
        ]
    ]
    assert ids == ["aaa-earlier-id", "zzz-later-id"]


def test_arbitrary_subsecond_digits_survive_without_truncation():
    event = synthetic_event(
        event_id=ID_A, effective_ts=datetime(2026, 9, 11, 12, 0, tzinfo=UTC)
    )
    result = build(
        retained_rows=[retained_row(event)],
        approved_event_bindings=[
            binding(
                funding_event_id=ID_A,
                event_timestamp="2026-09-11T12:00:00.123456789012Z",
            )
        ],
        coverage=coverage(expected_event_ids=[ID_A]),
    )

    assert result.accepted is True, result.report
    assert b'"2026-09-11T12:00:00.123456789012Z"' in result.candidate_bytes


def test_plus_zero_offset_is_respelled_z_without_moving_the_instant():
    result = build(
        approved_event_bindings=[
            binding(
                funding_event_id=ID_A,
                event_timestamp="2026-09-11T12:00:00.031527+00:00",
            ),
            binding(funding_event_id=ID_B, event_timestamp=TS_B),
        ]
    )

    assert result.candidate_bytes == build().candidate_bytes


def test_non_zero_offset_is_converted_exactly_not_dropped():
    result = build(
        approved_event_bindings=[
            binding(
                funding_event_id=ID_A,
                event_timestamp="2026-09-11T14:00:00.031527+02:00",
            ),
            binding(funding_event_id=ID_B, event_timestamp=TS_B),
        ]
    )

    assert result.candidate_bytes == build().candidate_bytes


@pytest.mark.parametrize(
    "timestamp",
    [
        "2026-09-15T16:39:00.031527+99:99",
        "2026-09-07T07:21:00.031527-99:99",
        "2026-09-12T12:00:00.031527+24:00",
        "2026-09-10T12:00:00.031527-24:00",
        "2026-09-11T13:00:00.031527+00:60",
        "2026-09-11T11:00:00.031527-00:60",
    ],
)
def test_invalid_rfc3339_offset_ranges_refuse(timestamp):
    result = build(approved_event_bindings=[
        binding(funding_event_id=ID_A, event_timestamp=timestamp),
        binding(funding_event_id=ID_B, event_timestamp=TS_B),
    ])

    assert result.accepted is False
    assert result.reason_code == exporter.CANDIDATE_TIMESTAMP_INVALID


@pytest.mark.parametrize(
    "timestamp",
    [
        "2026-09-12T11:59:00.031527+23:59",
        "2026-09-10T12:01:00.031527-23:59",
    ],
)
def test_legal_rfc3339_offset_edges_are_converted_exactly(timestamp):
    result = build(approved_event_bindings=[
        binding(funding_event_id=ID_A, event_timestamp=timestamp),
        binding(funding_event_id=ID_B, event_timestamp=TS_B),
    ])

    assert result.candidate_bytes == build().candidate_bytes


@pytest.mark.parametrize(
    "timestamp",
    [
        "0001-01-01T00:00:00+23:59",
        "9999-12-31T23:59:59-23:59",
    ],
)
def test_rfc3339_offset_calendar_overflow_refuses(timestamp):
    first = binding(funding_event_id=ID_A, event_timestamp=TS_A)
    first["event_timestamp"] = timestamp
    escaped = None
    try:
        result = build(
            approved_event_bindings=[
                first,
                binding(funding_event_id=ID_B, event_timestamp=TS_B),
            ],
            source_witnesses=coverage()["source_witnesses"],
        )
    except OverflowError as exc:
        escaped = exc
        result = None

    assert escaped is None
    assert result is not None
    assert result.accepted is False
    assert result.reason_code == exporter.CANDIDATE_TIMESTAMP_INVALID


def test_repeat_of_identical_input_is_byte_identical():
    first = build()
    second = build()

    assert first.candidate_bytes == second.candidate_bytes
    assert first.candidate_sha256 == second.candidate_sha256
    assert first.report == second.report


def test_report_carries_no_volatile_value_and_labels_the_limitations():
    report = build().report

    assert report["accepted"] is True
    assert report["synthetic_only"] is True
    assert report["production_mode"] == exporter.PRODUCTION_MODE_UNAVAILABLE
    assert report["non_admission"]["admission_status"] == exporter.ADMISSION_STATUS
    assert report["evidence_limitations"]
    assert all(isinstance(item, str) for item in report["evidence_limitations"])
    assert report["candidate_sha256"] == build().candidate_sha256
    # Nothing clock-derived may reach the report: the only instants it carries
    # are the caller's own declared interval bounds.
    assert _timestamps_in(report) == {START, END}


def test_extra_retained_rows_refuse_instead_of_being_silently_dropped():
    outside = synthetic_event(
        event_id="0xsynthetic0009",
        effective_ts=datetime(2026, 9, 11, 14, 0, tzinfo=UTC),
    )
    result = build(
        retained_rows=[
            retained_row(EVENT_A),
            retained_row(EVENT_B),
            retained_row(outside),
        ]
    )

    assert result.accepted is False
    assert result.reason_code == exporter.CANDIDATE_INVENTORY_MISMATCH
    assert result.report["inventory_missing_event_ids"] == ["0xsynthetic0009"]
    assert result.candidate_bytes is None


# ---------------------------------------------------------------------------
# Duplicates and conflicts
# ---------------------------------------------------------------------------


def test_duplicate_identical_binding_is_handled_once():
    duplicate = binding(funding_event_id=ID_A, event_timestamp=TS_A)
    result = build(
        approved_event_bindings=[
            binding(funding_event_id=ID_A, event_timestamp=TS_A),
            duplicate,
            binding(funding_event_id=ID_B, event_timestamp=TS_B),
        ]
    )

    assert result.accepted is True, result.report
    assert result.candidate_bytes == build().candidate_bytes


def test_conflicting_binding_for_one_event_refuses():
    result = build(
        approved_event_bindings=[
            binding(funding_event_id=ID_A, event_timestamp=TS_A),
            binding(
                funding_event_id=ID_A, event_timestamp=TS_A, raw_rate="0.0000126"
            ),
            binding(funding_event_id=ID_B, event_timestamp=TS_B),
        ]
    )

    assert result.accepted is False
    assert result.candidate_bytes is None
    assert result.candidate_sha256 is None
    assert result.reason_code == exporter.CANDIDATE_EVENT_CONFLICT
    assert ID_A in result.report["reason_detail"]


def test_duplicate_retained_rows_with_different_content_refuse():
    result = build(
        retained_rows=[
            retained_row(EVENT_A),
            retained_row(EVENT_A, payload_digest=DIGEST_A),
            retained_row(EVENT_B),
        ]
    )

    assert result.accepted is False
    assert result.reason_code == exporter.CANDIDATE_EVENT_CONFLICT


# ---------------------------------------------------------------------------
# Payload availability and integrity — inherited Store reason codes
# ---------------------------------------------------------------------------


def test_unavailable_payload_refuses_and_is_never_zero_filled():
    result = build(
        retained_rows=[
            retained_row(EVENT_A, payload=None),
            retained_row(EVENT_B),
        ]
    )

    assert result.accepted is False
    assert result.candidate_bytes is None
    assert result.reason_code == exporter.CANDIDATE_PAYLOAD_UNAVAILABLE
    assert result.report["store_reason_codes"] == {
        ID_A: exporter.CANDIDATE_PAYLOAD_UNAVAILABLE
    }


@pytest.mark.parametrize(
    "store_code",
    [
        "FUNDING_PAYLOAD_DIGEST_MISMATCH",
        "FUNDING_PAYLOAD_MALFORMED",
        "FUNDING_PAYLOAD_DOMAIN_MISMATCH",
        "FUNDING_PAYLOAD_IDENTITY_MISMATCH",
        "FUNDING_PAYLOAD_EVENT_UNKNOWN",
    ],
)
def test_store_refusal_codes_are_preserved_verbatim(store_code):
    result = build(
        retained_rows=[
            retained_row(EVENT_A, payload=None, payload_reason=store_code),
            retained_row(EVENT_B),
        ]
    )

    assert result.accepted is False
    assert result.reason_code == store_code
    assert result.report["store_reason_codes"] == {ID_A: store_code}


def test_tampered_payload_is_refused_by_the_pure_function_itself():
    """The pure function re-proves the digest; it never trusts the caller."""
    tampered = dict(EVENT_A.authoritative())
    tampered["amount_usdc"] = -1.26
    result = build(
        retained_rows=[
            retained_row(EVENT_A, payload=tampered),
            retained_row(EVENT_B),
        ]
    )

    assert result.accepted is False
    assert result.reason_code == "FUNDING_PAYLOAD_DIGEST_MISMATCH"


def test_payload_outside_the_authoritative_domain_is_refused():
    extra = dict(EVENT_A.authoritative())
    extra["oracle_price"] = 60000.5
    result = build(
        retained_rows=[
            retained_row(EVENT_A, payload=extra),
            retained_row(EVENT_B),
        ]
    )

    assert result.accepted is False
    assert result.reason_code == "FUNDING_PAYLOAD_DOMAIN_MISMATCH"


def test_payload_identity_disagreeing_with_its_row_is_refused():
    borrowed = dict(EVENT_B.authoritative())
    result = build(
        retained_rows=[
            retained_row(
                EVENT_A, payload=borrowed, payload_digest=EVENT_B.digest
            ),
            retained_row(EVENT_B),
        ]
    )

    assert result.accepted is False
    assert result.reason_code == "FUNDING_PAYLOAD_IDENTITY_MISMATCH"


@pytest.mark.parametrize("bad", [float("nan"), float("inf"), float("-inf")])
def test_nonfinite_payload_value_is_refused(bad):
    nonfinite = dict(EVENT_A.authoritative())
    nonfinite["amount_usdc"] = bad
    result = build(
        retained_rows=[
            retained_row(EVENT_A, payload=nonfinite),
            retained_row(EVENT_B),
        ]
    )

    assert result.accepted is False
    assert result.reason_code == exporter.CANDIDATE_NONFINITE_VALUE


@pytest.mark.parametrize("bad", [float("nan"), float("inf"), float("-inf")])
def test_duplicate_retained_identity_with_nonfinite_payload_refuses(bad):
    nonfinite = dict(EVENT_A.authoritative())
    nonfinite["amount_usdc"] = bad

    escaped = None
    try:
        result = build(retained_rows=[
            retained_row(EVENT_A),
            retained_row(EVENT_A, payload=nonfinite),
            retained_row(EVENT_B),
        ])
    except ValueError as exc:
        escaped = exc
        result = None

    assert escaped is None
    assert result is not None
    assert result.accepted is False
    assert result.reason_code == exporter.CANDIDATE_NONFINITE_VALUE


def test_optional_payload_fields_may_stay_none():
    sparse = synthetic_event(
        event_id=ID_A,
        effective_ts=datetime(2026, 9, 11, 12, 0, 0, 31527, tzinfo=UTC),
        position_szi=None,
        n_samples=None,
    )
    result = build(
        retained_rows=[retained_row(sparse), retained_row(EVENT_B)],
    )

    assert result.accepted is True, result.report
    assert b'"n_samples":null' in result.candidate_bytes
    assert b'"position_szi":null' in result.candidate_bytes


def test_unattributed_event_needs_an_explicit_scope_acknowledgement():
    unattributed = synthetic_event(
        event_id=ID_A,
        effective_ts=datetime(2026, 9, 11, 12, 0, 0, 31527, tzinfo=UTC),
        attribution=FundingAttribution.UNATTRIBUTED,
    )
    rows = [retained_row(unattributed), retained_row(EVENT_B)]

    silent = build(retained_rows=rows)
    assert silent.accepted is False
    assert silent.reason_code == exporter.CANDIDATE_ATTRIBUTION_SCOPE_MISMATCH

    acknowledged = build(
        retained_rows=rows, coverage=coverage(unattributed_event_ids=[ID_A])
    )
    assert acknowledged.accepted is True, acknowledged.report
    assert b'"attribution":"UNATTRIBUTED"' in acknowledged.candidate_bytes


# ---------------------------------------------------------------------------
# Binding validation — closed domain, exact decimals, no invented facts
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("value", [0.0000125, 1.25e-05, 1.0])
def test_binary_float_rate_is_refused_rather_than_silently_rounded(value):
    result = build(
        approved_event_bindings=[
            binding(funding_event_id=ID_A, event_timestamp=TS_A, raw_rate=value),
            binding(funding_event_id=ID_B, event_timestamp=TS_B),
        ]
    )

    assert result.accepted is False
    assert result.reason_code == exporter.CANDIDATE_PRECISION_UNREPRESENTABLE
    assert "raw_rate" in result.report["reason_detail"]


def test_binary_float_oracle_price_is_refused():
    result = build(
        approved_event_bindings=[
            binding(
                funding_event_id=ID_A, event_timestamp=TS_A, oracle_price=60000.5
            ),
            binding(funding_event_id=ID_B, event_timestamp=TS_B),
        ]
    )

    assert result.accepted is False
    assert result.reason_code == exporter.CANDIDATE_PRECISION_UNREPRESENTABLE


def test_decimal_strings_keep_their_exact_written_form():
    result = build(
        approved_event_bindings=[
            binding(
                funding_event_id=ID_A,
                event_timestamp=TS_A,
                raw_rate="0.00001250",
                oracle_price="60000.5000",
            ),
            binding(funding_event_id=ID_B, event_timestamp=TS_B),
        ]
    )

    assert result.accepted is True, result.report
    assert b'"raw_rate":"0.00001250"' in result.candidate_bytes
    assert b'"oracle_price":"60000.5000"' in result.candidate_bytes


@pytest.mark.parametrize(
    "literal", ["1e-5", "+1", ".5", "01.5", "0x1", "", "1_000", "nan", "Infinity"]
)
def test_ambiguous_numeric_literals_are_refused(literal):
    result = build(
        approved_event_bindings=[
            binding(funding_event_id=ID_A, event_timestamp=TS_A, raw_rate=literal),
            binding(funding_event_id=ID_B, event_timestamp=TS_B),
        ]
    )

    assert result.accepted is False
    assert result.reason_code in {
        exporter.CANDIDATE_BINDING_INVALID,
        exporter.CANDIDATE_PRECISION_UNREPRESENTABLE,
    }


@pytest.mark.parametrize("price", ["0", "-1", "-0.0001"])
def test_non_positive_oracle_price_is_refused(price):
    result = build(
        approved_event_bindings=[
            binding(
                funding_event_id=ID_A, event_timestamp=TS_A, oracle_price=price
            ),
            binding(funding_event_id=ID_B, event_timestamp=TS_B),
        ]
    )

    assert result.accepted is False
    assert result.reason_code == exporter.CANDIDATE_BINDING_INVALID


def test_short_payer_is_refused_because_only_long_is_approved():
    result = build(
        approved_event_bindings=[
            binding(
                funding_event_id=ID_A,
                event_timestamp=TS_A,
                positive_rate_payer="SHORT",
            ),
            binding(funding_event_id=ID_B, event_timestamp=TS_B),
        ]
    )

    assert result.accepted is False
    assert result.reason_code == exporter.CANDIDATE_BINDING_INVALID
    assert "positive_rate_payer" in result.report["reason_detail"]


def test_naive_binding_timestamp_is_refused():
    result = build(
        approved_event_bindings=[
            binding(
                funding_event_id=ID_A, event_timestamp="2026-09-11T12:00:00.031527"
            ),
            binding(funding_event_id=ID_B, event_timestamp=TS_B),
        ]
    )

    assert result.accepted is False
    assert result.reason_code == exporter.CANDIDATE_TIMESTAMP_INVALID


@pytest.mark.parametrize(
    "stamp",
    [
        "2026-09-11T12:00:60Z",
        "2026-09-11 12:00:00Z",
        "2026-09-11T12:00:00.Z",
        "2026-13-11T12:00:00Z",
        "2026-09-11T12:00:00+00:00Z",
    ],
)
def test_malformed_binding_timestamps_are_refused(stamp):
    result = build(
        approved_event_bindings=[
            binding(funding_event_id=ID_A, event_timestamp=stamp),
            binding(funding_event_id=ID_B, event_timestamp=TS_B),
        ]
    )

    assert result.accepted is False
    assert result.reason_code == exporter.CANDIDATE_TIMESTAMP_INVALID


def test_extra_binding_key_is_refused():
    extra = binding(funding_event_id=ID_A, event_timestamp=TS_A)
    extra["settlement_currency"] = "USDC"
    result = build(
        approved_event_bindings=[
            extra,
            binding(funding_event_id=ID_B, event_timestamp=TS_B),
        ]
    )

    assert result.accepted is False
    assert result.reason_code == exporter.CANDIDATE_BINDING_INVALID


def test_missing_binding_key_is_refused():
    short = binding(funding_event_id=ID_A, event_timestamp=TS_A)
    del short["oracle_price_source"]
    result = build(
        approved_event_bindings=[
            short,
            binding(funding_event_id=ID_B, event_timestamp=TS_B),
        ]
    )

    assert result.accepted is False
    assert result.reason_code == exporter.CANDIDATE_BINDING_INVALID


@pytest.mark.parametrize("field", ["source_event_digest", "source_sha256"])
def test_referenced_byte_digests_must_be_lower_case_sha256(field):
    if field == "source_event_digest":
        bad = binding(
            funding_event_id=ID_A, event_timestamp=TS_A, source_event_digest="A" * 64
        )
    else:
        bad = binding(
            funding_event_id=ID_A,
            event_timestamp=TS_A,
            provenance_override=provenance(source_sha256="not-a-digest"),
        )
    result = build(
        approved_event_bindings=[
            bad,
            binding(funding_event_id=ID_B, event_timestamp=TS_B),
        ]
    )

    assert result.accepted is False
    assert result.reason_code == exporter.CANDIDATE_BINDING_INVALID


def test_empty_provenance_is_refused():
    result = build(
        approved_event_bindings=[
            binding(
                funding_event_id=ID_A, event_timestamp=TS_A, provenance_override={}
            ),
            binding(funding_event_id=ID_B, event_timestamp=TS_B),
        ]
    )

    assert result.accepted is False
    assert result.reason_code == exporter.CANDIDATE_BINDING_INVALID


def test_source_event_digest_must_not_reuse_the_bridge_payload_digest():
    """The synthetic source domain is never the normalized Bridge digest."""
    result = build(
        approved_event_bindings=[
            binding(
                funding_event_id=ID_A,
                event_timestamp=TS_A,
                source_event_digest=EVENT_A.digest,
            ),
            binding(funding_event_id=ID_B, event_timestamp=TS_B),
        ]
    )

    assert result.accepted is False
    assert result.reason_code == exporter.CANDIDATE_DIGEST_DOMAIN_CONFLATION


def test_candidate_never_renames_the_payload_digest_field():
    body = json.loads(build().candidate_bytes)
    event = body["synthetic_candidate"]["synthetic_events"][0]

    assert "payload_digest" in event["bridge_evidence"]
    assert "source_event_digest" not in event["bridge_evidence"]
    assert event["binding"]["source_event_digest"] != event["bridge_evidence"][
        "payload_digest"
    ]


def test_candidate_carries_no_mtc_computed_field():
    body = build().candidate_bytes

    for field in (
        b"lifecycle_id",
        b"cumulative_funding",
        b"funding_cash_delta",
        b"position_side",
        b"open_qty",
        b"notional",
        b"cash_event_id",
        b"sequence",
        b"long_cashflow_rate",
    ):
        assert field not in body


# ---------------------------------------------------------------------------
# Whole-interval completeness — a coverage flag alone proves nothing
# ---------------------------------------------------------------------------


def test_coverage_true_without_a_matching_inventory_refuses():
    result = build(coverage=coverage(expected_event_ids=[ID_A]))

    assert result.accepted is False
    assert result.reason_code == exporter.CANDIDATE_INVENTORY_MISMATCH
    assert result.report["unbound_events"] == []
    assert result.report["inventory_missing_event_ids"] == [ID_B]


def test_incomplete_coverage_flag_refuses():
    result = build(coverage=coverage(complete=False))

    assert result.accepted is False
    assert result.reason_code == exporter.CANDIDATE_COVERAGE_INVALID


@pytest.mark.parametrize("flag", ["true", "VERIFIED", 1, None])
def test_non_boolean_completeness_assertions_refuse(flag):
    result = build(coverage=coverage(complete=flag))

    assert result.accepted is False
    assert result.reason_code == exporter.CANDIDATE_COVERAGE_INVALID


def test_retained_in_interval_event_absent_from_the_inventory_refuses():
    third = synthetic_event(
        event_id="0xsynthetic0003",
        effective_ts=datetime(2026, 9, 11, 12, 45, tzinfo=UTC),
    )
    result = build(
        retained_rows=[
            retained_row(EVENT_A),
            retained_row(EVENT_B),
            retained_row(third),
        ]
    )

    assert result.accepted is False
    assert result.reason_code == exporter.CANDIDATE_INVENTORY_MISMATCH
    assert result.report["inventory_missing_event_ids"] == ["0xsynthetic0003"]


def test_binding_for_an_event_outside_the_inventory_refuses():
    result = build(
        approved_event_bindings=[
            binding(funding_event_id=ID_A, event_timestamp=TS_A),
            binding(funding_event_id=ID_B, event_timestamp=TS_B),
            binding(
                funding_event_id="0xsynthetic0007", event_timestamp="2026-09-11T12:15:00Z"
            ),
        ]
    )

    assert result.accepted is False
    assert result.reason_code == exporter.CANDIDATE_BINDING_UNKNOWN_EVENT
    assert result.report["unknown_binding_event_ids"] == ["0xsynthetic0007"]


def test_inventoried_event_without_a_binding_refuses():
    result = build(
        approved_event_bindings=[binding(funding_event_id=ID_A, event_timestamp=TS_A)]
    )

    assert result.accepted is False
    assert result.reason_code == exporter.CANDIDATE_EVENT_UNBOUND
    assert result.report["unbound_events"] == [ID_B]


def test_binding_timestamp_outside_the_interval_refuses():
    result = build(
        approved_event_bindings=[
            binding(funding_event_id=ID_A, event_timestamp=TS_A),
            binding(funding_event_id=ID_B, event_timestamp="2026-09-11T13:00:00Z"),
        ]
    )

    assert result.accepted is False
    assert result.reason_code == exporter.CANDIDATE_BINDING_OUT_OF_INTERVAL
    assert result.report["out_of_interval_bindings"] == [ID_B]


def test_interval_start_is_inclusive_and_end_is_exclusive():
    at_start = build(
        approved_event_bindings=[
            binding(funding_event_id=ID_A, event_timestamp=START),
            binding(funding_event_id=ID_B, event_timestamp=TS_B),
        ]
    )
    assert at_start.accepted is True, at_start.report

    at_end = build(
        approved_event_bindings=[
            binding(funding_event_id=ID_A, event_timestamp=TS_A),
            binding(funding_event_id=ID_B, event_timestamp=END),
        ]
    )
    assert at_end.accepted is False
    assert at_end.reason_code == exporter.CANDIDATE_BINDING_OUT_OF_INTERVAL


def test_coverage_interval_must_equal_the_requested_interval():
    result = build(coverage=coverage(end="2026-09-11T14:00:00Z"))

    assert result.accepted is False
    assert result.reason_code == exporter.CANDIDATE_COVERAGE_INVALID


@pytest.mark.parametrize(
    "start,end",
    [
        (END, START),
        (START, START),
        ("2026-09-11T12:00:00", END),
        (12, END),
    ],
)
def test_invalid_intervals_are_refused(start, end):
    result = build(
        start_inclusive=start,
        end_exclusive=end,
        coverage=coverage(start=str(start), end=str(end)),
    )

    assert result.accepted is False
    assert result.reason_code in {
        exporter.CANDIDATE_INTERVAL_INVALID,
        exporter.CANDIDATE_TIMESTAMP_INVALID,
    }


def test_symbol_outside_the_witness_scope_is_refused():
    other = synthetic_event(
        event_id=ID_A, effective_ts=datetime(2026, 9, 11, 12, 0, 0, 31527, tzinfo=UTC)
    )
    row = retained_row(other)
    row["symbol"] = "ETH"
    result = build(retained_rows=[row, retained_row(EVENT_B)])

    assert result.accepted is False
    assert result.reason_code == exporter.CANDIDATE_SYMBOL_MISMATCH


def test_empty_interval_succeeds_only_with_a_complete_witness():
    proved = build(
        retained_rows=[],
        approved_event_bindings=[],
        coverage=coverage(expected_event_ids=[]),
    )
    assert proved.accepted is True, proved.report
    assert json.loads(proved.candidate_bytes)["synthetic_candidate"]["event_count"] == 0

    unproved = build(
        retained_rows=[retained_row(EVENT_A)],
        approved_event_bindings=[],
        coverage=coverage(expected_event_ids=[]),
    )
    assert unproved.accepted is False
    assert unproved.reason_code == exporter.CANDIDATE_INVENTORY_MISMATCH


# ---------------------------------------------------------------------------
# Production mode stays unavailable — no flag, callback or literal unlocks it
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "kind",
    ["PRODUCTION", "VERIFIED", "OWNER_APPROVED", "true", "APPROVED_BY_LEAD", ""],
)
def test_no_literal_evidence_kind_unlocks_production(kind):
    result = build(coverage=coverage(evidence_kind=kind))

    assert result.accepted is False
    assert result.reason_code == exporter.CANDIDATE_PRODUCTION_EVIDENCE_UNAVAILABLE
    assert result.report["production_mode"] == exporter.PRODUCTION_MODE_UNAVAILABLE


def test_the_module_exposes_no_production_switch():
    forbidden = {"allow_production", "production_enabled", "approve", "force"}
    assert forbidden.isdisjoint(dir(exporter))
    assert exporter.ACCEPTED_EVIDENCE_KINDS == (exporter.SYNTHETIC_EVIDENCE_KIND,)


# ---------------------------------------------------------------------------
# Independent input validation of the pure function
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("mutate", ["extra_key", "missing_key", "wrong_type", "not_a_map"])
def test_retained_rows_are_validated_independently(mutate):
    row = retained_row(EVENT_A)
    if mutate == "extra_key":
        row["recorded_ts"] = "2026-09-11T12:00:00Z"
    elif mutate == "missing_key":
        del row["attribution"]
    elif mutate == "wrong_type":
        row["payload_digest"] = 1234
    else:
        row = [EVENT_A.event_id]
    result = build(retained_rows=[row, retained_row(EVENT_B)])

    assert result.accepted is False
    assert result.reason_code == exporter.CANDIDATE_INPUT_INVALID


@pytest.mark.parametrize("value", [None, "rows", 42, {"event_id": ID_A}])
def test_non_sequence_inputs_are_refused(value):
    assert build(retained_rows=value).reason_code == exporter.CANDIDATE_INPUT_INVALID
    assert (
        build(approved_event_bindings=value).reason_code
        == exporter.CANDIDATE_INPUT_INVALID
    )


@pytest.mark.parametrize("value", [None, "", 7, {"complete": True}])
def test_invalid_coverage_shapes_are_refused(value):
    result = build(coverage=value)

    assert result.accepted is False
    assert result.reason_code == exporter.CANDIDATE_COVERAGE_INVALID


@pytest.mark.parametrize("value", [None, "", 7])
def test_invalid_schedule_ids_are_refused(value):
    result = build(schedule_id=value)

    assert result.accepted is False
    assert result.reason_code == exporter.CANDIDATE_INPUT_INVALID


def test_the_pure_function_touches_no_filesystem_or_database(monkeypatch, tmp_path):
    def forbidden(*args, **kwargs):  # pragma: no cover - must never run
        raise AssertionError("the pure function must not open anything")

    monkeypatch.setattr(exporter.sqlite3, "connect", forbidden)
    monkeypatch.setattr(Path, "write_bytes", forbidden)
    monkeypatch.setattr(Path, "open", forbidden)

    assert build().accepted is True


# ---------------------------------------------------------------------------
# CLI: caller-visible path over a quiescent offline snapshot
# ---------------------------------------------------------------------------


def test_cli_stages_three_deterministic_outputs(tmp_path, snapshot):
    before = sha256_file(snapshot)
    staging = tmp_path / "staging"

    code = run_cli(tmp_path, snapshot=snapshot, staging=staging)

    assert code == 0
    candidate = staging / exporter.CANDIDATE_FILENAME
    sidecar = staging / exporter.SIDECAR_FILENAME
    report = staging / exporter.REPORT_FILENAME
    assert sorted(child.name for child in staging.iterdir()) == sorted(
        [exporter.CANDIDATE_FILENAME, exporter.SIDECAR_FILENAME, exporter.REPORT_FILENAME]
    )
    expected = build()
    assert candidate.read_bytes() == expected.candidate_bytes
    assert sidecar.read_bytes() == (
        expected.candidate_sha256.encode("ascii") + b"\n"
    )
    assert sha256_file(candidate) == expected.candidate_sha256
    staged_report = json.loads(report.read_bytes())
    assert staged_report["accepted"] is True
    assert staged_report["candidate_sha256"] == expected.candidate_sha256

    # The snapshot is untouched and no WAL/SHM/journal companion appeared.
    assert sha256_file(snapshot) == before
    assert sidecar_files(snapshot) == []


def test_the_documented_command_line_works_as_written(tmp_path, snapshot):
    """The caller-visible invocation from the tool's own docstring."""
    staging = tmp_path / "staging"
    bindings = tmp_path / "bindings.json"
    bindings.write_bytes(packet_bytes())
    root = Path(__file__).resolve().parents[1]

    completed = subprocess.run(
        [
            sys.executable,
            str(root / "tools" / "export_mtc_funding.py"),
            "--snapshot", str(snapshot),
            "--bindings", str(bindings),
            "--symbol", SYMBOL,
            "--start", START,
            "--end", END,
            "--schedule-id", SCHEDULE_ID,
            "--staging", str(staging),
        ],
        capture_output=True,
        cwd=str(tmp_path),
        env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"),
        text=True,
        timeout=120,
    )

    assert completed.returncode == 0, completed.stderr
    assert "SYNTHETIC_ONLY" in completed.stdout
    assert "not an accepted economic record" in completed.stdout
    expected = build()
    assert (staging / exporter.CANDIDATE_FILENAME).read_bytes() == expected.candidate_bytes
    assert expected.candidate_sha256 in completed.stdout


def test_cli_output_is_byte_identical_across_runs(tmp_path, snapshot):
    first = tmp_path / "one"
    second = tmp_path / "two"

    assert run_cli(tmp_path, snapshot=snapshot, staging=first) == 0
    assert run_cli(tmp_path, snapshot=snapshot, staging=second) == 0

    for name in (
        exporter.CANDIDATE_FILENAME,
        exporter.SIDECAR_FILENAME,
        exporter.REPORT_FILENAME,
    ):
        assert (first / name).read_bytes() == (second / name).read_bytes()


def test_cli_never_calls_store_initialize(tmp_path, snapshot, monkeypatch):
    def boom(*args, **kwargs):  # pragma: no cover - must never run
        raise AssertionError("the exporter must never initialize or migrate")

    monkeypatch.setattr(Store, "initialize", boom)
    monkeypatch.setattr(Store, "__init__", boom)

    assert run_cli(tmp_path, snapshot=snapshot, staging=tmp_path / "staging") == 0


def test_cli_refuses_a_schema4_snapshot_without_migrating_it(tmp_path):
    snap = write_snapshot(
        tmp_path / "offline" / "v4.db", schema_version=SCHEMA_VERSION_BASELINE
    )
    before = sha256_file(snap)
    staging = tmp_path / "staging"

    code = run_cli(tmp_path, snapshot=snap, staging=staging)

    assert code != 0
    report = json.loads((staging / exporter.REPORT_FILENAME).read_bytes())
    assert report["reason_code"] == "FUNDING_PAYLOAD_SCHEMA_INACTIVE"
    assert not (staging / exporter.CANDIDATE_FILENAME).exists()
    assert not (staging / exporter.SIDECAR_FILENAME).exists()
    assert sha256_file(snap) == before
    assert sidecar_files(snap) == []
    reopened = Store(snap)
    try:
        assert reopened.get_meta("schema_version") == str(SCHEMA_VERSION_BASELINE)
    finally:
        reopened.close()


def test_cli_refuses_a_non_quiescent_snapshot_and_writes_nothing(tmp_path, snapshot):
    (snapshot.parent / (snapshot.name + "-wal")).write_bytes(b"")
    staging = tmp_path / "staging"

    code = run_cli(tmp_path, snapshot=snapshot, staging=staging)

    assert code != 0
    report = json.loads((staging / exporter.REPORT_FILENAME).read_bytes())
    assert report["reason_code"] == exporter.CANDIDATE_SNAPSHOT_NOT_QUIESCENT
    assert sorted(child.name for child in staging.iterdir()) == [
        exporter.REPORT_FILENAME
    ]


@pytest.mark.parametrize("suffix", ["-wal", "-shm", "-journal"])
def test_cli_refuses_a_companion_created_while_reading(
    tmp_path, snapshot, monkeypatch, suffix
):
    before = snapshot.read_bytes()
    companion = snapshot.with_name(snapshot.name + suffix)
    original = exporter._read_snapshot_rows

    def read_then_create_companion(*args, **kwargs):
        rows = original(*args, **kwargs)
        companion.write_bytes(b"arrived while reading")
        return rows

    monkeypatch.setattr(exporter, "_read_snapshot_rows", read_then_create_companion)
    staging = tmp_path / "staging"

    code = run_cli(tmp_path, snapshot=snapshot, staging=staging)

    assert code != 0
    report = json.loads((staging / exporter.REPORT_FILENAME).read_bytes())
    assert report["reason_code"] == exporter.CANDIDATE_SNAPSHOT_NOT_QUIESCENT
    assert not (staging / exporter.CANDIDATE_FILENAME).exists()
    assert not (staging / exporter.SIDECAR_FILENAME).exists()
    assert snapshot.read_bytes() == before
    assert companion.read_bytes() == b"arrived while reading"


def test_cli_refuses_a_missing_snapshot(tmp_path):
    staging = tmp_path / "staging"

    code = run_cli(tmp_path, snapshot=tmp_path / "nothing.db", staging=staging)

    assert code != 0
    assert not (tmp_path / "nothing.db").exists()
    report = json.loads((staging / exporter.REPORT_FILENAME).read_bytes())
    assert report["reason_code"] == exporter.CANDIDATE_SNAPSHOT_UNAVAILABLE


@pytest.mark.parametrize("existing_name", ["funding_candidate_synthetic.json", "notes.txt"])
def test_cli_refuses_a_non_empty_staging_directory_without_overwriting(
    tmp_path, snapshot, capsys, existing_name
):
    staging = tmp_path / "staging"
    staging.mkdir()
    existing = staging / existing_name
    existing.write_bytes(b"PRIOR ARTIFACT\n")

    code = run_cli(tmp_path, snapshot=snapshot, staging=staging)

    assert code != 0
    # The directory must be refused as a whole, not merely protected file by
    # file: an unrelated occupant blocks staging just as an artifact name does.
    assert exporter.CANDIDATE_STAGING_NOT_EMPTY in capsys.readouterr().err
    assert existing.read_bytes() == b"PRIOR ARTIFACT\n"
    assert sorted(child.name for child in staging.iterdir()) == [existing_name]


def test_cli_refusal_stages_a_report_but_no_candidate(tmp_path, snapshot):
    staging = tmp_path / "staging"
    packet = packet_bytes(
        bindings=[binding(funding_event_id=ID_A, event_timestamp=TS_A)]
    )

    code = run_cli(tmp_path, snapshot=snapshot, staging=staging, packet=packet)

    assert code != 0
    report = json.loads((staging / exporter.REPORT_FILENAME).read_bytes())
    assert report["accepted"] is False
    assert report["reason_code"] == exporter.CANDIDATE_EVENT_UNBOUND
    assert sorted(child.name for child in staging.iterdir()) == [
        exporter.REPORT_FILENAME
    ]


def test_cli_refuses_a_symbol_outside_the_witness_scope(tmp_path, snapshot):
    staging = tmp_path / "staging"

    code = run_cli(tmp_path, snapshot=snapshot, staging=staging, symbol="ETH")

    assert code != 0
    report = json.loads((staging / exporter.REPORT_FILENAME).read_bytes())
    assert report["reason_code"] == exporter.CANDIDATE_SYMBOL_MISMATCH


@pytest.mark.parametrize(
    "packet",
    [
        b"{not json",
        b"[]",
        json.dumps({"packet_version": "OTHER", "coverage": {}, "bindings": []}).encode(),
        json.dumps({"coverage": {}, "bindings": []}).encode(),
    ],
)
def test_cli_refuses_a_malformed_binding_packet(tmp_path, snapshot, packet):
    staging = tmp_path / "staging"

    code = run_cli(tmp_path, snapshot=snapshot, staging=staging, packet=packet)

    assert code != 0
    report = json.loads((staging / exporter.REPORT_FILENAME).read_bytes())
    assert report["reason_code"] == exporter.CANDIDATE_PACKET_INVALID


@pytest.mark.parametrize(
    ("old", "new"),
    [
        (
            b'{"bindings":',
            b'{"packet_version":"OTHER","bindings":',
        ),
        (
            b'"complete": true',
            b'"complete": false, "complete": true',
        ),
        (
            b'"raw_rate": "0.0000125"',
            b'"raw_rate": "invalid", "raw_rate": "0.0000125"',
        ),
        (
            b'"source_title": "SYNTHETIC-D1-FIXTURE"',
            b'"source_title": "OTHER", "source_title": "SYNTHETIC-D1-FIXTURE"',
        ),
    ],
    ids=["packet", "coverage", "binding", "provenance"],
)
def test_cli_rejects_duplicate_json_members_at_every_object_depth(
    tmp_path, snapshot, old, new
):
    packet = packet_bytes()
    duplicate_packet = packet.replace(old, new, 1)
    assert duplicate_packet != packet
    staging = tmp_path / "staging"

    code = run_cli(
        tmp_path, snapshot=snapshot, staging=staging, packet=duplicate_packet
    )

    assert code != 0
    report = json.loads((staging / exporter.REPORT_FILENAME).read_bytes())
    assert report["reason_code"] == exporter.CANDIDATE_PACKET_INVALID
    assert not (staging / exporter.CANDIDATE_FILENAME).exists()


@pytest.mark.parametrize("constant", [b"NaN", b"Infinity", b"-Infinity"])
def test_cli_rejects_nonfinite_source_witness_json_with_a_report(
    tmp_path, snapshot, constant
):
    bindings = [
        binding(funding_event_id=ID_A, event_timestamp=TS_A),
        binding(funding_event_id=ID_B, event_timestamp=TS_B),
    ]
    source = synthetic_source_bytes(bindings[0]).replace(
        b'"raw_rate":"0.0000125"', b'"raw_rate":' + constant
    )
    digest = hashlib.sha256(source).hexdigest()
    bindings[0]["provenance"]["source_sha256"] = digest
    bindings[0]["source_event_digest"] = digest
    cover = coverage()
    cover["source_witnesses"] = source_witnesses(bindings)
    cover["source_witnesses"][ID_A] = source.hex()
    packet = json.dumps({
        "bindings": bindings,
        "coverage": cover,
        "packet_version": exporter.PACKET_VERSION,
    }).encode("utf-8")
    staging = tmp_path / "staging"

    code = None
    escaped = None
    try:
        code = run_cli(tmp_path, snapshot=snapshot, staging=staging, packet=packet)
    except (TypeError, ValueError) as exc:
        escaped = exc

    assert escaped is None
    assert code != 0
    report = json.loads((staging / exporter.REPORT_FILENAME).read_bytes())
    assert report["reason_code"] == exporter.CANDIDATE_BINDING_INVALID
    assert not (staging / exporter.CANDIDATE_FILENAME).exists()


def test_cli_leaves_no_partial_artifact_when_a_write_fails(tmp_path, snapshot):
    staging = tmp_path / "staging"
    real_write = exporter._write_new_file
    calls: list[Path] = []

    def failing(path: Path, data: bytes) -> None:
        calls.append(path)
        if len(calls) == 3:
            raise OSError("synthetic staging failure")
        real_write(path, data)

    exporter._write_new_file = failing
    try:
        code = run_cli(tmp_path, snapshot=snapshot, staging=staging)
    finally:
        exporter._write_new_file = real_write

    assert code != 0
    assert not staging.exists()
    assert list(tmp_path.glob(".staging.*")) == []


def test_cli_refuses_a_drifting_snapshot(tmp_path, snapshot, monkeypatch):
    staging = tmp_path / "staging"
    real_read = exporter._read_snapshot_rows

    def drift(*args, **kwargs):
        rows = real_read(*args, **kwargs)
        with open(snapshot, "ab") as handle:
            handle.write(b"\x00" * 4096)
        return rows

    monkeypatch.setattr(exporter, "_read_snapshot_rows", drift)

    code = run_cli(tmp_path, snapshot=snapshot, staging=staging)

    assert code != 0
    report = json.loads((staging / exporter.REPORT_FILENAME).read_bytes())
    assert report["reason_code"] == exporter.CANDIDATE_SNAPSHOT_DRIFTED
    assert not (staging / exporter.CANDIDATE_FILENAME).exists()


# ---------------------------------------------------------------------------
# D1 bounded repair regressions
# ---------------------------------------------------------------------------


def test_valid_synthetic_source_byte_witness_is_accepted():
    result = build()

    assert result.accepted is True, result.report


def test_missing_synthetic_source_bytes_refuses_detached_digest_references():
    result = build(source_witnesses={})

    assert result.accepted is False
    assert "source bytes" in result.report["reason_detail"]


def test_tampered_synthetic_source_bytes_refuse():
    first = binding(funding_event_id=ID_A, event_timestamp=TS_A)
    second = binding(funding_event_id=ID_B, event_timestamp=TS_B)
    witnesses = source_witnesses([first, second])
    witnesses[ID_A] = witnesses[ID_A][:-2] + "00"
    result = build(approved_event_bindings=[
        first,
        second,
    ], source_witnesses=witnesses)

    assert result.accepted is False
    assert "source_sha256 does not hash" in result.report["reason_detail"]


def test_swapped_source_witness_cannot_launder_a_detached_binding():
    first = binding(funding_event_id=ID_A, event_timestamp=TS_A)
    second = binding(funding_event_id=ID_B, event_timestamp=TS_B)
    witnesses = source_witnesses([first, second])
    witnesses[ID_A] = witnesses[ID_B]
    first["provenance"]["source_sha256"] = second["provenance"]["source_sha256"]
    first["source_event_digest"] = second["source_event_digest"]
    result = build(
        approved_event_bindings=[first, second], source_witnesses=witnesses
    )

    assert result.accepted is False
    assert "does not describe this binding" in result.report["reason_detail"]


def test_source_event_digest_must_hash_the_explicit_source_bytes():
    first = binding(funding_event_id=ID_A, event_timestamp=TS_A)
    first["source_event_digest"] = "0" * 64
    result = build(approved_event_bindings=[
        first,
        binding(funding_event_id=ID_B, event_timestamp=TS_B),
    ])

    assert result.accepted is False
    assert "source_event_digest does not hash" in result.report["reason_detail"]


def test_unbound_unavailable_row_refuses_regardless_of_ledger_clock():
    outside = synthetic_event(
        event_id="0xsynthetic-unbound-old",
        effective_ts=datetime(2020, 1, 1, tzinfo=UTC),
    )
    result = build(retained_rows=[
        retained_row(EVENT_A),
        retained_row(EVENT_B),
        retained_row(outside, payload=None),
    ])

    assert result.accepted is False
    assert result.candidate_bytes is None
    assert result.reason_code == exporter.CANDIDATE_INVENTORY_MISMATCH
    assert result.report["inventory_missing_event_ids"] == [outside.event_id]


class _WriteThenFail:
    def __init__(self, handle, *, fail_on_close: bool = False):
        self.handle = handle
        self.fail_on_close = fail_on_close

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, traceback):
        self.close()

    def __getattr__(self, name):
        return getattr(self.handle, name)

    def write(self, data):
        if self.fail_on_close:
            return self.handle.write(data)
        self.handle.write(data[:7])
        self.handle.flush()
        raise OSError("synthetic partial write")

    def close(self):
        self.handle.close()
        if self.fail_on_close:
            raise OSError("synthetic close failure")


@pytest.mark.parametrize("fail_on_close", [False, True], ids=["partial-write", "close"])
def test_cli_never_publishes_after_write_or_close_failure(
    tmp_path, snapshot, monkeypatch, fail_on_close
):
    staging = tmp_path / "staging"
    real_open = open

    def failing_open(path, mode="r", *args, **kwargs):
        handle = real_open(path, mode, *args, **kwargs)
        if mode == "xb" and Path(path).name == exporter.CANDIDATE_FILENAME:
            return _WriteThenFail(handle, fail_on_close=fail_on_close)
        return handle

    monkeypatch.setattr(exporter, "open", failing_open, raising=False)

    assert run_cli(tmp_path, snapshot=snapshot, staging=staging) != 0
    assert not staging.exists()
    assert list(tmp_path.glob(".staging.*")) == []


def test_cli_reports_unpublished_scratch_when_cleanup_fails(
    tmp_path, snapshot, monkeypatch, capsys
):
    staging = tmp_path / "staging"
    real_write = exporter._write_new_file
    real_unlink = Path.unlink
    calls = 0

    def failing_later(path: Path, data: bytes):
        nonlocal calls
        calls += 1
        if calls == 2:
            raise OSError("synthetic later failure")
        return real_write(path, data)

    def failing_cleanup(path: Path, *args, **kwargs):
        if path.name == exporter.CANDIDATE_FILENAME:
            raise OSError("synthetic cleanup failure")
        return real_unlink(path, *args, **kwargs)

    monkeypatch.setattr(exporter, "_write_new_file", failing_later)
    monkeypatch.setattr(Path, "unlink", failing_cleanup)

    assert run_cli(tmp_path, snapshot=snapshot, staging=staging) != 0
    assert not staging.exists()
    scratch = list(tmp_path.glob(".staging.*"))
    assert len(scratch) == 1
    assert [child.name for child in scratch[0].iterdir()] == [
        exporter.CANDIDATE_FILENAME
    ]
    error = capsys.readouterr().err
    assert "cleanup incomplete" in error
    assert exporter.CANDIDATE_FILENAME in error


def test_publication_race_preserves_foreign_target_and_publishes_nothing(
    tmp_path, snapshot, monkeypatch
):
    staging = tmp_path / "staging"
    foreign = staging / "foreign.txt"
    real_write = exporter._write_new_file
    raced = False

    def race_before_publication(path: Path, data: bytes):
        nonlocal raced
        if not raced:
            raced = True
            staging.mkdir()
            foreign.write_bytes(b"FOREIGN\n")
        return real_write(path, data)

    monkeypatch.setattr(exporter, "_write_new_file", race_before_publication)

    assert run_cli(tmp_path, snapshot=snapshot, staging=staging) != 0
    assert foreign.read_bytes() == b"FOREIGN\n"
    assert [child.name for child in staging.iterdir()] == ["foreign.txt"]


def test_existing_empty_staging_directory_is_explicitly_refused(
    tmp_path, snapshot, capsys
):
    staging = tmp_path / "staging"
    staging.mkdir()

    assert run_cli(tmp_path, snapshot=snapshot, staging=staging) != 0
    assert list(staging.iterdir()) == []
    assert exporter.CANDIDATE_STAGING_NOT_EMPTY in capsys.readouterr().err


def test_staging_inside_repository_is_refused_before_writes(
    tmp_path, snapshot, monkeypatch, capsys
):
    repository = tmp_path / "repository"
    bridge = repository / "IBKR_PAPER_BRIDGE"
    bridge.mkdir(parents=True)
    (repository / ".git").write_text("gitdir: synthetic-worktree\n")
    mtc = repository / "MTC_COMMAND_CENTER"
    mtc.mkdir()
    staging = mtc / "staging"
    monkeypatch.setattr(exporter, "ROOT", bridge)

    assert run_cli(tmp_path, snapshot=snapshot, staging=staging) != 0
    assert not staging.exists()
    assert "CANDIDATE_STAGING_UNSAFE" in capsys.readouterr().err


def test_prepare_staging_refuses_the_current_owned_mtc_production_parent():
    repository = Path(__file__).resolve().parents[2]
    funding = (
        repository
        / "MTC_COMMAND_CENTER"
        / "01_MTC_PROJECT"
        / "00_PYTHON"
        / "mtc_v2"
        / "core"
        / "economic_records"
        / "funding"
    )
    target = funding / "__P012_PREFLIGHT_ONLY_NEVER_CREATE"
    assert funding.is_dir()
    assert not target.exists()

    with pytest.raises(exporter._Refusal) as refused:
        exporter._prepare_staging(target, Path(__file__), Path(exporter.__file__))

    assert refused.value.code == exporter.CANDIDATE_STAGING_UNSAFE
    assert not target.exists()


@pytest.mark.parametrize("ancestor_kind", ["git-directory", "git-file", "mtc-tree"])
def test_staging_under_foreign_repository_or_mtc_tree_is_refused(
    tmp_path, snapshot, capsys, ancestor_kind
):
    if ancestor_kind == "mtc-tree":
        foreign = tmp_path / "outside" / "MTC_COMMAND_CENTER"
    else:
        foreign = tmp_path / ancestor_kind
    foreign.mkdir(parents=True)
    if ancestor_kind == "git-directory":
        (foreign / ".git").mkdir()
    elif ancestor_kind == "git-file":
        (foreign / ".git").write_text("gitdir: synthetic-worktree\n")
    parent = foreign / "nested"
    parent.mkdir()
    staging = parent / "staging"

    assert run_cli(tmp_path, snapshot=snapshot, staging=staging) != 0
    assert not staging.exists()
    assert exporter.CANDIDATE_STAGING_UNSAFE in capsys.readouterr().err


def test_external_non_repository_staging_remains_allowed(tmp_path, snapshot):
    parent = tmp_path / "ordinary-external-parent"
    parent.mkdir()
    staging = parent / "staging"

    assert run_cli(tmp_path, snapshot=snapshot, staging=staging) == 0
    assert (staging / exporter.CANDIDATE_FILENAME).is_file()


def test_staging_symlink_ancestry_is_resolved_before_scope_check(
    tmp_path, snapshot, monkeypatch, capsys
):
    repository = tmp_path / "repository"
    bridge = repository / "IBKR_PAPER_BRIDGE"
    bridge.mkdir(parents=True)
    alias = tmp_path / "external-looking-alias"
    try:
        alias.symlink_to(bridge, target_is_directory=True)
    except OSError as exc:
        pytest.skip(f"directory symlink unavailable: {exc}")
    staging = alias / "staging"
    monkeypatch.setattr(exporter, "ROOT", bridge)

    assert run_cli(tmp_path, snapshot=snapshot, staging=staging) != 0
    assert not (bridge / "staging").exists()
    assert "CANDIDATE_STAGING_UNSAFE" in capsys.readouterr().err


@pytest.mark.parametrize("input_kind", ["snapshot", "bindings"])
def test_staging_cannot_overlap_an_input_path(
    tmp_path, snapshot, capsys, input_kind
):
    bindings = tmp_path / "packet" / "bindings.json"
    bindings.parent.mkdir()
    bindings.write_bytes(packet_bytes())
    staging = snapshot.parent if input_kind == "snapshot" else bindings.parent

    code = run_cli(
        tmp_path,
        snapshot=snapshot,
        staging=staging,
        bindings_path=bindings,
    )

    assert code != 0
    error = capsys.readouterr().err
    assert "CANDIDATE_STAGING_UNSAFE" in error
    assert "overlaps" in error


# ---------------------------------------------------------------------------
# Physical non-admission by the current production loader
# ---------------------------------------------------------------------------


def _mtc_python_root() -> Path | None:
    root = Path(__file__).resolve().parents[2]
    candidate = root / "MTC_COMMAND_CENTER" / "01_MTC_PROJECT" / "00_PYTHON"
    return candidate if (candidate / "mtc_v2").is_dir() else None


NON_ADMISSION_PROBE = r"""
import json, sys
from pathlib import Path
from mtc_v2.core.instrument import load_verified_json_record
from mtc_v2.core.economics import EconomicRecords, EconomicsRefusal

record = load_verified_json_record(Path(sys.argv[1]))
data = record.data
verdict = {
    "loaded": True,
    "has_schedule_id": "schedule_id" in data,
    "has_events": "events" in data,
    "has_settlement_currency": "settlement_currency" in data,
    "selection_events": data.get("events"),
}
try:
    EconomicRecords(
        instrument=None, cost=None, cost_digest=None,
        funding=data, funding_digest=record.digest,
    ).funding_schedule_id
    verdict["schedule_id_readable"] = True
except Exception as exc:
    verdict["schedule_id_readable"] = False
    verdict["schedule_id_error"] = type(exc).__name__
print(json.dumps(verdict))
"""


def test_current_production_loader_cannot_admit_the_candidate(tmp_path, snapshot):
    mtc_root = _mtc_python_root()
    if mtc_root is None:
        pytest.skip("MTC record loader is not present in this worktree")

    staging = tmp_path / "staging"
    assert run_cli(tmp_path, snapshot=snapshot, staging=staging) == 0

    # Present the candidate to the loader under the exact name/detached-digest
    # convention a production record would use. Loading bytes is not admission.
    posed = tmp_path / "posed"
    posed.mkdir()
    record_path = posed / f"{SCHEDULE_ID}.json"
    record_path.write_bytes((staging / exporter.CANDIDATE_FILENAME).read_bytes())
    (posed / f"{SCHEDULE_ID}.json.sha256").write_bytes(
        sha256_file(record_path).encode("ascii") + b"\n"
    )

    env = dict(os.environ, PYTHONPATH=str(mtc_root), PYTHONDONTWRITEBYTECODE="1")
    completed = subprocess.run(
        [sys.executable, "-c", NON_ADMISSION_PROBE, str(record_path)],
        capture_output=True,
        cwd=str(mtc_root),
        env=env,
        text=True,
        timeout=120,
    )
    assert completed.returncode == 0, completed.stderr
    verdict = json.loads(completed.stdout)

    assert verdict["loaded"] is True
    assert verdict["has_schedule_id"] is False
    assert verdict["has_events"] is False
    assert verdict["has_settlement_currency"] is False
    assert verdict["selection_events"] is None
    assert verdict["schedule_id_readable"] is False
