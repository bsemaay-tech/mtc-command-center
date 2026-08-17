# KICKOFF — Codex independent audit of the RP6-P0 C13 getent arm (read-only)

Dispatched by the Claude Lead, 2026-08-10. GLM implemented this arm (you did not — you
are the independent auditor for it). Audit only — modify nothing, commit nothing.

**The repository's two-tier counterpart-implementer rule is suspended by owner amendment
A2/A2a. Do the audit yourself. Do not sub-delegate.**

## Inputs (relative to `MTC_COMMAND_CENTER/11_TRIAGE/`)

1. `WPI_BLOCKS_DRAFT/RP6-P0.sh` — current bytes (claimed SHA-256
   `cfdb23b8834a783638723c54cf632973c1cc20c5fb676cb6d310a9d43b9acf1c`, 54109 B).
   The C13 arm = `p0_resolve_passwd`, `p0_resolve_accounts`, the `P0_STATE_UID`/
   `P0_STATE_GID` inputs, pinned `getent` as 12th RO tool, and the claim-line updates.
   Baseline before the arm: `6c5b8945…766f7`, 44979 B (in git history at `cbaf3ec8^`
   — diff against it to isolate the arm).
2. `WPI_BLOCKS_DRAFT/SELF_QA_RP6.md` — C13 sections: arm RED/GREEN, backstop QA with
   the Lead harness correction (as-drafted failing run retained), real outputs.
3. `WPI_BLOCKS_DRAFT/KICKOFF_GLM_RP6_GETENT_ARM.md` — the implementation contract.
4. `WPI_PREREG_DRAFT_ROUND1/WPI_PREREGISTRATION_DRAFT.md` — round 1.5 spec §8.1 rows
   1–3 (repair C13) — the binding requirement.
5. `DESIGN_DEFECT_PATTERNS_2026-08-10.md` — attack with the catalogue.

## Verify

- **V1** Diff isolation: `git diff cbaf3ec8^ -- <block>` restricted to the C13 arm +
  inputs + claim lines; every pre-existing arm byte-untouched.
- **V2** Spec conformance: rows 1–3 as written in round 1.5 — unique complete getent
  parse, gatea numeric equality (live id + prereg), mtc-bridge 999:988, valid
  no-match distinct from lookup error, names diagnostic only.
- **V3** Truthfulness: every branch of the new arm maps to the truthful class
  (Pattern 1); parser is a real passwd-grammar parser, not substring matching
  (Pattern 5); duplicate/ambiguous → unresolvable STOP.
- **V4** Execution-environment: getent pinned per inventory discipline (Pattern 4);
  the arm stays read-only.
- **V5** QA integrity: RE-RUN the C13 arm command and the corrected backstop command
  from SELF_QA_RP6.md yourself (local Git Bash; no host contact) and compare with the
  recorded outputs. Verify the Lead's harness-correction reasoning (drafted sed had no
  input; ungated summary) by inspecting the recorded as-drafted RED run.
- **V6** Hash: re-derive SHA-256 + bytes; compare to claims.

Output: write `WPI_BLOCKS_DRAFT/RP6_C13_CODEX_AUDIT_2026-08-10.md` — verdict line
first (`PASS` or `BLOCK: <n> findings`), one row per V-item with PASS/FAIL + one-line
evidence, findings most severe first. Touch ONLY that report file.
