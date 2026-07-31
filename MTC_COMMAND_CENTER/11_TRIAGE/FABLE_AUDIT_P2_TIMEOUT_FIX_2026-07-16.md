# Fable Audit — Task B `data_restore_timeout_s` 60→300s (PR #23) + Day 0 v5 deploy — 2026-07-16

Auditor: Claude Fable 5. Target: commits `79976577` (fix) + `74e0990b` (docs) on
`feature/ibkr-bridge-final` (worktree `C:\BTL2`), PR #23, vs base master `8721bce0`.
Codex report audited: `11_TRIAGE/P2_DATA_RESTORE_TIMEOUT_REPORT_2026-07-16.md`.

## Audit verdict: PASS

Every claim re-verified on real code and real runs — none taken from the report.

| Check | Evidence | Result |
|---|---|---|
| Scope = approved spec, nothing else | `git diff 8721bce0..79976577 --stat` = exactly 5 paths: `config/bridge.yaml` (+`data_restore_timeout_s: 300`), `bridge/app.py` (+1 wiring line, 300.0 fallback), `bridge/engine/engine.py` (+field `bar_data_restore_timeout_s: float = 300.0`, `max(30.0, …)` clamp in `__post_init__`, pass-through into `BarFeed(...)`), 2 test files | PASS |
| `bars.py` unchanged | `git diff 8721bce0..79976577 -- …/bars.py` = 0 lines; param pre-existed (`bars.py:97` default 60.0, consumed `bars.py:169`) | PASS |
| No notify/reconcile/protected-scope changes | full diff read; none | PASS |
| Suites, both CWDs, at `74e0990b` | repo root: **132 passed**; `IBKR_PAPER_BRIDGE/`: **132 passed** (base was 130; +2 new tests) — independently re-run by Fable | PASS |
| Tests fail on pre-fix code | Fresh temp worktree at `8721bce0` + the new test files: `1 failed, 2 passed` — the wiring test fails with exact `AttributeError: 'BridgeEngine' object has no attribute 'bar_data_restore_timeout_s'`. The two direct-`BarFeed` behavior tests pass on both versions because the feed param pre-existed — **Codex's report states this honestly** (the fix is config/engine wiring by design) | PASS |
| Fail-closed preserved | new test: no-fresh-bar case still emits exactly one `DATA_STALE reconnect_no_fresh_data` + disarm at >300s | PASS |
| Behavior coverage | 300s window: no stale at 239s, `DATA_RESTORED` on first fresh bar at 240s; legacy 60s on the same sequence: stale+disarm (proves the v4 killer is closed) | PASS |
| Secret grep | `git diff 8721bce0..74e0990b | grep -cE '[0-9a-fA-F]{64,}'` = 0 | PASS |
| `C:\P2RT` untouched during build | `1465f8f0`, status clean (verified before deploy) | PASS |

## Deploy — Day 0 v5 (Barış's 2026-07-16 (a) approval covers deploy on audit PASS)

Runbook identical to 2026-07-15 (Task-5-style):

1. `git -C C:/P2RT checkout --detach 74e0990b` — log/status clean, `diff 74e0990b` empty.
   (Bridge process was already down since 07:19:55Z — no live process disturbed.)
2. Suites inside `C:\P2RT`, both CWDs: **132 passed / 132 passed** (PYTHONUTF8=1).
3. Supervisor started: Task Scheduler `MTC-Bridge-P2` → server process up, uvicorn :8790.
4. New run `paper-20260716132819`, testnet, paper, DISARMED, `reconcile_ready: true`,
   fresh reconcile 2026-07-16T13:28:31Z; live 13:00Z hourly bar streaming (fresh bars verified).
5. ≥10-min observation gate: see deploy record below.

## Deploy record — Day 0 v5

**Day 0 v5 = 2026-07-16T13:41:26.908952Z** (`STATE_TRANSITION DISARMED->ARMED`), run
`paper-20260716132819`, deployed tip `74e0990b`, exactly ONE `ARM_REQUEST` (13:41:26.905557Z) +
one transition, positions `[]` / orders `[]`, reconcile clean, validation-tier (Jul-18 planned
PC-off remains a window boundary, not an incident; definitive ≥10-day D3 runs on the VPS).

**The ≥10-min gate produced live proof of the fix.** A real Hyperliquid testnet outage hit
during the observation window and the full tolerance chain absorbed it end-to-end:

```
13:36:56Z  DISCONNECT        bar feed disconnected
13:36:57Z  RECONNECT_RETRY   attempt=1; error=ServerError
13:37:03Z  RECONNECT_RETRY   attempt=2; error=ServerError
13:37:14Z  RECONNECT_RETRY   attempt=3; error=ServerError
13:37:34Z  RECONNECT_RETRY   attempt=4; error=ServerError
13:37:43Z  RECONCILE_FAILED_TOLERATED consecutive=1/3; error=ServerError   (no disarm — N=3 held)
13:38:20Z  RECONNECT         attempt=5   (success)
13:38:43Z  RECONCILE_RECOVERED
13:40:18Z  DATA_RESTORED     last_update=13:40:17Z
```

First fresh bar arrived **118 seconds after the successful reconnect** (13:38:20 → 13:40:18).
Under the old `data_restore_timeout_s = 60` this exact sequence fires
`DATA_STALE reconnect_no_fresh_data` and disarms — the v4 killer. Under the deployed 300s
window the run survived with zero `DATA_STALE`, zero ERROR-severity events, and a clean
reconcile. The fix is not just tested; it is field-validated on Day 0.

Gate facts: observation 13:28:19Z (run start) → 13:41:26Z ARM (>13 min); fresh bars verified
(live 13:00Z hourly bar streaming before and after the outage); `reconcile_ready: true`
throughout; DISARMED held stable until the single deliberate ARM.

## Post-deploy state

- `C:\P2RT` detached at `74e0990b`, status clean, diff vs `74e0990b` empty.
- Supervisor: Task Scheduler `MTC-Bridge-P2` running the server process.
- PR #23 (draft) points at the deployed tip; merge decision belongs to Barış.
- Daily D3 check unchanged: `/api/status` ARMED + fresh reconcile + `[]`/`[]` + pinned
  `git -C C:/P2RT log -1` = `74e0990b` + clean status. Benign ~10-min feed cycles and
  `RECONCILE_FAILED_TOLERATED` WARNs during real outages are expected behavior.

TESTNET ONLY; `HL_LIVE_ACK` unset; no secret printed; secret greps 0.
