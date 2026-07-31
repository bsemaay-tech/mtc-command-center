# TS-P1-001 Independent Adversarial Audit

Date: 2026-07-20  
Auditor: Codex  
Verdict: **BLOCK**

## Executive result

Claude's commit is clean, correctly scoped, semantically RED against its exact
parent, and GREEN for both the focused and complete bridge suites. An independent
oracle also confirms that the documented table and public API agree on all 121
ordered state pairs and exactly 44 legal pairs.

The commit nevertheless fails the acceptance gate:

1. The two supposedly immutable policy maps retain module-visible mutable backing
   dictionaries. A caller can mutate those dictionaries and make `FILLED -> OPEN`
   legal or make raw `OPEN` normalize to `FILLED` for later calls.
2. Illegal-transition errors are not reason-coded, and raw-status error construction
   interpolates arbitrary object `repr`. A hostile object can leak its representation
   or raise `RuntimeError` instead of the promised dedicated fail-closed exception.

No repair was made in this audit pass. TS-P1-002 must not start.

## Immutable target

| Fact | Verified now |
| --- | --- |
| Expected worktree | `C:\TSP1001` |
| Branch | `feature/ts-p1-001-order-state` |
| Base | `cfb08b819aa9890725344e8315571299718cd554` |
| Audited HEAD | `5140e062b8c1f3fcc78e96c7357060c60a51285d` |
| Commit subject | `feat(bridge): define canonical order-state invariants` |
| Descendant count | exactly 1 |
| Merge-base ancestry | base is an ancestor of HEAD; exit 0 |
| Audited porcelain before tests | empty |

Representative preflight commands:

```powershell
git -C C:\TSP1001 rev-parse --show-toplevel HEAD HEAD^ --abbrev-ref HEAD
git -C C:\TSP1001 merge-base --is-ancestor cfb08b819aa9890725344e8315571299718cd554 HEAD
git -C C:\TSP1001 rev-list --count cfb08b819aa9890725344e8315571299718cd554..HEAD
git -C C:\TSP1001 status --porcelain=v1
git -C C:\TSP1001 log -1 --format=%s
```

## Builder claimed versus verified now

| Claim | Independent result |
| --- | --- |
| One clean descendant commit on the expected branch/base | Verified |
| Exactly three allowed changed files | Verified |
| 74 focused tests pass | Verified twice |
| 292 full tests pass from both required CWDs | Verified |
| Changed Python compiles | Verified |
| Focused tests are semantically RED on the parent | Verified by a fresh throwaway worktree |
| Transition relation has 44 legal pairs of 121 | Verified with a doc-derived oracle |
| Exported policies are immutable | **Disproved**; mutable backing seeds alter later decisions |
| Errors meet the structured fail-closed contract | **Disproved**; illegal error lacks a reason code and hostile `repr` escapes the raw-status error |

Items in Claude's prompt/report were treated as specification and claims, never as
proof.

## Scope and repository evidence

```text
git diff --name-status cfb08b819aa9890725344e8315571299718cd554..5140e062b8c1f3fcc78e96c7357060c60a51285d
M  IBKR_PAPER_BRIDGE/bridge/engine/types.py
A  IBKR_PAPER_BRIDGE/docs/22_ORDER_STATE_CONTRACT.md
A  IBKR_PAPER_BRIDGE/tests/test_order_state.py

git diff --stat ...
3 files changed, 709 insertions(+), 1 deletion(-)
```

`git diff --check` was clean. A complement check over the complete changed-path list
found no fourth path. Targeted base comparisons were empty for `orders.py`, `db.py`,
broker adapters, configuration, schemas, migrations, strategy/risk logic, Pine,
parity, and protected paths. No local remote-tracking ref contains the audited HEAD.
This is local evidence only; no external network lookup was required or performed.
No push, PR mutation, merge, deploy, or next-task action was performed by this audit.

## Independent raw-status inventory

An AST-assisted literal survey plus direct inspection of `bridge/` and `tests/`
confirmed the lifecycle spellings below:

| Existing spelling | Current role | Contract result |
| --- | --- | --- |
| `OPEN` | broker/model default, mock producer, consumers/tests | mapped to `OPEN` |
| `SUBMITTED` | store/test injection; live-set consumers | mapped to `SUBMITTED` |
| `PENDING` | reserved/legacy live-set consumer; no producer found | explicitly mapped to `SUBMITTED` with rationale |
| `FILLED` | mock/fill completion producer; store/tests | mapped to `FILLED` |
| `CANCELLED_BY_ENGINE` | mock cancel producer | mapped to `CANCELED` |
| `WAITING_CHILD` | adapter-internal reconciliation dict | explicitly excluded/deferred; not persisted as `BrokerOrder.status` |

Decision-stage `SUBMITTED`/`REJECTED` values are a separate axis and are explicitly
excluded. The current Hyperliquid adapter still has a pre-existing permissive `OPEN`
fallback and string pass-through; the contract honestly defers wiring/removal of that
risk. No silent literal orphan was reproduced within this task's stated inventory.

## GREEN reproduction

Environment for every pytest command: `PYTHONUTF8=1`,
`PYTHONDONTWRITEBYTECODE=1`; pytest cache provider disabled to reduce audit residue.

From `C:\TSP1001`:

```text
python -m pytest IBKR_PAPER_BRIDGE/tests/test_order_state.py -q -p no:cacheprovider
74 passed in 0.52s

python -m pytest IBKR_PAPER_BRIDGE/tests -q -p no:cacheprovider
292 passed, 1 warning in 46.89s
```

From `C:\TSP1001\IBKR_PAPER_BRIDGE`:

```text
python -m pytest tests -q -p no:cacheprovider
292 passed, 1 warning in 44.03s

python -m pytest tests/test_order_state.py -q -p no:cacheprovider
74 passed in 0.31s

python -m py_compile bridge/engine/types.py tests/test_order_state.py
exit 0; no output
```

The sole full-suite warning in both CWDs was the same pre-existing
`StarletteDeprecationWarning`. The focused rerun after both full suites found no
observed order-dependent failure.

## Semantic RED against the exact parent

A validated short throwaway worktree `C:\T1R-ffc37575` was created detached at
`cfb08b819aa9890725344e8315571299718cd554`. Only the new focused test was copied
into it. From its `IBKR_PAPER_BRIDGE` directory:

```text
python -m pytest tests/test_order_state.py -q --tb=short -p no:cacheprovider
ImportError: cannot import name 'IllegalOrderTransitionError' from 'bridge.engine.types'
1 error during collection in 0.32s
exit 2
```

Porcelain contained only `?? IBKR_PAPER_BRIDGE/tests/test_order_state.py`. The exact
throwaway worktree was then removed; `Test-Path=False` and no worktree registration
remained.

For transparency, two discarded setup attempts are not counted as RED evidence: a
long `%TEMP%` checkout failed on Windows filename length and was fully removed, and
a subsequent command used the wrong CWD and collected no tests. The short-path run
above is the valid semantic reproduction.

## Independent transition oracle

The audit parsed the Markdown transition rows, constructed its own expected edge set,
added the documented eleven self edges, and compared every pair against the public
`can_transition` API twenty times. It did not use `ORDER_STATE_TRANSITIONS` to derive
expected results.

```text
pairs=121 legal=44 repeats=20 mismatches=[]
```

The committed focused test also contains an explicit independent expected relation;
its proof is not circular. The oracle above independently confirms it.

## Twelve adversarial probes

1. **PASS — Exhaustive pair totality.** 121 pairs, 44 legal, twenty identical
   repetitions per pair, zero oracle mismatch.
2. **PASS — Terminal resurrection.** `FILLED`, `CANCELED`, `REJECTED`, and `EXPIRED`
   have no outgoing non-self edge.
3. **PASS — Unknown blind retry.** `UNKNOWN_SUBMISSION` cannot reach `PENDING_NEW`
   or `SUBMITTING`.
4. **PASS — Progress regression.** `PARTIALLY_FILLED` cannot reach `PENDING_NEW`,
   `SUBMITTING`, `SUBMITTED`, or `OPEN`.
5. **PASS — Cancel/fill race.** `PENDING_CANCEL` accepts `OPEN`, partial/final fill,
   cancel, and expiry; the tested fallback set remains denied.
6. **PASS — Same-state replay.** All eleven self edges are legal, calls leave the
   relation unchanged, and the contract explicitly says replay is not lifecycle
   progress.
7. **PASS — Raw normalization abuse.** Known aliases normalize exactly. Garbage,
   whitespace-only, near misses, `None`, bool, numbers, bytes, and a plain object
   returned no state and raised the dedicated error. The hostile-`repr` failure is
   separately recorded as Finding F2.
8. **FAIL — Mutability attack.** Public assignment and `frozenset.add` are blocked,
   but the module-visible seed dictionaries change the policies observed by later
   public calls. Finding F1 is a mandatory BLOCK.
9. **PASS — Serialization compatibility.** Every enum value round-trips through
   string/JSON; `BrokerOrder.status` and `OrderUpdateEvent.status` remain `str`, and
   exact legacy model-dump field shapes are unchanged.
10. **PASS — Actual-status coverage.** All five lifecycle literals are mapped;
    `WAITING_CHILD` and decision-stage spellings are explicitly separated/deferred.
11. **PASS — Future-task boundary.** No persistence, broker wiring, retry/reconcile,
    partial-fill protection, migration, threshold, strategy, Pine, or parity behavior
    entered the diff.
12. **PASS — No mutation.** Final evidence: audited HEAD
    `5140e062b8c1f3fcc78e96c7357060c60a51285d`; porcelain empty; tracked hashes
    unchanged (`types.py`
    `04352C9A3719A2F7A7FEDCDF6F6BA93745A18AEB8581383BB3F7F08B6681E5CA`, test
    `799C9ECBE2704B04DED2525E492E5977295F856B18BA05D9C0760CB16B26C22A`,
    contract
    `6AD6B13ABDBE3E03D2477C05217B5EC39BF52CD9B8E42E8527B34C83CF204A40`);
    main unrelated status remained 128 entries with digest
    `4EE5238D307287B3B099DFF2E19B2CB3D43B693115733F46ACB0016185544140`;
    P2RT HEAD `008e065e8e0ffa68f46134da6698d58f91ef2dcb`, porcelain empty.

## Findings

### F1 — BLOCK/P0: mutable backing dictionaries defeat the policy boundary

Evidence: `bridge/engine/types.py:140-211` and `:248-257` create
`_ORDER_STATE_TRANSITIONS_SEED` and `_RAW_ORDER_STATUS_ALIASES_SEED`, then wrap those
same mutable objects in `MappingProxyType`. The proxy blocks writes *through the
proxy*; it does not freeze the underlying dictionary.

Reproduction in a fresh Python process (the original entries were restored in a
`finally` block):

```text
public_outer_blocked=True
public_inner_blocked=True
terminal_blocked=True
private_seed_changed_policy=True
FILLED -> OPEN: False before, True after seed replacement
normalize_raw_order_status('OPEN'): FILLED after alias-seed replacement
```

The tests at `tests/test_order_state.py:271-285` attack only the proxy and inner
`frozenset`; they never attack the named backing dictionaries. This disproves the
immutability claim at `docs/22_ORDER_STATE_CONTRACT.md:139-142` and the builder's
report. The audit prompt explicitly defines a mutable policy surface as BLOCK.

### F2 — BLOCK/P1: exception contract is not safely structured

`bridge/engine/types.py:215-221` stores `from_state` and `to_state`, but provides no
stable `reason_code`:

```text
IllegalOrderTransitionError reason_code=None
message='illegal order-state transition: FILLED -> OPEN'
```

`bridge/engine/types.py:242-245` formats `{raw!r}` into every raw-status error. Two
hostile-object probes reproduced:

```text
Leaky.__repr__ -> UnknownRawOrderStatusError message contains LEAK_TOKEN_9f8e7d
Exploding.__repr__ -> RuntimeError('repr exploded'), not UnknownRawOrderStatusError
```

Thus an object input can leak arbitrary representation text or escape the dedicated
fail-closed exception with a normal traceback. The focused tests at
`tests/test_order_state.py:215-220` and `:257-268` do not assert an illegal-transition
reason code or hostile-`repr` behavior.

Bounded nit, not an additional blocker: `can_transition([], OrderState.OPEN)` raises
`TypeError` because the list is unhashable. The documented totality domain is
`OrderState x OrderState`, so the repair need not widen that domain unless the public
contract is intentionally changed.

## Contract review

- The eleven state names and meanings are unambiguous.
- The transition relation is a complete table, not prose-only examples.
- Terminal and same-state semantics are explicit and oracle-correct.
- Raw broker spellings are separated from canonical states.
- The state-only quantity limitation is honest and does not claim fill arithmetic.
- UNKNOWN recovery is deferred to TS-P1-003 and blind retry is forbidden.
- Durable identity/persistence is deferred to TS-P1-002.
- Partial protect-or-flatten behavior is deferred to TS-P1-004.
- Rollback/read-old-state compatibility is described; this commit wires no reader.
- The invariant contract remains honestly marked **PROPOSED** pending owner acceptance.

ADR-0023 is Accepted, but that does not ratify this implementation's proposed policy
surface or the five open design choices.

## P2RT and no-mutation boundary

Only the permitted pre/post Git identity snapshots were taken. Pre-executable snapshot:

```text
HEAD=008e065e8e0ffa68f46134da6698d58f91ef2dcb
porcelain=<empty>
```

Post snapshot is recorded in Probe 12. No P2RT API/status GET, Task Scheduler,
process, database, exchange, credential, ARM/DISARM, or deploy action occurred.

## Verdict and sequence management

**BLOCK.** GREEN suites, correct scope, and a correct transition table do not override
the reproduced mutable policy surface or the unsafe/unreason-coded exception contract.

The only next-session artifact is
`MTC_COMMAND_CENTER/11_TRIAGE/CLAUDE_TSP1001_REPAIR_PROMPT_2026-07-20.md`.
It requires a new repair commit on the same task followed by independent Codex
re-audit. No TS-P1-002 prompt was created, and TS-P1-002 was not started.

Exact owner decision still required: **Baris must accept or reject the PROPOSED
TS-P1-001 invariant contract after a repair commit passes independent Codex re-audit;
until then TS-P1-002 remains blocked.**
