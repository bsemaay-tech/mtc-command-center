# Claude Repair Prompt — TS-P1-001 BLOCK Findings Only

Use this prompt in a fresh Claude session. Repair TS-P1-001 only. Do not start
TS-P1-002.

## Mission

Create one new local repair commit that fixes the two findings reproduced in:

`MTC_COMMAND_CENTER/11_TRIAGE/CODEX_TSP1001_AUDIT_2026-07-20.md`

Codex issued **BLOCK** against immutable audited commit
`5140e062b8c1f3fcc78e96c7357060c60a51285d`. Do not amend, rebase, or rewrite it.
After repair, stop for a fresh independent Codex re-audit.

## Read first

Read completely:

1. `C:\LAB\Tradingview_LAB_CLEAN\AGENTS.md`
2. canonical onboarding from `MTC_COMMAND_CENTER\_AI_MEMORY\START_HERE.md`
3. ADR-0023
4. TS-P1-001 and TS-P1-002 rows in both roadmap/backlog files
5. `MTC_COMMAND_CENTER\11_TRIAGE\CLAUDE_TSP1001_BUILD_PROMPT_2026-07-20.md`
6. `MTC_COMMAND_CENTER\11_TRIAGE\CLAUDE_TSP1001_BUILD_REPORT_2026-07-20.md`
7. `MTC_COMMAND_CENTER\11_TRIAGE\CODEX_TSP1001_AUDIT_2026-07-20.md`

Treat the audit's runtime reproductions as the repair specification. Reproduce both
failures before editing.

## Fixed topology and scope

- Worktree: `C:\TSP1001`
- Branch: `feature/ts-p1-001-order-state`
- Required parent of the new repair commit:
  `5140e062b8c1f3fcc78e96c7357060c60a51285d`
- Required result: exactly one new descendant repair commit; do not amend the audited
  commit.
- Allowed tracked paths, and no others:
  - `IBKR_PAPER_BRIDGE/bridge/engine/types.py`
  - `IBKR_PAPER_BRIDGE/tests/test_order_state.py`
  - `IBKR_PAPER_BRIDGE/docs/22_ORDER_STATE_CONTRACT.md`

These files contain committed work from the prior builder. Do not run `git checkout`,
`git reset`, `git restore`, `git stash`, or `git clean` on any tracked file. Do not
push, open/mutate a PR, merge, deploy, access P2RT, call an exchange, install a
dependency, or begin any next task.

No persistence, broker/exchange wiring, retry policy, unknown-resolution behavior,
partial-fill protection, migration, threshold, strategy/risk logic, Pine, parity, or
schema change is authorized.

## Reproduced Finding F1 — mutable policy backing

Current `MappingProxyType` objects wrap module-visible mutable dictionaries:

- `_ORDER_STATE_TRANSITIONS_SEED`
- `_RAW_ORDER_STATUS_ALIASES_SEED`

Codex changed the first to make `FILLED -> OPEN` legal and the second to make raw
`OPEN` normalize to `FILLED`. Both changes affected later public API decisions.

Repair requirements:

1. Remove caller-reachable/module-visible mutable backing policy dictionaries. A
   public proxy over a named mutable seed is not sufficient.
2. Preserve the public read-only `Mapping` surfaces and `frozenset` transition values.
3. Preserve exactly the already verified 11 states and 44 legal ordered pairs.
4. Preserve the five raw aliases and their current mappings.
5. Add a regression test that attacks the actual prior backing-surface failure, not
   only assignment through the proxy.

Do not solve this by hiding a new mutable seed under a different name.

## Reproduced Finding F2 — unsafe exception contract

Codex reproduced:

```text
IllegalOrderTransitionError reason_code=None
Leaky.__repr__ text appears in UnknownRawOrderStatusError.message
Exploding.__repr__ raises RuntimeError instead of UnknownRawOrderStatusError
```

Repair requirements:

1. Give `IllegalOrderTransitionError` a stable machine-readable `reason_code` while
   retaining structured `from_state` and `to_state` fields.
2. Do not interpolate arbitrary object `repr` into error messages.
3. Every non-string object passed to `normalize_raw_order_status`, including objects
   whose `__repr__` leaks or raises, must deterministically raise
   `UnknownRawOrderStatusError` with `NON_STRING_RAW_STATUS`.
4. Keep the existing empty/unrecognized string reason codes and alias semantics.
5. Add focused tests for the illegal-transition reason code, leaking `__repr__`, and
   exploding `__repr__`.
6. Update the contract so its immutability and exception claims precisely match the
   repaired implementation.

`can_transition` totality remains defined over `OrderState x OrderState`; do not widen
the API merely because an out-of-domain unhashable list raises `TypeError`.

## Frozen behavior

Do not change:

- state names or meanings;
- any of the 44 legal pairs;
- terminal or same-state semantics;
- `PENDING -> SUBMITTED`;
- `PENDING_CANCEL -> OPEN`;
- direct terminal edges;
- `WAITING_CHILD` exclusion;
- `UNKNOWN_SUBMISSION` resolution edges;
- existing Pydantic model fields/defaults/payload shape;
- PROPOSED/owner-gated status of the invariant contract.

The five design questions remain owner questions. A BLOCK repair is not authority to
resolve them differently.

## Required proof

Before committing:

1. Reproduce both original failures on parent `5140e062...` without modifying that
   commit.
2. Run the updated focused suite from `C:\TSP1001` with `PYTHONUTF8=1`.
3. Run the complete bridge suite from both required CWDs with `PYTHONUTF8=1`:
   - `C:\TSP1001`
   - `C:\TSP1001\IBKR_PAPER_BRIDGE`
4. Run `py_compile` for both changed Python files.
5. Run an explicit 121-pair independent expected-oracle check and prove 44 legal
   pairs with zero mismatch.
6. Re-run the backing-surface and hostile-`repr` probes in fresh Python processes.
7. Verify exact diff name/status/stat, `git diff --check`, protected-path identity,
   and clean porcelain after commit.
8. Verify the new commit's parent is exactly
   `5140e062b8c1f3fcc78e96c7357060c60a51285d`.

Do not lower the original test count. Report the new exact focused and complete-suite
counts; do not prestate them.

## Deliverables and stop condition

Create one new repair commit and write a concise repair report under
`MTC_COMMAND_CENTER/11_TRIAGE/` in the main worktree, following repository handoff
rules. The report must include pre-fix reproduction, exact diff, commands/counts,
new SHA/parent, and remaining owner gates.

Stop with:

- new repair commit SHA;
- exact parent SHA;
- focused/full counts from both CWDs;
- repair report path;
- confirmation of no push/PR/merge/deploy/P2RT/next-task action;
- `READY FOR INDEPENDENT CODEX RE-AUDIT`.

Do not create a TS-P1-002 build prompt. Do not start TS-P1-002. Baris acceptance of
the PROPOSED TS-P1-001 invariant contract remains a separate owner gate after a
successful independent re-audit.
