"""Regression tests for fail-closed strategy-registry promotion mapping."""

from __future__ import annotations

import importlib.util
import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "build_strategy_research_registry.py"
SPEC = importlib.util.spec_from_file_location("build_strategy_research_registry", MODULE_PATH)
assert SPEC and SPEC.loader
registry = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(registry)


class RegistryPromotionGuardTests(unittest.TestCase):
    def _build_entry(
        self,
        promotion_status: object = None,
        *,
        include_promotion_status: bool = True,
        yaml_text: str | None = None,
    ) -> tuple[dict, str]:
        with tempfile.TemporaryDirectory() as temp_dir:
            mcc_root = Path(temp_dir) / "MTC_COMMAND_CENTER"
            folder = (
                mcc_root
                / "03_QUANTLENS"
                / "strategies"
                / "STG999_registry_guard_fixture"
            )
            folder.mkdir(parents=True)
            producer_spec = {"candidate_id": "STG999"}
            if include_promotion_status:
                producer_spec["promotion_status"] = promotion_status
            (folder / "producer_spec.json").write_text(
                json.dumps(producer_spec), encoding="utf-8"
            )
            if yaml_text is not None:
                (folder / "01_candidate_metadata.yaml").write_text(
                    yaml_text, encoding="utf-8"
                )

            original_mcc_root = registry.MCC_ROOT
            output = io.StringIO()
            try:
                registry.MCC_ROOT = mcc_root
                with redirect_stdout(output):
                    entry = registry.build_strategy_entry(folder)
            finally:
                registry.MCC_ROOT = original_mcc_root
            return entry, output.getvalue()

    def test_unevaluated_forward_paper_is_refused(self) -> None:
        entry, output = self._build_entry(["FORWARD_PAPER_CANDIDATE"])

        self.assertEqual(entry["maturity_level"], "research_batch_only")
        self.assertEqual(entry["current_status"], "RESEARCH_BATCH")
        self.assertIn("STG999", output)
        self.assertIn("FORWARD_PAPER_CANDIDATE", output)

    def test_unevaluated_research_grade_is_refused(self) -> None:
        entry, output = self._build_entry(["RESEARCH_GRADE"])

        self.assertEqual(entry["maturity_level"], "research_batch_only")
        self.assertEqual(entry["current_status"], "RESEARCH_BATCH")
        self.assertNotIn("RESEARCH_GRADE", entry["current_status"])
        self.assertEqual(output.count("REFUSED"), 1)

    def test_robust_candidate_is_refused(self) -> None:
        entry, output = self._build_entry(["ROBUST_CANDIDATE"])

        self.assertEqual(entry["maturity_level"], "research_batch_only")
        self.assertEqual(entry["current_status"], "RESEARCH_BATCH")
        self.assertIn("ROBUST_CANDIDATE", output)
        self.assertEqual(output.count("REFUSED"), 1)

    def test_unevaluated_token_with_metadata_falls_through_to_triaged(self) -> None:
        entry, output = self._build_entry(
            ["FORWARD_PAPER_CANDIDATE"],
            yaml_text="codex_status: READY_FOR_PYTHON_PROTOTYPE\n",
        )

        self.assertEqual(entry["maturity_level"], "triaged_candidate")
        self.assertEqual(entry["current_status"], "READY_FOR_PYTHON_PROTOTYPE")
        self.assertNotIn("FORWARD_PAPER_CANDIDATE", entry["current_status"])
        self.assertEqual(output.count("REFUSED"), 1)

    def test_promoted_ladder_tokens_are_accepted_unchanged(self) -> None:
        tokens = [
            "PROMOTE_TO_FORWARD_PAPER_TRADE",
            "PROMOTE_TO_PARITY_CANDIDATE",
        ]
        entry, output = self._build_entry(tokens)

        self.assertEqual(entry["maturity_level"], "promoted_candidate")
        self.assertEqual(entry["current_status"], "|".join(tokens))
        self.assertNotIn("REFUSED", output)

    def test_missing_promotion_status_keeps_research_batch(self) -> None:
        entry, output = self._build_entry(include_promotion_status=False)

        self.assertEqual(entry["maturity_level"], "research_batch_only")
        self.assertEqual(entry["current_status"], "RESEARCH_BATCH")
        self.assertNotIn("REFUSED", output)

    def test_empty_promotion_status_keeps_research_batch(self) -> None:
        entry, output = self._build_entry([])

        self.assertEqual(entry["maturity_level"], "research_batch_only")
        self.assertEqual(entry["current_status"], "RESEARCH_BATCH")
        self.assertNotIn("REFUSED", output)

    def test_unknown_token_is_refused(self) -> None:
        entry, output = self._build_entry(["PLEASE_PROMOTE"])

        self.assertEqual(entry["maturity_level"], "research_batch_only")
        self.assertEqual(entry["current_status"], "RESEARCH_BATCH")
        self.assertIn("PLEASE_PROMOTE", output)
        self.assertEqual(output.count("REFUSED"), 1)

    def test_mixed_ladder_and_unevaluated_tokens_are_refused(self) -> None:
        entry, output = self._build_entry(
            ["PROMOTE_TO_FORWARD_PAPER_TRADE", "FORWARD_PAPER_CANDIDATE"]
        )

        self.assertEqual(entry["maturity_level"], "research_batch_only")
        self.assertEqual(entry["current_status"], "RESEARCH_BATCH")
        self.assertIn("FORWARD_PAPER_CANDIDATE", output)
        self.assertEqual(output.count("REFUSED"), 1)

    def test_non_promoted_ladder_tokens_are_refused(self) -> None:
        for token in ("REJECTED", "KEEP_AS_RESEARCH_NOTE"):
            with self.subTest(token=token):
                entry, output = self._build_entry([token])
                self.assertEqual(entry["maturity_level"], "research_batch_only")
                self.assertEqual(entry["current_status"], "RESEARCH_BATCH")
                self.assertIn(token, output)
                self.assertEqual(output.count("REFUSED"), 1)

    def test_bare_strings_are_stripped_and_empty_string_is_ignored(self) -> None:
        promoted, promoted_output = self._build_entry("  PROMOTE_TO_SANDBOX  ")
        empty, empty_output = self._build_entry("  ")

        self.assertEqual(promoted["maturity_level"], "promoted_candidate")
        self.assertEqual(promoted["current_status"], "PROMOTE_TO_SANDBOX")
        self.assertNotIn("REFUSED", promoted_output)
        self.assertEqual(empty["maturity_level"], "research_batch_only")
        self.assertEqual(empty["current_status"], "RESEARCH_BATCH")
        self.assertNotIn("REFUSED", empty_output)


if __name__ == "__main__":
    unittest.main()
