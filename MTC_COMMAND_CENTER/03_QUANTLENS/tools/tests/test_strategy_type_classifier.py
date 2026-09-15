from __future__ import annotations

import copy
import math
import sys
import unittest
from pathlib import Path


TOOLS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TOOLS))

from strategy_type_classifier import classify_holding_hours  # noqa: E402
from strategy_type_policy_set import compute_policy_version  # noqa: E402


def policy_fixture() -> dict:
    policy = {
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
        "types": {name: {"trade_count_min": None, "forward_trade_count_min": None, "forward_period_days": None} for name in ("day", "swing", "position")},
        "shared": {name: None for name in (
            "single_trade_loss_risk_unit_multiple_max", "stop_loss_ceiling_equity_fraction",
            "normal_market_condition_count_min", "occupancy_min", "trades_per_condition_min",
            "gap_ratio_max", "divergence_tolerance", "divergence_window_length_days",
            "divergence_min_paired_observations",
        )},
        "methods": {
            "regime_method_version": "rule_based_market_regime_v2",
            "gap_method_version": "data_gap_ratio_m2_v1",
            "divergence_method_version": "p021_divergence_v1",
        },
        "provenance": {},
        "version": "",
    }
    policy["version"] = compute_policy_version(policy)
    return policy


class StrategyTypeClassifierTests(unittest.TestCase):
    def test_independently_specified_classification_fixtures(self) -> None:
        cases = (
            ("day repeated pattern", [2, 1.5, 3, 2.5, 1, 2] * 2, "day", None, 2.0, 1.0),
            ("six-trade sample", [2, 1.5, 3, 2.5, 1, 2], None, "BLOCKED_INSUFFICIENT_SAMPLE", 2.0, 1.0),
            ("mixed thirds", [2] * 4 + [30] * 4 + [800] * 4, None, "BLOCKED_MIXED_HOLDING_PROFILE", 30.0, 1 / 3),
            ("24 strict boundary", [24] * 10, "swing", None, 24.0, 1.0),
            ("720 strict boundary", [720] * 10, "position", None, 720.0, 1.0),
            ("zero median", [0] * 10, None, "BLOCKED_UNMEASURABLE_HOLD", 0.0, 1.0),
            ("dominance at threshold", [2] * 8 + [30] * 2, "day", None, 2.0, 0.8),
            ("dominance below threshold", [2] * 7 + [30] * 3, None, "BLOCKED_MIXED_HOLDING_PROFILE", 2.0, 0.7),
        )
        for label, values, expected_type, refusal, expected_median, expected_dominance in cases:
            with self.subTest(label=label):
                result = classify_holding_hours(values, policy_fixture())
                self.assertEqual(result["strategy_type"], expected_type)
                self.assertEqual(result["refusal_code"], refusal)
                self.assertEqual(result["median_hold_hours"], expected_median)
                self.assertAlmostEqual(result["dominance"], expected_dominance)
                self.assertEqual(result["result_kind"], "P021_STRATEGY_TYPE_CLASSIFICATION_ONLY")
                self.assertNotIn("ready", result)

    def test_negative_precedes_short_sample(self) -> None:
        result = classify_holding_hours([-1, 2], policy_fixture())
        self.assertEqual(result["refusal_code"], "BLOCKED_NEGATIVE_HOLD")
        self.assertEqual(result["sample_count"], 1)

    def test_large_finite_even_sample_has_finite_median(self) -> None:
        result = classify_holding_hours([1e308] * 10, policy_fixture())
        self.assertEqual(result["status"], "CLASSIFIED")
        self.assertEqual(result["median_hold_hours"], 1e308)
        self.assertTrue(math.isfinite(result["median_hold_hours"]))

    def test_classifier_consumes_caller_taxonomy_values(self) -> None:
        policy = policy_fixture()
        policy["taxonomy"]["day_max_hours"] = 10.0
        policy["taxonomy"]["swing_max_hours"] = 100.0
        policy["version"] = compute_policy_version(policy)
        self.assertEqual(classify_holding_hours([10] * 10, policy)["strategy_type"], "swing")
        self.assertEqual(classify_holding_hours([100] * 10, policy)["strategy_type"], "position")

    def test_nonfinite_bool_and_non_number_refuse(self) -> None:
        for value in (True, float("nan"), "2"):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    classify_holding_hours([value], policy_fixture())


if __name__ == "__main__":
    unittest.main()
