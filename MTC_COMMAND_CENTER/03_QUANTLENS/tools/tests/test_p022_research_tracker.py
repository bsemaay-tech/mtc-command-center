"""Contract tests for the reduced-scope P0-22 local tracker.

These tests intentionally exercise the command line and the one documented
``disclose_report`` seam.  They do not depend on the tracker's SQLite schema.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
from contextlib import closing
from pathlib import Path
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = ROOT / "tools" / "p022_research_tracker.py"


def _load_tracker():
    spec = importlib.util.spec_from_file_location("p022_research_tracker", MODULE_PATH)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load {MODULE_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _walk(value):
    yield value
    if isinstance(value, dict):
        for key, item in value.items():
            yield key
            yield from _walk(item)
    elif isinstance(value, list):
        for item in value:
            yield from _walk(item)


class P022TrackerContractTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="p022-contract-")
        self.root = Path(self.tmp.name)
        self.db = self.root / "tracker.sqlite3"
        self.files = {}

    def tearDown(self):
        self.tmp.cleanup()

    def _file(self, name: str, data: bytes) -> Path:
        path = self.root / name
        path.write_bytes(data)
        self.files[name] = path
        return path

    def _spec(
        self,
        experiment_id: str = "exp-a",
        start: str = "2026-01-01T00:00:00Z",
        end: str = "2026-01-02T00:00:00Z",
        *,
        family_reference=None,
        parent_experiment_ids=None,
        related_experiment_ids=None,
        config=b"{\"setting\": 1}\n",
        prefix="a",
    ):
        strategy = self._file(f"{prefix}-strategy.pine", b"strategy fixture\n")
        configuration = self._file(f"{prefix}-config.json", config)
        dataset = self._file(f"{prefix}-dataset.csv", b"time,value\n1,2\n")
        report = self._file(f"{prefix}-report.bin", b"\x00\xffreport\n\x80\x01")
        references = [
            ("strategy-ref", "strategy", strategy),
            ("config-ref", "configuration", configuration),
            ("dataset-ref", "dataset", dataset),
            ("report-ref", "report", report),
        ]
        result = {
            "record_version": 1,
            "local_experiment_id": experiment_id,
            "period_start_utc": start,
            "period_end_utc": end,
            "references": [
                {
                    "reference_id": reference_id,
                    "role": role,
                    "path": str(path.resolve()),
                    "sha256": _sha256(path),
                }
                for reference_id, role, path in references
            ],
        }
        if family_reference is not None:
            result["family_reference"] = family_reference
        if parent_experiment_ids is not None:
            result["parent_experiment_ids"] = parent_experiment_ids
        if related_experiment_ids is not None:
            result["related_experiment_ids"] = related_experiment_ids
        return result

    def _write_spec(self, spec, name="spec.json") -> Path:
        path = self.root / name
        path.write_text(json.dumps(spec, indent=2), encoding="utf-8")
        return path

    def _run(self, *args) -> subprocess.CompletedProcess:
        return subprocess.run(
            [sys.executable, str(MODULE_PATH), *map(str, args)],
            cwd=ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=15,
            check=False,
        )

    def _register(self, spec, name="spec.json"):
        spec_path = self._write_spec(spec, name)
        result = self._run("register", "--db", self.db, "--spec", spec_path)
        self.assertEqual(result.returncode, 0, result.stderr.decode(errors="replace"))
        return result

    def _status(self, output_format="json"):
        result = self._run("status", "--db", self.db, "--format", output_format)
        self.assertEqual(result.returncode, 0, result.stderr.decode(errors="replace"))
        return result.stdout.decode("utf-8")

    def _status_json(self):
        return json.loads(self._status("json"))

    def _disclose(self, experiment_id="exp-a", revision=1, report_id="report-ref"):
        return self._run(
            "disclose",
            "--db",
            self.db,
            "--experiment-id",
            experiment_id,
            "--revision",
            revision,
            "--report-id",
            report_id,
        )

    @staticmethod
    def _non_local_paths(leaf="subject"):
        return (
            "\\\\server\\share\\" + leaf,
            "//server/share/" + leaf,
            "\\\\?\\C:\\" + leaf,
            "\\\\.\\PIPE\\" + leaf,
        )

    @staticmethod
    def _assert_markdown_inert(test_case, markdown):
        test_case.assertNotRegex(markdown, r"(?m)^#\s*LIVE_CANDIDATE\b")
        test_case.assertNotRegex(markdown, r"(?m)^[-*+]\s*clean-window\s+PASS\b")
        # A link-looking value is acceptable only inside the renderer's
        # escaped inline-code payload, never as an active list item.
        test_case.assertNotRegex(
            markdown, r"(?m)^-\s+(?!`)[^\n]*\[spoof\]\("
        )
        test_case.assertNotIn("```", markdown)

    def test_registration_is_idempotent_then_changed_config_is_revision_and_persists(self):
        first = self._spec()
        self._register(first)
        self._register(first, "same-spec.json")

        changed = self._spec(config=b"{\"setting\": 2}\n")
        self._register(changed, "changed-spec.json")
        data = self._status_json()  # a fresh process/reopen is part of this check
        revisions = {
            item["revision"]
            for item in _walk(data)
            if isinstance(item, dict)
            and isinstance(item.get("revision"), int)
        }
        self.assertIn(1, revisions)
        self.assertIn(2, revisions)
        self.assertNotIn(3, revisions)

    def test_replaced_or_missing_report_is_refused_with_zero_stdout(self):
        spec = self._spec()
        self._register(spec)
        report = self.files["a-report.bin"]
        report.write_bytes(b"replaced report")

        replaced = self._disclose()
        self.assertNotEqual(replaced.returncode, 0)
        self.assertEqual(replaced.stdout, b"")
        self.assertTrue(replaced.stderr)

        report.unlink()
        missing = self._disclose()
        self.assertNotEqual(missing.returncode, 0)
        self.assertEqual(missing.stdout, b"")
        self.assertTrue(missing.stderr)

    def test_disclosure_emits_exact_binary_buffer_and_duplicate_attempts(self):
        spec = self._spec()
        self._register(spec)
        tracker = _load_tracker()
        emitted = []

        tracker.disclose_report(
            str(self.db), "exp-a", 1, "report-ref", emitted.append
        )
        tracker.disclose_report(
            str(self.db), "exp-a", 1, "report-ref", emitted.append
        )
        self.assertEqual(emitted, [b"\x00\xffreport\n\x80\x01"] * 2)
        status = self._status_json()
        self.assertEqual(len(status["disclosure_attempts"]), 2)

    def _disclosure_table(self, connection):
        candidates = []
        for (table,) in connection.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
        ):
            quoted = table.replace('"', '""')
            columns = {
                row[1].lower()
                for row in connection.execute(f'PRAGMA table_info("{quoted}")')
            }
            # The contract requires append-only disclosure events, but does
            # not prescribe duplicated denormalized keys.  Identify the event
            # table by its report key and revision FK/number.
            if "report_id" in columns and ({"revision_id", "revision"} & columns):
                candidates.append(table)
        if not candidates:
            self.fail("contract test could not locate the disclosure-attempt table")
        return next(
            (name for name in candidates if "disclos" in name.lower() or "attempt" in name.lower()),
            candidates[0],
        )

    def _install_insert_failure_trigger(self):
        """Install a test-owned abort trigger without assuming a table name."""
        with closing(sqlite3.connect(self.db)) as connection:
            table = self._disclosure_table(connection)
            quoted_table = table.replace('"', '""')
            connection.execute(
                f'''CREATE TRIGGER p022_test_abort BEFORE INSERT ON "{quoted_table}"
                    BEGIN SELECT RAISE(ABORT, 'test-owned insert failure'); END'''
            )
            connection.commit()

    def _install_commit_failure_trigger(self):
        """Make an AFTER INSERT trigger create a deferred FK violation."""
        with closing(sqlite3.connect(self.db)) as connection:
            connection.execute("PRAGMA foreign_keys = ON")
            table = self._disclosure_table(connection)
            connection.execute(
                "CREATE TABLE p022_test_parent (id INTEGER PRIMARY KEY)"
            )
            connection.execute(
                """CREATE TABLE p022_test_deferred_child (
                    parent_id INTEGER NOT NULL,
                    FOREIGN KEY(parent_id) REFERENCES p022_test_parent(id)
                        DEFERRABLE INITIALLY DEFERRED
                )"""
            )
            quoted_table = table.replace('"', '""')
            connection.execute(
                f'''CREATE TRIGGER p022_test_commit_abort AFTER INSERT ON "{quoted_table}"
                    BEGIN INSERT INTO p022_test_deferred_child(parent_id) VALUES (1); END'''
            )
            connection.commit()

    def _assert_no_history(self, db: Path):
        """A failed pre-transaction registration leaves no user-table rows."""
        if not db.exists():
            return
        with closing(sqlite3.connect(db)) as connection:
            tables = [
                row[0]
                for row in connection.execute(
                    "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
                )
            ]
            for table in tables:
                quoted = table.replace('"', '""')
                count = connection.execute(f'SELECT COUNT(*) FROM "{quoted}"').fetchone()[0]
                self.assertEqual(count, 0, f"failed registration left rows in {table}")

    def test_registration_digest_mismatch_or_missing_reference_writes_no_history(self):
        mismatch_db = self.root / "mismatch.sqlite3"
        mismatch_spec = self._spec(prefix="mismatch")
        mismatch_spec["references"][1]["sha256"] = "0" * 64
        mismatch_path = self._write_spec(mismatch_spec, "mismatch.json")
        mismatch = self._run("register", "--db", mismatch_db, "--spec", mismatch_path)
        self.assertNotEqual(mismatch.returncode, 0)
        self.assertTrue(mismatch.stderr)
        self._assert_no_history(mismatch_db)

        missing_db = self.root / "missing-reference.sqlite3"
        missing_spec = self._spec(prefix="missing-reference")
        self.files["missing-reference-dataset.csv"].unlink()
        missing_path = self._write_spec(missing_spec, "missing-reference.json")
        missing = self._run("register", "--db", missing_db, "--spec", missing_path)
        self.assertNotEqual(missing.returncode, 0)
        self.assertTrue(missing.stderr)
        self._assert_no_history(missing_db)

    def test_insert_or_commit_failure_emits_zero_report_bytes(self):
        self._register(self._spec())
        self._install_insert_failure_trigger()
        result = self._disclose()
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout, b"")
        self.assertTrue(result.stderr)

    def test_commit_failure_emits_zero_report_bytes_and_persists_no_event(self):
        self._register(self._spec())
        self._install_commit_failure_trigger()
        result = self._disclose()
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout, b"")
        self.assertTrue(result.stderr)
        self.assertEqual(self._status_json()["disclosure_attempts"], [])

    def test_emitter_crash_after_commit_retains_whole_period_exposure(self):
        self._register(self._spec())
        tracker = _load_tracker()

        def crash(_buffer):
            raise RuntimeError("test emitter crash")

        with self.assertRaises(RuntimeError):
            tracker.disclose_report(str(self.db), "exp-a", 1, "report-ref", crash)

        status = self._status("json")
        self.assertIn("report-ref", status)
        self.assertIn("2026-01-01T00:00:00Z", status)
        self.assertIn("2026-01-02T00:00:00Z", status)
        self.assertIn("exposure", status.lower())

    def test_status_reports_lineage_conflicts_overlap_ref_drift_and_unmonitored_limits(self):
        a = self._spec(
            family_reference="family-a",
            parent_experiment_ids=["missing-parent"],
            related_experiment_ids=["exp-b"],
            prefix="a",
        )
        self._register(a, "a-v1.json")
        a2 = self._spec(
            family_reference="family-b",
            parent_experiment_ids=["missing-parent"],
            related_experiment_ids=["exp-b"],
            config=b"{\"setting\": 2}\n",
            prefix="a",
        )
        self._register(a2, "a-v2.json")
        b = self._spec(
            experiment_id="exp-b",
            start="2026-01-01T12:00:00Z",
            end="2026-01-03T00:00:00Z",
            family_reference="family-b",
            related_experiment_ids=["exp-a"],
            prefix="b",
        )
        self._register(b, "b.json")
        c = self._spec(experiment_id="exp-c", prefix="c")
        self._register(c, "c.json")

        # Current references deliberately drift after registration.
        self.files["a-strategy.pine"].write_bytes(b"changed strategy")
        self.files["b-dataset.csv"].unlink()

        status = self._status("json")
        lower = status.lower()
        self.assertIn("mismatch", lower)
        self.assertIn("missing", lower)
        self.assertIn("overlap", lower)
        self.assertIn("lineage", lower)
        self.assertIn("conflict", lower)
        self.assertIn("missing-parent", status)
        self.assertIn("exp-a", status)
        self.assertIn("exp-b", status)
        self.assertIn("exp-c", status)
        self.assertIn("local_log_only", lower)
        self.assertIn("access_completeness_unverified", lower)
        self.assertIn("unmonitored", lower)

        markdown = self._status("markdown").lower()
        self.assertIn("local_log_only", markdown)
        self.assertIn("access_completeness_unverified", markdown)

        # The refusal boundary must not turn local history into a positive
        # clean-window, certificate, promotion, or live-candidate claim.
        self.assertNotIn("live_candidate", lower)
        self.assertNotIn("clean-window certificate", lower)
        self.assertNotIn("clean window certificate", lower)

    def test_control_characters_are_rejected_in_all_stored_text_fields(self):
        attack = "field\n# LIVE_CANDIDATE\r\n- clean-window PASS\x1b"
        cases = [
            ("local_experiment_id", lambda spec: spec.update(local_experiment_id=attack)),
            ("reference_id", lambda spec: spec["references"][0].update(reference_id=attack)),
            ("family_reference", lambda spec: spec.update(family_reference=attack)),
            ("parent_experiment_ids", lambda spec: spec.update(parent_experiment_ids=[attack])),
            ("related_experiment_ids", lambda spec: spec.update(related_experiment_ids=[attack])),
            (
                "reference_path",
                lambda spec: spec["references"][0].update(
                    path=spec["references"][0]["path"] + attack
                ),
            ),
        ]
        for index, (field, mutate) in enumerate(cases):
            with self.subTest(field=field):
                db = self.root / f"control-{index}.sqlite3"
                spec = self._spec(prefix=f"control-{index}")
                mutate(spec)
                spec_path = self._write_spec(spec, f"control-{index}.json")
                result = self._run("register", "--db", db, "--spec", spec_path)
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(result.stdout, b"")
                self.assertTrue(result.stderr)
                self._assert_no_history(db)

    def test_markdown_delimiters_cannot_create_links_or_claims(self):
        attack = "family-safe` [spoof](https://example.invalid) # LIVE_CANDIDATE"
        spec = self._spec(family_reference=attack, prefix="markdown")
        spec_path = self._write_spec(spec, "markdown.json")
        result = self._run("register", "--db", self.db, "--spec", spec_path)
        if result.returncode != 0:
            self.assertEqual(result.stdout, b"")
            self.assertTrue(result.stderr)
            return
        self._assert_markdown_inert(self, self._status("markdown"))

    def test_tampered_text_fields_are_refused_or_rendered_as_inert_markdown(self):
        self._register(self._spec())
        attack = "tampered\n# LIVE_CANDIDATE\r\n- clean-window PASS\n[spoof](https://example.invalid)\n```"
        with closing(sqlite3.connect(self.db)) as connection:
            connection.execute(
                "UPDATE experiment_revisions SET local_experiment_id=?, family_reference=? WHERE id=1",
                (attack, attack),
            )
            connection.execute(
                'UPDATE "references" SET reference_id=? WHERE revision_id=1 AND role="report"',
                (attack,),
            )
            connection.commit()
        tracker = _load_tracker()
        try:
            markdown = tracker.status(self.db, "markdown")
        except tracker.TrackerError:
            return
        self._assert_markdown_inert(self, markdown)

    def test_non_local_spec_paths_are_rejected_before_open(self):
        tracker = _load_tracker()
        for path in self._non_local_paths("spec.json"):
            with self.subTest(path=path):
                with mock.patch.object(
                    tracker.Path,
                    "open",
                    autospec=True,
                    side_effect=AssertionError("spec path was opened"),
                ):
                    with self.assertRaises(tracker.TrackerError):
                        tracker.register(self.db, path)

    def test_non_local_db_paths_are_rejected_before_any_input_io(self):
        tracker = _load_tracker()
        spec = self._spec(prefix="db-path")
        spec_path = self._write_spec(spec, "db-path.json")
        for path in self._non_local_paths("tracker.sqlite3"):
            with self.subTest(path=path):
                with mock.patch.object(
                    tracker.Path,
                    "open",
                    autospec=True,
                    side_effect=AssertionError("input path was opened"),
                ):
                    with self.assertRaises(tracker.TrackerError):
                        tracker.register(path, spec_path)

    def test_non_local_registered_reference_paths_are_rejected_before_hashing(self):
        tracker = _load_tracker()
        for path in self._non_local_paths("strategy.pine"):
            with self.subTest(path=path):
                spec = self._spec(prefix="registered-path")
                spec["references"][0]["path"] = path
                spec_path = self._write_spec(spec, "registered-path.json")
                with mock.patch.object(
                    tracker,
                    "_hash_file",
                    side_effect=AssertionError("registered path was read"),
                ):
                    with self.assertRaises(tracker.TrackerError):
                        tracker.register(self.db, spec_path)

    def test_non_local_db_paths_are_rejected_before_status_or_disclosure_io(self):
        tracker = _load_tracker()
        for path in self._non_local_paths("tracker.sqlite3"):
            with self.subTest(path=path):
                with mock.patch.object(
                    tracker, "_connect", side_effect=AssertionError("database was opened")
                ):
                    with self.assertRaises(tracker.TrackerError):
                        tracker.status(path, "json")
                    with self.assertRaises(tracker.TrackerError):
                        tracker.disclose_report(path, "exp-a", 1, "report-ref", lambda _: None)

    def test_tampered_non_local_reference_paths_are_rejected_before_status_io(self):
        self._register(self._spec())
        tracker = _load_tracker()
        for path in self._non_local_paths("tampered-report.bin"):
            with self.subTest(path=path):
                with closing(sqlite3.connect(self.db)) as connection:
                    connection.execute(
                        'UPDATE "references" SET path=? WHERE revision_id=1 AND role="report"',
                        (path,),
                    )
                    connection.commit()
                original_exists = tracker.Path.exists

                def guarded_exists(candidate):
                    if os.fspath(candidate) == path:
                        raise AssertionError("tampered path was probed")
                    return original_exists(candidate)

                with mock.patch.object(
                    tracker.Path, "exists", autospec=True, side_effect=guarded_exists
                ):
                    with self.assertRaises(tracker.TrackerError):
                        tracker.status(self.db, "json")

    def test_tampered_non_local_report_path_is_rejected_before_disclosure_read(self):
        self._register(self._spec())
        tracker = _load_tracker()
        path = self._non_local_paths("tampered-report.bin")[0]
        with closing(sqlite3.connect(self.db)) as connection:
            connection.execute(
                'UPDATE "references" SET path=? WHERE revision_id=1 AND role="report"',
                (path,),
            )
            connection.commit()
        original_open = tracker.Path.open

        def guarded_open(candidate, *args, **kwargs):
            if os.fspath(candidate) == path:
                raise AssertionError("tampered report path was opened")
            return original_open(candidate, *args, **kwargs)

        with mock.patch.object(
            tracker.Path, "open", autospec=True, side_effect=guarded_open
        ):
            with self.assertRaises(tracker.TrackerError):
                tracker.disclose_report(
                    self.db, "exp-a", 1, "report-ref", lambda _: None
                )


if __name__ == "__main__":
    unittest.main()
