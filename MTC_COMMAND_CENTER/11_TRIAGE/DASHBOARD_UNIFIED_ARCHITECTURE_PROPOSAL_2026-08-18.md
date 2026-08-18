# Unified Trading-Bot Dashboard Architecture — Proposal (2026-08-18)

**Status:** PROPOSAL — design document only. Nothing here authorizes
implementation. The Bridge is a protected surface: any code change to it
requires owner approval and the tier-appropriate audit (AGENTS.md).

**Synthesizes four sources:**

| Source | Document |
|---|---|
| Owner UI content spec (Barış, 2026-08-17, 18 sections) | prototyped at `08_DASHBOARD_APP/apps/trading_bot_dashboard/` |
| Codex Part B decisions B1–B8 | `IBKR_PAPER_BRIDGE/docs/30_V2_BACKEND_AND_DASHBOARD_DESIGN_DECISIONS.md` |
| Gemini external research D1–D6 | `11_TRIAGE/V2_DASHBOARD_EXTERNAL_RESEARCH_DRAFT_2026-08-17.md` |
| Claude V1 code review of `bridge/static/` | GLOBAL_HANDOFF entry 2026-08-18 / this document |

---

## 1. Two-surface architecture (governing decision, from B1)

```
┌──────────────────────────────┐      ┌──────────────────────────────────┐
│  EXECUTION DASHBOARD         │      │  RESEARCH / COMMAND DASHBOARD    │
│  (Bridge, loopback-first)    │      │  (MCC / QuantLens, local)        │
│                              │      │                                  │
│  aggregate + worker drilldown│      │  scanner · watchlist · news      │
│  ARM/DISARM/KILL · gates     │ ───▶ │  backtest & optimization         │
│  positions · orders · risk   │frozen│  strategy research lab           │
│  journal · reconciliation    │pkgs  │  backtest-vs-live analytics      │
│  telemetry · alerts          │ only │  AI market view (advisory)       │
└──────────────────────────────┘      └──────────────────────────────────┘
```

**Safety invariants (restated from Part B — non-negotiable):**

1. Viewing never trades; selecting/preparing never ARMs (B2).
2. Only frozen, approved packages are eligible for execution (B2).
3. Every no-trade state carries a visible reason — a blocked system must be
   distinguishable from a quiet market (B3).
4. Loopback-first; login + 2FA + roles before any non-loopback exposure (B5).
5. AI is advisory and architecturally air-gapped from execution (B6/D6).
6. A stale feed must never look like a quiet market (D2; Claude global
   staleness rule, §4.1).

## 2. Feature matrix — what exists, what gets added, where, when

Layer: **E** = execution dashboard, **R** = research dashboard.
Phase: **V1.1** = observability upgrades to current bridge UI ·
**V2** = with the Hyperliquid multi-worker backend · **R** = research-side.

| # | Feature | Source | Layer | In V1 today? | Phase |
|---|---------|--------|-------|--------------|-------|
| 1 | ARM/DISARM/KILL + state topbar | V1 / B3 | E | ✅ yes | — |
| 2 | Gate monitor (per-gate PASS/BLOCK) | V1 | E | ✅ yes | — |
| 3 | Decision stream + per-trade decision chain | V1 | E | ✅ yes | — |
| 4 | Equity + Day P&L cards | V1 | E | ✅ yes | — |
| 5 | Positions / working orders tables | V1 | E | ⚠️ generic columns | V1.1 (add SL/TP, risk $, age, slippage, commission, order latency) |
| 6 | Price chart | V1 | E | ⚠️ primitive SVG | V1.1 (overlays, trade markers, tooltip; bar → decision-chain link §4.3) |
| 7 | Staleness badges + heartbeat + last-update stamps | D2 / Claude | E | ❌ | **V1.1 — top priority** |
| 8 | WS auto-reconnect + degraded-mode banner | Codex audit finding / Claude | E | ❌ | **V1.1 — top priority** |
| 9 | Next-bar countdown (not UTC label) | Codex audit finding | E | ❌ | V1.1 |
| 10 | Block reason pinned on Overview | B3 | E | ⚠️ buried in gate list | V1.1 |
| 11 | Equity curve + minimal perf stats (WR, PF, avg R, max DD) | Owner §7 | E | ❌ | V1.1 |
| 12 | Risk utilization meters (loss budgets, exposure vs caps) | Owner §6 | E | ❌ (limits exist in backend) | V1.1 |
| 13 | Event log levels + filter (INFO/WARN/ERROR/CRIT) | Owner §15 | E | ⚠️ flat table | V1.1 |
| 14 | ARM/DISARM/KILL audit-trail card (who/when/why) | Claude | E | ⚠️ hidden in events | V1.1 |
| 15 | Single notification channel + alert budget/dedup | Owner §16 (trimmed) / Claude | E | ❌ | V1.1 |
| 16 | Config/package integrity pill (frozen-pkg hash; CONFIG DRIFT alarm) | Claude, operationalizes B2 | E | ❌ | V1.1 |
| 17 | Order-latency p50/p95 (not last value) | Claude | E | ❌ | V1.1 |
| 18 | Daily P&L decomposition (edge vs fees vs slippage) | Claude | E | ❌ | V1.1 |
| 19 | Three-tier truth reconciliation view (bot DB vs exchange truth, DRIFT alarm, last-reconcile stamp) | D1 / Claude | E | ❌ | **V2 — mandatory before live** |
| 20 | Margin health, leverage mode, liquidation distance | D3 | E | ❌ (n/a on paper) | **V2 — mandatory for perps** |
| 21 | Multi-worker aggregate + per-strategy drill-down | B1/B4/D4 | E | ❌ (single worker) | V2 |
| 22 | Worker account/subaccount labels | B3 | E | ❌ | V2 |
| 23 | Access control: login, 2FA, roles | B5 | E | ❌ (loopback only) | V2 gate — before ANY exposure |
| 24 | Expected-vs-actual slippage & trade count (narrow) | Owner §17 (trimmed) | E | ❌ | V2 |
| 25 | Lean built-in metrics endpoint (no external stack) | D5 | E | ❌ | V2 |
| 26 | Market scanner + watchlist ranking | Owner §10 | R | ❌ | R |
| 27 | News + economic calendar + high-impact restriction banner | Owner §13 | R | ❌ | R |
| 28 | Full backtest-vs-live analytics | Owner §17 | R | ❌ (QuantLens owns metrics) | R |
| 29 | AI market view (regime/confidence/bias) | Owner §12 | R | ❌ | R (advisory only) |
| 30 | Why-No-Trade feed | Owner §12 / B3 | E | ⚠️ = gate BLOCK results | V1.1 (surface mechanically, no AI needed) |
| 31 | Read-only AI assistant that explains state | B6/B7 | E | ❌ | V2+ (approval-gated, read-only) |

## 3. Deferred / rejected items — with reasons

These were proposed in one of the sources and are **deliberately not** on the
execution dashboard roadmap. Recorded per owner request so the reasoning is
auditable.

| Item | Proposed by | Verdict | Reason |
|------|-------------|---------|--------|
| Market scanner / watchlist on execution surface | Owner spec §10 | Move to R | The bridge executes one frozen strategy per worker on fixed instruments; opportunity discovery is research. Putting discovery next to ARM blurs the B1 research/execution boundary that keeps unapproved ideas away from live accounts. |
| News feed + macro calendar on execution surface | Owner spec §13 | Move to R | The frozen strategy does not gate on macro events; an external news dependency adds a failure mode and an untrusted-content channel to a money-adjacent surface. If an event-restriction rule is ever adopted, it enters as a *risk gate* in the backend (visible via the gate monitor), not as a news widget. |
| AI Market View with confidence % on execution surface | Owner spec §12 (first half) | Move to R | The bridge's LLM gate is deliberately dormant (`NullLLMGate`), and D6 mandates an AI air-gap. A confidence meter on the execution screen implies an authority the AI must not have and invites "the AI said 78%" decision-making. The valuable half — *Why No Trade?* — needs no AI: mechanical gate reasons are already the truth. |
| Full backtest-vs-live panel on execution surface | Owner spec §17 | Trim to #24 | DSR/BH-FDR/multi-window comparison methodology is owned by QuantLens (07_BACKTEST_AND_OPTIMIZATION_RULES). The bridge keeps only the two live-degradation tripwires it can measure honestly: realized slippage and trade-count vs expectation. |
| Prometheus + Grafana monitoring stack | D5 (evaluated alternative) | Reject for now | D5's own conclusion, endorsed: a solo-operator, single-host system gets more from a lean built-in metrics endpoint. A monitoring stack is a second distributed system to operate, patch, and secure — new attack surface attached to money for marginal gain at this scale. Revisit only at multi-host scale. |
| Four notification channels (Telegram/Discord/Push/Email) | Owner spec §16 | Trim to one | Multi-channel alarms train the operator to mute them. One reliable channel with dedup and a rate budget beats four noisy ones. Add a second channel only as dead-man fallback for the first. |
| Full VPS telemetry wall (CPU/RAM/disk/network graphs) | Owner spec §14 | Trim | Metrics that never change a decision are noise. Keep the decision-relevant subset: heartbeat, feed/API latency, DB disk headroom, restart count. The rest belongs in host tooling, not the trading UI. |
| Manual order entry / position editing from the dashboard | (implied by "trading terminal" framing) | Reject | Violates B2's "viewing never trades." The only manual controls are PAUSE and flatten-style emergency actions, each behind typed confirmation. The dashboard is an observatory with a brake pedal, not a cockpit. |
| One dashboard per worker; combined research+execution dashboard | B1 alternatives | Reject | Both already rejected in Part B with correct reasoning: per-worker screens hide the aggregate; a combined surface puts "promote" next to a live account. |

## 4. Claude additions in detail (new relative to Part B / D1–D6)

1. **Global staleness rule (UI constitution, not a feature):** every panel
   renders its own data timestamp; past threshold it wears a yellow
   `STALE <age>` badge. Complements D2 (which covers the feed) by covering
   *every* data path including the dashboard's own snapshot.
2. **Config/package integrity pill:** topbar shows the frozen package hash the
   worker runs; mismatch with the approved registry ⇒ red `CONFIG DRIFT`.
   This is B2 made visible at runtime.
3. **Chart ↔ decision-chain link:** clicking a bar opens that bar's decision
   chain. V1 already stores the chain — this is free depth from existing data.
4. **First-class ARM/DISARM/KILL audit trail** (who/when/why card), not rows
   lost in the generic events table.
5. **Degraded-mode banner** paired with WS auto-reconnect: polling fallback +
   visible yellow state, so transport degradation is never silent.
6. **P&L decomposition** (edge vs fees vs slippage) — answers "why are we
   earning less than expected" before backtest-vs-live can.
7. **Latency percentiles (p50/p95)** for order round-trips — broker
   degradation appears in p95 long before the last-value metric moves.
8. **Alert budget/dedup** — repeated alarms collapse into one counted line;
   alarm fatigue is a real risk control failure mode.

## 5. Suggested sequencing

1. **V1.1 observability pass** (items 5–18, 30): pure UI + read-model work on
   the existing V1 dashboard; no trading-logic change, but still Bridge scope
   ⇒ owner approval + audit tier per AGENTS.md before any code.
2. **V2 items ride the V2 backend packages** (items 19–25) — reconciliation
   and margin views depend on Hyperliquid data structures being designed
   (Packages 1/2/7 in the accepted backlog).
3. **Research-side items (26–29)** evolve independently in
   `08_DASHBOARD_APP` / QuantLens with no bridge risk; the mock prototype
   already demonstrates their UI.

## 6. Open questions (feed the deep-research prompt)

- Which reconciliation cadences/patterns do mature bar-close bots use?
- Minimal alerting taxonomy for a solo operator (what pages vs what logs)?
- Incident-response UX: what must be on screen in the first 60 seconds?
- Journal schema conventions that make post-trade review fastest?
- Security baseline for self-hosted money-adjacent dashboards beyond
  loopback+2FA?

Deep-research prompt: `DEEP_RESEARCH_PROMPT_TRADING_BOT_DASHBOARD_2026-08-18.md`.
