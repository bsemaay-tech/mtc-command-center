---

# ROUND-3 ADDENDUM — read this together with the Gate-5 brief above

**Frozen SHA for this round: `dffbaf41`.** Whole-cycle delta: `git diff 732b37c3..dffbaf41`.
Round-3 repair only: `git diff 216682ba..dffbaf41`.

Floor at `dffbaf41`: **`2 failed, 1297 passed`** — still only the two pre-existing failures named in
the brief. A third failure is a required finding.

**This is the last repairable round.** Two of three non-accepting rounds are spent. If this round
does not draw an accepting verdict from both flagships, the Lead reports a failed cycle to the owner
rather than opening a fourth round. That raises the cost of a *wrong* required finding as much as the
cost of a missed one — state findings you can defend, and mark anything speculative as a nit.

## Cycle history — what each round closed and what it opened

| Round | SHA | Closed | Opened |
|---|---|---|---|
| 1 | `34d35286` | the whole class-A/B/C surface via one registry-driven boundary | R-1: S3T-B's own raise escaped through an empty `missing_identity` |
| 2 | `216682ba` | that escape, at the root — named binding faults | R-1: nullable-by-design NULL treated as corruption · R-2: fault type escaped an existing conversion contract · R-3: `DEFERRED` reachable and escaping |
| 3 | `dffbaf41` | all three | *your job* |

**Settled, and not to be re-opened** unless you find something concrete and reachable: the boundary
design itself (one `DurableRowAccessor` / `DURABLE_EVENT_ROWS` over a declared registry, routed by
returning typed rows from the store), both matrices generating from declared registries, the class-C
join as a conjunct with the epoch fence intact, and round 2's `expected_identity` binding-fault
naming. Both flagships already judged this **not** a fourth point fix.

## What round 3 changed

1. **Nullability is now part of the registry contract.** `DURABLE_EVENT_COLUMN_TYPES` maps to
   `DurableColumnContract(value_type, nullable)`. `orders.trade_id` and `trades.entry_px` are
   declared nullable; the other eight reject NULL. The corruption matrix branches on the contract and
   asserts the **accepting** case for nullable columns, not only the fault case.
2. **`DurableRowFault` now subclasses `ValueError`** instead of `RuntimeError`, so conversion-fault
   contracts that already existed catch it without every caller being edited. Affected callers were
   enumerated from the `Store` call graph; a generated check asserts both public closure entrypoints
   answer with `KillConflictError` and never a bare fault.
3. **The close-veto handler no longer re-raises on `DEFERRED`** — it returns
   `disposition == _KILL_LIFECYCLE_CONSUMED`, symmetric with its sibling. The `group_id`/active-epoch
   invariant was added as defence in depth, and the stale-episode and ABA-restoration cases are
   generated rather than argued.
4. The masking `UPDATE trades SET entry_px=100.0` was removed from the corruption matrix.

## Round-3 specific checks — in addition to every check in the brief

1. **Nullability declarations must be derived, not convenient.** For **each** of the ten registered
   columns, check the declaration against what actually writes it. `orders.trade_id` and
   `trades.entry_px` are claimed nullable-by-design; the other eight are claimed always-written. **A
   column wrongly declared nullable silently downgrades a real corruption to an accepted value** —
   that is strictly worse than R-1 was, because it fails *open* rather than closed. This is the
   highest-value check in this audit.
2. **Does nullable-at-the-boundary leak into identity requirements?** A NULL `orders.trade_id` is now
   accepted by the accessor. Confirm it is still treated as a missing kill-lifecycle identity and
   still quarantines — nullability and identity must stay separate concerns.
3. **The `ValueError` subclass change is wide-blast-radius. Hunt what it now silently swallows.**
   Every pre-existing `except ValueError` / `except (… ValueError …)` on any path that can reach a
   boundary-routed read now catches `DurableRowFault`. Some of those handlers convert to
   `KillConflictError`, which is the intent. **Find any that instead continue, substitute a default,
   or return a fallback value** — there a real corruption is now absorbed silently where it
   previously propagated and failed closed. Consider `_canonical_status`'s broad fallback in
   particular.
4. **`DEFERRED` containment.** Confirm no `KillConflictError` can leave `_ingest_fill` on the
   close-veto path, and that the direct callers at `orders.py:1302` / `:1683` translate `False` into
   their existing `UNKNOWN` outcomes without losing evidence.
5. **Test integrity — check this one by reading, not by trusting.** The round-3 diff removes 21 lines
   under `tests/`, including four assertions from the corruption matrix. The Lead's reading is that
   every one is re-added inside the new nullable/fault branches, with the fault branch keeping the
   originals verbatim, so the net is strictly stronger. **Verify that independently.** If any
   assertion was dropped rather than moved, that is a required finding.
6. **Keep hunting the next neighbour.** Three rounds, three times defeated by a site nobody had named.
