"""Synthetic, local-only checks for bundle quality timeframe handling."""

from __future__ import annotations

import csv
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

import create_optimization_data_bundle as subject


BASE_TIME = datetime(2026, 1, 1, tzinfo=timezone.utc)


def rows_at(*offsets: int) -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": (BASE_TIME + timedelta(seconds=offset)).isoformat(),
            "open": 10,
            "high": 12,
            "low": 9,
            "close": 11,
            "volume": 1,
        }
        for offset in offsets
    ]


class QualityTimeframeTests(unittest.TestCase):
    def validate(self, offsets: tuple[int, ...], timeframe: str):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name) / "synthetic_bundle"
        result = subject.validate_quality("SYNTHETIC", rows_at(*offsets), timeframe, root)
        gap_path = root / result["gap_report_path"]
        with gap_path.open("r", encoding="utf-8", newline="") as handle:
            gaps = list(csv.DictReader(handle))
        return result, gaps

    def test_5m_supports_complete_and_gapped_rows(self) -> None:
        complete, complete_gaps = self.validate((0, 300, 600), "5m")
        self.assertFalse(complete["has_gaps"])
        self.assertEqual(complete_gaps, [])

        gapped, gaps = self.validate((0, 300, 900), "5m")
        self.assertTrue(gapped["has_gaps"])
        self.assertEqual(gapped["gap_count"], 1)
        self.assertEqual(len(gaps), 1)
        self.assertEqual(gaps[0]["delta_seconds"], "600")
        self.assertEqual(gaps[0]["missing_bars_estimate"], "1")

    def test_5m_fractional_step_missing_count_rounds(self) -> None:
        result, gaps = self.validate((0, 570), "5m")
        self.assertEqual(result["gap_count"], 1)
        self.assertEqual(gaps[0]["delta_seconds"], "570")
        self.assertEqual(gaps[0]["missing_bars_estimate"], "1")

    def test_15m_fractional_step_missing_count_rounds(self) -> None:
        result, gaps = self.validate((0, 1710), "15m")
        self.assertEqual(result["gap_count"], 1)
        self.assertEqual(gaps[0]["delta_seconds"], "1710")
        self.assertEqual(gaps[0]["missing_bars_estimate"], "1")

    def test_unknown_timeframe_refuses_before_artifacts(self) -> None:
        for rows in ([], rows_at(0)):
            with self.subTest(row_count=len(rows)), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary) / "synthetic_bundle"
                with self.assertRaisesRegex(ValueError, "^unsupported timeframe: bogus$"):
                    subject.validate_quality("SYNTHETIC", rows, "bogus", root)
                self.assertFalse(root.exists())

    def test_gap_threshold_remains_strictly_above_one_point_five_steps(self) -> None:
        exact, exact_gaps = self.validate((0, 1350), "15m")
        self.assertFalse(exact["has_gaps"])
        self.assertEqual(exact_gaps, [])

        above, above_gaps = self.validate((0, 1351), "15m")
        self.assertTrue(above["has_gaps"])
        self.assertEqual(above_gaps[0]["missing_bars_estimate"], "1")

    def test_existing_named_timeframes_keep_complete_and_gapped_results(self) -> None:
        self.assertEqual(subject.EXPECTED_TIMEFRAMES, ["15m", "1h", "2h", "4h", "1D"])
        for timeframe, step in {
            "15m": 900,
            "1h": 3600,
            "2h": 7200,
            "4h": 14400,
            "1D": 86400,
        }.items():
            with self.subTest(timeframe=timeframe, shape="complete"):
                complete, complete_gaps = self.validate((0, step, 2 * step), timeframe)
                self.assertFalse(complete["has_gaps"])
                self.assertEqual(complete_gaps, [])
            with self.subTest(timeframe=timeframe, shape="gapped"):
                gapped, gaps = self.validate((0, step, 3 * step), timeframe)
                self.assertEqual(gapped["gap_count"], 1)
                self.assertEqual(gaps[0]["missing_bars_estimate"], "1")

    def test_sorting_duplicate_and_ohlc_meanings_remain(self) -> None:
        rows = rows_at(600, 0, 300, 300)
        rows[-1].update({"high": 8, "low": 9})
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "synthetic_bundle"
            result = subject.validate_quality("SYNTHETIC", rows, "5m", root)
        self.assertFalse(result["has_gaps"])
        self.assertEqual(result["duplicate_timestamp_count"], 1)
        self.assertEqual(result["ohlcv_validation_status"], "FAIL")
        self.assertEqual(result["invalid_ohlcv_count"], 3)


if __name__ == "__main__":
    unittest.main(verbosity=2)
