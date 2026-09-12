"""WP-P0-12 Path D, decision A — the production funding export mode.

D026 RED/GREEN for ``tools/export_mtc_funding.py`` under
``OD-20260912-P012-PATHD-1`` (A1=A forward-only own account, A2=B with M
PENDING, A3=A refuse the whole interval on any gap).

Everything in this file is still synthetic: the event hashes, amounts, rates,
capture bytes, account/product declarations and witnesses are invented for the
test and are *labelled* as declarations, which is exactly what the decision
allows a fixture to supply. Nothing here is a Hyperliquid capture, a venue
fact, or a claim about a real account, interval or payment, and a passing run
is not an acceptance.

RED (pre-fix, round 1): ``--mode`` is an unrecognised CLI argument
(``SystemExit: 2``) and ``export_mtc_funding`` has no ``MODE_PRODUCTION``,
``PRODUCTION_SOURCE_EVENT_DIGEST_DOMAIN`` or ``declarations`` parameter, so
every test below fails at import/attribute resolution; the tool's production
mode is the frozen string ``UNAVAILABLE_PENDING_SOURCE_EVENT_DIGEST_DOMAIN``.

RED (pre-repair, round 2) — behavioural, on the round-1 candidate ``81c3287d``,
with no new symbol involved:

* the capture-value tests: an adversarial capture claiming ETH, time 0 and
  ``usdc 999999`` was **accepted** beside an admitted BTC ``-1.25`` settlement,
  because the capture was bound by digest and identity pointer only;
* the forward-only tests: a declared interval on 2026-09-11, before the
  2026-09-12 owner signature, was **accepted**;
* the duplicate tests: three retained rows carrying one exact duplicate were
  **accepted** and emitted two settlement events, because ``_fold_unique``
  collapsed the duplicate before the settlement-key guard could see it.

RED (pre-repair, round 3) — behavioural, on the round-2 candidate ``fae07fa7``
(``capture_binding_probe.py``, lane A):

* the sample-count tests: captures claiming ``nSamples`` ``999``, ``true`` or
  nothing at all were **accepted** beside a retained ``n_samples`` of ``1``,
  because the capture binding covered only amount, rate, size and coin;
* the source test: a retained ``source`` of ``NOT_HL_USER_FUNDING`` was
  **accepted**, although the producer stamps exactly ``HL_USER_FUNDING``;
* the scope test: an ETH retained payload with an ETH capture was **accepted**
  under an outer BTC retained row, a BTC witness and a BTC candidate scope,
  because only the outer row's symbol was compared with the witness.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import replace
from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest

from bridge.engine.types import (
    FundingAttribution,
    FundingEventRecord,
    ReconcileAttemptState,
)
from bridge.store.db import SCHEMA_VERSION_FUNDING_PAYLOAD, Store
from tools import export_mtc_funding as exporter


# ---------------------------------------------------------------------------
# Synthetic fixture material — declarations included
# ---------------------------------------------------------------------------

SYMBOL = "BTC"
SCHEDULE_ID = "SYNTH-P012-PATHD-PRODUCTION-TARGET-V1"
# A1 = A forward-only: the declared interval opens after the owner signature
# instant 2026-09-12T11:00:00Z, so this fixture is admissible by date.  The
# round-1 fixture opened on 2026-09-11 and is kept below as a RED control.
START = "2026-09-12T12:00:00Z"
END = "2026-09-12T13:00:00Z"
PRE_SIGNATURE_START = "2026-09-11T12:00:00Z"
PRE_SIGNATURE_END = "2026-09-11T13:00:00Z"
DECLARED_ACCOUNT = "SYNTHETIC-DECLARED-ACCOUNT-0001"
DECLARED_PRODUCT = "SYNTHETIC-DECLARED-BTC-PERP"
DECLARED_INTERVAL = f"{START}/{END}"
WITNESS = "SYNTHETIC-DECLARED-WITNESS-0001"

ID_A = "0xsynthetic0002"
ID_B = "0xsynthetic0001"
TS_A = "2026-09-12T12:00:00.031Z"
TS_B = "2026-09-12T12:30:00Z"
RECORDED = datetime(2026, 9, 12, 12, 0, tzinfo=UTC)
EPOCH = datetime(1970, 1, 1, tzinfo=UTC)

EVENT_A = FundingEventRecord(
    event_id=ID_A,
    symbol=SYMBOL,
    amount_usdc=-1.25,
    effective_ts=datetime(2026, 9, 12, 12, 0, 0, 31000, tzinfo=UTC),
    source="HL_USER_FUNDING",
    attribution=FundingAttribution.ATTRIBUTED,
    funding_rate=0.0000125,
    position_szi=0.1,
    n_samples=1,
)
EVENT_B = FundingEventRecord(
    event_id=ID_B,
    symbol=SYMBOL,
    amount_usdc=-2.5,
    effective_ts=datetime(2026, 9, 12, 12, 30, tzinfo=UTC),
    source="HL_USER_FUNDING",
    attribution=FundingAttribution.ATTRIBUTED,
    funding_rate=0.000025,
    position_szi=0.1,
    n_samples=1,
)


def epoch_ms(moment: datetime) -> int:
    """Exact whole milliseconds since the epoch (no float rounding)."""
    return (moment.astimezone(UTC) - EPOCH) // timedelta(milliseconds=1)


def capture(event: FundingEventRecord, *, drop: tuple[str, ...] = (), **overrides) -> bytes:
    """One invented own-account capture row. Not a venue response.

    The layout is the ``userFunding`` element the production digest domain
    names: ``/hash`` is the settlement identity, ``/time`` is epoch
    milliseconds and ``/delta`` carries the coin, rate, size, settled cash and
    sample count.  ``nSamples`` is present exactly when the record carries one,
    because the producer normalizes an absent or non-integer ``nSamples`` to
    ``None`` (``bridge/broker/hyperliquid.py:2139``). ``drop`` removes a delta
    member so a capture can be made silent about a field it should state.
    """
    delta = {
        "coin": event.symbol,
        "fundingRate": repr(event.funding_rate),
        "szi": repr(event.position_szi),
        "type": "funding",
        "usdc": repr(event.amount_usdc),
    }
    if event.n_samples is not None:
        delta["nSamples"] = event.n_samples
    delta.update(overrides.pop("delta", {}))
    for member in drop:
        delta.pop(member, None)
    row = {
        "delta": delta,
        "hash": event.event_id,
        "time": epoch_ms(event.effective_ts),
    }
    row.update(overrides)
    return json.dumps(row, sort_keys=True, separators=(",", ":")).encode("utf-8")


def capture_digest(event: FundingEventRecord, **overrides) -> str:
    return hashlib.sha256(capture(event, **overrides)).hexdigest()


def retained_row(event: FundingEventRecord, **overrides) -> dict:
    row = {
        "attribution": event.attribution.value,
        "event_id": event.event_id,
        "ledger_effective_ts": event.effective_ts.astimezone(UTC).isoformat(),
        "payload": event.authoritative(),
        "payload_digest": event.digest,
        "payload_reason": exporter.PAYLOAD_RETAINED,
        "symbol": event.symbol,
    }
    row.update(overrides)
    return row


def provenance(digest: str) -> dict:
    return {
        "evidence_kind": exporter.PRODUCTION_EVIDENCE_KIND,
        "extraction_method": "OWN_ACCOUNT_AUTHENTICATED_CAPTURE_V1",
        "source_locator": "synthetic://p012-path-d/own-account-capture",
        "source_sha256": digest,
        "source_title": "SYNTHETIC-PATH-D-CAPTURE",
    }


def binding(
    event: FundingEventRecord,
    *,
    event_timestamp: str,
    account_scope: str = DECLARED_ACCOUNT,
    pointer: str = "/hash",
    source_event_digest: str | None = None,
    provenance_digest: str | None = None,
    extra: dict | None = None,
) -> dict:
    digest = source_event_digest or capture_digest(event)
    body = {
        "account_scope": account_scope,
        "capture_identity_pointer": pointer,
        "event_timestamp": event_timestamp,
        "funding_event_id": event.event_id,
        "positive_rate_payer": "LONG",
        "provenance": provenance(provenance_digest or capture_digest(event)),
        "source_event_digest": digest,
    }
    if extra:
        body.update(extra)
    return body


def coverage(
    *,
    expected_event_ids: list[str] | None = None,
    gap_event_ids: list[str] | None = None,
    declared_account: str = DECLARED_ACCOUNT,
    declared_product: str = DECLARED_PRODUCT,
    evidence_kind: str | None = None,
    source_witnesses: dict[str, str] | None = None,
    complete: object = True,
    start: str = START,
    end: str = END,
    symbol: str = SYMBOL,
) -> dict:
    return {
        "account_scope": declared_account,
        "complete": complete,
        "declared_account": declared_account,
        "declared_product": declared_product,
        "evidence_kind": (
            exporter.PRODUCTION_EVIDENCE_KIND if evidence_kind is None else evidence_kind
        ),
        "expected_event_ids": (
            [ID_A, ID_B] if expected_event_ids is None else expected_event_ids
        ),
        "gap_event_ids": [] if gap_event_ids is None else gap_event_ids,
        "interval_end_exclusive": end,
        "interval_start_inclusive": start,
        "source_witnesses": (
            {ID_A: capture(EVENT_A).hex(), ID_B: capture(EVENT_B).hex()}
            if source_witnesses is None
            else source_witnesses
        ),
        "symbol": symbol,
        "unattributed_event_ids": [],
        "witness_identity": WITNESS,
    }


def declarations(**overrides) -> dict:
    values = {
        "account": DECLARED_ACCOUNT,
        "interval": DECLARED_INTERVAL,
        "product": DECLARED_PRODUCT,
    }
    values.update(overrides)
    return values


def build(**kwargs):
    params = {
        "retained_rows": [retained_row(EVENT_A), retained_row(EVENT_B)],
        "approved_event_bindings": [
            binding(EVENT_A, event_timestamp=TS_A),
            binding(EVENT_B, event_timestamp=TS_B),
        ],
        "coverage": coverage(),
        "schedule_id": SCHEDULE_ID,
        "start_inclusive": START,
        "end_exclusive": END,
    }
    mode = kwargs.pop("mode", exporter.MODE_PRODUCTION)
    declared = kwargs.pop("declarations", declarations())
    params.update(kwargs)
    return exporter.build_funding_candidate(**params, mode=mode, declarations=declared)


def build_one(
    event: FundingEventRecord,
    blob: bytes,
    *,
    row_overrides: dict | None = None,
    cover_overrides: dict | None = None,
    **kwargs,
):
    """One whole interval carrying one settlement and one explicit capture."""
    digest = hashlib.sha256(blob).hexdigest()
    return build(
        retained_rows=[retained_row(event, **(row_overrides or {}))],
        approved_event_bindings=[
            binding(
                event,
                event_timestamp=TS_A,
                source_event_digest=digest,
                provenance_digest=digest,
            )
        ],
        coverage=coverage(
            expected_event_ids=[event.event_id],
            source_witnesses={event.event_id: blob.hex()},
            **(cover_overrides or {}),
        ),
        **kwargs,
    )


def write_snapshot(path: Path, *events: FundingEventRecord) -> Path:
    store = Store(path)
    store.initialize(target_schema_version=SCHEMA_VERSION_FUNDING_PAYLOAD)
    attempt_id = store.reserve_reconcile_attempt(
        run_id="run-p012-path-d", started_ts=RECORDED, deadline_s=5.0, max_skew_s=5.0
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


@pytest.fixture()
def snapshot(tmp_path: Path) -> Path:
    return write_snapshot(tmp_path / "offline" / "snapshot.db", EVENT_A, EVENT_B)


def packet_bytes(*, bindings=None, cover=None) -> bytes:
    return json.dumps(
        {
            "bindings": [
                binding(EVENT_A, event_timestamp=TS_A),
                binding(EVENT_B, event_timestamp=TS_B),
            ]
            if bindings is None
            else bindings,
            "coverage": coverage() if cover is None else cover,
            "packet_version": exporter.PRODUCTION_PACKET_VERSION,
        },
        sort_keys=True,
    ).encode("utf-8")


# ---------------------------------------------------------------------------
# The declaration gate — UNSPECIFIED until the owner supplies all three
# ---------------------------------------------------------------------------


def test_production_refuses_until_all_three_declarations_are_supplied() -> None:
    result = build(declarations=None)

    assert result.accepted is False
    assert result.reason_code == exporter.CANDIDATE_DECLARATION_UNSPECIFIED
    assert result.candidate_bytes is None
    assert "UNSPECIFIED" in result.report["reason_detail"]


@pytest.mark.parametrize("missing", ["account", "interval", "product"])
def test_one_missing_declaration_still_refuses(missing: str) -> None:
    result = build(declarations=declarations(**{missing: None}))

    assert result.accepted is False
    assert result.reason_code == exporter.CANDIDATE_DECLARATION_UNSPECIFIED


def test_a_declared_interval_that_is_not_the_requested_interval_refuses() -> None:
    result = build(
        declarations=declarations(interval="2026-09-12T12:00:00Z/2026-09-12T14:00:00Z")
    )

    assert result.accepted is False
    assert result.reason_code == exporter.CANDIDATE_DECLARATION_MISMATCH


def test_a_binding_outside_the_declared_account_refuses() -> None:
    result = build(
        approved_event_bindings=[
            binding(EVENT_A, event_timestamp=TS_A, account_scope="OTHER-ACCOUNT"),
            binding(EVENT_B, event_timestamp=TS_B),
        ]
    )

    assert result.accepted is False
    assert result.reason_code == exporter.CANDIDATE_DECLARATION_MISMATCH


# ---------------------------------------------------------------------------
# A1 = A forward-only: nothing before the owner signature is ever admitted
# ---------------------------------------------------------------------------


def test_the_forward_only_bound_is_the_exact_owner_signature_instant() -> None:
    assert exporter.PATH_D_SIGNATURE_INSTANT == "2026-09-12T11:00:00Z"


def test_a_declared_interval_before_the_owner_signature_refuses() -> None:
    """The round-1 fixture interval. RED: it was accepted on ``81c3287d``."""
    early_a = FundingEventRecord(
        event_id=ID_A,
        symbol=SYMBOL,
        amount_usdc=-1.25,
        effective_ts=datetime(2026, 9, 11, 12, 0, 0, 31000, tzinfo=UTC),
        source="HL_USER_FUNDING",
        attribution=FundingAttribution.ATTRIBUTED,
        funding_rate=0.0000125,
        position_szi=0.1,
        n_samples=1,
    )
    early_ts = "2026-09-11T12:00:00.031Z"
    result = build(
        retained_rows=[retained_row(early_a)],
        approved_event_bindings=[binding(early_a, event_timestamp=early_ts)],
        coverage=coverage(
            expected_event_ids=[ID_A],
            source_witnesses={ID_A: capture(early_a).hex()},
            start=PRE_SIGNATURE_START,
            end=PRE_SIGNATURE_END,
        ),
        start_inclusive=PRE_SIGNATURE_START,
        end_exclusive=PRE_SIGNATURE_END,
        declarations=declarations(
            interval=f"{PRE_SIGNATURE_START}/{PRE_SIGNATURE_END}"
        ),
    )

    assert result.accepted is False
    assert result.reason_code == exporter.CANDIDATE_FORWARD_ONLY_VIOLATION
    assert result.candidate_bytes is None
    assert "2026-09-12T11:00:00Z" in result.report["reason_detail"]


def test_an_interval_opening_exactly_on_the_signature_instant_is_admissible() -> None:
    """The bound is inclusive: the signature instant itself is forward-only."""
    boundary = FundingEventRecord(
        event_id=ID_A,
        symbol=SYMBOL,
        amount_usdc=-1.25,
        effective_ts=datetime(2026, 9, 12, 11, 30, tzinfo=UTC),
        source="HL_USER_FUNDING",
        attribution=FundingAttribution.ATTRIBUTED,
        funding_rate=0.0000125,
        position_szi=0.1,
        n_samples=1,
    )
    start = "2026-09-12T11:00:00Z"
    end = "2026-09-12T12:00:00Z"
    result = build(
        retained_rows=[retained_row(boundary)],
        approved_event_bindings=[
            binding(boundary, event_timestamp="2026-09-12T11:30:00Z")
        ],
        coverage=coverage(
            expected_event_ids=[ID_A],
            source_witnesses={ID_A: capture(boundary).hex()},
            start=start,
            end=end,
        ),
        start_inclusive=start,
        end_exclusive=end,
        declarations=declarations(interval=f"{start}/{end}"),
    )

    assert result.accepted is True, result.report


def test_an_authenticated_capture_time_outside_the_interval_refuses() -> None:
    """The capture's own settlement time must fall inside the declared interval.

    Everything the round-1 candidate checked agrees here: the ledger row's
    ``effective_ts`` and the binding both say 12:00:00.031, inside the declared
    interval, and the capture bytes hash to the declared digest and name this
    settlement.  But the *authenticated* settlement time — the one the retained
    payload and the capture both carry — is an hour earlier, outside the
    interval.  A ledger timestamp moved into the interval cannot drag the
    settlement in with it.
    """
    earlier = FundingEventRecord(
        event_id=ID_A,
        symbol=SYMBOL,
        amount_usdc=-1.25,
        effective_ts=datetime(2026, 9, 12, 11, 0, tzinfo=UTC),
        source="HL_USER_FUNDING",
        attribution=FundingAttribution.ATTRIBUTED,
        funding_rate=0.0000125,
        position_szi=0.1,
        n_samples=1,
    )
    outside = capture(earlier)
    digest = hashlib.sha256(outside).hexdigest()
    result = build(
        retained_rows=[
            # The payload (and its digest) are the earlier settlement; only the
            # ledger's own effective_ts column claims the later instant.
            retained_row(
                earlier,
                ledger_effective_ts=EVENT_A.effective_ts.astimezone(UTC).isoformat(),
            ),
            retained_row(EVENT_B),
        ],
        approved_event_bindings=[
            binding(
                EVENT_A,
                event_timestamp=TS_A,
                source_event_digest=digest,
                provenance_digest=digest,
            ),
            binding(EVENT_B, event_timestamp=TS_B),
        ],
        coverage=coverage(
            source_witnesses={
                ID_A: outside.hex(),
                ID_B: capture(EVENT_B).hex(),
            }
        ),
    )

    assert result.accepted is False
    assert result.reason_code == exporter.CANDIDATE_CAPTURE_TIME_OUT_OF_INTERVAL
    assert result.candidate_bytes is None


# ---------------------------------------------------------------------------
# The capture bytes must bind the admitted values, not only an identity
# ---------------------------------------------------------------------------


def test_an_adversarial_capture_does_not_bind_the_admitted_settlement() -> None:
    """RED on ``81c3287d``: this capture was accepted beside BTC ``-1.25``.

    The bytes hash correctly and ``/hash`` names this settlement, so the
    round-1 digest-plus-identity check passed while the capture claimed a
    different coin, a different instant and a different amount.
    """
    adversarial = json.dumps(
        {
            "delta": {
                "coin": "ETH",
                "fundingRate": "0.0",
                "szi": "0.0",
                "type": "funding",
                "usdc": "999999",
            },
            "hash": ID_A,
            "time": 0,
        },
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    digest = hashlib.sha256(adversarial).hexdigest()
    result = build(
        approved_event_bindings=[
            binding(
                EVENT_A,
                event_timestamp=TS_A,
                source_event_digest=digest,
                provenance_digest=digest,
            ),
            binding(EVENT_B, event_timestamp=TS_B),
        ],
        coverage=coverage(
            source_witnesses={
                ID_A: adversarial.hex(),
                ID_B: capture(EVENT_B).hex(),
            }
        ),
    )

    assert result.accepted is False
    assert result.candidate_bytes is None
    assert result.reason_code == exporter.CANDIDATE_CAPTURE_VALUE_MISMATCH
    assert "999999" in result.report["reason_detail"]


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("coin", "ETH"),
        ("fundingRate", "0.0000126"),
        ("szi", "0.2"),
        ("usdc", "-1.26"),
    ],
)
def test_one_changed_capture_field_refuses_the_candidate(field: str, value: str) -> None:
    tampered = capture(EVENT_A, delta={field: value})
    digest = hashlib.sha256(tampered).hexdigest()
    result = build(
        approved_event_bindings=[
            binding(
                EVENT_A,
                event_timestamp=TS_A,
                source_event_digest=digest,
                provenance_digest=digest,
            ),
            binding(EVENT_B, event_timestamp=TS_B),
        ],
        coverage=coverage(
            source_witnesses={
                ID_A: tampered.hex(),
                ID_B: capture(EVENT_B).hex(),
            }
        ),
    )

    assert result.accepted is False
    assert result.reason_code == exporter.CANDIDATE_CAPTURE_VALUE_MISMATCH
    assert field in result.report["reason_detail"] or value in result.report[
        "reason_detail"
    ]


def test_a_capture_that_is_not_a_funding_delta_refuses() -> None:
    tampered = capture(EVENT_A, delta={"type": "deposit"})
    digest = hashlib.sha256(tampered).hexdigest()
    result = build(
        approved_event_bindings=[
            binding(
                EVENT_A,
                event_timestamp=TS_A,
                source_event_digest=digest,
                provenance_digest=digest,
            ),
            binding(EVENT_B, event_timestamp=TS_B),
        ],
        coverage=coverage(
            source_witnesses={
                ID_A: tampered.hex(),
                ID_B: capture(EVENT_B).hex(),
            }
        ),
    )

    assert result.accepted is False
    assert result.reason_code == exporter.CANDIDATE_CAPTURE_VALUE_MISMATCH


def test_a_capture_time_truncated_below_the_retained_precision_refuses() -> None:
    """No silent truncation: 31.527 ms retained is not 31 ms captured."""
    sub_ms = FundingEventRecord(
        event_id=ID_A,
        symbol=SYMBOL,
        amount_usdc=-1.25,
        effective_ts=datetime(2026, 9, 12, 12, 0, 0, 31527, tzinfo=UTC),
        source="HL_USER_FUNDING",
        attribution=FundingAttribution.ATTRIBUTED,
        funding_rate=0.0000125,
        position_szi=0.1,
        n_samples=1,
    )
    truncated = capture(sub_ms)  # epoch_ms() floors 31.527 ms to 31 ms
    digest = hashlib.sha256(truncated).hexdigest()
    result = build(
        retained_rows=[retained_row(sub_ms)],
        approved_event_bindings=[
            binding(
                sub_ms,
                event_timestamp="2026-09-12T12:00:00.031527Z",
                source_event_digest=digest,
                provenance_digest=digest,
            )
        ],
        coverage=coverage(
            expected_event_ids=[ID_A], source_witnesses={ID_A: truncated.hex()}
        ),
    )

    assert result.accepted is False
    assert result.reason_code == exporter.CANDIDATE_CAPTURE_VALUE_MISMATCH


def test_the_admitted_values_are_exactly_the_capture_and_the_retained_payload() -> None:
    candidate = json.loads(build().candidate_bytes)
    events = {
        row["binding"]["funding_event_id"]: row
        for row in candidate["production_candidate"]["settlement_events"]
    }
    for event in (EVENT_A, EVENT_B):
        captured = json.loads(capture(event))
        payload = events[event.event_id]["bridge_evidence"]["payload"]
        assert payload["symbol"] == captured["delta"]["coin"]
        assert float(payload["funding_rate"]) == float(captured["delta"]["fundingRate"])
        assert float(payload["position_szi"]) == float(captured["delta"]["szi"])
        assert float(payload["amount_usdc"]) == float(captured["delta"]["usdc"])
        assert payload["n_samples"] == captured["delta"]["nSamples"]
        assert payload["source"] == "HL_USER_FUNDING"
        assert epoch_ms(event.effective_ts) == captured["time"]
        notes = events[event.event_id]["binding_notes"]
        assert notes["capture_values_bound_to_retained_payload"] is True
        assert notes["capture_value_pointers"]["n_samples"] == "/delta/nSamples"


# ---------------------------------------------------------------------------
# The capture's own sample count, and the producer's source normalization
#
# ``bridge/broker/hyperliquid.py:2139`` keeps ``delta.nSamples`` only when it is
# an ``int`` and not a ``bool``, and stamps ``source = "HL_USER_FUNDING"``.  A
# retained payload that disagrees with what that producer would have written is
# not the settlement the capture describes.
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("captured", [999, True, "1", 1.0])
def test_a_capture_sample_count_that_is_not_the_retained_one_refuses(captured) -> None:
    """RED at ``fae07fa7``: every one of these was admitted beside ``n_samples=1``.

    ``999`` is a different count; ``true``, ``"1"`` and ``1.0`` all normalize to
    ``None`` in the producer, so none of them can stand behind a retained ``1``.
    """
    result = build_one(EVENT_A, capture(EVENT_A, delta={"nSamples": captured}))

    assert result.accepted is False
    assert result.candidate_bytes is None
    assert result.reason_code == exporter.CANDIDATE_CAPTURE_VALUE_MISMATCH
    assert "nSamples" in result.report["reason_detail"]


def test_a_capture_silent_about_its_sample_count_refuses_a_retained_one() -> None:
    """RED at ``fae07fa7``: an absent ``nSamples`` was admitted beside ``1``."""
    result = build_one(EVENT_A, capture(EVENT_A, drop=("nSamples",)))

    assert result.accepted is False
    assert result.reason_code == exporter.CANDIDATE_CAPTURE_VALUE_MISMATCH


@pytest.mark.parametrize("retained", [True, 1.0, "1"])
def test_a_retained_sample_count_that_is_not_a_whole_number_refuses(retained) -> None:
    """``True == 1`` and ``1.0 == 1`` in Python; neither is a sample count."""
    mistyped = replace(EVENT_A, n_samples=retained)
    result = build_one(mistyped, capture(mistyped, delta={"nSamples": 1}))

    assert result.accepted is False
    assert result.reason_code == exporter.CANDIDATE_CAPTURE_VALUE_MISMATCH


def test_a_matching_sample_count_is_admitted() -> None:
    """The positive control for the same binding: agreement still builds."""
    result = build_one(EVENT_A, capture(EVENT_A))

    assert result.accepted is True, result.report
    payload = json.loads(result.candidate_bytes)["production_candidate"][
        "settlement_events"
    ][0]["bridge_evidence"]["payload"]
    assert payload["n_samples"] == 1


def test_a_silent_capture_beside_a_null_retained_sample_count_is_admitted() -> None:
    """The producer's own normalization, not a "must be present" rule.

    A venue row without ``nSamples`` retains ``n_samples = None``, and that pair
    agrees.  Refusing it would refuse authentic own-account settlements.
    """
    unsampled = replace(EVENT_A, n_samples=None)
    result = build_one(unsampled, capture(unsampled))

    assert result.accepted is True, result.report


def test_a_retained_source_outside_the_production_normalization_refuses() -> None:
    """RED at ``fae07fa7``: ``NOT_HL_USER_FUNDING`` was admitted.

    The capture carries no source member, so nothing is read from it here: the
    producer stamps one constant for own-account funding, and a retained row
    that carries anything else did not come off that path.
    """
    foreign = replace(EVENT_A, source="NOT_HL_USER_FUNDING")
    result = build_one(foreign, capture(foreign))

    assert result.accepted is False
    assert result.candidate_bytes is None
    assert result.reason_code == exporter.CANDIDATE_CAPTURE_VALUE_MISMATCH
    assert "HL_USER_FUNDING" in result.report["reason_detail"]


# ---------------------------------------------------------------------------
# Instrument scope: capture, retained payload, retained row, witness, candidate
# ---------------------------------------------------------------------------


def test_a_retained_payload_outside_the_witnessed_instrument_refuses() -> None:
    """RED at ``fae07fa7``: an ETH settlement was admitted into a BTC candidate.

    Everything the round-2 candidate compared agrees: the outer retained row
    says BTC like the witness, and the capture's coin equals the retained
    payload's coin.  But both of those are ETH, so the admitted settlement is
    not in the scope the candidate publishes.
    """
    eth = replace(EVENT_A, symbol="ETH")
    result = build_one(eth, capture(eth), row_overrides={"symbol": SYMBOL})

    assert result.accepted is False
    assert result.candidate_bytes is None
    assert result.reason_code == exporter.CANDIDATE_SYMBOL_MISMATCH


def test_a_same_instrument_candidate_is_admitted_end_to_end() -> None:
    """The positive control: the refusal above is disagreement, not a coin.

    Nothing in the tool prefers BTC; an ETH settlement whose capture, payload,
    retained row, witness and candidate scope all say ETH still builds.
    """
    eth = replace(EVENT_A, symbol="ETH")
    product = "SYNTHETIC-DECLARED-ETH-PERP"
    result = build_one(
        eth,
        capture(eth),
        cover_overrides={"symbol": "ETH", "declared_product": product},
        declarations=declarations(product=product),
    )

    assert result.accepted is True, result.report
    candidate = json.loads(result.candidate_bytes)
    assert candidate["production_candidate"]["symbol_scope"] == "ETH"
    assert candidate["declarations"]["product"] == product


# ---------------------------------------------------------------------------
# GREEN: a real digest domain replaces UNAVAILABLE_PENDING_...
# ---------------------------------------------------------------------------


def test_production_candidate_uses_a_real_capture_byte_digest_domain() -> None:
    result = build()

    assert result.accepted is True, result.report
    candidate = json.loads(result.candidate_bytes)
    assert candidate["source_event_digest_domain"] == (
        "HL_FUNDING_OWN_ACCOUNT_CAPTURE_BYTES_SHA256_V1"
    )
    assert (
        candidate["source_event_digest_domain"]
        != exporter.PRODUCTION_MODE_UNAVAILABLE
    )
    assert candidate["source_class"] == "HL_FUNDING_VENUE_REPORTED_CASH_V1"
    assert candidate["synthetic_only"] is False
    assert candidate["declarations"] == declarations()
    assert result.report["production_mode"] == (
        "HL_FUNDING_OWN_ACCOUNT_CAPTURE_BYTES_SHA256_V1"
    )
    assert result.report["mode"] == "PRODUCTION"

    # The digest is SHA-256 over the exact captured bytes, computed here
    # independently of the tool.
    events = candidate["production_candidate"]["settlement_events"]
    digests = {row["binding"]["funding_event_id"]: row["binding"]["source_event_digest"]
               for row in events}
    assert digests == {
        ID_A: hashlib.sha256(capture(EVENT_A)).hexdigest(),
        ID_B: hashlib.sha256(capture(EVENT_B)).hexdigest(),
    }
    # ...and it is not the Bridge's normalized payload digest.
    assert digests[ID_A] != EVENT_A.digest
    assert digests[ID_B] != EVENT_B.digest


def test_production_candidate_is_still_not_an_accepted_record() -> None:
    candidate = json.loads(build().candidate_bytes)

    assert candidate["admission_status"] == (
        "REFUSED_PENDING_T0_REVIEW_AND_OWNER_RATIFICATION"
    )
    assert "not an accepted economic record" in candidate["not_an_accepted_record"]
    # Physically unusable as an MTC funding schedule: the selection keys the
    # consumer needs are absent at the root.
    for key in ("events", "schedule_id", "settlement_currency"):
        assert key not in candidate


def test_no_oracle_value_and_no_substitute_rate_reach_the_candidate() -> None:
    candidate = json.loads(build().candidate_bytes)

    for row in candidate["production_candidate"]["settlement_events"]:
        assert sorted(row["binding"]) == sorted(exporter.PRODUCTION_BINDING_KEYS)
        assert row["binding_notes"]["oracle_value_admitted"] is False
        assert row["binding_notes"]["oracle_value_back_calculated"] is False
        # The only rate anywhere is the venue's own retained per-event field.
        assert "oracle_price" not in row["binding"]
        assert "raw_rate" not in row["binding"]
        assert row["bridge_evidence"]["payload"]["funding_rate"] is not None


@pytest.mark.parametrize("key", ["oracle_price", "oracle_price_source", "oracle_px"])
def test_an_oracle_field_in_a_production_binding_is_refused(key: str) -> None:
    result = build(
        approved_event_bindings=[
            binding(EVENT_A, event_timestamp=TS_A, extra={key: "114296"}),
            binding(EVENT_B, event_timestamp=TS_B),
        ]
    )

    assert result.accepted is False
    assert result.reason_code == exporter.CANDIDATE_ORACLE_VALUE_REFUSED


@pytest.mark.parametrize("key", ["context_funding_rate", "funding_rate", "raw_rate"])
def test_a_substitute_rate_in_a_production_binding_is_refused(key: str) -> None:
    result = build(
        approved_event_bindings=[
            binding(EVENT_A, event_timestamp=TS_A, extra={key: "-0.0001234208"}),
            binding(EVENT_B, event_timestamp=TS_B),
        ]
    )

    assert result.accepted is False
    assert result.reason_code == exporter.CANDIDATE_CONTEXT_RATE_SUBSTITUTION_REFUSED


# ---------------------------------------------------------------------------
# Guards
# ---------------------------------------------------------------------------


def test_any_gap_in_the_declared_interval_refuses_the_whole_interval() -> None:
    result = build(coverage=coverage(gap_event_ids=["0xsynthetic0007"]))

    assert result.accepted is False
    assert result.reason_code == exporter.CANDIDATE_INTERVAL_COVERAGE_GAP
    assert result.candidate_bytes is None
    assert "whole interval is refused" in result.report["reason_detail"]


def test_two_settlements_on_one_account_coin_and_instant_refuse() -> None:
    twin = FundingEventRecord(
        event_id="0xsynthetic0003",
        symbol=SYMBOL,
        amount_usdc=-1.25,
        effective_ts=EVENT_A.effective_ts,
        source="HL_USER_FUNDING",
        attribution=FundingAttribution.ATTRIBUTED,
        funding_rate=EVENT_A.funding_rate,
        position_szi=EVENT_A.position_szi,
        n_samples=1,
    )
    result = build(
        retained_rows=[retained_row(EVENT_A), retained_row(twin)],
        approved_event_bindings=[
            binding(EVENT_A, event_timestamp=TS_A),
            binding(twin, event_timestamp=TS_A),
        ],
        coverage=coverage(
            expected_event_ids=[ID_A, twin.event_id],
            source_witnesses={
                ID_A: capture(EVENT_A).hex(),
                twin.event_id: capture(twin).hex(),
            },
        ),
    )

    assert result.accepted is False
    assert result.reason_code == exporter.CANDIDATE_SETTLEMENT_KEY_CONFLICT


def test_an_exact_duplicate_retained_settlement_refuses_instead_of_folding() -> None:
    """RED on ``81c3287d``: three rows with one exact duplicate were accepted.

    ``_fold_unique`` collapsed the identical pair before the settlement-key
    guard could see it, and the candidate published two settlement events.
    A3 whole-interval semantics: a duplicate is a defect in the evidence, so
    the whole candidate is refused rather than silently deduplicated.
    """
    result = build(
        retained_rows=[
            retained_row(EVENT_A),
            retained_row(EVENT_A),
            retained_row(EVENT_B),
        ]
    )

    assert result.accepted is False
    assert result.candidate_bytes is None
    assert result.reason_code == exporter.CANDIDATE_DUPLICATE_SETTLEMENT
    assert ID_A in result.report["reason_detail"]


def test_an_exact_duplicate_binding_refuses_instead_of_folding() -> None:
    result = build(
        approved_event_bindings=[
            binding(EVENT_A, event_timestamp=TS_A),
            binding(EVENT_A, event_timestamp=TS_A),
            binding(EVENT_B, event_timestamp=TS_B),
        ]
    )

    assert result.accepted is False
    assert result.reason_code == exporter.CANDIDATE_DUPLICATE_SETTLEMENT


def test_a_conflicting_duplicate_still_refuses_as_a_conflict() -> None:
    result = build(
        retained_rows=[
            retained_row(EVENT_A),
            retained_row(EVENT_A, attribution="UNATTRIBUTED"),
            retained_row(EVENT_B),
        ]
    )

    assert result.accepted is False
    assert result.reason_code == exporter.CANDIDATE_EVENT_CONFLICT


def test_a_binding_time_that_is_not_the_venue_row_time_refuses() -> None:
    result = build(
        approved_event_bindings=[
            binding(EVENT_A, event_timestamp="2026-09-12T12:15:00Z"),
            binding(EVENT_B, event_timestamp=TS_B),
        ]
    )

    assert result.accepted is False
    assert result.reason_code == exporter.CANDIDATE_SETTLEMENT_TIME_CONFLICT


def test_a_settled_sign_that_contradicts_the_payer_convention_refuses() -> None:
    """A LONG-payer positive rate on a long position must settle negative."""
    wrong = FundingEventRecord(
        event_id=ID_A,
        symbol=SYMBOL,
        amount_usdc=+1.25,  # credited while the convention says paid
        effective_ts=EVENT_A.effective_ts,
        source="HL_USER_FUNDING",
        attribution=FundingAttribution.ATTRIBUTED,
        funding_rate=0.0000125,
        position_szi=0.1,
        n_samples=1,
    )
    result = build(
        retained_rows=[retained_row(wrong), retained_row(EVENT_B)],
        approved_event_bindings=[
            binding(wrong, event_timestamp=TS_A, provenance_digest=capture_digest(wrong),
                    source_event_digest=capture_digest(wrong)),
            binding(EVENT_B, event_timestamp=TS_B),
        ],
        coverage=coverage(
            source_witnesses={
                ID_A: capture(wrong).hex(),
                ID_B: capture(EVENT_B).hex(),
            }
        ),
    )

    assert result.accepted is False
    assert result.reason_code == exporter.CANDIDATE_PAYER_SIGN_CONFLICT


def test_a_short_position_credit_is_admitted_under_the_same_convention() -> None:
    short = FundingEventRecord(
        event_id=ID_A,
        symbol=SYMBOL,
        amount_usdc=+1.25,
        effective_ts=EVENT_A.effective_ts,
        source="HL_USER_FUNDING",
        attribution=FundingAttribution.ATTRIBUTED,
        funding_rate=0.0000125,
        position_szi=-0.1,
        n_samples=1,
    )
    result = build(
        retained_rows=[retained_row(short), retained_row(EVENT_B)],
        approved_event_bindings=[
            binding(short, event_timestamp=TS_A),
            binding(EVENT_B, event_timestamp=TS_B),
        ],
        coverage=coverage(
            source_witnesses={
                ID_A: capture(short).hex(),
                ID_B: capture(EVENT_B).hex(),
            }
        ),
    )

    assert result.accepted is True, result.report


def test_capture_bytes_that_do_not_hash_to_the_declared_digest_refuse() -> None:
    result = build(coverage=coverage(source_witnesses={
        ID_A: capture(EVENT_B).hex(),  # swapped
        ID_B: capture(EVENT_A).hex(),
    }))

    assert result.accepted is False
    assert result.reason_code == exporter.CANDIDATE_BINDING_INVALID


def test_capture_bytes_not_bound_to_this_settlement_refuse() -> None:
    result = build(
        approved_event_bindings=[
            binding(EVENT_A, event_timestamp=TS_A, pointer="/delta/coin"),
            binding(EVENT_B, event_timestamp=TS_B),
        ]
    )

    assert result.accepted is False
    assert result.reason_code == exporter.CANDIDATE_CAPTURE_IDENTITY_UNBOUND


def test_a_capture_whose_identity_names_another_settlement_refuses() -> None:
    """The canonical ``/hash`` pointer must name *this* settlement."""
    other = capture(EVENT_B)
    digest = hashlib.sha256(other).hexdigest()
    result = build(
        approved_event_bindings=[
            binding(
                EVENT_A,
                event_timestamp=TS_A,
                source_event_digest=digest,
                provenance_digest=digest,
            ),
            binding(EVENT_B, event_timestamp=TS_B),
        ],
        coverage=coverage(
            source_witnesses={ID_A: other.hex(), ID_B: capture(EVENT_B).hex()}
        ),
    )

    assert result.accepted is False
    assert result.reason_code == exporter.CANDIDATE_CAPTURE_IDENTITY_UNBOUND


def test_reusing_the_bridge_payload_digest_as_a_capture_digest_refuses() -> None:
    result = build(
        approved_event_bindings=[
            binding(
                EVENT_A,
                event_timestamp=TS_A,
                source_event_digest=EVENT_A.digest,
                provenance_digest=EVENT_A.digest,
            ),
            binding(EVENT_B, event_timestamp=TS_B),
        ],
        coverage=coverage(
            source_witnesses={ID_A: b"{}".hex(), ID_B: capture(EVENT_B).hex()}
        ),
    )

    assert result.accepted is False
    assert result.reason_code == exporter.CANDIDATE_DIGEST_DOMAIN_CONFLATION


# ---------------------------------------------------------------------------
# A2 = B with M PENDING: log and sign a risk, never refuse
# ---------------------------------------------------------------------------


def test_the_magnitude_guard_logs_a_signed_risk_and_never_refuses() -> None:
    extreme = FundingEventRecord(
        event_id=ID_A,
        symbol=SYMBOL,
        amount_usdc=-12345.0,
        effective_ts=EVENT_A.effective_ts,
        source="HL_USER_FUNDING",
        attribution=FundingAttribution.ATTRIBUTED,
        funding_rate=0.5,
        position_szi=0.1,
        n_samples=1,
    )
    result = build(
        retained_rows=[retained_row(extreme), retained_row(EVENT_B)],
        approved_event_bindings=[
            binding(extreme, event_timestamp=TS_A),
            binding(EVENT_B, event_timestamp=TS_B),
        ],
        coverage=coverage(
            source_witnesses={
                ID_A: capture(extreme).hex(),
                ID_B: capture(EVENT_B).hex(),
            }
        ),
    )

    assert result.accepted is True, result.report
    markers = {row["signed_risk_id"]: row for row in result.report["signed_risk_markers"]}
    magnitude = markers["PATHD-RISK-FUNDING-MAGNITUDE-M-PENDING-V1"]
    assert magnitude["state"] == "M_PENDING"
    assert magnitude["largest_observed_event_id"] == ID_A
    assert magnitude["observed_absolute_rates"] == [repr(2.5e-05), repr(0.5)]
    assert "PATHD-RISK-FUNDING-ORACLE-BINDING-OPEN-V1" in markers
    assert markers["PATHD-RISK-FUNDING-ORACLE-BINDING-OPEN-V1"]["state"] == "OPEN"


# ---------------------------------------------------------------------------
# The two modes never leak into each other
# ---------------------------------------------------------------------------


def test_the_synthetic_evidence_kind_is_not_accepted_in_production_mode() -> None:
    result = build(coverage=coverage(evidence_kind=exporter.SYNTHETIC_EVIDENCE_KIND))

    assert result.accepted is False
    assert result.reason_code == exporter.CANDIDATE_PRODUCTION_EVIDENCE_UNAVAILABLE


def test_the_production_evidence_kind_is_not_accepted_in_synthetic_mode() -> None:
    synthetic_shaped = {
        key: value
        for key, value in coverage(
            evidence_kind=exporter.PRODUCTION_EVIDENCE_KIND
        ).items()
        if key in exporter.COVERAGE_KEYS
    }
    result = exporter.build_funding_candidate(
        [retained_row(EVENT_A)],
        [],
        synthetic_shaped,
        SCHEDULE_ID,
        START,
        END,
    )

    assert result.accepted is False
    assert result.reason_code == exporter.CANDIDATE_PRODUCTION_EVIDENCE_UNAVAILABLE
    assert result.report["production_mode"] == (
        "UNAVAILABLE_PENDING_SOURCE_EVENT_DIGEST_DOMAIN"
    )
    assert exporter.ACCEPTED_EVIDENCE_KINDS == (exporter.SYNTHETIC_EVIDENCE_KIND,)


def test_the_forward_only_bound_is_a_production_rule_only() -> None:
    """D1 synthetic mode is unchanged: it has no signature bound at all."""
    synthetic_shaped = {
        key: value
        for key, value in coverage(
            start=PRE_SIGNATURE_START, end=PRE_SIGNATURE_END
        ).items()
        if key in exporter.COVERAGE_KEYS
    }
    result = exporter.build_funding_candidate(
        [retained_row(EVENT_A)],
        [],
        synthetic_shaped,
        SCHEDULE_ID,
        PRE_SIGNATURE_START,
        PRE_SIGNATURE_END,
    )

    # It refuses for the synthetic evidence-kind reason, never the forward-only
    # one: the pre-signature interval itself is not a synthetic-mode defect.
    assert result.reason_code != exporter.CANDIDATE_FORWARD_ONLY_VIOLATION


@pytest.mark.parametrize("mode", ["production", "PROD", "", None, True, 1])
def test_no_near_miss_literal_selects_production_mode(mode) -> None:
    result = exporter.build_funding_candidate(
        [retained_row(EVENT_A)],
        [],
        coverage(),
        SCHEDULE_ID,
        START,
        END,
        mode=mode,
    )

    assert result.accepted is False
    assert result.reason_code == exporter.CANDIDATE_MODE_INVALID


def test_synthetic_mode_takes_no_declarations() -> None:
    result = exporter.build_funding_candidate(
        [retained_row(EVENT_A)],
        [],
        coverage(),
        SCHEDULE_ID,
        START,
        END,
        declarations=declarations(),
    )

    assert result.accepted is False
    assert result.reason_code == exporter.CANDIDATE_DECLARATION_MISMATCH


def test_determinism_of_the_production_candidate() -> None:
    first = build()
    second = build()

    assert first.candidate_bytes == second.candidate_bytes
    assert first.candidate_sha256 == second.candidate_sha256
    assert first.report == second.report
    assert first.candidate_sha256 == hashlib.sha256(first.candidate_bytes).hexdigest()


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def run_cli(tmp_path: Path, *, snapshot: Path, staging: Path, packet: bytes | None = None,
            extra: list[str] | None = None) -> int:
    bindings_path = tmp_path / "production-bindings.json"
    bindings_path.write_bytes(packet_bytes() if packet is None else packet)
    return exporter.main(
        [
            "--snapshot", str(snapshot),
            "--bindings", str(bindings_path),
            "--symbol", SYMBOL,
            "--start", START,
            "--end", END,
            "--schedule-id", SCHEDULE_ID,
            "--staging", str(staging),
            "--mode", "PRODUCTION",
            *(extra or []),
        ]
    )


DECLARED_FLAGS = [
    "--declared-account", DECLARED_ACCOUNT,
    "--declared-product", DECLARED_PRODUCT,
    "--declared-interval", DECLARED_INTERVAL,
]


def test_cli_production_without_declarations_refuses_and_stages_only_a_report(
    tmp_path, snapshot
):
    staging = tmp_path / "staging"

    code = run_cli(tmp_path, snapshot=snapshot, staging=staging)

    assert code != 0
    assert sorted(child.name for child in staging.iterdir()) == [
        exporter.REPORT_FILENAME
    ]
    report = json.loads((staging / exporter.REPORT_FILENAME).read_bytes())
    assert report["reason_code"] == "CANDIDATE_DECLARATION_UNSPECIFIED"
    assert report["mode"] == "PRODUCTION"
    assert report["production_mode"] == (
        "HL_FUNDING_OWN_ACCOUNT_CAPTURE_BYTES_SHA256_V1"
    )


def test_cli_production_with_declarations_stages_a_candidate(tmp_path, snapshot):
    before = hashlib.sha256(snapshot.read_bytes()).hexdigest()
    staging = tmp_path / "staging"

    code = run_cli(tmp_path, snapshot=snapshot, staging=staging, extra=DECLARED_FLAGS)

    assert code == 0
    assert sorted(child.name for child in staging.iterdir()) == sorted(
        [
            exporter.CANDIDATE_FILENAME,
            exporter.SIDECAR_FILENAME,
            exporter.REPORT_FILENAME,
        ]
    )
    candidate = (staging / exporter.CANDIDATE_FILENAME).read_bytes()
    sidecar = (staging / exporter.SIDECAR_FILENAME).read_bytes()
    assert sidecar == hashlib.sha256(candidate).hexdigest().encode("ascii") + b"\n"
    assert json.loads(candidate)["declarations"] == declarations()

    # The snapshot is untouched and no companion appeared beside it.
    assert hashlib.sha256(snapshot.read_bytes()).hexdigest() == before
    assert [
        child.name
        for child in snapshot.parent.iterdir()
        if child.name.startswith(snapshot.name) and child.name != snapshot.name
    ] == []


def test_cli_production_refuses_a_snapshot_the_capture_contradicts(tmp_path):
    """The same capture binding on the materialize path, not the pure call.

    The retained rows here come out of a real Store snapshot through
    ``list_funding_events``/``get_funding_event_payload``, so this proves the
    binding holds for the payloads the tool actually reads rather than for
    hand-built rows: the stored settlement counts two samples, its capture in
    the packet states one, and the whole interval refuses with no candidate and
    no sidecar staged.
    """
    resampled = replace(EVENT_A, n_samples=2)
    snapshot = write_snapshot(tmp_path / "offline" / "snapshot.db", resampled, EVENT_B)
    staging = tmp_path / "staging"

    code = run_cli(tmp_path, snapshot=snapshot, staging=staging, extra=DECLARED_FLAGS)

    assert code != 0
    assert sorted(child.name for child in staging.iterdir()) == [
        exporter.REPORT_FILENAME
    ]
    report = json.loads((staging / exporter.REPORT_FILENAME).read_bytes())
    assert report["reason_code"] == exporter.CANDIDATE_CAPTURE_VALUE_MISMATCH
    assert report["accepted"] is False


def test_cli_production_refuses_a_snapshot_source_the_producer_never_writes(tmp_path):
    """The source normalization on the materialize path."""
    foreign = replace(EVENT_A, source="NOT_HL_USER_FUNDING")
    snapshot = write_snapshot(tmp_path / "offline" / "snapshot.db", foreign, EVENT_B)
    staging = tmp_path / "staging"

    code = run_cli(tmp_path, snapshot=snapshot, staging=staging, extra=DECLARED_FLAGS)

    assert code != 0
    report = json.loads((staging / exporter.REPORT_FILENAME).read_bytes())
    assert report["reason_code"] == exporter.CANDIDATE_CAPTURE_VALUE_MISMATCH
    assert "HL_USER_FUNDING" in report["reason_detail"]


def test_cli_production_refuses_a_synthetic_packet_version(tmp_path, snapshot):
    staging = tmp_path / "staging"
    packet = json.loads(packet_bytes())
    packet["packet_version"] = exporter.PACKET_VERSION

    code = run_cli(
        tmp_path,
        snapshot=snapshot,
        staging=staging,
        packet=json.dumps(packet, sort_keys=True).encode("utf-8"),
        extra=DECLARED_FLAGS,
    )

    assert code != 0
    report = json.loads((staging / exporter.REPORT_FILENAME).read_bytes())
    assert report["reason_code"] == exporter.CANDIDATE_PACKET_INVALID
