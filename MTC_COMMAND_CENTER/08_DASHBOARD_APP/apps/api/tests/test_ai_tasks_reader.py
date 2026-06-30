from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from mcc_readonly.ai_tasks_reader import build_ai_tasks


def _write_registry(root: Path, payload) -> None:
    reg = root / "05_REGISTRY"
    reg.mkdir(parents=True, exist_ok=True)
    (reg / "AI_TASKS.json").write_text(json.dumps(payload), encoding="utf-8")


class TestAiTasksReader(unittest.TestCase):
    def test_valid_registry(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            _write_registry(root, {
                "intro": "hi",
                "tasks": [
                    {"id": "t1", "title": "T1", "summary": "s", "read": ["a"], "knobs": ["K"], "prompt": "do {K}"},
                    {"id": "t2", "prompt": "p2"},
                ],
            })
            out = build_ai_tasks(root)
            self.assertTrue(out["available"])
            self.assertEqual(out["count"], 2)
            self.assertEqual([t["id"] for t in out["tasks"]], ["t1", "t2"])
            self.assertEqual(out["tasks"][0]["knobs"], ["K"])

    def test_skips_entries_without_id_or_prompt(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            _write_registry(root, {"tasks": [{"id": "ok", "prompt": "p"}, {"title": "no id"}, {"id": "nopro"}]})
            out = build_ai_tasks(root)
            self.assertEqual(out["count"], 1)
            self.assertEqual(out["tasks"][0]["id"], "ok")

    def test_missing_file(self):
        with tempfile.TemporaryDirectory() as d:
            out = build_ai_tasks(Path(d))
            self.assertFalse(out["available"])
            self.assertEqual(out["reason"], "registry_not_found")
            self.assertEqual(out["tasks"], [])

    def test_malformed_json(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            reg = root / "05_REGISTRY"
            reg.mkdir(parents=True)
            (reg / "AI_TASKS.json").write_text("{ not json", encoding="utf-8")
            out = build_ai_tasks(root)
            self.assertFalse(out["available"])
            self.assertTrue(out["reason"].startswith("json_error"))


if __name__ == "__main__":
    unittest.main()
