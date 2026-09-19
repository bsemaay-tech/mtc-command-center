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
:data:`PRODUCTION_MODE_UNAVAILABLE` for this default profile until the real
binding-packet schema and the ``source_event_digest`` byte domain are approved
and implemented elsewhere; the ``REAL_CAPTURE_READ_ONLY`` profile below
implements and verifies that byte domain (D-1) but remains equally
non-admitted (``OD-20260914-P012-ADMISSION-Q3`` "Wait").

Second evidence profile (2026-09-16, ``OD-20260916-P012-INTAKE-D1-D6-R-1``)
----------------------------------------------------------------------------
``--evidence-kind REAL_CAPTURE_READ_ONLY`` reads a packet built from a Path-1
read-only venue capture under the six ruled intake rules: D-1 the
``source_event_digest`` hashes the exact captured funding-row bytes
(``HL_USERFUNDING_ROW_V1:<hex>``); D-2 the event id is re-derived as
``hl-funding:<account-short>:<coin>:<time_ms>``; D-3 the venue stamp is kept
verbatim and ``interval_hour_utc`` is its floor; D-4 an oracle capture at the
funding instant must be named (a payment-derived price is never admitted);
D-5 the witness identity names the ownership-signature record; D-6 two
byte-identical funding passes, an hour-aligned window whose admission band is
``[start+tolerance, end+tolerance)`` (half-open, both ends shifted by the same
1-second settlement tolerance, ``D6-START B`` / ``OD-20260918-P012-D6START-B-1``)
so a payment stamped within the tolerance of a boundary belongs to exactly one
of the two adjacent windows, never both, and the fills-derived position at
every hour witnesses completeness.
The profile is named by the caller and must be declared by the packet; it is
not in :data:`ACCEPTED_EVIDENCE_KINDS`, it is not a mode, and its candidate is
labelled ``REFUSED_REAL_CAPTURE_READ_ONLY_NOT_A_PRODUCTION_RECORD``:
production admission is still not granted (``OD-20260914-P012-ADMISSION-Q3``).

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

# --- the real read-only capture profile (OD-20260916-P012-INTAKE-D1-D6-R-1) ---
# A second, explicitly declared evidence profile. It is NOT in
# ACCEPTED_EVIDENCE_KINDS: the default profile stays synthetic, and a packet is
# read under this profile only when the caller names it (``--evidence-kind`` /
# keyword-only ``evidence_kind=``) AND the packet declares the same kind in its
# coverage witness and in every binding's provenance. There is still no
# production mode: a real-capture candidate is labelled non-admitted and keeps
# the same structural non-consumability as the synthetic one.
REAL_CAPTURE_EVIDENCE_KIND = "REAL_CAPTURE_READ_ONLY"
REAL_CAPTURE_PACKET_VERSION = "REAL_CAPTURE_FUNDING_BINDING_PACKET_V1"
REAL_CAPTURE_ARTIFACT_KIND = "REAL_CAPTURE_FUNDING_CANDIDATE_V1"
REAL_CAPTURE_CANDIDATE_FILENAME = "funding_candidate_real_capture.json"
REAL_CAPTURE_SIDECAR_FILENAME = "funding_candidate_real_capture.json.sha256"
REAL_CAPTURE_REPORT_KIND = "REAL_CAPTURE_FUNDING_CANDIDATE_REPORT_V1"
REAL_SOURCE_EVENT_DIGEST_DOMAIN = "HL_USERFUNDING_ROW_V1"  # D-1
REAL_EVENT_ID_PREFIX = "hl-funding"  # D-2
# D-6 (i): the venue stamps the hour's payment up to this many seconds late. The
# admission band [start+tolerance, end+tolerance) applies the SAME tolerance to
# both boundaries (D6-START B, OD-20260918-P012-D6START-B-1): a payment stamped
# within the tolerance of a window's start belongs to the PREVIOUS window (it
# settles that window's last interval), mirroring how a payment stamped within
# the tolerance of the end still belongs to THIS window.
REAL_END_TOLERANCE_SECONDS = 1
REAL_POSITION_SOURCE_FILLS = "coverage.fills_witness"  # D-6 (ii)
REAL_POSITION_SOURCE_PAYMENTS = (  # D-6 (ii) when the fills witness has no fill
    "captured funding rows: the fills witness carries no fill for the symbol, so "
    "the position is the constant szi the payments themselves report and the "
    "per-row szi cross-check is vacuous"
)
REAL_SETTLEMENT_SOURCE = (  # D-1/D-3: re-derived from the exact captured venue row
    "HL_USERFUNDING_ROW_V1_CAPTURED"
)
REAL_CAPTURE_ADMISSION_STATUS = "REFUSED_REAL_CAPTURE_READ_ONLY_NOT_A_PRODUCTION_RECORD"
REAL_CAPTURE_CANDIDATE_BUILT = "REAL_CAPTURE_CANDIDATE_BUILT"
# D-1's source_event_digest byte domain (HL_USERFUNDING_ROW_V1) is implemented and
# verified for this profile, unlike the synthetic default, so the real profile's
# production_mode must not repeat PRODUCTION_MODE_UNAVAILABLE's stale reason; it is
# still refused, but only by the standing admission decision, never a missing digest
# domain (Sol T0 review of 8cbf4f1a, NIT-2).
REAL_CAPTURE_PRODUCTION_MODE_UNAVAILABLE = "UNAVAILABLE_PRODUCTION_ADMISSION_NOT_GRANTED"
REAL_CAPTURE_NOT_A_PRODUCTION_RECORD = (
    "Read-only capture evidence bound under the P0-12 intake rules D-1..D-6. "
    "This is not an accepted economic record and not an admitted production "
    'input: OD-20260914-P012-ADMISSION-Q3 ("Wait") stands. It must never be '
    "installed as an MTC funding schedule."
)
REAL_CAPTURE_EVIDENCE_LIMITATIONS = (
    (
        "REAL_CAPTURE_READ_ONLY: every binding is re-derived from the exact "
        "captured venue bytes carried in the coverage witness (D-1, D-2, D-3)."
    ),
    (
        "The capture manifest and its ownership-signature record are named by "
        "digest in the witness identity (D-5); this tool does not re-open them."
    ),
    (
        "The oracle capture behind each oracle_price is named by digest and JSON "
        "pointer (D-4); this tool does not re-open it and does not re-verify the price."
    ),
    (
        "Whole-interval completeness is witnessed by two byte-identical funding "
        "passes, an hour-aligned admission band [start+tolerance, end+tolerance) "
        "half-open with the same 1-second settlement tolerance on both ends "
        "(D6-START B) and the fills-derived position at every hour (D-6) - or, "
        "when the fills witness carries no fill for the symbol, the constant "
        "position the payments themselves report (completion_check.position_source "
        "names which); it is evidence about the captured window only."
    ),
    (
        "bridge_evidence.payload carries the retained Bridge observation beside "
        "the binding as labelled evidence only; only its effective_ts is compared "
        "to the binding's event_timestamp (binding_notes). The payload's other "
        "values (rate, size) are never cross-checked against the captured venue "
        "row bytes."
    ),
    (
        "Production admission is NOT granted (OD-20260914-P012-ADMISSION-Q3 "
        '"Wait"); this artifact is not admitted by any production selection path.'
    ),
)

# --- outcome and refusal codes --------------------------------------------
SYNTHETIC_CANDIDATE_BUILT = "SYNTHETIC_CANDIDATE_BUILT"
PAYLOAD_RETAINED = "FUNDING_PAYLOAD_RETAINED"

CANDIDATE_EVIDENCE_KIND_MISMATCH = "CANDIDATE_EVIDENCE_KIND_MISMATCH"
CANDIDATE_ORACLE_EVIDENCE_UNAVAILABLE = "CANDIDATE_ORACLE_EVIDENCE_UNAVAILABLE"
CANDIDATE_INPUT_INVALID = "CANDIDATE_INPUT_INVALID"
CANDIDATE_INTERVAL_INVALID = "CANDIDATE_INTERVAL_INVALID"
CANDIDATE_TIMESTAMP_INVALID = "CANDIDATE_TIMESTAMP_INVALID"
CANDIDATE_COVERAGE_INVALID = "CANDIDATE_COVERAGE_INVALID"
CANDIDATE_PRODUCTION_EVIDENCE_UNAVAILABLE = "CANDIDATE_PRODUCTION_EVIDENCE_UNAVAILABLE"
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
REAL_BINDING_KEYS = BINDING_KEYS + ("interval_hour_utc",)  # D-3 schedule key
REAL_COVERAGE_KEYS = COVERAGE_KEYS + ("fills_witness", "funding_witness_passes")

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
_HOUR_SECONDS = 3600
_REAL_SOURCE_EVENT_DIGEST = re.compile(
    rf"\A{REAL_SOURCE_EVENT_DIGEST_DOMAIN}:(?P<hex>[0-9a-f]{{64}})\Z"
)
_REAL_ORACLE_LOCATOR = re.compile(r"\A[0-9a-f]{64}#/\S+\Z")
_REAL_SOURCE_LOCATOR = re.compile(r"\A(?P<file>[^#]+)#/(?P<index>0|[1-9][0-9]*)\Z")
_REAL_WITNESS_MANIFEST = re.compile(
    r"\bmanifest_sha256=(?P<hex>[0-9a-f]{64})(?![0-9a-f])"
)
_REAL_WITNESS_RUN = re.compile(r"\brun (?P<run>[A-Za-z0-9._-]+)")
_REAL_WITNESS_OWNERSHIP = re.compile(
    r"\bownership OWNERSHIP_EVIDENCE: VERIFIED (?P<scope>\S+)"
)
_LOWER_HEX = re.compile(r"\A(?:[0-9a-f]{2})+\Z")


@dataclass(frozen=True)
class _EvidenceProfile:
    """Everything that differs between the two explicitly named evidence kinds.

    The synthetic profile is the default and its outputs are byte-for-byte the
    pre-existing ones. The real profile changes closed key sets, labels, file
    names and the D-1..D-6 checks — never a flag inside one shared code path.
    """

    kind: str
    packet_version: str
    artifact_kind: str
    candidate_filename: str
    sidecar_filename: str
    admission_status: str
    built_code: str
    digest_domain: str
    not_a_production_record: str
    evidence_limitations: tuple[str, ...]
    binding_keys: tuple[str, ...]
    coverage_keys: tuple[str, ...]
    candidate_key: str
    events_key: str
    schedule_key: str
    synthetic_only: bool
    end_tolerance_seconds: int
    report_kind: str
    settlement_source: str
    production_mode: str


_SYNTHETIC_PROFILE = _EvidenceProfile(
    kind=SYNTHETIC_EVIDENCE_KIND,
    packet_version=PACKET_VERSION,
    artifact_kind=ARTIFACT_KIND,
    candidate_filename=CANDIDATE_FILENAME,
    sidecar_filename=SIDECAR_FILENAME,
    admission_status=ADMISSION_STATUS,
    built_code=SYNTHETIC_CANDIDATE_BUILT,
    digest_domain=SOURCE_EVENT_DIGEST_DOMAIN,
    not_a_production_record=NOT_A_PRODUCTION_RECORD,
    evidence_limitations=EVIDENCE_LIMITATIONS,
    binding_keys=BINDING_KEYS,
    coverage_keys=COVERAGE_KEYS,
    candidate_key="synthetic_candidate",
    events_key="synthetic_events",
    schedule_key="synthetic_schedule_id",
    synthetic_only=True,
    end_tolerance_seconds=0,
    report_kind=REPORT_KIND,
    settlement_source=SETTLEMENT_SOURCE,
    production_mode=PRODUCTION_MODE_UNAVAILABLE,
)
_REAL_PROFILE = _EvidenceProfile(
    kind=REAL_CAPTURE_EVIDENCE_KIND,
    packet_version=REAL_CAPTURE_PACKET_VERSION,
    artifact_kind=REAL_CAPTURE_ARTIFACT_KIND,
    candidate_filename=REAL_CAPTURE_CANDIDATE_FILENAME,
    sidecar_filename=REAL_CAPTURE_SIDECAR_FILENAME,
    admission_status=REAL_CAPTURE_ADMISSION_STATUS,
    built_code=REAL_CAPTURE_CANDIDATE_BUILT,
    digest_domain=REAL_SOURCE_EVENT_DIGEST_DOMAIN,
    not_a_production_record=REAL_CAPTURE_NOT_A_PRODUCTION_RECORD,
    evidence_limitations=REAL_CAPTURE_EVIDENCE_LIMITATIONS,
    binding_keys=REAL_BINDING_KEYS,
    coverage_keys=REAL_COVERAGE_KEYS,
    candidate_key="real_capture_candidate",
    events_key="bound_events",
    schedule_key="candidate_schedule_id",
    synthetic_only=False,
    end_tolerance_seconds=REAL_END_TOLERANCE_SECONDS,
    report_kind=REAL_CAPTURE_REPORT_KIND,
    settlement_source=REAL_SETTLEMENT_SOURCE,
    production_mode=REAL_CAPTURE_PRODUCTION_MODE_UNAVAILABLE,
)
_EVIDENCE_PROFILES = {
    SYNTHETIC_EVIDENCE_KIND: _SYNTHETIC_PROFILE,
    REAL_CAPTURE_EVIDENCE_KIND: _REAL_PROFILE,
}


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
    evidence_kind: str = SYNTHETIC_EVIDENCE_KIND


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
        raise _Refusal(
            CANDIDATE_TIMESTAMP_INVALID, f"{field} is not a real instant: {exc}"
        )
    offset = parts["offset"]
    if offset != "Z":
        sign = -1 if offset[0] == "-" else 1
        offset_hours = int(offset[1:3])
        offset_minutes = int(offset[4:6])
        if offset_hours > 23 or offset_minutes > 59:
            raise _Refusal(
                CANDIDATE_TIMESTAMP_INVALID,
                f"{field} has an invalid RFC 3339 offset {offset!r}",
            )
        try:
            stamp -= timedelta(minutes=sign * (offset_hours * 60 + offset_minutes))
        except OverflowError as exc:
            raise _Refusal(
                CANDIDATE_TIMESTAMP_INVALID,
                f"{field} offset moves the timestamp outside the calendar range",
            ) from exc
    fraction_digits = parts["fraction"]
    spelled = stamp.strftime("%Y-%m-%dT%H:%M:%S")
    if fraction_digits is not None:
        spelled = f"{spelled}.{fraction_digits}"
    return _Instant(
        seconds=int((stamp - _EPOCH) // timedelta(seconds=1)),
        fraction=Decimal(0)
        if fraction_digits is None
        else Decimal(f"0.{fraction_digits}"),
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


def _require_closed_mapping(
    value: Any, keys: Sequence[str], label: str, code: str
) -> dict:
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


def _reject_json_constant(value: str) -> None:
    raise ValueError(f"non-standard JSON numeric constant {value!r}")


def _reject_duplicate_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON member {key!r}")
        result[key] = value
    return result


def _strict_json_loads(raw: bytes) -> Any:
    return json.loads(
        raw.decode("utf-8"),
        object_pairs_hook=_reject_duplicate_object,
        parse_constant=_reject_json_constant,
    )


# ---------------------------------------------------------------------------
# Input validation — the pure function trusts no caller
# ---------------------------------------------------------------------------


def _require_evidence_kind(kind: Any, profile: _EvidenceProfile, label: str) -> str:
    """The packet must say what the caller declared — in the witness and in
    every binding. A known-but-undeclared kind is a mismatch; an unknown kind
    stays the unapproved-contract refusal it always was."""
    if kind == profile.kind:
        return kind
    if isinstance(kind, str) and kind in _EVIDENCE_PROFILES:
        raise _Refusal(
            CANDIDATE_EVIDENCE_KIND_MISMATCH,
            f"{label} declares evidence_kind {kind!r} but the caller admitted only "
            f"{profile.kind!r}; the evidence profile is named explicitly, never inferred",
        )
    raise _Refusal(
        CANDIDATE_PRODUCTION_EVIDENCE_UNAVAILABLE,
        "the production completion-evidence contract is not approved or "
        f"implemented; only {profile.kind!r} is accepted under this run, got {kind!r}",
    )


def _require_whole_hour(instant: _Instant, field: str) -> None:
    if instant.fraction != 0 or instant.seconds % _HOUR_SECONDS:
        raise _Refusal(
            CANDIDATE_COVERAGE_INVALID,
            f"D-6: {field} must be aligned to a whole venue funding hour, got {instant.text!r}",
        )


def _require_hex_bytes(value: Any, field: str) -> bytes:
    if not isinstance(value, str) or _LOWER_HEX.fullmatch(value) is None:
        raise _Refusal(
            CANDIDATE_COVERAGE_INVALID,
            f"D-6: {field} must be the exact captured bytes as lower-case hex",
        )
    return bytes.fromhex(value)


def _validate_real_witness_identity(identity: str, account_scope: str) -> None:
    """D-5: the witness names the capture run, the manifest by digest and the
    ownership-signature record for exactly this account scope."""
    manifest = _REAL_WITNESS_MANIFEST.search(identity)
    run = _REAL_WITNESS_RUN.search(identity)
    ownership = _REAL_WITNESS_OWNERSHIP.search(identity)
    if manifest is None or run is None or ownership is None:
        raise _Refusal(
            CANDIDATE_COVERAGE_INVALID,
            "D-5: coverage.witness_identity must name the capture run "
            "(`run <id>`), the capture manifest (`manifest_sha256=<hex>`) and the "
            "ownership-signature record (`ownership OWNERSHIP_EVIDENCE: VERIFIED <scope>`)",
        )
    if ownership.group("scope") != account_scope:
        raise _Refusal(
            CANDIDATE_COVERAGE_INVALID,
            "D-5: the ownership-signature record named by the witness is for "
            f"{ownership.group('scope')!r}, not the witnessed account scope {account_scope!r}",
        )


def _validate_real_coverage_extras(witness: Mapping[str, Any]) -> dict[str, Any]:
    """D-6 witness material: two byte-identical funding passes and the fills."""
    raw_passes = witness["funding_witness_passes"]
    if isinstance(raw_passes, (str, bytes, Mapping)) or not isinstance(
        raw_passes, Sequence
    ):
        raise _Refusal(
            CANDIDATE_COVERAGE_INVALID,
            "D-6: coverage.funding_witness_passes must be a list of captured funding passes",
        )
    passes = [
        _require_hex_bytes(item, f"coverage.funding_witness_passes[{index}]")
        for index, item in enumerate(raw_passes)
    ]
    if len(passes) < 2:
        raise _Refusal(
            CANDIDATE_COVERAGE_INVALID,
            "D-6: at least two captured funding passes are required, got "
            f"{len(passes)}",
        )
    if any(item != passes[0] for item in passes[1:]):
        raise _Refusal(
            CANDIDATE_COVERAGE_INVALID,
            "D-6: the captured funding passes are not byte-identical",
        )
    return {
        "funding_pass_bytes": passes[0],
        "funding_pass_sha256": hashlib.sha256(passes[0]).hexdigest(),
        "fills_bytes": _require_hex_bytes(
            witness["fills_witness"], "coverage.fills_witness"
        ),
    }


def _validate_coverage(
    coverage: Any, start: _Instant, end: _Instant, profile: _EvidenceProfile
) -> tuple[dict[str, Any], dict[str, Any]]:
    if isinstance(coverage, Mapping) and "evidence_kind" in coverage:
        # the kind is judged before the shape: a packet of the other profile is
        # reported as a kind mismatch, not as a malformed witness
        _require_evidence_kind(coverage["evidence_kind"], profile, "coverage")
    witness = _require_closed_mapping(
        coverage, profile.coverage_keys, "coverage", CANDIDATE_COVERAGE_INVALID
    )
    kind = _require_evidence_kind(witness["evidence_kind"], profile, "coverage")
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
    account_scope = _require_text(
        witness["account_scope"], "coverage.account_scope", CANDIDATE_COVERAGE_INVALID
    )
    identity = _require_text(
        witness["witness_identity"],
        "coverage.witness_identity",
        CANDIDATE_COVERAGE_INVALID,
    )
    validated = {
        "account_scope": account_scope,
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
        "witness_identity": identity,
    }
    extras: dict[str, Any] = {}
    if profile is _REAL_PROFILE:
        _require_whole_hour(start, "coverage.interval_start_inclusive")
        _require_whole_hour(end, "coverage.interval_end_exclusive")
        _validate_real_witness_identity(identity, account_scope)
        extras = _validate_real_coverage_extras(witness)
        validated["fills_witness"] = witness["fills_witness"]
        validated["funding_witness_passes"] = list(witness["funding_witness_passes"])
    return validated, extras


def _validate_retained_row(raw: Any) -> dict[str, Any]:
    row = _require_closed_mapping(
        raw, RETAINED_ROW_KEYS, "retained row", CANDIDATE_INPUT_INVALID
    )
    event_id = _require_text(
        row["event_id"], "retained row event_id", CANDIDATE_INPUT_INVALID
    )
    symbol = _require_text(
        row["symbol"], "retained row symbol", CANDIDATE_INPUT_INVALID
    )
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
        raise _Refusal(
            CANDIDATE_INPUT_INVALID, "retained row payload must be an object or null"
        )
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
    if payload is not None:
        for field, value in payload.items():
            _assert_finite(value, f"retained payload {event_id}.{field}")
    return {
        "attribution": attribution,
        "event_id": event_id,
        "ledger_effective_ts": ledger,
        "ledger_instant": _parse_instant(
            ledger, f"retained row {event_id} ledger_effective_ts"
        ),
        "payload": None if payload is None else dict(payload),
        "payload_digest": digest,
        "payload_reason": reason,
        "symbol": symbol,
    }


def _validate_provenance(
    raw: Any, event_id: str, profile: _EvidenceProfile
) -> dict[str, str]:
    provenance = _require_closed_mapping(
        raw,
        PROVENANCE_KEYS,
        f"binding {event_id} provenance",
        CANDIDATE_BINDING_INVALID,
    )
    kind = _require_evidence_kind(
        provenance["evidence_kind"], profile, f"binding {event_id} provenance"
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


def _hour_text(seconds: int) -> str:
    return (_EPOCH + timedelta(seconds=seconds)).strftime("%Y-%m-%dT%H:00:00Z")


def _millisecond_text(time_ms: int) -> str:
    stamp = _EPOCH + timedelta(seconds=time_ms // 1000)
    return f"{stamp.strftime('%Y-%m-%dT%H:%M:%S')}.{time_ms % 1000:03d}Z"


def _require_real_oracle_source(value: Any, event_id: str) -> str:
    """D-4: production needs an oracle capture at the funding instant, named by
    digest and JSON pointer. A back-derived price, an unresolved marker or a
    prose label is not that capture.

    The ``"derived" in value.casefold()`` check below is a naming-convention
    guard, not a cryptographic one: it catches a locator that says what it is
    (``DERIVED_FROM_PAYMENT``, ``derived: ...``) but admits any locator that
    merely matches ``<sha256>#<json-pointer>`` without saying so. Real
    verification that the pointer resolves to an actual oracle capture is
    O-1 (oracle capture tool), not built here.
    """
    if (
        not isinstance(value, str)
        or value.startswith("UNRESOLVED")
        or "derived" in value.casefold()
        or _REAL_ORACLE_LOCATOR.fullmatch(value) is None
    ):
        raise _Refusal(
            CANDIDATE_ORACLE_EVIDENCE_UNAVAILABLE,
            f"D-4: binding {event_id} oracle_price_source must name an oracle capture "
            f"at the funding instant as <sha256>#<json-pointer>; a price derived from "
            f"the payment is research evidence only and is never admitted, got {value!r}",
        )
    return value


def _require_real_source_event_digest(value: Any, event_id: str) -> str:
    if not isinstance(value, str) or _REAL_SOURCE_EVENT_DIGEST.fullmatch(value) is None:
        raise _Refusal(
            CANDIDATE_BINDING_INVALID,
            f"D-1: binding {event_id} source_event_digest must be "
            f"{REAL_SOURCE_EVENT_DIGEST_DOMAIN}:<lower-case sha256 of the exact captured "
            f"funding row bytes>, got {value!r}",
        )
    return value


def _validate_binding(raw: Any, profile: _EvidenceProfile) -> dict[str, Any]:
    fields = _require_closed_mapping(
        raw, profile.binding_keys, "binding", CANDIDATE_BINDING_INVALID
    )
    event_id = _require_text(
        fields["funding_event_id"],
        "binding funding_event_id",
        CANDIDATE_BINDING_INVALID,
    )
    instant = _parse_instant(
        fields["event_timestamp"], f"binding {event_id} event_timestamp"
    )
    payer = fields["positive_rate_payer"]
    if payer != APPROVED_PAYER:
        raise _Refusal(
            CANDIDATE_BINDING_INVALID,
            f"binding {event_id} positive_rate_payer must be the approved "
            f"{APPROVED_PAYER} convention, got {payer!r}",
        )
    raw_rate_text, _ = _parse_decimal(
        fields["raw_rate"], f"binding {event_id} raw_rate"
    )
    if profile is _REAL_PROFILE:
        oracle_source = _require_real_oracle_source(
            fields["oracle_price_source"], event_id
        )
    else:
        oracle_source = _require_text(
            fields["oracle_price_source"],
            f"binding {event_id} oracle_price_source",
            CANDIDATE_BINDING_INVALID,
        )
    price_text, price = _parse_decimal(
        fields["oracle_price"], f"binding {event_id} oracle_price"
    )
    if price <= 0:
        raise _Refusal(
            CANDIDATE_BINDING_INVALID,
            f"binding {event_id} oracle_price must be positive",
        )
    body = {
        "event_timestamp": instant.text,
        "funding_event_id": event_id,
        "oracle_price": price_text,
        "oracle_price_source": oracle_source,
        "positive_rate_payer": payer,
        "provenance": _validate_provenance(fields["provenance"], event_id, profile),
        "raw_rate": raw_rate_text,
    }
    if profile is _REAL_PROFILE:
        body["source_event_digest"] = _require_real_source_event_digest(
            fields["source_event_digest"], event_id
        )
        digest_hex = _REAL_SOURCE_EVENT_DIGEST.fullmatch(
            body["source_event_digest"]
        ).group("hex")
        hour = _parse_instant(
            fields["interval_hour_utc"], f"binding {event_id} interval_hour_utc"
        )
        expected_hour = _hour_text(instant.seconds - instant.seconds % _HOUR_SECONDS)
        if fields["interval_hour_utc"] != expected_hour or hour.text != expected_hour:
            raise _Refusal(
                CANDIDATE_BINDING_INVALID,
                f"D-3: binding {event_id} interval_hour_utc must be the venue stamp "
                f"floored to the hour, {expected_hour!r}, got {fields['interval_hour_utc']!r}",
            )
        body["interval_hour_utc"] = expected_hour
    else:
        body["source_event_digest"] = _require_digest(
            fields["source_event_digest"],
            f"binding {event_id} source_event_digest",
            CANDIDATE_BINDING_INVALID,
        )
        digest_hex = body["source_event_digest"]
    return {
        "event_id": event_id,
        "instant": instant,
        "digest_hex": digest_hex,
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
        decoded = _strict_json_loads(source)
    except (UnicodeDecodeError, TypeError, ValueError) as exc:
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
    try:
        canonical_source = canonical_reconcile_json(decoded).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise _Refusal(
            CANDIDATE_BINDING_INVALID,
            f"binding {event_id} source bytes cannot be canonicalized: {exc}",
        ) from exc
    if canonical_source != source:
        raise _Refusal(
            CANDIDATE_BINDING_INVALID,
            f"binding {event_id} source bytes are not the exact canonical encoding",
        )
    if dict(decoded) != binding["source_fields"]:
        raise _Refusal(
            CANDIDATE_BINDING_INVALID,
            f"binding {event_id} source witness does not describe this binding",
        )


# ---------------------------------------------------------------------------
# Real read-only capture profile — the venue bytes are parsed, never grepped
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class _PassRow:
    """One funding row exactly as captured: its byte span inside the pass, the
    venue's fields, and the identity D-2 derives from them."""

    index: int
    raw: bytes
    time_ms: int
    coin: str
    usdc: Decimal
    szi: Decimal
    rate_text: str
    event_id: str


def _json_array_spans(payload: bytes, label: str) -> list[tuple[bytes, Any]]:
    """Every element of a captured JSON array as (exact bytes, decoded value)."""
    try:
        text = payload.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise _Refusal(
            CANDIDATE_COVERAGE_INVALID, f"D-6: {label} is not UTF-8: {exc}"
        ) from exc
    decoder = json.JSONDecoder(
        object_pairs_hook=_reject_duplicate_object, parse_constant=_reject_json_constant
    )
    whitespace = " \t\r\n"
    index = 0
    try:
        while text[index] in whitespace:
            index += 1
        if text[index] != "[":
            raise _Refusal(
                CANDIDATE_COVERAGE_INVALID, f"D-6: {label} is not a JSON array"
            )
        index += 1
        spans: list[tuple[bytes, Any]] = []
        while True:
            while text[index] in whitespace:
                index += 1
            if text[index] == "]":
                index += 1
                break
            if spans:
                if text[index] != ",":
                    raise _Refusal(
                        CANDIDATE_COVERAGE_INVALID, f"D-6: {label} is not a JSON array"
                    )
                index += 1
                while text[index] in whitespace:
                    index += 1
            value, end = decoder.raw_decode(text, index)
            spans.append((text[index:end].encode("utf-8"), value))
            index = end
        if text[index:].strip(whitespace):
            raise _Refusal(
                CANDIDATE_COVERAGE_INVALID, f"D-6: {label} carries trailing bytes"
            )
    except (IndexError, ValueError) as exc:
        raise _Refusal(
            CANDIDATE_COVERAGE_INVALID, f"D-6: {label} is not a JSON array: {exc}"
        ) from exc
    return spans


def _row_decimal(value: Any, label: str) -> tuple[str, Decimal]:
    try:
        return _parse_decimal(value, label)
    except _Refusal as exc:
        raise _Refusal(CANDIDATE_COVERAGE_INVALID, f"D-6: {exc.detail}") from exc


def _real_pass_rows(pass_bytes: bytes, account_scope: str) -> list[_PassRow]:
    rows: list[_PassRow] = []
    for index, (raw, value) in enumerate(_json_array_spans(pass_bytes, "funding pass")):
        label = f"funding pass row {index}"
        if not isinstance(value, Mapping) or not isinstance(
            value.get("delta"), Mapping
        ):
            raise _Refusal(
                CANDIDATE_COVERAGE_INVALID, f"D-6: {label} is not a venue funding row"
            )
        time_ms = value.get("time")
        delta = value["delta"]
        if isinstance(time_ms, bool) or not isinstance(time_ms, int) or time_ms < 0:
            raise _Refusal(
                CANDIDATE_COVERAGE_INVALID,
                f"D-6: {label} time is not a millisecond stamp",
            )
        if delta.get("type") != "funding":
            raise _Refusal(
                CANDIDATE_COVERAGE_INVALID, f"D-6: {label} is not a funding delta"
            )
        coin = delta.get("coin")
        if not isinstance(coin, str) or not coin:
            raise _Refusal(CANDIDATE_COVERAGE_INVALID, f"D-6: {label} carries no coin")
        _, usdc = _row_decimal(delta.get("usdc"), f"{label} usdc")
        _, szi = _row_decimal(delta.get("szi"), f"{label} szi")
        rate_text, _ = _row_decimal(delta.get("fundingRate"), f"{label} fundingRate")
        rows.append(
            _PassRow(
                index=index,
                raw=raw,
                time_ms=time_ms,
                coin=coin,
                usdc=usdc,
                szi=szi,
                rate_text=rate_text,
                event_id=f"{REAL_EVENT_ID_PREFIX}:{account_scope}:{coin}:{time_ms}",
            )
        )
    return rows


def _real_fills(
    fills_bytes: bytes, symbol: str
) -> tuple[Decimal | None, list[tuple[int, Decimal]]]:
    """The coin's fills as (time_ms, signed size), plus the position before the
    first of them, each fill's ``startPosition`` re-checked against the running
    position so a gap in the captured history cannot pass as continuity."""
    fills: list[tuple[int, Decimal, Decimal]] = []
    for index, (_, value) in enumerate(_json_array_spans(fills_bytes, "fills witness")):
        label = f"fills witness row {index}"
        if not isinstance(value, Mapping):
            raise _Refusal(
                CANDIDATE_COVERAGE_INVALID, f"D-6: {label} is not a venue fill row"
            )
        if value.get("coin") != symbol:
            if not isinstance(value.get("coin"), str):
                raise _Refusal(
                    CANDIDATE_COVERAGE_INVALID, f"D-6: {label} carries no coin"
                )
            continue
        time_ms = value.get("time")
        side = value.get("side")
        if (
            isinstance(time_ms, bool)
            or not isinstance(time_ms, int)
            or side not in ("A", "B")
        ):
            raise _Refusal(
                CANDIDATE_COVERAGE_INVALID, f"D-6: {label} is not a venue fill row"
            )
        _, size = _row_decimal(value.get("sz"), f"{label} sz")
        _, start_position = _row_decimal(
            value.get("startPosition"), f"{label} startPosition"
        )
        fills.append((time_ms, size if side == "B" else -size, start_position))
    fills.sort(key=lambda item: item[0])
    if not fills:
        return None, []
    running = fills[0][2]
    opening = running
    for time_ms, signed, start_position in fills:
        if start_position != running:
            raise _Refusal(
                CANDIDATE_COVERAGE_INVALID,
                f"D-6: the fills witness is not a contiguous {symbol} position history "
                f"(a fill at {_millisecond_text(time_ms)} starts from {start_position} "
                f"while the preceding fills leave {running})",
            )
        running += signed
    return opening, [(time_ms, signed) for time_ms, signed, _ in fills]


def _real_completion(
    pass_rows: list[_PassRow],
    fills_bytes: bytes,
    symbol: str,
    start: _Instant,
    end: _Instant,
) -> dict[str, Any]:
    """D-6 (ii): every whole hour of the window at which the fills-derived
    position is open must carry a payment, and every payment's own ``szi``
    must be that position. The grid runs ``[start+1h, end]``: the window's own
    start hour is excluded (D6-GRID A, ``OD-20260919-P012-D6-GRID-A-1``) to
    mirror the D6-START B admission band, which never admits a payment stamped
    within the tolerance of `start` into THIS window (it settles the previous
    one); the end hour itself stays in the grid because the venue stamps its
    payment inside the 1-second tolerance, which the admission band does
    admit here."""
    opening, fills = _real_fills(fills_bytes, symbol)
    # No fill for the symbol inside the fills witness: the position cannot change
    # inside the window, so the payments' own szi is the only position on record;
    # the completion check then names that producer, never the fills witness
    # (lane-8 exact-Opus review of 9ef072a8, REQUIRED-1).
    payments_position: Decimal | None = None
    if opening is None:
        constant = {row.szi for row in pass_rows}
        if len(constant) != 1:
            raise _Refusal(
                CANDIDATE_COVERAGE_INVALID,
                "D-6: the fills witness carries no fill for the coin, so the position "
                "cannot change inside the window, yet the captured payments show "
                f"positions {sorted(str(item) for item in constant)}",
            )
        payments_position = next(iter(constant))

    def position_at(time_ms: int) -> Decimal:
        if payments_position is not None:
            return payments_position
        return (Decimal(0) if opening is None else opening) + sum(
            (signed for fill_ms, signed in fills if fill_ms < time_ms), Decimal(0)
        )

    grid = list(range(start.seconds + _HOUR_SECONDS, end.seconds + 1, _HOUR_SECONDS))
    expected = [_hour_text(hour) for hour in grid if position_at(hour * 1000) != 0]
    observed = sorted(
        {
            _hour_text(row.time_ms // 1000 - (row.time_ms // 1000) % _HOUR_SECONDS)
            for row in pass_rows
        }
    )
    if expected != observed:
        raise _Refusal(
            CANDIDATE_COVERAGE_INVALID,
            "D-6: the fills-derived position expects payments at "
            f"{expected} but the captured funding passes carry payments at {observed}",
        )
    for row in pass_rows:
        at_stamp = position_at(row.time_ms)
        if at_stamp != row.szi:
            raise _Refusal(
                CANDIDATE_COVERAGE_INVALID,
                f"D-6: funding row {row.index} reports szi {row.szi} at "
                f"{_millisecond_text(row.time_ms)} while the fills witness gives {at_stamp}",
            )
    return {
        "expected_funding_hours": expected,
        "observed_funding_hours": observed,
        "opening_position": None if opening is None else str(opening),
        "position_source": (
            REAL_POSITION_SOURCE_PAYMENTS
            if payments_position is not None
            else REAL_POSITION_SOURCE_FILLS
        ),
    }


def _verify_real_row_witness(
    binding: Mapping[str, Any],
    source_hex: str,
    rows_by_index: Mapping[int, _PassRow],
    pass_sha256: str,
) -> None:
    """D-1, D-2, D-3 and the rate/payer facts, all re-derived from the captured
    row the binding points at; the binding's own claims are never trusted."""
    event_id = binding["event_id"]
    body = binding["body"]
    locator = _REAL_SOURCE_LOCATOR.fullmatch(body["provenance"]["source_locator"])
    if locator is None or int(locator.group("index")) not in rows_by_index:
        raise _Refusal(
            CANDIDATE_BINDING_INVALID,
            f"D-1: binding {event_id} provenance.source_locator must point at a row of the "
            f"captured funding pass as <file>#/<index>, got {body['provenance']['source_locator']!r}",
        )
    row = rows_by_index[int(locator.group("index"))]
    if bytes.fromhex(source_hex) != row.raw:
        raise _Refusal(
            CANDIDATE_BINDING_INVALID,
            f"D-1: binding {event_id} source witness bytes are not the located row "
            f"{row.index} of the captured funding pass",
        )
    if hashlib.sha256(row.raw).hexdigest() != binding["digest_hex"]:
        raise _Refusal(
            CANDIDATE_BINDING_INVALID,
            f"D-1: binding {event_id} source_event_digest does not hash the exact captured "
            f"bytes of funding row {row.index}",
        )
    if body["provenance"]["source_sha256"] != pass_sha256:
        raise _Refusal(
            CANDIDATE_BINDING_INVALID,
            f"binding {event_id} provenance.source_sha256 is not the digest of the "
            "captured funding pass it locates into",
        )
    if row.event_id != event_id:
        raise _Refusal(
            CANDIDATE_BINDING_INVALID,
            f"D-2: binding funding_event_id {event_id!r} is not the identity derived from "
            f"the located row, {row.event_id!r}",
        )
    stamp = _millisecond_text(row.time_ms)
    if body["event_timestamp"] != stamp:
        raise _Refusal(
            CANDIDATE_BINDING_INVALID,
            f"D-3: binding {event_id} event_timestamp must be the venue stamp verbatim, "
            f"{stamp!r}, got {body['event_timestamp']!r}",
        )
    if body["raw_rate"] != row.rate_text:
        raise _Refusal(
            CANDIDATE_BINDING_INVALID,
            f"binding {event_id} raw_rate {body['raw_rate']!r} is not the located row's "
            f"fundingRate {row.rate_text!r}",
        )
    rate = Decimal(row.rate_text)
    if row.usdc != 0 and row.szi != 0 and rate != 0:
        pays = (row.szi > 0) == (rate > 0)  # a long pays a positive rate
        if (row.usdc < 0) != pays:
            raise _Refusal(
                CANDIDATE_BINDING_INVALID,
                f"binding {event_id} positive_rate_payer {APPROVED_PAYER} contradicts the "
                f"located row (szi {row.szi}, fundingRate {row.rate_text}, usdc {row.usdc})",
            )


def _fold_unique(
    items: list[dict[str, Any]], key: str, label: str
) -> dict[str, dict[str, Any]]:
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


def _resolve_profile(evidence_kind: Any) -> _EvidenceProfile:
    profile = (
        _EVIDENCE_PROFILES.get(evidence_kind)
        if isinstance(evidence_kind, str)
        else None
    )
    if profile is None:
        raise _Refusal(
            CANDIDATE_PRODUCTION_EVIDENCE_UNAVAILABLE,
            f"evidence_kind {evidence_kind!r} names no evidence profile; the profiles are "
            f"{sorted(_EVIDENCE_PROFILES)} and none of them is a production mode",
        )
    return profile


def build_funding_candidate(
    retained_rows: Any,
    approved_event_bindings: Any,
    coverage: Any,
    schedule_id: Any,
    start_inclusive: Any,
    end_exclusive: Any,
    *,
    evidence_kind: str = SYNTHETIC_EVIDENCE_KIND,
) -> CandidateResult:
    """Build one funding candidate for a whole interval, or refuse.

    The result is atomic in meaning: either every inventoried event in
    ``[start_inclusive, end_exclusive)`` carries a verified retained payload
    and an explicit approved binding, or no candidate is produced at all. For
    the synthetic profile the admission band is exactly that interval
    (zero tolerance); for the real-capture profile it is shifted by the same
    settlement tolerance on both ends, ``[start+tolerance, end+tolerance)``
    (D6-START B). ``evidence_kind`` names the evidence profile the packet must
    satisfy; it defaults to the synthetic one and the packet must declare the
    same kind.
    """
    facts: dict[str, Any] = {}
    profile = _SYNTHETIC_PROFILE
    try:
        profile = _resolve_profile(evidence_kind)
        return _build(
            retained_rows,
            approved_event_bindings,
            coverage,
            schedule_id,
            start_inclusive,
            end_exclusive,
            facts,
            profile,
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
                profile=profile,
            ),
            evidence_kind=profile.kind,
        )


def _build(
    retained_rows: Any,
    approved_event_bindings: Any,
    coverage: Any,
    schedule_id: Any,
    start_inclusive: Any,
    end_exclusive: Any,
    facts: dict[str, Any],
    profile: _EvidenceProfile,
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
    facts["schedule_id"] = schedule

    witness, extras = _validate_coverage(coverage, start, end, profile)
    facts["symbol_scope"] = witness["symbol"]
    facts["account_scope"] = witness["account_scope"]
    facts["witness_identity"] = witness["witness_identity"]

    rows = [
        _validate_retained_row(raw)
        for raw in _require_sequence(retained_rows, "retained_rows")
    ]
    bindings = [
        _validate_binding(raw, profile)
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

    completion: dict[str, Any] | None = None
    rows_by_index: dict[int, _PassRow] = {}
    if profile is _REAL_PROFILE:
        pass_rows = _real_pass_rows(
            extras["funding_pass_bytes"], witness["account_scope"]
        )
        rows_by_index = {row.index: row for row in pass_rows}
        foreign = sorted(
            {row.coin for row in pass_rows if row.coin != witness["symbol"]}
        )
        if foreign:
            raise _Refusal(
                CANDIDATE_SYMBOL_MISMATCH,
                f"the captured funding pass carries rows for {foreign}, outside the "
                f"witnessed {witness['symbol']} scope",
            )
        if not inventory_set:
            raise _Refusal(
                CANDIDATE_COVERAGE_INVALID,
                "D-6: an empty inventory cannot be witnessed as a complete real capture",
            )
        pass_ids = [row.event_id for row in pass_rows]
        if len(set(pass_ids)) != len(pass_ids):
            raise _Refusal(
                CANDIDATE_COVERAGE_INVALID,
                "D-6: two captured funding rows derive the same identity",
            )
        uninventoried = sorted(set(pass_ids) - inventory_set)
        uncaptured = sorted(inventory_set - set(pass_ids))
        if uninventoried or uncaptured:
            raise _Refusal(
                CANDIDATE_COVERAGE_INVALID,
                "D-6: every row inside the captured funding pass needs a disposition "
                "under its D-2 identity hl-funding:<account-short>:<coin>:<time_ms>: "
                f"captured-but-uninventoried {uninventoried}, "
                f"inventoried-but-not-captured {uncaptured}",
            )
        completion = _real_completion(
            pass_rows, extras["fills_bytes"], witness["symbol"], start, end
        )

    # D6-START B (OD-20260918-P012-D6START-B-1): the SAME settlement tolerance
    # shifts BOTH boundaries, so the admission band is [start+tol, end+tol),
    # half-open. A payment stamped within the tolerance of `start` settles the
    # PREVIOUS window's last interval (mirror of the end rule) and is excluded
    # here; the previous window's own shifted band ends exactly where this one
    # begins, so the payment is attributed to exactly one window, never both,
    # and never dropped between them.
    start_limit = (start.seconds + profile.end_tolerance_seconds, start.fraction)
    end_limit = (end.seconds + profile.end_tolerance_seconds, end.fraction)
    events: list[dict[str, Any]] = []
    out_of_interval: list[str] = []
    for event_id in sorted(inventory_set):
        row = folded_rows[event_id]
        binding = folded_bindings[event_id]
        payload = _verify_retained_payload(row)
        if not (start_limit <= binding["instant"].sort_key < end_limit):
            out_of_interval.append(event_id)
            continue
        if binding["digest_hex"] == row["payload_digest"]:
            raise _Refusal(
                CANDIDATE_DIGEST_DOMAIN_CONFLATION,
                f"binding {event_id} reuses the normalized Bridge payload digest "
                "as a source_event_digest; the two byte domains are distinct",
            )
        if profile is _REAL_PROFILE:
            _verify_real_row_witness(
                binding,
                witness["source_witnesses"][event_id],
                rows_by_index,
                extras["funding_pass_sha256"],
            )
        else:
            _verify_source_witness(binding, witness["source_witnesses"][event_id])
        ledger_instant = row["ledger_instant"]
        events.append(
            {
                "sort_key": (binding["instant"].sort_key, event_id.encode("utf-8")),
                "body": {
                    "binding": binding["body"],
                    "binding_notes": {
                        "bridge_effective_ts_equals_binding_event_timestamp": (
                            ledger_instant.sort_key == binding["instant"].sort_key
                        ),
                        "settlement_rate_source": profile.settlement_source,
                        "settlement_time_source": profile.settlement_source,
                    },
                    "bridge_evidence": {
                        "attribution": row["attribution"],
                        "event_id": event_id,
                        "ledger_effective_ts": ledger_instant.text,
                        "payload": payload,
                        "payload_digest": row["payload_digest"],
                    },
                },
            }
        )

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
    effective_interval: dict[str, Any] = {
        "end_exclusive": end.text,
        "start_inclusive": start.text,
    }
    if profile is _REAL_PROFILE:
        # D6-START B: the SAME tolerance shifts both boundaries (Sol T0 review
        # of 8cbf4f1a, NIT-1: the prior output named only the end shift).
        effective_interval["start_tolerance_seconds"] = profile.end_tolerance_seconds
        effective_interval["end_tolerance_seconds"] = profile.end_tolerance_seconds
    candidate_body: dict[str, Any] = {
        "account_scope": witness["account_scope"],
        "coverage_witness": {
            **witness,
            "expected_event_ids": sorted(inventory),
            "unattributed_event_ids": sorted(witness["unattributed_event_ids"]),
        },
        "effective_interval": effective_interval,
        "event_count": len(events),
        "symbol_scope": witness["symbol"],
        profile.events_key: [event["body"] for event in events],
        profile.schedule_key: schedule,
    }
    if completion is not None:
        candidate_body["completion_check"] = completion
    candidate = {
        "admission_status": profile.admission_status,
        "artifact_kind": profile.artifact_kind,
        "bridge_payload_digest_domain": BRIDGE_PAYLOAD_DIGEST_DOMAIN,
        "not_a_production_record": profile.not_a_production_record,
        "numeric_representation": NUMERIC_REPRESENTATION,
        "source_event_digest_domain": profile.digest_domain,
        profile.candidate_key: candidate_body,
        "synthetic_only": profile.synthetic_only,
    }
    if profile is _REAL_PROFILE:
        candidate["evidence_kind"] = profile.kind
    body = canonical_reconcile_json(candidate).encode("utf-8") + b"\n"
    digest = hashlib.sha256(body).hexdigest()
    facts["event_count"] = len(events)
    facts["candidate_sha256"] = digest
    if profile is _REAL_PROFILE:
        detail = (
            "real-capture candidate bound under D-1..D-6 from the captured venue "
            'bytes; production admission is not granted (Q3 "Wait")'
        )
    else:
        detail = (
            "synthetic candidate built from synthetic caller facts; it is "
            "not evidence of real-world completeness"
        )
    return CandidateResult(
        accepted=True,
        reason_code=profile.built_code,
        report=_report(
            accepted=True,
            reason_code=profile.built_code,
            reason_detail=detail,
            facts=facts,
            profile=profile,
        ),
        candidate_bytes=body,
        candidate_sha256=digest,
        evidence_kind=profile.kind,
    )


def _report(
    *,
    accepted: bool,
    reason_code: str,
    reason_detail: str,
    facts: Mapping[str, Any],
    profile: _EvidenceProfile = _SYNTHETIC_PROFILE,
) -> dict[str, Any]:
    """One fully labelled, fully deterministic report. No clock is read."""
    return {
        "accepted": accepted,
        "candidate_sha256": facts.get("candidate_sha256"),
        "event_count": facts.get("event_count"),
        "evidence_kind": profile.kind,
        "evidence_limitations": list(profile.evidence_limitations),
        "inputs": {
            "account_scope": facts.get("account_scope"),
            "binding_count": facts.get("binding_count"),
            "interval": facts.get("interval"),
            "retained_row_count": facts.get("retained_row_count"),
            "symbol_scope": facts.get("symbol_scope"),
            profile.schedule_key: facts.get("schedule_id"),
            "witness_identity": facts.get("witness_identity"),
        },
        "inventory_missing_event_ids": facts.get("inventory_missing_event_ids", []),
        "inventory_unmatched_event_ids": facts.get("inventory_unmatched_event_ids", []),
        "non_admission": {
            "admission_status": profile.admission_status,
            "production_selection_keys_absent": [
                "events",
                "schedule_id",
                "settlement_currency",
            ],
            "statement": profile.not_a_production_record,
        },
        "out_of_interval_bindings": facts.get("out_of_interval_bindings", []),
        "out_of_scope_event_ids": facts.get("out_of_scope_event_ids", []),
        "production_mode": profile.production_mode,
        "reason_code": reason_code,
        "reason_detail": reason_detail,
        "report_kind": profile.report_kind,
        "store_reason_codes": facts.get("store_reason_codes", {}),
        "synthetic_only": profile.synthetic_only,
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
        raise _Refusal(
            CANDIDATE_SNAPSHOT_UNREADABLE, "cannot resolve the snapshot path"
        ) from exc
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
                    PAYLOAD_RETAINED
                    if payload is not None
                    else CANDIDATE_PAYLOAD_UNAVAILABLE
                )
            rows.append(
                {
                    "attribution": str(ledger["attribution"]),
                    "event_id": event_id,
                    "ledger_effective_ts": str(ledger["effective_ts"]),
                    "payload": payload,
                    "payload_digest": str(ledger["payload_digest"]),
                    "payload_reason": reason,
                    "symbol": str(ledger["symbol"]),
                }
            )
        return rows
    except sqlite3.Error as exc:
        raise _Refusal(
            CANDIDATE_SNAPSHOT_UNREADABLE,
            f"the snapshot is not a readable Bridge database: {type(exc).__name__}",
        ) from exc
    finally:
        conn.close()


def _load_packet(path: Path, profile: _EvidenceProfile) -> tuple[list[Any], Any]:
    try:
        raw = path.read_bytes()
    except OSError as exc:
        raise _Refusal(
            CANDIDATE_PACKET_INVALID,
            f"cannot read the binding packet: {type(exc).__name__}",
        ) from exc
    try:
        parsed = _strict_json_loads(raw)
    except (UnicodeDecodeError, TypeError, ValueError) as exc:
        raise _Refusal(
            CANDIDATE_PACKET_INVALID, f"the binding packet is not valid JSON: {exc}"
        ) from exc
    packet = _require_closed_mapping(
        parsed, PACKET_KEYS, "binding packet", CANDIDATE_PACKET_INVALID
    )
    if packet["packet_version"] != profile.packet_version:
        raise _Refusal(
            CANDIDATE_PACKET_INVALID,
            f"unsupported packet_version {packet['packet_version']!r}; under the "
            f"{profile.kind} profile this tool reads only {profile.packet_version}",
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


def _git_ancestor(path: Path) -> Path | None:
    absolute = Path(os.path.abspath(path))
    for candidate in (absolute, *absolute.parents):
        try:
            mode = (candidate / ".git").lstat().st_mode
        except FileNotFoundError:
            continue
        except OSError as exc:
            raise _Refusal(
                CANDIDATE_STAGING_UNSAFE,
                f"cannot inspect repository ancestry: {type(exc).__name__}",
            ) from exc
        if stat.S_ISDIR(mode) or stat.S_ISREG(mode):
            return candidate
    return None


def _is_under_mtc_tree(path: Path) -> bool:
    return any(
        candidate.name.casefold() == "mtc_command_center"
        for candidate in (path, *path.parents)
    )


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
    repository_root = _git_ancestor(resolved_root) or resolved_root
    if _contains_path(repository_root, resolved_staging):
        raise _Refusal(
            CANDIDATE_STAGING_UNSAFE,
            "the staging directory must be external to the Bridge repository",
        )
    if _git_ancestor(resolved_staging) is not None:
        raise _Refusal(
            CANDIDATE_STAGING_UNSAFE,
            "the staging directory must not be inside another Git checkout or worktree",
        )
    if _is_under_mtc_tree(resolved_staging):
        raise _Refusal(
            CANDIDATE_STAGING_UNSAFE,
            "the staging directory must not be under an MTC_COMMAND_CENTER tree",
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
    profile = _EVIDENCE_PROFILES[result.evidence_kind]
    report_bytes = canonical_reconcile_json(result.report).encode("utf-8") + b"\n"
    try:
        scratch = Path(tempfile.mkdtemp(prefix=f".{staging.name}.", dir=staging.parent))
    except OSError as exc:
        raise _Refusal(
            CANDIDATE_STAGING_FAILED,
            f"cannot create private staging scratch: {type(exc).__name__}",
        ) from exc
    try:
        if result.accepted:
            assert result.candidate_bytes is not None
            assert result.candidate_sha256 is not None
            candidate = scratch / profile.candidate_filename
            _write_new_file(candidate, result.candidate_bytes)
            sidecar = scratch / profile.sidecar_filename
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
            "Stage an MTC funding candidate from a quiescent offline Bridge "
            "snapshot and a separately verified binding packet, under the "
            "evidence profile named by --evidence-kind (SYNTHETIC_FIXTURE by "
            "default, or REAL_CAPTURE_READ_ONLY when named). "
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
    parser.add_argument(
        "--evidence-kind",
        dest="evidence_kind",
        choices=sorted(_EVIDENCE_PROFILES),
        default=SYNTHETIC_EVIDENCE_KIND,
        help=(
            "the evidence profile the packet must satisfy; the packet has to declare "
            "the same kind. Default: the synthetic profile. Neither is a production mode."
        ),
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = _parse_args(argv)
    profile = _EVIDENCE_PROFILES[args.evidence_kind]
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
        bindings, coverage = _load_packet(bindings_path, profile)
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
                    "schedule_id": args.schedule_id,
                    **refusal.facts,
                },
                profile=profile,
            ),
            evidence_kind=profile.kind,
        )
    else:
        result = build_funding_candidate(
            rows,
            bindings,
            coverage,
            args.schedule_id,
            args.start,
            args.end,
            evidence_kind=profile.kind,
        )

    try:
        _stage(staging, result)
    except _Refusal as refusal:
        print(f"{TOOL_NAME}: {refusal}", file=sys.stderr)
        return 1
    if not result.accepted:
        print(f"{TOOL_NAME}: refused ({result.reason_code})", file=sys.stderr)
        return 1
    label = "SYNTHETIC_ONLY" if profile.synthetic_only else profile.kind
    print(
        f"{TOOL_NAME}: staged {label} candidate "
        f"{result.candidate_sha256} under {staging.name}; it is not an accepted "
        "economic record"
    )
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
