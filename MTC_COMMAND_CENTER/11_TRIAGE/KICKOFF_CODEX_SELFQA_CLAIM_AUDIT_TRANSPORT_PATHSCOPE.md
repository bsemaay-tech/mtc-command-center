# KICKOFF — Codex: SELF_QA prose-vs-transcript claim audit — TRANSPORT and PATHSCOPE only

You are Codex, ANALYST. Working dir `C:\LAB\Tradingview_LAB_CLEAN`. No host, no network, no
commit, no block-byte edits. Write exactly ONE new file:
`MTC_COMMAND_CENTER/11_TRIAGE/WPI_SELFQA_CLAIM_AUDIT_TRANSPORT_PATHSCOPE_2026-08-12.md`.
Do not edit any audited document. Never git checkout/reset/stash.

**Scope is deliberately two documents, not four.** A GLM attempt at all four died on an API
timeout — `SELF_QA_RP6.md` alone is 1.0 MB and `SELF_QA_RP7.md` is 368 KB. This lane takes the
two smaller ones (`WPI_BLOCKS_DRAFT/SELF_QA_TRANSPORT.md`, 194 KB, and
`WPI_PREREG_DRAFT_ROUND1/SELF_QA_PATHSCOPE.md`, 109 KB). RP6 and RP7 get their own lanes.
**Do not read RP6 or RP7 here** — staying inside the scope is what makes this lane complete.

## Why this exists
The round-6 transport audit caught a **false byte-identity claim**: the self-QA asserted the
nine-file set was unchanged when two of those nine had in fact moved. Measurement right, scope
wrong. It survived until an auditor happened to check it. Nobody has systematically checked
whether these documents' prose matches their own pasted transcripts, and tonight's
second-flagship auditors will read them as ground truth.

**Transport is the highest-prior-probability document** — it is where the known instance lived,
so look for siblings of it there first.

## What to check, prose against the transcript in the same document

1. **Counts.** Every "N cases", "N/N pass", "N mutants killed", "N files unchanged" claim in
   prose — does the pasted transcript actually show that number?
2. **Scope words.** `all`, `every`, `no`, `none`, `unchanged`. This is where the known defect
   lived. For each, is the scope named the scope the evidence actually covers? Check especially
   any claim covering a *set* of files, where some members may be documents that legitimately
   change.
3. **Tense and status.** Prose saying a thing "is closed" or "was verified" — is the supporting
   transcript in the same document, does it point elsewhere (fine, if it says so), or is it
   absent (a finding)?
4. **Numbers that are not measurements.** RP6's `dynamic_targets=0` was a hardcoded literal
   formatted to look measured. Sweep each document's published output lines for constants
   presented as results. **Report the number of output lines you checked**, not just the hits.

## Rules
- Every finding carries `file:line` for **both** the prose claim and the transcript line, or
  states plainly that no transcript line exists.
- Classify each as **false** (contradicted by the document's own evidence), **unsupported** (no
  evidence either way), or **scope-wrong** (measurement correct, claim broader than the
  measurement).
- **Do not run the harnesses.** This is a documentary consistency audit against already-pasted
  transcripts.
- Do not edit anything. Report; the Lead edits.
- **A clean document is a useful result.** Say so plainly if that is what you find.
- State which sections of each document you covered. If you could not cover a section, say which
  and why — **do not imply coverage you did not achieve.**

Print: sections covered per document, findings by class, output lines checked for
non-measurements, and the single most consequential finding.
