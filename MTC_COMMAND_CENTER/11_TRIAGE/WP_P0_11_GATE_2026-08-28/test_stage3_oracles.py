from __future__ import annotations

import hashlib
import json
import sys
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path
from unittest.mock import patch

import row_arm
import stage1_freeze
from scenario_binding import (
    AuthorityRequirement,
    EXECUTION_OBSERVATION,
    SOURCE_CORROBORATION,
    ScenarioBindingError,
    bind_scenario,
    verifier_scenario_contract,
)
from stage3_oracle_contracts import stage3_oracle_mappings


class Stage3OracleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        if str(row_arm.A_PYTHON_ROOT) not in sys.path:
            sys.path.insert(0, str(row_arm.A_PYTHON_ROOT))
        cls.manifest = stage1_freeze.build_legacy_manifest(stage3=True)
        cls.rows = {row["row_id"]: row for row in cls.manifest["rows"]}

    def test_generator_and_verifier_are_separate_matching_objects(self) -> None:
        verifier = stage3_oracle_mappings()
        for row_id in ("C32", "C34", "C42"):
            generated = self.rows[row_id]["scenarios"][0]
            self.assertEqual(verifier[row_id], generated)
            self.assertIsNot(verifier[row_id], generated)
            self.assertEqual(
                generated,
                verifier_scenario_contract(row_id, stage3=True).as_mapping(),
            )

    def test_verifier_file_has_no_stage1_import(self) -> None:
        source = (Path(__file__).parent / "stage3_oracle_contracts.py").read_text(
            encoding="utf-8"
        )
        self.assertNotIn("stage1_freeze", source)

    def test_copied_prefixed_contracts_are_detected_before_execution(self) -> None:
        legacy = stage1_freeze.build_legacy_manifest(stage3=False)
        by_id = {row["row_id"]: row for row in legacy["rows"]}
        for row_id in ("C32", "C34", "C42"):
            with self.subTest(row_id=row_id):
                with self.assertRaises(ScenarioBindingError):
                    bind_scenario(
                        by_id[row_id]["scenarios"][0],
                        verifier_scenario_contract(row_id, stage3=True),
                    )

    def test_wrong_comparator_identifier_is_detected(self) -> None:
        original = row_arm.compare_exact.comparison_rule_id
        try:
            row_arm.compare_exact.comparison_rule_id = "WRONG_COMPARATOR_V1"
            with self.assertRaisesRegex(row_arm.RowStop, "comparator identifier"):
                row_arm.validate_contract_binding(
                    self.manifest, row_arm.ROW_CONTRACTS["C32"]
                )
        finally:
            row_arm.compare_exact.comparison_rule_id = original

    def test_authority_terminal_accounting_variants_fail_closed(self) -> None:
        requirements = (
            AuthorityRequirement("A_CURRENT_MASTER", EXECUTION_OBSERVATION),
            AuthorityRequirement("PINE_CURRENT_MASTER", SOURCE_CORROBORATION),
        )
        empty_execution = row_arm.authority_execution_observation(
            [], method="TEST", reason="missing execution"
        )
        pine = {"authority_name": "PINE_CURRENT_MASTER", "corroborated": True}
        missing_execution = row_arm.consume_authority_evidence(
            requirements, empty_execution, [pine]
        )
        self.assertFalse(missing_execution["satisfied"])
        self.assertIn("A_CURRENT_MASTER", missing_execution["unsatisfied"])

        a_execution = row_arm.authority_execution_observation(
            [{"module": "mtc_v2.core.runner", "path": "mtc_v2/core/runner.py"}],
            method="TEST",
            reason="A executed",
        )
        missing_source = row_arm.consume_authority_evidence(requirements, a_execution)
        self.assertFalse(missing_source["satisfied"])
        self.assertIn("PINE_CURRENT_MASTER", missing_source["unsatisfied"])

        undeclared = row_arm.consume_authority_evidence(
            requirements,
            row_arm.authority_execution_observation(
                [
                    {"module": "mtc_v2.core.runner", "path": "mtc_v2/core/runner.py"},
                    {"module": "src.engine", "path": "src/engine.py"},
                ],
                method="TEST",
                reason="undeclared B evidence",
            ),
            [pine],
        )
        self.assertEqual(["B_BACKTEST_FREEZE"], undeclared["undeclared"])
        self.assertFalse(undeclared["satisfied"])

        duplicate = [
            {
                "authority_name": "A_CURRENT_MASTER",
                "disposition": "EXECUTED",
            },
            {
                "authority_name": "A_CURRENT_MASTER",
                "disposition": "EXECUTED",
            },
            {
                "authority_name": "PINE_CURRENT_MASTER",
                "disposition": "SOURCE_CORROBORATED",
            },
        ]
        with self.assertRaisesRegex(
            row_arm.RowStop, "STOP_AUTHORITY_EVIDENCE_INCOMPLETE"
        ):
            row_arm.validate_authority_dispositions(requirements, duplicate)

    def test_c32_c34_c42_clean_producers_match_verifier_literals(self) -> None:
        old_root = row_arm.ACTIVE_AUTHORITY_ROOT
        row_arm.ACTIVE_AUTHORITY_ROOT = row_arm.A_PYTHON_ROOT
        try:
            for row_id in ("C32", "C34", "C42"):
                with self.subTest(row_id=row_id):
                    contract = row_arm.ROW_CONTRACTS[row_id]
                    observation, final_state = contract.producer(contract.complete_inputs)
                    actual = {
                        "observation": row_arm.encode_floats(observation),
                        "final_state": row_arm.encode_floats(final_state),
                    }
                    expected = {
                        "observation": row_arm.encode_floats(contract.expected_observation),
                        "final_state": row_arm.encode_floats(contract.expected_final_state),
                    }
                    self.assertEqual([], row_arm.compare_exact(expected, actual))
        finally:
            row_arm.ACTIVE_AUTHORITY_ROOT = old_root

    def test_c34_independent_mode_relations_are_observed(self) -> None:
        old_root = row_arm.ACTIVE_AUTHORITY_ROOT
        row_arm.ACTIVE_AUTHORITY_ROOT = row_arm.A_PYTHON_ROOT
        try:
            observation, _ = row_arm.produce_c34(
                row_arm.ROW_CONTRACTS["C34"].complete_inputs
            )
        finally:
            row_arm.ACTIVE_AUTHORITY_ROOT = old_root
        arms = observation["arms"]
        self.assertTrue(observation["l1_l3_field_identical"])
        self.assertEqual(arms["L1"], arms["L3"])
        self.assertNotEqual(arms["L1"]["checkpoints"], arms["L2"]["checkpoints"])

    def test_c42_source_and_b_discriminators_are_observed(self) -> None:
        source = row_arm.c42_source_correspondence_evidence()
        self.assertTrue(source["satisfied"])
        self.assertEqual("DETECTED", source["modified_copy_disposition"])
        self.assertEqual(0, source["restoration"]["closure_credit"])
        b_boundary = row_arm.c42_b_configuration_discriminator()
        self.assertTrue(b_boundary["refused"])
        self.assertEqual("REFUSED", b_boundary["outcome"])


class Stage3PublicationBoundaryTests(unittest.TestCase):
    def test_candidate_generation_writes_only_explicit_scratch_manifest(self) -> None:
        with tempfile.TemporaryDirectory(dir=stage1_freeze.STAGE3_SCRATCH_ROOT) as name:
            output = Path(name) / "candidate.json"
            args = type("Args", (), {"out": str(output)})()
            self.assertEqual(0, stage1_freeze.command_candidate_manifest(args))
            self.assertEqual(stage1_freeze.STAGE3_GATE_VERSION, json.loads(output.read_text(encoding="utf-8"))["gate_version"])

    def test_publication_refuses_missing_owner_v1_v2_and_hash_mismatch(self) -> None:
        with tempfile.TemporaryDirectory(dir=stage1_freeze.STAGE3_SCRATCH_ROOT) as name:
            root = Path(name)
            manifest = root / "manifest.json"
            stage1_freeze.write_json(manifest, stage1_freeze.build_legacy_manifest(stage3=True))
            receipt = root / "receipt.json"
            stage1_freeze.write_json(
                receipt,
                {
                    "gate_version": stage1_freeze.STAGE3_GATE_VERSION,
                    "legacy_manifest": {"sha256": stage1_freeze.sha256_file(manifest)},
                },
            )
            with self.assertRaisesRegex(SystemExit, "STOP_V3_ANCHOR_AUTHORITY_ABSENT"):
                stage1_freeze.validate_stage3_publication_prerequisites(
                    manifest_path=manifest,
                    receipt_path=receipt,
                    owner_authorization_path=root / "absent-owner.md",
                    output_path=root / "v3-anchor.json",
                )
            owner = root / "owner.md"
            owner.write_text("explicit test authority", encoding="utf-8")
            with self.assertRaisesRegex(SystemExit, "STOP_V1_V2_PUBLICATION_TARGET_REFUSED"):
                stage1_freeze.validate_stage3_publication_prerequisites(
                    manifest_path=manifest,
                    receipt_path=receipt,
                    owner_authorization_path=owner,
                    output_path=stage1_freeze.ANCHOR_PATH,
                )
            wrong = json.loads(receipt.read_text(encoding="utf-8"))
            wrong["legacy_manifest"]["sha256"] = "0" * 64
            stage1_freeze.write_json(receipt, wrong)
            with self.assertRaisesRegex(SystemExit, "STOP_V3_MANIFEST_RECEIPT_HASH_MISMATCH"):
                stage1_freeze.validate_stage3_publication_prerequisites(
                    manifest_path=manifest,
                    receipt_path=receipt,
                    owner_authorization_path=owner,
                    output_path=root / "v3-anchor.json",
                )


if __name__ == "__main__":
    unittest.main(verbosity=2)
