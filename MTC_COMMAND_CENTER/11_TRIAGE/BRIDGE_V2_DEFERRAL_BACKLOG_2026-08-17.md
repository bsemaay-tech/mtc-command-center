# Bridge V2 Deferral Backlog — 2026-08-17

**Mode:** read-only reconstruction converted into a documentation-only report  
**Scope:** `IBKR_PAPER_BRIDGE` source/docs plus current 2026-08 memory and
triage records  
**Authority:** inventory and sequencing only; this report authorizes no code,
deployment, host contact, credential use, broker/exchange action, TESTNET,
MAINNET, ARM, order, or economic action

## 1. Evidence caveat

`IBKR_PAPER_BRIDGE/docs/30_V2_BACKEND_AND_DASHBOARD_DESIGN_DECISIONS.md`
currently has an unrelated uncommitted B8 hosting edit (89 inserted lines plus
cross-reference changes). Its A1–A11 sections remain useful source evidence,
but the working-copy B8 text must not be treated as committed or accepted
authority until its owning documentation workflow finishes.

The frozen V1 candidate must remain isolated. The current owner roadmap permits
eligible V2 work only in separate branches/worktrees under the normal audit
tiers (`MTC_COMMAND_CENTER/_AI_MEMORY/NEXT_STEPS.md:7-20,68-71`).

## 2. Classification meanings

- **Already implemented V1 baseline** — present source capability; not a V2
  backlog item.
- **Implemented but opt-in / not activated** — source exists, but operational
  migration, activation, deployment, or acceptance is still separate work.
- **Dormant scaffolding** — classes/config/UI may exist, but the running factory
  does not wire the capability.
- **Explicitly deferred** — named as post-V1 work by a binding/current Bridge
  record.
- **Missing / open** — required by the newer V2 direction but no accepted
  implementation exists.
- **Separate future gate** — real-money, exchange, remote-control, or other work
  that must not be treated as an ordinary V2 feature.

## 3. Evidence-backed backlog

| Capability | Classification | Evidence and current reality | Dependency / risk tier |
|---|---|---|---|
| Single-strategy V1 runtime | **Already implemented V1 baseline** | V1 is explicitly one strategy, symbol and timeframe (`IBKR_PAPER_BRIDGE/docs/30_V2_BACKEND_AND_DASHBOARD_DESIGN_DECISIONS.md:50-59`). Runtime constructs one `BridgeEngine`, fixed `KeltnerTrailEma8`, and one `RiskEngine` (`IBKR_PAPER_BRIDGE/bridge/app.py:158-174`); `bridge.yaml:11` names one strategy file. | Not a V2 task. The V1 build must remain untouched (`docs/30...md:420-449`). |
| Core safety/execution foundation | **Already implemented; retain** | Gate monitor, duplicate/stale guards, loss cooldown, strategy-package permissions, Telegram notifier code, native SL/TP and leverage cap are recorded as adopted (`IBKR_PAPER_BRIDGE/docs/01_ARCHITECTURE.md:747-751`). The broker protocol already separates exchange operations (`IBKR_PAPER_BRIDGE/bridge/broker/base.py:154-207`). | Reuse as the V2 substrate. Any behavior change is protected **T0**. |
| Full reconciliation and authoritative risk | **Implemented but opt-in; not operationally activated** | Full reconciliation is inactive on default schema v4 (`IBKR_PAPER_BRIDGE/docs/26_FULL_RECONCILIATION_CONTRACT.md:1-10`); authoritative risk is opt-in v6 and owner-gated (`docs/27_AUTHORITATIVE_RISK_SNAPSHOT_CONTRACT.md:1-17`); daily controls are opt-in v7 with no operational migration (`docs/28_FULL_TSP1007_RISK_CONTROLS.md:1-15,44-49`); exposure/leverage/liquidation is opt-in v8 (`docs/29_TSP1008_EXPOSURE_LEVERAGE_LIQUIDATION.md:1-19`). | Activation/migration is **T0**. First produce a **T2** activation/migration contract. Never fold it into frozen V1 during soak. |
| Partial-fill recovery | **Implemented offline but still recorded as proposed** | `IBKR_PAPER_BRIDGE/docs/25_PARTIAL_FILL_PROTECTION_CONTRACT.md:3-18` names the modules/tests and says implemented/self-QA'd, pending independent audit/owner acceptance, and not deployed. | Reconcile actual acceptance status before redoing work. Protected order/broker surface: **T0**. |
| Optional LLM gate | **Dormant/unwired scaffolding** | `LLMGate` exists (`IBKR_PAPER_BRIDGE/bridge/engine/llm_gate.py:29-123`), but runtime supplies no gate; `BridgeEngine` therefore falls back to `NullLLMGate` (`bridge/engine/engine.py:62,114`). Config switches are OFF (`config/bridge.yaml:39-50`). The current truth correction is recorded at `MTC_COMMAND_CENTER/_AI_MEMORY/NEXT_STEPS.md:83-92`. | Provider credentials, persistence, activation and trading veto are **T0**. A read-only analysis-package generator is separable **T1**. |
| Multi-strategy workers | **Explicitly deferred / missing** | Preferred V2 is isolated workers under one VPS/release (`docs/30...md:131-164`); actual runtime remains one engine/Keltner (`bridge/app.py:158-174`). Worker boundary is open (`docs/30...md:892-899`). | Architecture contract **T2**; cross-cutting protected implementation **T0**. |
| Subaccounts and same-symbol isolation | **Explicitly deferred / open** | Preferred model is one risk bucket/subaccount/API wallet, but eligibility and fallback need reverification (`docs/30...md:166-201`). Same-symbol concurrency remains closed pending verified exchange mechanics and subaccount or virtual-book proof (`docs/30...md:203-254`). | Official-document verification is read-only **T2**; account, wallet, exchange and broker work is **T0**. |
| Portfolio Guardian | **Explicitly deferred / missing** | Guardian-above-workers is the preferred design (`docs/30...md:256-291`). Current `RiskEngine` has single-runtime exposure thresholds (`bridge/app.py:149-154`), but no multi-worker Guardian exists. | Threshold and veto contract **T2**; risk implementation **T0**. |
| Worker identity and storage separation | **Explicitly deferred / missing** | Per-worker P&L, state, order identity, version, symbol and timeframe are required; per-worker SQLite versus central Postgres remains open (`docs/30...md:293-326,892-905`). Postgres/Redis/Docker was explicitly deferred (`docs/01_ARCHITECTURE.md:761`), and current direct dependencies contain none (`requirements.in:26-35`). | Persistence and cross-cutting architecture are **T0**. Decide isolation/tenancy before code. |
| MTC sizing ownership and `OrderIntent` | **Blocking future-integration gap** | Current Bridge `Signal` has no quantity while `OrderPlan` has one Bridge-originated quantity (`bridge/engine/types.py:27-47`). MTC and Bridge are not connected (`docs/30...md:589-599`). Pine/Python multiplier and minimum-notional parity gaps plus the intent schema remain open (`docs/30...md:488-517,644-733`). | Contract/parity design **T2**; MTC/Pine/risk/order implementation **T0** and separately owner-gated. Must precede even the first MTC-connected worker (`docs/30...md:376-407`). |
| MTC exit lifecycle, Multi-TP and basket/add support | **Blocking missing capability** | Bridge supports one optional full-quantity TP and cannot express MTC fractional TP1/TP2 or basket/add semantics (`docs/30...md:799-806`). Required lifecycle-contract fields are at `docs/30...md:860-886`. | Contract **T2** first; order/broker/risk implementation **T0**. |
| Manual Execution Ticket | **Explicitly deferred / missing** | `IBKR_PAPER_BRIDGE/docs/01_ARCHITECTURE.md:755`; V1 supports only cancel/flatten manual actions. | Economic/order control: **T0**. Not a safe UI-only package. |
| Real-data shadow/ghost mode | **Explicitly deferred / missing** | `IBKR_PAPER_BRIDGE/docs/01_ARCHITECTURE.md:756`; also the legacy audit roadmap at `docs/05_AUDIT_RESOLUTION.md:47-52`. | Fixture/local-feed MockBroker prototype **T1**; live Hyperliquid feed attachment **T0**. |
| Deterministic macro/funding entry gate | **Explicitly deferred; partial concept only** | Architecture says a deterministic event/funding gate is preferable and only partly approximated by LLM `NO_TRADE` (`docs/01_ARCHITECTURE.md:757`). Funding evidence storage/reconciliation exists, but that is accounting truth, not an extreme-funding pre-trade gate. | Policy specification **T2**; trading veto implementation **T0**. |
| Market Context page | **Explicitly deferred / missing** | Movers, funding, OI and sentiment were deferred to V2 and must remain context-only (`docs/01_ARCHITECTURE.md:758`). | Read-only UI/data adapter **T1**. Any order-trigger use escalates to **T0**. |
| Additional venue/market/timeframe scope | **Separate future gates** | Binance is deferred to V2 (`docs/01_ARCHITECTURE.md:759`). V1 excludes spot, extra exchanges, leverage above 1 and sub-hour timeframes (`docs/00_PREREG.md:105-108`). Runtime chooses Mock or Hyperliquid testnet and fixed BTC/1x (`bridge/app.py:191-208`). | Broker/exchange/economic surfaces **T0**. MAINNET remains a separate real-money gate, not an ordinary V2 item. |
| Dashboard V2 aggregate/drill-down | **V1 foundation exists; V2 missing** | Current V1 has six pages and controls (`bridge/static/index.html:12-18,21-106`). V2 calls for one aggregate execution dashboard with per-strategy drill-down (`docs/30...md:911-942`) and worker health, freshness, block reasons and account labels (`docs/30...md:975-1037`). | Read-only mock/fixture UI **T1**. Worker control/API integration **T0**. |
| Frozen-package preparation workflow | **Direction recorded; activation design missing** | Only approved packages may be prepared, and preparation must never ARM (`docs/30...md:944-973`). No package-selection/staging workflow exists in the current six-page UI. | Read-only selector/proposal UI **T1**; backend activation/control path **T0**. |
| Login, 2FA, roles, phone/remote access | **Explicitly deferred / missing** | Required before non-localhost exposure (`docs/01_ARCHITECTURE.md:763-764`). V1 binds loopback and has no application identity layer (`bridge/app.py:98-103,234`). Mobile UI is outside V1 (`docs/00_PREREG.md:107-108`). | Security, host and remote-control architecture **T0**. Read-only topology specification may proceed as **T2**; no exposure should occur. |
| Dashboard AI assistance | **Direction only; package generator missing** | Initial route is a manually supplied read-only package to the owner's Codex subscription; embedded chat is deferred (`docs/30...md:1141-1154,1192-1216`). Package format is still open (`docs/30...md:1200-1212`). | Bounded read-only package generator **T1**. Embedded server chat and provider credentials **T0**. |
| V1.1 observability/operator tools | **Explicit legacy deferrals; mostly missing** | Counterfactual veto ledger, parity gauge, chaos runner, readiness UI, audit/export pack, first-N approval, health scorecard, digest, snapshots and flip state machine are listed at `docs/05_AUDIT_RESOLUTION.md:47-60`. That document says its IBKR wording is historical (`:1-19`), so each item needs Hyperliquid reverification. | Read-only export/parity/chaos/UI pieces **T1**; approvals, flip and order-changing tools **T0**. |
| Advanced legacy proposals | **Candidate ideas, not accepted backlog requirements** | Dead-man's switch, corporate-action guard, order-type A/B, slippage heatmap, FIX export, parameter sensitivity, multi-timeframe regime consensus and scenario widget appear at `docs/05_AUDIT_RESOLUTION.md:60`. | Re-triage against Hyperliquid and current goals before any Gate 1. Risk varies; anything affecting orders/risk is **T0**. |
| P3 long evaluation | **Pending, not a V2 feature** | At least 30 days of slippage and operational-parity evidence remains post-P2 (`docs/03_STATUS.md:148-156`; `docs/00_PREREG.md:35-40`). | Host/TESTNET execution **T0**. Do not confuse this with V2 development. |

## 4. Safe isolated packages during frozen V1 testing

### Package 1 — V2 architecture contract pack

**Tier: T2.** Settle worker boundary, worker identity, feed topology, store
model, Portfolio Guardian veto semantics and subaccount fallback. Documentation
only; no code or live exchange assumptions without current official evidence.

### Package 2 — MTC integration contract pack

**Tier: T2.** Resolve Pine/Python sizing and lifecycle parity; freeze
`OrderIntent`/`ExitIntent`, Multi-TP, basket/add, stop semantics, and
desired/accepted/actual-state schemas. No runtime wiring.

### Package 3 — Dashboard V2 read-only prototype

**Tier: T1.** Use fixture/mock data for an aggregate overview, per-worker
drill-down, Market Context page, desired/accepted/exchange-truth views and
phone-responsive monitoring. No ARM, order, config, credential or live-worker
API changes.

### Package 4 — Owner analysis-package generator

**Tier: T1.** Produce a bounded, redacted, read-only export for manual Codex
subscription analysis. No embedded API, provider credential or AI authority.

### Package 5 — Local observability toolkit

**Tier: T1.** Audit/export pack, offline decision-parity gauge, MockBroker chaos
drills and readiness-checklist UI. All broker/exchange calls remain mocked.

### Package 6 — Shadow-mode split

First build fixture/file-fed MockBroker shadow mode as **T1**. Keep real
Hyperliquid feed attachment in a separate **T0** package.

### Package 7 — Official exchange reverification

**Tier: T2, read-only.** Verify current subaccount, agent-wallet, same-symbol
netting, margin-mode and API-limit facts before V2 architecture relies on them.

### Package 8 — Protected V2 implementation packages

**Tier: T0, isolated only.** Multi-worker supervisor, Guardian, storage
migration, account routing, sizing validation, Multi-TP/baskets,
event/funding gate, additional broker and remote authenticated controls may be
designed locally, but must not be merged into or activate the frozen V1
candidate without their normal contracts and acceptance.

## 5. Fastest safe order

1. Complete **Package 1** and **Package 2** so protected implementation does not
   code unresolved ownership semantics.
2. Run **Packages 3, 4 and 5** in separate isolated worktrees; they are the
   highest-value non-economic work that can progress without touching V1.
3. Run the local-only half of **Package 6**.
4. Complete **Package 7** before subaccount, netting or wallet design is frozen.
5. Split **Package 8** into small T0 work packages and audit each immediately.
6. Keep schema activation, deployment, TESTNET execution, remote exposure,
   MAINNET and any economic control off the V1 soak lane.

This order uses the VPS testing period productively while preserving a clean
boundary: **V1 proves the frozen candidate; V2 work proceeds separately and
cannot change what is being tested.**
