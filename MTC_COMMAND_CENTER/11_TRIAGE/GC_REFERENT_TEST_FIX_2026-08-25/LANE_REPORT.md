# GC Referent Test Fix Lane Report - 2026-08-25

Role: Codex implementer under live Claude lead.

Branch: `fix/gc-referent-tests-20260825`

Audit tier classification: T1. This lane changed Bridge test code only. It did not touch product code, deploy/host scripts, credentials, Pine, parity, schemas, broker/exchange behavior, or trading logic. The live Claude lead owns independent acceptance.

## Diagnosis Confirmation

I read the required diagnosis from:

`feature/wp-p0-27-ci-home-20260825:MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_27_CI_HOME_2026-08-25/LINUX_RED_DIAGNOSIS.md`

The branch path in the dispatch brief omitted the `MTC_COMMAND_CENTER/11_TRIAGE/` prefix; the file exists at the path above.

I confirmed the diagnosis against `IBKR_PAPER_BRIDGE/tests/test_order_state.py` and `IBKR_PAPER_BRIDGE/bridge/engine/types.py`: the two red tests were asserting that the full transitive CPython GC referent graph contains no mutable containers. That overreaches the invariant. On CPython 3.12, `gc.get_referents(OrderState.MEMBER)` can expose Enum member implementation dictionaries; those dictionaries are runtime-owned Enum internals, not mutable policy backing data for `ORDER_STATE_TRANSITIONS` or `RAW_ORDER_STATUS_ALIASES`. The adjacent behavior-changing attack tests remain sound and were preserved.

## Fix

Changed only `IBKR_PAPER_BRIDGE/tests/test_order_state.py`.

The GC traversal now treats `Enum` members as runtime-owned atomic values, the same way it already treated classes as traversal boundaries:

```python
from enum import Enum

...

if isinstance(referent, (type, Enum)):
    continue
```

This keeps mutable policy containers visible. If the holder owns a `dict`, `list`, `set`, or `bytearray`, the repaired tests still collect it and fail. It only prevents traversal into Enum member implementation state, so the assertion no longer depends on whether a specific CPython version exposes `OrderState.OPEN.__dict__` through `gc.get_referents`.

Local version observation:

```text
python -c "import gc, sys; from IBKR_PAPER_BRIDGE.bridge.engine.types import OrderState; refs=gc.get_referents(OrderState.OPEN); print(sys.version); print(any(r is OrderState.OPEN.__dict__ for r in refs)); print([type(r).__name__ for r in refs[:10]])"

3.14.2 (tags/v3.14.2:df79316, Dec  5 2025, 17:18:21) [MSC v.1944 64 bit (AMD64)]
False
['str', 'str', 'EnumType', 'int', 'EnumType']
```

The diagnosis records CPython 3.12 CI exposing the Enum member dictionary. The repaired helper stops at the Enum member before that version-specific detail can matter.

Extra interpreter check:

```text
py -0p

 -V:3.14 *        C:\Python314\python.exe
 -V:3.13          C:\Users\BarışSemaay\AppData\Local\Microsoft\WindowsApps\PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0\python.exe
 -V:Astral/CPython3.13.13 C:\Users\BarışSemaay\AppData\Roaming\uv\python\cpython-3.13.13-windows-x86_64-none\python.exe
```

The 3.13.13 interpreter could not run pytest here:

```text
& 'C:\Users\BarışSemaay\AppData\Roaming\uv\python\cpython-3.13.13-windows-x86_64-none\python.exe' -m pytest IBKR_PAPER_BRIDGE/tests/test_order_state.py::test_gc_referents_of_transitions_contain_no_mutable_container IBKR_PAPER_BRIDGE/tests/test_order_state.py::test_gc_referents_of_raw_aliases_contain_no_mutable_container -q

C:\Users\BarışSemaay\AppData\Roaming\uv\python\cpython-3.13.13-windows-x86_64-none\python.exe: No module named pytest
```

## D026 RED/GREEN Evidence

Scratch copy used for mutations:

`C:\tmp\gc_ref_d026_20260825_1430`

Scratch baseline after copying the repaired tests:

```text
python -m pytest tests/test_order_state.py::test_gc_referents_of_transitions_contain_no_mutable_container tests/test_order_state.py::test_gc_referents_of_raw_aliases_contain_no_mutable_container -q

..                                                                       [100%]
2 passed in 1.02s
```

### Transition Referent Test

Scratch mutation in `bridge/engine/types.py`:

```diff
-(OrderState.FILLED, frozenset({OrderState.FILLED})),
+(OrderState.FILLED, {OrderState.FILLED}),
```

RED:

```text
python -m pytest tests/test_order_state.py::test_gc_referents_of_transitions_contain_no_mutable_container -q

F                                                                        [100%]
================================== FAILURES ===================================
________ test_gc_referents_of_transitions_contain_no_mutable_container ________

    def test_gc_referents_of_transitions_contain_no_mutable_container():
        referents = _transitive_gc_referents(ORDER_STATE_TRANSITIONS)
        mutable = [r for r in referents if isinstance(r, (dict, list, set, bytearray))]
>       assert mutable == []
E       AssertionError: assert [{<OrderState...D: 'FILLED'>}] == []
E
E         Left contains one more item: {<OrderState.FILLED: 'FILLED'>}
E         Use -v to get more diff

tests\test_order_state.py:402: AssertionError
=========================== short test summary info ===========================
FAILED tests/test_order_state.py::test_gc_referents_of_transitions_contain_no_mutable_container
1 failed in 1.24s
```

Restored mutation:

```diff
-(OrderState.FILLED, {OrderState.FILLED}),
+(OrderState.FILLED, frozenset({OrderState.FILLED})),
```

GREEN:

```text
python -m pytest tests/test_order_state.py::test_gc_referents_of_transitions_contain_no_mutable_container -q

.                                                                        [100%]
1 passed in 0.86s
```

### Raw-Alias Referent Test

Scratch mutation in `bridge/engine/types.py`:

```diff
-("OPEN", OrderState.OPEN),
+["OPEN", OrderState.OPEN],
```

RED:

```text
python -m pytest tests/test_order_state.py::test_gc_referents_of_raw_aliases_contain_no_mutable_container -q

F                                                                        [100%]
================================== FAILURES ===================================
________ test_gc_referents_of_raw_aliases_contain_no_mutable_container ________

    def test_gc_referents_of_raw_aliases_contain_no_mutable_container():
        referents = _transitive_gc_referents(RAW_ORDER_STATUS_ALIASES)
        mutable = [r for r in referents if isinstance(r, (dict, list, set, bytearray))]
>       assert mutable == []
E       AssertionError: assert [['OPEN', <Or...PEN: 'OPEN'>]] == []
E
E         Left contains one more item: ['OPEN', <OrderState.OPEN: 'OPEN'>]
E         Use -v to get more diff

tests\test_order_state.py:420: AssertionError
=========================== short test summary info ===========================
FAILED tests/test_order_state.py::test_gc_referents_of_raw_aliases_contain_no_mutable_container
1 failed in 0.76s
```

Restored mutation:

```diff
-["OPEN", OrderState.OPEN],
+("OPEN", OrderState.OPEN),
```

GREEN:

```text
python -m pytest tests/test_order_state.py::test_gc_referents_of_raw_aliases_contain_no_mutable_container -q

.                                                                        [100%]
1 passed in 0.42s
```

## Verification

Focused repaired tests:

```text
python -m pytest IBKR_PAPER_BRIDGE/tests/test_order_state.py::test_gc_referents_of_transitions_contain_no_mutable_container IBKR_PAPER_BRIDGE/tests/test_order_state.py::test_gc_referents_of_raw_aliases_contain_no_mutable_container -q

..                                                                       [100%]
2 passed in 1.07s
```

Adjacent behavior-changing attack tests:

```text
python -m pytest IBKR_PAPER_BRIDGE/tests/test_order_state.py::test_gc_referents_of_transitions_cannot_alter_can_transition IBKR_PAPER_BRIDGE/tests/test_order_state.py::test_gc_referents_of_raw_aliases_cannot_alter_normalization -q

..                                                                       [100%]
2 passed in 0.41s
```

Required full file:

```text
python -m pytest IBKR_PAPER_BRIDGE/tests/test_order_state.py -q

........................................................................ [ 52%]
.................................................................        [100%]
137 passed in 1.69s
```

Whole Bridge suite:

```text
python -m pytest tests -q --ignore=TSP1009B.pytest_tmp_s1r1

1370 passed, 1 warning in 182.06s (0:03:02)
```

Warning summary:

```text
..\..\Users\BarışSemaay\AppData\Roaming\Python\Python314\site-packages\fastapi\testclient.py:1
  C:\Users\BarışSemaay\AppData\Roaming\Python\Python314\site-packages\fastapi\testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
    from starlette.testclient import TestClient as TestClient  # noqa
```

Diff scope before report:

```text
git diff --stat

IBKR_PAPER_BRIDGE/tests/test_order_state.py | 10 ++++++----
1 file changed, 6 insertions(+), 4 deletions(-)
```

`git diff --check` exited 0.

No Claude CLI was launched or authenticated by this lane. A process check observed pre-existing `claude` processes on the host, including Claude Code processes parented outside this Codex shell; I did not start or interact with them.

CodeBurn at close:

```text
Today  $341.38  1483 calls    Month  $3509.23  13734 calls
```

## Final Commit SHA

The actual pushed branch-tip SHA is printed by the implementer after commit and push. A Git commit cannot contain its own final SHA inside a tracked file without changing that SHA.
