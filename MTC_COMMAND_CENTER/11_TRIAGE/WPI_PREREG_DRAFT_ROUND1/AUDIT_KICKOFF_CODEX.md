# AUDIT KICKOFF — WP-I preregistration draft, adversarial pass (Codex)

Authorized private-repo test-infrastructure review. Refute, do not confirm. This is a
DRAFT preregistration for a future read-only staging-verification unit; nothing here
has been executed and no host has been contacted. Documentation review only — local
fixtures allowed, no remote host contact, no git mutation.

Two other agents already touched this document (a counterpart implementer wrote it, a
reviewer passed one round). You are the independent third pass; do not defer to either.

## Scope — read ONLY

- `WPI_PREREGISTRATION_DRAFT.md`, `WPI_CHECK_FEASIBILITY.tsv`, `SELF_QA.md` (this
  directory) — the artifacts under audit.
- `../WPI_DRAFT_GLM_REVIEW_2026-08-09.md` — the prior review, so you do not repeat it.
- `../WPL_P2_STAGING_WPLP2-20260809T125940Z-8dc78f08/02_PREREG/PREREGISTRATION.md` —
  the accepted rigor template this draft must match.
- `../WPL_P2_STAGING_WPLP2-20260809T125940Z-8dc78f08/03_TRANSPORT/B3_STOP_ADJUDICATION.md`
  — the governing lesson (an accepted check assumed privileges the execution model did
  not have, and STOPped on first host contact).

## Audit questions

1. **Unprivileged feasibility, attacked.** For every check the TSV marks
   INCLUDE-READ-ONLY, construct a concrete host state in which the check cannot be
   evaluated by unprivileged `gatea` (permissions, ACLs, missing tool, SELinux/AppArmor,
   namespace, mount, missing execute bit, absent metadata). If such a state exists AND
   the draft's expectation table would render it as a FAIL rather than a STOP, that is a
   REQUIRED finding — it is the exact defect class that stopped B3.
2. **Expectation table soundness.** For each row, is the "exact predicted first
   divergence" actually the FIRST thing that diverges, or does an earlier probe in the
   same block fail first? Name any row whose predicted divergence is unreachable.
3. **Template parity and immutability.** Anything load-bearing in the accepted template
   that this draft weakens, omits, or states more loosely — especially: one-use RUNID
   burn rule, create-once, first-FAIL, three-outcome rc discipline, evidence closed by a
   separate invocation, remote-vs-local binding, and the immutability/void conditions.
4. **Placeholder and authority discipline.** Confirm no concrete one-use RUNID or
   colliding record root is minted, and that no Group C (mutating) check has any
   executable form. Flag anything that reads as authorization rather than as a plan.

## Output

Write exactly one file: `AUDIT_REPORT_CODEX.md` in this directory. Verdict first —
PASS / PASS-WITH-NITS / REQUEST_CHANGES / BLOCK — then findings ranked most severe
first, each with file+line, a concrete failure scenario (the host state that makes it
wrong), and the minimal fix. Then the four answers in order. A finding without a
concrete failure scenario is a nit; label it so. English, ASCII only.
