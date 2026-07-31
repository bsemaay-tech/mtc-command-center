# Claude Second Repair Prompt — TS-P1-001 Residual BLOCK Findings

Use this prompt in a fresh Claude session. Repair only the two residual findings from
the independent re-audit. Do not start TS-P1-002.

## Mission

Create exactly one new local child commit on top of
`851d88a084875e48b63fba455cb7b27f357c5ac4` that closes F1-R and F2-R in:

`MTC_COMMAND_CENTER/11_TRIAGE/CODEX_TSP1001_REAUDIT_2026-07-20.md`

Do not amend, rebase, or rewrite either prior commit. After the new repair commit,
stop for another independent Codex re-audit.

## Read first

Read completely:

1. `C:\LAB\Tradingview_LAB_CLEAN\AGENTS.md`
2. canonical onboarding from `MTC_COMMAND_CENTER\_AI_MEMORY\START_HERE.md`
3. ADR-0023
4. TS-P1-001 and TS-P1-002 rows in both roadmap/backlog files
5. `MTC_COMMAND_CENTER\11_TRIAGE\CODEX_TSP1001_AUDIT_2026-07-20.md`
6. `MTC_COMMAND_CENTER\11_TRIAGE\CLAUDE_TSP1001_REPAIR_PROMPT_2026-07-20.md`
7. `MTC_COMMAND_CENTER\11_TRIAGE\CLAUDE_TSP1001_REPAIR_REPORT_2026-07-20.md`
8. `MTC_COMMAND_CENTER\11_TRIAGE\CODEX_TSP1001_REAUDIT_2026-07-20.md`

Treat the re-audit's fresh-process reproductions as the repair specification. Reproduce
both failures against unmodified parent `851d88a...` before editing.

## Fixed topology and boundaries

- Worktree: `C:\TSP1001`
- Branch: `feature/ts-p1-001-order-state`
- Required parent of the new commit:
  `851d88a084875e48b63fba455cb7b27f357c5ac4`
- Allowed tracked paths, and no others:
  - `IBKR_PAPER_BRIDGE/bridge/engine/types.py`
  - `IBKR_PAPER_BRIDGE/tests/test_order_state.py`
  - `IBKR_PAPER_BRIDGE/docs/22_ORDER_STATE_CONTRACT.md`

These files contain committed work from prior agents. Do not run `git checkout`,
`git reset`, `git restore`, `git stash`, or `git clean` on any tracked file. Do not
push, open/mutate a PR, merge, deploy, access P2RT, call an exchange, install a
dependency, or begin a next task.

No persistence, broker wiring, retry/reconcile behavior, partial-fill protection,
migration, schema, threshold, strategy/risk logic, Pine, or parity change is authorized.

## F1-R — mutable `MappingProxyType` referents

The old seed names are gone, but both exported proxies still expose their mutable
backing dictionaries through the documented standard-library API
`gc.get_referents(proxy)`. Codex mutated those returned dicts and changed later public
decisions:

```text
gc_dict_referents=1/1
FILLED->OPEN: False before, True after
normalize('OPEN'): OrderState.OPEN before, OrderState.FILLED after
```

Repair requirements:

1. The policy backing representation itself must be immutable. Do not put a mutable
   dict behind `MappingProxyType`, whether named or anonymous.
2. Preserve read-only public `Mapping` behavior and `frozenset` transition values.
3. Preserve exactly the eleven states, 44 legal pairs, and five raw aliases.
4. Add fresh-process regression tests that use `gc.get_referents` against both
   exported mappings and prove no returned mutable object can alter later
   `can_transition` or `normalize_raw_order_status` decisions.
5. Do not broaden the threat model to module-variable rebinding, `ctypes`, or memory
   corruption. This finding concerns the existing exported object's ordinary Python
   referents.

A genuinely immutable mapping representation is required; another proxy over a dict
or a hidden mutable cache is not a fix. Do not add dependencies.

## F2-R — hostile metaclass escapes error construction

The replacement `type(raw).__name__` still performs class attribute lookup through a
caller-controlled metaclass:

```python
class HostileMeta(type):
    def __getattribute__(cls, name):
        if name == "__name__":
            raise RuntimeError("metaclass name exploded")
        return super().__getattribute__(name)

class Hostile(metaclass=HostileMeta):
    pass
```

Current result: `normalize_raw_order_status(Hostile())` raises `RuntimeError`, not
`UnknownRawOrderStatusError`.

Repair requirements:

1. Non-string error construction must not access caller-controlled instance or class
   attributes, including `type(raw).__name__`.
2. Every non-string object must deterministically raise
   `UnknownRawOrderStatusError` with `reason_code="NON_STRING_RAW_STATUS"`.
3. Keep `.raw` as the original object, but use a constant safe message for this path.
4. Preserve the already-correct illegal-transition reason code and the leaking/
   exploding `__repr__` fixes.
5. Add the hostile-metaclass regression test above and assert dedicated exception,
   stable reason code, and no attacker text in the message.

## Frozen behavior

Do not change state names/meanings, any of the 44 pairs, terminal or replay semantics,
raw alias mappings, `PENDING -> SUBMITTED`, `PENDING_CANCEL -> OPEN`, direct terminal
edges, `WAITING_CHILD` exclusion, UNKNOWN resolution edges, Pydantic payload shape, or
the PROPOSED owner gate. The five open design questions remain unresolved owner
questions.

## Required RED, GREEN, and scope proof

1. On exact parent `851d88a...`, reproduce F1-R and F2-R in fresh processes.
2. Copy only the updated focused test into a short throwaway worktree at the parent
   and show the new assertions fail for the intended semantic reasons.
3. Run the updated focused suite from `C:\TSP1001` with `PYTHONUTF8=1`; do not lower
   the current 80-test count.
4. Run the complete bridge suite from both required CWDs with `PYTHONUTF8=1`:
   `C:\TSP1001` and `C:\TSP1001\IBKR_PAPER_BRIDGE`.
5. Run `py_compile` for the two Python files.
6. Run a document-derived 121-pair oracle and prove exactly 44 legal pairs with zero
   mismatch.
7. Re-run the GC-referent and hostile-metaclass attacks in fresh processes.
8. Verify exact three-file diff, `git diff --check`, protected-path identity, clean
   post-commit porcelain, and exact new parent.

## Deliverables and stop condition

Create one new repair commit and a concise main-worktree report:

`MTC_COMMAND_CENTER/11_TRIAGE/CLAUDE_TSP1001_REPAIR2_REPORT_2026-07-20.md`

The report must separate claims from raw evidence and include pre-fix reproduction,
semantic RED, exact commands/counts, oracle, fresh-process post-fix probes, diff, new
SHA/parent, and remaining gates.

Stop with the new SHA, exact parent, focused/full counts from both CWDs, report path,
confirmation of no push/PR/merge/deploy/P2RT/next-task action, and:

`READY FOR INDEPENDENT CODEX RE-AUDIT`

Do not create a TS-P1-002 prompt. Baris acceptance of the PROPOSED TS-P1-001 invariant
contract remains a separate owner gate after a successful independent re-audit.
