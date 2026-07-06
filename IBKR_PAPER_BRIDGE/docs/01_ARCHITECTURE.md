# ARCHITECTURE — IBKR Paper Bridge v1

Design: Claude Fable 5, 2026-07-05. Target builder: Opus/Codex, one working day (see `02_BUILD_PLAN_1DAY.md`).
Everything here is decided — the builder should NOT re-litigate stack choices; deviations require a
dated note in this file explaining why.

---

## 1. Stack (decided)

| Layer | Choice | Why |
|---|---|---|
| Language | Python 3.11+ | Repo standard; broker libs are Python. |
| Broker API | **`ib_async`** (maintained fork of ib_insync) | asyncio-native, auto-reconnect, order/fill events as awaitables. Fallback if install problems: `ib_insync==0.9.86` (same API). Raw `ibapi` NOT used directly. |
| Backend | FastAPI + uvicorn, single process, asyncio | One event loop shares broker connection + engine + WebSocket. No Celery/Redis — keep 1-day buildable. |
| Persistence | SQLite (WAL mode), file `data/bridge.db` | Zero-ops, transactional, good enough for 1 strategy. All writes through one `Store` class. |
| Frontend | Static vanilla HTML/CSS/JS served by FastAPI (`/static`), WebSocket for live updates. **No build step, no npm.** | Same pattern as MCC dashboard; Opus/Codex build it fast; professional dark theme (spec §9). Chart: lightweight-charts via CDN (single `<script>` tag). |
| Config | YAML files under `config/` + runtime overrides from dashboard persisted to `data/runtime_config.json` | Human-diffable base + UI-editable runtime. |
| Scheduler | asyncio tasks (no APScheduler) | Bar clock, LLM refresh, reconciliation — all simple periodic coroutines. |
| LLM | Anthropic API (Claude, model `claude-sonnet-5` default) for veto/summary; **xAI Grok API** (`grok-4`, key already in `_deepseek_driver` provider env) for market-sentiment regime | Grok has X/news access for sentiment; Claude for structured veto reasoning. Both optional at runtime. |

Process model: **one process** `python -m bridge.app`. TWS/IB Gateway runs separately (user-launched).

---

## 2. Directory layout

```
IBKR_PAPER_BRIDGE/
  README.md
  docs/                      (these design docs)
  requirements.txt           fastapi, uvicorn[standard], ib_async, pydantic>=2, pyyaml, httpx, anthropic
  config/
    bridge.yaml              app config (ports, mode, fail-open policy, LLM on/off)
    strategies/
      keltner_trail_ema8.yaml
  bridge/
    app.py                   FastAPI factory + lifespan: start engine, ws manager
    settings.py              pydantic-settings; env: IBKR_HOST/PORT/CLIENT_ID, ANTHROPIC_API_KEY, XAI_API_KEY, IBKR_LIVE_ACK
    broker/
      base.py                Broker protocol (abstract)
      ibkr.py                IBKRBroker (ib_async impl)
      mock.py                MockBroker (deterministic sim fills; used by tests + dry-run mode)
    engine/
      engine.py              main loop orchestrator (state machine §5)
      bars.py                BarFeed: historical warmup + keepUpToDate live bars
      strategy_base.py       Strategy protocol
      strategies/
        keltner_trail_ema8.py
      risk.py                RiskEngine
      llm_gate.py            regime directive + pre-trade veto
      orders.py              OrderManager (bracket orders, reconciliation)
    store/
      db.py                  SQLite Store, schema §7, migrations inline (CREATE IF NOT EXISTS)
    api/
      routes.py              REST endpoints §8
      ws.py                  WebSocket hub (topic-based push)
    static/
      index.html  app.css  app.js
  tests/
    test_risk.py  test_strategy.py  test_order_manager_mock.py  test_engine_dryrun.py
  data/                      (git-ignored) bridge.db, runtime_config.json, logs/
```

Add to repo root `.gitignore`: `IBKR_PAPER_BRIDGE/data/`.

---

## 3. Dataflow (end to end)

```
TWS paper (7497)
   │ ib_async
   ▼
BarFeed ──bar closed──► Engine.on_bar()
                          │ 1. Strategy.on_bar(bars) → Signal | None
                          │ 2. RiskEngine.size(signal, account, config) → OrderPlan | Rejection
                          │ 3. LLMGate.check(order_plan, regime) → PASS | VETO(reason)
                          │ 4. OrderManager.submit(bracket) → order ids
                          ▼
                        Store (every step = one JSON decision row)
                          │
                          ▼
                        WS hub ──push──► Dashboard
LLM regime task (period: config, default 4h) ──► regime directive row + WS push
Reconciler task (60s) ──► positions/orders truth sync vs broker
```

Signal path is **synchronous per bar** — no queues. One symbol × one strategy in v1 keeps this trivial.

---

## 4. Core types (pydantic models, `bridge/engine/types.py`)

```python
class Bar(BaseModel):        ts: datetime; open: float; high: float; low: float; close: float; volume: float
class Signal(BaseModel):     ts: datetime; symbol: str; direction: Literal["LONG","SHORT","FLAT"]
                             reason: str                       # human-readable rule trace
                             ref_price: float                  # bar close at signal
class OrderPlan(BaseModel):  signal: Signal; qty: int; entry_type: Literal["MKT","LMT"]
                             limit_price: float | None; stop_loss: float; take_profit: float | None
                             risk_dollars: float; risk_pct: float
class Rejection(BaseModel):  stage: Literal["RISK","LLM","STATE"]; reason: str
class RegimeDirective(BaseModel):
                             ts: datetime; regime: Literal["LONG_ONLY","SHORT_ONLY","BOTH","NO_TRADE"]
                             confidence: float; ttl_minutes: int; sources: list[str]; rationale: str
```

---

## 5. Engine state machine

App-level states (persisted, shown as dashboard pill):

```
DISARMED ──[ARM click + confirm]──► ARMED ──signals may trade──► (stays ARMED)
ARMED ──[DISARM click | abort criterion §PREREG-7]──► DISARMED (cancels working entry orders;
                                                       SL/TP of open position stay working)
ANY ──[KILL click]──► KILLED (cancel ALL orders; optional flatten checkbox; requires app restart to re-arm)
```

Per-trade decision lifecycle (each transition = one row in `decisions`):

```
BAR_CLOSED → SIGNAL | NO_SIGNAL
SIGNAL → RISK_PASS(order_plan) | RISK_REJECT(reason)
RISK_PASS → LLM_PASS | LLM_VETO(reason) | LLM_SKIPPED(gate off / fail-open)
LLM_PASS → SUBMITTED(ids) → FILLED | PARTIAL | CANCELLED | REJECTED
FILLED → position managed by bracket (SL/TP working server-side at IBKR)
EXIT fill → TRADE_CLOSED(pnl, exit_reason ∈ {SL, TP, TRAIL, SIGNAL_FLIP, MANUAL, KILL})
```

Rules (AMENDED 2026-07-06 per audit round):
- **Step 0 of every `on_bar`:** read the freshest broker position snapshot (fill-callback-updated
  cache), never a stale engine-local copy — an SL can fill between bar close and decision.
- **Post-await state gate:** after ANY `await` in the decision chain (LLM veto, broker call),
  re-read app-state + position immediately before `OrderManager.submit`; abort the decision if
  ARMED was lost, KILL fired, or the position changed. KILL/DISARM set a flag that short-circuits
  any in-flight decision — KILL is preemptive, never queued behind a pending order.
- Only ONE open position per symbol. **Flip is DISABLED in v1** (`allow_flip` removed from config;
  hardcoded false). Opposite signal while in position ⇒ close-only sequence: (1) cancel bracket
  children, (2) submit reduce-only MKT close sized to live position qty at submit time, (3) done —
  no new entry this bar. A flip sub-state machine is v1.1 (05_AUDIT_RESOLUTION).
- Trailing exit (trail_ema8) is engine-driven: each bar close, engine modifies the SL order price
  (see §6.1 modify path — same orderId, `auxPrice` only, never qty).
- **DISARMED with open position:** no new entries; existing SL/TP stay working; **trail
  modifications CONTINUE** — trail only tightens the stop (risk-reducing), freezing it would
  increase exposure. (Decided against the freeze alternative; see 05_AUDIT_RESOLUTION.)
- **DISARM side-effects:** cancel working entry orders, trigger an IMMEDIATE reconcile pass (not
  wait 60 s), and resize any working SL/TP to current filled qty (partial-entry + DISARM race).
- **KILLED persists:** `app_state` is stored in the `meta` table; a process restart comes up
  KILLED (not DISARMED) until explicit operator ack via `/api/kill/ack`. Restart always creates a
  NEW `run_id`; the old run's data is read-only journal history.
- **On restart:** Reconciler runs BEFORE ARM is possible (ARM button disabled with "Resolving
  broker state…" until reconcile completes). Adoption/flatten rules per §6.1 restart-recovery
  (re-protect first; own-orderRef only; foreign positions untouched + WARN).

---

## 6. Component specs

### 6.1 Broker protocol (`broker/base.py`)

```python
class Broker(Protocol):
    async def connect(self) -> None                     # raises BrokerRefusedLive if port 7496 without IBKR_LIVE_ACK
    async def account(self) -> AccountSnapshot          # equity, buying_power, currency
    async def positions(self) -> list[Position]
    async def open_orders(self) -> list[BrokerOrder]
    async def historical_bars(self, symbol, tf, lookback) -> list[Bar]
    def subscribe_bars(self, symbol, tf, on_bar_closed: Callback) -> None
    async def place_bracket(self, plan: OrderPlan) -> BracketIds   # parent + SL + optional TP, OCA
    async def modify_stop(self, order_id, new_stop: float) -> None
    async def cancel(self, order_id) -> None
    async def cancel_all(self) -> None
    async def flatten(self, symbol) -> None
```

`IBKRBroker` implementation notes (for the builder) — **AMENDED per audit round 2026-07-06
(see 05_AUDIT_RESOLUTION.md); this section is the binding contract:**

- Connection: `ib_async.IB()`; `connectAsync(host, port, clientId)`; set `ib.reqMarketDataType(3)`
  (delayed) **before** data requests — paper accounts without market-data subscription get
  delayed-15min; this is FINE for 1h bars and must not be treated as an error. Log the data type
  actually returned. clientId from env, default 17. clientId collision at **startup** = hard error;
  a transient same-id busy during **reconnect** = retry with backoff (they are different cases).
- **BarFinalizer contract (replaces naive "new bar object" detection):**
  - Exchange calendar: NYSE, timezone `America/New_York` (`zoneinfo`); RTH 09:30–16:00; hardcoded
    US holiday/half-day table in `config/nyse_calendar.yaml` for v1.
  - Bar key: `(symbol, tf, bar_end_ts_utc)`. Algorithm: keep `last_bar_ts`; on `updateEvent` with
    `hasNewBar` / `bars[-1].date > last_bar_ts` ⇒ emit `bars[-2]` as closed, advance `last_bar_ts`.
  - **Session-end force-close:** the last RTH bar has no successor until next session — a timer at
    session close (16:00 ET, or half-day close) force-finalizes it. Without this the last daily
    signal fires ~17.5 h late.
  - **RTH 1h alignment:** AAPL RTH = 6.5 h ⇒ the 15:30–16:00 tail bar is 30 min. v1 policy:
    **discard the tail bar** (no signal on it); the parity golden run must use the same policy.
    Bar-boundary convention (ts + OHLC) must be asserted identical to the golden fixture BEFORE
    signal parity is evaluated (two-stage parity, PREREG §6).
  - **Reconnect:** on every (re)connect, re-issue the historical stream + quote subscriptions
    (they do NOT survive TWS restart), then verify the next bar arrives within 1× timeframe else
    `DATA_STALE`. First bar after reconnect may duplicate the last pre-disconnect bar — dedupe by
    checking a decision for that `bar_ts` already exists (idempotency guard).
  - **P0 sub-check:** verify `keepUpToDate` actually streams under data type 3 on this TWS build;
    if not, fall back to polled `reqHistoricalData` on a session-aligned timer. Document which
    path P0 selected.
- **Bracket:** `ib.bracketOrder(...)`; if `entry_type == 'MKT'`, parent MarketOrder(transmit=False)
  + StopOrder + LimitOrder(TP) sharing `ocaGroup`, last child `transmit=True`. Placement sequence
  is exactly parent→SL→TP and is P0-tested (orphan-children is a known TWS footgun).
  **Modify path (trail):** fetch the LIVE order via `ib.trades()` by persisted id, change ONLY
  `auxPrice`, re-`placeOrder` with the SAME orderId — never construct a new order object for a
  modify (creates a duplicate stop + orphan). If the live order can't be found: cancel + re-place
  SL and re-establish OCA — fallback path, log WARN. **Never modify child qty on partial fills** —
  IBKR auto-scales OCA children when a parent is cancelled/partially filled; qty-modify races
  IBKR's own scaling (audit: Gemini F-02).
- **Durable order identity:** persist `perm_id`, `parent_perm_id`, `oca_group`, `client_id`,
  `transmit_role`, `order_ref` (= our `decision_uid:role` tag set via `orderRef`) and contract
  JSON on every order row. Local orderIds are NOT durable across TWS restarts; the Reconciler
  matches by `perm_id` first, then by `order_ref`, then conservative attribute fallback
  (symbol+action+type+auxPrice+qty). Ambiguous match ⇒ WARN event, do NOT flatten a
  sensible-looking bracket.
- **TWS nightly restart recovery (P2-critical):** TWS restarts ~23:45 ET and paper API orders may
  be dropped. On reconnect, if a position tagged with our `orderRef` exists WITHOUT a working SL:
  **first re-submit a protective bracket** for the existing position (config
  `recover_orders_after_restart: true`, default true for paper); only if that submit fails ⇒
  flatten per PREREG §7. Positions NOT tagged with our orderRef (manual/foreign) are never
  adopted and never flattened — WARN banner only.
- Reconnect loop: watch `ib.disconnectedEvent`; backoff 5→60 s; unattended recovery through the
  nightly restart is a P2 exit criterion.

`MockBroker`: in-memory; `historical_bars` reads CSV fixture `tests/fixtures/AAPL_1h.csv`;
`subscribe_bars` replays remaining fixture rows on an accelerated clock (config); fills:
MKT fills at next bar open; SL/TP fill when bar range crosses the level (SL priority on same bar,
pessimistic). Deterministic — used by pytest and by `--dry-run` app mode.

### 6.2 Strategy protocol + first strategy

```python
class Strategy(Protocol):
    id: str
    warmup_bars: int
    def on_bar(self, bars: Sequence[Bar], position: Position | None) -> Signal | None
    def trail_level(self, bars: Sequence[Bar], position: Position) -> float | None  # None = no change
```

`keltner_trail_ema8.py` — port of MCC `KELTNER_STOP_V1` entry × `trail_ema8` exit
(FAZ 3B Stage-1 STRONG_PASS variant). Builder: copy the exact rule + parameters from
`MTC_COMMAND_CENTER/03_QUANTLENS` FAZ 3B artifacts into the YAML at build time
(entry: Keltner channel breakout w/ stop-entry semantics → here simplified to close-confirmed
breakout at bar close, MKT next; exit: trailing stop at EMA(8) of closes, long: SL = max(SL, ema8)).
Parameters in `config/strategies/keltner_trail_ema8.yaml`:

```yaml
id: keltner_trail_ema8
version: 1.0.0
source: MTC/FAZ3B_stage1       # provenance only — no runtime link
symbol: AAPL
timeframe: 1h
params: { kc_length: 20, kc_mult: 2.0, atr_length: 20, trail_ema: 8 }
direction_default: BOTH        # dashboard can restrict; LLM regime can restrict further
permissions:                   # enforced by engine at load + ARM time
  paper_allowed: true
  live_allowed: false          # live ARM refuses strategies without this flag
  requires_human_approval: true
risk_overrides: {}             # optional per-strategy tightening of bridge.yaml risk (never loosening)
```

This is the **strategy import format**: future MTC-researched strategies are exported into a file
of this shape; the bridge validates permissions + risk_overrides at load and refuses live use
unless `live_allowed: true` (which only Barış sets by hand).

**Parity requirement:** the Python port must be replay-testable — `tests/test_strategy.py`
feeds fixture bars and asserts signal timestamps against a golden list generated once from the
QuantLens engine (builder generates golden via one offline run — this is a read-only comparison,
not a live link).

### 6.3 RiskEngine (`engine/risk.py`) — pure function, fully unit-tested

Inputs: Signal, AccountSnapshot, open position count, today's realized P&L, config.
Checks in order (first failure returns `Rejection(stage="RISK", reason=...)`):

1. App ARMED; symbol enabled; within trading session (RTH).
2. Direction allowed: `effective_direction = intersect(config.direction, regime.regime)`;
   empty intersection or NO_TRADE ⇒ reject.
3. No open position (or flip allowed).
4. Daily loss limit not hit: `realized_today + unrealized <= -max_daily_loss_pct * day_start_equity` ⇒ reject + auto-DISARM.
   **Trading day = America/New_York date.** `day_start_equity` snapshotted at the first RTH bar
   (or engine start if later) into the `risk_days` table. Engine-computed daily P&L is logged
   side-by-side with IBKR's `realizedPnL`; divergence > 1% ⇒ DISARM + alert (reconciliation bug).
4b. Consecutive-loss stop: last `max_consecutive_losses` realized trades all losers
   (**loss = pnl < 0 regardless of exit_reason** — trail scratches count) ⇒ reject + auto-pause.
   **Counter resets to 0 on: any winning trade, new trading day, manual re-ARM.**
   **Unattended policy (P2 fix):** config `on_consecutive_loss: disarm | pause_auto_rearm`
   (default `pause_auto_rearm`: auto re-ARM after cooldown, max `max_auto_rearms_per_day: 2`,
   then hard DISARM).
4c. Cooldown: within `cooldown_minutes_after_loss` of the last LOSING trade close (any
   exit_reason) ⇒ reject "cooldown_active". Evaluated independently of 4b.
5. Sizing (fixed fractional): `risk_dollars = equity * risk_pct_per_trade` (default 0.5%);
   `stop_distance = |ref_price - stop_loss|` from strategy's initial SL
   (Keltner: opposite band; fallback `atr_mult_sl * ATR`); `qty = floor(risk_dollars / stop_distance)`.
5a. **Stop-validity guards (BEFORE division):** reject if `stop_distance <= 0` (div-by-zero),
   `stop_distance < min_stop_distance` (default `max(tick, 0.1% of ref_price)` — tiny stop ⇒
   absurd qty), stop on the wrong side of price, or price already gapped through the stop.
6. Constraint clamps: `qty * ref_price <= max_position_notional_pct * equity` (default 20%);
   qty ≥ 1 else reject "size_below_minimum".
6b. **Buying-power check:** `qty * ref_price <= buying_power * 0.95` else reject
   `INSUFFICIENT_BUYING_POWER` (prevents avoidable broker rejects).
7. TP: `take_profit = ref_price ± rr_ratio * stop_distance` if `tp_mode: rr` (default rr 2.0);
   `tp_mode: none` ⇒ trail-only exit (matches trail_ema8 philosophy; DEFAULT for v1).

Output `OrderPlan` with the full arithmetic trace in `reason` (auditable).

**Gate-results exposure:** RiskEngine returns, alongside pass/reject, an ordered
`gate_results: list[{gate, status: PASS|WARN|BLOCK|SKIP, detail}]` covering every check above +
LLM gate + duplicate/stale checks. Stored in the decision payload and rendered as the dashboard
**Gate Monitor** card — "signal ≠ order" made visible: what passed, what blocked, why.

### 6.4 LLM layer (`engine/llm_gate.py`) — two roles, both risk-reducing only

**Role A — Regime directive (periodic, default every 4 h + on demand from dashboard):**
- Calls Grok (`grok-4`, xAI API, key `XAI_API_KEY`) with a fixed prompt: given symbol + recent
  headlines/X sentiment it retrieves, output STRICT JSON `RegimeDirective`
  (regime ∈ LONG_ONLY|SHORT_ONLY|BOTH|NO_TRADE, confidence 0-1, ttl_minutes, rationale, sources[]).
- Validation: non-JSON / invalid regime / confidence < `min_confidence` (default 0.6) ⇒ directive
  IGNORED, fall back to config direction, log `LLM_INVALID`. `ttl_minutes` is **clamped to
  [15, 1440]** — an LLM-chosen huge TTL cannot freeze a stale regime.
- **TTL expiry (no silent widen):** expiry triggers an immediate refresh attempt; until a new
  valid directive arrives, the LAST directive stays in force up to 2× its TTL; beyond that, fall
  back to `config.direction` + WARN event. Expiry never silently converts NO_TRADE into BOTH
  within the 2×TTL window (audit: Cursor F-13).
- Regime can only **narrow** what config allows — never widen (config LONG_ONLY + regime BOTH = LONG_ONLY).
- **Prompt-injection mitigation (audit: DeepSeek F-03):** every retrieved headline/post is
  truncated (280 chars), control-chars + markdown fences stripped, URLs removed, and wrapped in
  labeled `[SOURCE_START]…[SOURCE_END]` blocks; system prompt instructs the model to treat block
  contents as DATA, never instructions. `directives` stores the source-text HASH, not raw text.
  Worst-case injection = forced NO_TRADE (denial, not financial exploit) — narrowing-only holds.
- Keys are the bridge's OWN env vars (`XAI_API_KEY`, `ANTHROPIC_API_KEY`) read by `settings.py` —
  never shared with `_deepseek_driver`'s config lifecycle.
- YouTube/market-video sentiment: v1 ships Grok-only; the `sources` abstraction
  (`llm_gate.SentimentSource` protocol) leaves a slot for a YouTube-transcript source later.

**Role B — Pre-trade veto (per order; `llm.veto_enabled: false` DEFAULT in v1 — audit consensus):**
- v1 ships the veto path implemented behind `NullLLMGate` default; enabled at P1 after the hot
  path is proven. Rationale: a synchronous 10 s external call on the bar→order path is both
  latency-dangerous and non-protective when fail-open (Codex F-08, Copilot F-07, Cursor F-14).
- When enabled: Claude (`claude-sonnet-5` — verified current Anthropic model ID, ANTHROPIC_API_KEY)
  receives the OrderPlan JSON + last N decisions + current regime, answers STRICT JSON
  `{verdict: "PASS"|"VETO", reason: str}` with a checklist prompt (SL present? size arithmetic
  consistent? conflicts with regime? feed stale?).
- Runs **async with a hard decision deadline** (`llm.veto_deadline_s: 5`): if no verdict by
  deadline ⇒ `LLM_SKIPPED`, formal rule proceeds; the engine loop / fill handlers are NEVER
  blocked by the call. `fail_policy: closed` available but not default (Barış 2026-07-05).
- **Cost guards:** `llm.max_vetos_per_day: 20` and `llm.max_daily_llm_cost_usd: 5` — exceeded ⇒
  auto-skip with `LLM_COST_LIMIT` event.
- Every call logged to `llm_calls`: prompt hash, model, latency, verdict, token counts, cost est.

**Hard boundary (enforced in code, not prompt):** LLM outputs are parsed into the two models above;
there is NO code path from LLM output to qty, price, or new-order fields.

### 6.5 OrderManager (`engine/orders.py`)

- Owns mapping decision_id ↔ broker order ids; writes every `orderStatus`/fill event to Store.
- **Duplicate-order protection:** submit is idempotent per decision_id; additionally a signal
  fingerprint `(symbol, direction, bar_ts)` may submit at most once per run — re-delivery of the
  same bar/signal (reconnect replays) can never double-order.
- **Stale-DATA guard (reworked — audit: Cursor F-01):** under delayed data type 3 a tick-age
  check is meaningless (feed is 15 min behind by design). Freshness for the 1h path = **bar age**:
  at submit, the triggering bar's `end_ts` must be < 0.5× timeframe old AND the feed must not be
  in `DATA_STALE` state. Staleness comparisons use **data timestamps** (`ticker.time` /
  `bar.date`), never local receipt time. `max_price_age_s` applies only when real-time data
  (type 1) is active.
- **Close = reduce-only semantics:** exit paths (close-on-opposite-signal, flatten, trail) size
  orders to current position qty read at submit time, never a cached value — a close can never
  open the opposite side.
- **Partial fills (reworked — audit: Gemini F-02, Codex F-04):** explicit states
  `ENTRY_PARTIAL → CHILDREN_RESIZE_PENDING → PROTECTED | UNPROTECTED_ABORT`. On parent partial
  fill > 60 s: cancel the remainder and **let IBKR's OCA auto-scaling resize the children — never
  modify child qty manually**; verify children match filled qty within 10 s, else
  `UNPROTECTED_ABORT` ⇒ flatten. Out-of-order `orderStatus` callbacks must be tolerated
  (state transitions keyed by permId+status, idempotent).
- **Stale entry order:** unfilled entry older than `max_open_order_age_s` (default 600 s) ⇒
  cancel entry + children, log `ORDER_STALE_CANCELLED` (signal is no longer relevant).
- Watchdog: order not acked in 120 s ⇒ abort criterion (PREREG §7) ⇒ DISARM + alert row.
- **Reconciler (reworked — audit: Opus F-11/F-17):** coroutine (60 s) compares broker truth vs DB.
  Freshly submitted orders sit in a **PENDING grace state** excluded from reconciliation until
  age > 2× interval — no action on in-flight races. Naked-position detection ALSO runs
  event-driven on every fill/position callback (not only the 60 s tick). Flatten only positions
  traceable to our `orderRef`; foreign positions ⇒ WARN banner, never touched. Reconciler also
  snapshots equity every 60 s during RTH into `equity` (feeds max-intraday-DD, PREREG §5) and
  runs the engine-vs-broker equity divergence check (>0.5% ⇒ WARN, >1% ⇒ DISARM).

### 6.6 BarFeed staleness
During RTH, if now − last_bar_update > 2 × timeframe ⇒ `DATA_STALE` event ⇒ DISARM (PREREG §7).

### 6.7 Notifier (`engine/notify.py`) — optional, high value for unattended P2
Telegram bot (env `TELEGRAM_BOT_TOKEN` + `TELEGRAM_CHAT_ID`; both unset ⇒ notifier disabled,
no error). Sends: fills, trade closes (w/ P&L), every event severity ≥ WARN, DISARM/KILL,
regime changes. Fire-and-forget with 5 s timeout — notification failure NEVER blocks trading path.

---

## 7. SQLite schema (Store; all ts UTC ISO)

Schema v2 (AMENDED 2026-07-06 — audit consensus: decision grouping, durable broker identity,
PREREG §5 first-class columns, fills granularity, bars persistence, risk days, versioning):

```sql
CREATE TABLE meta      (key TEXT PK, value TEXT);            -- schema_version, app_state (KILLED persists), created_at
CREATE TABLE runs      (run_id TEXT PK, started_ts, ended_ts, mode TEXT CHECK(mode IN ('paper','dry_run','live')),
                        config_json TEXT);
CREATE TABLE bars      (symbol, tf, bar_end_ts, open, high, low, close, volume,
                        data_type INT,                       -- 1 realtime / 3 delayed
                        PRIMARY KEY(symbol, tf, bar_end_ts)); -- every finalized bar; chart + parity forensics served from here
CREATE TABLE decisions (id INTEGER PK, decision_uid TEXT NOT NULL, -- UUID shared by all stages of one decision
                        run_id, ts, symbol, stage TEXT,      -- SIGNAL/RISK_PASS/RISK_REJECT/LLM_PASS/LLM_VETO/LLM_SKIPPED/SUBMITTED/...
                        trade_id INT,                        -- filled at SUBMITTED stage onward
                        payload_json TEXT, payload_version INT DEFAULT 1);
CREATE TABLE orders    (order_id TEXT PK, perm_id INT, parent_perm_id INT, oca_group TEXT,
                        client_id INT, transmit_role TEXT, order_ref TEXT, -- our decision_uid:role tag
                        contract_json TEXT, decision_uid TEXT, trade_id INT,
                        role TEXT,                           -- ENTRY/SL/TP
                        status, qty, filled_qty, avg_fill_px, ts_submit, ts_last);
CREATE TABLE fills     (fill_id TEXT PK, order_id, decision_uid, fill_ts, qty, px, commission);
CREATE TABLE trades    (trade_id INTEGER PK, run_id, symbol, direction, qty,
                        entry_decision_uid TEXT,             -- joins the full reasoning chain
                        signal_ts, decision_ts, submit_ts, first_fill_ts, last_fill_ts,
                        expected_px, entry_px, entry_ts, exit_px, exit_ts, exit_reason,
                        pnl, slippage_bps_entry, risk_dollars, risk_pct,
                        sl_initial, tp_initial, llm_directive_id INT);
CREATE TABLE equity    (run_id, ts, equity, cash, unrealized, realized_today,
                        PRIMARY KEY(run_id, ts));            -- sampled every 60s during RTH → max intraday DD computable
CREATE TABLE risk_days (trading_date TEXT PK,                -- America/New_York date
                        day_start_equity, realized_pnl_engine, realized_pnl_ibkr,
                        max_intraday_dd, consecutive_losses_end, auto_rearms_used);
CREATE TABLE directives(id INTEGER PK, ts, regime, confidence, ttl_minutes, rationale,
                        sources_hash TEXT,                   -- hash, not raw text (injection/leak hygiene)
                        raw_response TEXT, valid INT);
CREATE TABLE llm_calls (id INTEGER PK, ts, role TEXT,        -- regime/veto
                        model, prompt_hash, latency_ms, verdict, tokens_in, tokens_out, cost_est);
CREATE TABLE events    (id INTEGER PK, run_id, ts, severity TEXT, code TEXT, detail TEXT); -- DISCONNECT/RECONNECT/DATA_STALE/RECON_MISMATCH/CONFIG_CHANGED/KILL/...

CREATE INDEX idx_decisions_uid  ON decisions(decision_uid);
CREATE INDEX idx_decisions_run  ON decisions(run_id, ts);
CREATE INDEX idx_orders_permid  ON orders(perm_id);
CREATE INDEX idx_orders_trade   ON orders(trade_id);
CREATE INDEX idx_fills_order    ON fills(order_id);
CREATE INDEX idx_trades_run     ON trades(run_id);
CREATE INDEX idx_events_run_sev ON events(run_id, severity, ts);
```

Conventions: storage = UTC ISO; RTH/trading-day logic = America/New_York; display = ET.
`meta.schema_version` gates inline migrations. On PUT /api/config while ARMED, an events row
`CONFIG_CHANGED` records the field-level diff (old→new) so the journal shows context changes.

`decisions.payload_json` is the audit trail Barış asked for (thesis-history idea from the video,
adapted: every trade's full reasoning chain reconstructable by decision_id).

---

## 8. API (FastAPI)

REST (all JSON):
```
GET  /api/status            app state, broker conn, mode, data type, regime, account snapshot
GET  /api/config            merged config          PUT /api/config   validated runtime overrides
POST /api/arm  /api/disarm  /api/kill?flatten=bool
POST /api/regime/refresh    force LLM regime call
GET  /api/positions  /api/orders  /api/trades?limit=  /api/decisions?trade_id=  (joins via decision_uid)
GET  /api/equity?from=      equity curve
GET  /api/events?severity=
GET  /api/bars?n=300        from the bars TABLE (not a live broker call); shape:
                            {"bars":[{"time":unix_s,"open":..,"high":..,"low":..,"close":..,"volume":..}]}
                            (lightweight-charts native format; empty [] + UI spinner before warmup)
GET  /api/gates/latest      structured gate_results of the most recent decision (Gate Monitor source)
GET  /api/snapshot          one-shot full state: status+positions+orders+last trades+latest gates
GET  /api/runs/{run_id}     run record incl. config snapshot (System page)
POST /api/kill/ack          operator ack to leave persisted KILLED state after restart
```
WS `/ws`: server pushes `{topic, data}` for topics: `status`, `bar`, `decision`, `order`,
`position`, `equity`, `directive`, `event`. **Reconnect contract (audit):** on every WS `open`,
the server immediately pushes a full `snapshot` message (same payload as GET /api/snapshot);
the client re-renders from it — no missed-DISARM/fill gaps after tab sleep or network blips.
`status` also carries a monotonic `state_version`.

Confirmation model (AMENDED — audit: Opus F-10, Codex F-10):
- Mutating ops (ARM, PUT config while ARMED) require header `X-Confirm: <state_version>`;
  server rejects if it doesn't match current version (stale tab). Version is pushed on every
  WS status update, so an open dashboard always holds the current one.
- **KILL and DISARM are NEVER nonce-blocked** — safety actions must not fail on stale UI state.
  KILL uses its own two-step confirm (modal) client-side only.

---

## 9. Dashboard spec (professional; single dark theme)

Design language: near-black `#0d1117` bg, panel `#161b22`, border `#30363d`, text `#e6edf3`,
green `#3fb950` / red `#f85149` / amber `#d29922` accents, `Inter` + `JetBrains Mono` (numbers).
Layout: fixed left sidebar (nav + ARM/DISARM/KILL block), topbar (conn pill, mode pill
`PAPER` amber / `DRY-RUN` blue, regime pill, equity ticker), content grid.

Pages (hash-routed, one `app.js`):
1. **Overview** — equity curve (lightweight-charts), day P&L card, open position card (entry, SL,
   TP, unrealized, trail level), last-10 decisions stream, regime card (regime, confidence,
   countdown to TTL, rationale, refresh button), **Gate Monitor card** — last signal's full gate
   breakdown (§6.3 gate_results): green PASS / amber WARN / red BLOCK / grey SKIP per gate, with
   block reason text. Makes "signal ≠ order" visible at a glance.
2. **Strategy & Risk config** — strategy select (v1: one), symbol, timeframe (read-only v1),
   direction (BOTH/LONG/SHORT), risk % per trade, tp_mode (none/rr) + rr, max daily loss %,
   max notional %, allow_flip, LLM toggles (regime on/off, veto on/off, fail policy, min confidence).
   Save = PUT /api/config; changes while ARMED require confirm modal. **This mirrors the MTC_V2
   settings mental model Barış asked for (risk/SL/TP/money-management/direction in one panel).**
3. **Trading** — price chart w/ entry/SL/TP lines + trade markers; working orders table; positions
   table; manual actions: cancel order, flatten (confirm modal).
4. **Journal** — trades table (all PREREG §5 per-trade fields); click row → decision-chain drawer
   (SIGNAL → RISK → LLM → orders → fills, each with payload JSON pretty-printed).
5. **LLM** — directives history, veto log w/ reasons, call latency/token stats.
6. **System** — events log w/ severity filter, broker connection history, data staleness, DB size,
   config snapshot of the running `run_id`.

Kill switch: red button, sidebar bottom, always visible, double-confirm modal with "flatten
positions" checkbox. DISARMED state = amber banner across every page. KILLED = red banner.

---

## 10. Config (`config/bridge.yaml` defaults)

```yaml
mode: paper                    # paper | dry_run | live (live additionally needs --enable-live CLI flag + IBKR_LIVE_ACK env)
broker:
  host: 127.0.0.1
  port: 7497                   # allow-list {7497 TWS-paper, 4002 Gateway-paper}; ANY other port refused w/o live triple-lock
  client_id: 17
  market_data_type: 3
  recover_orders_after_restart: true   # re-protect naked position after TWS nightly restart before considering flatten
strategy_file: strategies/keltner_trail_ema8.yaml
risk:
  risk_pct_per_trade: 0.005
  max_daily_loss_pct: 0.02
  max_position_notional_pct: 0.20
  min_stop_distance_pct: 0.001 # 0.1% of ref_price floor (div-by-zero / absurd-qty guard)
  max_consecutive_losses: 3    # losers = pnl<0, any exit_reason; resets on win / new day / manual re-ARM
  on_consecutive_loss: pause_auto_rearm   # or: disarm (manual re-arm; breaks unattended P2)
  max_auto_rearms_per_day: 2
  cooldown_minutes_after_loss: 120
  max_open_order_age_s: 600    # cancel unfilled entries past relevance
  max_price_age_s: 90          # applies only when data_type==1 (realtime); delayed mode uses bar-age staleness
  tp_mode: none                # trail-only default
  rr_ratio: 2.0
notify: { telegram_enabled: true, heartbeat_hours: 6 }   # tokens from env; unset = silently disabled
llm:
  regime_enabled: true
  regime_refresh_minutes: 240
  min_confidence: 0.6
  ttl_clamp_minutes: [15, 1440]
  veto_enabled: false          # v1 default OFF (audit consensus); enable at P1
  veto_deadline_s: 5
  max_vetos_per_day: 20
  max_daily_llm_cost_usd: 5
  fail_policy: open            # open = formal rule proceeds on LLM failure
  regime_model: grok-4
  veto_model: claude-sonnet-5
server: { host: 127.0.0.1, port: 8790 }   # CORS restricted to 127.0.0.1 origins
```

---

## 11. Safety rails summary (enforced in code)

1. **Default-DENY port allow-list (AMENDED — audit: Opus F-01, the headline finding):** only paper
   ports `{7497 (TWS paper), 4002 (IB Gateway paper)}` are connectable. ANY other port — 7496
   (TWS live), **4001 (Gateway live — the standard unattended setup, missed by a 7496-only
   block-list)**, or custom — raises `BrokerRefusedLive`. Live requires the triple-lock:
   `--enable-live` CLI flag + `IBKR_LIVE_ACK=I_UNDERSTAND_THIS_IS_REAL_MONEY` env + strategy
   `live_allowed: true`. `broker.port` is NOT runtime-editable via PUT /api/config (yaml-only,
   restart required).
2. `mode: live` additionally requires dashboard double-confirm at ARM. v1 acceptance never uses it.
3. LLM outputs structurally cannot create/enlarge orders (§6.4 hard boundary).
4. Every abort criterion (PREREG §7) wired to auto-DISARM + red event.
5. Startup with unreconcilable broker state ⇒ start DISARMED with banner (never auto-trade into unknown state).
6. Secrets only from env; never logged; `data/` git-ignored.
7. This app never writes into `MTC_COMMAND_CENTER/` and never imports from it at runtime.
8. Dashboard renders ALL payload/log fields via `textContent` / `<pre>` — never `innerHTML`
   (XSS via strategy reason / event detail strings; audit: DeepSeek F-22).
9. FastAPI `CORSMiddleware` restricted to `127.0.0.1` origins; server binds 127.0.0.1 only.
10. Store redacts `(api.?key|token|secret|bearer)`-matching content from any persisted raw LLM
    response (no-op in v1, future-proofing).

## 12. Relationship to MCC / existing tracks

- Independent top-level app per Barış 2026-07-05. Shares the repo for versioning only.
- SYSTEM_TEST vertical slice (V1.1, closed) proved localhost signal plumbing; this bridge is the
  broker-facing successor track, with its own PREREG gates (P0-P3).
- Paper results feed BACK to MCC only as a written report (P3 slippage + parity report into
  `MTC_COMMAND_CENTER/11_TRIAGE/`), never as automatic promotion evidence.

## 13. Roadmap beyond v1 (ideas adopted from `live_trading_dashboard_final_report.md`, 2026-07-05)

Reviewed Barış's external design report; adopted into v1: gate monitor, duplicate-order +
stale-price guards, consecutive-loss stop + cooldown, strategy import format w/ permissions,
Telegram notifier. Deliberately DEFERRED (would break the 1-day build; revisit after P2):

| Idea | When | Note |
|---|---|---|
| Manual Execution Ticket (risk-calculated manual orders w/ gate check) | v1.1 | v1 has only cancel/flatten manual actions. |
| Event gate (CPI/FOMC/earnings block) | v1.1 | Partially covered by LLM regime NO_TRADE; a calendar-based hard gate is better — needs an events data source. |
| Market Context page (movers, funding, OI, sentiment) | v2 | Context layer only, never an order trigger. |
| Additional connectors (Binance/Bybit/Hyperliquid via direct HTTP/WS) | v2 | `Broker` protocol (§6.1) is already the abstraction seam; crypto connectors don't need a local terminal. |
| Postgres + Redis + Docker Compose | v2 / multi-strategy | SQLite + 1 process is correct at v1 scale; migrate when >1 strategy or VPS. |
| React/Next frontend | only if vanilla JS hits a wall | No build step is a feature for AI-driven iteration. |
| Login + 2FA + roles | REQUIRED before any non-localhost exposure | v1 binds to 127.0.0.1 only. |
| Deployment: local → Cloudflare Tunnel/Tailscale (monitor-only) → VPS | after P2 | IBKR needs local TWS/Gateway ⇒ end-state is hybrid: cloud dashboard + local execution bridge, OR IB Gateway on the VPS itself. **Tunnel phase is STRICTLY monitor-only: ARM/DISARM/KILL and config edits are ALL blocked remotely until login+2FA ships** (audit: Cursor F-19 — an unauthenticated tunnel URL holder must not be able to trade). |
| Multi-strategy portfolio + correlation/exposure gates | v2 | Requires portfolio-level risk engine (max correlated exposure, per-strategy caps — import format's `risk_overrides` is the hook). |
