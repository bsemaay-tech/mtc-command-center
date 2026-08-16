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

Required Exchange-plane content:

- Hyperliquid, not SQLite or the dashboard, owns the actual exchange account,
  positions, open orders, fills, margin, mark price, funding and liquidation
  facts. The Bridge owns local intent, identity and evidence; reconciliation
  compares them and fails closed on unresolved differences.
- TESTNET is mock-money machinery testing, not profitability proof and not
  MAINNET readiness. MAINNET is real money and requires a separate future
  audit, limits and explicit owner approval.
- Distinguish the main account (owns funds and positions) from the Agent/API
  wallet (delegated signer used by the Bridge). Never expose a secret. Explain
  that no-withdraw authority still permits economically harmful trading or
  protection cancellation if the key is stolen.
- Native reduce-only SL/TP resides at Hyperliquid after acceptance and can act
  while the Bridge is offline. A trigger price is not a guaranteed fill price.
  The last accepted trailing-stop level remains, but new trail calculations and
  updates pause while the Bridge is down. The current configured strategy has
  TP disabled even though one optional full-quantity TP path exists.

Required Observation/Control-plane content:

- Current V1 is already interactive on its private local surface: the dashboard
  calls `/api/arm`, `/api/disarm`, and `/api/kill`. It has no login, 2FA, or
  roles and the server intentionally binds to `127.0.0.1:8790`. Therefore it is
  not a public website and not phone-ready remote control today.
- Explain the recommended staged model visually: Bridge + dashboard stay on the
  VPS and private; the owner's PC/phone reaches a remote read-only view first
  through a private tunnel/VPN; owner-only interactive control is a later gated
  layer with authentication, 2FA, roles, fresh-state confirmation and complete
  audit logging. Never imply that opening port 8790 to the internet is safe.
- Explain control meanings: ARM permits eligible future signals but does not
  itself create an order; DISARM blocks new entries while existing native
  protection may remain; KILL is an emergency sticky state and must not be
  described as production-ready while the recorded hardening gap remains.
- Separate human and AI permissions. A future authenticated owner control panel
  may perform explicitly gated operations; the AI assistant remains read-only
  and may only explain, summarize, alert and prepare proposals.

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
