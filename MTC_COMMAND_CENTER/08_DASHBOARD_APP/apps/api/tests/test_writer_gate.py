from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path

from mcc_readonly.writer import process_inbox


SOURCE_MCC_ROOT = Path(__file__).resolve().parents[4]


class WriterGateTests(unittest.TestCase):
    def test_process_inbox_accepts_create_task_proposal(self) -> None:
        with _mcc_fixture() as root:
            proposal = {
                "schema_version": "1.0",
                "proposal_id": "TP-ACCEPT-001",
                "action": "create_task",
                "task": {
                    "id": "TEST-TASK-001",
                    "title": "Fixture task",
                    "status": "READY",
                    "assigned_ai": "Codex",
                    "phase": "Test",
                    "dependencies": [],
                    "requires_user_input": False,
                    "allowed_actions": ["test"],
                    "forbidden_actions": ["touch protected files"],
                    "expected_outputs": ["receipt"],
                    "report_path": None,
                    "created_at": "2026-05-30T00:00:00+03:00",
                    "updated_at": "2026-05-30T00:00:00+03:00",
                },
            }
            _write_proposal(root, proposal)
            result = process_inbox(root, owner_ai="test", task_id="TEST-WRITER")
            self.assertEqual(result["accepted"], 1)
            queue = _load_json(root / "02_TASKS" / "TASK_QUEUE.json")
            self.assertTrue(any(task["id"] == "TEST-TASK-001" for task in queue["tasks"]))
            receipt = _load_json(root / "02_TASKS" / "outbox" / "TP-ACCEPT-001.accepted.json")
            self.assertEqual(receipt["status"], "accepted")
            events = (root / "03_STATUS" / "status_events.jsonl").read_text(encoding="utf-8")
            self.assertIn("TASK_PROPOSAL_ACCEPTED", events)
            self.assertFalse((root / "02_TASKS" / ".locks" / "task_queue.lock").exists())
            backups = list((root / "03_STATUS" / ".backups").rglob("TASK_QUEUE.json.*.bak"))
            self.assertTrue(backups)

    def test_process_inbox_rejects_duplicate_task_id(self) -> None:
        with _mcc_fixture() as root:
            existing_id = _load_json(root / "02_TASKS" / "TASK_QUEUE.json")["tasks"][0]["id"]
            proposal = {
                "schema_version": "1.0",
                "proposal_id": "TP-REJECT-001",
                "action": "create_task",
                "task": {
                    "id": existing_id,
                    "title": "Duplicate task",
                    "status": "READY",
                    "assigned_ai": "Codex",
                    "phase": "Test",
                    "requires_user_input": False,
                },
            }
            _write_proposal(root, proposal)
            result = process_inbox(root, owner_ai="test", task_id="TEST-WRITER")
            self.assertEqual(result["rejected"], 1)
            receipt = _load_json(root / "02_TASKS" / "outbox" / "TP-REJECT-001.rejected.json")
            self.assertIn("task already exists", receipt["errors"][0])

    def test_process_inbox_rejects_invalid_json(self) -> None:
        with _mcc_fixture() as root:
            (root / "02_TASKS" / "inbox" / "bad.json").write_text("{bad", encoding="utf-8")
            result = process_inbox(root, owner_ai="test", task_id="TEST-WRITER")
            self.assertEqual(result["rejected"], 1)
            receipt = _load_json(root / "02_TASKS" / "outbox" / "bad.rejected.json")
            self.assertIn("json parse error", receipt["errors"][0])


class _mcc_fixture:
    def __enter__(self) -> Path:
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name) / "MTC_COMMAND_CENTER"
        for rel in ("02_TASKS", "03_STATUS", "06_SCHEMAS"):
            shutil.copytree(SOURCE_MCC_ROOT / rel, root / rel, ignore=shutil.ignore_patterns("__pycache__"))
        (root / "02_TASKS" / "inbox").mkdir(parents=True, exist_ok=True)
        (root / "02_TASKS" / "outbox").mkdir(parents=True, exist_ok=True)
        return root

    def __exit__(self, exc_type, exc, tb) -> None:
        self.tmp.cleanup()


def _write_proposal(root: Path, proposal: dict) -> None:
    path = root / "02_TASKS" / "inbox" / f"{proposal['proposal_id']}.json"
    path.write_text(json.dumps(proposal, ensure_ascii=False, indent=2), encoding="utf-8")


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
