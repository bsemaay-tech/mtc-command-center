"""MTC Run Watchdog — one-shot consumer of the run progress contract (Phase 5).

Designed to be invoked on a schedule by an external automation (n8n / Task Scheduler / cron):
each call reads progress/_latest.json, derives the run state, and fires a notification ONCE per
(run_id, state) transition into an alert state (done / failed / stalled / dead). De-dupe state is
kept in progress/_watchdog_state.json so repeated polls don't re-notify.

No agent needs to stay open. Notifications default to a local log file (safe, no outward action);
an optional webhook is sent only when --webhook-url is supplied (opt-in, e.g. n8n / Telegram).

Usage:
    python run_watchdog.py <progress_root> [--webhook-url URL] [--log FILE]
Exit code: 0 always (state is reported on stdout); designed to be polled.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

sys.path.insert(0, str(Path(__file__).resolve().parent))
from progress_emitter import derive_run_state, _atomic_write_json  # noqa: E402

ALERT_STATES = {"done", "failed", "stalled", "dead"}


def _load_json(path: Path) -> dict | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def _build_payload(run_id: str, state: str, heartbeat: dict, status: dict | None) -> dict[str, Any]:
    progress = heartbeat.get("progress") or {}
    return {
        "run_id": run_id,
        "state": state,
        "runner": heartbeat.get("runner"),
        "phase": heartbeat.get("phase"),
        "progress_pct": progress.get("pct"),
        "progress_current": progress.get("current"),
        "progress_total": progress.get("total"),
        "result": (status or {}).get("result"),
        "exit_code": (status or {}).get("exit_code"),
        "notified_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    }


def check(progress_root, notifier: Callable[[dict], None] | None = None,
          now: datetime | None = None) -> str | None:
    """Read the current run, derive state, notify once per (run_id, state) alert transition.

    Returns the derived state, or None if no run is present. Pure w.r.t. notification side-effect:
    the notifier callable is injected (defaults to a no-op when omitted, for read-only checks).
    """
    root = Path(progress_root)
    now = now or datetime.now(timezone.utc)
    latest = _load_json(root / "_latest.json")
    if not latest or not latest.get("run_id"):
        return None
    run_id = latest["run_id"]
    run_dir = root / run_id

    heartbeat = _load_json(run_dir / "heartbeat.json")
    if heartbeat is None:
        return None
    status = _load_json(run_dir / "status.json")

    state = derive_run_state(heartbeat, status, now)

    if notifier is not None and state in ALERT_STATES:
        dedupe_path = root / "_watchdog_state.json"
        seen = _load_json(dedupe_path) or {}
        if seen.get("run_id") != run_id or seen.get("state") != state:
            notifier(_build_payload(run_id, state, heartbeat, status))
            _atomic_write_json(dedupe_path, {
                "run_id": run_id, "state": state,
                "notified_at": now.isoformat().replace("+00:00", "Z"),
            })
    return state


def make_notifier(log_path: Path, webhook_url: str | None) -> Callable[[dict], None]:
    """Local-log notifier (always) + optional webhook POST (only if a URL is configured)."""
    def _notify(payload: dict) -> None:
        log_path.parent.mkdir(parents=True, exist_ok=True)
        with open(log_path, "a", encoding="utf-8") as handle:
            handle.write(json.dumps(payload, ensure_ascii=False, sort_keys=True) + "\n")
        if webhook_url:
            import urllib.request
            data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(webhook_url, data=data,
                                         headers={"Content-Type": "application/json"})
            try:
                urllib.request.urlopen(req, timeout=10).read()
            except Exception as exc:  # never let a webhook failure crash the poll
                with open(log_path, "a", encoding="utf-8") as handle:
                    handle.write(json.dumps({"webhook_error": str(exc), "run_id": payload.get("run_id")}) + "\n")
    return _notify


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="MTC run watchdog (one-shot poll)")
    parser.add_argument("progress_root")
    parser.add_argument("--webhook-url", default=None)
    parser.add_argument("--log", default=None, help="notification log file (default: <root>/_watchdog_notifications.log)")
    args = parser.parse_args(argv)

    root = Path(args.progress_root)
    log_path = Path(args.log) if args.log else root / "_watchdog_notifications.log"
    notifier = make_notifier(log_path, args.webhook_url)
    state = check(root, notifier=notifier)
    print(state if state is not None else "no-run")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
