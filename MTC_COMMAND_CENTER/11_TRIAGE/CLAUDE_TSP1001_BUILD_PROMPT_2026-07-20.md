# CLAUDE PROMPT — BUILD TS-P1-001 CANONICAL ORDER-STATE MACHINE

Use this prompt in a fresh Claude session. You are the builder/orchestrator for
the first of the 39 remaining full Trading System backlog tasks. Codex will audit
your committed result independently; do not ask Codex to trust this prompt or
your report.

## 1. Mission

Implement **TS-P1-001 — Canonical order states, transitions, and invariants** as
one bounded, offline, additive task. Produce one clean local commit and a
self-contained builder report for Codex. Do not push, open/update a PR, merge,
deploy, or touch the active bridge runtime.

Authoritative task card:
`C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\09_DOCS\ROADMAPS\TRADING_SYSTEM\05_IMPLEMENTATION_BACKLOG.md`
(TS-P1-001 row). Governing decision: ADR-0023, accepted under D016.

## 2. Read first

From `C:\LAB\Tradingview_LAB_CLEAN`, read completely and obey:

1. `AGENTS.md`
2. `MTC_COMMAND_CENTER\_AI_MEMORY\START_HERE.md`
3. the onboarding chain it names, especially `AI_RULES.md` and `DO_NOT_TOUCH.md`
4. `MTC_COMMAND_CENTER\09_DOCS\ADR\ADR-0023-idempotent-order-management-reconciliation.md`
5. the TS-P1-001 rows in `04_IMPLEMENTATION_ROADMAP.md` and
   `05_IMPLEMENTATION_BACKLOG.md`
6. this prompt

Use Cline CLI first for bounded mechanical editing, with `_deepseek_driver` only
as fallback, per repo token-discipline rules. Claude owns the design decisions
and must audit delegated output on the real diff. Do not send secrets or the
whole repo to any provider.

## 3. Fixed starting facts and worktree

- TS-P0 PR #25 is ready but unmerged.
- Its current local/remote head must be
  `cfb08b819aa9890725344e8315571299718cd554` on
  `feature/ts-p0-baseline` in clean worktree `C:\TSP0`.
- Current bridge suite baseline is **218 collected/passing tests** from each of
  the two required CWDs.
- The shared main worktree is intentionally dirty with unrelated user files.
  Never clean, reset, restore, checkout, stash, stage broadly, or overwrite it.
- `C:\P2RT` is the active Day 1 v2 runtime. It is completely out of scope.

Preflight:

1. Verify `C:\TSP0` branch, exact HEAD, remote branch SHA, and empty porcelain.
2. Verify `C:\TSP1001` and branch `feature/ts-p1-001-order-state` do not already
   contain work. If either exists, inspect and STOP rather than delete/reset it.
3. Create isolated worktree `C:\TSP1001` and branch
   `feature/ts-p1-001-order-state` from exact commit `cfb08b81`.
4. Run the 218-test baseline from both required CWDs before editing:
   - `C:\TSP1001`: `python -m pytest IBKR_PAPER_BRIDGE/tests -q`
   - `C:\TSP1001\IBKR_PAPER_BRIDGE`: `python -m pytest tests -q`
   Set `PYTHONUTF8=1`; use the existing interpreter/environment and install no
   dependency.

Any preflight mismatch or baseline failure is a hard STOP. Report it; do not
repair unrelated state.

## 4. Exact implementation scope

Tracked edits are limited to exactly these three paths in `C:\TSP1001`:

1. `IBKR_PAPER_BRIDGE\bridge\engine\types.py`
2. `IBKR_PAPER_BRIDGE\tests\test_order_state.py` (new)
3. `IBKR_PAPER_BRIDGE\docs\22_ORDER_STATE_CONTRACT.md` (new)

No other tracked file may change. In particular, do **not** edit `orders.py`,
`db.py`, broker adapters/mocks, API/routes, engine wiring, configuration,
schemas, migrations, strategy/risk logic, Pine, parity, or protected paths.
TS-P1-001 defines the pure canonical model; persistence and operational wiring
belong to later TS-P1 tasks.

## 5. Required design

First inventory every order-status spelling currently produced or consumed in
`bridge/` and `tests/` (for example `SUBMITTED`, `OPEN`, `PENDING`, `FILLED`,
`CANCELLED_BY_ENGINE`). Put the inventory and mapping rationale in the contract.
Do not silently reinterpret an existing spelling.

Add an additive canonical state model to `engine/types.py`. Exact symbol names
are yours to choose, but the public contract must provide:

- a string-serializable enum/value type;
- a documented canonical state set covering at minimum intent/pre-submit,
  submitting, accepted/submitted, resting/open, partially filled,
  pending-cancel, filled, canceled, rejected, expired, and ambiguous/unknown
  submission outcome;
- one immutable legal-transition relation;
- a pure `can_transition`-style query;
- one fail-closed transition validator that returns the target state for a
  legal transition and raises a dedicated structured exception for an illegal
  transition;
- explicit raw-status normalization or parsing behavior. Unknown/malformed raw
  statuses must never become a live, filled, or retryable state by default;
- explicit terminal-state and same-state/idempotency semantics.

Minimum invariants:

1. Every pair of canonical states has one deterministic legal/illegal answer.
2. Filled, canceled, rejected, and expired are terminal; terminal resurrection
   is forbidden. If same-state replay is allowed, document it as an idempotent
   observation, not a new lifecycle transition.
3. An ambiguous/unknown submission outcome cannot transition back to intent or
   submitting/retry without authoritative reconciliation evidence. TS-P1-003
   will implement recovery; TS-P1-001 must not create a blind-retry path.
4. Partial fill cannot regress to a lower-progress ordinary state. Pending
   cancel may still receive authoritative fill/terminal outcomes.
5. Unknown raw broker values fail closed and are reason-coded; no permissive
   default such as `OPEN` is allowed.
6. Transition helpers are side-effect-free and transition tables cannot be
   mutated by callers.
7. Existing Pydantic models and imports remain backward compatible. Do not wire
   the canonical model into persistence or broker behavior in this task.

The contract must contain: state glossary, raw-to-canonical mapping, complete
transition table, terminality, same-state behavior, fail-closed behavior,
quantity limitations (state-only logic cannot prove fill arithmetic), future
task boundaries, rollback, and Barış acceptance marker. Mark the invariant
contract **PROPOSED pending Barış review after Codex audit**; do not claim owner
acceptance yet.

## 6. TDD and required evidence

Use strict RED→GREEN:

1. Write `test_order_state.py` before implementing the new symbols.
2. Run it against the clean base code and capture semantic RED (missing model or
   violated invariants), not a syntax/environment failure.
3. Implement only enough in `types.py` to turn the focused suite green.

No new dependency such as Hypothesis. Exhaustive nested loops over the enum are
acceptable property-style evidence.

Focused tests must cover at least:

- exhaustive all-state-pairs agreement with the declared transition relation;
- every documented legal edge and representative illegal edges;
- terminal-state resurrection attempts;
- same-state/idempotent replay semantics;
- unknown-submission blind-resubmit rejection;
- partial-fill and pending-cancel race paths;
- known raw-status aliases and unknown/malformed inputs;
- string/JSON/Pydantic round-trip behavior;
- immutable transition-map attack;
- pure/no-mutation behavior;
- compatibility imports for existing models in `types.py`.

After focused GREEN, run the complete suite from both required CWDs. Expected
count is `218 + number_of_new_tests`, identical in both CWDs. Run
`python -m compileall` or a focused compile check for the changed Python files.

## 7. Adversarial self-review before commit

Attack your result before calling it done:

- Can `FILLED` become `OPEN`, `PARTIALLY_FILLED`, or `PENDING_CANCEL`?
- Can `CANCELED` or `REJECTED` be resurrected by a raw alias?
- Can `UNKNOWN_SUBMISSION` return to `SUBMITTING`?
- Does a garbage status accidentally normalize to `OPEN` or `SUBMITTED`?
- Can a caller mutate the exported transition set/map?
- Does `bool`, `None`, bytes, whitespace, or case variation bypass parsing?
- Is `PENDING_CANCEL -> FILLED` handled as authoritative race completion?
- Did you invent fill-quantity correctness that belongs to TS-P1-004?
- Did any production order, database, broker, exchange, or strategy path change?

Record results in the report.

## 8. Commit and report

Run the repo guard from `C:\TSP1001`. Stage the three allowed paths explicitly;
never use `git add .` or `git add -A`. Verify cached scope and `git diff --check`.
Create exactly one local commit, suggested message:

`feat(bridge): define canonical order-state invariants`

Do not push or modify PR #25. Leave `C:\TSP1001` clean at the new commit.

Write the builder report in the shared main worktree:

`MTC_COMMAND_CENTER\11_TRIAGE\CLAUDE_TSP1001_BUILD_REPORT_2026-07-20.md`

The report must clearly separate **builder claims** from raw evidence and include:

- base/head SHA, branch/worktree, exact diff and staged files;
- current raw-status inventory and chosen canonical mapping;
- complete state set, terminal states, and transition count;
- RED command/output summary and GREEN focused/full commands with exact counts;
- adversarial self-review results;
- repo-guard result and clean final porcelain;
- explicit confirmation of no P2RT/API/scheduler/network/deploy/push/PR action;
- unresolved design questions for Barış/Codex;
- exact instructions for the independent Codex auditor to locate the commit.

Update the canonical main-worktree handoffs conservatively, leaving them
uncommitted. End your response with: commit SHA, tests, report path, and
`READY FOR INDEPENDENT CODEX AUDIT`.

