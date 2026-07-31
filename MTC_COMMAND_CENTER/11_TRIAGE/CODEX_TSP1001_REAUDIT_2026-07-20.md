# TS-P1-001 Repair Commit Independent Re-Audit

Date: 2026-07-20  
Auditor: Codex  
Verdict: **BLOCK**

## Executive result

Repair commit `851d88a084875e48b63fba455cb7b27f357c5ac4` is a clean, correctly
scoped, one-commit child of the previously audited commit. Its new tests are
semantically RED on parent `5140e062...`, all focused and full suites are GREEN,
and the independent transition oracle still proves 44 legal pairs of 121.

The repair closes the original named-seed and hostile-`repr` examples, but it does
not close the governing contracts:

1. Both `MappingProxyType` objects still have mutable `dict` referents reachable
   through Python's standard `gc.get_referents()` API. Mutating those referents makes
   `FILLED -> OPEN` legal and remaps raw `OPEN -> FILLED` for later public calls.
2. `type(raw).__name__` is not guaranteed safe. A caller-controlled metaclass can
   override class attribute access and raise `RuntimeError`, escaping the promised
   `UnknownRawOrderStatusError` for a non-string object.

No audited-tree repair was made. TS-P1-002 remains blocked.

## Immutable target and scope

| Fact | Verified now |
| --- | --- |
| Worktree | `C:\TSP1001` |
| Branch | `feature/ts-p1-001-order-state` |
| Repaired HEAD | `851d88a084875e48b63fba455cb7b27f357c5ac4` |
| Exact parent | `5140e062b8c1f3fcc78e96c7357060c60a51285d` |
| Parent-to-HEAD count | 1 |
| Subject | `fix(bridge): close mutable policy-map backing + unsafe raw-status exception (F1/F2 repair)` |
| Pre-audit porcelain | empty |

```text
git diff --name-status 5140e062...851d88a0
M  IBKR_PAPER_BRIDGE/bridge/engine/types.py
M  IBKR_PAPER_BRIDGE/docs/22_ORDER_STATE_CONTRACT.md
M  IBKR_PAPER_BRIDGE/tests/test_order_state.py

3 files changed, 112 insertions(+), 19 deletions(-)
git diff --check: exit 0
```

The complete TS-P1-001 diff from `cfb08b81` still contains exactly the same three
allowed paths. Therefore `orders.py`, `db.py`, brokers, configuration, schemas,
migrations, strategy/risk logic, Pine, parity, and protected paths remain identical to
their applicable base. No local remote-tracking ref contains the repaired HEAD. No
network lookup, push, PR mutation, merge, deploy, or next-task action occurred.

## Builder claimed versus verified now

| Builder claim | Independent result |
| --- | --- |
| Exact new child commit and three-file scope | Verified |
| New tests RED on the audited parent | Verified: 5 failed, 75 passed |
| 80 focused tests pass | Verified twice |
| 298 full tests pass from both required CWDs | Verified |
| Compile clean | Verified |
| Transition relation remains 44/121 | Verified from the document, not the exported map |
| Old `_..._SEED` names removed | Verified |
| Original leaking/raising `__repr__` examples closed | Verified |
| No mutable backing object is caller-reachable | **Disproved** with `gc.get_referents()` |
| Copy-poisoning is the only mutation avenue | **Disproved** |
| `type(x).__name__` never invokes user-overridable code | **Disproved** with a hostile metaclass |

The builder report was treated as claims, not proof. The repository-mandated Cline
and cheap-harness inventory attempts both failed before producing usable evidence and
made no changes; all findings below were reproduced directly on the real worktree.

## Semantic RED on exact parent

A validated short throwaway worktree `C:\T1R2-68dc61eb` was created detached at
`5140e062b8c1f3fcc78e96c7357060c60a51285d`. Only the repaired focused test file was
copied over its parent version. From the throwaway `IBKR_PAPER_BRIDGE` directory:

```text
python -m pytest tests/test_order_state.py -q --tb=short -p no:cacheprovider
5 failed, 75 passed in 0.53s
exit 1
```

The five failures were semantic and exactly targeted: missing illegal-transition
reason code; leaked `repr`; exploding `repr`; named transition seed; named alias seed.
Porcelain contained only the modified focused test. The exact throwaway worktree was
removed and `Test-Path=False` afterward.

## GREEN and compile reproduction

All commands used `PYTHONUTF8=1`, `PYTHONDONTWRITEBYTECODE=1`, and disabled pytest's
cache provider.

From `C:\TSP1001`:

```text
python -m pytest IBKR_PAPER_BRIDGE/tests/test_order_state.py -q -p no:cacheprovider
80 passed in 0.29s

python -m pytest IBKR_PAPER_BRIDGE/tests -q -p no:cacheprovider
298 passed, 1 warning in 46.65s
```

From `C:\TSP1001\IBKR_PAPER_BRIDGE`:

```text
python -m pytest tests -q -p no:cacheprovider
298 passed, 1 warning in 47.25s

python -m pytest tests/test_order_state.py -q -p no:cacheprovider
80 passed in 0.26s

python -m py_compile bridge/engine/types.py tests/test_order_state.py
exit 0; no output
```

Both full runs produced the same pre-existing `StarletteDeprecationWarning`. No
order-dependent failure was observed.

## Independent transition oracle and twelve probes

The oracle parsed the repaired Markdown transition table, constructed its own expected
edge set plus documented self edges, and compared every public API pair twenty times.
It did not derive expected results from `ORDER_STATE_TRANSITIONS`.

```text
pairs=121 legal=44 repeats=20 mismatches=[]
```

1. **PASS — Exhaustive pair totality:** 121 stable pairs, 44 legal, zero mismatch.
2. **PASS — Terminal resurrection:** no non-self edge from any terminal state.
3. **PASS — Unknown blind retry:** no edge to `PENDING_NEW` or `SUBMITTING`.
4. **PASS — Progress regression:** partial fill cannot regress to ordinary live states.
5. **PASS — Cancel/fill race:** documented authoritative outcomes allowed; fallbacks denied.
6. **PASS — Same-state replay:** all eleven self edges; normal calls do not mutate policy.
7. **PASS — Ordinary raw abuse:** known aliases exact; garbage, whitespace, near misses,
   `None`, bool, number, bytes, and a plain object fail closed. The hostile-metaclass
   exception is Finding F2-R.
8. **FAIL — Mutability attack:** the named seeds are gone, but standard-library GC
   exposes one mutable dict behind each proxy and mutation changes later decisions.
9. **PASS — Serialization:** enum JSON round-trips and legacy model payload shapes hold.
10. **PASS — Status coverage:** all actual lifecycle literals mapped; `WAITING_CHILD` deferred.
11. **PASS — Future-task boundary:** repair remains within the same three TS-P1-001 files.
12. **PASS — No mutation:** final evidence is recorded below.

## Findings

### F1-R — BLOCK/P0: the mutable backing policy remains caller-reachable

`bridge/engine/types.py:143` and `:258` inline mutable dictionary literals into
`MappingProxyType`. This removes module names, but the proxy still holds each mutable
dict as a referent. Python's standard `gc` module returns that referent directly.

Fresh-process reproduction, with original entries restored in `finally`:

```text
named_seeds_absent=True
gc_dict_referents=1/1
before: FILLED->OPEN=False, raw OPEN=OrderState.OPEN
after:  FILLED->OPEN=True,  raw OPEN=OrderState.FILLED
policy_changed=True
```

This directly contradicts the current contract at
`docs/22_ORDER_STATE_CONTRACT.md:162-164`, which says no caller-reachable mutable
object backs either policy map, and the repair report's statements that no reference
remains except inside the proxy and copy-poisoning is the only available mutation
avenue. The new tests at `tests/test_order_state.py:314-335` scan module attributes and
mutate copies only; they do not inspect or attack the proxy's actual referent.

The governing audit rule explicitly makes a mutable policy surface BLOCK. This is not
module-variable rebinding, `ctypes`, or memory corruption; it uses a documented Python
standard-library introspection API against the exported policy objects.

### F2-R — BLOCK/P1: non-string normalization can still escape its dedicated error

`bridge/engine/types.py:252` builds the error message with
`type(raw).__name__`. Accessing `__name__` on a class is dispatched through its
metaclass and can execute caller-controlled code. Fresh-process reproduction:

```python
class HostileMeta(type):
    def __getattribute__(cls, name):
        if name == "__name__":
            raise RuntimeError("metaclass name exploded")
        return super().__getattribute__(name)

class Hostile(metaclass=HostileMeta):
    pass
```

```text
normalize_raw_order_status(Hostile())
=> RuntimeError: metaclass name exploded
reason_code=None
```

This contradicts `docs/22_ORDER_STATE_CONTRACT.md:170-174`, the repair requirement
that every non-string object deterministically raises `UnknownRawOrderStatusError`,
and the repair report's claim that `type(x).__name__` never invokes user-overridable
code. The original `Leaky.__repr__` and `Exploding.__repr__` cases do pass now, and
`IllegalOrderTransitionError.reason_code == "ILLEGAL_ORDER_TRANSITION"` is correct;
those narrower fixes do not satisfy the broader exception guarantee.

## Contract and governance review

The state vocabulary, meanings, 44-pair table, terminal/same-state semantics, raw
alias mapping, quantity limitation, task boundaries, rollback, and PROPOSED owner gate
remain correct and unchanged. UNKNOWN recovery remains deferred to TS-P1-003, durable
identity to TS-P1-002, and partial protect-or-flatten to TS-P1-004. The two repaired
immutability/exception invariants are the only remaining blockers reproduced here.

ADR-0023 is Accepted, but this PROPOSED invariant contract still requires independent
technical PASS and explicit Baris acceptance.

## Final no-mutation and P2RT evidence

Pre-audit hashes:

```text
types.py  7E195FDC902C34E07A5BF1CB26FFC18EEC7BC3FD0AFC1A68712AEE454ACCC81A
test      941260784AE10EFC742C00D2C4CC221493E513D1DBB5A5CCFB51F64C52DCB9CC
contract  985B14A856D97EF1BA52B5664CEB0236933605A460AF09475FE14C9A6932B8F9
```

Final evidence: audited HEAD remained
`851d88a084875e48b63fba455cb7b27f357c5ac4`, porcelain empty, and all three hashes
exactly matched the pre-audit values above. Main-worktree unrelated state remained
131 entries with digest
`0DAE657FAE94BF12CE2D681A6C18AECC803B97590592BC9150689D8B93AAEC74`.
P2RT post-snapshot remained HEAD
`008e065e8e0ffa68f46134da6698d58f91ef2dcb`, porcelain empty.

P2RT pre-snapshot was HEAD `008e065e8e0ffa68f46134da6698d58f91ef2dcb`,
porcelain empty. Post-snapshot is included in final evidence. No P2RT API/status GET,
Task Scheduler, process, database, exchange, credential, ARM/DISARM, or deploy action
occurred.

## Verdict and sequence management

**BLOCK.** The repair commit is not eligible for owner acceptance or TS-P1-002
sequencing despite its clean scope and GREEN suites.

The only next-session prompt is
`MTC_COMMAND_CENTER/11_TRIAGE/CLAUDE_TSP1001_REPAIR2_PROMPT_2026-07-20.md`.
It is limited to F1-R/F2-R, requires a new child repair commit, and then stops for a
fresh independent Codex re-audit. No TS-P1-002 prompt was created.

Exact owner decision still required: **Baris must accept or reject the PROPOSED
TS-P1-001 invariant contract only after a repair commit passes independent Codex
re-audit; until then TS-P1-002 remains blocked.**
