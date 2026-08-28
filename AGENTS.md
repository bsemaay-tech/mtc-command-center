# AGENTS.md — repository router

> **Identity.** This is the live MTC Command Center repository. The canonical checkout is
> `C:\LAB\Tradingview_LAB_CLEAN`; isolated worktrees of that repository are valid. The sibling
> `C:\LAB\tradingview-lab` is frozen legacy: do not read its onboarding, run it, or edit it.

## Load exactly one stage

1. Read this router and root `DECISIONS.md`.
2. Use `CONTEXT_MAP.md` to select exactly one stage for the task's primary deliverable.
3. Read that stage's `AGENTS.md`, `INPUTS.md`, `OUTPUTS.md`, `TESTS.md`, and `HANDOFF.md`.
4. Read only the task-triggered sources named by that stage. A stage `CONTEXT.md`, when present,
   is a lazy terminology glossary; never treat it as a spec, procedure, or handoff.

Do not load `_AI_MEMORY/history/` by default. Grep it on demand. For triage history, grep
`MTC_COMMAND_CENTER/11_TRIAGE/INDEX.md`, then open at most the relevant record.

## Global safety invariants

- Do not change Pine logic, parity behavior/corpora, MTC strategy behavior, trading logic,
  thresholds, broker/exchange behavior, or protected schemas without explicit owner approval.
- Treat `02_MTC_BACKTEST`, `07_ADAPTERS`, `01_PINE`/`*.pine`, every `MTC_V2` or parity path,
  `06_SCHEMAS`, and `.git/` as owner-gated protected scopes. Do not rewrite hardcoded paths without
  an approved rewrite policy.
- Never recommend or imply authorization for live trading. Host contact, deploy, credentials,
  TESTNET/mainnet, ARM, order placement, destructive Git, merge, and history cleanup each require
  explicit scope. Never add secrets or bypass hooks.
- Backtests, optimizations, servers, launchers, and result-artifact generation require task authority;
  a routed procedure is not authorization to execute it.
- Preserve research/execution trust separation. Execution consumes only frozen, hash-verified
  packages. Unknown ownership, checkout purpose, or live/scheduled dependency is a STOP.
- The stage-routed monorepo is ratified through Phase 0–V3. Do not re-decide or split it. A later
  split needs the measured trigger and its own authorization; migration never silently deletes.
- Use token-efficient targeted search before broad scans. Never inspect the frozen legacy repo.

## Work and acceptance invariants

- Every Gate-1 scope records T0/T1/T2/T3 before audit dispatch. Highest overlap wins:
  T0 economic/live/host/security/deploy; T1 non-economic product code/scripts; T2 docs/evidence;
  T3 status/index/process artifacts. T0 is immediate; other audits occur at package boundaries.
- Lead and implementer are separate flagships. The lead owns scope, independent acceptance,
  repair dispatch, and authorized sequencing; the counterpart implements and self-QAs. A lead
  never accepts an implementer report without inspecting the real diff and reproducing evidence.
- Repair limits are T0=3, T1=2, T2=1, T3=0. Stop after the cap. Accepting verdicts are PASS or
  PASS-WITH-NITS (optional nits only); REQUEST_CHANGES and BLOCK are non-accepting.
- A regression test offered as defect-closure evidence must show RED on exact pre-fix behavior or
  an equivalent mutation, then GREEN with the fix, with real commands/output recorded (D026).
- Work on a `feature/<scope>` branch, never directly on `master`. Stage exact explicit paths; never
  use `git add .` or `git add -A`.
- Record every write lane's branch, worktree, exact paths, and live-dependency status.
  `_AI_MEMORY/SESSION_LOCK.md` is a checked mirror/history, not the guard. The mandatory GitHub-
  issue claim was retired by owner decision 6 on 2026-08-26. Work reaches `master` only through a
  PR with `Bridge suite (Python 3.12)` green on an up-to-date head (ruleset 21444962, no bypass).
  WP-P0-27's mechanical claim/liveness check is planned, not built.
- Before releasing a claim, reconcile current `master`, the work branch, and durable tracker state.
  Preserve foreign edits; never reset, checkout, stash, or overwrite another lane's work.
- Current state belongs in the selected stage's capped `HANDOFF.md`. Historical journals are
  search-on-demand archives. Sticky owner decisions belong in root `DECISIONS.md`; never create
  per-model log files at repository root.

For workflow, audit-roster, delegation, Git/handoff, or repository-governance work, the selected
stage is `MTC_COMMAND_CENTER/00_AGENT_PROTOCOLS/`.
