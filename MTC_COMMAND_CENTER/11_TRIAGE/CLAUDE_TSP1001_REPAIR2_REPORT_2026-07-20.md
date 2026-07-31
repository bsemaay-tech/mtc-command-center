# CLAUDE TS-P1-001 SECOND REPAIR REPORT — 2026-07-20

Builder: Claude (Sonnet 5), repairing the two residual BLOCK findings (F1-R,
F2-R) from `MTC_COMMAND_CENTER/11_TRIAGE/CODEX_TSP1001_REAUDIT_2026-07-20.md`
against the immutable commit `851d88a084875e48b63fba455cb7b27f357c5ac4`.
This report separates **builder claims** from **raw evidence**. Codex must
re-audit the real diff independently — do not trust this report's prose.

## 1. Location for the independent Codex re-auditor

- Worktree: `C:\TSP1001`
- Branch: `feature/ts-p1-001-order-state`
- Prior repair commit, untouched, not amended: `851d88a084875e48b63fba455cb7b27f357c5ac4`
- New (second) repair commit: `a15a6b1f6648016fe99278fe993daa2c1b49b923`
- Verified parent: `851d88a084875e48b63fba455cb7b27f357c5ac4` (exact match via `git rev-parse HEAD^`).
- Inspect with:
  ```
  git show a15a6b1f6648016fe99278fe993daa2c1b49b923 --stat
  git diff 851d88a084875e48b63fba455cb7b27f357c5ac4 a15a6b1f6648016fe99278fe993daa2c1b49b923
  ```
- `C:\TSP0`, `C:\P2RT`, `C:\P1IF`, `C:\G5R`, `C:\BTL2` untouched this session. No push, no PR, no merge, no deploy.

## 2. Pre-fix reproduction (raw evidence, before any edit this session)

Both residual findings independently reproduced against unmodified `851d88a0`,
from `C:\TSP1001\IBKR_PAPER_BRIDGE` with `PYTHONUTF8=1`/`PYTHONPATH` set:

```text
named_seeds_absent=True
gc_dict_referents=1/1
before: FILLED->OPEN=False, raw OPEN=OrderState.OPEN
after:  FILLED->OPEN=True,  raw OPEN=OrderState.FILLED
policy_changed=True

BUG REPRODUCED: got RuntimeError instead: RuntimeError('metaclass name exploded')
```

Matches the re-audit's own numbers exactly (F1-R: `gc.get_referents()` on
either exported `MappingProxyType` returns the still-mutable backing `dict`
even with no name bound to it; F2-R: `type(raw).__name__` is dispatched
through `raw`'s metaclass, so a hostile metaclass overriding that lookup
raises `RuntimeError` instead of `UnknownRawOrderStatusError`).

## 3. Why the first repair wasn't enough, and what's different this time

The first repair (`851d88a0`) removed the *named* seed variables
(`_ORDER_STATE_TRANSITIONS_SEED`/`_RAW_ORDER_STATUS_ALIASES_SEED`) but still
built each export as `MappingProxyType({...})` — a dict literal passed
directly as the constructor argument. That closes "grab it by name" but not
"grab it via `gc.get_referents(exported_proxy)`", which is how
`MappingProxyType` is implemented in CPython: the proxy holds a real
reference to its wrapped dict, and `gc` (a standard-library, always-available
introspection module) surfaces that reference on request, independent of
any name. **No arrangement of `MappingProxyType` over a `dict` closes this**
— the fix has to stop using a `dict` as the backing representation.

**F1-R fix.** Added a small private `_ImmutableMapping(collections.abc.Mapping)`
backed by a `tuple` of `(key, value)` pairs (`__slots__ = ("_pairs",)`, no
`__dict__`). `__getitem__` does a short linear scan over the tuple (11 or 5
entries — negligible cost). Both `ORDER_STATE_TRANSITIONS` and
`RAW_ORDER_STATUS_ALIASES` are now instances of this class instead of
`MappingProxyType`. A tuple cannot be mutated in place at all (no
`__setitem__`/`append`/etc.), and its elements here are themselves immutable
(`OrderState` enum members, `str`, `frozenset`), so walking
`gc.get_referents` transitively from either export never reaches a `dict`,
`list`, or any other mutable container — confirmed by the new tests and the
fresh-process re-probe below.

**F2-R fix.** `UnknownRawOrderStatusError`'s message is now a constant string
per `reason_code` (`f"{reason_code}: raw order status could not be
normalized"`) and never touches any attribute of `raw` or `type(raw)` — not
`repr()`/`str()`, and not `type(raw).__name__` either. `self.raw = raw` is
unchanged (plain reference assignment, not an attribute *access* on `raw`,
so it triggers no hostile hook). This is safe against the hostile metaclass
because nothing about `raw`'s class is ever inspected at all, for any
`reason_code` (kept uniform across `NON_STRING_RAW_STATUS`, `EMPTY_RAW_STATUS`,
and `UNRECOGNIZED_RAW_STATUS` rather than special-casing just the non-string
path, to avoid leaving an asymmetric edge for a future audit to find).

## 4. Exact diff (raw evidence)

```
git diff --name-status 851d88a0 a15a6b1f
M	IBKR_PAPER_BRIDGE/bridge/engine/types.py
M	IBKR_PAPER_BRIDGE/docs/22_ORDER_STATE_CONTRACT.md
M	IBKR_PAPER_BRIDGE/tests/test_order_state.py

git diff --cached --stat (at commit time)
 IBKR_PAPER_BRIDGE/bridge/engine/types.py          | 216 +++++++++++++---------
 IBKR_PAPER_BRIDGE/docs/22_ORDER_STATE_CONTRACT.md |  75 +++++---
 IBKR_PAPER_BRIDGE/tests/test_order_state.py       |  78 ++++++++
 3 files changed, 258 insertions(+), 111 deletions(-)
```

Exactly the same three allowed paths as both prior commits, no others.
`git diff --cached --check` was clean.

## 5. New regression tests (added to `tests/test_order_state.py`)

- `test_hostile_metaclass_name_lookup_still_raises_dedicated_error` (new) — F2-R.
- `_transitive_gc_referents` helper (test-only): bounded BFS over
  `gc.get_referents`, skipping `type` objects (to stay scoped to *data*, not
  class/module machinery), capped at 200 nodes as a runaway-graph guard.
- `test_gc_referents_of_transitions_contain_no_mutable_container` (new) — F1-R,
  asserts the transitive referent set of `ORDER_STATE_TRANSITIONS` contains
  no `dict`/`list`/`set`/`bytearray`.
- `test_gc_referents_of_transitions_cannot_alter_can_transition` (new) — F1-R,
  attempts the audit's exact mutation on every mutable referent found (none
  are found) and proves `can_transition` is unaffected.
- `test_gc_referents_of_raw_aliases_contain_no_mutable_container` (new) — F1-R, same for the raw-alias table.
- `test_gc_referents_of_raw_aliases_cannot_alter_normalization` (new) — F1-R, same for `normalize_raw_order_status`.

**RED** (these 5 tests, run against `851d88a0`'s unmodified code, before any fix):

```text
FAILED tests/test_order_state.py::test_hostile_metaclass_name_lookup_still_raises_dedicated_error
FAILED tests/test_order_state.py::test_gc_referents_of_transitions_contain_no_mutable_container
FAILED tests/test_order_state.py::test_gc_referents_of_transitions_cannot_alter_can_transition
FAILED tests/test_order_state.py::test_gc_referents_of_raw_aliases_contain_no_mutable_container
FAILED tests/test_order_state.py::test_gc_referents_of_raw_aliases_cannot_alter_normalization
5 failed, 80 passed in 0.68s
```

Each failure inspected and confirmed semantic (the metaclass `RuntimeError`
propagating uncaught; the exact backing `dict` found and successfully
poisoned) — not a typo or environment issue.

**GREEN** after the fix:

```text
python -m pytest tests/test_order_state.py -q
85 passed in 0.94s
```

80 (prior) + 5 new = 85. No test count was lowered.

## 6. Full-suite evidence (raw, both required CWDs; expected `218 + 85 = 303`)

```text
C:\TSP1001>                       python -m pytest IBKR_PAPER_BRIDGE/tests -q   -> 303 passed, 1 warning, 46.35s
C:\TSP1001\IBKR_PAPER_BRIDGE>      python -m pytest tests -q                     -> 303 passed, 1 warning, 40.77s
```

Identical count both CWDs. Compile check:

```text
python -m py_compile IBKR_PAPER_BRIDGE\bridge\engine\types.py IBKR_PAPER_BRIDGE\tests\test_order_state.py
-> exit 0 (COMPILE OK)
```

## 7. Independent 121-pair oracle re-check (fresh process, raw evidence)

Same standalone oracle script as both prior rounds (independently
constructed expected relation, not derived from `ORDER_STATE_TRANSITIONS`),
run fresh after this repair:

```text
pairs=121 legal=44 repeats=20 mismatches=[]
```

Confirms the transition relation is byte-for-byte unchanged — this repair
touched only the backing representation and the exception message, per
"Frozen behavior."

## 8. Fresh-process re-probe of both residual findings (raw evidence, post-fix)

```text
F1-R transitions: total_referents=56 mutable_found=0
F1-R raw_aliases: total_referents=20 mutable_found=0
F1-R attack attempt: FILLED->OPEN before=False after=False unaffected=True
F1-R attack attempt: normalize('OPEN') before=OrderState.OPEN after=OrderState.OPEN unaffected=True

F2-R FIXED: got UnknownRawOrderStatusError reason_code='NON_STRING_RAW_STATUS' message='NON_STRING_RAW_STATUS: raw order status could not be normalized'
ORDER_STATE_TRANSITIONS has __dict__=False
```

- A bounded transitive `gc.get_referents` walk (56 nodes for transitions, 20
  for raw aliases) found **zero** mutable containers of any kind.
- Attempting the audit's exact mutation against every referent found (a
  no-op, since none were mutable) leaves `can_transition`/
  `normalize_raw_order_status` completely unaffected.
- The exact hostile-metaclass reproduction from the re-audit no longer
  raises `RuntimeError`; it now raises `UnknownRawOrderStatusError` with
  `reason_code="NON_STRING_RAW_STATUS"` and a message containing no
  attacker-supplied text.
- Confirmed the `_ImmutableMapping` instances have no `__dict__` (i.e., the
  `__slots__` design didn't accidentally reintroduce a mutable per-instance
  dict of its own).

## 9. Frozen behavior — confirmed unchanged

Not touched: state names/meanings, all 44 legal pairs (§7 above), terminal
and same-state semantics, raw alias mappings, `PENDING → SUBMITTED`,
`PENDING_CANCEL → OPEN`, direct terminal edges, `WAITING_CHILD` exclusion,
`UNKNOWN_SUBMISSION` resolution edges, existing Pydantic model
fields/defaults/payload shape, and the PROPOSED/owner-gated status. The five
open design questions from the original build report remain unresolved by
this repair.

## 10. Contract doc updated to match repaired implementation

`docs/22_ORDER_STATE_CONTRACT.md`: extended the "Repair history" note with
the F1-R/F2-R round; rewrote the raw-to-canonical mapping section's
exception description (constant message, no `type(raw).__name__`);
rewrote invariant 6 to describe the tuple-backed `_ImmutableMapping` (not
`MappingProxyType`) and the transitive-referent guarantee explicitly;
rewrote invariant 7 for the metaclass-safe constant-message exception;
updated the test-count reference from 80 to 85.

## 11. Explicit confirmation of no out-of-scope action

No P2RT action, no API/server start, no scheduler action, no deploy, no
push, no PR created/updated/merged, no next-task (TS-P1-002) work started.
`C:\TSP0` was not touched. Only `types.py`, `test_order_state.py`, and
`22_ORDER_STATE_CONTRACT.md` changed — identical scope to both prior
commits.

## 12. Remaining owner gates

- Independent Codex re-audit of commit `a15a6b1f6648016fe99278fe993daa2c1b49b923`.
- If re-audit passes: Barış acceptance of the PROPOSED TS-P1-001 invariant
  contract, including the five still-open design questions from the
  original build report — none of which either repair round resolved or was
  authorized to resolve.
- TS-P1-002 remains blocked until both of the above complete.

## 13. Result

**READY FOR INDEPENDENT CODEX RE-AUDIT**

- New repair commit SHA: `a15a6b1f6648016fe99278fe993daa2c1b49b923`
- Exact parent SHA: `851d88a084875e48b63fba455cb7b27f357c5ac4` (verified via `git rev-parse HEAD^`)
- Focused: 85/85 passed. Full suite: 303/303 passed, identical from both
  `C:\TSP1001` and `C:\TSP1001\IBKR_PAPER_BRIDGE`.
- Repair report path: `MTC_COMMAND_CENTER/11_TRIAGE/CLAUDE_TSP1001_REPAIR2_REPORT_2026-07-20.md`
- No push/PR/merge/deploy/P2RT/next-task action was taken.
