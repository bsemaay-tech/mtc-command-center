# Audit — IBKR Paper Bridge design

Model: Kimi K1.5 | Date: 2026-07-06 | Docs commit: c2c3bbb0

## 1. Summary verdict

**Ship-with-fixes** — the core architecture is sound for a one-day v1 build: mock-first, deterministic signal path, hard LLM boundary, and paper-only default are all correct. However, three design holes will cause immediate failure: (1) TWS nightly restart will trigger an unwanted position flatten every night under the current reconciler rule, making unattended P2 impossible; (2) the `orders` table lacks a `trade_id` foreign key, so the Journal page’s decision-chain drawer cannot be built from the schema as written; (3) the sizing formula crashes on zero stop-distance before the notional clamp can fire. All three are fixable within v1 scope. Several MEDIUM ambiguities (bar-close detection, flip sequence, daily-loss timezone) will force the builder to guess; the spec should be tightened.

## 2. Findings

| ID | Severity | Dimension | Location | Issue | Suggested fix |
|---|---|---|---|---|---|
| **F-01** | **CRITICAL** | A | ARCH §5, §6.1, PREREG §7 | TWS nightly restart (~23:45 ET) typically drops paper API orders. On reconnect, the Reconciler sees an open position with **no working SL** and executes the PREREG §7 "naked position" abort → **flatten**. This will happen every night, making **unattended P2 impossible**. | Add a **restart-recovery path**: on reconnect, if position exists but no SL/TP orders, re-submit a bracket for the existing position (with `transmit=True` on the SL child) **before** concluding naked position. Add a `recover_orders_after_restart: true` flag in config (default true for paper). If re-submit fails, *then* flatten. |
| **F-02** | **HIGH** | B | ARCH §5 | Trail behavior while DISARMED is undefined. The state machine says "SL/TP of open position stay working" but does **not** say whether trailing-stop modifications continue. If they continue, the engine is still trading while DISARMED; if they stop, the SL is frozen at a potentially stale level. | Explicitly amend §5: **DISARMED freezes trail modifications** (trail_level is no longer recalculated per bar); existing SL/TP remain working at their last prices. On re-ARM, trail recalculates from the next bar. |
| **F-03** | **HIGH** | C | ARCH §6.3 | Sizing formula `qty = floor(risk_dollars / stop_distance)` will **ZeroDivisionError** if `stop_distance` is zero or negative (gap, data error, or bad strategy parameter). The notional clamp (#6) is evaluated *after* sizing, so it cannot rescue the crash. | Add guard **before** sizing: `if stop_distance <= 0: reject "invalid_stop_distance"`. Also add a `min_stop_distance` floor (e.g., `$0.01` or `0.01 * ATR`) to prevent absurdly large sizes on tiny stops. |
| **F-04** | **HIGH** | E / F | ARCH §7 | The **Journal decision-chain drawer** (`/api/decisions?trade_id=`) cannot be served from the schema as written. `orders` has `decision_id` but **no `trade_id`**. To show a trade’s full chain (SIGNAL → RISK → LLM → SUBMITTED → FILLED), the API must join `trades` → `orders` → `decisions`, but there is no foreign key from orders to trades. | Add `trade_id INT` to the `orders` table (populated when the entry fill creates a trade). Alternatively, add `trade_id` to the `decisions` table at the SUBMITTED stage. Either way, the join must be explicit in the schema. |
| **F-05** | **MEDIUM** | A | ARCH §6.1 | `keepUpToDate` bar-close detection is underspecified. The spec says "emit `on_bar_closed` when a NEW bar object appears" but does not state the comparison algorithm (timestamp vs. list-length vs. bar hash). Different builders will implement this differently, leading to divergent behavior on reconnect replays or TWS restarts. | Specify the exact algorithm in §6.1: maintain `last_bar_ts`; on `updateEvent`, if `bars[-1].date > last_bar_ts`, emit `bars[-2]` as closed, set `last_bar_ts = bars[-1].date`. Also handle the first event (no prior bar) and reconnect (reset `last_bar_ts` from DB latest). |
| **F-06** | **MEDIUM** | C | ARCH §6.3, PREREG §7 | "Daily loss limit" and "today" are undefined in timezone. AAPL trades 09:30–16:00 ET. If a position is opened at 15:00 ET and closed at 09:30 ET the next day, which day does the P&L belong to? `day_start_equity` is undefined. | Define **trading day boundary** as 00:00–23:59 ET (or 09:30–16:00 ET if stricter). Store `day_start_equity` keyed to that boundary in the `equity` table at the first RTH bar of each day. Log the timezone explicitly. |
| **F-07** | **MEDIUM** | B | ARCH §5 | Flip sequence is undefined. "Close-then-open" does not specify: (a) cancel existing bracket first? (b) market or limit close? (c) wait for fill ack before new entry? (d) what if the close is rejected? | Add flip sub-state machine: (1) **cancel** existing bracket (SL/TP); (2) submit **reduce-only** market close for current `position.qty`; (3) **wait for fill ack**; (4) submit new entry bracket. If close is rejected, log `FLIP_CLOSE_REJECTED` event, DISARM, and do not submit new entry. |
| **F-08** | **MEDIUM** | C | ARCH §6.3 | Consecutive-loss counter reset is unspecified. The spec says "last `max_consecutive_losses` trades all losers ⇒ reject" but does **not** state whether a winning trade resets the counter to zero. Also, manual/KILL closes are not addressed. | Explicitly state: counter **resets to 0 on any realized winning trade** (exit P&L > 0). Manual/KILL closes count as a loss if P&L < 0, win if P&L > 0. Log counter value in `gate_results`. |
| **F-09** | **MEDIUM** | F | ARCH §8, §9 | No API endpoint serves the **Gate Monitor card** data in structured form. The Overview page needs the latest `gate_results` array, but the only relevant endpoint is `/api/decisions` which returns raw payload JSON. The builder must guess the JSON shape. | Add `GET /api/gates/latest` returning `{trade_id, decision_id, gate_results: [{gate, status, detail}]}` or append `latest_gate` to `/api/status`. |
| **F-10** | **MEDIUM** | H | PREREG §5, §6 | Slippage expected_px is defined as "bar close at signal" for all order types. For **MKT orders**, the fill is the next available price (typically the next bar open, which may gap overnight). This will **inflate slippage bps** with gap risk, making the 25 bps threshold misleading. | Define `expected_px` per order type: for **LMT**, use limit price; for **MKT**, use the mid-price at `submit_ts` (or next bar open if no quote). Document that slippage on MKT includes gap risk, and add a separate `execution_slippage` metric using `submit_ts` mid if available. |
| **F-11** | **MEDIUM** | E | ARCH §6.5, §7, PREREG §5 | `max_intraday_dd` is a pre-registered metric but the schema does **not** specify equity sampling frequency. A single daily equity snapshot cannot capture the true intraday drawdown. | Specify: the **Reconciler logs equity snapshot every 60 s during RTH** (configurable). Store in `equity` table. Add a `daily_max_drawdown` computed column or a separate `daily_stats` table updated at market close. |
| **F-12** | **LOW** | F | ARCH §8 | Chart endpoint `/api/bars?n=300` response format is unspecified. `lightweight-charts` expects `{time: unix, open, high, low, close, volume}`. The builder must guess the JSON shape. | Add explicit response format to §8: `{"bars": [{"time": unix_ms, "open": ..., "high": ..., "low": ..., "close": ..., "volume": ...}]}`. |
| **F-13** | **LOW** | C | ARCH §6.3 | RiskEngine checks `max_position_notional_pct` but **never checks buying_power**. On a cash account or restricted margin account, the order could be rejected by the broker even after passing risk checks. | Add check #6b: `qty * ref_price <= buying_power * 0.95` (5 % buffer). Reject reason: `INSUFFICIENT_BUYING_POWER`. |
| **F-14** | **LOW** | G | ARCH §8, §11 | No CORS or API rate-limiting is specified. FastAPI defaults allow cross-origin requests. If the user later exposes the dashboard via Cloudflare Tunnel (§13 roadmap), the API is unauthenticated and unrate-limited. | Add `CORSMiddleware` restricted to `127.0.0.1` origins only. Add a note in §11: **rate limiting and authentication are required before any non-localhost exposure**; they are not in v1 scope but are mandatory prerequisites for tunnel/VPS. |
| **F-15** | **LOW** | I | BUILD §Task 10 | Task 10 (Dashboard, 150 m) is **optimistic** for 6 pages + charts + WS + dark theme + modals in vanilla JS. Spec ambiguities (chart markers, Gate Monitor data source, WS reconnect) will burn builder time. | Split into **Task 10a** (Overview, Trading, Config — 90 m) and **Task 10b** (Journal, LLM, System — 60 m). Add a 30 m buffer, or extend to 180 m total. |
| **F-16** | **LOW** | D | ARCH §6.4 | No **cost ceiling** or rate-limiting is specified for LLM calls. Grok every 4 h is cheap, but Claude per-trade can be expensive if the strategy trades frequently (e.g., 10+ times/day). | Add config `llm.max_daily_veto_cost_usd` (default $5) and `llm.max_vetos_per_day` (default 20). When exceeded, veto gate auto-skips with `LLM_COST_LIMIT` event. |

## 3. Dimension notes

### A. Broker/API correctness

`ib_async` auto-reconnect is convenient but the design leans on it too heavily for TWS restart. The **CRITICAL** finding (F-01) dominates this dimension: the reconciler’s "naked position = flatten" rule will misfire after every TWS restart if paper orders are lost. This must be fixed before P2.

`reqMarketDataType(3)` is correct for paper without subscriptions, but the builder should note that historical data requests may still succeed without it (the type is mainly for real-time market data). The `useRTH=True` + 1h bars for AAPL is correct; the first bar after 9:30 ET is partial (9:30–10:00) and the strategy must handle it. The bar-close detection logic (F-05) needs to be explicit to avoid builder divergence.

Bracket/OCA semantics: modifying the SL via `ib.placeOrder` with the same `orderId` preserves the OCA group. The design is correct here, but partial-fill TP sizing (not mentioned) should also be clamped to the filled qty.

**No findings** on clientId collisions (default 17 is fine for a single client) or RTH vs pre/post-market (the spec correctly limits to RTH).

### B. State machine & concurrency

The three-state machine (DISARMED / ARMED / KILLED) is clean, but the **undefined trail behavior while DISARMED** (F-02) is a real ambiguity. A builder might implement either freeze or continue, with very different safety implications. The flip sequence (F-07) is also a guess zone: without a defined sub-state machine, the builder may submit the new entry before the old position is closed, creating a momentary double exposure.

Race conditions: the "synchronous per bar, no queues" design is correct for one symbol × one strategy. The duplicate-signal guard (`symbol, direction, bar_ts`) is good. The stale-price guard (`max_price_age_s: 90`) is reasonable for active equities but should use the last *tick* time, not the last *bar* time, otherwise it could reject during quiet periods.

Restart recovery: the reconciler’s position-adoption logic is sound **except** for the TWS restart case (F-01). KILLED persisting across restart is implied but not explicit; recommend adding `state` to the `runs` table or a `state` file in `data/`.

### C. Risk engine math & completeness

The sizing formula is the right fixed-fractional approach, but the **division-by-zero hole** (F-03) is a genuine crash risk. A gap or data error could set `stop_distance` to zero before the notional clamp runs. The `min_stop_distance` guard is cheap and necessary.

Daily-loss accounting (F-06) is underspecified in timezone. The formula `realized_today + unrealized` is mark-to-market, which is conservative but can trigger false positives on large unrealized drawdowns that later recover. Barış’s taste is conservative, so this is acceptable, but the timezone boundary must be explicit.

Consecutive-loss / cooldown interaction (F-08): the counter reset rule is missing. If the builder assumes it resets on any winner, that’s correct; if not, the strategy could DISARM permanently after three losers even if the next trade is a winner. The cooldown (`cooldown_minutes_after_loss`) should probably only apply to the *most recent* loss, not all losses.

Missing risk rules: **buying power check** (F-13), **max trades per day** (not in v1, acceptable), **max spread** (not in v1, acceptable), and **position-size in shares** (only notional % is checked). For AAPL at ~$200, notional % is equivalent to share count, so this is fine for v1.

### D. LLM gate

The "narrowing-only, fail-open, hard code boundary" design is **structurally enforceable** as specified. The `RegimeDirective` and veto JSON schemas are strict; the code only extracts `regime`, `confidence`, `verdict`, and `reason`. There is no code path from LLM output to qty or price. This is the correct defensive design.

Prompt-injection surface via Grok/X content is real but mitigated by the narrowing-only rule: an attacker can only induce `NO_TRADE` (most restrictive), which is a denial-of-service, not a financial exploit. The `fail_policy: open` default is a human decision (Barış) and correctly documented. The 10 s veto timeout is acceptable for 1h bars.

**Cost ceiling** (F-16) is a missing operational guard. A volatile day could generate 20+ signals, each triggering a Claude call. At ~$0.01–$0.03 per call, this is negligible, but for future strategies with higher frequency, a ceiling is cheap insurance.

### E. Data & persistence

The schema is minimalist but functional for v1. The **Journal drawer schema gap** (F-04) is the most significant: the `orders` table needs a `trade_id` column, or the decision chain cannot be reconstructed per trade. The `max_intraday_dd` sampling gap (F-11) means the PREREG metric is technically uncomputable from the schema as written.

Missing indices: for P3 analysis, queries on `decisions(run_id, ts)`, `trades(run_id, symbol)`, and `events(run_id, severity)` will be slow without indices. Add at build time:
```sql
CREATE INDEX idx_decisions_run_ts ON decisions(run_id, ts);
CREATE INDEX idx_trades_run ON trades(run_id);
CREATE INDEX idx_events_run_sev ON events(run_id, severity);
```

Clock/timezone policy: "all ts UTC ISO" is correct for storage, but the engine must convert to ET for RTH checks. The design should explicitly state: **storage = UTC, display = local (ET for AAPL), RTH logic = ET.**

`payload_json` schema evolution: no versioning is mentioned. Recommend adding `payload_version` to the `decisions` table or a top-level `version` field in the JSON.

### F. Dashboard & API

The dashboard spec is comprehensive for a 1-day build, but several ambiguities will force the builder to guess:

- **Gate Monitor card** (F-09): no data source specified.
- **Chart endpoint format** (F-12): no JSON shape specified.
- **WS reconnect behavior**: the design says "Dashboard is fully WS-driven after initial REST load" but does not specify what happens on WS reconnect. The client should do a full REST refresh and re-subscribe to topics.
- **Decision-chain drawer** (F-04): blocked by schema gap.
- **System page config snapshot**: there is no `/api/runs/{run_id}` endpoint; the builder must add it or repurpose `/api/config`.
- **Confirm-nonce**: the design uses `X-Confirm` header from `/api/status`. This is correct for REST, but if dangerous ops are ever exposed via WS, the nonce must be checked there too. For v1, only REST dangerous ops are specified, so this is fine.

The 6-page scope in 150 minutes (F-15) is aggressive but doable if the spec is tightened. The dark theme color spec is good and copy-pasteable.

### G. Security

localhost-only binding (`127.0.0.1:8790`) is correct for v1. Secrets handling via pydantic-settings + env is standard. The **double-lock for live port** (env var + dashboard confirm + `live_allowed` flag) is a robust three-layer defense.

**CORS / rate limiting** (F-14) is a LOW finding because it only matters if the user deviates from localhost. The roadmap (§13) correctly notes "Login + 2FA + roles REQUIRED before any non-localhost exposure." Add the same note to the API spec.

What breaks on tunnel/VPS: the dashboard is unauthenticated, so anyone with the tunnel URL can arm/disarm/kill. The roadmap acknowledges this but does not list it as a prerequisite for the tunnel phase. It should be: **tunnel phase is monitor-only, with config edits blocked remotely, but ARM/KILL should also be blocked remotely until auth is added.**

### H. PREREG soundness

**Signal parity rule** (≥95 %): well-defined and measurable, but the "identical bars" assumption is fragile. The bridge uses delayed IBKR data (15 min) while the offline engine uses the Alpaca bundle. Bar timestamps and OHLCV may differ slightly. The P3 comparison should use **bridge-logged bars** (from `BarFeed`) as the input to the offline replay, not the original bundle. The design does not specify this.

**LLM veto audit**: "veto precision reviewed" is subjective. The design should add a proxy metric: **"veto precision rate"** = (# of vetoed trades that would have been losers based on forward price movement at exit) / (total vetoes). If this rate is < 50 %, demote to flag-only.

**Slippage rule** (25 bps): well-defined, but the `expected_px` definition (F-10) needs to account for MKT order gap risk. Otherwise, slippage will routinely exceed 25 bps on overnight gaps and trigger a false investigation.

Gates P0-P3 are well-sequenced and have clear exit criteria. The abort criteria (PREREG §7) are comprehensive and correctly wired to auto-DISARM.

### I. Build plan feasibility

**Task order is correct**: mock-first (Tasks 1–7) before IBKR adapter (Task 8) is the right risk-mitigation strategy. Hidden dependencies:

- **Task 3** (MockBroker fixture) requires the builder to locate or generate AAPL 1h data. The Alpaca bundle location is not specified in the design; the builder may waste time searching. Add a note: "Fixture generator script reads from `MTC_COMMAND_CENTER/...` Alpaca bundle or falls back to synthetic."
- **Task 4** (Strategy port) requires generating the golden signal list from QuantLens. The builder needs to know exactly how to run the offline engine. If the FAZ 3B artifacts are not in the expected path, this task blocks.
- **Task 6** (Engine on mock) is the integration point for Tasks 3, 4, 5. The 90 m estimate is tight but plausible if the builder is experienced with asyncio state machines.
- **Task 8** (IBKRBroker) 90 m is tight for reconnect, bracket, live-port refusal, and error handling. The integration test (`tools/smoke_p0.py`) is gated by Barış approval, which is correct.
- **Task 10** (Dashboard) 150 m is the most likely to overrun (F-15). The Gate Monitor card, WS-driven updates, and chart markers are each non-trivial in vanilla JS.
- **Task 11** (Notifier + polish) 45 m is reasonable.

**Missing tasks**:
- No explicit task for **generating the golden signal list** from QuantLens (implied in Task 4 but not a standalone task).
- No explicit task for **writing the `docs/03_STATUS.md`** known-gaps log (mentioned in Task 11 but not a standalone task).
- No explicit task for **trail exit logic testing** on MockBroker (SL/TP are tested, but trail modifications are not explicitly covered).

Acceptance criteria gaps:
- Task 6: "same-bar signal re-delivery → exactly one order" is good, but does not test **reconnect replay** (TWS sending the same bar twice with a gap).
- Task 10: "Manual: dry-run replay visible live" is a manual test; it proves the dashboard runs but not that every page is correct.

## 4. Improvements

| # | What | Why | Cost | Doc / § | Fits v1? |
|---|---|---|---|---|---|
| **IMP-01** | **TWS restart recovery**: on reconnect, if position exists but no SL/TP orders, re-submit bracket for existing position before concluding naked position. Add `recover_orders_after_restart: true` (default true for paper, false for live). | Prevents nightly unwanted flatten (F-01), making unattended P2 possible. | **M** | ARCH §5, §6.1 | **v1.1** (safe to defer if P0 proves orders persist; but if they don't, this is P2-blocking) |
| **IMP-02** | **Add `trade_id` to `orders` and `decisions` tables**: `orders.trade_id INT` (nullable until fill), and `decisions.trade_id INT` at SUBMITTED stage. | Enables the Journal decision-chain drawer (F-04); without it, the Journal page is unbuildable as spec'd. | **S** | ARCH §7 | **v1** |
| **IMP-03** | **Add `min_stop_distance` guard and `buying_power` check**: reject if `stop_distance <= min_stop_distance` (e.g., $0.01) before sizing; add `qty * ref_price <= buying_power * 0.95` after notional clamp. | Prevents ZeroDivisionError (F-03) and broker rejects from insufficient funds (F-13). | **S** | ARCH §6.3 | **v1** |
| **IMP-04** | **Explicit DISARMED trail freeze**: amend state machine: DISARMED stops trail recalculation per bar; existing SL/TP remain at last price. Trail resumes on re-ARM. | Removes ambiguity (F-02); prevents DISARMED from still actively trading via trail modifications. | **S** | ARCH §5 | **v1** |
| **IMP-05** | **Add `GET /api/gates/latest` endpoint**: return structured `gate_results` for the most recent decision, plus `GET /api/runs/{run_id}` for System page config snapshot. | Removes dashboard guesswork (F-09, F-12). | **S** | ARCH §8 | **v1** |
| **IMP-06** | **Define `expected_px` per order type**: MKT orders use mid-price at `submit_ts` (or next bar open) as expected; LMT orders use limit price. Document gap-risk inclusion. | Makes the 25 bps slippage rule meaningful (F-10). | **S** | PREREG §5 | **v1** |
| **IMP-07** | **Add RTH checker with NYSE hours**: hardcode NYSE RTH 09:30–16:00 ET for v1; use `zoneinfo` for timezone. Store `day_start_equity` at 09:30 ET. | Removes timezone ambiguity (F-06) and makes daily-loss accounting deterministic. | **S** | ARCH §6.3, §7 | **v1** |
| **IMP-08** | **Consecutive-loss counter reset rule**: explicit in risk checks: counter resets to 0 on any realized winning trade; manual/KILL closes count based on P&L. | Prevents permanent DISARM after three losers (F-08). | **S** | ARCH §6.3 | **v1** |
| **IMP-09** | **Equity sampling for max intraday DD**: Reconciler logs `equity` snapshot every 60 s during RTH; add `daily_max_drawdown` to `equity` table or a new `daily_stats` table. | Makes PREREG §5 `max_intraday_dd` computable (F-11). | **S** | ARCH §6.5, §7 | **v1** |
| **IMP-10** | **Split Task 10 into 10a + 10b + 30 m buffer**: 10a = Overview + Trading + Config (90 m); 10b = Journal + LLM + System (60 m). Total 180 m. | Prevents dashboard overrun (F-15). | **S** | BUILD §Task 10 | **v1** |
| **IMP-11** | **Add flip sub-state machine**: (1) cancel bracket, (2) submit reduce-only market close, (3) wait for fill ack, (4) submit new entry. Log `FLIP_CLOSE_REJECTED` on failure. | Prevents double exposure and undefined behavior (F-07). | **M** | ARCH §5 | **v1** |
| **IMP-12** | **Add `bar-close` detection algorithm to §6.1**: track `last_bar_ts`, compare `bars[-1].date`, emit previous bar on increase. Handle reconnect reset. | Removes builder guesswork (F-05). | **S** | ARCH §6.1 | **v1** |

## 5. Feature ideas

| # | Feature | User value for solo systematic trader | Cost | Phase | Risk introduced |
|---|---|---|---|---|---|
| **FEA-01** | **Broker health scorecard** — dashboard page tracking API latency, reconnect frequency, order ack time, fill ratio, and 7-day trend. | Early warning for API degradation (e.g., TWS sluggishness before a major move). Prevents missed fills blamed on "the strategy." | **S** | **v1.1** | Negligible. Read-only. |
| **FEA-02** | **Auto-regime fallback on data staleness** — independent of LLM, if `BarFeed` reports `DATA_STALE` (or last bar > 2× bar period), the engine auto-overrides regime to `NO_TRADE` regardless of Grok output. | Hard safety net: even if Grok is stale or wrong, missing data stops trading. | **S** | **v1** | Could over-trigger if data staleness is transient; requires a grace count (e.g., 2 consecutive stale events). |
| **FEA-03** | **Trade annotation / bar snapshot on fill** — store the full OHLCV bar (and optionally last 5 bars) at entry and exit in a `trade_snapshots` table. | Enables visual debugging: "Why did this trade enter here?" Reduces reliance on external charting for journal review. | **M** | **v1.1** | Storage bloat; cap at 5 bars per trade (~1 KB each). |
| **FEA-04** | **Paper equity divergence monitor** — compare bridge-computed equity (`trades` + `equity` table) against broker-reported equity (`AccountSnapshot`). Alert if diverged > 0.5 %. | Catches reconciliation bugs (missed fills, double-counting, partial fill mishandling) before they compound. | **S** | **v1.1** | Could false-positive if broker includes unsettled cash or other positions; needs a tolerance threshold. |
| **FEA-05** | **One-click export decisions to Parquet** — `POST /api/export/decisions` generates a Parquet file of the full `decisions` + `orders` + `trades` chain for a date range. | Enables offline analysis in Python/pandas without SQL queries. Fits Barış’s research workflow. | **S** | **v1.1** | File I/O; requires disk space check. No trading risk. |
| **FEA-06** | **Manual execution ticket** — dashboard form where Barış enters symbol, direction, and risk $; the engine runs the full risk + LLM gate check and submits a bracket. | Allows discretionary override while keeping all safety rails (risk, LLM veto, logging). | **M** | **v1.1** | Already in roadmap; re-listing here because it is high-value for a solo trader who wants to act on a non-signal insight. |
| **FEA-07** | **Strategy parameter sensitivity heatmap** — dashboard page that replays the last N bars with ±10 % parameter perturbations and shows signal-frequency heatmap. | Rapidly answers "Would this parameter change have avoided that whipsaw?" without a full backtest. | **M** | **v2** | CPU-intensive; must run in background thread to avoid blocking trading loop. |
| **FEA-08** | **Event gate (CPI / FOMC / earnings hard block)** — calendar-based hard gate that auto-rejects signals within ±30 min of known macro events. | Complements LLM regime with deterministic, zero-latency protection. Prevents trading into known volatility. | **M** | **v1.1** | Requires event data source (e.g., `economcal.com` API or manual CSV). Stale calendar = false confidence. |
| **FEA-09** | **Position size optimizer (Kelly criterion)** — optional risk model that computes `f*` from recent trade history and caps at `risk_pct_per_trade`. | Systematic sizing based on edge quality rather than fixed %. | **M** | **v2** | Overfitting risk if Kelly window is too short; requires a floor/ceiling clamp. |
| **FEA-10** | **Multi-timeframe regime consensus** — Grok regime checks 1h, 4h, and daily alignment; only trade if ≥2 of 3 agree. | Reduces false signals in choppy markets where a single timeframe is noisy. | **L** | **v2** | Adds complexity to LLM prompt and latency; could over-filter. |

## 6. Top-3 verdict

**1. Fix TWS restart recovery (F-01 / IMP-01)** — If this is not fixed, the bridge will flatten its position every night when TWS restarts, making the PREREG P2 gate (unattended ≥10 trading days) literally impossible. The reconciler’s "naked position = flatten" rule is correct for safety, but it must be preceded by a re-submit attempt for the existing position. This is a design-level bug, not an implementation detail. It should be the first fix because it determines whether the product can survive a single night without human intervention. Cost is medium because it touches reconnect, reconciler, and order submission paths, but it fits v1.1 without breaking the 1-day build if P0 proves that paper orders actually persist (which is uncertain). If P0 shows orders are lost, this becomes a v1-blocker.

**2. Add `trade_id` linkage to schema (F-04 / IMP-02)** — The Journal page is one of the six dashboard pages and a core differentiator for the product. The spec says "click row → decision-chain drawer" but the SQLite schema as written provides no foreign key to join a trade to its decisions. A builder will either (a) hack a join via `symbol` + `ts` range, which is fragile, or (b) skip the drawer entirely, leaving a broken feature. This is a 5-minute schema change (`ALTER TABLE orders ADD COLUMN trade_id`) that unlocks a major UI component. It should be in v1 because it is trivial and prevents builder guesswork.

**3. Add stop-distance validation and buying-power check (F-03 / IMP-03)** — The sizing formula `floor(risk_dollars / stop_distance)` will crash with a `ZeroDivisionError` if a data gap or strategy bug produces `stop_distance = 0`. This is a runtime exception in the critical trading path. The `max_position_notional_pct` clamp is evaluated after sizing, so it cannot prevent the crash. A `min_stop_distance` guard (e.g., `$0.01`) and a `buying_power` check are pure additions to the RiskEngine with no side effects, fully unit-testable, and prevent two classes of hard failure: Python exceptions and broker rejections. This is a 15-minute change with high safety ROI and should be in v1.
