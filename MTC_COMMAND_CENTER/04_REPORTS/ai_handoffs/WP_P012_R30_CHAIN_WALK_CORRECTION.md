# Correction — "four chains, zero breaks" conflated *no contradiction* with *verified*

Issued 2026-09-09 by the Lead (Claude Opus 5, session `tradingview-lab-clean-c1`) against its own
earlier statements. Additive; the documents corrected are on `master` and are **not** rewritten.

## What was claimed

`WP_P012_R30_REPAIR5_VERIFICATION_REPORT.md` §5 and `WP_P012_R30_LEAD_ACCEPTANCE.md` §2 both report
four identity chain walks with **zero breaks**, and the acceptance document uses that as part of its
evidence. The same claim was made verbally to the owner several times on 2026-09-09.

## What is actually true

The Lead's chain-walk script skipped any transition where **either** side was absent:

```python
breaks = [i for i in range(len(e) - 1)
          if e[i].get(new_key) is not None
          and e[i + 1].get(old_key) is not None      # <-- silently skips absent fields
          and e[i][new_key] != e[i + 1][old_key]]
```

So a transition whose predecessor field does not exist was counted as passing rather than as
unexamined. Re-measured, separating the two:

| chain | transitions | verified | **unverifiable** | contradictions |
|---|---|---|---|---|
| `manifest.reseal_history` | 31 | 31 | 0 | 0 |
| `anchor.reseal_history` | 27 | 27 | 0 | 0 |
| `anchor.base_repin_history` (base commit) | 15 | 15 | 0 | 0 |
| **`anchor.base_repin_history` (core tree)** | 15 | **11** | **4** | 0 |

`anchor.base_repin_history` entries **1 through 4 have no `old_core_tree_oid_at_base` field at all**,
so core-tree transitions `0→1`, `1→2`, `2→3` and `3→4` cannot be checked in either direction. Entry 0
lacking it is expected — it is the genesis entry.

**The claim was not false.** There are no contradictions on any of the four chains, and the core-tree
chain links correctly from entry 4 through entry 15, ending at `9a3283ae…`, which matches the live
`anchor.core_tree_oid_at_base`. What was wrong is the word *verified*: four transitions were reported
as passing when nothing had examined them.

## How it was found

**Not by the Lead.** The fail-closed declared-field validator built on
`feature/p012-declared-field-validator-20260909` refuses at HEAD with
`RESEAL_CHAIN_CONTINUOUS anchor.base_repin_history.core_tree.0->1 … old_core_tree_oid_at_base=None`
and three more like it. The Lead then reproduced the gap directly from the artifact.

That is the validator earning its keep on its first run: its first four findings are a blind spot in
the Lead's own verification, in a claim that had already been put to the owner and written into an
acceptance document.

## Why it is the same defect family

This cycle's ten findings share one shape — **a check that did not run, reported as a check that
passed**. So does this. A chain walk that skips absent fields reports "zero breaks" for a chain it
never fully traversed, exactly as `verify_bceg.py` reports `475 passed` for a suite of 476 with one
permanent skip, and exactly as an aborted gate pipeline once reported "two known problems" while
twelve checks had never executed.

## Impact

**Low for the artifact, and it changes no verdict.** Zero contradictions were found on any chain, the
core-tree chain terminates at the correct live value, and nothing in re-seal #30's seal, design pin,
receipt identities or gate result depends on the four unverifiable transitions.

**Not low for the claim.** "Zero breaks across four chains" was carried into an acceptance document
as evidence. The accurate statement is: **three chains fully verified; the fourth has 11 of 15
transitions verified and 4 unverifiable because the record does not carry the predecessor field.**

## Not fixed here

Whether `anchor.base_repin_history` entries 1–4 *should* carry `old_core_tree_oid_at_base` is a
question about the artifact, not about the walk. Backfilling those fields would mean writing values
into dated historical entries, which is the F6 defect this cycle already repaired once. **Left open
deliberately**, and recorded for the owner.
