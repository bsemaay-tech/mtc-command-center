# Audit — IBKR Paper Bridge design
Model: GitHub Copilot (MAI-Code-1-Flash) | Date: 2026-07-05 | Docs commit: ccf960cc

## 1. Summary verdict
Ship-with-fixes for a mock-first v1, but not for unattended paper operation until the broker contract is tightened. The overall direction is sound: paper-only, one-symbol, deterministic rules, and LLM narrowing-only are all good constraints. The architecture is still vulnerable to IBKR bar-finalization errors, durable order identity gaps, partial-fill ambiguity, and PREREG metrics that are not yet measurable enough to be binding. I would allow scaffold/mock work to proceed, but I would block any paper-order build milestone until the adapter recovery and metrics contracts are made explicit.

## 2. Findings

| ID | Severity | Dimension A-I | Location doc§ | Issue | Suggested fix |
|---|---|---|---|---|---|
| F-01 | HIGH | A, B, E | 01_ARCHITECTURE §5-6.1 | The design relies on `keepUpToDate=True` and “new bar object means previous bar is final,” but it never defines the exact bar-finalization contract for IBKR. In practice this is a classic source of duplicate/missed bars during reconnects, partial updates, and delayed market-data replay. | Add a formal `BarFinalizer` contract with bar key, session timezone, RTH rules, duplicate suppression, and reconnect replay rules; test half-days, holidays, delayed-data fallback, and reconnect replay with fixtures. |
| F-02 | HIGH | A, B, E | 01_ARCHITECTURE §5, §6.5, §7 | Order recovery is under-specified because the schema stores only local order IDs, while IBKR recovery depends on durable broker identities such as `permId`, parent/child relationships, OCA group, and transmit role. A restart can easily create an “unknown state” that the reconciler cannot safely adopt. | Persist broker-side identity fields and contract metadata in the orders table, then reconcile by `permId` first and only fall back to heuristics when necessary. |
| F-03 | HIGH | A, B, C | 01_ARCHITECTURE §5, §6.5 | Partial-fill handling is not robust enough for unattended paper trading. The plan says “cancel remainder, keep SL sized to filled qty,” but it does not define what happens if child orders fail, are resized out of order, or arrive after a parent is already partially filled. | Introduce explicit partial-fill states and a protected/unprotected transition model; test parent partial fill, child reject, resize failures, and out-of-order callbacks before any paper P0. |
| F-04 | HIGH | C | 01_ARCHITECTURE §6.3 | The risk engine covers the main sizing formula, but it does not define hard guards for stop-distance pathologies such as zero/tiny stop, gap-through-stop, stop on the wrong side of the price, and non-USD equity/currency handling. These are exactly the kind of edge cases that can produce nonsense quantities or mis-sized entries. | Add hard reject paths for min stop distance, gap-through-stop, invalid stop side, and currency/asset constraints, and make the arithmetic trace explicit in the decision payload. |
| F-05 | HIGH | G | README principle 3; 01_ARCHITECTURE §8, §10-13 | The live-port double-lock is weak. `IBKR_LIVE_ACK` plus a stale-tab confirm nonce is not meaningful authentication or authorization, and future tunnel/VPS exposure would make the bridge reachable from outside localhost without a real security model. | For v1, either remove live mode from the default runtime or require a separate CLI flag plus environment and strategy permission gates; add auth and remote-operation policy before any tunnel or VPS use. |
| F-06 | MEDIUM | C, E | 00_PREREG §5-7; 01_ARCHITECTURE §6.3, §7 | Daily-loss accounting is not yet measurable enough. The design does not define the timezone of the trading day, whether the metric is bridge-only or whole-account, how day-start equity is stored persistently, or how to reset after a broker restart. | Add `risk_days` data and a declared day-boundary policy keyed by exchange date and account snapshot; define whether unrealized and realized PnL are both included. |
| F-07 | MEDIUM | D, B, I | 01_ARCHITECTURE §3, §6.4; 02_BUILD_PLAN task 9 | The LLM path is too hot-path and latency-sensitive for v1. A 10-second veto in the synchronous order path can delay or block an otherwise valid entry, and the current prompt surface is vulnerable to news/X source poisoning even if the output is narrow. | Keep regime as a cached background signal and make pre-trade veto advisory/off-by-default for v1; add source allowlists, redaction, and explicit timeout behavior that never delays the order past a bounded threshold. |
| F-08 | MEDIUM | E, H | 00_PREREG §5; 01_ARCHITECTURE §7 | The schema cannot compute every PREREG metric cleanly without parsing arbitrary JSON. It lacks first-class fields for expected price, submit/fill latency, fill records, and directive linkage, which makes parity/slippage reporting fragile. | Add normalized `signals`, `fills`, `risk_days`, and `llm_calls` tables or columns, while retaining JSON payloads for auditability. |
| F-09 | MEDIUM | F, G, B | 01_ARCHITECTURE §8-9 | The confirmation model is under-specified. A single `app_state_nonce` does not explain whether ARM/DISARM/KILL are action-scoped, body-hash guarded, or refreshed by state version; that will cause builders to invent inconsistent behavior and makes emergency actions brittle. | Use action-scoped confirmation tokens with action, state version, body hash, and short TTL; keep KILL on a separate two-step flow that revalidates server state immediately before execution. |
| F-10 | MEDIUM | I | 02_BUILD_PLAN tasks 1-11 | The build plan is optimistic for the stated scope. Task 8 combines delayed-data handling, bar-finalization, bracket orders, reconnect recovery, and live-port refusal in one 90-minute slice, and Task 10 asks for a six-page dashboard with WS and charts in 150 minutes. | Split the work into a clear mock-core slice plus a second pass for IBKR hardening and dashboard polish, or lower the acceptance bar for the one-day build. |
| F-11 | MEDIUM | H, A, E | 00_PREREG §4-6 | The gates are directionally strong but not yet sharp enough to be binding. “Zero unexplained order states,” “signal parity,” and “slippage” lack a glossary, denominator, timestamp normalization rules, and treatment of missing/late bars. | Add a metrics glossary defining expected-price semantics, parity denominators, event taxonomy, timestamp normalization, and missing-bar policy before the first paper gate. |
| F-12 | LOW | F | 01_ARCHITECTURE §9; 02_BUILD_PLAN task 10 | The dashboard spec is broad enough that a builder could over-interpret the polish requirements and under-deliver the core monitoring flow. The minimum usable slice is not explicit. | Define a minimum dashboard contract for Overview, Strategy/Risk, Trading, and Journal with required fields, empty states, and error handling; move extra polish to v1.1. |

## 3. Dimension notes

A. Broker/API correctness — Findings: F-01, F-02, F-03, F-11. The docs mention the right IBKR topics, but the adapter contract is not exact enough to prevent real-world failures around bar finality, reconnect recovery, and partial fills.

B. State machine & concurrency — Findings: F-01, F-02, F-03, F-07, F-09. The app-level DISARMED/ARMED/KILLED model is simple and good, but the per-trade lifecycle needs explicit states for reconnect replay, config changes while armed, partial fills, and emergency actions under stale UI state.

C. Risk engine math & completeness — Findings: F-03, F-04, F-06. The sizing formula is reasonable, but stop-distance edge cases and daily-loss accounting are not yet tight enough for unattended paper trading.

D. LLM gate — Findings: F-07. The narrowing-only boundary is the right idea; the weakness is latency, fail-open semantics, source poisoning, and insufficient telemetry on the hot path.

E. Data & persistence — Findings: F-01, F-02, F-06, F-08, F-11. The JSON audit trail is useful, but PREREG metrics and recovery need more normalized data and durable broker identifiers.

F. Dashboard & API — Findings: F-09, F-12. The dashboard pages are plausible, but the API confirmation behavior and minimum usable UI contract need more precision so the builder does not invent critical behavior.

G. Security — Findings: F-05, F-09. Localhost-only v1 is acceptable, but any live or remote path needs a real security model before exposure beyond a single machine.

H. PREREG soundness — Findings: F-08, F-11. The gates are directionally strong, but signal parity, slippage, and unexplained states need sharper definitions to be defensible.

I. Build plan feasibility — Findings: F-01, F-07, F-10, F-12. The plan is credible as mock-first scaffolding, but not as a robust unattended paper bridge without a tighter adapter and a narrower acceptance bar.

## 4. Improvements

| ID | What | Why | Cost | Doc/section amended | Fits v1? |
|---|---|---|---|---|---|
| I-01 | Add a formal `BarFinalizer` contract and fixtures for delayed bars, half-days, reconnect replay, and duplicate suppression. | Prevents the most likely broker correctness failure: missed or duplicated hourly bars. | M | 01_ARCHITECTURE §5-6.1, 02_BUILD_PLAN task 8 | Yes |
| I-02 | Extend the order schema and reconciler contract with `permId`, parent/child IDs, OCA group, client ID, transmit role, and contract JSON. | Makes restart recovery and repair operations reliable instead of heuristic. | M | 01_ARCHITECTURE §6.5, §7 | Yes |
| I-03 | Add a PREREG metrics glossary defining signal parity, slippage, unexplained order states, timestamp normalization, and missing-bar policy. | Turns the gates from good intentions into verifiable pass/fail criteria. | S | 00_PREREG §5-6 | Yes |
| I-04 | Introduce explicit partial-fill protection states and tests before paper P0. | Prevents unprotected partial positions and out-of-order child-order chaos. | M | 01_ARCHITECTURE §5, §6.5, 02_BUILD_PLAN tasks 6-8 | Yes |
| I-05 | Split build acceptance into mock-core and IBKR hardening passes. | Keeps the one-day build realistic and avoids rushing the highest-risk adapter work. | S | 02_BUILD_PLAN header and task gates | Yes |
| I-06 | Make live mode require a separate explicit runtime path and strategy permission, not just env plus nonce. | Reduces accidental live-port exposure and makes the safety boundary clearer. | S | README principle 3; 01_ARCHITECTURE §8-13 | Yes |
| I-07 | Add normalized `signals`, `fills`, `risk_days`, and `llm_calls` tables while keeping JSON payloads. | Makes PREREG reporting and forensic review much easier than parsing JSON blobs. | M | 01_ARCHITECTURE §7 | v1.1 |
| I-08 | Move hot-path pre-trade LLM veto to advisory/off-by-default for v1 and keep regime as cached background state. | Avoids latency and fail-open confusion while preserving the human decision boundary. | S | 01_ARCHITECTURE §6.4; 02_BUILD_PLAN task 9 | Yes |

## 5. Feature ideas

| ID | Feature | User value for a solo systematic trader | Cost | Suggested phase | Risk introduced |
|---|---|---|---|---|---|
| FI-01 | Shadow-live mode on real IBKR bars that logs would-orders without submitting them. | Lets the user validate bar timing, parity, and dashboard flow before any paper orders are placed. | M | v1.1 | Users may confuse shadow metrics with real execution evidence unless the UI is explicit. |
| FI-02 | Replay/debug cockpit that walks a run through decisions, broker events, and fills in a timeline. | Makes post-incident review fast and reduces time spent reconstructing what happened. | M | v1.1 | Adds UI complexity and must stay read-only. |
| FI-03 | Session readiness checklist before ARM. | Prevents accidental ARM into a bad env: stale bars, unknown orders, missing data, or invalid strategy config. | S | v1.1 | Too many warnings can create alert fatigue unless they are ranked. |
| FI-04 | One-click audit export pack with config, decisions, fills, trades, equity, and events. | Makes it easy to hand a paper session to another reviewer without scraping the DB manually. | S | v1.1 | Must redact secrets and raw LLM responses. |
| FI-05 | Symbol-status and corporate-action guard rails for AAPL and other symbols. | Avoids confusion around splits, dividends, halts, and special sessions. | M | v2 | False positives may block harmless sessions if the data source is imperfect. |
| FI-06 | Manual approval gate for the first N signals before auto mode. | Gives the user a safer bridge from dry-run to unattended paper without granting the LLM trading authority. | M | v1.1 | Human approval delays fills and must be clearly labeled. |
| FI-07 | Chaos-drill runner for duplicate bars, disconnects, child-order rejects, and stale fills. | Builds confidence that the bridge survives the boring failures that matter most in unattended running. | M | v1.1 | Drills must be clearly isolated from real paper execution. |

## 6. Top-3 verdict
1. Fix broker bar-finalization and durable order identity before any paper-order milestone. The bridge will otherwise look “alive” while silently losing bar closes or misidentifying bracket children after reconnects, which makes every downstream metric and safety rule untrustworthy.
2. Make PREREG metrics computable and binding before build day. Signal parity and slippage need a defined contract now, otherwise P3 can become a debate about methodology instead of a pass/fail gate.
3. Narrow v1 scope to mock-core plus explicit IBKR hardening. One day is enough for the scaffold, strategy port, risk logic, mock broker, API, and a minimal dashboard; it is not enough for a polished six-page product plus robust bracket recovery and partial-fill safety.
