# KICKOFF — Codex: SELF_QA prose-vs-transcript claim audit — RP7 ONLY

You are Codex, ANALYST. Working dir `C:\LAB\Tradingview_LAB_CLEAN`. No host, no network, no
commit, no block-byte edits. Write exactly ONE new file:
`MTC_COMMAND_CENTER/11_TRIAGE/WPI_SELFQA_CLAIM_AUDIT_RP7_2026-08-12.md`.
Never git checkout/reset/stash.

**Scope is ONE document:** `WPI_BLOCKS_DRAFT/SELF_QA_RP7.md` (368 KB). Do **not** read
`SELF_QA_RP6.md`, `SELF_QA_TRANSPORT.md` or `SELF_QA_PATHSCOPE.md` — the other three have their
own lanes, and staying in scope is what makes this lane completable. A four-document attempt
timed out earlier today.

## Why
The same audit run against transport and pathscope
(`WPI_SELFQA_CLAIM_AUDIT_TRANSPORT_PATHSCOPE_2026-08-12.md`) found **3 false and 3 unsupported**
claims — prose contradicted by the document's own pasted transcripts, including a cleanup the
evidence shows failed and a count that was off by one. RP7 has not been checked this way, and
tonight's second-flagship auditor will read it as ground truth.

## What to check, prose against the transcript in the same document
1. **Counts.** Every "N cases", "N/N pass", "N mutants killed", "N unchanged" claim — does the
   pasted transcript show that number?
2. **Scope words.** `all`, `every`, `no`, `none`, `unchanged`. Is the scope named the scope the
   evidence covers? The known instance elsewhere had a correct measurement and a claim broader
   than it.
3. **Tense and status.** Prose saying something "is closed" or "was verified" — is the supporting
   transcript here, does it point elsewhere (fine if stated), or is it absent (a finding)?
4. **Numbers that are not measurements.** RP6's `dynamic_targets=0` was a hardcoded literal
   formatted to look measured. Sweep the published output lines for constants presented as
   results. **Report how many output lines you checked**, not only the hits.

## RP7-specific things worth targeting
Round 9's central claim is that the status body is bound by DESCRIPTOR end to end and that
`wpi_alloc_leaf` is deleted. Check that the prose describing that repair matches what the pasted
transcripts actually show, and that any "no remaining name-addressed leaf" style absolute is
supported rather than asserted.

## Rules
- Every finding carries `file:line` for **both** the prose claim and the transcript line, or says
  plainly that no transcript line exists.
- Classify **false** / **unsupported** / **scope-wrong**.
- **Do not run the harness.** Documentary consistency only, against already-pasted transcripts.
- Do not edit anything. Report; the Lead edits.
- **A clean document is a useful result** — say so plainly if that is what you find.
- State which sections you covered. If you cannot cover a section, say which and why — **do not
  imply coverage you did not achieve.**

Print: sections covered, findings by class, output lines checked, and the most consequential
finding.
