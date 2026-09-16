"""Executable checks for the P030 Shape-B archive exporter."""

from __future__ import annotations

import hashlib
import json
import subprocess
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
                collector_fixtures.raw_bar(base + offset * collector_fixtures.STEP),
                source_producer="WS_LIVE",
                ingest_time=now,
                env_lineage_id="fixture-lineage",
                identities=collector_fixtures.IDENTITIES,
            )
            self.assertIsNotNone(bar)
            self.assertEqual(archive.append_bar(bar), "APPENDED")
        source = source_root / "bars" / "HYPERLIQUID" / "BTC" / "15m" / "2026-02.jsonl"
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

    def test_exported_collector_fixture_is_accepted_by_stable_prefix_adapter(
        self,
    ) -> None:
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
            self.assertEqual(
                stable["dataset_content_hash"], receipt.dataset_content_hash
            )
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
            self.assertEqual(
                stored["source_path"], source.relative_to(source_root).as_posix()
            )
            self.assertEqual(
                stored["source_sha256"], hashlib.sha256(source.read_bytes()).hexdigest()
            )
            self.assertEqual(
                stored["exported_sha256"],
                hashlib.sha256(target.read_bytes()).hexdigest(),
            )
            self.assertEqual(stored["source_record_count"], 2)
            self.assertEqual(stored["exported_record_count"], 2)
            self.assertTrue(stored["identity_recomputed"])
            self.assertEqual(stored["exported_at_utc"], EXPORTED_AT)
            self.assertEqual(
                stored["exporter_sha256"],
                hashlib.sha256(
                    Path(subject.__file__).read_bytes().replace(b"\r\n", b"\n")
                ).hexdigest(),
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
                self.assertRegex(
                    exported["observation_id"], r"^p030obs-v1:[0-9a-f]{64}$"
                )
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
            with self.assertRaisesRegex(
                subject.ExportRefused, "target partition already exists"
            ) as caught:
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
            with self.assertRaisesRegex(
                subject.ExportRefused, "not parseable JSON"
            ) as caught:
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
            with self.assertRaisesRegex(
                subject.ExportRefused, "source partition is empty"
            ) as caught:
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

            staging = Path(str(target) + subject.STAGING_SUFFIX)

            def changed_target_read(path):
                data = original_read_bytes(path)
                if path == staging:
                    return data + b"tamper"
                return data

            with mock.patch.object(
                Path, "read_bytes", autospec=True, side_effect=changed_target_read
            ):
                with self.assertRaisesRegex(
                    subject.ExportRefused, "re-read differs"
                ) as caught:
                    subject.export_partition(
                        source,
                        target,
                        source_root=source_root,
                        exported_at_utc=EXPORTED_AT,
                    )
            self.assertEqual(caught.exception.code, "target_verify_failed")
            # lane-3 T0 review finding 1: a verify refusal publishes nothing under the target name
            self.assertFalse(target.exists())
            self.assertFalse(Path(str(target) + ".p030export.json").exists())
            self.assertTrue(staging.exists())

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
            rows = [
                json.loads(line)
                for line in source.read_text(encoding="utf-8").splitlines()
            ]
            rows[0]["observation_id"] = "p030obs-v1:" + "0" * 64
            source.write_text(
                "".join(
                    json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n"
                    for row in rows
                ),
                encoding="utf-8",
            )
            with self.assertRaisesRegex(
                subject.ExportRefused, "stored prefixed observation_id"
            ) as caught:
                subject.export_partition(
                    source,
                    root / "out.jsonl",
                    source_root=source_root,
                    exported_at_utc=EXPORTED_AT,
                )
            self.assertEqual(caught.exception.code, "identity_mismatch")


class ArchiveExporterRefusalCodeTests(unittest.TestCase):
    """One explicit negative test per ExportRefused code (Gemini K-01..K-04, O9FIX 2026-09-15).

    Codes covered here: invalid_timestamp (incl. the whole-second rule, K-03), source_outside_root,
    source_unreadable, short_read (two arms), source_line_invalid (overflow and NaN literal, K-01),
    source_line_noncanonical, source_fields_mismatch, contract_refused (row-level and slice-level,
    K-02), mixed_dataset_descriptor, receipt_exists, target_unwritable, receipt_unwritable.
    target_exists, empty_partition, target_verify_failed and identity_mismatch keep their tests above.
    """

    def _partition(self, root: Path) -> tuple[Path, Path]:
        return ArchiveExporterTests._collector_partition(self, root)

    @staticmethod
    def _rows(source: Path) -> list[dict]:
        return [
            json.loads(line) for line in source.read_text(encoding="utf-8").splitlines()
        ]

    @staticmethod
    def _write_rows(source: Path, rows: list[dict]) -> None:
        source.write_text(
            "".join(
                json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n"
                for row in rows
            ),
            encoding="utf-8",
        )

    def _refused(
        self, code: str, message_regex: str, source: Path, root: Path, **overrides
    ):
        kwargs = {
            "source_root": overrides.pop("source_root", root),
            "exported_at_utc": overrides.pop("exported_at_utc", EXPORTED_AT),
        }
        target = overrides.pop("target", root / "out.jsonl")
        with self.assertRaisesRegex(subject.ExportRefused, message_regex) as caught:
            subject.export_partition(source, target, **kwargs)
        self.assertEqual(caught.exception.code, code)
        return caught.exception

    def test_invalid_timestamp_refusals_including_sub_second(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source_root, source = self._partition(root)
            for stamp in ("2026-09-14T00:00:00.500Z", "2026-09-14T00:00:00.000001Z"):
                self._refused(
                    "invalid_timestamp",
                    "whole seconds",
                    source,
                    root,
                    source_root=source_root,
                    exported_at_utc=stamp,
                )
            for stamp in (
                "2026-09-14T00:00:00+00:00",
                "2026-09-14T00:00:00",
                "not-a-time",
                20260914,
            ):
                self._refused(
                    "invalid_timestamp",
                    "UTC Z timestamp",
                    source,
                    root,
                    source_root=source_root,
                    exported_at_utc=stamp,
                )
            self.assertFalse((root / "out.jsonl").exists())

    def test_source_outside_root_refusal(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source_root, source = self._partition(root)
            self._refused(
                "source_outside_root",
                "relative to source_root",
                source,
                root,
                source_root=root / "elsewhere",
            )

    def test_source_unreadable_refusal(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._refused(
                "source_unreadable", "unreadable", root / "missing.jsonl", root
            )

    def test_short_read_refusals(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source_root, source = self._partition(root)
            source.write_bytes(source.read_bytes().rstrip(b"\n"))
            self._refused(
                "short_read", "partial line", source, root, source_root=source_root
            )

            source_root, source = self._partition(root / "second")
            original_stat = Path.stat

            def inflated_stat(path, *args, **kwargs):
                result = original_stat(path, *args, **kwargs)
                if path == source:
                    return _StatWithSize(result, result.st_size + 1)
                return result

            with mock.patch.object(Path, "stat", inflated_stat):
                self._refused(
                    "short_read",
                    "short or partial",
                    source,
                    root / "second",
                    source_root=source_root,
                )

    def test_source_line_invalid_for_overflow_and_nan_literals(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            # one exact message per arm (Gemini K-06 / lane-3 finding 3): an overflow literal is
            # parsed and refused as non-finite; a NaN literal is refused at the parser
            for name, line, message in (
                ("overflow.jsonl", b'{"open":1e999}\n', "non-finite"),
                ("nan.jsonl", b'{"open":NaN}\n', "not parseable"),
                ("nested.jsonl", b'{"a":{"b":[1,-1e999]}}\n', "non-finite"),
            ):
                source = root / name
                source.write_bytes(line)
                self._refused("source_line_invalid", message, source, root)

    def test_source_line_noncanonical_refusal(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "pretty.jsonl"
            source.write_bytes(b'{"open": 1}\n')
            self._refused("source_line_noncanonical", "not canonical", source, root)

    def test_source_fields_mismatch_refusal(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source_root, source = self._partition(root)
            rows = self._rows(source)
            rows[0]["unexpected"] = 1
            self._write_rows(source, rows)
            self._refused(
                "source_fields_mismatch",
                "extra=\\['unexpected'\\]",
                source,
                root,
                source_root=source_root,
            )

    def test_contract_refused_from_row_identity(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source_root, source = self._partition(root)
            rows = self._rows(source)
            rows[0]["open"] = "not-a-decimal"
            self._write_rows(source, rows)
            self._refused(
                "contract_refused",
                "decimal string",
                source,
                root,
                source_root=source_root,
            )

    def test_contract_refused_from_slice_validation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source_root, source = self._partition(root)
            rows = self._rows(source)
            duplicated = [rows[0], rows[0]]
            self._write_rows(source, duplicated)
            self._refused(
                "contract_refused",
                "duplicate observation_id",
                source,
                root,
                source_root=source_root,
            )

            source_root, source = self._partition(root / "window")
            rows = self._rows(source)
            for row in rows:
                row["bar_close_time"] = row["bar_open_time"]
            self._write_rows(source, rows)
            self._refused(
                "contract_refused",
                "must be after bar_open_time",
                source,
                root / "window",
                source_root=source_root,
            )

    def test_mixed_dataset_descriptor_refusal(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source_root, source = self._partition(root)
            rows = self._rows(source)
            rows[1]["venue"] = "OTHERVENUE"
            self._write_rows(source, rows)
            self._refused(
                "mixed_dataset_descriptor",
                "does not match descriptor",
                source,
                root,
                source_root=source_root,
            )

    def test_receipt_exists_refusal(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source_root, source = self._partition(root)
            target = root / "out.jsonl"
            Path(str(target) + ".p030export.json").write_bytes(b"{}\n")
            self._refused(
                "receipt_exists",
                "receipt already exists",
                source,
                root,
                source_root=source_root,
                target=target,
            )
            self.assertFalse(target.exists())

    def test_target_and_receipt_unwritable_refusals(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source_root, source = self._partition(root)
            target = root / "out.jsonl"
            original_open = Path.open

            staging_target = Path(str(target) + subject.STAGING_SUFFIX)

            def denied_target(path, *args, **kwargs):
                if path == staging_target:
                    raise PermissionError("target denied")
                return original_open(path, *args, **kwargs)

            with mock.patch.object(Path, "open", denied_target):
                self._refused(
                    "target_unwritable",
                    "unwritable",
                    source,
                    root,
                    source_root=source_root,
                    target=target,
                )
            self.assertFalse(target.exists())
            self.assertFalse(staging_target.exists())

            receipt = Path(str(target) + ".p030export.json")
            staging_receipt = Path(str(receipt) + subject.STAGING_SUFFIX)

            def denied_receipt(path, *args, **kwargs):
                if path == staging_receipt:
                    raise PermissionError("receipt denied")
                return original_open(path, *args, **kwargs)

            with mock.patch.object(Path, "open", denied_receipt):
                self._refused(
                    "receipt_unwritable",
                    "receipt is unwritable",
                    source,
                    root,
                    source_root=source_root,
                    target=target,
                )
            # lane-3 T0 review finding 1 / 7: a receipt refusal publishes nothing under the target name
            self.assertFalse(target.exists())
            self.assertFalse(receipt.exists())
            self.assertTrue(staging_target.exists())

    def test_mid_write_failure_publishes_nothing_under_the_target_name(self) -> None:
        """Lane-3 T0 review finding 1: an ENOSPC-shaped failure after the file was created must not
        leave a truncated partition under the target name (the adapter would accept it)."""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source_root, source = self._partition(root)
            target = root / "out.jsonl"
            staging_target = Path(str(target) + subject.STAGING_SUFFIX)
            original_open = Path.open

            def half_then_enospc(path, *args, **kwargs):
                handle = original_open(path, *args, **kwargs)
                if path == staging_target and args and "x" in args[0]:
                    real_write = handle.write

                    def write(data):
                        real_write(data[: len(data) // 2])
                        raise OSError(28, "No space left on device")

                    handle.write = write
                return handle

            with mock.patch.object(Path, "open", half_then_enospc):
                self._refused(
                    "target_unwritable",
                    "nothing was published",
                    source,
                    root,
                    source_root=source_root,
                    target=target,
                )
            self.assertFalse(target.exists())
            self.assertFalse(Path(str(target) + ".p030export.json").exists())
            # the half-written bytes exist only under the staging name, which is never a partition name
            self.assertTrue(staging_target.exists())
            self.assertTrue(staging_target.name.endswith(subject.STAGING_SUFFIX))
            self.assertLess(staging_target.stat().st_size, source.stat().st_size)
            # a second run refuses on the leftover instead of adopting or removing it
            self._refused(
                "target_exists",
                "staging partial",
                source,
                root,
                source_root=source_root,
                target=target,
            )
            self.assertTrue(staging_target.exists())

    def test_publish_failure_of_the_target_leaves_receipt_without_partition(
        self,
    ) -> None:
        """The documented residual window: the receipt is published first (inert alone); if taking the
        target name then fails, the partition stays under the staging name."""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source_root, source = self._partition(root)
            target = root / "out.jsonl"
            staging_target = Path(str(target) + subject.STAGING_SUFFIX)
            receipt = Path(str(target) + ".p030export.json")
            original_replace = subject.os.replace

            def deny_target_publish(src, dst, *args, **kwargs):
                if Path(dst) == target:
                    raise PermissionError("publish denied")
                return original_replace(src, dst, *args, **kwargs)

            with mock.patch.object(subject.os, "replace", deny_target_publish):
                self._refused(
                    "target_unwritable",
                    "could not be published",
                    source,
                    root,
                    source_root=source_root,
                    target=target,
                )
            self.assertFalse(target.exists())
            self.assertTrue(receipt.exists())
            self.assertTrue(staging_target.exists())
            self.assertEqual(staging_target.read_bytes().count(b"\n"), 2)

    def test_exporter_sha256_is_the_lf_form_on_any_checkout(self) -> None:
        """Lane-3 T0 review finding 5: the receipt's exporter digest must not depend on CRLF checkout."""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source_root, source = self._partition(root)
            module = Path(subject.__file__)
            lf_digest = hashlib.sha256(
                module.read_bytes().replace(b"\r\n", b"\n")
            ).hexdigest()
            receipt = subject.export_partition(
                source,
                root / "a.jsonl",
                source_root=source_root,
                exported_at_utc=EXPORTED_AT,
            )
            self.assertEqual(receipt.exporter_sha256, lf_digest)
            original_read_bytes = Path.read_bytes

            def crlf_checkout(path):
                data = original_read_bytes(path)
                if path == module:
                    return data.replace(b"\r\n", b"\n").replace(b"\n", b"\r\n")
                return data

            with mock.patch.object(
                Path, "read_bytes", autospec=True, side_effect=crlf_checkout
            ):
                receipt_crlf = subject.export_partition(
                    source,
                    root / "b.jsonl",
                    source_root=source_root,
                    exported_at_utc=EXPORTED_AT,
                )
            self.assertEqual(receipt_crlf.exporter_sha256, lf_digest)

    def test_dotdot_traversal_is_refused_even_when_lexically_under_root(self) -> None:
        """Lane-3 T0 review finding 2: `..` components used to pass the lexical relative_to check
        and land in the receipt as `../../outside/...`."""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source_root, source = self._partition(root)
            outside = root / "outside"
            outside.mkdir()
            (outside / "2026-02.jsonl").write_bytes(source.read_bytes())
            declared_root = source_root / "bars"
            traversal = declared_root / ".." / ".." / "outside" / "2026-02.jsonl"
            self.assertTrue(traversal.exists())
            self._refused(
                "source_outside_root",
                "canonical relative POSIX",
                traversal,
                root,
                source_root=declared_root,
            )
            with self.assertRaises(ValueError):
                capture_stable_prefix(
                    traversal,
                    root / "stable",
                    source_root=declared_root,
                    high_water_bytes=10,
                    captured_at_utc=CAPTURED_AT,
                    dataset_content_hash="p030ds-v1:" + "0" * 64,
                )

    def test_percent_encoded_segments_are_refused_like_the_adapter(self) -> None:
        """Gemini delta review of the repair (P030_R1 NIT 2): the adapter refuses percent-escaped
        spellings such as ``%2e%2e`` as non-canonical; the exporter must refuse the same input."""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source_root, source = self._partition(root)
            escaped_dir = source_root / "%2e%2e"
            escaped_dir.mkdir()
            escaped = escaped_dir / "2026-02.jsonl"
            escaped.write_bytes(source.read_bytes())
            self._refused(
                "source_outside_root",
                "canonical relative POSIX",
                escaped,
                root,
                source_root=source_root,
            )
            with self.assertRaises(ValueError):
                capture_stable_prefix(
                    escaped,
                    root / "stable",
                    source_root=source_root,
                    high_water_bytes=10,
                    captured_at_utc=CAPTURED_AT,
                    dataset_content_hash="p030ds-v1:" + "0" * 64,
                )

    def test_junction_component_is_refused_like_the_adapter(self) -> None:
        """Lane-3 T0 review finding 2: a junction inside the root that points outside must be refused
        by the exporter exactly as the adapter refuses it on the same field."""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            _, source = self._partition(root)
            jroot = root / "jroot"
            jroot.mkdir()
            outside = root / "joutside"
            outside.mkdir()
            (outside / "2026-02.jsonl").write_bytes(source.read_bytes())
            link = jroot / "link"
            created = subprocess.run(
                ["cmd", "/c", "mklink", "/J", str(link), str(outside)],
                capture_output=True,
                text=True,
                check=False,
            )
            if created.returncode != 0 or not link.is_junction():
                self.skipTest("cannot create an NTFS junction on this host")
            self._refused(
                "source_outside_root",
                "symlink or junction",
                link / "2026-02.jsonl",
                root,
                source_root=jroot,
            )
            with self.assertRaises(ValueError):
                capture_stable_prefix(
                    link / "2026-02.jsonl",
                    root / "stable",
                    source_root=jroot,
                    high_water_bytes=10,
                    captured_at_utc=CAPTURED_AT,
                    dataset_content_hash="p030ds-v1:" + "0" * 64,
                )
            self.assertFalse((root / "out.jsonl").exists())


class _StatWithSize:
    """os.stat_result stand-in that reports a larger st_size."""

    def __init__(self, result, st_size: int) -> None:
        self._result = result
        self.st_size = st_size

    def __getattr__(self, name):
        return getattr(self._result, name)


if __name__ == "__main__":
    unittest.main(verbosity=2)
