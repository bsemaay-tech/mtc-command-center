# AUDIT RESOLUTION — 2026-07-06 (Claude Fable 5 triage)

> **BROKER NOTE (added 2026-07-06, after this triage):** these audits were written against the
> IBKR design. The broker was then changed to **Hyperliquid** (see `07_BROKER_DECISION.md`), which
> DISSOLVES several IBKR-specific findings rather than fixing them: the port allow-list became a
> testnet/mainnet network lock; the BarFinalizer lost all NYSE-calendar / session-end / tail-bar /
> delayed-data complexity (crypto is 24/7, real-time); the TWS nightly-restart recovery is no longer
> needed (no desktop terminal); `permId`/OCA identity became `cloid`/`positionTpsl` groups; and the
> "synthetic vs native stop" risk is resolved by Hyperliquid's native resting trigger orders. The
> non-broker findings (decision_uid schema, post-await state gate, reconciler grace, consecutive-loss
> policy, LLM veto default-off + injection mitigation, PREREG metrics glossary, honest multi-day
> build plan) all carried over unchanged. The IBKR-flavored wording below is kept as the historical
> triage record; the binding spec is the amended, Hyperliquid-native `00/01/02` docs.

Inputs: 7 external audits in `docs/audits/` (Codex GPT-5, Claude Opus 4.8, Gemini 3.1 Pro,
DeepSeek V4 Pro, Cursor Composer, GitHub Copilot, Kimi K1.5), all on docs commit `c2c3bbb0`.
All 7 verdicts: **ship-with-fixes**. This file records what was adopted into the design docs
(now AMENDED in place), what was deferred, and what was rejected with reasons. The amended
00/01/02 docs are the binding spec; this file is the change log + rationale.

## 1. Adopted into v1 (design docs amended)

| # | Change | Sources (finding) | Amended |
|---|---|---|---|
| A-01 | **Default-DENY broker port allow-list** {7497, 4002}; 4001 (IB Gateway LIVE) was waved through by the old 7496-only block. Live = triple-lock (`--enable-live` CLI + `IBKR_LIVE_ACK` env + strategy `live_allowed`). `broker.port` not runtime-editable. | Opus F-01 (CRITICAL), Codex F-05, Copilot F-05 | ARCH §11.1, §10 |
| A-02 | **BarFinalizer contract**: NYSE calendar/ET, bar-key algorithm (`last_bar_ts`), session-end force-close of the final RTH bar, 30-min tail-bar discard, reconnect re-subscribe + duplicate-bar dedup, P0 check that keepUpToDate streams under delayed type 3 (else polled fallback). | Opus F-03/04/05/06, Codex F-02, DeepSeek F-01 (CRITICAL)/F-20, Cursor F-05/07, Gemini F-03, Copilot F-01, Kimi F-05 | ARCH §6.1 |
| A-03 | **Durable order identity**: persist perm_id, parent_perm_id, oca_group, client_id, transmit_role, orderRef (= decision_uid:role), contract JSON; reconcile permId-first. | Codex F-03, Cursor F-02 (CRITICAL), Copilot F-02, DeepSeek F-04 (CRITICAL) | ARCH §6.1, §7 |
| A-04 | **TWS nightly-restart recovery**: naked own-orderRef position ⇒ re-submit protective bracket FIRST; flatten only if that fails; foreign/manual positions never adopted/flattened (WARN only). Without this the bridge would flatten every night → P2 impossible. | Kimi F-01 (CRITICAL), Opus F-17 | ARCH §6.1, §5; PREREG §7 |
| A-05 | **Stop-validity guards before sizing** (÷0, min distance, wrong side, gapped-through) + buying-power check ×0.95. | Gemini F-01 (CRITICAL), Kimi F-03/13, Opus F-14, Cursor F-10, Codex F-07, DeepSeek F-10, Copilot F-04 | ARCH §6.3 (5a, 6b) |
| A-06 | **Schema v2**: decision_uid grouping; trades gets entry_decision_uid + signal/decision/submit/fill ts + expected_px + llm_directive_id; orders gets trade_id + broker identity; new fills / bars / risk_days / llm_calls / meta tables; equity keyed (run_id, ts) + 60 s RTH sampling; indices; UTC-storage/ET-logic convention; CONFIG_CHANGED event. | Opus F-09/18/19, DeepSeek F-02 (CRITICAL)/F-08/14, Cursor F-16/17/25, Gemini F-05, Kimi F-04/11, Codex F-09/14, Copilot F-08 | ARCH §7 |
| A-07 | **Post-await state gate + preemptive KILL** + step-0 fresh position read + DISARM immediate-reconcile & SL resize. | Opus F-02, DeepSeek F-07/11, Cursor F-04 (CRITICAL), F-23 | ARCH §5, §6.5 |
| A-08 | **Reconciler PENDING grace** (2× interval) + event-driven naked check + own-orderRef-only flatten + engine-vs-broker equity divergence check (>0.5% WARN / >1% DISARM). | Opus F-11/17, Cursor F-23, Kimi FEA-04, DeepSeek F-13 | ARCH §6.5 |
| A-09 | **Consecutive-loss semantics + unattended policy**: loss = pnl<0 any exit reason; reset on win/new day/re-ARM; `on_consecutive_loss: pause_auto_rearm` default (max 2/day) — fixes the P2-unattended contradiction. Cooldown from last losing close, independent. | Opus F-08, DeepSeek F-05, Cursor F-12, Kimi F-08 | ARCH §6.3; PREREG §7 |
| A-10 | **DISARMED trail behavior decided: trail CONTINUES** (it only tightens the stop = risk-reducing). Kimi argued freeze, Cursor argued continue — continue wins: freezing leaves a live position under a stale stop, which INCREASES exposure; "LLM/engine may only reduce risk" logic applies. | Cursor F-03 vs Kimi F-02 (conflict resolved) | ARCH §5 |
| A-11 | **Flip disabled in v1** (config key removed): opposite signal = cancel bracket → reduce-only MKT close → done. Flip sub-state machine = v1.1. | Gemini F-08, Kimi F-07, Cursor F-09 | ARCH §5 |
| A-12 | **Partial fills**: never modify child qty (IBKR OCA auto-scales — qty-modify races it); explicit ENTRY_PARTIAL→…→PROTECTED/UNPROTECTED_ABORT states; SL modify = price-only, same orderId. | Gemini F-02, Codex F-04, DeepSeek F-06, Copilot F-03 | ARCH §6.1, §6.5 |
| A-13 | **Stale-DATA guard rework**: under delayed type 3, tick-age is meaningless — freshness = bar age (data timestamps, not receipt time); `max_price_age_s` only under realtime. | Cursor F-01 (CRITICAL), Opus F-22 | ARCH §6.5, §10 |
| A-14 | **LLM hardening**: TTL clamp [15,1440]; expiry = hold last directive ≤2×TTL then config.direction (never silent NO_TRADE→BOTH widen); prompt-injection source blocks (truncate/strip/wrap, store hash); veto async w/ 5 s deadline; **veto default OFF in v1** (enable at P1); cost caps (20 vetoes/day, $5/day); own env keys. Injection worst case stays denial-only (narrowing holds). | Cursor F-13/14/15, DeepSeek F-03 (CRITICAL)/F-12, Opus F-20, Codex F-08, Copilot F-07, Kimi F-16 | ARCH §6.4, §10 |
| A-15 | **Daily-loss accounting**: trading day = America/New_York; day_start_equity at first RTH bar into risk_days; engine vs IBKR realizedPnL logged side-by-side, >1% divergence ⇒ DISARM. | Codex F-06, Opus F-15, Cursor F-11, DeepSeek F-13, Kimi F-06, Copilot F-06 | ARCH §6.3, §7 |
| A-16 | **KILLED persists** in meta across restart until `/api/kill/ack`; restart = new run_id; startup reconcile blocks ARM until resolved. | Cursor F-08, DeepSeek F-19, I-01 | ARCH §5, §8 |
| A-17 | **KILL/DISARM never nonce-blocked**; X-Confirm = monotonic state_version pushed over WS; WS reconnect = server pushes full snapshot; `/api/snapshot`, `/api/gates/latest`, `/api/runs/{id}`, `/api/bars` format + bars-table sourcing + Gate Monitor empty state. | Opus F-10, Codex F-10, Cursor F-18/26/27, DeepSeek F-16/17/18, Kimi F-09/12, Gemini F-07 | ARCH §8, §9 |
| A-18 | **PREREG metrics glossary** (expected_px per order type incl. MKT gap caveat; slippage = plumbing metric under paper+delayed; unexplained-state taxonomy; missing-bar policy) + **two-stage parity** (bar identity on bridge-logged bars first, then ≥95% signal parity; golden from SOURCE engine + documented execution transform) + **operational veto precision** (≥20 vetoes, <40% ⇒ demote). | Codex F-01/12, Opus F-12, H-notes, Cursor F-20/21, Kimi F-10, Copilot F-11, Gemini H-note | PREREG §5, §6 |
| A-19 | **Build plan honesty**: relabeled 2 days (Day 1 mock core + 10a; Day 2 IBKR + 10b + polish); task 3b golden-generation added; NullLLMGate wired in task 6; test_store explicit; TWS setup checklist doc (`06_TWS_SETUP.md`, Bypass Order Precautions) + P0 no-popup assertion; scope-cut priority list; concurrency/OCA acceptance tests added. | ALL audits (Codex F-11, Opus F-13/24/F-07, Gemini F-04, DeepSeek F-23/24/25, Cursor F-22/28/29, Kimi F-15, Copilot F-10) | BUILD PLAN |
| A-20 | Security polish: XSS textContent-only rendering; CORS 127.0.0.1; raw-LLM-response redaction regex; tunnel phase = strictly monitor-only (ARM/KILL also blocked remotely until auth). | DeepSeek F-21/22, Kimi F-14, Cursor F-19, Opus F-25 | ARCH §11, §13 |
| A-21 | Ops niceties: Telegram 6 h heartbeat (RTH), next-bar countdown pill, max_open_order_age_s=600 stale-entry cancel, golden_run_id in strategy YAML. | DeepSeek I-03/04/05, I-02 | ARCH §6.5, §6.7, §9, §10 |

## 2. Deferred (added to roadmap; not v1)

| Item | Sources | Phase |
|---|---|---|
| Shadow/ghost mode (real TWS bars → MockBroker orders) | Codex FI-01, Gemini FI-3, Copilot FI-01, Opus feat-2 | v1.1 — first candidate after build |
| Counterfactual veto ledger (makes veto-precision computable live) | Opus feat-3 | v1.1 (the PREREG rule logs the would-be OrderPlan at veto time from v1 — ledger UI is v1.1) |
| Live parity gauge (rolling parity % on dashboard) | Opus feat-1, Cursor FE-01 | v1.1 |
| Chaos-drill runner (disconnect/dup-bar/child-reject drills) | Codex FI-07, Copilot FI-07 | v1.1 |
| Session-readiness checklist UI before ARM (startup reconcile part IS v1) | Codex FI-03, Copilot FI-03 | v1.1 |
| Audit/export pack (zip of run: config, decisions, fills, equity) | Codex FI-04, Cursor FE-06, Kimi FEA-05, Opus feat-6 | v1.1 |
| Deterministic event calendar (earnings/FOMC CSV hard NO_TRADE) | Opus feat-4, Kimi FEA-08 (already §13) | v1.1 |
| First-N-signals manual approval mode | Codex FI-06, Copilot FI-06 | v1.1 |
| Broker health scorecard; weekly digest; trade bar-snapshots; flip sub-state machine; Manual Execution Ticket | Kimi FEA-01/-03, DeepSeek M-04, Gemini/Kimi/Cursor | v1.1 |
| Dead-man's switch; corporate-action guard; order-type A/B; slippage heatmap; FIX export; param-sensitivity heatmap; multi-TF regime consensus; position-scenario widget | Opus feat-5/7, Codex FI-05, Gemini FI-1, Kimi FEA-07/-10, Cursor FE-07, DeepSeek M-08 | v2 |

## 3. Rejected (with reasons)

| Proposal | Source | Reason |
|---|---|---|
| Continuous target-position rebalancing (replace brackets) | Gemini FI-4 | Rewrites OrderManager; bracket semantics are simpler, auditable, and sufficient for 1 symbol × 1 strategy. v2 at earliest, only if multi-strategy portfolio demands it. |
| Kelly-criterion sizing | Kimi FEA-09 | Conflicts with the plumbing objective: sizing must stay boring/deterministic while validating execution. Edge-adaptive sizing is a research question for MCC, not the bridge. |
| Cut v1 dashboard to 1-2 pages | Gemini F-04 (partial) | Barış explicitly wants the full professional dashboard; adopted the milder consensus fix instead: 10a/10b split across 2 days + scope-cut priority list. |
| DISARMED freezes trail | Kimi F-02 | Conflict resolved the other way (A-10): trail-continue is strictly risk-reducing; freeze leaves a live position under a stale stop. |
| `claude-sonnet-5` is not a real model ID | DeepSeek F-09 | Incorrect — `claude-sonnet-5` is a current Anthropic model ID (Claude 5 family, 2026). Kept; noted as verified in ARCH §6.4. |
| TOTP-style nonce | Gemini F-07 | Overkill for localhost single-user; adopted state_version model instead (A-17). |
| Remove live mode from runtime entirely | Codex F-05 (partial) | Kept behind the triple-lock (A-01) — deleting it would just move the risk to a future hasty re-add; the allow-list + CLI flag achieves the same protection with a documented path. |

## 4. Net effect

- PREREG gates are now measurable (glossary, two-stage parity, operational veto rule).
- The three P2-killers are closed by design: nightly flatten (A-04), last-bar-never-closes (A-02),
  auto-DISARM-vs-unattended contradiction (A-09).
- The one money-safety hole (Gateway 4001) is closed by allow-list (A-01).
- Build plan is honest: 2 days, with a defined cut order that never sacrifices safety tests.
