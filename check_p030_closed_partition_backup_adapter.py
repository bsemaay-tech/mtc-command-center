"""Synthetic-only checks for P030 stable-prefix backup and verified restore."""

from __future__ import annotations

import json
import tempfile
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

    def test_speculative_replay_opening_api_is_absent(self) -> None:
        self.assertFalse(hasattr(subject, "open_verified_replay_prefix"))

    def test_receipt_always_refuses_absolute_or_noncanonical_source_path(self) -> None:
        invalid_paths = (
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

    def test_failed_check_only_never_replays_or_restores(self) -> None:
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
                with self.assertRaisesRegex(ValueError, "P026 check-only failed"):
                    subject.restore_verified_prefix(
                        config_path, run_id=run_id, store_id=self.STORE_ID, target=target
                    )
            self.assertEqual(calls, [True])
            self.assertEqual(list(target.iterdir()), [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
