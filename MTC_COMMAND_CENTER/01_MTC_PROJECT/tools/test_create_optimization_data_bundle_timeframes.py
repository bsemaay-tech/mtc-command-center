"""Synthetic, local-only checks for bundle quality timeframe handling."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone, tzinfo
from pathlib import Path
from unittest import mock

QUANTLENS_TOOLS = Path(__file__).resolve().parents[2] / "03_QUANTLENS" / "tools"
sys.path.insert(0, str(QUANTLENS_TOOLS))

import create_optimization_data_bundle as subject
from strategy_type_policy_set import compute_policy_version


BASE_TIME = datetime(2026, 1, 1, tzinfo=timezone.utc)


class SemanticNaiveTimezone(tzinfo):
    def utcoffset(self, value):
        return None


class StateChangingTimezone(tzinfo):
    def __init__(self) -> None:
        self.calls = 0

    def utcoffset(self, value):
        self.calls += 1
        return timedelta(0) if self.calls == 1 else None


def gap_policy_fixture() -> dict:
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
        "types": {
            name: {
                "trade_count_min": None,
                "forward_trade_count_min": None,
                "forward_period_days": None,
            }
            for name in ("day", "swing", "position")
        },
        "shared": {
            name: None
            for name in (
                "single_trade_loss_risk_unit_multiple_max",
                "stop_loss_ceiling_equity_fraction",
                "normal_market_condition_count_min",
                "occupancy_min",
                "trades_per_condition_min",
                "gap_ratio_max",
                "divergence_tolerance",
                "divergence_window_length_days",
                "divergence_min_paired_observations",
            )
        },
        "methods": {
            "regime_method_version": "rule_based_market_regime_v2",
            "gap_method_version": "data_gap_ratio_m2_v1",
            "divergence_method_version": "p021_divergence_v1",
        },
        "provenance": {"fixture": "synthetic-only"},
        "version": "",
    }
    policy["version"] = compute_policy_version(policy)
    return policy


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


def write_source_csv(path: Path, rows: list[dict[str, object]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=["time", "open", "high", "low", "close", "volume"]
        )
        writer.writeheader()
        writer.writerows(
            [
                {
                    "time": row["timestamp_utc"],
                    **{
                        key: row[key]
                        for key in ("open", "high", "low", "close", "volume")
                    },
                }
                for row in rows
            ]
        )


class QualityTimeframeTests(unittest.TestCase):
    def test_build_preserves_source_order_for_h1_and_sorts_emitted_rows(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            archive = root / "archive"
            archive.mkdir()
            source_path = archive / "BINANCE_BTCUSDT,5m_fixture.csv"
            write_source_csv(source_path, rows_at(0, 600, 300, 900))
            args = argparse.Namespace(
                repo_root=root / "repo",
                bundle_parent=root / "bundle-parent",
                archive_root=archive,
                datasets_root=root / "absent",
                date_token="fixture",
                closed_candle_cutoff_utc=BASE_TIME + timedelta(seconds=1200),
                gap_policy=gap_policy_fixture(),
            )

            with mock.patch.object(
                subject, "measure_data_gaps", wraps=subject.measure_data_gaps
            ) as h1_measure, mock.patch.object(
                subject, "prepare_dataset_evidence", wraps=subject.prepare_dataset_evidence
            ) as prepare:
                subject.build_bundle(args)

            self.assertEqual(h1_measure.call_count, 1)
            source_offsets = [
                datetime.fromisoformat(row["timestamp_utc"]).timestamp()
                - BASE_TIME.timestamp()
                for row in prepare.call_args.args[0]
            ]
            self.assertEqual(source_offsets, [0.0, 600.0, 300.0, 900.0])
            bundle_root = (
                root / "bundle-parent" / "MTC_V2_OPTIMIZATION_DATA_BUNDLE_fixture"
            )
            manifest = json.loads(
                (bundle_root / "DATA_BUNDLE_MANIFEST.json").read_text(encoding="utf-8")
            )["datasets"][0]
            self.assertEqual(
                manifest["gap_measurement"]["out_of_order_interval_count"], 1
            )
            normalized_path = bundle_root / manifest["normalized_path"]
            with normalized_path.open("r", encoding="utf-8", newline="") as handle:
                emitted = list(csv.DictReader(handle))
            self.assertEqual(
                [row["timestamp_utc"] for row in emitted],
                [
                    "2026-01-01T00:00:00Z",
                    "2026-01-01T00:05:00Z",
                    "2026-01-01T00:10:00Z",
                    "2026-01-01T00:15:00Z",
                ],
            )

    def test_yaml_serializes_dataset_identity_as_nested_mapping(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "manifest.yml"
            subject.write_simple_yaml(
                path,
                {
                    "datasets": [
                        {
                            "dataset_id": "SYNTHETIC",
                            "dataset_hash": {
                                "contract": "ds-v1",
                                "digest": "f" * 64,
                            },
                        }
                    ]
                },
            )
            lines = path.read_text(encoding="utf-8").splitlines()

        self.assertIn("    dataset_hash:", lines)
        self.assertIn('      contract: "ds-v1"', lines)
        self.assertIn(f'      digest: "{"f" * 64}"', lines)
        self.assertFalse(any("{'contract':" in line for line in lines))

    def test_build_refuses_invalid_closed_ohlcv_before_dataset_emission(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            archive = root / "archive"
            archive.mkdir()
            source_path = archive / "BINANCE_BTCUSDT,5m_fixture.csv"
            invalid_rows = rows_at(0, 300)
            invalid_rows[0]["volume"] = -1
            write_source_csv(source_path, invalid_rows)
            args = argparse.Namespace(
                repo_root=root / "repo",
                bundle_parent=root / "bundle-parent",
                archive_root=archive,
                datasets_root=root / "absent",
                date_token="fixture",
                closed_candle_cutoff_utc=BASE_TIME + timedelta(seconds=600),
                gap_policy=gap_policy_fixture(),
            )

            with mock.patch.object(
                subject,
                "validate_quality",
                side_effect=AssertionError("invalid evidence reached quality emission"),
            ):
                with self.assertRaisesRegex(
                    ValueError, "^semantically invalid closed OHLCV refuses bundle emission$"
                ):
                    subject.build_bundle(args)

            bundle_parent = root / "bundle-parent"
            self.assertEqual(list(bundle_parent.rglob("normalized/**/*.csv")), [])
            self.assertEqual(
                [
                    path
                    for path in bundle_parent.rglob("*")
                    if path.is_file() and "manifest" in path.name.lower()
                ],
                [],
            )

    def test_build_refuses_source_without_volume(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            archive = root / "archive"
            archive.mkdir()
            source_path = archive / "BINANCE_BTCUSDT,5m_fixture.csv"
            with source_path.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(
                    handle, fieldnames=["time", "open", "high", "low", "close"]
                )
                writer.writeheader()
                for row in rows_at(0, 300):
                    writer.writerow(
                        {
                            "time": row["timestamp_utc"],
                            **{
                                key: row[key]
                                for key in ("open", "high", "low", "close")
                            },
                        }
                    )
            args = argparse.Namespace(
                repo_root=root / "repo",
                bundle_parent=root / "bundle-parent",
                archive_root=archive,
                datasets_root=root / "absent",
                date_token="fixture",
                closed_candle_cutoff_utc=BASE_TIME + timedelta(seconds=600),
                gap_policy=gap_policy_fixture(),
            )

            with mock.patch.object(
                subject,
                "validate_quality",
                side_effect=AssertionError("volume-less rows reached quality"),
            ) as validate:
                with self.assertRaisesRegex(ValueError, "^row 1 volume is required$"):
                    subject.build_bundle(args)

            validate.assert_not_called()
            self.assertFalse((root / "bundle-parent").exists())
            self.assertFalse((root / "repo").exists())

    def test_explicit_evidence_inputs_refuses_timezone_naive_string_cutoff(self) -> None:
        args = argparse.Namespace(
            closed_candle_cutoff_utc="2026-01-01T00:10:00",
            gap_policy=gap_policy_fixture(),
        )
        with self.assertRaisesRegex(
            ValueError,
            "^closed_candle_cutoff_utc must be a timezone-aware timestamp$",
        ):
            subject.explicit_evidence_inputs(args)

    def test_prepare_dataset_evidence_refuses_semantically_naive_cutoff(self) -> None:
        with self.assertRaisesRegex(
            ValueError,
            "^closed_candle_cutoff_utc must be timezone-aware$",
        ):
            subject.prepare_dataset_evidence(
                rows_at(-86400, -86100),
                instrument_id="BINANCE:BTCUSDT",
                timeframe="5m",
                closed_candle_cutoff_utc=datetime(
                    2026, 1, 1, 0, 10, tzinfo=SemanticNaiveTimezone()
                ),
                gap_policy=gap_policy_fixture(),
            )

    def test_prepare_dataset_evidence_refuses_state_changing_timezone(self) -> None:
        carrier = StateChangingTimezone()
        with self.assertRaisesRegex(
            ValueError,
            "^closed_candle_cutoff_utc must be timezone-aware$",
        ):
            subject.prepare_dataset_evidence(
                rows_at(-86400, -86100),
                instrument_id="BINANCE:BTCUSDT",
                timeframe="5m",
                closed_candle_cutoff_utc=datetime(
                    2026, 1, 1, 0, 10, tzinfo=carrier
                ),
                gap_policy=gap_policy_fixture(),
            )
        self.assertEqual(carrier.calls, 0)

    def test_explicit_evidence_inputs_stabilizes_hostile_timezone_refusal(self) -> None:
        class HostileTimezone(tzinfo):
            def utcoffset(self, value):
                raise RuntimeError("hostile timezone")

        args = argparse.Namespace(
            closed_candle_cutoff_utc=datetime(
                2026, 1, 1, 0, 10, tzinfo=HostileTimezone()
            ),
            gap_policy=gap_policy_fixture(),
        )
        with self.assertRaisesRegex(
            ValueError,
            "^closed_candle_cutoff_utc must be a timezone-aware timestamp$",
        ):
            subject.explicit_evidence_inputs(args)

    def test_explicit_evidence_inputs_preserves_builtin_fixed_offset(self) -> None:
        args = argparse.Namespace(
            closed_candle_cutoff_utc=datetime(
                2026, 1, 1, 3, 10, tzinfo=timezone(timedelta(hours=3))
            ),
            gap_policy=gap_policy_fixture(),
        )

        cutoff, _ = subject.explicit_evidence_inputs(args)

        self.assertEqual(cutoff, datetime(2026, 1, 1, 0, 10, tzinfo=timezone.utc))
        self.assertIs(cutoff.tzinfo, timezone.utc)

    def test_build_refuses_timezone_naive_datetime_before_any_write(self) -> None:
        args = argparse.Namespace(
            repo_root="unused",
            bundle_parent="unused",
            archive_root="unused",
            datasets_root="unused",
            date_token="fixture",
            closed_candle_cutoff_utc=datetime(2026, 1, 1, 0, 10),
            gap_policy=gap_policy_fixture(),
        )
        with self.assertRaisesRegex(
            ValueError,
            "^closed_candle_cutoff_utc must be a timezone-aware timestamp$",
        ):
            subject.explicit_evidence_inputs(args)
        with mock.patch.object(
            subject.Path,
            "mkdir",
            side_effect=AssertionError("write boundary reached"),
        ) as mkdir, mock.patch.object(subject, "write_csv") as write_csv:
            with self.assertRaisesRegex(
                ValueError,
                "^closed_candle_cutoff_utc must be a timezone-aware timestamp$",
            ):
                subject.build_bundle(args)
        mkdir.assert_not_called()
        write_csv.assert_not_called()

    def test_build_refuses_semantically_naive_datetime_before_any_write(self) -> None:
        args = argparse.Namespace(
            repo_root="unused",
            bundle_parent="unused",
            archive_root="unused",
            datasets_root="unused",
            date_token="fixture",
            closed_candle_cutoff_utc=datetime(
                2026, 1, 1, 0, 10, tzinfo=SemanticNaiveTimezone()
            ),
            gap_policy=gap_policy_fixture(),
        )
        with mock.patch.object(
            subject.Path,
            "mkdir",
            side_effect=AssertionError("write boundary reached"),
        ) as mkdir, mock.patch.object(subject.Path, "rename") as rename, mock.patch.object(
            subject, "write_csv"
        ) as write_csv:
            with self.assertRaisesRegex(
                ValueError,
                "^closed_candle_cutoff_utc must be a timezone-aware timestamp$",
            ):
                subject.build_bundle(args)
        mkdir.assert_not_called()
        rename.assert_not_called()
        write_csv.assert_not_called()

    def test_build_refuses_state_changing_timezone_before_any_write(self) -> None:
        carrier = StateChangingTimezone()
        args = argparse.Namespace(
            repo_root="unused",
            bundle_parent="unused",
            archive_root="unused",
            datasets_root="unused",
            date_token="fixture",
            closed_candle_cutoff_utc=datetime(
                2026, 1, 1, 0, 10, tzinfo=carrier
            ),
            gap_policy=gap_policy_fixture(),
        )
        with mock.patch.object(
            subject.Path,
            "mkdir",
            side_effect=AssertionError("write boundary reached"),
        ) as mkdir, mock.patch.object(subject.Path, "rename") as rename, mock.patch.object(
            subject, "write_csv"
        ) as write_csv:
            with self.assertRaisesRegex(
                ValueError,
                "^closed_candle_cutoff_utc must be a timezone-aware timestamp$",
            ):
                subject.build_bundle(args)
        self.assertEqual(carrier.calls, 0)
        mkdir.assert_not_called()
        rename.assert_not_called()
        write_csv.assert_not_called()

    def test_validate_quality_consumes_one_bound_evidence_record(self) -> None:
        clean_evidence = subject.prepare_dataset_evidence(
            rows_at(0, 300, 600),
            instrument_id="BINANCE:BTCUSDT",
            timeframe="5m",
            closed_candle_cutoff_utc=BASE_TIME + timedelta(seconds=900),
            gap_policy=gap_policy_fixture(),
        )
        foreign_rows = rows_at(0, 300, 900)
        foreign_rows[-1].update({"high": 8, "low": 9})
        foreign_evidence = subject.prepare_dataset_evidence(
            foreign_rows,
            instrument_id="BINANCE:BTCUSDT",
            timeframe="5m",
            closed_candle_cutoff_utc=BASE_TIME + timedelta(seconds=1200),
            gap_policy=gap_policy_fixture(),
        )
        self.assertEqual(
            foreign_evidence["quality"]["gap_measurement"]["gap_event_count"], 1
        )
        self.assertEqual(
            foreign_evidence["quality"]["ohlcv_validation_status"], "FAIL"
        )
        self.assertEqual(
            len(clean_evidence["closed_rows"]),
            len(foreign_evidence["closed_rows"]),
        )
        spliced_evidence = {
            **clean_evidence,
            "quality": foreign_evidence["quality"],
        }
        row_tampered_evidence = {
            **clean_evidence,
            "closed_rows": [dict(row) for row in clean_evidence["closed_rows"]],
        }
        row_tampered_evidence["closed_rows"][1]["volume"] = 2.0
        quality_tampered_evidence = {
            **clean_evidence,
            "quality": {
                **clean_evidence["quality"],
                "invalid_ohlcv_count": 1,
            },
        }
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            result = subject.validate_quality(
                "SYNTHETIC", "5m", root, evidence=clean_evidence
            )
            with (root / result["duplicate_report_path"]).open(
                "r", encoding="utf-8", newline=""
            ) as handle:
                duplicate_detail = list(csv.DictReader(handle))

            self.assertEqual(result["duplicate_timestamp_count"], len(duplicate_detail))
            self.assertEqual(
                result["invalid_ohlcv_count"],
                len(clean_evidence["quality"]["invalid_ohlcv_reasons"]),
            )
            for label, evidence in (
                ("spliced", spliced_evidence),
                ("row-tampered", row_tampered_evidence),
                ("quality-tampered", quality_tampered_evidence),
            ):
                refusal_root = root / label
                with self.subTest(label=label), self.assertRaisesRegex(
                    ValueError,
                    "^evidence quality does not match closed rows and timeframe$",
                ):
                    subject.validate_quality(
                        label.upper(),
                        "5m",
                        refusal_root,
                        evidence=evidence,
                    )
                self.assertFalse(refusal_root.exists())

    def test_public_evidence_seam_returns_exact_h1_m2_shape(self) -> None:
        evidence = subject.prepare_dataset_evidence(
            rows_at(0, 900, 2700, 3600),
            instrument_id="BINANCE:BTCUSDT",
            timeframe="15m",
            closed_candle_cutoff_utc=BASE_TIME + timedelta(seconds=4500),
            gap_policy=gap_policy_fixture(),
        )

        self.assertNotIn("gap_measurement", evidence)
        measurement = evidence["quality"]["gap_measurement"]
        self.assertEqual(
            set(measurement),
            {
                "result_kind",
                "timeframe",
                "step_seconds",
                "observation_count",
                "interval_count",
                "coverage_seconds",
                "coverage_days",
                "expected_bars",
                "gap_event_count",
                "missing_bar_count",
                "m1_gap_event_ratio",
                "m2_missing_bar_ratio",
                "m3_missing_time_ratio",
                "max_gap_bars",
                "max_gap_seconds",
                "duplicate_timestamp_count",
                "out_of_order_interval_count",
                "early_interval_count",
                "irregular_interval_count",
                "series_clean",
                "policy_version",
            },
        )
        self.assertEqual(measurement["result_kind"], "P021_DATA_GAP_MEASUREMENT_ONLY")
        self.assertEqual(measurement["observation_count"], 4)
        self.assertEqual(measurement["interval_count"], 3)
        self.assertEqual(measurement["coverage_seconds"], 3600.0)
        self.assertEqual(measurement["expected_bars"], 5)
        self.assertEqual(measurement["gap_event_count"], 1)
        self.assertEqual(measurement["missing_bar_count"], 1)
        self.assertAlmostEqual(measurement["m1_gap_event_ratio"], 1 / 3)
        self.assertAlmostEqual(measurement["m2_missing_bar_ratio"], 1 / 5)
        self.assertAlmostEqual(measurement["m3_missing_time_ratio"], 1 / 4)
        self.assertEqual(measurement["policy_version"], gap_policy_fixture()["version"])
        self.assertNotIn("ready", measurement)

    def test_public_evidence_seam_calls_h1_once_in_source_order(self) -> None:
        with mock.patch.object(
            subject, "measure_data_gaps", wraps=subject.measure_data_gaps
        ) as h1_measure:
            evidence = subject.prepare_dataset_evidence(
                rows_at(300, 0, 600),
                instrument_id="BINANCE:BTCUSDT",
                timeframe="5m",
                closed_candle_cutoff_utc=BASE_TIME + timedelta(seconds=900),
                gap_policy=gap_policy_fixture(),
            )

        self.assertEqual(h1_measure.call_count, 1)
        observed_timestamps = list(h1_measure.call_args.args[0])
        self.assertEqual(
            [timestamp - BASE_TIME.timestamp() for timestamp in observed_timestamps],
            [300.0, 0.0, 600.0],
        )
        self.assertEqual(
            evidence["quality"]["gap_measurement"]["out_of_order_interval_count"], 1
        )
        self.assertFalse(evidence["quality"]["gap_measurement"]["series_clean"])

    def test_descending_source_order_refuses_through_h1(self) -> None:
        with mock.patch.object(
            subject, "measure_data_gaps", wraps=subject.measure_data_gaps
        ) as h1_measure:
            with self.assertRaisesRegex(
                ValueError, "^timestamp span must be finite and positive$"
            ):
                subject.prepare_dataset_evidence(
                    rows_at(600, 300, 0),
                    instrument_id="BINANCE:BTCUSDT",
                    timeframe="5m",
                    closed_candle_cutoff_utc=BASE_TIME
                    + timedelta(seconds=900),
                    gap_policy=gap_policy_fixture(),
                )

        self.assertEqual(h1_measure.call_count, 1)
        observed = list(h1_measure.call_args.args[0])
        self.assertEqual(
            [timestamp - BASE_TIME.timestamp() for timestamp in observed],
            [600.0, 300.0, 0.0],
        )

    def test_public_evidence_seam_refuses_only_structurally_invalid_ohlcv(self) -> None:
        cases = []
        for label, value, message in (
            ("missing", None, "row 1 volume is required"),
            ("blank", "", "row 1 volume must be a finite number"),
            ("text", "bad", "row 1 volume must be a finite number"),
            ("boolean", True, "row 1 volume must be a finite number"),
            ("nan", float("nan"), "row 1 volume must be a finite number"),
            ("infinity", float("inf"), "row 1 volume must be a finite number"),
        ):
            rows = rows_at(0, 300)
            if value is None:
                rows[0].pop("volume")
            else:
                rows[0]["volume"] = value
            cases.append((label, rows, message))
        for label, rows, message in cases:
            with self.subTest(label=label), self.assertRaisesRegex(ValueError, f"^{message}$"):
                subject.prepare_dataset_evidence(
                    rows,
                    instrument_id="BINANCE:BTCUSDT",
                    timeframe="5m",
                    closed_candle_cutoff_utc=BASE_TIME + timedelta(seconds=600),
                    gap_policy=gap_policy_fixture(),
                )

    def test_finite_semantic_ohlcv_failures_withhold_dataset_identity(self) -> None:
        cases = []
        negative_volume = rows_at(0, 300)
        negative_volume[0]["volume"] = -1
        cases.append(("negative volume", negative_volume, "negative_volume"))
        inconsistent = rows_at(0, 300)
        inconsistent[0].update({"high": 8, "low": 9})
        cases.append(("inconsistent OHLC", inconsistent, "high_below_low"))

        for label, rows, reason in cases:
            with self.subTest(label=label):
                evidence = subject.prepare_dataset_evidence(
                    rows,
                    instrument_id="BINANCE:BTCUSDT",
                    timeframe="5m",
                    closed_candle_cutoff_utc=BASE_TIME + timedelta(seconds=600),
                    gap_policy=gap_policy_fixture(),
                )
                self.assertEqual(evidence["quality"]["ohlcv_validation_status"], "FAIL")
                self.assertGreater(evidence["quality"]["invalid_ohlcv_count"], 0)
                self.assertIn(
                    reason,
                    [finding["reason"] for finding in evidence["quality"]["invalid_ohlcv_reasons"]],
                )
                self.assertIsNone(evidence["dataset_hash"])
                self.assertEqual(len(evidence["closed_rows"]), 2)

    def test_valid_evidence_exposes_pass_and_dataset_identity(self) -> None:
        evidence = subject.prepare_dataset_evidence(
            rows_at(0, 300),
            instrument_id="BINANCE:BTCUSDT",
            timeframe="5m",
            closed_candle_cutoff_utc=BASE_TIME + timedelta(seconds=600),
            gap_policy=gap_policy_fixture(),
        )
        self.assertEqual(evidence["quality"]["ohlcv_validation_status"], "PASS")
        self.assertEqual(evidence["quality"]["invalid_ohlcv_count"], 0)
        self.assertEqual(set(evidence["dataset_hash"]), {"contract", "digest"})
        self.assertEqual(evidence["dataset_hash"]["contract"], "ds-v1")
        self.assertRegex(evidence["dataset_hash"]["digest"], "^[0-9a-f]{64}$")

    def test_closed_candle_cutoff_precedes_measurement(self) -> None:
        rows = rows_at(0, 300, 600, 900)
        rows[-1]["volume"] = "forming-row-is-not-consumed"
        evidence = subject.prepare_dataset_evidence(
            rows,
            instrument_id="BINANCE:BTCUSDT",
            timeframe="5m",
            closed_candle_cutoff_utc=BASE_TIME + timedelta(seconds=900),
            gap_policy=gap_policy_fixture(),
        )

        self.assertEqual(evidence["excluded_forming_candle_count"], 1)
        self.assertEqual(evidence["closed_candle_cutoff_utc"], "2026-01-01T00:15:00Z")
        self.assertEqual(len(evidence["closed_rows"]), 3)
        self.assertEqual(
            [row["timestamp_utc"] for row in evidence["closed_rows"]],
            [
                "2026-01-01T00:00:00Z",
                "2026-01-01T00:05:00Z",
                "2026-01-01T00:10:00Z",
            ],
        )
        self.assertEqual(evidence["quality"]["gap_measurement"]["observation_count"], 3)
        self.assertTrue(evidence["quality"]["gap_measurement"]["series_clean"])

        with self.assertRaisesRegex(ValueError, "^closed_candle_cutoff_utc must be timezone-aware$"):
            subject.prepare_dataset_evidence(
                rows_at(0, 300),
                instrument_id="BINANCE:BTCUSDT",
                timeframe="5m",
                closed_candle_cutoff_utc=datetime(2026, 1, 1, 0, 10),
                gap_policy=gap_policy_fixture(),
            )

    def test_ds_v1_identity_matches_independent_literal_and_binds_volume(self) -> None:
        rows = rows_at(300, 0, 600, 900)
        evidence = subject.prepare_dataset_evidence(
            rows,
            instrument_id="BINANCE:BTCUSDT",
            timeframe="5m",
            closed_candle_cutoff_utc=BASE_TIME + timedelta(seconds=900),
            gap_policy=gap_policy_fixture(),
        )
        canonical_bytes = (
            "p021.dataset/v1\n"
            "BINANCE:BTCUSDT\n"
            "5m\n"
            "2026-01-01T00:00:00Z\n"
            "2026-01-01T00:10:00Z\n"
            "3\n"
            "2026-01-01T00:00:00Z,0x1.4000000000000p+3,0x1.8000000000000p+3,"
            "0x1.2000000000000p+3,0x1.6000000000000p+3,0x1.0000000000000p+0\n"
            "2026-01-01T00:05:00Z,0x1.4000000000000p+3,0x1.8000000000000p+3,"
            "0x1.2000000000000p+3,0x1.6000000000000p+3,0x1.0000000000000p+0\n"
            "2026-01-01T00:10:00Z,0x1.4000000000000p+3,0x1.8000000000000p+3,"
            "0x1.2000000000000p+3,0x1.6000000000000p+3,0x1.0000000000000p+0\n"
        ).encode("utf-8")
        expected = {
            "contract": "ds-v1",
            "digest": hashlib.sha256(canonical_bytes).hexdigest(),
        }
        self.assertEqual(evidence["dataset_hash"], expected)

        reordered = subject.prepare_dataset_evidence(
            rows_at(0, 300, 600, 900),
            instrument_id="BINANCE:BTCUSDT",
            timeframe="5m",
            closed_candle_cutoff_utc=BASE_TIME + timedelta(seconds=900),
            gap_policy=gap_policy_fixture(),
        )
        self.assertEqual(reordered["dataset_hash"], expected)

        changed_volume_rows = rows_at(0, 300, 600, 900)
        changed_volume_rows[1]["volume"] = 2
        changed_volume = subject.prepare_dataset_evidence(
            changed_volume_rows,
            instrument_id="BINANCE:BTCUSDT",
            timeframe="5m",
            closed_candle_cutoff_utc=BASE_TIME + timedelta(seconds=900),
            gap_policy=gap_policy_fixture(),
        )
        self.assertNotEqual(changed_volume["dataset_hash"], expected)

        for field, value in {
            "open": 10.5,
            "high": 12.5,
            "low": 8.5,
            "close": 10.5,
            "volume": 2,
        }.items():
            mutated_rows = rows_at(0, 300, 600, 900)
            mutated_rows[1][field] = value
            mutated = subject.prepare_dataset_evidence(
                mutated_rows,
                instrument_id="BINANCE:BTCUSDT",
                timeframe="5m",
                closed_candle_cutoff_utc=BASE_TIME + timedelta(seconds=900),
                gap_policy=gap_policy_fixture(),
            )
            with self.subTest(field=field):
                self.assertNotEqual(mutated["dataset_hash"], expected)

        changed_instrument = subject.prepare_dataset_evidence(
            rows_at(0, 300, 600, 900),
            instrument_id="BINANCE:ETHUSDT",
            timeframe="5m",
            closed_candle_cutoff_utc=BASE_TIME + timedelta(seconds=900),
            gap_policy=gap_policy_fixture(),
        )
        self.assertNotEqual(changed_instrument["dataset_hash"], expected)

        changed_timeframe = subject.prepare_dataset_evidence(
            rows_at(0, 300, 600),
            instrument_id="BINANCE:BTCUSDT",
            timeframe="15m",
            closed_candle_cutoff_utc=BASE_TIME + timedelta(seconds=1800),
            gap_policy=gap_policy_fixture(),
        )
        self.assertNotEqual(changed_timeframe["dataset_hash"], expected)

        changed_forming_rows = rows_at(0, 300, 600, 900)
        changed_forming_rows[-1]["close"] = 10
        changed_forming = subject.prepare_dataset_evidence(
            changed_forming_rows,
            instrument_id="BINANCE:BTCUSDT",
            timeframe="5m",
            closed_candle_cutoff_utc=BASE_TIME + timedelta(seconds=900),
            gap_policy=gap_policy_fixture(),
        )
        self.assertEqual(changed_forming["dataset_hash"], expected)

    def validate(self, offsets: tuple[int, ...], timeframe: str):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name) / "synthetic_bundle"
        step = subject.TIMEFRAME_SECONDS[timeframe]
        evidence = subject.prepare_dataset_evidence(
            rows_at(*offsets),
            instrument_id="BINANCE:BTCUSDT",
            timeframe=timeframe,
            closed_candle_cutoff_utc=BASE_TIME + timedelta(seconds=max(offsets) + step),
            gap_policy=gap_policy_fixture(),
        )
        result = subject.validate_quality(
            "SYNTHETIC",
            timeframe,
            root,
            evidence=evidence,
        )
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
        self.assertEqual(
            set(gaps[0]),
            {
                "prev_timestamp_utc",
                "next_timestamp_utc",
                "delta_seconds",
                "missing_bars_estimate",
            },
        )
        self.assertEqual(gaps[0]["prev_timestamp_utc"], "2026-01-01T00:05:00+00:00")
        self.assertEqual(gaps[0]["next_timestamp_utc"], "2026-01-01T00:15:00+00:00")
        self.assertEqual(gaps[0]["delta_seconds"], "600")
        self.assertEqual(gaps[0]["missing_bars_estimate"], "1")

    def test_legacy_gap_csv_sorts_without_erasing_source_order_evidence(self) -> None:
        with mock.patch.object(
            subject, "measure_data_gaps", wraps=subject.measure_data_gaps
        ) as h1_measure:
            result, legacy_gaps = self.validate((0, 600, 300, 900), "5m")

        self.assertEqual(h1_measure.call_count, 1)
        self.assertEqual(result["gap_measurement"]["gap_event_count"], 2)
        self.assertEqual(
            result["gap_measurement"]["out_of_order_interval_count"], 1
        )
        self.assertEqual(legacy_gaps, [])

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
                    subject.validate_quality(
                        "SYNTHETIC",
                        "bogus",
                        root,
                        evidence={"closed_rows": rows, "quality": {}},
                    )
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
        rows = rows_at(0, 300, 600, 300)
        rows[-1].update({"high": 8, "low": 9})
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "synthetic_bundle"
            evidence = subject.prepare_dataset_evidence(
                rows,
                instrument_id="BINANCE:BTCUSDT",
                timeframe="5m",
                closed_candle_cutoff_utc=BASE_TIME + timedelta(seconds=900),
                gap_policy=gap_policy_fixture(),
            )
            result = subject.validate_quality(
                "SYNTHETIC",
                "5m",
                root,
                evidence=evidence,
            )
        self.assertFalse(result["has_gaps"])
        self.assertEqual(result["duplicate_timestamp_count"], 1)
        self.assertEqual(result["ohlcv_validation_status"], "FAIL")
        self.assertEqual(result["invalid_ohlcv_count"], 3)

    def test_validate_quality_projects_exact_h1_result_without_remeasurement(self) -> None:
        evidence = subject.prepare_dataset_evidence(
            rows_at(0, 300, 900),
            instrument_id="BINANCE:BTCUSDT",
            timeframe="5m",
            closed_candle_cutoff_utc=BASE_TIME + timedelta(seconds=1200),
            gap_policy=gap_policy_fixture(),
        )
        with tempfile.TemporaryDirectory() as temporary, mock.patch.object(
            subject, "measure_data_gaps", side_effect=AssertionError("must not remeasure")
        ):
            result = subject.validate_quality(
                "SYNTHETIC",
                "5m",
                Path(temporary),
                evidence=evidence,
            )
        self.assertIs(result["gap_measurement"], evidence["quality"]["gap_measurement"])
        self.assertEqual(result["has_gaps"], True)
        self.assertEqual(result["gap_count"], 1)
        self.assertEqual(result["expected_bars"], 4)

    def test_build_refuses_missing_explicit_evidence_inputs_before_any_write(self) -> None:
        args = argparse.Namespace(
            repo_root="unused",
            bundle_parent="unused",
            archive_root="unused",
            datasets_root="unused",
            date_token="fixture",
        )
        with mock.patch.object(subject.Path, "mkdir") as mkdir, mock.patch.object(
            subject.Path, "rename"
        ) as rename, mock.patch.object(subject, "write_csv") as write_csv:
            with self.assertRaisesRegex(ValueError, "closed_candle_cutoff_utc is required"):
                subject.build_bundle(args)
        mkdir.assert_not_called()
        rename.assert_not_called()
        write_csv.assert_not_called()

    def test_build_refuses_equal_length_foreign_quality_before_any_artifact(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            archive = root / "archive"
            archive.mkdir()
            source_path = archive / "BINANCE_BTCUSDT,5m_fixture.csv"
            with source_path.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(
                    handle, fieldnames=["time", "open", "high", "low", "close", "volume"]
                )
                writer.writeheader()
                writer.writerows(
                    [
                        {"time": row["timestamp_utc"], **{key: row[key] for key in ("open", "high", "low", "close", "volume")}}
                        for row in rows_at(0, 300, 600)
                    ]
                )
            args = argparse.Namespace(
                repo_root=root / "repo",
                bundle_parent=root / "bundle-parent",
                archive_root=archive,
                datasets_root=root / "absent",
                date_token="fixture",
                closed_candle_cutoff_utc=BASE_TIME + timedelta(seconds=600),
                gap_policy=gap_policy_fixture(),
            )
            prepare_real = subject.prepare_dataset_evidence

            def splice_equal_length_foreign_quality(rows, **kwargs):
                clean = prepare_real(rows, **kwargs)
                foreign = prepare_real(
                    rows_at(0, 600),
                    instrument_id=kwargs["instrument_id"],
                    timeframe=kwargs["timeframe"],
                    closed_candle_cutoff_utc=BASE_TIME + timedelta(seconds=900),
                    gap_policy=kwargs["gap_policy"],
                )
                self.assertEqual(len(clean["closed_rows"]), len(foreign["closed_rows"]))
                return {**clean, "quality": foreign["quality"]}

            with mock.patch.object(
                subject,
                "prepare_dataset_evidence",
                side_effect=splice_equal_length_foreign_quality,
            ):
                with self.assertRaisesRegex(
                    ValueError,
                    "^evidence quality does not match closed rows and timeframe$",
                ):
                    subject.build_bundle(args)

            self.assertFalse((root / "bundle-parent").exists())
            self.assertFalse((root / "repo").exists())

    def test_build_projects_evidence_into_manifest_and_quality_records(self) -> None:
        class StopAfterQualityRecord(Exception):
            pass

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            archive = root / "archive"
            archive.mkdir()
            source_path = archive / "BINANCE_BTCUSDT,5m_fixture.csv"
            with source_path.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(
                    handle, fieldnames=["time", "open", "high", "low", "close", "volume"]
                )
                writer.writeheader()
                for row in rows_at(0, 300, 600):
                    writer.writerow(
                        {"time": row["timestamp_utc"], **{key: row[key] for key in ("open", "high", "low", "close", "volume")}}
                    )
            args = argparse.Namespace(
                repo_root=root / "repo",
                bundle_parent=root / "bundle-parent",
                archive_root=archive,
                datasets_root=root / "absent",
                date_token="fixture",
                closed_candle_cutoff_utc=BASE_TIME + timedelta(seconds=600),
                gap_policy=gap_policy_fixture(),
            )
            measurement = {
                "result_kind": "P021_DATA_GAP_MEASUREMENT_ONLY",
                "timeframe": "5m",
                "gap_event_count": 0,
                "duplicate_timestamp_count": 0,
                "expected_bars": 1,
            }
            prepared = {
                "closed_rows": rows_at(0, 300),
                "excluded_forming_candle_count": 1,
                "closed_candle_cutoff_utc": "2026-01-01T00:10:00Z",
                "quality": {
                    "gap_measurement": measurement,
                    "ohlcv_validation_status": "PASS",
                    "invalid_ohlcv_count": 0,
                    "invalid_ohlcv_reasons": [],
                },
                "dataset_hash": {"contract": "ds-v1", "digest": "f" * 64},
            }
            projected_quality = {
                "gap_measurement": measurement,
                "has_gaps": False,
                "gap_count": 0,
                "gap_report_path": "quality/gaps.csv",
                "duplicate_timestamp_count": 0,
                "duplicate_report_path": "quality/duplicates.csv",
                "ohlcv_validation_status": "PASS",
                "ohlcv_report_path": "quality/ohlcv.md",
                "invalid_ohlcv_count": 0,
                "invalid_ohlcv_reasons": [],
                "expected_bars": 1,
            }
            records: dict[str, dict] = {}

            def record_json(path, payload):
                records[Path(path).name] = payload
                if Path(path).name == "DATA_QUALITY_SUMMARY.json":
                    raise StopAfterQualityRecord

            fake_stat = mock.Mock(st_size=123)
            original_stat = subject.Path.stat

            def stat_existing_or_generated(path, *args, **kwargs):
                try:
                    return original_stat(path, *args, **kwargs)
                except FileNotFoundError:
                    if "raw" in path.parts or "normalized" in path.parts:
                        return fake_stat
                    raise

            with mock.patch.object(subject.Path, "mkdir"), mock.patch.object(
                subject.Path, "write_text"
            ), mock.patch.object(
                subject.Path, "stat", autospec=True, side_effect=stat_existing_or_generated
            ), mock.patch.object(
                subject, "write_csv"
            ), mock.patch.object(subject, "write_simple_yaml"), mock.patch.object(
                subject, "write_json", side_effect=record_json
            ), mock.patch.object(subject, "safe_copy"), mock.patch.object(
                subject, "sha256_file", return_value="fixture-sha"
            ), mock.patch.object(
                subject, "prepare_dataset_evidence", return_value=prepared
            ), mock.patch.object(
                subject, "validate_quality", return_value=projected_quality
            ), mock.patch.object(
                subject, "classify_regimes", return_value={"counts": {}, "rows": 1}
            ):
                with self.assertRaises(StopAfterQualityRecord):
                    subject.build_bundle(args)

            manifest = records["DATA_BUNDLE_MANIFEST.json"]["datasets"][0]
            quality_record = records["DATA_QUALITY_SUMMARY.json"]["datasets"][0]
            for record in (manifest, quality_record):
                self.assertEqual(
                    record["dataset_hash"],
                    {"contract": "ds-v1", "digest": "f" * 64},
                )
                self.assertEqual(record["closed_candle_cutoff_utc"], "2026-01-01T00:10:00Z")
                self.assertEqual(record["excluded_forming_candle_count"], 1)
            self.assertIs(manifest["gap_measurement"], measurement)
            self.assertIs(quality_record["gap_measurement"], measurement)
            self.assertEqual(manifest["start"], "2026-01-01T00:00:00+00:00")
            self.assertEqual(manifest["end"], "2026-01-01T00:05:00+00:00")


if __name__ == "__main__":
    unittest.main(verbosity=2)
