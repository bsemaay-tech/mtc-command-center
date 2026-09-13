"""Synthetic-only checks for P030 stable-prefix backup and verified restore."""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import tempfile
import types
import unittest
from pathlib import Path
from unittest import mock

import p030_closed_partition_backup_adapter as subject


class StablePrefixBackupAdapterTests(unittest.TestCase):
    STORE_ID = "fixture-p030-archive"
    CAPTURED_AT = "2026-09-12T00:00:00Z"
    DATASET_CONTENT_HASH = "p030ds-v1:" + "a" * 64
    OBS_1 = "p030obs-v1:" + "1" * 64
    OBS_2 = "p030obs-v1:" + "2" * 64
    OBS_3 = "p030obs-v1:" + "3" * 64

    @staticmethod
    def _line(observation_id: str, close: int) -> bytes:
        return (
            json.dumps(
                {"close": close, "observation_id": observation_id},
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
            )
            + "\n"
        ).encode("utf-8")

    def _capture(self, root: Path) -> tuple[Path, Path, Path, bytes]:
        source_root = root / "source-root"
        source = source_root / "feeds" / "live.jsonl"
        source.parent.mkdir(parents=True)
        prefix = self._line(self.OBS_1, 10) + self._line(self.OBS_2, 11)
        source.write_bytes(prefix)
        stable = root / "stable-prefix"
        receipt = subject.capture_stable_prefix(
            source,
            stable,
            source_root=source_root,
            high_water_bytes=len(prefix),
            captured_at_utc=self.CAPTURED_AT,
            dataset_content_hash=self.DATASET_CONTENT_HASH,
        )
        return source, stable, receipt, prefix

    def _runnable_config(self, root: Path, stable: Path) -> Path:
        config_path = root / "backup-config.json"
        config_path.write_text(
            json.dumps(
                {
                    "schema": "mtc.opsa_backup_config/v1",
                    "backup_root": str(root / "backups"),
                    "stores": [
                        {"id": self.STORE_ID, "path": str(stable), "class": "protected"}
                    ],
                }
            ),
            encoding="utf-8",
        )
        return config_path

    def test_committed_configuration_is_explicitly_non_runnable(self) -> None:
        config_path = Path(__file__).with_name("p030_opsa_backup_config.json")
        config = json.loads(config_path.read_text(encoding="utf-8"))
        self.assertEqual(config["schema"], "mtc.opsa_backup_config/v1")
        self.assertIsNone(config["backup_root"])
        self.assertIsNone(config["stores"][0]["id"])
        self.assertIsNone(config["stores"][0]["path"])
        self.assertEqual(config["stores"][0]["class"], "protected")
        with tempfile.TemporaryDirectory() as temporary, mock.patch.object(
            subject.backup, "run_backup"
        ) as run_backup, mock.patch.object(
            subject.restore, "run_restore"
        ) as run_restore:
            root = Path(temporary)
            with self.assertRaisesRegex(ValueError, "backup config is not runnable"):
                subject.backup_stable_prefix(
                    config_path,
                    stable_receipt=root / "synthetic-receipt.json",
                    store_id=self.STORE_ID,
                    source_root=root / "synthetic-source",
                )
            target = root / "synthetic-empty-target"
            target.mkdir()
            with self.assertRaisesRegex(ValueError, "backup config is not runnable"):
                subject.restore_verified_prefix(
                    config_path,
                    run_id="opsa-synthetic",
                    store_id=self.STORE_ID,
                    target=target,
                )
        run_backup.assert_not_called()
        run_restore.assert_not_called()

    def test_capture_binds_exact_canonical_complete_prefix_and_allows_later_append(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source, stable, receipt_path, prefix = self._capture(root)
            receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
            self.assertEqual(
                set(receipt),
                {
                    "schema",
                    "state",
                    "source_path",
                    "snapshot_rel",
                    "high_water_bytes",
                    "record_count",
                    "last_observation_id",
                    "prefix_sha256",
                    "captured_at_utc",
                    "dataset_content_hash",
                },
            )
            self.assertEqual(receipt["state"], "stable_prefix")
            self.assertEqual(receipt["high_water_bytes"], len(prefix))
            self.assertEqual(receipt["record_count"], 2)
            self.assertEqual(receipt["last_observation_id"], self.OBS_2)
            self.assertEqual(receipt["source_path"], "feeds/live.jsonl")
            self.assertFalse(Path(receipt["source_path"]).is_absolute())
            self.assertEqual(receipt["captured_at_utc"], self.CAPTURED_AT)
            self.assertEqual(receipt["dataset_content_hash"], self.DATASET_CONTENT_HASH)
            self.assertEqual((stable / receipt["snapshot_rel"]).read_bytes(), prefix)

            with source.open("ab") as handle:
                handle.write(self._line(self.OBS_3, 12))
            config_path = self._runnable_config(root, stable)
            run_id = subject.backup_stable_prefix(
                config_path,
                stable_receipt=receipt_path,
                store_id=self.STORE_ID,
                source_root=root / "source-root",
            )
            self.assertTrue(run_id.startswith("opsa-"))

    def test_capture_refuses_partial_line_and_noncanonical_jsonl(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "live.jsonl"
            canonical = self._line(self.OBS_1, 10)
            source.write_bytes(canonical)
            with self.assertRaisesRegex(ValueError, "high-water prefix must end with newline"):
                subject.capture_stable_prefix(
                    source,
                    root / "partial",
                    source_root=root,
                    high_water_bytes=len(canonical) - 1,
                    captured_at_utc=self.CAPTURED_AT,
                    dataset_content_hash=self.DATASET_CONTENT_HASH,
                )
            source.write_text(
                json.dumps({"observation_id": self.OBS_1, "close": 10}) + "\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "prefix record is not canonical JSONL"):
                subject.capture_stable_prefix(
                    source,
                    root / "noncanonical",
                    source_root=root,
                    high_water_bytes=source.stat().st_size,
                    captured_at_utc=self.CAPTURED_AT,
                    dataset_content_hash=self.DATASET_CONTENT_HASH,
                )

    def test_capture_refuses_noncontract_dataset_and_observation_identities(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "live.jsonl"
            source.write_bytes(self._line(self.OBS_1, 10))
            with self.assertRaisesRegex(ValueError, "dataset_content_hash must match p030ds-v1"):
                subject.capture_stable_prefix(
                    source,
                    root / "bad-dataset",
                    source_root=root,
                    high_water_bytes=source.stat().st_size,
                    captured_at_utc=self.CAPTURED_AT,
                    dataset_content_hash="not-a-p030-dataset-id",
                )
            source.write_bytes(self._line("not-a-p030-observation-id", 10))
            with self.assertRaisesRegex(ValueError, "observation_id must match p030obs-v1"):
                subject.capture_stable_prefix(
                    source,
                    root / "bad-observation",
                    source_root=root,
                    high_water_bytes=source.stat().st_size,
                    captured_at_utc=self.CAPTURED_AT,
                    dataset_content_hash=self.DATASET_CONTENT_HASH,
                )

    def test_capture_refuses_nonfinite_json_constants(self) -> None:
        for constant in ("NaN", "Infinity", "-Infinity"):
            with self.subTest(constant=constant), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                source = root / "live.jsonl"
                source.write_bytes(
                    (
                        '{"close":'
                        + constant
                        + ',"observation_id":"'
                        + self.OBS_1
                        + '"}\n'
                    ).encode("utf-8")
                )
                with self.assertRaisesRegex(ValueError, "non-finite JSON constant"):
                    subject.capture_stable_prefix(
                        source,
                        root / "stable",
                        source_root=root,
                        high_water_bytes=source.stat().st_size,
                        captured_at_utc=self.CAPTURED_AT,
                        dataset_content_hash=self.DATASET_CONTENT_HASH,
                    )

    def test_capture_refuses_caller_supplied_symlink_before_resolution(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source_link = root / "linked.jsonl"
            source_link.write_bytes(self._line(self.OBS_1, 10))
            stable = root / "stable"
            original_resolve = subject.Path.resolve

            def refuse_source_resolution(path, *args, **kwargs):
                if path == source_link:
                    raise AssertionError("caller source was resolved before symlink refusal")
                return original_resolve(path, *args, **kwargs)

            def fixture_is_symlink(path):
                return path == source_link

            with mock.patch.object(
                subject.Path, "resolve", autospec=True, side_effect=refuse_source_resolution
            ), mock.patch.object(
                subject.Path, "is_symlink", autospec=True, side_effect=fixture_is_symlink
            ):
                with self.assertRaisesRegex(ValueError, "source JSONL must not be a symlink"):
                    subject.capture_stable_prefix(
                        source_link,
                        stable,
                        source_root=root,
                        high_water_bytes=source_link.stat().st_size,
                        captured_at_utc=self.CAPTURED_AT,
                        dataset_content_hash=self.DATASET_CONTENT_HASH,
                    )
            self.assertFalse(stable.exists())

    def test_capture_and_prebackup_refuse_real_junction_ancestor(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            physical = root / "physical"
            physical_source_root = physical / "source-root"
            physical_source = physical_source_root / "feeds" / "live.jsonl"
            physical_source.parent.mkdir(parents=True)
            prefix = self._line(self.OBS_1, 10)
            physical_source.write_bytes(prefix)
            junction = root / "junction-ancestor"
            created = subprocess.run(
                ["cmd", "/c", "mklink", "/J", str(junction), str(physical)],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(created.returncode, 0, created.stderr or created.stdout)
            self.assertTrue(junction.is_junction())

            stable = root / "stable"
            with self.assertRaisesRegex(ValueError, "symlink or junction"):
                subject.capture_stable_prefix(
                    junction / "source-root" / "feeds" / "live.jsonl",
                    stable,
                    source_root=junction / "source-root",
                    high_water_bytes=len(prefix),
                    captured_at_utc=self.CAPTURED_AT,
                    dataset_content_hash=self.DATASET_CONTENT_HASH,
                )
            self.assertFalse(stable.exists())

            receipt = subject.capture_stable_prefix(
                physical_source,
                stable,
                source_root=physical_source_root,
                high_water_bytes=len(prefix),
                captured_at_utc=self.CAPTURED_AT,
                dataset_content_hash=self.DATASET_CONTENT_HASH,
            )
            config_path = self._runnable_config(root, stable)
            with mock.patch.object(subject.backup, "run_backup") as run_backup:
                with self.assertRaisesRegex(ValueError, "symlink or junction"):
                    subject.backup_stable_prefix(
                        config_path,
                        stable_receipt=receipt,
                        store_id=self.STORE_ID,
                        source_root=junction / "source-root",
                    )
            run_backup.assert_not_called()

    def test_capture_refuses_intermediate_symlink_or_junction_component(self) -> None:
        for link_kind in ("is_symlink", "is_junction"):
            with self.subTest(link_kind=link_kind), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                source_root = root / "source-root"
                intermediate = source_root / "feeds"
                source = intermediate / "live.jsonl"
                intermediate.mkdir(parents=True)
                source.write_bytes(self._line(self.OBS_1, 10))
                original = getattr(subject.Path, link_kind)

                def fixture_link(path, *args, **kwargs):
                    return path == intermediate or original(path, *args, **kwargs)

                with mock.patch.object(
                    subject.Path, link_kind, autospec=True, side_effect=fixture_link
                ):
                    with self.assertRaisesRegex(ValueError, "symlink or junction"):
                        subject.capture_stable_prefix(
                            source,
                            root / "stable",
                            source_root=source_root,
                            high_water_bytes=source.stat().st_size,
                            captured_at_utc=self.CAPTURED_AT,
                            dataset_content_hash=self.DATASET_CONTENT_HASH,
                        )

    def test_post_backup_verification_refuses_replaced_intermediate_component(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            _, stable, receipt, _ = self._capture(root)
            config_path = self._runnable_config(root, stable)
            ancestor_above_source_root = root
            unchanged_backup = subject.backup.run_backup
            unchanged_is_symlink = subject.Path.is_symlink
            replaced = False

            def replace_after_backup(*args, **kwargs):
                nonlocal replaced
                result = unchanged_backup(*args, **kwargs)
                replaced = True
                return result

            def fixture_is_symlink(path, *args, **kwargs):
                return (
                    replaced and path == ancestor_above_source_root
                ) or unchanged_is_symlink(path, *args, **kwargs)

            with mock.patch.object(
                subject.backup, "run_backup", side_effect=replace_after_backup
            ), mock.patch.object(
                subject.Path, "is_symlink", autospec=True, side_effect=fixture_is_symlink
            ):
                with self.assertRaisesRegex(ValueError, "symlink or junction"):
                    subject.backup_stable_prefix(
                        config_path,
                        stable_receipt=receipt,
                        store_id=self.STORE_ID,
                        source_root=root / "source-root",
                    )

    def test_backup_refuses_prefix_mutation_or_truncation_before_p026(self) -> None:
        for condition in ("mutation", "truncation"):
            with self.subTest(condition=condition), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                source, stable, receipt, prefix = self._capture(root)
                config_path = self._runnable_config(root, stable)
                if condition == "mutation":
                    source.write_bytes(prefix.replace(b"1" * 64, b"f" * 64, 1))
                else:
                    source.write_bytes(self._line(self.OBS_1, 10))
                with mock.patch.object(subject.backup, "run_backup") as run_backup:
                    with self.assertRaisesRegex(ValueError, "source prefix"):
                        subject.backup_stable_prefix(
                            config_path,
                            stable_receipt=receipt,
                            store_id=self.STORE_ID,
                            source_root=root / "source-root",
                        )
                run_backup.assert_not_called()

    def test_config_refuses_duplicate_keys_and_nonfinite_json_before_p026(self) -> None:
        for kind in ("duplicate", "nonfinite"):
            with self.subTest(kind=kind), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                _, stable, receipt, _ = self._capture(root)
                config_path = self._runnable_config(root, stable)
                raw = config_path.read_text(encoding="utf-8")
                if kind == "duplicate":
                    raw = raw.replace(
                        '"schema": "mtc.opsa_backup_config/v1"',
                        '"schema": "mtc.opsa_backup_config/v1", '
                        '"schema": "mtc.opsa_backup_config/v1"',
                    )
                    expected = "duplicate JSON key"
                else:
                    raw = raw[:-1] + ', "synthetic_probe": NaN}'
                    expected = "non-finite JSON constant"
                config_path.write_text(raw, encoding="utf-8")
                with mock.patch.object(subject.backup, "run_backup") as run_backup:
                    with self.assertRaisesRegex(ValueError, expected):
                        subject.backup_stable_prefix(
                            config_path,
                            stable_receipt=receipt,
                            store_id=self.STORE_ID,
                            source_root=root / "source-root",
                        )
                run_backup.assert_not_called()

    def test_config_and_receipt_refuse_nested_overflowed_numbers_before_p026(
        self,
    ) -> None:
        for container in ("config", "receipt"):
            with self.subTest(container=container), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                _, stable, receipt, _ = self._capture(root)
                config_path = self._runnable_config(root, stable)
                path = config_path if container == "config" else receipt
                raw = path.read_text(encoding="utf-8").rstrip()
                raw = raw[:-1] + ', "synthetic_probe": {"nested": [1e9999]}}'
                path.write_text(raw, encoding="utf-8")
                with mock.patch.object(subject.backup, "run_backup") as run_backup:
                    with self.assertRaisesRegex(ValueError, "non-finite JSON number"):
                        subject.backup_stable_prefix(
                            config_path,
                            stable_receipt=receipt,
                            store_id=self.STORE_ID,
                            source_root=root / "source-root",
                        )
                run_backup.assert_not_called()

    def test_backup_consumes_bound_config_when_original_is_swapped(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            _, stable, receipt, _ = self._capture(root)
            config_path = self._runnable_config(root, stable)
            original_backup = subject.backup.run_backup
            swapped_root = root / "swapped-backups"

            def swap_original_before_p026(bound_config_path, *args, **kwargs):
                config_path.write_text(
                    json.dumps(
                        {
                            "schema": "mtc.opsa_backup_config/v1",
                            "backup_root": str(swapped_root),
                            "stores": [
                                {
                                    "id": self.STORE_ID,
                                    "path": str(stable),
                                    "class": "protected",
                                }
                            ],
                        }
                    ),
                    encoding="utf-8",
                )
                self.assertNotEqual(Path(bound_config_path), config_path)
                return original_backup(bound_config_path, *args, **kwargs)

            with mock.patch.object(
                subject.backup,
                "run_backup",
                side_effect=swap_original_before_p026,
            ):
                run_id = subject.backup_stable_prefix(
                    config_path,
                    stable_receipt=receipt,
                    store_id=self.STORE_ID,
                    source_root=root / "source-root",
                )
            self.assertTrue((root / "backups" / "runs" / run_id).is_dir())
            self.assertFalse(swapped_root.exists())

    def test_restore_checks_first_and_produces_verified_receipt(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            _, stable, receipt, _ = self._capture(root)
            config_path = self._runnable_config(root, stable)
            run_id = subject.backup_stable_prefix(
                config_path,
                stable_receipt=receipt,
                store_id=self.STORE_ID,
                source_root=root / "source-root",
            )
            target = root / "restore-target"
            target.mkdir()
            unchanged_restore = subject.restore.run_restore
            calls: list[tuple[bool, Path | None]] = []

            def record_restore(*args, **kwargs):
                calls.append((kwargs["check_only"], args[2]))
                return unchanged_restore(*args, **kwargs)

            with mock.patch.object(subject.restore, "run_restore", side_effect=record_restore):
                verified = subject.restore_verified_prefix(
                    config_path, run_id=run_id, store_id=self.STORE_ID, target=target
                )
            self.assertEqual([call[0] for call in calls], [True, False])
            self.assertIsNone(calls[0][1])
            self.assertTrue(calls[1][1].samefile(target))
            receipt = json.loads(verified.read_text(encoding="utf-8"))
            self.assertEqual(receipt["schema"], "p030.verified_restore/v1")
            self.assertEqual(receipt["state"], "verified_restore")

    def test_restore_refuses_rehashed_archive_with_dot_source_path(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            _, stable, receipt, _ = self._capture(root)
            config_path = self._runnable_config(root, stable)
            run_id = subject.backup_stable_prefix(
                config_path,
                stable_receipt=receipt,
                store_id=self.STORE_ID,
                source_root=root / "source-root",
            )
            backup_root = root / "backups"
            archived_receipt = (
                backup_root
                / "runs"
                / run_id
                / self.STORE_ID
                / subject.STABLE_RECEIPT_NAME
            )
            receipt_object = json.loads(archived_receipt.read_bytes())
            receipt_object["source_path"] = "."
            receipt_raw = (
                json.dumps(
                    receipt_object,
                    ensure_ascii=False,
                    sort_keys=True,
                    indent=2,
                )
                + "\n"
            ).encode("utf-8")
            archived_receipt.write_bytes(receipt_raw)
            manifest = backup_root / "manifest.jsonl"
            records = [json.loads(line) for line in manifest.read_bytes().splitlines()]
            receipt_record = next(
                record
                for record in records
                if record.get("run_id") == run_id
                and record.get("record") == "file"
                and record.get("rel") == subject.STABLE_RECEIPT_NAME
            )
            receipt_record["size"] = len(receipt_raw)
            receipt_record["sha256"] = hashlib.sha256(receipt_raw).hexdigest()
            run_end = next(
                record
                for record in records
                if record.get("run_id") == run_id
                and record.get("record") == "run_end"
            )
            run_end["bytes"] = sum(
                record["size"]
                for record in records
                if record.get("run_id") == run_id
                and record.get("record") == "file"
            )
            manifest.write_bytes(
                b"".join(
                    (json.dumps(record, sort_keys=True) + "\n").encode("utf-8")
                    for record in records
                )
            )
            target = root / "restore-target"
            target.mkdir()
            unchanged_restore = subject.restore.run_restore
            with mock.patch.object(
                subject.restore, "run_restore", wraps=unchanged_restore
            ) as run_restore:
                with self.assertRaisesRegex(ValueError, "source_path"):
                    subject.restore_verified_prefix(
                        config_path,
                        run_id=run_id,
                        store_id=self.STORE_ID,
                        target=target,
                    )
            run_restore.assert_not_called()
            self.assertFalse(
                (target / subject.VERIFIED_RESTORE_RECEIPT_NAME).exists()
            )

    def test_manifest_refuses_duplicate_keys_and_nonfinite_json_before_p026(self) -> None:
        for kind in ("duplicate", "nonfinite"):
            with self.subTest(kind=kind), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                _, stable, receipt, _ = self._capture(root)
                config_path = self._runnable_config(root, stable)
                run_id = subject.backup_stable_prefix(
                    config_path,
                    stable_receipt=receipt,
                    store_id=self.STORE_ID,
                    source_root=root / "source-root",
                )
                manifest = root / "backups" / "manifest.jsonl"
                lines = manifest.read_text(encoding="utf-8").splitlines()
                if kind == "duplicate":
                    lines[0] = lines[0][:-1] + ', "record": "run_start"}'
                    expected = "duplicate JSON key"
                else:
                    lines[0] = lines[0][:-1] + ', "synthetic_probe": NaN}'
                    expected = "non-finite JSON constant"
                manifest.write_text("\n".join(lines) + "\n", encoding="utf-8")
                target = root / "restore-target"
                target.mkdir()
                with mock.patch.object(subject.restore, "run_restore") as run_restore:
                    with self.assertRaisesRegex(ValueError, expected):
                        subject.restore_verified_prefix(
                            config_path,
                            run_id=run_id,
                            store_id=self.STORE_ID,
                            target=target,
                        )
                run_restore.assert_not_called()

    def test_manifest_refuses_boolean_size_and_byte_totals_before_p026(self) -> None:
        for field in ("file.size", "run_end.bytes"):
            with self.subTest(field=field), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                _, stable, receipt, _ = self._capture(root)
                config_path = self._runnable_config(root, stable)
                run_id = subject.backup_stable_prefix(
                    config_path,
                    stable_receipt=receipt,
                    store_id=self.STORE_ID,
                    source_root=root / "source-root",
                )
                manifest = root / "backups" / "manifest.jsonl"
                records = [
                    json.loads(line)
                    for line in manifest.read_text(encoding="utf-8").splitlines()
                ]
                if field == "file.size":
                    next(
                        record
                        for record in records
                        if record.get("record") == "file"
                    )["size"] = True
                    next(
                        record
                        for record in records
                        if record.get("record") == "run_end"
                    )["bytes"] = sum(
                        record["size"]
                        for record in records
                        if record.get("record") == "file"
                    )
                else:
                    for record in records:
                        if record.get("record") == "file":
                            record["size"] = 0
                    next(
                        record
                        for record in records
                        if record.get("record") == "file"
                    )["size"] = 1
                    next(
                        record
                        for record in records
                        if record.get("record") == "run_end"
                    )["bytes"] = True
                manifest.write_text(
                    "".join(
                        json.dumps(record, sort_keys=True) + "\n"
                        for record in records
                    ),
                    encoding="utf-8",
                )
                target = root / "restore-target"
                target.mkdir()
                with mock.patch.object(subject.restore, "run_restore") as run_restore:
                    with self.assertRaisesRegex(
                        ValueError, "complete successful P026 run"
                    ):
                        subject.restore_verified_prefix(
                            config_path,
                            run_id=run_id,
                            store_id=self.STORE_ID,
                            target=target,
                        )
                run_restore.assert_not_called()

    def test_manifest_refuses_inconsistent_byte_total_before_p026(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            _, stable, receipt, _ = self._capture(root)
            config_path = self._runnable_config(root, stable)
            run_id = subject.backup_stable_prefix(
                config_path,
                stable_receipt=receipt,
                store_id=self.STORE_ID,
                source_root=root / "source-root",
            )
            manifest = root / "backups" / "manifest.jsonl"
            records = [
                json.loads(line)
                for line in manifest.read_text(encoding="utf-8").splitlines()
            ]
            next(
                record
                for record in records
                if record.get("record") == "run_end"
            )["bytes"] += 1
            manifest.write_text(
                "".join(
                    json.dumps(record, sort_keys=True) + "\n" for record in records
                ),
                encoding="utf-8",
            )
            target = root / "restore-target"
            target.mkdir()
            with mock.patch.object(subject.restore, "run_restore") as run_restore:
                with self.assertRaisesRegex(
                    ValueError, "complete successful P026 run"
                ):
                    subject.restore_verified_prefix(
                        config_path,
                        run_id=run_id,
                        store_id=self.STORE_ID,
                        target=target,
                    )
            run_restore.assert_not_called()

    def test_manifest_refuses_overflowed_size_and_byte_totals_before_p026(
        self,
    ) -> None:
        for field in ("file.size", "run_end.bytes"):
            with self.subTest(field=field), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                _, stable, receipt, _ = self._capture(root)
                config_path = self._runnable_config(root, stable)
                run_id = subject.backup_stable_prefix(
                    config_path,
                    stable_receipt=receipt,
                    store_id=self.STORE_ID,
                    source_root=root / "source-root",
                )
                manifest = root / "backups" / "manifest.jsonl"
                lines = manifest.read_text(encoding="utf-8").splitlines()
                record_kind, key = field.split(".")
                for index, line in enumerate(lines):
                    record = json.loads(line)
                    if record.get("record") == record_kind:
                        lines[index] = line.replace(
                            f'"{key}": {record[key]}', f'"{key}": 1e9999'
                        )
                        break
                else:
                    self.fail(f"missing manifest record for {field}")
                manifest.write_text("\n".join(lines) + "\n", encoding="utf-8")
                target = root / "restore-target"
                target.mkdir()
                with mock.patch.object(subject.restore, "run_restore") as run_restore:
                    with self.assertRaisesRegex(ValueError, "non-finite JSON number"):
                        subject.restore_verified_prefix(
                            config_path,
                            run_id=run_id,
                            store_id=self.STORE_ID,
                            target=target,
                        )
                run_restore.assert_not_called()

    def test_manifest_is_rechecked_between_check_only_and_restore(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            _, stable, receipt, _ = self._capture(root)
            config_path = self._runnable_config(root, stable)
            run_id = subject.backup_stable_prefix(
                config_path,
                stable_receipt=receipt,
                store_id=self.STORE_ID,
                source_root=root / "source-root",
            )
            manifest = root / "backups" / "manifest.jsonl"
            target = root / "restore-target"
            target.mkdir()
            unchanged_restore = subject.restore.run_restore
            calls: list[bool] = []

            def corrupt_after_check(*args, **kwargs):
                calls.append(kwargs["check_only"])
                result = unchanged_restore(*args, **kwargs)
                if kwargs["check_only"]:
                    lines = manifest.read_text(encoding="utf-8").splitlines()
                    lines[0] = lines[0][:-1] + ', "record": "run_start"}'
                    manifest.write_text("\n".join(lines) + "\n", encoding="utf-8")
                return result

            with mock.patch.object(
                subject.restore, "run_restore", side_effect=corrupt_after_check
            ):
                with self.assertRaisesRegex(ValueError, "duplicate JSON key"):
                    subject.restore_verified_prefix(
                        config_path,
                        run_id=run_id,
                        store_id=self.STORE_ID,
                        target=target,
                    )
            self.assertEqual(calls, [True])
            self.assertEqual(list(target.iterdir()), [])

    def test_isolated_config_redirect_after_check_never_reaches_restore(self) -> None:
        for defect, expected in (
            ("duplicate_backup_root", "duplicate JSON key"),
            ("nonfinite", "non-finite JSON constant"),
        ):
            with self.subTest(defect=defect), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                _, stable, receipt, _ = self._capture(root)
                config_path = self._runnable_config(root, stable)
                run_id = subject.backup_stable_prefix(
                    config_path,
                    stable_receipt=receipt,
                    store_id=self.STORE_ID,
                    source_root=root / "source-root",
                )
                alternate_root = root / "alternate-backups"
                shutil.copytree(root / "backups", alternate_root)
                target = root / "restore-target"
                target.mkdir()
                unchanged_restore = subject.restore.run_restore
                calls: list[bool] = []

                def redirect_after_check(bound_config_path, *args, **kwargs):
                    calls.append(kwargs["check_only"])
                    result = unchanged_restore(bound_config_path, *args, **kwargs)
                    if kwargs["check_only"]:
                        raw = Path(bound_config_path).read_text(encoding="utf-8")
                        if defect == "duplicate_backup_root":
                            configured_root = json.loads(raw)["backup_root"]
                            anchor = f'  "backup_root": {json.dumps(configured_root)},'
                            replacement = (
                                anchor
                                + f'\n  "backup_root": {json.dumps(str(alternate_root))},'
                            )
                            self.assertEqual(raw.count(anchor), 1)
                            raw = raw.replace(anchor, replacement)
                        else:
                            raw = raw.rstrip()[:-1] + ',\n  "synthetic_probe": NaN\n}\n'
                        Path(bound_config_path).write_text(raw, encoding="utf-8")
                    return result

                with mock.patch.object(
                    subject.restore,
                    "run_restore",
                    side_effect=redirect_after_check,
                ):
                    with self.assertRaisesRegex(ValueError, expected):
                        subject.restore_verified_prefix(
                            config_path,
                            run_id=run_id,
                            store_id=self.STORE_ID,
                            target=target,
                        )
                self.assertEqual(calls, [True])
                self.assertEqual(list(target.iterdir()), [])
                self.assertFalse(
                    (target / subject.VERIFIED_RESTORE_RECEIPT_NAME).exists()
                )

    def test_manifest_swap_immediately_before_restore_never_yields_receipt(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            _, stable, receipt, _ = self._capture(root)
            config_path = self._runnable_config(root, stable)
            run_id = subject.backup_stable_prefix(
                config_path,
                stable_receipt=receipt,
                store_id=self.STORE_ID,
                source_root=root / "source-root",
            )
            manifest = root / "backups" / "manifest.jsonl"
            target = root / "restore-target"
            target.mkdir()
            unchanged_restore = subject.restore.run_restore

            def swap_before_restore(*args, **kwargs):
                if not kwargs["check_only"]:
                    lines = manifest.read_text(encoding="utf-8").splitlines()
                    lines[0] = lines[0][:-1] + ', "record": "run_start"}'
                    manifest.write_text("\n".join(lines) + "\n", encoding="utf-8")
                return unchanged_restore(*args, **kwargs)

            with mock.patch.object(
                subject.restore, "run_restore", side_effect=swap_before_restore
            ):
                with self.assertRaisesRegex(ValueError, "duplicate JSON key"):
                    subject.restore_verified_prefix(
                        config_path,
                        run_id=run_id,
                        store_id=self.STORE_ID,
                        target=target,
                    )
            self.assertFalse(
                (target / subject.VERIFIED_RESTORE_RECEIPT_NAME).exists()
            )

    def test_restore_consumes_isolated_validated_archive_snapshot(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            _, stable, receipt, original_prefix = self._capture(root)
            config_path = self._runnable_config(root, stable)
            run_id = subject.backup_stable_prefix(
                config_path,
                stable_receipt=receipt,
                store_id=self.STORE_ID,
                source_root=root / "source-root",
            )
            backup_root = root / "backups"
            manifest = backup_root / "manifest.jsonl"
            archived = backup_root / "runs" / run_id / self.STORE_ID
            archived_receipt = archived / subject.STABLE_RECEIPT_NAME
            archived_snapshot = archived / "live.jsonl"
            original_manifest = manifest.read_bytes()
            original_receipt = archived_receipt.read_bytes()
            original_snapshot = archived_snapshot.read_bytes()

            alternate_snapshot = self._line(self.OBS_3, 99)
            alternate_receipt_object = json.loads(original_receipt)
            alternate_receipt_object.update(
                {
                    "high_water_bytes": len(alternate_snapshot),
                    "record_count": 1,
                    "last_observation_id": self.OBS_3,
                    "prefix_sha256": hashlib.sha256(alternate_snapshot).hexdigest(),
                    "dataset_content_hash": "p030ds-v1:" + "b" * 64,
                }
            )
            alternate_receipt = (
                json.dumps(
                    alternate_receipt_object,
                    ensure_ascii=False,
                    sort_keys=True,
                    indent=2,
                )
                + "\n"
            ).encode("utf-8")
            alternate_records = [
                json.loads(line) for line in original_manifest.splitlines()
            ]
            alternate_members = {
                subject.STABLE_RECEIPT_NAME: alternate_receipt,
                "live.jsonl": alternate_snapshot,
            }
            for record in alternate_records:
                member = alternate_members.get(record.get("rel"))
                if record.get("run_id") == run_id and member is not None:
                    record["size"] = len(member)
                    record["sha256"] = hashlib.sha256(member).hexdigest()
                if record.get("run_id") == run_id and record.get("record") == "run_end":
                    record["bytes"] = sum(map(len, alternate_members.values()))
            alternate_manifest = b"".join(
                (json.dumps(record, sort_keys=True) + "\n").encode("utf-8")
                for record in alternate_records
            )

            target = root / "restore-target"
            target.mkdir()
            unchanged_restore = subject.restore.run_restore

            def aba_swap_during_restore(*args, **kwargs):
                if kwargs["check_only"]:
                    return unchanged_restore(*args, **kwargs)
                manifest.write_bytes(alternate_manifest)
                archived_receipt.write_bytes(alternate_receipt)
                archived_snapshot.write_bytes(alternate_snapshot)
                try:
                    return unchanged_restore(*args, **kwargs)
                finally:
                    manifest.write_bytes(original_manifest)
                    archived_receipt.write_bytes(original_receipt)
                    archived_snapshot.write_bytes(original_snapshot)

            with mock.patch.object(
                subject.restore, "run_restore", side_effect=aba_swap_during_restore
            ):
                verified = subject.restore_verified_prefix(
                    config_path,
                    run_id=run_id,
                    store_id=self.STORE_ID,
                    target=target,
                )
            self.assertEqual(
                (target / self.STORE_ID / "live.jsonl").read_bytes(),
                original_prefix,
                "shared archive influenced isolated restore bytes",
            )
            verified_receipt = json.loads(verified.read_text(encoding="utf-8"))
            self.assertEqual(
                verified_receipt["dataset_content_hash"],
                self.DATASET_CONTENT_HASH,
                "shared archive influenced verified content ID",
            )

    def test_shared_archive_reversion_mutant_is_detected(self) -> None:
        source = Path(subject.__file__).read_text(encoding="utf-8")
        anchor = (
            '        isolated_config = {**config, "backup_root": str(isolated_root)}\n'
        )
        self.assertEqual(source.count(anchor), 1)
        mutant = types.ModuleType("p030_closed_partition_backup_shared_archive_mutant")
        mutant.__file__ = subject.__file__
        exec(
            compile(
                source.replace(
                    anchor,
                    "        isolated_config = config  # shared-archive reversion mutant\n",
                ),
                mutant.__file__,
                "exec",
            ),
            mutant.__dict__,
        )

        with mock.patch(f"{__name__}.subject", mutant), self.assertRaisesRegex(
            AssertionError, "shared archive influenced isolated restore bytes"
        ):
            self.test_restore_consumes_isolated_validated_archive_snapshot()

    def test_intruder_after_check_only_blocks_actual_restore(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            _, stable, receipt, _ = self._capture(root)
            config_path = self._runnable_config(root, stable)
            run_id = subject.backup_stable_prefix(
                config_path,
                stable_receipt=receipt,
                store_id=self.STORE_ID,
                source_root=root / "source-root",
            )
            target = root / "restore-target"
            target.mkdir()
            intruder = target / "synthetic-intruder"
            unchanged_restore = subject.restore.run_restore
            calls: list[bool] = []

            def intrude_after_check(*args, **kwargs):
                calls.append(kwargs["check_only"])
                result = unchanged_restore(*args, **kwargs)
                if kwargs["check_only"]:
                    intruder.write_text("fixture", encoding="utf-8")
                return result

            with mock.patch.object(
                subject.restore, "run_restore", side_effect=intrude_after_check
            ):
                with self.assertRaisesRegex(ValueError, "restore target must be empty"):
                    subject.restore_verified_prefix(
                        config_path,
                        run_id=run_id,
                        store_id=self.STORE_ID,
                        target=target,
                    )
            self.assertEqual(calls, [True])
            self.assertEqual(intruder.read_text(encoding="utf-8"), "fixture")

    def test_intruder_after_restore_config_verification_blocks_actual_restore(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            _, stable, receipt, _ = self._capture(root)
            config_path = self._runnable_config(root, stable)
            run_id = subject.backup_stable_prefix(
                config_path,
                stable_receipt=receipt,
                store_id=self.STORE_ID,
                source_root=root / "source-root",
            )
            target = root / "restore-target"
            target.mkdir()
            intruder = target / "synthetic-intruder"
            unchanged_verify = subject._verify_isolated_config
            unchanged_restore = subject.restore.run_restore
            verification_calls = 0
            restore_calls: list[bool] = []

            def intrude_after_restore_config_verification(*args, **kwargs):
                nonlocal verification_calls
                result = unchanged_verify(*args, **kwargs)
                verification_calls += 1
                if verification_calls == 3:
                    intruder.write_text("fixture", encoding="utf-8")
                return result

            def record_restore(*args, **kwargs):
                restore_calls.append(kwargs["check_only"])
                return unchanged_restore(*args, **kwargs)

            with mock.patch.object(
                subject,
                "_verify_isolated_config",
                side_effect=intrude_after_restore_config_verification,
            ), mock.patch.object(
                subject.restore,
                "run_restore",
                side_effect=record_restore,
            ):
                with self.assertRaisesRegex(ValueError, "restore target must be empty"):
                    subject.restore_verified_prefix(
                        config_path,
                        run_id=run_id,
                        store_id=self.STORE_ID,
                        target=target,
                    )
            self.assertEqual(restore_calls, [True])
            self.assertEqual(intruder.read_text(encoding="utf-8"), "fixture")
            self.assertFalse(
                (target / subject.VERIFIED_RESTORE_RECEIPT_NAME).exists()
            )

    def test_partial_run_that_p026_check_only_accepts_never_reaches_restore(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            _, stable, receipt, _ = self._capture(root)
            config_path = self._runnable_config(root, stable)
            run_id = subject.backup_stable_prefix(
                config_path,
                stable_receipt=receipt,
                store_id=self.STORE_ID,
                source_root=root / "source-root",
            )
            manifest = root / "backups" / "manifest.jsonl"
            records = [json.loads(line) for line in manifest.read_text(encoding="utf-8").splitlines()]
            run_end = next(
                record
                for record in records
                if record.get("record") == "run_end" and record.get("run_id") == run_id
            )
            run_end["status"] = "partial"
            run_end["errors"] = ["synthetic partial fixture"]
            manifest.write_text(
                "".join(json.dumps(record, sort_keys=True) + "\n" for record in records),
                encoding="utf-8",
            )
            self.assertEqual(
                subject.restore.run_restore(
                    config_path,
                    run_id,
                    None,
                    check_only=True,
                    store_filter={self.STORE_ID},
                ),
                subject.RC_OK,
            )
            target = root / "restore-target"
            target.mkdir()
            with mock.patch.object(subject.restore, "run_restore") as run_restore:
                with self.assertRaisesRegex(ValueError, "complete successful P026 run"):
                    subject.restore_verified_prefix(
                        config_path,
                        run_id=run_id,
                        store_id=self.STORE_ID,
                        target=target,
                    )
            run_restore.assert_not_called()

    def assert_run_envelope_defect_refused(
        self, module: types.ModuleType, defect: str
    ) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            _, stable, receipt, _ = self._capture(root)
            config_path = self._runnable_config(root, stable)
            run_id = module.backup_stable_prefix(
                config_path,
                stable_receipt=receipt,
                store_id=self.STORE_ID,
                source_root=root / "source-root",
            )
            manifest = root / "backups" / "manifest.jsonl"
            records = [
                json.loads(line)
                for line in manifest.read_text(encoding="utf-8").splitlines()
            ]
            run_end = next(
                record for record in records if record.get("record") == "run_end"
            )
            if defect == "duplicate_start":
                records.append(
                    next(
                        record.copy()
                        for record in records
                        if record["record"] == "run_start"
                    )
                )
            elif defect == "missing_snapshot":
                records = [
                    record
                    for record in records
                    if not (
                        record.get("record") == "file"
                        and record.get("rel") == "live.jsonl"
                    )
                ]
                run_end["files"] = 1
            elif defect == "wrong_store":
                next(
                    record
                    for record in records
                    if record.get("record") == "file"
                    and record.get("rel") == "live.jsonl"
                )["store_id"] = "fixture-other-store"
            elif defect == "status_non_ok_errors_empty":
                run_end["status"] = "partial"
            elif defect == "status_ok_nonempty_errors":
                run_end["errors"] = ["synthetic failure"]
            elif defect == "duplicate_expected_member":
                duplicate = next(
                    record.copy()
                    for record in records
                    if record.get("record") == "file"
                    and record.get("rel") == "live.jsonl"
                )
                records.append(duplicate)
                run_end["files"] += 1
                run_end["bytes"] += duplicate["size"]
            else:
                self.fail(f"unknown run-envelope defect: {defect}")
            manifest.write_text(
                "".join(
                    json.dumps(record, sort_keys=True) + "\n" for record in records
                ),
                encoding="utf-8",
            )
            target = root / "restore-target"
            target.mkdir()
            with mock.patch.object(module.restore, "run_restore") as run_restore:
                with self.assertRaisesRegex(
                    ValueError, "complete successful P026 run"
                ):
                    module.restore_verified_prefix(
                        config_path,
                        run_id=run_id,
                        store_id=self.STORE_ID,
                        target=target,
                    )
            run_restore.assert_not_called()

    def test_restore_requires_exact_run_envelope_store_and_members(self) -> None:
        for defect in (
            "duplicate_start",
            "missing_snapshot",
            "wrong_store",
            "status_non_ok_errors_empty",
            "status_ok_nonempty_errors",
            "duplicate_expected_member",
        ):
            with self.subTest(defect=defect):
                self.assert_run_envelope_defect_refused(subject, defect)

    def test_run_envelope_guards_are_independently_load_bearing(self) -> None:
        source = Path(subject.__file__).read_text(encoding="utf-8")
        mutations = {
            "status_non_ok_errors_empty": (
                '    if end.get("status") != "ok" or end.get("errors") != []:\n',
                '    if False or end.get("errors") != []:\n',
            ),
            "status_ok_nonempty_errors": (
                '    if end.get("status") != "ok" or end.get("errors") != []:\n',
                '    if end.get("status") != "ok" or False:\n',
            ),
            "duplicate_expected_member": (
                "        or len(actual) != len(expected)\n",
                "        or False\n",
            ),
        }
        for defect, (anchor, replacement) in mutations.items():
            with self.subTest(defect=defect):
                self.assertEqual(source.count(anchor), 1)
                mutant = types.ModuleType(f"p030_run_envelope_{defect}_mutant")
                mutant.__file__ = subject.__file__
                exec(
                    compile(source.replace(anchor, replacement), mutant.__file__, "exec"),
                    mutant.__dict__,
                )
                with self.assertRaises(AssertionError):
                    self.assert_run_envelope_defect_refused(mutant, defect)

    def test_speculative_replay_opening_api_is_absent(self) -> None:
        self.assertFalse(hasattr(subject, "open_verified_replay_prefix"))

    def test_receipt_always_refuses_absolute_or_noncanonical_source_path(self) -> None:
        invalid_paths = (
            ".",
            "C:/synthetic/live.jsonl",
            "/synthetic/live.jsonl",
            "feeds\\live.jsonl",
            "feeds//live.jsonl",
            "feeds/../live.jsonl",
            "feeds%2Flive.jsonl",
        )
        for invalid in invalid_paths:
            with self.subTest(source_path=invalid), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                _, stable, receipt_path, _ = self._capture(root)
                receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
                receipt["source_path"] = invalid
                receipt_path.write_text(json.dumps(receipt), encoding="utf-8")
                with self.assertRaisesRegex(ValueError, "source_path"):
                    subject._verify_stable_receipt(
                        stable, receipt_path, verify_source=False
                    )

    def test_receipt_strictly_validates_types_identities_and_lower_hex(self) -> None:
        cases = {
            "schema": "wrong",
            "state": "wrong",
            "high_water_bytes": True,
            "record_count": True,
            "last_observation_id": "p030obs-v1:" + "A" * 64,
            "prefix_sha256": "A" * 64,
            "captured_at_utc": 1,
            "dataset_content_hash": "p030ds-v1:" + "A" * 64,
            "snapshot_rel": "../live.jsonl",
        }
        for field, invalid in cases.items():
            with self.subTest(field=field), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                source_root = root / "source-root"
                source = source_root / "feeds" / "live.jsonl"
                source.parent.mkdir(parents=True)
                prefix = self._line(self.OBS_1, 10)
                source.write_bytes(prefix)
                stable = root / "stable-prefix"
                receipt_path = subject.capture_stable_prefix(
                    source,
                    stable,
                    source_root=source_root,
                    high_water_bytes=len(prefix),
                    captured_at_utc=self.CAPTURED_AT,
                    dataset_content_hash=self.DATASET_CONTENT_HASH,
                )
                receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
                receipt[field] = invalid
                receipt_path.write_text(json.dumps(receipt), encoding="utf-8")
                with self.assertRaisesRegex(ValueError, field):
                    subject._verify_stable_receipt(
                        stable, receipt_path, verify_source=False
                    )

    def test_receipt_refuses_duplicate_keys_and_nonfinite_json(self) -> None:
        for kind in ("duplicate", "nonfinite"):
            with self.subTest(kind=kind), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                _, stable, receipt_path, _ = self._capture(root)
                raw = receipt_path.read_text(encoding="utf-8")
                if kind == "duplicate":
                    raw = raw.replace(
                        '"record_count": 2,',
                        '"record_count": 2,\n  "record_count": 2,',
                    )
                    expected = "duplicate JSON key"
                else:
                    raw = raw.replace('"record_count": 2,', '"record_count": NaN,')
                    expected = "non-finite JSON constant"
                receipt_path.write_text(raw, encoding="utf-8")
                with self.assertRaisesRegex(ValueError, expected):
                    subject._verify_stable_receipt(
                        stable, receipt_path, verify_source=False
                    )

    def test_backup_rechecks_source_and_snapshot_after_p026_success(self) -> None:
        for changed in ("source", "snapshot"):
            with self.subTest(changed=changed), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                source, stable, receipt, _ = self._capture(root)
                config_path = self._runnable_config(root, stable)
                unchanged_backup = subject.backup.run_backup

                def mutate_after_backup(*args, **kwargs):
                    result = unchanged_backup(*args, **kwargs)
                    path = source if changed == "source" else stable / "live.jsonl"
                    path.write_bytes(path.read_bytes().replace(b"1" * 64, b"f" * 64, 1))
                    return result

                with mock.patch.object(
                    subject.backup, "run_backup", side_effect=mutate_after_backup
                ):
                    with self.assertRaisesRegex(ValueError, f"{changed} prefix"):
                        subject.backup_stable_prefix(
                            config_path,
                            stable_receipt=receipt,
                            store_id=self.STORE_ID,
                            source_root=root / "source-root",
                        )

    def test_backup_refuses_coordinated_valid_staging_replacement_after_p026(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source, stable, receipt, _ = self._capture(root)
            config_path = self._runnable_config(root, stable)
            snapshot = stable / "live.jsonl"
            alternate_snapshot = self._line(self.OBS_3, 99)
            alternate_receipt_object = json.loads(receipt.read_bytes())
            alternate_receipt_object.update(
                {
                    "high_water_bytes": len(alternate_snapshot),
                    "record_count": 1,
                    "last_observation_id": self.OBS_3,
                    "prefix_sha256": hashlib.sha256(alternate_snapshot).hexdigest(),
                    "dataset_content_hash": "p030ds-v1:" + "b" * 64,
                }
            )
            alternate_receipt = (
                json.dumps(
                    alternate_receipt_object,
                    ensure_ascii=False,
                    sort_keys=True,
                    indent=2,
                )
                + "\n"
            ).encode("utf-8")
            unchanged_backup = subject.backup.run_backup

            def replace_staging_after_backup(*args, **kwargs):
                result = unchanged_backup(*args, **kwargs)
                source.write_bytes(alternate_snapshot)
                snapshot.write_bytes(alternate_snapshot)
                receipt.write_bytes(alternate_receipt)
                return result

            with mock.patch.object(
                subject.backup,
                "run_backup",
                side_effect=replace_staging_after_backup,
            ):
                with self.assertRaisesRegex(ValueError, "prevalidated staging bytes"):
                    subject.backup_stable_prefix(
                        config_path,
                        stable_receipt=receipt,
                        store_id=self.STORE_ID,
                        source_root=root / "source-root",
                    )

    def test_backup_refuses_archived_pair_that_differs_from_prevalidated_staging(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            _, stable, receipt, _ = self._capture(root)
            config_path = self._runnable_config(root, stable)
            original_receipt = receipt.read_bytes()
            snapshot = stable / "live.jsonl"
            original_snapshot = snapshot.read_bytes()
            alternate_snapshot = self._line(self.OBS_3, 99)
            alternate_receipt_object = json.loads(original_receipt)
            alternate_receipt_object.update(
                {
                    "high_water_bytes": len(alternate_snapshot),
                    "record_count": 1,
                    "last_observation_id": self.OBS_3,
                    "prefix_sha256": hashlib.sha256(alternate_snapshot).hexdigest(),
                    "dataset_content_hash": "p030ds-v1:" + "b" * 64,
                }
            )
            alternate_receipt = (
                json.dumps(
                    alternate_receipt_object,
                    ensure_ascii=False,
                    sort_keys=True,
                    indent=2,
                )
                + "\n"
            ).encode("utf-8")
            unchanged_backup = subject.backup.run_backup

            def aba_during_backup(*args, **kwargs):
                receipt.write_bytes(alternate_receipt)
                snapshot.write_bytes(alternate_snapshot)
                try:
                    return unchanged_backup(*args, **kwargs)
                finally:
                    receipt.write_bytes(original_receipt)
                    snapshot.write_bytes(original_snapshot)

            with mock.patch.object(
                subject.backup, "run_backup", side_effect=aba_during_backup
            ):
                with self.assertRaisesRegex(ValueError, "prevalidated staging bytes"):
                    subject.backup_stable_prefix(
                        config_path,
                        stable_receipt=receipt,
                        store_id=self.STORE_ID,
                        source_root=root / "source-root",
                    )

    def assert_backup_binds_bytes_from_the_same_read_that_validated_them(
        self, module: types.ModuleType
    ) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source, stable, receipt, _ = self._capture(root)
            config_path = self._runnable_config(root, stable)
            original_receipt = receipt.read_bytes()
            snapshot = stable / "live.jsonl"
            alternate_snapshot = self._line(self.OBS_3, 99)
            alternate_receipt_object = json.loads(original_receipt)
            alternate_receipt_object.update(
                {
                    "high_water_bytes": len(alternate_snapshot),
                    "record_count": 1,
                    "last_observation_id": self.OBS_3,
                    "prefix_sha256": hashlib.sha256(alternate_snapshot).hexdigest(),
                    "dataset_content_hash": "p030ds-v1:" + "b" * 64,
                }
            )
            alternate_receipt = (
                json.dumps(
                    alternate_receipt_object,
                    ensure_ascii=False,
                    sort_keys=True,
                    indent=2,
                )
                + "\n"
            ).encode("utf-8")
            unchanged_verify = module._verify_stable_receipt
            first_validation = True

            def swap_after_first_validation(*args, **kwargs):
                nonlocal first_validation
                result = unchanged_verify(*args, **kwargs)
                if first_validation:
                    first_validation = False
                    source.write_bytes(alternate_snapshot)
                    receipt.write_bytes(alternate_receipt)
                    snapshot.write_bytes(alternate_snapshot)
                return result

            with mock.patch.object(
                module,
                "_verify_stable_receipt",
                side_effect=swap_after_first_validation,
            ):
                with self.assertRaisesRegex(ValueError, "prevalidated staging bytes"):
                    module.backup_stable_prefix(
                        config_path,
                        stable_receipt=receipt,
                        store_id=self.STORE_ID,
                        source_root=root / "source-root",
                    )

    def test_backup_binds_bytes_from_the_same_read_that_validated_them(self) -> None:
        self.assert_backup_binds_bytes_from_the_same_read_that_validated_them(subject)

    def test_validate_then_reopen_reversion_is_detected(self) -> None:
        source = Path(subject.__file__).read_text(encoding="utf-8")
        anchor = """        _, receipt_before, snapshot_before = _verify_stable_receipt(
            stable_prefix,
            stable_receipt,
            verify_source=True,
            source_root=source_root,
            include_bytes=True,
        )
        prevalidated_staging = receipt_before, snapshot_before
"""
        replacement = """        stable_before, _, _ = _verify_stable_receipt(
            stable_prefix,
            stable_receipt,
            verify_source=True,
            source_root=source_root,
            include_bytes=True,
        )
        receipt_before = Path(stable_receipt).read_bytes()
        snapshot_before = resolve_confined_path(
            stable_prefix, stable_before["snapshot_rel"]
        ).read_bytes()
        prevalidated_staging = receipt_before, snapshot_before
"""
        self.assertEqual(source.count(anchor), 1)
        mutant = types.ModuleType("p030_validate_then_reopen_mutant")
        mutant.__file__ = subject.__file__
        exec(
            compile(source.replace(anchor, replacement), mutant.__file__, "exec"),
            mutant.__dict__,
        )
        with self.assertRaises(AssertionError):
            self.assert_backup_binds_bytes_from_the_same_read_that_validated_them(
                mutant
            )

    def test_restore_refuses_nonempty_target_before_p026(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            _, stable, receipt, _ = self._capture(root)
            config_path = self._runnable_config(root, stable)
            run_id = subject.backup_stable_prefix(
                config_path,
                stable_receipt=receipt,
                store_id=self.STORE_ID,
                source_root=root / "source-root",
            )
            target = root / "nonempty"
            target.mkdir()
            (target / "keep").write_text("keep", encoding="utf-8")
            with mock.patch.object(subject.restore, "run_restore") as run_restore:
                with self.assertRaisesRegex(ValueError, "restore target must be empty"):
                    subject.restore_verified_prefix(
                        config_path, run_id=run_id, store_id=self.STORE_ID, target=target
                    )
            run_restore.assert_not_called()

    def test_tampered_backup_never_reaches_p026_restore(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            _, stable, receipt, _ = self._capture(root)
            config_path = self._runnable_config(root, stable)
            run_id = subject.backup_stable_prefix(
                config_path,
                stable_receipt=receipt,
                store_id=self.STORE_ID,
                source_root=root / "source-root",
            )
            backup_file = next((root / "backups" / "runs" / run_id).rglob("live.jsonl"))
            backup_file.write_bytes(b"tampered\n")
            target = root / "restore-target"
            target.mkdir()
            unchanged_restore = subject.restore.run_restore
            calls: list[bool] = []

            def record_restore(*args, **kwargs):
                calls.append(kwargs["check_only"])
                return unchanged_restore(*args, **kwargs)

            with mock.patch.object(subject.restore, "run_restore", side_effect=record_restore):
                with self.assertRaisesRegex(ValueError, "snapshot prefix"):
                    subject.restore_verified_prefix(
                        config_path, run_id=run_id, store_id=self.STORE_ID, target=target
                    )
            self.assertEqual(calls, [])
            self.assertEqual(list(target.iterdir()), [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
