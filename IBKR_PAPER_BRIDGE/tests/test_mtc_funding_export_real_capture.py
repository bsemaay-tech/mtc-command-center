"""P0-12 funding materializer — the REAL_CAPTURE_READ_ONLY evidence profile (D-1..D-6).

Authority: ``OD-20260916-P012-INTAKE-D1-D6-R-1``. The six intake rules are enforced by
``export_mtc_funding.py`` only when the caller explicitly declares the real profile; the
default profile stays ``SYNTHETIC_FIXTURE`` and its carried fences live untouched in
``test_mtc_funding_export.py``.

Fixture material
----------------
``FUNDING_PASS`` is the exact 433-byte Hyperliquid ``userFunding`` response of the Path-1
read-only capture r1 (``p012-path1-20260914T1500Z-1900Z-r1``): two BTC funding rows stamped
41 ms and 60 ms past the hour, the venue's zero hash, no account address. ``FILLS`` is
venue-shaped ``userFillsByTime`` JSON carrying r1's real sizes, sides, prices, times and
``startPosition`` values with synthetic transaction hashes. The retained rows are FIXTURES:
no Bridge store has observed these events (the deployed store is schema v4), so they are
what a schema-v10 store would have to carry, built here from the captured values and
labelled as such. The oracle capture is a FIXTURE locator: r1 captured no oracle read, which
is exactly why the un-patched r1 packet must refuse under D-4.

Nothing here admits production: every accepted candidate is labelled
``REFUSED_REAL_CAPTURE_READ_ONLY_NOT_A_PRODUCTION_RECORD`` and carries no MTC selection key.
"""

from __future__ import annotations

import hashlib
import json
import re
from datetime import UTC, datetime
from pathlib import Path

import pytest

from bridge.engine.types import (
    FundingAttribution,
    FundingEventRecord,
    ReconcileAttemptState,
)
from bridge.store.db import SCHEMA_VERSION_FUNDING_PAYLOAD, Store
from tools import export_mtc_funding as exporter

REAL = "REAL_CAPTURE_READ_ONLY"
SYMBOL = "BTC"
SCHEDULE_ID = "REAL-P012-INTAKE-S4-TEST"
START = "2026-09-14T15:00:00Z"
END = "2026-09-14T19:00:00Z"
SCOPE = "0x1234…5678"  # short-form account scope, synthetic
RUN_ID = "p012-path1-20260914T1500Z-1900Z-r1"
MANIFEST_SHA = hashlib.sha256(b"fixture-capture-manifest").hexdigest()
ORACLE_SHA = hashlib.sha256(b"fixture-oracle-capture").hexdigest()
ORACLE_LOCATOR = f"{ORACLE_SHA}#/1/0/oraclePx"
FUNDING_FILE = "funding_pass1_page001.json"
FILLS_FILE = "fills_pass1_page001.json"
RECORDED = datetime(2026, 9, 14, 19, 5, tzinfo=UTC)

# The exact captured bytes (r1, pass 1 == pass 2).
FUNDING_PASS = (
    b'[{"time":1789405200041,"hash":"0x'
    + b"0" * 64
    + b'","delta":{"type":"funding","coin":"BTC","usdc":"-0.000571","szi":"0.00058",'
    b'"fundingRate":"0.0000125","nSamples":null}},{"time":1789408800060,"hash":"0x'
    + b"0"
    * 64
    + b'","delta":{"type":"funding","coin":"BTC","usdc":"-0.000572","szi":"0.00058",'
    b'"fundingRate":"0.0000125","nSamples":null}}]'
)
FUNDING_SHA = hashlib.sha256(FUNDING_PASS).hexdigest()
T1_MS, T2_MS = 1789405200041, 1789408800060
TS1, TS2 = "2026-09-14T17:00:00.041Z", "2026-09-14T18:00:00.060Z"
HOUR1, HOUR2 = "2026-09-14T17:00:00Z", "2026-09-14T18:00:00Z"
ID1 = f"hl-funding:{SCOPE}:BTC:{T1_MS}"
ID2 = f"hl-funding:{SCOPE}:BTC:{T2_MS}"


def _fill(
    px: str, sz: str, side: str, time_ms: int, start: str, direction: str, seed: int
) -> str:
    tx = "0x" + hashlib.sha256(f"fixture-fill-{seed}".encode()).hexdigest()
    return (
        f'{{"coin":"BTC","px":"{px}","sz":"{sz}","side":"{side}","time":{time_ms},'
        f'"startPosition":"{start}","dir":"{direction}","closedPnl":"0.0","hash":"{tx}",'
        f'"oid":{544824403105 + seed},"crossed":true,"fee":"0.005423","tid":{261929593852405 + seed},'
        f'"feeToken":"USDC","twapId":null}}'
    )


# r1's position: opened 16:03-16:14Z in four fills to 0.00058, closed 18:08:43Z.
FILLS_R1 = [
    _fill("78462.0", "0.00016", "B", 1789401810942, "0.0", "Open Long", 1),
    _fill("78451.0", "0.00013", "B", 1789401915271, "0.00016", "Open Long", 2),
    _fill("78438.0", "0.00013", "B", 1789401971269, "0.00029", "Open Long", 3),
    _fill("78410.0", "0.00016", "B", 1789402474869, "0.00042", "Open Long", 4),
    _fill("78993.0", "0.00058", "A", 1789409323372, "0.00058", "Close Long", 5),
]


def fills_bytes(fills: list[str] | None = None) -> bytes:
    return ("[" + ",".join(FILLS_R1 if fills is None else fills) + "]").encode("utf-8")


def row_spans(pass_bytes: bytes) -> list[bytes]:
    """Exact byte spans of the array elements — the test's own independent parser."""
    text = pass_bytes.decode("utf-8")
    decoder = json.JSONDecoder()
    index = text.index("[") + 1
    spans: list[bytes] = []
    while True:
        while text[index] in " \t\r\n":
            index += 1
        if text[index] == "]":
            return spans
        _, end = decoder.raw_decode(text, index)
        spans.append(text[index:end].encode("utf-8"))
        index = end
        while text[index] in " \t\r\n":
            index += 1
        if text[index] == ",":
            index += 1


ROW1, ROW2 = row_spans(FUNDING_PASS)


def event(event_id: str, stamp: datetime, amount: float) -> FundingEventRecord:
    """FIXTURE retained event: what a schema-v10 store would carry for this row."""
    return FundingEventRecord(
        event_id=event_id,
        symbol=SYMBOL,
        amount_usdc=amount,
        effective_ts=stamp,
        source="HL_USER_FUNDING",
        attribution=FundingAttribution.ATTRIBUTED,
        funding_rate=0.0000125,
        position_szi=0.00058,
        n_samples=None,
    )


EVENT1 = event(ID1, datetime(2026, 9, 14, 17, 0, 0, 41000, tzinfo=UTC), -0.000571)
EVENT2 = event(ID2, datetime(2026, 9, 14, 18, 0, 0, 60000, tzinfo=UTC), -0.000572)


def retained_row(record: FundingEventRecord) -> dict:
    return {
        "attribution": record.attribution.value,
        "event_id": record.event_id,
        "ledger_effective_ts": record.effective_ts.astimezone(UTC).isoformat(),
        "payload": record.authoritative(),
        "payload_digest": record.digest,
        "payload_reason": exporter.PAYLOAD_RETAINED,
        "symbol": record.symbol,
    }


def real_binding(
    *,
    event_id: str,
    stamp: str,
    hour: str,
    row: bytes,
    index: int,
    oracle_price: str = "78758.6",
    oracle_source: str = ORACLE_LOCATOR,
    evidence_kind: str = REAL,
    **overrides,
) -> dict:
    body = {
        "event_timestamp": stamp,
        "funding_event_id": event_id,
        "interval_hour_utc": hour,
        "oracle_price": oracle_price,
        "oracle_price_source": oracle_source,
        "positive_rate_payer": exporter.APPROVED_PAYER,
        "provenance": {
            "evidence_kind": evidence_kind,
            "extraction_method": "capture_own_account_evidence.py tool_sha256=00b3b8f69f0e4870 user_funding_history",
            "source_locator": f"{FUNDING_FILE}#/{index}",
            "source_sha256": FUNDING_SHA,
            "source_title": f"Hyperliquid userFunding {SCOPE} run {RUN_ID}",
        },
        "raw_rate": "0.0000125",
        "source_event_digest": (
            f"{exporter.REAL_SOURCE_EVENT_DIGEST_DOMAIN}:{hashlib.sha256(row).hexdigest()}"
        ),
    }
    body.update(overrides)
    return body


def witness_identity(
    *, ownership: str = "OWNERSHIP_EVIDENCE: VERIFIED", scope: str = SCOPE
) -> str:
    return (
        f"capture_own_account_evidence.py tool_sha256=00b3b8f69f0e4870 run {RUN_ID}; "
        f"manifest_sha256={MANIFEST_SHA}; ownership {ownership} {scope}"
    )


def real_coverage(
    *,
    bindings: list[dict],
    rows: list[bytes] | None = None,
    passes: list[bytes] | None = None,
    fills: bytes | None = None,
    start: str = START,
    end: str = END,
    identity: str | None = None,
    **overrides,
) -> dict:
    row_bytes = [ROW1, ROW2] if rows is None else rows
    body = {
        "account_scope": SCOPE,
        "complete": True,
        "evidence_kind": REAL,
        "expected_event_ids": [item["funding_event_id"] for item in bindings],
        "fills_witness": (fills_bytes() if fills is None else fills).hex(),
        "funding_witness_passes": [
            item.hex()
            for item in ([FUNDING_PASS, FUNDING_PASS] if passes is None else passes)
        ],
        "interval_end_exclusive": end,
        "interval_start_inclusive": start,
        "symbol": SYMBOL,
        "source_witnesses": {
            item["funding_event_id"]: raw.hex()
            for item, raw in zip(bindings, row_bytes)
        },
        "unattributed_event_ids": [],
        "witness_identity": witness_identity() if identity is None else identity,
    }
    body.update(overrides)
    return body


def r1_bindings(**overrides) -> list[dict]:
    return [
        real_binding(
            event_id=ID1, stamp=TS1, hour=HOUR1, row=ROW1, index=0, **overrides
        ),
        real_binding(
            event_id=ID2, stamp=TS2, hour=HOUR2, row=ROW2, index=1, **overrides
        ),
    ]


def build(
    *,
    rows: list[dict] | None = None,
    bindings: list[dict] | None = None,
    cover: dict | None = None,
    start: str = START,
    end: str = END,
    **kwargs,
) -> exporter.CandidateResult:
    selected = r1_bindings() if bindings is None else bindings
    return exporter.build_funding_candidate(
        [retained_row(EVENT1), retained_row(EVENT2)] if rows is None else rows,
        selected,
        real_coverage(bindings=selected) if cover is None else cover,
        SCHEDULE_ID,
        start,
        end,
        **kwargs,
    )


_ANY_TIMESTAMP = re.compile(
    r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})"
)


def _day_prefixes(value) -> set[str]:
    found: set[str] = set()
    if isinstance(value, dict):
        for item in value.values():
            found |= _day_prefixes(item)
    elif isinstance(value, list):
        for item in value:
            found |= _day_prefixes(item)
    elif isinstance(value, str):
        found |= {stamp[:11] for stamp in _ANY_TIMESTAMP.findall(value)}
    return found


# ---------------------------------------------------------------------------
# Explicit admission — a profile the caller names, never a toggle
# ---------------------------------------------------------------------------


def test_the_real_profile_is_never_selected_by_default():
    result = build()  # no evidence_kind declared -> the SYNTHETIC profile

    assert result.accepted is False
    assert result.reason_code == exporter.CANDIDATE_EVIDENCE_KIND_MISMATCH
    assert exporter.ACCEPTED_EVIDENCE_KINDS == (exporter.SYNTHETIC_EVIDENCE_KIND,)
    assert exporter.REAL_CAPTURE_EVIDENCE_KIND not in exporter.ACCEPTED_EVIDENCE_KINDS


def test_a_declared_real_profile_refuses_a_packet_that_does_not_say_so():
    cover = real_coverage(
        bindings=r1_bindings(), evidence_kind=exporter.SYNTHETIC_EVIDENCE_KIND
    )

    result = build(cover=cover, evidence_kind=REAL)

    assert result.accepted is False
    assert result.reason_code == exporter.CANDIDATE_EVIDENCE_KIND_MISMATCH


def test_one_binding_of_another_kind_refuses_the_whole_packet():
    bindings = r1_bindings()
    bindings[1]["provenance"]["evidence_kind"] = exporter.SYNTHETIC_EVIDENCE_KIND

    result = build(
        bindings=bindings, cover=real_coverage(bindings=bindings), evidence_kind=REAL
    )

    assert result.accepted is False
    assert result.reason_code == exporter.CANDIDATE_EVIDENCE_KIND_MISMATCH


@pytest.mark.parametrize(
    "kind", ["PRODUCTION", "VERIFIED", "real_capture_read_only", ""]
)
def test_an_unknown_declared_kind_is_unavailable_not_a_profile(kind):
    result = build(evidence_kind=kind)

    assert result.accepted is False
    assert result.reason_code == exporter.CANDIDATE_PRODUCTION_EVIDENCE_UNAVAILABLE
    assert result.report["production_mode"] == exporter.PRODUCTION_MODE_UNAVAILABLE


def test_the_cli_names_the_profile_explicitly_and_defaults_to_synthetic():
    base = [
        "--snapshot",
        "s",
        "--bindings",
        "b",
        "--symbol",
        SYMBOL,
        "--start",
        START,
        "--end",
        END,
        "--schedule-id",
        SCHEDULE_ID,
        "--staging",
        "x",
    ]

    assert exporter._parse_args(base).evidence_kind == exporter.SYNTHETIC_EVIDENCE_KIND
    assert exporter._parse_args(base + ["--evidence-kind", REAL]).evidence_kind == REAL
    with pytest.raises(SystemExit):
        exporter._parse_args(base + ["--evidence-kind", "PRODUCTION"])
    with pytest.raises(SystemExit):
        exporter._parse_args(base + ["--mode", "PRODUCTION"])


# ---------------------------------------------------------------------------
# D-4 — the r1 capture carries no oracle read, so r1 refuses; a named oracle
# capture is required for a candidate
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("price", "source"),
    [
        ("UNRESOLVED:D-4", "UNRESOLVED:D-4"),
        ("78758.6", "DERIVED_FROM_PAYMENT"),
        ("78758.6", "derived: usdc / (szi * rate)"),
        ("78758.6", "oracle read at the funding instant"),
        ("78758.6", "sha256:" + ORACLE_SHA),
    ],
)
def test_r1_without_a_named_oracle_capture_refuses_under_d4(price, source):
    bindings = r1_bindings(oracle_price=price, oracle_source=source)

    result = build(
        bindings=bindings, cover=real_coverage(bindings=bindings), evidence_kind=REAL
    )

    assert result.accepted is False
    assert result.reason_code == exporter.CANDIDATE_ORACLE_EVIDENCE_UNAVAILABLE
    assert "D-4" in result.report["reason_detail"]


# ---------------------------------------------------------------------------
# The accepted real-capture candidate — labelled, non-admitted, deterministic
# ---------------------------------------------------------------------------


def test_r1_with_a_named_oracle_capture_materializes_a_labelled_candidate():
    result = build(evidence_kind=REAL)

    assert result.accepted is True, result.report["reason_detail"]
    assert result.reason_code == exporter.REAL_CAPTURE_CANDIDATE_BUILT
    candidate = json.loads(result.candidate_bytes)
    assert candidate["artifact_kind"] == exporter.REAL_CAPTURE_ARTIFACT_KIND
    assert candidate["evidence_kind"] == REAL
    assert candidate["synthetic_only"] is False
    assert candidate["admission_status"] == exporter.REAL_CAPTURE_ADMISSION_STATUS
    assert (
        candidate["source_event_digest_domain"]
        == exporter.REAL_SOURCE_EVENT_DIGEST_DOMAIN
    )
    assert (
        candidate["bridge_payload_digest_domain"]
        == exporter.BRIDGE_PAYLOAD_DIGEST_DOMAIN
    )
    assert {"events", "schedule_id", "settlement_currency"}.isdisjoint(candidate)
    body = candidate["real_capture_candidate"]
    assert body["event_count"] == 2
    assert body["effective_interval"] == {
        "end_exclusive": END,
        "end_tolerance_seconds": 1,
        "start_inclusive": START,
    }
    events = body["bound_events"]
    assert [item["binding"]["funding_event_id"] for item in events] == [ID1, ID2]
    assert [item["binding"]["event_timestamp"] for item in events] == [TS1, TS2]
    assert [item["binding"]["interval_hour_utc"] for item in events] == [HOUR1, HOUR2]
    assert events[0]["binding"]["source_event_digest"] == (
        f"{exporter.REAL_SOURCE_EVENT_DIGEST_DOMAIN}:{hashlib.sha256(ROW1).hexdigest()}"
    )
    assert events[0]["bridge_evidence"]["payload_digest"] == EVENT1.digest
    assert (
        body["coverage_witness"]["funding_witness_passes"] == [FUNDING_PASS.hex()] * 2
    )
    assert body["completion_check"]["expected_funding_hours"] == [HOUR1, HOUR2]
    assert result.report["evidence_kind"] == REAL
    assert result.report["synthetic_only"] is False
    assert result.report["production_mode"] == exporter.PRODUCTION_MODE_UNAVAILABLE
    assert (
        result.report["non_admission"]["admission_status"]
        == exporter.REAL_CAPTURE_ADMISSION_STATUS
    )
    assert any(
        "oracle" in item.lower() for item in result.report["evidence_limitations"]
    )
    assert any("Q3" in item for item in result.report["evidence_limitations"])


def test_the_real_candidate_is_deterministic_and_carries_only_capture_day_instants():
    first = build(evidence_kind=REAL)
    second = build(evidence_kind=REAL)

    assert first.candidate_bytes == second.candidate_bytes
    assert first.report == second.report
    assert (
        first.candidate_bytes.endswith(b"\n")
        and first.candidate_bytes.count(b"\n") == 1
    )
    assert _day_prefixes(json.loads(first.candidate_bytes)) == {"2026-09-14T"}
    assert _day_prefixes(first.report) == {"2026-09-14T"}


def test_the_synthetic_profile_still_refuses_a_real_packet_by_kind():
    # The real profile adds nothing to the default accepted set; a SYNTHETIC caller
    # that receives real evidence is told the kind disagrees, not that it passed.
    result = build(evidence_kind=exporter.SYNTHETIC_EVIDENCE_KIND)

    assert result.accepted is False
    assert result.reason_code == exporter.CANDIDATE_EVIDENCE_KIND_MISMATCH


# ---------------------------------------------------------------------------
# D-1 — the digest hashes the exact captured row bytes, at the located index
# ---------------------------------------------------------------------------


def _refused(result: exporter.CandidateResult, code: str, rule: str) -> None:
    assert result.accepted is False
    assert result.reason_code == code, result.report["reason_detail"]
    assert rule in result.report["reason_detail"]


def test_d1_digest_must_hash_the_exact_captured_row_bytes_not_a_reserialization():
    bindings = r1_bindings()
    for item, raw in zip(bindings, [ROW1, ROW2]):
        canonical = json.dumps(
            json.loads(raw), sort_keys=True, separators=(",", ":")
        ).encode()
        assert canonical != raw  # the venue's key order is not the canonical order
        item["source_event_digest"] = (
            f"{exporter.REAL_SOURCE_EVENT_DIGEST_DOMAIN}:{hashlib.sha256(canonical).hexdigest()}"
        )

    result = build(
        bindings=bindings, cover=real_coverage(bindings=bindings), evidence_kind=REAL
    )

    _refused(result, exporter.CANDIDATE_BINDING_INVALID, "D-1")


@pytest.mark.parametrize(
    "digest",
    [
        hashlib.sha256(ROW1).hexdigest(),  # untagged
        "SYNTHETIC_SOURCE_EVENT_DIGEST_V1:" + hashlib.sha256(ROW1).hexdigest(),
        "HL_USERFUNDING_ROW_V1:" + hashlib.sha256(ROW1).hexdigest().upper(),
    ],
)
def test_d1_digest_must_carry_the_ruled_domain_tag(digest):
    bindings = r1_bindings()
    bindings[0]["source_event_digest"] = digest

    result = build(
        bindings=bindings, cover=real_coverage(bindings=bindings), evidence_kind=REAL
    )

    _refused(result, exporter.CANDIDATE_BINDING_INVALID, "D-1")


def test_d1_row_bytes_must_be_the_located_span_of_the_funding_pass():
    bindings = r1_bindings()
    # swap the two rows' witnesses: each digest still hashes its own bytes, but the
    # bytes are not the span at the locator index of that binding
    cover = real_coverage(bindings=bindings, rows=[ROW2, ROW1])
    for item, raw in zip(bindings, [ROW2, ROW1]):
        item["source_event_digest"] = (
            f"{exporter.REAL_SOURCE_EVENT_DIGEST_DOMAIN}:{hashlib.sha256(raw).hexdigest()}"
        )

    result = build(bindings=bindings, cover=cover, evidence_kind=REAL)

    _refused(result, exporter.CANDIDATE_BINDING_INVALID, "D-1")


def test_d1_digest_never_reuses_the_bridge_payload_digest():
    bindings = r1_bindings()
    bindings[0]["source_event_digest"] = (
        f"{exporter.REAL_SOURCE_EVENT_DIGEST_DOMAIN}:{EVENT1.digest}"
    )

    result = build(
        bindings=bindings, cover=real_coverage(bindings=bindings), evidence_kind=REAL
    )

    assert result.accepted is False
    assert result.reason_code == exporter.CANDIDATE_DIGEST_DOMAIN_CONFLATION


# ---------------------------------------------------------------------------
# D-2 / D-3 — identity and instants re-derived from the row, never trusted
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "event_id",
    [
        f"hl-funding:0xdead…beef:BTC:{T1_MS}",  # another scope
        f"hl-funding:{SCOPE}:ETH:{T1_MS}",  # another coin
        f"hl-funding:{SCOPE}:BTC:{T1_MS - 41}",  # the hour, not the stamp
        f"0x{'0' * 64}",  # the venue's zero hash
    ],
)
def test_d2_event_id_must_rederive_from_scope_coin_and_stamp(event_id):
    bindings = r1_bindings()
    bindings[0]["funding_event_id"] = event_id
    rows = [retained_row(EVENT1), retained_row(EVENT2)]
    rows[0]["event_id"] = event_id
    rows[0]["payload"]["event_id"] = event_id
    rows[0]["payload_digest"] = exporter.reconcile_digest(rows[0]["payload"])

    result = build(
        rows=rows,
        bindings=bindings,
        cover=real_coverage(bindings=bindings),
        evidence_kind=REAL,
    )

    # the captured row's own D-2 identity is missing from the inventory, so the
    # pass-level disposition check names both identities
    _refused(result, exporter.CANDIDATE_COVERAGE_INVALID, "D-2")
    assert ID1 in result.report["reason_detail"]
    assert event_id in result.report["reason_detail"]


def test_d2_a_binding_that_locates_another_captured_row_is_refused():
    # every identity is inventoried and captured, but binding ID1 points at row 1
    # with row 1's exact bytes and digest: D-1 holds, D-2 must still fail
    bindings = r1_bindings()
    bindings[0]["provenance"]["source_locator"] = f"{FUNDING_FILE}#/1"
    bindings[0]["source_event_digest"] = (
        f"{exporter.REAL_SOURCE_EVENT_DIGEST_DOMAIN}:{hashlib.sha256(ROW2).hexdigest()}"
    )
    cover = real_coverage(bindings=bindings, rows=[ROW2, ROW2])

    result = build(bindings=bindings, cover=cover, evidence_kind=REAL)

    _refused(result, exporter.CANDIDATE_BINDING_INVALID, "D-2")


@pytest.mark.parametrize(
    ("stamp", "hour"),
    [
        ("2026-09-14T17:00:00Z", HOUR1),  # rounded away
        ("2026-09-14T17:00:00.041000Z", HOUR1),  # respelled
        (TS1, "2026-09-14T17:00:00.041Z"),  # hour key not floored
        (TS1, "2026-09-14T16:00:00Z"),  # wrong hour
    ],
)
def test_d3_stamp_is_verbatim_and_the_hour_key_is_its_floor(stamp, hour):
    bindings = r1_bindings()
    bindings[0]["event_timestamp"] = stamp
    bindings[0]["interval_hour_utc"] = hour

    result = build(
        bindings=bindings, cover=real_coverage(bindings=bindings), evidence_kind=REAL
    )

    _refused(result, exporter.CANDIDATE_BINDING_INVALID, "D-3")


def test_d3_the_hour_key_is_a_required_ninth_binding_field():
    bindings = r1_bindings()
    del bindings[0]["interval_hour_utc"]

    result = build(
        bindings=bindings, cover=real_coverage(bindings=bindings), evidence_kind=REAL
    )

    assert result.accepted is False
    assert result.reason_code == exporter.CANDIDATE_BINDING_INVALID
    assert "interval_hour_utc" in result.report["reason_detail"]


def test_raw_rate_and_the_payer_convention_are_checked_against_the_row():
    bindings = r1_bindings()
    bindings[0]["raw_rate"] = "0.0000126"
    result = build(
        bindings=bindings, cover=real_coverage(bindings=bindings), evidence_kind=REAL
    )
    _refused(result, exporter.CANDIDATE_BINDING_INVALID, "fundingRate")

    # a long paying at a positive rate shows a negative usdc delta; a positive one
    # contradicts the approved LONG-pays convention
    contradiction = ROW1.replace(b'"usdc":"-0.000571"', b'"usdc":"0.000571"')
    pass_bytes = FUNDING_PASS.replace(ROW1, contradiction)
    bindings = r1_bindings()
    bindings[0]["source_event_digest"] = (
        f"{exporter.REAL_SOURCE_EVENT_DIGEST_DOMAIN}:{hashlib.sha256(contradiction).hexdigest()}"
    )
    for item in bindings:
        item["provenance"]["source_sha256"] = hashlib.sha256(pass_bytes).hexdigest()
    cover = real_coverage(
        bindings=bindings, rows=[contradiction, ROW2], passes=[pass_bytes, pass_bytes]
    )
    result = build(bindings=bindings, cover=cover, evidence_kind=REAL)
    _refused(result, exporter.CANDIDATE_BINDING_INVALID, "positive_rate_payer")


# ---------------------------------------------------------------------------
# D-5 — the witness must name the ownership-signature record
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "identity",
    [
        f"capture_own_account_evidence.py run {RUN_ID}; manifest_sha256={MANIFEST_SHA}",
        witness_identity(ownership="OWNERSHIP_EVIDENCE: UNVERIFIED"),
        witness_identity(scope="0xdead…beef"),
        witness_identity().replace(
            f"manifest_sha256={MANIFEST_SHA}", "manifest_sha256=missing"
        ),
        witness_identity().replace(f"run {RUN_ID}", "run"),
    ],
)
def test_d5_witness_identity_must_name_the_ownership_record_for_this_scope(identity):
    bindings = r1_bindings()

    result = build(
        bindings=bindings,
        cover=real_coverage(bindings=bindings, identity=identity),
        evidence_kind=REAL,
    )

    _refused(result, exporter.CANDIDATE_COVERAGE_INVALID, "D-5")


# ---------------------------------------------------------------------------
# D-6 — hour-aligned window, byte-identical passes, 1-second end tolerance,
# fills-based expected count, every captured row inventoried
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("start", "end"),
    [
        ("2026-09-14T15:30:00Z", END),
        (START, "2026-09-14T18:59:59Z"),
        (START, "2026-09-14T19:00:00.5Z"),
    ],
)
def test_d6_the_window_must_be_aligned_to_whole_hours(start, end):
    bindings = r1_bindings()

    result = build(
        bindings=bindings,
        cover=real_coverage(bindings=bindings, start=start, end=end),
        start=start,
        end=end,
        evidence_kind=REAL,
    )

    _refused(result, exporter.CANDIDATE_COVERAGE_INVALID, "D-6")


@pytest.mark.parametrize(
    "passes",
    [
        [FUNDING_PASS],  # one pass only
        [FUNDING_PASS, FUNDING_PASS + b"\n"],  # not byte-identical
        [FUNDING_PASS, b"[]"],
    ],
)
def test_d6_two_byte_identical_funding_passes_are_required(passes):
    bindings = r1_bindings()

    result = build(
        bindings=bindings,
        cover=real_coverage(bindings=bindings, passes=passes),
        evidence_kind=REAL,
    )

    _refused(result, exporter.CANDIDATE_COVERAGE_INVALID, "D-6")


def test_d6_the_pass_digest_must_be_the_provenance_source_digest():
    bindings = r1_bindings()
    bindings[1]["provenance"]["source_sha256"] = hashlib.sha256(
        b"another file"
    ).hexdigest()

    result = build(
        bindings=bindings, cover=real_coverage(bindings=bindings), evidence_kind=REAL
    )

    _refused(result, exporter.CANDIDATE_BINDING_INVALID, "source_sha256")


def _window_15_to_18() -> tuple[list[dict], dict]:
    """A [15:00, 18:00) window: the 18:00:00.060Z payment settles the 17-18 interval and
    lands 60 ms past the requested end. The capture's fills show the position still open
    at 18:00 (closed 18:08), so the payment is expected and must be admitted."""
    end = "2026-09-14T18:00:00Z"
    bindings = r1_bindings()
    cover = real_coverage(bindings=bindings, end=end)
    return bindings, cover


def test_d6_one_second_end_tolerance_admits_the_venue_late_stamp():
    bindings, cover = _window_15_to_18()

    result = build(
        bindings=bindings, cover=cover, end="2026-09-14T18:00:00Z", evidence_kind=REAL
    )

    assert result.accepted is True, result.report["reason_detail"]
    body = json.loads(result.candidate_bytes)["real_capture_candidate"]
    assert body["event_count"] == 2
    assert body["completion_check"]["expected_funding_hours"] == [HOUR1, HOUR2]


def test_d6_a_stamp_more_than_one_second_past_the_end_is_out_of_interval():
    late = ROW2.replace(b'"time":1789408800060', b'"time":1789408801060')
    pass_bytes = FUNDING_PASS.replace(ROW2, late)
    bindings = r1_bindings()
    bindings[1]["event_timestamp"] = "2026-09-14T18:00:01.060Z"
    bindings[1]["funding_event_id"] = f"hl-funding:{SCOPE}:BTC:1789408801060"
    bindings[1]["source_event_digest"] = (
        f"{exporter.REAL_SOURCE_EVENT_DIGEST_DOMAIN}:{hashlib.sha256(late).hexdigest()}"
    )
    for item in bindings:
        item["provenance"]["source_sha256"] = hashlib.sha256(pass_bytes).hexdigest()
    rows = [
        retained_row(EVENT1),
        retained_row(
            event(
                bindings[1]["funding_event_id"],
                datetime(2026, 9, 14, 18, 0, 1, 60000, tzinfo=UTC),
                -0.000572,
            )
        ),
    ]
    cover = real_coverage(
        bindings=bindings,
        rows=[ROW1, late],
        passes=[pass_bytes, pass_bytes],
        end="2026-09-14T18:00:00Z",
    )

    result = build(
        rows=rows,
        bindings=bindings,
        cover=cover,
        end="2026-09-14T18:00:00Z",
        evidence_kind=REAL,
    )

    assert result.accepted is False
    assert result.reason_code == exporter.CANDIDATE_BINDING_OUT_OF_INTERVAL


def test_d6_fills_that_leave_the_position_open_demand_the_missing_payment():
    # drop the closing fill: the position of 0.00058 stays open through 19:00Z, so the
    # fills expect a 19:00 payment the funding pass does not carry
    bindings = r1_bindings()
    cover = real_coverage(bindings=bindings, fills=fills_bytes(FILLS_R1[:4]))

    result = build(bindings=bindings, cover=cover, evidence_kind=REAL)

    _refused(result, exporter.CANDIDATE_COVERAGE_INVALID, "D-6")
    assert "2026-09-14T19:00:00Z" in result.report["reason_detail"]


def test_d6_a_row_position_that_disagrees_with_the_fills_refuses():
    bindings = r1_bindings()
    fills = list(FILLS_R1)
    # a self-consistent fills history that reaches 0.00057, not the rows' 0.00058
    fills[3] = _fill(
        "78410.0", "0.00015", "B", 1789402474869, "0.00042", "Open Long", 4
    )
    fills[4] = _fill(
        "78993.0", "0.00057", "A", 1789409323372, "0.00057", "Close Long", 5
    )

    result = build(
        bindings=bindings,
        cover=real_coverage(bindings=bindings, fills=fills_bytes(fills)),
        evidence_kind=REAL,
    )

    _refused(result, exporter.CANDIDATE_COVERAGE_INVALID, "szi")


def test_d6_a_gap_in_the_fills_history_refuses():
    # the closing fill claims to start from 0.00058 while the captured fills
    # before it only reach 0.00057: the witness is not a contiguous history
    bindings = r1_bindings()
    fills = list(FILLS_R1)
    fills[3] = _fill(
        "78410.0", "0.00015", "B", 1789402474869, "0.00042", "Open Long", 4
    )

    result = build(
        bindings=bindings,
        cover=real_coverage(bindings=bindings, fills=fills_bytes(fills)),
        evidence_kind=REAL,
    )

    _refused(result, exporter.CANDIDATE_COVERAGE_INVALID, "contiguous")


def test_d6_fills_that_are_not_venue_fill_rows_refuse():
    bindings = r1_bindings()

    for fills in (b"not json", b'{"a":1}', b'[{"coin":"BTC","sz":"0.1"}]', b"[]"):
        result = build(
            bindings=bindings,
            cover=real_coverage(bindings=bindings, fills=fills),
            evidence_kind=REAL,
        )
        _refused(result, exporter.CANDIDATE_COVERAGE_INVALID, "D-6")


def test_d6_every_row_inside_the_captured_pass_needs_a_disposition():
    # inventory, bindings and retained rows all omit the second captured row; the
    # pass bytes still carry it, so nothing may pass silently
    bindings = r1_bindings()[:1]
    cover = real_coverage(bindings=bindings, rows=[ROW1])

    result = build(
        rows=[retained_row(EVENT1)], bindings=bindings, cover=cover, evidence_kind=REAL
    )

    _refused(result, exporter.CANDIDATE_COVERAGE_INVALID, "D-6")
    assert ID2 in result.report["reason_detail"]


def test_d6_a_foreign_coin_row_inside_the_pass_refuses():
    foreign = ROW2.replace(b'"coin":"BTC"', b'"coin":"ETH"')
    pass_bytes = FUNDING_PASS.replace(ROW2, foreign)
    bindings = r1_bindings()[:1]
    bindings[0]["provenance"]["source_sha256"] = hashlib.sha256(pass_bytes).hexdigest()
    cover = real_coverage(
        bindings=bindings, rows=[ROW1], passes=[pass_bytes, pass_bytes]
    )

    result = build(
        rows=[retained_row(EVENT1)], bindings=bindings, cover=cover, evidence_kind=REAL
    )

    assert result.accepted is False
    assert result.reason_code == exporter.CANDIDATE_SYMBOL_MISMATCH


def test_d6_the_completion_check_names_the_fills_witness_as_the_position_source():
    """D-6 (ii) provenance on the normal r1 path: the position that expects the
    payments comes from the fills witness, and the completion check says so
    (lane-8 exact-Opus review of ``9ef072a8``, REQUIRED-1: the two provenance
    fields were emitted but never asserted)."""
    result = build(evidence_kind=REAL)

    assert result.accepted is True, result.report["reason_detail"]
    check = json.loads(result.candidate_bytes)["real_capture_candidate"][
        "completion_check"
    ]
    assert check["position_source"] == exporter.REAL_POSITION_SOURCE_FILLS
    assert check["position_source"] == "coverage.fills_witness"
    assert check["opening_position"] == "0.0"
    assert check["expected_funding_hours"] == [HOUR1, HOUR2]


@pytest.mark.parametrize(
    "fills",
    [
        b"[]",
        (
            "["
            + _fill("1.0", "1", "B", 1789405000000, "0.0", "Open Long", 9).replace(
                '"coin":"BTC"', '"coin":"ETH"'
            )
            + "]"
        ).encode("utf-8"),
    ],
    ids=["empty-fills-witness", "another-coin-only"],
)
def test_d6_without_a_fill_for_the_symbol_the_position_source_is_the_payments(fills):
    """D-6 (ii) accepting branch with no fill for the symbol: the position is the
    constant szi the payments report, every grid hour of a [17:00, 18:00) window
    carries a payment, and the completion check names the payments - not the fills
    witness - as the producer of that position (lane-8 REQUIRED-1: this branch was
    reachable, accepting and unlabelled; three mutants of it survived the suite)."""
    start, end = "2026-09-14T17:00:00Z", "2026-09-14T18:00:00Z"
    bindings = r1_bindings()
    cover = real_coverage(bindings=bindings, fills=fills, start=start, end=end)

    result = build(
        bindings=bindings, cover=cover, start=start, end=end, evidence_kind=REAL
    )

    assert result.accepted is True, result.report["reason_detail"]
    body = json.loads(result.candidate_bytes)["real_capture_candidate"]
    check = body["completion_check"]
    assert check["position_source"] == exporter.REAL_POSITION_SOURCE_PAYMENTS
    assert check["position_source"] != exporter.REAL_POSITION_SOURCE_FILLS
    assert "fills witness carries no fill" in check["position_source"]
    assert check["opening_position"] is None
    assert check["expected_funding_hours"] == [HOUR1, HOUR2]
    assert check["observed_funding_hours"] == [HOUR1, HOUR2]
    assert body["coverage_witness"]["fills_witness"] == fills.hex()
    assert any(
        "position the payments" in item
        for item in result.report["evidence_limitations"]
    )


def test_d6_an_empty_inventory_cannot_be_witnessed():
    cover = real_coverage(bindings=[], rows=[], passes=[b"[]", b"[]"], fills=b"[]")

    result = build(rows=[], bindings=[], cover=cover, evidence_kind=REAL)

    _refused(result, exporter.CANDIDATE_COVERAGE_INVALID, "D-6")


def test_the_real_coverage_witness_is_a_closed_shape():
    bindings = r1_bindings()
    cover = real_coverage(bindings=bindings)
    del cover["fills_witness"]
    result = build(bindings=bindings, cover=cover, evidence_kind=REAL)
    assert result.accepted is False
    assert result.reason_code == exporter.CANDIDATE_COVERAGE_INVALID

    cover = real_coverage(bindings=bindings, witness_rule="anything")
    result = build(bindings=bindings, cover=cover, evidence_kind=REAL)
    assert result.accepted is False
    assert result.reason_code == exporter.CANDIDATE_COVERAGE_INVALID


# ---------------------------------------------------------------------------
# CLI — the documented command with the profile named; snapshot is a FIXTURE
# ---------------------------------------------------------------------------


def write_snapshot(path: Path) -> Path:
    store = Store(path)
    store.initialize(target_schema_version=SCHEMA_VERSION_FUNDING_PAYLOAD)
    attempt_id = store.reserve_reconcile_attempt(
        run_id="run-p012-s4", started_ts=RECORDED, deadline_s=5.0, max_skew_s=5.0
    )
    store.finalize_reconcile_attempt(
        attempt_id=attempt_id,
        state=ReconcileAttemptState.INCOMPLETE,
        ended_ts=RECORDED,
        duration_ms=1,
        canonical_hash=None,
        reason_code="FIXTURE_RETAINED_ROWS_FOR_REAL_CAPTURE_TEST",
        funding_events=(EVENT1, EVENT2),
        accepted=False,
        fresh=False,
    )
    store.close()
    return path


def real_packet_bytes() -> bytes:
    bindings = r1_bindings()
    packet = {
        "packet_version": exporter.REAL_CAPTURE_PACKET_VERSION,
        "coverage": real_coverage(bindings=bindings),
        "bindings": bindings,
    }
    return json.dumps(packet, sort_keys=True, ensure_ascii=False).encode("utf-8")


def _cli(tmp_path: Path, staging: Path, *extra: str) -> int:
    snapshot = write_snapshot(tmp_path / "offline" / "snapshot.db")
    packet = tmp_path / "bindings.json"
    packet.write_bytes(real_packet_bytes())
    return exporter.main(
        [
            "--snapshot",
            str(snapshot),
            "--bindings",
            str(packet),
            "--symbol",
            SYMBOL,
            "--start",
            START,
            "--end",
            END,
            "--schedule-id",
            SCHEDULE_ID,
            "--staging",
            str(staging),
            *extra,
        ]
    )


def test_cli_stages_the_real_capture_candidate_only_under_the_named_profile(tmp_path):
    staging = tmp_path / "staged_real"

    assert _cli(tmp_path, staging, "--evidence-kind", REAL) == 0

    names = sorted(item.name for item in staging.iterdir())
    assert names == [
        exporter.REAL_CAPTURE_CANDIDATE_FILENAME,
        exporter.REAL_CAPTURE_SIDECAR_FILENAME,
        exporter.REPORT_FILENAME,
    ]
    candidate = (staging / exporter.REAL_CAPTURE_CANDIDATE_FILENAME).read_bytes()
    sidecar = (staging / exporter.REAL_CAPTURE_SIDECAR_FILENAME).read_text(
        encoding="ascii"
    )
    assert sidecar == hashlib.sha256(candidate).hexdigest() + "\n"
    report = json.loads((staging / exporter.REPORT_FILENAME).read_bytes())
    assert report["accepted"] is True
    assert report["evidence_kind"] == REAL
    assert report["reason_code"] == exporter.REAL_CAPTURE_CANDIDATE_BUILT


def test_cli_without_the_profile_refuses_the_same_real_packet(tmp_path):
    staging = tmp_path / "staged_default"

    assert _cli(tmp_path, staging) == 1

    names = sorted(item.name for item in staging.iterdir())
    assert names == [exporter.REPORT_FILENAME]
    report = json.loads((staging / exporter.REPORT_FILENAME).read_bytes())
    assert report["accepted"] is False
    assert report["reason_code"] == exporter.CANDIDATE_PACKET_INVALID
    assert report["evidence_kind"] == exporter.SYNTHETIC_EVIDENCE_KIND
