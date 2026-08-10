# KICKOFF — RP6-P0.sh bounded repair (F1, F3, F4) + SELF_QA_RP6.md

Dispatched by the Claude Lead, 2026-08-10. Sequencing authorized by owner grant #5:
WP-I direction is settled (draft round 1.4, catalogue-pass VERIFIED-CLOSED by GLM at
commit `6a8b0896`), so the RP6-P0 repair proceeds now.

**The repository's two-tier counterpart-implementer rule is suspended by owner amendment
A2/A2a. Implement this yourself. Do not sub-delegate to Claude Max or any other agent.**

## Inputs (all relative to `MTC_COMMAND_CENTER/11_TRIAGE/`)

1. `WPI_BLOCKS_DRAFT/RP6-P0.sh` — the partial block (repair target).
2. `WPI_BLOCKS_DRAFT/RP6_P0_GLM_AUDIT_2026-08-10.md` — the audit (F1–F4).
3. `WPI_BLOCKS_DRAFT/LEAD_ADJUDICATION_RP6_2026-08-10.md` — binding scope: F2 closed
   (polarity correct as written), draft-side Pattern 8 already repaired in round 1.4.
4. `WPI_PREREG_DRAFT_ROUND1/WPI_PREREGISTRATION_DRAFT.md` — round 1.4, the current
   binding specification (section 8.1 P0 rows are now numeric-identity; the block's
   numeric-only approach is the accepted contract).
5. `DESIGN_DEFECT_PATTERNS_2026-08-10.md` — binding pre-read before touching the block.

Do not read handoff files or GATE_A_A* files.

## Repair scope — exactly these, nothing else

- **F1 [MEDIUM]** — the false child-execution claim at lines 59-62 and the
  `children=2_readonly_cleared_env` token at line 861. The block runs ~20+ children;
  only the two `env -i` launches are cleared-env. State the surface honestly or drop
  the token. Note draft round 1.4 now carries a binding probe execution-environment
  rule (catalogue Pattern 4): prefer aligning the block's real child-launch discipline
  with that rule (fixed cwd, LC_ALL=C, pinned PATH/absolute helpers, run-owned TMPDIR)
  over merely weakening the claim — but do NOT expand the block's scope.
- **F3 [LOW]** — canonicalize the components of `$P0_VENV_ROOT/bin/python` or disclose
  the intermediate-symlink residual in the `does_not_establish` line (round 1.4 row 18
  requires any accepted symlink's resolved target to be preregistered — check which
  branch fits the block's role and say why in the QA).
- **F4 [LOW]** — add the `:?` fail-closed backstops behind the rc-3 input pre-checks,
  matching the accepted block's defence in depth.

Preserve everywhere: STOP-vs-FAIL truthfulness (inability to evaluate is STOP, never
FAIL), rc 0/1/3 contract, numeric-identity rule, read-only scope (no host mutation, no
file content printed).

## Deliverables

1. Repaired `WPI_BLOCKS_DRAFT/RP6-P0.sh`.
2. `WPI_BLOCKS_DRAFT/SELF_QA_RP6.md` — per draft round 1.4 acceptance rules (C16):
   exact paste-and-run commands with REAL captured RED output against the pre-fix
   bytes (or a deliberate mutation) and GREEN output with the repaired bytes, for each
   of F1/F3/F4. Run them locally (Git Bash / MSYS is available); no host contact, no
   ssh, no network. If an environment limit makes a specific check unrunnable locally,
   record that as an explicit documented limit — never fake output.
3. Update `WPI_BLOCKS_DRAFT/STATUS_RP6_P0.md`: PARTIAL → REPAIRED-PENDING-AUDIT with
   one line per finding disposition.

Touch ONLY those three files. Do not commit — the Lead verifies, routes the GLM
re-audit, and commits.
