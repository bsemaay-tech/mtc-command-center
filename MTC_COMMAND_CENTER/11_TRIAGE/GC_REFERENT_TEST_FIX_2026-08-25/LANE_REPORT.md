# GC Referent Test Fix Lane Report - 2026-08-25

Role: Codex implementer under live Claude lead.

Branch: `fix/gc-referent-tests-20260825`

Audit tier classification: T1. This lane changed Bridge test code plus one product docstring that was rechecked and found inaccurate after the new helper behavior. It did not touch deploy/host scripts, credentials, Pine, parity, schemas, broker/exchange behavior, or trading logic. The live Claude lead owns independent acceptance.

## Replacement Applied

Changed `IBKR_PAPER_BRIDGE/tests/test_order_state.py` from stopping traversal at every `Enum` member to traversing Enum members while skipping only the small Enum-internal member dictionary:

```python
_ENUM_INTERNAL_KEYS = frozenset({"_value_", "_name_", "__objclass__", "_sort_order_"})

...

if isinstance(referent, type):
    continue
if isinstance(referent, dict) and set(referent) <= _ENUM_INTERNAL_KEYS:
    continue
```

This is strictly better than the previous fix because mutable containers owned by the immutable mapping holder still remain visible, and mutable containers reachable only through an `Enum` member are visible again. The helper now ignores only the runtime-owned Enum internal dictionary that made the original assertion depend on interpreter internals.

Local referent probe after the change:

```text
python -c "import tests.test_order_state as t; refs=t._transitive_gc_referents(t.ORDER_STATE_TRANSITIONS); print('count', len(refs)); print('types', sorted({type(r).__name__ for r in refs})); print('order_states', sum(isinstance(r, t.OrderState) for r in refs)); print('mutable', [type(r).__name__ for r in refs if isinstance(r, (dict, list, set, bytearray))])"

count 55
types ['OrderState', 'frozenset', 'int', 'str', 'tuple']
order_states 11
mutable []
```

## Version Boundary Correction

The prior report understated the exposure as CPython 3.12-specific. The auditor verified the Enum-member coverage loss on 3.12, 3.13, and 3.14. I also checked the local 3.13.13 interpreter with a standalone `str, Enum` member:

```text
& 'C:\Users\BarışSemaay\AppData\Roaming\uv\python\cpython-3.13.13-windows-x86_64-none\python.exe' -c "import gc, sys; from enum import Enum; Status = Enum('Status', {'OPEN': 'OPEN'}, type=str); refs=gc.get_referents(Status.OPEN); print(sys.version); print(any(r is Status.OPEN.__dict__ for r in refs)); print([type(r).__name__ for r in refs])"

3.13.13 (main, Jun  2 2026, 22:38:31) [MSC v.1944 64 bit (AMD64)]
True
['dict', 'EnumType']
```

The same local 3.13.13 interpreter still cannot run the Bridge pytest nodes because it lacks `pydantic`; no 3.13 pytest result is claimed from this lane.

## Blind-Spot RED/GREEN

Temporary product mutation used to prove the auditor's blind spot is closed:

```python
OrderState.FILLED.poisoned_policy = {OrderState.FILLED: frozenset({OrderState.OPEN})}
```

This creates a genuinely mutable policy container reachable only through `OrderState.FILLED`.

RED:

```text
python -m pytest tests/test_order_state.py::test_gc_referents_of_transitions_contain_no_mutable_container -q

F                                                                        [100%]
FAILED tests/test_order_state.py::test_gc_referents_of_transitions_contain_no_mutable_container
E       AssertionError: assert [{<OrderState...N: 'OPEN'>})}] == []
E         Left contains one more item: {<OrderState.FILLED: 'FILLED'>: frozenset({<OrderState.OPEN: 'OPEN'>})}
1 failed in 0.53s
```

GREEN after restoring the temporary mutation:

```text
python -m pytest tests/test_order_state.py::test_gc_referents_of_transitions_contain_no_mutable_container -q

.                                                                        [100%]
1 passed in 0.38s
```

## Original D026 RED/GREEN

Repeated the prior mutation:

```diff
-(OrderState.FILLED, frozenset({OrderState.FILLED})),
+(OrderState.FILLED, {OrderState.FILLED}),
```

RED:

```text
python -m pytest tests/test_order_state.py::test_gc_referents_of_transitions_contain_no_mutable_container -q

F                                                                        [100%]
FAILED tests/test_order_state.py::test_gc_referents_of_transitions_contain_no_mutable_container
E       AssertionError: assert [{<OrderState...D: 'FILLED'>}] == []
E         Left contains one more item: {<OrderState.FILLED: 'FILLED'>}
1 failed in 0.63s
```

GREEN after restoring `frozenset({OrderState.FILLED})`:

```text
python -m pytest tests/test_order_state.py::test_gc_referents_of_transitions_contain_no_mutable_container -q

.                                                                        [100%]
1 passed in 0.52s
```

## Corrected Statements

- The old statement "This keeps mutable policy containers visible" was incomplete. Accurate replacement: holder-owned mutable containers remain visible, and Enum-member-owned mutable containers are visible again; only Enum-internal dictionaries with keys contained in `_ENUM_INTERNAL_KEYS` are skipped.
- The old CPython 3.12-only attribution was wrong. The exposure is not bounded to 3.12; the auditor verified it on 3.12, 3.13, and 3.14, and the local standalone 3.13.13 check exposes the member dictionary.
- `IBKR_PAPER_BRIDGE/bridge/engine/types.py` docstring was rechecked under the new helper behavior. It was still slightly wrong because the traversal reaches Enum `_sort_order_` `int` values. I corrected the docstring from "tuples, `frozenset`s, and `OrderState`/`str` values" to "tuples, `frozenset`s, `int`s, and `OrderState`/`str` values".

## Verification

Focused repaired tests:

```text
python -m pytest tests/test_order_state.py::test_gc_referents_of_transitions_contain_no_mutable_container tests/test_order_state.py::test_gc_referents_of_raw_aliases_contain_no_mutable_container -q

..                                                                       [100%]
2 passed in 0.42s
```

Adjacent behavior-changing GC attack tests:

```text
python -m pytest tests/test_order_state.py::test_gc_referents_of_transitions_cannot_alter_can_transition tests/test_order_state.py::test_gc_referents_of_raw_aliases_cannot_alter_normalization -q

..                                                                       [100%]
2 passed in 0.42s
```

Full order-state file:

```text
python -m pytest tests/test_order_state.py -q

........................................................................ [ 52%]
.................................................................        [100%]
137 passed in 1.58s
```

Whole Bridge suite:

```text
python -m pytest tests -q --ignore=TSP1009B.pytest_tmp_s1r1

1370 passed, 1 warning in 157.18s (0:02:37)
```

Warning summary:

```text
C:\Users\BarışSemaay\AppData\Roaming\Python\Python314\site-packages\fastapi\testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
```

No Claude CLI was launched or authenticated by this lane. A process check observed pre-existing `claude` processes on the host, including Claude Code processes outside this Codex shell; I did not start or interact with them.

CodeBurn at start:

```text
Today  $349.73  1526 calls    Month  $3517.58  13777 calls
```

CodeBurn at close:

```text
Today  $355.89  1574 calls    Month  $3523.74  13825 calls
```

## Final Commit SHA

The actual pushed branch-tip SHA is printed by the implementer after commit and push. A Git commit cannot contain its own final SHA inside a tracked file without changing that SHA.
