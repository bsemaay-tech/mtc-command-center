# Deep Research Report: Dashboard & Observability for Bar-Close Retail Trading Bots

> **Research Scope Statement**: This report is strictly limited to bar-close decision cadence (5-minute to 1-hour candles), single-operator, self-hosted, retail-scale (five-figure USD) trading systems. All recommendations are evaluated against this constraint.

---

## 1. Feature Inventory of Comparable Systems

### Freqtrade + FreqUI

FreqUI is Freqtrade's official web frontend, featuring a responsive design with light/dark themes.

**Main Screen (Dashboard)** :
- Multi-bot overview (switchable/filterable)
- Wallet balance over time chart (including unrealized P&L)
- Pair list (left side), candlestick chart with technical indicators (center), current positions (bottom)
- Entry/exit signal markers visualized on the chart

**One Click Away**:
- Trade View: Visualize trades and interactively start/stop bots, force open/close positions
- Plot Configurator: Custom technical indicator combinations
- Backtesting interface
- System settings (timezone, background sync, confirmation dialogs)

**Deliberately Absent**: FreqUI does not support hot-editing strategy parameters (requires strategy file modification); no native multi-account support (requires third-party tools).

**Most Frequently Requested by Users**: Multi-account monitoring, richer chart configurations, mobile adaptation.

### Jesse

Jesse provides two web interfaces:

**app.py (port 8060)** — Full AI-augmented system:
- 9 functional modules: System Overview, Multi-exchange Prices, AI Analysis Process, Decision Process, Strategy Evolution, Trade Records, Risk Control, System Configuration, Logs
- Real-time trading signal monitoring, AI prediction display, intelligent suggestion system, arbitrage opportunity analysis

**dashboard.py (port 8061)** — Focused on data display:
- Strategy evolution path visualization, performance metrics monitoring

Jesse v3 roadmap includes: customizable dashboard layouts, Monte Carlo analysis UI, built-in code editor.

### OctoBot

OctoBot provides a unified dashboard for managing wallets, automations, and multi-strategy setups. Supports:
- Multiple strategy types (Grid, DCA, Crypto Basket, TradingView signals)
- 15+ exchange integrations (including Hyperliquid)
- Web, Mobile App, and Telegram interfaces

### Hummingbot Dashboard

Built on Streamlit:
- Strategy controller visual configuration and backtesting
- Multi-bot deployment and management
- Performance analytics (Sharpe ratio, PnL, max drawdown, win rate)
- Backtest manager (including Optuna hyperparameter optimization)

Since v2.7.0, driven by the Hummingbot API for a more robust architecture.

### NautilusTrader Pro Dashboard

Professional-grade dashboard:
- Real-time node monitoring and control
- Portfolio status, execution records, strategy management
- Real-time performance metrics
- Docker containerized deployment

Provides interactive HTML tearsheets for backtest analysis (Plotly-based).

**Extraction for Bar-Close Cadence**: The following features from these systems are directly relevant — pair/strategy status overview, position and PnL display, candlestick charts with signal markers, risk metric monitoring, and trade history querying. The following are of limited value — microsecond latency monitoring, order book depth visualization, HFT-specific panels (Jesse's dashboard.py component for AI trading is partially overkill).

---

## 2. Reconciliation

### Core Patterns

Reconciliation is the process of comparing the local execution state (orders, fills, positions) against the exchange's authoritative state. Local views can diverge due to network failures, process restarts, partial fills not processed, etc.

**Recommended Patterns**:
1. **Dual-path reconciliation**: WebSocket real-time incremental updates + periodic REST queries as ground truth.
2. **Regular probes**: Compare exchange positions with the local DB at fixed intervals (e.g., every 15 minutes).
3. **Tolerance handling**: Set quantity/amount thresholds to ignore dust-level discrepancies.
4. **Auto-repair**: Automatically correct when safe; alert for human intervention when dangerous.

**Reconciliation Levels**:
- **Order-level matching vs Fill-level matching**: A single order may generate multiple fills (especially in derivatives). Aggregating fills by order before matching avoids false-positive drift alerts.

### Consequences of Missing Reconciliation (Post-Mortem Evidence)

- **Orphan positions**: Exist on the exchange but are unrecorded locally → capital/resource leakage.
- **Phantom positions**: Exist locally but not on the exchange → trigger unwanted operations.
- **Drift**: Gradual state inconsistency over time.
- **Specific Case**: A retail trader's reconciler generated 33 false-positive "DB↔Exchange DRIFT" alerts when an order changed from 1 contract to 2 contracts — because the exchange split the 2 contracts into two 1-contract fills, and the reconciler matched at the fill level rather than the order level.

**Design Recommendations**:
- Reconciliation cadence: For bar-close cadence, every 5–15 minutes is sufficient.
- Alert thresholds: Set reasonable tolerances (e.g., 5%–10%) to avoid noise.
- Audit trail: Log all reconciliation operations (including auto-repairs).

---

## 3. Staleness & Transport Health

### Core Problem

WebSockets can technically maintain a "connected" status while data flow has stopped; the main loop can deadlock without throwing exceptions. Standard error handling fails to catch this — because there is no error, only an absence of activity.

### Best Practices

**Heartbeat Design**:
- **Separate business-layer heartbeat from transport-layer keepalive**: Transport keepalive only maintains the connection; business-layer heartbeat verifies data flow.
- Heartbeat intervals should be compressed to less than half the load balancer timeout (typically 25–30 seconds, or even 15 seconds).
- For bar-close subscriptions: threshold should be `interval + 45s` (e.g., a 30m candle → ~31 minutes).

**Dead Man's Switch**:
- Heartbeat + watchdog thread: Trigger deduplicated critical alerts when the code stops "breathing."
- Example: `@ops.heartbeat(timeout_seconds=30)` decorator — triggers an alert if not called within 30 seconds.

**Distinguishing "Frozen Feed" vs "Quiet Market"**:
- Use a state machine: `realtime → delayed → close → stale` with automatic data source switching.
- Persist the timestamp of the last candle as an anchor; on reconnection, pull historical candles from the breakpoint.
- Maintain a last-received-data timestamp for each subscribed instrument.

**Exchange-Side Patterns**:
- Scheduled cancel-all (e.g., every 24 hours) as a fallback to prevent zombie orders.
- Position-level orphan detection — heartbeat monitoring answers "is the process running?" but position safety requires answering "are all positions being actively managed?"

---

## 4. Alerting for a Solo Operator

### Alert Taxonomy

**Critical (Immediate Push, Audible)** :
- Bot stopped unexpectedly
- Exchange API connection lost
- Stop-loss triggered
- Liquidation warning (approaching liquidation price)
- Account balance below threshold
- Dead-man alert (heartbeat timeout)

**Important (Notification, Can Wait)** :
- Trade start/end (with P&L)
- Take-profit reached
- Daily P&L crosses threshold (positive or negative)

**Informational (Digest or Optional)** :
- Grid fills, DCA buys, position changes, unrealized P&L updates

**Digest Only (Daily/Weekly)** :
- Total trades today, weekly win/loss ratio, total realized P&L, best/worst trades

### Fatigue Prevention Strategies

1. **Channel separation**: Critical alerts → primary Telegram (with sound); informational → muted group; digest → email.
2. **Batch non-urgent notifications**: 4-hour digest instead of per-event notifications.
3. **Status flag deduplication**: Send only once while a condition persists; reset only when the condition clears.
4. **Deduplication window**: e.g., same alert only once per 15 minutes.
5. **Threshold filtering**: Only notify when P&L exceeds a threshold.

### Notification Channel Reliability

- **Telegram**: Default channel for crypto traders — instant, rich formatting, mute schedules, robust Bot API.
- **Discord**: Suitable for team/community sharing.
- **Email**: Not suitable for real-time alerts (too slow); suitable for daily digests and written records.
- **ntfy**: Lightweight push alternative.

**Telegram Reliability Considerations**: Need to handle API rate limits, bot token rotation, and persistent chat IDs. For critical alerts, recommend pushing to two independent channels for redundancy.

---

## 5. Incident-Response UX — What the First Screen Must Answer in 60 Seconds

### Key Lessons from Incident Reports

**Case 1: 16-Hour Downtime, Positions Still Alive**
> "The bot died. The positions stayed alive. For 16 hours, neither Sentinel nor Horus spotted the discrepancy. That gap — between process aliveness and position safety — is where the loss lives."
>
> Lesson: Heartbeat monitoring answers "is the process running?" but position safety requires answering "are all positions being actively managed?" These are different checks.

**Case 2: Reconciliation False-Positive Storm**
> 33 false-positive "DB↔Exchange DRIFT" alerts. Root cause: the exchange split a 2-contract order into two 1-contract fills, and the reconciler matched at the fill level.
>
> Lesson: Aggregate fills by order before reconciling.

**Case 3: Undetected Data Stagnation**
> WebSocket remained connected but data flow stopped; the main loop deadlocked without exceptions.

### 60-Second Incident Response First Screen Checklist

| Priority | Display | Purpose |
|----------|---------|---------|
| 🔴 P0 | **All current positions** (instrument, direction, size, entry price, current price, unrealized P&L, liquidation distance) | Confirm capital safety |
| 🔴 P0 | **Bot aliveness** (last heartbeat time, status of each worker process) | Confirm system is running |
| 🔴 P0 | **Exchange connection status** (last message time per WebSocket, REST availability) | Confirm data source health |
| 🟠 P1 | **Latest reconciliation result** (local vs exchange discrepancies, if any) | Detect drift |
| 🟠 P1 | **Most recent trade decision** (time, direction, rationale, execution result) | Understand what the bot is doing |
| 🟡 P2 | **Risk budget consumption** (daily loss % used, current max drawdown) | Assess if brakes are needed |
| 🟡 P2 | **System resources** (CPU, memory, disk) | Rule out infrastructure issues |

**Key Principle**: The first incident screen should not require scrolling or clicking — all critical status should be visible in a single view. Design for practical usability over aesthetic animations.

---

## 6. Trade Journal & Post-Trade Review

### Journal Schema Design

**TradeDecisionRecord (Complete Trade Record)** :
- Trade identifiers: instrument, direction (LONG/SHORT), size
- Prices: entry, exit, target, stop-loss
- Timestamps: entry time, exit time (ISO 8601)
- Outcome: status (OPEN/WIN/LOSS), realized P&L, holding period, exit reason, exit mechanism
- Decision context (DecisionContext)

**DecisionContext (Decision Chain)** :
- `agent_signals`: Contribution of each decision signal (agent name, signal direction, confidence, reasoning)
- `portfolio_decision`: Portfolio-level decision
- `risk_assessment`: Risk manager output
- `strategy_params`: Strategy parameters (entry conditions, risk-reward ratio, etc.)
- `scanner_source`: Signal origin

### Storage Granularity Recommendations

For bar-close cadence (0–5 trades/day):

| Stored Content | Granularity | Retention |
|----------------|-------------|-----------|
| Decision context (including indicator values) | Per trade | Permanent |
| Candlestick snapshots (indicator values at decision time) | Per trade | Permanent |
| System state snapshots | Per minute or per candle | 30 days |
| Raw logs (debug) | Per event | 7 days |
| Fill/order data | Per event | Permanent |

**Storage Format**: Append-only JSONL (diary.jsonl) + structured storage in SQLite.

### Chart-Linked Replay

- Mark entries/exits on the candlestick chart
- Hover to display detailed decision data
- Filter and replay by time range

---

## 7. Performance Analytics Minimal Set — Statistical Meaningfulness at Small N

### Considerations for 0–5 Trades/Day

**Small Sample Problem**: With 5 trades, percentage growth can be misleading. Past performance does not guarantee future results.

**Statistically Meaningful Metrics**:

| Metric | Applicability | Notes |
|--------|---------------|-------|
| **Realized P&L ($)** | ✅ Direct | Absolute value, independent of sample size |
| **Average P&L per trade** | ✅ Direct | Simple average, stabilizes as trades accumulate |
| **Win Rate** | ⚠️ Use with caution | Highly volatile when N<30; use as reference only |
| **Profit Factor** | ⚠️ Use with caution | Easily distorted by extreme values at small N |
| **Max Drawdown ($)** | ✅ Direct | Absolute value is meaningful |
| **Max Drawdown (%)** | ⚠️ Use with caution | Small account percentages fluctuate heavily |
| **Sharpe Ratio** | ❌ Not applicable | Requires large sample size for significance |
| **Sortino Ratio** | ❌ Not applicable | Same as above |

### Live Slippage Tracking

- Record **expected price** (signal price at decision time) vs **actual fill price** per trade.
- Calculate slippage = actual fill price - expected price (directional).
- Cumulative slippage statistics: mean, standard deviation, max slippage.
- Compare against backtest assumptions: e.g., if backtest assumed 0.05% slippage but live shows 0.15%, strategy expectations need adjustment.

### What Mature Systems Compute

Freqtrade calculates:
- Max drawdown (amount and period)
- Underwater period
- Win rate, profit factor, number of trades

These are computed periodically by the PerformanceMonitor and written to the local SQLite DB.

**Recommendation**: Display live vs backtest comparisons (PnL curve overlay, slippage comparison) in the dashboard, but clearly label the sample size.

---

## 8. Risk-Guard Visualization

### Risk State Display

**Guards to Display**:
- Daily loss limit: used ($ and %), remaining
- Weekly loss limit: same as above
- Max drawdown kill switch: current drawdown ($ and %), trigger threshold, distance to trigger
- Consecutive loss pause: current consecutive losses, trigger threshold
- Exposure cap: current total exposure ($), cap ($)

**Status Color Scheme**:
- 🟢 Green: Normal (< 50% limit)
- 🟡 Yellow: Warning (50%–80% limit)
- 🟠 Orange: Near trigger (80%–95% limit)
- 🔴 Red: Triggered / Braked

### Kill Switch UI

- Large red "KILL" button with double confirmation
- Display all currently active positions to assess before killing
- State change audit trail: timestamp, operator, reason
- Clear three-state display: ARM / DISARM / KILL

### Pre-Trigger Warnings

- Send a warning notification when losses reach 80% of the limit
- Highlight in the dashboard when drawdown approaches the kill threshold
- Countdown or "remaining allowance" display

---

## 9. Security Baseline

### Current State Assessment

The system currently uses loopback-only (127.0.0.1) + SSH tunnel access. This already **mitigates the majority of remote attack vectors**.

### Additional Hardening Recommendations

| Measure | Priority | Notes |
|---------|----------|-------|
| **Strong JWT secret** | High | Use a fixed `jwt_secret_key` rather than a temporary token regenerated on each restart |
| **API authentication** | High | All non-localhost endpoints require authentication |
| **Rate limiting** | Medium | 5 authentication attempts per 15 minutes |
| **CSRF protection** | Medium | Enable for all POST endpoints |
| **Session management** | Medium | Session timeout controls |
| **2FA** | Medium | Mandatory if exposed remotely |
| **HTTPS reverse proxy** | Medium | When accessing remotely |
| **Strict CORS configuration** | Low | Allow only explicitly defined origins |

### Documented Security Incidents & Lessons

- **Exposed FreqUI/Grafana instances** found by scanners are a common issue. Freqtrade officially strongly recommends **not exposing the API to the internet**.
- **Misconfigured CORS** leads to cross-origin attacks.
- For remote deployments, set `API_AUTH_KEY`; for local localhost workflows, low friction can be maintained.

**Practical Advice for Solo Operators**: Keep loopback+SSH tunnel as the primary access method. If remote access is required, use HTTPS reverse proxy + strong authentication + 2FA. Regularly check for accidentally exposed services.

---

## 10. Perpetual-Specific Surfaces

### Must-Display Metrics

| Metric | Importance | Notes |
|--------|------------|-------|
| **Margin health** | 🔴 Critical | Used margin / total margin ratio |
| **Liquidation price** | 🔴 Critical | Distance from current price to liquidation for open positions |
| **Free margin ratio** | 🟠 Important | Margin available for new positions |
| **Unrealized P&L** | 🟠 Important | Including margin impact |
| **Funding rate** | 🟡 Medium | Current rate and cumulative impact on P&L |
| **Leverage** | 🟡 Medium | Current effective leverage |
| **Exposure/Equity ratio** | 🟡 Medium | Risk concentration |

### Misleading Presentations to Avoid

1. **Displaying only percentages without absolutes**: Small accounts show volatile percentages that can mislead.
2. **Ignoring cumulative funding rate impact**: Perpetual funding rates continuously erode or augment P&L; cumulative funding must be displayed.
3. **Unclear liquidation price display**: Show both the absolute liquidation price and the distance from the current price (in $ and %).
4. **Isolated leverage display**: Leverage must be viewed together with margin usage and volatility.

### How Comparable Dashboards Present These

Hyperliquid-specific dashboards typically display:
- Total account value, unrealized P&L, used margin, withdrawable balance
- Per position: instrument, entry/mark price, leverage, P&L
- Margin utilization, concentration score, free margin ratio

**Recommendation for Bar-Close Cadence**: Given low decision frequency, real-time refresh of these metrics (every 30–60 seconds is sufficient) is not strictly necessary, but liquidation warnings must be pushed in real time.

---

## 11. Anti-Features

### Features to Avoid

| Anti-Feature | Why Useless/Harmful | Source |
|--------------|---------------------|--------|
| **Axis-less charts** | Cannot read precise prices | General UX consensus |
| **Excessive aesthetics/animations** | Adds visual noise, reduces glanceability | General UX consensus |
| **Always-on "AI sentiment"** | No decision value for bar-close strategies; distracts | General consensus |
| **False precision** | Displaying too many decimals (e.g., $0.00000001) creates false certainty | Industry consensus |
| **Pushed social/news content** | Irrelevant to trading decisions; distracts | General consensus |
| **Sub-second latency monitoring** | Bar-close cadence doesn't need microsecond latency data | This report's scope |
| **Order book depth heatmaps** | Bar-close strategies don't rely on microstructure | This report's scope |
| **Axis-less numerical charts** | Impossible to perform quantitative analysis | General UX consensus |
| **Mandatory multi-window/complex layouts** | Single operator needs simplicity and one-screen visibility | General consensus |

### Features Users Have Actually Reported as Useless

- Trading 212 users complained the new UI "focuses excessively on aesthetics and animations rather than practical usability"
- "Statistics features are useless; the theme is now terrible"
- 15-minute delayed market data makes dashboards completely useless for 1-hour and shorter timeframes

**Core Principle**: For a bar-close solo operator, the Dashboard should prioritize displaying the **minimum information set required for decision-making**, rather than feature stacking.

---

## Consolidated Summary Table

| Feature | Problem It Solves | Evidence (Source) | Fits Bar-Close Solo Cadence? | Suggested Surface |
|---------|-------------------|-------------------|------------------------------|-------------------|
| Multi-bot/strategy status overview | Quick understanding of all strategy run states | FreqUI Dashboard | ✅ Fully applicable | Execution Dashboard |
| Candlestick chart + trade signal markers | Visual decision validation | FreqUI | ✅ Fully applicable | Execution Dashboard |
| Positions & P&L real-time display | Understand current risk exposure | FreqUI | ✅ Fully applicable | Execution Dashboard |
| Reconciliation (local vs exchange) | Detect orphan/phantom positions | Position Tracker | ✅ Fully applicable | Execution Dashboard |
| Data freshness / heartbeat monitoring | Detect "silent death" | opsquant | ✅ Fully applicable | Execution Dashboard |
| Dead-man switch alert | Notify when bot stops | opsquant | ✅ Fully applicable | Backend Gate |
| Tiered alerts (critical/important/digest) | Prevent alert fatigue | Industry consensus | ✅ Fully applicable | Backend Gate |
| Trade decision logging (with context) | "Why did the bot do that?" | TradeDecisionRecord | ✅ Fully applicable | Research Dashboard |
| Live vs backtest comparison | Detect strategy degradation | Industry consensus | ✅ Fully applicable | Research Dashboard |
| Risk guard visualization | Risk budget status at a glance | Industry consensus | ✅ Fully applicable | Execution Dashboard |
| Kill Switch (read-only + brakes) | Emergency stop | Industry consensus | ✅ Fully applicable | Execution Dashboard |
| Margin health / liquidation distance | Perpetual-specific risk | Industry consensus | ✅ Fully applicable | Execution Dashboard |
| Cumulative funding rate impact | Accurate perpetual P&L | Industry consensus | ✅ Fully applicable | Execution Dashboard |
| Strategy parameter hot-editing | Allow UI strategy modification | Governance prohibition | ❌ Not applicable (governance) | Do Not Implement |
| Manual order entry | Bypass strategy governance | Governance prohibition | ❌ Not applicable (governance) | Do Not Implement |
| Order book depth maps | Bar-close strategies don't rely on order book | Scope statement | ❌ Not applicable | Do Not Implement |
| Microsecond latency monitoring | Decision latency budget is seconds | Scope statement | ❌ Not applicable | Do Not Implement |
| Multi-tenant/team features | Single operator | Scope statement | ❌ Not applicable | Do Not Implement |
| Always-on AI sentiment | No decision value | Industry consensus | ❌ Not applicable | Do Not Implement |
| False precision (>6 decimals) | Creates false certainty | Industry consensus | ❌ Not applicable | Do Not Implement |

---

## Discarded Findings (Out-of-Scope Filtering Audit)

| Discarded Finding | Reason for Exclusion (One Line) |
|-------------------|--------------------------------|
| Kernel bypass networking | Decision latency budget is seconds, no need for microsecond networking |
| FPGA acceleration | Bar-close cadence involves minimal computation, CPU is sufficient |
| Order book microstructure analysis | Strategies are based on candles, not the order book |
| Tick-level data replay | Decisions are based on 5-minute to 1-hour candles |
| Multi-asset portfolio optimization | Each worker trades a single instrument |
| Options/Greeks monitoring | Only perpetual futures are traded |
| FIX protocol connectivity | REST/WebSocket APIs are sufficient |
| Institutional OMS/EMS | Single retail operator, no multi-desk requirement |
| ML feature stores | Strategies come from Pine Script ports; no ML involved |
| Market-making analytics | Strategies are directional, not market-making |
| Multi-tenant/SaaS features | Single self-hosted operator |
| Sub-second order latency monitoring | 500ms latency is operationally fine for bar-close cadence |