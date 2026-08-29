from __future__ import annotations

import hashlib
import io
import json
import os
import re
import tempfile
import unittest
from contextlib import redirect_stdout
from copy import deepcopy
from pathlib import Path
from unittest.mock import patch

import p011_gate
import row_arm
from scenario_binding import (
    EXPECTED_ROW_POSITIONS,
    ManifestRowError,
    ManifestScenarioSource,
    ScenarioShapeError,
    bind_scenario,
    lookup_manifest_row,
    manifest_scenario,
    verifier_scenario_contract,
)


GATE_DIR = Path(__file__).resolve().parent
MANIFEST_PATH = GATE_DIR / "p011_legacy_manifest.json"
_VARIANT_TEMP = tempfile.TemporaryDirectory(prefix="p011_n28_")
VARIANT_DIR = Path(_VARIANT_TEMP.name)
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
NARROWED_FINALIZER_STATUS = (
    "SHAPE_AND_IDENTITY_ACCEPTED; producer execution NOT verified by this gate"
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


def _write_result(name: str, value: dict | list) -> Path:
    VARIANT_DIR.mkdir(parents=True, exist_ok=True)
    path = VARIANT_DIR / name
    path.write_text(
        json.dumps(value, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return path


def _write_n33_json(relative_path: str, value: dict | list) -> Path:
    variant_root = Path(os.environ.get("P011_N33_VARIANT_DIR", str(VARIANT_DIR)))
    path = variant_root / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return path


def _scenario_for(manifest: dict, row_id: str) -> dict:
    scenario = manifest_scenario(
        ManifestScenarioSource(
            manifest=manifest,
            row_id=row_id,
            expected_position=EXPECTED_ROW_POSITIONS[row_id],
        )
    )
    if type(scenario) is not dict:
        raise AssertionError(f"{row_id} scenario is not mutable")
    return scenario


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
        lookup_manifest_row(duplicate, "C02", EXPECTED_ROW_POSITIONS["C02"])["row_id"] = "C01"
        with self.assertRaisesRegex(ManifestRowError, "duplicated"):
            lookup_manifest_row(duplicate, "C01")
        reordered = deepcopy(manifest)
        rows_by_id = {row["row_id"]: row for row in reordered["rows"]}
        swapped_ids = ["C02", "C01", *[f"C{index:02d}" for index in range(3, 43)]]
        reordered["rows"] = [rows_by_id[row_id] for row_id in swapped_ids]
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
    def _write_finalizer_input(
        self,
        name: str,
        *,
        empty_artifact: str | None = None,
        empty_json_artifact: str | None = None,
    ) -> Path:
        caller_input = VARIANT_DIR / name
        caller_input.mkdir(parents=True, exist_ok=True)
        baseline = {
            "adapters": {
                "observation_adapter": {
                    "binding": "test fixture",
                    "sha256": p011_gate.sha256_file(Path(p011_gate.__file__)),
                }
            },
            "conservation": {"total_records": 1},
            "source": {"resolved_import_bindings": []},
        }
        values = {
            "baseline_manifest.json": p011_gate.canonical_bytes(baseline),
            "final_states.json": p011_gate.canonical_bytes({"profile": {"state": "present"}}),
            "mtc_v2_legacy_sequence.jsonl": b"{}\n",
            "row_corroboration.json": p011_gate.canonical_bytes({"rows": [{"row_id": "C01"}]}),
        }
        for artifact, value in values.items():
            if artifact == empty_artifact:
                value = b""
            elif artifact == empty_json_artifact:
                value = b"{}\n"
            (caller_input / artifact).write_bytes(value)
        return caller_input

    def _invoke_finalizer(
        self,
        caller_input_1: Path,
        caller_input_2: Path,
        matrix_path: Path,
        *,
        schema_path: Path | None = None,
    ) -> int:
        anchor = json.loads(p011_gate.ANCHOR_PATH.read_text(encoding="utf-8"))
        anchor["legacy_manifest_sha256"] = p011_gate.sha256_file(
            p011_gate.GATE_DIR / "p011_legacy_manifest.json"
        )
        anchor_path = _write_n33_json("finalizer/copied_anchor.json", anchor)
        captured_writes: dict[Path, dict] = {}

        def capture_write(path: Path, value: dict) -> None:
            captured_writes[path] = deepcopy(value)

        stdout = io.StringIO()
        with (
            patch.object(p011_gate, "ANCHOR_PATH", anchor_path),
            patch.object(p011_gate, "SCHEMA_PATH", schema_path or p011_gate.SCHEMA_PATH),
            patch.object(
                p011_gate,
                "row_arm_receipt",
                return_value={
                    "counts": {"green": 27, "not_applicable": 2, "stop": 13, "total": 42},
                    "outcome": "STOP",
                    "reason": "test fixture",
                },
            ),
            patch.object(p011_gate, "write_json", side_effect=capture_write),
            redirect_stdout(stdout),
        ):
            return_code = p011_gate.command_finalize_candidate(
                type(
                    "Args",
                    (),
                    {
                        "caller_input_1": str(caller_input_1),
                        "caller_input_2": str(caller_input_2),
                        "mutation_matrix": str(matrix_path),
                    },
                )()
            )
        self.finalizer_output = json.loads(stdout.getvalue())
        self.finalizer_writes = captured_writes
        return return_code

    def _assert_narrowed_finalizer_status(self) -> None:
        self.assertEqual(NARROWED_FINALIZER_STATUS, self.finalizer_output["outcome"])
        self.assertEqual("STOP", self.finalizer_output["full_gate_outcome"])
        receipt = next(
            value
            for path, value in self.finalizer_writes.items()
            if path.name == "P011_GATE_RECEIPT.json"
        )
        anchor = next(
            value
            for path, value in self.finalizer_writes.items()
            if path.name == "copied_anchor.json"
        )
        self.assertEqual(NARROWED_FINALIZER_STATUS, receipt["receipt_state"])
        self.assertEqual(
            NARROWED_FINALIZER_STATUS,
            receipt["producer_and_adapter_bindings"]["baseline_generator"]["status"],
        )
        self.assertEqual(
            NARROWED_FINALIZER_STATUS,
            receipt["producer_and_adapter_bindings"]["a_observation_adapter"]["status"],
        )
        self.assertEqual(NARROWED_FINALIZER_STATUS, receipt["baseline_outputs"]["status"])
        comparison = receipt["baseline_outputs"]["caller_supplied_byte_comparison"]
        self.assertEqual(
            {"caller_input_1", "caller_input_2", "byte_identical", "artifacts"},
            set(comparison),
        )
        for artifact in comparison["artifacts"]:
            self.assertEqual(
                {"artifact", "caller_input_1_sha256", "caller_input_2_sha256"},
                set(artifact),
            )
        self.assertTrue(comparison["byte_identical"])
        self.assertEqual(NARROWED_FINALIZER_STATUS, anchor["freeze_state"])

    def test_caller_input_flags_bind_honest_names_and_legacy_flags_are_absent(self) -> None:
        parser = p011_gate.build_parser()
        args = parser.parse_args(
            [
                "finalize-candidate",
                "--caller-input-1",
                "first",
                "--caller-input-2",
                "second",
                "--mutation-matrix",
                "matrix.json",
            ]
        )
        self.assertEqual("first", args.caller_input_1)
        self.assertEqual("second", args.caller_input_2)
        self.assertFalse(hasattr(args, "run" + "1"))
        self.assertFalse(hasattr(args, "run" + "2"))
        comparison_args = parser.parse_args(
            [
                "verify-caller-supplied-byte-comparison",
                "--caller-input-1",
                "first",
                "--caller-input-2",
                "second",
            ]
        )
        self.assertEqual("first", comparison_args.caller_input_1)
        self.assertEqual("second", comparison_args.caller_input_2)
        command_action = next(action for action in parser._actions if action.dest == "command")
        for command in ("finalize-candidate", "verify-caller-supplied-byte-comparison"):
            option_strings = {
                option
                for action in command_action.choices[command]._actions
                for option in action.option_strings
            }
            self.assertNotIn("--" + "run" + "1", option_strings)
            self.assertNotIn("--" + "run" + "2", option_strings)

    def test_finalize_candidate_refuses_zero_row_and_schema_short_matrix(self) -> None:
        caller_input_1 = self._write_finalizer_input("finalizer/matrix_input_1")
        caller_input_2 = self._write_finalizer_input("finalizer/matrix_input_2")
        matrix = json.loads(
            (
                p011_gate.GATE_DIR
                / "evidence"
                / "discrimination_matrix"
                / "discrimination_matrix.json"
            ).read_text(encoding="utf-8")
        )

        zero_matrix = {
            "digest_component_count": 0,
            "event_component_count": 0,
            "matrix_row_count": 0,
            "outcome": "PASS",
            "red_count": 0,
            "restored_green_count": 0,
            "rows": [],
        }
        zero_path = _write_n33_json("finalizer/zero_matrix.json", zero_matrix)
        with self.assertRaisesRegex(p011_gate.GateStop, "matrix.*rows"):
            self._invoke_finalizer(caller_input_1, caller_input_2, zero_path)

        short_matrix = deepcopy(matrix)
        short_matrix["catalog_field_count"] -= 1
        short_matrix["matrix_row_count"] -= 1
        short_matrix["red_count"] -= 1
        short_matrix["restored_green_count"] -= 1
        short_matrix["rows"] = short_matrix["rows"][:-1]
        short_path = _write_n33_json("finalizer/schema_short_matrix.json", short_matrix)
        with self.assertRaisesRegex(p011_gate.GateStop, "observation-schema field catalog"):
            self._invoke_finalizer(caller_input_1, caller_input_2, short_path)

        empty_catalog_schema = json.loads(p011_gate.SCHEMA_PATH.read_text(encoding="utf-8"))
        empty_catalog_schema["field_catalog"] = []
        empty_catalog_schema_path = _write_n33_json(
            "finalizer/empty_catalog_schema.json", empty_catalog_schema
        )
        with self.assertRaisesRegex(p011_gate.GateStop, "schema field catalog is absent"):
            self._invoke_finalizer(
                caller_input_1,
                caller_input_2,
                p011_gate.GATE_DIR
                / "evidence"
                / "discrimination_matrix"
                / "discrimination_matrix.json",
                schema_path=empty_catalog_schema_path,
            )

        invalid_path_matrix = deepcopy(matrix)
        invalid_path_matrix["rows"][0]["stable_field_component_path"] = "wrong.path"
        invalid_path = _write_n33_json(
            "finalizer/invalid_path_matrix.json", invalid_path_matrix
        )
        with self.assertRaisesRegex(p011_gate.GateStop, "row paths differ"):
            self._invoke_finalizer(caller_input_1, caller_input_2, invalid_path)

        for section, return_code, reason in (
            ("red", 0, "RED return-code declarations"),
            ("restoration", 1, "restoration return-code declarations"),
        ):
            with self.subTest(section=section):
                invalid_evidence = deepcopy(matrix)
                invalid_evidence["rows"][0][section]["return_code"] = return_code
                invalid_path = _write_n33_json(
                    f"finalizer/invalid_{section}_matrix.json", invalid_evidence
                )
                with self.assertRaisesRegex(p011_gate.GateStop, reason):
                    self._invoke_finalizer(caller_input_1, caller_input_2, invalid_path)

        invalid_component_count = deepcopy(matrix)
        invalid_component_count["digest_component_count"] -= 1
        invalid_component_path = _write_n33_json(
            "finalizer/invalid_digest_count_matrix.json", invalid_component_count
        )
        with self.assertRaisesRegex(p011_gate.GateStop, "digest-component count"):
            self._invoke_finalizer(caller_input_1, caller_input_2, invalid_component_path)

        invalid_digest_row = deepcopy(matrix)
        digest_row = next(row for row in invalid_digest_row["rows"] if row["digest_component"])
        digest_row["digest_component"] = False
        invalid_digest_row_path = _write_n33_json(
            "finalizer/invalid_digest_row_matrix.json", invalid_digest_row
        )
        with self.assertRaisesRegex(p011_gate.GateStop, "digest-component path set"):
            self._invoke_finalizer(caller_input_1, caller_input_2, invalid_digest_row_path)

        moved_digest_row = deepcopy(matrix)
        digest_row = next(row for row in moved_digest_row["rows"] if row["digest_component"])
        non_digest_row = next(
            row for row in moved_digest_row["rows"] if not row["digest_component"]
        )
        digest_row["digest_component"] = False
        non_digest_row["digest_component"] = True
        moved_digest_row_path = _write_n33_json(
            "finalizer/moved_digest_row_matrix.json", moved_digest_row
        )
        with self.assertRaisesRegex(p011_gate.GateStop, "digest-component path set"):
            self._invoke_finalizer(caller_input_1, caller_input_2, moved_digest_row_path)

        scalar_variants = (
            ("matrix_row_count", matrix["matrix_row_count"] - 1, "declared row count"),
            ("catalog_field_count", matrix["catalog_field_count"] - 1, "declared catalog count"),
            ("schema_sha256", "0" * 64, "schema pin differs"),
            ("event_component_count", matrix["event_component_count"] - 1, "event-component count"),
            (
                "red_count",
                matrix["red_count"] - 1,
                "declared RED return-code count",
            ),
            (
                "restored_green_count",
                matrix["restored_green_count"] - 1,
                "declared restoration return-code count",
            ),
            ("outcome", "STOP", "declared outcome/failures"),
            ("failures", ["FIELD-001"], "declared outcome/failures"),
        )
        for field, value, reason in scalar_variants:
            with self.subTest(field=field):
                invalid_matrix = deepcopy(matrix)
                invalid_matrix[field] = value
                invalid_path = _write_n33_json(
                    f"finalizer/invalid_{field}_matrix.json", invalid_matrix
                )
                with self.assertRaisesRegex(p011_gate.GateStop, reason):
                    self._invoke_finalizer(caller_input_1, caller_input_2, invalid_path)

        green_path = (
            p011_gate.GATE_DIR
            / "evidence"
            / "discrimination_matrix"
            / "discrimination_matrix.json"
        )
        self.assertEqual(
            0,
            self._invoke_finalizer(caller_input_1, caller_input_2, green_path),
        )
        self._assert_narrowed_finalizer_status()

    def test_finalize_candidate_narrows_acceptance_without_producer_execution(self) -> None:
        caller_input_1 = self._write_finalizer_input("finalizer/narrowed_input_1")
        caller_input_2 = self._write_finalizer_input("finalizer/narrowed_input_2")
        matrix = json.loads(
            (
                p011_gate.GATE_DIR
                / "evidence"
                / "discrimination_matrix"
                / "discrimination_matrix.json"
            ).read_text(encoding="utf-8")
        )
        shared_output = {
            "command_argv": ["test", "no-producer-executed"],
            "evidence_sha256": "0" * 64,
            "stderr": "",
            "stdout": "IDENTICAL_NO_EXECUTION_OUTPUT",
        }
        for row in matrix["rows"]:
            row["matrix_id"] = "FIELD-001"
            row["owning_record_or_digest"] = "NO_PRODUCER_EXECUTED"
            row["actual_changed_record_count"] = 0
            row["expected_changed_record_count"] = 0
            row["failing_record_keys"] = []
            row["mutation"]["after"] = row["mutation"]["before"]
            row["red"] = {**shared_output, "return_code": 1}
            row["restoration"] = {**shared_output, "return_code": 0}
        matrix_path = _write_n33_json("finalizer/no_producer_execution.json", matrix)

        self.assertEqual(
            0,
            self._invoke_finalizer(caller_input_1, caller_input_2, matrix_path),
        )
        self._assert_narrowed_finalizer_status()

    def test_finalize_candidate_refuses_each_empty_build_artifact(self) -> None:
        matrix_path = (
            p011_gate.GATE_DIR
            / "evidence"
            / "discrimination_matrix"
            / "discrimination_matrix.json"
        )
        artifacts = (
            "baseline_manifest.json",
            "final_states.json",
            "mtc_v2_legacy_sequence.jsonl",
            "row_corroboration.json",
        )
        for index, artifact in enumerate(artifacts):
            with self.subTest(artifact=artifact):
                caller_input_1 = self._write_finalizer_input(
                    f"finalizer/empty_{index}_input_1", empty_artifact=artifact
                )
                caller_input_2 = self._write_finalizer_input(
                    f"finalizer/empty_{index}_input_2", empty_artifact=artifact
                )
                with self.assertRaisesRegex(p011_gate.GateStop, "artifact is empty"):
                    self._invoke_finalizer(caller_input_1, caller_input_2, matrix_path)

        for index, artifact in enumerate(
            ("baseline_manifest.json", "final_states.json", "row_corroboration.json")
        ):
            with self.subTest(logically_empty=artifact):
                caller_input_1 = self._write_finalizer_input(
                    f"finalizer/logical_empty_{index}_input_1", empty_json_artifact=artifact
                )
                caller_input_2 = self._write_finalizer_input(
                    f"finalizer/logical_empty_{index}_input_2", empty_json_artifact=artifact
                )
                with self.assertRaisesRegex(p011_gate.GateStop, "artifact is empty"):
                    self._invoke_finalizer(caller_input_1, caller_input_2, matrix_path)

    def test_row_corroboration_reason_uses_present_row_counts(self) -> None:
        manifest = _load_manifest()
        policy_row = next(
            row
            for row in manifest["rows"]
            if row["disposition"] == "NOT_A_LEGACY_REPRODUCTION_ROW"
        )
        result = p011_gate.build_row_corroboration({"rows": [deepcopy(policy_row)]})
        self.assertEqual(
            "0 direct-build producer adapters and their D026 mutations are frozen but not executed "
            "by this sequence builder; 1 policy-only row; 1 row total",
            result["reason"],
        )

    def test_missing_receipt_pin_sha256_is_row_fail(self) -> None:
        base_receipt = json.loads(row_arm.RECEIPT_PATH.read_text(encoding="utf-8"))
        cases = (
            ("legacy_manifest", "receipt legacy-manifest pin differs"),
            ("observation_schema", "receipt observation-schema pin differs"),
        )
        for index, (section, reason) in enumerate(cases):
            with self.subTest(section=section):
                receipt = deepcopy(base_receipt)
                receipt["legacy_manifest"]["sha256"] = row_arm.sha256_file(row_arm.MANIFEST_PATH)
                receipt["observation_schema"]["sha256"] = row_arm.sha256_file(row_arm.SCHEMA_PATH)
                receipt[section].pop("sha256")
                receipt_path = _write_n33_json(f"missing_pin_{index}/receipt.json", receipt)

                anchor = json.loads(row_arm.ANCHOR_PATH.read_text(encoding="utf-8"))
                anchor["legacy_manifest_sha256"] = row_arm.sha256_file(row_arm.MANIFEST_PATH)
                anchor["receipt_sha256"] = row_arm.sha256_file(receipt_path)
                anchor_path = _write_n33_json(f"missing_pin_{index}/anchor.json", anchor)
                with (
                    patch.object(row_arm, "ANCHOR_PATH", anchor_path),
                    patch.object(row_arm, "RECEIPT_PATH", receipt_path),
                ):
                    with self.assertRaisesRegex(row_arm.RowFail, reason):
                        row_arm.validate_frozen_inputs()

    def test_copied_anchor_repin_cannot_authorize_receipt_manifest_mismatch(self) -> None:
        anchor = json.loads(row_arm.ANCHOR_PATH.read_text(encoding="utf-8"))
        anchor["legacy_manifest_sha256"] = row_arm.sha256_file(row_arm.MANIFEST_PATH)
        anchor_path = _write_n33_json("anchor_repin_only.json", anchor)

        with patch.object(row_arm, "ANCHOR_PATH", anchor_path):
            with self.assertRaisesRegex(
                row_arm.RowFail, "receipt legacy-manifest pin differs"
            ) as raised:
                row_arm.validate_frozen_inputs()

        _write_n33_json(
            "anchor_repin_only_refusal.json",
            {
                "outcome": "REFUSED",
                "reason": str(raised.exception),
                "variant": str(anchor_path),
            },
        )

    def test_copied_receipt_schema_pin_mismatch_is_refused(self) -> None:
        receipt = json.loads(row_arm.RECEIPT_PATH.read_text(encoding="utf-8"))
        receipt["legacy_manifest"]["sha256"] = row_arm.sha256_file(
            row_arm.MANIFEST_PATH
        )
        receipt["observation_schema"]["sha256"] = "0" * 64
        receipt_path = _write_n33_json("receipt_wrong_schema_pin.json", receipt)

        anchor = json.loads(row_arm.ANCHOR_PATH.read_text(encoding="utf-8"))
        anchor["legacy_manifest_sha256"] = row_arm.sha256_file(row_arm.MANIFEST_PATH)
        anchor["receipt_sha256"] = row_arm.sha256_file(receipt_path)
        anchor_path = _write_n33_json("anchor_for_wrong_schema_receipt.json", anchor)

        with (
            patch.object(row_arm, "ANCHOR_PATH", anchor_path),
            patch.object(row_arm, "RECEIPT_PATH", receipt_path),
        ):
            with self.assertRaisesRegex(
                row_arm.RowFail, "receipt observation-schema pin differs"
            ) as raised:
                row_arm.validate_frozen_inputs()

        _write_n33_json(
            "wrong_schema_pin_refusal.json",
            {
                "outcome": "REFUSED",
                "reason": str(raised.exception),
                "variant": str(receipt_path),
            },
        )

    def test_row_arm_receipt_claims_only_counts_and_refuses_count_variant(self) -> None:
        evidence = {
            "counts": {"green": 27, "not_applicable": 2, "stop": 13, "total": 42},
            "gate_version": p011_gate.GATE_VERSION,
            "outcome": "STOP",
        }
        evidence_path = _write_n33_json(
            "counts_only/evidence/row_arm/row_corroboration.json", evidence
        )
        counts_root = evidence_path.parents[2]
        with patch.object(p011_gate, "GATE_DIR", counts_root):
            result = p011_gate.row_arm_receipt()
        self.assertEqual(
            "accepted summary counts are 27 GREEN, 13 STOP, 2 policy-only, 42 total",
            result["reason"],
        )

        evidence["counts"]["green"] = 26
        _write_n33_json(
            "counts_only/evidence/row_arm/row_corroboration.json", evidence
        )
        with patch.object(p011_gate, "GATE_DIR", counts_root):
            with self.assertRaisesRegex(
                p011_gate.GateStop, "does not carry the current"
            ) as raised:
                p011_gate.row_arm_receipt()
        _write_n33_json(
            "counts_only_refusal.json",
            {
                "input": str(evidence_path),
                "outcome": "REFUSED",
                "reason": str(raised.exception),
            },
        )

    def test_compare_exact_reports_actual_expected_leaf_visits(self) -> None:
        visited: list[str] = []
        mismatches = row_arm.compare_exact(
            {"kept": 1, "missing": {"nested": 2}},
            {"kept": 1},
            expected_leaf_paths_visited=visited,
        )
        self.assertEqual(["$.kept"], visited)
        self.assertEqual("missing", mismatches[0]["reason"])

    def test_rule2_a_junk_manifest_value_is_refused(self) -> None:
        manifest = _load_manifest()
        scenario = _scenario_for(manifest, "C01")
        scenario["literal_expected_observation"] = {"junk": "NOT_THE_VERIFIER_LITERAL"}
        path = _write_variant("rule2_a_junk_manifest.json", manifest)
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        with patch.object(p011_gate, "run_profile") as run_profile_spy:
            with self.assertRaises(p011_gate.GateStop) as raised:
                p011_gate.validate_legacy_manifest(path, digest)
        output = {
            "check": "manifest scenario vs verifier-owned scenario contract",
            "input": {
                "literal_expected_observation": scenario["literal_expected_observation"],
                "variant": str(path),
            },
            "outcome": "REFUSED",
            "producer_executed": run_profile_spy.called,
            "reason": str(raised.exception),
        }
        _write_result("rule2_a_output.json", output)
        self.assertFalse(run_profile_spy.called)

    def test_rule2_b_wrong_observed_authority_stops_exact_set_match(self) -> None:
        binding = row_arm.validate_contract_binding(
            _load_manifest(), row_arm.ROW_CONTRACTS["C01"]
        )
        observation = row_arm.authority_execution_observation(
            [{"module": "src.engine", "path": "src/engine.py"}],
            method="RUNTIME_MODULES_RESOLVED_UNDER_BOUND_AUTHORITY_ROOT_V1",
            reason="RULE 2 probe supplied a B runtime import to an A-only row",
        )
        output = row_arm.consume_authority_execution(binding, observation)
        clean_observation = row_arm.authority_execution_observation(
            [{"module": "mtc_v2.core.runner", "path": "mtc_v2/core/runner.py"}],
            method="RUNTIME_MODULES_RESOLVED_UNDER_BOUND_AUTHORITY_ROOT_V1",
            reason="RULE 2 clean-side observation",
        )
        with self.assertRaises(row_arm.RowStop) as raised:
            row_arm.require_same_authority_names(
                observation, clean_observation, "C01"
            )
        _write_result(
            "rule2_b_output.json",
            {
                "check": "declared authority set vs runtime import observation",
                "output": output,
                "red_green_consistency_probe": {
                    "clean_actual_authority_names": clean_observation[
                        "actual_authority_names"
                    ],
                    "mutant_actual_authority_names": observation[
                        "actual_authority_names"
                    ],
                    "outcome": "REFUSED",
                    "reason": str(raised.exception),
                },
            },
        )
        self.assertFalse(output["exact_set_match"])
        self.assertEqual(["A_CURRENT_MASTER"], output["missing"])
        self.assertEqual(["B_BACKTEST_FREEZE"], output["unexpected"])

    def test_eighteen_missing_key_variants_refuse_before_producer(self) -> None:
        results: list[dict] = []
        with patch.object(p011_gate, "run_profile") as run_profile_spy:
            for key in REQUIRED_VARIANT_KEYS:
                for with_extra in (False, True):
                    manifest = _load_manifest()
                    scenario = _scenario_for(manifest, "C01")
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
        _write_result("section2_results.json", results)
        self.assertEqual(18, len(results))
        self.assertTrue(all(item["outcome"] == "REFUSED" for item in results))
        self.assertFalse(any(item["producer_executed"] for item in results))

    def test_wrong_mutation_mismatch_path_is_refused(self) -> None:
        binding = row_arm.validate_contract_binding(
            _load_manifest(), row_arm.ROW_CONTRACTS["C01"]
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
        with self.assertRaisesRegex(row_arm.RowStop, "required RED predicate"):
            row_arm.consume_producer_mutation_red(binding, wrong_red)

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

    def test_sequence_builder_publishes_no_unexecuted_consumption_claim(self) -> None:
        corroboration = p011_gate.build_row_corroboration(_load_manifest())
        applicable = [
            row for row in corroboration["rows"] if row["status"] == "STOP"
        ]
        self.assertEqual(40, len(applicable))
        self.assertFalse(any("contract_consumption" in row for row in applicable))

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
            for row in manifest["rows"]:
                if row["disposition"] != "APPLICABLE":
                    continue
                row_id = row["row_id"]
                binding = bind_scenario(
                    _scenario_for(manifest, row_id), verifier_scenario_contract(row_id)
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
                        scenario = _scenario_for(changed, row_id)
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

        _write_result("leaf_variant_matrix.json", matrix)
        expected_variants = sum(
            len(
                bind_scenario(
                    _scenario_for(manifest, row["row_id"]),
                    verifier_scenario_contract(row["row_id"]),
                ).declared_leaves
            )
            for row in manifest["rows"]
            if row["disposition"] == "APPLICABLE"
        ) * 3
        self.assertEqual(expected_variants, len(matrix))
        self.assertFalse(any(item["producer_executed"] for item in matrix))

    def test_reordered_rows_are_refused(self) -> None:
        manifest = _load_manifest()
        rows_by_id = {row["row_id"]: row for row in manifest["rows"]}
        swapped_ids = ["C02", "C01", *[f"C{index:02d}" for index in range(3, 43)]]
        manifest["rows"] = [rows_by_id[row_id] for row_id in swapped_ids]
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
        _write_result("section4b_result.json", result)

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
        _write_result("section3_result.json", result)

    def test_unresolved_authority_observations_name_the_execution_path(self) -> None:
        records = row_arm.build_unresolved_records(_load_manifest())
        by_row = {item["row_id"]: item for item in records}
        c28 = by_row["C28"]["authority_execution"]
        self.assertEqual([], c28["actual_authority_names"])
        self.assertEqual([], c28["observation"]["runtime_imports"])
        self.assertEqual(
            "NO_PRODUCER_CALL_NO_RESOLUTION_PERFORMED",
            c28["observation"]["method"],
        )
        self.assertIn("no producer call occurred", c28["observation"]["reason"])
        c32 = by_row["C32"]["authority_execution"]
        self.assertEqual(["A_CURRENT_MASTER"], c32["actual_authority_names"])
        self.assertTrue(c32["observation"]["runtime_imports"])
        self.assertEqual(
            "RUNTIME_MODULES_RESOLVED_UNDER_BOUND_AUTHORITY_ROOT_V1",
            c32["observation"]["method"],
        )
        self.assertIn("probe returned after importing", c32["observation"]["reason"])


def tearDownModule() -> None:
    _VARIANT_TEMP.cleanup()


if __name__ == "__main__":
    unittest.main(verbosity=2)
