"""TS-P0-003 — honest monitoring-window state.

The soak/monitoring window state is derived from PERSISTED evidence (store
meta keys) plus a liveness staleness rule, never from the last in-memory
claim. Consequence: a bridge that died while ARMED goes stale and any reader
computing the window state sees DOWN — a down bridge can never present as an
active soak window.

States:
  RUNNING      window started, liveness fresh, app_state ARMED, no
               interruption recorded since the last reset.
  DOWN         no window started, or liveness evidence missing/stale, or the
               persisted evidence is unreadable.
  INTERRUPTED  window started and bridge alive, but the window had a recorded
               gap (crash/downtime > stale threshold) or is currently not
               ARMED (disarmed/killed mid-window). Sticky across re-arm.
  RESET        the operator explicitly reset the window and no new window has
               started yet.

Reset policy (PROPOSED, pending Barış confirmation — see
docs/RUNTIME_BASELINE_CONTRACT.md cross-reference in the TS-P0 build report):
an interruption is sticky until an explicit ``reset_window`` call; re-arming
alone never clears it, so a window with a gap can never silently count as
continuous soak evidence. Downtime gaps shorter than ``stale_after_s`` do not
stamp an interruption (brief maintenance tolerance).
"""

from __future__ import annotations

from datetime import UTC, datetime

WINDOW_RUNNING = "RUNNING"
WINDOW_DOWN = "DOWN"
WINDOW_INTERRUPTED = "INTERRUPTED"
WINDOW_RESET = "RESET"

META_STARTED = "window_started_ts"
META_LAST_ALIVE = "window_last_alive_ts"
META_INTERRUPTED = "window_interrupted_ts"
META_RESET = "window_reset_ts"

DEFAULT_STALE_AFTER_S = 300.0


def _parse_ts(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=UTC)
    return parsed


def compute_window_state(
    *,
    app_state: str,
    started_ts: datetime | None,
    last_alive_ts: datetime | None,
    interrupted_ts: datetime | None,
    reset_ts: datetime | None,
    now: datetime,
    stale_after_s: float,
) -> str:
    """Pure decision function; order of rules is the contract.

    1. reset marker with no window started since -> RESET
    2. no window started -> DOWN
    3. liveness missing or older than stale_after_s -> DOWN
    4. interruption recorded -> INTERRUPTED
    5. ARMED -> RUNNING
    6. otherwise (alive but DISARMED/KILLED mid-window) -> INTERRUPTED
    """
    if reset_ts is not None and started_ts is None:
        return WINDOW_RESET
    if started_ts is None:
        return WINDOW_DOWN
    if last_alive_ts is None:
        return WINDOW_DOWN
    if (now - last_alive_ts).total_seconds() > stale_after_s:
        return WINDOW_DOWN
    if interrupted_ts is not None:
        return WINDOW_INTERRUPTED
    if app_state == "ARMED":
        return WINDOW_RUNNING
    return WINDOW_INTERRUPTED


def window_status(
    store,
    *,
    app_state: str,
    now: datetime | None = None,
    stale_after_s: float = DEFAULT_STALE_AFTER_S,
) -> dict:
    """Read-model block for /api/status. Fails safe: unreadable evidence is
    reported as DOWN with an explicit error, never as an active window."""
    now = now if now is not None else datetime.now(UTC)
    try:
        started = _parse_ts(store.get_meta(META_STARTED))
        last_alive = _parse_ts(store.get_meta(META_LAST_ALIVE))
        interrupted = _parse_ts(store.get_meta(META_INTERRUPTED))
        reset = _parse_ts(store.get_meta(META_RESET))
    except Exception:
        return {
            "state": WINDOW_DOWN,
            "started_ts": None,
            "last_alive_ts": None,
            "interrupted_ts": None,
            "reset_ts": None,
            "stale_after_s": stale_after_s,
            "error": "store_unreadable",
        }
    state = compute_window_state(
        app_state=app_state,
        started_ts=started,
        last_alive_ts=last_alive,
        interrupted_ts=interrupted,
        reset_ts=reset,
        now=now,
        stale_after_s=stale_after_s,
    )
    return {
        "state": state,
        "started_ts": started.isoformat() if started else None,
        "last_alive_ts": last_alive.isoformat() if last_alive else None,
        "interrupted_ts": interrupted.isoformat() if interrupted else None,
        "reset_ts": reset.isoformat() if reset else None,
        "stale_after_s": stale_after_s,
        "error": None,
    }


def record_window_start(store, now: datetime) -> None:
    """Called on ARM. Starts a window if none is active; clears a pending
    reset marker. Never clears a recorded interruption (sticky until
    reset_window)."""
    if not store.get_meta(META_STARTED):
        store.set_meta(META_STARTED, now.isoformat())
    store.set_meta(META_RESET, "")


def record_liveness(store, now: datetime) -> None:
    """Called on each successful reconcile cycle (the bridge's health pulse)."""
    store.set_meta(META_LAST_ALIVE, now.isoformat())


def detect_interruption(store, now: datetime, stale_after_s: float) -> bool:
    """Called once at engine startup. Stamps a sticky interruption when an
    active window has a liveness gap larger than stale_after_s. Returns True
    when a NEW interruption was stamped."""
    started = _parse_ts(store.get_meta(META_STARTED))
    if started is None:
        return False
    last_alive = _parse_ts(store.get_meta(META_LAST_ALIVE))
    gap_s = (
        (now - last_alive).total_seconds() if last_alive is not None else None
    )
    if gap_s is not None and gap_s <= stale_after_s:
        return False
    if store.get_meta(META_INTERRUPTED):
        return False  # already recorded
    store.set_meta(META_INTERRUPTED, now.isoformat())
    return True


def reset_window(store, now: datetime) -> None:
    """Explicit operator reset: the current window's evidence run ends; a new
    window only exists after the next record_window_start."""
    store.set_meta(META_RESET, now.isoformat())
    store.set_meta(META_STARTED, "")
    store.set_meta(META_INTERRUPTED, "")
    store.set_meta(META_LAST_ALIVE, "")
