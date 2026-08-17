# KICKOFF — GLM-5.2: audit the SELF_QA documents' own claims against their own transcripts

You are GLM-5.2 via the Z.AI route. **You are running UNATTENDED — do not ask for approval, do
not write a plan and stop. Execute directly and write your verdict file.** Working dir
`C:\LAB\Tradingview_LAB_CLEAN`. Read-only: create nothing except your verdict file, no git
mutation, no host, no network.

## Why this exists
The STATUS-versus-bytes sweep found the round-6 transport audit had caught a **false
byte-identity claim**: the self-QA asserted the nine-file set was unchanged when two of the nine
had in fact moved. That is a claim contradicted by the document's own evidence — and it survived
until an auditor happened to check it.

The SELF_QA documents are the largest artifacts in the package and the ones every auditor reads
as ground truth. **Nobody has systematically checked whether their prose claims match their own
pasted transcripts.** That is the gap this dispatch closes, before tonight's second-flagship
auditors treat those claims as established.

## What to audit
`WPI_BLOCKS_DRAFT/SELF_QA_RP6.md`, `SELF_QA_RP7.md`, `SELF_QA_TRANSPORT.md`, and
`WPI_PREREG_DRAFT_ROUND1/SELF_QA_PATHSCOPE.md`.

For each document, check the **prose against the transcript in the same document**:

1. **Counts.** Every "N cases", "N/N pass", "N mutants killed", "N files unchanged" style claim in
   prose — does the pasted transcript actually show that number? Report any prose figure the
   transcript does not support.
2. **Scope words.** Claims of the form "all", "every", "no", "unchanged", "none". These are where
   the transport defect lived: "the nine-file set is unchanged" was false because the scope was
   wrong, not because the measurement was. For each such claim, is the scope it names the scope
   the evidence actually covers?
3. **Tense and status.** Prose that says a thing "is closed" or "was verified" — is the supporting
   transcript in the same document, or does it point elsewhere, or is it absent? A claim whose
   evidence is elsewhere is fine if it says so; a claim that implies local evidence and has none
   is a finding.
4. **Numbers that are not measurements.** The RP6 defect found today: `dynamic_targets=0` was a
   hardcoded literal formatted to look measured. Sweep each document's published output lines for
   constants presented as results. Report the count you checked, not just the hits.

## Rules
- Every finding carries `file:line` for **both** the prose claim and the transcript line (or
  states that no transcript line exists).
- Classify each as **false** (contradicted by own evidence), **unsupported** (no evidence either
  way), or **scope-wrong** (measurement right, claim broader than the measurement).
- Do not edit any document. Report; the Lead edits.
- **A clean document is a useful result** — these are huge files and confirming they are honest
  is worth as much as finding a defect. List which documents you swept fully versus partially, so
  coverage is provable.
- If a document is too large to sweep exhaustively, say which sections you covered and which you
  did not — **do not imply full coverage you did not achieve.**
- Mark anything you could not execute `PENDING-LEAD-EXECUTION`; **never fabricate a green run.**

Write ONE new file:
`MTC_COMMAND_CENTER/11_TRIAGE/WPI_SELFQA_CLAIM_AUDIT_GLM_2026-08-12.md`.
Print: documents swept (full/partial), findings by class, output lines checked for
non-measurements, and the single most consequential finding.
