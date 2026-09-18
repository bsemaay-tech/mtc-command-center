"""Unit + falsification tests for the OPS-A tooling (WP-P0-26 local half).

Run:  python -m unittest test_opsa -v     (from MTC_COMMAND_CENTER/tools/opsa)

D026 note: the *drill-level* RED/GREEN demonstrations (damaged live copy unrecoverable
without backup; killed heartbeat flagged) live in
``11_TRIAGE/WP_P0_26_OPSA_2026-08-25/RESTORE_DRILL_EVIDENCE.md`` with commands + real
output. These tests are the repeatable regression layer below that: several of them
(tampered backup, stale heartbeat, corrupt heartbeat, dry-run writes nothing) are the
same falsifications, automated. Standard library only.
"""
from __future__ import annotations

import contextlib
import hashlib
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from datetime import timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from opsa_common import (  # noqa: E402
    COMPLETE_MARKER_NAME, RUN_MANIFEST_NAME, parse_utc_iso, utc_now, write_once_bytes,
)
import backup  # noqa: E402
import heartbeat  # noqa: E402
import restore  # noqa: E402
import watchdog  # noqa: E402

TOOLS_DIR = Path(__file__).resolve().parent


def write_config(root: Path, backup_root: Path, stores: list[dict]) -> Path:
    config = {"schema": "mtc.opsa_backup_config/v1",
              "backup_root": str(backup_root), "stores": stores}
    path = root / "opsa_config.json"
    path.write_text(json.dumps(config, indent=2), encoding="utf-8")
    return path


def make_fixture_store(root: Path) -> Path:
    """Evidence-store fixture: nested dirs, CRLF text, binary bytes, an empty dir."""
    store = root / "live" / "ledger_store"
    (store / "sub").mkdir(parents=True, exist_ok=True)
    (store / "empty_dir").mkdir(parents=True, exist_ok=True)
    (store / "ledger.jsonl").write_bytes(
        b'{"row":1,"note":"alpha"}\r\n{"row":2,"note":"beta"}\r\n')
    (store / "sub" / "blob.bin").write_bytes(bytes(range(256)) * 4)
    return store


class BackupRestoreTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory(prefix="opsa_test_")
        self.root = Path(self._tmp.name)
        self.store = make_fixture_store(self.root)
        self.backup_root = self.root / "backups"
        self.config = write_config(self.root, self.backup_root,
                                   [{"id": "ledger_store", "path": str(self.store),
                                     "class": "protected"}])
        self.manifest = self.backup_root / "manifest.jsonl"

    def tearDown(self):
        self._tmp.cleanup()

    def _run_backup(self, **kw):
        return backup.run_backup(self.config, **kw)

    def _run_ids(self) -> list[str]:
        """Run ids in manifest order (the repair removed latest-run selection: tests name runs)."""
        return [json.loads(line)["run_id"]
                for line in self.manifest.read_text(encoding="utf-8").splitlines()
                if line.strip() and json.loads(line).get("record") == "run_start"]

    def _only_run_id(self) -> str:
        ids = self._run_ids()
        self.assertEqual(len(ids), 1)
        return ids[0]

    def _run_dir(self, run_id: str) -> Path:
        return self.backup_root / "runs" / run_id

    def test_roundtrip_byte_identical(self):
        """Back up, damage the live copy, restore -> every file byte-identical."""
        self.assertEqual(self._run_backup(), 0)
        # Damage the live store (overwrite one file, empty another).
        (self.store / "ledger.jsonl").write_bytes(b"CORRUPTED")
        (self.store / "sub" / "blob.bin").write_bytes(b"")
        target = self.root / "restored"
        run_id = self._only_run_id()
        # Completion evidence exists for a clean run (WP-P0-26 repair).
        self.assertTrue((self._run_dir(run_id) / "COMPLETE.json").is_file())
        self.assertTrue((self._run_dir(run_id) / "RUN_MANIFEST.jsonl").is_file())
        rc = restore.run_restore(self.config, run_id=run_id, target=target)
        self.assertEqual(rc, 0)
        self.assertEqual((target / "ledger_store" / "ledger.jsonl").read_bytes(),
                         b'{"row":1,"note":"alpha"}\r\n{"row":2,"note":"beta"}\r\n')
        self.assertEqual((target / "ledger_store" / "sub" / "blob.bin").read_bytes(),
                         bytes(range(256)) * 4)
        self.assertTrue((target / "ledger_store" / "empty_dir").is_dir())

    def test_manifest_append_only_across_runs(self):
        """A second backup run appends; the first run's lines are byte-for-byte intact."""
        self.assertEqual(self._run_backup(), 0)
        first = self.manifest.read_bytes()
        first_lines = first.decode().splitlines()
        self.assertEqual(self._run_backup(), 0)
        second = self.manifest.read_bytes()
        self.assertTrue(second.startswith(first))  # prefix preserved, never rewritten
        self.assertGreater(len(second), len(first))
        appended = second.decode().splitlines()[len(first_lines):]
        self.assertTrue(all(json.loads(line)["run_id"] != json.loads(first_lines[1])["run_id"]
                            for line in appended))

    def test_dry_run_writes_nothing(self):
        """Dry-run must not create the run dir nor append any manifest byte."""
        self.assertEqual(self._run_backup(dry_run=True), 0)
        self.assertFalse(self.manifest.exists())
        self.assertFalse((self.backup_root / "runs").exists())

    def test_missing_store_reports_error_not_success(self):
        """A configured store path that does not exist => loud partial, rc 1."""
        bad = write_config(self.root, self.backup_root,
                           [{"id": "ghost", "path": str(self.root / "nope"), "class": "x"}])
        rc = backup.run_backup(bad)
        self.assertEqual(rc, 1)

    def test_restore_refuses_tampered_backup(self):
        """Falsification: flip one byte in the BACKUP -> restore must FAIL (rc 1)."""
        self.assertEqual(self._run_backup(), 0)
        run_dir = next((self.backup_root / "runs").iterdir())
        victim = run_dir / "ledger_store" / "sub" / "blob.bin"
        data = bytearray(victim.read_bytes())
        data[7] ^= 0xFF
        victim.write_bytes(bytes(data))
        rc = restore.run_restore(self.config, run_id=self._only_run_id(), target=self.root / "restored")
        self.assertEqual(rc, 1)
        self.assertFalse((self.root / "restored" / "ledger_store" / "sub" / "blob.bin").exists())

    def test_check_only_detects_corruption_writes_nothing(self):
        self.assertEqual(self._run_backup(), 0)
        run_dir = next((self.backup_root / "runs").iterdir())
        victim = run_dir / "ledger_store" / "ledger.jsonl"
        victim.write_bytes(b"tampered")
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = restore.run_restore(self.config, run_id=self._only_run_id(), target=None, check_only=True)
        self.assertEqual(rc, 1)
        self.assertFalse((self.root / "restored").exists())
        summary = json.loads(buf.getvalue().strip().splitlines()[-1])
        # Audit R1 nit 4: --check-only writes nothing, so it must not claim
        # directories it did not create (old code reported the dir-record count).
        self.assertEqual(summary["dirs_recreated"], 0)

    def test_newest_run_is_restored_only_by_its_explicit_id(self):
        """Two runs; the second (changed content) restores by its own id, never by 'latest'."""
        self.assertEqual(self._run_backup(store_filter={"ledger_store"}), 0)
        (self.store / "ledger.jsonl").write_bytes(b'{"row":1,"note":"CHANGED"}\r\n')
        self.assertEqual(self._run_backup(store_filter={"ledger_store"}), 0)
        first, second = self._run_ids()
        target = self.root / "restored"
        self.assertEqual(restore.run_restore(self.config, run_id=second, target=target), 0)
        self.assertEqual((target / "ledger_store" / "ledger.jsonl").read_bytes(),
                         b'{"row":1,"note":"CHANGED"}\r\n')
        older = self.root / "restored_first"
        self.assertEqual(restore.run_restore(self.config, run_id=first, target=older), 0)
        self.assertEqual((older / "ledger_store" / "ledger.jsonl").read_bytes(),
                         b'{"row":1,"note":"alpha"}\r\n{"row":2,"note":"beta"}\r\n')

    def test_restore_without_explicit_run_id_fails_closed(self):
        """Falsification 4 (owner packet §5): no run id => refused; --latest no longer exists."""
        self.assertEqual(self._run_backup(), 0)
        target = self.root / "restored"
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr):
            rc = restore.run_restore(self.config, run_id=None, target=target)
        self.assertEqual(rc, 3)
        self.assertIn("explicit --run", stderr.getvalue())
        self.assertFalse(target.exists())
        with self.assertRaises(ValueError):
            restore.select_run([{"record": "run_start", "run_id": "x"}], None, None)
        result = subprocess.run(
            [sys.executable, str(TOOLS_DIR / "restore.py"), "--config", str(self.config),
             "--latest", "--to", str(target)],
            cwd=TOOLS_DIR, capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 2)  # argparse: --latest unknown / --run missing
        self.assertIn("--run", result.stderr)
        self.assertFalse(target.exists())

    def test_interrupted_run_has_no_completion_marker_and_restore_refuses(self):
        """Falsification 1: a copy that dies mid-run leaves no COMPLETE.json; restore refuses it."""
        real_copyfile = backup.shutil.copyfile
        calls = {"n": 0}

        def dying_copyfile(src, dst, *a, **kw):
            calls["n"] += 1
            if calls["n"] == 2:
                raise OSError("simulated interruption during the second file copy")
            return real_copyfile(src, dst, *a, **kw)

        backup.shutil.copyfile = dying_copyfile
        try:
            rc = self._run_backup()
        finally:
            backup.shutil.copyfile = real_copyfile
        self.assertEqual(rc, 1)
        run_id = self._only_run_id()
        self.assertFalse((self._run_dir(run_id) / "COMPLETE.json").exists())
        self.assertFalse((self._run_dir(run_id) / "RUN_MANIFEST.jsonl").exists())
        target = self.root / "restored"
        for check_only in (False, True):
            with self.subTest(check_only=check_only):
                stderr = io.StringIO()
                with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(stderr):
                    rc = restore.run_restore(self.config, run_id=run_id,
                                             target=None if check_only else target,
                                             check_only=check_only)
                self.assertEqual(rc, 3)
                report = json.loads(stderr.getvalue().strip().splitlines()[-1])
                self.assertEqual(report["error"], "run_not_complete")
                self.assertIn("no completion marker", report["detail"])
        self.assertFalse(target.exists())

    def test_hand_made_completion_evidence_cannot_revive_a_run_the_tool_did_not_close(self):
        """Gemini detection F-01 (2026-09-15): a COMPLETE.json + RUN_MANIFEST.jsonl pair written by
        hand into runs/<run_id>/ -- internally consistent, digest-bound, matching the global file
        records -- must still be refused when the global manifest holds no successful run_end for
        the run: (1) an interrupted run whose run_end says partial; (2) a crashed run with no
        run_end at all. RED on the slice-2 restore: it restored arm 1 with rc 0."""
        real_copyfile = backup.shutil.copyfile
        calls = {"n": 0}

        def dying_copyfile(src, dst, *a, **kw):
            calls["n"] += 1
            if calls["n"] == 2:
                raise OSError("simulated interruption during the second file copy")
            return real_copyfile(src, dst, *a, **kw)

        backup.shutil.copyfile = dying_copyfile
        try:
            self.assertEqual(self._run_backup(), 1)
        finally:
            backup.shutil.copyfile = real_copyfile
        run_id = self._only_run_id()
        records = [json.loads(line) for line in
                   self.manifest.read_text(encoding="utf-8").splitlines()]
        run_records = [r for r in records if r.get("run_id") == run_id
                       and r.get("record") in ("file", "dir", "skipped")]
        files = [r for r in run_records if r["record"] == "file"]
        self.assertEqual(len(files), 1)  # the copy died on the second file

        def forge(run_dir: Path) -> None:
            lines = [json.dumps({"record": "run_manifest_header",
                                 "schema": "mtc.opsa_run_manifest/v1", "run_id": run_id},
                                sort_keys=True)]
            lines += [json.dumps(r, sort_keys=True) for r in run_records]
            manifest_bytes = ("\n".join(lines) + "\n").encode("utf-8")
            (run_dir / RUN_MANIFEST_NAME).write_bytes(manifest_bytes)
            marker = {"schema": "mtc.opsa_run_complete/v1", "run_id": run_id,
                      "files": len(files), "readback": "all_match",
                      "run_manifest_sha256": hashlib.sha256(manifest_bytes).hexdigest()}
            (run_dir / COMPLETE_MARKER_NAME).write_text(json.dumps(marker, sort_keys=True),
                                                        encoding="utf-8")

        def assert_refused(config: Path, arm: str) -> None:
            target = self.root / f"restored_{arm}"
            for check_only in (True, False):
                with self.subTest(arm=arm, check_only=check_only):
                    stderr = io.StringIO()
                    with contextlib.redirect_stdout(io.StringIO()), \
                            contextlib.redirect_stderr(stderr):
                        rc = restore.run_restore(config, run_id=run_id,
                                                 target=None if check_only else target,
                                                 check_only=check_only)
                    self.assertEqual(rc, 3)
                    report = json.loads(stderr.getvalue().strip().splitlines()[-1])
                    self.assertEqual(report["error"], "run_not_complete")
                    self.assertIn("run_end", report["detail"])
            self.assertFalse(target.exists())

        # arm 1: interrupted run -- the tool wrote run_end with status partial and one error
        forge(self._run_dir(run_id))
        assert_refused(self.config, "interrupted")

        # arm 2: crashed run -- same run directory, global manifest without any run_end
        crashed_root = self.root / "crashed_backups"
        (crashed_root / "runs").mkdir(parents=True)
        shutil.copytree(self._run_dir(run_id), crashed_root / "runs" / run_id)
        (crashed_root / "manifest.jsonl").write_text(
            "".join(json.dumps(r) + "\n" for r in records if r.get("record") != "run_end"),
            encoding="utf-8")
        cfg_dir = self.root / "crashed_cfg"
        cfg_dir.mkdir()
        crashed_config = write_config(cfg_dir, crashed_root,
                                      [{"id": "ledger_store", "path": str(self.store),
                                        "class": "protected"}])
        assert_refused(crashed_config, "crashed")

    def test_completed_run_restores_by_explicit_id_including_copied_run_directory(self):
        """Falsification 2: a completed run (marker + per-run manifest) restores by explicit id, and
        the run directory copied elsewhere still verifies (evidence is self-contained)."""
        self.assertEqual(self._run_backup(), 0)
        run_id = self._only_run_id()
        run_dir = self._run_dir(run_id)
        marker = json.loads((run_dir / "COMPLETE.json").read_text(encoding="utf-8"))
        self.assertEqual(marker["schema"], "mtc.opsa_run_complete/v1")
        self.assertEqual(marker["run_id"], run_id)
        self.assertEqual(marker["files"], 2)
        self.assertEqual(marker["readback"], "all_match")
        self.assertEqual(marker["run_manifest_sha256"],
                         hashlib.sha256((run_dir / "RUN_MANIFEST.jsonl").read_bytes()).hexdigest())
        # Copy the whole backup root elsewhere: the copied run must still verify and restore.
        copied_root = self.root / "copied_backups"
        shutil.copytree(self.backup_root, copied_root)
        (self.root / "cfg2").mkdir()
        copied_config = write_config(self.root / "cfg2", copied_root,
                                     [{"id": "ledger_store", "path": str(self.store),
                                       "class": "protected"}])
        target = self.root / "restored_from_copy"
        rc = restore.run_restore(copied_config, run_id=run_id, target=target)
        self.assertEqual(rc, 0)
        self.assertEqual((target / "ledger_store" / "sub" / "blob.bin").read_bytes(),
                         bytes(range(256)) * 4)
        # The marker and per-run manifest are immutable: writing them again is refused.
        with self.assertRaises(FileExistsError):
            write_once_bytes(run_dir / "COMPLETE.json", b"{}")
        with self.assertRaises(FileExistsError):
            write_once_bytes(run_dir / "RUN_MANIFEST.jsonl", b"")

    def test_tampered_marker_or_run_manifest_is_refused(self):
        """Falsification 3: a tampered/mismatched marker or per-run manifest is refused; a hash
        mismatch of a backed-up file is still refused behind the gate."""
        self.assertEqual(self._run_backup(), 0)
        run_id = self._only_run_id()
        run_dir = self._run_dir(run_id)
        target = self.root / "restored"

        def refused(detail_fragment: str):
            stderr = io.StringIO()
            with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(stderr):
                rc = restore.run_restore(self.config, run_id=run_id, target=target)
            self.assertEqual(rc, 3)
            report = json.loads(stderr.getvalue().strip().splitlines()[-1])
            self.assertEqual(report["error"], "run_not_complete")
            self.assertIn(detail_fragment, report["detail"])
            self.assertFalse(target.exists())

        manifest_path = run_dir / "RUN_MANIFEST.jsonl"
        marker_path = run_dir / "COMPLETE.json"
        good_manifest = manifest_path.read_bytes()
        good_marker = marker_path.read_bytes()
        # (a) per-run manifest tampered (one byte appended) -> marker hash mismatch
        manifest_path.write_bytes(good_manifest + b"\n")
        refused("per-run manifest hash mismatch")
        manifest_path.write_bytes(good_manifest)
        # (b) marker names another run
        payload = json.loads(good_marker)
        payload["run_id"] = "opsa-19000101T000000.000Z"
        marker_path.write_bytes(json.dumps(payload).encode("utf-8"))
        refused("names run")
        # (c) marker unreadable
        marker_path.write_bytes(b"not json")
        refused("unreadable")
        marker_path.write_bytes(good_marker)
        # (d) per-run record differs from the global manifest (digest forged, marker re-hashed)
        lines = good_manifest.decode("utf-8").splitlines()
        rec = json.loads(lines[-1])
        rec["sha256"] = "0" * 64
        lines[-1] = json.dumps(rec, ensure_ascii=False, sort_keys=True)
        forged = ("\n".join(lines) + "\n").encode("utf-8")
        manifest_path.write_bytes(forged)
        payload = json.loads(good_marker)
        payload["run_manifest_sha256"] = hashlib.sha256(forged).hexdigest()
        marker_path.write_bytes(json.dumps(payload, sort_keys=True).encode("utf-8"))
        refused("differ from the global manifest")
        manifest_path.write_bytes(good_manifest)
        marker_path.write_bytes(good_marker)
        # (d2) NIT-1 (exact-Opus read of e114ed31): the marker's own claims are validated, not only
        # the four pair-integrity fields - a falsified readback or run_manifest name is refused
        # before restore could print "completion_marker": "verified"
        payload = json.loads(good_marker)
        payload["readback"] = "partial"
        marker_path.write_bytes(json.dumps(payload, sort_keys=True).encode("utf-8"))
        refused("declares readback='partial'")
        payload = json.loads(good_marker)
        payload["run_manifest"] = "OTHER.jsonl"
        marker_path.write_bytes(json.dumps(payload, sort_keys=True).encode("utf-8"))
        refused("names run_manifest='OTHER.jsonl'")
        marker_path.write_bytes(good_marker)
        # (e) intact evidence, but a backed-up file bit-rots -> hash mismatch still refuses (rc 1)
        victim = run_dir / "ledger_store" / "ledger.jsonl"
        data = bytearray(victim.read_bytes())
        data[0] ^= 0xFF
        victim.write_bytes(bytes(data))
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            rc = restore.run_restore(self.config, run_id=run_id, target=target)
        self.assertEqual(rc, 1)
        self.assertFalse((target / "ledger_store" / "ledger.jsonl").exists())

    def test_nonexistent_run_is_check_failure_not_empty_success(self):
        """D026: an explicit unknown run id must fail closed with rc 3."""
        self.assertEqual(self._run_backup(), 0)
        target = self.root / "restored"
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr):
            rc = restore.run_restore(
                self.config, run_id="opsa-19000101T000000.000Z", target=target)
        self.assertEqual(rc, 3)
        self.assertIn("run id not found in manifest", stderr.getvalue())
        self.assertFalse(target.exists())

    def test_partial_run_declaring_files_but_having_no_records_fails_closed(self):
        """D026: a partial manifest cannot turn zero restored records into success."""
        run_id = "opsa-20260825T000000.000Z"
        self.backup_root.mkdir(parents=True)
        lines = [
            {"record": "run_start", "schema": "mtc.opsa_manifest/v1", "run_id": run_id},
            {"record": "dir", "run_id": run_id, "store_id": "ledger_store",
             "rel": "empty_dir"},
            {"record": "run_end", "run_id": run_id, "status": "partial", "files": 1,
             "errors": ["copy failed"]},
        ]
        self.manifest.write_text(
            "".join(json.dumps(line) + "\n" for line in lines), encoding="utf-8")

        for check_only in (False, True):
            with self.subTest(check_only=check_only):
                stdout = io.StringIO()
                stderr = io.StringIO()
                target = None if check_only else self.root / "restored"
                with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                    rc = restore.run_restore(
                        self.config, run_id=run_id, target=target, check_only=check_only)
                self.assertEqual(rc, 3)
                # WP-P0-26 repair: the completion gate refuses first (no COMPLETE.json for the
                # hand-written partial run) — before any record is read for verification.
                report = json.loads(stderr.getvalue().strip().splitlines()[-1])
                self.assertEqual(report["error"], "run_not_complete")
                if target is not None:
                    self.assertFalse(target.exists())
        # Forge complete-looking evidence for the same partial run (per-run manifest with the dir
        # record only, marker declaring files=0): the gate refuses on the global run_end
        # (status partial, one error) before anything else -- Gemini F-01, slice 3.
        def forge(run_dir: Path, dir_record: dict, run: str) -> None:
            run_dir.mkdir(parents=True, exist_ok=True)
            forged_lines = [json.dumps({"record": "run_manifest_header",
                                        "schema": "mtc.opsa_run_manifest/v1",
                                        "run_id": run}, sort_keys=True),
                            json.dumps(dir_record, sort_keys=True)]
            forged = ("\n".join(forged_lines) + "\n").encode("utf-8")
            (run_dir / "RUN_MANIFEST.jsonl").write_bytes(forged)
            (run_dir / "COMPLETE.json").write_text(json.dumps({
                "schema": "mtc.opsa_run_complete/v1", "run_id": run, "files": 0,
                "run_manifest_sha256": hashlib.sha256(forged).hexdigest(),
                # NIT-1: the gate now also checks the marker's own claims, so a forgery meant to
                # reach the fences BEHIND the gate must carry the tool's values for them
                "readback": "all_match", "run_manifest": "RUN_MANIFEST.jsonl"}), encoding="utf-8")

        forge(self.backup_root / "runs" / run_id, lines[1], run_id)
        stderr = io.StringIO()
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(stderr):
            rc = restore.run_restore(self.config, run_id=run_id, target=None, check_only=True)
        self.assertEqual(rc, 3)
        report = json.loads(stderr.getvalue().strip().splitlines()[-1])
        self.assertEqual(report["error"], "run_not_complete")
        self.assertIn("run_end is status='partial'", report["detail"])

        # The older "nothing to verify" fence still stands behind the gate: a run the tool
        # closed successfully with ZERO files (run_end ok, files 0, no errors) plus the same
        # forged pair passes the gate and must still be refused for having nothing to verify.
        empty_run = "opsa-20260825T000100.000Z"
        empty_dir_record = {"record": "dir", "run_id": empty_run, "store_id": "ledger_store",
                            "rel": "empty_dir"}
        with self.manifest.open("a", encoding="utf-8") as handle:
            for line in ({"record": "run_start", "schema": "mtc.opsa_manifest/v1",
                          "run_id": empty_run},
                         empty_dir_record,
                         {"record": "run_end", "run_id": empty_run, "status": "ok",
                          "files": 0, "errors": []}):
                handle.write(json.dumps(line) + "\n")
        forge(self.backup_root / "runs" / empty_run, empty_dir_record, empty_run)
        stdout = io.StringIO()
        stderr = io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            rc = restore.run_restore(self.config, run_id=empty_run, target=None, check_only=True)
        self.assertEqual(rc, 3)
        self.assertIn("nothing to verify", stderr.getvalue())
        summary = json.loads(stdout.getvalue().strip().splitlines()[-1])
        self.assertEqual(summary["status"], "failed")
        self.assertEqual(summary["verified_against_manifest"], 0)

    def test_restore_rejects_plain_parent_store_id_before_any_outside_write(self):
        """D026: a malicious manifest store id cannot escape the restore target."""
        run_id = "opsa-20260825T010000.000Z"
        payload = b"must stay confined"
        source = self.backup_root / "runs" / "outside" / "payload.bin"
        source.parent.mkdir(parents=True)
        source.write_bytes(payload)
        lines = [
            {"record": "run_start", "schema": "mtc.opsa_manifest/v1", "run_id": run_id},
            {"record": "file", "run_id": run_id, "store_id": "../outside",
             "rel": "payload.bin", "sha256": hashlib.sha256(payload).hexdigest()},
            {"record": "run_end", "run_id": run_id, "status": "ok", "files": 1,
             "errors": []},
        ]
        self.manifest.parent.mkdir(parents=True, exist_ok=True)
        self.manifest.write_text(
            "".join(json.dumps(line) + "\n" for line in lines), encoding="utf-8")
        target = self.root / "restore_target"
        outside = self.root / "outside" / "payload.bin"

        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            rc = restore.run_restore(self.config, run_id=run_id, target=target)

        self.assertFalse(outside.exists())
        self.assertFalse(target.exists())
        self.assertEqual(rc, 3)

    def _run_restore_cli_with_record(self, record: dict) -> tuple[subprocess.CompletedProcess, Path]:
        run_id = "opsa-20260825T020000.000Z"
        payload = b"field-validation-fixture"
        record = {"record": "file", "run_id": run_id,
                  "rel": "payload.bin", "sha256": hashlib.sha256(payload).hexdigest(),
                  **record}
        source = self.backup_root / "runs" / str(record.get("store_id")) / "payload.bin"
        source.parent.mkdir(parents=True, exist_ok=True)
        source.write_bytes(payload)
        lines = [
            {"record": "run_start", "schema": "mtc.opsa_manifest/v1", "run_id": run_id},
            record,
            {"record": "run_end", "run_id": run_id, "status": "ok", "files": 1,
             "errors": []},
        ]
        self.manifest.write_text(
            "".join(json.dumps(line) + "\n" for line in lines), encoding="utf-8")
        target = self.root / "restore_target"
        result = subprocess.run(
            [sys.executable, str(TOOLS_DIR / "restore.py"),
             "--config", str(self.config), "--run", run_id, "--to", str(target)],
            cwd=TOOLS_DIR, capture_output=True, text=True, check=False,
        )
        return result, target

    def _assert_structured_manifest_check_failure(
            self, result: subprocess.CompletedProcess, target: Path, field: str) -> None:
        self.assertNotIn("Traceback", result.stderr)
        self.assertEqual(result.returncode, 3)
        report = json.loads(result.stderr.strip().splitlines()[-1])
        self.assertEqual(report["status"], "check_failed")
        self.assertEqual(report["error"], "invalid_manifest_record")
        self.assertEqual(report["field"], field)
        self.assertFalse(target.exists())

    def test_restore_cli_missing_store_id_is_structured_check_failure_without_writes(self):
        """D026: a missing store_id is rejected before confinement, never stringified."""
        result, target = self._run_restore_cli_with_record({})
        self._assert_structured_manifest_check_failure(result, target, "store_id")

    def test_restore_cli_empty_path_is_structured_check_failure_without_writes(self):
        """D026: an empty manifest path (rel) is rejected before confinement."""
        result, target = self._run_restore_cli_with_record(
            {"store_id": "ledger_store", "rel": ""})
        self._assert_structured_manifest_check_failure(result, target, "rel")

    def test_backup_rejects_percent_encoded_parent_store_id_without_writes(self):
        """D026: encoded separators in ids are rejected, not treated as safe literals."""
        encoded = write_config(
            self.root, self.backup_root,
            [{"id": "..%2Foutside", "path": str(self.store), "class": "protected"}],
        )
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            rc = backup.run_backup(encoded)
        self.assertEqual(rc, 3)
        self.assertFalse(self.manifest.exists())
        self.assertFalse((self.backup_root / "runs").exists())

    def test_backup_rejects_store_ids_reserved_for_completion_evidence_without_writes(self):
        """A store named like the per-run completion files would occupy their path inside
        runs/<run_id>/; the config is refused before any run directory exists."""
        for reserved in (RUN_MANIFEST_NAME, COMPLETE_MARKER_NAME):
            with self.subTest(store_id=reserved):
                config = write_config(
                    self.root, self.backup_root,
                    [{"id": reserved, "path": str(self.store), "class": "protected"}],
                )
                stdout, stderr = io.StringIO(), io.StringIO()
                with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                    rc = backup.run_backup(config)
                self.assertEqual(rc, 3)
                self.assertFalse(self.manifest.exists())
                self.assertFalse((self.backup_root / "runs").exists())


class HeartbeatPathTests(unittest.TestCase):
    def test_heartbeat_rejects_traversal_absolute_and_drive_ids_without_writes(self):
        """D026: unsafe heartbeat ids cannot write inside or beside the state root."""
        cases = ("", "../escaped", "..%2Fescaped", "{absolute}", "C:drive_escape")
        for case in cases:
            with self.subTest(case=case), tempfile.TemporaryDirectory(
                    prefix="opsa_hb_path_") as tmp:
                root = Path(tmp)
                state_dir = root / "state"
                beat_id = str(root / "absolute") if case == "{absolute}" else case
                with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(
                        io.StringIO()):
                    rc = heartbeat.main([
                        "emit", "--state-dir", str(state_dir), "--id", beat_id,
                    ])
                self.assertEqual(list(root.rglob("*.hb.json")), [])
                self.assertEqual(rc, 3)


class WatchdogTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory(prefix="opsa_wd_")
        self.root = Path(self._tmp.name)
        self.state_dir = self.root / "state"
        self.state_dir.mkdir(parents=True)

    def tearDown(self):
        self._tmp.cleanup()

    def _beat(self, beat_id: str, at, note: str | None = None) -> None:
        payload = {"schema": "mtc.opsa_heartbeat/v1", "id": beat_id,
                   "emitted_at": at.isoformat(timespec="seconds").replace("+00:00", "Z"),
                   "seq": 1, "pid": os.getpid()}
        if note:
            payload["note"] = note
        (self.state_dir / f"{beat_id}.hb.json").write_text(
            json.dumps(payload), encoding="utf-8")

    def _run_watchdog_cli(self, argv: list[str]) -> tuple[int, dict]:
        """Run the full CLI (classification + notifier) capturing stdout's JSON report."""
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = watchdog.run_check(argv)
        return rc, json.loads(buf.getvalue().strip().splitlines()[-1])

    def _events(self) -> list[dict]:
        return [json.loads(line) for line in
                (self.root / "alerts.jsonl").read_text(encoding="utf-8").splitlines()]

    def test_fresh_heartbeat_ok(self):
        now = utc_now()
        self._beat("feed", now - timedelta(seconds=10))
        report = watchdog.check(self.state_dir, silence_seconds=900, expect=[], now=now)
        self.assertEqual(report["overall"], "ok")
        self.assertEqual(report["ids"]["feed"]["state"], "ok")

    def test_stale_heartbeat_silent(self):
        """Falsification: a killed process's stale beat must classify silent -> alert."""
        now = utc_now()
        self._beat("feed", now - timedelta(seconds=5000))
        report = watchdog.check(self.state_dir, silence_seconds=900, expect=[], now=now)
        self.assertEqual(report["overall"], "alert")
        self.assertEqual(report["ids"]["feed"]["state"], "silent")

    def test_missing_expected_id_alerts(self):
        now = utc_now()
        self._beat("feed", now)
        report = watchdog.check(self.state_dir, silence_seconds=900,
                                expect=["feed", "worker"], now=now)
        self.assertEqual(report["overall"], "alert")
        self.assertEqual(report["ids"]["worker"]["state"], "missing")

    def test_unreadable_heartbeat_is_check_failed_not_ok(self):
        """Falsification: corrupt JSON must NOT pass and must NOT claim silence."""
        (self.state_dir / "feed.hb.json").write_text("{ not json", encoding="utf-8")
        report = watchdog.check(self.state_dir, silence_seconds=900, expect=[], now=utc_now())
        self.assertEqual(report["overall"], "check_failed")
        self.assertEqual(report["ids"]["feed"]["state"], "unreadable")

    def test_bad_timestamp_is_check_failed(self):
        self._beat("feed", utc_now())
        path = self.state_dir / "feed.hb.json"
        payload = json.loads(path.read_text(encoding="utf-8"))
        payload["emitted_at"] = "yesterday-ish"
        path.write_text(json.dumps(payload), encoding="utf-8")
        report = watchdog.check(self.state_dir, silence_seconds=900, expect=[], now=utc_now())
        self.assertEqual(report["ids"]["feed"]["state"], "bad_timestamp")

    def test_future_timestamp_is_check_failed(self):
        now = utc_now()
        self._beat("feed", now + timedelta(hours=3))
        report = watchdog.check(self.state_dir, silence_seconds=900, expect=[], now=now)
        self.assertEqual(report["ids"]["feed"]["state"], "clock_skew")
        self.assertEqual(report["overall"], "check_failed")

    def test_empty_state_dir_is_check_failed_not_ok(self):
        report = watchdog.check(self.state_dir, silence_seconds=900, expect=[], now=utc_now())
        self.assertEqual(report["overall"], "check_failed")

    def test_missing_state_dir_is_check_failed(self):
        report = watchdog.check(self.root / "gone", silence_seconds=900,
                                expect=["feed"], now=utc_now())
        self.assertEqual(report["overall"], "check_failed")

    def test_local_log_notifier_writes_event(self):
        now = utc_now()
        self._beat("feed", now - timedelta(seconds=5000))
        notifier = watchdog.LocalLogNotifier(self.root / "alerts.jsonl")
        notifier.notify({"schema": "mtc.opsa_watchdog_event/v1", "id": "feed",
                         "state": "silent"})
        lines = (self.root / "alerts.jsonl").read_text(encoding="utf-8").splitlines()
        self.assertEqual(len(lines), 1)
        self.assertEqual(json.loads(lines[0])["state"], "silent")

    def test_missing_state_dir_yields_rc3_and_exactly_one_notifier_event(self):
        """Falsification (audit R1 #1): a vanished state dir must reach the notifier.

        Old behaviour: rc 3 with ZERO delivered events — the evidence-store-vanished
        scenario left no alert record anywhere. Required: rc 3 AND exactly one
        notifier event (synthetic id ``_watchdog_check`` carrying the error).
        """
        rc, report = self._run_watchdog_cli([
            "--state-dir", str(self.root / "gone"), "--silence-seconds", "900",
            "--notifier-log", str(self.root / "alerts.jsonl"),
        ])
        self.assertEqual(rc, 3)
        self.assertEqual(report["overall"], "check_failed")
        events = self._events()
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0]["id"], "_watchdog_check")
        self.assertEqual(events[0]["state"], "check_failed")
        self.assertIn("does not exist", events[0]["error"])

    def test_empty_state_dir_no_expect_notifies_check_failed(self):
        """Same guarantee for the other empty-ids branch: watching nothing must
        still leave exactly one notifier event, not a bare rc 3."""
        rc, report = self._run_watchdog_cli([
            "--state-dir", str(self.state_dir), "--silence-seconds", "900",
            "--notifier-log", str(self.root / "alerts.jsonl"),
        ])
        self.assertEqual(rc, 3)
        self.assertEqual(report["overall"], "check_failed")
        events = self._events()
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0]["id"], "_watchdog_check")
        self.assertIn("no heartbeat files", events[0]["error"])

    def test_invalid_now_is_check_failed_not_traceback(self):
        """Audit R1 nit 6: unparseable --now => check-failed record + notifier event
        + rc 3, never an unhandled ValueError traceback exiting rc 1."""
        self._beat("feed", utc_now())
        rc, report = self._run_watchdog_cli([
            "--state-dir", str(self.state_dir), "--silence-seconds", "900",
            "--now", "not-a-timestamp",
            "--notifier-log", str(self.root / "alerts.jsonl"),
        ])
        self.assertEqual(rc, 3)
        self.assertEqual(report["overall"], "check_failed")
        self.assertIn("--now", report["error"])
        events = self._events()
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0]["id"], "_watchdog_check")

    def test_per_id_outcomes_still_notify_per_id(self):
        """The synthetic event is an addition, not a replacement: a normal silent
        beat still notifies exactly once for that id (no _watchdog_check event)."""
        now = utc_now()
        self._beat("feed", now - timedelta(seconds=5000))
        rc, _ = self._run_watchdog_cli([
            "--state-dir", str(self.state_dir), "--silence-seconds", "900",
            "--notifier-log", str(self.root / "alerts.jsonl"),
        ])
        self.assertEqual(rc, 2)
        events = self._events()
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0]["id"], "feed")
        self.assertEqual(events[0]["state"], "silent")

    def test_silence_bound_is_required_and_has_no_ratified_default(self):
        """The 900-second default claimed '#39' provenance that was never ratified.

        RED on the pre-fix code: argparse supplied 900.0 and the run proceeded, so no
        SystemExit was raised. GREEN now: the bound is required and its absence errors.
        """
        now = utc_now()
        self._beat("feed", now - timedelta(seconds=5000))
        with contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit) as caught:
                self._run_watchdog_cli([
                    "--state-dir", str(self.state_dir),
                    "--notifier-log", str(self.root / "alerts.jsonl"),
                ])
        self.assertEqual(caught.exception.code, 2)
        source = Path("watchdog.py").read_text(encoding="utf-8")
        self.assertNotIn("default=900.0", source)
        self.assertNotIn("plan #39", source)

    def test_alert_recovery_alert_emits_all_three_transitions_once_each(self):
        """A recovery is a transition, not a state to stay silent about.

        RED on the pre-fix code: `ok` was skipped before the ledger was written, so
        prev_seen kept 'silent' and the SECOND alert was deduplicated away — two events,
        no recovery. GREEN now: three events, each exactly once.
        """
        state_file = self.root / "dedupe.json"
        log = self.root / "alerts.jsonl"
        argv = ["--state-dir", str(self.state_dir), "--silence-seconds", "900",
                "--notifier-log", str(log), "--state-file", str(state_file)]

        now = utc_now()
        self._beat("feed", now - timedelta(seconds=5000))   # silent -> alert
        self._run_watchdog_cli(argv)
        self._beat("feed", utc_now())                        # fresh -> recovery
        self._run_watchdog_cli(argv)
        self._beat("feed", utc_now() - timedelta(seconds=5000))  # silent again -> alert
        self._run_watchdog_cli(argv)

        states = [(event["id"], event["state"]) for event in self._events()]
        self.assertEqual(states, [("feed", "silent"), ("feed", "recovered"), ("feed", "silent")])

    def test_corrupt_dedupe_state_fails_safe_by_re_alerting(self):
        """Unreadable ledger must re-alert rather than crash or silently pass."""
        state_file = self.root / "dedupe.json"
        log = self.root / "alerts.jsonl"
        state_file.write_text("{ not json", encoding="utf-8")
        self._beat("feed", utc_now() - timedelta(seconds=5000))
        rc, _ = self._run_watchdog_cli([
            "--state-dir", str(self.state_dir), "--silence-seconds", "900",
            "--notifier-log", str(log), "--state-file", str(state_file),
        ])
        self.assertEqual(rc, 2)
        self.assertEqual([event["state"] for event in self._events()], ["silent"])


class NoDeleteGuaranteeTests(unittest.TestCase):
    """The no-delete guarantee is enforced by source inspection, not intent.

    A delete path cannot 'accidentally' appear: this test fails if any tool under
    tools/opsa contains a destructive call. (os.replace is a write, not a delete;
    .write_bytes(/.write_text( are overwrites of files this tooling owns or creates
    and are deliberately NOT banned — scope is deletion/truncation/removal of
    existing paths.)
    """

    def test_no_delete_calls_in_opsa_tools(self):
        # Call-site syntax (with parens) so docstrings that NAME the banned calls
        # (opsa_common's no-delete guarantee statement) do not self-match.
        # ``.unlink(`` covers both ``path.unlink()`` and ``path.unlink(missing_ok=True)``
        # (audit R1: the old ``.unlink()`` needle missed the missing_ok form); the
        # same call-site-prefix logic covers rmdir/truncate/move variants.
        banned = ("os.remove(", "os.unlink(", ".unlink(", "os.rmdir(", ".rmdir(",
                  "shutil.rmtree(", ".rmtree(", "shutil.move(", "os.truncate(",
                  "send2trash(")
        offenders: list[str] = []
        tool_files = ["opsa_common.py", "backup.py", "restore.py", "heartbeat.py", "watchdog.py"]
        for name in tool_files:  # the test file itself is out of scope (it names the needles)
            source = (TOOLS_DIR / name).read_text(encoding="utf-8")
            for needle in banned:
                if needle in source:
                    offenders.append(f"{name}: {needle}")
        self.assertEqual(offenders, [], f"delete code path found: {offenders}")


class TimestampTests(unittest.TestCase):
    def test_parse_roundtrip(self):
        now = utc_now().replace(microsecond=0)
        self.assertEqual(parse_utc_iso(
            now.isoformat(timespec="seconds").replace("+00:00", "Z")), now)

    def test_parse_rejects_naive(self):
        with self.assertRaises(ValueError):
            parse_utc_iso("2026-08-25T03:00:00")


if __name__ == "__main__":
    unittest.main()
