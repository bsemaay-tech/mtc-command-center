# KICKOFF — Codex: independently re-derive the D026 map's counts

You are Codex, ANALYST. Working dir `C:\LAB\Tradingview_LAB_CLEAN`. No host, no network, no
commit, no block-byte edits. Write exactly ONE new file:
`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_D026_MAP_COUNT_RECHECK_2026-08-12.md`.
Do not edit the map itself or any other file. Never git checkout/reset/stash.

## Why
`AUDIT2_D026_MAP_CURRENT_CYCLE_2026-08-12.md` closes Audit-2 packet 7 and its numbers are now
quoted in the handoff package changelog, the blocker map and the acceptance matrix:

- 39 closure/evidence rows mapped
- 28 fully closed with located RED + GREEN on the stated final bytes
- 11 unlocated/supplemental evidence flags (with one deliberate overlap)
- 15 disclosed residuals with no closure test by design
- open current-audit findings: **0** (after RP6-11 was resolved by round 17)

**Those counts came from a single lane and nobody has re-derived them.** A count that is wrong in
the direction of "more closed than reality" is exactly the failure mode this project keeps
finding, and today produced a live example: RP6's `dynamic_targets=0` was a hardcoded literal
presented as a measurement.

## What to do
1. **Re-derive every count from the map's own rows.** Do not trust the summary block; count the
   table rows yourself and classify each independently. Report your number beside the map's for
   each of the five categories.
2. **Check the classifications, not just the arithmetic.** For each row the map calls "fully
   closed", confirm the map actually cites a located RED *and* a located GREEN *and* names the
   bytes the GREEN was measured on. A row missing any of the three is not fully closed, whatever
   the summary says.
3. **Check the overlap statement.** The map says the eleventh unlocated flag is the same RP6-11
   row already counted OPEN, "so the numbers are not falsely additive". Verify that is the only
   overlap and that no other row is double-counted across categories.
4. **Check the residual count against the source STATUS files** (RP6 1, RP7 2, transport 1,
   SEC102 4, pathscope 7 = 15). SEC102 in particular now carries four owner-accepted trusted-base
   assumptions plus one GLM nit — confirm whether the map's "4" is still right after that, and
   say so either way.
5. **Check the post-r17 state.** The map was written before RP6 round 17 and then edited to
   record the resolution. Confirm the RP6 rows and the "open findings = 0" claim are consistent
   with the r17 bytes now in the repo.

## Rules
- Every disagreement carries a `file:line` and the corrected number.
- If the counts are right, say so plainly — a confirmation is a useful result.
- Do not fix the map. Report; the Lead edits.

Print a comparison table of map-count versus your-count for all five categories, and the total
number of rows whose classification you disagree with.
