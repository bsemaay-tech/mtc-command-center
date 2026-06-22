"""TDD tests for run_watchdog — the one-shot consumer an external scheduler (n8n) calls."""
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TOOLS))

from run_watchdog import check  # noqa: E402


def _ts(minutes_ago: float) -> str:
    return (datetime.now(timezone.utc) - timedelta(minutes=minutes_ago)).isoformat().replace("+00:00", "Z")


def _write(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload), encoding="utf-8")


def _make_run(progress_root: Path, run_id: str, *, updated_ago=0.1, progress_ago=0.1, status=None):
    _write(progress_root / "_latest.json", {"run_id": run_id})
    _write(progress_root / run_id / "heartbeat.json", {
        "schema": "mtc.run_progress/v1", "run_id": run_id, "runner": "unit",
        "updated_at": _ts(updated_ago), "last_progress_at": _ts(progress_ago),
        "phase": "sweep", "progress": {"current": 5, "total": 10, "pct": 50.0},
    })
    if status is not None:
        _write(progress_root / run_id / "status.json", status)


class RecordingNotifier:
    def __init__(self):
        self.sent = []

    def __call__(self, payload):
        self.sent.append(payload)


def test_no_alert_while_running(tmp_path):
    prog = tmp_path / "progress"
    _make_run(prog, "r1")
    notifier = RecordingNotifier()
    state = check(prog, notifier=notifier)
    assert state == "running"
    assert notifier.sent == []


def test_alerts_once_on_failed_then_dedupes(tmp_path):
    prog = tmp_path / "progress"
    _make_run(prog, "r2", status={"result": "fail", "exit_code": 1})
    notifier = RecordingNotifier()

    state1 = check(prog, notifier=notifier)
    state2 = check(prog, notifier=notifier)  # second poll, same state

    assert state1 == "failed"
    assert state2 == "failed"
    assert len(notifier.sent) == 1  # deduped
    assert notifier.sent[0]["run_id"] == "r2"
    assert notifier.sent[0]["state"] == "failed"


def test_alerts_on_done_with_progress_payload(tmp_path):
    prog = tmp_path / "progress"
    _make_run(prog, "r3", status={"result": "ok", "exit_code": 0})
    notifier = RecordingNotifier()
    check(prog, notifier=notifier)
    assert notifier.sent[0]["state"] == "done"
    assert notifier.sent[0]["progress_pct"] == 50.0


def test_alerts_on_stalled(tmp_path):
    prog = tmp_path / "progress"
    _make_run(prog, "r4", updated_ago=1, progress_ago=30)
    notifier = RecordingNotifier()
    state = check(prog, notifier=notifier)
    assert state == "stalled"
    assert len(notifier.sent) == 1


def test_no_run_present_returns_none(tmp_path):
    notifier = RecordingNotifier()
    state = check(tmp_path / "progress", notifier=notifier)
    assert state is None
    assert notifier.sent == []
