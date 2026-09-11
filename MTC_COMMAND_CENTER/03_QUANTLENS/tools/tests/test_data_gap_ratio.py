from __future__ import annotations

import math
import sys
import unittest
from pathlib import Path


TOOLS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TOOLS))

from data_gap_ratio import measure_data_gaps  # noqa: E402
from strategy_type_policy_set import compute_policy_version  # noqa: E402


def policy_fixture(gap_method_version: str = "data_gap_ratio_m2_v1") -> dict:
    policy = {
        "schema": "p021.strategy_type_policy_set/v1",
        "policy_id": "p021-evidence-policy",
        "profile": "balanced",
        "taxonomy": {
            "day_max_hours": 24.0, "swing_max_hours": 720.0, "dominance_min": 0.8,
            "sample_min": 10, "unmeasurable_hold_median_hours": 0.0,
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
            "gap_method_version": gap_method_version,
            "divergence_method_version": "p021_divergence_v1",
        },
        "provenance": {},
        "version": "",
    }
    policy["version"] = compute_policy_version(policy)
    return policy


class DataGapRatioTests(unittest.TestCase):
    def assert_ratio(self, actual: float, expected: float) -> None:
        self.assertTrue(math.isclose(actual, expected, rel_tol=1e-12, abs_tol=1e-12), (actual, expected))

    def test_independently_specified_gap_fixtures(self) -> None:
        cases = (
            ("one hourly hole", [0, 3600, 7200, 14400, 18000], "1h", 0.25, 1 / 6, 0.2),
            ("one fifteen-minute hole", [0, 900, 2700, 3600], "15m", 1 / 3, 0.2, 0.25),
        )
        for label, timestamps, timeframe, m1, m2, m3 in cases:
            with self.subTest(label=label):
                result = measure_data_gaps(timestamps, timeframe, policy_fixture())
                self.assert_ratio(result["m1_gap_event_ratio"], m1)
                self.assert_ratio(result["m2_missing_bar_ratio"], m2)
                self.assert_ratio(result["m3_missing_time_ratio"], m3)
                self.assertEqual(result["max_gap_bars"], 1)
                self.assertFalse(result["series_clean"])
                self.assertEqual(result["result_kind"], "P021_DATA_GAP_MEASUREMENT_ONLY")
                self.assertNotIn("ready", result)

    def test_one_point_nine_steps_rounds_to_one_missing_bar(self) -> None:
        result = measure_data_gaps([0, 570], "5m", policy_fixture())
        self.assertEqual(result["missing_bar_count"], 1)
        self.assertEqual(result["expected_bars"], 3)
        self.assert_ratio(result["m2_missing_bar_ratio"], 1 / 3)
        self.assertEqual(result["irregular_interval_count"], 1)

    def test_nonintegral_step_has_exact_diagnostic_without_becoming_a_gap(self) -> None:
        result = measure_data_gaps([0, 300.0000000001], "5m", policy_fixture())
        self.assertEqual(result["gap_event_count"], 0)
        self.assertEqual(result["m2_missing_bar_ratio"], 0)
        self.assertEqual(result["irregular_interval_count"], 1)
        self.assertFalse(result["series_clean"])

    def test_derived_timestamp_arithmetic_must_remain_finite(self) -> None:
        cases = (
            ("delta overflow", [-1e308, 1e308]),
            ("missing-time accumulation overflow", [0, 1e308, 0, 1e308]),
            ("missing-time ratio overflow", [0, 1e308, 0, 1e-308]),
        )
        for label, timestamps in cases:
            with self.subTest(label=label):
                with self.assertRaises(ValueError):
                    measure_data_gaps(timestamps, "5m", policy_fixture())

    def test_leading_and_trailing_absence_are_not_added(self) -> None:
        result = measure_data_gaps([3_600, 7_200, 10_800], "1h", policy_fixture())
        self.assertEqual(result["expected_bars"], 3)
        self.assertEqual(result["missing_bar_count"], 0)
        self.assertTrue(result["series_clean"])

    def test_duplicate_order_and_early_diagnostics_never_look_clean(self) -> None:
        result = measure_data_gaps([0, 300, 300, 250, 400, 900], "5m", policy_fixture())
        self.assertEqual(result["duplicate_timestamp_count"], 1)
        self.assertEqual(result["out_of_order_interval_count"], 1)
        self.assertEqual(result["early_interval_count"], 1)
        self.assertGreater(result["irregular_interval_count"], 0)
        self.assertFalse(result["series_clean"])

    def test_unknown_method_timeframe_undefined_and_invalid_inputs_refuse(self) -> None:
        cases = (
            ("method", lambda: measure_data_gaps([0, 300], "5m", policy_fixture("future_method"))),
            ("timeframe", lambda: measure_data_gaps([0, 300], "1m", policy_fixture())),
            ("empty", lambda: measure_data_gaps([], "5m", policy_fixture())),
            ("singleton", lambda: measure_data_gaps([0], "5m", policy_fixture())),
            ("nonpositive span", lambda: measure_data_gaps([1, 0], "5m", policy_fixture())),
            ("bool", lambda: measure_data_gaps([0, True], "5m", policy_fixture())),
            ("nonfinite", lambda: measure_data_gaps([0, float("inf")], "5m", policy_fixture())),
        )
        for label, call in cases:
            with self.subTest(label=label):
                with self.assertRaises(ValueError):
                    call()


if __name__ == "__main__":
    unittest.main()
