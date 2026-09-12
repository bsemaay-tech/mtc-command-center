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
* In production mode a capture's digest and identity pointer are necessary but
  not sufficient: the capture must also *state* the coin, settlement time,
  rate, size and cash the candidate admits, and those must equal the retained
  eight-field payload. Agreement between the two evidence sources is still not
  provenance — both are supplied by the caller.
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
from decimal import Decimal, InvalidOperation
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

# --- OD-20260912-P012-PATHD-1 decision A: production mode ------------------
# Two disjoint modes.  ``SYNTHETIC`` is the frozen D1 behaviour and is the
# default everywhere; ``PRODUCTION`` is the owner-signed
# ``HL_FUNDING_VENUE_REPORTED_CASH_V1`` class.  Neither mode is an acceptance,
# and no literal, flag or evidence kind moves a run from one mode into the
# other: the mode is an explicit caller argument and each mode has its own
# closed key sets, its own evidence kinds and its own digest domain.
MODE_SYNTHETIC = "SYNTHETIC"
MODE_PRODUCTION = "PRODUCTION"
EXPORT_MODES = (MODE_SYNTHETIC, MODE_PRODUCTION)

PRODUCTION_SOURCE_CLASS = "HL_FUNDING_VENUE_REPORTED_CASH_V1"
PRODUCTION_EVIDENCE_KIND = PRODUCTION_SOURCE_CLASS
PRODUCTION_ACCEPTED_EVIDENCE_KINDS = (PRODUCTION_EVIDENCE_KIND,)
PRODUCTION_PACKET_VERSION = "HL_FUNDING_VENUE_REPORTED_CASH_BINDING_PACKET_V1"
PRODUCTION_ARTIFACT_KIND = "HL_FUNDING_VENUE_REPORTED_CASH_CANDIDATE_V1"
PRODUCTION_REPORT_KIND = "HL_FUNDING_VENUE_REPORTED_CASH_CANDIDATE_REPORT_V1"
# The real byte domain that replaces UNAVAILABLE_PENDING_SOURCE_EVENT_DIGEST_DOMAIN:
# lower-case hex SHA-256 over the exact, unmodified bytes of one authenticated
# own-account funding-history capture.  It is deliberately distinct from
# BRIDGE_PAYLOAD_DIGEST_DOMAIN, which hashes the Bridge's *normalized* payload.
PRODUCTION_SOURCE_EVENT_DIGEST_DOMAIN = (
    "HL_FUNDING_OWN_ACCOUNT_CAPTURE_BYTES_SHA256_V1"
)
PRODUCTION_ADMISSION_STATUS = "REFUSED_PENDING_T0_REVIEW_AND_OWNER_RATIFICATION"
# A1 = A forward-only.  The owner signed OD-20260912-P012-PATHD-1 in chat on
# 2026-09-12 at ~11:00Z (`PATH_D_DECISION_SIGNED_20260912.md`), and the
# decision admits own-account funding from that point forward only.  This is
# the exact lower bound a declared interval must respect; it is a constant of
# the decision, never derived from a clock, an input or an environment, so the
# same inputs always produce the same verdict.
PATH_D_SIGNATURE_INSTANT = "2026-09-12T11:00:00Z"
# The capture layout the production digest domain names.  A capture is one
# ``userFunding`` element: ``/hash`` is the settlement identity, ``/time`` is
# whole epoch milliseconds and ``/delta`` carries the coin, the payment rate,
# the position size and the settled cash.  These pointers are fixed, not
# caller-supplied: a caller who could choose where the values live could point
# every one of them at a field that happens to match.  A capture whose layout
# differs is refused rather than reinterpreted.
PRODUCTION_CAPTURE_IDENTITY_POINTER = "/hash"
PRODUCTION_CAPTURE_TIME_POINTER = "/time"
PRODUCTION_CAPTURE_TIME_UNIT = "EPOCH_MILLISECONDS"
PRODUCTION_CAPTURE_DELTA_TYPE_POINTER = "/delta/type"
PRODUCTION_CAPTURE_DELTA_TYPE = "funding"
# retained eight-field payload member -> pointer into the capture bytes.
PRODUCTION_CAPTURE_VALUE_POINTERS = {
    "amount_usdc": "/delta/usdc",
    "funding_rate": "/delta/fundingRate",
    "position_szi": "/delta/szi",
    "symbol": "/delta/coin",
}
PRODUCTION_SETTLEMENT_SOURCE = "HL_VENUE_REPORTED_OWN_ACCOUNT_SETTLEMENT"
NOT_AN_ACCEPTED_RECORD = (
    "Prepared under OD-20260912-P012-PATHD-1. This is not an accepted economic "
    "record: T0 review, R29 semantic redo, Section-16 record review, owner "
    "human ratification, current-head protected CI and protected merge all "
    "remain required, and no deploy, live-trading, order or ARM authority "
    "arises from it."
)
# A2 = B with M PENDING: the magnitude guard logs and raises a signed risk; it
# never refuses until the owner sets M after N observations.
MAGNITUDE_GUARD_SIGNED_RISK_ID = "PATHD-RISK-FUNDING-MAGNITUDE-M-PENDING-V1"
ORACLE_BINDING_SIGNED_RISK_ID = "PATHD-RISK-FUNDING-ORACLE-BINDING-OPEN-V1"
NO_INDEPENDENT_REVALUATION_SIGNED_RISK_ID = (
    "PATHD-RISK-FUNDING-NO-INDEPENDENT-REVALUATION-V1"
)

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
CANDIDATE_MODE_INVALID = "CANDIDATE_MODE_INVALID"
CANDIDATE_DECLARATION_UNSPECIFIED = "CANDIDATE_DECLARATION_UNSPECIFIED"
CANDIDATE_DECLARATION_MISMATCH = "CANDIDATE_DECLARATION_MISMATCH"
CANDIDATE_INTERVAL_COVERAGE_GAP = "CANDIDATE_INTERVAL_COVERAGE_GAP"
CANDIDATE_SETTLEMENT_KEY_CONFLICT = "CANDIDATE_SETTLEMENT_KEY_CONFLICT"
CANDIDATE_SETTLEMENT_TIME_CONFLICT = "CANDIDATE_SETTLEMENT_TIME_CONFLICT"
CANDIDATE_PAYER_SIGN_CONFLICT = "CANDIDATE_PAYER_SIGN_CONFLICT"
CANDIDATE_ORACLE_VALUE_REFUSED = "CANDIDATE_ORACLE_VALUE_REFUSED"
CANDIDATE_CONTEXT_RATE_SUBSTITUTION_REFUSED = (
    "CANDIDATE_CONTEXT_RATE_SUBSTITUTION_REFUSED"
)
CANDIDATE_CAPTURE_IDENTITY_UNBOUND = "CANDIDATE_CAPTURE_IDENTITY_UNBOUND"
CANDIDATE_CAPTURE_VALUE_MISMATCH = "CANDIDATE_CAPTURE_VALUE_MISMATCH"
CANDIDATE_CAPTURE_TIME_OUT_OF_INTERVAL = "CANDIDATE_CAPTURE_TIME_OUT_OF_INTERVAL"
CANDIDATE_FORWARD_ONLY_VIOLATION = "CANDIDATE_FORWARD_ONLY_VIOLATION"
CANDIDATE_DUPLICATE_SETTLEMENT = "CANDIDATE_DUPLICATE_SETTLEMENT"

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

# --- production-mode closed domains ---------------------------------------
# No oracle value and no substitute rate may enter a production binding: the
# admitted inputs are exactly the eight authoritative FundingEventRecord fields
# already retained by schema v10, read back from the Bridge ledger.
PRODUCTION_BINDING_KEYS = (
    "account_scope",
    "capture_identity_pointer",
    "event_timestamp",
    "funding_event_id",
    "positive_rate_payer",
    "provenance",
    "source_event_digest",
)
FORBIDDEN_ORACLE_BINDING_KEYS = (
    "mark_price",
    "markPx",
    "oracle_price",
    "oracle_price_source",
    "oracle_px",
    "oraclePx",
)
FORBIDDEN_RATE_BINDING_KEYS = (
    "context_funding_rate",
    "funding_rate",
    "fundingRate",
    "premium",
    "raw_rate",
)
PRODUCTION_COVERAGE_KEYS = COVERAGE_KEYS + (
    "declared_account",
    "declared_product",
    "gap_event_ids",
)
DECLARATION_KEYS = ("account", "interval", "product")

PRODUCTION_EVIDENCE_LIMITATIONS = (
    "Source class HL_FUNDING_VENUE_REPORTED_CASH_V1: the venue's own reported "
    "funding cash is booked as read. The Bridge never recomputes it from "
    "price x size and performs no independent revaluation, so a venue-side or "
    "capture-side error in an amount is undetectable by design.",
    "F-19/F-20 stay OPEN: no oracle value is admitted, derived or "
    "back-calculated, and the minute asset-context funding rate never "
    "substitutes for a payment rate. OPEN05 and OPEN07 stay OPEN.",
    "The magnitude guard A2 = B has M PENDING: rate magnitude is logged and "
    "carried as a signed risk, and never refuses, until the owner sets M after "
    "the declared observations.",
    "The declared account, product and interval are caller declarations "
    "recorded verbatim. This tool does not authenticate them and this artifact "
    "is not evidence that they are real.",
    "A1 = A is enforced forward-only from the owner signature instant "
    + PATH_D_SIGNATURE_INSTANT
    + ": a declared interval opening earlier is refused whole, never clipped, "
    "and every admitted settlement's authenticated capture time must fall "
    "inside the declared interval.",
    "The capture bytes must state the admitted values: the coin, settlement "
    "time, payment rate, position size and settled cash read out of the "
    "capture must equal the Bridge's retained eight-field payload for the same "
    "settlement, and the capture layout is fixed rather than caller-chosen. "
    "What this does NOT establish is provenance: the capture is still supplied "
    "by the caller, so agreement proves the two evidence sources tell one "
    "story, not that either came from the venue.",
    "An exact duplicate settlement refuses the whole candidate instead of "
    "collapsing into one event, so a double-counted row can never disappear "
    "silently.",
    "This artifact is not an accepted economic record: T0 review, R29 semantic "
    "redo, Section-16 record review and owner human ratification remain "
    "required, and it grants no deploy, live-trading, order or ARM authority.",
)

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
        offset_hours = int(offset[1:3])
        offset_minutes = int(offset[4:6])
        if offset_hours > 23 or offset_minutes > 59:
            raise _Refusal(
                CANDIDATE_TIMESTAMP_INVALID,
                f"{field} has an invalid RFC 3339 offset {offset!r}",
            )
        try:
            stamp -= timedelta(
                minutes=sign * (offset_hours * 60 + offset_minutes)
            )
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


def _instant_milliseconds(instant: _Instant) -> Decimal:
    """The instant as exact epoch milliseconds, subsecond digits intact."""
    return Decimal(instant.seconds) * 1000 + instant.fraction * 1000


# Parsed once, from the decision constant above, through the same parser every
# caller instant goes through.  No clock is read here or anywhere else.
_SIGNATURE_BOUND = _parse_instant(PATH_D_SIGNATURE_INSTANT, "PATH_D_SIGNATURE_INSTANT")


def _require_mode(mode: Any) -> str:
    if mode not in EXPORT_MODES:
        raise _Refusal(
            CANDIDATE_MODE_INVALID,
            f"mode must be one of {list(EXPORT_MODES)}, got {mode!r}",
        )
    return str(mode)


def _validate_declarations(mode: str, declarations: Any, start: _Instant, end: _Instant) -> dict[str, str]:
    """The DECLARED account/product/interval, or a typed refusal.

    OD-20260912-P012-PATHD-1 leaves account/product/interval UNSPECIFIED until
    authenticated evidence exists, so production mode refuses until a caller
    supplies all three explicitly.  Nothing is defaulted or inferred.

    A1 = A is forward-only, so the declared interval must also open at or after
    :data:`PATH_D_SIGNATURE_INSTANT`.  An interval reaching back before the
    owner's signature is refused outright; it is never clipped, shifted or
    partially admitted.
    """
    if mode != MODE_PRODUCTION:
        if declarations:
            raise _Refusal(
                CANDIDATE_DECLARATION_MISMATCH,
                "declarations are a production-mode input; synthetic mode takes none",
            )
        return {}
    if declarations is None:
        raise _Refusal(
            CANDIDATE_DECLARATION_UNSPECIFIED,
            "the declared account, product and interval are UNSPECIFIED under "
            "OD-20260912-P012-PATHD-1; production mode refuses until all three "
            "are supplied explicitly",
        )
    supplied = _require_closed_mapping(
        declarations, DECLARATION_KEYS, "declarations", CANDIDATE_DECLARATION_UNSPECIFIED
    )
    declared: dict[str, str] = {}
    for key in DECLARATION_KEYS:
        value = supplied[key]
        if not isinstance(value, str) or not value.strip():
            raise _Refusal(
                CANDIDATE_DECLARATION_UNSPECIFIED,
                f"declared {key} is UNSPECIFIED; production mode refuses until "
                "--declared-account, --declared-product and --declared-interval "
                "are all supplied",
            )
        declared[key] = value
    expected_interval = f"{start.text}/{end.text}"
    if declared["interval"] != expected_interval:
        raise _Refusal(
            CANDIDATE_DECLARATION_MISMATCH,
            f"declared interval {declared['interval']!r} is not the requested "
            f"interval {expected_interval!r}",
        )
    if start.sort_key < _SIGNATURE_BOUND.sort_key:
        raise _Refusal(
            CANDIDATE_FORWARD_ONLY_VIOLATION,
            f"the declared interval opens at {start.text}, before the Path D "
            f"signature instant {PATH_D_SIGNATURE_INSTANT}; A1 = A admits own "
            "account funding forward-only from the owner's signature, and a "
            "pre-signature interval is refused whole rather than clipped",
        )
    return declared


def _validate_coverage(
    coverage: Any,
    start: _Instant,
    end: _Instant,
    *,
    mode: str = MODE_SYNTHETIC,
    declared: Mapping[str, str] | None = None,
) -> dict[str, Any]:
    production = mode == MODE_PRODUCTION
    keys = PRODUCTION_COVERAGE_KEYS if production else COVERAGE_KEYS
    accepted_kinds = (
        PRODUCTION_ACCEPTED_EVIDENCE_KINDS if production else ACCEPTED_EVIDENCE_KINDS
    )
    witness = _require_closed_mapping(
        coverage, keys, "coverage", CANDIDATE_COVERAGE_INVALID
    )
    kind = witness["evidence_kind"]
    if kind not in accepted_kinds:
        raise _Refusal(
            CANDIDATE_PRODUCTION_EVIDENCE_UNAVAILABLE,
            "the production completion-evidence contract is not approved or "
            f"implemented; only {list(accepted_kinds)} is accepted, got {kind!r}",
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
    extra: dict[str, Any] = {}
    if production:
        declared = dict(declared or {})
        gaps = _require_id_list(witness["gap_event_ids"], "coverage.gap_event_ids")
        if gaps:
            # A3 = A: any gap refuses the WHOLE interval; nothing is interpolated
            # and no partial interval is ever published.
            raise _Refusal(
                CANDIDATE_INTERVAL_COVERAGE_GAP,
                "the declared interval carries settlement gaps "
                f"{sorted(gaps)}; the whole interval is refused and no "
                "settlement is interpolated or defaulted",
            )
        declared_account = _require_text(
            witness["declared_account"],
            "coverage.declared_account",
            CANDIDATE_DECLARATION_UNSPECIFIED,
        )
        declared_product = _require_text(
            witness["declared_product"],
            "coverage.declared_product",
            CANDIDATE_DECLARATION_UNSPECIFIED,
        )
        if declared_account != declared.get("account") or declared_product != declared.get(
            "product"
        ):
            raise _Refusal(
                CANDIDATE_DECLARATION_MISMATCH,
                "the completion witness declares account/product "
                f"{declared_account!r}/{declared_product!r}, which is not the "
                f"declared {declared.get('account')!r}/{declared.get('product')!r}",
            )
        if witness["account_scope"] != declared_account:
            raise _Refusal(
                CANDIDATE_DECLARATION_MISMATCH,
                "coverage.account_scope must be the declared account",
            )
        extra = {
            "declared_account": declared_account,
            "declared_product": declared_product,
            "gap_event_ids": [],
        }
    return {
        **extra,
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
    if payload is not None:
        for field, value in payload.items():
            _assert_finite(value, f"retained payload {event_id}.{field}")
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


def _validate_provenance(
    raw: Any, event_id: str, *, mode: str = MODE_SYNTHETIC
) -> dict[str, str]:
    provenance = _require_closed_mapping(
        raw, PROVENANCE_KEYS, f"binding {event_id} provenance", CANDIDATE_BINDING_INVALID
    )
    kind = provenance["evidence_kind"]
    accepted_kinds = (
        PRODUCTION_ACCEPTED_EVIDENCE_KINDS
        if mode == MODE_PRODUCTION
        else ACCEPTED_EVIDENCE_KINDS
    )
    if kind not in accepted_kinds:
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


def _validate_production_binding(raw: Any, declared: Mapping[str, str]) -> dict[str, Any]:
    """One production binding: identity, settlement time, payer, capture digest.

    A production binding carries *no* price and *no* rate.  The payment rate and
    the settled amount are the venue's own retained ``userFunding`` fields; the
    consumed oracle value (F-19/F-20) is not admitted, not derived and not
    back-calculated, and the minute asset-context funding rate can never enter
    here because the key is refused outright.
    """
    if isinstance(raw, Mapping):
        oracle_keys = sorted(set(raw) & set(FORBIDDEN_ORACLE_BINDING_KEYS))
        if oracle_keys:
            raise _Refusal(
                CANDIDATE_ORACLE_VALUE_REFUSED,
                f"production binding carries oracle fields {oracle_keys}; no "
                "oracle value is admitted, derived or back-calculated",
            )
        rate_keys = sorted(set(raw) & set(FORBIDDEN_RATE_BINDING_KEYS))
        if rate_keys:
            raise _Refusal(
                CANDIDATE_CONTEXT_RATE_SUBSTITUTION_REFUSED,
                f"production binding carries rate fields {rate_keys}; a context "
                "or caller-supplied rate never substitutes for the venue's own "
                "retained payment rate",
            )
    fields = _require_closed_mapping(
        raw, PRODUCTION_BINDING_KEYS, "production binding", CANDIDATE_BINDING_INVALID
    )
    event_id = _require_text(
        fields["funding_event_id"],
        "binding funding_event_id",
        CANDIDATE_BINDING_INVALID,
    )
    instant = _parse_instant(fields["event_timestamp"], f"binding {event_id} event_timestamp")
    payer = fields["positive_rate_payer"]
    if payer != APPROVED_PAYER:
        raise _Refusal(
            CANDIDATE_BINDING_INVALID,
            f"binding {event_id} positive_rate_payer must be the approved "
            f"{APPROVED_PAYER} convention, got {payer!r}",
        )
    account_scope = _require_text(
        fields["account_scope"], f"binding {event_id} account_scope", CANDIDATE_BINDING_INVALID
    )
    if account_scope != declared.get("account"):
        raise _Refusal(
            CANDIDATE_DECLARATION_MISMATCH,
            f"binding {event_id} is scoped to {account_scope!r}, not the "
            f"declared account {declared.get('account')!r}",
        )
    pointer = _require_text(
        fields["capture_identity_pointer"],
        f"binding {event_id} capture_identity_pointer",
        CANDIDATE_BINDING_INVALID,
    )
    if pointer != PRODUCTION_CAPTURE_IDENTITY_POINTER:
        # Fixed for the same reason the value pointers are: a caller free to
        # choose where the identity lives could aim at any field that happens
        # to spell this event id.  The binding still states the pointer
        # explicitly so the artifact records what was read.
        raise _Refusal(
            CANDIDATE_CAPTURE_IDENTITY_UNBOUND,
            f"binding {event_id} capture_identity_pointer must be the canonical "
            f"{PRODUCTION_CAPTURE_IDENTITY_POINTER!r} of an own-account funding "
            f"capture, got {pointer!r}",
        )
    body = {
        "account_scope": account_scope,
        "capture_identity_pointer": pointer,
        "event_timestamp": instant.text,
        "funding_event_id": event_id,
        "positive_rate_payer": payer,
        "provenance": _validate_provenance(
            fields["provenance"], event_id, mode=MODE_PRODUCTION
        ),
        "source_event_digest": _require_digest(
            fields["source_event_digest"],
            f"binding {event_id} source_event_digest",
            CANDIDATE_BINDING_INVALID,
        ),
    }
    return {"event_id": event_id, "instant": instant, "source_fields": {}, "body": body}


def _resolve_json_pointer(document: Any, pointer: str) -> Any:
    node = document
    for raw_token in pointer.split("/")[1:]:
        token = raw_token.replace("~1", "/").replace("~0", "~")
        if isinstance(node, Mapping):
            if token not in node:
                return None
            node = node[token]
            continue
        if isinstance(node, list):
            if not token.isdigit():
                return None
            index = int(token)
            if index >= len(node):
                return None
            node = node[index]
            continue
        return None
    return node


def _capture_number(value: Any, label: str) -> Decimal:
    """One capture or payload number as an exact decimal, or a refusal.

    Venue captures spell numbers as decimal strings and the Bridge retains
    them as floats, so both sides are normalized through :class:`Decimal`,
    which compares by value: ``"1.25e-05"``, ``"0.0000125"`` and
    ``0.0000125`` are one number, and ``999999`` is not ``-1.25``.
    """
    if value is None or isinstance(value, bool):
        raise _Refusal(
            CANDIDATE_CAPTURE_VALUE_MISMATCH, f"{label} is not a number: {value!r}"
        )
    if isinstance(value, float):
        if not math.isfinite(value):
            raise _Refusal(
                CANDIDATE_CAPTURE_VALUE_MISMATCH, f"{label} is not a finite number"
            )
        text = repr(value)
    elif isinstance(value, int):
        text = str(value)
    elif isinstance(value, str):
        text = value.strip()
    else:
        raise _Refusal(
            CANDIDATE_CAPTURE_VALUE_MISMATCH, f"{label} is not a number: {value!r}"
        )
    try:
        number = Decimal(text)
    except InvalidOperation as exc:
        raise _Refusal(
            CANDIDATE_CAPTURE_VALUE_MISMATCH,
            f"{label} is not an exact decimal number: {text!r}",
        ) from exc
    if not number.is_finite():
        raise _Refusal(
            CANDIDATE_CAPTURE_VALUE_MISMATCH, f"{label} is not a finite number"
        )
    return number


def _verify_capture_values(
    event_id: str,
    decoded: Any,
    payload: Mapping[str, Any],
    start: _Instant,
    end: _Instant,
) -> Decimal:
    """Prove the capture states the values this settlement was admitted on.

    A digest proves the bytes were not edited and the identity pointer proves
    they name this settlement; neither says the bytes *agree* with what is
    being booked.  Here the capture's own coin, settlement time, payment rate,
    position size and settled cash must equal the retained eight-field payload
    for the same event, and the capture's time must fall inside the declared
    interval (A1 = A).  Any disagreement refuses; nothing is reconciled,
    rounded or preferred.

    Returns the capture's settlement time in exact epoch milliseconds.
    """
    delta_type = _resolve_json_pointer(decoded, PRODUCTION_CAPTURE_DELTA_TYPE_POINTER)
    if delta_type != PRODUCTION_CAPTURE_DELTA_TYPE:
        raise _Refusal(
            CANDIDATE_CAPTURE_VALUE_MISMATCH,
            f"binding {event_id} capture {PRODUCTION_CAPTURE_DELTA_TYPE_POINTER} is "
            f"{delta_type!r}, not a {PRODUCTION_CAPTURE_DELTA_TYPE!r} delta; these "
            "bytes do not describe a funding settlement",
        )
    for field, pointer in sorted(PRODUCTION_CAPTURE_VALUE_POINTERS.items()):
        captured = _resolve_json_pointer(decoded, pointer)
        retained = payload.get(field)
        if field == "symbol":
            if not isinstance(captured, str) or captured != retained:
                raise _Refusal(
                    CANDIDATE_CAPTURE_VALUE_MISMATCH,
                    f"binding {event_id} capture {pointer} is {captured!r} but the "
                    f"retained payload {field} is {retained!r}",
                )
            continue
        if retained is None:
            raise _Refusal(
                CANDIDATE_CAPTURE_VALUE_MISMATCH,
                f"binding {event_id} cannot be bound to its capture: the retained "
                f"payload carries no {field}",
            )
        captured_number = _capture_number(
            captured, f"binding {event_id} capture {pointer}"
        )
        retained_number = _capture_number(
            retained, f"binding {event_id} retained payload {field}"
        )
        if captured_number != retained_number:
            raise _Refusal(
                CANDIDATE_CAPTURE_VALUE_MISMATCH,
                f"binding {event_id} capture {pointer} is {captured!r} but the "
                f"retained payload {field} is {retained!r}",
            )
    captured_ms = _capture_number(
        _resolve_json_pointer(decoded, PRODUCTION_CAPTURE_TIME_POINTER),
        f"binding {event_id} capture {PRODUCTION_CAPTURE_TIME_POINTER}",
    )
    settlement = _parse_instant(
        payload.get("effective_ts"), f"binding {event_id} retained payload effective_ts"
    )
    retained_ms = _instant_milliseconds(settlement)
    if captured_ms != retained_ms:
        # Exact equality in the millisecond domain: a capture that merely
        # truncates a finer retained instant is a mismatch, never a rounding.
        raise _Refusal(
            CANDIDATE_CAPTURE_VALUE_MISMATCH,
            f"binding {event_id} capture {PRODUCTION_CAPTURE_TIME_POINTER} is "
            f"{captured_ms} {PRODUCTION_CAPTURE_TIME_UNIT} but the retained payload "
            f"settles at {settlement.text} ({retained_ms})",
        )
    if not (
        _instant_milliseconds(start) <= captured_ms < _instant_milliseconds(end)
    ):
        raise _Refusal(
            CANDIDATE_CAPTURE_TIME_OUT_OF_INTERVAL,
            f"binding {event_id} authenticated capture settles at {settlement.text}, "
            f"outside the declared interval [{start.text}, {end.text})",
        )
    return captured_ms


def _verify_production_capture(
    binding: Mapping[str, Any],
    capture_hex: str,
    payload: Mapping[str, Any],
    start: _Instant,
    end: _Instant,
) -> int:
    """Bind one authenticated capture's exact bytes to this event.

    ``PRODUCTION_SOURCE_EVENT_DIGEST_DOMAIN`` is SHA-256 over these bytes as
    received.  The bytes are not normalized, not re-encoded and not
    canonicalized: the digest domain is the capture, so a Bridge payload digest
    can never be reused as one.

    Three separate questions are answered, and all three must hold: are these
    the bytes the binding declares (digest), do they name this settlement
    (identity pointer), and do they *state the admitted values* (value
    binding)?
    """
    event_id = binding["event_id"]
    try:
        capture = bytes.fromhex(capture_hex)
    except ValueError as exc:  # pragma: no cover - _require_source_witnesses screens this
        raise _Refusal(
            CANDIDATE_COVERAGE_INVALID,
            f"coverage.source_witnesses[{event_id!r}] is not hex",
        ) from exc
    digest = hashlib.sha256(capture).hexdigest()
    if binding["body"]["provenance"]["source_sha256"] != digest:
        raise _Refusal(
            CANDIDATE_BINDING_INVALID,
            f"binding {event_id} provenance.source_sha256 does not hash its "
            "captured bytes",
        )
    if binding["body"]["source_event_digest"] != digest:
        raise _Refusal(
            CANDIDATE_BINDING_INVALID,
            f"binding {event_id} source_event_digest does not hash its captured "
            f"bytes under {PRODUCTION_SOURCE_EVENT_DIGEST_DOMAIN}",
        )
    try:
        decoded = _strict_json_loads(capture)
    except (UnicodeDecodeError, TypeError, ValueError) as exc:
        raise _Refusal(
            CANDIDATE_BINDING_INVALID,
            f"binding {event_id} captured bytes are not strict UTF-8 JSON: {exc}",
        ) from exc
    identity = _resolve_json_pointer(decoded, binding["body"]["capture_identity_pointer"])
    if identity != event_id:
        raise _Refusal(
            CANDIDATE_CAPTURE_IDENTITY_UNBOUND,
            f"binding {event_id} capture_identity_pointer "
            f"{binding['body']['capture_identity_pointer']!r} resolves to "
            f"{identity!r}, so these bytes are not bound to this settlement",
        )
    _verify_capture_values(event_id, decoded, payload, start, end)
    return len(capture)


def _check_payer_sign(binding: Mapping[str, Any], payload: Mapping[str, Any]) -> None:
    """The settled cash sign must agree with the payer convention and the side.

    Under ``positive_rate_payer = LONG`` a long position with a positive rate
    pays, so ``amount_usdc`` must be non-positive; every other combination is
    mirrored.  A disagreeing row is refused rather than re-signed.
    """
    event_id = binding["event_id"]
    rate = payload.get("funding_rate")
    szi = payload.get("position_szi")
    amount = payload.get("amount_usdc")
    if rate is None or szi is None or amount is None:
        raise _Refusal(
            CANDIDATE_PAYER_SIGN_CONFLICT,
            f"event {event_id} cannot be sign-checked: the retained payload is "
            "missing funding_rate, position_szi or amount_usdc",
        )
    payer_factor = 1.0 if binding["body"]["positive_rate_payer"] == APPROVED_PAYER else -1.0
    side = 1.0 if float(szi) > 0 else -1.0 if float(szi) < 0 else 0.0
    rate_sign = 1.0 if float(rate) > 0 else -1.0 if float(rate) < 0 else 0.0
    expected = -payer_factor * side * rate_sign
    observed = 1.0 if float(amount) > 0 else -1.0 if float(amount) < 0 else 0.0
    if observed != expected:
        raise _Refusal(
            CANDIDATE_PAYER_SIGN_CONFLICT,
            f"event {event_id} settled {float(amount)} with rate {float(rate)} "
            f"and position_szi {float(szi)}; the "
            f"{binding['body']['positive_rate_payer']}-payer convention requires "
            f"sign {expected}, observed {observed}",
        )


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


def _fold_unique(
    items: list[dict[str, Any]],
    key: str,
    label: str,
    *,
    refuse_duplicates: bool = False,
) -> dict[str, dict[str, Any]]:
    """Collapse or refuse repeated identities; any conflict always refuses.

    ``refuse_duplicates`` is the production rule and is off for the frozen D1
    synthetic behaviour.  Under A3 whole-interval semantics a settlement that
    appears twice is a defect in the evidence, not a formatting artifact: one
    of the two rows is unexplained, and which one was double-counted upstream
    is exactly what a silent fold would hide.  So the whole candidate is
    refused rather than deduplicated.  Synthetic mode keeps folding identical
    entries byte for byte as before.
    """
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
        if refuse_duplicates:
            raise _Refusal(
                CANDIDATE_DUPLICATE_SETTLEMENT,
                f"{label} {identity} is supplied more than once; an exact "
                "duplicate settlement is refused, never folded, so a "
                "double-counted row cannot disappear into a single event",
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
    *,
    mode: str = MODE_SYNTHETIC,
    declarations: Any = None,
) -> CandidateResult:
    """Build one funding candidate for a whole interval, or refuse.

    The result is atomic in meaning: either every inventoried event in
    ``[start_inclusive, end_exclusive)`` carries a verified retained payload
    and an explicit approved binding, or no candidate is produced at all.

    ``mode`` defaults to :data:`MODE_SYNTHETIC`, which is the frozen D1
    behaviour, byte for byte.  :data:`MODE_PRODUCTION` is the owner-signed
    ``HL_FUNDING_VENUE_REPORTED_CASH_V1`` class and additionally requires the
    DECLARED account/product/interval; it is still not an acceptance.
    """
    facts: dict[str, Any] = {}
    try:
        selected = _require_mode(mode)
        facts["mode"] = selected
        return _build(
            retained_rows,
            approved_event_bindings,
            coverage,
            schedule_id,
            start_inclusive,
            end_exclusive,
            facts,
            selected,
            declarations,
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
                mode=facts.get("mode", MODE_SYNTHETIC),
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
    mode: str = MODE_SYNTHETIC,
    declarations: Any = None,
) -> CandidateResult:
    production = mode == MODE_PRODUCTION
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

    declared = _validate_declarations(mode, declarations, start, end)
    if production:
        facts["declarations"] = dict(declared)
    witness = _validate_coverage(coverage, start, end, mode=mode, declared=declared)
    facts["symbol_scope"] = witness["symbol"]
    facts["account_scope"] = witness["account_scope"]
    facts["witness_identity"] = witness["witness_identity"]

    rows = [_validate_retained_row(raw) for raw in _require_sequence(retained_rows, "retained_rows")]
    bindings = [
        (
            _validate_production_binding(raw, declared)
            if production
            else _validate_binding(raw)
        )
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

    folded_rows = _fold_unique(
        rows, "event_id", "retained row", refuse_duplicates=production
    )
    folded_bindings = _fold_unique(
        bindings, "event_id", "binding", refuse_duplicates=production
    )

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
    settlement_keys: dict[tuple[str, str, tuple[int, Decimal]], str] = {}
    magnitudes: list[tuple[float, str]] = []
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
        ledger_instant = row["ledger_instant"]
        if production:
            # F-16 exact-once: one settlement per (account, coin, event time).
            settlement_key = (
                binding["body"]["account_scope"],
                row["symbol"],
                binding["instant"].sort_key,
            )
            duplicate = settlement_keys.get(settlement_key)
            if duplicate is not None:
                raise _Refusal(
                    CANDIDATE_SETTLEMENT_KEY_CONFLICT,
                    f"events {duplicate} and {event_id} claim the same "
                    f"(account, coin, event time) settlement "
                    f"({settlement_key[0]}, {settlement_key[1]}, "
                    f"{binding['instant'].text})",
                )
            settlement_keys[settlement_key] = event_id
            if ledger_instant.sort_key != binding["instant"].sort_key:
                raise _Refusal(
                    CANDIDATE_SETTLEMENT_TIME_CONFLICT,
                    f"binding {event_id} settles at {binding['instant'].text} "
                    f"but the venue's own retained row is {ledger_instant.text}",
                )
            _verify_production_capture(
                binding, witness["source_witnesses"][event_id], payload, start, end
            )
            _check_payer_sign(binding, payload)
            rate = payload.get("funding_rate")
            if rate is not None:
                magnitudes.append((abs(float(rate)), event_id))
            notes = {
                "bridge_effective_ts_equals_binding_event_timestamp": True,
                "capture_values_bound_to_retained_payload": True,
                "capture_value_pointers": dict(PRODUCTION_CAPTURE_VALUE_POINTERS),
                "capture_time_pointer": PRODUCTION_CAPTURE_TIME_POINTER,
                "capture_time_unit": PRODUCTION_CAPTURE_TIME_UNIT,
                "settlement_rate_source": PRODUCTION_SETTLEMENT_SOURCE,
                "settlement_time_source": PRODUCTION_SETTLEMENT_SOURCE,
                "oracle_value_admitted": False,
                "oracle_value_back_calculated": False,
                "source_event_digest_domain": PRODUCTION_SOURCE_EVENT_DIGEST_DOMAIN,
            }
        else:
            _verify_source_witness(binding, witness["source_witnesses"][event_id])
            notes = {
                "bridge_effective_ts_equals_binding_event_timestamp": (
                    ledger_instant.sort_key == binding["instant"].sort_key
                ),
                "settlement_rate_source": SETTLEMENT_SOURCE,
                "settlement_time_source": SETTLEMENT_SOURCE,
            }
        events.append({
            "sort_key": (binding["instant"].sort_key, event_id.encode("utf-8")),
            "body": {
                "binding": binding["body"],
                "binding_notes": notes,
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
    inner = {
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
    }
    if production:
        # A2 = B with M PENDING: log the observed magnitudes and raise the
        # signed risk; never refuse on magnitude.
        magnitudes.sort()
        facts["signed_risk_markers"] = [
            {
                "signed_risk_id": MAGNITUDE_GUARD_SIGNED_RISK_ID,
                "state": "M_PENDING",
                "statement": (
                    "The A2 magnitude cap M is not set. Observed |funding_rate| "
                    "values are logged and never refused until the owner sets M "
                    "after the declared observations."
                ),
                "observed_absolute_rates": [repr(value) for value, _event in magnitudes],
                "largest_observed_event_id": magnitudes[-1][1] if magnitudes else None,
            },
            {
                "signed_risk_id": ORACLE_BINDING_SIGNED_RISK_ID,
                "state": "OPEN",
                "statement": (
                    "F-19/F-20 are unanswered. No oracle value is admitted, "
                    "derived or back-calculated here; OPEN05 and OPEN07 stay OPEN."
                ),
            },
            {
                "signed_risk_id": NO_INDEPENDENT_REVALUATION_SIGNED_RISK_ID,
                "state": "ACCEPTED",
                "statement": (
                    "The venue's own reported funding cash is booked without "
                    "independent revaluation."
                ),
            },
        ]
        candidate = {
            "admission_status": PRODUCTION_ADMISSION_STATUS,
            "artifact_kind": PRODUCTION_ARTIFACT_KIND,
            "bridge_payload_digest_domain": BRIDGE_PAYLOAD_DIGEST_DOMAIN,
            "declarations": dict(declared),
            "not_an_accepted_record": NOT_AN_ACCEPTED_RECORD,
            "numeric_representation": NUMERIC_REPRESENTATION,
            "production_candidate": {
                **inner,
                "settlement_events": [event["body"] for event in events],
                "target_schedule_id": schedule,
            },
            "signed_risk_markers": facts["signed_risk_markers"],
            "source_class": PRODUCTION_SOURCE_CLASS,
            "source_event_digest_domain": PRODUCTION_SOURCE_EVENT_DIGEST_DOMAIN,
            "synthetic_only": False,
        }
        outcome_detail = (
            "production candidate built for the declared account/product/"
            "interval under " + PRODUCTION_SOURCE_CLASS + "; it is not an "
            "accepted economic record"
        )
    else:
        candidate = {
            "admission_status": ADMISSION_STATUS,
            "artifact_kind": ARTIFACT_KIND,
            "bridge_payload_digest_domain": BRIDGE_PAYLOAD_DIGEST_DOMAIN,
            "not_a_production_record": NOT_A_PRODUCTION_RECORD,
            "numeric_representation": NUMERIC_REPRESENTATION,
            "source_event_digest_domain": SOURCE_EVENT_DIGEST_DOMAIN,
            "synthetic_candidate": {
                **inner,
                "synthetic_events": [event["body"] for event in events],
                "synthetic_schedule_id": schedule,
            },
            "synthetic_only": True,
        }
        outcome_detail = (
            "synthetic candidate built from synthetic caller facts; it is "
            "not evidence of real-world completeness"
        )
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
            reason_detail=outcome_detail,
            facts=facts,
            mode=mode,
        ),
        candidate_bytes=body,
        candidate_sha256=digest,
    )


def _report(
    *,
    accepted: bool,
    reason_code: str,
    reason_detail: str,
    facts: Mapping[str, Any],
    mode: str = MODE_SYNTHETIC,
) -> dict[str, Any]:
    """One fully labelled, fully deterministic report. No clock is read."""
    if mode == MODE_PRODUCTION:
        return {
            "accepted": accepted,
            "candidate_sha256": facts.get("candidate_sha256"),
            "declarations": facts.get("declarations"),
            "event_count": facts.get("event_count"),
            "evidence_limitations": list(PRODUCTION_EVIDENCE_LIMITATIONS),
            "inputs": {
                "account_scope": facts.get("account_scope"),
                "binding_count": facts.get("binding_count"),
                "interval": facts.get("interval"),
                "retained_row_count": facts.get("retained_row_count"),
                "symbol_scope": facts.get("symbol_scope"),
                "target_schedule_id": facts.get("synthetic_schedule_id"),
                "witness_identity": facts.get("witness_identity"),
            },
            "inventory_missing_event_ids": facts.get("inventory_missing_event_ids", []),
            "inventory_unmatched_event_ids": facts.get("inventory_unmatched_event_ids", []),
            "mode": MODE_PRODUCTION,
            "non_admission": {
                "admission_status": PRODUCTION_ADMISSION_STATUS,
                "production_selection_keys_absent": [
                    "events",
                    "schedule_id",
                    "settlement_currency",
                ],
                "statement": NOT_AN_ACCEPTED_RECORD,
            },
            "out_of_interval_bindings": facts.get("out_of_interval_bindings", []),
            "out_of_scope_event_ids": facts.get("out_of_scope_event_ids", []),
            "production_mode": PRODUCTION_SOURCE_EVENT_DIGEST_DOMAIN,
            "reason_code": reason_code,
            "reason_detail": reason_detail,
            "report_kind": PRODUCTION_REPORT_KIND,
            "signed_risk_markers": facts.get("signed_risk_markers", []),
            "source_class": PRODUCTION_SOURCE_CLASS,
            "store_reason_codes": facts.get("store_reason_codes", {}),
            "synthetic_only": False,
            "unbound_events": facts.get("unbound_events", []),
            "uninventoried_event_ids": facts.get("uninventoried_event_ids", []),
            "unknown_binding_event_ids": facts.get("unknown_binding_event_ids", []),
        }
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


def _load_packet(path: Path, mode: str = MODE_SYNTHETIC) -> tuple[list[Any], Any]:
    expected_version = (
        PRODUCTION_PACKET_VERSION if mode == MODE_PRODUCTION else PACKET_VERSION
    )
    try:
        raw = path.read_bytes()
    except OSError as exc:
        raise _Refusal(
            CANDIDATE_PACKET_INVALID, f"cannot read the binding packet: {type(exc).__name__}"
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
    if packet["packet_version"] != expected_version:
        raise _Refusal(
            CANDIDATE_PACKET_INVALID,
            f"unsupported packet_version {packet['packet_version']!r}; this mode "
            f"reads only {expected_version}",
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
    parser.add_argument("--mode", choices=list(EXPORT_MODES), default=MODE_SYNTHETIC)
    parser.add_argument("--declared-account", dest="declared_account", default=None)
    parser.add_argument("--declared-product", dest="declared_product", default=None)
    parser.add_argument("--declared-interval", dest="declared_interval", default=None)
    return parser.parse_args(argv)


def _cli_declarations(args: argparse.Namespace) -> dict[str, Any] | None:
    if args.mode != MODE_PRODUCTION:
        return None
    supplied = {
        "account": args.declared_account,
        "interval": args.declared_interval,
        "product": args.declared_product,
    }
    if all(value is None for value in supplied.values()):
        # Every declaration is UNSPECIFIED: let the pure function raise the one
        # typed refusal rather than inventing a partial declaration here.
        return None
    return supplied


def main(argv: Sequence[str] | None = None) -> int:
    args = _parse_args(argv)
    staging = Path(args.staging)
    snapshot = Path(args.snapshot)
    bindings_path = Path(args.bindings)
    mode = args.mode
    declarations = _cli_declarations(args)
    try:
        _prepare_staging(staging, snapshot, bindings_path)
    except _Refusal as refusal:
        print(f"{TOOL_NAME}: {refusal}", file=sys.stderr)
        return 1

    try:
        _assert_quiescent(snapshot)
        before = _sha256_file(snapshot)
        bindings, coverage = _load_packet(bindings_path, mode)
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
                mode=mode,
            ),
        )
    else:
        result = build_funding_candidate(
            rows,
            bindings,
            coverage,
            args.schedule_id,
            args.start,
            args.end,
            mode=mode,
            declarations=declarations,
        )

    try:
        _stage(staging, result)
    except _Refusal as refusal:
        print(f"{TOOL_NAME}: {refusal}", file=sys.stderr)
        return 1
    if not result.accepted:
        print(f"{TOOL_NAME}: refused ({result.reason_code})", file=sys.stderr)
        return 1
    label = MODE_PRODUCTION if mode == MODE_PRODUCTION else "SYNTHETIC_ONLY"
    print(
        f"{TOOL_NAME}: staged {label} candidate "
        f"{result.candidate_sha256} under {staging.name}; it is not an accepted "
        "economic record"
    )
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
