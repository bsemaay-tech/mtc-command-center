# AUDIT PROMPT — IBKR Paper Bridge design review

> Copy everything below the line into Codex / GPT / Gemini / DeepSeek / any reviewer LLM.
> Each model writes its own report file; Barış collects them; Claude later triages and adopts.

---

## ROLE

You are an independent senior reviewer auditing the **design** (no code exists yet) of a
paper-trading execution bridge + dashboard for Interactive Brokers. You did not write these docs.
Be adversarial: your job is to find what will break, what is unsafe, what is missing, and what
would make the product meaningfully better. Praise is worthless; findings and proposals are the
deliverable. You MUST produce both an audit AND improvement/feature proposals — a report with
findings but no proposals is incomplete and will be rejected.

## INPUT — read in this order (all under `IBKR_PAPER_BRIDGE/` in repo `C:\LAB\Tradingview_LAB_CLEAN`)

1. `README.md` — the 6 non-negotiable principles (these are BINDING constraints, not suggestions).
2. `docs/00_PREREG.md` — gates P0-P3, abort criteria, pre-registered metrics/decision rules.
3. `docs/01_ARCHITECTURE.md` — full design: stack, components, state machine, risk engine,
   LLM gate, SQLite schema, API, dashboard spec, config, safety rails, roadmap (§13).
4. `docs/02_BUILD_PLAN_1DAY.md` — 11 build tasks with acceptance criteria.

Context you must respect (do not re-litigate):
- Builder is an LLM (Opus/Codex) with ONE working day for v1. Feasibility within that budget is
  itself an audit dimension — flag any task you believe exceeds its estimate.
- LLM in the product is veto/regime-only and can never create/enlarge orders. This is a binding
  human decision. Proposals that give an LLM order authority will be discarded.
- v1 = paper only (TWS port 7497), one strategy, one symbol (AAPL 1h), localhost, SQLite,
  no-build-step frontend. Bigger-stack proposals belong in the roadmap section of your report,
  not as v1 findings.

## AUDIT DIMENSIONS (cover every one; write "no findings" explicitly where clean)

A. **Broker/API correctness** — ib_async/TWS realities: delayed market data type 3 behavior,
   `reqHistoricalData keepUpToDate` bar-close detection edge cases, bracket/OCA semantics,
   order-id lifecycle across reconnects, TWS nightly restart, clientId collisions, RTH vs
   pre/post-market bars, AAPL trading-hours vs the bar clock.
B. **State machine & concurrency** — holes in DISARMED/ARMED/KILLED and the per-trade decision
   chain; race conditions (bar close vs fill event vs reconciler vs config change while ARMED);
   restart/recovery paths; partial-fill handling; flip logic.
C. **Risk engine math & completeness** — sizing formula edge cases (gap through stop, zero/tiny
   stop distance, equity currency), daily-loss accounting (unrealized vs realized, day boundary,
   timezone), consecutive-loss/cooldown interaction with trail exits, missing risk rules.
D. **LLM gate** — is the "narrowing-only, fail-open, hard code boundary" design actually
   enforceable as specified? Prompt-injection surface via news/X content feeding Grok; TTL and
   min-confidence logic; veto latency on the trading path.
E. **Data & persistence** — SQLite schema gaps (can every PREREG §5 metric actually be computed
   from these tables?), missing indices, decision-chain reconstructability, clock/timezone policy.
F. **Dashboard & API** — spec ambiguities an implementer would guess wrong; confirm-nonce design;
   WS reconnect/state resync; anything in the 6 pages that can't be built from the spec as written.
G. **Security** — localhost assumptions, secrets handling, live-port double-lock bypass routes,
   what breaks when the user later exposes this via tunnel/VPS (§13).
H. **PREREG soundness** — are gates P0-P3 and the pre-registered decision rules (signal parity
   ≥95%, slippage 25 bps, veto-precision review) well-defined and measurable as written?
I. **Build plan feasibility** — task order, hidden dependencies, estimates, missing tasks,
   acceptance criteria that don't actually prove the deliverable.

## MANDATORY PROPOSALS (after findings)

1. **Improvements** (≥5): concrete changes to the existing design. Each: what, why, cost (S/M/L),
   which doc/section it amends, and whether it fits v1 (without breaking the 1-day budget) or v1.1.
2. **Feature ideas** (≥5): new capabilities NOT in the docs or §13 roadmap. Each: user value for a
   solo systematic trader, cost, suggested phase (v1.1/v2), and any risk it introduces.
3. **Top-3 verdict**: the three changes you would make first if this were your money on paper
   heading to live, ranked, one paragraph each.

## OUTPUT — file, format, repo rules

Write ONE markdown file: `IBKR_PAPER_BRIDGE/docs/audits/AUDIT_<your-model-name>_<YYYY-MM-DD>.md`

```markdown
# Audit — IBKR Paper Bridge design
Model: <name+version> | Date: <date> | Docs commit: <git short hash reviewed>

## 1. Summary verdict            (5 lines max: ship / ship-with-fixes / redesign, and why)
## 2. Findings                   (table: ID F-01… | Severity | Dimension A-I | Location doc§ | Issue | Suggested fix)
   Severity: CRITICAL = will lose money / order safety hole; HIGH = will break unattended P2;
   MEDIUM = wrong/ambiguous spec, builder will guess; LOW = polish.
## 3. Dimension notes            (A-I, one short block each, "no findings" allowed)
## 4. Improvements               (≥5, per spec above)
## 5. Feature ideas              (≥5, per spec above)
## 6. Top-3 verdict
```

Repo rules (BINDING):
- You may READ anything in the repo; you MUST NOT modify the design docs, anything under
  `MTC_COMMAND_CENTER/` protected scopes (`01_PINE`, `02_MTC_BACKTEST`, `07_ADAPTERS`, `MTC_V2`),
  or any file outside `IBKR_PAPER_BRIDGE/docs/audits/`. Your report file is your ONLY write.
- Never edit on `master`. A hook may auto-revert HEAD to master between tool calls — commit with
  a single inline command: `git checkout -B feature/ibkr-bridge-audit-<model>; git add IBKR_PAPER_BRIDGE/docs/audits/<your file>; git commit -m "docs(ibkr-bridge): design audit by <model>"`.
  Stage ONLY your report file (never `git add .`). Do not push, do not merge.
- Do not run any code, backtest, broker connection, or network call against IBKR. Design review only.
