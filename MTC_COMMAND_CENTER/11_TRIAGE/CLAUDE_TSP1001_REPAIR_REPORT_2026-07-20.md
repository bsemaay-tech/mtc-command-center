# CLAUDE TS-P1-001 REPAIR REPORT — 2026-07-20

Builder: Claude (Sonnet 5), repairing the two BLOCK findings from
`MTC_COMMAND_CENTER/11_TRIAGE/CODEX_TSP1001_AUDIT_2026-07-20.md` against the
immutable audited commit `5140e062b8c1f3fcc78e96c7357060c60a51285d`. This
report separates **builder claims** from **raw evidence**. Codex must
re-audit the real diff independently — do not trust this report's prose.

## 1. Location for the independent Codex re-auditor

- Worktree: `C:\TSP1001`
- Branch: `feature/ts-p1-001-order-state`
- Audited (BLOCKed) commit, untouched, not amended: `5140e062b8c1f3fcc78e96c7357060c60a51285d`
- New repair commit: `851d88a084875e48b63fba455cb7b27f357c5ac4`
- Repair commit's parent (verified): `5140e062b8c1f3fcc78e96c7357060c60a51285d` — exact match, confirmed via `git rev-parse HEAD^`.
- Inspect with:
  ```
  git show 851d88a084875e48b63fba455cb7b27f357c5ac4 --stat
  git diff 5140e062b8c1f3fcc78e96c7357060c60a51285d 851d88a084875e48b63fba455cb7b27f357c5ac4
  ```
- `C:\TSP0`, `C:\P2RT`, `C:\P1IF`, `C:\G5R`, `C:\BTL2` were not touched this session. No push, no PR, no merge, no deploy.

## 2. Pre-fix reproduction (raw evidence, before any edit this session)

Both findings were independently reproduced against the unmodified audited
commit, from `C:\TSP1001\IBKR_PAPER_BRIDGE` with `PYTHONUTF8=1` and
`PYTHONPATH` set to that directory, via a throwaway script (not committed):

```text
F2a reason_code='<no-attr>'
F2b message='NON_STRING_RAW_STATUS: unrecognized raw order status LEAK_TOKEN_9f8e7d' leaked=True
F2c BUG REPRODUCED: got RuntimeError instead of UnknownRawOrderStatusError: RuntimeError('repr exploded')

F1a FILLED->OPEN before=False after=True
F1b normalize('OPEN') before=OrderState.OPEN after=OrderState.FILLED
```

This matches the audit's own reproduction exactly (mutable seed dict lets a
mutation change `can_transition`/`normalize_raw_order_status` decisions;
`IllegalOrderTransitionError` has no `reason_code`; a hostile `__repr__`
leaks into or crashes `UnknownRawOrderStatusError` construction).

## 3. Repair approach

**F1 (mutable backing dictionaries).** The bug was not that the proxies
were writable — direct assignment and `frozenset.add` were already blocked —
it was that `_ORDER_STATE_TRANSITIONS_SEED` and
`_RAW_ORDER_STATUS_ALIASES_SEED` were module-level names bound to the same
mutable `dict` object each `MappingProxyType` wraps, so any caller could
mutate the dict directly through that name and change what the proxy shows.
Fix: removed both names. The dict literals are now written directly as the
argument to `MappingProxyType({...})`, so after that statement executes, no
reference to the underlying mutable dict remains anywhere except inside the
proxy itself (which exposes no method to retrieve it). This is not "a
mutable seed under a different name" — there is no name at all.

**F2 (unsafe exception contract).**
- `IllegalOrderTransitionError` now sets `self.reason_code =
  "ILLEGAL_ORDER_TRANSITION"` (a single stable value — the pure transition
  table has no concept of *why* a pair is illegal beyond "not in the legal
  set", so no further categorization was invented) alongside the existing
  `from_state`/`to_state` fields. Its message still formats
  `from_state.value`/`to_state.value` — safe, because these are always our
  own closed `OrderState` enum members, never externally supplied raw data
  (unlike `raw` in `normalize_raw_order_status`, which is typed `object` by
  design because it parses untrusted broker/DB strings). This asymmetry is
  deliberate, not an oversight.
- `UnknownRawOrderStatusError.__init__` no longer interpolates `{raw!r}`
  into its message. It now reports only `type(raw).__name__`. `type(x)` and
  `.__name__` never invoke user-overridable code, so a hostile `__repr__`
  (leaking or raising) can no longer affect message construction at all.
  `self.raw = raw` is unchanged — a caller who wants the original value
  still has it, at their own risk if they choose to `repr()` it themselves.

## 4. Exact diff (raw evidence)

```
git diff --name-status 5140e062 851d88a0
M	IBKR_PAPER_BRIDGE/bridge/engine/types.py
M	IBKR_PAPER_BRIDGE/docs/22_ORDER_STATE_CONTRACT.md
M	IBKR_PAPER_BRIDGE/tests/test_order_state.py

git diff --cached --stat (at commit time)
 IBKR_PAPER_BRIDGE/bridge/engine/types.py          | 34 ++++++++------
 IBKR_PAPER_BRIDGE/docs/22_ORDER_STATE_CONTRACT.md | 41 +++++++++++++++--
 IBKR_PAPER_BRIDGE/tests/test_order_state.py       | 56 +++++++++++++++++++++++
 3 files changed, 112 insertions(+), 19 deletions(-)
```

Exactly the three allowed paths — the same three as the audited commit, no
others. `git diff --cached --check` was clean (no whitespace errors).

## 5. New regression tests (added to `tests/test_order_state.py`)

- `test_illegal_transition_error_is_structured` — extended with a
  `reason_code == "ILLEGAL_ORDER_TRANSITION"` assertion (F2).
- `test_leaking_repr_object_fails_closed_without_leaking_into_message` (new) — F2.
- `test_exploding_repr_object_still_raises_dedicated_error_not_a_repr_crash` (new) — F2.
- `test_no_module_level_mutable_dict_backs_the_transition_policy` (new) — F1,
  **name-agnostic**: scans every attribute in `vars(bridge.engine.types)`
  for *any* plain `dict` containing `OrderState.FILLED` as a key, regardless
  of what it's called. Per the repair prompt's "do not hide a new mutable
  seed under a different name," this does not rely on the old name.
- `test_no_module_level_mutable_dict_backs_the_raw_alias_policy` (new) — F1,
  same name-agnostic approach for the raw-alias table.
- `test_mutating_a_copy_of_transitions_does_not_affect_can_transition` (new) — F1,
  proves the one avenue a real caller does have (`dict(ORDER_STATE_TRANSITIONS)`)
  cannot affect the original.
- `test_mutating_a_copy_of_raw_aliases_does_not_affect_normalization` (new) — F1, same for raw aliases.

**RED** (these 5 tests/assertions, run against the audited commit's
unmodified code, before any fix):

```text
FAILED tests/test_order_state.py::test_illegal_transition_error_is_structured
FAILED tests/test_order_state.py::test_leaking_repr_object_fails_closed_without_leaking_into_message
FAILED tests/test_order_state.py::test_exploding_repr_object_still_raises_dedicated_error_not_a_repr_crash
FAILED tests/test_order_state.py::test_no_module_level_mutable_dict_backs_the_transition_policy
FAILED tests/test_order_state.py::test_no_module_level_mutable_dict_backs_the_raw_alias_policy
5 failed, 75 passed in 0.63s
```

Each failure was inspected and confirmed to fail for the intended semantic
reason (missing `reason_code`, leaked token in message, `RuntimeError`
instead of the dedicated exception, and the exact `_..._SEED` name found by
the scan) — not a typo or environment issue.

**GREEN** after the fix:

```text
python -m pytest tests/test_order_state.py -q
80 passed in 0.46s
```

74 (prior) + 6 new tests = 80. No test count was lowered; one existing test
was strengthened in place (added an assertion) rather than counted as new.

## 6. Full-suite evidence (raw, both required CWDs; expected `218 + 80 = 298`)

```text
C:\TSP1001>                       python -m pytest IBKR_PAPER_BRIDGE/tests -q   -> 298 passed, 1 warning, 42.86s
C:\TSP1001\IBKR_PAPER_BRIDGE>      python -m pytest tests -q                     -> 298 passed, 1 warning, 40.07s
```

Identical count both CWDs. Compile check:

```text
python -m py_compile IBKR_PAPER_BRIDGE\bridge\engine\types.py IBKR_PAPER_BRIDGE\tests\test_order_state.py
-> exit 0 (COMPILE OK)
```

## 7. Independent 121-pair oracle re-check (fresh process, raw evidence)

A standalone script (not part of the pytest suite) independently
constructed the expected 44-of-121 transition relation and compared it
against the public `can_transition` API, 20 repeats per pair, in a fresh
Python process:

```text
pairs=121 legal=44 repeats=20 mismatches=[]
```

Confirms the transition relation itself is byte-for-byte unchanged by this
repair — only the backing-mutability and exception-safety issues were
touched, per "Frozen behavior."

## 8. Fresh-process re-probe of both findings (raw evidence, post-fix)

```text
F1 seed-name-gone: _ORDER_STATE_TRANSITIONS_SEED exists=False
F1 seed-name-gone: _RAW_ORDER_STATUS_ALIASES_SEED exists=False
F1 module-level plain-dict names: ['__builtins__', '__annotations__']
F1a copy-poison FILLED->OPEN before=False after=False unaffected=True
F1b copy-poison normalize('OPEN') before=OrderState.OPEN after=OrderState.OPEN unaffected=True

F2a reason_code='ILLEGAL_ORDER_TRANSITION' from_state=<OrderState.FILLED: 'FILLED'> to_state=<OrderState.OPEN: 'OPEN'>
F2b message='NON_STRING_RAW_STATUS: unrecognized raw order status of type Leaky' leaked=False reason_code='NON_STRING_RAW_STATUS'
F2c FIXED: got UnknownRawOrderStatusError reason_code='NON_STRING_RAW_STATUS'
```

- The only module-level plain `dict` attributes remaining are `__builtins__`
  and `__annotations__` — standard Python module artifacts present on every
  module, unrelated to either policy map. No named mutable backing dict
  survives.
- Copy-poisoning (the only mutation avenue actually available to a caller
  now) leaves `can_transition`/`normalize_raw_order_status` unaffected.
- The exact hostile-`repr` probes from the audit (`Leaky`, `Exploding`) no
  longer leak or crash; both now raise `UnknownRawOrderStatusError` with
  `reason_code="NON_STRING_RAW_STATUS"`.

## 9. Frozen behavior — confirmed unchanged

Not touched: state names/meanings, all 44 legal pairs (§7 above), terminal
and same-state semantics, `PENDING → SUBMITTED`, `PENDING_CANCEL → OPEN`,
direct terminal edges, `WAITING_CHILD` exclusion, `UNKNOWN_SUBMISSION`
resolution edges, existing Pydantic model fields/defaults, and the
PROPOSED/owner-gated status of the contract. The five open design questions
from the original build report are unresolved by this repair (this was a
BLOCK repair, not a design-question resolution pass).

## 10. Contract doc updated to match repaired implementation

`docs/22_ORDER_STATE_CONTRACT.md`: added a "Repair history" note; updated
the raw-to-canonical mapping section to state the error message never
interpolates `repr`/`str` of `raw` (only `type(raw).__name__`) and that
`IllegalOrderTransitionError` always carries `reason_code ==
"ILLEGAL_ORDER_TRANSITION"`; rewrote invariant 6 to state precisely that no
module-level name backs either policy dict (not just that the proxy blocks
direct writes); added invariant 7 for the exception-safety guarantee
(renumbering the former invariant 7 to 8); updated the test-count reference
from 74 to 80.

## 11. Explicit confirmation of no out-of-scope action

No P2RT action, no API/server start, no scheduler action, no deploy, no
push, no PR created/updated/merged, no next-task (TS-P1-002) work started or
scaffolded. `C:\TSP0` was not touched. Only `types.py`, `test_order_state.py`,
and `22_ORDER_STATE_CONTRACT.md` changed, identically to the audited
commit's scope.

## 12. Remaining owner gates

- Independent Codex re-audit of commit `851d88a084875e48b63fba455cb7b27f357c5ac4` (this repair).
- If re-audit passes: Barış acceptance of the PROPOSED TS-P1-001 invariant
  contract, including the five still-open design questions from the
  original build report (`CLAUDE_TSP1001_BUILD_REPORT_2026-07-20.md` §11) —
  none of which this repair resolved or was authorized to resolve.
- TS-P1-002 remains blocked until both of the above complete.

## 13. Result

**READY FOR INDEPENDENT CODEX RE-AUDIT**

- New repair commit SHA: `851d88a084875e48b63fba455cb7b27f357c5ac4`
- Exact parent SHA: `5140e062b8c1f3fcc78e96c7357060c60a51285d` (verified via `git rev-parse HEAD^`)
- Focused: 80/80 passed. Full suite: 298/298 passed, identical from both
  `C:\TSP1001` and `C:\TSP1001\IBKR_PAPER_BRIDGE`.
- Repair report path: `MTC_COMMAND_CENTER/11_TRIAGE/CLAUDE_TSP1001_REPAIR_REPORT_2026-07-20.md`
- No push/PR/merge/deploy/P2RT/next-task action was taken.
