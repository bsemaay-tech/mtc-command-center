"""WP-P0-12 O-1 Phase A — verify oracle reads taken around a funding instant (2026-09-19).

A sibling of ``capture_own_account_evidence.py``; that tool is not touched. This one has two
jobs and admits nothing by itself:

* ``--verify-existing <reads-dir>`` (the mode Phase A uses): read the oracle reader's own
  outputs — ``ORACLE_READS_MANIFEST.jsonl``, the raw response files it names and their
  ``.sha256`` sidecars — **exactly as they are**, and decide whether a funding instant has a
  genuine, fresh, self-consistent bracket. Nothing in the reader's directory is rewritten,
  moved, renamed, re-hashed or supplemented. Every output of this tool goes elsewhere.
* the scheduled collector (``plan_bracket`` / ``collect_bracket``) for future windows. Phase A
  ships **no transport at all**: the collector must be handed one explicitly, so this module
  has no code path that can reach a venue. Wiring a live transport is separately authorized
  work and must never run while the Lead's reader is running.

The contract implemented here is ``ADMISSION_G2_R3_LEAD_DECISIONS.md`` (which tightens the
freshness rule of ``G2_PLAN.md`` r3 §5.6 to cover entire intervals and removes the proposed
15-second span allowance), plus ``G2_PLAN.md`` r3 §5-§7.

Two boundaries this module exists to hold:

1. **A summary field is never trusted.** ``oraclePx``/``markPx``/``funding``/``coin`` in the
   JSONL are convenience copies. The admitted value is what the raw bytes yield at the
   recorded JSON pointer; every convenience copy is independently re-derived and compared, so
   a manifest can never redirect the tool to a different price or a different asset.
2. **There is no supported bound for the payment-derived comparison.** The exact ``Decimal``
   diagnostic ``D = |usdc| / (|szi| * |fundingRate|)`` is always computed and recorded as
   research evidence, and the instant still stays ``UNRESOLVED:D-4`` under
   ``CORROBORATION_UNAVAILABLE_NO_SUPPORTED_BOUND``. No half-ULP bound is invented, the owner's
   O-2 oracle-agreement tolerance is **not** reused as a payment bound, and no flag, environment
   variable or configuration file can relax any of it. A documented venue rounding rule or an
   explicit owner comparison policy is required before this corroboration can admit anything.

Authority: ``OD-20260919-P012-O1-BUILD-1`` (build), ``OD-20260917-P012-ORACLE-O1-O3-1`` (the
fixed 0.05 % tolerance). This tool produces a candidate locator honestly; it does not move the
``REAL_CAPTURE_READ_ONLY`` production fence, which continues to refuse.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections.abc import Callable
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any

MANIFEST_FILENAME = "ORACLE_READS_MANIFEST.jsonl"
ADMITTED_COIN = "BTC"
ORACLE_KIND = "metaAndAssetCtxs"
STATE_KIND = "clearinghouseState"

#: OD-20260917-P012-ORACLE-O1-O3-1 — the owner's O-2 tolerance, fixed at 0.05 %.
#: There is deliberately no flag, environment variable or configuration behind this name.
O2_RELATIVE_TOLERANCE = Decimal("0.0005")

#: ADMISSION_G2_R3_LEAD_DECISIONS.md: an ENGINEERING cutoff, not a claim about venue cadence
#: or settlement correctness. Each read must lie ENTIRELY inside its side of the hour.
FRESHNESS_WINDOW = timedelta(seconds=5)

#: the shape export_mtc_funding._require_real_oracle_source demands
LOCATOR_PATTERN = re.compile(r"[0-9a-f]{64}#(/[^#]*)+")

HOST_CLOCK_LIMITATION = (
    "These are host wall clock observations (the reader host's Windows clock, not the "
    "venue's) of a public endpoint. They bracket the funding hour; they do NOT identify the "
    "price the venue used at settlement. The official funding page documents the formula but "
    "publishes no per-event settlement-oracle price and no immutable pointer."
)

CORROBORATED = "CORROBORATED"
CORROBORATION_UNAVAILABLE_NO_SUPPORTED_BOUND = (
    "CORROBORATION_UNAVAILABLE_NO_SUPPORTED_BOUND"
)
CORROBORATION_UNAVAILABLE_ZERO_DENOMINATOR = (
    "CORROBORATION_UNAVAILABLE_ZERO_DENOMINATOR"
)
CORROBORATION_UNAVAILABLE_ZERO_PAYMENT = "CORROBORATION_UNAVAILABLE_ZERO_PAYMENT"
CORROBORATION_CONTRADICTION_SIGN = "CORROBORATION_CONTRADICTION_SIGN"
CORROBORATION_CONTRADICTION_MAGNITUDE = "CORROBORATION_CONTRADICTION_MAGNITUDE"

#: export_mtc_funding.APPROVED_PAYER — a LONG position pays when the rate is positive.
APPROVED_PAYER = "LONG"

RESEARCH_ONLY = (
    "RESEARCH_EVIDENCE_ONLY: the payment-derived price is never written into oracle_price "
    "and never becomes a source locator."
)

_HOUR_FILE = re.compile(r"H(\d{8})T(\d{6})Z")
_POINTER_INDEX = re.compile(r"/1/(\d+)/oraclePx")


class OracleRefused(ValueError):
    """A refusal that names its class. Every refusal keeps the instant UNRESOLVED:D-4."""

    def __init__(self, code: str, message: str) -> None:
        super().__init__(f"{code}: {message}")
        self.code = code


def _refuse(code: str, message: str) -> OracleRefused:
    return OracleRefused(code, message)


# --------------------------------------------------------------------------- strict JSON


def _reject_duplicate(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        if key in out:
            raise _refuse("ORACLE_MANIFEST_INVALID", f"duplicate JSON member {key!r}")
        out[key] = value
    return out


def _reject_constant(value: str) -> None:
    raise _refuse("ORACLE_MANIFEST_INVALID", f"non-finite JSON constant {value}")


def _strict_loads(text: str, code: str, label: str) -> Any:
    try:
        return json.loads(
            text, object_pairs_hook=_reject_duplicate, parse_constant=_reject_constant
        )
    except OracleRefused:
        raise
    except (ValueError, UnicodeDecodeError) as exc:
        raise _refuse(code, f"{label}: {exc}") from exc


def _decimal(text: Any, label: str, code: str) -> Decimal:
    if not isinstance(text, str) or not text.strip():
        raise _refuse(code, f"{label} must be a non-empty decimal string, got {text!r}")
    try:
        value = Decimal(text)
    except (InvalidOperation, ValueError) as exc:
        raise _refuse(code, f"{label} is not a decimal: {text!r}") from exc
    if not value.is_finite():
        raise _refuse(code, f"{label} is not finite: {text!r}")
    return value


def _instant(text: Any, label: str) -> datetime:
    """A timestamp is accepted only with an explicit offset, and is compared in UTC."""
    if not isinstance(text, str) or not text:
        raise _refuse("ORACLE_TIMESTAMP_INVALID", f"{label} must be a timestamp string")
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError as exc:
        raise _refuse("ORACLE_TIMESTAMP_INVALID", f"{label}: {text!r} ({exc})") from exc
    if parsed.tzinfo is None or parsed.tzinfo.utcoffset(parsed) is None:
        raise _refuse(
            "ORACLE_TIMESTAMP_INVALID", f"{label} carries no explicit offset: {text!r}"
        )
    return parsed.astimezone(UTC)


def _pointer(document: Any, pointer: str, label: str) -> Any:
    if not isinstance(pointer, str) or not pointer.startswith("/"):
        raise _refuse(
            "ORACLE_POINTER_UNRESOLVED", f"{label}: {pointer!r} is not a JSON pointer"
        )
    node = document
    for token in pointer[1:].split("/"):
        token = token.replace("~1", "/").replace("~0", "~")
        if isinstance(node, list):
            if not token.isdigit() or int(token) >= len(node):
                raise _refuse(
                    "ORACLE_POINTER_UNRESOLVED",
                    f"{label}: {pointer!r} does not resolve",
                )
            node = node[int(token)]
        elif isinstance(node, dict):
            if token not in node:
                raise _refuse(
                    "ORACLE_POINTER_UNRESOLVED",
                    f"{label}: {pointer!r} does not resolve",
                )
            node = node[token]
        else:
            raise _refuse(
                "ORACLE_POINTER_UNRESOLVED", f"{label}: {pointer!r} does not resolve"
            )
    return node


def _hour_of(moment: datetime) -> datetime:
    return moment.astimezone(UTC).replace(minute=0, second=0, microsecond=0)


def _hour_text(moment: datetime) -> str:
    return _hour_of(moment).strftime("%Y-%m-%dT%H:00:00Z")


# ------------------------------------------------------------------------ verified reads


@dataclass(frozen=True)
class VerifiedRead:
    """One manifest row whose every claim has been re-derived from the raw bytes."""

    file: str
    label: str
    kind: str
    role: str
    hour_utc: str
    coin: str
    sha256: str
    byte_length: int
    started: datetime
    ended: datetime
    pointer: str
    oracle_price: Decimal

    @property
    def locator(self) -> str:
        return f"{self.sha256}#{self.pointer}"


@dataclass(frozen=True)
class Resolution:
    """A funding instant with a genuine, fresh, agreeing bracket."""

    hour_utc: str
    event_utc: datetime
    admitted_read: VerifiedRead
    pre: VerifiedRead
    post: VerifiedRead
    relative_agreement: Decimal
    position_witness: dict[str, Any] | None

    @property
    def admitted_price(self) -> Decimal:
        return self.admitted_read.oracle_price

    @property
    def locator(self) -> str:
        return self.admitted_read.locator

    @property
    def tolerance(self) -> Decimal:
        return O2_RELATIVE_TOLERANCE

    def evidence(self) -> dict[str, Any]:
        return {
            "hour_utc": self.hour_utc,
            "event_timestamp": self.event_utc.isoformat(),
            "admitted_price": str(self.admitted_price),
            "admitted_locator": self.locator,
            "admitted_file": self.admitted_read.file,
            "selection_rule": "closest eligible raw observation at or before the event",
            "pre": _interval(self.pre),
            "post": _interval(self.post),
            "relative_agreement": str(self.relative_agreement),
            "o2_tolerance": str(O2_RELATIVE_TOLERANCE),
            "o2_formula": "abs(pre - post) / min(pre, post)",
            "position_witness": self.position_witness,
            "host_clock_limitation": HOST_CLOCK_LIMITATION,
        }


def _interval(read: VerifiedRead) -> dict[str, str]:
    return {
        "file": read.file,
        "started_utc": read.started.isoformat(),
        "ended_utc": read.ended.isoformat(),
        "oracle_price": str(read.oracle_price),
        "sha256": read.sha256,
    }


def _verify_bytes(reads_dir: Path, row: dict[str, Any]) -> bytes:
    name = row.get("file")
    if not isinstance(name, str) or not name or "/" in name or "\\" in name:
        raise _refuse("ORACLE_MANIFEST_INVALID", f"row names no plain file: {name!r}")
    path = reads_dir / name
    if not path.is_file():
        raise _refuse("ORACLE_RAW_MISSING", f"{name}: the raw response file is absent")
    data = path.read_bytes()
    measured = hashlib.sha256(data).hexdigest()
    if measured != row.get("sha256"):
        raise _refuse(
            "ORACLE_RAW_BYTES_MISMATCH",
            f"{name}: measured {measured} but the manifest records {row.get('sha256')!r}",
        )
    sidecar_path = reads_dir / (name + ".sha256")
    if not sidecar_path.is_file():
        raise _refuse(
            "ORACLE_SIDECAR_MISMATCH", f"{name}: the .sha256 sidecar is absent"
        )
    sidecar = sidecar_path.read_text(encoding="ascii").strip().split()[0]
    if sidecar != measured:
        raise _refuse(
            "ORACLE_SIDECAR_MISMATCH",
            f"{name}: the sidecar records {sidecar} but the bytes measure {measured}",
        )
    if row.get("bytes") != len(data):
        raise _refuse(
            "ORACLE_RAW_LENGTH_MISMATCH",
            f"{name}: {len(data)} bytes on disk but the manifest records {row.get('bytes')!r}",
        )
    if row.get("http_status") != 200:
        raise _refuse(
            "ORACLE_HTTP_STATUS_NOT_200",
            f"{name}: http_status {row.get('http_status')!r} is not 200",
        )
    return data


def _hour_from_file(name: str) -> str:
    match = _HOUR_FILE.match(name)
    if match is None:
        raise _refuse(
            "ORACLE_MANIFEST_INVALID", f"{name}: no H<date>T<time>Z hour prefix"
        )
    stamp = datetime.strptime(match.group(1) + match.group(2), "%Y%m%d%H%M%S").replace(
        tzinfo=UTC
    )
    if (stamp.minute, stamp.second) != (0, 0):
        raise _refuse(
            "ORACLE_MANIFEST_INVALID", f"{name}: not filed under a whole hour"
        )
    return _hour_text(stamp)


def _cross_check(name: str, manifest_value: Any, raw_value: Any, field: str) -> None:
    if manifest_value != raw_value:
        raise _refuse(
            "ORACLE_SUMMARY_DISAGREES_WITH_RAW",
            f"{name}: the manifest {field} is {manifest_value!r} but the raw bytes yield "
            f"{raw_value!r}; a summary field is never trusted",
        )


def _verify_oracle_row(reads_dir: Path, row: dict[str, Any]) -> VerifiedRead:
    name = row["file"]
    data = _verify_bytes(reads_dir, row)
    document = _strict_loads(
        data.decode("utf-8", "replace"), "ORACLE_RAW_UNPARSABLE", name
    )

    pointer = row.get("json_pointer_oraclePx")
    raw_price_text = _pointer(document, pointer, name)
    index_match = _POINTER_INDEX.fullmatch(str(pointer))
    if index_match is None:
        raise _refuse(
            "ORACLE_POINTER_UNRESOLVED",
            f"{name}: {pointer!r} is not an asset-context oraclePx pointer",
        )
    asset_index = int(index_match.group(1))
    raw_coin = _pointer(document, f"/0/universe/{asset_index}/name", name)

    _cross_check(name, row.get("coin"), raw_coin, "coin")
    _cross_check(name, row.get("oraclePx"), raw_price_text, "oraclePx")
    context = _pointer(document, f"/1/{asset_index}", name)
    if not isinstance(context, dict):
        raise _refuse(
            "ORACLE_POINTER_UNRESOLVED", f"{name}: asset context is not an object"
        )
    _cross_check(name, row.get("markPx"), context.get("markPx"), "markPx")
    _cross_check(name, row.get("funding"), context.get("funding"), "funding")

    if raw_coin != ADMITTED_COIN:
        raise _refuse(
            "ORACLE_COIN_NOT_ADMITTED",
            f"{name}: the pointer resolves to {raw_coin!r}, not {ADMITTED_COIN}",
        )

    price = _decimal(raw_price_text, f"{name} oraclePx", "ORACLE_VALUE_INVALID")
    if price <= 0:
        raise _refuse(
            "ORACLE_VALUE_INVALID",
            f"{name}: oraclePx {raw_price_text!r} is not positive",
        )

    started = _instant(row.get("started_utc"), f"{name} started_utc")
    ended = _instant(row.get("ended_utc"), f"{name} ended_utc")
    if started > ended:
        raise _refuse(
            "ORACLE_TIMESTAMP_INVALID",
            f"{name}: started_utc {started.isoformat()} is after ended_utc {ended.isoformat()}",
        )

    label = row.get("label")
    if not isinstance(label, str) or not label:
        raise _refuse("ORACLE_MANIFEST_INVALID", f"{name}: no label")
    role = label.rsplit("_", 1)[-1]
    return VerifiedRead(
        file=name,
        label=label,
        kind=ORACLE_KIND,
        role=role,
        hour_utc=_hour_from_file(name),
        coin=raw_coin,
        sha256=row["sha256"],
        byte_length=row["bytes"],
        started=started,
        ended=ended,
        pointer=pointer,
        oracle_price=price,
    )


def _verify_state_row(reads_dir: Path, row: dict[str, Any]) -> dict[str, Any]:
    """The hour's position witness — context only. A position witness is not a funding
    event and never substitutes for a userFunding row."""
    name = row["file"]
    data = _verify_bytes(reads_dir, row)
    document = _strict_loads(
        data.decode("utf-8", "replace"), "ORACLE_RAW_UNPARSABLE", name
    )
    positions = document.get("assetPositions") if isinstance(document, dict) else None
    if not isinstance(positions, list):
        raise _refuse("ORACLE_RAW_UNPARSABLE", f"{name}: no assetPositions array")
    raw_summary = [
        {"coin": item["position"]["coin"], "szi": item["position"]["szi"]}
        for item in positions
        if isinstance(item, dict) and isinstance(item.get("position"), dict)
    ]
    _cross_check(name, row.get("assetPositions"), raw_summary, "assetPositions")
    witness = next(
        (item for item in raw_summary if item["coin"] == ADMITTED_COIN), None
    )
    return {
        "file": name,
        "hour_utc": _hour_from_file(name),
        "sha256": row["sha256"],
        "coin": ADMITTED_COIN,
        "szi": None if witness is None else witness["szi"],
        "note": "position witness, context only; not a funding event",
    }


def select_at_or_before(
    candidates: tuple[VerifiedRead, ...] | list[VerifiedRead],
    event: datetime,
    hour_utc: str = "",
) -> VerifiedRead:
    """§5.7 selection: the **closest eligible raw observation at or before E**.

    Never an average of the bracket and never a payment-derived value. With a bracket that
    passed the freshness rule exactly one observation qualifies — the ``pre`` read, because
    ``post.started`` must be after ``E`` — but the rule is written and tested over a wider
    candidate set so a future caller cannot silently pick the wrong one.
    """
    eligible = [r for r in candidates if r.ended <= event]
    if not eligible:
        raise _refuse(
            "ORACLE_BRACKET_DOES_NOT_STRADDLE_EVENT",
            f"{hour_utc}: no observation ended at or before the event",
        )
    return max(eligible, key=lambda r: r.ended)


class OracleReads:
    """Every row of one reader directory, each verified against its own raw bytes."""

    def __init__(
        self,
        reads_dir: Path,
        reads: list[VerifiedRead],
        witnesses: dict[str, dict[str, Any]],
    ) -> None:
        self.reads_dir = reads_dir
        self.reads = tuple(reads)
        self.witnesses = dict(witnesses)

    def _one(self, hour_utc: str, role: str) -> VerifiedRead:
        found = [r for r in self.reads if r.hour_utc == hour_utc and r.role == role]
        if len(found) != 1:
            raise _refuse(
                "ORACLE_PAIR_AMBIGUOUS",
                f"{hour_utc}: expected exactly one {role!r} read, found {len(found)}",
            )
        return found[0]

    def resolve(self, hour_utc: str, event_utc: datetime) -> Resolution:
        """The §5/§6 gate. Any failure refuses; a refused instant stays UNRESOLVED:D-4."""
        if not isinstance(event_utc, datetime) or event_utc.tzinfo is None:
            raise _refuse(
                "ORACLE_TIMESTAMP_INVALID",
                "the validated funding-event timestamp must be timezone-aware",
            )
        event = event_utc.astimezone(UTC)
        hour = _instant(hour_utc.replace("Z", "+00:00"), "hour")
        if _hour_text(event) != _hour_text(hour) or _hour_text(hour) != hour_utc:
            raise _refuse(
                "ORACLE_HOUR_IDENTITY_MISMATCH",
                f"the event {event.isoformat()} does not belong to hour {hour_utc}",
            )

        pre, post = self._one(hour_utc, "pre"), self._one(hour_utc, "post")
        if pre.coin != post.coin:
            raise _refuse(
                "ORACLE_PAIR_AMBIGUOUS", f"{hour_utc}: the bracket mixes assets"
            )

        # ADMISSION_G2_R3_LEAD_DECISIONS.md — ENTIRE intervals, not just their edges.
        if not (hour - FRESHNESS_WINDOW <= pre.started and pre.ended <= hour):
            raise _refuse(
                "ORACLE_BRACKET_STALE",
                f"{hour_utc}: the pre read {pre.started.isoformat()}..{pre.ended.isoformat()} "
                f"is not entirely inside [H-{FRESHNESS_WINDOW.seconds}s, H]",
            )
        if not (hour < post.started and post.ended <= hour + FRESHNESS_WINDOW):
            raise _refuse(
                "ORACLE_BRACKET_STALE",
                f"{hour_utc}: the post read {post.started.isoformat()}..{post.ended.isoformat()} "
                f"is not entirely inside (H, H+{FRESHNESS_WINDOW.seconds}s]",
            )
        # the reads must straddle the EVENT, not merely the hour
        if not (pre.ended <= event <= post.started):
            raise _refuse(
                "ORACLE_BRACKET_DOES_NOT_STRADDLE_EVENT",
                f"{hour_utc}: pre.ended {pre.ended.isoformat()} <= E {event.isoformat()} "
                f"<= post.started {post.started.isoformat()} does not hold",
            )

        agreement = abs(pre.oracle_price - post.oracle_price) / min(
            pre.oracle_price, post.oracle_price
        )
        if agreement > O2_RELATIVE_TOLERANCE:
            raise _refuse(
                "ORACLE_TOLERANCE_EXCEEDED",
                f"{hour_utc}: the two reads disagree by {agreement} > {O2_RELATIVE_TOLERANCE} "
                f"(OD-20260917-P012-ORACLE-O1-O3-1)",
            )

        admitted = select_at_or_before((pre, post), event, hour_utc)
        return Resolution(
            hour_utc=hour_utc,
            event_utc=event,
            admitted_read=admitted,
            pre=pre,
            post=post,
            relative_agreement=agreement,
            position_witness=self.witnesses.get(hour_utc),
        )


def load_reads(reads_dir: Path | str) -> OracleReads:
    """Verify every row of a reader directory. Read-only: nothing here writes."""
    reads_dir = Path(reads_dir)
    manifest_path = reads_dir / MANIFEST_FILENAME
    if not manifest_path.is_file():
        raise _refuse("ORACLE_MANIFEST_INVALID", f"{manifest_path} is absent")
    reads: list[VerifiedRead] = []
    witnesses: dict[str, dict[str, Any]] = {}
    for number, line in enumerate(
        manifest_path.read_text(encoding="utf-8").splitlines(), start=1
    ):
        if not line.strip():
            continue
        row = _strict_loads(
            line, "ORACLE_MANIFEST_INVALID", f"{MANIFEST_FILENAME}:{number}"
        )
        if not isinstance(row, dict):
            raise _refuse(
                "ORACLE_MANIFEST_INVALID",
                f"{MANIFEST_FILENAME}:{number} is not an object",
            )
        kind = row.get("kind")
        if kind == ORACLE_KIND:
            reads.append(_verify_oracle_row(reads_dir, row))
        elif kind == STATE_KIND:
            witness = _verify_state_row(reads_dir, row)
            witnesses[witness["hour_utc"]] = witness
        else:
            raise _refuse(
                "ORACLE_MANIFEST_INVALID",
                f"{MANIFEST_FILENAME}:{number}: unknown kind {kind!r}",
            )
    return OracleReads(reads_dir, reads, witnesses)


# ------------------------------------------------------- payment-derived corroboration


def corroborate(
    admitted_price: Decimal,
    usdc: str,
    szi: str,
    funding_rate: str,
    *,
    corroboration_bound: Decimal | None = None,
) -> dict[str, Any]:
    """Exact ``Decimal`` diagnostics for ``D = |usdc| / (|szi| * |fundingRate|)``.

    ``corroboration_bound`` has **no CLI flag, no environment variable and no configuration
    file behind it**. Production leaves it ``None``, which is
    ``CORROBORATION_UNAVAILABLE_NO_SUPPORTED_BOUND`` — no examined venue page states a rounding
    mode or a hidden precision for ``szi``/``fundingRate``, so the comparison cannot be
    adjudicated and the instant fails closed. It exists so a test can exercise the adjudicated
    branches explicitly, and so a future owner-defined guard or documented venue bytes have one
    obvious place to arrive. The O-2 oracle-agreement tolerance is a different question and is
    never substituted here.

    The returned ``derived_price`` is research evidence. It is never an oracle price and never
    a source locator.
    """
    payment = _decimal(usdc, "usdc", "ORACLE_PAYMENT_INPUT_INVALID")
    size = _decimal(szi, "szi", "ORACLE_PAYMENT_INPUT_INVALID")
    rate = _decimal(funding_rate, "fundingRate", "ORACLE_PAYMENT_INPUT_INVALID")

    result: dict[str, Any] = {
        "formula": "D = |usdc| / (|szi| * |fundingRate|)",
        "usdc": str(payment),
        "szi": str(size),
        "funding_rate": str(rate),
        "admitted_price": str(admitted_price),
        "payer_convention": APPROVED_PAYER,
        "derived_price": None,
        "absolute_difference": None,
        "relative_difference": None,
        "bound": None if corroboration_bound is None else str(corroboration_bound),
        "statement": RESEARCH_ONLY,
    }

    # the sign check is separate and is NOT skipped when the magnitude test is unavailable
    sign_consistent = True
    if payment and size and rate:
        expected = -1 if (size > 0) == (rate > 0) else 1
        sign_consistent = (1 if payment > 0 else -1) == expected
    result["sign_consistent"] = sign_consistent
    if not sign_consistent:
        result["status"] = CORROBORATION_CONTRADICTION_SIGN
        result["corroborated"] = False
        return result

    if size == 0 or rate == 0:
        result["status"] = CORROBORATION_UNAVAILABLE_ZERO_DENOMINATOR
        result["corroborated"] = False
        return result

    derived = abs(payment) / (abs(size) * abs(rate))
    result["derived_price"] = str(derived)
    result["absolute_difference"] = str(abs(derived - admitted_price))
    result["relative_difference"] = str(abs(derived - admitted_price) / admitted_price)

    if payment == 0:
        # quantization of a small position or rate can produce this; it is unavailable
        # evidence, never a proved contradiction
        result["status"] = CORROBORATION_UNAVAILABLE_ZERO_PAYMENT
        result["corroborated"] = False
        return result

    if corroboration_bound is None:
        result["status"] = CORROBORATION_UNAVAILABLE_NO_SUPPORTED_BOUND
        result["corroborated"] = False
        return result

    inside = abs(derived - admitted_price) / admitted_price <= corroboration_bound
    result["status"] = CORROBORATED if inside else CORROBORATION_CONTRADICTION_MAGNITUDE
    result["corroborated"] = inside
    return result


# ------------------------------------------------------------- the scheduled collector


def plan_bracket(hour: datetime) -> list[dict[str, Any]]:
    """The design note's schedule (H-2 s / H+2 s, then the position witness). Pure
    arithmetic — planning a read is not taking one."""
    hour = hour.astimezone(UTC)
    return [
        {
            "label": "pre",
            "at": hour - timedelta(seconds=2),
            "request": {"type": ORACLE_KIND},
        },
        {
            "label": "post",
            "at": hour + timedelta(seconds=2),
            "request": {"type": ORACLE_KIND},
        },
        {
            "label": "state",
            "at": hour + timedelta(seconds=3),
            "request": {"type": STATE_KIND},
        },
    ]


Transport = Callable[[str, dict[str, Any]], tuple[int, bytes, str, str]]


def collect_bracket(
    hour: datetime,
    *,
    out_dir: Path | str,
    transport: Transport,
    address: str | None = None,
) -> Path:
    """Write one bracket in the reader's exact on-disk shape.

    ``transport`` is required and has no default: this module ships no way to reach a venue,
    so there is no code path here that can perform a live read. Supplying a live transport is
    separately authorized work, and it must never run while the Lead's own reader is running.
    """
    out = Path(out_dir)
    if out.exists():
        raise _refuse("ORACLE_OUTPUT_EXISTS", f"output directory already exists: {out}")
    hour = hour.astimezone(UTC)
    stamp = hour.strftime("H%Y%m%dT%H%M%SZ")
    out.mkdir(parents=True)
    rows: list[dict[str, Any]] = []
    for step in plan_bracket(hour):
        label = step["label"]
        request = dict(step["request"])
        if request["type"] == STATE_KIND and address:
            request["user"] = address
        status, body, started, ended = transport(label, request)
        suffix = ORACLE_KIND if label != "state" else STATE_KIND
        name = f"{stamp}_{label}_{suffix}.json"
        (out / name).write_bytes(body)
        digest = hashlib.sha256(body).hexdigest()
        (out / (name + ".sha256")).write_text(digest + "\n", encoding="ascii")
        row: dict[str, Any] = {
            "bytes": len(body),
            "clock": "host wall clock (Windows), not the venue's",
            "ended_utc": ended,
            "file": name,
            "http_status": status,
            "kind": suffix,
            "label": f"{stamp}_{label}",
            "request": request,
            "sha256": digest,
            "started_utc": started,
            "tolerance_owner_O2": "0.05%",
        }
        document = _strict_loads(
            body.decode("utf-8", "replace"), "ORACLE_RAW_UNPARSABLE", name
        )
        if suffix == ORACLE_KIND:
            index = next(
                i
                for i, asset in enumerate(document[0]["universe"])
                if asset["name"] == ADMITTED_COIN
            )
            context = document[1][index]
            row.update(
                coin=ADMITTED_COIN,
                funding=context["funding"],
                json_pointer_oraclePx=f"/1/{index}/oraclePx",
                markPx=context["markPx"],
                oraclePx=context["oraclePx"],
            )
        else:
            row.update(
                assetPositions=[
                    {"coin": item["position"]["coin"], "szi": item["position"]["szi"]}
                    for item in document["assetPositions"]
                ],
                venue_time_ms=document.get("time"),
            )
        rows.append(row)
    (out / MANIFEST_FILENAME).write_text(
        "".join(
            json.dumps(row, sort_keys=True, ensure_ascii=False, allow_nan=False) + "\n"
            for row in rows
        ),
        encoding="utf-8",
    )
    return out


# --------------------------------------------------------------------------------- CLI


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Verify oracle reads around a funding instant. Read-only: the reads directory is "
            "never written. The O-2 tolerance and the freshness cutoffs are fixed constants "
            "with no command-line knob, and no option can admit evidence."
        )
    )
    parser.add_argument(
        "--verify-existing",
        required=True,
        help="an oracle reader directory (read-only)",
    )
    parser.add_argument(
        "--hour", required=True, help="funding hour, e.g. 2026-09-19T15:00:00Z"
    )
    parser.add_argument(
        "--event-timestamp",
        required=True,
        help="the validated funding-event timestamp, with an explicit UTC offset",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        reads = load_reads(Path(args.verify_existing))
        resolution = reads.resolve(
            args.hour, _instant(args.event_timestamp, "--event-timestamp")
        )
    except OracleRefused as exc:
        print(f"ORACLE_REFUSED {exc.code}: {exc}", file=sys.stderr)
        return 3
    print(
        json.dumps(resolution.evidence(), ensure_ascii=False, sort_keys=True, indent=2)
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
