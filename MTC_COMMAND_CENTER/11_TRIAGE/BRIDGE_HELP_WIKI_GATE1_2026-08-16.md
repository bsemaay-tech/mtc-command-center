# Bridge Help / System Map — Gate 1

**Date:** 2026-08-16  
**Owner request:** Add an interactive Help/Wiki to the existing Bridge dashboard,
using the whole-system diagram as the starting point. Clicking a component must
show a non-technical explanation. The same knowledge must also be usable by a
later AI trying to understand the code.

## Classification

- **Audit tier:** T1 — non-economic dashboard product code and tests.
- **Protected/economic impact:** none permitted.
- **Implementer:** counterpart Claude Code CLI.
- **Acceptance:** Codex Lead independently inspects the diff and executes the
  relevant static-dashboard tests. A fresh T1 flagship review is required at the
  work-package boundary. The two-round T1 cap applies.

## Allowed files

- `IBKR_PAPER_BRIDGE/bridge/static/index.html`
- `IBKR_PAPER_BRIDGE/bridge/static/app.css`
- `IBKR_PAPER_BRIDGE/bridge/static/app.js`
- one new static, machine-readable Help knowledge file under
  `IBKR_PAPER_BRIDGE/bridge/static/`
- `IBKR_PAPER_BRIDGE/tests/test_dashboard_static.py`
- one AI-facing Help/Wiki reference document under `IBKR_PAPER_BRIDGE/docs/`

## Required behavior

1. Add a distinct **Help / System Map** navigation page.
2. Show the Research, Execution, Exchange, and Dashboard/Operations planes.
3. Make each component keyboard- and pointer-activatable.
4. On activation, show: plain-language purpose, what it does, what it does not
   do, what connects to it, responsibility boundaries/overlaps, current status,
   safety notes, and relevant source paths.
5. Include at least the components shown in the owner-provided diagram, including
   the State Machine, RiskEngine, OrderManager, Reconciler, Store/WAL, Hyperliquid,
   VPS operations, strategy research/promotion, and Dashboard.
6. Clearly distinguish **current V1**, **future V2 direction**, and **separate
   future gate**. Never present a plan as implemented.
7. Use one machine-readable knowledge source for the human UI and future AI use;
   the AI-facing Markdown document must point to that source rather than duplicate
   all explanatory facts.
8. Preserve the existing no-`innerHTML` static safety contract and avoid external
   UI dependencies.
9. Be responsive and usable with keyboard focus and reduced-motion preferences.

## Explicit exclusions

- No strategy, MTC, Pine, parity, RiskEngine, OrderManager, reconciler, state
  machine, broker, API, database, or configuration behavior changes.
- No ARM, DISARM, KILL, TESTNET, MAINNET, wallet, order, server, VPS, credential,
  install, or deployment action.
- No claim that KILL hardening, V2 multi-strategy operation, Dashboard AI actions,
  or MAINNET readiness is complete.

## Validation

- Existing and new static-dashboard tests pass.
- JSON/structured knowledge parses and contains unique component IDs and valid
  internal relationship targets.
- Root dashboard still serves successfully through the existing FastAPI test
  client; no real server is launched.
- Lead checks the actual diff for scope and truthful current/planned labels.
