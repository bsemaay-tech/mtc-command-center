# AUDIT KICKOFF — round 4 closure audit (Codex, narrow, owner-authorized round)

The owner authorized one bounded round beyond the original 3-round budget, scoped to
exactly the two audit-3 survivors. This audit is correspondingly narrow.

## Scope — read ONLY

- `audit3/AUDIT3_REPORT.md` (your two surviving findings), `ROUND4_KICKOFF_PREPARED_NOT_DISPATCHED.md`
  (the bounded scope), `round4/` (under audit), `round3/` (baseline).

## Audit questions

1. **Finding 1 closure**: does the empty-nonzero-read/zero-records arm now STOP in
   BOTH blocks? Re-run your directory-as-mounts-source fixture against round4 code
   and report actual rc/output. Also re-run the populated unterminated-final-record
   fixture to confirm it still STOPs. Evaluate the honesty of the stated mid-table
   read-error limitation (bash read cannot distinguish it from EOF after ≥1 record):
   is the limitation real, correctly scoped, and disclosed rather than hidden?
2. **Finding 2 closure**: are exact executable RED and GREEN commands + real output
   now present for every item 1–6 closure test, including the new read-error arm?
   Is the corrected subcount arithmetic exact? Sample at least 3 commands by
   reproducing them.
3. **Regression sweep**: diff round3 → round4. The only admissible deltas are the two
   fixes and their documentation. Anything else, or anything audit 3 verified CLOSED
   now weakened, is a REQUIRED finding.

## Output

`audit4/AUDIT4_REPORT.md`, verdict first: **PASS / PASS-WITH-NITS / BLOCK** (BLOCK
escalates to the owner; there is no round 5). Findings ranked, concrete failure
scenarios required. English, ASCII only.
