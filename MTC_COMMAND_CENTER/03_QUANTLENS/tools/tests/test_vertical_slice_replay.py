import csv
import json
import sys
import tempfile
import unittest
from pathlib import Path


TOOLS_DIR = Path(__file__).resolve().parents[1]
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))


class TestStg002ReplayEmitter(unittest.TestCase):
    def write_fixture_csvs(self, temp_dir):
        trades_path = Path(temp_dir) / "trades.csv"
        signals_path = Path(temp_dir) / "signals.csv"

        with trades_path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.writer(handle)
            writer.writerow(
                ["entry_time", "exit_time", "entry", "stop", "exit", "reason", "ret_net_pct", "R"]
            )
            writer.writerow(
                [
                    "2026-05-01T10:00:00+0000",
                    "2026-05-01T14:00:00+0000",
                    "10.50",
                    "9.50",
                    "11.20",
                    "trail",
                    "6.67",
                    "1.70",
                ]
            )
            writer.writerow(
                [
                    "2026-05-02T08:00:00+00:00",
                    "2026-05-02T12:30:00Z",
                    "12.00",
                    "11.00",
                    "11.80",
                    "stop",
                    "-1.67",
                    "-0.20",
                ]
            )

        with signals_path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.writer(handle)
            writer.writerow(
                [
                    "timestamp_utc",
                    "open",
                    "high",
                    "low",
                    "close",
                    "atr14",
                    "ema8",
                    "long_entry",
                    "stop_at_signal",
                ]
            )
            writer.writerow(["2026-05-01T09:00:00Z", "10", "11", "9", "10.5", "1", "10", "1", "9.5"])

        return trades_path, signals_path

    def test_trades_rows_emit_one_entry_and_one_exit_each(self):
        from vertical_slice.stg002_replay_emitter import build_expected_payloads_from_trades

        with tempfile.TemporaryDirectory() as temp_dir:
            trades_path, _ = self.write_fixture_csvs(temp_dir)

            payloads = build_expected_payloads_from_trades(
                trades_path, auth_token="synthetic-token"
            )

        self.assertEqual(len(payloads), 4)
        self.assertEqual([payload["action"] for payload in payloads], ["ENTRY", "EXIT", "ENTRY", "EXIT"])

    def test_entry_exit_field_mapping_is_trades_driven(self):
        from vertical_slice.stg002_replay_emitter import build_expected_payloads_from_trades

        with tempfile.TemporaryDirectory() as temp_dir:
            trades_path, _ = self.write_fixture_csvs(temp_dir)
            payloads = build_expected_payloads_from_trades(
                trades_path, auth_token="synthetic-token"
            )

        entry = payloads[0]
        exit_payload = payloads[1]

        self.assertEqual(entry["bar_time_utc"], "2026-05-01T09:00:00Z")
        self.assertEqual(entry["timestamp_utc"], "2026-05-01T10:00:00Z")
        self.assertEqual(entry["stop_loss"], 9.5)
        self.assertIsNone(entry["take_profit"])
        self.assertEqual(exit_payload["bar_time_utc"], "2026-05-01T14:00:00Z")
        self.assertEqual(exit_payload["exit_reason"], "trail")

    def test_payload_ids_and_checksums_are_deterministic(self):
        from vertical_slice.stg002_replay_emitter import build_expected_payloads_from_trades

        with tempfile.TemporaryDirectory() as temp_dir:
            trades_path, _ = self.write_fixture_csvs(temp_dir)
            first = build_expected_payloads_from_trades(trades_path, auth_token="synthetic-token")
            second = build_expected_payloads_from_trades(trades_path, auth_token="synthetic-token")

        for left, right in zip(first, second):
            self.assertEqual(left["signal_id"], right["signal_id"])
            self.assertEqual(left["idempotency_key"], right["idempotency_key"])
            self.assertEqual(left["checksum"], right["checksum"])

    def test_write_replay_artifacts_in_temp_dir_with_manifest_labels(self):
        from vertical_slice.constants import BANNER
        from vertical_slice.stg002_replay_emitter import write_replay_artifacts

        with tempfile.TemporaryDirectory() as temp_dir:
            trades_path, signals_path = self.write_fixture_csvs(temp_dir)
            output_dir = Path(temp_dir) / "out"

            write_replay_artifacts(
                trades_csv_path=trades_path,
                signals_csv_path=signals_path,
                output_dir=output_dir,
                auth_token="synthetic-token",
            )

            expected_path = output_dir / "expected_signals.jsonl"
            manifest_path = output_dir / "emitter_manifest.json"
            rows = [json.loads(line) for line in expected_path.read_text(encoding="utf-8").splitlines()]
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

        self.assertEqual(len(rows), 4)
        self.assertEqual(manifest["banner"], BANNER)
        self.assertEqual(manifest["benchmark_role"], "SYSTEM_TEST_ONLY")
        self.assertFalse(manifest["promotable"])
        self.assertEqual(manifest["strategy_approval_status"], "NOT_APPROVED")
        self.assertIn("robust_final = 0", manifest["robustness_note"])

    def test_emitter_docstring_marks_signal_bar_as_nominal(self):
        from vertical_slice import stg002_replay_emitter

        self.assertIn("nominal signal-bar reconstruction", stg002_replay_emitter.__doc__)

    def test_run_local_replay_entry_function_writes_ledgers_and_summary(self):
        from vertical_slice.constants import BANNER
        from vertical_slice.stg002_replay_emitter import run_local_replay

        with tempfile.TemporaryDirectory() as temp_dir:
            trades_path, signals_path = self.write_fixture_csvs(temp_dir)
            output_dir = Path(temp_dir) / "system_test_like_output"

            summary = run_local_replay(
                trades_csv_path=trades_path,
                signals_csv_path=signals_path,
                output_dir=output_dir,
                auth_token="synthetic-token",
            )

            received_rows = [
                json.loads(line)
                for line in (output_dir / "received_signals.jsonl")
                .read_text(encoding="utf-8")
                .splitlines()
            ]
            fills = [
                json.loads(line)
                for line in (output_dir / "simulated_fills.jsonl")
                .read_text(encoding="utf-8")
                .splitlines()
            ]
            persisted_summary = json.loads(
                (output_dir / "reconciliation_summary.json").read_text(encoding="utf-8")
            )
            report_text = (output_dir / "reconciliation_report.md").read_text(
                encoding="utf-8"
            )

        self.assertEqual(summary["status"], "OK")
        self.assertEqual(summary["expected_count"], 4)
        self.assertEqual(summary["received_count"], 4)
        self.assertEqual(summary["filled_count"], 4)
        self.assertEqual(summary["duplicates_dropped"], 0)
        self.assertEqual(summary["rejected_count"], 0)
        self.assertEqual(summary["unexplained_count"], 0)
        self.assertEqual({row["disposition"] for row in received_rows}, {"accepted"})
        self.assertTrue(all(row["simulated"] for row in fills))
        self.assertEqual(persisted_summary, summary)
        self.assertIn(BANNER, report_text)


if __name__ == "__main__":
    unittest.main()
