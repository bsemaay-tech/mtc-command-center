"""TDD tests for progress_emitter — the canonical run progress/heartbeat/event emitter."""
import json
import os
import sys
from pathlib import Path

import pytest

# emitter lives one dir up
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from datetime import datetime, timedelta, timezone  # noqa: E402

from progress_emitter import Emitter, NullEmitter, emitter_from_env, derive_run_state  # noqa: E402


def _ts_ago(minutes: float) -> str:
    return (datetime.now(timezone.utc) - timedelta(minutes=minutes)).isoformat().replace("+00:00", "Z")


def _now() -> datetime:
    return datetime.now(timezone.utc)


def test_derive_state_done_and_failed_from_status():
    hb = {"updated_at": _ts_ago(0.1), "last_progress_at": _ts_ago(0.1)}
    assert derive_run_state(hb, {"result": "ok"}, _now()) == "done"
    assert derive_run_state(hb, {"result": "fail"}, _now()) == "failed"


def test_derive_state_running_stalled_dead_from_timestamps():
    assert derive_run_state({"updated_at": _ts_ago(0.1), "last_progress_at": _ts_ago(0.1)}, None, _now()) == "running"
    assert derive_run_state({"updated_at": _ts_ago(1), "last_progress_at": _ts_ago(30)}, None, _now()) == "stalled"
    assert derive_run_state({"updated_at": _ts_ago(60), "last_progress_at": _ts_ago(60)}, None, _now()) == "dead"


def _read_json(p: Path) -> dict:
    return json.loads(p.read_text(encoding="utf-8"))


def _events(run_dir: Path) -> list[dict]:
    lines = (run_dir / "events.jsonl").read_text(encoding="utf-8").splitlines()
    return [json.loads(ln) for ln in lines if ln.strip()]


def test_run_started_writes_heartbeat_latest_and_first_event(tmp_path):
    e = Emitter(tmp_path, run_id="r1", runner="unit")
    e.run_started(total=10, meta={"symbols": ["BTCUSDT"]})

    run_dir = tmp_path / "r1"
    hb = _read_json(run_dir / "heartbeat.json")
    assert hb["schema"] == "mtc.run_progress/v1"
    assert hb["run_id"] == "r1"
    assert hb["runner"] == "unit"
    assert hb["started_at"] and hb["updated_at"]
    assert hb["progress"]["total"] == 10

    latest = _read_json(tmp_path / "_latest.json")
    assert latest["run_id"] == "r1"

    evs = _events(run_dir)
    assert evs[0]["seq"] == 1
    assert evs[0]["type"] == "run_started"


def test_progress_updates_pct_and_last_progress_and_seq(tmp_path):
    e = Emitter(tmp_path, run_id="r2", runner="unit")
    e.run_started(total=200)
    e.progress(current=50, total=200)

    hb = _read_json(tmp_path / "r2" / "heartbeat.json")
    assert hb["progress"]["current"] == 50
    assert hb["progress"]["pct"] == 25.0
    assert hb["last_progress_at"]  # set on real forward progress
    # seq increments: run_started=1, progress=2
    assert hb["last_event_seq"] == 2


def test_events_jsonl_is_append_only_with_monotonic_seq(tmp_path):
    e = Emitter(tmp_path, run_id="r3", runner="unit")
    e.run_started(total=3)
    e.phase("cpcv")
    e.event("error", {"msg": "boom"})
    e.progress(current=1, total=3)

    seqs = [ev["seq"] for ev in _events(tmp_path / "r3")]
    assert seqs == [1, 2, 3, 4]


def test_atomic_writes_leave_no_tmp_files(tmp_path):
    e = Emitter(tmp_path, run_id="r4", runner="unit")
    e.run_started(total=5)
    e.progress(current=2, total=5)
    e.finished("ok", summary={"completed": 5})

    leftovers = list((tmp_path / "r4").glob("*.tmp")) + list(tmp_path.glob("*.tmp"))
    assert leftovers == []


def test_finished_writes_status_json(tmp_path):
    e = Emitter(tmp_path, run_id="r5", runner="unit")
    e.run_started(total=5)
    e.finished("fail", summary={"completed": 2}, exit_code=1)

    st = _read_json(tmp_path / "r5" / "status.json")
    assert st["schema"] == "mtc.run_status/v1"
    assert st["result"] == "fail"
    assert st["exit_code"] == 1
    assert st["finished_at"]


def test_null_emitter_writes_nothing(tmp_path):
    e = NullEmitter()
    e.run_started(total=5)
    e.progress(current=1, total=5)
    e.finished("ok")
    assert list(tmp_path.iterdir()) == []


def test_emitter_from_env_gates_on_flag(tmp_path, monkeypatch):
    monkeypatch.delenv("MTC_RUN_EMITTER", raising=False)
    assert isinstance(emitter_from_env(tmp_path, "x", "unit"), NullEmitter)

    monkeypatch.setenv("MTC_RUN_EMITTER", "1")
    assert isinstance(emitter_from_env(tmp_path, "x", "unit"), Emitter)
