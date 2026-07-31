# CODEX PROMPT — INDEPENDENT AUDIT + TASK MANAGER FOR TS-P1-001

Use this prompt in a fresh Codex session after Claude reports that TS-P1-001 is
built and committed. You are the independent adversarial auditor and sequence
manager. You are not the builder and must not repair the audited commit in the
same pass.

## 1. Mission and program rule

Independently audit Claude's TS-P1-001 canonical order-state implementation on
real code and tests. Issue **PASS / PASS-WITH-NITS / BLOCK**. Do not trust the
builder report as evidence.

This begins the 39-task sequence:

- exactly one backlog task is built at a time;
- Claude builds and creates one local commit;
- Codex independently audits that immutable commit;
- BLOCK produces a bounded Claude repair prompt for the same task;
- PASS/PASS-WITH-NITS produces the next Claude build prompt, but does not start
  the next task;
- no task is pushed, merged, or deployed merely because tests or audit pass;
- owner, migration, testnet, merge, and deployment gates remain separate.

## 2. Read first

Read completely:

1. `C:\LAB\Tradingview_LAB_CLEAN\AGENTS.md`
2. canonical onboarding chain from `_AI_MEMORY\START_HERE.md`
3. ADR-0023
4. TS-P1-001 and TS-P1-002 rows in both roadmap/backlog files
5. `MTC_COMMAND_CENTER\11_TRIAGE\CLAUDE_TSP1001_BUILD_PROMPT_2026-07-20.md`
6. Claude's report:
   `MTC_COMMAND_CENTER\11_TRIAGE\CLAUDE_TSP1001_BUILD_REPORT_2026-07-20.md`

Treat items 5–6 as claims/specification, not proof.

## 3. Fixed expected topology and boundaries

- Base must be `cfb08b819aa9890725344e8315571299718cd554`.
- Expected worktree: `C:\TSP1001`.
- Expected branch: `feature/ts-p1-001-order-state`.
- Claude must provide one clean descendant commit.
- Expected tracked diff is exactly:
  - `IBKR_PAPER_BRIDGE/bridge/engine/types.py`
  - `IBKR_PAPER_BRIDGE/tests/test_order_state.py`
  - `IBKR_PAPER_BRIDGE/docs/22_ORDER_STATE_CONTRACT.md`
- No push/PR/merge/deploy should have occurred.

Audit is read-only toward `C:\TSP1001`. Do not edit, commit, amend, rebase,
checkout, reset, restore, stash, clean, stage, or push it. Never use
`git restore` for RED proof. Do not touch main-worktree user changes.

`C:\P2RT` is active Day 1 v2. Only two read-only Git identity snapshots are
allowed (before/after: HEAD + porcelain). No API/status GET, Task Scheduler,
process, database, exchange, credential, ARM/DISARM, or deploy action.

No external network is required. Do not install dependencies.

## 4. Preflight facts to verify

Before running tests:

1. Verify worktree path, branch, exact base ancestry, HEAD, clean porcelain,
   commit count, and commit message.
2. Verify diff name/status/stat and that only the three allowed paths changed.
3. Verify `orders.py`, `db.py`, broker files, config, schemas, migrations,
   strategy/risk logic, Pine, parity, and protected paths are byte-identical to
   base.
4. Inventory actual status strings independently across bridge code/tests and
   compare them with the contract's raw-status table.
5. Capture P2RT HEAD/porcelain once before executable audit work.

Any unexpected scope or dirty audited worktree is at least BLOCK unless clearly
proved unrelated and immutable.

## 5. Required reproductions

### A. Green suites

Run Claude's focused test and the complete suite from both required CWDs with
`PYTHONUTF8=1`. Confirm exact collected/passed counts and no order-dependent
failure. Run a compile check for changed Python files.

### B. Semantic RED against the parent

Create a throwaway worktree at exact base `cfb08b81`. Copy only the new focused
test into the throwaway tree and run it against base code. Expected result is a
semantic RED proving the new contract/model is absent or violates the new
tests. Preserve the audited worktree byte-for-byte; compare hashes before/after.
Remove only the exact throwaway worktree after verifying its resolved path.

### C. Independent transition oracle

Do not merely call the implementation's own table to prove itself. Parse the
documented transition table into an independent expected set (or construct an
explicit oracle in a temporary audit script outside the repo) and compare every
state pair against the public API. A test that derives expected results from the
same exported map is circular and insufficient.

## 6. Twelve adversarial probes

Run and report each separately:

1. **Exhaustive pair totality:** every canonical state pair has one stable
   allowed/denied result; no missing state or nondeterminism.
2. **Terminal resurrection:** FILLED/CANCELED/REJECTED/EXPIRED cannot become
   live, partial, pending-cancel, or submitting through any public path.
3. **Unknown blind retry:** ambiguous/unknown submission cannot transition to
   intent/submitting without authoritative resolution.
4. **Progress regression:** PARTIALLY_FILLED cannot regress to ordinary
   accepted/open/submitted state.
5. **Cancel/fill race:** PENDING_CANCEL can accept authoritative fill/terminal
   outcomes while illegal fallback paths remain blocked.
6. **Same-state replay:** behavior is explicit, consistent between code/doc,
   side-effect-free, and not counted as lifecycle progress.
7. **Raw normalization abuse:** garbage, whitespace, mixed case, near-miss,
   `None`, bool, number, bytes, and object inputs never default to a safe/live
   state. Known aliases map exactly as documented.
8. **Mutability attack:** callers cannot alter the legal-transition relation,
   terminal set, or alias map and thereby change later decisions.
9. **Serialization compatibility:** enum/value round-trips through string/JSON
   and existing Pydantic imports/models without changing legacy payload shape.
10. **Actual-status coverage:** every currently produced/consumed status is
    mapped or explicitly documented as deferred/fail-closed; no silent orphan.
11. **Future-task boundary:** no persistence, broker/exchange wiring, retry,
    unknown-resolution, partial-fill protection, migration, threshold, or
    strategy behavior slipped into TS-P1-001.
12. **No mutation:** audited worktree file hashes/status unchanged; main
    unrelated changes untouched; P2RT before/after HEAD and porcelain identical.

Also inspect exception messages: illegal transitions must be structured and
reason-coded without leaking arbitrary object representations or producing
tracebacks in normal caller use.

## 7. Contract review

Judge the implementation against ADR-0023 and task boundaries:

- state names and meanings unambiguous;
- complete transition table, not prose-only examples;
- terminality and same-state semantics explicit;
- raw broker status vs canonical state clearly separated;
- state-only model does not falsely claim fill-quantity correctness;
- UNKNOWN recovery explicitly deferred to TS-P1-003 with blind retry forbidden;
- persistence/idempotent identity deferred to TS-P1-002;
- partial protect-or-flatten deferred to TS-P1-004;
- rollback/read-old-state compatibility described;
- invariant contract honestly marked PROPOSED pending Barış acceptance.

## 8. Verdict and management output

Write:

`MTC_COMMAND_CENTER\11_TRIAGE\CODEX_TSP1001_AUDIT_2026-07-20.md`

The report must separate **builder claimed** from **verified now**, include raw
commands/counts, scope evidence, RED proof, all twelve probes, findings with
file:line and reproducible evidence, P2RT before/after identity, and one verdict:

- **PASS:** all acceptance and adversarial requirements hold.
- **PASS-WITH-NITS:** no safety/contract blocker; enumerate bounded nits.
- **BLOCK:** any fail-open transition, circular-only test proof, undocumented
  actual status, mutable policy surface, scope breach, false evidence claim, or
  reproducible regression.

Do not fix findings in this audit session.

Then create exactly one next-session prompt:

- If BLOCK: `CLAUDE_TSP1001_REPAIR_PROMPT_2026-07-20.md`, limited to reproduced
  findings and requiring a new repair commit plus Codex re-audit.
- If PASS/PASS-WITH-NITS:
  `CLAUDE_TSP1002_BUILD_PROMPT_2026-07-20.md`, self-contained for TS-P1-002,
  based on the audited TS-P1-001 commit. It must preserve the TS-P1-002 migration
  and owner-review gates and must not begin implementation automatically.

Update canonical handoffs conservatively. No push, PR mutation, merge, deploy,
or next-task execution. End with verdict, audited SHA, report path, next prompt
path, and the exact owner decision still required.

