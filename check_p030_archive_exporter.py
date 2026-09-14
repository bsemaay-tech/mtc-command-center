"""Executable checks for the P030 Shape-B archive exporter."""

from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import check_market_data_collector as collector_fixtures
import market_data_collector
import p030_archive_exporter as subject
from p030_closed_partition_backup_adapter import capture_stable_prefix


EXPORTED_AT = "2026-09-14T00:00:00Z"
CAPTURED_AT = "2026-09-14T00:01:00Z"


class ArchiveExporterTests(unittest.TestCase):
    def _collector_partition(self, root: Path) -> tuple[Path, Path]:
        source_root = root / "collector-root"
        archive = market_data_collector.MonthlyArchive(source_root)
        now = collector_fixtures.JANUARY_LAST_BAR + 10 * collector_fixtures.STEP
        base = collector_fixtures.PERSISTED_ORDER_BASE
        for offset in (0, 1):
            bar = market_data_collector.normalize_bar(
                collector_fixtures.raw_bar(
                    base + offset * collector_fixtures.STEP
                ),
                source_producer="WS_LIVE",
                ingest_time=now,
                env_lineage_id="fixture-lineage",
                identities=collector_fixtures.IDENTITIES,
            )
            self.assertIsNotNone(bar)
            self.assertEqual(archive.append_bar(bar), "APPENDED")
        source = (
            source_root
            / "bars"
            / "HYPERLIQUID"
            / "BTC"
            / "15m"
            / "2026-02.jsonl"
        )
        self.assertTrue(source.is_file())
        return source_root, source

    def _export(self, root: Path, name: str = "exported.jsonl"):
        source_root, source = self._collector_partition(root)
        target = root / "export-root" / name
        receipt = subject.export_partition(
            source,
            target,
            source_root=source_root,
            exported_at_utc=EXPORTED_AT,
        )
        return source_root, source, target, receipt

    def test_exported_collector_fixture_is_accepted_by_stable_prefix_adapter(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source_root, source, target, receipt = self._export(root)
            raw_message = None
            try:
                capture_stable_prefix(
                    source,
                    root / "raw-stable",
                    source_root=source_root,
                    high_water_bytes=source.stat().st_size,
                    captured_at_utc=CAPTURED_AT,
                    dataset_content_hash=receipt.dataset_content_hash,
                )
            except ValueError as error:
                raw_message = str(error)
            self.assertIn(
                raw_message,
                {
                    "observation_id must match p030obs-v1 identity",
                    "prefix record is not canonical JSONL",
                },
            )

            stable_receipt = capture_stable_prefix(
                target,
                root / "exported-stable",
                source_root=target.parent,
                high_water_bytes=target.stat().st_size,
                captured_at_utc=CAPTURED_AT,
                dataset_content_hash=receipt.dataset_content_hash,
            )
            stable = json.loads(stable_receipt.read_text(encoding="utf-8"))
            self.assertEqual(stable["record_count"], 2)
            self.assertEqual(stable["dataset_content_hash"], receipt.dataset_content_hash)
            print(f"D-13 RED RAW REFUSAL: {raw_message}")
            print("D-13 GREEN EXPORTED CAPTURE: PASS")

    def test_receipt_fields_hashes_and_identity_rewrite_are_correct(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source_root, source, target, receipt = self._export(root)
            receipt_path = Path(str(target) + ".p030export.json")
            stored = json.loads(receipt_path.read_text(encoding="utf-8"))
            self.assertEqual(
                set(stored),
                {
                    "schema",
                    "source_path",
                    "source_sha256",
                    "source_record_count",
                    "exporter_sha256",
                    "exported_sha256",
                    "exported_record_count",
                    "dataset_content_hash",
                    "exported_at_utc",
                    "identity_recomputed",
                },
            )
            self.assertEqual(stored, receipt.as_dict())
            self.assertEqual(stored["schema"], "p030.archive_export/v1")
            self.assertEqual(stored["source_path"], source.relative_to(source_root).as_posix())
            self.assertEqual(stored["source_sha256"], hashlib.sha256(source.read_bytes()).hexdigest())
            self.assertEqual(stored["exported_sha256"], hashlib.sha256(target.read_bytes()).hexdigest())
            self.assertEqual(stored["source_record_count"], 2)
            self.assertEqual(stored["exported_record_count"], 2)
            self.assertTrue(stored["identity_recomputed"])
            self.assertEqual(stored["exported_at_utc"], EXPORTED_AT)
            self.assertEqual(
                stored["exporter_sha256"],
                hashlib.sha256(Path(subject.__file__).read_bytes()).hexdigest(),
            )

            raw_rows = [
                json.loads(line)
                for line in source.read_text(encoding="utf-8").splitlines()
            ]
            exported_rows = [
                json.loads(line)
                for line in target.read_text(encoding="utf-8").splitlines()
            ]
            for raw, exported in zip(raw_rows, exported_rows, strict=True):
                self.assertRegex(raw["observation_id"], r"^[0-9a-f]{64}$")
                self.assertRegex(raw["producer_payload_hash"], r"^[0-9a-f]{64}$")
                self.assertRegex(exported["observation_id"], r"^p030obs-v1:[0-9a-f]{64}$")
                self.assertRegex(
                    exported["producer_payload_hash"],
                    r"^p030payload-v1:[0-9a-f]{64}$",
                )
                for key, value in raw.items():
                    if key not in {"observation_id", "producer_payload_hash"}:
                        self.assertEqual(exported[key], value)

    def test_target_exists_refusal(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source_root, source = self._collector_partition(root)
            target = root / "already.jsonl"
            target.write_bytes(b"occupied\n")
            with self.assertRaisesRegex(subject.ExportRefused, "target partition already exists") as caught:
                subject.export_partition(
                    source,
                    target,
                    source_root=source_root,
                    exported_at_utc=EXPORTED_AT,
                )
            self.assertEqual(caught.exception.code, "target_exists")

    def test_malformed_line_refusal(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "bad.jsonl"
            source.write_bytes(b'{"not":\n')
            with self.assertRaisesRegex(subject.ExportRefused, "not parseable JSON") as caught:
                subject.export_partition(
                    source,
                    root / "out.jsonl",
                    source_root=root,
                    exported_at_utc=EXPORTED_AT,
                )
            self.assertEqual(caught.exception.code, "source_line_invalid")

    def test_empty_partition_refusal(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "empty.jsonl"
            source.write_bytes(b"")
            with self.assertRaisesRegex(subject.ExportRefused, "source partition is empty") as caught:
                subject.export_partition(
                    source,
                    root / "out.jsonl",
                    source_root=root,
                    exported_at_utc=EXPORTED_AT,
                )
            self.assertEqual(caught.exception.code, "empty_partition")

    def test_target_reread_byte_identity_refusal(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source_root, source = self._collector_partition(root)
            target = root / "tampered-read.jsonl"
            original_read_bytes = Path.read_bytes

            def changed_target_read(path):
                data = original_read_bytes(path)
                if path == target:
                    return data + b"tamper"
                return data

            with mock.patch.object(Path, "read_bytes", autospec=True, side_effect=changed_target_read):
                with self.assertRaisesRegex(subject.ExportRefused, "re-read differs") as caught:
                    subject.export_partition(
                        source,
                        target,
                        source_root=source_root,
                        exported_at_utc=EXPORTED_AT,
                    )
            self.assertEqual(caught.exception.code, "target_verify_failed")

    def test_two_exports_are_byte_identical(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source_root, source = self._collector_partition(root)
            first = root / "first.jsonl"
            second = root / "second.jsonl"
            subject.export_partition(
                source, first, source_root=source_root, exported_at_utc=EXPORTED_AT
            )
            subject.export_partition(
                source, second, source_root=source_root, exported_at_utc=EXPORTED_AT
            )
            self.assertEqual(first.read_bytes(), second.read_bytes())
            self.assertEqual(
                Path(str(first) + ".p030export.json").read_bytes(),
                Path(str(second) + ".p030export.json").read_bytes(),
            )

    def test_prefixed_identity_mismatch_is_refused(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source_root, source = self._collector_partition(root)
            rows = [json.loads(line) for line in source.read_text(encoding="utf-8").splitlines()]
            rows[0]["observation_id"] = "p030obs-v1:" + "0" * 64
            source.write_text(
                "".join(
                    json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n"
                    for row in rows
                ),
                encoding="utf-8",
            )
            with self.assertRaisesRegex(subject.ExportRefused, "stored prefixed observation_id") as caught:
                subject.export_partition(
                    source,
                    root / "out.jsonl",
                    source_root=source_root,
                    exported_at_utc=EXPORTED_AT,
                )
            self.assertEqual(caught.exception.code, "identity_mismatch")


if __name__ == "__main__":
    unittest.main(verbosity=2)
