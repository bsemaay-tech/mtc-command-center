"""OPS-A heartbeat emitter (WP-P0-26 dead-man watchdog, local half).

A watched process emits a heartbeat file ``<state_dir>/<id>.hb.json`` containing its
own UTC timestamp. The watchdog (watchdog.py) detects silence by reading that
timestamp — never the file's mtime, so a touched-but-not-written file cannot fake
liveness (plan #45 time discipline: staleness is measured against the payload's UTC
timestamp, not filesystem metadata).

Writes are atomic (tmp + os.replace), so a checker never observes a torn heartbeat.
An *unreadable* heartbeat is the checker's problem (check-failure there), not a fake
OK — this emitter only ever writes complete files.

There is deliberately NO "stopped"/"final" marker: the dead-man contract is silence
beyond the bound ⇒ alert, regardless of why the beats stopped (crash, kill, hang,
host death). A graceful-stop marker would let a killed process look tidy.

Usage:
    python heartbeat.py emit  --state-dir D --id NAME [--note TEXT]   # one beat
    python heartbeat.py loop  --state-dir D --id NAME --interval SECONDS \
                              [--count N] [--note TEXT]               # beat until count/kill

``loop`` exits without a final marker when its count is reached or it is killed
(Ctrl-C is swallowed and NOT logged as a beat) — that stop is exactly the silence the
watchdog must catch.

Reuse record: atomic-write + UTC-Z timestamp patterns harvested from
``03_QUANTLENS/tools/progress_emitter.py``.
"""
from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from opsa_common import (  # noqa: E402
    HEARTBEAT_SCHEMA, RC_CHECK_FAILED, atomic_write_json, require_non_empty_string,
    resolve_confined_path, utc_now_iso,
)


def emit(state_dir: Path, beat_id: str, seq: int, note: str | None = None) -> Path:
    beat_id = require_non_empty_string(beat_id, "id", "heartbeat")
    path = resolve_confined_path(state_dir, f"{beat_id}.hb.json")
    atomic_write_json(path, {
        "schema": HEARTBEAT_SCHEMA,
        "id": beat_id,
        "seq": seq,
        "emitted_at": utc_now_iso(),
        "pid": _pid(),
        **({"note": note} if note else {}),
    })
    return path


def _pid() -> int:
    import os
    return os.getpid()


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="OPS-A heartbeat emitter (dead-man watchdog source)")
    sub = parser.add_subparsers(dest="command", required=True)

    def common(p):
        p.add_argument("--state-dir", required=True, help="directory holding heartbeat files")
        p.add_argument("--id", required=True, help="watched-process id (file name stem)")
        p.add_argument("--note", default=None, help="optional free-text note carried in the beat")

    e = sub.add_parser("emit", help="write one heartbeat")
    common(e)

    l = sub.add_parser("loop", help="emit every --interval seconds until --count or killed")
    common(l)
    l.add_argument("--interval", type=float, default=60.0, help="seconds between beats")
    l.add_argument("--count", type=int, default=0, help="stop after N beats (0 = forever)")

    args = parser.parse_args(argv)
    state_dir = Path(args.state_dir)
    state_dir.mkdir(parents=True, exist_ok=True)

    if args.command == "emit":
        try:
            path = emit(state_dir, args.id, seq=1, note=args.note)
        except ValueError as exc:
            print(f"error: unsafe heartbeat id: {exc}", file=sys.stderr)
            return RC_CHECK_FAILED
        print(f"heartbeat written: {path}")
        return 0

    seq = 0
    try:
        while args.count == 0 or seq < args.count:
            seq += 1
            try:
                path = emit(state_dir, args.id, seq=seq, note=args.note)
            except ValueError as exc:
                print(f"error: unsafe heartbeat id: {exc}", file=sys.stderr)
                return RC_CHECK_FAILED
            print(f"beat seq={seq} -> {path}", flush=True)
            if args.count != 0 and seq >= args.count:
                break
            time.sleep(args.interval)
    except KeyboardInterrupt:
        # Swallowed on purpose: stopping silently IS the dead-man condition.
        return 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
