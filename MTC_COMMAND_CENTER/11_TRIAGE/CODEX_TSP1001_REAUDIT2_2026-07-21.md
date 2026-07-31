# TS-P1-001 Second-Repair Independent Re-Audit

Date: 2026-07-21  
Auditor: Codex  
Verdict: **BLOCK**

## Executive result

Commit `a15a6b1f6648016fe99278fe993daa2c1b49b923` is a clean, correctly scoped,
one-commit child of `851d88a084875e48b63fba455cb7b27f357c5ac4`. The repaired tests are
semantically RED on that parent, 85 focused and both 303-test complete suites are
GREEN, compile is clean, and the document-derived oracle still proves 44 legal pairs
of 121.

F2-R is closed: hostile instance representation and hostile metaclass attacks now
raise the dedicated constant-message `UnknownRawOrderStatusError`.

F1-R remains open. `_ImmutableMapping` stores its tuple in a writable `_pairs` slot.
A caller can assign a replacement tuple directly to either exported mapping and make
`FILLED -> OPEN` legal or raw `OPEN` normalize to `FILLED`. Tuple contents are
immutable and the GC closure contains no mutable containers, but the policy holder
object itself is mutable. This is a mandatory mutable-policy-surface BLOCK.

No repair was made in this audit pass. TS-P1-002 remains blocked.

## Immutable target and scope

| Fact | Verified now |
| --- | --- |
| Worktree | `C:\TSP1001` |
| Branch | `feature/ts-p1-001-order-state` |
| Audited HEAD | `a15a6b1f6648016fe99278fe993daa2c1b49b923` |
| Exact parent | `851d88a084875e48b63fba455cb7b27f357c5ac4` |
| Parent-to-HEAD count | 1 |
| Commit subject | `fix(bridge): true immutable Mapping + metaclass-safe error (F1-R/F2-R repair)` |
| Pre-audit porcelain | empty |

```text
git diff --name-status 851d88a0..a15a6b1f
M  IBKR_PAPER_BRIDGE/bridge/engine/types.py
M  IBKR_PAPER_BRIDGE/docs/22_ORDER_STATE_CONTRACT.md
M  IBKR_PAPER_BRIDGE/tests/test_order_state.py

3 files changed, 258 insertions(+), 111 deletions(-)
git diff --check: exit 0
```

The full task diff from `cfb08b81` still contains exactly the same three allowed
paths. No protected, broker, persistence, migration, strategy/risk, Pine, parity,
schema, or configuration path changed. No local remote-tracking ref contains HEAD.
No external network, push, PR mutation, merge, deploy, or next-task action occurred.

## Builder claimed versus verified now

| Builder claim | Independent result |
| --- | --- |
| Exact child commit and three-file scope | Verified |
| New tests RED on parent | Verified: 5 failed, 80 passed |
| 85 focused tests pass | Verified twice |
| 303 full tests pass from both required CWDs | Verified |
| Compile clean | Verified |
| Transition relation unchanged at 44/121 | Verified independently from contract |
| GC closure has no mutable container | Verified: 56/20 referents, zero dict/list/set/bytearray |
| Hostile metaclass cannot escape the dedicated error | Verified |
| Exported mappings are unbreakably immutable | **Disproved: `_pairs` can be rebound** |

The required Cline inspection failed before starting because its local session was
missing. The cheap-harness fallback was unable to read the allowlisted files and
produced no usable evidence. Neither wrote repository files. All results below were
independently reproduced on the real worktree.

## Semantic RED on exact parent

A validated short throwaway worktree `C:\T1R3-8461a280` was created detached at
`851d88a084875e48b63fba455cb7b27f357c5ac4`. Only the updated focused test was
copied over the parent version.

```text
python -m pytest tests/test_order_state.py -q --tb=short -p no:cacheprovider
5 failed, 80 passed in 0.54s
exit 1
```

Failures were the intended hostile-metaclass case plus four GC-referent assertions.
Porcelain contained only the modified focused test. The exact throwaway worktree was
removed; `Test-Path=False` afterward.

## GREEN and compile reproduction

All test commands used `PYTHONUTF8=1`, `PYTHONDONTWRITEBYTECODE=1`, and disabled the
pytest cache provider.

From `C:\TSP1001`:

```text
focused: 85 passed in 0.33s
full:    303 passed, 1 warning in 34.55s
```

From `C:\TSP1001\IBKR_PAPER_BRIDGE`:

```text
full:    303 passed, 1 warning in 35.62s
focused: 85 passed in 0.29s
py_compile bridge/engine/types.py tests/test_order_state.py: exit 0
```

The warning was the same pre-existing `StarletteDeprecationWarning`. No
order-dependent failure was observed.

## Independent oracle and twelve probes

The audit parsed the Markdown transition table, constructed an independent expected
set plus documented self edges, and compared all public API pairs twenty times:

```text
pairs=121 legal=44 repeats=20 mismatches=[]
```

1. **PASS — Totality:** 121 stable pairs, 44 legal, zero mismatch.
2. **PASS — Terminal resurrection:** no terminal non-self edge.
3. **PASS — Unknown blind retry:** no edge to intent/submitting.
4. **PASS — Progress regression:** partial fill cannot regress to ordinary live states.
5. **PASS — Cancel/fill race:** authoritative outcomes allowed; fallbacks denied.
6. **PASS — Same-state replay:** all eleven self edges; ordinary calls are pure.
7. **PASS — Raw abuse:** known aliases exact; malformed and non-string inputs fail closed.
8. **FAIL — Mutability:** GC containers are clean, but direct `_pairs` assignment changes
   both later transition and normalization decisions.
9. **PASS — Serialization:** enum JSON and legacy Pydantic payload shapes unchanged.
10. **PASS — Status coverage:** all lifecycle literals mapped; `WAITING_CHILD` deferred.
11. **PASS — Future-task boundary:** exact same three-file TS-P1-001 scope.
12. **PASS — No mutation:** final evidence below.

## Finding F1-R2 — BLOCK/P0: tuple storage is held in a writable slot

`bridge/engine/types.py:140-173` defines a normal Python object with
`__slots__ = ("_pairs",)` and assigns `self._pairs` in `__init__`. `__slots__`
removes the instance dictionary; it does not make a slot read-only. Fresh-process
reproduction, restoring the original tuples in `finally`:

```text
ORDER_STATE_TRANSITIONS._pairs = ((FILLED, {FILLED, OPEN}),)
FILLED -> OPEN: False before, True after

RAW_ORDER_STATUS_ALIASES._pairs = (("OPEN", FILLED),)
raw OPEN: OrderState.OPEN before, OrderState.FILLED after
```

This uses direct ordinary attribute assignment—no module-variable rebinding,
`ctypes`, class monkeypatching, or memory corruption.

The tests at `tests/test_order_state.py:365-419` inspect transitive referents and try
to mutate only `dict`/`list` objects. They never attack the exported holder's writable
slot. The contract at `docs/22_ORDER_STATE_CONTRACT.md:166-181` correctly says tuples
cannot be mutated *in place*, but incorrectly concludes that the exported policy is
immutable; the tuple reference can be replaced wholesale. The repair report likewise
confuses an immutable stored value and absence of `__dict__` with an immutable holder.

F2-R is independently closed:

```text
Hostile metaclass + exploding repr
=> UnknownRawOrderStatusError
reason_code=NON_STRING_RAW_STATUS
message=NON_STRING_RAW_STATUS: raw order status could not be normalized
```

## Governance and verdict

The state vocabulary, 44-pair table, raw aliases, terminal/replay rules, quantity
limitation, task boundaries, rollback, and PROPOSED owner gate remain correct. UNKNOWN
recovery remains TS-P1-003, durable identity TS-P1-002, and partial protection
TS-P1-004.

**BLOCK.** The only next prompt is
`MTC_COMMAND_CENTER/11_TRIAGE/CLAUDE_TSP1001_REPAIR3_PROMPT_2026-07-21.md`.
It fixes only the writable-holder issue and requires another child commit plus
independent re-audit. No TS-P1-002 prompt was created.

Pre-audit hashes:

```text
types.py  1430D03CE9E6A2CF3ACBFA32E5C286671A2B769C13F2C48EE79FC638368359CD
test      AB1195F6922E4F6E7B797CDAB0338BB26ECCC7A2CCBD8809DF7D54C30F8B718B
contract  FD1A7B0E8EB0B2A5F21414A394684F17E537561080002B866902ADFB115CE456
```

Final no-mutation/P2RT evidence: audited HEAD remained
`a15a6b1f6648016fe99278fe993daa2c1b49b923`, porcelain empty, and all three hashes
exactly matched the pre-audit values. Main unrelated state remained 134 entries with
digest `3D7BBE889427A0FDC1B15DA5F8CDF143D476EC09F1F70A7B29FFF78AFCCE242D`.
P2RT remained HEAD `008e065e8e0ffa68f46134da6698d58f91ef2dcb`, porcelain empty; only the
permitted pre/post Git identity snapshots were taken.

Exact owner decision still required: **Baris must accept or reject the PROPOSED
TS-P1-001 invariant contract only after a repair passes independent Codex re-audit;
until then TS-P1-002 remains blocked.**
