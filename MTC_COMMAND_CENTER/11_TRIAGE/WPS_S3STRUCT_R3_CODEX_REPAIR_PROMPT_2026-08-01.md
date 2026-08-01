# S3-STRUCT ROUND 3 — CODEX REPAIR DISPATCH (2026-08-01)

## 0. ROLE OVERRIDE — READ FIRST

**You are the IMPLEMENTER.** Claude `claude-opus-5` is Lead and acceptance authority; you are the
counterpart flagship implementer (`gpt-5.6-sol`, effort `xhigh`). Do **not** delegate to Claude Code
CLI or any other model — a delegation attempt returns `ConnectionRefused` and wastes the round.

**You cannot run Git.** `.git` is read-only for you. The Lead does every Git operation.

Workspace: `C:/WPS` — branch `feature/ts-p1-009b-s2-closure`, HEAD `216682ba` (your round-2 work,
already committed by the Lead).

## 1. THIS IS THE LAST REPAIRABLE ROUND

Round 2 (`216682ba`) was **not accepted**: `REQUEST_CHANGES` from canonical auditor `claude-opus-5`
xhigh, both findings **reproduced by the Lead on real source**. Suite was clean —
`2 failed, 1266 passed`, no third failure, no weakened tests, allowlist exact.

**Two of three non-accepting rounds are spent.** If round 3 does not produce an accepting verdict
from both flagships, the Lead stops and reports a failed cycle to the owner. There is no round 4.

**What is settled and must not be redesigned.** Both the auditor and the Lead judged the boundary
genuinely structural: one `DurableRowAccessor` / `DURABLE_EVENT_ROWS` over the declared
`DURABLE_EVENT_COLUMN_TYPES` registry, routed by returning typed *rows* from the store rather than by
wrapping call sites; both legacy helpers deleted; both matrices generated from declared registries;
the class-C join added as a conjunct with the epoch fence intact. The R-1 fix from round 2
(`expected_identity` and the named binding reasons) is also accepted. **Do not re-open any of it.**
Both findings below are containment gaps at the boundary's *edges*.

## 2. R-1 (REQUIRED) — the registry has no nullability contract, so a normal state latches KILLED

`orders.py:3473`. Reproduced by the Lead with **no corruption injected**.

`create_trade` does not list `entry_px` in its INSERT columns — verified at **both**
`db.py:4858-4862` and `db.py:7565-7570`. Every trade is therefore created with `entry_px IS NULL`
until an ENTRY fill triggers `update_trade_entry`. The predecessor read
`self._store_float(trade["entry_px"] or trade["expected_px"], …)`, and that `or` existed **precisely**
to select `expected_px` in that state.

Round 1 replaced it with two eager reads:

```python
entry_qty = trade["qty"]
stored_entry_px = trade["entry_px"]      # faults before the `or` can run
expected_entry_px = trade["expected_px"]
entry_px = stored_entry_px or expected_entry_px
```

`DurableRowFault` is a `RuntimeError`, so the enclosing
`except (InvalidOperation, TypeError, ValueError, OverflowError, LotQuantizationError)` at
`orders.py:3478-3484` does not catch it. It unwinds to the drain and is contained as a durable kill.

The `else` branch is entered **exactly** when the trade has no ENTRY-fill aggregate — which is
**exactly** when `entry_px` is NULL. **The `expected_px` half of the fallback is now dead code, and
every entry into that branch faults.** At `732b37c3` the same state closed the trade on the
`expected_px` basis.

**Your own matrix masks it.** The trades arm in `tests/test_engine_dryrun.py` contains:

```python
store.conn.execute("UPDATE trades SET entry_px=100.0 WHERE trade_id=?", (trade_id,))
```

That line is not part of the corruption being tested. It exists to stop the boundary faulting on the
ordinary NULL before the intended column is reached. **Remove it and make the matrix honest.**

### Fix the contract, not the call site

Patching `orders.py:3473` alone will be rejected. The root cause is that the registry treats **"SQL
NULL"** as a single fault case, when in this schema NULL means two different things:

- `trades.entry_px` is NULL **by design** until entry fills — a legitimate absent value.
- `fills.fee` NULL is **corruption** — the v8→v9 migration admits it and nothing writes it.

**Declare nullability per column in `DURABLE_EVENT_COLUMN_TYPES`.** For each registered column state
whether NULL is an admissible absent value or a fault, and derive that from the schema and from what
actually writes the column — not from which call site currently happens to break. A column that is
nullable by design must return an explicit absent result the caller can act on (`None`, or whatever
shape you choose), never a fault.

Then **generate the matrix from that contract**, so a nullable-by-design column asserts NULL is
**accepted and handled**, and a non-nullable column asserts NULL **faults**. That assertion is what
would have caught R-1 in round 1, and it is what stops the next nullable-by-design column repeating
it.

## 3. R-2 (REQUIRED) — the boundary's fault type escapes existing conversion-fault contracts

`db.py:6655` and `db.py:6664`. `_expected_kill_flatten_closure_in_tx` calls `trade_fill_totals` and
`trade_costs`. **This round routed both through `DURABLE_EVENT_ROWS`** (`db.py:7776-7783`,
`7805-7812`, `9561-9576`), but its containment clause at `db.py:6668-6680` catches only
`(InvalidOperation, KeyError, TypeError, ValueError, OverflowError)`.

`DurableRowFault(RuntimeError)` matches none of them. Verified by the auditor:

```
fee=None  -> DurableRowFault DURABLE_FILLS_FEE_NULL             | caught? False
fee='abc' -> DurableRowFault DURABLE_FILLS_FEE_NON_NUMERIC_TEXT | caught? False
```

`fills.fee` / `fills.funding` are exactly the schema-admitted class: `REAL` affinity, no `NOT NULL`,
migration-preserved. `trade_costs` previously used `COALESCE(SUM(fee), 0.0)` and never raised at all;
your routing made it raise, into a caller with no handler for it.

**Failing path:** a `fills` row for an APPLIED `KILL_FLATTEN` order carries `fee = NULL` → operator
ACK → `acknowledge_kill_evidence` (`db.py:7219`, `BEGIN IMMEDIATE` at `7224`) →
`_assert_kill_flatten_closure_in_tx` (`7275`) → `_expected_kill_flatten_closure_in_tx` →
`trade_costs` → bare `RuntimeError` named `DURABLE_FILLS_FEE_NULL` instead of
`KillConflictError("KILL_FLATTEN_LIFECYCLE_CONFLICT")`. The same escape exists at `db.py:6863` via
`validate_applied_kill_flatten_lifecycle_closures`, which `orders.py:1709` calls inside the kill
flatten flow.

### Again: fix the class, not the two clauses

Adding `DurableRowFault` to that one `except` closes the two sites the auditor named and leaves the
class open — which is the exact failure mode this whole cycle exists to end. **Every caller that
already has a conversion-fault contract and now reaches a boundary-routed read has this bug.**

Enumerate them and close them systematically. Two candidate strategies, your choice, but justify it:

- Make the boundary's fault satisfy the contracts that already exist — e.g. have `DurableRowFault`
  inherit from a type the existing conversion-fault handlers already catch, so no caller has to be
  edited to be correct. If you choose this, state clearly what it means for the S3T-A requirement
  that the boundary not raise a bare `ValueError`/`TypeError` into a caller, and make sure a fault
  is still distinguishable by type where that matters.
- Or keep the distinct type and add containment at **every** such caller — in which case you must
  enumerate the complete set and prove the enumeration is complete, not sample it.

**Then prove it with a test**, not with a claim: no bare `DurableRowFault` may escape any public
`Store` API reachable from the kill-evidence or ACK paths. Generate that check rather than listing
the two sites above.

## 4. ALSO REQUIRED — fold in N-5 and N-4

**N-5.** The round-2 rationale claimed `record_kill_lifecycle_deferral` was "strictly stronger" than
the close-path predicate. **It is not, and the Lead's acceptance of that reasoning was wrong.** The
close binds on `resolved_epoch.episode_id` (`db.py:7656`); the deferral binds on `orders.group_id`
via `kill_identity[0]` (`db.py:5338-5352`); `_kill_lifecycle_identity` never requires them to be
equal — it only requires `get_kill_request(episode_id)` to exist. With active epoch **A** and a
well-formed `KILL_FLATTEN` order still bound to an older, still-present episode **B**, the close
vetoes and the deferral succeeds. `DEFERRED` is reachable **with no second `Store` at all**.

Make the invariant true: when an epoch is active, `_kill_lifecycle_identity` must require the order's
`group_id` to equal the active episode. Add a generated case for the A/B mismatch.

**N-4.** With N-5 enforced and `_ingest_queued_event` already allowlisting
`KILL_LIFECYCLE_IDENTITY_MISSING`, the `raise` on `DEFERRED` at `orders.py:3621` is redundant and
re-defers the same fill. Remove the asymmetry with its sibling handler, which returns `False`.

**Explicitly deferred to TS-P1-010 — do NOT fix these now:** N-1 (int64 range check applied to
`FINITE_FLOAT`), N-2 (two reason codes for one storage-class fault), N-3 (asymmetric TEXT policy
between `INT64` and `FINITE_FLOAT`), and the `trades.sl_initial` / `tp_initial` registry gap at
`orders.py:3069-3071` / `3186` (reachable from `reconcile()` but **not** from a queued broker event,
so outside S3T-C as scoped). Do not widen scope to them.

## 5. UNCHANGED CONSTRAINTS

**Allowlist — exhaustive:**

```
IBKR_PAPER_BRIDGE/bridge/engine/orders.py
IBKR_PAPER_BRIDGE/bridge/store/db.py
IBKR_PAPER_BRIDGE/tests/test_engine_dryrun.py
IBKR_PAPER_BRIDGE/tests/test_store.py
IBKR_PAPER_BRIDGE/docs/31_KILL_EVIDENCE_EPOCH_CONTRACT.md
```

`bridge/engine/engine.py` is **not** allowed. Report a needed scope extension; never take one.

**Forbidden:** any `*.pine`, `MTC_V2`, `parity`, `01_PINE`, `02_MTC_BACKTEST`, `07_ADAPTERS` path ·
`bridge/engine/strategies/**`, `config/strategies/**` · `bridge/api/routes.py` · `bridge/broker/**` ·
**any risk-threshold value** in `config/bridge.yaml` · any credential, wallet secret, API key, host,
IP or private path · **weakening, deleting, skipping or `xfail`-ing any existing test — grep your own
diff for `-` lines under `tests/` before reporting.** Removing the masking `UPDATE trades SET
entry_px=100.0` line is required by §2 and is not a weakening — report it explicitly. · any migration
or schema change · any broker, network, TESTNET, ARM or runtime action. DISARMED only.

`KILL_STALE_EVIDENCE_RECORD_FAILED` and genuine evidence-store write failures **still propagate**.

**Test contract** — from `C:/WPS/IBKR_PAPER_BRIDGE`:

```
python -m pytest -q --ignore=TSP1009B.pytest_tmp_s1r1 -p no:randomly
```

`--ignore` is mandatory. Never pass `--basetemp` inside `.pytest_cache`.

Floor at `216682ba`: **`2 failed, 1266 passed`** — the two pre-existing failures only. **Do not "fix"
them.** A third failure is a required finding. Run the full suite yourself before reporting.

## 6. REPORT FORMAT — end with exactly this

```
Nullability contract : <how the registry now declares it, per column, and why each choice>
R-1 fix              : <what orders.py:3473 does now; proof the expected_px basis is live again>
Masking line removed : <yes + where; the matrix arm must now fail without the fix>
R-2 strategy         : <which of the two strategies, and the justification>
R-2 completeness     : <how you enumerated every affected caller, and the proof it is complete>
R-2 generated check  : <the test that proves no bare DurableRowFault escapes those APIs>
N-5 invariant        : <where group_id is now compared to the active epoch + the A/B case>
N-4 removed          : <yes + the resulting disposition on DEFERRED>
Matrix totals        : <columns x cases, including the nullable-by-design accept cases>
files changed        : <exact list>
tests added          : <names>
existing tests touched : <list>   # every '-' line under tests/ must appear here
suite output         : <the literal final pytest line>
scope extensions     : <none | what you needed and why you did NOT take it>
open risks           : <anything the Lead should probe first>
```

Begin. Implement in `C:/WPS`. No Git. No delegation.
