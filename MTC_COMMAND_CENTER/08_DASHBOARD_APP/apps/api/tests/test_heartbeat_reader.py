from __future__ import annotations

import json
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

from mcc_readonly.heartbeat_reader import build_overnight_heartbeat


def _ts(minutes_ago: float) -> str:
    return (datetime.now(timezone.utc) - timedelta(minutes=minutes_ago)).isoformat().replace("+00:00", "Z")


def _write(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload), encoding="utf-8")


def _new_contract(overnight: Path, run_id: str, *, updated_ago: float,
                  progress_ago: float, status: dict | None = None) -> None:
    prog = overnight / "progress"
    _write(prog / "_latest.json", {"run_id": run_id})
    _write(prog / run_id / "heartbeat.json", {
        "schema": "mtc.run_progress/v1", "run_id": run_id, "runner": "unit", "pid": 1,
        "started_at": _ts(60), "updated_at": _ts(updated_ago), "last_progress_at": _ts(progress_ago),
        "phase": "sweep", "state": "running",
        "progress": {"current": 50, "total": 200, "pct": 25.0, "eta_seconds": 100},
        "counters": {"completed": 50, "failed": 0}, "last_event_seq": 51,
    })
    if status is not None:
        _write(prog / run_id / "status.json", status)


class HeartbeatReaderTests(unittest.TestCase):
    def test_reads_new_progress_contract_running(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            overnight = Path(tmp)
            _new_contract(overnight, "r1", updated_ago=0.2, progress_ago=0.2)
            out = build_overnight_heartbeat(overnight)
            self.assertTrue(out["available"])
            self.assertEqual(out["source"], "progress/v1")
            self.assertEqual(out["run_id"], "r1")
            self.assertEqual(out["state"], "running")
            self.assertTrue(out["is_alive"])
            self.assertEqual(out["progress_pct"], 25.0)

    def test_new_contract_done_when_status_ok(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            overnight = Path(tmp)
            _new_contract(overnight, "r2", updated_ago=0.2, progress_ago=0.2,
                          status={"schema": "mtc.run_status/v1", "run_id": "r2",
                                  "result": "ok", "exit_code": 0, "finished_at": _ts(0.1)})
            out = build_overnight_heartbeat(overnight)
            self.assertEqual(out["state"], "done")

    def test_new_contract_failed_when_status_fail(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            overnight = Path(tmp)
            _new_contract(overnight, "r3", updated_ago=0.2, progress_ago=0.2,
                          status={"schema": "mtc.run_status/v1", "run_id": "r3",
                                  "result": "fail", "exit_code": 1, "finished_at": _ts(0.1)})
            out = build_overnight_heartbeat(overnight)
            self.assertEqual(out["state"], "failed")

    def test_new_contract_stalled_when_progress_old_but_proc_alive(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            overnight = Path(tmp)
            # proc alive (updated 1m ago) but no forward progress for 30m
            _new_contract(overnight, "r4", updated_ago=1.0, progress_ago=30.0)
            out = build_overnight_heartbeat(overnight)
            self.assertEqual(out["state"], "stalled")
            self.assertTrue(out["is_alive"])

    def test_new_contract_dead_when_updated_old(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            overnight = Path(tmp)
            _new_contract(overnight, "r5", updated_ago=60.0, progress_ago=60.0)
            out = build_overnight_heartbeat(overnight)
            self.assertEqual(out["state"], "dead")
            self.assertFalse(out["is_alive"])

    def test_falls_back_to_legacy_heartbeat_glob(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            overnight = Path(tmp)
            _write(overnight / "_heartbeat_oldrun.json",
                   {"run_id": "oldrun", "timestamp": _ts(0.2), "status": "running", "stage": "sweep"})
            out = build_overnight_heartbeat(overnight)
            self.assertTrue(out["available"])
            self.assertEqual(out["source"], "legacy")
            self.assertEqual(out["run_id"], "oldrun")
            self.assertTrue(out["is_alive"])

    def test_unavailable_when_nothing_present(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = build_overnight_heartbeat(Path(tmp))
            self.assertFalse(out["available"])


if __name__ == "__main__":
    unittest.main()
