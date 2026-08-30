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
    BLOCKED_BY_DESIGN,
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

    def test_copied_pre_fix_contracts_are_refused_by_binding(self) -> None:
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

    def test_c42_pinned_seams_do_not_claim_sequence_extraction(self) -> None:
        source = row_arm.c42_source_correspondence_evidence()
        self.assertFalse(source["satisfied"])
        self.assertTrue(source["clean"]["pinned_canonical_seams_present"])
        self.assertFalse(source["clean"]["source_sequence_extracted"])
        self.assertEqual("DETECTED", source["modified_copy_disposition"])
        self.assertEqual(0, source["restoration"]["closure_credit"])
        b_boundary = row_arm.c42_b_configuration_discriminator()
        self.assertTrue(b_boundary["boundary_observed"])
        self.assertTrue(b_boundary["refused"])
        self.assertEqual("REFUSED", b_boundary["outcome"])

    def test_c42_unavailable_b_boundary_is_not_observed(self) -> None:
        completed = __import__("subprocess").CompletedProcess(
            args=[], returncode=7, stdout="", stderr="boundary unavailable"
        )
        with (
            patch.object(row_arm, "_materialize_prefix", return_value=[]),
            patch.object(row_arm.subprocess, "run", return_value=completed),
        ):
            result = row_arm.c42_b_configuration_discriminator()
        self.assertFalse(result["boundary_observed"])
        self.assertFalse(result["refused"])
        self.assertEqual("NOT_OBSERVED", result["outcome"])

    def test_desktop_rows_declare_blocked_mode(self) -> None:
        for row_id in ("C28", "C29", "C30"):
            scenario = self.rows[row_id]["scenarios"][0]
            requirements = scenario["clean_producer_corroboration"][
                "authority_requirements"
            ]
            self.assertEqual(BLOCKED_BY_DESIGN, requirements[0]["evidence_mode"])

    def test_finalizer_authority_disposition_variants_are_refused(self) -> None:
        requirements = [
            item.as_mapping()
            for item in verifier_scenario_contract(
                "C42", stage3=True
            ).clean_producer_corroboration.authority_requirements
        ]
        accounting = {
            "complete": True,
            "exact_set_match": True,
            "satisfied": True,
            "terminal_dispositions": [
                {
                    "authority_name": "A_CURRENT_MASTER",
                    "evidence_mode": EXECUTION_OBSERVATION,
                    "disposition": "EXECUTED",
                },
                {
                    "authority_name": "PINE_CURRENT_MASTER",
                    "evidence_mode": SOURCE_CORROBORATION,
                    "disposition": "SOURCE_CORROBORATED",
                },
            ],
        }
        record = {"authority_execution": accounting}
        p011_gate = __import__("p011_gate")
        p011_gate._validate_final_authority_dispositions(
            row_id="C42",
            terminal_status="GREEN",
            record=record,
            requirements=requirements,
        )
        variants = []
        missing = deepcopy(accounting)
        missing["terminal_dispositions"] = missing["terminal_dispositions"][:1]
        variants.append(
            (
                "missing",
                missing,
                "STOP_AUTHORITY_EVIDENCE_INCOMPLETE: C42",
            )
        )
        duplicate = deepcopy(accounting)
        duplicate["terminal_dispositions"].append(
            deepcopy(duplicate["terminal_dispositions"][0])
        )
        variants.append(
            (
                "duplicate",
                duplicate,
                "STOP_AUTHORITY_EVIDENCE_INCOMPLETE: C42",
            )
        )
        incompatible = deepcopy(accounting)
        incompatible["terminal_dispositions"][0][
            "disposition"
        ] = "SOURCE_CORROBORATED"
        variants.append(
            (
                "incompatible",
                incompatible,
                "STOP_AUTHORITY_EXECUTION_DISPOSITION_INCOMPATIBLE: C42",
            )
        )
        for variant_name, variant, expected_reason in variants:
            with self.subTest(variant=variant_name):
                with self.assertRaises(p011_gate.GateStop) as raised:
                    p011_gate._validate_final_authority_dispositions(
                        row_id="C42",
                        terminal_status="GREEN",
                        record={"authority_execution": variant},
                        requirements=requirements,
                    )
                self.assertEqual(expected_reason, str(raised.exception))


class Stage3PublicationBoundaryTests(unittest.TestCase):
    def test_candidate_generation_writes_requested_scratch_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            output = root / "candidate.json"
            args = type(
                "Args", (), {"out": str(output), "scratch_root": str(root)}
            )()
            self.assertEqual(0, stage1_freeze.command_candidate_manifest(args))
            self.assertEqual(stage1_freeze.STAGE3_GATE_VERSION, json.loads(output.read_text(encoding="utf-8"))["gate_version"])

    def test_publication_refuses_absent_authorization_file_v1_v2_and_hash_mismatch(self) -> None:
        with tempfile.TemporaryDirectory() as name:
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
                    authorization_file_path=root / "absent-authorization-file.md",
                    output_path=root / "v3-anchor.json",
                )
            authorization_file = root / "authorization-file.md"
            authorization_file.write_text(
                "authorization file presence fixture", encoding="utf-8"
            )
            with self.assertRaisesRegex(SystemExit, "STOP_V1_V2_PUBLICATION_TARGET_REFUSED"):
                stage1_freeze.validate_stage3_publication_prerequisites(
                    manifest_path=manifest,
                    receipt_path=receipt,
                    authorization_file_path=authorization_file,
                    output_path=stage1_freeze.ANCHOR_PATH,
                )
            presence = stage1_freeze.validate_stage3_publication_prerequisites(
                manifest_path=manifest,
                receipt_path=receipt,
                authorization_file_path=authorization_file,
                output_path=root / "v3-anchor.json",
            )
            self.assertEqual(
                "P011_V3_PREREQUISITE_FILE_PRESENCE_v1",
                presence["anchor_schema_version"],
            )
            self.assertNotIn("signature_basis", presence)
            wrong = json.loads(receipt.read_text(encoding="utf-8"))
            wrong["legacy_manifest"]["sha256"] = "0" * 64
            stage1_freeze.write_json(receipt, wrong)
            with self.assertRaisesRegex(SystemExit, "STOP_V3_MANIFEST_RECEIPT_HASH_MISMATCH"):
                stage1_freeze.validate_stage3_publication_prerequisites(
                    manifest_path=manifest,
                    receipt_path=receipt,
                    authorization_file_path=authorization_file,
                    output_path=root / "v3-anchor.json",
                )


if __name__ == "__main__":
    unittest.main(verbosity=2)
