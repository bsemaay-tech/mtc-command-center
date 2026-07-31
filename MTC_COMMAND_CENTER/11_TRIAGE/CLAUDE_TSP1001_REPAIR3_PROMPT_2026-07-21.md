# Claude Third Repair Prompt — TS-P1-001 Writable Holder Only

Use this prompt in a fresh Claude session. Repair only F1-R2 from:

`MTC_COMMAND_CENTER/11_TRIAGE/CODEX_TSP1001_REAUDIT2_2026-07-21.md`

Do not start TS-P1-002.

## Mission and fixed topology

Create exactly one new local child commit on top of
`a15a6b1f6648016fe99278fe993daa2c1b49b923`.

- Worktree: `C:\TSP1001`
- Branch: `feature/ts-p1-001-order-state`
- Required new parent: `a15a6b1f6648016fe99278fe993daa2c1b49b923`
- Allowed tracked paths only:
  - `IBKR_PAPER_BRIDGE/bridge/engine/types.py`
  - `IBKR_PAPER_BRIDGE/tests/test_order_state.py`
  - `IBKR_PAPER_BRIDGE/docs/22_ORDER_STATE_CONTRACT.md`

Read `AGENTS.md`, canonical onboarding, ADR-0023, both TS-P1-001/002 roadmap and
backlog rows, all prior TS-P1-001 audit/repair reports and prompts, and the new re-audit
report above. Reproduce F1-R2 against unmodified parent before editing.

Do not amend/rebase prior commits. Do not use checkout/reset/restore/stash/clean on
tracked files. No push, PR, merge, deploy, P2RT, network, dependency, migration,
broker, persistence, strategy/risk, schema, Pine, parity, or next-task action.

## Reproduced residual defect

Tuple contents are immutable, but the `_ImmutableMapping` holder is not:

```python
ORDER_STATE_TRANSITIONS._pairs = (
    (OrderState.FILLED, frozenset({OrderState.FILLED, OrderState.OPEN})),
)
RAW_ORDER_STATUS_ALIASES._pairs = (("OPEN", OrderState.FILLED),)
```

Both assignments succeed and change later public decisions. `__slots__` only removes
`__dict__`; it does not freeze the slot.

## Repair requirements

1. Use an intrinsically immutable holder as well as immutable contents. There must be
   no writable storage attribute whose replacement changes policy decisions.
2. A tuple subclass with `__slots__ = ()` and Mapping methods is one acceptable
   dependency-free design; implementation choice remains yours if it meets the proof.
3. Preserve public read-only `collections.abc.Mapping` behavior, all eleven states,
   exactly 44 legal pairs, all five aliases, and `frozenset` transition values.
4. Add regression tests that attempt both normal attribute assignment and
   `object.__setattr__` against the actual exported holders and prove policy decisions
   cannot change.
5. Retain the transitive-GC tests. Test the holder itself, not only mutable containers
   in its referent graph.
6. Update contract wording to distinguish immutable contents from an immutable holder.

Do not broaden the threat model to module-variable rebinding, class monkeypatching,
`ctypes`, or memory corruption. Direct mutation of the existing exported object is the
finding.

## Frozen behavior

F2-R is closed and must remain closed: constant raw-status error messages, hostile
metaclass/`repr` safety, stable reason codes, and `.raw` preservation. Do not change
state names, transitions, aliases, terminal/replay semantics, `PENDING -> SUBMITTED`,
`PENDING_CANCEL -> OPEN`, direct terminal edges, `WAITING_CHILD`, UNKNOWN resolution,
Pydantic payload shapes, or the PROPOSED owner gate. The five design questions remain
owner decisions.

## Required proof

1. Fresh-process pre-fix reproduction on exact parent `a15a6b1f...`.
2. Semantic RED by copying only the updated focused test into a short throwaway
   worktree at the parent.
3. Updated focused suite with `PYTHONUTF8=1`; do not lower the current 85 count.
4. Complete suite from both `C:\TSP1001` and
   `C:\TSP1001\IBKR_PAPER_BRIDGE`.
5. `py_compile` for both Python files.
6. Document-derived 121-pair oracle: exactly 44 legal, zero mismatch.
7. Fresh-process direct assignment and `object.__setattr__` attacks against both
   exports; all must fail without changing later decisions.
8. Transitive-GC, hostile-metaclass, hostile-`repr`, serialization, exact three-file
   scope, `git diff --check`, protected identity, exact parent, and clean post-commit
   porcelain checks.

## Deliverables and stop

Create one new repair commit and report:

`MTC_COMMAND_CENTER/11_TRIAGE/CLAUDE_TSP1001_REPAIR3_REPORT_2026-07-21.md`

Report raw RED/GREEN commands and counts, attacks, oracle, diff, SHA/parent, and gates.
Stop with `READY FOR INDEPENDENT CODEX RE-AUDIT`. Do not create or start TS-P1-002.
Owner acceptance remains separate after a technical PASS.
