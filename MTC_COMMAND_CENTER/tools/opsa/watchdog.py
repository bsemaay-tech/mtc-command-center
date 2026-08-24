"""OPS-A dead-man watchdog checker (WP-P0-26, local half — skeleton).

One-shot checker (designed to be scheduled externally; NO schedule is installed by
this package — host installation is gated behind G9): scans ``<state_dir>/*.hb.json``,
computes each heartbeat's age from its payload UTC timestamp (never mtime), and flags
silence beyond the configurable bound.

Per-id outcomes (distinct, never conflated — DESIGN_DEFECT_PATTERNS pattern 1):

- ``ok``               — fresh (age <= bound; small future skew <= tolerance tolerated)
- ``silent``           — heartbeat present but older than the bound   → ALERT
- ``missing``          — expected id (from --expect) has no file      → ALERT
- ``unreadable``       — file exists but cannot be read/parsed        → CHECK-FAILED
- ``bad_timestamp``    — readable but emitted_at missing/unparseable  → CHECK-FAILED
- ``clock_skew``       — emitted_at is far in the FUTURE              → CHECK-FAILED

Process exit code: 0 all ok · 2 any ALERT (silent/missing) · 3 any check-failure and
no alert. When both classes are present rc is 2 — the dead-man alert is the loudest
actionable signal; the full per-id truth is always on stdout either way. An empty
state dir (no heartbeats and no --expect) is CHECK-FAILED, not OK: a watchdog that
watches nothing cannot pass (fail-closed). An unparseable ``--now`` value is itself
a CHECK-FAILED record (rc 3), never an unhandled traceback.

Notifiers are pluggable: implement the ``Notifier`` interface and register it in
``NOTIFIERS``. This package ships ONLY ``local_log`` (append-only JSONL file) — the
phone-push notifier is deliberately absent until the owner picks a technology
(NOTIFIER_PROPOSAL.md) and the G9-gated host step authorizes outward delivery.
Alert payloads carry no secrets and no controls (plan §12.6.2(f)).

Every ``alert`` and ``check_failed`` outcome produces at least one notifier event.
Directory-level check-failures (missing state dir; nothing to watch; invalid
``--now``) carry no per-id events, so the checker delivers ONE synthetic
checker-level event (id ``_watchdog_check``, state ``check_failed``, the error
text) — otherwise rc 3 would be the only trace and the evidence-store-vanished
scenario would leave no alert record anywhere.

Usage:
    python watchdog.py --state-dir D --silence-seconds 900 [--expect id1,id2] \
                       [--notifier local_log] [--notifier-log PATH] \
                       [--state-file PATH] [--now ISO]

``--now`` (UTC ISO) is a test hook for deterministic drills; production runs omit it.
``--state-file`` enables notify-once-per-(id,state) de-duplication across checks.

Reuse record: one-shot poll + injected notifier + local-log notifier + notify-once
dedupe state file harvested from ``03_QUANTLENS/tools/run_watchdog.py``; UTC-Z age
math from ``progress_emitter._age_minutes``.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Protocol

sys.path.insert(0, str(Path(__file__).resolve().parent))
from opsa_common import (  # noqa: E402
    RC_ALERT, RC_CHECK_FAILED, RC_OK, WATCHDOG_EVENT_SCHEMA, append_jsonl,
    atomic_write_json, parse_utc_iso, utc_now,
)

#: Heartbeat timestamps this far in the future (seconds) are tolerated as clock jitter.
FUTURE_TOLERANCE_SECONDS = 60.0

ALERT_STATES = {"silent", "missing"}
CHECK_FAILED_STATES = {"unreadable", "bad_timestamp", "clock_skew"}


class Notifier(Protocol):
    """Pluggable delivery interface. Implementations must never crash the checker."""

    def notify(self, event: dict[str, Any]) -> None: ...


class LocalLogNotifier:
    """Append-only local JSONL log — the only notifier shipped in this package."""

    def __init__(self, log_path: Path):
        self.log_path = Path(log_path)

    def notify(self, event: dict[str, Any]) -> None:
        append_jsonl(self.log_path, event)


def _make_local_log_notifier(args, state_dir: Path) -> LocalLogNotifier:
    log_path = Path(args.notifier_log) if args.notifier_log else state_dir / "_watchdog_alerts.jsonl"
    return LocalLogNotifier(log_path)


#: Registry the --notifier flag selects from: name -> factory(args, state_dir).
#: The phone-push entry arrives post-G9, after the owner picks a technology
#: (NOTIFIER_PROPOSAL.md) — add the class + factory here and nothing else changes.
NOTIFIERS: dict[str, Any] = {"local_log": _make_local_log_notifier}


def classify(beat_path: Path, now, silence_seconds: float) -> tuple[str, dict[str, Any]]:
    """Classify one heartbeat file. Returns (state, detail-dict for the report line)."""
    try:
        payload = json.loads(beat_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return "unreadable", {"error": str(exc)}
    if not isinstance(payload, dict):
        return "unreadable", {"error": "payload is not a JSON object"}
    try:
        emitted_at = parse_utc_iso(payload["emitted_at"])
    except KeyError:
        return "bad_timestamp", {"error": "emitted_at missing"}
    except ValueError as exc:
        return "bad_timestamp", {"error": str(exc)}
    age = (now - emitted_at).total_seconds()
    if age < -FUTURE_TOLERANCE_SECONDS:
        return "clock_skew", {"emitted_at": payload["emitted_at"],
                              "age_seconds": round(age, 1)}
    if age > silence_seconds:
        return "silent", {"emitted_at": payload["emitted_at"],
                          "age_seconds": round(age, 1),
                          "bound_seconds": silence_seconds}
    return "ok", {"emitted_at": payload["emitted_at"], "age_seconds": round(age, 1)}


def check(state_dir: Path, silence_seconds: float, expect: list[str],
          now=None) -> dict[str, Any]:
    """Pure evaluation: returns the per-id result map + overall verdict, notifies no one."""
    now = now or utc_now()
    state_dir = Path(state_dir)
    results: dict[str, dict[str, Any]] = {}

    beat_files: dict[str, Path] = {}
    if not state_dir.is_dir():
        # The checker cannot read the heartbeat store at all — that is an inability to
        # evaluate (rc 3), NOT evidence that every process went silent. Could be the
        # watched host's death OR this checker's own mount problem; either way it is
        # reported loudly, never as a per-process silence claim and never as OK.
        return {"overall": "check_failed", "ids": {},
                "error": f"state dir does not exist: {state_dir}"}
    for path in sorted(state_dir.glob("*.hb.json")):
        beat_files[path.name[: -len(".hb.json")]] = path

    for beat_id, path in beat_files.items():
        state, detail = classify(path, now, silence_seconds)
        results[beat_id] = {"state": state, **detail}

    for beat_id in expect:
        if beat_id not in results:
            results[beat_id] = {"state": "missing", "expected": True}

    if not results:
        return {"overall": "check_failed", "ids": {},
                "error": "no heartbeat files found and no --expect ids given (watching nothing cannot be OK)"}

    states = {r["state"] for r in results.values()}
    if states & ALERT_STATES:
        overall = "alert"
    elif states & CHECK_FAILED_STATES:
        overall = "check_failed"
    else:
        overall = "ok"
    return {"overall": overall, "ids": results}


#: Synthetic notifier id for checker-level failures that produce no per-id events.
WATCHDOG_CHECK_ID = "_watchdog_check"


def _print_report(report: dict[str, Any]) -> None:
    for beat_id, detail in sorted(report["ids"].items()):
        print(f"{beat_id}: state={detail['state']} " +
              " ".join(f"{k}={v}" for k, v in detail.items() if k != "state"))
    if report.get("error"):
        print(f"error: {report['error']}", file=sys.stderr)
    print(json.dumps(report, ensure_ascii=False))


def _notify_outcome(report: dict[str, Any], notifier, state_file: Path | None,
                    checked_at, silence_seconds: float) -> None:
    """Deliver one notifier event per alerting/check-failed id.

    Directory-level check-failures (missing state dir; nothing to watch; invalid
    ``--now``) carry NO per-id events — without a synthetic event the loop below
    would iterate nothing and rc 3 would be the only trace of the outcome. So when
    the outcome produced no per-id events, exactly one checker-level event (id
    ``_watchdog_check``) carries the error text instead: every ``alert`` and
    ``check_failed`` outcome leaves at least one notifier event.
    """
    prev_seen: dict[str, str] = {}
    if state_file is not None and state_file.exists():
        try:
            prev_seen = {k: v for k, v in json.loads(
                state_file.read_text(encoding="utf-8")).items() if isinstance(v, str)}
        except (OSError, json.JSONDecodeError):
            prev_seen = {}  # unreadable dedupe state => treat as first sighting (fail loud)
    to_notify: dict[str, dict[str, Any]] = dict(report["ids"])
    if not to_notify:
        to_notify = {WATCHDOG_CHECK_ID: {"state": "check_failed",
                                         "error": report.get("error", "no events delivered")}}
    for beat_id, detail in sorted(to_notify.items()):
        state = detail["state"]
        if beat_id != WATCHDOG_CHECK_ID and state not in (ALERT_STATES | CHECK_FAILED_STATES):
            continue
        if state_file is not None and prev_seen.get(beat_id) == state:
            continue  # already notified for this (id, state); still reported on stdout
        notifier.notify({
            "schema": WATCHDOG_EVENT_SCHEMA, "id": beat_id, "state": state,
            "silence_bound_seconds": silence_seconds,
            "checked_at": checked_at.isoformat(timespec="seconds").replace("+00:00", "Z"),
            **{k: v for k, v in detail.items() if k not in ("state", "expected")},
        })
        prev_seen[beat_id] = state
    if state_file is not None:
        atomic_write_json(state_file, prev_seen)


def run_check(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="OPS-A dead-man watchdog checker (one-shot)")
    parser.add_argument("--state-dir", required=True, help="directory holding *.hb.json heartbeats")
    parser.add_argument("--silence-seconds", type=float, default=900.0,
                        help="silence bound in seconds (default 900 = 15 min per plan #39)")
    parser.add_argument("--expect", default="",
                        help="comma-separated ids that MUST have a heartbeat (missing => alert)")
    parser.add_argument("--notifier", default="local_log", choices=sorted(NOTIFIERS),
                        help="notifier factory (only local_log ships in this package)")
    parser.add_argument("--notifier-log", default=None,
                        help="notifier log file (default <state_dir>/_watchdog_alerts.jsonl)")
    parser.add_argument("--state-file", default=None,
                        help="optional dedupe state file: notify once per (id, state) transition")
    parser.add_argument("--now", default=None,
                        help="UTC ISO timestamp override (TEST HOOK for deterministic drills)")
    args = parser.parse_args(argv)

    state_dir = Path(args.state_dir)
    notifier = NOTIFIERS[args.notifier](args, state_dir)
    state_file = Path(args.state_file) if args.state_file else None
    now = utc_now()

    if args.now:
        try:
            now = parse_utc_iso(args.now)
        except ValueError as exc:
            # A bad --now is an inability to evaluate: check-failure record + notifier
            # event + rc 3 — never an unhandled traceback exiting rc 1.
            report = {"overall": "check_failed", "ids": {},
                      "error": f"invalid --now value: {exc}"}
            _print_report(report)
            _notify_outcome(report, notifier, state_file, now, args.silence_seconds)
            return RC_CHECK_FAILED

    expect = [x.strip() for x in args.expect.split(",") if x.strip()]
    report = check(state_dir, args.silence_seconds, expect, now=now)
    _print_report(report)

    if notifier is not None and report["overall"] in ("alert", "check_failed"):
        _notify_outcome(report, notifier, state_file, now, args.silence_seconds)

    if report["overall"] == "alert":
        return RC_ALERT
    if report["overall"] == "check_failed":
        return RC_CHECK_FAILED
    return RC_OK


if __name__ == "__main__":
    raise SystemExit(run_check(sys.argv[1:]))
