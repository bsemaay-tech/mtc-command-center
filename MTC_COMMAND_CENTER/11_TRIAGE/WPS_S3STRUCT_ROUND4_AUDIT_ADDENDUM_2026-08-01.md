---

# ROUND-4 ADDENDUM — read this together with the Gate-5 brief above

**Frozen SHA for this round: `16cbc717`.** Round-4 delta: `git diff dffbaf41..16cbc717`.
Whole-cycle delta: `git diff 732b37c3..16cbc717`.

Floor at `dffbaf41`: `2 failed, 1297 passed`. At `16cbc717`: **`2 failed, 1304 passed`** — still only
the two pre-existing failures named in the brief. A third failure is a required finding.

## This is a bounded round, not an open one

The S3-STRUCT cycle hit its three-round bound and was stopped and reported. **Barış authorised
exactly one further round, scoped to round-3 R-1 and nothing else.**

That changes what you are auditing for. **Scope creep is itself a required finding this round.** If
the diff changes anything not required by R-1 — the boundary design, the registry, the nullability
contract, the class-C join, the epoch fence, `expected_identity`, `DEFERRED` containment, or any
deferred nit — say so, even if the change is an improvement.

Equally: **do not require anything outside R-1.** The deferred nits (N-1 int64 range check on
`FINITE_FLOAT`, N-2 two reason codes for one storage-class fault, N-3 asymmetric TEXT policy, the
`trades.sl_initial` / `tp_initial` registry gap, the raw reads in `record_kill_action_event`) are
owner-deferred to TS-P1-010. Raising them as required repairs would block a round that was authorised
to fix one defect.

## What R-1 was

Round 3 made `DurableRowFault` a `ValueError` subclass so the store-side conversion contracts would
catch it. That was correct and stays. The same change also handed the fault to the **engine-side**
quantity-integrity handlers at `orders.py:3375/3444/3495/3569/3674`, each of which calls
`_quantity_integrity_fault` → `app_state = "DISARMED"`, with no `kill_latched` and no typed evidence.
At `216682ba` the fault was a `RuntimeError`, was not caught there, and reached the drain →
`KILLED`, ARM refused. **At `dffbaf41`, `engine.arm()` succeeds after schema-admitted corruption** —
the first defect in this programme that fails **open**. Both flagships found it independently.

## What round 4 changed

`orders.py` gains **12 lines**: an `except DurableRowFault` branch placed *ahead* of each pre-existing
`ValueError` tuple at the five ingest sites, routing to `_contain_durable_row_fault`; plus a
`except DurableRowFault: raise` guard in `_has_live_entry_remainder_exact` so its fault reaches the
caller's containment instead of being converted to `LotQuantizationError`. Everything else is tests.

## Round-4 specific checks

1. **Ordinary faults must be untouched.** The whole risk of this fix is over-correction. A genuine
   `InvalidOperation` / `TypeError` / `ValueError` / `OverflowError` / `LotQuantizationError` from any
   source that is *not* a durable-row fault must still produce `FILL_QUANTITY_INTEGRITY`, leave
   `kill_latched` false, and write `DISARMED`. **Killing on an ordinary conversion error would be a
   new fail-closed-too-hard defect** — a bridge that will not start after a benign broker quirk.
   Verify this by construction, not only by the parametrized test.
2. **Is the handler enumeration actually complete?** Round 3 shipped this defect because its
   completeness proof walked the `Store` call graph and never entered `OrderManager`. The round-4
   prompt pinned the boundary as *every* `except` in `orders.py` that can catch a `ValueError` —
   named, in a tuple, as `Exception`, or bare — on any path reachable from either drain or a direct
   `_ingest_fill` caller. **Re-derive that set yourself and compare it to the implementer's.** A site
   present in yours and absent from theirs is a required finding.
3. **`_canonical_status`'s broad `except Exception: return str(raw_status)`.** The implementer claims
   it cannot swallow a durable-row fault because the registered reads (`order["filled_qty"]`,
   `order["qty"]`) happen *before* the `try`. Check that directly — a fallback that silently returns a
   raw status string on a corruption would be the same class of downgrade as R-1.
4. **`_has_live_entry_remainder_exact` re-raise chain.** Its `except DurableRowFault: raise` relies on
   the caller's containment at the `live_entry_remainder` site. Confirm the fault actually lands
   there and is not caught by an intermediate handler on the way.
5. **Test integrity, and whether the tests can fail.** The diff removes 10 lines under `tests/`. The
   Lead read each in context and judged them strengthening or justified: the matrix's loose
   `row["code"] == reason_code or reason_code in str(row["detail"])` became an exact `reason_code in
   event_codes` plus `"FILL_QUANTITY_INTEGRITY" not in event_codes` plus a direct
   `kill_latched is True`; the `_synced_fills` assertion became conditional only because the
   `orders.trade_id` case now queues an `OrderUpdateEvent`; the fixture gained a
   `target_schema_version` parameter with the default preserved. **Verify that independently.**
6. **The falsification is the point of this round.** Two prior matrices in this cycle passed while
   proving nothing — one masked a defect with `UPDATE trades SET entry_px=100.0`, the other used a
   fixture that starts already `KILLED` so the assertion restated the fixture. The Lead re-ran the two
   new corruption cases against `dffbaf41` in an isolated worktree and observed
   `Failed: DID NOT RAISE <class 'RuntimeError'>` for both, with the 5 ordinary-fault cases passing.
   **Confirm the new clean-fixture case genuinely starts ARMED, un-latched, with no
   `kill_request_active`, and that `app_state == "KILLED"` is therefore a real assertion.**
7. **Next neighbour, one last time.** Both flagships previously found no unrouted durable read on the
   queued-event reachable set. Confirm round 4 did not create one.
