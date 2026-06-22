"""MTC Run Emitter Supervisor — observe a run, guarantee liveness + terminal state.

Launches a backtest command with the emitter enabled, writes a process-liveness file
every tick (independent of whether the runner is mid-compute), and on child exit writes
a terminal status.json. The supervisor's killer feature: a crashed / killed runner that
never called Emitter.finished() still gets an honest status.json (result=fail, exit_code),
which the in-runner emitter alone cannot guarantee.

It does NOT rewrite the runner's heartbeat.json (no shared-file race): the runner owns
heartbeat/events, the supervisor owns supervisor.json + the fallback terminal status.

Usage:
    python run_emitter_supervisor.py <progress_root> <run_id> -- <command> [args...]
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import threading
import time
from datetime import datetime, timezone
from pathlib import Path

# import the emitter's atomic writer + schema constant
sys.path.insert(0, str(Path(__file__).resolve().parent))
from progress_emitter import Emitter, _atomic_write_json, STATUS_SCHEMA, _utc_now  # noqa: E402


# Map the sweep runner's native run_status.json "status" -> canonical terminal hint.
_NATIVE_TERMINAL = {"completed": "ok", "time_budget_reached": "ok", "failed": "fail"}


def republish_native_status(emitter, status_file, total=None):
    """Translate the runner's EXISTING native run_status.json into the canonical contract.

    Reads ``completed_evaluations`` / ``failed_evaluations`` / ``status`` (already written by
    run_quantlens_overnight_research.py) and forwards them through the emitter. Touches no
    engine code. Returns a terminal hint ("ok"/"fail") or "running"/None.
    """
    status_file = Path(status_file)
    if not status_file.exists():
        return None
    try:
        data = json.loads(status_file.read_text(encoding="utf-8"))
    except Exception:
        return None

    completed = data.get("completed_evaluations")
    failed = data.get("failed_evaluations")
    if completed is not None:
        emitter.progress(current=int(completed), total=total)
    if failed is not None:
        emitter.counters(failed=int(failed))

    native = data.get("status")
    if native in _NATIVE_TERMINAL:
        return _NATIVE_TERMINAL[native]
    return "running" if native else None


def _write_liveness(run_dir: Path, run_id: str, child_pid: int) -> None:
    _atomic_write_json(run_dir / "supervisor.json", {
        "schema": "mtc.run_supervisor/v1",
        "run_id": run_id,
        "child_pid": child_pid,
        "alive_at": _utc_now(),
    })


def supervise(progress_root, run_id: str, cmd_argv: list[str], tick_seconds: float = 30.0,
              status_file=None, status_total=None) -> int:
    """Run cmd_argv with the emitter enabled; tick liveness; guarantee terminal status.

    If ``status_file`` is given, the supervisor owns a canonical Emitter and republishes the
    runner's native run_status.json (progress + terminal) into the contract WITHOUT the engine
    emitting anything itself. Otherwise it only proves liveness + fills a terminal status if the
    child never wrote one (e.g. a crash).
    """
    root = Path(progress_root)
    run_dir = root / run_id
    run_dir.mkdir(parents=True, exist_ok=True)

    env = dict(os.environ)
    env["MTC_RUN_EMITTER"] = "1"
    env["MTC_RUN_ID"] = run_id
    env["MTC_PROGRESS_ROOT"] = str(root)

    emitter = Emitter(root, run_id, "supervisor") if status_file is not None else None
    if emitter is not None:
        emitter.run_started(total=int(status_total) if status_total is not None else 0)

    started_at = _utc_now()
    proc = subprocess.Popen(cmd_argv, env=env)
    _write_liveness(run_dir, run_id, proc.pid)

    stop = threading.Event()

    def _ticker() -> None:
        while not stop.wait(tick_seconds):
            _write_liveness(run_dir, run_id, proc.pid)
            if emitter is not None:
                republish_native_status(emitter, status_file, total=status_total)

    ticker = threading.Thread(target=_ticker, daemon=True)
    ticker.start()

    exit_code = proc.wait()
    stop.set()
    _write_liveness(run_dir, run_id, proc.pid)

    if emitter is not None:
        # Deterministic final republish (independent of tick timing) + terminal status.
        hint = republish_native_status(emitter, status_file, total=status_total)
        if hint in ("ok", "fail"):
            result = hint
        else:
            result = "ok" if exit_code == 0 else "fail"
        emitter.finished(result, summary={"native_status_file": str(status_file)}, exit_code=exit_code)
        return exit_code

    # No status-file mode: only fill the gap if the runner did not write its own status.json.
    status_path = run_dir / "status.json"
    if not status_path.exists():
        _atomic_write_json(status_path, {
            "schema": STATUS_SCHEMA,
            "run_id": run_id,
            "runner": "supervisor",
            "result": "ok" if exit_code == 0 else "fail",
            "exit_code": int(exit_code),
            "started_at": started_at,
            "finished_at": _utc_now(),
            "summary": {"note": "terminal state recorded by supervisor (runner did not finish())"},
            "report_path": None,
        })
    return exit_code


def _parse_and_run(argv: list[str]) -> int:
    usage = ("usage: run_emitter_supervisor.py <progress_root> <run_id> "
             "[--status-file PATH] [--status-total N] [--tick SECONDS] -- <command...>")
    if len(argv) < 3:
        print(usage, file=sys.stderr)
        return 2
    root, run_id = argv[0], argv[1]
    rest = argv[2:]
    status_file = None
    status_total = None
    tick = 30.0
    # consume leading options up to the "--" separator
    while rest and rest[0] != "--":
        opt = rest.pop(0)
        if opt == "--status-file":
            status_file = rest.pop(0)
        elif opt == "--status-total":
            status_total = int(rest.pop(0))
        elif opt == "--tick":
            tick = float(rest.pop(0))
        else:
            print(f"error: unknown option {opt}\n{usage}", file=sys.stderr)
            return 2
    if rest and rest[0] == "--":
        rest = rest[1:]
    if not rest:
        print("error: no command given after --", file=sys.stderr)
        return 2
    return supervise(root, run_id, rest, tick_seconds=tick,
                     status_file=status_file, status_total=status_total)


if __name__ == "__main__":
    raise SystemExit(_parse_and_run(sys.argv[1:]))
