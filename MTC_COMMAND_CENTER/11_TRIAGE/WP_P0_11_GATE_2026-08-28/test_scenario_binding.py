from __future__ import annotations

import hashlib
import json
import unittest
from collections import defaultdict
from copy import deepcopy
from pathlib import Path

import p011_gate
import row_arm
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
VARIANT_DIR = Path(r"C:\tmp\N3_VARIANTS")
REQUIRED_VARIANT_KEYS = (
    "scenario_id",
    "producer_adapter",
    "complete_inputs",
    "literal_expected_observation",
    "literal_expected_final_state",
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

    def test_sixteen_missing_key_variants_refuse_before_producer(self) -> None:
        results: list[dict] = []
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
                            "producer_executed": False,
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
        self.assertEqual(16, len(results))
        self.assertTrue(all(item["outcome"] == "REFUSED" for item in results))

    def test_reordered_rows_are_refused(self) -> None:
        manifest = _load_manifest()
        manifest["rows"][0], manifest["rows"][1] = manifest["rows"][1], manifest["rows"][0]
        path = _write_variant("after_fix_reordered_c01_c02.json", manifest)
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        with self.assertRaisesRegex(p011_gate.GateFail, "position mismatch") as raised:
            p011_gate.validate_legacy_manifest(path, digest)
        result = {
            "outcome": "REFUSED",
            "producer_executed": False,
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
