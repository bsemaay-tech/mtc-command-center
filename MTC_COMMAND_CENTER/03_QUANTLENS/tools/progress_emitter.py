"""MTC Run Progress Emitter — canonical, stable progress/heartbeat/event contract.

Single source of truth for what a long backtest run writes so an external watchdog
(Phase 5 = n8n) can detect finished / failed / stalled and report % progress WITHOUT
keeping an AI agent open, and WITHOUT touching parity-sensitive engine code.

Layout written under <progress_root>/:
    <run_id>/heartbeat.json   (mtc.run_progress/v1, overwritten each update, atomic)
    <run_id>/events.jsonl     (append-only, one JSON object per line, monotonic seq)
    <run_id>/status.json      (mtc.run_status/v1, written once at terminal, atomic)
    _latest.json              (stable pointer -> {"run_id": ...})

Env-gated: emitter_from_env() returns a real Emitter only when MTC_RUN_EMITTER=1,
otherwise a NullEmitter (all methods no-op) so opted-out runs are byte-identical.

CLI (for shell / PowerShell runners):
    python progress_emitter.py <root> <run_id> run-started --runner R --total N
    python progress_emitter.py <root> <run_id> progress --current C --total N
    python progress_emitter.py <root> <run_id> event --type T --data '{"k":"v"}'
    python progress_emitter.py <root> <run_id> finished --result ok|fail [--exit-code N]
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

PROGRESS_SCHEMA = "mtc.run_progress/v1"
STATUS_SCHEMA = "mtc.run_status/v1"
ENV_FLAG = "MTC_RUN_EMITTER"


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _age_minutes(ts_str, now: datetime) -> float | None:
    if not ts_str:
        return None
    try:
        ts = datetime.fromisoformat(str(ts_str).replace("Z", "+00:00"))
        return (now - ts).total_seconds() / 60
    except Exception:
        return None


def derive_run_state(heartbeat: dict[str, Any], status: dict[str, Any] | None, now: datetime,
                     alive_minutes: float = 15.0, stall_minutes: float = 15.0) -> str:
    """Pure state machine shared by the dashboard reader and the watchdog.

    done/failed when a terminal status.json exists; otherwise dead (process gone) /
    stalled (alive but no forward progress) / running, from the two heartbeat timestamps.
    """
    if status is not None:
        return "done" if status.get("result") == "ok" else "failed"
    proc_age = _age_minutes(heartbeat.get("updated_at"), now)
    progress_age = _age_minutes(heartbeat.get("last_progress_at"), now)
    if proc_age is None or proc_age >= alive_minutes:
        return "dead"
    if progress_age is not None and progress_age >= stall_minutes:
        return "stalled"
    return "running"


def _atomic_write_json(path: Path, payload: dict[str, Any]) -> None:
    """Write JSON via tmp file + os.replace so readers never see a torn file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(dir=str(path.parent), prefix=path.name + ".", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, ensure_ascii=False, sort_keys=True)
        os.replace(tmp_name, path)
    except BaseException:
        if os.path.exists(tmp_name):
            os.remove(tmp_name)
        raise


class Emitter:
    """Real emitter. Owns one run's heartbeat/events/status files."""

    def __init__(self, progress_root: Path | str, run_id: str, runner: str) -> None:
        self.root = Path(progress_root)
        self.run_id = run_id
        self.runner = runner
        self.run_dir = self.root / run_id
        self.heartbeat_path = self.run_dir / "heartbeat.json"
        self.events_path = self.run_dir / "events.jsonl"
        self.status_path = self.run_dir / "status.json"
        self.latest_path = self.root / "_latest.json"
        self._seq = 0
        self._started_at: str | None = None
        self._started_monotonic: float | None = None
        self._last_progress_at: str | None = None
        self._phase: str | None = None
        self._progress = {"current": 0, "total": 0, "pct": 0.0, "eta_seconds": None}
        self._counters: dict[str, Any] = {}

    # -- public API -------------------------------------------------------
    def run_started(self, total: int = 0, meta: dict[str, Any] | None = None) -> None:
        self._started_at = _utc_now()
        self._started_monotonic = time.monotonic()
        self._progress["total"] = int(total)
        self._append_event("run_started", {"total": int(total), "meta": meta or {}})
        self._write_heartbeat()
        _atomic_write_json(self.latest_path, {"run_id": self.run_id, "updated_at": _utc_now()})

    def phase(self, name: str) -> None:
        self._phase = name
        self._append_event("phase_started", {"phase": name})
        self._write_heartbeat()

    def progress(self, current: int, total: int | None = None) -> None:
        if total is not None:
            self._progress["total"] = int(total)
        self._progress["current"] = int(current)
        tot = self._progress["total"]
        self._progress["pct"] = round(current / tot * 100, 1) if tot else 0.0
        self._progress["eta_seconds"] = self._eta(current, tot)
        self._last_progress_at = _utc_now()
        self._append_event("progress", {"current": int(current), "total": tot})
        self._write_heartbeat()

    def counters(self, **kv: Any) -> None:
        self._counters.update(kv)
        self._write_heartbeat()

    def event(self, type: str, data: dict[str, Any] | None = None) -> None:
        self._append_event(type, data or {})
        self._write_heartbeat()

    def finished(self, result: str, summary: dict[str, Any] | None = None,
                 exit_code: int = 0, report_path: str | None = None) -> None:
        self._append_event("run_finished", {"result": result, "exit_code": int(exit_code)})
        self._write_heartbeat(final_state=result)
        _atomic_write_json(self.status_path, {
            "schema": STATUS_SCHEMA,
            "run_id": self.run_id,
            "runner": self.runner,
            "result": result,
            "exit_code": int(exit_code),
            "finished_at": _utc_now(),
            "summary": summary or {},
            "report_path": report_path,
        })

    # -- internals --------------------------------------------------------
    def _eta(self, current: int, total: int) -> float | None:
        if not current or not total or self._started_monotonic is None or current >= total:
            return None
        elapsed = time.monotonic() - self._started_monotonic
        per = elapsed / current
        return round(per * (total - current), 1)

    def _append_event(self, type: str, data: dict[str, Any]) -> None:
        self._seq += 1
        self.events_path.parent.mkdir(parents=True, exist_ok=True)
        line = json.dumps({"seq": self._seq, "ts": _utc_now(), "type": type, "data": data},
                          ensure_ascii=False, sort_keys=True)
        with open(self.events_path, "a", encoding="utf-8") as handle:
            handle.write(line + "\n")

    def _write_heartbeat(self, final_state: str | None = None) -> None:
        _atomic_write_json(self.heartbeat_path, {
            "schema": PROGRESS_SCHEMA,
            "run_id": self.run_id,
            "runner": self.runner,
            "pid": os.getpid(),
            "started_at": self._started_at,
            "updated_at": _utc_now(),
            "last_progress_at": self._last_progress_at,
            "phase": self._phase,
            "state": final_state or "running",
            "progress": dict(self._progress),
            "counters": dict(self._counters),
            "last_event_seq": self._seq,
        })


class NullEmitter:
    """No-op emitter used when MTC_RUN_EMITTER is not set. Same API, writes nothing."""

    def run_started(self, *a: Any, **k: Any) -> None: ...
    def phase(self, *a: Any, **k: Any) -> None: ...
    def progress(self, *a: Any, **k: Any) -> None: ...
    def counters(self, *a: Any, **k: Any) -> None: ...
    def event(self, *a: Any, **k: Any) -> None: ...
    def finished(self, *a: Any, **k: Any) -> None: ...


def emitter_from_env(progress_root: Path | str, run_id: str, runner: str):
    """Return a real Emitter only when MTC_RUN_EMITTER=1, else a NullEmitter."""
    if os.environ.get(ENV_FLAG) == "1":
        return Emitter(progress_root, run_id, runner)
    return NullEmitter()


# -- CLI (for non-Python runners) -----------------------------------------
def _cli(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="MTC run progress emitter CLI")
    parser.add_argument("root")
    parser.add_argument("run_id")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_start = sub.add_parser("run-started")
    p_start.add_argument("--runner", default="cli")
    p_start.add_argument("--total", type=int, default=0)

    p_prog = sub.add_parser("progress")
    p_prog.add_argument("--runner", default="cli")
    p_prog.add_argument("--current", type=int, required=True)
    p_prog.add_argument("--total", type=int, default=None)

    p_evt = sub.add_parser("event")
    p_evt.add_argument("--runner", default="cli")
    p_evt.add_argument("--type", required=True)
    p_evt.add_argument("--data", default="{}")

    p_fin = sub.add_parser("finished")
    p_fin.add_argument("--runner", default="cli")
    p_fin.add_argument("--result", required=True, choices=["ok", "fail"])
    p_fin.add_argument("--exit-code", type=int, default=0)

    args = parser.parse_args(argv)
    e = Emitter(args.root, args.run_id, getattr(args, "runner", "cli"))
    # CLI is stateless across calls; seq restarts but events.jsonl append preserves history.
    if args.cmd == "run-started":
        e.run_started(total=args.total)
    elif args.cmd == "progress":
        e.progress(current=args.current, total=args.total)
    elif args.cmd == "event":
        e.event(args.type, json.loads(args.data))
    elif args.cmd == "finished":
        e.finished(args.result, exit_code=args.exit_code)
    return 0


if __name__ == "__main__":
    raise SystemExit(_cli(sys.argv[1:]))
