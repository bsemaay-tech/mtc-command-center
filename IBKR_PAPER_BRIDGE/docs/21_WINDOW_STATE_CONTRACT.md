# 21 — Honest Monitoring-Window State (TS-P0-003)

Module: `bridge/engine/window.py`. Read-model surface: `status()["window"]`
(engine) and the `window` key in `init_runtime_state`'s `bridge_status`
(engine-less app). Tests: `tests/test_window_state.py`.

## Problem

Before this change the monitoring/soak window had no explicit state: a
dashboard or evidence report reading the last persisted `app_state == ARMED`
could present a DEAD bridge as an active soak window (see
`19_P2_RECONNECT_INCIDENT_2026-07-13.md`).

## Model

Window state is DERIVED from persisted evidence + a liveness staleness rule —
never from an in-memory claim:

| Meta key | Written by | Meaning |
| --- | --- | --- |
| `window_started_ts` | `record_window_start` (on ARM, if no window active) | Window exists since this instant. |
| `window_last_alive_ts` | `record_liveness` (startup reconcile + every successful reconcile cycle) | Bridge health pulse. |
| `window_interrupted_ts` | `detect_interruption` (engine startup, gap > `stale_after_s`) | Sticky gap record. |
| `window_reset_ts` | `reset_window` (explicit operator action; no HTTP surface yet) | Evidence run explicitly restarted. |

Decision order (`compute_window_state`, pure function — order is the
contract):

1. reset marker and no window started since → **RESET**
2. no window started → **DOWN**
3. liveness missing, future-dated, or age > `stale_after_s` (default 300s) → **DOWN**
4. interruption recorded → **INTERRUPTED**
5. `app_state == ARMED` → **RUNNING**
6. otherwise (alive but DISARMED/KILLED mid-window) → **INTERRUPTED**

**Invariant (tested exhaustively):** RUNNING requires fresh liveness AND
ARMED AND no recorded interruption — a down bridge can never present as an
active soak window. Unreadable store evidence reports DOWN with
`error: store_unreadable`, never a fabricated active state. Any non-empty
persisted window timestamp that cannot be parsed reports DOWN with
`error: invalid_meta:<meta-key>`. Future-dated liveness reports DOWN with
`error: future_liveness`; exact-threshold liveness remains fresh.

## Reset policy — CONFIRMED by Barış, 2026-07-20 (D018)

- An interruption is **sticky**: re-arming alone never clears it. Only an
  explicit `reset_window` call starts a clean evidence run. Rationale: a
  window with a gap must never silently count as continuous soak evidence.
- Downtime gaps ≤ `stale_after_s` (300s) do not stamp an interruption
  (brief-maintenance tolerance); while disarmed the window still shows
  INTERRUPTED live.
- `reset_window` currently has no HTTP endpoint by design (no new control
  surface without approval); it is an operator/runbook action via Python.

## Deployment note

Built and tested at the repo only. The running `C:\P2RT` instance is NOT
redeployed by this task; deploy is a later, separate Barış gate. Existing
status consumers are unaffected: the `window` key is additive and all
pre-existing keys/behavior are unchanged (full 164-test baseline suite green,
now 210 with the new tests).
