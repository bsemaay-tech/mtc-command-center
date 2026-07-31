# P2 Reconnect/Reconciler Race Fix — Builder Report (2026-07-14)

**Status: TASKS 1–3 BUILT AND LOCALLY VERIFIED; STOPPED FOR FABLE AUDIT.**

Task 4 was not attempted. No deployment, runtime restart, API call, ARM request,
process action, broker/exchange request, push, or `C:\P2RT` file change occurred.

## Scope and Git identity

- Dedicated worktree: `C:\BFIX`
- Branch: `feature/ibkr-bridge-final`
- Required baseline: `960369b972208d29ae018a1868b946e180458a46`
- Implementation commit: `da44d1ff662acc8ab19c12af624c8ebed536e92b`
- Commit subject: `fix(bridge): remove reconnect reconcile race`
- Runtime worktree remained detached at `54278b66f2299baf4f2c02486923b91120b25b1e`.

## Task 1 — Atomic replacement-client swap

`IBKR_PAPER_BRIDGE/bridge/broker/hyperliquid.py`:

- `:97` initializes `rebuilding = False`.
- `:105-107` documents the confirmed invariant: the old `Info` object's REST methods,
  including `user_state`, remain usable while its websocket subscriptions are dead;
  `BarFeed` owns bar-staleness handling.
- `:115-124` preserves the existing dead-websocket test and builds replacements into locals.
- `:125-131` registers every existing candle subscription on the replacement `Info`
  before exposure.
- `:134` exposes `info` and `exchange` together using one tuple assignment.
- `:135-143` resets and restores account/user-channel state using the existing path.
- `:144-153` always clears `rebuilding` and disconnects the old dead socket only after a
  completed swap, best effort.
- `:587-599` makes `_build_sdk_clients()` return `(new_info, new_exchange)` without
  mutating broker attributes.

No strategy, band, trail, risk, sizing, configuration, notifier threshold, Pine, parity,
or MTC behavior changed.

## Task 2 — Narrow reconcile deferral guard

`IBKR_PAPER_BRIDGE/bridge/engine/engine.py:336-347` uses the exception class name rather
than importing the concrete Hyperliquid adapter, avoiding engine-to-adapter coupling. Only
`HyperliquidNotConfigured` while `broker.rebuilding` is true writes:

```
severity=WARN
code=RECONCILE_DEFERRED
detail=broker rebuilding
```

The branch returns `False` without changing reconcile-health fields, publishing a state
change, notifying, or disarming. The original fail-closed path remains at `:348-367` for the
same exception outside a rebuild and for every other exception during a rebuild.

## Task 3 — Deterministic tests

`IBKR_PAPER_BRIDGE/tests/test_hyperliquid_broker.py`:

- `:1239` updates the existing dead-websocket rebuild test for the return-value builder.
- `:1305` blocks client construction with `threading.Event`, proves `positions()` uses the
  old client, then drives the engine reconcile cycle during the real blocked rebuild and
  proves the state remains ARMED with no `RECONCILE_FAILED` or synthetic defer.
- `:1372` forces `HyperliquidNotConfigured` with `rebuilding=True` and proves the exact
  deferred-event contract plus unchanged reconcile-health fields.
- `:1425` proves the same exception with `rebuilding=False` still disarms.
- `:1467` proves a different exception while rebuilding still disarms.
- `:1519` proves candle subscriptions precede exposure, user channels subscribe exactly
  once each, and the old disconnect callback observes the replacement already swapped in.

These five added tests plus the updated rebuild regression exercise behavior that the
pre-fix implementation does not satisfy: it nulled the broker clients before a blocked
build, had no defer branch, and disconnected the old socket before replacement exposure.

## Commands and independently reproduced outputs

Focused suite from `C:\BFIX`:

```powershell
$env:PYTHONUTF8='1'
python -m pytest IBKR_PAPER_BRIDGE/tests/test_hyperliquid_broker.py -q
```

```text
.....................................................                    [100%]
53 passed in 2.46s
```

Full suite from repository root:

```powershell
$env:PYTHONUTF8='1'
python -m pytest IBKR_PAPER_BRIDGE/tests -q
```

```text
........................................................................ [ 56%]
.......................................................                  [100%]
127 passed, 1 warning in 15.63s
```

Full suite from bridge root:

```powershell
$env:PYTHONUTF8='1'
python -m pytest tests -q
```

```text
........................................................................ [ 56%]
.......................................................                  [100%]
127 passed, 1 warning in 15.58s
```

Both warnings are the pre-existing FastAPI/Starlette `TestClient` deprecation warning.
Required baseline was 122 tests; the new total is 127.

Pre-commit checks:

```text
git diff --check
<no output>

HL_LIVE_ACK is unset

staged secret grep [0-9a-fA-F]{64,}
0 matches
```

The commit staged exactly:

```text
IBKR_PAPER_BRIDGE/bridge/broker/hyperliquid.py
IBKR_PAPER_BRIDGE/bridge/engine/engine.py
IBKR_PAPER_BRIDGE/tests/test_hyperliquid_broker.py
```

## Honest anomalies

1. The mandatory first-choice Cline invocation failed before editing with
   `session not found: 1784037560511_efcuo`.
2. The `_deepseek_driver` fallback produced a compiling implementation and tests, but its
   initial result had three audit defects: non-exact deferred-event detail, a disconnect
   test that did not observe ordering, and no engine reconcile inside the genuinely blocked
   rebuild. Codex corrected all three before accepting the result or running the suites.
3. The delegated report claimed 127 passes; that claim was ignored until Codex independently
   reproduced both complete suites above.
4. Git emitted only line-ending normalization notices (`LF` may become `CRLF` on a future
   checkout); `git diff --check` remained clean.
5. The branch is local only at this stop point. Nothing was pushed.

## Audit/deploy gate

Fable must audit the committed code and rerun validation on real files. Task 4 remains
locked until both conditions are present: **Fable audit PASS** and **Barış explicit go**.
Until then, do not sync `C:\P2RT`, restart the supervised child, call ARM, reset P2 Day 0,
or push under an assumed deployment authorization.
