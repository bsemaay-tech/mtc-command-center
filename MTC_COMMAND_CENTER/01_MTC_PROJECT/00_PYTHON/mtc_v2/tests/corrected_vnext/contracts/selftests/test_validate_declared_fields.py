from __future__ import annotations

import hashlib
import re
import subprocess
import sys
import unittest
from copy import deepcopy
from pathlib import Path


SELFTESTS = Path(__file__).resolve().parent
CONTRACTS = SELFTESTS.parent
MTC_V2_PARENT = SELFTESTS.parents[4]
if str(MTC_V2_PARENT) not in sys.path:
    sys.path.insert(0, str(MTC_V2_PARENT))

from mtc_v2.tests.corrected_vnext.contracts import validate_declared_fields as validator


class DeclaredFieldValidatorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.manifest = validator.load_json_exact(CONTRACTS / "CONTRACT_TABLES_MANIFEST.json")
        cls.anchor = validator.load_json_exact(CONTRACTS / "implementation_anchor.json")
        cls.registry = validator.load_json_exact(CONTRACTS / "declared_field_registry.json")
        cls.design_text = Path(cls.manifest["design"]["file"]).read_text(encoding="utf-8")
        cls.repo_root = validator._repo_root()
        cls.path_count = len(
            subprocess.check_output(
                [
                    "git",
                    "-C",
                    str(cls.repo_root),
                    "ls-files",
                    "--",
                    CONTRACTS.parent.relative_to(cls.repo_root).as_posix(),
                ],
                text=True,
            ).splitlines()
        )
        baseline_path = Path(cls.manifest["legacy_event_order_map_pin"]["baseline_manifest"]["path"])
        cls.baseline_digest = hashlib.sha256(baseline_path.read_bytes()).hexdigest()

    def codes(
        self,
        manifest: dict | None = None,
        anchor: dict | None = None,
        registry: dict | None = None,
        **kwargs: object,
    ) -> list[str]:
        return [
            refusal.code
            for refusal in validator.validate_documents(
                deepcopy(self.manifest if manifest is None else manifest),
                deepcopy(self.anchor if anchor is None else anchor),
                deepcopy(self.registry if registry is None else registry),
                repo_root=self.repo_root,
                **kwargs,
            )
        ]

    def test_seal_state_seal_agree_red_green(self) -> None:
        self.assertNotIn("SEAL_STATE_SEAL_AGREE", self.codes())
        mutated = deepcopy(self.manifest)
        mutated["seal_state"]["EXPECTED_SEAL_SHA"] = "a" * 64
        self.assertIn("SEAL_STATE_SEAL_AGREE", self.codes(mutated))

    def test_seal_state_base_agree_red_green(self) -> None:
        self.assertNotIn("SEAL_STATE_BASE_AGREE", self.codes())
        mutated = deepcopy(self.manifest)
        mutated["seal_state"]["IMPLEMENTATION_BASE_SHA"] = "b" * 40
        self.assertIn("SEAL_STATE_BASE_AGREE", self.codes(mutated))

    def test_reseal_chain_continuous_red_green(self) -> None:
        clean_anchor = deepcopy(self.anchor)
        history = clean_anchor["base_repin_history"]
        for index in range(1, len(history)):
            history[index]["old_core_tree_oid_at_base"] = history[index - 1]["new_core_tree_oid_at_base"]
        self.assertNotIn("RESEAL_CHAIN_CONTINUOUS", self.codes(anchor=clean_anchor))

        mutated = deepcopy(self.manifest)
        mutated["reseal_history"][3]["old_EXPECTED_SEAL_SHA"] = "c" * 64
        self.assertIn(
            "RESEAL_CHAIN_CONTINUOUS",
            self.codes(manifest=mutated, anchor=clean_anchor),
        )

    def test_orphan_predecessor_red_green(self) -> None:
        self.assertNotIn("ORPHAN_PREDECESSOR", self.codes())
        mutated = deepcopy(self.anchor)
        mutated["reseal_history"][4]["old_EXPECTED_SEAL_SHA"] = "d" * 64
        self.assertIn("ORPHAN_PREDECESSOR", self.codes(anchor=mutated))

    def test_design_version_matches_bytes_red_green(self) -> None:
        self.assertNotIn(
            "DESIGN_VERSION_MATCHES_BYTES",
            self.codes(design_text=self.design_text),
        )
        mutated = deepcopy(self.manifest)
        mutated["design"]["version"] = "v8.6"
        self.assertIn(
            "DESIGN_VERSION_MATCHES_BYTES",
            self.codes(manifest=mutated, design_text=self.design_text),
        )

    def test_design_changelog_adopted_red_green(self) -> None:
        clean_design = re.sub(
            r"^(###\s+23\.22\s+)v1\.25(\s+change log)",
            r"\1v1.24\2",
            self.design_text,
            count=1,
            flags=re.MULTILINE,
        )
        self.assertNotIn(
            "DESIGN_CHANGELOG_ADOPTED",
            self.codes(design_text=clean_design),
        )
        mutated_design = re.sub(
            r"^(###\s+23\.22\s+)v1\.24(\s+change log)",
            r"\1v9.7\2",
            clean_design,
            count=1,
            flags=re.MULTILINE,
        )
        self.assertIn(
            "DESIGN_CHANGELOG_ADOPTED",
            self.codes(design_text=mutated_design),
        )

    def test_heading_map_accurate_red_green(self) -> None:
        clean = deepcopy(self.manifest)
        actual: dict[str, int] = {}
        for line_number, line in enumerate(self.design_text.splitlines(), 1):
            match = re.match(r"^#{1,6}\s+(.+?)\s*$", line)
            if match is not None:
                actual[match.group(1)] = line_number
        heading_map = clean["design"]["heading_line_map_measured_at_reseal17"]
        for heading in heading_map:
            heading_map[heading] = actual[heading]
        self.assertNotIn(
            "HEADING_MAP_ACCURATE",
            self.codes(manifest=clean, design_text=self.design_text),
        )

        mutated = deepcopy(clean)
        first_heading = next(iter(heading_map))
        mutated["design"]["heading_line_map_measured_at_reseal17"][first_heading] += 37
        self.assertIn(
            "HEADING_MAP_ACCURATE",
            self.codes(manifest=mutated, design_text=self.design_text),
        )

    def test_path_count_accurate_red_green(self) -> None:
        clean = deepcopy(self.manifest)
        statement = clean["expected_value_provenance"]["statement"]
        clean["expected_value_provenance"]["statement"] = re.sub(
            r"\b1194 paths under tests/corrected_vnext/",
            f"{self.path_count} paths under tests/corrected_vnext/",
            statement,
        )
        self.assertNotIn(
            "PATH_COUNT_ACCURATE",
            self.codes(manifest=clean, tracked_path_count=self.path_count),
        )

        mutated = deepcopy(clean)
        mutated["expected_value_provenance"]["statement"] = re.sub(
            rf"\b{self.path_count} paths under tests/corrected_vnext/",
            f"{self.path_count + 23} paths under tests/corrected_vnext/",
            mutated["expected_value_provenance"]["statement"],
        )
        self.assertIn(
            "PATH_COUNT_ACCURATE",
            self.codes(manifest=mutated, tracked_path_count=self.path_count),
        )

    def test_section16_status_consistent_red_green(self) -> None:
        clean = deepcopy(self.manifest)
        clean["section_16_review"]["status"] = "COMPLETE"
        clean["section_16_review"]["statement"] = (
            "The independent semantic coverage review is installed and complete."
        )
        self.assertNotIn("SECTION16_STATUS_CONSISTENT", self.codes(manifest=clean))

        mutated = deepcopy(clean)
        mutated["section_16_review"]["status"] = "UNPERFORMED_BY_MUTATION"
        mutated["section_16_review"]["statement"] = (
            "This deliberately different review has not been performed."
        )
        self.assertIn("SECTION16_STATUS_CONSISTENT", self.codes(manifest=mutated))

    def test_baseline_pin_current_or_labelled_red_green(self) -> None:
        clean = deepcopy(self.manifest)
        clean["legacy_event_order_map_pin"]["baseline_manifest"]["historical"] = True
        self.assertNotIn(
            "BASELINE_PIN_CURRENT_OR_LABELLED",
            self.codes(manifest=clean, baseline_digest=self.baseline_digest),
        )

        mutated = deepcopy(clean)
        baseline = mutated["legacy_event_order_map_pin"]["baseline_manifest"]
        del baseline["historical"]
        baseline["sha256"] = "7" * 64
        self.assertIn(
            "BASELINE_PIN_CURRENT_OR_LABELLED",
            self.codes(manifest=mutated, baseline_digest=self.baseline_digest),
        )

    def test_historical_labelled_red_green(self) -> None:
        clean = deepcopy(self.manifest)
        live = validator._live_identity(self.repo_root)
        clean["repository_evidence_identity"].update(live)
        self.assertNotIn("HISTORICAL_LABELLED", self.codes(manifest=clean))

        mutated = deepcopy(clean)
        mutated["repository_evidence_identity"]["head_commit"] = "e" * 40
        mutated["repository_evidence_identity"]["verification"] = (
            "This deliberately different identity now tracks a mutation; run this session."
        )
        self.assertIn("HISTORICAL_LABELLED", self.codes(manifest=mutated))

    def test_invented_top_level_field_is_unregistered(self) -> None:
        mutated = deepcopy(self.manifest)
        mutated["invented_validator_field_83"] = "different from every historical defect"
        self.assertIn("UNREGISTERED_FIELD", self.codes(manifest=mutated))

    def test_missing_registered_field_is_refused(self) -> None:
        mutated = deepcopy(self.manifest)
        del mutated["bundle_id"]
        self.assertIn("MISSING_DECLARED_FIELD", self.codes(manifest=mutated))

    def test_false_enforced_claim_is_unproven(self) -> None:
        mutated = deepcopy(self.registry)
        schema_entry = next(
            entry for entry in mutated["entries"] if entry["path"] == "manifest.schema"
        )
        schema_entry["enforced_at"] = "tests/corrected_vnext/verify_bceg.py:2950"
        self.assertIn("ENFORCED_CLAIM_UNPROVEN", self.codes(registry=mutated))


if __name__ == "__main__":
    unittest.main()
