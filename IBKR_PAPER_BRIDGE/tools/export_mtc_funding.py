"""Offline, synthetic-only MTC funding candidate materializer (P0-12 D1).

What this tool is
-----------------
One offline CLI plus one pure function. Given

* a named, quiescent, owner-supplied **offline snapshot** of a Bridge database
  that already carries retained funding payloads (schema v10), and
* a separately source-verified **binding packet** carrying, per funding event,
  the eight current MTC input fields plus an explicit whole-interval
  completion witness,

it stages a *synthetic candidate* under an external directory, or it refuses.

What this tool is NOT
---------------------
It is **not** a production record producer. Everything it emits is labelled
``SYNTHETIC_ONLY`` and is wrapped in a shape that current MTC record selection
physically cannot consume: the candidate root carries no ``schedule_id``, no
``events`` and no ``settlement_currency``, so
``EconomicRecords.funding_schedule_id`` raises and
``ExecutionEconomics._resolve_funding`` refuses with its own
``REFUSED_MISSING_FUNDING_EVENT``. There is no mode switch, callback, boolean
gate or magic literal that turns a synthetic candidate into a production
record: the only accepted completion-evidence kind is
:data:`SYNTHETIC_EVIDENCE_KIND`, and production mode stays
:data:`PRODUCTION_MODE_UNAVAILABLE` until the real binding-packet schema and the
``source_event_digest`` byte domain are approved and implemented elsewhere.

It also activates nothing. It never calls ``Store.initialize()``, never
migrates, checkpoints or backfills, never writes to a database, and never
copies a live one. ``Store.__init__``/``Store.conn`` are deliberately unused,
because opening through them would create the file, set
``PRAGMA journal_mode=WAL`` and ``PRAGMA foreign_keys=ON`` — all writes against
a snapshot. Instead :class:`_ReadOnlySnapshot` composes the *actual* Store
retrieval methods onto an explicitly read-only, immutable SQLite connection, so
the retained-payload verification and its reason codes are inherited rather
than re-implemented.

Evidence boundaries this tool does not cross
--------------------------------------------
* Caller facts are synthetic fixtures. A successful candidate says nothing
  about real-world completeness, a real account, or a real payment.
* ``payload_digest`` stays the normalized Bridge integrity digest. It is never
  renamed to, reused as, or compared equal to a ``source_event_digest``; a
  binding that reuses it is refused.
* A retained payload's ``effective_ts``/``funding_rate`` are Bridge
  observations, not authoritative settlement time/rate. They are carried as
  labelled evidence beside — never merged into — the explicit synthetic
  binding.
* A ``coverage`` flag alone proves nothing. An explicit inventory of every
  event in the interval, an account scope and a witness identity are required,
  and every retained/bound/inventoried identity must reconcile exactly.
* Unknown, out-of-interval, uninventoried and out-of-scope identities are
  always named in the report. Nothing disappears silently.

Invocation
----------
    python IBKR_PAPER_BRIDGE/tools/export_mtc_funding.py \\
        --snapshot OFFLINE_SCHEMA10_COPY --bindings VERIFIED_LOCAL_PACKET \\
        --symbol BTC --start UTC --end UTC --schedule-id ID \\
        --staging NEW_NONEXISTENT_DIRECTORY

The staging target must be external to the Bridge repository and both input
paths, have no symlink/reparse-point ancestry, and not exist yet. Exit code 0
atomically publishes ``funding_candidate_synthetic.json``, its detached
``.sha256`` sidecar and ``materialization_report.json``. Any refusal exits
non-zero, stages the report only, and never writes a candidate or sidecar.
All three staged outputs are deterministic: identical input bytes produce
identical output bytes, and no clock value reaches any artifact.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import re
import sqlite3
import stat
import sys
import tempfile
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from decimal import Decimal
from pathlib import Path
from typing import Any, Mapping, Sequence

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from bridge.engine.types import canonical_reconcile_json, reconcile_digest
from bridge.store.db import ReconcileConflictError, Store

TOOL_NAME = "export_mtc_funding"

# --- staged artifact names -------------------------------------------------
CANDIDATE_FILENAME = "funding_candidate_synthetic.json"
SIDECAR_FILENAME = "funding_candidate_synthetic.json.sha256"
REPORT_FILENAME = "materialization_report.json"

# --- synthetic-only labels -------------------------------------------------
ARTIFACT_KIND = "SYNTHETIC_FUNDING_CANDIDATE_V1"
REPORT_KIND = "SYNTHETIC_FUNDING_CANDIDATE_REPORT_V1"
PACKET_VERSION = "SYNTHETIC_FUNDING_BINDING_PACKET_V1"
SYNTHETIC_EVIDENCE_KIND = "SYNTHETIC_FIXTURE"
ACCEPTED_EVIDENCE_KINDS = (SYNTHETIC_EVIDENCE_KIND,)
SOURCE_EVENT_DIGEST_DOMAIN = "SYNTHETIC_SOURCE_EVENT_DIGEST_V1"
BRIDGE_PAYLOAD_DIGEST_DOMAIN = "BRIDGE_NORMALIZED_RECONCILE_DIGEST"
NUMERIC_REPRESENTATION = "DECIMAL_STRING_V1"
SETTLEMENT_SOURCE = "SYNTHETIC_BINDING_ONLY"
ADMISSION_STATUS = "REFUSED_SYNTHETIC_ONLY_NOT_A_PRODUCTION_RECORD"
PRODUCTION_MODE_UNAVAILABLE = "UNAVAILABLE_PENDING_SOURCE_EVENT_DIGEST_DOMAIN"
NOT_A_PRODUCTION_RECORD = (
    "Synthetic test scaffolding. This is not an accepted economic record, not "
    "venue evidence, and not a claim about any real account, interval or "
    "payment. It must never be installed as an MTC funding schedule."
)
APPROVED_PAYER = "LONG"

# --- outcome and refusal codes --------------------------------------------
SYNTHETIC_CANDIDATE_BUILT = "SYNTHETIC_CANDIDATE_BUILT"
PAYLOAD_RETAINED = "FUNDING_PAYLOAD_RETAINED"

CANDIDATE_INPUT_INVALID = "CANDIDATE_INPUT_INVALID"
CANDIDATE_INTERVAL_INVALID = "CANDIDATE_INTERVAL_INVALID"
CANDIDATE_TIMESTAMP_INVALID = "CANDIDATE_TIMESTAMP_INVALID"
CANDIDATE_COVERAGE_INVALID = "CANDIDATE_COVERAGE_INVALID"
CANDIDATE_PRODUCTION_EVIDENCE_UNAVAILABLE = (
    "CANDIDATE_PRODUCTION_EVIDENCE_UNAVAILABLE"
)
CANDIDATE_BINDING_INVALID = "CANDIDATE_BINDING_INVALID"
CANDIDATE_BINDING_OUT_OF_INTERVAL = "CANDIDATE_BINDING_OUT_OF_INTERVAL"
CANDIDATE_BINDING_UNKNOWN_EVENT = "CANDIDATE_BINDING_UNKNOWN_EVENT"
CANDIDATE_EVENT_UNBOUND = "CANDIDATE_EVENT_UNBOUND"
CANDIDATE_EVENT_CONFLICT = "CANDIDATE_EVENT_CONFLICT"
CANDIDATE_INVENTORY_MISMATCH = "CANDIDATE_INVENTORY_MISMATCH"
CANDIDATE_INVENTORY_INCOMPLETE = "CANDIDATE_INVENTORY_INCOMPLETE"
CANDIDATE_ATTRIBUTION_SCOPE_MISMATCH = "CANDIDATE_ATTRIBUTION_SCOPE_MISMATCH"
CANDIDATE_SYMBOL_MISMATCH = "CANDIDATE_SYMBOL_MISMATCH"
CANDIDATE_PAYLOAD_UNAVAILABLE = "CANDIDATE_PAYLOAD_UNAVAILABLE"
CANDIDATE_NONFINITE_VALUE = "CANDIDATE_NONFINITE_VALUE"
CANDIDATE_PRECISION_UNREPRESENTABLE = "CANDIDATE_PRECISION_UNREPRESENTABLE"
CANDIDATE_DIGEST_DOMAIN_CONFLATION = "CANDIDATE_DIGEST_DOMAIN_CONFLATION"
CANDIDATE_PACKET_INVALID = "CANDIDATE_PACKET_INVALID"
CANDIDATE_SNAPSHOT_UNAVAILABLE = "CANDIDATE_SNAPSHOT_UNAVAILABLE"
CANDIDATE_SNAPSHOT_NOT_QUIESCENT = "CANDIDATE_SNAPSHOT_NOT_QUIESCENT"
CANDIDATE_SNAPSHOT_UNREADABLE = "CANDIDATE_SNAPSHOT_UNREADABLE"
CANDIDATE_SNAPSHOT_DRIFTED = "CANDIDATE_SNAPSHOT_DRIFTED"
CANDIDATE_STAGING_NOT_EMPTY = "CANDIDATE_STAGING_NOT_EMPTY"
CANDIDATE_STAGING_FAILED = "CANDIDATE_STAGING_FAILED"
CANDIDATE_STAGING_UNSAFE = "CANDIDATE_STAGING_UNSAFE"

# --- closed input domains --------------------------------------------------
RETAINED_ROW_KEYS = (
    "attribution",
    "event_id",
    "ledger_effective_ts",
    "payload",
    "payload_digest",
    "payload_reason",
    "symbol",
)
BINDING_KEYS = (
    "event_timestamp",
    "funding_event_id",
    "oracle_price",
    "oracle_price_source",
    "positive_rate_payer",
    "provenance",
    "raw_rate",
    "source_event_digest",
)
PROVENANCE_KEYS = (
    "evidence_kind",
    "extraction_method",
    "source_locator",
    "source_sha256",
    "source_title",
)
SOURCE_BINDING_KEYS = (
    "event_timestamp",
    "funding_event_id",
    "oracle_price",
    "oracle_price_source",
    "positive_rate_payer",
    "raw_rate",
)
COVERAGE_KEYS = (
    "account_scope",
    "complete",
    "evidence_kind",
    "expected_event_ids",
    "interval_end_exclusive",
    "interval_start_inclusive",
    "symbol",
    "source_witnesses",
    "unattributed_event_ids",
    "witness_identity",
)
PACKET_KEYS = ("bindings", "coverage", "packet_version")

EVIDENCE_LIMITATIONS = (
    "SYNTHETIC_ONLY: every caller fact in this run is a synthetic fixture.",
    "This artifact does not verify real-world interval completeness.",
    "Authoritative settlement time and rate are not established; the binding "
    "values are synthetic and the Bridge payload values are normalized "
    "observations only.",
    "The production binding-packet schema and the source_event_digest byte "
    "domain are unresolved; production mode is unavailable.",
    "This artifact is not an accepted economic record and is not admitted by "
    "any production selection path.",
)

_LOWER_SHA256 = re.compile(r"\A[0-9a-f]{64}\Z")
_DECIMAL_LITERAL = re.compile(r"\A-?(?:0|[1-9][0-9]*)(?:\.[0-9]+)?\Z")
_RFC3339_UTC = re.compile(
    r"\A(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})"
    r"T(?P<hour>\d{2}):(?P<minute>\d{2}):(?P<second>\d{2})"
    r"(?:\.(?P<fraction>\d+))?"
    r"(?P<offset>Z|[+-]\d{2}:\d{2})\Z"
)
_EPOCH = datetime(1970, 1, 1, tzinfo=UTC)


class _Refusal(Exception):
    """One closed refusal carrying the code that will reach the report."""

    def __init__(self, code: str, detail: str, **facts: Any) -> None:
        self.code = code
        self.detail = detail
        self.facts = facts
        super().__init__(f"{code}: {detail}")


@dataclass(frozen=True)
class _Instant:
    """An exact UTC instant plus the caller's own subsecond spelling.

    ``seconds`` is whole seconds since the epoch and ``fraction`` is an exact
    :class:`~decimal.Decimal` below one second, so arbitrary subsecond
    precision survives and ordering never degrades to a lexicographic
    comparison of fractional digits (``.1`` and ``.10`` are one instant).
    ``text`` is the canonical ``Z`` spelling with the original digits intact.
    """

    seconds: int
    fraction: Decimal
    text: str

    @property
    def sort_key(self) -> tuple[int, Decimal]:
        return (self.seconds, self.fraction)


@dataclass(frozen=True)
class CandidateResult:
    """Either synthetic candidate bytes plus a non-admission report, or a
    refusal report and no record bytes."""

    accepted: bool
    reason_code: str
    report: dict[str, Any]
    candidate_bytes: bytes | None = None
    candidate_sha256: str | None = None


# ---------------------------------------------------------------------------
# Exact scalar parsing
# ---------------------------------------------------------------------------


def _parse_instant(value: Any, field: str) -> _Instant:
    if not isinstance(value, str):
        raise _Refusal(
            CANDIDATE_TIMESTAMP_INVALID, f"{field} must be an RFC 3339 UTC string"
        )
    match = _RFC3339_UTC.fullmatch(value)
    if match is None:
        raise _Refusal(
            CANDIDATE_TIMESTAMP_INVALID,
            f"{field} must be an explicit aware RFC 3339 timestamp, got {value!r}",
        )
    parts = match.groupdict()
    try:
        stamp = datetime(
            int(parts["year"]),
            int(parts["month"]),
            int(parts["day"]),
            int(parts["hour"]),
            int(parts["minute"]),
            int(parts["second"]),
            tzinfo=UTC,
        )
    except ValueError as exc:
        raise _Refusal(CANDIDATE_TIMESTAMP_INVALID, f"{field} is not a real instant: {exc}")
    offset = parts["offset"]
    if offset != "Z":
        sign = -1 if offset[0] == "-" else 1
        stamp -= timedelta(
            minutes=sign * (int(offset[1:3]) * 60 + int(offset[4:6]))
        )
    fraction_digits = parts["fraction"]
    spelled = stamp.strftime("%Y-%m-%dT%H:%M:%S")
    if fraction_digits is not None:
        spelled = f"{spelled}.{fraction_digits}"
    return _Instant(
        seconds=int((stamp - _EPOCH) // timedelta(seconds=1)),
        fraction=Decimal(0) if fraction_digits is None else Decimal(f"0.{fraction_digits}"),
        text=f"{spelled}Z",
    )


def _parse_decimal(value: Any, field: str) -> tuple[str, Decimal]:
    """Accept only an unambiguous decimal literal, preserving its exact form.

    A binary ``float`` has already lost the caller's decimal meaning, so it is
    refused rather than re-rounded under a billing rule this tool has no
    authority to choose.
    """
    if isinstance(value, bool):
        raise _Refusal(CANDIDATE_BINDING_INVALID, f"{field} must be a decimal literal")
    if isinstance(value, float):
        raise _Refusal(
            CANDIDATE_PRECISION_UNREPRESENTABLE,
            f"{field} was supplied as a binary float; supply an exact decimal "
            "literal string instead of a value whose decimal meaning is already lost",
        )
    if isinstance(value, int):
        text = str(value)
    elif isinstance(value, str):
        text = value
    else:
        raise _Refusal(CANDIDATE_BINDING_INVALID, f"{field} must be a decimal literal")
    if _DECIMAL_LITERAL.fullmatch(text) is None:
        raise _Refusal(
            CANDIDATE_BINDING_INVALID,
            f"{field} must be a plain decimal literal, got {text!r}",
        )
    return text, Decimal(text)


def _require_text(value: Any, field: str, code: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise _Refusal(code, f"{field} must be a non-empty string")
    return value


def _require_digest(value: Any, field: str, code: str) -> str:
    if not isinstance(value, str) or _LOWER_SHA256.fullmatch(value) is None:
        raise _Refusal(code, f"{field} must be a lower-case SHA-256 hex digest")
    return value


def _require_closed_mapping(value: Any, keys: Sequence[str], label: str, code: str) -> dict:
    if not isinstance(value, Mapping):
        raise _Refusal(code, f"{label} must be an object")
    if tuple(sorted(value)) != tuple(sorted(keys)):
        raise _Refusal(
            code,
            f"{label} must carry exactly {sorted(keys)}, got {sorted(value)}",
        )
    return dict(value)


def _require_sequence(value: Any, label: str) -> list:
    if isinstance(value, (str, bytes)) or isinstance(value, Mapping):
        raise _Refusal(CANDIDATE_INPUT_INVALID, f"{label} must be a sequence")
    if not isinstance(value, Sequence):
        raise _Refusal(CANDIDATE_INPUT_INVALID, f"{label} must be a sequence")
    return list(value)


def _require_id_list(value: Any, field: str) -> list[str]:
    if isinstance(value, (str, bytes)) or not isinstance(value, Sequence):
        raise _Refusal(CANDIDATE_COVERAGE_INVALID, f"{field} must be a list of ids")
    ids: list[str] = []
    for item in value:
        ids.append(_require_text(item, f"{field} entry", CANDIDATE_COVERAGE_INVALID))
    if len(set(ids)) != len(ids):
        raise _Refusal(CANDIDATE_COVERAGE_INVALID, f"{field} repeats an identity")
    return ids


def _require_source_witnesses(value: Any) -> dict[str, str]:
    if not isinstance(value, Mapping):
        raise _Refusal(
            CANDIDATE_COVERAGE_INVALID,
            "coverage.source_witnesses must map event ids to exact synthetic source bytes",
        )
    witnesses: dict[str, str] = {}
    for raw_event_id, raw_hex in value.items():
        event_id = _require_text(
            raw_event_id,
            "coverage.source_witnesses event id",
            CANDIDATE_COVERAGE_INVALID,
        )
        if (
            not isinstance(raw_hex, str)
            or not raw_hex
            or len(raw_hex) % 2
            or re.fullmatch(r"[0-9a-f]+", raw_hex) is None
        ):
            raise _Refusal(
                CANDIDATE_COVERAGE_INVALID,
                f"coverage.source_witnesses[{event_id!r}] must be lower-case hex source bytes",
            )
        witnesses[event_id] = raw_hex
    return witnesses


def _assert_finite(value: Any, field: str) -> None:
    if isinstance(value, bool) or value is None:
        return
    if isinstance(value, float) and not math.isfinite(value):
        raise _Refusal(CANDIDATE_NONFINITE_VALUE, f"{field} is not a finite number")


# ---------------------------------------------------------------------------
# Input validation — the pure function trusts no caller
# ---------------------------------------------------------------------------


def _validate_coverage(
    coverage: Any, start: _Instant, end: _Instant
) -> dict[str, Any]:
    witness = _require_closed_mapping(
        coverage, COVERAGE_KEYS, "coverage", CANDIDATE_COVERAGE_INVALID
    )
    kind = witness["evidence_kind"]
    if kind not in ACCEPTED_EVIDENCE_KINDS:
        raise _Refusal(
            CANDIDATE_PRODUCTION_EVIDENCE_UNAVAILABLE,
            "the production completion-evidence contract is not approved or "
            f"implemented; only {list(ACCEPTED_EVIDENCE_KINDS)} is accepted, got {kind!r}",
        )
    if witness["complete"] is not True:
        raise _Refusal(
            CANDIDATE_COVERAGE_INVALID,
            "coverage.complete must be the boolean True; an incomplete or "
            "non-boolean assertion cannot prove whole-interval coverage",
        )
    witness_start = _parse_instant(
        witness["interval_start_inclusive"], "coverage.interval_start_inclusive"
    )
    witness_end = _parse_instant(
        witness["interval_end_exclusive"], "coverage.interval_end_exclusive"
    )
    if witness_start.sort_key != start.sort_key or witness_end.sort_key != end.sort_key:
        raise _Refusal(
            CANDIDATE_COVERAGE_INVALID,
            "the witnessed interval is not the requested interval",
        )
    return {
        "account_scope": _require_text(
            witness["account_scope"], "coverage.account_scope", CANDIDATE_COVERAGE_INVALID
        ),
        "complete": True,
        "evidence_kind": kind,
        "expected_event_ids": _require_id_list(
            witness["expected_event_ids"], "coverage.expected_event_ids"
        ),
        "interval_end_exclusive": end.text,
        "interval_start_inclusive": start.text,
        "symbol": _require_text(
            witness["symbol"], "coverage.symbol", CANDIDATE_COVERAGE_INVALID
        ),
        "source_witnesses": _require_source_witnesses(witness["source_witnesses"]),
        "unattributed_event_ids": _require_id_list(
            witness["unattributed_event_ids"], "coverage.unattributed_event_ids"
        ),
        "witness_identity": _require_text(
            witness["witness_identity"],
            "coverage.witness_identity",
            CANDIDATE_COVERAGE_INVALID,
        ),
    }


def _validate_retained_row(raw: Any) -> dict[str, Any]:
    row = _require_closed_mapping(
        raw, RETAINED_ROW_KEYS, "retained row", CANDIDATE_INPUT_INVALID
    )
    event_id = _require_text(row["event_id"], "retained row event_id", CANDIDATE_INPUT_INVALID)
    symbol = _require_text(row["symbol"], "retained row symbol", CANDIDATE_INPUT_INVALID)
    attribution = _require_text(
        row["attribution"], "retained row attribution", CANDIDATE_INPUT_INVALID
    )
    digest = _require_digest(
        row["payload_digest"], "retained row payload_digest", CANDIDATE_INPUT_INVALID
    )
    reason = _require_text(
        row["payload_reason"], "retained row payload_reason", CANDIDATE_INPUT_INVALID
    )
    ledger = _require_text(
        row["ledger_effective_ts"],
        "retained row ledger_effective_ts",
        CANDIDATE_INPUT_INVALID,
    )
    payload = row["payload"]
    if payload is not None and not isinstance(payload, Mapping):
        raise _Refusal(CANDIDATE_INPUT_INVALID, "retained row payload must be an object or null")
    if payload is None and reason == PAYLOAD_RETAINED:
        raise _Refusal(
            CANDIDATE_INPUT_INVALID,
            f"retained row {event_id} claims a retained payload but carries none",
        )
    if payload is not None and reason != PAYLOAD_RETAINED:
        raise _Refusal(
            CANDIDATE_INPUT_INVALID,
            f"retained row {event_id} carries a payload under reason {reason}",
        )
    return {
        "attribution": attribution,
        "event_id": event_id,
        "ledger_effective_ts": ledger,
        "ledger_instant": _parse_instant(ledger, f"retained row {event_id} ledger_effective_ts"),
        "payload": None if payload is None else dict(payload),
        "payload_digest": digest,
        "payload_reason": reason,
        "symbol": symbol,
    }


def _validate_provenance(raw: Any, event_id: str) -> dict[str, str]:
    provenance = _require_closed_mapping(
        raw, PROVENANCE_KEYS, f"binding {event_id} provenance", CANDIDATE_BINDING_INVALID
    )
    kind = provenance["evidence_kind"]
    if kind not in ACCEPTED_EVIDENCE_KINDS:
        raise _Refusal(
            CANDIDATE_PRODUCTION_EVIDENCE_UNAVAILABLE,
            f"binding {event_id} provenance.evidence_kind {kind!r} is not an "
            "approved production evidence kind",
        )
    return {
        "evidence_kind": kind,
        "extraction_method": _require_text(
            provenance["extraction_method"],
            f"binding {event_id} provenance.extraction_method",
            CANDIDATE_BINDING_INVALID,
        ),
        "source_locator": _require_text(
            provenance["source_locator"],
            f"binding {event_id} provenance.source_locator",
            CANDIDATE_BINDING_INVALID,
        ),
        "source_sha256": _require_digest(
            provenance["source_sha256"],
            f"binding {event_id} provenance.source_sha256",
            CANDIDATE_BINDING_INVALID,
        ),
        "source_title": _require_text(
            provenance["source_title"],
            f"binding {event_id} provenance.source_title",
            CANDIDATE_BINDING_INVALID,
        ),
    }


def _validate_binding(raw: Any) -> dict[str, Any]:
    fields = _require_closed_mapping(
        raw, BINDING_KEYS, "binding", CANDIDATE_BINDING_INVALID
    )
    event_id = _require_text(
        fields["funding_event_id"], "binding funding_event_id", CANDIDATE_BINDING_INVALID
    )
    instant = _parse_instant(fields["event_timestamp"], f"binding {event_id} event_timestamp")
    payer = fields["positive_rate_payer"]
    if payer != APPROVED_PAYER:
        raise _Refusal(
            CANDIDATE_BINDING_INVALID,
            f"binding {event_id} positive_rate_payer must be the approved "
            f"{APPROVED_PAYER} convention, got {payer!r}",
        )
    raw_rate_text, _ = _parse_decimal(fields["raw_rate"], f"binding {event_id} raw_rate")
    price_text, price = _parse_decimal(
        fields["oracle_price"], f"binding {event_id} oracle_price"
    )
    if price <= 0:
        raise _Refusal(
            CANDIDATE_BINDING_INVALID, f"binding {event_id} oracle_price must be positive"
        )
    body = {
        "event_timestamp": instant.text,
        "funding_event_id": event_id,
        "oracle_price": price_text,
        "oracle_price_source": _require_text(
            fields["oracle_price_source"],
            f"binding {event_id} oracle_price_source",
            CANDIDATE_BINDING_INVALID,
        ),
        "positive_rate_payer": payer,
        "provenance": _validate_provenance(fields["provenance"], event_id),
        "raw_rate": raw_rate_text,
        "source_event_digest": _require_digest(
            fields["source_event_digest"],
            f"binding {event_id} source_event_digest",
            CANDIDATE_BINDING_INVALID,
        ),
    }
    return {
        "event_id": event_id,
        "instant": instant,
        "source_fields": {key: body[key] for key in SOURCE_BINDING_KEYS},
        "body": body,
    }


def _verify_source_witness(binding: Mapping[str, Any], source_hex: str) -> None:
    event_id = binding["event_id"]
    source = bytes.fromhex(source_hex)
    digest = hashlib.sha256(source).hexdigest()
    provenance_digest = binding["body"]["provenance"]["source_sha256"]
    if provenance_digest != digest:
        raise _Refusal(
            CANDIDATE_BINDING_INVALID,
            f"binding {event_id} provenance.source_sha256 does not hash its explicit source bytes",
        )
    if binding["body"]["source_event_digest"] != digest:
        raise _Refusal(
            CANDIDATE_BINDING_INVALID,
            f"binding {event_id} source_event_digest does not hash its explicit source bytes",
        )
    try:
        decoded = json.loads(source.decode("utf-8"))
    except (UnicodeDecodeError, ValueError) as exc:
        raise _Refusal(
            CANDIDATE_BINDING_INVALID,
            f"binding {event_id} source bytes are not canonical UTF-8 JSON: {exc}",
        ) from exc
    if not isinstance(decoded, Mapping) or tuple(sorted(decoded)) != tuple(
        sorted(SOURCE_BINDING_KEYS)
    ):
        raise _Refusal(
            CANDIDATE_BINDING_INVALID,
            f"binding {event_id} source witness does not describe this binding's explicit fields",
        )
    if canonical_reconcile_json(decoded).encode("utf-8") != source:
        raise _Refusal(
            CANDIDATE_BINDING_INVALID,
            f"binding {event_id} source bytes are not the exact canonical encoding",
        )
    if dict(decoded) != binding["source_fields"]:
        raise _Refusal(
            CANDIDATE_BINDING_INVALID,
            f"binding {event_id} source witness does not describe this binding",
        )


def _fold_unique(items: list[dict[str, Any]], key: str, label: str) -> dict[str, dict[str, Any]]:
    """Duplicate identical entries collapse to one; any conflict refuses."""
    folded: dict[str, dict[str, Any]] = {}
    for item in items:
        identity = item[key]
        existing = folded.get(identity)
        if existing is None:
            folded[identity] = item
            continue
        if canonical_reconcile_json(_comparable(existing)) != canonical_reconcile_json(
            _comparable(item)
        ):
            raise _Refusal(
                CANDIDATE_EVENT_CONFLICT,
                f"conflicting {label} for event {identity}",
            )
    return folded


def _comparable(item: Mapping[str, Any]) -> dict[str, Any]:
    """A JSON-comparable view; ``_Instant`` compares by its exact spelling."""
    return {
        key: (value.text if isinstance(value, _Instant) else value)
        for key, value in item.items()
    }


def _verify_retained_payload(row: Mapping[str, Any]) -> dict[str, Any]:
    """Re-prove one retained payload independently of whoever supplied it.

    The checks and the codes they raise mirror
    ``Store._decode_funding_payload`` exactly, so a caller cannot launder a
    tampered payload past the exporter by pre-approving it.
    """
    event_id = row["event_id"]
    payload = row["payload"]
    if payload is None:
        raise _Refusal(
            row["payload_reason"],
            f"no usable retained payload for {event_id}; it stays unavailable and "
            "is never zeroed, reconstructed or omitted",
            store_reason_codes={event_id: row["payload_reason"]},
        )
    if tuple(sorted(payload)) != tuple(sorted(Store._FUNDING_PAYLOAD_FIELDS)):
        raise _Refusal(
            "FUNDING_PAYLOAD_DOMAIN_MISMATCH",
            f"retained payload for {event_id} is not the authoritative domain",
            store_reason_codes={event_id: "FUNDING_PAYLOAD_DOMAIN_MISMATCH"},
        )
    for field, value in payload.items():
        _assert_finite(value, f"retained payload {event_id}.{field}")
    if reconcile_digest(payload) != row["payload_digest"]:
        raise _Refusal(
            "FUNDING_PAYLOAD_DIGEST_MISMATCH",
            f"retained payload for {event_id} does not reproduce its digest",
            store_reason_codes={event_id: "FUNDING_PAYLOAD_DIGEST_MISMATCH"},
        )
    if str(payload["event_id"]) != str(event_id):
        raise _Refusal(
            "FUNDING_PAYLOAD_IDENTITY_MISMATCH",
            f"retained payload identity disagrees with its row {event_id}",
            store_reason_codes={event_id: "FUNDING_PAYLOAD_IDENTITY_MISMATCH"},
        )
    return dict(payload)


# ---------------------------------------------------------------------------
# The approved pure entry point
# ---------------------------------------------------------------------------


def build_funding_candidate(
    retained_rows: Any,
    approved_event_bindings: Any,
    coverage: Any,
    schedule_id: Any,
    start_inclusive: Any,
    end_exclusive: Any,
) -> CandidateResult:
    """Build one synthetic funding candidate for a whole interval, or refuse.

    The result is atomic in meaning: either every inventoried event in
    ``[start_inclusive, end_exclusive)`` carries a verified retained payload
    and an explicit approved binding, or no candidate is produced at all.
    """
    facts: dict[str, Any] = {}
    try:
        return _build(
            retained_rows,
            approved_event_bindings,
            coverage,
            schedule_id,
            start_inclusive,
            end_exclusive,
            facts,
        )
    except _Refusal as refusal:
        facts.update(refusal.facts)
        return CandidateResult(
            accepted=False,
            reason_code=refusal.code,
            report=_report(
                accepted=False,
                reason_code=refusal.code,
                reason_detail=refusal.detail,
                facts=facts,
            ),
        )


def _build(
    retained_rows: Any,
    approved_event_bindings: Any,
    coverage: Any,
    schedule_id: Any,
    start_inclusive: Any,
    end_exclusive: Any,
    facts: dict[str, Any],
) -> CandidateResult:
    schedule = _require_text(schedule_id, "schedule_id", CANDIDATE_INPUT_INVALID)
    if not isinstance(start_inclusive, str) or not isinstance(end_exclusive, str):
        raise _Refusal(
            CANDIDATE_INTERVAL_INVALID,
            "start_inclusive and end_exclusive must be exact RFC 3339 UTC strings",
        )
    start = _parse_instant(start_inclusive, "start_inclusive")
    end = _parse_instant(end_exclusive, "end_exclusive")
    if start.sort_key >= end.sort_key:
        raise _Refusal(
            CANDIDATE_INTERVAL_INVALID, "start_inclusive must precede end_exclusive"
        )
    facts["interval"] = {"start_inclusive": start.text, "end_exclusive": end.text}
    facts["synthetic_schedule_id"] = schedule

    witness = _validate_coverage(coverage, start, end)
    facts["symbol_scope"] = witness["symbol"]
    facts["account_scope"] = witness["account_scope"]
    facts["witness_identity"] = witness["witness_identity"]

    rows = [_validate_retained_row(raw) for raw in _require_sequence(retained_rows, "retained_rows")]
    bindings = [
        _validate_binding(raw)
        for raw in _require_sequence(approved_event_bindings, "approved_event_bindings")
    ]
    facts["retained_row_count"] = len(rows)
    facts["binding_count"] = len(bindings)

    for row in rows:
        if row["symbol"] != witness["symbol"]:
            raise _Refusal(
                CANDIDATE_SYMBOL_MISMATCH,
                f"retained event {row['event_id']} is {row['symbol']}, outside the "
                f"witnessed {witness['symbol']} scope",
            )

    folded_rows = _fold_unique(rows, "event_id", "retained row")
    folded_bindings = _fold_unique(bindings, "event_id", "binding")

    inventory = list(witness["expected_event_ids"])
    inventory_set = set(inventory)
    row_ids = set(folded_rows)
    binding_ids = set(folded_bindings)

    unknown = sorted(binding_ids - row_ids)
    facts["unknown_binding_event_ids"] = unknown
    if unknown:
        raise _Refusal(
            CANDIDATE_BINDING_UNKNOWN_EVENT,
            f"bindings reference events with no retained ledger row: {unknown}",
        )

    outside_inventory = sorted(row_ids - inventory_set)
    unmatched_inventory = sorted(inventory_set - row_ids)
    facts["inventory_missing_event_ids"] = outside_inventory
    facts["inventory_unmatched_event_ids"] = unmatched_inventory
    if outside_inventory or unmatched_inventory:
        raise _Refusal(
            CANDIDATE_INVENTORY_MISMATCH,
            "the completion witness inventory disagrees with the supplied "
            f"evidence: retained-but-uninventoried {outside_inventory}, "
            f"inventoried-without-evidence {unmatched_inventory}",
        )

    unbound = sorted(inventory_set - binding_ids)
    facts["unbound_events"] = unbound
    if unbound:
        raise _Refusal(
            CANDIDATE_EVENT_UNBOUND,
            f"inventoried events carry no approved binding: {unbound}",
        )

    source_witness_ids = set(witness["source_witnesses"])
    missing_source_bytes = sorted(inventory_set - source_witness_ids)
    extra_source_bytes = sorted(source_witness_ids - inventory_set)
    if missing_source_bytes or extra_source_bytes:
        raise _Refusal(
            CANDIDATE_BINDING_INVALID,
            "coverage source bytes must match the complete inventory exactly: "
            f"missing {missing_source_bytes}, extra {extra_source_bytes}",
        )

    facts["out_of_scope_event_ids"] = []

    events: list[dict[str, Any]] = []
    out_of_interval: list[str] = []
    for event_id in sorted(inventory_set):
        row = folded_rows[event_id]
        binding = folded_bindings[event_id]
        payload = _verify_retained_payload(row)
        if not (start.sort_key <= binding["instant"].sort_key < end.sort_key):
            out_of_interval.append(event_id)
            continue
        if binding["body"]["source_event_digest"] == row["payload_digest"]:
            raise _Refusal(
                CANDIDATE_DIGEST_DOMAIN_CONFLATION,
                f"binding {event_id} reuses the normalized Bridge payload digest "
                "as a source_event_digest; the two byte domains are distinct",
            )
        _verify_source_witness(binding, witness["source_witnesses"][event_id])
        ledger_instant = row["ledger_instant"]
        events.append({
            "sort_key": (binding["instant"].sort_key, event_id.encode("utf-8")),
            "body": {
                "binding": binding["body"],
                "binding_notes": {
                    "bridge_effective_ts_equals_binding_event_timestamp": (
                        ledger_instant.sort_key == binding["instant"].sort_key
                    ),
                    "settlement_rate_source": SETTLEMENT_SOURCE,
                    "settlement_time_source": SETTLEMENT_SOURCE,
                },
                "bridge_evidence": {
                    "attribution": row["attribution"],
                    "event_id": event_id,
                    "ledger_effective_ts": ledger_instant.text,
                    "payload": payload,
                    "payload_digest": row["payload_digest"],
                },
            },
        })

    facts["out_of_interval_bindings"] = sorted(out_of_interval)
    if out_of_interval:
        raise _Refusal(
            CANDIDATE_BINDING_OUT_OF_INTERVAL,
            "approved bindings settle outside the requested interval: "
            f"{sorted(out_of_interval)}",
        )

    acknowledged = set(witness["unattributed_event_ids"])
    observed = {
        event_id
        for event_id in inventory_set
        if folded_rows[event_id]["attribution"] != "ATTRIBUTED"
    }
    if acknowledged != observed:
        raise _Refusal(
            CANDIDATE_ATTRIBUTION_SCOPE_MISMATCH,
            "the witness must acknowledge exactly the non-ATTRIBUTED retained "
            f"events; acknowledged {sorted(acknowledged)}, observed {sorted(observed)}",
        )

    events.sort(key=lambda event: event["sort_key"])
    candidate = {
        "admission_status": ADMISSION_STATUS,
        "artifact_kind": ARTIFACT_KIND,
        "bridge_payload_digest_domain": BRIDGE_PAYLOAD_DIGEST_DOMAIN,
        "not_a_production_record": NOT_A_PRODUCTION_RECORD,
        "numeric_representation": NUMERIC_REPRESENTATION,
        "source_event_digest_domain": SOURCE_EVENT_DIGEST_DOMAIN,
        "synthetic_candidate": {
            "account_scope": witness["account_scope"],
            "coverage_witness": {
                **witness,
                "expected_event_ids": sorted(inventory),
                "unattributed_event_ids": sorted(witness["unattributed_event_ids"]),
            },
            "effective_interval": {
                "end_exclusive": end.text,
                "start_inclusive": start.text,
            },
            "event_count": len(events),
            "symbol_scope": witness["symbol"],
            "synthetic_events": [event["body"] for event in events],
            "synthetic_schedule_id": schedule,
        },
        "synthetic_only": True,
    }
    body = canonical_reconcile_json(candidate).encode("utf-8") + b"\n"
    digest = hashlib.sha256(body).hexdigest()
    facts["event_count"] = len(events)
    facts["candidate_sha256"] = digest
    return CandidateResult(
        accepted=True,
        reason_code=SYNTHETIC_CANDIDATE_BUILT,
        report=_report(
            accepted=True,
            reason_code=SYNTHETIC_CANDIDATE_BUILT,
            reason_detail=(
                "synthetic candidate built from synthetic caller facts; it is "
                "not evidence of real-world completeness"
            ),
            facts=facts,
        ),
        candidate_bytes=body,
        candidate_sha256=digest,
    )


def _report(
    *, accepted: bool, reason_code: str, reason_detail: str, facts: Mapping[str, Any]
) -> dict[str, Any]:
    """One fully labelled, fully deterministic report. No clock is read."""
    return {
        "accepted": accepted,
        "candidate_sha256": facts.get("candidate_sha256"),
        "event_count": facts.get("event_count"),
        "evidence_limitations": list(EVIDENCE_LIMITATIONS),
        "inputs": {
            "account_scope": facts.get("account_scope"),
            "binding_count": facts.get("binding_count"),
            "interval": facts.get("interval"),
            "retained_row_count": facts.get("retained_row_count"),
            "symbol_scope": facts.get("symbol_scope"),
            "synthetic_schedule_id": facts.get("synthetic_schedule_id"),
            "witness_identity": facts.get("witness_identity"),
        },
        "inventory_missing_event_ids": facts.get("inventory_missing_event_ids", []),
        "inventory_unmatched_event_ids": facts.get("inventory_unmatched_event_ids", []),
        "non_admission": {
            "admission_status": ADMISSION_STATUS,
            "production_selection_keys_absent": [
                "events",
                "schedule_id",
                "settlement_currency",
            ],
            "statement": NOT_A_PRODUCTION_RECORD,
        },
        "out_of_interval_bindings": facts.get("out_of_interval_bindings", []),
        "out_of_scope_event_ids": facts.get("out_of_scope_event_ids", []),
        "production_mode": PRODUCTION_MODE_UNAVAILABLE,
        "reason_code": reason_code,
        "reason_detail": reason_detail,
        "report_kind": REPORT_KIND,
        "store_reason_codes": facts.get("store_reason_codes", {}),
        "synthetic_only": True,
        "unbound_events": facts.get("unbound_events", []),
        "uninventoried_event_ids": facts.get("uninventoried_event_ids", []),
        "unknown_binding_event_ids": facts.get("unknown_binding_event_ids", []),
    }


# ---------------------------------------------------------------------------
# Offline snapshot access — read-only, quiescent, never initialized
# ---------------------------------------------------------------------------


class _ReadOnlySnapshot:
    """The real Store retrieval methods bound to a read-only connection.

    ``Store.__init__``/``Store.conn`` are bypassed on purpose: that property
    creates the database file, sets ``PRAGMA journal_mode=WAL`` and
    ``PRAGMA foreign_keys=ON``, all of which write. Composing the unbound
    methods here keeps the retained-payload verification, and every reason
    code it raises, exactly as the Store defines them.
    """

    def __init__(self, conn: sqlite3.Connection) -> None:
        self.conn = conn

    _rows = Store._rows
    get_meta = Store.get_meta
    full_reconcile_enabled = Store.full_reconcile_enabled
    funding_payload_retention_enabled = Store.funding_payload_retention_enabled
    list_funding_events = Store.list_funding_events
    get_funding_event_payload = Store.get_funding_event_payload


_SNAPSHOT_COMPANIONS = ("-wal", "-shm", "-journal")


def _assert_quiescent(snapshot: Path) -> None:
    if not snapshot.is_file():
        raise _Refusal(
            CANDIDATE_SNAPSHOT_UNAVAILABLE,
            "the named offline snapshot does not exist; this tool never copies "
            "or captures a live database",
        )
    present = [
        suffix
        for suffix in _SNAPSHOT_COMPANIONS
        if snapshot.with_name(snapshot.name + suffix).exists()
    ]
    if present:
        raise _Refusal(
            CANDIDATE_SNAPSHOT_NOT_QUIESCENT,
            f"the snapshot carries {present}; only a quiescent offline copy with "
            "no WAL, SHM or journal companion can be read",
        )


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _read_snapshot_rows(snapshot: Path, symbol: str) -> list[dict[str, Any]]:
    """Read retained rows through the Store's own verified retrieval path."""
    try:
        uri = f"{snapshot.resolve().as_uri()}?mode=ro&immutable=1"
    except ValueError as exc:  # pragma: no cover - defensive
        raise _Refusal(CANDIDATE_SNAPSHOT_UNREADABLE, "cannot resolve the snapshot path") from exc
    try:
        conn = sqlite3.connect(uri, uri=True)
    except sqlite3.Error as exc:
        raise _Refusal(
            CANDIDATE_SNAPSHOT_UNREADABLE,
            f"cannot open the snapshot read-only: {type(exc).__name__}",
        ) from exc
    conn.row_factory = sqlite3.Row
    snap = _ReadOnlySnapshot(conn)
    try:
        if not snap.funding_payload_retention_enabled():
            raise _Refusal(
                "FUNDING_PAYLOAD_SCHEMA_INACTIVE",
                "retained funding payloads require schema v10; this tool never "
                "migrates a snapshot to reach it",
            )
        rows: list[dict[str, Any]] = []
        for ledger in snap.list_funding_events(symbol=symbol):
            event_id = str(ledger["event_id"])
            try:
                payload = snap.get_funding_event_payload(event_id)
            except ReconcileConflictError as exc:
                payload, reason = None, exc.code
            else:
                reason = (
                    PAYLOAD_RETAINED if payload is not None else CANDIDATE_PAYLOAD_UNAVAILABLE
                )
            rows.append({
                "attribution": str(ledger["attribution"]),
                "event_id": event_id,
                "ledger_effective_ts": str(ledger["effective_ts"]),
                "payload": payload,
                "payload_digest": str(ledger["payload_digest"]),
                "payload_reason": reason,
                "symbol": str(ledger["symbol"]),
            })
        return rows
    except sqlite3.Error as exc:
        raise _Refusal(
            CANDIDATE_SNAPSHOT_UNREADABLE,
            f"the snapshot is not a readable Bridge database: {type(exc).__name__}",
        ) from exc
    finally:
        conn.close()


def _load_packet(path: Path) -> tuple[list[Any], Any]:
    try:
        raw = path.read_bytes()
    except OSError as exc:
        raise _Refusal(
            CANDIDATE_PACKET_INVALID, f"cannot read the binding packet: {type(exc).__name__}"
        ) from exc
    try:
        parsed = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, ValueError) as exc:
        raise _Refusal(
            CANDIDATE_PACKET_INVALID, f"the binding packet is not valid JSON: {exc}"
        ) from exc
    packet = _require_closed_mapping(
        parsed, PACKET_KEYS, "binding packet", CANDIDATE_PACKET_INVALID
    )
    if packet["packet_version"] != PACKET_VERSION:
        raise _Refusal(
            CANDIDATE_PACKET_INVALID,
            f"unsupported packet_version {packet['packet_version']!r}; this tool "
            f"reads only {PACKET_VERSION}",
        )
    if isinstance(packet["bindings"], Mapping) or not isinstance(
        packet["bindings"], list
    ):
        raise _Refusal(CANDIDATE_PACKET_INVALID, "packet bindings must be a list")
    return packet["bindings"], packet["coverage"]


# ---------------------------------------------------------------------------
# Staging — no overwrite, no candidate on refusal, no partial success
# ---------------------------------------------------------------------------


def _contains_path(parent: Path, child: Path) -> bool:
    return parent == child or parent in child.parents


def _has_reparse_ancestor(path: Path) -> bool:
    absolute = Path(os.path.abspath(path))
    for candidate in (absolute, *absolute.parents):
        try:
            metadata = candidate.lstat()
        except OSError:
            continue
        if candidate.is_symlink() or (
            getattr(metadata, "st_file_attributes", 0)
            & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0)
        ):
            return True
    return False


def _prepare_staging(staging: Path, snapshot: Path, bindings: Path) -> None:
    if _has_reparse_ancestor(staging):
        raise _Refusal(
            CANDIDATE_STAGING_UNSAFE,
            "the staging path has a symlink or reparse-point ancestor",
        )
    try:
        resolved_staging = staging.resolve(strict=False)
        resolved_root = ROOT.resolve(strict=True)
        resolved_snapshot = snapshot.resolve(strict=False)
        resolved_bindings = bindings.resolve(strict=False)
    except OSError as exc:
        raise _Refusal(
            CANDIDATE_STAGING_UNSAFE,
            f"cannot resolve the staging boundary: {type(exc).__name__}",
        ) from exc
    if _contains_path(resolved_root, resolved_staging):
        raise _Refusal(
            CANDIDATE_STAGING_UNSAFE,
            "the staging directory must be external to the Bridge repository",
        )
    for label, input_path in (
        ("snapshot", resolved_snapshot),
        ("bindings", resolved_bindings),
    ):
        if _contains_path(resolved_staging, input_path) or _contains_path(
            input_path, resolved_staging
        ):
            raise _Refusal(
                CANDIDATE_STAGING_UNSAFE,
                f"the staging directory overlaps the {label} input path",
            )
    if staging.exists() or staging.is_symlink():
        raise _Refusal(
            CANDIDATE_STAGING_NOT_EMPTY,
            "the staging directory must be a new, non-existing path; this tool "
            "never overwrites or adopts an existing directory",
        )
    if not staging.parent.is_dir():
        raise _Refusal(
            CANDIDATE_STAGING_FAILED,
            "the staging directory's parent must already exist",
        )


def _write_new_file(path: Path, data: bytes) -> None:
    """Create one new file; an existing path is never clobbered."""
    with open(path, "xb") as handle:
        handle.write(data)


def _cleanup_scratch(scratch: Path) -> list[str]:
    residual: list[str] = []
    try:
        children = list(scratch.iterdir())
    except OSError:
        return [str(scratch)]
    for child in children:
        try:
            child.unlink()
        except OSError:
            residual.append(child.name)
    try:
        scratch.rmdir()
    except OSError:
        if not residual:
            residual.append(str(scratch))
    return residual


def _stage(staging: Path, result: CandidateResult) -> None:
    report_bytes = canonical_reconcile_json(result.report).encode("utf-8") + b"\n"
    try:
        scratch = Path(
            tempfile.mkdtemp(prefix=f".{staging.name}.", dir=staging.parent)
        )
    except OSError as exc:
        raise _Refusal(
            CANDIDATE_STAGING_FAILED,
            f"cannot create private staging scratch: {type(exc).__name__}",
        ) from exc
    try:
        if result.accepted:
            assert result.candidate_bytes is not None
            assert result.candidate_sha256 is not None
            candidate = scratch / CANDIDATE_FILENAME
            _write_new_file(candidate, result.candidate_bytes)
            sidecar = scratch / SIDECAR_FILENAME
            _write_new_file(sidecar, result.candidate_sha256.encode("ascii") + b"\n")
        report = scratch / REPORT_FILENAME
        _write_new_file(report, report_bytes)
        scratch.rename(staging)
    except OSError as exc:
        residual = _cleanup_scratch(scratch)
        if residual:
            detail = (
                f"staging failed: {type(exc).__name__}; cleanup incomplete; "
                f"unpublished scratch {scratch} retains {residual}"
            )
        else:
            detail = (
                f"staging failed before publication and private scratch was removed: "
                f"{type(exc).__name__}"
            )
        raise _Refusal(
            CANDIDATE_STAGING_FAILED,
            detail,
        ) from exc


def _parse_args(argv: Sequence[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog=TOOL_NAME,
        description=(
            "Stage a SYNTHETIC_ONLY MTC funding candidate from a quiescent "
            "offline Bridge snapshot and a separately verified binding packet. "
            "The result is never an accepted economic record."
        ),
    )
    parser.add_argument("--snapshot", required=True)
    parser.add_argument("--bindings", required=True)
    parser.add_argument("--symbol", required=True)
    parser.add_argument("--start", required=True)
    parser.add_argument("--end", required=True)
    parser.add_argument("--schedule-id", required=True, dest="schedule_id")
    parser.add_argument("--staging", required=True)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = _parse_args(argv)
    staging = Path(args.staging)
    snapshot = Path(args.snapshot)
    bindings_path = Path(args.bindings)
    try:
        _prepare_staging(staging, snapshot, bindings_path)
    except _Refusal as refusal:
        print(f"{TOOL_NAME}: {refusal}", file=sys.stderr)
        return 1

    try:
        _assert_quiescent(snapshot)
        before = _sha256_file(snapshot)
        bindings, coverage = _load_packet(bindings_path)
        if not isinstance(coverage, Mapping) or coverage.get("symbol") != args.symbol:
            raise _Refusal(
                CANDIDATE_SYMBOL_MISMATCH,
                f"--symbol {args.symbol!r} is outside the witnessed scope "
                f"{coverage.get('symbol')!r}"
                if isinstance(coverage, Mapping)
                else "the packet carries no coverage witness object",
            )
        rows = _read_snapshot_rows(snapshot, args.symbol)
        if _sha256_file(snapshot) != before:
            raise _Refusal(
                CANDIDATE_SNAPSHOT_DRIFTED,
                "the snapshot changed while it was being read; only a quiescent "
                "offline copy can be materialized",
            )
        _assert_quiescent(snapshot)
    except _Refusal as refusal:
        result = CandidateResult(
            accepted=False,
            reason_code=refusal.code,
            report=_report(
                accepted=False,
                reason_code=refusal.code,
                reason_detail=refusal.detail,
                facts={
                    "interval": {
                        "start_inclusive": args.start,
                        "end_exclusive": args.end,
                    },
                    "symbol_scope": args.symbol,
                    "synthetic_schedule_id": args.schedule_id,
                    **refusal.facts,
                },
            ),
        )
    else:
        result = build_funding_candidate(
            rows, bindings, coverage, args.schedule_id, args.start, args.end
        )

    try:
        _stage(staging, result)
    except _Refusal as refusal:
        print(f"{TOOL_NAME}: {refusal}", file=sys.stderr)
        return 1
    if not result.accepted:
        print(f"{TOOL_NAME}: refused ({result.reason_code})", file=sys.stderr)
        return 1
    print(
        f"{TOOL_NAME}: staged SYNTHETIC_ONLY candidate "
        f"{result.candidate_sha256} under {staging.name}; it is not an accepted "
        "economic record"
    )
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
