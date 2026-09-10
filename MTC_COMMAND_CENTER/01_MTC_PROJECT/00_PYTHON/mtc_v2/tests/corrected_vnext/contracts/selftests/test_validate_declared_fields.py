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

    def test_heading_map_historical_consistent_red_green(self) -> None:
        """The map is a dated reseal-17 snapshot, so positive drift is EXPECTED.

        An earlier version of this check compared the snapshot against current line
        numbers and produced 8 false refusals on the real manifest. Correcting those
        entries would have falsified a dated historical record. The sound invariants are
        that every declared heading still exists, and that drift is never negative --
        a heading moving earlier means content was deleted above an append-only design.
        """
        actual: dict[str, int] = {}
        for line_number, line in enumerate(self.design_text.splitlines(), 1):
            match = re.match(r"^#{1,6}\s+(.+?)\s*$", line)
            if match is not None:
                actual.setdefault(match.group(1), line_number)

        # GREEN: the real manifest, untouched. Its 8 drifted entries are +1/+3, i.e.
        # positive, and must NOT refuse.
        self.assertNotIn(
            "HEADING_MAP_HISTORICAL_CONSISTENT",
            self.codes(manifest=self.manifest, design_text=self.design_text),
        )

        heading_map = self.manifest["design"]["heading_line_map_measured_at_reseal17"]
        first_heading = next(iter(heading_map))

        # RED 1: negative drift -- declared later than where the heading actually sits.
        earlier = deepcopy(self.manifest)
        earlier["design"]["heading_line_map_measured_at_reseal17"][first_heading] = (
            actual[first_heading] + 50
        )
        self.assertIn(
            "HEADING_MAP_HISTORICAL_CONSISTENT",
            self.codes(manifest=earlier, design_text=self.design_text),
        )

        # RED 2: a declared heading that no longer exists in the design at all.
        vanished = deepcopy(self.manifest)
        vanished_map = vanished["design"]["heading_line_map_measured_at_reseal17"]
        vanished_map["A heading that was never in this design"] = vanished_map.pop(
            first_heading
        )
        self.assertIn(
            "HEADING_MAP_HISTORICAL_CONSISTENT",
            self.codes(manifest=vanished, design_text=self.design_text),
        )

        # And positive drift specifically must stay GREEN.
        drifted = deepcopy(self.manifest)
        drifted["design"]["heading_line_map_measured_at_reseal17"][first_heading] = max(
            1, actual[first_heading] - 37
        )
        self.assertNotIn(
            "HEADING_MAP_HISTORICAL_CONSISTENT",
            self.codes(manifest=drifted, design_text=self.design_text),
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

    @staticmethod
    def _strip_dating(block: dict) -> None:
        """Remove every dating marker from a block's OWN keys.

        Needed because repair 6 (HIST-2026-0024) dated these blocks in the record, so a
        RED case has to say explicitly that it is testing an UNDATED stale field. Nested
        children are left alone deliberately: a marker inside a child dates the child, and
        the checker no longer accepts one as covering the parent.
        """
        for key in list(block):
            folded = key.casefold()
            if "measured_at" in folded or folded in {
                "historical",
                "historical_label",
                "as_of",
                "as_of_utc",
                "captured_at",
                "captured_at_utc",
            }:
                del block[key]

    def test_section16_claiming_done_without_a_receipt_is_refused(self) -> None:
        """The dangerous direction, unchecked until repair 6.

        The first version only caught the record calling the review UNDONE while a valid
        receipt existed -- the self-deprecating direction, and the harmless one. It never
        caught the record claiming the acceptance-blocking review was DONE with nothing
        backing it, which is the direction that could wave a package through.
        """
        done = deepcopy(self.manifest)
        done["section_16_review"]["status"] = "PERFORMED_OWNER_RATIFIED"

        # GREEN: a validating receipt is installed, so the claim is backed.
        self.assertNotIn("SECTION16_STATUS_CONSISTENT", self.codes(manifest=done))

        # RED: the same claim with an empty receipt.
        # Note on the API: semantic_review=None means "not supplied, read it from disk",
        # so None cannot express absence here. A receipt that fails to validate is the
        # in-memory equivalent, and the genuinely-missing-file path is asserted directly
        # below instead of being faked through this parameter.
        self.assertIn(
            "SECTION16_STATUS_CONSISTENT",
            self.codes(manifest=done, semantic_review={}),
        )

        # RED: and with a receipt carrying the wrong schema.
        self.assertIn(
            "SECTION16_STATUS_CONSISTENT",
            self.codes(
                manifest=done,
                semantic_review={"schema": "DELIBERATELY_NOT_THE_REVIEW_SCHEMA"},
            ),
        )

        # A missing receipt file leaves semantic_review as None after the load fails, so
        # the predicate that decides this must reject None outright.
        self.assertFalse(validator._semantic_review_is_validating(None))

        # GREEN: with no valid receipt, a record that still says PENDING is honest.
        pending = deepcopy(self.manifest)
        pending["section_16_review"]["status"] = "PENDING"
        self.assertNotIn(
            "SECTION16_STATUS_CONSISTENT",
            self.codes(manifest=pending, semantic_review={}),
        )

    def test_baseline_pin_current_or_labelled_red_green(self) -> None:
        clean = deepcopy(self.manifest)
        clean["legacy_event_order_map_pin"]["baseline_manifest"]["historical"] = True
        self.assertNotIn(
            "BASELINE_PIN_CURRENT_OR_LABELLED",
            self.codes(manifest=clean, baseline_digest=self.baseline_digest),
        )

        # GREEN: the record as repaired -- a stale sha256 dated by a sibling that NAMES it.
        self.assertNotIn(
            "BASELINE_PIN_CURRENT_OR_LABELLED",
            self.codes(baseline_digest=self.baseline_digest),
        )

        # RED: a wrong digest with every dating marker stripped from the block itself.
        mutated = deepcopy(clean)
        baseline = mutated["legacy_event_order_map_pin"]["baseline_manifest"]
        self._strip_dating(baseline)
        baseline["sha256"] = "7" * 64
        self.assertIn(
            "BASELINE_PIN_CURRENT_OR_LABELLED",
            self.codes(manifest=mutated, baseline_digest=self.baseline_digest),
        )

        # RED: a marker nested in a CHILD must not discharge the parent's stale field.
        # This is the loophole repair 6 exposed -- current_run.measured_at dates the
        # current run, not the historical sha256 beside it.
        nested_only = deepcopy(mutated)
        nested_only["legacy_event_order_map_pin"]["baseline_manifest"]["current_run"] = {
            "measured_at": "2026-09-10",
            "sha256": "9" * 64,
        }
        self.assertIn(
            "BASELINE_PIN_CURRENT_OR_LABELLED",
            self.codes(manifest=nested_only, baseline_digest=self.baseline_digest),
        )

    def test_historical_labelled_red_green(self) -> None:
        clean = deepcopy(self.manifest)
        live = validator._live_identity(self.repo_root)
        clean["repository_evidence_identity"].update(live)
        self.assertNotIn("HISTORICAL_LABELLED", self.codes(manifest=clean))

        # GREEN: the record as repaired -- values still stale, but the block is dated.
        # It also QUOTES the present-tense phrase it corrected, which the first version of
        # this check punished. Quoting a former assertion is not making it.
        self.assertNotIn("HISTORICAL_LABELLED", self.codes())

        # RED: stale AND undated AND written in the present tense.
        mutated = deepcopy(clean)
        block = mutated["repository_evidence_identity"]
        self._strip_dating(block)
        block["head_commit"] = "e" * 40
        block["verification"] = (
            "This deliberately different identity now tracks a mutation; run this session."
        )
        self.assertIn("HISTORICAL_LABELLED", self.codes(manifest=mutated))

        # RED: stale and undated is enough on its own -- no present-tense wording needed.
        quiet = deepcopy(mutated)
        quiet["repository_evidence_identity"]["verification"] = (
            "A deliberately different neutral sentence carrying no tense cue at all."
        )
        self.assertIn("HISTORICAL_LABELLED", self.codes(manifest=quiet))

    def test_record_own_dating_convention_discharges_the_label(self) -> None:
        """This record dates a snapshot in the KEY NAME, and that must be accepted.

        `design.heading_line_map_measured_at_reseal17` plus four
        `heading_line_map_addition_measured_at_reseal{25,26,28,30}` siblings -- five uses. The
        first version of this validator recognised "historical", "captured_at" and "as_of",
        three spellings this record has never used, and omitted the one it does. It would have
        demanded a new convention while a working one sat five keys away.
        """
        # (a) a dated inner field, no boolean
        inner = deepcopy(self.manifest)
        baseline = inner["legacy_event_order_map_pin"]["baseline_manifest"]
        baseline["sha256_measured_at"] = "re-seal #24, 2026-09-05"
        self.assertNotIn(
            "BASELINE_PIN_CURRENT_OR_LABELLED",
            self.codes(manifest=inner, baseline_digest=self.baseline_digest),
        )

        # (b) the date carried in the key name, exactly as the design block does it
        keyed = deepcopy(self.manifest)
        pin = keyed["legacy_event_order_map_pin"]
        pin["baseline_manifest_measured_at_reseal24"] = pin.pop("baseline_manifest")
        pin["baseline_manifest"] = deepcopy(
            pin["baseline_manifest_measured_at_reseal24"]
        )
        pin["baseline_manifest"]["measured_at"] = "re-seal #24, 2026-09-05"
        self.assertNotIn(
            "BASELINE_PIN_CURRENT_OR_LABELLED",
            self.codes(manifest=keyed, baseline_digest=self.baseline_digest),
        )

        # (c) RED is unchanged: a wrong digest with NO dating of any kind still refuses.
        bare = deepcopy(self.manifest)
        bare_pin = bare["legacy_event_order_map_pin"]["baseline_manifest"]
        bare_pin["sha256"] = "7" * 64
        for key in list(bare_pin):
            if "measured_at" in key or key in {"historical", "as_of", "captured_at"}:
                del bare_pin[key]
        self.assertIn(
            "BASELINE_PIN_CURRENT_OR_LABELLED",
            self.codes(manifest=bare, baseline_digest=self.baseline_digest),
        )

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
