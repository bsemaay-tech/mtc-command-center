# Governance stage verification

Read before writes/execution. Verify consequences, not document length or generated confidence.

- State one completion example and independently derived expected result before implementation.
  Exercise the relevant working path; record observed outcome, limitation and remaining gap.
- Publish exact repeatable command, cwd, runtime/version and required environment without secrets.
  Preserve actual exit code, output and source identity. Failed published command/environment is
  FAILED or BLOCKED, never PASS. Do not replace the real artifact with extraction/simulation.
- For executable gate/evidence artifacts, before flagship dispatch someone other than the author
  executes the published QA command VERBATIM: happy path and a meaningful RED/mutant arm.
  For defect closure/safety, real RED on exact pre-fix behavior or an equivalent mutation, then
  GREEN with the fix, remains required. Expected results come from an independent contract or
  counterfactual, never implementation output alone. Unproved closure evidence is supplemental.
  Ordinary prose/cosmetic edits need relevant content/link/visual checks, not artificial mutants.
- Each Gate-5 auditor states which new tests' RED/GREEN evidence they reproduced and what remains
  unverified. Changing a carried regression fence requires old/new assertions executed against
  the same deviant output; silently weakening it is BLOCK-class. Establish old behavior by execution.
- Check actual encoding, clock domain, hashes, sizes and identity where relevant. With text
  normalization state byte forms or pin Git blob OID. Verify links; search corrected claims in
  current consumers, identifying frozen/historical matches without rewriting accepted evidence.
- For generated status/index outputs, verify deterministic regeneration when generation is the
  task. Reuse valid frozen suite/security evidence per `REVIEW_POLICY.md`; rerun for changed source,
  environment or unresolved concerns, not an identical new review label.
- Before a commit inspect actual diff and exact staged paths, run scoped checks and normal repo
  guard/hooks. Preserve foreign edits. Master acceptance still requires the exact protected
  `Bridge suite (Python 3.12)` on an up-to-date head; local checks do not replace it.
- Commands over the 600-second foreground ceiling use a background supervisor. One overnight
  loop only; unattended multi-hour work requires verified AC/DC sleep/hibernate disabled.
  Autonomous turns retain active delegated work or an explicit wake condition; route preflight
  and labelled partial state follow `AUTONOMY_AUTHORIZATION.md`.
