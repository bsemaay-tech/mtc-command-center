# CODEX PROMPT — P2 Reconnect/Reconciler Race Fix + Single Restart Window (2026-07-14)

Author: Claude Fable 5 (auditor). Executor: Codex GPT-5 (builder).
Incident record: GLOBAL_HANDOFF `[Claude Fable 5] 2026-07-14 — P2 INCIDENT` (commit `f64a5bb5`
on `feature/donchian-crypto-ladder`).

## INCIDENT SUMMARY (Fable-verified on runtime code + event store — do not re-derive)

P2 Day 0 v2 (ARM 2026-07-13T15:17:05Z) died at **2026-07-13T16:46:42Z**, 1h29m in. Chain:

1. Routine ~10-min ws "Expired" cycle → `BarFeed.reconnect()` → broker `connect()`.
2. `connect()` in `bridge/broker/hyperliquid.py` (~lines 108-117) does
   `self.info = None; self.exchange = None`, then rebuilds clients in a thread —
   a seconds-long window where `self.info is None`, EVERY reconnect cycle.
3. The 60s reconciler (`engine.py _reconcile_loop`) fired inside that window:
   `positions()` (line ~183-184) raised `HyperliquidNotConfigured` →
   `_run_reconcile_cycle` (line ~330-354) treats ANY exception single-strike →
   `RECONCILE_FAILED` event + **auto-DISARM**.
4. 61s later: DATA_RESTORED + `RECONCILE_RECOVERED`. The runtime killed its own window while
   otherwise healthy. Collision odds ≈ rebuild_secs/60 per cycle × ~6 cycles/hour →
   **P2's ≥10-day uninterrupted window is unreachable until this race is removed.**

Also on record: a REAL Hyperliquid testnet outage 07:52-07:54Z Jul 14 (RECONNECT_RETRY ×5
`ServerError`, DATA_STALE) while already DISARMED — that path behaved correctly and stays
untouched.

## SCOPE RAILS

1. **Minimal diff.** Only the race fix + its tests. Do NOT bundle the notify-threshold change,
   dashboard work, or anything else into this window.
2. Branch: `feature/ibkr-bridge-final` (currently free — not checked out in any worktree).
   Create a dedicated worktree first:
   `git -C C:/LAB/Tradingview_LAB_CLEAN worktree add C:/BFIX feature/ibkr-bridge-final`
   and do ALL work there (this is what kept FZ3G5 safe; never use
   `--ignore-other-worktrees` on a branch another worktree has checked out).
3. **`C:\P2RT` untouched during build.** Deploy (Task 4) happens only AFTER Fable audit PASS
   and Barış's explicit go.
4. TESTNET only, `HL_LIVE_ACK` unset, never print `HL_API_WALLET_KEY`. Secret grep
   `[0-9a-fA-F]{64,}` on staged diff = 0 before every commit.
5. `PYTHONUTF8=1`; both suites (repo root + `IBKR_PAPER_BRIDGE/`) green before claiming done.
   Base = 122 passed at `960369b9`. Note: conftest now blocks real Telegram in tests.
6. Design authority: `docs/01_ARCHITECTURE.md` + fail-closed doctrine (`59c334c0`). The
   fail-closed PRINCIPLE stays; only its false-positive trigger is removed.
7. Report honestly; Fable audits on real code and will re-run everything.

## TASK 1 — PRIMARY FIX: atomic client swap in `connect()`

Rework the rebuild path in `bridge/broker/hyperliquid.py connect()` so `self.info` /
`self.exchange` are NEVER null while the broker is nominally connected:

- Detect dead ws exactly as now (manager.is_alive false).
- Build the replacement clients into LOCALS (a `_build_sdk_clients`-equivalent that returns
  new instances instead of assigning attributes — refactor as needed).
- Subscribe the candle feeds for `self._bar_subscriptions` on the NEW Info object before it
  goes live.
- Swap `self.info` / `self.exchange` to the new instances atomically (single assignment
  each, no awaits between them), then reset `_user_channels_subscribed = False` and run
  `_subscribe_user_channels` as today.
- Disconnect the OLD dead socket after the swap (best-effort, exceptions swallowed as now).
- Key invariant to state in a comment: `Info.user_state` and friends are REST calls — the old
  client keeps serving the reconciler correctly while the ws-dead replacement is being built;
  only the ws subscriptions are dead, and BarFeed already handles bar staleness.

## TASK 2 — SECONDARY GUARD (defense in depth, small)

- Broker: set a `self.rebuilding: bool` flag around the rebuild section of `connect()`
  (True from dead-ws detection until after the swap; always cleared in `finally`).
- Engine `_run_reconcile_cycle`: if the exception is `HyperliquidNotConfigured` AND
  `getattr(self.broker, "rebuilding", False)` is True → do NOT flip `reconcile_ready`, do
  NOT disarm; insert a WARN event `RECONCILE_DEFERRED` `detail="broker rebuilding"` and
  return False. Single-strike behavior is UNCHANGED for every other exception and for
  `HyperliquidNotConfigured` outside a rebuild (that still means genuinely broken config).
- Import the exception type where the engine can see it without creating a circular import
  (string-match on `type(exc).__name__` is acceptable if imports are awkward — state which
  you chose and why).

## TASK 3 — TESTS (write first or alongside; all must fail on pre-fix code)

1. **Race reproduction:** fake SDK whose client-build blocks on an event; start `connect()`
   rebuild, call `positions()` mid-rebuild → must return via the old client (Task 1) instead
   of raising; assert no `RECONCILE_FAILED`/disarm when driven through the engine.
2. **Deferred-cycle test:** force `HyperliquidNotConfigured` while `rebuilding=True` through
   `_run_reconcile_cycle` → assert state stays ARMED, `RECONCILE_DEFERRED` WARN event
   written, `reconcile_ready` unchanged.
3. **Fail-closed regression:** same exception with `rebuilding=False` → still disarms
   (single-strike preserved); any other exception during rebuild → still disarms.
4. **Swap integrity:** after a simulated rebuild, candle subscriptions re-registered on the
   new Info, user channels re-subscribed exactly once, old socket disconnected.
5. Full suites from BOTH CWDs; paste tails. Expect ≥122 + new tests.

Commit(s) to `feature/ibkr-bridge-final` in C:/BFIX, conventional messages, explicit paths,
secret grep each. Then write
`MTC_COMMAND_CENTER/11_TRIAGE/P2_RACE_FIX_REPORT_2026-07-14.md` (commands + outputs +
file:line for every claim, honest anomalies section), update `GLOBAL_HANDOFF.md` (dated
section) — and **STOP for Fable audit. Do not deploy.**

## TASK 4 — DEPLOY + RE-ARM (LOCKED: only after Fable audit PASS + Barış explicit go)

Single restart window, exactly this order (mirrors the proven 2026-07-13 cycle):

1. Verify exchange positions/orders `[]` via API; bridge is already DISARMED.
2. Stop the supervised child process (leave the Task Scheduler supervisor job alone — it
   restarts the child; or stop/start the scheduler task as done 2026-07-13, state which).
3. Sync the pinned runtime: `git -C C:/P2RT checkout --detach <audited-tip>` (P2RT is a
   LINKED WORKTREE, detached-HEAD doctrine — never check out the branch there).
4. Suites from BOTH P2RT CWDs (`PYTHONUTF8=1`); conftest now prevents Telegram leakage.
5. Supervisor (re)start → new run id, DISARMED. Observe ≥10 minutes: at least one full
   `DISCONNECT -> RECONNECT attempt=1 -> DATA_RESTORED` cycle AND ≥2 clean reconciles AND
   at least one reconnect with NO `RECONCILE_FAILED`/`RECONCILE_DEFERRED`-storm (a single
   deferred WARN during a rebuild is acceptable and expected occasionally).
6. Exactly ONE ARM call with `X-Confirm`. Verify: one `ARM_REQUEST` + one `DISARMED->ARMED`,
   post-ARM reconciles clean, positions/orders still `[]`.
7. **Record new Day 0 timestamp.** Update `docs/03_STATUS.md` (new Day 0, new tip, test
   count, race-fix note), `GLOBAL_HANDOFF.md`, `NEXT_STEPS.md`. Commit on
   `feature/ibkr-bridge-final` from C:/BFIX. P2 clock reset recorded: this is the approved
   single restart window (fix + conftest + golden all live together).
8. Push `feature/ibkr-bridge-final` (updates PR #16) only if Barış's go includes it —
   otherwise leave local and say so.

STOP conditions during deploy: any suite failure, any unexplained ERROR event, more than one
ARM transition, any position/order appearing — abort, leave DISARMED, report.
