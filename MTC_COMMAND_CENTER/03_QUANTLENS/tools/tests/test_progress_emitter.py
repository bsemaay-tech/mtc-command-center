"""TDD tests for progress_emitter — the canonical run progress/heartbeat/event emitter."""
import json
import os
import sys
from pathlib import Path

import pytest

# emitter lives one dir up
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from progress_emitter import Emitter, NullEmitter, emitter_from_env  # noqa: E402


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
