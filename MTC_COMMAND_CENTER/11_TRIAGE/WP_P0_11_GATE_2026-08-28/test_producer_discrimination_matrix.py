from __future__ import annotations

import json
import sys
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path
from unittest.mock import patch


GATE_DIR = Path(__file__).resolve().parent
EVIDENCE_DIR = GATE_DIR / "evidence"
if str(EVIDENCE_DIR) not in sys.path:
    sys.path.insert(0, str(EVIDENCE_DIR))

import producer_discrimination_matrix as matrix_tool


class ProducerDiscriminationMatrixTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory(
            dir=Path(r"C:\tmp\N51_VARIANTS")
        )
        self.root = Path(self.temp.name)
        self.expected = self.root / "micro_expected.jsonl"
        representative_path = (
            GATE_DIR
            / "evidence"
            / "discrimination_matrix"
            / "representative_expected.jsonl"
        )
        first = json.loads(representative_path.read_text(encoding="utf-8"))
        second = deepcopy(first)
        second["bar_index"] = first["bar_index"] + 1
        second["timestamp"] = "2021-01-01T07:00:00+00:00"
        records = [first, second]
        self.expected.write_bytes(
            b"".join(matrix_tool.canonical_bytes(record) for record in records)
        )
        self.schema = self.root / "micro_schema.json"
        matrix_tool.write_json(
            self.schema,
            {
                "digest_catalog": {
                    "state_digest_components": [
                        "account.total_entries",
                        "events[*].reason",
                    ]
                },
                "field_catalog": [
                    {
                        "owning_record": "observation",
                        "path": "account.total_entries",
                        "type": "integer",
                    },
                    {
                        "owning_record": "event",
                        "path": "events[*].reason",
                        "type": "string",
                    },
                    {
                        "owning_record": "observation",
                        "path": "position.working_exits[*].never_present",
                        "type": "string",
                    },
                ]
            },
        )
        self.matrix_path, self.transcript_path = matrix_tool.build_matrix(
            expected_path=self.expected,
            schema_path=self.schema,
            output_dir=self.root / "output",
        )

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_scalar_wildcard_and_absent_paths_use_fresh_comparator_inputs(self) -> None:
        matrix = matrix_tool.load_json(self.matrix_path)
        by_path = {row["path"]: row for row in matrix["rows"]}
        scalar = by_path["account.total_entries"]
        self.assertEqual("DETECTED", scalar["status"])
        self.assertEqual(2, scalar["mutated_record_count"])
        self.assertEqual(2, scalar["changed_record_count"])
        self.assertEqual(1, scalar["return_code"])

        wildcard = by_path["events[*].reason"]
        self.assertEqual("DETECTED", wildcard["status"])
        self.assertEqual(2, wildcard["mutated_record_count"])
        self.assertEqual(2, wildcard["mutated_occurrence_count"])
        self.assertEqual(2, wildcard["changed_record_count"])

        absent = by_path["position.working_exits[*].never_present"]
        self.assertEqual("UNEXERCISED_ABSENT_IN_CORPUS", absent["status"])
        self.assertEqual(0, absent["changed_record_count"])
        self.assertEqual(0, absent["return_code"])
        self.assertEqual("STOP", matrix["outcome"])
        self.assertEqual(0, matrix["writer_integrity_restoration"]["closure_credit"])
        self.assertEqual(
            "NON_INDEPENDENT_WRITER_INTEGRITY_ONLY",
            matrix["writer_integrity_restoration"]["independence"],
        )
        self.assertEqual(
            "PASS",
            matrix_tool.validate_matrix_against_transcript(
                self.matrix_path, self.transcript_path
            )["outcome"],
        )

    def test_matrix_only_count_tamper_is_detected_against_transcript(self) -> None:
        matrix = matrix_tool.load_json(self.matrix_path)
        matrix["rows"][0]["changed_record_count"] += 1
        tampered = self.root / "tampered_count.json"
        matrix_tool.write_json(tampered, matrix)
        with self.assertRaisesRegex(
            matrix_tool.MatrixEvidenceError, "claim differs from transcript"
        ):
            matrix_tool.validate_matrix_against_transcript(
                tampered, self.transcript_path
            )
        with patch.object(matrix_tool.p011_gate, "SCHEMA_PATH", self.schema):
            with self.assertRaisesRegex(
                matrix_tool.p011_gate.GateFail, "claim differs from transcript"
            ):
                matrix_tool.p011_gate.validate_stage3_matrix_transcript(
                    tampered, self.transcript_path
                )

    def test_absent_list_and_wrong_outcome_tampers_are_detected(self) -> None:
        matrix = matrix_tool.load_json(self.matrix_path)
        absent_tamper = deepcopy(matrix)
        absent_tamper["absent_paths"] = []
        absent_path = self.root / "tampered_absent.json"
        matrix_tool.write_json(absent_path, absent_tamper)
        with self.assertRaisesRegex(matrix_tool.MatrixEvidenceError, "absent list"):
            matrix_tool.validate_matrix_against_transcript(
                absent_path, self.transcript_path
            )
        with patch.object(matrix_tool.p011_gate, "SCHEMA_PATH", self.schema):
            with self.assertRaisesRegex(matrix_tool.p011_gate.GateFail, "absent list"):
                matrix_tool.p011_gate.validate_stage3_matrix_transcript(
                    absent_path, self.transcript_path
                )

        outcome_tamper = deepcopy(matrix)
        outcome_tamper["outcome"] = "PASS"
        outcome_path = self.root / "tampered_outcome.json"
        matrix_tool.write_json(outcome_path, outcome_tamper)
        with self.assertRaisesRegex(matrix_tool.MatrixEvidenceError, "outcome"):
            matrix_tool.validate_matrix_against_transcript(
                outcome_path, self.transcript_path
            )
        with patch.object(matrix_tool.p011_gate, "SCHEMA_PATH", self.schema):
            with self.assertRaisesRegex(matrix_tool.p011_gate.GateFail, "outcome"):
                matrix_tool.p011_gate.validate_stage3_matrix_transcript(
                    outcome_path, self.transcript_path
                )


if __name__ == "__main__":
    unittest.main(verbosity=2)
