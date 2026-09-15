# Correction to acceptance evidence — the heading map was not wrong

**Author:** Lead (claude-opus-5) · **Date:** 2026-09-10
**Corrects:** `WP_P012_R30_LEAD_ACCEPTANCE.md` §5, line 87
**Method:** additive. The corrected document is **not rewritten**, for the same reason its own §5 gives
for not rewriting historical values.

This is the **second** additive correction to that acceptance document. The first is
`WP_P012_R30_CHAIN_WALK_CORRECTION.md`, which corrected "four chains, zero breaks".

---

## The claim, as it stands in acceptance evidence

> `heading_line_map_measured_at_reseal17` 8 of 26 entries wrong

Listed there as one of the open declared-but-unchecked defects.

## It is false

Measured against `C:\tmp\LANE_PROMPTS_20260828\P012_FRESH_DESIGN_V1.md` at `d64d8fce`:

| | count |
|---|---|
| entries whose declared line number is **exact today** | 18 of 26 |
| entries that **drifted** | 8 of 26 |
| drift magnitude | **+1 or +3**, never negative |
| headings that no longer exist | **0** |

Drift increases monotonically with position in the file. That is the signature of **content inserted
above**, not of a wrong measurement.

**The field is a dated snapshot and says so in its own name** — `measured_at_reseal17`. The design
block records every later addition in *sibling* keys
(`heading_line_map_addition_measured_at_reseal25`, `…26`, `…28`, `…30`) instead of rewriting the base
map, so the record is deliberately **append-only** and its base entries are *expected* to drift as the
design grows. **The 26 declared values were correct at re-seal 17, which is what they claim to be.**

## Where the false claim came from

`gpt-5.6-sol` reported it in its round-5 audit. I carried it into the acceptance document **without
measuring it**, and then built a validator check (`HEADING_MAP_ACCURATE`) on the same premise, which
produced **8 false refusals** on its first run. Fixed in `fc924648`; the check is now
`HEADING_MAP_HISTORICAL_CONSISTENT` and tests the invariants that are sound for a snapshot — every
declared heading still exists, and drift is never negative.

**Two independent actors made the same category error**, which is why it survived: neither of us
compared the field's *name* against what we were measuring it for.

## Why this correction matters more than the number

Had the claim been acted on as written, the repair would have been to **update those 8 entries to
today's line numbers** — overwriting a dated historical measurement with current values. That is
precisely the defect repaired in `2f1008ab` earlier in this same cycle. **A false "wrong" verdict on a
historical record invites a repair that destroys the record.**

## The two adjacent claims in the same list, re-measured

Since one line in that list was wrong, I measured the others rather than leaving them on my earlier
word.

| claim in `WP_P012_R30_LEAD_ACCEPTANCE.md` §5 | verdict |
|---|---|
| `section_16_review.status` still `PENDING` | **correct**, and detailed in `WP_P012_R30_REPAIR6_PATCH_PLAN.md` §2 |
| `repository_evidence_identity` a stale snapshot | **correct** — all three values differ from live git; §4 of the same plan |
| `heading_line_map_measured_at_reseal17` 8 of 26 entries wrong | **FALSE — this correction** |
| `expected_value_provenance.statement` says 1194 paths where the tree holds 1195 | **was correct when written; now dated.** The tree holds **1198** at `d64d8fce`. The count drifted twice in one night from ordinary commits, which is the argument for **removing** it rather than re-pinning it |
| `legacy_event_order_map_pin.baseline_manifest` six re-seals stale | **correct** — the pin records re-seal **#24**, the current seal is re-seal **#30** |

So of five listed items: three correct, one correct-but-now-dated, one false.

## Effect on the verdict

**None.** All five fields are read by zero gate code, the seal is unchanged at `b6ac5a46…`, and the
gate re-measured at `d64d8fce` reports `acceptance_blockers: 0` with
`expected_source_provenance.status: MATCH`. The acceptance this document corrects stands; one of its
listed open defects is not a defect, which makes the remaining list **shorter**, not longer.

## What it says about the method

The chain-walk correction was a check that did not run being reported as a check that passed. **This
one is different: a finding I inherited from another reviewer and repeated without measuring.** The
first failure mode is caught by re-reading your own scripts. This one is only caught by measuring
someone else's claim before adopting it — and I did not, until building a tool on top of it forced the
measurement.
