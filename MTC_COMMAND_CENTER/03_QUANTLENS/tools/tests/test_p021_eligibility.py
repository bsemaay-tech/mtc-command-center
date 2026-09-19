from __future__ import annotations

import unittest
from collections import UserString, namedtuple
from collections.abc import Mapping
from dataclasses import replace
from datetime import datetime, timedelta, timezone, tzinfo
from unittest.mock import patch

from mtc_contracts.admission import EligibilityState
from mtc_contracts.lineage import UnsimulatedControl
from pydantic import ValidationError

import p021_evidence_contracts
import p021_readiness_rules
from p021_evidence_contracts import (
    ControlInventoryItem,
    ClosedBarRuntimeReceipt,
    DatasetIdentity,
    DecisionKey,
    EvidenceContractRefused,
    IntentEvidence,
    compare_lookahead,
    control_inventory_sha256,
    evaluate_control_evidence,
    intent_evidence_sha256,
    require_ds_v1_digest,
    unsimulated_controls_sha256,
    validate_closed_bar_runtime_receipt,
)


_EXPECTED_OPEN_NUMBERS = {
    "divergence_tolerance_intent",
    "divergence_tolerance_return",
    "divergence_window_length",
    "divergence_min_paired_observations",
}
_EXPECTED_CHECK_IDS = {
    "P021.DETERMINISTIC_REPLAY",
    "P021.LOOKAHEAD_PREFIX",
    "P021.REPAINT_CLOSED_BAR",
    "P021.DATA_QUALITY",
    "P021.BASIC_FAILURE_FLOOR",
    "P021.UNSIMULATED_CONTROLS",
    "P021.BACKTEST_FORWARD_DIVERGENCE",
}


class StringAlias(str):
    def __new__(cls, value: str, alias: str) -> StringAlias:
        instance = super().__new__(cls, value)
        instance.alias = alias
        return instance

    def __eq__(self, other: object) -> bool:
        return other == self.alias

    def __ne__(self, other: object) -> bool:
        return not self == other

    def __hash__(self) -> int:
        return hash(self.alias)


class BrokenIterable:
    def __iter__(self):
        raise RuntimeError("malformed carrier")


class P021ContractTestCase(unittest.TestCase):
    def assert_refused_reason(
        self, reason_id: str, function: object, /, *args: object, **kwargs: object
    ) -> None:
        with self.assertRaises(EvidenceContractRefused) as caught:
            function(*args, **kwargs)  # type: ignore[operator]
        self.assertEqual(caught.exception.reason_id, reason_id)

    def assert_readiness_fence(self) -> None:
        record = p021_readiness_rules.readiness_record()
        self.assertIs(record["ready"], False)
        self.assertEqual(record["status"], "REFUSED")
        self.assertEqual(len(record["checks"]), 7)
        self.assertEqual(
            {check["check_id"] for check in record["checks"]},
            _EXPECTED_CHECK_IDS,
        )
        self.assertTrue(
            all(check["status"] == "REFUSED" for check in record["checks"])
        )
        self.assertEqual(len(record["open_numbers"]), 4)  # B-06 is two numbers under M-C
        # S2 (OD-20260915-P021-S2-RECOMMENDED-1): gap_ratio_max is CLOSED in the catalogue and DATA_QUALITY
        # carries the value and the two pins, yet every check still refuses readiness.
        data_quality = next(c for c in record["checks"] if c["check_id"] == "P021.DATA_QUALITY")
        self.assertEqual(data_quality["limits"]["gap_ratio_max"], 0.0001)
        self.assertEqual(data_quality["limits"]["gap_ratio_metric"], "m2_missing_bar_ratio")
        self.assertEqual(
            data_quality["limits"]["gap_ratio_formula_id"],
            "m2_missing_bar_ratio@data_gap_ratio.py v1 (fixed-step 24/7, half-open span, "
            "leading/trailing absence excluded)",
        )
        self.assertEqual(data_quality["limits"]["dataset_hash_contract"], "ds-v1")
        self.assertEqual(data_quality["missing_numbers"], [])
        self.assertEqual(data_quality["missing_rules"], ["accepted_corrected_engine.B01"])
        divergence = next(c for c in record["checks"] if c["check_id"] == "P021.BACKTEST_FORWARD_DIVERGENCE")
        self.assertEqual(divergence["limits"]["divergence_metric"], "M-C")
        self.assertNotIn("divergence_metric.B05", divergence["missing_rules"])
        # lane-6 exact-Opus review of 7fecf204 (REQUIRED-1/2): the pinned definition is the ratified M-C,
        # i.e. rows M-A and M-B of packet section 4 verbatim, and B-06 is two open numbers under M-C.
        definition = divergence["limits"]["divergence_metric_definition"]
        self.assertEqual(definition, p021_readiness_rules.DIVERGENCE_METRIC_DEFINITION)
        self.assertIn(
            "per-pair signed difference of realized trade return (forward - backtest), aggregated as "
            "the mean over the aligned window, reported with the count and the standard deviation",
            definition,
        )
        self.assertIn("unit: return fraction per trade", definition)
        self.assertIn(
            "share of backtest intents that the forward path produced at the same bar (entry/exit "
            "decisions match), independent of P&L",
            definition,
        )
        self.assertIn("each with its own tolerance", definition)
        for absent in ("absolute", "R-multiple", "size class"):
            self.assertNotIn(absent, definition)
        self.assertEqual(
            divergence["missing_numbers"][:2],
            ["divergence_tolerance_intent", "divergence_tolerance_return"],
        )
        b06 = {item["name"] for item in record["open_numbers"] if item["blocker"] == "B-06"}
        self.assertEqual(b06, {"divergence_tolerance_intent", "divergence_tolerance_return"})
        # NIT-2 of the same review: the S2 provenance is pinned like the S2 values
        self.assertEqual(record["policy_set"]["s2_decided_at"], "2026-09-15")
        self.assertIn("OD-20260915-P021-S2-RECOMMENDED-1", record["policy_set"]["s2_source_document"])
        gap_source = next(n["source"] for n in record["closed_numbers"] if n["name"] == "gap_ratio_max")
        self.assertIn("OD-20260915-P021-S2-RECOMMENDED-1", gap_source)
        self.assertEqual(record["policy_set"]["owner_decisions"]["P021_DECISION_3"], "T")
        self.assertEqual(record["policy_set"]["owner_decisions"]["P021_DIVERGENCE_METRIC"], "M-C")
        closed = {n["name"]: n["value"] for n in record["closed_numbers"]}
        self.assertIn("gap_ratio_max", closed)
        self.assertEqual(closed["gap_ratio_max"], 0.0001)
        self.assertEqual(
            {item["name"] for item in record["open_numbers"]},
            _EXPECTED_OPEN_NUMBERS,
        )

    def setUp(self) -> None:
        self.assert_readiness_fence()

    def tearDown(self) -> None:
        self.assert_readiness_fence()


class ReadinessFenceTests(P021ContractTestCase):
    def test_refuses_duplicate_open_number_record(self) -> None:
        changed = p021_readiness_rules.readiness_record()
        changed["open_numbers"].append(dict(changed["open_numbers"][0]))

        with patch.object(
            p021_readiness_rules,
            "readiness_record",
            return_value=changed,
        ):
            with self.assertRaises(AssertionError):
                self.assert_readiness_fence()

    def test_refuses_replaced_check_id(self) -> None:
        changed = p021_readiness_rules.readiness_record()
        changed["checks"][0]["check_id"] = "P021.REPLACED_BY_MUTANT"

        with patch.object(
            p021_readiness_rules,
            "readiness_record",
            return_value=changed,
        ):
            with self.assertRaises(AssertionError):
                self.assert_readiness_fence()


class DsV1CompatibilityTests(P021ContractTestCase):
    def test_refuses_non_builtin_string_envelope_keys(self) -> None:
        class AliasKey:
            def __init__(self, value: str) -> None:
                self.value = value

            def __eq__(self, other: object) -> bool:
                return self.value == other

            def __hash__(self) -> int:
                return hash(self.value)

        digest = "a" * 64
        for key_type in (UserString, AliasKey):
            envelope = {
                key_type("contract"): "ds-v1",
                key_type("digest"): digest,
            }
            with self.subTest(key_type=key_type.__name__):
                self.assert_refused_reason(
                    "DS_V1_INVALID_ENVELOPE",
                    require_ds_v1_digest,
                    envelope,
                )

    def test_refuses_str_subclass_envelope_keys(self) -> None:
        class StringKey(str):
            pass

        digest = "a" * 64
        envelopes = (
            {StringKey("contract"): "ds-v1", "digest": digest},
            {"contract": "ds-v1", StringKey("digest"): digest},
            {
                StringKey("contract"): "ds-v1",
                StringKey("digest"): digest,
            },
        )
        for envelope in envelopes:
            with self.subTest(keys=tuple(type(key).__name__ for key in envelope)):
                self.assert_refused_reason(
                    "DS_V1_INVALID_ENVELOPE",
                    require_ds_v1_digest,
                    envelope,
                )

    def test_refusal_exposes_stable_reason_id(self) -> None:
        with self.assertRaises(EvidenceContractRefused) as caught:
            require_ds_v1_digest({"contract": "ds-v2", "digest": "a" * 64})

        self.assertEqual(caught.exception.reason_id, "DS_V1_UNSUPPORTED_CONTRACT")

    def test_accepts_exact_envelope_and_refuses_incompatible_shapes(self) -> None:
        digest = "a" * 64

        self.assertEqual(
            require_ds_v1_digest({"contract": "ds-v1", "digest": digest}),
            digest,
        )

        incompatible = (
            {"contract": "ds-v2", "digest": digest},
            {"contract": "ds-v1", "digest": f"sha256:{digest}"},
            {"contract": "ds-v1", "digest": digest.upper()},
            {"contract": "ds-v1", "digest": digest, "path": "dataset.parquet"},
        )
        for envelope in incompatible:
            with self.subTest(envelope=envelope):
                with self.assertRaises(EvidenceContractRefused):
                    require_ds_v1_digest(envelope)

        class StatefulEnvelope(Mapping):
            def __init__(self) -> None:
                self.iterations = 0
                self.contract_reads = 0
                self.digest_reads = 0

            def __iter__(self):
                self.iterations += 1
                return iter(("contract", "digest"))

            def __len__(self) -> int:
                return 2

            def __getitem__(self, key: object) -> object:
                if key == "contract":
                    self.contract_reads += 1
                    if self.contract_reads == 1:
                        return "ds-v1"
                    return StringAlias("ds-v2", "ds-v1")
                if key == "digest":
                    self.digest_reads += 1
                    return digest
                raise KeyError(key)

        stateful = StatefulEnvelope()
        self.assertEqual(require_ds_v1_digest(stateful), digest)
        self.assertEqual(
            (stateful.iterations, stateful.contract_reads, stateful.digest_reads),
            (1, 1, 1),
        )

        class BrokenItemsEnvelope(StatefulEnvelope):
            def items(self):
                raise RuntimeError("hostile items view")

        self.assert_refused_reason(
            "DS_V1_INVALID_ENVELOPE",
            require_ds_v1_digest,
            BrokenItemsEnvelope(),
        )

        class DuplicateItemsEnvelope(StatefulEnvelope):
            def items(self):
                return (
                    ("contract", "ds-v1"),
                    ("contract", "ds-v2"),
                    ("digest", digest),
                )

        self.assert_refused_reason(
            "DS_V1_INVALID_ENVELOPE",
            require_ds_v1_digest,
            DuplicateItemsEnvelope(),
        )

    def test_refuses_string_subclasses_for_contract_and_digest_values(self) -> None:
        digest = "a" * 64
        self.assert_refused_reason(
            "DS_V1_UNSUPPORTED_CONTRACT",
            require_ds_v1_digest,
            {
                "contract": StringAlias("ds-v2", "ds-v1"),
                "digest": digest,
            },
        )
        self.assert_refused_reason(
            "INVALID_SHA256:dataset.digest",
            require_ds_v1_digest,
            {
                "contract": "ds-v1",
                "digest": StringAlias("b" * 64, digest),
            },
        )


class ControlIdentityTests(P021ContractTestCase):
    def test_hashes_versioned_canonical_preimages_to_bare_sha256(self) -> None:
        inventory = (
            ControlInventoryItem("restart_recovery", False),
            ControlInventoryItem("fee", True),
        )
        manifest = (
            UnsimulatedControl(
                control_id="restart_recovery",
                required_for_promotion=False,
                reason="not replayable",
            ),
        )

        self.assertEqual(
            control_inventory_sha256(inventory),
            "0f85b49ba6ad2daa079ede9fe1d95a25392fee3cf9803d3d0bacea09401c1197",
        )
        self.assertEqual(
            unsimulated_controls_sha256(manifest),
            "3c9f17ed023484eda860359d39714cc74947b12f3dfbf6f63c5784283298f117",
        )
        self.assertEqual(
            control_inventory_sha256(tuple(reversed(inventory))),
            control_inventory_sha256(inventory),
        )
        self.assertNotEqual(
            control_inventory_sha256(
                (ControlInventoryItem("fee", False), inventory[0])
            ),
            control_inventory_sha256(inventory),
        )

    def test_manifest_hash_is_order_stable_and_field_sensitive(self) -> None:
        manifest = (
            UnsimulatedControl(
                control_id="fee",
                required_for_promotion=True,
                reason="not simulated",
            ),
            UnsimulatedControl(
                control_id="restart_recovery",
                required_for_promotion=False,
                reason="not replayable",
            ),
        )

        baseline = unsimulated_controls_sha256(manifest)
        self.assertEqual(
            baseline,
            "402c47808d80c9e19faa3dd47931252e1ab9fb19cfccda9b85a7bbd5d7c55516",
        )
        self.assertEqual(unsimulated_controls_sha256(tuple(reversed(manifest))), baseline)
        self.assertNotEqual(
            unsimulated_controls_sha256(
                (
                    manifest[0].model_copy(update={"reason": "different reason"}),
                    manifest[1],
                )
            ),
            baseline,
        )
        self.assertNotEqual(
            unsimulated_controls_sha256(
                (
                    manifest[0].model_copy(
                        update={"contract_version": "9.9.9"}
                    ),
                    manifest[1],
                )
            ),
            baseline,
        )
        self.assertNotEqual(
            unsimulated_controls_sha256(
                (
                    manifest[0].model_copy(
                        update={"required_for_promotion": False}
                    ),
                    manifest[1],
                )
            ),
            baseline,
        )

    def test_refuses_malformed_inventory_and_manifest_carriers(self) -> None:
        for function, reason_id in (
            (control_inventory_sha256, "CONTROL_INVENTORY_INVALID_CARRIER"),
            (
                unsimulated_controls_sha256,
                "UNSIMULATED_CONTROLS_INVALID_CARRIER",
            ),
        ):
            for carrier in (
                None,
                7,
                "not-an-item-sequence",
                {"item": object()},
                BrokenIterable(),
            ):
                with self.subTest(function=function.__name__, carrier=carrier):
                    self.assert_refused_reason(reason_id, function, carrier)

    def test_refuses_duplicate_and_malformed_identity_inputs(self) -> None:
        duplicate_inventory = (
            ControlInventoryItem("fee", True),
            ControlInventoryItem("fee", True),
        )
        duplicate_manifest = (
            UnsimulatedControl(
                control_id="fee", required_for_promotion=True, reason="first"
            ),
            UnsimulatedControl(
                control_id="fee", required_for_promotion=True, reason="second"
            ),
        )

        self.assert_refused_reason(
            "CONTROL_INVENTORY_DUPLICATE_ID",
            control_inventory_sha256,
            duplicate_inventory,
        )
        self.assert_refused_reason(
            "CONTROL_INVENTORY_INVALID_REQUIRED_FLAG",
            control_inventory_sha256,
            (ControlInventoryItem("fee", 1),),
        )
        self.assert_refused_reason(
            "CONTROL_INVENTORY_INVALID_ITEM",
            control_inventory_sha256,
            (object(),),
        )
        self.assert_refused_reason(
            "UNSIMULATED_CONTROLS_DUPLICATE_ID",
            unsimulated_controls_sha256,
            duplicate_manifest,
        )
        self.assert_refused_reason(
            "UNSIMULATED_CONTROLS_INVALID_ITEM",
            unsimulated_controls_sha256,
            (object(),),
        )
        blank_reason = duplicate_manifest[0].model_copy(update={"reason": " "})
        self.assert_refused_reason(
            "UNSIMULATED_CONTROLS_INVALID_REASON",
            unsimulated_controls_sha256,
            (blank_reason,),
        )
        invalid_flag = duplicate_manifest[0].model_copy(
            update={"required_for_promotion": 1}
        )
        self.assert_refused_reason(
            "UNSIMULATED_CONTROLS_INVALID_REQUIRED_FLAG",
            unsimulated_controls_sha256,
            (invalid_flag,),
        )
        blank_control_id = duplicate_manifest[0].model_copy(update={"control_id": " "})
        self.assert_refused_reason(
            "UNSIMULATED_CONTROLS_INVALID_CONTROL_ID",
            unsimulated_controls_sha256,
            (blank_control_id,),
        )
        with self.assertRaises(ValidationError):
            UnsimulatedControl(
                control_id="restart_recovery",
                required_for_promotion=False,
                reason=" ",
            )

    def test_refuses_inventory_record_subclasses(self) -> None:
        class InventorySubclass(ControlInventoryItem):
            pass

        self.assert_refused_reason(
            "CONTROL_INVENTORY_INVALID_ITEM",
            control_inventory_sha256,
            (InventorySubclass("fee", True),),
        )

    def test_refuses_manifest_record_subclasses(self) -> None:
        class ManifestSubclass(UnsimulatedControl):
            pass

        self.assert_refused_reason(
            "UNSIMULATED_CONTROLS_INVALID_ITEM",
            unsimulated_controls_sha256,
            (
                ManifestSubclass(
                    control_id="fee",
                    required_for_promotion=True,
                    reason="not simulated",
                ),
            ),
        )

    def test_refuses_boolean_type_spoofs(self) -> None:
        class BoolSpoof(int):
            @property
            def __class__(self):
                return bool

        flag = BoolSpoof(1)
        self.assertIsInstance(flag, bool)
        self.assert_refused_reason(
            "CONTROL_INVENTORY_INVALID_REQUIRED_FLAG",
            control_inventory_sha256,
            (ControlInventoryItem("fee", flag),),
        )
        manifest_item = UnsimulatedControl(
            control_id="fee",
            required_for_promotion=True,
            reason="not simulated",
        ).model_copy(update={"required_for_promotion": flag})
        self.assert_refused_reason(
            "UNSIMULATED_CONTROLS_INVALID_REQUIRED_FLAG",
            unsimulated_controls_sha256,
            (manifest_item,),
        )

    def test_refuses_manifest_string_subclasses(self) -> None:
        manifest_item = UnsimulatedControl(
            control_id="fee",
            required_for_promotion=True,
            reason="not simulated",
        )
        mutations = (
            (
                manifest_item.model_copy(
                    update={"control_id": StringAlias("fee", "fee")}
                ),
                "UNSIMULATED_CONTROLS_INVALID_CONTROL_ID",
            ),
            (
                manifest_item.model_copy(
                    update={"reason": StringAlias("not simulated", "not simulated")}
                ),
                "UNSIMULATED_CONTROLS_INVALID_REASON",
            ),
            (
                manifest_item.model_copy(
                    update={
                        "contract_version": StringAlias(
                            manifest_item.contract_version,
                            manifest_item.contract_version,
                        )
                    }
                ),
                "UNSIMULATED_CONTROLS_INVALID_CONTRACT_VERSION",
            ),
        )
        for mutation, reason_id in mutations:
            with self.subTest(reason_id=reason_id):
                self.assert_refused_reason(
                    reason_id,
                    unsimulated_controls_sha256,
                    (mutation,),
                )


class ControlAllowanceTests(P021ContractTestCase):
    def test_refuses_target_state_class_spoof(self) -> None:
        class TargetStateSpoof:
            @property
            def __class__(self):
                return EligibilityState

        target_state = TargetStateSpoof()
        self.assertIsInstance(target_state, EligibilityState)
        self.assert_refused_reason(
            "CONTROL_INVALID_TARGET_STATE",
            evaluate_control_evidence,
            target_state=target_state,
            inventory=(),
            executed_control_ids=(),
            manifest=(),
            expected_control_inventory_hash=control_inventory_sha256(()),
            expected_unsimulated_controls_hash=unsimulated_controls_sha256(()),
        )

    def test_refuses_executed_control_id_tuple_subclasses(self) -> None:
        class TupleSubclass(tuple):
            pass

        NamedTupleCarrier = namedtuple("NamedTupleCarrier", ("control_id",))
        inventory = (ControlInventoryItem("fee", True),)
        common = {
            "target_state": EligibilityState.SHADOW_ELIGIBLE,
            "inventory": inventory,
            "manifest": (),
            "expected_control_inventory_hash": control_inventory_sha256(inventory),
            "expected_unsimulated_controls_hash": unsimulated_controls_sha256(()),
        }

        for carrier in (NamedTupleCarrier("fee"), TupleSubclass(("fee",))):
            with self.subTest(carrier_type=type(carrier).__name__):
                self.assert_refused_reason(
                    "CONTROL_INVALID_EXECUTED_IDS_CARRIER",
                    evaluate_control_evidence,
                    executed_control_ids=carrier,
                    **common,
                )

    def test_refuses_malformed_executed_control_id_carriers(self) -> None:
        inventory = (ControlInventoryItem("fee", True),)
        manifest = (
            UnsimulatedControl(
                control_id="fee",
                required_for_promotion=True,
                reason="not simulated",
            ),
        )
        common = {
            "target_state": EligibilityState.SHADOW_ELIGIBLE,
            "inventory": inventory,
            "manifest": manifest,
            "expected_control_inventory_hash": control_inventory_sha256(inventory),
            "expected_unsimulated_controls_hash": unsimulated_controls_sha256(
                manifest
            ),
        }

        for carrier in ("fee", {"fee": True}, None, ["fee"]):
            with self.subTest(carrier=carrier):
                self.assert_refused_reason(
                    "CONTROL_INVALID_EXECUTED_IDS_CARRIER",
                    evaluate_control_evidence,
                    executed_control_ids=carrier,
                    **common,
                )

    def test_refuses_executed_control_id_string_alias(self) -> None:
        inventory = (ControlInventoryItem("fee", True),)
        self.assert_refused_reason(
            "INVALID_TEXT:executed_control_id",
            evaluate_control_evidence,
            target_state=EligibilityState.SHADOW_ELIGIBLE,
            inventory=inventory,
            executed_control_ids=(StringAlias("not-fee", "fee"),),
            manifest=(),
            expected_control_inventory_hash=control_inventory_sha256(inventory),
            expected_unsimulated_controls_hash=unsimulated_controls_sha256(()),
        )

    def test_materializes_inventory_and_manifest_once(self) -> None:
        inventory = (
            ControlInventoryItem("fee", True),
            ControlInventoryItem("restart_recovery", False),
        )
        manifest = (
            UnsimulatedControl(
                control_id="restart_recovery",
                required_for_promotion=False,
                reason="not replayable",
            ),
        )
        evidence = evaluate_control_evidence(
            target_state=EligibilityState.SHADOW_ELIGIBLE,
            inventory=iter(inventory),
            executed_control_ids=("fee",),
            manifest=iter(manifest),
            expected_control_inventory_hash=control_inventory_sha256(inventory),
            expected_unsimulated_controls_hash=unsimulated_controls_sha256(
                manifest
            ),
        )
        self.assertEqual(evidence.informational_control_ids, ("restart_recovery",))

    def test_snapshots_inventory_before_manifest_iteration(self) -> None:
        class HostileString(str):
            def __hash__(self) -> int:
                raise RuntimeError("hostile inventory hash")

        inventory_item = ControlInventoryItem("fee", True)
        expected_inventory_hash = control_inventory_sha256((inventory_item,))

        class MutatingManifest:
            def __init__(self) -> None:
                self.iterations = 0

            def __iter__(self):
                self.iterations += 1
                object.__setattr__(
                    inventory_item,
                    "control_id",
                    HostileString("fee"),
                )
                return iter(())

        manifest = MutatingManifest()
        evidence = evaluate_control_evidence(
            target_state=EligibilityState.SHADOW_ELIGIBLE,
            inventory=(inventory_item,),
            executed_control_ids=("fee",),
            manifest=manifest,
            expected_control_inventory_hash=expected_inventory_hash,
            expected_unsimulated_controls_hash=unsimulated_controls_sha256(()),
        )

        self.assertEqual(manifest.iterations, 1)
        self.assertEqual(evidence.inventory_sha256, expected_inventory_hash)
        self.assertEqual(evidence.undeclared_control_ids, ())

    def test_required_unsimulated_control_caps_above_shadow(self) -> None:
        inventory = (
            ControlInventoryItem("fee", True),
            ControlInventoryItem("restart_recovery", False),
        )
        manifest = (
            UnsimulatedControl(
                control_id="fee",
                required_for_promotion=True,
                reason="not simulated",
            ),
            UnsimulatedControl(
                control_id="restart_recovery",
                required_for_promotion=False,
                reason="not replayable",
            ),
        )
        expected_inventory_hash = (
            "0f85b49ba6ad2daa079ede9fe1d95a25392fee3cf9803d3d0bacea09401c1197"
        )
        expected_manifest_hash = (
            "402c47808d80c9e19faa3dd47931252e1ab9fb19cfccda9b85a7bbd5d7c55516"
        )

        shadow = evaluate_control_evidence(
            target_state=EligibilityState.SHADOW_ELIGIBLE,
            inventory=inventory,
            executed_control_ids=(),
            manifest=manifest,
            expected_control_inventory_hash=expected_inventory_hash,
            expected_unsimulated_controls_hash=expected_manifest_hash,
        )
        self.assertEqual(shadow.blocking_required_control_ids, ())
        self.assertEqual(shadow.informational_control_ids, ("restart_recovery",))

        for state in (
            EligibilityState.TESTNET_PAPER_ELIGIBLE,
            EligibilityState.LIVE_CANDIDATE,
            EligibilityState.LIMITED_LIVE_APPROVED,
        ):
            with self.subTest(state=state):
                evidence = evaluate_control_evidence(
                    target_state=state,
                    inventory=inventory,
                    executed_control_ids=(),
                    manifest=manifest,
                    expected_control_inventory_hash=expected_inventory_hash,
                    expected_unsimulated_controls_hash=expected_manifest_hash,
                )
                self.assertEqual(evidence.blocking_required_control_ids, ("fee",))

        with self.assertRaisesRegex(EvidenceContractRefused, "HASH_MISMATCH"):
            evaluate_control_evidence(
                target_state=EligibilityState.SHADOW_ELIGIBLE,
                inventory=inventory,
                executed_control_ids=(),
                manifest=manifest,
                expected_control_inventory_hash="0" * 64,
                expected_unsimulated_controls_hash=expected_manifest_hash,
            )

    def test_refuses_mismatched_classification_hashes_and_omitted_inventory(
        self,
    ) -> None:
        inventory = (
            ControlInventoryItem("fee", True),
            ControlInventoryItem("restart_recovery", False),
        )
        mismatched_manifest = (
            UnsimulatedControl(
                control_id="fee",
                required_for_promotion=False,
                reason="misclassified",
            ),
        )
        inventory_hash = control_inventory_sha256(inventory)
        mismatched_manifest_hash = unsimulated_controls_sha256(mismatched_manifest)
        self.assert_refused_reason(
            "CONTROL_REQUIRED_FLAG_MISMATCH",
            evaluate_control_evidence,
            target_state=EligibilityState.SHADOW_ELIGIBLE,
            inventory=inventory,
            executed_control_ids=(),
            manifest=mismatched_manifest,
            expected_control_inventory_hash=inventory_hash,
            expected_unsimulated_controls_hash=mismatched_manifest_hash,
        )

        empty_manifest_hash = unsimulated_controls_sha256(())
        self.assert_refused_reason(
            "CONTROL_UNDECLARED_INVENTORY_ITEM",
            evaluate_control_evidence,
            target_state=EligibilityState.SHADOW_ELIGIBLE,
            inventory=inventory,
            executed_control_ids=("fee",),
            manifest=(),
            expected_control_inventory_hash=inventory_hash,
            expected_unsimulated_controls_hash=empty_manifest_hash,
        )

        common = {
            "target_state": EligibilityState.SHADOW_ELIGIBLE,
            "inventory": inventory,
            "executed_control_ids": ("fee",),
            "manifest": (),
        }
        self.assert_refused_reason(
            "CONTROL_INVENTORY_HASH_MISMATCH",
            evaluate_control_evidence,
            **common,
            expected_control_inventory_hash="0" * 64,
            expected_unsimulated_controls_hash=empty_manifest_hash,
        )
        self.assert_refused_reason(
            "CONTROL_MANIFEST_HASH_MISMATCH",
            evaluate_control_evidence,
            **common,
            expected_control_inventory_hash=inventory_hash,
            expected_unsimulated_controls_hash="0" * 64,
        )


class IntentIdentityTests(P021ContractTestCase):
    def test_binds_p012_semantics_and_deployment_to_a_bare_digest(self) -> None:
        intent = IntentEvidence(
            candidate_id="cand-1",
            package_hash="a" * 64,
            deployment_identity_hash="b" * 64,
            dataset_identity=DatasetIdentity("ds-v1", "c" * 64),
            instrument_id="BINANCE:BTCUSDT",
            decision_bar_timestamp_utc=datetime(2026, 1, 1, tzinfo=timezone.utc),
            intent_id="intent-1",
            p012_intent_contract="p012.intent-stream/v1",
            p012_semantic_payload_sha256="d" * 64,
        )

        self.assertEqual(
            intent_evidence_sha256(intent),
            "fa64dbb8bacaffacf92870fee6dc27c17d31300d80323dc78ddd457802b1d226",
        )
        changed = IntentEvidence(
            **{
                **intent.__dict__,
                "p012_semantic_payload_sha256": "e" * 64,
            }
        )
        self.assertNotEqual(
            intent_evidence_sha256(changed),
            intent_evidence_sha256(intent),
        )

    def test_refuses_unsupported_p012_contract_and_string_aliases(self) -> None:
        intent = IntentEvidence(
            candidate_id="cand-1",
            package_hash="a" * 64,
            deployment_identity_hash="b" * 64,
            dataset_identity=DatasetIdentity("ds-v1", "c" * 64),
            instrument_id="BINANCE:BTCUSDT",
            decision_bar_timestamp_utc=datetime(2026, 1, 1, tzinfo=timezone.utc),
            intent_id="intent-1",
            p012_intent_contract="p012.intent-stream/v1",
            p012_semantic_payload_sha256="d" * 64,
        )
        self.assert_refused_reason(
            "INTENT_UNSUPPORTED_P012_CONTRACT",
            intent_evidence_sha256,
            replace(intent, p012_intent_contract="p012.intent-stream/v2"),
        )
        for mutation, reason_id in (
            (
                replace(
                    intent,
                    candidate_id=StringAlias("other", "cand-1"),
                ),
                "INVALID_TEXT:candidate_id",
            ),
            (
                replace(
                    intent,
                    package_hash=StringAlias("f" * 64, "a" * 64),
                ),
                "INVALID_SHA256:package_hash",
            ),
            (
                replace(
                    intent,
                    p012_intent_contract=StringAlias(
                        "p012.intent-stream/v2", "p012.intent-stream/v1"
                    ),
                ),
                "INTENT_UNSUPPORTED_P012_CONTRACT",
            ),
        ):
            with self.subTest(reason_id=reason_id):
                self.assert_refused_reason(
                    reason_id, intent_evidence_sha256, mutation
                )

    def test_refuses_dataset_identity_subclasses(self) -> None:
        class DatasetIdentitySubclass(DatasetIdentity):
            pass

        intent = IntentEvidence(
            candidate_id="cand-1",
            package_hash="a" * 64,
            deployment_identity_hash="b" * 64,
            dataset_identity=DatasetIdentitySubclass("ds-v1", "c" * 64),
            instrument_id="BINANCE:BTCUSDT",
            decision_bar_timestamp_utc=datetime(
                2026, 1, 1, tzinfo=timezone.utc
            ),
            intent_id="intent-1",
            p012_intent_contract="p012.intent-stream/v1",
            p012_semantic_payload_sha256="d" * 64,
        )

        self.assert_refused_reason(
            "DS_V1_INVALID_IDENTITY",
            intent_evidence_sha256,
            intent,
        )

    def test_refuses_untrusted_utc_offset_carriers(self) -> None:
        class ZeroEqualTimedelta(timedelta):
            def __eq__(self, other: object) -> bool:
                return other == timedelta(0)

            def __ne__(self, other: object) -> bool:
                return not self == other

        class SpoofedUtc(tzinfo):
            def utcoffset(self, value: datetime | None) -> timedelta:
                return ZeroEqualTimedelta(hours=1)

            def dst(self, value: datetime | None) -> timedelta:
                return timedelta(0)

        class HostileUtc(tzinfo):
            def utcoffset(self, value: datetime | None) -> timedelta:
                raise RuntimeError("hostile offset")

            def dst(self, value: datetime | None) -> timedelta:
                return timedelta(0)

        for unsafe_zone in (SpoofedUtc(), HostileUtc()):
            intent = IntentEvidence(
                candidate_id="cand-1",
                package_hash="a" * 64,
                deployment_identity_hash="b" * 64,
                dataset_identity=DatasetIdentity("ds-v1", "c" * 64),
                instrument_id="BINANCE:BTCUSDT",
                decision_bar_timestamp_utc=datetime(
                    2026, 1, 1, tzinfo=unsafe_zone
                ),
                intent_id="intent-1",
                p012_intent_contract="p012.intent-stream/v1",
                p012_semantic_payload_sha256="d" * 64,
            )
            with self.subTest(zone_type=type(unsafe_zone).__name__):
                self.assert_refused_reason(
                    "INVALID_UTC_DATETIME:decision_bar_timestamp_utc",
                    intent_evidence_sha256,
                    intent,
                )

    def test_refuses_builtin_timezone_with_spoofed_offset(self) -> None:
        class ZeroEqualTimedelta(timedelta):
            def __eq__(self, other: object) -> bool:
                return other == timedelta(0)

            def __ne__(self, other: object) -> bool:
                return not self == other

        spoofed_zone = timezone(ZeroEqualTimedelta(hours=1))
        timestamp = datetime(2026, 1, 1, tzinfo=spoofed_zone)
        self.assertIs(type(spoofed_zone), timezone)
        self.assertIs(type(timestamp.utcoffset()), ZeroEqualTimedelta)
        intent = IntentEvidence(
            candidate_id="cand-1",
            package_hash="a" * 64,
            deployment_identity_hash="b" * 64,
            dataset_identity=DatasetIdentity("ds-v1", "c" * 64),
            instrument_id="BINANCE:BTCUSDT",
            decision_bar_timestamp_utc=timestamp,
            intent_id="intent-1",
            p012_intent_contract="p012.intent-stream/v1",
            p012_semantic_payload_sha256="d" * 64,
        )

        self.assert_refused_reason(
            "INVALID_UTC_DATETIME:decision_bar_timestamp_utc",
            intent_evidence_sha256,
            intent,
        )

    def test_refuses_naive_builtin_datetime(self) -> None:
        intent = IntentEvidence(
            candidate_id="cand-1",
            package_hash="a" * 64,
            deployment_identity_hash="b" * 64,
            dataset_identity=DatasetIdentity("ds-v1", "c" * 64),
            instrument_id="BINANCE:BTCUSDT",
            decision_bar_timestamp_utc=datetime(2026, 1, 1),
            intent_id="intent-1",
            p012_intent_contract="p012.intent-stream/v1",
            p012_semantic_payload_sha256="d" * 64,
        )

        self.assert_refused_reason(
            "INVALID_UTC_DATETIME:decision_bar_timestamp_utc",
            intent_evidence_sha256,
            intent,
        )


class LookaheadDomainTests(P021ContractTestCase):
    @staticmethod
    def _intent(
        timestamp: datetime,
        intent_id: str,
        semantic_payload_sha256: str = "d" * 64,
    ) -> IntentEvidence:
        return IntentEvidence(
            candidate_id="cand-1",
            package_hash="a" * 64,
            deployment_identity_hash="b" * 64,
            dataset_identity=DatasetIdentity("ds-v1", "c" * 64),
            instrument_id="BINANCE:BTCUSDT",
            decision_bar_timestamp_utc=timestamp,
            intent_id=intent_id,
            p012_intent_contract="p012.intent-stream/v1",
            p012_semantic_payload_sha256=semantic_payload_sha256,
        )

    def test_uses_fixed_closed_bar_union_and_counts_one_sided_decisions(self) -> None:
        timestamps = tuple(
            datetime(2026, 1, 1, minute=minute, tzinfo=timezone.utc)
            for minute in range(3)
        )
        keys = tuple(DecisionKey("BINANCE:BTCUSDT", value) for value in timestamps)
        shared = self._intent(timestamps[0], "shared")

        evidence = compare_lookahead(
            closed_decision_keys=keys,
            full_intents={
                keys[0]: shared,
                keys[1]: self._intent(timestamps[1], "full-only"),
            },
            prefix_intents={
                keys[0]: shared,
                keys[2]: self._intent(timestamps[2], "prefix-only"),
            },
        )

        self.assertEqual(evidence.tested_decision_count, 3)
        self.assertEqual(evidence.intent_mismatch_count, 2)
        self.assertEqual(evidence.first_mismatch_key, keys[1])

        with self.assertRaisesRegex(EvidenceContractRefused, "LOOKAHEAD_EMPTY_UNION"):
            compare_lookahead(
                closed_decision_keys=(),
                full_intents={},
                prefix_intents={},
            )

    def test_refuses_hostile_class_properties_at_carrier_boundaries(self) -> None:
        class HostileClassCarrier:
            @property
            def __class__(self):
                raise RuntimeError("hostile class property")

        carrier = HostileClassCarrier()
        timestamp = datetime(2026, 1, 1, tzinfo=timezone.utc)
        key = DecisionKey("BINANCE:BTCUSDT", timestamp)
        intent = self._intent(timestamp, "intent")
        cases = (
            (
                "CONTROL_INVENTORY_INVALID_CARRIER",
                control_inventory_sha256,
                (carrier,),
                {},
            ),
            (
                "UNSIMULATED_CONTROLS_INVALID_CARRIER",
                unsimulated_controls_sha256,
                (carrier,),
                {},
            ),
            (
                "DS_V1_INVALID_ENVELOPE",
                require_ds_v1_digest,
                (carrier,),
                {},
            ),
            (
                "LOOKAHEAD_INVALID_CLOSED_KEYS_CARRIER",
                compare_lookahead,
                (),
                {
                    "closed_decision_keys": carrier,
                    "full_intents": {key: intent},
                    "prefix_intents": {key: intent},
                },
            ),
            (
                "LOOKAHEAD_INVALID_MAPPING:full_intents",
                compare_lookahead,
                (),
                {
                    "closed_decision_keys": (key,),
                    "full_intents": carrier,
                    "prefix_intents": {key: intent},
                },
            ),
        )
        for reason_id, function, args, kwargs in cases:
            with self.subTest(reason_id=reason_id):
                self.assert_refused_reason(
                    reason_id,
                    function,
                    *args,
                    **kwargs,
                )

    def test_distinguishes_causal_match_from_future_reading_on_common_key(
        self,
    ) -> None:
        timestamp = datetime(2026, 1, 1, tzinfo=timezone.utc)
        key = DecisionKey("BINANCE:BTCUSDT", timestamp)
        causal = self._intent(timestamp, "intent")

        matching = compare_lookahead(
            closed_decision_keys=(key,),
            full_intents={key: causal},
            prefix_intents={key: causal},
        )
        self.assertEqual(matching.intent_mismatch_count, 0)
        self.assertIsNone(matching.first_mismatch_key)

        future_reading = self._intent(timestamp, "intent", "e" * 64)
        mismatching = compare_lookahead(
            closed_decision_keys=(key,),
            full_intents={key: future_reading},
            prefix_intents={key: causal},
        )
        self.assertEqual(mismatching.intent_mismatch_count, 1)
        self.assertEqual(mismatching.first_mismatch_key, key)
        self.assertNotEqual(
            mismatching.first_full_intent_sha256,
            mismatching.first_prefix_intent_sha256,
        )

        self.assert_refused_reason(
            "LOOKAHEAD_DECISION_OUTSIDE_CLOSED_UNIVERSE",
            compare_lookahead,
            closed_decision_keys=(),
            full_intents={key: causal},
            prefix_intents={key: causal},
        )

        class EqualDatetime(datetime):
            def __eq__(self, other: object) -> bool:
                return True

            def __hash__(self) -> int:
                return 0

        full_time = EqualDatetime(2026, 1, 1, tzinfo=timezone.utc)
        prefix_time = EqualDatetime(2026, 1, 1, minute=1, tzinfo=timezone.utc)
        hostile_key = DecisionKey("BINANCE:BTCUSDT", full_time)
        self.assert_refused_reason(
            "INVALID_UTC_DATETIME:decision_key.decision_bar_timestamp_utc",
            compare_lookahead,
            closed_decision_keys=(hostile_key,),
            full_intents={hostile_key: self._intent(full_time, "intent")},
            prefix_intents={
                DecisionKey("BINANCE:BTCUSDT", prefix_time): self._intent(
                    prefix_time, "intent"
                )
            },
        )

    def test_digest_collision_cannot_hide_structural_intent_difference(self) -> None:
        timestamp = datetime(2026, 1, 1, tzinfo=timezone.utc)
        key = DecisionKey("BINANCE:BTCUSDT", timestamp)
        full = self._intent(timestamp, "intent", "e" * 64)
        prefix = self._intent(timestamp, "intent", "d" * 64)
        collided_digest = "f" * 64

        with patch.object(
            p021_evidence_contracts,
            "intent_evidence_sha256",
            return_value=collided_digest,
        ):
            evidence = compare_lookahead(
                closed_decision_keys=(key,),
                full_intents={key: full},
                prefix_intents={key: prefix},
            )

        self.assertEqual(evidence.intent_mismatch_count, 1)
        self.assertEqual(evidence.first_mismatch_key, key)
        self.assertEqual(evidence.first_full_intent_sha256, collided_digest)
        self.assertEqual(evidence.first_prefix_intent_sha256, collided_digest)

    def test_refuses_intent_subclass_that_suppresses_structural_difference(
        self,
    ) -> None:
        class AlwaysEqualIntent(IntentEvidence):
            def __eq__(self, other: object) -> bool:
                return True

            def __ne__(self, other: object) -> bool:
                return False

            __hash__ = IntentEvidence.__hash__

        timestamp = datetime(2026, 1, 1, tzinfo=timezone.utc)
        key = DecisionKey("BINANCE:BTCUSDT", timestamp)
        prefix = self._intent(timestamp, "intent", "d" * 64)
        full = AlwaysEqualIntent(
            **{
                **prefix.__dict__,
                "p012_semantic_payload_sha256": "e" * 64,
            }
        )

        self.assert_refused_reason(
            "INTENT_INVALID_EVIDENCE",
            compare_lookahead,
            closed_decision_keys=(key,),
            full_intents={key: full},
            prefix_intents={key: prefix},
        )

    def test_refuses_hostile_intent_fields_before_equality(self) -> None:
        class HostileString(str):
            def __eq__(self, other: object) -> bool:
                raise RuntimeError("hostile string equality")

            def __ne__(self, other: object) -> bool:
                raise RuntimeError("hostile string equality")

            __hash__ = str.__hash__

        class HostileDatetime(datetime):
            def __eq__(self, other: object) -> bool:
                raise RuntimeError("hostile datetime equality")

            def __ne__(self, other: object) -> bool:
                raise RuntimeError("hostile datetime equality")

            __hash__ = datetime.__hash__

        timestamp = datetime(2026, 1, 1, tzinfo=timezone.utc)
        key = DecisionKey("BINANCE:BTCUSDT", timestamp)
        valid = self._intent(timestamp, "intent")
        mutations = (
            (
                replace(valid, instrument_id=HostileString("BINANCE:BTCUSDT")),
                "INVALID_TEXT:instrument_id",
            ),
            (
                replace(
                    valid,
                    decision_bar_timestamp_utc=HostileDatetime(
                        2026, 1, 1, tzinfo=timezone.utc
                    ),
                ),
                "INVALID_UTC_DATETIME:decision_bar_timestamp_utc",
            ),
        )
        for hostile, reason_id in mutations:
            with self.subTest(reason_id=reason_id):
                self.assert_refused_reason(
                    reason_id,
                    compare_lookahead,
                    closed_decision_keys=(key,),
                    full_intents={key: hostile},
                    prefix_intents={key: valid},
                )

    def test_snapshots_full_records_before_prefix_mapping_mutation(self) -> None:
        timestamp = datetime(2026, 1, 1, tzinfo=timezone.utc)
        full_key = DecisionKey("BINANCE:BTCUSDT", timestamp)
        prefix_key = DecisionKey("BINANCE:BTCUSDT", timestamp)
        full_intent = self._intent(timestamp, "intent", "e" * 64)
        prefix_intent = self._intent(timestamp, "intent", "d" * 64)
        full_digest = intent_evidence_sha256(full_intent)
        prefix_digest = intent_evidence_sha256(prefix_intent)
        self.assertNotEqual(full_digest, prefix_digest)

        class MutatingPrefixMapping(Mapping):
            def __init__(self) -> None:
                self.items_calls = 0

            def __iter__(self):
                return iter((prefix_key,))

            def __len__(self) -> int:
                return 1

            def __getitem__(self, key: object) -> IntentEvidence:
                if key == prefix_key:
                    return prefix_intent
                raise KeyError(key)

            def items(self):
                self.items_calls += 1
                if self.items_calls > 1:
                    raise RuntimeError("items view requested twice")
                object.__setattr__(
                    full_key,
                    "decision_bar_timestamp_utc",
                    datetime(2026, 1, 1, minute=1, tzinfo=timezone.utc),
                )
                object.__setattr__(
                    full_intent,
                    "p012_semantic_payload_sha256",
                    "d" * 64,
                )
                return ((prefix_key, prefix_intent),)

        prefix_mapping = MutatingPrefixMapping()
        evidence = compare_lookahead(
            closed_decision_keys=(full_key,),
            full_intents={full_key: full_intent},
            prefix_intents=prefix_mapping,
        )

        self.assertEqual(prefix_mapping.items_calls, 1)
        self.assertEqual(evidence.intent_mismatch_count, 1)
        self.assertIsNot(evidence.first_mismatch_key, full_key)
        self.assertNotEqual(evidence.first_mismatch_key, full_key)
        self.assertEqual(evidence.first_mismatch_key, prefix_key)
        self.assertEqual(evidence.first_full_intent_sha256, full_digest)
        self.assertEqual(evidence.first_prefix_intent_sha256, prefix_digest)

    def test_snapshots_nested_dataset_before_mapping_mutation(self) -> None:
        timestamp = datetime(2026, 1, 1, tzinfo=timezone.utc)
        key = DecisionKey("BINANCE:BTCUSDT", timestamp)
        full_dataset = DatasetIdentity("ds-v1", "e" * 64)
        full_intent = replace(
            self._intent(timestamp, "intent"),
            dataset_identity=full_dataset,
        )
        prefix_intent = replace(
            self._intent(timestamp, "intent"),
            dataset_identity=DatasetIdentity("ds-v1", "d" * 64),
        )
        full_digest = intent_evidence_sha256(full_intent)
        prefix_digest = intent_evidence_sha256(prefix_intent)
        self.assertNotEqual(full_digest, prefix_digest)

        class MutatingPrefixMapping(Mapping):
            def __init__(self) -> None:
                self.items_calls = 0

            def __iter__(self):
                return iter((key,))

            def __len__(self) -> int:
                return 1

            def __getitem__(self, item: object) -> IntentEvidence:
                if item == key:
                    return prefix_intent
                raise KeyError(item)

            def items(self):
                self.items_calls += 1
                if self.items_calls > 1:
                    raise RuntimeError("items view requested twice")
                object.__setattr__(full_dataset, "digest", "d" * 64)
                return ((key, prefix_intent),)

        prefix_mapping = MutatingPrefixMapping()
        evidence = compare_lookahead(
            closed_decision_keys=(key,),
            full_intents={key: full_intent},
            prefix_intents=prefix_mapping,
        )

        self.assertEqual(prefix_mapping.items_calls, 1)
        self.assertEqual(evidence.intent_mismatch_count, 1)
        self.assertEqual(evidence.first_full_intent_sha256, full_digest)
        self.assertEqual(evidence.first_prefix_intent_sha256, prefix_digest)

    def test_refuses_decision_key_subclasses(self) -> None:
        class DecisionKeySubclass(DecisionKey):
            pass

        timestamp = datetime(2026, 1, 1, tzinfo=timezone.utc)
        key = DecisionKeySubclass("BINANCE:BTCUSDT", timestamp)
        intent = self._intent(timestamp, "intent")

        self.assert_refused_reason(
            "LOOKAHEAD_INVALID_DECISION_KEY",
            compare_lookahead,
            closed_decision_keys=(key,),
            full_intents={key: intent},
            prefix_intents={key: intent},
        )

    def test_refuses_malformed_closed_decision_key_carriers(self) -> None:
        timestamp = datetime(2026, 1, 1, tzinfo=timezone.utc)
        key = DecisionKey("BINANCE:BTCUSDT", timestamp)
        intent = self._intent(timestamp, "intent")
        for carrier in (
            None,
            7,
            "not-a-key-sequence",
            {key: True},
            BrokenIterable(),
        ):
            with self.subTest(carrier=carrier):
                self.assert_refused_reason(
                    "LOOKAHEAD_INVALID_CLOSED_KEYS_CARRIER",
                    compare_lookahead,
                    closed_decision_keys=carrier,
                    full_intents={key: intent},
                    prefix_intents={key: intent},
                )

        class ItemsMapping(Mapping):
            def __init__(self, entries: object) -> None:
                self.entries = entries

            def __iter__(self):
                return iter(())

            def __len__(self) -> int:
                return 0

            def __getitem__(self, key: object) -> object:
                raise KeyError(key)

            def items(self):
                return self.entries

        duplicate = ItemsMapping(
            (
                (key, intent),
                (key, self._intent(timestamp, "evolved-intent")),
            )
        )
        self.assert_refused_reason(
            "LOOKAHEAD_DUPLICATE_INTENT_KEY:full_intents",
            compare_lookahead,
            closed_decision_keys=(key,),
            full_intents=duplicate,
            prefix_intents={key: intent},
        )

        PairSubclass = namedtuple("PairSubclass", ("key", "intent"))
        for hostile_entries in (
            BrokenIterable(),
            ((key,),),
            (PairSubclass(key, intent),),
        ):
            with self.subTest(hostile_entries=hostile_entries):
                self.assert_refused_reason(
                    "LOOKAHEAD_INVALID_MAPPING:full_intents",
                    compare_lookahead,
                    closed_decision_keys=(key,),
                    full_intents=ItemsMapping(hostile_entries),
                    prefix_intents={key: intent},
                )

        class SingleViewMapping(ItemsMapping):
            def __init__(self) -> None:
                super().__init__(((key, intent),))
                self.items_calls = 0

            def items(self):
                self.items_calls += 1
                if self.items_calls > 1:
                    raise RuntimeError("items view requested twice")
                return super().items()

        single_view = SingleViewMapping()
        evidence = compare_lookahead(
            closed_decision_keys=(key,),
            full_intents=single_view,
            prefix_intents={key: intent},
        )
        self.assertEqual(evidence.intent_mismatch_count, 0)
        self.assertEqual(single_view.items_calls, 1)


class ClosedBarReceiptTests(P021ContractTestCase):
    @staticmethod
    def _receipt() -> ClosedBarRuntimeReceipt:
        dataset = DatasetIdentity("ds-v1", "c" * 64)
        return ClosedBarRuntimeReceipt(
            candidate_id="cand-1",
            package_hash="a" * 64,
            deployment_identity_hash="b" * 64,
            dataset_identity=dataset,
            instrument_id="BINANCE:BTCUSDT",
            timeframe="test-timeframe",
            bar_open_timestamp_utc=datetime(2026, 1, 1, tzinfo=timezone.utc),
            bar_close_timestamp_utc=datetime(
                2026, 1, 1, minute=5, tzinfo=timezone.utc
            ),
            decision_timestamp_utc=datetime(
                2026, 1, 1, minute=5, second=1, tzinfo=timezone.utc
            ),
            intent_sha256="d" * 64,
            runtime_producer_id="decision-loop",
            runtime_code_sha256="e" * 64,
            source="RUNTIME_DECISION_LOOP",
        )

    @staticmethod
    def _validate(receipt: ClosedBarRuntimeReceipt) -> ClosedBarRuntimeReceipt:
        return validate_closed_bar_runtime_receipt(
            receipt,
            expected_candidate_id="cand-1",
            expected_package_sha256="a" * 64,
            expected_deployment_identity_sha256="b" * 64,
            expected_dataset_identity=DatasetIdentity("ds-v1", "c" * 64),
            expected_intent_sha256="d" * 64,
            expected_runtime_code_sha256="e" * 64,
            expected_instrument_id="BINANCE:BTCUSDT",
            expected_timeframe="test-timeframe",
            expected_runtime_producer_id="decision-loop",
        )

    def test_refuses_receipt_subclasses_and_mutable_attribute_views(self) -> None:
        class ReceiptSubclass(ClosedBarRuntimeReceipt):
            pass

        class MutableViewReceipt(ClosedBarRuntimeReceipt):
            def __getattribute__(self, name: str) -> object:
                if name == "candidate_id":
                    reads = object.__getattribute__(self, "_candidate_reads")
                    object.__setattr__(self, "_candidate_reads", reads + 1)
                    if reads >= 2:
                        return "other-candidate"
                return super().__getattribute__(name)

        base = self._receipt()
        ordinary_subclass = ReceiptSubclass(**base.__dict__)
        mutable_view = MutableViewReceipt(**base.__dict__)
        object.__setattr__(mutable_view, "_candidate_reads", 0)

        for receipt in (ordinary_subclass, mutable_view):
            with self.subTest(receipt_type=type(receipt).__name__):
                self.assert_refused_reason(
                    "CLOSED_BAR_INVALID_RECEIPT",
                    self._validate,
                    receipt,
                )
        self.assertEqual(
            object.__getattribute__(mutable_view, "_candidate_reads"),
            0,
        )

    def test_requires_runtime_source_and_closed_bar_chronology(self) -> None:
        receipt = self._receipt()
        validated = self._validate(receipt)
        self.assertIs(validated, receipt)

        class ReversingDatetime(datetime):
            def __lt__(self, other: object) -> bool:
                return True

            def __le__(self, other: object) -> bool:
                return True

        self.assert_refused_reason(
            "INVALID_UTC_DATETIME:bar_open_timestamp_utc",
            self._validate,
            replace(
                receipt,
                bar_open_timestamp_utc=ReversingDatetime(
                    2026, 1, 1, minute=10, tzinfo=timezone.utc
                ),
                bar_close_timestamp_utc=ReversingDatetime(
                    2026, 1, 1, minute=5, tzinfo=timezone.utc
                ),
                decision_timestamp_utc=ReversingDatetime(
                    2026, 1, 1, minute=4, tzinfo=timezone.utc
                ),
            ),
        )

        self.assert_refused_reason(
            "CLOSED_BAR_INVALID_RUNTIME_SOURCE",
            self._validate,
            replace(receipt, source="BUILD_ASSERTION"),
        )
        self.assert_refused_reason(
            "CLOSED_BAR_INVALID_CHRONOLOGY",
            self._validate,
            replace(
                receipt,
                bar_close_timestamp_utc=receipt.decision_timestamp_utc.replace(
                    second=2
                ),
            ),
        )
        self.assert_refused_reason(
            "CLOSED_BAR_INVALID_CHRONOLOGY",
            self._validate,
            replace(
                receipt,
                bar_open_timestamp_utc=receipt.bar_close_timestamp_utc,
            ),
        )
        non_utc = timezone(timedelta(hours=1))
        for field_name in (
            "bar_open_timestamp_utc",
            "bar_close_timestamp_utc",
            "decision_timestamp_utc",
        ):
            mutation = replace(
                receipt,
                **{
                    field_name: getattr(receipt, field_name).astimezone(non_utc),
                },
            )
            with self.subTest(field_name=field_name):
                self.assert_refused_reason(
                    f"INVALID_UTC_DATETIME:{field_name}",
                    self._validate,
                    mutation,
                )

    def test_refuses_stateful_timezone_before_chronology(self) -> None:
        class StatefulTimezone(tzinfo):
            def __init__(self, later_offset: timedelta) -> None:
                self.later_offset = later_offset
                self.calls = 0

            def utcoffset(self, value: datetime | None) -> timedelta:
                self.calls += 1
                if self.calls == 1:
                    return timedelta(0)
                return self.later_offset

            def dst(self, value: datetime | None) -> timedelta:
                return timedelta(0)

        open_zone = StatefulTimezone(timedelta(hours=10))
        close_zone = StatefulTimezone(timedelta(0))
        decision_zone = StatefulTimezone(timedelta(hours=-10))
        receipt = replace(
            self._receipt(),
            bar_open_timestamp_utc=datetime(
                2026, 1, 1, minute=10, tzinfo=open_zone
            ),
            bar_close_timestamp_utc=datetime(
                2026, 1, 1, minute=5, tzinfo=close_zone
            ),
            decision_timestamp_utc=datetime(
                2026, 1, 1, minute=4, tzinfo=decision_zone
            ),
        )

        self.assert_refused_reason(
            "INVALID_UTC_DATETIME:bar_open_timestamp_utc",
            self._validate,
            receipt,
        )
        self.assertEqual(
            (open_zone.calls, close_zone.calls, decision_zone.calls),
            (0, 0, 0),
        )

    def test_refuses_each_wrong_runtime_identity(self) -> None:
        receipt = self._receipt()
        mutations = (
            replace(receipt, candidate_id="other-candidate"),
            replace(receipt, package_hash="f" * 64),
            replace(receipt, deployment_identity_hash="f" * 64),
            replace(receipt, dataset_identity=DatasetIdentity("ds-v1", "f" * 64)),
            replace(receipt, instrument_id="other-instrument"),
            replace(receipt, timeframe="other-timeframe"),
            replace(receipt, runtime_producer_id="other-producer"),
            replace(receipt, intent_sha256="f" * 64),
            replace(receipt, runtime_code_sha256="f" * 64),
        )
        for mutation in mutations:
            with self.subTest(mutation=mutation):
                self.assert_refused_reason(
                    "CLOSED_BAR_IDENTITY_MISMATCH",
                    self._validate,
                    mutation,
                )

    def test_binds_instrument_timeframe_and_runtime_producer_identity(self) -> None:
        receipt = self._receipt()
        expected = {
            "expected_candidate_id": "cand-1",
            "expected_package_sha256": "a" * 64,
            "expected_deployment_identity_sha256": "b" * 64,
            "expected_dataset_identity": DatasetIdentity("ds-v1", "c" * 64),
            "expected_intent_sha256": "d" * 64,
            "expected_runtime_code_sha256": "e" * 64,
            "expected_instrument_id": "BINANCE:BTCUSDT",
            "expected_timeframe": "test-timeframe",
            "expected_runtime_producer_id": "decision-loop",
        }
        self.assertIs(
            validate_closed_bar_runtime_receipt(receipt, **expected),
            receipt,
        )
        for field_name in ("instrument_id", "timeframe", "runtime_producer_id"):
            with self.subTest(actual=field_name):
                self.assert_refused_reason(
                    "CLOSED_BAR_IDENTITY_MISMATCH",
                    validate_closed_bar_runtime_receipt,
                    receipt,
                    **{**expected, f"expected_{field_name}": "other"},
                )
        for field_name in ("instrument_id", "timeframe", "runtime_producer_id"):
            with self.subTest(expected=field_name):
                self.assert_refused_reason(
                    "CLOSED_BAR_IDENTITY_MISMATCH",
                    validate_closed_bar_runtime_receipt,
                    replace(receipt, **{field_name: "other"}),
                    **expected,
                )

    def test_refuses_non_builtin_runtime_identity_strings_actual_and_expected(self) -> None:
        receipt = self._receipt()
        expected = {
            "expected_candidate_id": "cand-1",
            "expected_package_sha256": "a" * 64,
            "expected_deployment_identity_sha256": "b" * 64,
            "expected_dataset_identity": DatasetIdentity("ds-v1", "c" * 64),
            "expected_intent_sha256": "d" * 64,
            "expected_runtime_code_sha256": "e" * 64,
            "expected_instrument_id": "BINANCE:BTCUSDT",
            "expected_timeframe": "test-timeframe",
            "expected_runtime_producer_id": "decision-loop",
        }
        for field_name in ("instrument_id", "timeframe", "runtime_producer_id"):
            with self.subTest(actual=field_name):
                self.assert_refused_reason(
                    f"INVALID_TEXT:{field_name}",
                    validate_closed_bar_runtime_receipt,
                    replace(receipt, **{field_name: StringAlias("wrong", getattr(receipt, field_name))}),
                    **expected,
                )
        for field_name in ("instrument_id", "timeframe", "runtime_producer_id"):
            with self.subTest(expected=field_name):
                self.assert_refused_reason(
                    f"INVALID_TEXT:expected_{field_name}",
                    validate_closed_bar_runtime_receipt,
                    receipt,
                    **{**expected, f"expected_{field_name}": StringAlias("wrong", expected[f"expected_{field_name}"])},
                )

    def test_refuses_string_subclasses_across_runtime_identity_boundary(self) -> None:
        receipt = self._receipt()
        actual_mutations = (
            (
                replace(
                    receipt,
                    source=StringAlias(
                        "BUILD_ASSERTION", "RUNTIME_DECISION_LOOP"
                    ),
                ),
                "CLOSED_BAR_INVALID_RUNTIME_SOURCE",
            ),
            (
                replace(
                    receipt,
                    candidate_id=StringAlias("other", "cand-1"),
                ),
                "INVALID_TEXT:candidate_id",
            ),
            (
                replace(
                    receipt,
                    package_hash=StringAlias("f" * 64, "a" * 64),
                ),
                "INVALID_SHA256:package_hash",
            ),
            (
                replace(
                    receipt,
                    deployment_identity_hash=StringAlias("f" * 64, "b" * 64),
                ),
                "INVALID_SHA256:deployment_identity_hash",
            ),
            (
                replace(
                    receipt,
                    dataset_identity=DatasetIdentity(
                        "ds-v1", StringAlias("f" * 64, "c" * 64)
                    ),
                ),
                "INVALID_SHA256:dataset.digest",
            ),
            (
                replace(
                    receipt,
                    intent_sha256=StringAlias("f" * 64, "d" * 64),
                ),
                "INVALID_SHA256:intent_sha256",
            ),
            (
                replace(
                    receipt,
                    runtime_code_sha256=StringAlias("f" * 64, "e" * 64),
                ),
                "INVALID_SHA256:runtime_code_sha256",
            ),
        )
        for mutation, reason_id in actual_mutations:
            with self.subTest(reason_id=reason_id):
                self.assert_refused_reason(reason_id, self._validate, mutation)

        expected = {
            "expected_candidate_id": "cand-1",
            "expected_package_sha256": "a" * 64,
            "expected_deployment_identity_sha256": "b" * 64,
            "expected_dataset_identity": DatasetIdentity("ds-v1", "c" * 64),
            "expected_intent_sha256": "d" * 64,
            "expected_runtime_code_sha256": "e" * 64,
            "expected_instrument_id": "BINANCE:BTCUSDT",
            "expected_timeframe": "test-timeframe",
            "expected_runtime_producer_id": "decision-loop",
        }
        expected_aliases = (
            (
                "expected_candidate_id",
                StringAlias("other", "cand-1"),
                "INVALID_TEXT:expected_candidate_id",
            ),
            (
                "expected_package_sha256",
                StringAlias("f" * 64, "a" * 64),
                "INVALID_SHA256:expected_package_sha256",
            ),
            (
                "expected_deployment_identity_sha256",
                StringAlias("f" * 64, "b" * 64),
                "INVALID_SHA256:expected_deployment_identity_sha256",
            ),
            (
                "expected_dataset_identity",
                DatasetIdentity("ds-v1", StringAlias("f" * 64, "c" * 64)),
                "INVALID_SHA256:dataset.digest",
            ),
            (
                "expected_intent_sha256",
                StringAlias("f" * 64, "d" * 64),
                "INVALID_SHA256:expected_intent_sha256",
            ),
            (
                "expected_runtime_code_sha256",
                StringAlias("f" * 64, "e" * 64),
                "INVALID_SHA256:expected_runtime_code_sha256",
            ),
            (
                "expected_instrument_id",
                StringAlias("other", "BINANCE:BTCUSDT"),
                "INVALID_TEXT:expected_instrument_id",
            ),
            (
                "expected_timeframe",
                StringAlias("other", "test-timeframe"),
                "INVALID_TEXT:expected_timeframe",
            ),
            (
                "expected_runtime_producer_id",
                StringAlias("other", "decision-loop"),
                "INVALID_TEXT:expected_runtime_producer_id",
            ),
        )
        for field_name, value, reason_id in expected_aliases:
            inputs = {**expected, field_name: value}
            with self.subTest(field_name=field_name):
                self.assert_refused_reason(
                    reason_id,
                    validate_closed_bar_runtime_receipt,
                    receipt,
                    **inputs,
                )


if __name__ == "__main__":
    unittest.main()
