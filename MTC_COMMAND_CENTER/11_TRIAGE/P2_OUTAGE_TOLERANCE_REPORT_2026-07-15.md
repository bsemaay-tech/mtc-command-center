# P2 Outage-Tolerance Build Report — 2026-07-15

Status: **TASKS 1-4 COMPLETE; FABLE AUDIT REQUIRED.** Task 5 deploy/ARM and Task 6 PR merges were not performed.

## Build identity and safety boundary

- Worktree: `C:\BTOL`
- Branch: `feature/ibkr-bridge-final`
- Base: `8e53439e`
- Code commit: `0e644b527fbc176c43d796499723742cb929998d`
- Runtime worktree remained untouched: `C:\P2RT` is still detached at `cc4ce67d555d567ce9390cf2c70a00a7e8a2e0fe` with a clean status.
- Testnet boundary preserved. `HL_LIVE_ACK` was explicitly unset for tests. No wallet key was read or printed.
- No deploy, process restart, ARM, push, PR merge, fixture regeneration, or strategy-entry/risk/sizing change was performed.

## Implementation evidence

### Task 1 — consecutive reconcile tolerance

- `IBKR_PAPER_BRIDGE/bridge/engine/engine.py:44-60` defines and validates `reconcile_max_consecutive_failures=3` and initializes `_consecutive_reconcile_failures=0`.
- `engine.py:346-359` retains the rebuild-only `HyperliquidNotConfigured` defer branch. It still leaves state, reconcile health, timestamp, and failure counter unchanged. The Task-3-required deferred notification is dispatched at line 359.
- `engine.py:362-397` increments genuine failures, marks reconcile health not ready, emits `RECONCILE_FAILED_TOLERATED` WARN below the limit, and emits the existing fail-closed `RECONCILE_FAILED` ERROR plus disarm at the limit.
- `engine.py:399-408` resets the counter on every successful reconcile and preserves `RECONCILE_RECOVERED`.
- `IBKR_PAPER_BRIDGE/config/bridge.yaml:19` declares the limit in the risk block; `bridge/app.py:113-115` threads it into the engine with default 3.

The binding window is three consecutive 60-second reconcile cycles: nominally about three minutes from the last known-good reconcile evidence. A successful cycle resets the budget completely.

### Task 2 — reconnect outer budget

- `IBKR_PAPER_BRIDGE/bridge/engine/bars.py:95-109` adds the constructor-controlled `reconnect_attempts=9`.
- `bars.py:183-199` uses that value while preserving the existing exponential delay and 60-second cap.
- `IBKR_PAPER_BRIDGE/config/bridge.yaml:8-9`, `bridge/app.py:116-117`, and `bridge/engine/engine.py:45-46,90-91` thread the attempt count and base delay from config to `BarFeed`.

Exact worst-case schedule: attempt start times are `0, 5, 15, 35, 75, 135, 195, 255, 315` seconds. Equivalently, cumulative waiting is `0+5+10+20+40+60+60+60+60 = 315 seconds` (5m15s) before the ninth attempt fails and `DATA_STALE` is emitted.

`data_restore_timeout_s` remains 60 seconds (`bars.py:97,169`). It starts only after connect/resubscribe succeeds, so it does not shorten the 315-second reconnect loop; it remains a separate post-reconnect proof that fresh data actually resumed. The two-bar `last_update` guard remains unchanged (`bars.py:178`); the dead-websocket branch returns after the reconnect result, so this guard does not race or truncate the reconnect budget.

### Task 3 — routine Telegram suppression

- `IBKR_PAPER_BRIDGE/bridge/engine/engine.py:24` defines the explicit routine suppression set.
- `engine.py:416-425` always inserts feed events into the store, suppresses Telegram for routine `DISCONNECT`, first-attempt `RECONNECT`, and `DATA_RESTORED`, and continues to send retry/stale and later-attempt reconnect alerts.
- Reconcile tolerated, deferred, failed, recovered, state transition, ARM/DISARM/KILL, and heartbeat notification paths remain active.

## Deterministic tests

- `tests/test_engine_dryrun.py:44-49`: two failures remain ARMED; the third disarms; success resets the counter before another two failures.
- `tests/test_hyperliquid_broker.py:1372,1426`: rebuild defer does not count or alter health; genuine nonconfiguration reaches the three-strike disarm.
- `tests/test_p1_failure_drills.py:288`: six failed connects plus success on attempt 7 simulate 195 seconds (3m15s) with no `DATA_STALE`.
- `tests/test_p1_failure_drills.py:320`: nine failures schedule exactly 315 seconds, emit `DATA_STALE`, and invoke the real engine stale-disarm callback.
- `tests/test_task11_polish.py:67`: the routine triple remains in the store with zero notifier sends; retry, later-attempt reconnect, and stale events notify.
- These tests were not separately executed against base `8e53439e`; by construction the new reconcile/config assertions and 9-attempt expectations are absent or contradictory on that base. Fable should independently perform any desired pre-change mutation check.

## Verification output

Focused affected suites:

```text
........................................................................ [ 91%]
.......                                                                  [100%]
79 passed, 1 warning in 7.51s
```

Final full suite from `C:\BTOL`:

```text
........................................................................ [ 55%]
..........................................................               [100%]
130 passed, 1 warning in 22.04s
```

Final full suite from `C:\BTOL\IBKR_PAPER_BRIDGE`:

```text
........................................................................ [ 55%]
..........................................................               [100%]
130 passed, 1 warning in 20.50s
```

The only warning in both runs is the existing Starlette `httpx` deprecation warning from `fastapi/testclient.py`.

Additional gates:

```text
git diff --check
# no output; PASS

staged secret regex: [0-9a-fA-F]{64,}
staged_secret_matches=0
```

## Honest anomalies

1. The mandated Cline-first attempt detached from the short shell window and exited without changing the worktree.
2. The DeepSeek fallback ignored the intended `C:\BTOL` read paths, wandered through the shared checkout, and hit `max_iters` without `finish()` or any allowed write. Its report was discarded as evidence.
3. The implementation was therefore applied locally under the documented fallback exception, then audited through the complete diff, focused tests, two full-suite runs, `git diff --check`, and the staged secret scan.
4. PowerShell on this host does not support `&&`; the required checkout/add/commit sequence was executed with explicit `$LASTEXITCODE` gates instead.

## Audit gate

Fable must audit code commit `0e644b52` and this report. **No ARM / no deploy performed.** Task 5 remains locked pending Fable PASS plus Barış go. Task 6 remains locked until the audit and must not be conflated with deployment approval.
