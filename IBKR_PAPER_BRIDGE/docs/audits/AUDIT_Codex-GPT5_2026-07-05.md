# Audit - IBKR Paper Bridge design
Model: Codex GPT-5 | Date: 2026-07-05 | Docs commit: c2c3bbb0

## 1. Summary verdict

Ship-with-fixes for a mock-first v1, but not for unattended P2 until the IBKR bar/order/recovery contract is tightened. The design is directionally safe because it is paper-only, one-symbol, and LLM-narrowing-only. The weak points are measurable parity, IBKR order identity across reconnects, partial-fill recovery, and one-day estimate realism. I would not let a builder start Task 8 until the adapter acceptance tests are more exact.

## 2. Findings

| ID | Severity | Dimension A-I | Location doc section | Issue | Suggested fix |
|---|---|---|---|---|---|
| F-01 | HIGH | A, H, I | `01_ARCHITECTURE` sec. 6.2; `00_PREREG` sec. 6; `02_BUILD_PLAN` task 4 | The first strategy is intentionally changed from QuantLens stop-entry semantics to close-confirmed breakout plus market-next entry, but P3 requires at least 95% bridge-vs-offline signal parity on identical bars. A golden generated from the bridge port can pass while the bridge no longer matches the research engine. | Define the accepted semantic delta before build: either port the original signal semantics exactly, or change PREREG parity to compare a documented "bridge execution transform" against the offline engine. Golden timestamps must come from the original source engine, not the new port itself. |
| F-02 | HIGH | A, B, E | `01_ARCHITECTURE` sec. 6.1, 6.6 | `keepUpToDate=True` plus "new bar object means previous bar is final" is under-specified for IBKR. Hourly RTH bars need exchange-time bar keys, DST/holiday/half-day handling, delayed-data awareness, and idempotent finalization after reconnect replay. The design can miss, duplicate, or late-fire a bar close. | Add a `BarFinalizer` contract: exchange timezone, RTH session calendar, bar key `(symbol, tf, session_date, end_ts)`, finalization delay, duplicate suppression, and reconnect replay rules. Test half-day, holiday gap, reconnect replay, and delayed-data cases with fixtures. |
| F-03 | HIGH | A, B, E | `01_ARCHITECTURE` sec. 5, 6.1, 6.5, 7 | Order recovery depends on matching broker open orders to DB rows, but the schema stores only `order_id` and `decision_id`. IBKR recovery often needs `permId`, `parentId`, `clientId`, `ocaGroup`, transmit role, and local-vs-broker ID mapping; local order IDs are not a durable identity across sessions. | Persist broker identity fields: `perm_id`, `parent_perm_id`, `client_id`, `oca_group`, `transmit_role`, `broker_order_ref`, submitted contract JSON, and last known IB status. Reconciler should match by `permId` first, then conservative fallbacks. |
| F-04 | HIGH | A, B, C | `01_ARCHITECTURE` sec. 5, 6.5 | Partial-fill handling is too thin. "Cancel remainder, keep SL sized to filled qty" can leave child quantities wrong, TP/SL OCA inconsistent, or a naked partial position while modify/cancel events arrive out of order. This is an order-safety hole even in paper. | Add explicit states for `ENTRY_PARTIAL`, `ENTRY_FILLED_CHILDREN_RESIZE_PENDING`, `PROTECTED`, and `UNPROTECTED_ABORT`. Acceptance must simulate parent partial fills, child rejects, child resize failure, and out-of-order status callbacks. |
| F-05 | HIGH | G | `README` principle 3; `01_ARCHITECTURE` sec. 8, 11, 13 | The live double-lock is not strong enough as specified. `IBKR_LIVE_ACK` plus dashboard double-confirm can be accidentally enabled by config/env, and `X-Confirm` is a stale-tab guard, not authentication or authorization. The roadmap later allows tunnels where ARM/KILL remain enabled remotely. | For v1, remove live mode from normal runtime paths or require a separate `--enable-live` CLI flag plus env plus strategy `live_allowed`. Before any tunnel, add auth, origin checks, CSRF protection, read-only remote mode by default, and explicit remote-operation policy. |
| F-06 | MEDIUM | C, E | `00_PREREG` sec. 5-7; `01_ARCHITECTURE` sec. 6.3, 7 | Daily-loss math is not measurable enough. The design mixes realized and unrealized PnL, but does not define trading-day timezone, `day_start_equity` persistence, whether manual/non-bridge IBKR activity is included, or how realized PnL is reset after TWS restart. | Store `risk_day` rows keyed by exchange date with day-start equity, realized bridge PnL, unrealized bridge PnL, account equity snapshot, and reset policy. Define whether daily loss is bridge-only or whole-account. |
| F-07 | MEDIUM | C | `01_ARCHITECTURE` sec. 6.3, 10 | Sizing covers the basic formula but not stop-distance pathologies: zero/tiny stop distance, stop already crossed after a gap, stop on the wrong side of price, non-USD symbols later, fractional-share policy, and max-share clamp. | Add hard guards: minimum stop distance in bps/dollars, stop-side validation, gap-through-stop reject, max quantity, currency field on AccountSnapshot, and explicit integer-share policy for AAPL. |
| F-08 | MEDIUM | D, B, I | `01_ARCHITECTURE` sec. 3, 6.4; `02_BUILD_PLAN` task 9 | The per-trade Claude veto sits on the synchronous bar-to-order path with a 10 second timeout and fail-open default. That makes it both latency-sensitive and non-protective when unavailable. Grok/news/X input also creates a prompt-injection and source-trust surface, even though the parsed output is narrow. | Keep regime as cached background state. For v1, make pre-trade veto optional/off by default or run it as a precomputed advisory, not a hot-path dependency. Add source allowlist/redaction, prompt-injection tests, and explicit "LLM unavailable cannot delay order past N seconds" behavior. |
| F-09 | MEDIUM | E, H | `00_PREREG` sec. 5; `01_ARCHITECTURE` sec. 7 | The SQLite schema cannot compute every PREREG metric cleanly without parsing arbitrary JSON payloads. It lacks normalized signal rows, expected price, submit/fill latency fields, fill records, risk-at-entry percent, directive ID at entry, and indices/foreign keys. | Add normalized tables or columns for `signals`, `fills`, `decision_chain_links`, `trade_directive_id`, `expected_px`, `submit_ts`, `first_fill_ts`, `last_fill_ts`, and indexed `run_id/symbol/ts/stage`. JSON remains useful, but metrics need first-class fields. |
| F-10 | MEDIUM | F, G, B | `01_ARCHITECTURE` sec. 8-9 | The confirm-nonce design is ambiguous. A single `app_state_nonce` does not say whether a PUT config, ARM, DISARM, and KILL are protected by action-specific intent, body hash, TTL, or state version. It can also make emergency operations brittle if the UI state is stale. | Use action-scoped confirmation tokens containing action, state version, body hash, and short TTL. Keep emergency KILL available with a separate two-step flow that revalidates server state immediately before execution. |
| F-11 | MEDIUM | I | `02_BUILD_PLAN` tasks 1-11 | The one-day plan is under-estimated. The task estimates total roughly a long day before integration friction, but Task 8 alone includes IBKR delayed data, bars, brackets, reconnect, live refusal, and a smoke tool. Task 10 asks for a six-page polished WS dashboard in 150 minutes. | Split into Day 1 mock-core plus API, Day 2 IBKR adapter/recovery, Day 3 dashboard polish/P0. If still forcing one day, downgrade acceptance to mock-core complete and IBKR adapter skeleton with unit tests only. |
| F-12 | MEDIUM | H, A, E | `00_PREREG` sec. 4-6 | P0-P3 are directionally good but some decision rules are not well-defined. "Zero unexplained order states" has no taxonomy; slippage uses bar close as expected price while MKT-next-open execution includes overnight/session gap; signal parity lacks denominator, timezone alignment, and treatment of missing bars. | Add a metrics glossary: unexplained-state categories, expected-price definition per order type, signal-parity denominator, timestamp normalization, missing-bar policy, and confidence intervals for small sample sizes. |
| F-13 | LOW | F | `01_ARCHITECTURE` sec. 9; `02_BUILD_PLAN` task 10 | Dashboard build spec is broad enough that builders can guess differently: six pages, charts, modals, WS, journal drawer, dark theme, and screenshots are all required, but no minimum v1 screen contract is separated from polish. | Define a minimum dashboard acceptance slice: Overview, Strategy/Risk, Trading, Journal with required fields and empty states. Move LLM/System page polish and screenshots to v1.1 if time runs out. |
| F-14 | LOW | D, E | `01_ARCHITECTURE` sec. 6.4, 7 | LLM logging says prompt hash, latency, verdict, tokens, but schema has no LLM call table and `directives.raw_response` risks storing unredacted external text. | Add `llm_calls` table with prompt hash, model, latency, status, token counts, redacted response, and a secret/source redaction rule. |

## 3. Dimension notes

### A. Broker/API correctness

Findings: F-02, F-03, F-04, F-12. The docs know the right IBKR topics, but the implementation contract is not exact enough for bar-close finality, durable order identity, partial fills, or expected-price/slippage accounting.

### B. State machine & concurrency

Findings: F-02, F-03, F-04, F-08, F-10. The DISARMED/ARMED/KILLED model is simple and good, but the per-trade lifecycle needs explicit states for reconnect replay, config changes while armed, partial fills, and emergency actions under stale UI state.

### C. Risk engine math & completeness

Findings: F-04, F-06, F-07. The main sizing formula is reasonable for AAPL 1h, but boundary cases around stop distance, daily PnL accounting, and partial-fill protection are not yet tight enough.

### D. LLM gate

Findings: F-08, F-14. The narrowing-only hard boundary is the right constraint. The remaining risk is not LLM order authority; it is latency, fail-open semantics, source poisoning, and insufficient call telemetry.

### E. Data & persistence

Findings: F-02, F-03, F-06, F-09, F-12, F-14. The JSON audit trail is useful, but PREREG metrics and recovery need normalized fields and durable broker identities.

### F. Dashboard & API

Findings: F-10, F-13. The dashboard pages are plausible, but the API confirmation model and minimum dashboard slice need more precision so the builder does not invent critical behavior.

### G. Security

Findings: F-05, F-10. Localhost-only v1 is acceptable. Any live mode or tunnel path needs real auth and stricter separation between read-only monitoring and trading operations.

### H. PREREG soundness

Findings: F-01, F-09, F-12. The gates are directionally strong, but parity and slippage are not currently measurable enough to be binding without more definitions.

### I. Build plan feasibility

Findings: F-01, F-08, F-11, F-13. The plan is buildable as a mock-first demo in one day, but not as a robust IBKR unattended paper bridge with all dashboard and recovery promises.

## 4. Improvements

| ID | What | Why | Cost | Doc/section amended | Fits v1? |
|---|---|---|---|---|---|
| I-01 | Add a formal `BarFinalizer` spec and fixtures for RTH, half-days, DST, delayed data, and reconnect replay. | Prevent duplicate/missed hourly signals, which is the most likely real broker correctness failure. | M | `01_ARCHITECTURE` sec. 6.1/6.6; `02_BUILD_PLAN` task 8 | Yes, before Task 8 |
| I-02 | Extend order schema and reconciler contract with `permId`, parent/child IDs, OCA group, client ID, transmit role, and contract JSON. | Makes restart recovery and order adoption auditable instead of heuristic. | M | `01_ARCHITECTURE` sec. 6.5/7 | Yes |
| I-03 | Write a PREREG metrics glossary covering signal parity, slippage, unexplained order states, timestamps, missing bars, and day-boundary policy. | Turns P0-P3 from good intentions into measurable pass/fail gates. | S | `00_PREREG` sec. 5-6 | Yes |
| I-04 | Add a partial-fill protection state machine and tests before paper P0. | Prevents unprotected partial positions and wrong child quantities. | M | `01_ARCHITECTURE` sec. 5/6.5; `02_BUILD_PLAN` task 6/8 | Yes |
| I-05 | Split build acceptance into "Day 1 mock-core" and "IBKR hardening follow-up." | Keeps the one-day builder from rushing the highest-risk adapter work. | S | `02_BUILD_PLAN` header and task gates | Yes |
| I-06 | Disable live mode completely in v1 runtime unless a separate CLI flag is provided. | Reduces accidental live-port paths while keeping future live design possible. | S | `README` principle 3; `01_ARCHITECTURE` sec. 10/11 | Yes |
| I-07 | Add normalized `signals`, `fills`, `risk_days`, and `llm_calls` tables while keeping JSON payloads. | Lets PREREG reports be computed with SQL and reduces fragile JSON parsing. | M | `01_ARCHITECTURE` sec. 7 | v1.1 if time constrained |
| I-08 | Move hot-path pre-trade LLM veto to advisory/off-by-default for v1; keep cached regime only. | Avoids latency and fail-open confusion while preserving the human decision that LLM can only narrow risk. | S | `01_ARCHITECTURE` sec. 6.4; `02_BUILD_PLAN` task 9 | Yes |

## 5. Feature ideas

| ID | Feature | User value for a solo systematic trader | Cost | Suggested phase | Risk introduced |
|---|---|---|---|---|---|
| FI-01 | Shadow-live mode on real IBKR bars: compute signals/risk and log would-orders, but never submit. | Lets Baris validate bar timing, parity, LLM directives, and dashboard flow against real market data before any paper orders. | M | v1.1 | Users may confuse shadow metrics with executable paper results unless banners are strict. |
| FI-02 | Replay/debug cockpit: load a run, broker events, and DB rows into a step-through timeline. | Makes post-incident review fast: "what did the bridge know, when, and why did it act?" | M | v1.1 | Extra UI complexity; must remain read-only. |
| FI-03 | Session readiness checklist before ARM: TWS connected, data type known, clock sync, no stale bars, no unknown broker orders, strategy permissions valid. | Prevents accidental ARM into a bad environment. | S | v1.1 | Too many warnings can create alert fatigue if not ranked. |
| FI-04 | Post-session audit pack export: one zip or folder with config snapshot, trades, decisions, fills, events, equity, and metric summary. | Makes it easy to hand a paper session to Claude/Codex/MCC for review without scraping the DB manually. | S | v1.1 | Must redact secrets and raw LLM responses. |
| FI-05 | Corporate-action and symbol-status guard for AAPL: split/dividend/calendar status warnings before ARM. | Avoids confusing signal parity and price levels around splits, dividends, halts, or special sessions. | M | v2 | Needs a reliable data source; false positives may block harmless sessions. |
| FI-06 | First-N-signal manual approval mode: the engine prepares an order plan and waits for human approve/reject before submission, then can graduate to auto. | Useful transition between dry-run and unattended paper without giving the LLM or dashboard a manual strategy role. | M | v1.1 | Human delay changes fills; reports must label these trades as manual-approved. |
| FI-07 | Broker chaos drill runner for paper/dry-run: forced disconnect, duplicate bar replay, child-order reject, delayed fill, and DB restart drill. | Creates confidence that P2 unattended operation survives boring real failures. | M | v1.1 | Must never run against live; drills need clear mode guards. |

## 6. Top-3 verdict

1. **Fix IBKR bar/order identity before Task 8.** If this were my money, even paper money on the path to live, I would first harden bar finalization, durable order IDs, and reconnect reconciliation. A wrong bar close or unadoptable bracket is the class of bug that makes every other dashboard and PREREG metric untrustworthy.

2. **Make PREREG metrics computable before build day.** The current gates are good but not binding enough. Signal parity must resolve the close-confirmed-vs-original-strategy semantic change, and slippage must separate signal-to-entry gap from broker execution quality. Without that, P3 can become a debate instead of a gate.

3. **Cut the v1 build to mock-core plus explicit IBKR hardening.** One day is enough for scaffold, store, strategy port, risk engine, mock broker, API, and a minimal dashboard. It is not enough for robust IBKR delayed bars, bracket recovery, partial-fill safety, and a polished six-page WS dashboard. I would protect the schedule by narrowing v1 acceptance rather than letting the builder rush the broker adapter.
