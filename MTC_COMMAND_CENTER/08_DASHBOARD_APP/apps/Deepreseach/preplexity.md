1. Feature inventory of comparable systems
Freqtrade + FreqUI
FreqUI provides a trade view and dashboard as its core screens. The trade view visualizes trades the bot is making and allows interaction (start/stop, force entries/exits if configured). The dashboard gives an overview of performance and status, with multi-bot switching if applicable. Recent additions (2026.4) include a wallet-balance-over-time chart showing actual balance including unrealized P&L, deposits, and withdrawals. FreqUI also added live metrics like CAGR, Calmar, Sortino, Sharpe, and SQN directly in the dashboard, plus an "At Risk" field in the trade detail pane for real-time risk exposure. One click away are backtesting, performance analytics (equity curves, drawdown), log monitoring, and configuration management. Deliberately absent from the execution view: manual order entry beyond force-trade controls, and parameter editing is limited to configuration pages rather than live trading screens. Docs and issues show users demanded better live metrics, chart annotations, and risk visibility most.

Jesse
Jesse's GUI dashboard replaced its CLI in 0.30.0 and serves as the primary interface at localhost:9000. The Live page shows real-time candle charts, position monitoring, watchlist display, and supports multiple simultaneous sessions. Aggregated live metrics include Total P&L, P&L %, Current/Started Balance, Open Positions, Open Orders, Total Trades, and Win Rate, all updated in real-time. One click away are backtest, optimize, Monte Carlo, import candles, strategies (built-in code editor), settings, and history pages. A trade chart feature lets users browse saved candles, executed orders, closed trades, and indicator values while a session runs or after it ends. Jesse docs emphasize real-time logs and notifications (Telegram, Slack, Discord) as heavily used. Users demanded interactive charts, multi-session equity comparison, and per-trade context capture most.

Hummingbot (Condor)
Hummingbot's Condor provides both a Telegram-based control center and a web dashboard. The web dashboard shows a unified portfolio across exchanges with real-time balance, portfolio value history, asset distribution, and 24h P&L. The Bots section monitors multiple bot instances with health indicators, system metrics (CPU, memory, uptime), controller performance, start/stop controls, and log viewing. The Positions panel tracks open positions across exchanges with real-time P&L, size, leverage, entry/mark prices, and quick close actions. Condor also supports executor configuration (grid, DCA, TWAP, position executors) with visual configuration and live performance metrics. Deliberately absent from the core monitoring view: manual order entry beyond executor configuration, and parameter tuning is isolated to executor setup pages. Community feedback emphasizes bot health, log access, and multi-bot deployment monitoring most.

OctoBot, NautilusTrader, Gekko successors
OctoBot's public documentation is sparse; its dashboard focuses on strategy configuration and backtesting rather than live execution monitoring. [research gap] NautilusTrader emphasizes low-latency execution and does not ship a retail-facing dashboard; its observability is log/metrics-driven. [research gap] Gekko's successors (e.g., Freqtrade, Jesse) absorbed its user base; modern dashboards follow FreqUI/Jesse patterns above. [research gap]

2. Reconciliation
Reconciliation patterns for bots with local DB truth vs exchange reality center on reconciliation loops that run on startup and periodically. The exchange is treated as source of truth; local state is a cache.

Startup sequence best practice:

Load local state from disk/DB.

Run reconciliation loop before enabling trading.

Update risk limits based on corrected position.

Resume WebSocket streams.

Enable trading only after steps 1–4 complete.

Reconciliation loop detects:

Orphan orders: Orders on exchange not tracked locally.

Ghost orders: Local orders that never reached exchange.

Stale fills: Fills that happened while disconnected.

Position drift: Final truth check against exchange position.

Post-mortems show that without reconciliation, bots suffer phantom/orphan positions, double fills, and ghost orders after restart, leading to unintended exposure or missed exits. One incident report notes bots bleeding for hours due to position-tracking drift before an alert fired.

Cadence: Run reconciliation on every startup, then periodically (e.g., every N minutes) and after any WebSocket reconnect. Drift should be logged for monitoring and alerting.

3. Staleness & transport health
Heartbeat design: Application-level ping/pong inside WebSocket (not just TCP keepalive) is essential. Send ping every 10–30 seconds; expect pong within 5–10 seconds or treat connection as dead.

Dead-man patterns:

Client-side: Background watchdog thread monitors last-received heartbeat timestamp; if no message in configurable window, force reconnect.

Exchange-side: Use exchange auto-cancel-all-orders-after-N-seconds timer (dead-man's switch); bot refreshes timer while healthy; if bot goes dark, exchange cancels resting orders.

"Feed frozen vs market quiet" disambiguation: Track last event time per channel, heartbeat round-trip time, event age, and sequence identifier. Log gap between last received message and disconnect time to distinguish idle timeout from sudden drop.

Reconnect strategy: Exponential backoff with jitter (base 1–2s, cap 30–60s) to avoid thundering herd. After reconnect, fetch REST snapshot of relevant state (orders, positions) and reconcile before resuming live updates.

Staleness surfacing: Display WebSocket state (connected/reconnecting/disconnected), last message age, and reconnect count on dashboard. Alert if last message age exceeds threshold (e.g., 2× loop interval).

4. Alerting for a solo operator
Alert taxonomy (page vs digest vs log-only):

Page immediately: SL/TP trigger, large loss, order error, exchange outage, position drift detected, bot went silent (dead-man).

Digest (batched): Daily P&L report, configuration changes, routine reconnections.

Log-only: Minor API retries, successful fills within expected slippage, normal heartbeats.

Rate-limiting/dedup: Deduplicate identical events; use exponential backoff retries for notification delivery (immediate, 5s, 15s, 1min, then switch to backup channel). Implement dead-letter queue for undelivered alerts.

Dead-man ("bot went silent") alerts: Use external heartbeat service (e.g., Healthchecks.io); bot pings every N minutes; if pings stop, alert via email + push. Set grace period to ~2× loop interval.

Notification-channel reliability: Telegram has ~1–3s delivery, 99.9% rate, instant push; email can take 30s–5min and may hit spam. Best practice: Telegram for real-time, email for reports; fallback to SMS for critical if Telegram unavailable.

5. Incident-response UX
First 60 seconds, first screen must answer:

Is the bot alive? (heartbeat status, last message age)

What is the current position? (size, entry, unrealized P&L, liquidation price)

Are orders aligned? (open orders on exchange vs local, ghost/orphan detection)

What failed? (exchange outage, WebSocket disconnect, API error rate spike)

What are risk limits? (daily loss remaining, drawdown status, kill-switch armed/triggered)

Incident write-ups highlight needs: exchange outage → show reconnect state and last known good position; partial fill storm → show fill history and slippage vs expected; stuck orders → show order status and cancel capability; restart with open positions → show reconciliation status and corrected position.

On-screen checklist derived:

Bot heartbeat OK?

Position reconciled with exchange?

Open orders match local state?

Risk limits within bounds?

Last error logged with timestamp?

6. Trade journal & post-trade review
Journal schema essentials:

Decision-chain logging: Log every decision, order, fill, and error with context (gate states, indicator values at entry).

Per-trade context: Capture indicator values, gate states, signal strength, timestamp, bar close that triggered.

Chart-linked replay: Interactive charts showing saved candles, executed orders, closed trades, and indicator overlays for each trade.

Granularity worth storing:

Entry/exit prices, sizes, timestamps.

Indicator values at decision time.

Gate states (e.g., risk guard armed/triggered).

Slippage vs expected fill.

Error messages and retry counts.

Review UI: Table of executed trades with navigation to most profitable/worst trades; filter by date, symbol, P&L. Equity curve with trade markers; click to jump to trade chart.

7. Performance analytics minimal set
For 0–5 trades/day, statistically meaningful metrics:

Live slippage tracking: Average slippage per trade vs backtest expectation; flag if live slippage exceeds backtest by >50%.

Expectancy/PF confidence at small N: Show profit factor with confidence interval (e.g., bootstrap or Monte Carlo range) rather than point estimate.

Drawdown presentation: Rolling drawdown from peak equity; compare to backtest max drawdown (alert if live DD >120% of backtest).

Trade count and frequency: Track if live trade frequency deviates >40% from expected (signals execution issues).

What mature bots compute live vs delegate:

Live: P&L, win rate, open positions, slippage per fill, order success/failure rate.

Delegate to research: Sharpe/Sortino/CAGR (computed offline on larger samples), Monte Carlo robustness, walk-forward optimization.

8. Risk-guard visualization
UI patterns for loss budgets, kill switches, exposure caps:

Armed/triggered states: Visual indicator (green/yellow/red) showing if risk guard is armed, pre-trigger warning, or triggered.

Pre-trigger warnings: Show remaining budget (e.g., "Daily loss: $80/$100 remaining") with progress bar.

Audit trail: Log state changes (who/when/why) for kill-switch triggers, exposure cap breaches, consecutive-loss pauses.

Exposure caps: Display current exposure vs max allowed (e.g., "Exposure: $150/$200 max per market").

Consecutive-loss pause: Show count (e.g., "Losses: 3/5 before pause") with reset timer.

9. Security baseline
Hardening beyond loopback+SSH-tunnel:

Auth patterns: JWT with strong secret; 2FA (TOTP) for web dashboard; session handling with timeout and CSRF protection on control endpoints (ARM/DISARM/KILL).

CSRF mitigation: Set cookie_samesite=strict; use __Secure- or __Host- cookie prefixes.

CORS: Restrict CORS_origins to exact origin (no trailing slash); never use * with credentials.

Documented compromises: Exposed FreqUI/Grafana instances found by scanners due to misconfigured CORS or missing auth. Lessons: bind to loopback only; require JWT; enforce 2FA for any remote exposure.

Proportionate to solo operator: TOTP 2FA, session timeout (e.g., 15min idle), rate-limiting on login, audit log of logins and control actions.

10. Perp-specific surfaces
Margin health: Show initial margin ratio (IMR) and maintenance margin ratio (MMR); alert if MMR approaches liquidation threshold.

Liquidation distance: Display liquidation price and distance from current mark price; update in real-time.

Funding-rate impact: Show current funding rate, next funding countdown, and cumulative funding paid/received since position open.

Presentations that mislead:

Showing only predicted funding rate without countdown → traders miss timing.

Displaying unrealized P&L without funding accrual → understates true P&L.

Liquidation price without margin mode (cross/isolated) context → misestimates risk.

Best practice: Unified view with margin usage, liquidation distance, funding P&L matrix (current interval + historical), and scenario modeling (stress test price moves).

11. Anti-features
Features commonly present but useless/harmful for bar-close solo-operator cadence:

Tick-level microstructure analytics: Irrelevant for bar-close decisions; screen candy. [exclude per scope]

Always-on AI sentiment: Adds noise, no decision value for frozen-parameter strategies. [opinion: aligns with governance constraint]

Manual order entry: Forbidden by governance; harmful if accidentally used. [constraint]

Fake precision (e.g., P&L to 8 decimals): Misleading at retail scale; round to sensible units. [opinion]

Sub-second latency dashboards: Overkill for seconds-level decision budget. [exclude per scope]

Sources: Practitioner blogs emphasize forward-test over backtest, and warn against overfitting to noise; dashboards should not encourage parameter tweaking live.

Consolidated feature table
feature	problem it solves	evidence (source)	fits bar-close solo-operator cadence? (yes/no/partial + why)	suggested surface
Reconciliation loop on startup	Prevents orphan/ghost orders, position drift	
yes — critical for safety after restart	backend gate + dashboard status
WebSocket heartbeat + dead-man switch	Detects silent disconnects, cancels orders if bot dies	
yes — matches seconds-level latency budget	backend gate + alert
External heartbeat (Healthchecks.io)	"Bot went silent" alert for solo operator	
yes — simple, reliable liveness check	backend gate + alert
Live slippage tracking vs backtest	Measures execution gap, flags degradation	
yes — meaningful even at small N	execution dashboard
Profit factor with confidence interval	Avoids overconfidence at small sample size	
partial — needs 30+ trades for reliability	research dashboard
Risk guard armed/triggered visualization	Shows loss budget status, kill-switch state	
yes — essential for operational safety	execution dashboard
Margin health (IMR/MMR) + liquidation distance	Prevents liquidation surprise on perps	
yes — perp-specific risk	execution dashboard
Funding-rate P&L matrix	Tracks cumulative funding impact on P&L	
yes — material for perp holding	execution dashboard
Trade journal with indicator context	Answers "why did bot do that?" post-trade	
yes — supports review and debugging	research dashboard
2FA + CSRF + CORS hardening	Prevents unauthorized dashboard access	
yes — security baseline	execution dashboard (auth layer)
Tick-level microstructure analytics	Low-latency order-book analysis	[exclude per scope]	no — irrelevant for bar-close	not at all
Manual order entry UI	Allows ad-hoc trading	[constraint]	no — forbidden by governance	not at all
Always-on AI sentiment	Real-time news/sentiment feed	[opinion]	no — adds noise, no decision value	not at all
Sub-second latency dashboard	Microsecond-level execution monitoring	[exclude per scope]	no — overkill for seconds budget	not at all
Discarded findings (out-of-scope-for-cadence)
Co-location/FPGA/kernel bypass latency dashboards: Only relevant for HFT; bar-close bot has seconds-level budget. [exclude]

Market-making order-book-depth analytics: Hummingbot market-making focus; not applicable to bar-close strategies. [exclude]

OMS/EMS/FIX connectivity: Institutional multi-desk systems; solo operator uses WebSocket/REST. [exclude]

Options/greeks, portfolio-margin optimization: Perp futures only; no options in scope. [exclude]

ML feature-store/alpha-research tooling: Strategies are frozen-parameter; no live re-optimization. [exclude]

Sub-second reaction features: Any dashboard requiring <1s response is mismatched to bar-close cadence. [exclude]