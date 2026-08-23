# MRC Bridge — Open-Source Technical Foundation Investigation

**Research snapshot: 18 August 2026**

The central conclusion is strong: **MRC Bridge should not be built by cloning one trading platform, and it should not attempt to rewrite the whole trading stack.** The best foundation is a modular MRC-owned control plane wrapped around several specialist engines.

The recommended combination is:

**NautilusTrader** as the primary trading/runtime/backtesting engine, **hftbacktest** for high-fidelity HFT simulation, **Hummingbot** as an isolated specialist crypto/DEX/market-making runtime, **CCXT + cryptofeed + native Nautilus adapters** for exchange coverage and market data, **Qlib + MLflow** for ML research/model lifecycle, **MG Exchange Chart / TradingView Lightweight Charts / KLineChart** for charting, **NATS JetStream** for the distributed event backbone, **PostgreSQL + ClickHouse + Redis** for persistence, **Prometheus + OpenTelemetry** for observability, and **Keycloak** for IAM.

The most important part is what **not** to outsource: MRC should own the canonical order/state model, consolidated portfolio, global risk engine, reconciliation, audit trail, orchestration/control plane, canonical APIs, and dashboard. Those are the pieces that make MRC Bridge a coherent product rather than a UI sitting on someone else's bot.

---

# 1. Executive Summary

The recommended hierarchy is:

| Priority | Project | Role in MRC | Decision |
|---|---|---|---|
| **1** | **NautilusTrader** | Primary live/backtest/strategy/execution engine | **WRAP / CORE ENGINE** |
| **2** | **hftbacktest** | L2/L3, latency, queue-position HFT simulation | **RUN AS SERVICE** |
| **3** | **Hummingbot + Hummingbot API** | Crypto market-making, arbitrage, DEX/CEX runtime | **RUN AS SERVICE** |
| **4** | **CCXT** | Long-tail crypto exchange adapters | **WRAP** |
| **5** | **cryptofeed** | High-rate normalized crypto market data | **WRAP** |
| **6** | **QuantConnect LEAN** | Traditional-market coverage / second validation engine | **SEPARATE SERVICE** |
| **7** | **Qlib** | ML/quant research | **USE / ADAPT** |
| **8** | **MLflow** | Models, experiments, AI lifecycle | **USE DIRECTLY** |
| **9** | **MG Exchange Chart** | Advanced TradingView-like chart prototype | **PROTOTYPE / USE if validated** |
| **10** | **Lightweight Charts** | Stable chart-rendering fallback | **USE DIRECTLY** |
| **11** | **KLineChart** | Alternative advanced web charting | **PROTOTYPE** |
| **12** | **Artio** | Institutional FIX gateway | **SERVICE WHEN NEEDED** |
| **13** | **vn.py** | Traditional/Asian connectivity/reference | **REFERENCE / ADAPTER SOURCE** |
| **14** | **Jesse** | Strategy UX/optimization patterns | **REFERENCE / OPTIONAL RUNTIME** |
| **15** | **VisualHFT** | Order-flow/microstructure UI | **REFERENCE** |
| **16** | **OpenCharts** | Terminal UX/reference implementation | **ADAPT UI IDEAS** |
| **17** | **OpenTerminalUI** | Dashboard/page architecture | **REFERENCE** |
| **18** | **OpenAlgo** | Broker-gateway/UI ideas | **REFERENCE; AGPL** |
| **19** | **Tesser** | Emerging Rust design ideas | **WATCH / PROTOTYPE** |
| **20** | **OpenTrade/OEMS** | OEMS architecture | **REFERENCE** |
| **21** | **Barter** | Rust trading primitives | **REFERENCE / COMPONENTS** |
| **22** | **Freqtrade** | Crypto strategy/UI/optimization reference | **REFERENCE ONLY** |
| **23** | **OctoBot** | Bot/plugin architecture | **REFERENCE ONLY** |
| **24** | **StockSharp** | Connector/terminal feature reference | **REFERENCE; LICENSE REVIEW** |
| **25** | **Lumibot** | AI-decision/strategy UX ideas | **REFERENCE; LICENSE BLOCK** |
| **26** | **Superalgos** | Visual workflows/dashboard ideas | **REFERENCE** |
| **27** | **NATS** | Event transport / JetStream | **USE DIRECTLY** |
| **28** | **ClickHouse** | Tick/event/analytics store | **USE DIRECTLY** |
| **29** | **Prometheus + OpenTelemetry** | Metrics/telemetry | **USE DIRECTLY** |
| **30** | **Keycloak** | Authentication/IAM | **USE DIRECTLY** |

NautilusTrader is the strongest overall core-engine candidate because of its deterministic event-driven design, Rust core, Python integration, unified live/backtest architecture, and broad asset/venue ambitions.

LEAN remains the strongest mature secondary engine, particularly for traditional markets and validation.

vn.py remains highly relevant for broker connectivity and traditional-market ideas, especially in Asian markets.

Qlib remains one of the strongest open-source ML research frameworks but should not be treated as an execution platform.

---

# 2. Why a Modular Architecture Wins

There are effectively five different engineering problems hiding underneath the term "trading platform":

1. Deterministic strategy execution
2. Exchange/broker connectivity and execution
3. Market-data ingestion
4. Simulation/research
5. Control-plane/risk/operations/UI

No project is best at all five.

NautilusTrader is closest, but Hummingbot has much stronger crypto-market-making ecosystem breadth; hftbacktest models queue/latency behavior far more deeply; LEAN has exceptionally mature traditional-asset/broker infrastructure; Qlib is far stronger as an ML research framework; and web terminal projects provide far more dashboard functionality than Nautilus itself.

The correct MRC philosophy is:

> **MRC owns the interfaces and state. Engines are replaceable workers.**

That allows MRC to upgrade, remove, or replace NautilusTrader, Hummingbot, LEAN or another engine without rewriting the dashboard or business layer.

---

# 3. Serious Engine Comparison

Scores below are architectural assessments rather than mechanically calculated GitHub-popularity rankings.

Legend:

- **A** — Architecture
- **CQ** — Code quality
- **Mat** — Maturity
- **Maint** — Maintenance
- **Perf** — Performance
- **BT** — Backtesting
- **MD** — Market data
- **C** — Crypto
- **T** — Traditional markets
- **Ext** — Extensibility
- **Lic** — Licensing suitability

| Project | A | CQ | Mat | Maint | Perf | Live | BT | Risk | OMS | MD | C | T | Ext | API | UI | Docs | Lic | MRC |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **NautilusTrader** | 10 | 9 | 8 | 10 | 10 | 9 | 9 | 8 | 9 | 9 | 9 | 9 | 10 | 9 | 2 | 9 | 7 | **10** |
| **LEAN** | 9 | 9 | 10 | 10 | 7 | 9 | 9 | 7 | 8 | 9 | 7 | 10 | 9 | 8 | 4 | 10 | 10 | **9** |
| **Hummingbot** | 8 | 8 | 9 | 9 | 8 | 10 | 6 | 6 | 8 | 9 | 10 | 1 | 9 | 9 | 7 | 9 | 10 | **9 crypto** |
| **vn.py** | 8 | 8 | 10 | 9 | 6 | 9 | 8 | 7 | 8 | 9 | 7 | 10 | 9 | 7 | 7 | 8 | 10 | 8 |
| **Barter** | 9 | 8 | 6 | 8 | 9 | 8 | 8 | 6 | 7 | 8 | 9 | 3 | 9 | 7 | 1 | 7 | 10 | 8 |
| **Jesse** | 8 | 8 | 8 | 8 | 7 | 8 | 8 | 6 | 7 | 6 | 9 | 1 | 9 | 8 | 8 | 8 | 10 | 8 |
| **hftbacktest** | 9 | 9 | 7 | 8 | 10 | 5 | 10 | 4 | 5 | 10 | 9 | 3 | 8 | 6 | 1 | 8 | 10 | **9 specialist** |
| **Tesser** | 9 | 8 | 3 | 8 | 9 | 7 | 8 | 6 | 6 | 7 | 8 | 2 | 9 | 6 | 2 | 7 | 10 | 7 |
| **StockSharp** | 9 | 8 | 10 | 8 | 8 | 9 | 9 | 7 | 9 | 10 | 9 | 10 | 8 | 6 | 9 | 8 | 3 | 6 |
| **OpenAlgo** | 8 | 8 | 6 | 9 | 5 | 8 | 6 | 6 | 8 | 7 | 3 | 8 | 8 | 9 | 8 | 8 | 2 | 6 |
| **Lumibot** | 7 | 8 | 7 | 9 | 5 | 9 | 7 | 6 | 6 | 7 | 7 | 9 | 8 | 8 | 4 | 8 | 1 | 6 |
| **Freqtrade** | 8 | 8 | 9 | 10 | 6 | 9 | 8 | 7 | 6 | 7 | 10 | 0 | 9 | 9 | 8 | 9 | 4 | 6 |
| **OctoBot** | 7 | 7 | 8 | 8 | 6 | 8 | 7 | 6 | 6 | 7 | 9 | 0 | 8 | 7 | 8 | 7 | 4 | 5 |
| **Qlib** | 8 | 9 | 9 | 7 | 6 | 2 | 8 | 6 | 2 | 8 | 3 | 8 | 9 | 6 | 2 | 9 | 10 | 7 |
| **Qubx** | 8 | 7 | 4 | 7 | 7 | 7 | 8 | 5 | 5 | 6 | 8 | 3 | 8 | 7 | 2 | 7 | 4 | 5 |
| **OpenTrade/OEMS** | 8 | 7 | 7 | 4 | 8 | 8 | 4 | 6 | 9 | 6 | 5 | 8 | 7 | 6 | 2 | 5 | 10 | 6 |

Nautilus therefore wins **MRC core-engine fit**, not every individual category.

Tesser is worth monitoring closely because its Rust workspace separates core types, broker traits, execution, events, strategy, portfolio, indicators and backtesting. Architecturally it is close to the interface-oriented direction MRC should use, but it is still too young to replace NautilusTrader.

---

# 4. NautilusTrader — Primary Recommendation

Use it for:

- strategy runtime
- order-state machinery
- execution adapters
- live/paper parity
- portfolio calculation inside an engine instance
- general event/tick backtesting
- high-frequency data types
- critical exchange/broker adapters

Its Rust core/Python control surface fits MRC's proposed Python/FastAPI + Rust architecture unusually well.

But do **not** make MRC's public API use Nautilus-specific objects.

Use an adapter:

```text
MRC ExecutionProvider
        ↓
NautilusExecutionAdapter
        ↓
NautilusTrader
```

The LGPL-3.0 license is workable for proprietary systems, but it needs deliberate separation and compliance.

**Decision: WRAP. Do not fork unless absolutely necessary.**

---

# 5. QuantConnect LEAN

LEAN is the strongest secondary engine for MRC.

Reasons:

- decade-plus project maturity
- C#/Python
- strong multi-asset support
- stocks/options/futures/FX/crypto
- highly modular brokerage/data-provider architecture
- unified research/backtest/live model
- Apache-2.0 licensing
- large active ecosystem

The weakness is architectural mismatch: introducing the CLR/C# runtime as MRC's primary engine would complicate a Python/Rust system.

Therefore:

**Do not base all MRC on LEAN.**

Instead:

```text
MRC BacktestProvider
        ↓
LeanBacktestService

MRC ExecutionProvider
        ↓
LeanBrokerService
```

This is especially useful for validating a strategy independently against Nautilus and accessing brokers/datasets where LEAN's adapters are better.

**Decision: RUN AS SEPARATE SERVICE.**

---

# 6. Hummingbot

Hummingbot is more strategically important than Freqtrade for MRC.

Its platform covers CEXs and DEXs and is aimed at automated/high-frequency crypto strategies.

The newer **Hummingbot API** exposes a REST control plane for bots, balances, orders and connectors and includes Docker-oriented orchestration.

MRC should **not merge Hummingbot's internal bot architecture into MRC**.

Run it like this:

```text
MRC
 ↓
HummingbotProvider
 ↓ REST
Hummingbot API
 ↓
Hummingbot containers
 ↓
CEX / DEX
```

This gives MRC crypto market-making and DEX capability without making MRC dependent on Hummingbot internals.

**Decision: RUN AS SEPARATE SERVICE.**

---

# 7. Market-Data Architecture

Use three connector tiers.

## Tier 1 — Critical production venues

Use **native Nautilus adapters** or MRC-written native adapters.

These should handle:

- sequence IDs
- reconnect/recovery
- incremental books
- order acknowledgements
- exact venue semantics
- execution reports

## Tier 2 — Broad crypto real-time coverage

Use **cryptofeed**.

Useful for:

- books
- trades
- tickers
- exchange-normalized feeds
- high-rate WebSocket market data

## Tier 3 — Long-tail connector coverage

Use **CCXT**.

CCXT provides very broad crypto exchange support and common interfaces.

Do **not** use CCXT as the sole hot-path execution implementation for high-value venues.

Broad cross-exchange abstraction and exchange-specific low-latency fidelity solve different problems.

---

# 8. OMS / EMS / FIX

## OMS

Use the Nautilus order model and state machine **inside Nautilus**, but MRC must define its own canonical state machine externally.

Suggested model:

```text
CREATED
→ VALIDATED
→ RISK_ACCEPTED
→ SUBMITTED
→ ACKNOWLEDGED
→ PARTIALLY_FILLED
→ FILLED

Alternative paths:
REJECTED
CANCEL_PENDING
CANCELLED
REPLACE_PENDING
EXPIRED
UNKNOWN
RECONCILING
```

**UNKNOWN** and **RECONCILING** are particularly important.

## EMS / Smart Routing

Build a thin MRC execution-policy layer.

It should decide:

- venue
- order type
- passive/aggressive
- slice size
- participation
- cancel/replace behavior
- maximum slippage
- retry policy

Then delegate actual order transport.

## FIX

For institutional FIX connectivity, prototype **Artio** first.

Alternatives:

- Fix8
- QuickFIX
- OpenTrade/OEMS

**Decision: RUN FIX gateway as a separate service.**

---

# 9. Risk — Build This in MRC

This is one of the important exceptions to the "reuse before build" rule.

Existing trading frameworks generally know:

```text
strategy → orders → positions
```

MRC needs:

```text
all engines
+ all exchanges
+ all accounts
+ all strategies
+ portfolio correlations
+ stale-data state
+ infrastructure state
+ exchange health
+ liquidation distance
+ aggregate leverage
→ one authoritative trading permission
```

Therefore:

**BUILD MRC Global Risk Service.**

It should support at least:

```text
GLOBAL
ACCOUNT
VENUE
STRATEGY
SYMBOL
ASSET
POSITION
ORDER
```

limits.

And global system states:

```text
NORMAL
WARNING
REDUCE_ONLY
CLOSE_ONLY
HALTED
EMERGENCY_FLATTEN
RECONCILING
```

This service must sit **before execution adapters**, not inside the dashboard.

---

# 10. Backtesting Realism Comparison

| Engine | Event | Tick | L2/L3 | Latency | Queue | Partial fills | Fees | Funding | Liquidation | Replay |
|---|---|---|---|---|---|---|---|---|---|---|
| **hftbacktest** | ✅ | ✅ | **✅✅** | **✅✅** | **✅✅** | ✅ | ✅ | modelable | modelable | **✅✅** |
| **NautilusTrader** | **✅✅** | **✅✅** | ✅ | ✅ | partial/model | ✅ | ✅ | ✅ adapter/model | modelable | **✅✅** |
| **LEAN** | **✅✅** | ✅ | limited vs HFT | models | limited | ✅ | ✅ | asset dependent | asset dependent | ✅ |
| **Jesse** | ✅ | candle/trade oriented | ❌ | ❌ | ❌ | ✅ | ✅ | crypto aware | some | ✅ |
| **Freqtrade** | candle | limited | ❌ | ❌ | ❌ | models | ✅ | futures aware | limited | deterministic |
| **vn.py** | ✅ | ✅ | connector dependent | limited | limited | ✅ | ✅ | connector dependent | limited | ✅ |
| **Tesser** | ✅ | evolving | evolving | evolving | evolving | evolving | evolving | evolving | evolving | ✅ design goal |

Recommended:

```text
Normal / swing / day / medium-frequency
        → Nautilus BacktestProvider

HFT / market making / queue-sensitive
        → hftbacktest HftSimulationProvider

Cross-check / traditional markets
        → LEAN ValidationProvider
```

---

# 11. AI / ML

## Qlib

Use it for:

- alpha/feature research
- supervised ML experiments
- factor modeling
- research pipelines
- market/regime models

## MLflow

Use MLflow for:

- experiment tracking
- model versions
- artifact tracking
- registry
- evaluation
- deployment metadata

## MRC AI Decision Ledger

This should be MRC-owned.

Each AI decision should persist:

```text
decision_id
timestamp
strategy_id
model_id
model_version
feature_snapshot_id
market_state_id
portfolio_state_id
risk_state_id

raw_prediction
confidence
regime
explanation

proposed_action
risk_adjusted_action
final_action

human_override
execution_result
post_trade_result
```

Lumibot contains interesting AI/agent trading and decision-trace ideas, but should remain reference-only until licensing is fully clarified.

---

# 12. Charting Investigation

## MG Exchange Chart

MG Exchange Chart deserves an MRC prototype immediately.

Its feature set includes:

- Canvas2D + optional WebGL
- multi-chart grids
- drawing tools
- indicators
- CVD
- volume profile
- order lines
- liquidation/breakeven lines
- draggable orders
- TP/SL position overlays
- real-time tick/bar updates
- mobile interactions
- drawing persistence
- custom indicators
- trade-request and order-line events

Its biggest problem is its youth.

**Decision: PROTOTYPE immediately — do not commit production architecture yet.**

## TradingView Lightweight Charts

Still the safer foundation.

Advantages:

- mature
- compact
- fast
- TypeScript-friendly
- large ecosystem

Disadvantage:

MRC would need to implement significantly more TradingView-style trading functionality itself.

## KLineChart

A strong Apache-2.0 trading-specific alternative.

Recommended chart strategy:

```text
MRC ChartProvider
    ├── MG Exchange Chart
    ├── Lightweight Charts
    └── KLineChart
```

Prototype all three behind the same MRC interface.

---

# 13. Dashboard Research

OpenCharts is a valuable architectural reference because its frontend is isolated from its backend behind REST-style and streaming service modules.

The MRC UI should follow:

```text
React components
       ↓
frontend domain store
       ↓
MRC API SDK
       ↓
REST / WebSocket
```

Never:

```text
React component
       ↓
Nautilus / Hummingbot / LEAN-specific API
```

OpenTerminalUI is also useful as a page/UX reference because of the breadth of its terminal structure.

---

# 14. MRC Dashboard Feature-Source Matrix

| MRC page/widget | Best OSS source/reference |
|---|---|
| **Command Center** | OpenTerminalUI + MRC custom |
| Trading Chart | **MG Exchange Chart / Lightweight Charts** |
| Drawings | **MG Exchange Chart** |
| Position/SL/TP overlays | **MG Exchange Chart** |
| Watchlist | OpenCharts / OpenTerminalUI |
| Positions | OpenCharts + Hummingbot Dashboard |
| Orders | OpenCharts / OpenAlgo |
| Trade History | OpenCharts |
| DOM | **VisualHFT / OpenCharts** |
| Time & Sales | VisualHFT / OpenTerminalUI |
| Bot Manager | **Hummingbot Dashboard/API** |
| Strategy Manager | Jesse / Freqtrade concepts |
| Signals | MRC custom |
| AI Decisions | **MRC custom; Lumibot concepts** |
| Risk Dashboard | **MRC custom** |
| Exposure | MRC custom |
| Performance | pyfolio-style analytics + MRC UI |
| Backtesting | MRC + Nautilus |
| HFT Backtesting | hftbacktest |
| Optimization | Jesse patterns / Optuna |
| Screener | OpenTerminalUI/OpenAlgo patterns |
| Order Flow | **VisualHFT** |
| CVD | MG Exchange Chart |
| Liquidations | MRC market-data service |
| Whale Activity | MRC crypto intelligence |
| Funding | MRC crypto data |
| Open Interest | MRC crypto data |
| Market Regime | Qlib/MRC AI |
| Alerts | MRC notification service |
| Logs | MRC/OpenTelemetry |
| VPS | Prometheus/MRC |
| Broker Status | MRC |
| Exchange Status | MRC |
| Latency | MRC/Prometheus |
| System Health | Prometheus/OpenTelemetry |

---

# 15. Licensing Matrix

> **Important:** This is not legal advice. Before commercial distribution, MRC should have OSS counsel review the exact composition, linking model, container boundaries, network exposure, distribution model, and modified-source obligations.

| Project | Current license | Proprietary MRC assessment |
|---|---|---|
| LEAN | Apache-2.0 | 🟢 Excellent |
| Hummingbot | Apache-2.0 | 🟢 Excellent |
| Hummingbot API | MIT | 🟢 Excellent |
| vn.py | MIT | 🟢 Excellent |
| Jesse | MIT | 🟢 Excellent |
| Barter | MIT | 🟢 Excellent |
| Qlib | MIT | 🟢 Excellent |
| hftbacktest | MIT | 🟢 Excellent |
| Tesser | MIT + Apache-2.0 | 🟢 Excellent |
| OpenTrade | Apache-2.0 | 🟢 Excellent |
| CCXT | MIT | 🟢 Excellent |
| cryptofeed | permissive | 🟢 Good |
| Artio | Apache-2.0 | 🟢 Excellent |
| Lightweight Charts | Apache-2.0 + attribution | 🟢 Good |
| KLineChart | Apache-2.0 | 🟢 Excellent |
| MG Exchange Chart | Apache-2.0 | 🟢 Excellent |
| OpenCharts | MIT | 🟢 Excellent |
| OpenTerminalUI | MIT | 🟢 Excellent |
| NautilusTrader | LGPL-3.0 | 🟡 Manageable |
| Fix8 | LGPL-3.0 | 🟡 Manageable |
| Freqtrade | GPL-3.0 | 🟠 Avoid embedding |
| OctoBot | GPL family | 🟠 Avoid core integration |
| Qubx | GPL-3.0 | 🟠 Avoid embedding |
| OpenAlgo | AGPL-3.0 | 🔴 Strong proprietary concern |
| Grafana | AGPL-3.0 current | 🟠 Keep isolated/review |
| StockSharp | current/custom/Other | 🔴 Legal review |
| Lumibot | conflicting MIT/GPL signals | 🔴 Block pending clarification |
| QuickFIX | custom QuickFIX license | 🟡/🔴 Review |
| vectorbt | Apache + Commons Clause components | 🔴 Productization issue |
| TimescaleDB | mixed Apache/Timescale License | 🟠 Boundary review |

General response:

```text
permissive dependency
      → normal integration

LGPL component
      → clean library/process boundary

GPL component
      → preferably separate service
         + legal review

AGPL component
      → do not build proprietary MRC around it
         without explicit legal review

custom / conflicting license
      → blocked until reviewed
```

---

# 16. MRC Subsystem Decision Matrix

| MRC subsystem | Decision | Foundation |
|---|---|---|
| **Market Data** | **WRAP** | Nautilus + cryptofeed |
| Exchange Connectors | **WRAP** | Native Nautilus + CCXT fallback |
| DEX Connectors | **SERVICE** | Hummingbot |
| Broker Connectors | **WRAP/SERVICE** | Nautilus + LEAN; vn.py reference |
| OMS | **WRAP + MRC FACADE** | Nautilus |
| EMS | **BUILD thin layer** | MRC + execution adapters |
| Smart Router | **BUILD** | MRC |
| FIX | **SERVICE** | Artio |
| Portfolio local | **WRAP** | Nautilus |
| Portfolio global | **BUILD** | MRC |
| Accounting | **BUILD** | MRC ledger |
| Reconciliation | **BUILD** | MRC |
| Pre-trade Risk | **BUILD** | MRC |
| Portfolio Risk | **BUILD** | MRC |
| Kill Switch | **BUILD** | MRC |
| Strategy Runtime | **USE/WRAP** | Nautilus |
| Crypto MM runtime | **SERVICE** | Hummingbot |
| General Backtester | **USE** | Nautilus |
| Secondary Validator | **SERVICE** | LEAN |
| HFT Simulator | **USE/SERVICE** | hftbacktest |
| Optimizer | **ADAPT** | Optuna/Ray patterns |
| Paper Trading | **USE/WRAP** | Nautilus |
| ML Research | **USE** | Qlib |
| Model Registry | **USE** | MLflow |
| AI Decision Ledger | **BUILD** | MRC |
| Indicators | **USE** | Existing libraries/Jesse Rust/etc. |
| Charting | **USE/ADAPT** | MG / Lightweight / KLine |
| Dashboard | **BUILD** | React/Next |
| Bot Orchestration | **BUILD thin layer** | Docker → K8s |
| Alerts | **BUILD thin layer** | Notification adapters |
| Logging | **USE** | OpenTelemetry |
| Audit Trail | **BUILD** | MRC event ledger |
| Operational metrics | **USE** | Prometheus |
| Database OLTP | **USE** | PostgreSQL |
| Tick/analytics DB | **USE** | ClickHouse |
| Cache/state projection | **USE** | Redis |
| VPS Monitoring | **USE** | Prometheus |
| Authentication | **USE** | Keycloak |
| API Gateway/BFF | **BUILD** | FastAPI |
| Event Bus | **USE** | NATS JetStream |

---

# 17. Proposed MRC Architecture

```text
┌───────────────────────────────────────────────────────────┐
│                     MRC BRIDGE UI                         │
│               React / Next.js / TypeScript                │
│                                                           │
│ Command Center │ Charts │ Bots │ Risk │ Backtests │ VPS  │
└────────────────────────────┬──────────────────────────────┘
                             │
                     REST + WebSocket
                             │
┌────────────────────────────▼──────────────────────────────┐
│                   MRC API / BFF                          │
│                       FastAPI                            │
│                                                         │
│ Authentication │ RBAC │ API versioning │ WS sessions   │
└────────────────────────────┬──────────────────────────────┘
                             │
            Commands         │         Queries
                  ┌──────────┴──────────┐
                  ▼                     ▼
         ┌────────────────┐    ┌──────────────────┐
         │ MRC Command Bus│    │ MRC State Layer  │
         │ NATS JetStream │    │ Redis/Postgres   │
         └───────┬────────┘    └────────┬─────────┘
                 │                       ▲
                 │ events                │ projections
                 ▼                       │
┌──────────────────────────────────────────────────────────┐
│                    MRC SERVICES                          │
│                                                          │
│ Market Data │ Risk │ Portfolio │ Reconciliation         │
│ Accounting  │ Alerts │ AI │ Bot Orchestrator            │
│ Backtest Manager │ Audit │ Infrastructure Monitor       │
└───┬───────────────┬───────────────┬──────────────────────┘
    │               │               │
    ▼               ▼               ▼
┌──────────┐ ┌─────────────┐ ┌────────────────┐
│ Nautilus │ │ Hummingbot  │ │ hftbacktest    │
│ Engines  │ │ instances   │ │ workers        │
└────┬─────┘ └──────┬──────┘ └────────────────┘
     │              │
     ├──────────────┼──────────────┐
     ▼              ▼              ▼
 Exchanges        DEXs          Brokers/FIX
                                  │
                              ┌───▼───┐
                              │ Artio │
                              └───────┘

Research side:
Qlib → MLflow → MRC Model Gateway → Strategy Runtime

Historical/event storage:
Postgres │ ClickHouse │ Object Storage

Observability:
OpenTelemetry → Prometheus → MRC System Health
```

---

# 18. Interfaces MRC Should Define Immediately

The public contracts matter more than selecting a specific engine.

```python
class MarketDataProvider:
    subscribe(...)
    unsubscribe(...)
    snapshot(...)
    historical(...)
    health(...)

class ExecutionProvider:
    submit_order(...)
    cancel_order(...)
    replace_order(...)
    open_orders(...)
    reconcile(...)

class PortfolioProvider:
    positions(...)
    balances(...)
    exposures(...)
    pnl(...)

class RiskProvider:
    validate_order(...)
    current_state(...)
    limits(...)
    halt(...)
    flatten(...)

class BacktestProvider:
    run(...)
    cancel(...)
    results(...)

class StrategyRuntime:
    deploy(...)
    start(...)
    pause(...)
    stop(...)
    state(...)

class BotRuntime:
    create(...)
    start(...)
    stop(...)
    logs(...)
    health(...)

class ChartProvider:
    history(...)
    subscribe(...)
    drawings(...)
    overlays(...)
```

Implementations then become:

```text
NautilusExecutionProvider
HummingbotExecutionProvider
LeanExecutionProvider

NautilusBacktestProvider
LeanBacktestProvider
HftBacktestProvider
```

They are implementations, not MRC's architecture.

---

# 19. Event Sourcing, CQRS and Recovery

MRC should adopt **selective event sourcing**, not turn the entire platform into an academic event-sourcing exercise.

Persist immutable events for:

```text
OrderRequested
RiskAccepted
RiskRejected
OrderSubmitted
OrderAcknowledged
OrderRejected
OrderPartiallyFilled
OrderFilled
OrderCancelRequested
OrderCancelled

BalanceObserved
PositionObserved
ReconciliationStarted
ReconciliationCompleted

RiskStateChanged
KillSwitchActivated

StrategyStarted
StrategyStopped
StrategyCrashed

ExchangeDisconnected
ExchangeRecovered
```

Then derive:

```text
positions
orders
balances
P&L
exposure
dashboard state
```

as projections.

This gives MRC:

- deterministic reconstruction
- incident investigation
- AI decision auditing
- crash recovery
- reconciliation
- replay
- reliable dashboard history

---

# 20. Exchange Disconnect and Crash Recovery

This should be treated as a first-class trading feature.

After process restart or connection loss:

```text
1. disable new risk-taking
2. reconnect authenticated sessions
3. fetch balances
4. fetch positions
5. fetch open orders
6. fetch recent fills
7. compare remote state to MRC state
8. classify differences
9. rebuild canonical state
10. emit reconciliation events
11. reopen execution only when safe
```

Never assume:

```text
HTTP timeout = order failed
```

It may mean:

```text
order succeeded
+
acknowledgement was lost
```

This distinction is one of the most important differences between professional execution infrastructure and ordinary trading bots.

---

# 21. Hot Path Versus Cold Path

Do **not** route latency-sensitive execution through excessive microservices.

## Hot path

```text
Market event
  ↓
Strategy
  ↓
local/precomputed risk
  ↓
Execution adapter
  ↓
Exchange
```

## Asynchronous path

```text
event
 ↓
NATS
 ├─ audit
 ├─ ClickHouse
 ├─ dashboard
 ├─ analytics
 ├─ AI logging
 ├─ alerts
 └─ monitoring
```

For genuinely low-latency/HFT workloads, MRC can colocate:

```text
strategy + risk guard + execution
```

inside the same Rust/Nautilus worker.

---

# 22. Strategy / Process Isolation

Each live bot should have:

```text
strategy_id
deployment_id
code_version
config_version
container_image
engine_version
account
permissions
resource_limits
risk_limits
```

Recommended initial model:

```text
MRC Orchestrator
        ↓
Docker container
        ↓
one strategy/runtime unit
```

Later:

```text
Kubernetes
→ namespaces
→ deployments/jobs
→ resource quotas
→ secrets
→ affinity
→ rolling deployment controls
```

---

# 23. High Availability

Execution should generally be **active/passive**, not two active replicas blindly sending orders.

Recommended:

```text
Execution Actor A = active
Execution Actor B = warm standby

distributed lease
+
fencing token
+
single authoritative owner
```

Failover:

```text
lease expires
→ standby takes ownership
→ reconcile exchange
→ verify open orders/positions
→ resume
```

The primary goal is not instantaneous failover.

The primary goal is:

> **Never send duplicate orders.**

---

# 24. Storage

## PostgreSQL

Use for:

- users
- configuration
- strategies
- deployments
- accounts
- permissions
- canonical order metadata
- portfolio snapshots
- risk configuration
- model metadata

## Redis

Use for:

- ephemeral projections
- session state
- latest market state
- cached dashboards
- distributed leases/rate limits

**Do not make Redis the authoritative trading ledger.**

## ClickHouse

Use for:

- tick data
- trades
- book snapshots/deltas
- latency series
- execution analytics
- backtest results
- massive event-analysis queries

---

# 25. Projects to Reject as MRC's Core

## Freqtrade

Excellent crypto bot and strategy research ecosystem.

But:

**GPL + crypto-only orientation + bot-centric architecture → not the MRC foundation.**

Reference its UX and strategy-management ideas instead.

## OctoBot

Useful crypto bot/plugin ecosystem, but GPL-family licensing and less suitable institutional architecture.

## OpenAlgo

Interesting broker/API/UI project.

But:

**AGPL makes it a poor proprietary MRC dependency without deliberate legal planning.**

## Superalgos

Good visual/workflow ideas, but its current development trajectory is less attractive than modern alternatives.

## StockSharp

Feature breadth is extraordinary.

Do not build commercial MRC around it until its current licensing has been professionally reviewed.

## Lumibot

Interesting strategy/live/backtest and AI-agent ideas.

**License inconsistency disqualifies immediate integration.**

## vectorbt

Very useful research technology.

Commons-Clause restrictions make embedding/productization less attractive.

---

# 26. Projects Worth Prototyping Immediately

Run eight technical spikes before freezing architecture.

## POC A — NautilusTrader core

Build:

```text
Binance/Bybit
→ market data
→ sample strategy
→ risk
→ order
→ fill
→ MRC WebSocket
→ React dashboard
```

Test restart and reconciliation.

## POC B — MG Exchange Chart

Implement:

- 500k+ bars
- real-time updates
- four-chart layout
- 10 indicators
- 30 drawings
- position overlays
- draggable orders
- SL/TP
- backtest markers

Compare against Lightweight Charts and KLineChart.

## POC C — hftbacktest

Replay real Binance/Bybit L2 data with:

- artificial latency
- limit-order queue
- partial fills
- maker strategy

## POC D — Hummingbot

MRC launches and manages multiple Hummingbot containers through an adapter.

## POC E — Event ledger

```text
OrderRequested
RiskAccepted
Submitted
Ack
PartialFill
Fill
```

Flow into NATS and Postgres/ClickHouse projections.

## POC F — Crash recovery

Kill execution service with a live paper/open order.

Restart.

MRC must recover without duplicate orders.

## POC G — Global risk

Two Nautilus strategies + one Hummingbot bot:

```text
total BTC exposure > limit
```

must trigger a **global** restriction regardless of engine.

## POC H — AI decision trace

```text
feature snapshot
→ prediction
→ decision
→ risk decision
→ order
→ fill
```

all traceable by one `decision_id`.

---

# 27. Recommended Technology Stack

```text
FRONTEND
React
Next.js
TypeScript

CHARTING
POC: MG Exchange Chart
Fallback/base: Lightweight Charts
Alternative: KLineChart

API / CONTROL
Python
FastAPI
Pydantic

TRADING HOT PATH
NautilusTrader
Rust where MRC-specific low latency is required

CRYPTO SPECIALIST
Hummingbot
CCXT
cryptofeed

BACKTESTING
NautilusTrader
hftbacktest
LEAN validation service

ML / AI
Qlib
PyTorch/scikit ecosystem
MLflow
MRC AI Decision Ledger

EVENTING
NATS JetStream

DATABASE
PostgreSQL
ClickHouse
Redis

OBSERVABILITY
OpenTelemetry
Prometheus
MRC operational UI

AUTH
Keycloak

DEPLOYMENT
Linux
Docker
Docker Compose initially
Kubernetes later
```

---

# 28. Development Priorities

## Phase 1 — Architecture contracts

Before dashboard expansion:

1. canonical Instrument
2. canonical MarketEvent
3. canonical Order
4. canonical Fill
5. canonical Position
6. provider interfaces
7. event envelopes
8. IDs/idempotency
9. execution state machine
10. risk-state model

## Phase 2 — Trading spine

```text
market data
→ strategy
→ risk
→ OMS
→ adapter
→ exchange
→ reconciliation
→ audit
```

## Phase 3 — Operational control plane

```text
bots
strategies
accounts
deployment
logs
metrics
health
alerts
```

## Phase 4 — Professional dashboard

Build the full interface on top of **stable MRC APIs**.

## Phase 5 — HFT / AI

Only once execution/state/recovery are trustworthy:

```text
hftbacktest
Qlib
AI decision system
advanced crypto analytics
order flow
```

---

# 29. What MRC Should Not Build From Scratch

There is no justification for MRC engineers to spend months recreating:

- a general event-driven trading engine
- a second general-purpose backtester
- HFT queue/latency simulation
- dozens of crypto exchange REST clients
- a FIX protocol parser/session engine
- authentication/IAM
- metrics scraping
- distributed telemetry
- a high-volume analytical database
- ML experiment/model tracking
- basic candlestick rendering

Mature components already exist.

Engineering effort should instead focus on MRC's real differentiation:

> **Cross-engine state, global risk, orchestration, reconciliation, professional UX, AI auditability and unified operations.**

---

# 30. Final Architecture Decision

If the architectural direction were frozen today, this should be the **MRC Bridge baseline**:

```text
                    MRC BRIDGE
                         │
              React / Next.js UI
                         │
                  MRC TypeScript SDK
                         │
             REST + WebSocket Gateway
                         │
                    FastAPI
                         │
       ┌─────────────────┴─────────────────┐
       │                                   │
 MRC Command/Event Layer             MRC Query/State
     NATS JetStream                  Redis/Postgres
       │                                   ▲
       │                                   │
 ┌─────┴───────────────────────────────────┴─────┐
 │               MRC CONTROL PLANE              │
 │                                              │
 │ Global Risk                                  │
 │ Global Portfolio                             │
 │ Accounting                                   │
 │ Reconciliation                               │
 │ Audit                                        │
 │ Bot Orchestration                            │
 │ Alerting                                     │
 │ AI Decision Ledger                           │
 └─────┬──────────────┬──────────────┬──────────┘
       │              │              │
       ▼              ▼              ▼
 NautilusTrader   Hummingbot      Backtest Pool
   PRIMARY          CRYPTO       ┌───────────────┐
   ENGINE          SPECIALIST    │ Nautilus      │
                                │ hftbacktest   │
                                │ LEAN          │
                                └───────────────┘
       │              │
       └───────┬──────┘
               │
   MRC ExecutionProvider
               │
     Exchange/Broker/FIX
               │
    Native / CCXT / Artio


MARKET DATA
Native adapters + cryptofeed + CCXT
               │
           ClickHouse


AI / RESEARCH
Qlib
 ↓
MLflow
 ↓
MRC Model Gateway
 ↓
Strategies


OBSERVABILITY
OpenTelemetry
 ↓
Prometheus
 ↓
MRC System Health


AUTH
Keycloak
```

---

# Final Recommendation

**Do not look for an "MRC Bridge open-source equivalent" to fork.**

Instead, build MRC Bridge as the **control plane above multiple engines**.

The strongest overall combination is:

> **NautilusTrader + Hummingbot + hftbacktest + LEAN + cryptofeed + CCXT + Qlib + MLflow + MG/Lightweight Charts + NATS + PostgreSQL + ClickHouse + Redis + OpenTelemetry + Prometheus + Keycloak.**

Of these, **NautilusTrader is the most important architectural dependency**, but MRC should deliberately make it replaceable.

**hftbacktest is the clearest example of functionality MRC should not rewrite.**

**Hummingbot should become a specialist crypto runtime rather than MRC's foundation.**

**MG Exchange Chart is one of the most interesting dashboard discoveries**, but because it is young it should be benchmarked before production selection.

The defensible MRC product is the layer none of these projects provides completely:

> **A unified professional trading operating system controlling multiple specialized engines through MRC-owned state, risk, APIs, auditability and UX.**
