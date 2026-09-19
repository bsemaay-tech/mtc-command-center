"""WP-P0-12 funding intake adapter — the NON-ACCEPTING half of the production intake (2026-09-15).

Reads one Path-1 read-only capture run (``CAPTURE_MANIFEST.json`` + ``DERIVED_EXTRACTION.json`` written by
``capture_own_account_evidence.py``) and emits, deterministically and offline:

* ``binding_packet_draft.json`` — the shape ``export_mtc_funding.py`` consumes, with every field the captured
  bytes can supply filled, and every field they cannot supply set to the literal ``UNRESOLVED:D-n``
  (the decision that would resolve it). Nothing is guessed: no oracle price, no digest domain, no
  admitted evidence kind. The export tool refuses this packet today by design; the actual refusal
  code is computed by calling the tool (``gap_report.export_tool_outcome_today``), never declared,
  so the two tools cannot silently disagree.
* ``retained_rows_expected.json`` — what a schema-v10 Bridge store would have to retain per event.
* ``intake_gap_report.json`` — the open decisions D-1..D-6, counts, the completeness-rule result and
  the refusal the export tool raises for this packet.

Every draft artifact carries the label ``NONACCEPTING_INTAKE_DRAFT``. No network, no credential, no
write into the capture directory (the output directory is write-once). Authority:
``OD-20260915-BUILD-ABC-1`` item (b); design note ``P012_FUNDING_INTAKE_DESIGN_20260915.md``.

Slice 4 (2026-09-16, ``OD-20260916-P012-INTAKE-D1-D6-R-1``): when the run directory also carries the
raw response files named by the manifest (bytes re-hashed against ``response_sha256``), a fourth
output ``binding_packet_real_capture.json`` is written in the shape ``export_mtc_funding.py`` reads
under ``--evidence-kind REAL_CAPTURE_READ_ONLY``: D-1 digests over the exact captured row bytes,
D-2 identities, D-3 verbatim stamps plus ``interval_hour_utc``, D-5 witness identity naming the
manifest and its ownership record, D-6 witness material (both funding passes, the fills pass).
The oracle fields stay ``UNRESOLVED:D-4`` until an oracle capture at the funding instants exists,
so the export tool refuses this packet with ``CANDIDATE_ORACLE_EVIDENCE_UNAVAILABLE`` — the honest
outcome for a run that captured no oracle read. Nothing here admits production.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools import capture_oracle_at_funding as oracle_tool
from tools import export_mtc_funding as exporter

ADAPTER_VERSION = "p012-funding-intake/v1"
DRAFT_LABEL = "NONACCEPTING_INTAKE_DRAFT"
PACKET_VERSION_TARGET = "SYNTHETIC_FUNDING_BINDING_PACKET_V1"
PROPOSED_EVIDENCE_KIND = "REAL_CAPTURE_READ_ONLY"
APPROVED_PAYER = (
    "LONG"  # export_mtc_funding.APPROVED_PAYER — the tool's own rule, not a guess
)
PAYLOAD_RETAINED = "FUNDING_PAYLOAD_RETAINED"
HOUR_MS = 3_600_000
# slice 4 — the accepting shape (values ruled by OD-20260916-P012-INTAKE-D1-D6-R-1)
RULING = "OD-20260916-P012-INTAKE-D1-D6-R-1"
REAL_PACKET_FILENAME = "binding_packet_real_capture.json"
REAL_PACKET_VERSION = "REAL_CAPTURE_FUNDING_BINDING_PACKET_V1"
REAL_DIGEST_DOMAIN = "HL_USERFUNDING_ROW_V1"
REAL_EVENT_ID_PREFIX = "hl-funding"
EXPECTED_REAL_TOOL_REFUSAL = "CANDIDATE_ORACLE_EVIDENCE_UNAVAILABLE"
BRIDGE_DIGEST_UNAVAILABLE = "UNAVAILABLE:BRIDGE_OBSERVATION_REQUIRED"
DECISIONS = {
    "D-1": "production source_event_digest byte domain",
    "D-2": "funding_event_id rule for venue funding rows (the venue hash is the zero hash)",
    "D-3": "event timestamp: venue stamp verbatim vs hour boundary",
    "D-4": "oracle price and its source for a funding instant (not in the funding row)",
    "D-5": "admitting a real read-only capture evidence kind beside SYNTHETIC_FIXTURE",
    "D-6": "whole-interval completion witness for read-only captures",
}
# D-5 is RESOLVED (OD-20260916-P012-INTAKE-D1-D6-R-1): export_mtc_funding.py admits
# REAL_CAPTURE_READ_ONLY under its own evidence profile. The draft packet built by
# build_intake() below still labels itself SYNTHETIC_FUNDING_BINDING_PACKET_V1 and is
# never the accepting shape (see build_real_packet()), so its own evidence_kind_status
# names the resolution and points at the accepting shape rather than claiming D-5 is
# still open.
D5_RESOLVED_NOTE = "RESOLVED:D-5 (see binding_packet_real_capture.json for the accepting shape)"


def unresolved(decision: str) -> str:
    assert decision in DECISIONS
    return f"UNRESOLVED:{decision}"


class IntakeRefused(ValueError):
    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code


def _reject_duplicate(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        if key in out:
            raise IntakeRefused(
                "INTAKE_INPUT_INVALID", f"duplicate JSON member {key!r}"
            )
        out[key] = value
    return out


def _reject_constant(value: str) -> None:
    raise IntakeRefused("INTAKE_INPUT_INVALID", f"non-finite JSON constant {value}")


def strict_load(path: Path) -> Any:
    try:
        return json.loads(
            path.read_bytes().decode("utf-8"),
            object_pairs_hook=_reject_duplicate,
            parse_constant=_reject_constant,
        )
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise IntakeRefused("INTAKE_INPUT_INVALID", f"{path.name}: {exc}") from exc


def short_address(address: str) -> str:
    if (
        not isinstance(address, str)
        or not address.startswith("0x")
        or len(address) != 42
    ):
        raise IntakeRefused(
            "INTAKE_INPUT_INVALID", "manifest address is not a 20-byte 0x address"
        )
    return address[:6] + "…" + address[-4:]


def utc_z(ms: int) -> str:
    return (
        datetime.fromtimestamp(ms / 1000, tz=UTC).strftime("%Y-%m-%dT%H:%M:%S.")
        + f"{ms % 1000:03d}Z"
    )


def _text(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise IntakeRefused(
            "INTAKE_INPUT_INVALID", f"{label} must be a non-empty string"
        )
    return value


def _int(value: Any, label: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise IntakeRefused("INTAKE_INPUT_INVALID", f"{label} must be an integer")
    return value


def hour_z(ms: int) -> str:
    return datetime.fromtimestamp(ms // HOUR_MS * HOUR_MS / 1000, tz=UTC).strftime(
        "%Y-%m-%dT%H:00:00Z"
    )


def load_raw_responses(run_dir: Path, manifest: dict[str, Any]) -> dict[str, bytes]:
    """The raw response files the manifest names, when present in the run directory,
    each re-hashed against the manifest's ``response_sha256`` (a mismatch refuses).
    Absent files mean no real-capture packet, never a guessed one."""
    raw: dict[str, bytes] = {}
    for response in manifest.get("responses") or []:
        name = response.get("file")
        if not isinstance(name, str) or not name or "/" in name or "\\" in name:
            continue
        path = run_dir / name
        if not path.is_file():
            continue
        data = path.read_bytes()
        if hashlib.sha256(data).hexdigest() != response.get("response_sha256"):
            raise IntakeRefused(
                "INTAKE_INPUT_INVALID",
                f"{name}: bytes do not reproduce the manifest response_sha256",
            )
        raw[name] = data

    return raw


def array_spans(payload: bytes, label: str) -> list[tuple[bytes, Any]]:
    """Every element of a captured JSON array as (exact bytes, decoded value)."""
    decoder = json.JSONDecoder(
        object_pairs_hook=_reject_duplicate, parse_constant=_reject_constant
    )
    try:
        text = payload.decode("utf-8")
        index = 0
        while text[index] in " \t\r\n":
            index += 1
        if text[index] != "[":
            raise IntakeRefused("INTAKE_INPUT_INVALID", f"{label} is not a JSON array")
        index += 1
        spans: list[tuple[bytes, Any]] = []
        while True:
            while text[index] in " \t\r\n":
                index += 1
            if text[index] == "]":
                break
            if spans:
                if text[index] != ",":
                    raise IntakeRefused(
                        "INTAKE_INPUT_INVALID", f"{label} is not a JSON array"
                    )
                index += 1
                while text[index] in " \t\r\n":
                    index += 1
            value, end = decoder.raw_decode(text, index)
            spans.append((text[index:end].encode("utf-8"), value))
            index = end
    except (UnicodeDecodeError, IndexError, ValueError) as exc:
        raise IntakeRefused("INTAKE_INPUT_INVALID", f"{label}: {exc}") from exc
    return spans


def load_capture(
    run_dir: Path,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, bytes], str]:
    manifest_bytes = (run_dir / "CAPTURE_MANIFEST.json").read_bytes()
    manifest = strict_load(run_dir / "CAPTURE_MANIFEST.json")
    derived = strict_load(run_dir / "DERIVED_EXTRACTION.json")
    if (
        not isinstance(manifest, dict)
        or manifest.get("kind") != "P012_PATH1_OWN_ACCOUNT_CAPTURE_MANIFEST_V1"
    ):
        raise IntakeRefused(
            "INTAKE_INPUT_INVALID", "manifest kind is not the Path-1 capture manifest"
        )
    if (
        not isinstance(derived, dict)
        or derived.get("label") != "DERIVED_VIEW_NOT_ORIGINAL_BYTES"
    ):
        raise IntakeRefused("INTAKE_INPUT_INVALID", "derived extraction label missing")
    if not isinstance(derived.get("funding"), list) or not isinstance(
        derived.get("fills"), list
    ):
        raise IntakeRefused(
            "INTAKE_INPUT_INVALID",
            "derived extraction must carry funding and fills lists",
        )
    raw = load_raw_responses(run_dir, manifest)
    return manifest, derived, raw, hashlib.sha256(manifest_bytes).hexdigest()


def resolve_oracle_binding(
    oracle: oracle_tool.OracleReads,
    event_id: str,
    time_ms: int,
    delta: dict[str, Any],
    corroboration_bound: Any | None = None,
) -> dict[str, Any]:
    """D-4 for one inventoried funding event, fail-closed at every step.

    The oracle bracket is verified against the reader's raw bytes (§5) and then the
    payment-derived corroboration is adjudicated (§7). ``oracle_price`` is filled **only** when
    both succeed. With no supported comparison bound — the state of the evidence today — §7 is
    ``CORROBORATION_UNAVAILABLE_NO_SUPPORTED_BOUND`` and the instant stays ``UNRESOLVED:D-4``
    however well the bracket verified. The payment-derived price is recorded as research
    evidence and is never written into the packet.
    """
    record: dict[str, Any] = {
        "funding_event_id": event_id,
        "hour_utc": hour_z(time_ms),
        "event_timestamp": utc_z(time_ms),
        "admitted": False,
        "unresolved": unresolved("D-4"),
        "candidate_price": None,
        "candidate_locator": None,
        "corroboration": None,
        "host_clock_limitation": oracle_tool.HOST_CLOCK_LIMITATION,
    }
    try:
        resolution = oracle.resolve(
            hour_z(time_ms), datetime.fromtimestamp(time_ms / 1000, tz=UTC)
        )
    except oracle_tool.OracleRefused as exc:
        record["oracle_verification"] = exc.code
        record["oracle_refusal"] = str(exc)
        return record

    record["oracle_verification"] = "VERIFIED"
    record["candidate_price"] = str(resolution.admitted_price)
    record["candidate_locator"] = resolution.locator
    record["bracket"] = resolution.evidence()
    try:
        corroboration = oracle_tool.corroborate(
            resolution.admitted_price,
            _text(delta.get("usdc"), "delta.usdc"),
            _text(delta.get("szi"), "delta.szi"),
            _text(delta.get("fundingRate"), "delta.fundingRate"),
            corroboration_bound=corroboration_bound,
        )
    except oracle_tool.OracleRefused as exc:
        record["corroboration"] = {"status": exc.code, "corroborated": False}
        return record

    record["corroboration"] = corroboration
    if corroboration["corroborated"]:
        record["admitted"] = True
        record["unresolved"] = None
    return record


def build_real_packet(
    manifest: dict[str, Any],
    derived: dict[str, Any],
    raw: dict[str, bytes],
    manifest_sha256: str,
    oracle: oracle_tool.OracleReads | None = None,
    corroboration_bound: Any | None = None,
) -> tuple[dict[str, Any] | None, str, dict[str, Any] | None]:
    """The accepting shape under D-1..D-6, built from the exact captured bytes, or
    ``(None, reason, None)`` when the run directory does not carry them.

    With ``oracle`` absent the packet is byte-identical to the one built before O-1 existed."""
    address = short_address(manifest.get("address"))
    run_id = _text(manifest.get("run_id"), "manifest.run_id")
    coin = _text(manifest.get("coin"), "manifest.coin")
    responses = manifest.get("responses") or []
    tool_sha = _text(
        (responses or [{}])[0].get("tool_sha256", ""), "responses[0].tool_sha256"
    )
    funding_files = [
        r.get("file")
        for r in responses
        if str(r.get("file", "")).startswith("funding_pass")
    ]
    fills_files = [
        r.get("file")
        for r in responses
        if str(r.get("file", "")).startswith("fills_pass")
    ]
    if len(funding_files) < 2 or not fills_files:
        return (
            None,
            "the manifest names fewer than two funding passes or no fills pass",
            None,
        )
    missing = [name for name in funding_files + fills_files[:1] if name not in raw]
    if missing:
        return (
            None,
            f"raw response bytes absent from the run directory: {missing}",
            None,
        )
    if not isinstance(manifest.get("window"), dict):
        return None, "the manifest carries no window", None
    window = manifest["window"]
    pass_bytes = raw[funding_files[0]]
    spans = array_spans(pass_bytes, funding_files[0])
    derived_keys = {
        (row.get("time"), row.get("coin"))
        for row in derived["funding"]
        if isinstance(row, dict)
    }
    bindings: list[dict[str, Any]] = []
    witnesses: dict[str, str] = {}
    oracle_events: list[dict[str, Any]] = []
    for index, (raw_row, value) in enumerate(spans):
        if not isinstance(value, dict) or not isinstance(value.get("delta"), dict):
            raise IntakeRefused(
                "INTAKE_INPUT_INVALID",
                f"{funding_files[0]}#/{index} is not a funding row",
            )
        delta = value["delta"]
        time_ms = _int(value.get("time"), f"{funding_files[0]}#/{index}.time")
        row_coin = _text(delta.get("coin"), f"{funding_files[0]}#/{index}.delta.coin")
        if row_coin != coin:
            raise IntakeRefused(
                "INTAKE_INPUT_INVALID",
                f"{funding_files[0]}#/{index} coin {row_coin!r} is not the run coin {coin!r}",
            )
        if (time_ms, row_coin) not in derived_keys:
            raise IntakeRefused(
                "INTAKE_INPUT_INVALID",
                f"{funding_files[0]}#/{index} is not listed by the derived view",
            )
        event_id = f"{REAL_EVENT_ID_PREFIX}:{address}:{row_coin}:{time_ms}"
        witnesses[event_id] = raw_row.hex()
        oracle_price = oracle_source = unresolved("D-4")
        if oracle is not None:
            event = resolve_oracle_binding(
                oracle, event_id, time_ms, delta, corroboration_bound
            )
            oracle_events.append(event)
            if event["admitted"]:
                oracle_price = event["candidate_price"]
                oracle_source = event["candidate_locator"]
        bindings.append(
            {
                "event_timestamp": utc_z(time_ms),
                "funding_event_id": event_id,
                "interval_hour_utc": hour_z(time_ms),
                "oracle_price": oracle_price,
                "oracle_price_source": oracle_source,
                "positive_rate_payer": APPROVED_PAYER,
                "provenance": {
                    "evidence_kind": PROPOSED_EVIDENCE_KIND,
                    "extraction_method": (
                        f"capture_own_account_evidence.py tool_sha256={tool_sha[:16]} "
                        "user_funding_history"
                    ),
                    "source_locator": f"{funding_files[0]}#/{index}",
                    "source_sha256": hashlib.sha256(pass_bytes).hexdigest(),
                    "source_title": f"Hyperliquid userFunding {address} run {run_id}",
                },
                "raw_rate": _text(
                    delta.get("fundingRate"),
                    f"{funding_files[0]}#/{index}.delta.fundingRate",
                ),
                "source_event_digest": (
                    f"{REAL_DIGEST_DOMAIN}:{hashlib.sha256(raw_row).hexdigest()}"
                ),
            }
        )
    if len(bindings) != len(derived["funding"]):
        raise IntakeRefused(
            "INTAKE_INPUT_INVALID",
            "the derived view and the captured funding pass disagree on the row count",
        )
    oracle_report = (
        None
        if oracle is None
        else {
            "mode": "VERIFY_EXISTING",
            "reads_dir": str(oracle.reads_dir),
            "events": oracle_events,
            "o2_tolerance": str(oracle_tool.O2_RELATIVE_TOLERANCE),
            "freshness_seconds": int(oracle_tool.FRESHNESS_WINDOW.total_seconds()),
            "statement": (
                "Oracle brackets verified against the reader's raw bytes. An instant is filled "
                "only when §5 verification AND the §7 payment corroboration both succeed; with "
                "no supported comparison bound the corroboration is unavailable and the instant "
                "stays UNRESOLVED:D-4. The payment-derived price is research evidence and is "
                "never an oracle price. Nothing here admits production evidence."
            ),
        }
    )
    ownership = manifest.get("ownership_evidence") or {}
    witness = completeness(manifest)
    packet = {
        "packet_version": REAL_PACKET_VERSION,
        "bindings": bindings,
        "coverage": {
            "account_scope": address,
            "complete": witness["complete"],
            "evidence_kind": PROPOSED_EVIDENCE_KIND,
            "expected_event_ids": [b["funding_event_id"] for b in bindings],
            "fills_witness": raw[fills_files[0]].hex(),
            "funding_witness_passes": [raw[name].hex() for name in funding_files],
            "interval_end_exclusive": _text(window.get("end"), "window.end"),
            "interval_start_inclusive": _text(window.get("start"), "window.start"),
            "symbol": coin,
            "source_witnesses": witnesses,
            "unattributed_event_ids": [],
            "witness_identity": (
                f"capture_own_account_evidence.py tool_sha256={tool_sha[:16]} run {run_id}; "
                f"manifest_sha256={manifest_sha256}; "
                f"ownership {ownership.get('status')} "
                f"{short_address(ownership.get('recovered_address', manifest.get('address')))}"
            ),
        },
    }
    return packet, "built from the captured bytes", oracle_report


def completeness(manifest: dict[str, Any]) -> dict[str, Any]:
    """The D-6 rule as the adapter applies it: hour-aligned window AND both funding passes byte-identical."""
    window = manifest.get("window") or {}
    start_ms = _int(window.get("start_ms"), "window.start_ms")
    end_ms = _int(window.get("end_ms"), "window.end_ms")
    reasons: list[str] = []
    if start_ms % HOUR_MS or end_ms % HOUR_MS:
        reasons.append("window is not aligned to venue funding hours")
    if end_ms <= start_ms:
        reasons.append("window is empty or reversed")
    passes = {}
    for response in manifest.get("responses") or []:
        name = response.get("file", "")
        if name.startswith("funding_pass"):
            passes[name] = response.get("response_sha256")
    if len(passes) < 2:
        reasons.append("fewer than two funding passes captured")
    elif len(set(passes.values())) != 1:
        reasons.append("funding passes are not byte-identical")
    return {
        "rule": "hour-aligned window AND two byte-identical funding passes (proposed D-6)",
        "complete": not reasons,
        "reasons": reasons,
        "window_start_utc": window.get("start"),
        "window_end_utc": window.get("end"),
        "funding_passes": passes,
    }


def _export_tool_outcome_today(packet: dict[str, Any]) -> dict[str, str]:
    """What export_mtc_funding.py actually does with this draft packet today,
    computed by calling it directly instead of declaring a guessed code: the
    two producers (this adapter and the export tool) must never be allowed to
    silently disagree (lane-8 exact-Opus review of a871e429, NIT-A)."""
    coverage = packet["coverage"]
    probe = exporter.build_funding_candidate(
        [],
        [],
        coverage,
        "P012_INTAKE_ADAPTER_PROBE",
        coverage["interval_start_inclusive"],
        coverage["interval_end_exclusive"],
    )
    assert not probe.accepted, "the non-accepting draft packet must never be admitted"
    return {"refusal_code": probe.reason_code, "reason": probe.report["reason_detail"]}


def build_intake(
    manifest: dict[str, Any],
    derived: dict[str, Any],
    raw: dict[str, bytes] | None = None,
    manifest_sha256: str | None = None,
    oracle: oracle_tool.OracleReads | None = None,
    corroboration_bound: Any | None = None,
) -> dict[str, Any]:
    address = short_address(manifest.get("address"))
    run_id = _text(manifest.get("run_id"), "manifest.run_id")
    coin = _text(manifest.get("coin"), "manifest.coin")
    tool_sha = _text(
        (manifest.get("responses") or [{}])[0].get("tool_sha256", ""),
        "responses[0].tool_sha256",
    )
    file_by_sha: dict[str, str] = {}
    for response in manifest.get("responses") or []:
        # the derived view is built from pass 1; pass 2 carries the same bytes (same sha) — keep the first
        file_by_sha.setdefault(response.get("response_sha256"), response.get("file"))
    witness = completeness(manifest)

    bindings: list[dict[str, Any]] = []
    retained: list[dict[str, Any]] = []
    for index, row in enumerate(derived["funding"]):
        if not isinstance(row, dict) or row.get("kind") != "DERIVED_FUNDING":
            raise IntakeRefused(
                "INTAKE_INPUT_INVALID", f"funding[{index}] is not a DERIVED_FUNDING row"
            )
        time_ms = _int(row.get("time"), f"funding[{index}].time")
        row_coin = _text(row.get("coin"), f"funding[{index}].coin")
        rate = _text(row.get("fundingRate"), f"funding[{index}].fundingRate")
        usdc = _text(row.get("usdc"), f"funding[{index}].usdc")
        szi = _text(row.get("szi"), f"funding[{index}].szi")
        source_sha = _text(
            row.get("capture_sha256"), f"funding[{index}].capture_sha256"
        )
        pointer = _text(row.get("json_pointer"), f"funding[{index}].json_pointer")
        if row_coin != coin:
            raise IntakeRefused(
                "INTAKE_INPUT_INVALID",
                f"funding[{index}] coin {row_coin!r} is not the run coin {coin!r}",
            )
        event_id = f"hl-funding:{address}:{row_coin}:{time_ms}"  # proposed D-2 rule, labelled below
        source_file = file_by_sha.get(source_sha, "UNKNOWN_CAPTURE_FILE")
        bindings.append(
            {
                "event_timestamp": utc_z(time_ms),
                "funding_event_id": event_id,
                "funding_event_id_rule": "PROPOSED:D-2 hl-funding:<account-short>:<coin>:<time_ms>",
                "oracle_price": unresolved("D-4"),
                "oracle_price_source": unresolved("D-4"),
                "positive_rate_payer": APPROVED_PAYER,
                "positive_rate_payer_basis": "export_mtc_funding.APPROVED_PAYER (tool constant)",
                "provenance": {
                    "evidence_kind": PROPOSED_EVIDENCE_KIND,
                    "evidence_kind_status": D5_RESOLVED_NOTE,
                    "extraction_method": f"capture_own_account_evidence.py tool_sha256={tool_sha[:16]} user_funding_history",
                    "source_locator": f"{source_file}#{pointer}",
                    "source_sha256": source_sha,
                    "source_title": f"Hyperliquid userFunding {address} run {run_id}",
                },
                "raw_rate": rate,
                "source_event_digest": unresolved("D-1"),
                "observed": {"usdc": usdc, "szi": szi, "venue_hash": row.get("hash")},
            }
        )
        retained.append(
            {
                "attribution": address,
                "event_id": event_id,
                "ledger_effective_ts": utc_z(time_ms),
                "payload": {
                    "coin": row_coin,
                    "fundingRate": rate,
                    "szi": szi,
                    "usdc": usdc,
                },
                # the Bridge's normalized reconcile digest is a Bridge OBSERVATION of the
                # event, not the D-1 source domain; no store has observed these events
                "payload_digest": BRIDGE_DIGEST_UNAVAILABLE,
                "payload_reason": PAYLOAD_RETAINED,
                "symbol": row_coin,
            }
        )

    packet = {
        "label": DRAFT_LABEL,
        "adapter_version": ADAPTER_VERSION,
        "packet_version": PACKET_VERSION_TARGET,
        "bindings": bindings,
        "coverage": {
            "account_scope": address,
            "complete": witness["complete"],
            "evidence_kind": PROPOSED_EVIDENCE_KIND,
            "expected_event_ids": [b["funding_event_id"] for b in bindings],
            "interval_end_exclusive": witness["window_end_utc"],
            "interval_start_inclusive": witness["window_start_utc"],
            "symbol": coin,
            "source_witnesses": [
                {"file": name, "sha256": sha}
                for name, sha in sorted(witness["funding_passes"].items())
            ],
            "unattributed_event_ids": [],
            "witness_identity": (
                f"capture_own_account_evidence.py tool_sha256={tool_sha[:16]} run {run_id}; "
                f"ownership {((manifest.get('ownership_evidence') or {}).get('status'))} "
                f"{short_address((manifest.get('ownership_evidence') or {}).get('recovered_address', manifest.get('address')))}"
            ),
            "witness_rule": witness["rule"],
            "witness_reasons": witness["reasons"],
        },
    }
    gap_report = {
        "label": DRAFT_LABEL,
        "adapter_version": ADAPTER_VERSION,
        "run_id": run_id,
        "account_scope": address,
        "funding_events": len(bindings),
        "fills": len(derived["fills"]),
        "completeness": witness,
        "unresolved_fields": {
            "bindings[*].source_event_digest": "D-1",
            "retained_rows[*].payload_digest": BRIDGE_DIGEST_UNAVAILABLE,
            "bindings[*].funding_event_id (rule proposed, value derived)": "D-2",
            "bindings[*].event_timestamp (venue stamp kept verbatim)": "D-3",
            "bindings[*].oracle_price / oracle_price_source": "D-4",
            "coverage.evidence_kind / provenance.evidence_kind": D5_RESOLVED_NOTE,
            "coverage.complete (adapter rule, not the tool's approved witness)": "D-6",
        },
        "decisions": DECISIONS,
        "export_tool_outcome_today": _export_tool_outcome_today(packet),
        "statement": (
            "Collected, not incorporated. This draft is not an accepted economic record, not venue "
            "evidence for C-10, and not an input to any production selection path."
        ),
    }
    real_packet, real_reason, oracle_report = (
        build_real_packet(
            manifest, derived, raw, manifest_sha256, oracle, corroboration_bound
        )
        if raw is not None and manifest_sha256 is not None
        else (None, "raw response bytes were not supplied", None)
    )
    gap_report["real_capture_packet"] = {
        "ruling": RULING,
        "file": REAL_PACKET_FILENAME if real_packet is not None else None,
        "status": "BUILT" if real_packet is not None else "NOT_BUILT",
        "reason": real_reason,
        "decisions_applied": {
            "D-1": f"source_event_digest = {REAL_DIGEST_DOMAIN}:sha256(exact captured row bytes)",
            "D-2": f"funding_event_id = {REAL_EVENT_ID_PREFIX}:<account-short>:<coin>:<time_ms>",
            "D-3": "event_timestamp = venue stamp verbatim; interval_hour_utc = its floor",
            "D-5": "witness_identity names run, manifest_sha256 and the ownership record",
            "D-6": (
                "coverage carries both funding passes and the fills pass as exact bytes; the "
                "export tool re-derives the completeness grid (which excludes the window's own "
                "start hour, D6-GRID A), the admission band [start+1s, end+1s) (the same "
                "1-second tolerance on both boundaries, D6-START B) and the fills-based "
                "expected count on read"
            ),
        },
        "unresolved": {
            "bindings[*].oracle_price / oracle_price_source": (
                "D-4: no oracle capture at the funding instants exists in this run"
            ),
        },
        "export_tool_invocation": "export_mtc_funding.py --evidence-kind REAL_CAPTURE_READ_ONLY",
        "export_tool_outcome_expected": EXPECTED_REAL_TOOL_REFUSAL,
        "statement": (
            "The accepting shape of the intake. It admits NO production evidence: "
            "OD-20260914-P012-ADMISSION-Q3 (Wait) and the gate order Q6 stand."
        ),
    }
    if oracle_report is not None:
        gap_report["real_capture_packet"]["oracle"] = oracle_report
    return {
        "packet": packet,
        "retained_rows": {"label": DRAFT_LABEL, "rows": retained},
        "gap_report": gap_report,
        "real_packet": real_packet,
    }


def _canonical(obj: Any) -> bytes:
    return (
        json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False)
        + "\n"
    ).encode("utf-8")


def write_outputs(out_dir: Path, intake: dict[str, Any]) -> dict[str, str]:
    out_dir = Path(out_dir)
    if out_dir.exists():
        raise IntakeRefused(
            "INTAKE_OUTPUT_EXISTS",
            f"output directory already exists (write-once): {out_dir}",
        )
    out_dir.mkdir(parents=True)
    digests: dict[str, str] = {}
    outputs = [
        ("binding_packet_draft.json", intake["packet"]),
        ("retained_rows_expected.json", intake["retained_rows"]),
        ("intake_gap_report.json", intake["gap_report"]),
    ]
    if intake.get("real_packet") is not None:
        outputs.append((REAL_PACKET_FILENAME, intake["real_packet"]))
    for name, obj in outputs:
        raw = _canonical(obj)
        with (out_dir / name).open("xb") as handle:
            handle.write(raw)
        digest = hashlib.sha256(raw).hexdigest()
        (out_dir / (name + ".sha256")).write_text(digest + "\n", encoding="ascii")
        digests[name] = digest
    return digests


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--run-dir", required=True, help="a Path-1 capture run directory (read-only)"
    )
    parser.add_argument("--out", required=True, help="write-once output directory")
    parser.add_argument(
        "--oracle-reads",
        help=(
            "an oracle reader directory (read-only). Absent: the packet is exactly what it "
            "was before O-1 existed. Present: each instant's bracket is verified against the "
            "raw bytes and still fails closed unless its corroboration can be adjudicated. "
            "There is no option that relaxes a tolerance, supplies a comparison bound or "
            "admits evidence."
        ),
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        manifest, derived, raw, manifest_sha256 = load_capture(Path(args.run_dir))
        oracle = (
            oracle_tool.load_reads(Path(args.oracle_reads))
            if args.oracle_reads
            else None
        )
        intake = build_intake(manifest, derived, raw, manifest_sha256, oracle)
        digests = write_outputs(Path(args.out), intake)
    except IntakeRefused as exc:
        print(f"INTAKE_REFUSED {exc.code}: {exc}", file=sys.stderr)
        return 3
    except oracle_tool.OracleRefused as exc:
        print(f"ORACLE_REFUSED {exc.code}: {exc}", file=sys.stderr)
        return 3
    report = intake["gap_report"]
    real = report["real_capture_packet"]
    oracle_mode = (real.get("oracle") or {}).get("mode", "ABSENT")
    print(
        f"{DRAFT_LABEL} events={report['funding_events']} fills={report['fills']} "
        f"complete={report['completeness']['complete']} "
        f"export_tool_would_refuse={report['export_tool_outcome_today']['refusal_code']} "
        f"real_packet={real['status']} real_packet_tool_outcome_expected={real['export_tool_outcome_expected']} "
        f"oracle_reads={oracle_mode}"
    )
    for name, digest in digests.items():
        print(f"{digest}  {name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
