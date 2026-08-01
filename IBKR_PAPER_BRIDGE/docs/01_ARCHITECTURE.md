# ARCHITECTURE — Crypto Paper Bridge (Hyperliquid) v1

Design: Claude Fable 5, 2026-07-05; **broker decision finalized to Hyperliquid 2026-07-06**
(see `07_BROKER_DECISION.md` — IBKR and Signum evaluated and NOT chosen). Everything here is
decided — the builder should NOT re-litigate stack choices; deviations require a dated note in
this file. Directory is still named `IBKR_PAPER_BRIDGE/` for git-history continuity only; the
product is the **Crypto Paper Bridge** and the live broker is **Hyperliquid** (testnet = paper).

---

## 0. Why Hyperliquid (one paragraph — full record in 07_BROKER_DECISION.md)

IBKR was closed (North-Cyprus address verification failed; TWS/Gateway desktop-middleware
complexity). Signum was evaluated in depth (it is a good execution relay, signal-source-agnostic,
even supports your own strategy) but it places **market orders only with NO native resting stop**
(its "stop" is a strategy-fired market exit, 5–10 s latency, single point of failure) and adds a
vendor + monthly fee; routing our engine through it would neuter the risk engine. **Hyperliquid is
API-first (no desktop terminal), has native resting stop/TP trigger orders (real on-book
protection), a testnet that is our paper environment, runs 24/7 (faster P2, no session/holiday
complexity), and its API wallet cannot withdraw (built-in safety).** It is the truest fit for our
broker-abstracted design with the least loss of the risk engine.

---

## 1. Stack (decided)

| Layer | Choice | Why |
|---|---|---|
| Language | Python 3.11+ | Repo standard; Hyperliquid SDK is Python. |
| Exchange API | **`hyperliquid-python-sdk`** (official `hyperliquid` package): `Info` (read: user_state, candles, meta) + `Exchange` (write: signed orders) + WebSocket (live candles, fills, user events). Fallback: raw HTTP to `/info` + `/exchange` with `eth-account` signing. | API-first, no desktop terminal, native trigger (SL/TP) orders, WS live data. |
| Auth | **API wallet (agent wallet)** created in the Hyperliquid UI — can trade, **cannot withdraw**. Env: `HL_ACCOUNT_ADDRESS` (main), `HL_API_WALLET_KEY` (agent private key). | Withdrawal-disabled by construction — the strongest secret-safety property. |
| Backend | FastAPI + uvicorn, single process, asyncio | One event loop shares exchange connection + engine + WebSocket. No Celery/Redis. |
| Persistence | SQLite (WAL mode), file `data/bridge.db` | Zero-ops, transactional, good for 1 strategy. All writes via one `Store` class. |
| Frontend | Static vanilla HTML/CSS/JS served by FastAPI (`/static`), WebSocket for live updates. **No build step, no npm.** | Fast to build; professional dark theme (§9). Chart: lightweight-charts via CDN. |
| Config | YAML under `config/` + runtime overrides from dashboard persisted to `data/runtime_config.json` | Human-diffable base + UI-editable runtime. |
| Scheduler | asyncio tasks (no APScheduler) | Bar clock, LLM refresh, reconciliation — periodic coroutines. |
| LLM | Anthropic API (Claude, `claude-sonnet-5`) for veto/summary; **xAI Grok** (`grok-4`) for market-sentiment regime | Grok has X/news access; Claude for structured veto. Both optional. |

Process model: **one process** `python -m bridge.app`. No external terminal — Hyperliquid is a
pure API (this is the whole reason the design simplifies vs IBKR).

---

## 2. Directory layout

```
IBKR_PAPER_BRIDGE/            (legacy dir name; product = Crypto Paper Bridge)
  README.md
  docs/                       (these design docs)
  requirements.txt            fastapi, uvicorn[standard], hyperliquid-python-sdk, eth-account, pydantic>=2, pyyaml, httpx, anthropic
  config/
    bridge.yaml               app config (network, mode, leverage, LLM on/off)
    strategies/
      keltner_trail_ema8.yaml
  bridge/
    app.py                    FastAPI factory + lifespan: start engine, ws manager
    settings.py               pydantic-settings; env: HL_ACCOUNT_ADDRESS, HL_API_WALLET_KEY, ANTHROPIC_API_KEY, XAI_API_KEY, HL_LIVE_ACK
    broker/
      base.py                 Broker protocol (abstract)
      hyperliquid.py          HyperliquidBroker (hyperliquid-python-sdk impl)
      mock.py                 MockBroker (deterministic sim fills; tests + dry-run mode)
    engine/
      engine.py               main loop orchestrator (state machine §5)
      bars.py                 BarFeed: historical warmup + live WS candles
      strategy_base.py        Strategy protocol
      strategies/
        keltner_trail_ema8.py
      risk.py                 RiskEngine
      llm_gate.py             regime directive + pre-trade veto
      orders.py               OrderManager (bracket = entry + tp/sl trigger group, reconciliation)
      notify.py               Telegram notifier
    store/
      db.py                   SQLite Store, schema §7, inline migrations
    api/
      routes.py               REST endpoints §8
      ws.py                   WebSocket hub (topic-based push)
    static/
      index.html  app.css  app.js
  tests/
    test_store.py  test_risk.py  test_strategy.py  test_order_manager_mock.py  test_engine_dryrun.py  test_llm_gate.py
  data/                       (git-ignored) bridge.db, runtime_config.json, logs/
```

Add to repo root `.gitignore`: `IBKR_PAPER_BRIDGE/data/`.

---

## 3. Dataflow (end to end)

```
Hyperliquid testnet  (WS candles + user events)
   │ hyperliquid-python-sdk
   ▼
BarFeed ──bar closed──► Engine.on_bar()
                          │ 1. Strategy.on_bar(bars) → Signal | None
                          │ 2. RiskEngine.size(signal, account, config) → OrderPlan | Rejection
                          │ 3. LLMGate.check(order_plan, regime) → PASS | VETO(reason)
                          │ 4. OrderManager.submit(entry + tp/sl trigger group) → order ids
                          ▼
                        Store (every step = one JSON decision row)
                          │
                          ▼
                        WS hub ──push──► Dashboard
LLM regime task (period: config, default 4h) ──► regime directive row + WS push
Reconciler task (60s) ──► positions/orders truth sync vs exchange
```

Signal path is **synchronous per bar** — no queues. One coin × one strategy in v1 keeps this trivial.

---

## 4. Core types (pydantic models, `bridge/engine/types.py`)

```python
class Bar(BaseModel):        ts: datetime; open: float; high: float; low: float; close: float; volume: float
class Signal(BaseModel):     ts: datetime; symbol: str; direction: Literal["LONG","SHORT","FLAT"]
                             reason: str                       # human-readable rule trace
                             ref_price: float                  # bar close at signal
class OrderPlan(BaseModel):  signal: Signal; qty: float; entry_type: Literal["MKT","LMT"]  # qty float — crypto fractional, rounded to szDecimals
                             limit_price: float | None; stop_loss: float; take_profit: float | None
                             leverage: int; risk_dollars: float; risk_pct: float
class Position(BaseModel):   symbol: str; size: float; entry_px: float; unrealized: float
                             leverage: int; liquidation_px: float | None; margin_used: float
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
                                                       SL/TP triggers of open position stay working)
ANY ──[KILL click]──► KILLED (latch first; owned-only cancel; optional exact-owned flatten;
                              evidence-gated ACK reaches DISARMED, never ARMED)
```

Per-trade decision lifecycle (each transition = one row in `decisions`):

```
BAR_CLOSED → SIGNAL | NO_SIGNAL
SIGNAL → RISK_PASS(order_plan) | RISK_REJECT(reason)
RISK_PASS → LLM_PASS | LLM_VETO(reason) | LLM_SKIPPED(gate off / fail-open)
LLM_PASS → SUBMITTED(ids) → FILLED | PARTIAL | CANCELLED | REJECTED
FILLED → position protected by native SL/TP trigger orders (resting on Hyperliquid, reduce-only)
EXIT fill → TRADE_CLOSED(pnl, exit_reason ∈ {SL, TP, TRAIL, SIGNAL_FLIP, MANUAL, KILL, LIQUIDATION})
```

Rules (AMENDED 2026-07-06 per audit round; Hyperliquid-adapted):
- **Step 0 of every `on_bar`:** read the freshest exchange position snapshot (fill-callback-updated
  cache), never a stale engine-local copy — an SL trigger can fill between bar close and decision.
- **Post-await state gate:** after ANY `await` in the decision chain (LLM veto, exchange call),
  re-read app-state + position immediately before `OrderManager.submit`; abort the decision if
  ARMED was lost, KILL fired, or the position changed. KILL/DISARM set a flag that short-circuits
  any in-flight decision — KILL is preemptive, never queued behind a pending order.
- Only ONE open position per coin. **Flip is DISABLED in v1** (`allow_flip` removed; hardcoded
  false). Opposite signal while in position ⇒ close-only sequence: (1) cancel the tp/sl trigger
  group, (2) submit reduce-only MKT close sized to live position qty at submit time, (3) done — no
  new entry this bar. A flip sub-state machine is v1.1 (05_AUDIT_RESOLUTION).
- Trailing exit (trail_ema8) is engine-driven: each bar close, engine **modifies the SL trigger's
  `triggerPx`** (see §6.1 modify path — same cloid, price only, never qty).
- **DISARMED with open position:** no new entries; existing SL/TP triggers stay working; **trail
  modifications CONTINUE** — trail only tightens the stop (risk-reducing); freezing it would
  increase exposure. (Decided against freeze; see 05_AUDIT_RESOLUTION.)
- **DISARM side-effects:** cancel working entry orders, trigger an IMMEDIATE reconcile pass (not
  wait 60 s), and confirm the SL/TP triggers match current position qty.
- **KILLED persists:** on opt-in schema v9, `app_state`, the active episode pointer, immutable
  request/action identity and append-only broker/query evidence survive restart. Restart resumes
  UNKNOWN or reserved actions by querying the same identity; it never resends without direct
  `NOT_APPLIED` proof and never auto-ACKs or auto-ARMs. Explicit `/api/kill/ack` requires a fresh
  current accepted reconciliation checkpoint bound to the safe terminal proof and reaches
  DISARMED. Pre-v9 stores retain the KILLED latch but cannot perform or ACK the v9 coordinator.
- **On restart / reconnect:** Reconciler runs BEFORE ARM is possible (ARM button disabled with
  "Resolving exchange state…" until reconcile completes). Adoption/re-protect rules per §6.1
  (re-protect first; own-cloid only; foreign positions untouched + WARN).

---

## 6. Component specs

### 6.1 Broker protocol (`broker/base.py`)

```python
class Broker(Protocol):
    async def connect(self) -> None                     # raises BrokerRefusedLive if network=mainnet without the triple-lock
    async def account(self) -> AccountSnapshot          # equity(USDC), available_margin, withdrawable
    async def positions(self) -> list[Position]
    async def open_orders(self) -> list[BrokerOrder]
    async def historical_bars(self, coin, tf, lookback) -> list[Bar]
    def subscribe_bars(self, coin, tf, on_bar_closed: Callback) -> None
    async def place_bracket(self, plan: OrderPlan) -> BracketIds   # entry + SL trigger + optional TP trigger (normalTpsl group)
    async def modify_stop(self, cloid, new_stop: float) -> None
    async def cancel(self, cloid) -> None
    async def cancel_all(self) -> None
    async def flatten(self, coin) -> None
```

TS-P1-009 does not change those broad legacy methods. Its separate
`KillRecoveryBroker` capability uses only `lot_unit`, exact `symbol_snapshot`, direct
`query_order`, `cancel_order_by_cloid`, and exact-size `flatten_reduce_only`. The coordinator
never calls `cancel_all()` or the broad `flatten()` path.

`HyperliquidBroker` implementation notes (for the builder) — **this section is the binding
contract:**

- **Connection:** `Info(base_url, skip_ws=False)` + `Exchange(wallet, base_url, account_address=HL_ACCOUNT_ADDRESS)`
  where `wallet = eth_account.Account.from_key(HL_API_WALLET_KEY)`. `base_url` =
  `constants.TESTNET_API_URL` for paper, mainnet ONLY under the triple-lock (§11). Log the network
  and the resolved account at startup.
- **BarFinalizer contract (much simpler than IBKR — 24/7, no calendar):**
  - Timezone: **UTC only.** No RTH, no NYSE calendar, no half-days, no session-end special case.
    Crypto trades continuously.
  - Bar key: `(coin, tf, bar_end_ts_utc)` where bar boundaries are wall-clock UTC (e.g. 1h bars
    close at :00). Live candles via WS `subscription={"type":"candle","coin":coin,"interval":tf}`;
    each candle msg carries open-time `t` and close-time `T`. Algorithm: keep `last_bar_ts`; when a
    candle with a newer `t` appears (or a wall-clock timer crosses the interval boundary), the
    previous candle is final → emit `on_bar_closed`. The timer is the authority so a quiet market
    (no new candle msg) still closes the bar on schedule.
  - Historical warmup: `info.candles_snapshot(coin, tf, start_ms, end_ms)`.
  - **Reconnect:** on every (re)connect, re-subscribe candles + user events (WS subs do NOT survive
    a socket drop), then verify the next bar/heartbeat arrives within 1× timeframe else `DATA_STALE`.
    First candle after reconnect may duplicate the last pre-drop bar — dedupe by checking a decision
    for that `bar_ts` already exists (idempotency guard). No scheduled nightly restart exists (it is
    an API, not a desktop app) — this whole class of IBKR problem is gone.
  - **P0 sub-check:** confirm WS candles stream on testnet and the close-detection fires on the
    interval boundary within a couple seconds.
- **Bracket = entry + native trigger orders (the real advantage over Signum):**
  - Submit entry (MKT = aggressive IOC, or LMT GTC) together with two **trigger orders** using
    `grouping="normalTpsl"` (amended 2026-07-12): an SL trigger
    `{"trigger":{"triggerPx":sl,"isMarket":true,"tpsl":"sl"}}` and an optional TP trigger
    `{...,"tpsl":"tp"}`, both `reduce_only=True`. These are **real resting orders on the
    Hyperliquid book** — they protect the position even if the bridge process dies.
  - `normalTpsl` grouping links entry and triggers with individual sizing; each trigger order
    carries its own quantity and reduces the position by that size.  The `reprotect_position`
    path uses `grouping="positionTpsl"` because it protects an already-open position and the
    position-linked semantics are appropriate for re-protection.
  - **Partial-fill behaviour:** `normalTpsl` sends entry-matching trigger quantities. The P0
    smoke uses a far-below-market resting entry, so it does not claim partial-fill coverage. At
    runtime, reconciliation must compare live position and protective-trigger quantities; an
    unmatched partial fill remains an `ENTRY_PARTIAL → PROTECTED | UNPROTECTED_ABORT` case and
    must be re-protected or flattened under the existing 10 s guard.
  - **G2 fallback (2026-07-12):** if `normalTpsl` is rejected by the exchange with a type/grouping
    error (e.g. `"Trigger order has unexpected type."`), the smoke harness performs deterministic
    C3 cleanup and makes exactly **one** second attempt via `place_bracket(…, grouping="na")` —
    entry + independent trigger SL (the installed SDK still requires `tpsl:"sl"`, no TP). No
    loop, no third attempt.
    On any fallback failure, cleanup and stop.
  - **2026-07-12 testnet observation (historical):** the real bulk response with `positionTpsl` was
    `{"status":"ok","response":{"type":"order","data":{"statuses":[{"error":"Trigger order has unexpected type."}]}}}`.
    This motivated the shift to `normalTpsl` as the default and the `na` fallback path.
  - **2026-07-12 testnet observation (attempt 6):** `normalTpsl` accepted the resting entry and
    returned a second group status string, `"waitingForFill"`, while the far-below-market entry was
    unfilled. This is a pending child state, not a grouping/type rejection; the smoke did not invoke
    its `na` fallback. The parser currently treats non-dict statuses as malformed, so a new approved
    local parsing change is required before another P0 attempt can verify and cancel this accepted
    entry/child group.
  - **2026-07-12 P0 PASS amendment (attempt 7, `p0-20260712T201750Z`):** across runs the exchange
    returned BOTH child shapes: (a) plain string `"waitingForFill"` (attempt 6) and (b) the child
    as its own `{"resting":{oid}}` status visible in open_orders (attempt 7). The adapter accepts
    both; known pending strings normalize to `WAITING_CHILD` and are exempt from open_orders
    visibility. Real on-exchange SL trigger `modify_order` verified working (attempt 7). Entry
    bracket grouping = `normalTpsl`; `positionTpsl` reserved for re-protecting an existing
    position. **P0 exit criteria MET** — see `14_P0_SMOKE_REPORT.md`.
  - **Client order id:** set `cloid` (128-bit hex derived from `decision_uid:role`) on every order
    for durable identity. The exchange also returns `oid`. Persist both.
  - **Modify (trail):** `exchange.modify_order(cloid_or_oid, new_order)` changing ONLY the SL
    trigger's `triggerPx` — same cloid, price only, never qty. If the live order can't be found:
    cancel + re-place the SL trigger, log WARN.
- **Leverage / margin:** call `exchange.update_leverage(leverage, coin, is_cross=False)` (isolated)
  at startup. **v1 default leverage = 1 (no leverage)** — bounds risk; higher leverage requires an
  explicit config change and is discouraged for the plumbing phase.
- **Durable identity & reconcile:** persist `cloid`, `oid`, `group_id`, `order_ref`
  (= `decision_uid:role`), order JSON on every order row. The Reconciler reads `info.user_state(address)`
  (positions + open orders live on-chain) and matches by `cloid` first, then `order_ref`, then
  conservative attribute fallback (coin+side+type+triggerPx+sz). Ambiguous match ⇒ WARN, do NOT
  flatten a sensible-looking protected position.
- **Reconnect re-protect:** if, after reconnect, a position tagged with our cloid exists WITHOUT a
  working SL trigger, **first re-submit the SL/TP trigger group** (config
  `recover_orders_after_reconnect: true`, default true); only if that fails ⇒ flatten per PREREG §7.
  Because SL is a native resting order, this case is rare (the stop survives socket drops) — but the
  guard stays. Positions NOT tagged with our cloid (manual/foreign) are never adopted or flattened
  — WARN banner only.
- Reconnect loop: watch the WS disconnect event; backoff 5→60 s; unattended recovery is a P2 exit
  criterion.

`MockBroker`: in-memory; `historical_bars` reads CSV fixture `tests/fixtures/BTC_1h.csv`;
`subscribe_bars` replays remaining fixture rows on an accelerated clock (config); fills:
MKT fills at next bar open; SL/TP trigger fills when bar range crosses the level (SL priority on the
same bar, pessimistic). Deterministic — used by pytest and by `--dry-run` app mode.

### 6.2 Strategy protocol + first strategy

```python
class Strategy(Protocol):
    id: str
    warmup_bars: int
    def on_bar(self, bars: Sequence[Bar], position: Position | None) -> Signal | None
    def trail_level(self, bars: Sequence[Bar], position: Position) -> float | None  # None = no change
```

`keltner_trail_ema8.py` — Keltner channel breakout entry × EMA(8) trailing-stop exit, **ported to
crypto (BTC perp 1h) as the plumbing subject** (entry: close-confirmed breakout at bar close, MKT
next; exit: trailing stop at EMA(8) of closes, long: SL = max(SL, ema8), short mirror). This is a
**plumbing test subject only — NOT a promotion claim**; the strategy has not passed the MTC 4-gate
ladder. (The open crypto research lead is `GEN_DONCHIAN_BREAKOUT`; either can be the subject — the
point is exercising the pipeline, not the edge.) Parameters in
`config/strategies/keltner_trail_ema8.yaml`:

```yaml
id: keltner_trail_ema8
version: 1.0.0
source: MTC/crypto_plumbing_subject   # provenance only — no runtime link
golden_run_id: ""                     # filled by build task 3b (QuantLens crypto run)
symbol: BTC                           # Hyperliquid perp coin
timeframe: 1h
params: { kc_length: 20, kc_mult: 2.0, atr_length: 20, trail_ema: 8 }
direction_default: BOTH               # dashboard can restrict; LLM regime can restrict further
permissions:                          # enforced by engine at load + ARM time
  paper_allowed: true
  live_allowed: false                 # mainnet ARM refuses strategies without this flag
  requires_human_approval: true
risk_overrides: {}                    # optional per-strategy tightening of bridge.yaml risk (never loosening)
```

This is the **strategy import format**: future MTC-researched strategies export into a file of this
shape; the bridge validates permissions + risk_overrides at load and refuses mainnet use unless
`live_allowed: true` (which only Barış sets by hand).

**Parity requirement:** the Python port must be replay-testable — `tests/test_strategy.py` feeds
fixture bars and asserts signal timestamps against a golden list generated once from the QuantLens
engine on the SAME crypto bars (build task 3b; read-only comparison, not a live link).

### 6.3 RiskEngine (`engine/risk.py`) — pure function, fully unit-tested

Inputs: Signal, AccountSnapshot, open position, today's realized P&L, config.
Checks in order (first failure returns `Rejection(stage="RISK", reason=...)`):

1. App ARMED; coin enabled; feed not `DATA_STALE`. (No trading-session gate — crypto is 24/7.)
2. Direction allowed: `effective_direction = intersect(config.direction, regime.regime)`;
   empty intersection or NO_TRADE ⇒ reject.
3. No open position (flip disabled v1).
4. Daily loss limit not hit: `realized_today + unrealized <= -max_daily_loss_pct * day_start_equity`
   ⇒ reject + auto-DISARM. **Trading day = UTC date** (crypto 24/7). `day_start_equity` snapshotted
   at 00:00 UTC (or engine start if later) into `risk_days`. Engine-computed daily P&L is logged
   side-by-side with the exchange's reported realized P&L; divergence > 1% ⇒ DISARM + alert.
4b. Consecutive-loss stop: last `max_consecutive_losses` realized trades all losers
   (**loss = pnl < 0 regardless of exit_reason** — trail scratches count) ⇒ reject + auto-pause.
   **Counter resets to 0 on: any winning trade, new UTC day, manual re-ARM.**
   **Unattended policy (P2):** config `on_consecutive_loss: disarm | pause_auto_rearm`
   (default `pause_auto_rearm`: auto re-ARM after cooldown, max `max_auto_rearms_per_day: 2`,
   then hard DISARM).
4c. Cooldown: within `cooldown_minutes_after_loss` of the last LOSING trade close (any exit_reason)
   ⇒ reject "cooldown_active". Independent of 4b.
5. Sizing (fixed fractional): `risk_dollars = equity * risk_pct_per_trade` (default 0.5%);
   `stop_distance = |ref_price - stop_loss|`; `qty = risk_dollars / stop_distance`, rounded DOWN to
   the coin's `szDecimals`.
5a. **Stop-validity guards (BEFORE division):** reject if `stop_distance <= 0` (div-by-zero),
   `stop_distance < min_stop_distance` (default `max(tick, 0.1% of ref_price)`), stop on the wrong
   side of price, or price already gapped through the stop.
6. Constraint clamps: `qty * ref_price <= max_position_notional_pct * equity` (default 20%);
   **min order value $10** (Hyperliquid minimum) else reject "below_min_notional".
6b. **Margin check:** `qty * ref_price / leverage <= available_margin * 0.95` else reject
   `INSUFFICIENT_MARGIN`.
6c. **Leverage cap:** `leverage <= max_leverage` (default 1) else reject `LEVERAGE_TOO_HIGH`.
7. TP: `take_profit = ref_price ± rr_ratio * stop_distance` if `tp_mode: rr`; `tp_mode: none` ⇒
   trail-only exit (matches trail_ema8 philosophy; DEFAULT for v1).

Output `OrderPlan` with the full arithmetic trace in `reason` (auditable).

**Gate-results exposure:** RiskEngine returns, alongside pass/reject, an ordered
`gate_results: list[{gate, status: PASS|WARN|BLOCK|SKIP, detail}]` covering every check above + LLM
gate + duplicate/stale checks. Stored in the decision payload and rendered as the dashboard **Gate
Monitor** card — "signal ≠ order" made visible: what passed, what blocked, why.

### 6.4 LLM layer (`engine/llm_gate.py`) — two roles, both risk-reducing only

**Role A — Regime directive (periodic, default every 4 h + on demand):**
- Calls Grok (`grok-4`, `XAI_API_KEY`) with a fixed prompt: given the coin + recent crypto
  headlines/X sentiment it retrieves, output STRICT JSON `RegimeDirective`
  (regime ∈ LONG_ONLY|SHORT_ONLY|BOTH|NO_TRADE, confidence 0-1, ttl_minutes, rationale, sources[]).
- Validation: non-JSON / invalid regime / confidence < `min_confidence` (default 0.6) ⇒ directive
  IGNORED, fall back to config direction, log `LLM_INVALID`. `ttl_minutes` **clamped to [15, 1440]**.
- **TTL expiry (no silent widen):** expiry triggers an immediate refresh; until a new valid
  directive arrives, the last directive holds up to 2× its TTL; beyond that, fall back to
  `config.direction` + WARN. Expiry never silently converts NO_TRADE into BOTH within the 2×TTL
  window (audit: Cursor F-13).
- Regime can only **narrow** what config allows — never widen.
- **Prompt-injection mitigation (audit: DeepSeek F-03):** every retrieved headline/post is truncated
  (280 chars), control-chars + markdown fences stripped, URLs removed, wrapped in labeled
  `[SOURCE_START]…[SOURCE_END]` blocks; system prompt treats block contents as DATA, never
  instructions. `directives` stores the source-text HASH, not raw text. Worst-case injection =
  forced NO_TRADE (denial, not a financial exploit) — narrowing-only holds.
- Keys are the bridge's OWN env vars (`XAI_API_KEY`, `ANTHROPIC_API_KEY`) read by `settings.py`.
- This is Barış's "AI picks market sentiment → long-only / short-only / no-trade" idea, implemented
  safely: it can only restrict direction, never open or enlarge a trade. YouTube/market-video
  sentiment: v1 ships Grok-only; the `SentimentSource` protocol leaves a slot for a YouTube source.

**Role B — Pre-trade veto (per order; `llm.veto_enabled: false` DEFAULT in v1 — audit consensus):**
- v1 ships the veto path behind `NullLLMGate` default; enabled at P1 after the hot path is proven.
  A synchronous external call on the bar→order path is latency-risky and non-protective when
  fail-open (Codex F-08, Copilot F-07, Cursor F-14).
- When enabled: Claude (`claude-sonnet-5`, `ANTHROPIC_API_KEY`) gets the OrderPlan JSON + last N
  decisions + current regime, answers STRICT JSON `{verdict:"PASS"|"VETO", reason}` with a checklist
  prompt (SL present? size arithmetic consistent? conflicts with regime? feed stale? leverage ≤ cap?).
- Runs **async with a hard deadline** (`llm.veto_deadline_s: 5`): no verdict by deadline ⇒
  `LLM_SKIPPED`, formal rule proceeds; the engine loop / fill handlers are NEVER blocked.
  `fail_policy: closed` available but not default.
- **Cost guards:** `llm.max_vetos_per_day: 20`, `llm.max_daily_llm_cost_usd: 5` — exceeded ⇒
  auto-skip with `LLM_COST_LIMIT` event.
- Every call logged to `llm_calls`: prompt hash, model, latency, verdict, tokens, cost est.

**Hard boundary (enforced in code, not prompt):** LLM outputs are parsed into the two models above;
there is NO code path from LLM output to qty, price, leverage, or new-order fields.

### 6.5 OrderManager (`engine/orders.py`)

- Owns mapping decision_uid ↔ exchange order ids (cloid/oid); writes every order-status/fill event
  to Store.
- **Duplicate-order protection:** submit is idempotent per decision_uid; a signal fingerprint
  `(coin, direction, bar_ts)` may submit at most once per run — reconnect replays can never
  double-order.
- **Stale-DATA guard:** freshness = **bar age** using data timestamps (candle `T`), never local
  receipt time; at submit the triggering bar's `end_ts` must be < 0.5× timeframe old AND the feed
  not in `DATA_STALE`. (Hyperliquid is real-time; no delayed-feed caveat.)
- **Close = reduce-only semantics:** exit paths (close-on-opposite-signal, flatten, trail) size
  orders to current position qty read at submit time — a close can never open the opposite side.
- **Partial fills:** with `normalTpsl` grouping the SL/TP carry explicit entry-matching quantities,
  so reconciliation must compare trigger quantities with the live position after a partial fill.
  Exact child-resize behavior is not P0-proven; an unmatched partial remains
  `ENTRY_PARTIAL → PROTECTED | UNPROTECTED_ABORT` and must be re-protected or flattened under the
  10 s guard. Out-of-order status callbacks are tolerated (transitions keyed by cloid+status,
  idempotent).
- **Stale entry order:** unfilled LMT entry older than `max_open_order_age_s` (default 600 s) ⇒
  cancel entry + its triggers, log `ORDER_STALE_CANCELLED`.
- Watchdog: order not acked in 120 s ⇒ abort criterion (PREREG §7) ⇒ DISARM + alert.
- **Reconciler (60 s):** compares exchange truth (`info.user_state`) vs DB. Freshly submitted orders
  sit in a **PENDING grace state** excluded until age > 2× interval — no action on in-flight races.
  Naked-position detection ALSO runs event-driven on every fill/position callback. Flatten only
  positions traceable to our cloid; foreign positions ⇒ WARN, never touched. Reconciler snapshots
  equity every 60 s into `equity` (feeds max-intraday-DD, PREREG §5) and runs the engine-vs-exchange
  equity divergence check (>0.5% ⇒ WARN, >1% ⇒ DISARM). Also tracks funding payments (log only, v1).
- **Epoch drain (TS-P1-005):** `drain_queued_events()` ingests queued broker callbacks under the
  per-symbol writer locks with no broker I/O. The full reconciler calls it once, after taking the
  global full-writer guard, so a capture always sees one coherent local epoch.
  `sync_broker_state()` now delegates its first half to it; its behavior is unchanged.

### 6.5b FullReconciler (`engine/reconcile.py`) — TS-P1-005, opt-in

Separate from the 60 s light reconciler above, and never a substitute for it.

- **One bounded capture per cycle**: reserve a durable attempt → take the *global* full-writer
  guard (an overlapping full attempt is refused, not queued) → drain the event epoch → collect
  read-only evidence for seven components (open orders, fills, positions, balances, margin,
  funding, local pending actions) → validate → deterministic diff → **atomically** commit
  snapshot, diff, provenance, verdict and the latest-accepted pointer, last. No SQLite
  transaction ever spans broker I/O; lock order is always guard → symbol locks.
- **Read-only**: zero cancel/adopt/re-protect/flatten/retry. Foreign state is observed, never
  touched.
- **Envelope (D2=A)**: 5 s monotonic deadline **enforced during collection** — every adapter await
  runs under `asyncio.timeout(remaining budget)`, so a hung broker call is cut off in bounded wall
  time (`STALE` / `FULL_RECONCILE_DEADLINE_EXCEEDED`, no checkpoint) rather than only detected
  afterwards; the post-hoc monotonic check stays as a second guard. Plus ≤5 s component source
  skew, fail-closed on clock rollback, future/stale source timestamps and adapter client rebuild.
  Four bounded REST reads nominally (`user_state` serves positions+balances+margin from one
  observation).
- **Fills/funding window**: durable coverage continuity, **no fixed lookback**. Before the first
  acceptance the lower bound is `min(run's durable started_ts, MIN(reconcile_attempts.started_ts))`,
  so a restart under a new `run_id` before anything was ever accepted cannot skip the previous
  run's observation window; after an acceptance every capture starts at the upper bound the last
  *accepted* checkpoint proved. Failures and downtime widen the next window instead of skipping it;
  an interval the endpoint cannot prove fails closed.
- **Separate readiness gate**: `full_reconcile_ready` derives only from a *fresh accepted v6
  checkpoint* that is also **the most recently resolved attempt**, and the engine additionally
  latches it shut while `full_reconcile_error` is set (cleared only by a fresh accept). Freshness
  bound reuses the accepted light formula `max(reconcile_interval_s × 3, 30 s)`. The light
  `reconcile_ready` keeps its own owner and can never satisfy it; on a v6 store `arm()` requires
  both. On a v4/v5 store nothing changes.
- **Separate failure budget**: the full capture runs outside the light reconcile try/handler, so a
  full ledger/capture failure never touches `reconcile_ready`, the light consecutive-failure
  budget, or ARMED state — it only latches the full gate.
- **Persistence**: additive opt-in schema **v6** — `reconcile_attempts`, `reconcile_components`,
  `reconcile_diffs`, `reconcile_checkpoints`, `funding_events`, plus one transactional `meta`
  pointer (latest-accepted checkpoint). Coverage derives from that checkpoint's immutable
  fills/funding component cursor bounds. Default target stays
  v4; v6 is reached only via the proven v4→v5→v6 chain.
- **Funding (D3=A)**: a separate signed ledger keyed by the exchange event `hash`, never folded
  into fills and never consumed by risk before TS-P1-006 / full TS-P1-007.
- Full contract: `26_FULL_RECONCILIATION_CONTRACT.md`.

### 6.5c Authoritative risk-input snapshot — TS-P1-006, opt-in

On schema v6, ARM and every new-entry risk decision resolve one immutable v2
view from the transactional latest-accepted reconcile pointer. The view carries
checkpoint/hash/time provenance and canonical positions, balances, and margin
rows from the same accepted account observation. Risk does not call the point
`account()` endpoint or accept `open_position=None` on this path. Legacy v1,
stale, future, superseded, incomplete, malformed, or tampered evidence vetoes
and DISARMs; there is no fallback. Default v4 behavior and all numeric risk
policy remain unchanged. Full contract:
`27_AUTHORITATIVE_RISK_SNAPSHOT_CONTRACT.md`.

### 6.6 BarFeed staleness
24/7: if `now − last_bar_update > 2 × timeframe` ⇒ `DATA_STALE` event ⇒ DISARM (PREREG §7). No RTH
condition — the check runs continuously.

### 6.7 Notifier (`engine/notify.py`) — optional, high value for unattended P2
Telegram bot (env `TELEGRAM_BOT_TOKEN` + `TELEGRAM_CHAT_ID`; both unset ⇒ disabled, no error).
Sends: fills, trade closes (w/ P&L), every event severity ≥ WARN, DISARM/KILL, regime changes,
and a **6 h heartbeat** (RTH-agnostic — "bridge alive, position, equity, last bar"). Fire-and-forget
with 5 s timeout — a notification failure NEVER blocks the trading path.

---

## 7. SQLite schema (Store; all ts UTC ISO)

Schema v2 (audit consensus: decision grouping, durable exchange identity, PREREG §5 first-class
columns, fills granularity, bars persistence, risk days, versioning):

```sql
CREATE TABLE meta      (key TEXT PK, value TEXT);            -- schema_version, app_state (KILLED persists), created_at
CREATE TABLE runs      (run_id TEXT PK, started_ts, ended_ts, mode TEXT CHECK(mode IN ('paper','dry_run','live')),
                        network TEXT,                        -- testnet | mainnet
                        config_json TEXT);
CREATE TABLE bars      (coin, tf, bar_end_ts, open, high, low, close, volume,
                        PRIMARY KEY(coin, tf, bar_end_ts)); -- every finalized bar; chart + parity forensics served from here
CREATE TABLE decisions (id INTEGER PK, decision_uid TEXT NOT NULL, -- UUID shared by all stages of one decision
                        run_id, ts, coin, stage TEXT,        -- SIGNAL/RISK_PASS/RISK_REJECT/LLM_PASS/LLM_VETO/LLM_SKIPPED/SUBMITTED/...
                        trade_id INT,                        -- filled at SUBMITTED stage onward
                        payload_json TEXT, payload_version INT DEFAULT 1);
CREATE TABLE orders    (cloid TEXT PK, oid INT, group_id TEXT, order_ref TEXT,  -- our decision_uid:role tag
                        order_json TEXT, decision_uid TEXT, trade_id INT,
                        role TEXT,                           -- ENTRY/SL/TP
                        status, qty, filled_qty, avg_fill_px, ts_submit, ts_last);
CREATE TABLE fills     (fill_id TEXT PK, cloid, decision_uid, fill_ts, qty, px, fee, funding);
CREATE TABLE trades    (trade_id INTEGER PK, run_id, coin, direction, qty,
                        entry_decision_uid TEXT,             -- joins the full reasoning chain
                        signal_ts, decision_ts, submit_ts, first_fill_ts, last_fill_ts,
                        expected_px, entry_px, entry_ts, exit_px, exit_ts, exit_reason,
                        pnl, slippage_bps_entry, risk_dollars, risk_pct, leverage,
                        sl_initial, tp_initial, llm_directive_id INT);
CREATE TABLE equity    (run_id, ts, equity, cash, unrealized, realized_today,
                        PRIMARY KEY(run_id, ts));            -- sampled every 60s → max intraday DD computable
CREATE TABLE risk_days (trading_date TEXT PK,                -- UTC date
                        day_start_equity, realized_pnl_engine, realized_pnl_broker,
                        max_intraday_dd, consecutive_losses_end, auto_rearms_used);
CREATE TABLE directives(id INTEGER PK, ts, regime, confidence, ttl_minutes, rationale,
                        sources_hash TEXT,                   -- hash, not raw text
                        raw_response TEXT, valid INT);
CREATE TABLE llm_calls (id INTEGER PK, ts, role TEXT,        -- regime/veto
                        model, prompt_hash, latency_ms, verdict, tokens_in, tokens_out, cost_est);
CREATE TABLE events    (id INTEGER PK, run_id, ts, severity TEXT, code TEXT, detail TEXT); -- DISCONNECT/RECONNECT/DATA_STALE/RECON_MISMATCH/CONFIG_CHANGED/KILL/LIQUIDATION_WARN/...

CREATE INDEX idx_decisions_uid  ON decisions(decision_uid);
CREATE INDEX idx_decisions_run  ON decisions(run_id, ts);
CREATE INDEX idx_orders_oid     ON orders(oid);
CREATE INDEX idx_orders_trade   ON orders(trade_id);
CREATE INDEX idx_fills_cloid    ON fills(cloid);
CREATE INDEX idx_trades_run     ON trades(run_id);
CREATE INDEX idx_events_run_sev ON events(run_id, severity, ts);
```

Schema v6 (TS-P1-005 full reconciliation, **additive and opt-in** — the operational baseline
target stays v4; v6 is reached only via the proven v4→v5→v6 chain and never by merely opening a
database):

```sql
CREATE TABLE reconcile_attempts   (attempt_id TEXT PK,          -- recon-v1:<sha256>
                                   run_id, seq INT, state TEXT, -- COLLECTING/COMPLETE/INCOMPLETE/CONFLICTING/STALE
                                   started_ts, ended_ts, duration_ms INT,
                                   deadline_s REAL, max_skew_s REAL,   -- the D2=A envelope, durably recorded
                                   complete INT, fresh INT, canonical_hash TEXT, reason_code TEXT,
                                   UNIQUE(run_id, seq));        -- resolvable exactly once; DELETE refused
CREATE TABLE reconcile_components (component_row_id INTEGER PK, attempt_id → reconcile_attempts,
                                   component TEXT, source TEXT, status TEXT, observed_ts,
                                   exact INT, complete INT, row_count INT,
                                   cursor_start_ms INT, cursor_end_ms INT, page_count INT, call_count INT,
                                   payload_digest TEXT, reason_code TEXT,
                                   UNIQUE(attempt_id, component));      -- append-only
CREATE TABLE reconcile_diffs      (diff_row_id INTEGER PK, attempt_id → reconcile_attempts, seq INT,
                                   kind TEXT, subject TEXT, reason_code TEXT,
                                   ownership TEXT,              -- OWNED/FOREIGN_IDENTIFIED/UNKNOWN_OWNERSHIP
                                   blocking INT, payload_json TEXT,
                                   UNIQUE(attempt_id, seq));            -- append-only
CREATE TABLE reconcile_checkpoints(checkpoint_id TEXT PK,       -- ckpt-v1:<sha256>
                                   attempt_id TEXT UNIQUE → reconcile_attempts, run_id,
                                   accepted_ts, canonical_hash TEXT, snapshot_json TEXT, reason_code TEXT);
                                                                        -- fully immutable
CREATE TABLE funding_events       (event_id TEXT PK,            -- authoritative exchange hash, never synthesized
                                   symbol, amount_usdc REAL,    -- signed delta.usdc
                                   effective_ts, source TEXT,
                                   attribution TEXT,            -- ATTRIBUTED | UNATTRIBUTED, first-seen
                                   payload_digest TEXT,         -- exchange-authoritative fields ONLY
                                                                -- (attribution is locally derived → excluded)
                                   first_seen_attempt_id → reconcile_attempts,
                                   recorded_ts);                        -- append-only
-- latest accepted checkpoint pointer: meta['reconcile_checkpoint_latest'],
-- fills/funding coverage upper bound: derived from that checkpoint's immutable
-- FILLS/FUNDING reconcile_components cursor_end_ms values (no second pointer).
-- Coverage is monotonic and advances ONLY on acceptance, so a failed attempt or
-- a downtime widens the next window instead of leaving an unobserved gap.
```

Schema v9 (TS-P1-009 kill evidence, **additive and opt-in**; source v8 only):

```sql
CREATE TABLE kill_requests      (episode_id TEXT PK, generation INT, run_id, symbol,
                                 flatten_requested INT, requested_ts, policy_version,
                                 terminal_state, terminal_reason, terminal_ts,
                                 safe_checkpoint_id → reconcile_checkpoints,
                                 safe_checkpoint_ts, proof_digest, ack_state, ack_ts);
CREATE TABLE kill_actions       (action_id TEXT PK, episode_id → kill_requests,
                                 kind, target, qty_lots, cloid, reserved_ts,
                                 deadline_ts, current_outcome);
CREATE TABLE kill_action_events (event_row_id INTEGER PK, action_id → kill_actions,
                                 seq INT, status, evidence_source, reason_code,
                                 evidence_json, evidence_digest, observed_ts);
-- sole transactional active pointer: meta['kill_request_active']
```

Request and action identity fields are immutable; action events are append-only. Migration runs
under `BEGIN IMMEDIATE`, performs no broker I/O, preserves predecessor evidence, and rolls back
cleanly to reopenable v8 on any DDL/meta/pointer failure. Default initialization is still v4;
opening v4-v8 never creates these objects. Full contract:
`30_TSP1009_KILL_EVIDENCE_RECOVERY.md`.

Conventions: storage = UTC ISO; **all logic = UTC** (no timezone gymnastics — crypto is 24/7);
display = local. `meta.schema_version` gates inline migrations — and a meta row alone is not
proof of a version: a database claiming v6 without v6 objects fails closed. On PUT /api/config
while ARMED, a `CONFIG_CHANGED` events row records the field-level diff (old→new).

`decisions.payload_json` is the audit trail Barış asked for (thesis-history idea, adapted: every
trade's full reasoning chain reconstructable by decision_uid).

---

## 8. API (FastAPI)

REST (all JSON):
```
GET  /api/status            app state, exchange conn, mode, network, regime, account snapshot
GET  /api/config            merged config          PUT /api/config   validated runtime overrides
POST /api/arm  /api/disarm  /api/kill?flatten=bool
POST /api/regime/refresh    force LLM regime call
GET  /api/positions  /api/orders  /api/trades?limit=  /api/decisions?trade_id=  (joins via decision_uid)
GET  /api/equity?from=      equity curve
GET  /api/events?severity=
GET  /api/bars?n=300        from the bars TABLE (not a live exchange call); shape:
                            {"bars":[{"time":unix_s,"open":..,"high":..,"low":..,"close":..,"volume":..}]}
GET  /api/gates/latest      structured gate_results of the most recent decision (Gate Monitor source)
GET  /api/snapshot          one-shot full state: status+positions+orders+last trades+latest gates
GET  /api/runs/{run_id}     run record incl. config snapshot (System page)
POST /api/kill/ack          evidence-gated operator ACK; result is DISARMED
```
WS `/ws`: server pushes `{topic, data}` for topics: `status`, `bar`, `decision`, `order`,
`position`, `equity`, `directive`, `event`. **Reconnect contract:** on every WS `open` the server
immediately pushes a full `snapshot` message (same payload as GET /api/snapshot); the client
re-renders from it — no missed-DISARM/fill gaps after tab sleep or network blips. `status` carries a
monotonic `state_version`.

Confirmation model:
- Mutating ops (ARM, PUT config while ARMED) require header `X-Confirm: <state_version>`; server
  rejects on mismatch (stale tab). Version is pushed on every WS status update.
- KILL ACK also requires the current `X-Confirm` value plus a fresh pointed safe-terminal
  reconciliation proof. ACK itself is never cancel/flatten evidence and never reaches ARMED.
- **KILL and DISARM are NEVER nonce-blocked** — safety actions must not fail on stale UI state.
  KILL uses its own two-step confirm (modal) client-side.

---

## 9. Dashboard spec (professional; single dark theme)

Design language: near-black `#0d1117` bg, panel `#161b22`, border `#30363d`, text `#e6edf3`,
green `#3fb950` / red `#f85149` / amber `#d29922` accents, `Inter` + `JetBrains Mono` (numbers).
Layout: fixed left sidebar (nav + ARM/DISARM/KILL block), topbar (conn pill, mode pill
`TESTNET` amber / `DRY-RUN` blue / `MAINNET` red, regime pill, equity ticker, next-bar countdown).

Pages (hash-routed, one `app.js`):
1. **Overview** — equity curve (lightweight-charts), day P&L card, open position card (entry, SL,
   TP, unrealized, **leverage, liquidation price, funding**, trail level), last-10 decisions stream,
   regime card (regime, confidence, TTL countdown, rationale, refresh), **Gate Monitor card** —
   last signal's full gate breakdown (§6.3): green PASS / amber WARN / red BLOCK / grey SKIP with
   block reason; empty state "No signal yet — next bar in HH:MM:SS". Makes "signal ≠ order" visible.
2. **Strategy & Risk config** — strategy select (v1: one), coin, timeframe (read-only v1),
   direction (BOTH/LONG/SHORT), risk % per trade, **leverage (≤ max_leverage)**, tp_mode (none/rr)
   + rr, max daily loss %, max notional %, LLM toggles (regime on/off, veto on/off, fail policy,
   min confidence). Save = PUT /api/config; changes while ARMED require confirm modal. **Mirrors the
   MTC_V2 settings mental model (risk/SL/TP/money-management/direction in one panel).**
3. **Trading** — price chart w/ entry/SL/TP lines + trade markers + liquidation line; working orders
   table; positions table; manual actions: cancel order, flatten (confirm modal).
4. **Journal** — trades table (all PREREG §5 fields); click row → decision-chain drawer
   (SIGNAL → RISK → LLM → orders → fills, each with payload JSON pretty-printed).
5. **LLM** — directives history, veto log w/ reasons, call latency/token/cost stats.
6. **System** — events log w/ severity filter, exchange connection history, data staleness, DB size,
   config snapshot of the running `run_id`, network + leverage banner.

Kill switch: red button, sidebar bottom, always visible, double-confirm modal with "flatten
positions" checkbox. DISARMED = amber banner every page. KILLED = red banner. MAINNET = persistent
red "REAL MONEY" banner.

---

## 10. Config (`config/bridge.yaml` defaults)

```yaml
mode: paper                    # paper | dry_run | live (live == mainnet; needs --enable-live CLI + HL_LIVE_ACK env + strategy live_allowed)
broker:
  network: testnet             # testnet (paper) | mainnet (triple-locked)
  coin: BTC
  leverage: 1                  # v1 default = no leverage; ≤ risk.max_leverage
  margin_mode: isolated
  recover_orders_after_reconnect: true
strategy_file: strategies/keltner_trail_ema8.yaml
risk:
  risk_pct_per_trade: 0.005
  max_daily_loss_pct: 0.02
  max_position_notional_pct: 0.20
  min_stop_distance_pct: 0.001 # 0.1% of ref_price floor (div-by-zero / absurd-qty guard)
  min_order_usd: 10            # Hyperliquid minimum order value
  max_leverage: 1              # hard cap; raising it is a deliberate, discouraged change
  max_consecutive_losses: 3    # losers = pnl<0 any exit_reason; resets on win / new UTC day / manual re-ARM
  on_consecutive_loss: pause_auto_rearm   # or: disarm (manual re-arm; breaks unattended P2)
  max_auto_rearms_per_day: 2
  cooldown_minutes_after_loss: 120
  max_open_order_age_s: 600
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
  fail_policy: open
  regime_model: grok-4
  veto_model: claude-sonnet-5
server: { host: 127.0.0.1, port: 8790 }   # CORS restricted to 127.0.0.1 origins
```

---

## 11. Safety rails summary (enforced in code)

1. **Default-DENY network lock:** `network: testnet` (paper) is the default and only unlocked target.
   `network: mainnet` (real money) requires the triple-lock: `--enable-live` CLI flag +
   `HL_LIVE_ACK=I_UNDERSTAND_THIS_IS_REAL_MONEY` env + strategy `live_allowed: true`. `broker.network`
   is NOT runtime-editable via PUT /api/config (yaml-only, restart required).
2. **API wallet cannot withdraw** — use a Hyperliquid agent/API wallet, never the main key. Even a
   fully compromised bridge cannot move funds off the exchange. This is the primary money-safety rail.
3. **Leverage cap** default 1 (no leverage); raising `max_leverage` is a deliberate config change.
4. LLM outputs structurally cannot create/enlarge orders or change leverage (§6.4 hard boundary).
5. Every abort criterion (PREREG §7) wired to auto-DISARM + red event.
6. Startup with unreconcilable exchange state ⇒ start DISARMED with banner (never auto-trade into
   unknown state).
7. Native resting SL/TP triggers protect the position even if the bridge process dies (the key
   safety advantage over a synthetic-stop relay).
8. Secrets only from env; never logged; `data/` git-ignored.
9. This app never writes into `MTC_COMMAND_CENTER/` and never imports from it at runtime.
10. Dashboard renders ALL payload/log fields via `textContent` / `<pre>` — never `innerHTML`.
11. FastAPI `CORSMiddleware` restricted to `127.0.0.1`; server binds 127.0.0.1 only.
12. Store redacts `(api.?key|token|secret|bearer|private)`-matching content from any persisted raw
    LLM response.

## 12. Relationship to MCC / existing tracks

- Independent top-level app. Shares the repo for versioning only.
- SYSTEM_TEST vertical slice (V1.1, closed) proved localhost signal plumbing; this bridge is the
  exchange-facing successor, with its own PREREG gates (P0-P3).
- Paper (testnet) results feed BACK to MCC only as a written report (P3 slippage + parity report
  into `MTC_COMMAND_CENTER/11_TRIAGE/`), never as automatic promotion evidence.

## 13. Roadmap beyond v1

Adopted into v1: gate monitor, duplicate-order + stale-data guards, consecutive-loss stop +
cooldown, strategy import format w/ permissions, Telegram notifier, native SL/TP triggers, leverage
cap. Deliberately DEFERRED:

| Idea | When | Note |
|---|---|---|
| Manual Execution Ticket (risk-calculated manual orders w/ gate check) | v1.1 | v1 has only cancel/flatten manual actions. |
| Real-data shadow mode (live testnet bars → MockBroker, no orders) | v1.1 | De-risks the arm decision; loud UI pill. |
| Event/funding gate (macro calendar / extreme funding block) | v1.1 | Partially covered by LLM regime NO_TRADE; a deterministic gate is better. |
| Market Context page (movers, funding, OI, sentiment) | v2 | Context layer only, never an order trigger. |
| **Binance connector** (spot/USDⓈ-M) | v2 | `Broker` protocol (§6.1) is the seam; add alongside Hyperliquid when a second venue is wanted. |
| IBKR / Signum | **NOT chosen** (see `07_BROKER_DECISION.md`) | IBKR blocked by KKTC address verification; Signum = market-only, no native resting stop, vendor lock. Re-evaluate only if requirements change. |
| Postgres + Redis + Docker Compose | v2 / multi-strategy | SQLite + 1 process is correct at v1 scale. |
| React/Next frontend | only if vanilla JS hits a wall | No build step is a feature. |
| Login + 2FA + roles | REQUIRED before any non-localhost exposure | v1 binds to 127.0.0.1 only. |
| Deployment: local → small VPS (24/7) | after P2 | **Hyperliquid is a pure API — no desktop terminal — so the engine runs directly on a ~$5/mo VPS; no hybrid bridge needed** (this is a concrete win over the IBKR path). Tunnel/remote access stays STRICTLY monitor-only (ARM/DISARM/KILL + config edits blocked remotely) until login+2FA ships. |
| Multi-strategy portfolio + correlation/exposure gates | v2 | Portfolio-level risk engine; `risk_overrides` is the hook. |
# Durable risk-control layer (opt-in schema v7)

TS-P1-007 extends the accepted reconciliation boundary with two additive
persistence objects: immutable checkpoint-bound daily-risk rows and immutable
control latch/reset evidence. The reconcile transaction derives them from the
same accepted account checkpoint; the pure risk engine consumes the paired
portfolio/daily view. The runtime default remains schema v4, so activation and
operational migration require separate owner authorization.

# Exposure-control layer (opt-in schema v8)

TS-P1-008 enriches the same accepted account observation with position gross
mark notional, reported leverage, and liquidation price. Independent risk
checks symbol/portfolio gross exposure, wallet utilization, effective leverage,
and directional liquidation distance both at ARM and before submission. The
one-position gate remains and no scheduler or automatic broker mutation is
introduced. Default schema remains v4.

# Kill evidence and recovery layer (opt-in schema v9)

TS-P1-009 replaces the broad best-effort KILL path only when v9 is explicitly active. Memory is
latched first; one transaction persists KILLED, the immutable request, and the active pointer
before broker I/O. Mutation takes the full-writer guard before the symbol writer and uses only
proven-owned identities. Cancel and flatten have separate fixed five-second monotonic/UTC
verification budgets. UNKNOWN, deadline, crash, partial application, quarantine, or ownership
ambiguity remains KILLED and query-only until direct evidence resolves the same identity.

Entries are always cancelled first. Owned reduce-only protection is retained unless exact owned
lots are flattened and an authoritative flat snapshot has been observed; only then may residual
owned protection be cancelled. A fresh accepted reconciliation checkpoint binds the safe terminal
proof required by ACK. Default schema remains v4; no migration, activation, exchange call, or
runtime start is automatic.
