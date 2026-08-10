# KICKOFF — GLM independent verification of the round-1.4 catalogue pass (read-only)

You are GLM-5.2, acting as the independent second auditor. Codex (the implementer of this
round) applied the ten-pattern defect catalogue to the accepted WP-I preregistration draft
and claims: `CATALOGUE-PASS-COMPLETE: 17 findings repaired, 0 patterns clean`.

You must verify that claim adversarially. Codex implemented; you audit. Do not repair
anything — report only.

Read exactly these three files (relative to `MTC_COMMAND_CENTER/11_TRIAGE/`):

1. `DESIGN_DEFECT_PATTERNS_2026-08-10.md` — the catalogue (10 patterns).
2. `WPI_PREREG_DRAFT_ROUND1/WPI_PREREGISTRATION_DRAFT.md` — the repaired draft (round 1.4).
3. `WPI_PREREG_DRAFT_ROUND1/WPI_CATALOGUE_PASS_CODEX_2026-08-10.md` — Codex's report.

Verify:

- **V1** Each of the 17 reported repairs is actually present in the draft text at the
  claimed location, and does what the report claims.
- **V2** No repair weakened any check: the STOP-vs-FAIL contract holds everywhere
  (inability to evaluate is STOP, never FAIL; a check that cannot fail proves nothing).
- **V3** The `<PIN-BEFORE-DISPATCH>` placeholders for `WPI_UNIT_FRAGMENT_SHA256` and
  `WPI_LOG_DIR` are untouched, and the draft's read-only scope and authority claims are
  unchanged.
- **V4** No regression of the earlier round 1.1–1.3 fixes (GLM F1 interpreter-exec STOP;
  Codex F1 metadata-readability precedence; Codex F2 netns binding; F3/F4 system-manager
  access STOPs).
- **V5** Sample-attack at least three repaired rows with the catalogue's own falsification
  style: describe a concrete host state that would slip through if the repair were
  cosmetic. State whether the repaired text actually stops it.
- **V6** The report's per-pattern coverage claim: for each of the 10 patterns, confirm the
  report lists at least one finding or a credible no-instance justification (Codex claims
  0 patterns clean, i.e. all 10 had instances — check that is consistent).

Output format: verdict line first — `VERIFIED-CLOSED` or `FINDINGS: <n>` — then one row
per V-item with PASS/FAIL and one-line evidence, then any findings with location + defect
+ minimal fix. Plain text. Do not modify any file.
