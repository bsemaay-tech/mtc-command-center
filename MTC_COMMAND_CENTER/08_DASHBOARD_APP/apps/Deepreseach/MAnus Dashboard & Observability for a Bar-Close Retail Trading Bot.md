# Dashboard & Observability for a Bar-Close Retail Trading Bot

**Research status:** research input only; it authorizes nothing. Any adopted feature remains subject to owner approval and the existing audit-tier flow. **Scope:** one owner, 1–5 Python workers, one instrument per worker, 5-minute to 1-hour bar-close decisions, 0–5 decisions per day per strategy, self-hosted Linux VPS, SQLite WAL, Hyperliquid perpetuals planned live venue, Interactive Brokers paper equities research, read-only dashboard plus ARM/DISARM/KILL/emergency-flatten brakes. **Research date:** 18 August 2026.

## Executive conclusion

The correct product is not a generic “trading dashboard.” It is a **small incident cockpit with a linked trade journal**. The home screen should answer, in one glance, whether the bot is allowed to act, whether the venue-side position and orders agree with local state, whether the market and private execution feeds are fresh, what the last decision was, whether risk guards are approaching or have crossed a limit, and what the operator should do next. Mature systems consistently expose status, trades, positions, logs, activity, charts, performance, notifications, and emergency controls, but they differ in emphasis: FreqUI and OctoBot are user-facing bot consoles; Jesse is chart- and activity-centric; Hummingbot exposes an operational API and orchestration layer; NautilusTrader is strongest as a live-engine reference for reconciliation and recovery rather than as a finished retail dashboard.[1](#ref-1)[4](#ref-4)[5](#ref-5)[6](#ref-6)[7](#ref-7)

The most important design decision is to separate **decision correctness** from **execution certainty**. A bar-close bot may correctly decide “no trade,” and it may also be intentionally inactive because it is DISARMED. Neither is a failure. Conversely, a process can be alive while its market feed, private order stream, or venue position view is stale. The dashboard therefore needs explicit states for `RUNNING`, `ARMED`, `DISARMED`, `STALE_DATA`, `RECONCILING`, `DRIFT`, `RISK_PAUSED`, and `KILL_LATCHED`; a single green process heartbeat is not enough. Google’s SRE guidance supports this symptom-first separation: monitor the user-visible failure, retain white-box telemetry for causes, and keep human-facing alerts simple and low-noise.[12](#ref-12)

A useful implementation rule is: **the local database is the audit and decision history; the venue is authoritative for current exposure, open orders, fills, margin, and liquidation state.** The system should reconcile them before trading after startup, continuously while exposed, at every decision boundary, and after any ambiguous order result. NautilusTrader explicitly aligns cached order and position state with venue reports before strategies start and continues checking in-flight orders, open orders, positions, and own order books.[7](#ref-7) Hyperliquid’s API provides the corresponding order, fill, position, and account information surfaces, while its dead-man endpoint and WebSocket heartbeat support independent safety supervision.[9](#ref-9)[10](#ref-10)[11](#ref-11)

## Evidence quality and interpretation

Official documentation is used wherever available. Maintainer statements, release notes, and issue threads are used to identify concrete failure modes, but an issue thread is evidence that a failure occurred in that implementation—not a statistical estimate of how often it occurs. The report labels such cases as **single-thread evidence**. No strong, independent comparative study was found that ranks Telegram, email, and push notifications by end-to-end reliability for a solo trading operator. The recommended design therefore treats each channel as best-effort, uses an external liveness check for page-worthy failures, and persists every alert in the dashboard and audit log.

Where a recommendation is a design synthesis rather than a documented feature, it is marked as such. Exact thresholds for liquidation-distance alerts, stale-data windows, risk budgets, and notification escalation must come from the venue contract, the existing risk framework, and owner approval; this report does not set trading parameters.

## 1. Feature inventory of comparable systems

### What mature systems actually ship

| System | Main screen or primary operating surface | One click away or exposed through the operating surface | Deliberately absent or not emphasized | Transferable lesson |
|---|---|---|---|---|
| **Freqtrade + FreqUI** | Bot status, trades, performance, wallet/balance history, charts, and configuration-oriented views. The UI can connect to multiple bots and exposes bot health and trading state.[1](#ref-1) | Start/stop, stop-entry, force exit or entry, cancel an open order, reload configuration, logs, status, balance, trade history, profit periods, and other REST-backed controls.[2](#ref-2) | The documentation does not present a governance model in which manual order entry is structurally forbidden; its API includes force-entry and force-exit actions. The UI is therefore a useful comparator but not a governance template for this system.[1](#ref-1)[2](#ref-2) | Status, trade, balance, log, and control primitives are mature. Retain the visibility; remove manual-entry and strategy-edit capabilities under the fixed governance constraint. |
| **Jesse** | Live/paper session status, candle chart, equity curve, activity, logs/errors, trades, orders, and session information. A trade chart can browse candles, executed orders, closed trades, and indicator values.[4](#ref-4) | Chart navigation, indicator panes, trade-linked chart inspection, session monitoring, and issue/log review. The changelog emphasizes reconnect handling, clearer send failures, rate-limit handling, and paper-order recovery.[4](#ref-4) | It is not primarily an incident-control cockpit; chart and session exploration are more prominent than a venue-versus-local reconciliation matrix. | Adopt chart-linked replay and visible errors, but put execution certainty and risk state above chart decoration. |
| **OctoBot** | Portfolio and automation monitoring, with separate interfaces for manual bots, backtesting, and reports. The project also emphasizes mobile/new-interface access.[5](#ref-5) | Telegram monitoring of robot, portfolio, and profits, plus an emergency-sell action; reports and backtesting are available in adjacent surfaces.[5](#ref-5) | The feature model is broader and more user-facing than the requested read-only-plus-brakes model. | Use an emergency channel and compact portfolio view, but keep the allowed actions limited to ARM/DISARM/KILL/flatten. |
| **Hummingbot** | Strategy-runner/API surfaces expose balances, portfolio distribution, order management, positions, bot orchestration, archived analytics, and host CPU/RAM/disk metrics. The API also supports WebSocket streaming and per-bot logs/data.[6](#ref-6) | Start/stop and orchestration, order and position monitoring, real-time notifications through Condor/mobile/Telegram integrations, and operational telemetry.[6](#ref-6) | The platform’s heritage includes market-making and broad execution control. Those capabilities should not be imported merely because the API exposes them. | Separate worker state, venue state, host state, and notifications; use a small read-only read model plus brakes rather than a general order console. |
| **NautilusTrader** | The official material is an engine and live-node reference more than a polished retail dashboard. It exposes lifecycle, reconciliation, cache restoration, runner metrics, and coordinated shutdown concepts.[7](#ref-7) | Startup recovery, execution reconciliation, command outcomes, continuous checks, data-event rate/staleness, queue depth, and controlled shutdown.[7](#ref-7) | It does not provide a turnkey solo-operator dashboard matching this brief. | Use its lifecycle and reconciliation semantics as the backend contract, then build a deliberately small operator UI over them. |
| **Gekko** | Historically provided web UI, live/paper trading, profit/risk metrics, graphing, backtesting, data import, and notification plugins.[8](#ref-8) | Historical web controls and notification plugins. | The official site states that Gekko is no longer maintained. It is not a valid current implementation reference or “successor” baseline.[8](#ref-8) | Treat it as historical context only. Do not inherit stale operational assumptions from an unmaintained project. |

Across these systems, the most transferable common denominator is a **status-to-history path**: current state on the primary screen, logs/orders/trades one click away, and charts linked to the actual execution record. The systems differ in how much control they expose, so the requested governance model must be treated as a design constraint rather than inferred from the comparator set. FreqUI’s documented force-entry/force-exit surface is particularly important: it proves that “mature” does not mean “appropriate for this owner-approved, no-manual-entry operating model.”[1](#ref-1)[2](#ref-2)

### Recommended first screen

The first screen should have six compact zones: **execution state**, **venue truth**, **data freshness**, **last decision**, **risk guards**, and **operator action**. A chart is useful, but it should be below these zones or available through a linked trade view. The most valuable large text is not “today’s P&L”; it is “ARMED — one open long — venue/local MATCHED — private stream fresh 3 s ago — next decision in 11 min — no action required.”

## 2. Reconciliation

### Pattern and authority

A local SQLite WAL database is excellent for durable decision history, audit events, strategy versions, and an append-only operational journal. It should not be treated as the sole authority for live exposure. Current venue-side position, open orders, fills, margin, and account health must be queried from the venue and compared with local expectations. This is not a rejection of the local database as the system’s source of truth for decisions; it is a separation between **what the bot believes it decided** and **what the venue confirms currently exists**.

NautilusTrader’s live-node documentation gives the clearest reference pattern: restore cached state, reconcile against venue reports before starting trader components, abort startup if connection or reconciliation fails, and continue checking in-flight orders, open orders, positions, and own order books during runtime.[7](#ref-7) Freqtrade’s FAQ provides a lower-level warning from a different architecture: when balances or trades are changed outside the bot, exchange-order refinding is best effort and can fail for unsupported order types or older exchange records.[3](#ref-3) The practical conclusion is that drift must be visible and state transitions must be auditable; recovery should not silently rewrite history.

### Recommended reconciliation state machine

| State | Meaning | Trading behavior | Operator surface |
|---|---|---|---|
| **MATCHED** | Venue position/orders and local expected state agree within venue rounding and fee rules. | Normal behavior, subject to other guards. | Green/neutral status with last reconciliation time and source timestamps. |
| **VENUE_AHEAD** | Venue shows a position, fill, or open order not represented locally. | Freeze new entries; allow only a pre-approved recovery path or flatten brake. | Red “venue ahead” banner with venue IDs, amount, age, and next action. |
| **LOCAL_AHEAD** | Local intent/order exists but venue cannot confirm it. | Freeze retries; query status/fills; do not assume rejection or absence. | Amber “unknown execution” state with command ID, retry count, and last query. |
| **RECONCILING** | A command or stream result is ambiguous and the venue query is in progress. | No new exposure; do not issue a duplicate order merely because an ACK is missing. | Prominent pending state with elapsed time and explicit “do not retry blindly.” |
| **FLAT_CONFIRMED** | Venue reports no position and no relevant open orders; local state is closed/settled. | Normal if ARMED and data is healthy. | Confirmed flat, with timestamp and account/margin snapshot. |
| **KILL_LATCHED** | A risk or operator kill is active and must be explicitly cleared through the approved flow. | No new entries; flatten action may remain available. | Persistent latch, trigger reason, actor, time, and clearance procedure. |

The minimum cadence should be **startup before strategy activation**, **at every bar decision boundary**, **after every submit/cancel/flatten command**, and **after any private-stream reconnect or ambiguous response**. While a position or resting protective order exists, a periodic background reconciliation should run independently of the strategy loop. A practical initial implementation is to refresh frequently enough to detect a lost private stream within one or two decision intervals, with the exact interval chosen from venue rate limits and risk tolerance. This cadence is a design recommendation, not an exchange-prescribed number.

### Failure modes that the UI must make explicit

Maintainer issue threads illustrate why “order submitted” and “order canceled” are not sufficient final states. Freqtrade documented a partial fill below the venue minimum tradable amount; simply closing the local trade would leave residual value at the exchange and make the accounting disappear from the bot’s perspective.[15](#ref-15) A Hummingbot issue documents a cancel/fill race in which an order filled while cancellation was in progress, cancellation returned “order not found,” and the executor did not open, causing an imbalance.[16](#ref-16) Other single-thread Hummingbot examples show account-position stream exceptions followed by repeated close attempts, and delayed or incomplete fill updates combined with zero-size retries.[17](#ref-17)[18](#ref-18)

The UI should therefore show **requested quantity, acknowledged quantity, filled quantity, remaining quantity, venue minimums, last fill timestamp, and order-state confidence**. A cancel response should be rendered as `CANCEL_REQUESTED` until a subsequent venue query confirms `CANCELED` with no intervening fill. A completed event with incomplete fill information should be rendered as `EXECUTION_DATA_INCOMPLETE`, not as a clean final fill. These are operational conclusions derived from the cited incidents; the issue threads are not prevalence studies.

## 3. Staleness and transport health

### Three clocks, not one heartbeat

A bar-close bot needs three independent freshness indicators. The **process clock** answers whether the worker loop is alive. The **market-data clock** answers when the last complete candle, mark/index price, and relevant feed update were received. The **private-execution clock** answers when the last order, fill, position, or account update was received and when the last successful REST reconciliation completed. A green process heartbeat alongside a stale private stream is unsafe; a fresh market feed with a dead worker is also unsafe.

For each instrument, show the last complete bar timestamp, expected next bar close, observed wall-clock delay, last WebSocket message, last successful ping/pong, last REST snapshot, and last private-stream event. At bar close, classify the decision as `NO_SIGNAL`, `BLOCKED_BY_GATE`, `SKIPPED_STALE_DATA`, `DECISION_MADE`, or `DECISION_PENDING`. This is the critical distinction between **market quiet** and **feed frozen**. Freqtrade’s FAQ makes the same distinction operationally: missing candles can arise from low volume or an exchange outage, and outdated history can indicate exchange downtime, system-time problems, low volume, or an API problem.[3](#ref-3)

Hyperliquid’s WebSocket documentation says the server closes a connection if it has not sent a message for 60 seconds and supports client ping/pong heartbeats.[10](#ref-10) This makes a client-side transport indicator mandatory, but it does not by itself prove that the subscribed account channel is delivering all order and position updates. Use ping/pong for transport health, event timestamps for data freshness, and REST reconciliation for state certainty.

### Recovery and dead-man design

The normal recovery path is: detect stale or disconnected stream; mark the feed as degraded; stop new entries; reconnect with bounded backoff; resubscribe; query REST state; compare orders, fills, position, and margin; then clear the degraded state only after the data stream and reconciliation agree. Freqtrade documents falling back from WebSocket to REST after an interruption; that is a useful availability pattern, but it should be surfaced to the operator rather than hidden.[3](#ref-3)

Use two independent dead-man mechanisms. First, the worker and systemd layer should have a process watchdog that restarts a failed process, but a restart alone must not re-arm trading. Second, the venue-side schedule-cancel facility should be renewed by a small control-plane lease while the bot is healthy. Hyperliquid documents a schedule-cancel endpoint for future cancel-all behavior.[9](#ref-9) The lease should be treated as a backstop for stale resting orders, not as a substitute for position reconciliation, a protective risk design, or an emergency flatten path. Exact lease duration and refresh interval should be derived from the venue API semantics and the operator’s risk budget.

The dashboard should expose the dead-man lease’s **last successful renewal, expiry time, renewal error, and whether it covers open orders only or the intended venue protection**. If the lease cannot be renewed, the status should move to `PROTECTION_DEGRADED` and the system should follow the existing API/data-feed failure guard.

## 4. Alerting for a solo operator

Google SRE’s alerting guidance is directly applicable even though the bot is small: paging is expensive, noisy pages cause people to second-guess or ignore alerts, and human-facing rules should be simple, robust, and tied to a clear failure.[12](#ref-12) The SRE workbook further recommends considering precision, recall, detection time, and reset time rather than creating a message for every unusual metric.[13](#ref-13) Prometheus Alertmanager provides concrete mechanisms—grouping, inhibition, routing, repeat intervals, silences, and multiple receivers—that can be copied into a small custom alert state machine without adopting the entire stack.[14](#ref-14)

### Alert taxonomy

| Priority | Page immediately | Digest or scheduled summary | Log-only |
|---|---|---|---|
| **Exposure and reconciliation** | Nonzero venue exposure while the worker is DISARMED/KILL_LATCHED; venue/local drift; unknown order outcome after a command; unconfirmed flatten; missing protective state when required. | Repeated transient drift that self-resolves and leaves no exposure, with a clear resolution event. | Normal matched reconciliation and zero-position snapshots. |
| **Data and transport** | Stale market data at a required decision boundary while ARMED; private execution stream stale while exposed; process dead while exposure or a required order exists; failed dead-man renewal when coverage is needed. | WebSocket reconnect that completes, REST fallback, rate-limit backoff, or isolated public-feed gap with no exposure impact. | A normal ping/pong, a single retry that succeeds, and ordinary bar-close heartbeat. |
| **Risk guards** | Daily/weekly loss or max-drawdown kill trigger; exposure-cap breach; liquidation-health threshold crossing; consecutive-loss pause if governance requires immediate acknowledgement. | Pre-trigger warning with headroom and trend; funding/cost accumulation; slippage outlier that does not breach a hard guard. | Routine headroom updates and normal risk-budget consumption. |
| **Execution** | Order or fill state is ambiguous beyond the approved reconciliation window; repeated order attempts or retry storm; a reduce-only/flatten action cannot be confirmed. | Order pending longer than the strategy’s expected execution window but with confirmed bounded exposure; venue rate limit or maintenance notice. | Normal ACK, fill, fee, funding, and clean close events. |

“Bot went silent” requires a separate monitor because the bot cannot reliably page the owner about its own death. Use an external check against the VPS or a second process that expects a signed heartbeat containing worker state, last complete bar, last reconciliation, and current exposure. A heartbeat receipt should be periodic; the external monitor should page only when the silence duration is materially longer than the cadence expected for the current instrument and exposure state.

### Rate limiting and deduplication

Group alerts by an incident key such as `(worker, instrument, failure class, venue)`, not by every exception line. Send one firing notification, then bounded updates when the state changes or a repeat interval expires, and one resolved notification. Inhibit child alerts when a parent condition explains them: for example, suppress “no fills” and “no new decisions” while the entire venue connection is down, but retain the high-priority “private stream stale while exposed” alert. This mirrors Alertmanager’s grouping and inhibition model.[14](#ref-14)

Each alert record should contain a stable fingerprint, first-seen time, last-seen time, severity, state transition, affected exposure, notification attempts, delivery response, and resolution time. Notification delivery is not the same as operator acknowledgement. I found no reliable cross-channel study establishing that Telegram, email, or push is universally dependable for this use case. Therefore, for page-worthy exposure or reconciliation incidents, use two independent transports where practical and retain the dashboard/audit log as the source of alert history.

A useful page template is: **what is wrong; current exposure; what is protected; last confirmed venue state; last local state; how old the data is; what automatic brakes already fired; and the single safe next action.** Do not send raw stack traces as the primary message; link them from the incident record.

## 5. Incident-response UX

The first screen should answer seven questions in under 60 seconds: **Is the bot allowed to act? What is the venue-side exposure? Are there open orders? Do local and venue states match? Are data and private streams fresh? What was the last decision and why? What is the next safe action?** This is a direct translation of the failure patterns above, not a generic dashboard preference.

| First-60-second question | Required display | Safe operator action |
|---|---|---|
| Is it acting? | Per-worker state: process, ARMED/DISARMED, strategy version/hash, current gate, last loop time. | DISARM or KILL if authorization is uncertain; never re-arm after a restart automatically. |
| What exists at the venue? | Position side/size/notional, open orders, last fill, margin health, mark/oracle price, and venue timestamps. | Treat venue state as live exposure until reconciled. |
| Is local state trustworthy? | Local expected position/orders beside venue state, drift classification, reconciliation age. | Freeze new entries for any non-MATCHED state. |
| Is the data fresh? | Last complete candle, expected close, feed age, private-stream age, REST snapshot age, reconnect count. | Distinguish “no signal” from “stale data”; allow the existing feed-failure guard to hold the bot DISARMED. |
| What did it decide? | Decision ID, bar ID, strategy/parameter hash, gate results, indicator snapshot, risk budget before/after, order intent. | Open the linked chart/replay rather than searching raw logs. |
| What happened to the order? | Client command, venue order ID, ACK, fills, partial quantity, cancel state, retry count, fees. | Query and reconcile ambiguous outcomes; do not blindly duplicate. |
| What should I do now? | One recommended action: “no action,” “keep disarmed,” “reconcile,” “confirm flatten,” or “inspect risk guard.” | Use only the four approved brakes and require confirmation for destructive actions. |

For an ambiguous order, the incident screen should lock new entries, show an elapsed timer, and present a **reconcile** action—not a “retry order” button. For emergency flatten, show a preflight summary of side, size, margin, open orders, and intended reduce-only semantics; after confirmation, keep the incident active until the venue confirms flat. The screen must distinguish “flatten command submitted” from “flat confirmed.”

## 6. Trade journal and post-trade review

At this cadence, storing every tick or full order-book snapshot is unnecessary for the execution dashboard. The valuable unit is the **decision chain**: one immutable record per bar evaluation, plus a linked order/fill event stream when an order is attempted. The journal should preserve enough information to answer “why did the bot do that?” even after the strategy code or data vendor changes.

| Journal layer | Minimum fields | Why it matters |
|---|---|---|
| Bar input | Instrument, timeframe, bar open/close, exchange timestamp, local receipt time, OHLCV, data source, completeness flag. | Separates a genuine signal from a stale, partial, or wrong-timeframe candle. |
| Strategy identity | Strategy name, frozen parameter-set ID, code commit/hash, Pine/Python parity version, deployment ID. | Makes the decision reproducible and prevents code drift from rewriting history. |
| Gate and indicator snapshot | Each entry/exit gate as true/false/unknown, indicator values used, regime filters, cooldown state, exposure state. | Shows exactly which condition blocked or created a decision. |
| Risk snapshot | Risk budget before and after, proposed quantity, exposure cap headroom, loss-budget headroom, kill/guard states. | Explains why a valid signal was not traded or was sized down. |
| Intent and command | Decision ID, action, side, quantity, order type, reduce-only/protective flag, idempotency/client ID, submission time, local result. | Connects a strategy decision to an execution request without implying execution certainty. |
| Venue events | Venue order ID, status transitions, fill IDs, fill quantity/price, fees, funding, timestamps, cancel/replace outcomes, error codes. | Provides venue-grounded execution truth and supports reconciliation. |
| Post-trade context | Exit reason, realized P&L, slippage versus reference, MAE/MFE, holding time, funding paid/received, reconciliation result. | Supports post-trade review and comparison with backtest assumptions. |

The review UI should be a three-pane **Why / What / Result** view. “Why” shows the bar chart and gates; “What” shows the order and venue timeline; “Result” shows fills, costs, risk-budget movement, and final reconciliation. The chart should place entry, exit, protective actions, and relevant indicator levels on the exact bar used by the decision. A strategy hash and a compact JSON snapshot of inputs are worth storing even if the full data can be reconstructed, because reconstruction can change when upstream candle corrections or code versions change.

## 7. Minimal performance analytics

For 0–5 trades per day, live analytics should emphasize **descriptive operational facts** over inferential claims. The top screen should show net realized P&L, unrealized P&L, equity curve, current and peak-to-trough drawdown, exposure time, trade count, fees, funding, and slippage. It should always show the sample size and date window. Win rate, expectancy, profit factor, and rolling averages can be useful in the research view, but at small N they should be visibly labeled as unstable estimates rather than as evidence that the strategy has a reliable edge.

The minimal live set is:

| Metric | Live use | Presentation rule |
|---|---|---|
| Net equity and realized/unrealized P&L | Capital and current exposure monitoring. | Separate realized, unrealized, fees, and funding; show absolute and percentage values. |
| Drawdown | Risk-guard operation. | Show current drawdown, high-water mark, max observed drawdown, and distance to the configured kill threshold. |
| Slippage | Detect execution degradation versus the strategy’s backtest assumption. | Compare effective fill price with the decision reference and show distribution by side and market condition; do not hide fees or funding inside slippage. |
| Trade count and holding time | Context for interpreting other metrics. | Put N beside every rate or ratio. |
| Expectancy/profit factor | Review and research. | Use descriptive labels and uncertainty context; do not place a single small-N value in a “health score.” |
| Exposure and turnover | Risk and cost context. | Show time-in-market, notional, leverage, and turnover separately. |
| Funding and fees | Perpetual-specific cost attribution. | Show cash amount, rate, side, notional basis, and period. |

Slippage should be computed at the fill level and aggregated per trade and per day. The backtest comparison should use the same reference convention in both environments: for example, decision-time mid/mark or the strategy’s documented execution proxy. It should not compare a live fill against a later bar close. A slippage outlier should first be an investigation signal, not an automatic strategy-retuning instruction.

Hyperliquid’s funding documentation is especially relevant to attribution: funding is paid hourly, the formula uses the spot oracle to convert position size to notional, and the rate is peer-to-peer.[21](#ref-21) Funding therefore belongs in a separate cost line and in the decision-chain context. Research analytics should handle out-of-sample performance, expectancy distributions, and statistical uncertainty; the execution dashboard should remain an operational surface.

## 8. Risk-guard visualization

The risk framework already exists, so the dashboard should make its state **legible, historical, and hard to misread**. Use a guard matrix with one row per guard: per-trade risk, daily loss, weekly loss, maximum drawdown, consecutive losses, API/data protection, and exposure cap. Each row should show current value, configured limit, headroom, state, trigger time, and automatic action.

| Guard state | Meaning | UI treatment |
|---|---|---|
| **ARMED / CLEAR** | Guard is active and current value is below the warning boundary. | Neutral/green state with headroom and last evaluation time. |
| **PRE-TRIGGER** | Warning boundary is crossed, but the hard limit is not. | Amber state with trend, remaining headroom, and expected action if the trend persists. |
| **TRIGGERED** | Hard limit crossed; the configured pause/kill/flatten behavior has fired. | Red, persistent state with exact trigger value, timestamp, source event, and current exposure. |
| **DISARMED** | Guard is not active because the system or owner intentionally disabled it. | Prominent reason and audit record; never style it as healthy. |
| **KILL_LATCHED** | Trading is blocked until an explicit approved clearance. | Persistent banner; show who/what latched it and the clearance requirements. |
| **UNKNOWN** | Required input is stale or unavailable. | Treat conservatively; no new entries until the input is restored or an approved fallback is applied. |

Every state change should append an audit event containing actor (`system`, `owner`, or `deployment`), timestamp, prior state, new state, reason code, measured value, configured threshold ID, and related decision/order IDs. The ARM/DISARM/KILL/flatten controls should be separate from informational controls, use POST/PUT rather than GET, require explicit confirmation for destructive actions, and use step-up authentication where the dashboard is remotely exposed. No parameter editing or manual order entry belongs in this surface.

## 9. Security baseline

Loopback-only service access through an SSH tunnel is already a strong default for a solo operator. If remote exposure is ever needed, prefer a private overlay/VPN or access proxy over direct internet exposure. Freqtrade’s REST documentation recommends localhost access, strong credentials, a random JWT secret, and SSH tunneling or VPN rather than exposing the API directly; Hummingbot similarly recommends a private network such as Tailscale and keeping authentication enabled.[2](#ref-2)[6](#ref-6)

The minimum hardening beyond loopback is a host firewall, a dedicated unprivileged service account, strict file permissions on SQLite and secrets, encrypted backups, dependency and OS patching, and API keys restricted to the required venue actions with withdrawals disabled where the venue supports that separation. Use a dedicated venue subaccount or otherwise prevent manual activity from sharing the bot’s position namespace; Freqtrade’s maintainer discussion explicitly warns that manual activity can be incorporated into recovery/refinding behavior and recommends leaving bot positions alone or using a subaccount.[3](#ref-3)[20](#ref-20)

For the web layer, use a modern framework’s session handling; secure, HttpOnly, SameSite cookies where cookie sessions are used; idle and absolute session expiry; session rotation after authentication; rate limiting; and no secrets in URLs or logs. OWASP emphasizes that a session token is effectively equivalent to the strongest authentication method used and must be unpredictable, meaningless, and protected.[24](#ref-24) Because ARM/DISARM/KILL/flatten are state-changing operations, use POST/PUT, CSRF protection or a non-cookie authentication model with equivalent origin defenses, explicit user interaction for sensitive actions, and origin validation. OWASP specifically advises against using GET for state-changing actions and recommends CSRF tokens or equivalent defenses.[25](#ref-25)

A proportionate authentication design is: login plus TOTP or a hardware security key for remote access; a short-lived session; step-up authentication for KILL and flatten; a read-only default; and a separate audit trail for every control request and result. If a control request arrives twice, the backend should use an idempotency key and return the existing command state rather than submitting a duplicate.

I did not find a verified primary incident in this research pass that specifically documents an exposed FreqUI or Grafana instance causing a retail trading loss. That absence should not be interpreted as safety evidence. The official project guidance to keep interfaces private, combined with OWASP’s session and CSRF guidance, is sufficient to treat direct public exposure as an avoidable risk rather than as an acceptable default.[2](#ref-2)[6](#ref-6)[24](#ref-24)[25](#ref-25)

## 10. Perpetual-futures surfaces

A perpetual-futures dashboard should present **risk in the units that can cause a forced event**, not merely leverage. Hyperliquid documents hourly funding, mark-price-based liquidation, cross or isolated margin, maintenance margin, and the possibility that the displayed liquidation price can change with funding, other cross positions, and changing liquidity.[21](#ref-21)[22](#ref-22)[23](#ref-23)

| Surface | Required fields | Commonly misleading presentation |
|---|---|---|
| Position | Side, size, notional, entry price, mark price, unrealized P&L, realized P&L, leverage, margin mode. | Showing leverage as the primary risk score; leverage is a setting, not the remaining liquidation cushion. |
| Price reference | Last/book price, mark price, oracle/index price, and timestamps. | Using last trade price to imply liquidation risk when the venue uses mark price. |
| Margin health | Account equity, margin used, available margin, maintenance margin requirement, margin mode, and cross-account dependencies. | A single margin percentage without saying whether it is cross or isolated or what is included. |
| Liquidation | Estimated liquidation price, mark-price distance in dollars and percentage, maintenance tier, and calculation timestamp. | Treating a displayed liquidation price as exact or static. Hyperliquid explicitly says estimates can be inaccurate and can change.[22](#ref-22) |
| Funding | Current and next rate, side paying/receiving, next funding time, cumulative funding paid/received, and notional basis. | Showing a percentage without side, period, notional, or cash impact. |
| Basis/oracle | Mark-versus-oracle and perp-versus-oracle difference with time series. | Interpreting a transient basis as a strategy signal or risk event without context. |
| Stress context | Owner-approved scenarios such as mark-price move, funding accrual, and gap/slippage assumptions. | A false-precision “distance to liquidation” gauge that ignores liquidity and cross-margin interactions. |

The primary visual should be an **account-health card** with a mark-price-based liquidation cushion, not a speedometer. Use the exchange’s exact formula where possible, show calculation freshness, and display a caveat whenever the number is estimated. A pre-trigger alert should be tied to approved margin-health thresholds and current exposure, not to a generic leverage color scale. Funding should be attributed in cash terms and included in net P&L only through a clearly labeled component.

## 11. Anti-features

The following features are common in generic “trading dashboard” concepts but are a poor fit for this system. Some are not universally harmful; they are harmful here because their value depends on a different cadence, strategy type, governance model, or sample size.

| Anti-feature | Why it is harmful or low-value here | Replacement |
|---|---|---|
| Microsecond latency panels, co-location metrics, kernel/FPGA telemetry | Decision latency is seconds and the system is not HFT; the metrics create false urgency. | Bar-close decision delay, order acknowledgment time, feed freshness, and reconciliation age. |
| Tick heatmaps and deep order-book visualizations | Strategy decisions use completed bars, not depth or market making; large screens become noise. | Last complete bar, reference prices, spread only when relevant to execution, and bar-linked replay. |
| Manual order entry or arbitrary force-entry controls | Violates governance and creates an unjournaled path around the research/promotion pipeline. | ARM/DISARM/KILL/flatten brakes with confirmation and audit. |
| Parameter editing from the live UI | Can change strategy behavior without the owner-approved promotion path. | Display frozen parameter-set ID and deployment hash; change only through promotion/deployment. |
| Always-on AI sentiment or regime “scores” | Adds an ungoverned decision input and tends to produce non-actionable screen candy. | Show only deterministic gates and advisory analysis outside order flow. |
| Live Sharpe, profit factor, or expectancy as a single health badge | Small N makes the estimate unstable and encourages overinterpretation. | Show sample size, window, costs, drawdown, and descriptive distributions. |
| Push notification for every bar, heartbeat, or no-signal event | Creates alert fatigue and makes true failures easier to ignore. Google SRE explicitly warns that noisy pages are ignored.[12](#ref-12) | Digest routine events; page only on exposure, drift, stale protection, or guard triggers. |
| Raw log wall on the home screen | Text volume obscures the current state and the needed action. | Structured incident cards, with raw logs one click away. |
| Automatic re-optimization or self-modifying strategy | Conflicts with frozen, pre-approved parameters and makes post-trade explanation harder. | Research-only backtest/review workflow with explicit promotion. |
| Team/tenant/dashboards-for-everything permission model | Adds complexity without a multi-user requirement. | One owner, strong authentication, explicit audit identity, and least privilege. |
| Options Greeks and portfolio-margin optimization | Explicitly out of scope for the current venues and strategy. | Perpetual margin, mark price, liquidation cushion, funding, and exposure caps. |

These exclusions are partly supported by the project scope itself and partly by the cited SRE signal-to-noise principles. They should be understood as **cadence-fit decisions**, not claims that the features are never useful in other trading systems.

## Consolidated feature decision table

| Feature | Problem it solves | Evidence (source) | Fits bar-close solo-operator cadence? | Suggested surface |
|---|---|---|---|---|
| Per-worker process, ARMED/DISARMED/KILL state | Prevents uncertainty about whether a worker may act | FreqUI status/control surfaces; SRE dashboard principles [1](#ref-1)[12](#ref-12) | **Yes**; central operating state | Execution dashboard |
| Venue position and open-order panel | Shows actual exposure rather than local belief | Nautilus reconciliation; Hyperliquid info API [7](#ref-7)[11](#ref-11) | **Yes**; highest priority | Execution dashboard |
| Local-versus-venue reconciliation badge | Detects phantom, orphan, or ambiguous state | Nautilus live docs; Freqtrade FAQ [3](#ref-3)[7](#ref-7) | **Yes**; required | Execution dashboard + backend gate |
| Startup reconciliation before re-arm | Prevents restart with stale or duplicated state | Nautilus live lifecycle [7](#ref-7) | **Yes**; required | Backend gate |
| Reconciliation after every ambiguous command | Handles cancel/fill races and missing ACKs | Hummingbot issues [16](#ref-16)[18](#ref-18) | **Yes**; required | Backend gate + incident screen |
| Bar freshness and expected-close timer | Separates market quiet from feed frozen | Freqtrade FAQ; Hyperliquid heartbeat [3](#ref-3)[10](#ref-10) | **Yes**; required | Execution dashboard |
| Private-stream freshness | Detects stale order/position state while exposed | Hyperliquid heartbeat; Nautilus runner metrics [7](#ref-7)[10](#ref-10) | **Yes**; required | Execution dashboard + backend gate |
| REST fallback with degraded badge | Preserves availability during WebSocket interruption | Freqtrade FAQ [3](#ref-3) | **Yes, partial**; only with explicit degraded state | Backend gate + execution dashboard |
| Venue-side scheduled cancel/dead-man lease | Cancels stale resting orders if control plane dies | Hyperliquid exchange API [9](#ref-9) | **Yes**; backstop, not full risk control | Backend gate + execution dashboard |
| External bot-silent monitor | Detects process/host failure that cannot self-page | SRE black-box monitoring principles [12](#ref-12) | **Yes**; especially while exposed | Backend/independent monitor |
| Grouped, deduplicated alert state machine | Avoids notification fatigue and repeated stack traces | SRE alerting; Alertmanager [12](#ref-12)[13](#ref-13)[14](#ref-14) | **Yes**; essential for one owner | Backend + notifications |
| Two-channel page for exposure/drift | Avoids single notification transport failure | No strong comparative reliability study found; design synthesis | **Yes, partial**; use for highest severity only | Notifications + audit log |
| Incident card with one next action | Reduces time to triage while away from desk | Derived from cited failure threads [15](#ref-15)[16](#ref-16)[17](#ref-17) | **Yes**; required | Execution dashboard |
| Decision-chain journal | Answers why a signal was blocked or traded | FreqUI/Jesse chart and trade surfaces; design synthesis [1](#ref-1)[4](#ref-4) | **Yes**; high value at low trade count | Execution + research dashboard |
| Chart-linked trade replay | Connects candle, gates, order, fills, and result | Jesse trade chart [4](#ref-4) | **Yes**; high value | Research dashboard, linked from execution |
| Fill-level slippage and cost attribution | Detects divergence from backtest assumptions | Hummingbot/Freqtrade execution issues; Hyperliquid funding docs [15](#ref-15)[21](#ref-21) | **Yes**; useful even with few trades | Research dashboard + post-trade view |
| P&L, drawdown, exposure time, fees, funding | Gives operational performance without fake precision | FreqUI/Jesse/OctoBot performance surfaces [1](#ref-1)[4](#ref-4)[5](#ref-5) | **Yes**; required | Execution dashboard + research dashboard |
| Expectancy/PF/Win rate with N and window | Supports review but risks small-N overinterpretation | SRE precision/recall analogy; design synthesis [13](#ref-13) | **Partial**; research-only, descriptive | Research dashboard |
| Risk-guard matrix with headroom | Makes loss/exposure controls actionable | Existing risk framework; SRE alertability principles [12](#ref-12) | **Yes**; required | Execution dashboard |
| Guard audit timeline | Explains who/what/when/why for a pause or kill | OWASP/audit design plus governance constraint [24](#ref-24)[25](#ref-25) | **Yes**; required | Execution dashboard + audit log |
| Step-up auth and CSRF protection on brakes | Prevents browser/session abuse of state-changing controls | OWASP session and CSRF guidance [24](#ref-24)[25](#ref-25) | **Yes**; required if remote | Backend + control UI |
| Hyperliquid mark/oracle/liquidation/funding card | Shows the actual mechanics of perp risk | Hyperliquid funding/liquidation/spec docs [21](#ref-21)[22](#ref-22)[23](#ref-23) | **Yes**; required for live perps | Execution dashboard |
| HFT latency, depth, Greeks, ML sentiment, auto-reoptimization | Avoids importing features whose value depends on out-of-scope systems | Explicit scope exclusions; Gekko maintenance status [8](#ref-8) | **No** for this system | Not at all |

## Findings explicitly discarded as out of scope

**Co-location, kernel bypass, FPGA, microsecond latency, and tick-level latency dashboards** were discarded because the bot decides on 5-minute to 1-hour bar closes and has a seconds-level decision budget. Only order-acknowledgment and data-freshness timing transfers.

**Deep order-book and market-making analytics** were discarded because the strategy is not market making and does not depend on depth. A compact spread or execution-reference value may transfer when explaining fills.

**Institutional OMS/EMS/FIX workflows and multi-desk/multi-tenant permission systems** were discarded because the system has one owner, 1–5 workers, and no SaaS or team requirement. The transferable part is command auditability and reconciliation.

**Options Greeks and portfolio-margin optimization** were discarded because the planned live product is a crypto perpetual future and the prompt explicitly excludes options. Perpetual margin, mark price, funding, and liquidation health were retained.

**ML feature stores, always-on sentiment, self-optimizing strategies, and automatic parameter re-optimization** were discarded because the strategy is frozen and promoted through a governed research pipeline. Any advisory LLM must remain isolated from order flow.

**Screen-candy widgets, per-bar notifications, and single-number live health scores** were discarded because they increase noise or imply statistical confidence that the small sample cannot support. They were replaced by structured state, headroom, audit history, and chart-linked evidence.

## References

<a id="ref-1"></a>[1] Freqtrade, “FreqUI,” official documentation: <https://www.freqtrade.io/en/stable/freq-ui/>

<a id="ref-2"></a>[2] Freqtrade, “REST API,” official documentation: <https://www.freqtrade.io/en/stable/rest-api/>

<a id="ref-3"></a>[3] Freqtrade, “FAQ,” official documentation: <https://www.freqtrade.io/en/stable/faq/>

<a id="ref-4"></a>[4] Jesse, official documentation and changelog: <https://docs.jesse.trade/> and <https://docs.jesse.trade/docs/changelog>

<a id="ref-5"></a>[5] OctoBot, official guide: <https://www.octobot.cloud/en/guides/octobot>

<a id="ref-6"></a>[6] Hummingbot, “Hummingbot API,” official documentation: <https://hummingbot.org/hummingbot-api/>

<a id="ref-7"></a>[7] NautilusTrader, “Live Trading,” official documentation: <https://nautilustrader.io/docs/latest/concepts/live/>

<a id="ref-8"></a>[8] Gekko, official project site and maintenance notice: <https://gekko.wizb.it/>

<a id="ref-9"></a>[9] Hyperliquid, “Exchange endpoint,” official API documentation: <https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/exchange-endpoint>

<a id="ref-10"></a>[10] Hyperliquid, “WebSocket timeouts and heartbeats,” official API documentation: <https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/websocket/timeouts-and-heartbeats>

<a id="ref-11"></a>[11] Hyperliquid, “Info endpoint,” official API documentation: <https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint>

<a id="ref-12"></a>[12] Google SRE, “Monitoring Distributed Systems”: <https://sre.google/sre-book/monitoring-distributed-systems/>

<a id="ref-13"></a>[13] Google SRE Workbook, “Alerting on SLOs”: <https://sre.google/workbook/alerting-on-slos/>

<a id="ref-14"></a>[14] Prometheus, “Alertmanager configuration”: <https://prometheus.io/docs/alerting/latest/configuration/>

<a id="ref-15"></a>[15] Freqtrade maintainer issue, “Partial fill below minimum tradable amount”: <https://github.com/freqtrade/freqtrade/issues/2877>

<a id="ref-16"></a>[16] Hummingbot issue, “Order filled while in the process of cancellation”: <https://github.com/hummingbot/hummingbot/issues/7140>

<a id="ref-17"></a>[17] Hummingbot issue, “Gate.io perpetual position-stream exception and repeated close attempts”: <https://github.com/hummingbot/hummingbot/issues/6032>

<a id="ref-18"></a>[18] Hummingbot issue, “Hyperliquid delayed/incomplete fill updates and zero-size order”: <https://github.com/hummingbot/hummingbot/issues/7322>

<a id="ref-19"></a>[19] Hummingbot issue, “Failed order events followed by successful fills causing duplicate orders”: <https://github.com/hummingbot/hummingbot/issues/7294>

<a id="ref-20"></a>[20] Freqtrade issue, “Exchange-order refinding after balance/state mismatch”: <https://github.com/freqtrade/freqtrade/issues/11085>

<a id="ref-21"></a>[21] Hyperliquid, “Funding,” official trading documentation: <https://hyperliquid.gitbook.io/hyperliquid-docs/trading/funding>

<a id="ref-22"></a>[22] Hyperliquid, “Liquidations,” official trading documentation: <https://hyperliquid.gitbook.io/hyperliquid-docs/trading/liquidations>

<a id="ref-23"></a>[23] Hyperliquid, “Contract specifications,” official trading documentation: <https://hyperliquid.gitbook.io/hyperliquid-docs/trading/contract-specifications>

<a id="ref-24"></a>[24] OWASP, “Session Management Cheat Sheet”: <https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html>

<a id="ref-25"></a>[25] OWASP, “Cross-Site Request Forgery Prevention Cheat Sheet”: <https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html>

<a id="ref-26"></a>[26] Interactive Brokers, official API documentation: <https://interactivebrokers.github.io/tws-api/order_submission.html> and <https://www.interactivebrokers.com/campus/ibkr-api-page/webapi-doc/>
