# Audit — IBKR Paper Bridge design
Model: Cursor Composer | Date: 2026-07-05 | Docs commit: c2c3bbb0

## 1. Summary verdict

**Ship-with-fixes.** The architecture is coherent for a solo paper-plumbing v1: mock-first build order, narrowing-only LLM, bracket-centric execution, and PREREG gates are the right skeleton. However, several spec holes will cause wrong orders, false aborts, or unmeasurable P3 gates if built literally — especially IBKR identity persistence across reconnects, delayed-data vs stale-price contradiction, DISARMED behavior with open positions, trading-day timezone for risk accounting, and synchronous LLM veto on the bar-close hot path. Fix ~8 HIGH/CRITICAL items in the design docs before the one-day build; defer multi-broker and auth to roadmap as already planned.

---

## 2. Findings

| ID | Severity | Dimension | Location doc§ | Issue | Suggested fix |
|---|---|---|---|---|---|
| F-01 | CRITICAL | A | 01_ARCH §6.1, §6.5 | `reqMarketDataType(3)` yields up-to-15-min-delayed TRADES; `max_price_age_s: 90` at submit will reject valid signals or force false `STALE_PRICE` during normal paper operation. | Decouple bar-clock staleness from quote freshness: for delayed type 3, disable or scale `max_price_age_s` to bar-period logic; log `data_type` and use bar `close` age, not tick age, for 1h mode. |
| F-02 | CRITICAL | A | 01_ARCH §6.1, §6.5 | Order identity across TWS reconnect uses `order_id TEXT` only; IBKR reissues `orderId` on reconnect while `permId` is stable. Reconciler matching on ephemeral ids orphans brackets after nightly restart (P2 criterion). | Store `perm_id`, `parent_id`, `oca_group` on every order row; reconcile by `permId` first; map legacy ids on reconnect event. |
| F-03 | CRITICAL | B | 01_ARCH §5 | DISARMED cancels entry orders but leaves SL/TP working; trail modify (§5, §6.2) is engine-driven each bar — spec silent on whether DISARMED still modifies stops. If yes, disarm is cosmetic; if no, trail stops freeze while position remains naked to gap risk without updated trail. | Explicit rule: DISARMED + open position ⇒ trail updates continue, no new entries; document in §5 state table. |
| F-04 | CRITICAL | B | 01_ARCH §5, §6.5 | Bar-close path is synchronous; fill/partial-fill/`orderStatus` events are async. No ordering guarantee between `on_bar()` sizing and a fill updating position qty before trail/flip submit — close orders can overshoot or flip can double-size. | Serialize per-symbol execution behind a mutex/actor queue: bar decisions enqueue; fill events drain queue before next submit; position qty always read from broker at submit. |
| F-05 | HIGH | A | 01_ARCH §6.1 | `keepUpToDate` bar-close rule ("new bar object appears") breaks across reconnect (history replay), partial first bar after open, and early-close sessions; ib_async may mutate last bar in place on some builds. | BarFeed maintains local finalized-bar buffer; close = timestamp strictly advances + optional exchange-calendar validation; unit-test reconnect replay fixture. |
| F-06 | HIGH | A | 01_ARCH §6.1 | Manual MKT bracket (`transmit=False` parent + OCA children) is a common IBKR footgun: wrong transmit sequence leaves orphan children or rejected combos on paper. | Document exact placement sequence; integration test in P0; fallback to `ib.bracketOrder` with dummy limit then replace with market parent if API allows. |
| F-07 | HIGH | A | 01_ARCH §6.1, 00_PREREG §3 | `useRTH=True` 1h bars vs signal at "bar close" — last bar of session may close before 16:00 ET; pre/post bars excluded but abort staleness (§6.6) still runs "during market hours" without defining calendar (half-days, holidays). | Wire `exchange_calendars` NYSE schedule; staleness disabled outside session; document AAPL 1h bar labeling (bar end time convention). |
| F-08 | HIGH | B | 01_ARCH §5 | KILLED requires app restart to re-arm but KILLED state persistence across process restart is unspecified — restart could come up DISARMED and trade into a KILL-intended flat state. | Persist `app_state` in SQLite; startup always reconciles broker first; KILLED survives restart until explicit ack workflow. |
| F-09 | HIGH | B | 01_ARCH §5 | Flip=false + opposite signal says "just close" but no order type, timing (same bar vs next open), or reduce-only path specified — implementer will guess MKT vs cancel bracket. | Add `exit_on_opposite_signal: CLOSE_AT_NEXT_OPEN \| CLOSE_IMMEDIATE` and always reduce-only market close with decision row. |
| F-10 | HIGH | C | 01_ARCH §6.3 | `qty = floor(risk_dollars / stop_distance)` — zero or near-zero `stop_distance` (band pinch, bad ATR) yields div-by-zero or absurd size before notional clamp. | Min stop distance = `max(tick_size, 0.1% of ref_price, atr_floor)`; reject `stop_too_tight` before sizing. |
| F-11 | HIGH | C | 01_ARCH §6.3, 00_PREREG §7 | Daily loss uses `realized_today + unrealized` vs `day_start_equity` but "today" timezone unstated while schema mandates UTC — off-by-one around midnight UTC vs ET session boundary. | Define trading day = America/New_York date; snapshot `day_start_equity` at first RTH bar or configurable roll time; store `trading_date` on equity rows. |
| F-12 | HIGH | C | 01_ARCH §6.3, 00_PREREG §7 | Consecutive-loss counter and cooldown trigger on "SL exit" (§6.3 4c) but exits include `TRAIL`, `SIGNAL_FLIP`, `TP` — a trail stop loss may not increment losses or trigger cooldown, undermining abort intent. | Consecutive losses = `pnl < 0` regardless of `exit_reason`; cooldown after any losing trade close. |
| F-13 | HIGH | D | 01_ARCH §6.4 | Regime directive TTL expiry ⇒ `BOTH` silently widens from active `NO_TRADE` / narrowed regime — contradicts "LLM only reduces risk" for the TTL window after a valid high-confidence veto of direction. | On TTL expiry, fall back to last valid directive narrowed by config, or `config.direction` only — never auto-widen to BOTH; require explicit refresh. |
| F-14 | HIGH | D | 01_ARCH §6.4, §3 | Pre-trade veto is on synchronous bar path with 10s timeout — blocks entire engine loop; under slow API, bar-close decisions slip to next minute and orders fire off stale intent. | Run veto async with `decision deadline = bar_close + Ns`; if incomplete, fail-open to `LLM_SKIPPED` without blocking reconciler/fill handlers. |
| F-15 | HIGH | D | 01_ARCH §6.4 | Grok ingests X/headlines — prompt-injection via malicious headline text can force `NO_TRADE` or confidence gaming; narrowing-only does not block regime=NO_TRADE denial of all trades. | Strip HTML/URLs; schema-validate; cap rationale length; ignore directives whose `sources` are empty; optional allowlist of source domains; log raw hash not raw text in DB. |
| F-16 | HIGH | E | 01_ARCH §7, 00_PREREG §5 | `trades` table has no `decision_id` / `signal_ts` / `submit_ts` columns — P3 per-trade metrics require multi-table reconstruction with ambiguous joins if multiple decisions per bar. | Add FK `entry_decision_id`, denormalized `signal_ts`, `submit_ts`, `expected_px`, `llm_directive_id` on `trades`. |
| F-17 | HIGH | E | 01_ARCH §7, 00_PREREG §5 | `max intraday DD` per day not computable — `equity` table has no sampling policy (only implied event writes); sparse rows understate DD. | Equity snapshot every 60s during RTH + on every fill; add `intraday_peak_equity` rolling column or materialized daily summary table. |
| F-18 | HIGH | F | 01_ARCH §8, §9 | WebSocket spec lacks reconnect contract — after drop, client may miss `DISARM`/`KILL` events; no `GET /api/snapshot` full-state resync endpoint defined. | On WS connect, server pushes full snapshot message; document client resync sequence; heartbeat + `status` topic on interval. |
| F-19 | HIGH | G | 01_ARCH §11, §13 | §13 says tunnel phase allows remote ARM/KILL without auth — any tunnel URL holder can trade paper now and live later. Contradicts §13 login requirement "before non-localhost exposure." | Tunnel phase: monitor-only WS/REST; ARM/KILL localhost-only until auth ships; or mandatory Tailscale ACL + token. |
| F-20 | HIGH | H | 00_PREREG §6 | Signal parity ≥95% references "offline engine replay on identical bars" but live bars are IBKR delayed/RTH while golden likely from Alpaca bundle (02_BUILD_PLAN task 3) — bars are not identical. | P3 parity uses archived IBKR bar export as canonical; define bar alignment rules (timestamp, adjust for splits); report mismatch taxonomy. |
| F-21 | HIGH | H | 00_PREREG §6 | "Veto precision reviewed; if noise ⇒ demote" — no metric, sample size, or threshold; not measurable as written. | Pre-register: review last N vetoes; precision = vetoes where next-bar adverse move ≥X bps without veto; demote if precision <40% after ≥20 vetoes. |
| F-22 | HIGH | I | 02_BUILD_PLAN | Task estimates sum to ~735 min (12.25 h) excluding integration/debug — exceeds one working day; task 6 (90m) and task 10 (150m) are especially optimistic. | Cut v1 dashboard to 3 pages (Overview, Journal, System) or defer LLM/Notifier pages; mark task 10 as 240m or v1.1; add explicit scope-cut list. |
| F-23 | MEDIUM | B | 01_ARCH §6.5 | Naked-position flatten depends on 60s reconciler — up to 60s unprotected violates spirit of PREREG §7 "flatten immediately." | Subscribe to `positionEvent` / order status; naked check on every fill and position update, reconciler as backup. |
| F-24 | MEDIUM | C | 01_ARCH §6.3 | Gap-through-stop not reflected in risk sizing (uses static stop distance) — acceptable for paper but daily loss can exceed `max_daily_loss_pct` intrabar. | Add optional `worst_case_gap_pct` clamp on notional or document as known paper limitation in PREREG. |
| F-25 | MEDIUM | E | 01_ARCH §7 | No indices on `decisions(run_id, ts)`, `orders(decision_id)`, `events(severity, ts)` — journal and P3 queries will degrade over 30 days. | Add indices in schema §7; note in task 2 acceptance. |
| F-26 | MEDIUM | F | 01_ARCH §9 | Gate Monitor shows `gate_results` including LLM gates, but RiskEngine §6.3 owns gate_results list while LLM runs after risk — unclear single payload shape and who appends LLM rows. | Engine assembles unified `gate_results` post-pipeline; store once on final pre-submit decision row. |
| F-27 | MEDIUM | F | 01_ARCH §8 | `X-Confirm` nonce rotation after arm/disarm/kill not specified — stale tab might hold valid nonce briefly. | Nonce rotates on every state transition; dangerous ops reject nonce older than 30s. |
| F-28 | MEDIUM | I | 02_BUILD_PLAN | Task 6 builds full engine without LLM stub (task 9 later) — dry-run won't exercise LLM_SKIPPED/fail-open paths in integration test. | Insert `NullLLMGate` in task 6; task 9 swaps implementation; extend `test_engine_dryrun` for veto timeout injection. |
| F-29 | MEDIUM | I | 02_BUILD_PLAN | Task 2 acceptance cites `test_store` but §2 directory layout lists no `test_store.py` — acceptance doesn't prove migrations. | Add `tests/test_store.py` to layout and task 2 deliverable. |
| F-30 | LOW | A | 01_ARCH §6.1 | `clientId` collision fails at startup only — TWS restart with same client connected causes subtle partial connection. | Retry with documented alternate ids; surface clear dashboard error. |
| F-31 | LOW | G | 01_ARCH §10 | API keys in env on shared Windows host — no mention of user-level secret store. | Document OS credential manager pattern in quickstart; never log env at startup. |

---

## 3. Dimension notes

### A. Broker/API correctness
Delayed type 3 + 90s stale guard is the sharpest contradiction (F-01). IBKR identity (`permId`) and MKT bracket placement (F-02, F-06) are the other paper-to-P2 blockers. Bar-close detection (F-05) and exchange calendar (F-07) need explicit fixtures before IBKRBroker is "done."

### B. State machine & concurrency
DISARMED vs trail (F-03), async fill vs sync bar (F-04), flip semantics (F-09), and KILLED persistence (F-08) are underspecified enough that two builders would ship incompatible behavior. Partial-fill handling is mentioned (§6.5) but not wired to state machine transitions.

### C. Risk engine math & completeness
Sizing edge cases (F-10), trading-day boundary (F-11), and consecutive-loss definition (F-12) will cause either runaway size or silent abort bypass. Gap risk (F-24) is acceptable for v1 if documented. Equity currency assumed USD — no finding if AAPL-only v1.

### D. LLM gate
Hard JSON boundary is sound in principle; enforceability breaks on TTL widen (F-13), synchronous latency (F-14), and untrusted Grok content (F-15). Fail-open on veto timeout aligns with README but must not block the event loop.

### E. Data & persistence
Schema cannot cleanly produce PREREG §5 without trade/decision linkage and equity sampling policy (F-16, F-17). UTC storage is fine if trading-day derivation is explicit (F-11). Indices (F-25) are cheap v1 wins.

### F. Dashboard & API
Six pages are buildable from spec but WS reconnect (F-18), nonce lifecycle (F-27), and gate_results ownership (F-26) will cause frontend/backend mismatch. Journal drawer depends on F-16 fix.

### G. Security
Localhost-only v1 is appropriate. §13 tunnel allowing remote ARM/KILL without auth (F-19) is the main forward-looking hole. Live double-lock is good; local malware can still set `IBKR_LIVE_ACK` — acceptable for solo machine if acknowledged.

### H. PREREG soundness
Gates P0–P2 are concrete. P3 parity (F-20) and veto audit (F-21) are not yet scientifically pre-registered — they will become arguments instead of decisions. Slippage rule (25 bps median) is measurable once `expected_px` is defined as bar close vs next-bar open fill (state explicitly in PREREG §5).

### I. Build plan feasibility
Mock-first order is correct. Total time exceeds one day (F-22); task 8 IBKR integration should not block dry-run demo (already noted). Missing `test_store` (F-29) and LLM ordering (F-28) are fixable plan edits.

---

## 4. Improvements

| # | What | Why | Cost | Amends | Phase |
|---|---|---|---|---|---|
| I-01 | Add `perm_id`/`oca_group` to orders schema + reconciler matching | P2 nightly restart survival | M | 01_ARCH §6.1, §6.5, §7 | v1 |
| I-02 | Trading-day roll in America/New_York + `day_start_equity` snapshot | Correct daily-loss and cooldown | S | 01_ARCH §6.3, §7; 00_PREREG §5 | v1 |
| I-03 | Per-symbol asyncio queue serializing bar logic and fill handlers | Prevents flip/partial-fill races | M | 01_ARCH §3, §5 | v1 |
| I-04 | `NullLLMGate` + async veto with deadline; engine never blocks >2s on LLM | Safe hot path | M | 01_ARCH §6.4, §3 | v1 |
| I-05 | Regime TTL fallback to `last_valid_directive` intersect config, not BOTH | Stops silent widen after NO_TRADE | S | 01_ARCH §6.4 | v1 |
| I-06 | `GET /api/snapshot` + WS full push on connect | Dashboard correctness after reconnect | S | 01_ARCH §8 | v1 |
| I-07 | Denormalize P3 trade metrics + equity 60s sampler | Makes PREREG metrics computable | M | 01_ARCH §7; 00_PREREG §5 | v1 |
| I-08 | Explicit DISARMED rules for open positions (trail continues, no entries) | Removes state ambiguity | S | 01_ARCH §5 | v1 |
| I-09 | IBKR bar export as parity canonical + alignment doc | Measurable signal parity | M | 00_PREREG §6 | v1.1 (post-P2 capture) |
| I-10 | Scope-cut: defer pages 5–6 (LLM/System split) to v1.1 | Fits one-day budget | S | 02_BUILD_PLAN task 10 | v1 |

---

## 5. Feature ideas

| # | Capability | User value (solo systematic trader) | Cost | Phase | Risk |
|---|---|---|---|---|---|
| FE-01 | **Decision replay mode** — feed stored bars through engine offline, diff decisions vs live log | Debug parity without TWS | M | v1.1 | None if read-only |
| FE-02 | **Bracket health panel** — live OCA group map, parent/child status, permId | Instant visibility when IBKR silently drops a child | M | v1.1 | Low |
| FE-03 | **Expected-vs-actual fill simulator** on MockBroker using spread/vol model | Calibrate slippage thresholds before live | M | v1.1 | False confidence if model naive |
| FE-04 | **Arm profile presets** ("conservative", "plumbing test") — one-click risk YAML | Faster iteration without manual config edits | S | v1.1 | User confusion if presets stale |
| FE-05 | **Broker clock skew monitor** — compare IBKR server time vs local UTC | Catches bar-close mis-labeling | S | v1.1 | Low |
| FE-06 | **Audit export bundle** — zip SQLite slice + config + redacted logs for PR | Handoff to future you or reviewer | S | v1.1 | Must redact API keys |
| FE-07 | **Position-scenario stress widget** — show P&L if gap ±X% through stop | Intuitive risk awareness | M | v2 | Educational only |

---

## 6. Top-3 verdict

**1. Fix IBKR order identity and execution serialization first (F-02, F-04, I-01, I-03).** If I were funding paper toward live, the highest-loss scenarios are not bad strategy signals but duplicate orders after reconnect, bracket orphans, and close orders sized on stale position qty. No amount of dashboard polish compensates for unreconciled `orderId`/`permId` drift across TWS nightly restarts. This is the foundation P2 explicitly tests; without it, "zero unexplained order states" is not achievable.

**2. Resolve delayed-data vs risk-clock semantics before writing BarFeed or RiskEngine (F-01, F-05, F-07, I-02).** The product's formal rule is bar-close-driven on 1h RTH bars, but the spec simultaneously imports tick-age guards and IBKR delayed feeds without a single clock policy. That will produce false stale aborts, missed entries, or parity failures that look like strategy bugs. Define one document section: bar timestamp convention, trading-day boundary, and what "fresh" means under `market_data_type: 3`.

**3. Make PREREG metrics actually computable and pre-register P3 decision rules (F-16, F-17, F-20, F-21, I-07).** Paper plumbing is the objective; if the schema cannot emit slippage, signal_ts chains, and intraday DD, P3 becomes a manual spreadsheet exercise and the LLM veto demotion rule becomes subjective. Denormalize trade-level metrics at fill time, sample equity during RTH, and write the parity and veto-precision operational definitions before the build day so tests assert them.
