from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path


TOOLS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TOOLS))

import p021_readiness_rules  # noqa: E402
from strategy_type_policy_set import (  # noqa: E402
    PolicySetError,
    compute_policy_version,
    validate_policy_set,
)


ACCEPTED_ARTIFACT_FIXTURE = {
    "schema": "p021.strategy_type_policy_set/v1",
    "policy_id": "p021-evidence-policy",
    "profile": "balanced",
    "taxonomy": {
        "day_max_hours": 24.0,
        "swing_max_hours": 720.0,
        "dominance_min": 0.8,
        "sample_min": 10,
        "unmeasurable_hold_median_hours": 0.0,
        "classified_unit": "strategy_id|asset|timeframe|variant|parameter_set",
    },
    "types": {
        "day": {"trade_count_min": 30, "forward_trade_count_min": 20, "forward_period_days": 21},
        "swing": {"trade_count_min": 30, "forward_trade_count_min": 12, "forward_period_days": 119},
        "position": {"trade_count_min": 12, "forward_trade_count_min": 12, "forward_period_days": 364},
    },
    "shared": {
        "single_trade_loss_risk_unit_multiple_max": 1,
        "stop_loss_ceiling_equity_fraction": 0.005,
        "normal_market_condition_count_min": 2,
        "occupancy_min": 0.1,
        "trades_per_condition_min": 3,
        "gap_ratio_max": None,
        "divergence_tolerance": None,
        "divergence_window_length_days": None,
        "divergence_min_paired_observations": None,
    },
    "methods": {
        "regime_method_version": "rule_based_market_regime_v2",
        "gap_method_version": "data_gap_ratio_m2_v1",
        "divergence_method_version": "p021_divergence_v1",
    },
    # Compatibility fixture only: the packet's detailed provenance was historical.
    "provenance": {},
    "version": "p021pol-v1:4a807136e78650ef393556f91d3448855fc397ee9f0eee6efb7594c9dbdf69f2",
}


class PolicySetTests(unittest.TestCase):
    def test_accepted_artifact_hash_is_reproduced(self) -> None:
        self.assertEqual(compute_policy_version(ACCEPTED_ARTIFACT_FIXTURE), ACCEPTED_ARTIFACT_FIXTURE["version"])
        self.assertEqual(validate_policy_set(ACCEPTED_ARTIFACT_FIXTURE), ACCEPTED_ARTIFACT_FIXTURE["version"])

    def test_hash_uses_recursive_float_hex_and_excludes_version_and_provenance(self) -> None:
        changed_provenance = copy.deepcopy(ACCEPTED_ARTIFACT_FIXTURE)
        changed_provenance["provenance"] = {"historical": True}
        changed_provenance["version"] = "ignored while computing"
        self.assertEqual(compute_policy_version(changed_provenance), ACCEPTED_ARTIFACT_FIXTURE["version"])
        changed_value = copy.deepcopy(ACCEPTED_ARTIFACT_FIXTURE)
        changed_value["taxonomy"]["dominance_min"] = 0.75
        self.assertNotEqual(compute_policy_version(changed_value), ACCEPTED_ARTIFACT_FIXTURE["version"])

    def test_missing_required_key_and_hash_mutation_refuse(self) -> None:
        missing = copy.deepcopy(ACCEPTED_ARTIFACT_FIXTURE)
        del missing["shared"]["gap_ratio_max"]
        with self.assertRaisesRegex(PolicySetError, "gap_ratio_max"):
            validate_policy_set(missing)
        changed = copy.deepcopy(ACCEPTED_ARTIFACT_FIXTURE)
        changed["taxonomy"]["sample_min"] = 11
        with self.assertRaisesRegex(PolicySetError, "version mismatch"):
            validate_policy_set(changed)

    def test_nullable_fields_remain_valid_unset(self) -> None:
        policy = copy.deepcopy(ACCEPTED_ARTIFACT_FIXTURE)
        for block in policy["types"].values():
            for key in block:
                block[key] = None
        for key in policy["shared"]:
            policy["shared"][key] = None
        policy["version"] = compute_policy_version(policy)
        self.assertEqual(validate_policy_set(policy), policy["version"])
        self.assertIsNone(policy["shared"]["gap_ratio_max"])
        # Catalogue-only S2 closure: the accepted artifact still carries None here until B-22
        # ratifies the whole set (the catalogue value is 0.0001 - see test_current_readiness_catalogue_stays_refused).

    def test_nonfinite_bool_and_unsupported_json_values_refuse(self) -> None:
        for label, path, value in (
            ("bool", ("taxonomy", "day_max_hours"), True),
            ("nonfinite", ("taxonomy", "day_max_hours"), float("inf")),
            ("unsupported", ("provenance", "bad"), object()),
        ):
            with self.subTest(label=label):
                policy = copy.deepcopy(ACCEPTED_ARTIFACT_FIXTURE)
                policy[path[0]][path[1]] = value
                if label in {"nonfinite", "unsupported"}:
                    with self.assertRaises(PolicySetError):
                        compute_policy_version({**policy, "bad": value})
                else:
                    policy["version"] = compute_policy_version(policy)
                    with self.assertRaises(PolicySetError):
                        validate_policy_set(policy)

    def test_current_readiness_catalogue_stays_refused(self) -> None:
        record = p021_readiness_rules.readiness_record()
        self.assertFalse(record["ready"])
        self.assertEqual(record["status"], "REFUSED")
        self.assertEqual({item["name"] for item in record["open_numbers"]}, {
            "divergence_tolerance",
            "divergence_window_length",
            "divergence_min_paired_observations",
        })


if __name__ == "__main__":
    unittest.main()
