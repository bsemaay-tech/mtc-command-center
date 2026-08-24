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
import io
import json
import os
import sys
import tempfile
import unittest
from datetime import timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from opsa_common import parse_utc_iso, utc_now  # noqa: E402
import backup  # noqa: E402
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

    def test_roundtrip_byte_identical(self):
        """Back up, damage the live copy, restore -> every file byte-identical."""
        self.assertEqual(self._run_backup(), 0)
        # Damage the live store (overwrite one file, empty another).
        (self.store / "ledger.jsonl").write_bytes(b"CORRUPTED")
        (self.store / "sub" / "blob.bin").write_bytes(b"")
        target = self.root / "restored"
        rc = restore.run_restore(self.config, run_id=None, target=target)
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
        rc = restore.run_restore(self.config, run_id=None, target=self.root / "restored")
        self.assertEqual(rc, 1)
        self.assertFalse((self.root / "restored" / "ledger_store" / "sub" / "blob.bin").exists())

    def test_check_only_detects_corruption_writes_nothing(self):
        self.assertEqual(self._run_backup(), 0)
        run_dir = next((self.backup_root / "runs").iterdir())
        victim = run_dir / "ledger_store" / "ledger.jsonl"
        victim.write_bytes(b"tampered")
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = restore.run_restore(self.config, run_id=None, target=None, check_only=True)
        self.assertEqual(rc, 1)
        self.assertFalse((self.root / "restored").exists())
        summary = json.loads(buf.getvalue().strip().splitlines()[-1])
        # Audit R1 nit 4: --check-only writes nothing, so it must not claim
        # directories it did not create (old code reported the dir-record count).
        self.assertEqual(summary["dirs_recreated"], 0)

    def test_latest_selects_newest_run(self):
        """--latest restores the highest run_id, not an arbitrary one."""
        self.assertEqual(self._run_backup(store_filter={"ledger_store"}), 0)
        (self.store / "ledger.jsonl").write_bytes(b'{"row":1,"note":"CHANGED"}\r\n')
        self.assertEqual(self._run_backup(store_filter={"ledger_store"}), 0)
        runs = sorted((self.backup_root / "runs").iterdir())
        self.assertEqual(len(runs), 2)
        target = self.root / "restored"
        rc = restore.run_restore(self.config, run_id=None, target=target)
        self.assertEqual(rc, 0)
        # Newest run must carry the CHANGED content (proves --latest, not --first).
        self.assertEqual((target / "ledger_store" / "ledger.jsonl").read_bytes(),
                         b'{"row":1,"note":"CHANGED"}\r\n')


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
