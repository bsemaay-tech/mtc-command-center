from __future__ import annotations

import hashlib
import io
import json
import re
import unittest
from collections import defaultdict
from contextlib import redirect_stdout
from copy import deepcopy
from pathlib import Path
from unittest.mock import patch

import p011_gate
import row_arm
import stage1_freeze
from scenario_binding import (
    ConsumerEvidence,
    ExecutionEvidence,
    ManifestRowError,
    ManifestScenarioSource,
    ScenarioBindingError,
    ScenarioShapeError,
    bind_scenario,
    consume_execution,
    lookup_manifest_row,
    require_complete,
    verifier_scenario_contract,
)


GATE_DIR = Path(__file__).resolve().parent
MANIFEST_PATH = GATE_DIR / "p011_legacy_manifest.json"
VARIANT_DIR = Path(r"C:\tmp\N8_VARIANTS")
REQUIRED_VARIANT_KEYS = (
    "scenario_id",
    "producer_adapter",
    "complete_inputs",
    "literal_expected_observation",
    "literal_expected_final_state",
    "expectation_derivation",
    "comparison_rule",
    "clean_producer_corroboration",
    "producer_mutation",
)


def _load_manifest() -> dict:
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def _write_variant(name: str, manifest: dict) -> Path:
    VARIANT_DIR.mkdir(parents=True, exist_ok=True)
    path = VARIANT_DIR / name
    path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return path


_PATH_TOKEN = re.compile(r"\.([^\.\[]+)|\[(\d+)\]")


def _path_tokens(path: str) -> list[str | int]:
    return [
        int(index) if index else key
        for key, index in _PATH_TOKEN.findall(path)
    ]


def _mutated_value(value: object) -> object:
    if type(value) is bool:
        return not value
    if type(value) is str:
        return f"{value}__N8_VARIANT"
    if type(value) is int:
        return value + 1
    if type(value) is float:
        return value + 0.5
    if value is None:
        return "N8_VARIANT"
    if type(value) is dict:
        return {"unknown_sibling_n8": True}
    if type(value) is list:
        return ["N8_VARIANT"]
    raise AssertionError(f"unsupported declared leaf type: {type(value).__name__}")


def _apply_leaf_variant(scenario: dict, path: str, operation: str) -> None:
    tokens = _path_tokens(path)
    parent: object = scenario
    for token in tokens[:-1]:
        parent = parent[token]  # type: ignore[index]
    key = tokens[-1]
    value = parent[key]  # type: ignore[index]
    if operation == "mutate":
        parent[key] = _mutated_value(value)  # type: ignore[index]
        return
    if operation == "delete":
        if type(parent) is dict:
            parent.pop(key)
        else:
            parent.pop(key)  # type: ignore[arg-type]
        return
    if operation != "unknown_sibling":
        raise AssertionError(operation)
    if type(value) is dict:
        value["unknown_sibling_n8"] = True
    elif type(value) is list:
        value.append("N8_UNKNOWN_SIBLING")
    elif type(parent) is dict:
        parent["unknown_sibling_n8"] = True
    else:
        parent.append("N8_UNKNOWN_SIBLING")  # type: ignore[union-attr]


class ScenarioBindingModuleTests(unittest.TestCase):
    def setUp(self) -> None:
        self.contract = verifier_scenario_contract("C01")
        self.scenario = self.contract.as_mapping()

    def test_complete_consumption_conserves_every_declared_leaf(self) -> None:
        binding = bind_scenario(self.scenario, self.contract)
        grouped: dict[str, list[str]] = defaultdict(list)
        for leaf in binding.declared_leaves:
            grouped[leaf.expected_consumer].append(leaf.path)
        records = {
            consumer: ConsumerEvidence(
                consumer=consumer,
                declaration_paths=tuple(paths),
                evidence={"result": "satisfied"},
            )
            for consumer, paths in grouped.items()
        }
        execution = ExecutionEvidence(
            comparators=tuple(
                record
                for consumer, record in records.items()
                if consumer not in {"authority_execution", "producer_mutation_restoration"}
            ),
            authority_executions=(records["authority_execution"],),
            mutation_restorations=(records["producer_mutation_restoration"],),
        )
        consumption = consume_execution(binding, execution)
        require_complete(consumption)
        self.assertEqual(len(binding.declared_leaves), len(binding.bound_paths))
        self.assertEqual(len(binding.declared_leaves), len(consumption.consumed_leaves))

    def test_incomplete_consumption_names_path_and_expected_consumer(self) -> None:
        binding = bind_scenario(self.scenario, self.contract)
        consumption = consume_execution(binding, ExecutionEvidence())
        with self.assertRaisesRegex(
            ScenarioBindingError,
            r"declaration path .* reached no consumer; expected ",
        ):
            require_complete(consumption)

    def test_duplicate_consumption_is_refused(self) -> None:
        binding = bind_scenario(self.scenario, self.contract)
        leaf = binding.declared_leaves[0]
        record = ConsumerEvidence(
            consumer=leaf.expected_consumer,
            declaration_paths=(leaf.path,),
            evidence={"result": "satisfied"},
        )
        with self.assertRaisesRegex(ScenarioBindingError, "consumed more than once"):
            consume_execution(binding, ExecutionEvidence(comparators=(record, record)))

    def test_wrong_consumer_is_refused(self) -> None:
        binding = bind_scenario(self.scenario, self.contract)
        leaf = binding.declared_leaves[0]
        record = ConsumerEvidence(
            consumer="wrong_consumer",
            declaration_paths=(leaf.path,),
            evidence={"result": "satisfied"},
        )
        with self.assertRaisesRegex(ScenarioBindingError, "expected consumer"):
            consume_execution(binding, ExecutionEvidence(comparators=(record,)))

    def test_missing_plus_extra_top_level_key_is_refused(self) -> None:
        scenario = deepcopy(self.scenario)
        scenario.pop("scenario_id")
        scenario["unknown_control"] = True
        with self.assertRaisesRegex(ScenarioShapeError, "missing=.*scenario_id.*extra"):
            bind_scenario(scenario, self.contract)

    def test_row_lookup_refuses_absent_duplicate_and_wrong_position(self) -> None:
        manifest = _load_manifest()
        with self.assertRaisesRegex(ManifestRowError, "absent"):
            lookup_manifest_row(manifest, "C99")
        duplicate = deepcopy(manifest)
        duplicate["rows"][1]["row_id"] = "C01"
        with self.assertRaisesRegex(ManifestRowError, "duplicated"):
            lookup_manifest_row(duplicate, "C01")
        reordered = deepcopy(manifest)
        reordered["rows"][0], reordered["rows"][1] = (
            reordered["rows"][1],
            reordered["rows"][0],
        )
        with self.assertRaisesRegex(ManifestRowError, "position mismatch"):
            bind_scenario(
                ManifestScenarioSource(
                    manifest=reordered,
                    row_id="C01",
                    expected_position=0,
                ),
                self.contract,
            )


class GateVariantTests(unittest.TestCase):
    def test_compare_exact_reports_actual_expected_leaf_visits(self) -> None:
        visited: list[str] = []
        mismatches = row_arm.compare_exact(
            {"kept": 1, "missing": {"nested": 2}},
            {"kept": 1},
            expected_leaf_paths_visited=visited,
        )
        self.assertEqual(["$.kept"], visited)
        self.assertEqual("missing", mismatches[0]["reason"])

    def test_eighteen_missing_key_variants_refuse_before_producer(self) -> None:
        results: list[dict] = []
        with patch.object(p011_gate, "run_profile") as run_profile_spy:
            for key in REQUIRED_VARIANT_KEYS:
                for with_extra in (False, True):
                    manifest = _load_manifest()
                    scenario = manifest["rows"][0]["scenarios"][0]
                    scenario.pop(key)
                    if with_extra:
                        scenario["unknown_control"] = "EXTRA_CONTROL"
                    suffix = "with_extra" if with_extra else "missing_only"
                    path = _write_variant(f"after_fix_{key}_{suffix}.json", manifest)
                    digest = hashlib.sha256(path.read_bytes()).hexdigest()
                    try:
                        p011_gate.validate_legacy_manifest(path, digest)
                    except p011_gate.GateStop as exc:
                        results.append(
                            {
                                "deleted_key": key,
                                "extra_unknown_key": with_extra,
                                "outcome": "REFUSED",
                                "producer_executed": run_profile_spy.called,
                                "reason": str(exc),
                                "variant": str(path),
                            }
                        )
                    else:
                        self.fail(f"variant was accepted: {path}")
        result_path = VARIANT_DIR / "section2_results.json"
        result_path.write_text(
            json.dumps(results, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        self.assertEqual(18, len(results))
        self.assertTrue(all(item["outcome"] == "REFUSED" for item in results))
        self.assertFalse(any(item["producer_executed"] for item in results))

    def test_comparison_and_expectation_provenance_are_typed(self) -> None:
        contract = verifier_scenario_contract("C01")
        self.assertEqual(stage1_freeze.COMPARISON_RULE_ID, contract.comparison_rule)
        self.assertEqual(
            stage1_freeze.EXPECTATION_METHOD_ID,
            contract.expectation_derivation.method,
        )

    def test_wrong_mutation_mismatch_path_is_refused_by_named_consumer(self) -> None:
        binding = row_arm.validate_contract_binding(
            _load_manifest(), row_arm.ROW_CONTRACTS["C01"]
        )
        application = row_arm.mutation_application_contract(
            row_arm.ROW_CONTRACTS["C01"].mutation
        )
        wrong_red = {
            "parsed_output": {
                "comparison": {
                    "mismatches": [
                        {"path": "$.observation.candidate_side", "reason": "value"}
                    ]
                },
                "outcome": "FAIL",
            },
            "return_code": 1,
        }
        clean_green = {
            "parsed_output": {"comparison": {"mismatches": []}, "outcome": "PASS"},
            "return_code": 0,
        }
        with self.assertRaisesRegex(row_arm.RowStop, "required RED predicate"):
            row_arm.consume_producer_mutation_restoration(
                binding,
                application,
                wrong_red,
                clean_green,
            )

    def test_wrong_mutation_replacement_is_refused_by_named_consumer(self) -> None:
        binding = row_arm.validate_contract_binding(
            _load_manifest(), row_arm.ROW_CONTRACTS["C01"]
        )
        wrong_application = row_arm.mutation_application_contract(
            row_arm.Mutation(
                row_arm.ROW_CONTRACTS["C01"].mutation.mutation_id,
                row_arm.ROW_CONTRACTS["C01"].mutation.target,
                "        if raw.long == raw.short:\n            return None\n",
                "        if raw.long == raw.short:\n            return POSITION_SIDE_LONG\n",
            )
        )
        canonical_red = {
            "parsed_output": {
                "comparison": {
                    "mismatches": [
                        {"path": "$.observation.gated_long", "reason": "value"}
                    ]
                },
                "outcome": "FAIL",
            },
            "return_code": 1,
        }
        canonical_green = {
            "parsed_output": {"comparison": {"mismatches": []}, "outcome": "PASS"},
            "return_code": 0,
        }
        with self.assertRaisesRegex(row_arm.RowStop, "target or replacement differs"):
            row_arm.consume_producer_mutation_restoration(
                binding,
                wrong_application,
                canonical_red,
                canonical_green,
            )

    def test_authority_control_is_bound_by_identity_not_position(self) -> None:
        results = [
            {"error": None, "valid": True, "value": value}
            for value in reversed(row_arm.C32_AUTHORITY_VALUES)
        ]
        results.insert(
            2,
            {
                "error": "ValueError: invalid",
                "valid": False,
                "value": row_arm.C32_INVALID_CONTROL,
            },
        )
        authority, control = row_arm.partition_c32_results(results)
        self.assertEqual(
            list(row_arm.C32_AUTHORITY_VALUES),
            [item["value"] for item in authority],
        )
        self.assertEqual(row_arm.C32_INVALID_CONTROL, control["value"])
        self.assertFalse(control["valid"])

    def test_sequence_builder_records_terminal_consumption_for_every_leaf(self) -> None:
        corroboration = p011_gate.build_row_corroboration(_load_manifest())
        applicable = [
            row for row in corroboration["rows"] if row["status"] == "STOP"
        ]
        self.assertEqual(40, len(applicable))
        for row in applicable:
            consumption = row["contract_consumption"]
            self.assertEqual("CONSERVED_STOP", consumption["status"])
            self.assertEqual(
                consumption["declared_leaf_count"],
                consumption["bound_leaf_count"],
            )
            self.assertEqual(
                consumption["declared_leaf_count"],
                consumption["consumed_leaf_count"],
            )

    def test_full_declared_leaf_variant_matrix_refuses_and_restores(self) -> None:
        manifest = _load_manifest()
        variant_root = VARIANT_DIR / "leaf_variants"
        variant_root.mkdir(parents=True, exist_ok=True)
        matrix: list[dict] = []
        leaf_number = 0

        def write_manifest(path: Path, value: dict) -> str:
            path.write_text(
                json.dumps(
                    value,
                    allow_nan=False,
                    ensure_ascii=False,
                    separators=(",", ":"),
                    sort_keys=True,
                )
                + "\n",
                encoding="utf-8",
            )
            return hashlib.sha256(path.read_bytes()).hexdigest()

        def validate(path: Path, digest: str) -> tuple[int, str, dict]:
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                return_code = p011_gate.main(
                    [
                        "validate-legacy-manifest",
                        "--legacy-manifest",
                        str(path),
                        "--legacy-manifest-sha256",
                        digest,
                    ]
                )
            output_line = stdout.getvalue().strip().splitlines()[-1]
            return return_code, output_line, json.loads(output_line)

        with patch.object(p011_gate, "run_profile") as run_profile_spy:
            for row_index, row in enumerate(manifest["rows"]):
                if row["disposition"] != "APPLICABLE":
                    continue
                row_id = row["row_id"]
                binding = bind_scenario(
                    row["scenarios"][0], verifier_scenario_contract(row_id)
                )
                for leaf in binding.declared_leaves:
                    leaf_number += 1
                    restored_path = variant_root / f"leaf_{leaf_number:04d}_{row_id}_restored.json"
                    restored_sha256 = write_manifest(restored_path, manifest)
                    restored_rc, restored_line, restored_output = validate(
                        restored_path, restored_sha256
                    )
                    self.assertEqual(0, restored_rc, restored_line)
                    self.assertEqual("PASS", restored_output["outcome"])
                    for operation in ("mutate", "delete", "unknown_sibling"):
                        changed = deepcopy(manifest)
                        scenario = changed["rows"][row_index]["scenarios"][0]
                        _apply_leaf_variant(scenario, leaf.path, operation)
                        variant_path = variant_root / (
                            f"leaf_{leaf_number:04d}_{row_id}_{operation}.json"
                        )
                        variant_sha256 = write_manifest(variant_path, changed)
                        return_code, output_line, output = validate(
                            variant_path, variant_sha256
                        )
                        self.assertIn(return_code, {1, 3}, output_line)
                        self.assertIn(output["outcome"], {"FAIL", "STOP"})
                        matrix.append(
                            {
                                "actual_output_line": output_line,
                                "declaration_path": leaf.path,
                                "expected_consumer": leaf.expected_consumer,
                                "operation": operation,
                                "producer_executed": run_profile_spy.called,
                                "restoration_output_line": restored_line,
                                "restored_sha256": restored_sha256,
                                "row_id": row_id,
                                "terminal_disposition": "REFUSED_BEFORE_PRODUCER",
                                "variant": str(variant_path),
                                "variant_sha256": variant_sha256,
                            }
                        )

        matrix_path = VARIANT_DIR / "leaf_variant_matrix.json"
        matrix_path.write_text(
            json.dumps(matrix, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        expected_variants = sum(
            len(
                bind_scenario(
                    row["scenarios"][0], verifier_scenario_contract(row["row_id"])
                ).declared_leaves
            )
            for row in manifest["rows"]
            if row["disposition"] == "APPLICABLE"
        ) * 3
        self.assertEqual(expected_variants, len(matrix))
        self.assertFalse(any(item["producer_executed"] for item in matrix))

    def test_reordered_rows_are_refused(self) -> None:
        manifest = _load_manifest()
        manifest["rows"][0], manifest["rows"][1] = manifest["rows"][1], manifest["rows"][0]
        path = _write_variant("after_fix_reordered_c01_c02.json", manifest)
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        with patch.object(p011_gate, "run_profile") as run_profile_spy:
            with self.assertRaisesRegex(p011_gate.GateFail, "position mismatch") as raised:
                p011_gate.validate_legacy_manifest(path, digest)
        result = {
            "outcome": "REFUSED",
            "producer_executed": run_profile_spy.called,
            "reason": str(raised.exception),
            "variant": str(path),
        }
        (VARIANT_DIR / "section4b_result.json").write_text(
            json.dumps(result, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

    def test_c32_validates_five_authority_values_and_rejects_control(self) -> None:
        records = row_arm.build_unresolved_records(_load_manifest())
        c32 = next(item for item in records if item["row_id"] == "C32")
        validation = c32["source_evidence"]["validation_by_value"]
        authority_values = list(row_arm.C32_AUTHORITY_VALUES)
        self.assertEqual(authority_values, [item["value"] for item in validation[:-1]])
        self.assertTrue(all(item["valid"] for item in validation[:-1]))
        self.assertEqual(row_arm.C32_INVALID_CONTROL, validation[-1]["value"])
        self.assertFalse(validation[-1]["valid"])
        self.assertEqual("UNRESOLVED_AUTHORITY_CONTRADICTION", c32["status"])
        result = {
            "authority_values": authority_values,
            "invalid_control": validation[-1],
            "status": c32["status"],
            "validation_by_value": validation,
        }
        (VARIANT_DIR / "section3_result.json").write_text(
            json.dumps(result, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
