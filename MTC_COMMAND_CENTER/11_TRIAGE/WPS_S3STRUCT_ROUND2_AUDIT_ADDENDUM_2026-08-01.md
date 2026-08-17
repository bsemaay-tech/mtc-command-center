---

# ROUND-2 ADDENDUM — read this together with the Gate-5 brief above

**Frozen SHA for this round: `216682ba`.** Round delta for the whole cycle:
`git diff 732b37c3..216682ba`. Round-2 repair only: `git diff 34d35286..216682ba`.

Floor moves with the round. At `216682ba` the suite is **`2 failed, 1266 passed`** — still only the
two pre-existing failures named in the brief. A third failure is a required finding.

## What happened in round 1

Round 1 (`34d35286`) was **not accepted**. Canonical auditor `gpt-5.6-sol` xhigh returned
`REQUEST_CHANGES` with one required finding, and the Lead reproduced the whole chain on real source
before it bound. The other flagship did not run that round, so round 1 has one flagship verdict only.

Round 1's boundary work was judged sound by both that auditor and the Lead — one registry-driven
`DurableRowAccessor` over `DURABLE_EVENT_COLUMN_TYPES`, a matrix generated from that registry, the
class-C join added as a conjunct with the epoch fence intact, both legacy helpers deleted. **That is
not re-opened. Do not re-litigate it** unless you find something concrete and reachable.

**R-1, the finding:** S3T-B's own new raise opened the next neighbour.
`close_trade_once_with_decision` raised `KILL_LIFECYCLE_IDENTITY_MISSING` when the binding broke;
`_ingest_queued_event` routed that to `_defer_kill_lifecycle_event`, which re-read the mutated order
and called `_kill_lifecycle_identity`; that helper returned an **empty** `missing_identity` because a
role no longer equal to `KILL_FLATTEN` was indistinguishable from an order that was never kill-bound.
No quarantine ran, `UNBOUND` came back, the conflict was re-raised, and neither drain catches
`KillConflictError` — so `BridgeEngine.start()` did not return normally.

## What round 2 changed

`_kill_lifecycle_identity` now takes an optional `expected_identity`. Given one, a changed `role`,
`group_id` or `trade_id`, and a deleted order row, each produce a distinct named reason from
`KILL_LIFECYCLE_BINDING_FAULT_REASONS`. Given none, it returns `(None, None, ())` exactly as before.
The close conflict is contained in `_ingest_fill` where it is raised. The mutation cases are
parametrized **from that reason registry**, so adding a binding element without a mutation fails the
suite rather than quietly narrowing coverage.

## Round-2 specific checks — in addition to every check in the brief

1. **Is the repair at the root or at the drain?** Adding `except KillConflictError` to the two drains
   was explicitly forbidden: it contains the symptom and buries the missing evidence. Confirm the
   fault is *named* and *recorded*, not merely swallowed.
2. **`raise` on `DEFERRED`.** The new `_ingest_fill` handler re-raises if
   `_defer_kill_lifecycle_event` returns `DEFERRED`, which would re-open R-1. The Lead's reading is
   that this is unreachable because `record_kill_lifecycle_deferral`'s identity query is strictly
   stronger than the close path's binding predicate — it joins `kill_requests` → `orders`
   (role + `group_id` + `trade_id`) → `trades` → `fills`, so anything the close vetoes the deferral
   also rejects. **Check that reasoning.** If you can construct a state where the close vetoes and
   the deferral succeeds, `DEFERRED` becomes reachable and R-1 returns. Note also that this handler
   is asymmetric with its sibling roughly forty lines above, which returns `False` on `DEFERRED`.
3. **Evidence cardinality.** The store veto (`_record_kill_lifecycle_binding_rejection`) and the
   engine quarantine (`_quarantine_kill_lifecycle_identity`) both append identity evidence for the
   same event. The implementer flagged this himself. Is the resulting event count correct,
   deduplicated where it should be, and free of unbounded growth across repeated drains? Round 1 of
   the *previous* cycle relocated an unbounded-growth defect, so this is not a theoretical worry.
4. **Did the fix narrow anything?** `expected_identity=None` must preserve the old behaviour exactly,
   or ordinary ENTRY/SL/TP fill routing through `_ingest_fill` changes silently.
5. **Keep hunting the next neighbour.** Every round of this cycle so far was defeated by a site
   nobody had named. Two rounds of three are now spent; this is the last round that can be repaired
   before the owner has to be told the cycle failed.
