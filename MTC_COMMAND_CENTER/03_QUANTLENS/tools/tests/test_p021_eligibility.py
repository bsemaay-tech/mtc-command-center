from __future__ import annotations

import unittest
from collections import UserString, namedtuple
from dataclasses import replace
from datetime import datetime, timedelta, timezone
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
    "gap_ratio_max",
    "divergence_tolerance",
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
        self.assertEqual(len(record["open_numbers"]), 4)
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


class ControlAllowanceTests(P021ContractTestCase):
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

    def test_refuses_each_wrong_runtime_identity(self) -> None:
        receipt = self._receipt()
        mutations = (
            replace(receipt, candidate_id="other-candidate"),
            replace(receipt, package_hash="f" * 64),
            replace(receipt, deployment_identity_hash="f" * 64),
            replace(receipt, dataset_identity=DatasetIdentity("ds-v1", "f" * 64)),
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
