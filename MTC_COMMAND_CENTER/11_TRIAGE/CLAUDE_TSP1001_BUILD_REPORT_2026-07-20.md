# CLAUDE TS-P1-001 BUILD REPORT — 2026-07-20

Builder: Claude (Sonnet 5), acting as builder/orchestrator per
`CLAUDE_TSP1001_BUILD_PROMPT_2026-07-20.md`. This report separates **builder
claims** from **raw evidence** (command output). Codex must audit the real
diff independently — do not trust this report's prose without checking the
commit.

## 1. Location for the independent Codex auditor

- Worktree: `C:\TSP1001`
- Branch: `feature/ts-p1-001-order-state`
- Base commit (parent, = required TS-P0 baseline HEAD): `cfb08b819aa9890725344e8315571299718cd554`
- New commit (HEAD): `5140e062b8c1f3fcc78e96c7357060c60a51285d`
- Inspect with, from any clone/worktree that has these commits (or directly
  in `C:\TSP1001`):
  ```
  git show 5140e062b8c1f3fcc78e96c7357060c60a51285d --stat
  git diff cfb08b819aa9890725344e8315571299718cd554 5140e062b8c1f3fcc78e96c7357060c60a51285d
  ```
- `C:\TSP1001` is left clean at this commit (verified below). PR #25
  (`feature/ts-p0-baseline`) is untouched. `C:\TSP0`, `C:\P2RT`, `C:\P1IF`,
  `C:\G5R`, `C:\BTL2` were not touched by this session.

## 2. Preflight (raw evidence)

`C:\TSP1001` already existed as a registered worktree (branch
`feature/ts-p1-001-order-state`) before this session, at exactly the
required base commit, with **zero prior work**:

```
git -C C:\TSP1001 rev-parse HEAD          -> cfb08b819aa9890725344e8315571299718cd554
git -C C:\TSP1001 status --porcelain      -> (empty)
git -C C:\TSP1001 diff --stat             -> (empty)
git -C C:\TSP1001 diff cfb08b81 --stat    -> (empty)
```

Per the prompt's instruction ("If either exists, inspect and STOP rather
than delete/reset it"), this was inspected, found clean and correctly
based, and used as-is — nothing was deleted, reset, or recreated.

`C:\TSP0` verified separately: HEAD `cfb08b819aa9890725344e8315571299718cd554`,
matches `origin/feature/ts-p0-baseline`, branch `feature/ts-p0-baseline`,
porcelain clean.

**Baseline test run (218 expected, both required CWDs):**

- `C:\TSP1001` → `python -m pytest IBKR_PAPER_BRIDGE/tests -q` → **218 passed**, 1 warning (pre-existing `httpx`/starlette deprecation notice, unrelated), 38.28s.
- `C:\TSP1001\IBKR_PAPER_BRIDGE` → `python -m pytest tests -q` → **218 passed**, same warning, 41.37s.

(Note for future sessions: the PowerShell tool resets its shell cwd to the
primary working directory between calls — each baseline/suite run had to
`Set-Location` explicitly in the same call as the `pytest` invocation. An
earlier accidental run without `Set-Location` executed against the *main*
worktree's `IBKR_PAPER_BRIDGE` — a different branch — and produced 114
passed; that result is not part of this task's evidence and is called out
here only so it isn't mistaken for a baseline discrepancy.)

## 3. Exact implementation scope (raw evidence)

```
git show 5140e062 --stat
 IBKR_PAPER_BRIDGE/bridge/engine/types.py          | 170 ++++++++++-
 IBKR_PAPER_BRIDGE/docs/22_ORDER_STATE_CONTRACT.md | 190 ++++++++++++
 IBKR_PAPER_BRIDGE/tests/test_order_state.py       | 350 ++++++++++++++++++++++
 3 files changed, 709 insertions(+), 1 deletion(-)
```

Exactly the three paths named in the prompt's scope section — no other
tracked file changed. The single deletion is the pre-existing
`from typing import Literal` line, replaced with
`from typing import Literal, Mapping` (additive import, same line).
`orders.py`, `db.py`, broker adapters/mocks, API/routes, engine wiring,
config, schemas, migrations, strategy/risk logic, Pine, and parity were not
touched (confirmed by the stat above listing only these 3 files, and by the
repo guard dirty-set check in §6 matching exactly these 3 paths before
staging).

## 4. Raw-status inventory and chosen mapping (builder claim; full detail in the contract doc)

Grep across `IBKR_PAPER_BRIDGE/bridge/**/*.py` and `tests/**/*.py` for order
status literals found: `"OPEN"` (default + most-used live state),
`"SUBMITTED"` (test-only, no current producer), `"PENDING"` (referenced only
in a live-set membership check, never assigned by any producer),
`"FILLED"` (terminal), `"CANCELLED_BY_ENGINE"` (terminal, British-spelling
raw literal). Also found and explicitly **excluded** with rationale:
`"WAITING_CHILD"` (an adapter-internal reconciliation-dict field for a
child SL/TP order awaiting parent trigger — never assigned to
`BrokerOrder.status` or persisted), and the decision-pipeline `"stage"`
values `"SUBMITTED"`/`"REJECTED"` (a different, pre-existing, unrelated
concept — whether a *decision* produced an order at all, not an order's
exchange lifecycle). Full inventory table with producer/consumer file:line
provenance is in `docs/22_ORDER_STATE_CONTRACT.md` §"Raw-status inventory".

Mapping chosen: `OPEN→OPEN`, `SUBMITTED→SUBMITTED`, `PENDING→SUBMITTED`,
`FILLED→FILLED`, `CANCELLED_BY_ENGINE→CANCELED`. Rationale for the one
non-obvious choice (`PENDING→SUBMITTED` rather than `→OPEN`) is recorded in
the contract doc.

## 5. Complete state set, terminal states, transition count (builder claim; raw table in contract doc)

11 canonical states: `PENDING_NEW, SUBMITTING, SUBMITTED, OPEN,
PARTIALLY_FILLED, PENDING_CANCEL, FILLED, CANCELED, REJECTED, EXPIRED,
UNKNOWN_SUBMISSION`.

4 terminal states: `FILLED, CANCELED, REJECTED, EXPIRED` (zero outgoing
edges except self).

Transition count: **44 legal ordered pairs out of 121 possible** (11×11) —
33 state-change edges + 11 idempotent same-state edges. Full adjacency
table is in the contract doc and is asserted exhaustively by
`test_exhaustive_all_pairs_agree_with_declared_relation` and
`test_total_legal_transition_count_is_44_including_self_loops`.

## 6. TDD evidence (raw command output)

**RED** — test file written first, run against the unmodified base
`types.py` (before any new symbols existed):

```
python -m pytest tests/test_order_state.py -q
ImportError while importing test module 'tests/test_order_state.py'.
tests\test_order_state.py:9: in <module>
    from bridge.engine.types import (
E   ImportError: cannot import name 'IllegalOrderTransitionError' from 'bridge.engine.types'
1 error in 0.39s
```

Semantic RED confirmed: failure is "missing model" (an `ImportError` for a
not-yet-defined symbol), not a typo/syntax error in the test itself.

**GREEN** — after implementing the additive block in `types.py`:

```
python -m pytest tests/test_order_state.py -q
74 passed in 0.42s
```

**Full suite, both required CWDs** (expected `218 + 74 = 292`):

```
C:\TSP1001>                       python -m pytest IBKR_PAPER_BRIDGE/tests -q  -> 292 passed, 1 warning, 48.34s
C:\TSP1001\IBKR_PAPER_BRIDGE>      python -m pytest tests -q                    -> 292 passed, 1 warning, 48.20s
```

Identical count in both CWDs, matching the expected `218 + N` formula.

**Compile check:**

```
python -m py_compile IBKR_PAPER_BRIDGE\bridge\engine\types.py IBKR_PAPER_BRIDGE\tests\test_order_state.py
-> exit 0 (COMPILE OK)
```

## 7. Test coverage against the prompt's minimum-coverage list (builder claim)

All 12 required categories are covered (test names in
`tests/test_order_state.py`):

| Requirement | Test(s) |
| --- | --- |
| Exhaustive all-pairs agreement | `test_exhaustive_all_pairs_agree_with_declared_relation`, `test_total_legal_transition_count_is_44_including_self_loops` |
| Legal/illegal edge spot checks | `test_representative_legal_edges`, `test_representative_illegal_edges` |
| Terminal-state resurrection | `test_terminal_states_forbid_resurrection`, `test_terminal_state_set_is_exactly_four` |
| Same-state/idempotent replay | `test_same_state_is_always_legal_idempotent_replay` |
| Unknown-submission blind-resubmit rejection | `test_unknown_submission_forbids_blind_retry`, `test_unknown_submission_resolves_via_reconciliation_evidence` |
| Partial-fill / pending-cancel races | `test_partial_fill_cannot_regress_to_ordinary_lower_progress_state`, `test_pending_cancel_still_receives_authoritative_fill_and_terminal_outcomes`, `test_pending_cancel_race_can_revert_to_open_on_cancel_reject` |
| Raw aliases + unknown/malformed inputs | `test_known_raw_status_aliases_normalize`, `test_raw_alias_table_matches_documented_inventory`, `test_unknown_or_malformed_raw_status_fails_closed` |
| String/JSON/Pydantic round-trip | `test_order_state_string_equality_and_value_roundtrip`, `test_order_state_pydantic_json_roundtrip`, `test_order_state_accepts_plain_string_in_pydantic_model` |
| Immutable transition-map attack | `test_transition_map_values_are_frozensets_immutable_to_callers`, `test_transition_map_itself_is_read_only`, `test_raw_alias_table_is_read_only` |
| Pure/no-mutation behavior | `test_can_transition_and_validate_are_pure_no_mutation` |
| Compatibility imports for existing models | `test_existing_models_remain_constructible_and_backward_compatible` |
| Non-string (bool/None/bytes/etc.) bypass | `test_non_string_raw_status_fails_closed_not_bypassed` |

## 8. Adversarial self-review (builder claim, cross-checked against raw test evidence in §6)

- **Can `FILLED` become `OPEN`, `PARTIALLY_FILLED`, or `PENDING_CANCEL`?** No — `FILLED`'s only legal target is itself; enforced by the transition table and asserted for all 4 terminals × all other 10 states (40 assertions) in `test_terminal_states_forbid_resurrection`.
- **Can `CANCELED`/`REJECTED` be resurrected by a raw alias?** No — `normalize_raw_order_status` and `validate_order_transition` are independent functions; nothing in this task composes "normalize then apply without validating," and the transition table alone forbids any edge out of a terminal state regardless of what a normalized raw value produces. No wiring into any caller exists yet (scope boundary).
- **Can `UNKNOWN_SUBMISSION` return to `SUBMITTING`?** No — absent from its edge set by construction; `test_unknown_submission_forbids_blind_retry` asserts both `can_transition` returns `False` and `validate_order_transition` raises for `PENDING_NEW` and `SUBMITTING`.
- **Does a garbage status accidentally normalize to `OPEN`/`SUBMITTED`?** No — only exact known aliases (after `.strip().upper()`) match; everything else raises `UnknownRawOrderStatusError`. Tested with `"BOGUS"`, empty string, whitespace-only, `"OPENN"`, and the excluded `"WAITING_CHILD"`/`"waitingForFill"` spellings.
- **Can a caller mutate the exported transition set/map?** No — `ORDER_STATE_TRANSITIONS` is a `MappingProxyType` over `frozenset` values; both mutation attempts (outer assignment, inner `.add`) raise, tested directly.
- **Does `bool`, `None`, bytes, whitespace, or case variation bypass parsing?** `bool`/`None`/`bytes`/list/dict are rejected by an explicit `isinstance(raw, str)` gate before any string method is called (raising `NON_STRING_RAW_STATUS`, not crashing or silently coercing). Whitespace and case are intentionally tolerated for *known* aliases only (matches existing `hyperliquid.py` `.upper()` behavior) — tested both the tolerant and the fail-closed paths.
- **Is `PENDING_CANCEL -> FILLED` handled as authoritative race completion?** Yes, explicit edge, tested.
- **Did I invent fill-quantity correctness belonging to TS-P1-004?** No — `PARTIALLY_FILLED` is a state label only; no qty/VWAP arithmetic implemented; the contract doc's "Quantity limitation" section says so explicitly, and `orders.py` (where real fill arithmetic lives) is untouched.
- **Did any production order, database, broker, exchange, or strategy path change?** No — see §3; only `types.py` (additive block) plus two new files changed. No import of the new symbols exists anywhere outside the new test file, so nothing in the running system's behavior can change from this commit.

## 9. Repo guard and final state (raw evidence)

Preflight guard (before staging), from `C:\TSP1001`:
```
=== MTC Repo Guard (dry-run, read-only) ===
[branch]    feature/ts-p1-001-order-state
[dirty]     3 entr(y/ies): M .../types.py, ?? .../22_ORDER_STATE_CONTRACT.md, ?? .../test_order_state.py
[staged]    none
[protected] none
[untracked] no risky files
RESULT: PASS
```

Staged set verified to equal the intended set exactly (`git diff --cached
--name-only` → the 3 allowed paths, nothing else); `git diff --cached
--check` produced no output (no whitespace/conflict-marker errors).

Commit created: `git commit -m "feat(bridge): define canonical order-state invariants"` →
`5140e062b8c1f3fcc78e96c7357060c60a51285d`.

Post-commit guard, from `C:\TSP1001`:
```
[dirty]     clean
[staged]    none
[protected] none
[untracked] no risky files
RESULT: PASS
```

```
branch:            feature/ts-p1-001-order-state
files changed:     IBKR_PAPER_BRIDGE/bridge/engine/types.py, IBKR_PAPER_BRIDGE/docs/22_ORDER_STATE_CONTRACT.md, IBKR_PAPER_BRIDGE/tests/test_order_state.py
checks run:        pytest (baseline ×2, focused RED/GREEN, full suite ×2), py_compile, repo_guard.ps1 (×2)
guard:             PASS
commit:            5140e062b8c1f3fcc78e96c7357060c60a51285d
pushed:            no
remaining dirty:   none
next action:       independent Codex Gate-5 audit on the real diff
```

## 10. Explicit confirmation of no out-of-scope action

No P2RT action, no API/server start, no scheduler action, no network call
beyond ordinary local `git` operations, no deploy, no push, no PR
created/updated/merged, no execution of backtests/optimizations/broker/
live/paper actions. `C:\TSP0` (PR #25) was read-only inspected, not
modified. This session ran entirely in `C:\TSP1001` plus this one report
file and (below) conservative, uncommitted handoff-note updates in the
shared main worktree.

## 11. Unresolved design questions for Barış / Codex

1. **`PENDING → SUBMITTED` alias choice.** No current code actually
   produces raw `"PENDING"`; it was mapped to the more conservative live
   bucket (`SUBMITTED`) rather than `OPEN` purely from the read-only
   inventory. If either of you has out-of-band knowledge of what a future
   broker adapter means by `PENDING`, this mapping may need to change.
2. **`PENDING_CANCEL -> OPEN` (cancel-reject reversion).** Included as a
   realistic race (exchange declines a cancel, order remains live) and
   does not violate any written invariant, but it is not explicitly
   required by the prompt or ADR-0023. Flagging in case the intent was for
   `PENDING_CANCEL` to be cancel-only-forward.
3. **Direct terminal edges bypassing `PENDING_CANCEL`** (`OPEN→CANCELED`,
   `SUBMITTED→CANCELED`, `OPEN→FILLED` without `PARTIALLY_FILLED`, etc.).
   Justified in the contract doc by `MockBroker`'s existing atomic
   cancel/fill behavior, but this does widen the legal-edge set beyond the
   minimum the prompt enumerates. Willing to narrow if Barış/Codex prefer a
   stricter model that forces every cancel through `PENDING_CANCEL`.
4. **`WAITING_CHILD` exclusion.** Treated as out-of-band and excluded
   entirely from the canonical model rather than given its own state
   (e.g. a `PENDING_TRIGGER`/child-order concept). A future task formalizing
   bracket child-order lifecycle may need to revisit this.
5. **`UNKNOWN_SUBMISSION`'s wide resolution set** (all 8 non-`PENDING_NEW`/
   `SUBMITTING` states are legal targets). This was a deliberate choice to
   let TS-P1-003's reconciliation logic decide what the true state actually
   is without this task pre-judging it, but it is intentionally permissive
   at the pure-transition level — the fail-closed guarantee here is only
   that `UNKNOWN_SUBMISSION` can never reach `PENDING_NEW`/`SUBMITTING`
   (i.e., no blind retry), not that every other target is independently
   justified yet.

## 12. Result

**READY FOR INDEPENDENT CODEX AUDIT**

- Commit: `5140e062b8c1f3fcc78e96c7357060c60a51285d` (branch
  `feature/ts-p1-001-order-state`, worktree `C:\TSP1001`, parent
  `cfb08b819aa9890725344e8315571299718cd554`)
- Tests: 74/74 new focused tests green; 292/292 full suite green identically
  from both required CWDs (`218` baseline + `74` new); compile check clean.
- Report path: `MTC_COMMAND_CENTER/11_TRIAGE/CLAUDE_TSP1001_BUILD_REPORT_2026-07-20.md`
