from __future__ import annotations

import unittest
from datetime import datetime, timezone

from mcc_readonly.task_lifecycle import build_task_lifecycle


class TaskLifecycleTests(unittest.TestCase):
    def test_detects_waiting_and_stale_candidates(self) -> None:
        diagnostics = build_task_lifecycle(
            {
                "tasks": [
                    {
                        "id": "A",
                        "title": "Waiting task",
                        "status": "WAITING_FOR_USER",
                        "phase": "Test",
                        "requires_user_input": True,
                    },
                    {
                        "id": "B",
                        "title": "Stale task",
                        "status": "IN_PROGRESS",
                        "phase": "Test",
                        "timeout_seconds": 10,
                        "updated_at": "2026-05-30T00:00:00+00:00",
                    },
                    {
                        "id": "C",
                        "title": "Ready task",
                        "status": "READY",
                        "phase": "Test",
                    },
                ]
            },
            now=datetime(2026, 5, 30, 0, 1, 0, tzinfo=timezone.utc),
        )
        self.assertEqual(diagnostics["summary"]["waiting_for_user"], 1)
        self.assertEqual(diagnostics["summary"]["stale_candidates"], 1)
        self.assertIn("WAITING_FOR_USER", diagnostics["task_flags"]["A"])
        self.assertIn("STALE_CANDIDATE", diagnostics["task_flags"]["B"])


if __name__ == "__main__":
    unittest.main()

