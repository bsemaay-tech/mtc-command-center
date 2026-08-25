"""Verify the WP-P0-10 fixture contract without claiming kernel evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from decimal import Decimal
from pathlib import Path
from typing import Any


AUTHORITY_RELATIVE_PATH = (
    "MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_09_CAPABILITY_TABLE_2026-08-25/"
    "CAPABILITY_CANONICALIZATION_TABLE.md"
)
AUTH_PREFIX = f"{AUTHORITY_RELATIVE_PATH}:"
NORMALIZATION = (
    "UTF-8 JSON object of assertion path -> value; keys sorted; "
    "separators comma/colon; one LF terminator"
)
EXPECTED_BUILT = list(range(1, 18)) + list(range(20, 26))
EXPECTED_BLOCKED = [18, 19]
EXPECTED_VALUE_COUNT = 241
COHERENCE_FAMILIES = [4, 5, 22, 24]
COHERENCE_EXPECTED_VALUE_COUNT = 24
CITATION_PATTERN = re.compile(
    rf"{re.escape(AUTH_PREFIX)}(?P<start>[1-9][0-9]*)-(?P<end>[1-9][0-9]*) "
    r"\((?P<label>[^)]+)\)"
)
ROW_LABEL_PATTERN = re.compile(r"C(?P<c>[0-9]{2})/GF-(?P<gf>[0-9]{2})")
CROSS_CUTTING_PATTERN = re.compile(r"cross-cutting rule (?P<rule>[1-4])")


class VerificationError(Exception):
    """A named, user-correctable fixture-contract failure."""


def require(condition: bool, reason: str) -> None:
    if not condition:
        raise VerificationError(reason)


def canonical_bytes(value: Any) -> bytes:
    """Render JSON data in the fixture comparison seam's canonical form."""

    text = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    return (text + "\n").encode("utf-8")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise VerificationError(f"duplicate_json_key key={key}")
        result[key] = value
    return result


def reject_non_json_constant(value: str) -> None:
    raise VerificationError(f"non_json_constant value={value}")


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(
        path.read_text(encoding="utf-8"),
        object_pairs_hook=reject_duplicate_keys,
        parse_constant=reject_non_json_constant,
    )
    require(isinstance(value, dict), f"json_root_not_object path={path}")
    return value


def authority_text_sha256(text: str) -> str:
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    return sha256_bytes(normalized.encode("utf-8"))


def enclosing_c_section(lines: list[str], start: int) -> str | None:
    for index in range(start - 1, -1, -1):
        match = re.match(r"^### (C[0-9]{2})\b", lines[index])
        if match:
            return match.group(1)
    return None


def resolve_citation(citation: str, authority_lines: list[str]) -> dict[str, Any]:
    require(isinstance(citation, str), "citation_not_string")
    match = CITATION_PATTERN.fullmatch(citation)
    require(match is not None, f"citation_syntax_invalid citation={citation}")
    start = int(match.group("start"))
    end = int(match.group("end"))
    label = match.group("label")
    require(start <= end, f"citation_range_reversed citation={citation}")
    require(
        end <= len(authority_lines),
        f"citation_range_out_of_bounds citation={citation} authority_lines={len(authority_lines)}",
    )
    fragment_lines = authority_lines[start - 1 : end]
    fragment = "\n".join(fragment_lines) + "\n"

    row_match = ROW_LABEL_PATTERN.fullmatch(label)
    cross_match = CROSS_CUTTING_PATTERN.fullmatch(label)
    if row_match:
        c_number = row_match.group("c")
        gf_number = row_match.group("gf")
        require(
            c_number == gf_number,
            f"citation_row_identity_mismatch citation={citation}",
        )
        expected_section = f"C{c_number}"
        actual_section = enclosing_c_section(authority_lines, start)
        require(
            actual_section == expected_section,
            f"citation_wrong_section citation={citation} actual={actual_section}",
        )
        require(
            re.search(rf"\*\*GF-{gf_number}\b", fragment) is not None,
            f"citation_gf_marker_missing citation={citation}",
        )
    elif cross_match:
        rule_number = cross_match.group("rule")
        require(
            "## 4. Cross-cutting acceptance rules for WP-P0-10" in "\n".join(
                authority_lines[:start]
            ),
            f"citation_cross_cutting_section_missing citation={citation}",
        )
        require(
            any(line.startswith(f"{rule_number}. ") for line in fragment_lines),
            f"citation_cross_cutting_rule_missing citation={citation}",
        )
    elif label == "explicit non-decision":
        require(
            "does not decide snapshot-drift handling, the allocator/Guardian internal split"
            in fragment,
            f"citation_non_decision_missing citation={citation}",
        )
    else:
        raise VerificationError(f"citation_label_invalid citation={citation}")

    return {
        "reference": citation,
        "content_sha256": sha256_bytes(fragment.encode("utf-8")),
    }


def resolved_citations(
    citations: Any,
    authority_lines: list[str],
    location: str,
) -> list[dict[str, Any]]:
    require(
        isinstance(citations, list) and citations,
        f"citations_missing location={location}",
    )
    require(
        len(citations) == len(set(citations)),
        f"duplicate_citation location={location}",
    )
    return [resolve_citation(citation, authority_lines) for citation in citations]


def build_authority_binding(
    fixture: dict[str, Any],
    authority_lines: list[str],
) -> tuple[str, int]:
    family_number = fixture["family"]["number"]
    assertions = fixture["expected_output"]["assertions"]
    resolved_assertions: list[dict[str, Any]] = []
    citation_count = 0
    for item in assertions:
        location = f"family={family_number:02d} path={item['path']}"
        citations = resolved_citations(item["citations"], authority_lines, location)
        citation_count += len(citations)
        resolved_assertions.append(
            {
                "path": item["path"],
                "value": item["value"],
                "citations": citations,
            }
        )

    expected_output = fixture["expected_output"]
    output_hash_citations = resolved_citations(
        expected_output["sha256_citations"],
        authority_lines,
        f"family={family_number:02d} output_sha256",
    )
    state_hash_citations = resolved_citations(
        expected_output["final_state_sha256_citations"],
        authority_lines,
        f"family={family_number:02d} final_state_sha256",
    )
    citation_count += len(output_hash_citations) + len(state_hash_citations)

    mutation = fixture["deliberate_mutation"]
    mutation_citation = resolve_citation(mutation["citation"], authority_lines)
    citation_count += 1
    binding = {
        "family": fixture["family"],
        "assertions": resolved_assertions,
        "output_hash_citations": output_hash_citations,
        "state_hash_citations": state_hash_citations,
        "source_mutation_descriptor": {
            "target": mutation["target"],
            "from": mutation["from"],
            "to": mutation["to"],
            "citation": mutation_citation,
            "rationale": mutation["rationale"],
        },
    }
    return sha256_bytes(canonical_bytes(binding)), citation_count


def decimal_value(expected: dict[str, Any], path: str, family: int) -> Decimal:
    require(path in expected, f"family={family:02d} coherence_path_missing path={path}")
    try:
        return Decimal(str(expected[path]))
    except Exception as exc:
        raise VerificationError(
            f"family={family:02d} coherence_not_decimal path={path} value={expected[path]}"
        ) from exc


def require_equal(actual: Any, expected: Any, reason: str) -> None:
    require(actual == expected, f"{reason} expected={expected} actual={actual}")


def validate_coherence(fixture: dict[str, Any], expected: dict[str, Any]) -> None:
    family = fixture["family"]["number"]
    if family == 4:
        config = fixture["config"]
        metadata = fixture["frozen_metadata"]
        bucket = Decimal(metadata["bucket_capital"])
        risk_fraction = Decimal(config["requested_risk_fraction"])
        entry = Decimal(config["entry"])
        stop = Decimal(config["stop"])
        multiplier = Decimal(metadata["contract_multiplier"])
        risk_capital = bucket * risk_fraction
        per_unit_risk = abs(entry - stop) * multiplier
        proposed_qty = risk_capital / per_unit_risk
        require_equal(
            decimal_value(expected, "resolution.risk_capital", family),
            risk_capital,
            "family=04 coherence=risk_capital",
        )
        require_equal(
            decimal_value(expected, "resolution.per_unit_risk", family),
            per_unit_risk,
            "family=04 coherence=per_unit_risk",
        )
        require_equal(
            decimal_value(expected, "resolution.proposed_qty", family),
            proposed_qty,
            "family=04 coherence=proposed_qty",
        )
        require_equal(
            decimal_value(expected, "resolution.realised_risk_at_stop", family),
            proposed_qty * abs(entry - stop) * multiplier,
            "family=04 coherence=realised_risk_at_stop",
        )
        require_equal(
            decimal_value(expected, "resolution.fee_at_0_1_pct", family),
            proposed_qty * entry * multiplier * Decimal("0.001"),
            "family=04 coherence=fee_at_0_1_pct",
        )
        require_equal(
            decimal_value(expected, "short_twin.proposed_qty", family),
            proposed_qty,
            "family=04 coherence=short_twin_proposed_qty",
        )
        require_equal(
            decimal_value(expected, "state.contract_multiplier", family),
            multiplier,
            "family=04 coherence=state_contract_multiplier",
        )
    elif family == 5:
        config = fixture["config"]
        metadata = fixture["frozen_metadata"]
        quantity = Decimal(config["raw_quantity"])
        notional = quantity * Decimal(config["price"]) * Decimal(
            metadata["contract_multiplier"]
        )
        require_equal(
            decimal_value(expected, "quantity.floored", family),
            quantity,
            "family=05 coherence=floored_quantity",
        )
        require_equal(
            decimal_value(expected, "quantity.notional", family),
            notional,
            "family=05 coherence=notional",
        )
        require(
            notional < Decimal(metadata["min_notional"]),
            "family=05 coherence=fixture_not_below_min_notional",
        )
        require_equal(
            expected.get("decision.outcome"),
            "REJECT",
            "family=05 coherence=minimum_notional_outcome",
        )
        require_equal(
            expected.get("decision.reason"),
            "BELOW_MIN_NOTIONAL",
            "family=05 coherence=minimum_notional_reason",
        )
        require_equal(
            expected.get("fills.count"),
            0,
            "family=05 coherence=minimum_notional_fills",
        )
        require_equal(
            expected.get("state.order_emitted"),
            False,
            "family=05 coherence=minimum_notional_order_emitted",
        )
    elif family == 22:
        require_equal(
            expected.get("duplicate.intent_count"),
            1,
            "family=22 coherence=duplicate_intent_count",
        )
        require_equal(
            expected.get("duplicate.event_stream_equal_baseline"),
            True,
            "family=22 coherence=duplicate_event_stream",
        )
        require_equal(
            expected.get("duplicate.final_state_hash_equal_baseline"),
            True,
            "family=22 coherence=duplicate_final_state",
        )
        require_equal(
            expected.get("state.duplicate_disposition"),
            "DUPLICATE_NOOP",
            "family=22 coherence=duplicate_disposition",
        )
    elif family == 24:
        config = fixture["config"]
        require_equal(
            config.get("deliveries"),
            2,
            "family=24 coherence=delivery_count",
        )
        require_equal(
            expected.get("intent.first_delivery"),
            "APPLIED",
            "family=24 coherence=first_delivery",
        )
        require_equal(
            expected.get("intent.second_delivery"),
            "DUPLICATE_NOOP",
            "family=24 coherence=second_delivery",
        )
        require_equal(
            expected.get("intent.identity_stable"),
            True,
            "family=24 coherence=intent_identity",
        )
        for path in (
            "fills.count",
            "economic_effects.count",
            "state.intent_ledger_entries",
        ):
            require_equal(
                expected.get(path),
                1,
                f"family=24 coherence={path.replace('.', '_')}",
            )
        require_equal(
            expected.get("state.position.qty"),
            config.get("qty"),
            "family=24 coherence=position_quantity",
        )


def validate_manifest(manifest: dict[str, Any]) -> list[dict[str, Any]]:
    require(
        manifest.get("schema_version") == "wp-p0-10-golden-suite-manifest-v2",
        f"manifest_schema_version actual={manifest.get('schema_version')}",
    )
    require(
        manifest.get("family_count") == 25,
        f"manifest_family_count expected=25 actual={manifest.get('family_count')}",
    )
    require(
        manifest.get("built_count") == 23,
        f"manifest_built_count expected=23 actual={manifest.get('built_count')}",
    )
    require(
        manifest.get("blocked_count") == 2,
        f"manifest_blocked_count expected=2 actual={manifest.get('blocked_count')}",
    )
    require(
        manifest.get("built_family_numbers") == EXPECTED_BUILT,
        "manifest_built_family_numbers_mismatch",
    )
    require(
        manifest.get("blocked_family_numbers") == EXPECTED_BLOCKED,
        "manifest_blocked_family_numbers_mismatch",
    )
    require(
        manifest.get("expected_value_count") == EXPECTED_VALUE_COUNT,
        f"manifest_expected_value_count expected={EXPECTED_VALUE_COUNT} "
        f"actual={manifest.get('expected_value_count')}",
    )
    require(
        manifest.get("coherence_validated_families") == COHERENCE_FAMILIES,
        "manifest_coherence_validated_families_mismatch",
    )
    require(
        manifest.get("coherence_expected_value_count")
        == COHERENCE_EXPECTED_VALUE_COUNT,
        "manifest_coherence_expected_value_count_mismatch",
    )
    require(
        manifest.get("coherence_unvalidated_expected_value_count")
        == EXPECTED_VALUE_COUNT - COHERENCE_EXPECTED_VALUE_COUNT,
        "manifest_coherence_unvalidated_expected_value_count_mismatch",
    )
    require(
        manifest.get("authority") == AUTHORITY_RELATIVE_PATH,
        "manifest_authority_path_mismatch",
    )
    d026 = manifest.get("d026_status")
    require(isinstance(d026, dict), "manifest_d026_status_missing")
    require(
        d026.get("built_families") == "UNEARNED",
        "manifest_d026_status_must_be_unearned",
    )
    require(d026.get("earned_count") == 0, "manifest_d026_earned_count_must_be_zero")
    require(
        d026.get("unearned_count") == 23,
        "manifest_d026_unearned_count_must_be_23",
    )
    families = manifest.get("families")
    require(isinstance(families, list), "manifest_families_not_list")
    require(len(families) == 25, "manifest_family_entries expected=25")
    require(
        [item.get("number") for item in families] == list(range(1, 26)),
        "manifest_family_entry_numbers_mismatch",
    )
    return families


def validate_fixture(
    fixture: dict[str, Any],
    manifest_item: dict[str, Any],
    authority_lines: list[str],
) -> tuple[int, bytes, str, str, Any, int]:
    number = manifest_item["number"]
    require(
        fixture.get("schema_version") == "wp-p0-10-golden-fixture-v1",
        f"family={number:02d} schema_version_mismatch",
    )
    family = fixture.get("family")
    require(isinstance(family, dict), f"family={number:02d} metadata_missing")
    require(family.get("number") == number, f"family={number:02d} number_mismatch")
    require(
        family.get("name") == manifest_item.get("name"),
        f"family={number:02d} name_mismatch",
    )
    require(family.get("status") == "BUILT", f"family={number:02d} status_not_built")
    authority = fixture.get("authority")
    require(isinstance(authority, dict), f"family={number:02d} authority_missing")
    require(
        authority.get("path") == AUTHORITY_RELATIVE_PATH,
        f"family={number:02d} authority_path_mismatch",
    )
    require(isinstance(fixture.get("config"), dict), f"family={number:02d} config_missing")
    require(
        isinstance(fixture.get("frozen_metadata"), dict),
        f"family={number:02d} frozen_metadata_missing",
    )
    require(
        isinstance(fixture.get("normalized_bars"), list),
        f"family={number:02d} normalized_bars_not_list",
    )

    expected_output = fixture.get("expected_output")
    require(
        isinstance(expected_output, dict),
        f"family={number:02d} expected_output_missing",
    )
    require(
        expected_output.get("normalization") == NORMALIZATION,
        f"family={number:02d} normalization_mismatch",
    )
    assertions = expected_output.get("assertions")
    require(
        isinstance(assertions, list) and assertions,
        f"family={number:02d} assertions_missing",
    )
    expected: dict[str, Any] = {}
    for item in assertions:
        require(isinstance(item, dict), f"family={number:02d} assertion_not_object")
        path = item.get("path")
        require(
            isinstance(path, str) and path,
            f"family={number:02d} assertion_path_invalid",
        )
        require(path not in expected, f"family={number:02d} duplicate_path path={path}")
        require("value" in item, f"family={number:02d} assertion_value_missing path={path}")
        expected[path] = item["value"]

    expected_bytes = canonical_bytes(expected)
    expected_sha = sha256_bytes(expected_bytes)
    require(
        expected_sha == expected_output.get("sha256"),
        f"family={number:02d} output_sha256_mismatch",
    )
    state = {key: value for key, value in expected.items() if key.startswith("state.")}
    require(state, f"family={number:02d} state_assertions_missing")
    state_sha = sha256_bytes(canonical_bytes(state))
    require(
        state_sha == expected_output.get("final_state_sha256"),
        f"family={number:02d} final_state_sha256_mismatch",
    )

    mutation = fixture.get("deliberate_mutation")
    require(isinstance(mutation, dict), f"family={number:02d} mutation_descriptor_missing")
    target = mutation.get("target")
    require(target in expected, f"family={number:02d} mutation_target_missing target={target}")
    require(
        expected[target] == mutation.get("from"),
        f"family={number:02d} mutation_from_mismatch target={target}",
    )
    require(
        mutation.get("to") != mutation.get("from"),
        f"family={number:02d} mutation_values_equal target={target}",
    )
    require(
        isinstance(mutation.get("rationale"), str) and mutation["rationale"],
        f"family={number:02d} mutation_rationale_missing",
    )

    validate_coherence(fixture, expected)
    authority_binding_sha, citation_count = build_authority_binding(
        fixture, authority_lines
    )
    require(
        authority_binding_sha == manifest_item.get("authority_binding_sha256"),
        f"family={number:02d} authority_binding_sha256_mismatch",
    )
    fixture_contract_sha = sha256_bytes(canonical_bytes(fixture))
    require(
        fixture_contract_sha == manifest_item.get("fixture_contract_sha256"),
        f"family={number:02d} fixture_contract_sha256_mismatch",
    )
    return number, expected_bytes, expected_sha, target, mutation["to"], citation_count


def main() -> int:
    if not __debug__:
        raise VerificationError("python_optimization_forbidden __debug__=false")

    parser = argparse.ArgumentParser()
    parser.add_argument("fixture_dir", type=Path)
    parser.add_argument("output_dir", type=Path)
    args = parser.parse_args()

    manifest = load_json(args.fixture_dir / "manifest.json")
    families = validate_manifest(manifest)
    authority_path = Path.cwd() / Path(AUTHORITY_RELATIVE_PATH)
    authority_text = authority_path.read_text(encoding="utf-8")
    require(
        authority_text_sha256(authority_text)
        == manifest.get("authority_text_lf_sha256"),
        "authority_text_lf_sha256_mismatch",
    )
    authority_lines = authority_text.replace("\r\n", "\n").replace("\r", "\n").splitlines()

    blocked_entries = [item for item in families if item.get("status") == "BLOCKED"]
    require(
        [item.get("number") for item in blocked_entries] == EXPECTED_BLOCKED,
        "blocked_family_entries_mismatch",
    )
    for blocked in blocked_entries:
        number = blocked["number"]
        require(
            isinstance(blocked.get("missing_semantics"), list)
            and blocked["missing_semantics"],
            f"family={number:02d} blocked_missing_semantics_empty",
        )
        require(
            isinstance(blocked.get("unblocks_when"), str) and blocked["unblocks_when"],
            f"family={number:02d} blocked_unblocks_when_empty",
        )
        resolved_citations(
            blocked.get("authority_evidence"),
            authority_lines,
            f"family={number:02d} blocked_authority_evidence",
        )

    expected_fixture_names = {f"family_{number:02d}.json" for number in EXPECTED_BUILT}
    actual_fixture_names = {path.name for path in args.fixture_dir.glob("family_*.json")}
    require(
        actual_fixture_names == expected_fixture_names,
        "fixture_file_set_mismatch",
    )

    rendered: list[tuple[int, bytes]] = []
    contract_lines: list[str] = []
    fixture_manifest_hashes_matched = 0
    citation_line_ranges_validated = 0
    expected_values_total = 0
    mismatch_detected = 0
    match_restored = 0
    for manifest_item in families:
        status = manifest_item.get("status")
        require(status in {"BUILT", "BLOCKED"}, f"manifest_status_invalid status={status}")
        if status == "BLOCKED":
            continue
        number = manifest_item["number"]
        expected_name = f"family_{number:02d}.json"
        require(
            manifest_item.get("fixture") == expected_name,
            f"family={number:02d} fixture_name_mismatch",
        )
        fixture = load_json(args.fixture_dir / expected_name)
        (
            number,
            expected_bytes,
            expected_sha,
            target,
            mutation_to,
            citation_count,
        ) = validate_fixture(fixture, manifest_item, authority_lines)
        fixture_manifest_hashes_matched += 1
        citation_line_ranges_validated += citation_count

        expected = {
            item["path"]: item["value"]
            for item in fixture["expected_output"]["assertions"]
        }
        expected_values_total += len(expected)
        candidate = dict(expected)
        candidate[target] = mutation_to
        mismatches = [
            key for key in sorted(expected) if candidate.get(key) != expected[key]
        ]
        require(
            mismatches == [target],
            f"family={number:02d} contract_discriminator_mismatch paths={mismatches}",
        )
        mismatch_detected += 1
        contract_lines.append(
            f"FAMILY {number:02d} FIXTURE_CONTRACT_MISMATCH_DETECTED "
            f"mismatch_count=1 path={target} "
            f"expected={json.dumps(expected[target], ensure_ascii=False, separators=(',', ':'))} "
            f"candidate={json.dumps(candidate[target], ensure_ascii=False, separators=(',', ':'))}"
        )

        candidate[target] = expected[target]
        require(candidate == expected, f"family={number:02d} contract_restore_mismatch")
        require(
            canonical_bytes(candidate) == expected_bytes,
            f"family={number:02d} contract_restore_byte_mismatch",
        )
        match_restored += 1
        contract_lines.append(
            f"FAMILY {number:02d} FIXTURE_CONTRACT_MATCH_RESTORED path={target} "
            f"value={json.dumps(candidate[target], ensure_ascii=False, separators=(',', ':'))} "
            f"byte_match=true sha256={expected_sha}"
        )
        rendered.append((number, expected_bytes))

    require(
        fixture_manifest_hashes_matched == 23,
        "fixture_manifest_hash_count expected=23",
    )
    require(
        expected_values_total == EXPECTED_VALUE_COUNT,
        f"expected_value_count expected={EXPECTED_VALUE_COUNT} "
        f"actual={expected_values_total}",
    )
    require(mismatch_detected == 23, "contract_mismatch_count expected=23")
    require(match_restored == 23, "contract_restore_count expected=23")

    args.output_dir.mkdir(parents=True, exist_ok=True)
    for number, expected_bytes in rendered:
        (args.output_dir / f"family_{number:02d}.output.json").write_bytes(
            expected_bytes
        )
    for line in contract_lines:
        print(line)
    print(
        "SUMMARY "
        "built=23 blocked=2 "
        f"fixture_manifest_hashes_matched={fixture_manifest_hashes_matched} "
        f"citation_line_ranges_validated={citation_line_ranges_validated} "
        "coherence_families=04,05,22,24 "
        f"coherence_expected_values_validated={COHERENCE_EXPECTED_VALUE_COUNT} "
        f"expected_values_total={expected_values_total} "
        f"contract_mismatch_detected={mismatch_detected} "
        f"contract_match_restored={match_restored} "
        "d026_earned=0 d026_unearned=23"
    )
    return 0


def entrypoint() -> int:
    try:
        return main()
    except VerificationError as exc:
        print(f"VERIFY_FAIL reason={exc}", file=sys.stderr)
        return 1
    except (OSError, UnicodeError, json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
        print(
            f"VERIFY_FAIL reason={type(exc).__name__}:{exc}",
            file=sys.stderr,
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(entrypoint())
