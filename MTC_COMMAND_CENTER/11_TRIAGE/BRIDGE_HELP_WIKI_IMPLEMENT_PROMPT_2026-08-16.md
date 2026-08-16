# Counterpart implementation task — Bridge Help / System Map

You are the counterpart implementation agent. Work only in
`C:\LAB\Tradingview_LAB_CLEAN` on branch `codex/bridge-help-wiki`.

Read, in order:

1. root `AGENTS.md`
2. `MTC_COMMAND_CENTER/_AI_MEMORY/START_HERE.md`
3. `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_HELP_WIKI_GATE1_2026-08-16.md`
4. the existing Bridge dashboard files and static-dashboard test
5. `IBKR_PAPER_BRIDGE/docs/01_ARCHITECTURE.md`
6. relevant parts of
   `IBKR_PAPER_BRIDGE/docs/30_V2_BACKEND_AND_DASHBOARD_DESIGN_DECISIONS.md`

Implement the complete bounded T1 Help/Wiki feature described by the Gate-1
contract. The owner is non-technical. The Help page should be visually clear,
interactive, and useful as a long-term project map. Clicking or keyboard-opening
each component must show a concise plain-language explanation, responsibility
boundaries, connections, status, safety notes, and source paths. Include simple
and technical detail modes if they materially improve clarity.

Use one new machine-readable static JSON file as the canonical Help knowledge
source. The browser must render it without external libraries. Create one short
AI-facing Markdown index under `IBKR_PAPER_BRIDGE/docs/` that tells future agents
how to consume and verify the JSON; it must not duplicate the whole knowledge
base.

Truth constraints:

- Distinguish current V1, future V2 direction, and separately gated future work.
- Research/QuantLens develops and promotes strategies; it never sends live
  orders.
- The current Bridge runtime is one strategy, symbol, and timeframe; Keltner is
  a plumbing subject, not a profitability claim.
- RiskEngine authorizes/rejects and sizes; OrderManager executes and protects.
- The term reconciler has two current paths: light operational reconciliation
  inside OrderManager can recover/re-protect/flatten owned state; FullReconciler
  is separate and read-only, creates authoritative checkpoints, and never
  mutates exchange state.
- Hyperliquid is authoritative for exchange facts; Bridge records remain
  authoritative for local intent and ownership. Incomplete/stale/conflicting
  evidence fails closed.
- DISARMED blocks new entries but does not automatically flatten; ARMED is
  conditional permission, not an order; KILLED is sticky. Clearly label the
  current KILL hardening gap: do not present KILL as production-ready.
- Dashboard is observation/control/help; it does not invent strategy or bypass
  backend gates.
- Optional LLM veto/reduce-only direction is initially OFF; no autonomous code
  editing or direct order authority.
- TESTNET comes first; MAINNET is a separate future owner/audit gate.

Allowed files are exactly those in Gate 1. Do not modify any Python runtime,
API, broker, state, strategy, risk, order, reconciler, database, configuration,
deployment, memory, lock, or unrelated test file. Do not run a server, browser,
backtest, broker, deployment, or network action. Do not use git checkout, reset,
stash, clean, commit, or push. Existing untracked files belong to the owner and
must be ignored.

Preserve the current no-`innerHTML` contract. Use safe DOM construction,
accessible buttons/dialog or detail panel behavior, keyboard operation,
responsive layout, visible focus, and reduced-motion handling. Keep the existing
dashboard features working.

Run the narrow static-dashboard test with the repository's available Python
environment. If the default interpreter lacks dependencies, locate the existing
workspace venv; do not install anything. Also run a JSON parse/integrity check
and `git diff --check` on the allowed paths.

At the end, report only: files changed, feature summary, exact validation run and
results, and any unresolved issue. Do not claim acceptance; the Codex Lead owns
independent inspection and Gate 5.
