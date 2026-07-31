# FABLE BUILD PROMPT — TS-P0-001 → TS-P0-004 (Phase 0 baseline chain), 2026-07-19

You are Claude Fable 5 in a FRESH session, acting as BUILDER for the MTC trading-system
roadmap Phase 0. Owner Barış has explicitly directed on 2026-07-19: Fable builds
TS-P0-001 and then continues, in order, through every subsequent task that can be
completed without pausing for an owner decision; a separate Fable session will
independently audit the result afterward. This owner directive supersedes the backlog's
"Recommended AI" routing (Cline/DeepSeek build) for this run.

Do not redo prior audits. Do not touch the running monitoring window.

## 1. Canonical context

- Canonical repo: `C:\LAB\Tradingview_LAB_CLEAN` (never `C:\LAB\tradingview-lab`).
- Read first: `AGENTS.md`, then `MTC_COMMAND_CENTER\_AI_MEMORY\START_HERE.md`, then load
  the `mtc-repo-guard` skill before any git action.
- Backlog (authoritative task cards):
  `MTC_COMMAND_CENTER\09_DOCS\ROADMAPS\TRADING_SYSTEM\05_IMPLEMENTATION_BACKLOG.md`
  — NOTE: the ROADMAPS directory is currently UNTRACKED in the main worktree. Read it
  from the MAIN worktree path above (it will not exist in your build worktree).
- Current master: **`008e065e`** (PR #24 merge; contains audited interim TS-P1-007).
- Runtime: `C:\P2RT`, detached at **`008e065e`**, bridge RUNNING and ARMED in the live
  Day 1 v1 monitoring window (run `paper-20260719185026`, paper/testnet).
  **READ-ONLY toward C:\P2RT. Never write, checkout, restart, stop, ARM, DISARM, or
  touch its scheduler/task/DB. `git -C C:\P2RT` read commands and file-hash reads are
  allowed and are exactly what TS-P0-001 needs.**
- Main worktree is DIRTY with pre-existing user files (36 entries) — protected. Never
  clean/reset/stash/checkout them. Build in an isolated worktree.

## 2. Workspace

```
git -C C:\LAB\Tradingview_LAB_CLEAN worktree add C:\TSP0 -b feature/ts-p0-baseline 008e065e
```

All code work happens in `C:\TSP0`. Commit locally per task (one commit per task,
conventional messages). **NO push, NO PR, NO merge** — the independent Fable audit gates
those. Known repo quirk: a hook can flip the MAIN worktree's HEAD back to master between
tool calls; your separate worktree is unaffected, but never assume main-worktree branch
state.

## 3. Task chain (execute in order; each has full card in the backlog — re-read it)

### Task A — TS-P0-001: read-only repo/runtime baseline manifest + drift checker

Build exactly per the card:

- `IBKR_PAPER_BRIDGE\tools\check_runtime_baseline.py` — offline CLI, explicit
  `--repo-root`, `--runtime-root`, expected-release inputs; reads Git HEAD/status +
  selected bridge source/config hashes; emits deterministic JSON + Markdown manifests;
  exit **0** exact clean match, **2** drift/dirty/missing runtime, **3** invalid
  evidence input. Default operation: no HTTP, no exchange, no Task Scheduler, no
  database, no process-control.
- `IBKR_PAPER_BRIDGE\tests\test_runtime_baseline.py` — required tests from the card:
  clean match, commit drift, dirty repo, dirty runtime, missing runtime, changed config,
  invalid Git output, deterministic file ordering, secret-safe output, no-mutation.
  Use temp git repos as fixtures; never mutate the real repo/runtime in tests.
- `IBKR_PAPER_BRIDGE\docs\RUNTIME_BASELINE_CONTRACT.md` — schema version, field
  definitions, exit-code contract, hash scope (list the exact files/trees hashed and WHY
  — Barış will review this scope afterward).
- Acceptance: output contains schema version, timestamp, both canonical paths, both
  commits, dirty flags, selected tree/file hashes, config hash, explicit match verdict;
  missing paths / malformed git output fail safely (exit 3, no traceback spew);
  byte-stable output except the declared timestamp field; NO secrets (never read `.env`,
  never hash credential files, redaction test proves it).
- Integration proof (read-only, after unit tests green): run the tool once against the
  REAL pair `--repo-root C:\TSP0 --runtime-root C:\P2RT` with expected commit
  `008e065e`, capture command + raw exit code + manifest; then show
  `git -C C:\P2RT status --porcelain` empty and HEAD unchanged (before/after).

### Task B — TS-P0-002: release/rollback evidence contract + manifest tool

Per card: `IBKR_PAPER_BRIDGE/docs/RELEASE_EVIDENCE_CONTRACT.md` + manifest tool/tests +
report. Manifest must validate commit/tree/config/lock/schema/runtime hashes and a
rollback commit; include tamper, missing-field, and old-version tests. No deploy, no
checkout, no requirements change. Build on top of Task A's hashing primitives — do not
duplicate them. Mark the contract document header **DRAFT — pending Barış approval**
(the card requires owner approval of the contract; drafting + tooling is in scope,
declaring it binding is not).

### Task C — TS-P0-003: honest monitoring-window state

Per card: bridge status/read-model gains an explicit window state —
running / down / interrupted / reset — such that a DOWN bridge can NEVER present as an
active soak window. Tests: every transition, stale-age behavior. Constraints: NO
restart/ARM/scheduler action; code + tests only, in the worktree. This touches live
bridge source (`bridge/`): keep the diff minimal and additive; the running P2RT instance
is NOT redeployed (deploy is a later, separate Barış gate). Existing behavior must not
change for any current caller — prove with the full suite. Reset policy semantics you
implement must be written into doc + report as **proposed, pending Barış confirmation**.

### Task D — TS-P0-004: ADR-0018/0025 status closure

The owner decision ALREADY EXISTS: D016 + addendum (2026-07-18) in
`_AI_MEMORY\DECISIONS.md` ratified ADR-0018..0029. This task is therefore
verify-and-record, not decide: check the ADR files/index actually reflect the ratified
status with correct decision citation; fix only status/link inconsistencies if found
(docs-only); produce the decision report the card requires, citing D016 evidence. If you
find the ADR files already consistent, the deliverable is the verification report
closing TS-P0-004. **Do not invent or alter any decision content.**

### STOP boundary

STOP after TS-P0-004. Phase 1 (TS-P1-001+) requires owner acceptance of the order-state
invariant contract and separate design sessions — out of scope. Also STOP immediately
and record a blocker instead of improvising if: a task card conflicts with repository
reality, a protected scope (`01_PINE`, `02_MTC_BACKTEST`, `07_ADAPTERS`, `MTC_V2`,
parity, schemas) would be touched, or any step would require a runtime/scheduler/network
mutation.

## 4. Engineering discipline (mandatory)

- TDD: write failing tests first per task; keep a RED proof (failing run output on the
  pre-task code) for every new behavior — the auditor will reproduce it.
- Run tests from BOTH CWDs (`C:\TSP0` and `C:\TSP0\IBKR_PAPER_BRIDGE`); Windows,
  `PYTHONUTF8=1` where needed.
- Full regression after each task: `python -m pytest IBKR_PAPER_BRIDGE/tests -q` — the
  pre-existing suite (164 tests at `008e065e`) must stay green; record exact counts.
- Determinism: sorted keys/file ordering, canonical JSON, declared-timestamp-only
  variability; prove byte-stability with a repeated-run test.
- Secret safety: tools must never read or emit env secrets; add an explicit negative
  test (planted fake secret file is neither read nor hashed unless in declared scope).
- Small bounded diffs; no new frameworks, no event buses, no speculative abstractions.
- D/M/R per backlog: governing doc updated (D); `GLOBAL_HANDOFF.md` / `NEXT_STEPS.md` /
  `ACTIVE_FILES.md` updated in the MAIN worktree, uncommitted (M — main tree carries
  unrelated user changes; follow existing convention); dated run report(s) in
  `MTC_COMMAND_CENTER\11_TRIAGE\` (R).

## 5. Hard safety boundaries

No push/PR/merge. No deploy. No `C:\P2RT` mutation (read-only access only). No
bridge/scheduler/process action. No ARM/DISARM/kill. No exchange/testnet/network calls
from tools or tests (offline only). No threshold/strategy/signal/Pine/parity/schema
change. No credential access; never print or hash secrets. No dependency additions
without recording a blocker (stdlib + existing deps only — hashing needs only stdlib).
Live/mainnet stays blocked. The Day 1 v1 monitoring window must be COMPLETELY
UNAFFECTED by your session — final report must prove P2RT HEAD + status unchanged and
bridge still reachable (one read-only `GET /api/status` at session end is allowed for
that proof).

## 6. End-of-session deliverables

1. **Build report:** `MTC_COMMAND_CENTER\11_TRIAGE\FABLE_TSP0_BUILD_REPORT_2026-07-19.md`
   with per task: outcome (DONE / BLOCKED+why), exact files+symbols, commit SHA, test
   commands with exact counts from both CWDs, RED-proof evidence, integration-run
   command + raw exit code (Task A), and open items needing Barış (P0-001 hash scope
   confirm; P0-002 contract approval; P0-003 reset-policy confirm).
2. **Audit handoff:** `MTC_COMMAND_CENTER\11_TRIAGE\FABLE_TSP0_AUDIT_HANDOFF_2026-07-19.md`
   for the independent Fable auditor: worktree path, branch, per-task target commits,
   exact reproduction commands (green suites, RED proofs via `git restore` against
   parent commits — COMMITTED state only), adversarial attack checklist (hash-scope
   bypass, symlink/path traversal, dirty-state false-negative, exit-code lies,
   byte-stability, secret leakage, window-state false-active, no-mutation), and the
   requested verdict form PASS / PASS-WITH-NITS / BLOCK.
3. Memory files updated (M) as above; worktree `C:\TSP0` left CLEAN at the final commit.
4. Safety confirmation block: explicit NO for push/deploy/P2RT-write/scheduler/ARM/
   threshold/strategy/credential actions, plus the window-unaffected proof.

Report facts only from evidence produced this session. "Reported by a prior session"
and "verified now" must stay distinguishable. Begin by loading the repo guard, reading
the backlog cards, and verifying the git facts above; then build.
