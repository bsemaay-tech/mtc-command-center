"""WP-P0-12 funding intake adapter — the NON-ACCEPTING half of the production intake (2026-09-15).

Reads one Path-1 read-only capture run (``CAPTURE_MANIFEST.json`` + ``DERIVED_EXTRACTION.json`` written by
``capture_own_account_evidence.py``) and emits, deterministically and offline:

* ``binding_packet_draft.json`` — the shape ``export_mtc_funding.py`` consumes, with every field the captured
  bytes can supply filled, and every field they cannot supply set to the literal ``UNRESOLVED:D-n``
  (the decision that would resolve it). Nothing is guessed: no oracle price, no digest domain, no
  admitted evidence kind. The export tool refuses this packet today by design
  (``CANDIDATE_PRODUCTION_EVIDENCE_UNAVAILABLE``: only ``SYNTHETIC_FIXTURE`` evidence is accepted).
* ``retained_rows_expected.json`` — what a schema-v10 Bridge store would have to retain per event.
* ``intake_gap_report.json`` — the open decisions D-1..D-6, counts, the completeness-rule result and
  the refusal the export tool raises for this packet.

Every artifact carries the label ``NONACCEPTING_INTAKE_DRAFT``. No network, no credential, no write
into the capture directory (the output directory is write-once). Authority: ``OD-20260915-BUILD-ABC-1``
item (b); design note ``P012_FUNDING_INTAKE_DESIGN_20260915.md``.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ADAPTER_VERSION = "p012-funding-intake/v1"
DRAFT_LABEL = "NONACCEPTING_INTAKE_DRAFT"
PACKET_VERSION_TARGET = "SYNTHETIC_FUNDING_BINDING_PACKET_V1"
PROPOSED_EVIDENCE_KIND = "REAL_CAPTURE_READ_ONLY"
APPROVED_PAYER = (
    "LONG"  # export_mtc_funding.APPROVED_PAYER — the tool's own rule, not a guess
)
PAYLOAD_RETAINED = "FUNDING_PAYLOAD_RETAINED"
EXPECTED_TOOL_REFUSAL = "CANDIDATE_PRODUCTION_EVIDENCE_UNAVAILABLE"
HOUR_MS = 3_600_000
DECISIONS = {
    "D-1": "production source_event_digest byte domain (also the retained payload_digest domain)",
    "D-2": "funding_event_id rule for venue funding rows (the venue hash is the zero hash)",
    "D-3": "event timestamp: venue stamp verbatim vs hour boundary",
    "D-4": "oracle price and its source for a funding instant (not in the funding row)",
    "D-5": "admitting a real read-only capture evidence kind beside SYNTHETIC_FIXTURE",
    "D-6": "whole-interval completion witness for read-only captures",
}


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


def load_capture(run_dir: Path) -> tuple[dict[str, Any], dict[str, Any]]:
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
    return manifest, derived


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


def build_intake(manifest: dict[str, Any], derived: dict[str, Any]) -> dict[str, Any]:
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
                    "evidence_kind_status": unresolved("D-5"),
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
                "payload_digest": unresolved("D-1"),
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
            "retained_rows[*].payload_digest": "D-1",
            "bindings[*].funding_event_id (rule proposed, value derived)": "D-2",
            "bindings[*].event_timestamp (venue stamp kept verbatim)": "D-3",
            "bindings[*].oracle_price / oracle_price_source": "D-4",
            "coverage.evidence_kind / provenance.evidence_kind": "D-5",
            "coverage.complete (adapter rule, not the tool's approved witness)": "D-6",
        },
        "decisions": DECISIONS,
        "export_tool_outcome_today": {
            "refusal_code": EXPECTED_TOOL_REFUSAL,
            "reason": "only SYNTHETIC_FIXTURE evidence is accepted; this packet carries a real read-only capture",
        },
        "statement": (
            "Collected, not incorporated. This draft is not an accepted economic record, not venue "
            "evidence for C-10, and not an input to any production selection path."
        ),
    }
    return {
        "packet": packet,
        "retained_rows": {"label": DRAFT_LABEL, "rows": retained},
        "gap_report": gap_report,
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
    for name, obj in (
        ("binding_packet_draft.json", intake["packet"]),
        ("retained_rows_expected.json", intake["retained_rows"]),
        ("intake_gap_report.json", intake["gap_report"]),
    ):
        raw = _canonical(obj)
        with (out_dir / name).open("xb") as handle:
            handle.write(raw)
        digest = hashlib.sha256(raw).hexdigest()
        (out_dir / (name + ".sha256")).write_text(digest + "\n", encoding="ascii")
        digests[name] = digest
    return digests


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--run-dir", required=True, help="a Path-1 capture run directory (read-only)"
    )
    parser.add_argument("--out", required=True, help="write-once output directory")
    args = parser.parse_args(argv)
    try:
        manifest, derived = load_capture(Path(args.run_dir))
        intake = build_intake(manifest, derived)
        digests = write_outputs(Path(args.out), intake)
    except IntakeRefused as exc:
        print(f"INTAKE_REFUSED {exc.code}: {exc}", file=sys.stderr)
        return 3
    report = intake["gap_report"]
    print(
        f"{DRAFT_LABEL} events={report['funding_events']} fills={report['fills']} "
        f"complete={report['completeness']['complete']} export_tool_would_refuse={EXPECTED_TOOL_REFUSAL}"
    )
    for name, digest in digests.items():
        print(f"{digest}  {name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
