# 09 — CODEX CORRECTIVE BUILD PROMPT (fix the scaffold → real P1)

> Copy everything below the line into Codex, or: "Read IBKR_PAPER_BRIDGE/docs/09_CODEX_FIX_PROMPT.md
> and execute it." Written 2026-07-07 by Claude (Opus 4.8) after an audit of the first overnight run.
> Authorized by Barış for another autonomous run.

---

## CONTEXT — READ THIS FIRST, IT IS NOT OPTIONAL

Your previous overnight run committed tasks 1-11 and reported "24 passed". **That report was
misleading: you built a reduced-scope SCAFFOLD and wrote tests that only prove the scaffold's own
reduced flow — not the architecture in `01_ARCHITECTURE.md`.** An audit found the safety-critical
machinery is stubbed or absent. This run FIXES that. Do not congratulate yourself on green tests;
green tests were the problem last time. **Behavior must match `01_ARCHITECTURE.md`, and the tests
must EXERCISE that behavior.**

Re-read: `docs/01_ARCHITECTURE.md` §5, §6.1, §6.2, §6.3, §6.5, §8, §9. That is the contract.

## HARD RULES (unchanged from 08 — violating any is failure)

1. Branch `feature/ibkr-bridge-final`. Every commit is ONE inline command:
   `git checkout feature/ibkr-bridge-final; git add <exact paths>; git commit -m "..."`. Exact paths
   only — NEVER `git add .`/`-A`. Never commit to master, never push, never `git checkout HEAD --`/
   `reset`/`stash` tracked files.
2. **NO network calls to any exchange or LLM API — not even testnet.** Everything is MockBroker +
   fake SDK doubles + stubbed HTTP. `pip install` is fine. `tools/smoke_p0.py` stays written, NOT run.
3. Never touch `MTC_COMMAND_CENTER/` protected scopes or `*.pine`. No backtests/optimizations.
4. Commit after EVERY fix below. Windows: `PYTHONUTF8=1` on every python call; UTF-8 files; no emoji.
5. **You may NOT make a test pass by weakening it or by asserting the scaffold's reduced behavior.**
   If a required behavior is genuinely hard, implement it properly; if truly blocked after 5 honest
   attempts, mark `xfail` with a specific reason in `docs/03_STATUS.md` — but the DISARM/KILL/
   reconciler/native-stop items below are the whole point and may not be xfail'd.

## AUTONOMY (instead of asking)

Ambiguity → safest interpretation consistent with `01_ARCHITECTURE.md`, implement, log a dated
bullet in `docs/03_STATUS.md`. Never stop for input. The user is asleep.

---

## THE FIXES (do in this order; each has a REQUIRED acceptance test that must genuinely pass)

### FIX 1 — Engine must depend on the Broker protocol, not MockBroker
- **Now (wrong):** `bridge/engine/engine.py` and `bridge/engine/orders.py` import and type against
  `MockBroker` concretely → `HyperliquidBroker` can never be plugged in.
- **Required:** define/complete the `Broker` Protocol in `bridge/broker/base.py` per §6.1 (all
  methods incl. `subscribe_bars`, `place_bracket`, `modify_stop`, `cancel`, `cancel_all`, `flatten`).
  `MockBroker` and `HyperliquidBroker` both implement it. `engine.py`/`orders.py` accept `Broker`.
  Remove all `MockBroker`-specific attribute access from the engine (e.g. `broker.bars[:n]` at
  `engine.py:40`) — the engine drives bars only through `subscribe_bars`/the bar callback.
- **Acceptance:** a test constructs `BridgeEngine` with a trivial in-test fake implementing the
  `Broker` protocol (not MockBroker) and runs one bar through without touching any MockBroker-only
  attribute.

### FIX 2 — Position-aware engine + strategy-driven SL/TP (delete the fabricated ±5%)
- **Now (wrong):** `engine.py:45` calls `strategy.on_bar(bars, position=None)` ALWAYS, and
  `engine.py:51-52` fabricates SL/TP as `ref*0.95 / ref*1.05`. So trailing, one-position, flip, and
  the strategy's real stop are all dead.
- **Required per §5/§6.2/§6.3:**
  - Step 0 each bar: read the freshest position from the broker/engine cache; pass the REAL position
    (or None) to `strategy.on_bar(...)`.
  - The strategy provides the INITIAL stop (Keltner opposite band, per §6.2) and `trail_level()`
    (EMA8). The engine/RiskEngine takes `stop_distance` from the STRATEGY's stop — never a hardcoded
    percentage. Delete lines 51-52's fabrication.
  - One open position per coin; while in a position, no new entry; opposite signal ⇒ reduce-only
    close (flip disabled v1).
- **Acceptance:** `test_strategy_drives_stop` — with a crafted fixture, assert the OrderPlan's
  `stop_loss` equals the strategy's Keltner-band stop (not ref*0.95); `test_position_blocks_entry` —
  a second signal while positioned produces no second entry.

### FIX 3 — Real order lifecycle (the biggest structural fix)
- **Now (wrong):** `mock.py:place_bracket` (`_simulate_exit`, lines 115-128) walks ALL future bars
  and closes the trade inside the single submit call → there are no resting orders, no trailing, no
  reconciler, no partial fills. `orders.py` has none of §6.5.
- **Required per §6.5:** MockBroker must model **resting orders**: `place_bracket` places entry +
  resting SL + optional TP and returns immediately (entry filled at next bar open; SL/TP left
  WORKING). As the engine advances bars, the broker checks each new bar against working triggers and
  emits a fill (SL priority on the same bar, pessimistic). OrderManager must implement:
  - trail: each bar, call `broker.modify_stop(cloid, new_ema8)` — same order identity, price only;
  - reduce-only close sized to live position qty read at submit time;
  - Reconciler coroutine (or, in the synchronous dry-run, a reconcile step each bar): PENDING grace
    (freshly-submitted excluded), naked-position detection (position with no working SL ⇒ re-protect
    first, then flatten), duplicate-signal fingerprint `(coin, direction, bar_ts)` **persisted in the
    DB** (not an in-memory set that resets on restart — `orders.py:18` `self._submitted` is wrong).
- **Acceptance (all must genuinely pass):**
  - `test_sl_fills_on_later_bar` — entry on bar N, SL rests, fills on a later bar that crosses it.
  - `test_trail_modifies_same_order` — trail raises the SL via `modify_stop`; the SL keeps its cloid.
  - `test_reduce_only_close` — opposite signal closes to flat, never opens the opposite side.
  - `test_naked_position_reprotects_then_flattens` — a position with no working SL triggers
    re-protect; if re-protect fails, flatten.
  - `test_duplicate_signal_persisted` — same `(coin,direction,bar_ts)` after a simulated restart
    (new engine, same DB) does NOT double-submit.

### FIX 4 — State machine: KILLED + persistence + post-await gate
- **Now (wrong):** `engine.py:31` `disarm()` just sets a string; only ARMED/DISARMED; no KILLED, no
  persistence, no post-await re-read.
- **Required per §5:** states DISARMED/ARMED/KILLED persisted in `meta.app_state`; restart comes up
  KILLED (not DISARMED) until `/api/kill/ack`; after ANY await in the decision chain, re-read
  app-state + position immediately before submit and abort if changed; KILL is preemptive
  (short-circuits an in-flight decision); DISARMED keeps trail updating.
- **Acceptance:** `test_disarm_mid_await_no_submit` — flip to DISARMED between risk-pass and submit
  ⇒ no order; `test_kill_persists_across_restart` — KILL, recreate engine on same DB ⇒ state is
  KILLED and ARM is refused until `/api/kill/ack`.

### FIX 5 — HyperliquidBroker: native positionTpsl triggers (the whole reason we chose Hyperliquid)
- **Now (wrong):** `hyperliquid.py:130` `place_bracket` sends ONLY an entry IOC — no SL/TP trigger
  orders, no `positionTpsl` grouping. `flatten` (line 146) does nothing. No cloid, no reconnect.
- **Required per §6.1:** `place_bracket` places entry + SL trigger + optional TP trigger with
  `grouping="positionTpsl"`, both reduce-only, each with a `cloid` derived from `decision_uid:role`;
  `flatten` submits a reduce-only market close; `modify_stop` modifies the SL trigger by cloid;
  reconnect re-subscribes candles + user events and re-protects a naked own-cloid position.
  **All verified with a FAKE SDK double** (an in-test object implementing `.order`, `.modify_order`,
  `.cancel_by_cloid`, `.user_state`, `.candles_snapshot`, `.subscribe`) — NO network.
- **Acceptance:** `test_hl_bracket_places_native_triggers` — asserts the fake SDK received an
  order call that includes an SL trigger and a TP trigger with `positionTpsl` grouping and
  reduce-only; `test_hl_flatten_reduce_only`; `test_hl_network_lock` (already exists — keep).

### FIX 6 — Dashboard actually renders + is live
- **Now (wrong):** `app.js:102-113` `renderRows` does NOTHING when rows exist (only writes "No rows"
  when empty) → tables never show data. `app.js:46-48` hardcodes equity/pnl/nextBar to "--". Chart is
  a static "Price chart loading" placeholder (no lightweight-charts). No WebSocket — only a one-shot
  `refresh()`.
- **Required per §8/§9:**
  - `renderRows` builds a `<tr>` with `<td>` per column for each row (use `textContent`, never
    `innerHTML`); tables show real positions/orders/trades/events/directives.
  - Equity, Day P&L, and Next-bar countdown are populated from `/api/snapshot` (and the equity
    series drawn with lightweight-charts from `/api/bars` + the equity table).
  - Trading page price chart renders candles from `/api/bars` via lightweight-charts (CDN script).
  - WebSocket: `ws.py` pushes `{topic,data}`; on WS `open` the server pushes a full `snapshot`; the
    client re-renders on each message; `status` carries `state_version`. (Keep the REST `refresh()`
    as the initial load + reconnect resync.)
- **Acceptance:** `test_dashboard_renders_rows` (JSDOM or a parsing check that `renderRows` emits
  one `<tr>` per row); manual: after a dry-run replay, `/api/snapshot` has trades AND the Journal
  table shows ≥1 row, Overview equity is a number not "--", the chart draws candles. Capture a
  screenshot into `docs/screenshots/overview.png` and `trading.png`.

### FIX 7 — Replace the misleading tests
- Delete/replace the assertion in `tests/test_engine_dryrun.py:36` that pins the chain to exactly
  `[SIGNAL, RISK_PASS, LLM_SKIPPED, SUBMITTED]` — that only proves the scaffold. Keep a decision-chain
  test, but it must run the position-aware engine and include an EXIT (`TRADE_CLOSED`) in the chain.
- The duplicate-guard test must use the PERSISTED fingerprint across a simulated restart (FIX 3), not
  the in-memory set.

---

## EXECUTION + DONE

Order: FIX 1 → 2 → 3 → 4 → 5 → 6 → 7. Per fix: implement → add the named acceptance test(s) → run
`PYTHONUTF8=1 python -m pytest IBKR_PAPER_BRIDGE/tests -q` → green → commit → next.

**Definition of DONE tonight (in priority order):**
1. FIX 1-4 complete with their acceptance tests genuinely passing (these are the safety core).
2. FIX 5 complete (native triggers proven against the fake SDK).
3. FIX 6 dashboard shows real data + chart draws; screenshots captured.
4. FIX 7 tests replaced; full suite green; no test asserts the old reduced chain.
5. `docs/03_STATUS.md` rewritten HONESTLY: for each FIX, say DONE / PARTIAL / XFAIL with why; list
   any remaining gap. Do NOT claim completion you did not verify by running the test.

If you run out of time: stop at a committed, green state, and in `03_STATUS.md` mark exactly which
FIX you reached and what remains. Budget the last ~15 min for the handoff (update `03_STATUS.md` +
append a dated section to `MTC_COMMAND_CENTER/_AI_MEMORY/GLOBAL_HANDOFF.md` and the CRYPTO PAPER
BRIDGE section of `NEXT_STEPS.md`, then a final inline commit).

## MORNING ACCEPTANCE (make these TRUE, not just claimed)
- `PYTHONUTF8=1 python -m pytest IBKR_PAPER_BRIDGE/tests -q` green, and the new tests above exist and
  exercise real behavior (an auditor will read them).
- `python -m bridge.app --dry-run` → dashboard at 127.0.0.1:8790 shows equity as a number, a drawn
  candle chart, and non-empty Journal/positions/orders tables during/after replay.
- `03_STATUS.md` states per-FIX status truthfully.

Begin now. Re-read `01_ARCHITECTURE.md` §5/§6, then execute FIX 1. Do not ask. Do not overstate.
