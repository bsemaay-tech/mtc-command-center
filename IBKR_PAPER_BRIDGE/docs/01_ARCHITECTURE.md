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

Rules:
- Only ONE open position per symbol. New opposite signal while in position ⇒ close-then-open
  only if config `allow_flip: true`, else just close.
- Trailing exit (trail_ema8) is engine-driven: each bar close, if trail condition hits, engine
  replaces the SL order (modify, not cancel+new, to keep OCA intact).
- On restart: Reconciler loads open orders/positions from broker, matches against `orders` table,
  adopts unknown position into managed state IF it has matching working SL, else abort-flattens (PREREG §7).

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

`IBKRBroker` implementation notes (for the builder):
- `ib_async.IB()`; `connectAsync(host, port, clientId)`; set `ib.reqMarketDataType(3)` (delayed)
  **before** data requests — paper accounts without market-data subscription get delayed-15min;
  this is FINE for 1h bars and must not be treated as an error. Log the data type actually returned.
- Bars: `reqHistoricalData(..., keepUpToDate=True)` with `barSizeSetting='1 hour'`,
  `useRTH=True`, `whatToShow='TRADES'`. The updateEvent fires on partial bars — only emit
  `on_bar_closed` when a NEW bar object appears (previous bar is then final).
- Bracket: `ib.bracketOrder(action, qty, limitPrice, takeProfitPrice, stopLossPrice)` then
  place all three; if `entry_type == 'MKT'`, build manually: parent MarketOrder(transmit=False)
  + StopOrder + LimitOrder(TP) sharing `ocaGroup`, last child `transmit=True`.
- Reconnect: watch `ib.disconnectedEvent`; retry loop with backoff 5→60 s; TWS restarts nightly
  (~23:45 exchange time) — reconnect + Reconciler must recover unattended (PREREG Gate P2 criterion).
- clientId from env, default 17; collision with another API client is a startup error, not a retry.

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
symbol: AAPL
timeframe: 1h
params: { kc_length: 20, kc_mult: 2.0, atr_length: 20, trail_ema: 8 }
direction_default: BOTH        # dashboard can restrict; LLM regime can restrict further
```

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
5. Sizing (fixed fractional): `risk_dollars = equity * risk_pct_per_trade` (default 0.5%);
   `stop_distance = |ref_price - stop_loss|` from strategy's initial SL
   (Keltner: opposite band; fallback `atr_mult_sl * ATR`); `qty = floor(risk_dollars / stop_distance)`.
6. Constraint clamps: `qty * ref_price <= max_position_notional_pct * equity` (default 20%);
   qty ≥ 1 else reject "size_below_minimum".
7. TP: `take_profit = ref_price ± rr_ratio * stop_distance` if `tp_mode: rr` (default rr 2.0);
   `tp_mode: none` ⇒ trail-only exit (matches trail_ema8 philosophy; DEFAULT for v1).

Output `OrderPlan` with the full arithmetic trace in `reason` (auditable).

### 6.4 LLM layer (`engine/llm_gate.py`) — two roles, both risk-reducing only

**Role A — Regime directive (periodic, default every 4 h + on demand from dashboard):**
- Calls Grok (`grok-4`, xAI API, key `XAI_API_KEY`) with a fixed prompt: given symbol + recent
  headlines/X sentiment it retrieves, output STRICT JSON `RegimeDirective`
  (regime ∈ LONG_ONLY|SHORT_ONLY|BOTH|NO_TRADE, confidence 0-1, ttl_minutes, rationale, sources[]).
- Validation: non-JSON / invalid regime / confidence < `min_confidence` (default 0.6) ⇒ directive
  IGNORED, fall back to `BOTH`, log `LLM_INVALID`. Expired TTL ⇒ `BOTH`.
- Regime can only **narrow** what config allows — never widen (config LONG_ONLY + regime BOTH = LONG_ONLY).
- YouTube/market-video sentiment: v1 ships Grok-only; the `sources` abstraction
  (`llm_gate.SentimentSource` protocol) leaves a slot for a YouTube-transcript source later.

**Role B — Pre-trade veto (per order, only if `llm.veto_enabled: true`):**
- Claude (`claude-sonnet-5`, ANTHROPIC_API_KEY) receives the OrderPlan JSON + last N decisions +
  current regime, answers STRICT JSON `{verdict: "PASS"|"VETO", reason: str}` with a checklist
  prompt (SL present? size arithmetic consistent? conflicts with regime? symbol halted per feed staleness?).
- Timeout 10 s. **Fail-open** (`llm.fail_policy: open`, default): timeout/error ⇒ `LLM_SKIPPED`,
  trade proceeds per formal rule. `fail_policy: closed` available but not default (per Barış 2026-07-05).
- Every call logged: prompt hash, latency, verdict, tokens.

**Hard boundary (enforced in code, not prompt):** LLM outputs are parsed into the two models above;
there is NO code path from LLM output to qty, price, or new-order fields.

### 6.5 OrderManager (`engine/orders.py`)

- Owns mapping decision_id ↔ broker order ids; writes every `orderStatus`/fill event to Store.
- Bracket submit; on partial fill > 60 s, cancel remainder, keep SL sized to filled qty (modify).
- Watchdog: order not acked in 120 s ⇒ abort criterion (PREREG §7) ⇒ DISARM + alert row.
- Reconciler coroutine (60 s): `broker.positions() ∪ open_orders()` vs DB expectations; any
  divergence ⇒ `events` row severity=WARN and dashboard banner; naked position ⇒ flatten (PREREG §7).

### 6.6 BarFeed staleness
During RTH, if now − last_bar_update > 2 × timeframe ⇒ `DATA_STALE` event ⇒ DISARM (PREREG §7).

---

## 7. SQLite schema (Store; all ts UTC ISO)

```sql
CREATE TABLE runs      (run_id TEXT PK, started_ts, mode TEXT CHECK(mode IN ('paper','dry_run','live')),
                        config_json TEXT);
CREATE TABLE decisions (id INTEGER PK, run_id, ts, symbol, stage TEXT,      -- SIGNAL/RISK_PASS/RISK_REJECT/LLM_PASS/LLM_VETO/LLM_SKIPPED/SUBMITTED/...
                        payload_json TEXT);                                  -- full model dump of that stage
CREATE TABLE orders    (order_id TEXT PK, decision_id INT, role TEXT,        -- ENTRY/SL/TP
                        status, qty, filled_qty, avg_fill_px, ts_submit, ts_last);
CREATE TABLE trades    (trade_id INTEGER PK, run_id, symbol, direction, qty, entry_px, entry_ts,
                        exit_px, exit_ts, exit_reason, pnl, slippage_bps_entry, risk_dollars);
CREATE TABLE equity    (ts PK, equity, cash, unrealized, realized_today);
CREATE TABLE directives(id INTEGER PK, ts, regime, confidence, ttl_minutes, rationale, sources_json,
                        raw_response TEXT, valid INT);
CREATE TABLE events    (id INTEGER PK, ts, severity TEXT, code TEXT, detail TEXT); -- DISCONNECT/RECONNECT/DATA_STALE/RECON_MISMATCH/KILL/...
```

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
GET  /api/positions  /api/orders  /api/trades?limit=  /api/decisions?trade_id=
GET  /api/equity?from=      equity curve
GET  /api/events?severity=
GET  /api/bars?n=300        recent bars for chart
```
WS `/ws`: server pushes `{topic, data}` for topics: `status`, `bar`, `decision`, `order`,
`position`, `equity`, `directive`, `event`. Dashboard is fully WS-driven after initial REST load.

Dangerous ops (`/api/arm`, `/api/kill`, PUT config while ARMED) require header
`X-Confirm: <app_state_nonce>` returned by `/api/status` — prevents stale-tab accidents.

---

## 9. Dashboard spec (professional; single dark theme)

Design language: near-black `#0d1117` bg, panel `#161b22`, border `#30363d`, text `#e6edf3`,
green `#3fb950` / red `#f85149` / amber `#d29922` accents, `Inter` + `JetBrains Mono` (numbers).
Layout: fixed left sidebar (nav + ARM/DISARM/KILL block), topbar (conn pill, mode pill
`PAPER` amber / `DRY-RUN` blue, regime pill, equity ticker), content grid.

Pages (hash-routed, one `app.js`):
1. **Overview** — equity curve (lightweight-charts), day P&L card, open position card (entry, SL,
   TP, unrealized, trail level), last-10 decisions stream, regime card (regime, confidence,
   countdown to TTL, rationale, refresh button).
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
mode: paper                    # paper | dry_run | live(refused w/o IBKR_LIVE_ACK)
broker: { host: 127.0.0.1, port: 7497, client_id: 17, market_data_type: 3 }
strategy_file: strategies/keltner_trail_ema8.yaml
risk:
  risk_pct_per_trade: 0.005
  max_daily_loss_pct: 0.02
  max_position_notional_pct: 0.20
  tp_mode: none                # trail-only default
  rr_ratio: 2.0
  allow_flip: false
llm:
  regime_enabled: true
  regime_refresh_minutes: 240
  min_confidence: 0.6
  veto_enabled: true
  fail_policy: open            # open = formal rule proceeds on LLM failure
  regime_model: grok-4
  veto_model: claude-sonnet-5
server: { host: 127.0.0.1, port: 8790 }
```

---

## 11. Safety rails summary (enforced in code)

1. Port 7496 (live) ⇒ `BrokerRefusedLive` unless env `IBKR_LIVE_ACK=I_UNDERSTAND_THIS_IS_REAL_MONEY`.
2. `mode: live` additionally requires dashboard double-confirm at ARM. v1 acceptance never uses it.
3. LLM outputs structurally cannot create/enlarge orders (§6.4 hard boundary).
4. Every abort criterion (PREREG §7) wired to auto-DISARM + red event.
5. Startup with unreconcilable broker state ⇒ start DISARMED with banner (never auto-trade into unknown state).
6. Secrets only from env; never logged; `data/` git-ignored.
7. This app never writes into `MTC_COMMAND_CENTER/` and never imports from it at runtime.

## 12. Relationship to MCC / existing tracks

- Independent top-level app per Barış 2026-07-05. Shares the repo for versioning only.
- SYSTEM_TEST vertical slice (V1.1, closed) proved localhost signal plumbing; this bridge is the
  broker-facing successor track, with its own PREREG gates (P0-P3).
- Paper results feed BACK to MCC only as a written report (P3 slippage + parity report into
  `MTC_COMMAND_CENTER/11_TRIAGE/`), never as automatic promotion evidence.
