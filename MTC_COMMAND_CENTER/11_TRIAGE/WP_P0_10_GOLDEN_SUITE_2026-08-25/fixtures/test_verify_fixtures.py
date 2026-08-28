"""Executable tamper regressions for the WP-P0-10 fixture verifier."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Callable


FIXTURE_DIR = Path(__file__).resolve().parent
AUTHORITY_RELATIVE_PATH = (
    "MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_09_CAPABILITY_TABLE_2026-08-25/"
    "CAPABILITY_CANONICALIZATION_TABLE.md"
)
AUTH_PREFIX = f"{AUTHORITY_RELATIVE_PATH}:"


def canonical_bytes(value: Any) -> bytes:
    return (
        json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )
        + "\n"
    ).encode("utf-8")


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def fixture(path: Path, number: int) -> tuple[Path, dict[str, Any]]:
    fixture_path = path / f"family_{number:02d}.json"
    return fixture_path, json.loads(fixture_path.read_text(encoding="utf-8"))


def assertion(data: dict[str, Any], target: str) -> dict[str, Any]:
    return next(
        item
        for item in data["expected_output"]["assertions"]
        if item["path"] == target
    )


def recompute_internal_hashes(data: dict[str, Any]) -> None:
    expected = {
        item["path"]: item["value"]
        for item in data["expected_output"]["assertions"]
    }
    state = {key: value for key, value in expected.items() if key.startswith("state.")}
    data["expected_output"]["sha256"] = hashlib.sha256(
        canonical_bytes(expected)
    ).hexdigest()
    data["expected_output"]["final_state_sha256"] = hashlib.sha256(
        canonical_bytes(state)
    ).hexdigest()


def resolved_citation(citation: str, authority_lines: list[str]) -> dict[str, str]:
    match = re.fullmatch(rf"{re.escape(AUTH_PREFIX)}(\d+)-(\d+) \([^)]+\)", citation)
    if match is None:
        raise ValueError(f"unsupported citation: {citation}")
    start, end = (int(value) for value in match.groups())
    fragment = "\n".join(authority_lines[start - 1 : end]) + "\n"
    return {
        "reference": citation,
        "content_sha256": hashlib.sha256(fragment.encode("utf-8")).hexdigest(),
    }


def recompute_authority_binding_hash(data: dict[str, Any]) -> str:
    authority_text = (Path.cwd() / AUTHORITY_RELATIVE_PATH).read_text(encoding="utf-8")
    authority_lines = authority_text.replace("\r\n", "\n").replace("\r", "\n").splitlines()
    expected_output = data["expected_output"]
    mutation = data["deliberate_mutation"]
    binding = {
        "family": data["family"],
        "assertions": [
            {
                "path": item["path"],
                "value": item["value"],
                "citations": [
                    resolved_citation(citation, authority_lines)
                    for citation in item["citations"]
                ],
            }
            for item in expected_output["assertions"]
        ],
        "output_hash_citations": [
            resolved_citation(citation, authority_lines)
            for citation in expected_output["sha256_citations"]
        ],
        "state_hash_citations": [
            resolved_citation(citation, authority_lines)
            for citation in expected_output["final_state_sha256_citations"]
        ],
        "source_mutation_descriptor": {
            "target": mutation["target"],
            "from": mutation["from"],
            "to": mutation["to"],
            "citation": resolved_citation(mutation["citation"], authority_lines),
            "rationale": mutation["rationale"],
        },
    }
    return hashlib.sha256(canonical_bytes(binding)).hexdigest()


def write_fixture_with_manifest_hash(
    path: Path,
    number: int,
    fixture_path: Path,
    data: dict[str, Any],
) -> None:
    write_json(fixture_path, data)
    manifest_path = path / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest_item = next(
        item for item in manifest["families"] if item["number"] == number
    )
    manifest_item["fixture_contract_sha256"] = hashlib.sha256(
        canonical_bytes(data)
    ).hexdigest()
    write_json(manifest_path, manifest)


def tamper_family_04_bug_value(path: Path) -> None:
    fixture_path, data = fixture(path, 4)
    assertion(data, "resolution.proposed_qty")["value"] = "20"
    data["deliberate_mutation"]["from"] = "20"
    data["deliberate_mutation"]["to"] = "2"
    recompute_internal_hashes(data)
    write_json(fixture_path, data)


def tamper_family_06_citations(path: Path) -> None:
    fixture_path, data = fixture(path, 6)
    fabricated = (
        "MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_09_CAPABILITY_TABLE_2026-08-25/"
        "CAPABILITY_CANONICALIZATION_TABLE.md:99999-99999 "
        "(C99/GF-99)"
    )
    for item in data["expected_output"]["assertions"]:
        item["citations"] = [fabricated]
    data["expected_output"]["sha256_citations"] = [fabricated]
    data["expected_output"]["final_state_sha256_citations"] = [fabricated]
    data["deliberate_mutation"]["citation"] = fabricated
    data["companion_scenarios"][0]["source"] = fabricated
    write_json(fixture_path, data)


def tamper_family_04_incoherent_risk(path: Path) -> None:
    fixture_path, data = fixture(path, 4)
    assertion(data, "resolution.per_unit_risk")["value"] = "25"
    recompute_internal_hashes(data)
    write_json(fixture_path, data)


def tamper_family_05_incoherent_accept(path: Path) -> None:
    fixture_path, data = fixture(path, 5)
    assertion(data, "decision.outcome")["value"] = "ACCEPT"
    data["deliberate_mutation"]["from"] = "ACCEPT"
    data["deliberate_mutation"]["to"] = "REJECT"
    recompute_internal_hashes(data)
    write_json(fixture_path, data)


def tamper_family_24_duplicate_effects(path: Path) -> None:
    fixture_path, data = fixture(path, 24)
    assertion(data, "economic_effects.count")["value"] = 2
    assertion(data, "state.position.qty")["value"] = "2"
    data["deliberate_mutation"]["from"] = 2
    data["deliberate_mutation"]["to"] = 1
    recompute_internal_hashes(data)
    write_json(fixture_path, data)


def tamper_manifest_built_count(path: Path) -> None:
    manifest_path = path / "manifest.json"
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    data["built_count"] = 22
    write_json(manifest_path, data)


def tamper_family_12_empty_primary_inputs(path: Path) -> None:
    fixture_path, data = fixture(path, 12)
    data["config"] = {}
    data["normalized_bars"] = []
    write_fixture_with_manifest_hash(path, 12, fixture_path, data)


def tamper_family_03_renamed_companion_assertion(path: Path) -> None:
    fixture_path, data = fixture(path, 3)
    data["companion_scenarios"] = [
        scenario
        for scenario in data["companion_scenarios"]
        if "legacy_precision.research_qty" not in scenario["assertion_inputs"]
    ]
    item = assertion(data, "legacy_precision.research_qty")
    item["path"] = "compat_precision.research_qty"
    recompute_internal_hashes(data)
    write_fixture_with_manifest_hash(path, 3, fixture_path, data)


def tamper_family_01_missing_signal_mode(path: Path) -> None:
    fixture_path, data = fixture(path, 1)
    del data["config"]["signal_mode"]
    write_fixture_with_manifest_hash(path, 1, fixture_path, data)


def tamper_cross_row_misspelling(path: Path) -> None:
    fixture_path, data = fixture(path, 1)
    item = assertion(data, "producer.bar0.raw")
    del item["input_paths"]
    item["cross_row_imprt"] = {
        "source": item["citations"][0],
        "inputs": {"whatever": "not a real path"},
    }
    write_fixture_with_manifest_hash(path, 1, fixture_path, data)


def tamper_family_03_cross_row_import(path: Path) -> None:
    fixture_path, data = fixture(path, 3)
    data["companion_scenarios"] = [
        scenario
        for scenario in data["companion_scenarios"]
        if "legacy_precision.research_qty" not in scenario["assertion_inputs"]
    ]
    item = assertion(data, "legacy_precision.research_qty")
    item["cross_row_import"] = {
        "source": item["citations"][0],
        "inputs": {"input_not_present_in_cited_row": "not a real path"},
    }
    write_fixture_with_manifest_hash(path, 3, fixture_path, data)


def tamper_family_14_cross_row_imports(path: Path) -> None:
    fixture_path, data = fixture(path, 14)
    data["companion_scenarios"] = []
    for target in ("legacy.long_stop_close_only", "legacy.short_stop_close_only"):
        item = assertion(data, target)
        item["cross_row_import"] = {
            "source": item["citations"][0],
            "inputs": {"whatever": "not a real path"},
        }
    write_fixture_with_manifest_hash(path, 14, fixture_path, data)


def tamper_family_20_missing_mirror_expected_value(path: Path) -> None:
    fixture_path, data = fixture(path, 20)
    del data["mirror_expected_values"]["family_03"]["qty"]
    write_fixture_with_manifest_hash(path, 20, fixture_path, data)


def tamper_family_10_companion_ohlcv_close_deleted(path: Path) -> None:
    fixture_path, data = fixture(path, 10)
    scenario = next(
        scenario
        for scenario in data["companion_scenarios"]
        if scenario["id"] == "C36_GF36_legacy_break_even_modes__local"
    )
    del scenario["normalized_bars"][3]["ohlcv"][3]
    write_fixture_with_manifest_hash(path, 10, fixture_path, data)


def tamper_family_02_c32_master_gate_deleted(path: Path) -> None:
    fixture_path, data = fixture(path, 2)
    for scenario in data["companion_scenarios"]:
        if scenario["source"].endswith("(C32/GF-32)"):
            del scenario["config"]["tw_audit_semantics_mode"]
    write_fixture_with_manifest_hash(path, 2, fixture_path, data)


def tamper_family_10_c36_master_gate_deleted(path: Path) -> None:
    fixture_path, data = fixture(path, 10)
    for scenario in data["companion_scenarios"]:
        if scenario["source"].endswith("(C36/GF-36)"):
            del scenario["config"]["tw_audit_semantics_mode"]
    write_fixture_with_manifest_hash(path, 10, fixture_path, data)


def tamper_family_11_c37_master_gate_deleted(path: Path) -> None:
    fixture_path, data = fixture(path, 11)
    for scenario in data["companion_scenarios"]:
        if scenario["source"].endswith("(C37/GF-37)"):
            del scenario["config"]["tw_audit_semantics_mode"]
    write_fixture_with_manifest_hash(path, 11, fixture_path, data)


def tamper_family_10_companion_ohlcv_key_deleted(path: Path) -> None:
    fixture_path, data = fixture(path, 10)
    scenario = next(
        scenario
        for scenario in data["companion_scenarios"]
        if scenario["id"] == "C36_GF36_legacy_break_even_modes__local"
    )
    del scenario["normalized_bars"][1]["ohlcv"]
    write_fixture_with_manifest_hash(path, 10, fixture_path, data)


def tamper_family_10_companion_bar_deleted(path: Path) -> None:
    fixture_path, data = fixture(path, 10)
    scenario = next(
        scenario
        for scenario in data["companion_scenarios"]
        if scenario["id"] == "C36_GF36_legacy_break_even_modes__local"
    )
    del scenario["normalized_bars"][2]
    write_fixture_with_manifest_hash(path, 10, fixture_path, data)


def tamper_family_10_companion_bars_reordered(path: Path) -> None:
    fixture_path, data = fixture(path, 10)
    scenario = next(
        scenario
        for scenario in data["companion_scenarios"]
        if scenario["id"] == "C36_GF36_legacy_break_even_modes__local"
    )
    bars = scenario["normalized_bars"]
    bars[1], bars[2] = bars[2], bars[1]
    write_fixture_with_manifest_hash(path, 10, fixture_path, data)


def tamper_family_10_companion_bar_index_scrambled(path: Path) -> None:
    fixture_path, data = fixture(path, 10)
    scenario = next(
        scenario
        for scenario in data["companion_scenarios"]
        if scenario["id"] == "C36_GF36_legacy_break_even_modes__local"
    )
    scenario["normalized_bars"][2]["index"] = 99
    write_fixture_with_manifest_hash(path, 10, fixture_path, data)


def tamper_family_10_companion_bar_not_object(path: Path) -> None:
    fixture_path, data = fixture(path, 10)
    scenario = next(
        scenario
        for scenario in data["companion_scenarios"]
        if scenario["id"] == "C36_GF36_legacy_break_even_modes__local"
    )
    scenario["normalized_bars"][2] = "not-a-bar"
    write_fixture_with_manifest_hash(path, 10, fixture_path, data)


def tamper_family_10_companion_ohlcv_metadata_deleted(path: Path) -> None:
    fixture_path, data = fixture(path, 10)
    scenario = next(
        scenario
        for scenario in data["companion_scenarios"]
        if scenario["id"] == "C36_GF36_legacy_break_even_modes__local"
    )
    del scenario["frozen_metadata"]["ohlcv_fields"]
    write_fixture_with_manifest_hash(path, 10, fixture_path, data)


def tamper_family_10_companion_all_indices_deleted(path: Path) -> None:
    fixture_path, data = fixture(path, 10)
    scenario = next(
        scenario
        for scenario in data["companion_scenarios"]
        if scenario["id"] == "C36_GF36_legacy_break_even_modes__local"
    )
    for bar in scenario["normalized_bars"]:
        del bar["index"]
    write_fixture_with_manifest_hash(path, 10, fixture_path, data)


def tamper_family_02_c32_retained_mapping_assertion_renamed(path: Path) -> None:
    fixture_path, data = fixture(path, 2)
    scenario = next(
        scenario
        for scenario in data["companion_scenarios"]
        if scenario["id"] == "C32_GF32_legacy_reentry_modes__local"
    )
    input_paths = scenario["assertion_inputs"].pop("legacy.local.reentry_bar")
    scenario["assertion_inputs"]["compat.local.reentry_bar"] = [
        input_path
        for input_path in input_paths
        if input_path
        not in {
            "config.tw_audit_semantics_mode",
            "config.tw_reversal_reentry_mode",
        }
    ]
    del scenario["config"]["tw_audit_semantics_mode"]
    del scenario["config"]["tw_reversal_reentry_mode"]
    assertion(data, "legacy.local.reentry_bar")["path"] = "compat.local.reentry_bar"
    recompute_internal_hashes(data)
    write_json(fixture_path, data)
    manifest_path = path / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest_item = next(
        item for item in manifest["families"] if item["number"] == 2
    )
    manifest_item["authority_binding_sha256"] = recompute_authority_binding_hash(data)
    manifest_item["fixture_contract_sha256"] = hashlib.sha256(
        canonical_bytes(data)
    ).hexdigest()
    manifest["assertion_input_path_count"] -= 2
    write_json(manifest_path, manifest)


def tamper_family_02_plural_selector(path: Path) -> None:
    fixture_path, data = fixture(path, 2)
    scenario = data["companion_scenarios"][0]
    selector = scenario["config"].pop("tw_reversal_reentry_mode")
    scenario["config"]["tw_reversal_reentry_modes"] = [selector]
    input_paths = scenario["assertion_inputs"]["legacy.local.reentry_bar"]
    selector_index = input_paths.index("config.tw_reversal_reentry_mode")
    input_paths[selector_index] = "config.tw_reversal_reentry_modes"
    write_fixture_with_manifest_hash(path, 2, fixture_path, data)


def tamper_family_02_selector_rehomed_fixture_local(path: Path) -> None:
    fixture_path, data = fixture(path, 2)
    scenario = next(
        scenario
        for scenario in data["companion_scenarios"]
        if "legacy.local.reentry_bar" in scenario["assertion_inputs"]
    )
    scenario_id = scenario["id"]
    original_input_paths = scenario["assertion_inputs"].pop("legacy.local.reentry_bar")
    data["companion_scenarios"] = [
        item for item in data["companion_scenarios"] if item["id"] != scenario_id
    ]
    item = assertion(data, "legacy.local.reentry_bar")
    item["input_paths"] = ["family.number"]
    write_json(fixture_path, data)
    manifest_path = path / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest_item = next(
        item for item in manifest["families"] if item["number"] == 2
    )
    manifest_item["fixture_contract_sha256"] = hashlib.sha256(
        canonical_bytes(data)
    ).hexdigest()
    manifest["companion_assertion_count"] -= 1
    manifest["assertion_input_path_count"] += 1 - len(original_input_paths)
    write_json(manifest_path, manifest)


def tamper_family_03_missing_literal_input(path: Path) -> None:
    fixture_path, data = fixture(path, 3)
    scenario = next(
        scenario
        for scenario in data["companion_scenarios"]
        if "legacy_precision.research_qty" in scenario["assertion_inputs"]
    )
    del scenario["literal_inputs"]["raw_quantity"]
    write_fixture_with_manifest_hash(path, 3, fixture_path, data)


def tamper_family_03_missing_primary_input(path: Path) -> None:
    fixture_path, data = fixture(path, 3)
    del data["config"]["entry_reference_price"]
    write_fixture_with_manifest_hash(path, 3, fixture_path, data)


def run_verifier(
    verifier: Path,
    fixture_dir: Path,
    output_dir: Path,
    optimized: bool = False,
) -> subprocess.CompletedProcess[str]:
    command = [sys.executable]
    if optimized:
        command.append("-O")
    command.extend([str(verifier), str(fixture_dir), str(output_dir)])
    env = os.environ.copy()
    env.pop("PYTHONOPTIMIZE", None)
    return subprocess.run(
        command,
        cwd=Path.cwd(),
        env=env,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
    )


def reason_line(result: subprocess.CompletedProcess[str]) -> str:
    lines = [
        line.strip()
        for line in (result.stderr + "\n" + result.stdout).splitlines()
        if line.strip()
    ]
    named = next((line for line in lines if line.startswith("VERIFY_FAIL reason=")), None)
    if named:
        return named
    return "no_named_rejection" if result.returncode == 0 else "unnamed_nonzero_rejection"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verifier", type=Path, default=FIXTURE_DIR / "verify_fixtures.py")
    args = parser.parse_args()
    verifier = args.verifier.resolve()
    cases: list[tuple[str, Callable[[Path], None], bool, str | None]] = [
        ("family_04_bug_value", tamper_family_04_bug_value, False, None),
        ("family_06_fabricated_citations", tamper_family_06_citations, False, None),
        ("family_04_incoherent_risk", tamper_family_04_incoherent_risk, False, None),
        ("family_05_incoherent_accept", tamper_family_05_incoherent_accept, False, None),
        ("family_24_duplicate_effects", tamper_family_24_duplicate_effects, False, None),
        (
            "b1_family_12_empty_primary_inputs",
            tamper_family_12_empty_primary_inputs,
            False,
            "VERIFY_FAIL reason=family=12 normalized_bar_count_mismatch "
            "context=fixture expected=2 actual=0",
        ),
        (
            "b1_family_03_renamed_companion_assertion",
            tamper_family_03_renamed_companion_assertion,
            False,
            "VERIFY_FAIL reason=family=03 assertion_input_source_undeclared "
            "path=compat_precision.research_qty",
        ),
        (
            "b1_family_01_missing_signal_mode",
            tamper_family_01_missing_signal_mode,
            False,
            "VERIFY_FAIL reason=family=01 assertion_input_presence_missing "
            "path=producer.bar0.raw input=config.signal_mode",
        ),
        (
            "b1_cross_row_misspelling",
            tamper_cross_row_misspelling,
            False,
            "VERIFY_FAIL reason=family=01 cross_row_import_unsupported "
            "field=cross_row_imprt path=producer.bar0.raw",
        ),
        (
            "b2_family_03_cross_row_import",
            tamper_family_03_cross_row_import,
            False,
            "VERIFY_FAIL reason=family=03 cross_row_import_unsupported "
            "field=cross_row_import path=legacy_precision.research_qty",
        ),
        (
            "b2_family_14_cross_row_imports",
            tamper_family_14_cross_row_imports,
            False,
            "VERIFY_FAIL reason=family=14 cross_row_import_unsupported "
            "field=cross_row_import path=legacy.long_stop_close_only",
        ),
        (
            "b3_family_20_missing_mirror_expected_value",
            tamper_family_20_missing_mirror_expected_value,
            False,
            "VERIFY_FAIL reason=family=20 assertion_input_presence_missing "
            "path=mirror.family_03.qty input=mirror_expected_values.family_03.qty",
        ),
        (
            "b4_family_02_plural_selector",
            tamper_family_02_plural_selector,
            False,
            "VERIFY_FAIL reason=family=02 companion_selector_mismatch "
            "path=legacy.local.reentry_bar selector=tw_reversal_reentry_mode "
            "expected=local actual=None",
        ),
        (
            "b6_family_03_missing_literal_input",
            tamper_family_03_missing_literal_input,
            False,
            "VERIFY_FAIL reason=family=03 assertion_input_presence_missing "
            "path=legacy_precision.research_qty input=literal_inputs.raw_quantity",
        ),
        (
            "b6_family_03_missing_primary_input",
            tamper_family_03_missing_primary_input,
            False,
            "VERIFY_FAIL reason=family=03 assertion_input_presence_missing "
            "path=request.accepted input=config.entry_reference_price",
        ),
        ("manifest_built_count_normal", tamper_manifest_built_count, False, None),
        (
            "manifest_built_count_optimized",
            tamper_manifest_built_count,
            True,
            "VERIFY_FAIL reason=python_optimization_forbidden",
        ),
        (
            "n2_family_10_companion_ohlcv_close_deleted",
            tamper_family_10_companion_ohlcv_close_deleted,
            False,
            "VERIFY_FAIL reason=family=10 normalized_bar_ohlcv_length_mismatch "
            "context=companion:C36_GF36_legacy_break_even_modes__local "
            "index=3 expected=5 actual=4",
        ),
        (
            "r1_family_02_c32_master_gate_deleted",
            tamper_family_02_c32_master_gate_deleted,
            False,
            "VERIFY_FAIL reason=family=02 master_gate_mismatch "
            "path=legacy.local.reentry_bar input=config.tw_audit_semantics_mode "
            "expected=research actual=None",
        ),
        (
            "r1_family_10_c36_master_gate_deleted",
            tamper_family_10_c36_master_gate_deleted,
            False,
            "VERIFY_FAIL reason=family=10 master_gate_mismatch "
            "path=legacy.local.exit input=config.tw_audit_semantics_mode "
            "expected=research actual=None",
        ),
        (
            "r1_family_11_c37_master_gate_deleted",
            tamper_family_11_c37_master_gate_deleted,
            False,
            "VERIFY_FAIL reason=family=11 master_gate_mismatch "
            "path=legacy.local.exit input=config.tw_audit_semantics_mode "
            "expected=research actual=None",
        ),
        (
            "r2_family_10_companion_ohlcv_key_deleted",
            tamper_family_10_companion_ohlcv_key_deleted,
            False,
            "VERIFY_FAIL reason=family=10 normalized_bar_ohlcv_missing "
            "context=companion:C36_GF36_legacy_break_even_modes__local index=1",
        ),
        (
            "r2_family_10_companion_bar_deleted",
            tamper_family_10_companion_bar_deleted,
            False,
            "VERIFY_FAIL reason=family=10 normalized_bar_count_mismatch "
            "context=companion:C36_GF36_legacy_break_even_modes__local "
            "expected=5 actual=4",
        ),
        (
            "r2_family_10_companion_bars_reordered",
            tamper_family_10_companion_bars_reordered,
            False,
            "VERIFY_FAIL reason=family=10 normalized_bar_index_mismatch "
            "context=companion:C36_GF36_legacy_break_even_modes__local "
            "position=1 actual=2",
        ),
        (
            "r2_family_10_companion_bar_index_scrambled",
            tamper_family_10_companion_bar_index_scrambled,
            False,
            "VERIFY_FAIL reason=family=10 normalized_bar_index_mismatch "
            "context=companion:C36_GF36_legacy_break_even_modes__local "
            "position=2 actual=99",
        ),
        (
            "r3_family_10_companion_bar_not_object",
            tamper_family_10_companion_bar_not_object,
            False,
            "VERIFY_FAIL reason=family=10 normalized_bar_not_object "
            "context=companion:C36_GF36_legacy_break_even_modes__local index=2",
        ),
        (
            "r4d_family_10_companion_ohlcv_metadata_deleted",
            tamper_family_10_companion_ohlcv_metadata_deleted,
            False,
            "VERIFY_FAIL reason=family=10 ohlcv_shape_contract_mismatch "
            "context=companion:C36_GF36_legacy_break_even_modes__local",
        ),
        (
            "r4d_family_10_companion_all_indices_deleted",
            tamper_family_10_companion_all_indices_deleted,
            False,
            "VERIFY_FAIL reason=family=10 normalized_bar_index_mismatch "
            "context=companion:C36_GF36_legacy_break_even_modes__local "
            "position=0 actual=None",
        ),
        (
            "r4d_family_02_c32_retained_mapping_assertion_renamed",
            tamper_family_02_c32_retained_mapping_assertion_renamed,
            False,
            "VERIFY_FAIL reason=family=02 companion_assertion_inventory_mismatch "
            "id=C32_GF32_legacy_reentry_modes__local",
        ),
        (
            "n4_family_02_selector_rehomed_fixture_local",
            tamper_family_02_selector_rehomed_fixture_local,
            False,
            "VERIFY_FAIL reason=family=02 companion_selector_fixture_local_forbidden "
            "path=legacy.local.reentry_bar",
        ),
    ]

    with tempfile.TemporaryDirectory(prefix="wp_p010_verifier_regression_") as temp:
        temp_path = Path(temp)
        baseline_output = temp_path / "baseline_output"
        baseline = run_verifier(verifier, FIXTURE_DIR, baseline_output)
        baseline_clean = baseline.returncode == 0
        print(
            f"BASELINE rc={baseline.returncode} clean={str(baseline_clean).lower()} "
            f"detail={reason_line(baseline)}"
        )

        rejected = 0
        for index, (name, mutate, optimized, expected_reason) in enumerate(
            cases, start=1
        ):
            case_dir = temp_path / f"case_{index:02d}"
            shutil.copytree(FIXTURE_DIR, case_dir)
            mutate(case_dir)
            result = run_verifier(
                verifier,
                case_dir,
                temp_path / f"case_{index:02d}_output",
                optimized=optimized,
            )
            detail = reason_line(result)
            was_rejected = result.returncode != 0 and (
                expected_reason is None or expected_reason in detail
            )
            rejected += int(was_rejected)
            print(
                f"TAMPER name={name} optimized={str(optimized).lower()} "
                f"rc={result.returncode} rejected={str(was_rejected).lower()} "
                f"detail={detail}"
            )

    passed = baseline_clean and rejected == len(cases)
    print(
        f"VERIFIER_REGRESSION_SUMMARY baseline_clean={int(baseline_clean)} "
        f"tamper_rejected={rejected}/{len(cases)} result={'PASS' if passed else 'FAIL'}"
    )
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
