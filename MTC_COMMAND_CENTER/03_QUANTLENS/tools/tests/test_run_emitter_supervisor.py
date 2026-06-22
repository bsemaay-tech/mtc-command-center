"""TDD tests for run_emitter_supervisor — terminal-state + liveness guarantee around a run."""
import json
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TOOLS))

from run_emitter_supervisor import supervise, republish_native_status  # noqa: E402
from progress_emitter import Emitter  # noqa: E402


def _emit_finished_ok_child() -> list[str]:
    code = (
        "import os,sys;"
        f"sys.path.insert(0, r'{TOOLS}');"
        "from progress_emitter import Emitter;"
        "e=Emitter(os.environ['MTC_PROGRESS_ROOT'], os.environ['MTC_RUN_ID'], 'fake');"
        "e.run_started(total=1); e.progress(1,1); e.finished('ok');"
    )
    return [sys.executable, "-c", code]


def _crash_child_without_finishing() -> list[str]:
    return [sys.executable, "-c", "import sys; sys.exit(1)"]


def _read_json(p: Path) -> dict:
    return json.loads(p.read_text(encoding="utf-8"))


def test_supervisor_records_ok_terminal_status(tmp_path):
    rc = supervise(tmp_path, "sok", _emit_finished_ok_child(), tick_seconds=0.05)
    assert rc == 0
    st = _read_json(tmp_path / "sok" / "status.json")
    assert st["result"] == "ok"


def test_supervisor_writes_fail_status_when_child_crashes_without_finishing(tmp_path):
    rc = supervise(tmp_path, "scrash", _crash_child_without_finishing(), tick_seconds=0.05)
    assert rc == 1
    st = _read_json(tmp_path / "scrash" / "status.json")
    assert st["result"] == "fail"
    assert st["exit_code"] == 1


def test_supervisor_does_not_overwrite_runner_terminal_status(tmp_path):
    supervise(tmp_path, "sown", _emit_finished_ok_child(), tick_seconds=0.05)
    st = _read_json(tmp_path / "sown" / "status.json")
    # runner's own finished('ok') stays authoritative even though child exited 0
    assert st["result"] == "ok"
    assert st["runner"] == "fake"


def test_supervisor_writes_liveness_file(tmp_path):
    supervise(tmp_path, "slive", _emit_finished_ok_child(), tick_seconds=0.05)
    sup = _read_json(tmp_path / "slive" / "supervisor.json")
    assert sup["run_id"] == "slive"
    assert sup["child_pid"]
    assert sup["alive_at"]


def test_republish_native_status_maps_progress_and_counters(tmp_path):
    native = tmp_path / "run_status.json"
    native.write_text(json.dumps({
        "status": "running", "completed_evaluations": 120, "failed_evaluations": 3,
    }), encoding="utf-8")

    e = Emitter(tmp_path, "rn", "unit")
    e.run_started(total=200)
    state = republish_native_status(e, native, total=200)

    hb = _read_json(tmp_path / "rn" / "heartbeat.json")
    assert hb["progress"]["current"] == 120
    assert hb["progress"]["pct"] == 60.0
    assert hb["counters"]["failed"] == 3
    assert state == "running"


def test_republish_native_status_maps_terminal_states(tmp_path):
    native = tmp_path / "s.json"
    e = Emitter(tmp_path, "rt", "unit")
    e.run_started(total=10)

    native.write_text(json.dumps({"status": "completed", "completed_evaluations": 10}), encoding="utf-8")
    assert republish_native_status(e, native, total=10) == "ok"

    native.write_text(json.dumps({"status": "failed", "completed_evaluations": 4}), encoding="utf-8")
    assert republish_native_status(e, native, total=10) == "fail"

    native.write_text(json.dumps({"status": "time_budget_reached", "completed_evaluations": 8}), encoding="utf-8")
    assert republish_native_status(e, native, total=10) == "ok"


def test_republish_native_status_missing_file_is_noop(tmp_path):
    e = Emitter(tmp_path, "rm", "unit")
    e.run_started(total=10)
    assert republish_native_status(e, tmp_path / "nope.json", total=10) is None


def test_supervisor_status_file_mode_publishes_canonical_progress_and_terminal(tmp_path):
    native = tmp_path / "native_run_status.json"
    child = [sys.executable, "-c",
             "import json,sys;"
             f"open(r'{native}','w').write(json.dumps("
             "{'status':'completed','completed_evaluations':42,'failed_evaluations':0}));"
             "sys.exit(0)"]
    rc = supervise(tmp_path, "swf", child, tick_seconds=0.05,
                   status_file=native, status_total=100)
    assert rc == 0
    hb = _read_json(tmp_path / "swf" / "heartbeat.json")
    assert hb["progress"]["current"] == 42
    assert hb["progress"]["pct"] == 42.0
    st = _read_json(tmp_path / "swf" / "status.json")
    assert st["result"] == "ok"
